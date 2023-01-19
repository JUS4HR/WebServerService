from argparse import ArgumentParser
from multiprocessing import Process
from os import get_terminal_size as getTerminalSize
from sys import exit as sysExit
from time import sleep as timeSleep

import Log
from Config import Config, ConfigInstance, setConfigPath
from Signal import killServer, setCallback, setupServer, signal
from Singleton import isFirstInstance
from WebApp import App

RELOAD_SIGNAL = "reload"
QUIT_SIGNAL = "quit"

configTemplate: Config = {
    "debug": (False, "Enable debug mode"),
    "webAppList": (["example"], "List of names of web apps"),
}

parser = ArgumentParser()
parser.add_argument("-n",
                    "--root-name",
                    type=str,
                    default="webServer",
                    help="The name of the main process.")
parser.add_argument("-c",
                    "--config-path",
                    default="~/.webServer",
                    help="The directory to store config files.")
parser.add_argument("-r",
                    "--reload",
                    type=str,
                    help="Reload a web app by name.")
parser.add_argument("-q",
                    "--quit",
                    action="store_true",
                    help="Quit main process")
parser.add_argument("-t",
                    "--test",
                    action="store_true",
                    help="Test apps' plugins. Quit after loading.")
args = parser.parse_args()

rootName = args.root_name
runningFlag = True
appList: dict[str, App] = {}
threadList: dict[str, Process] = {}
config: ConfigInstance | None = None


def reloadCallback(name: str) -> None:
    global threadList
    if name in threadList:
        threadList[name].terminate()
        threadList[name] = Process(target=appList[name].run)
        threadList[name].start()
        Log.info("Web app", name, "reloaded.")
    else:
        Log.error("Web app", name, "not found.")


def signalCallback(signal: str, param: str):
    Log.info("Signal received: " + signal)
    if signal == RELOAD_SIGNAL:
        reloadCallback(param)
    elif signal == QUIT_SIGNAL:
        global runningFlag
        runningFlag = False


def server():
    global runningFlag
    # check arguments
    if args.reload is not None:
        raise ValueError("Cannot reload when main process is not running.")
    if args.quit:
        raise ValueError("Cannot quit when main process is not running.")
    # start
    setCallback(signalCallback)
    setupServer(rootName)
    if config is None:
        raise ValueError("Config not initialized.")
    for name in config["webAppList"]:
        Log.info("Initializing web app: " + name)
        appList[name] = App(name)
        thisReloadCallback = lambda name=name: signal(rootName, RELOAD_SIGNAL,
                                                      name)
        appList[name].setReloadCallback(thisReloadCallback)
        threadList[name] = Process(target=appList[name].run)
        threadList[name].start()
    if args.test:
        runningFlag = False
        Log.debug("Test mode. Quitting after loading.")
    try:
        while runningFlag:
            timeSleep(1)
    except KeyboardInterrupt:
        pass
    for name, item in threadList.items():
        item.terminate()
        Log.info("Web app: " + name + " terminated.")
    killServer()
    Log.info("Main process terminated.")
    Log.info("=====================================")
    sysExit(0)


def client():
    if args.reload is not None:
        if args.quit:
            raise ValueError("Cannot quit and reload at the same time.")
        if config is None:
            raise ValueError("Config not initialized.")
        if args.reload not in config["webAppList"]:
            Log.error("Existing web app list: " + str(config["webAppList"]))
            raise ValueError("Cannot reload a non-exist web app.")
        Log.info("Reloading web app: " + args.reload)
        signal(rootName, RELOAD_SIGNAL, args.reload)
    if args.quit:
        Log.info("Quitting main process.")
        signal(rootName, QUIT_SIGNAL, "")
    if args.reload is None and not args.quit:
        raise ValueError("Main process is already running.")
    sysExit(0)


def main():
    global config
    setConfigPath(args.config_path)
    Log.init()
    config = ConfigInstance("main", configTemplate)
    if isFirstInstance(rootName):
        server()
    else:
        client()


if __name__ == "__main__":
    main()