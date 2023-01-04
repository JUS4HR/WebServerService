from sys import exit as sysExit
from multiprocessing import Process
from typing import Callable

from Config import Config, ConfigInstance, setConfigPath
from Singleton import isFirstInstance
from WebApp import App

configTemplate: Config = {
    "debug": (False, "Enable debug mode"),
    "webAppList": (["example"], "List of names of web apps"),
}

keywordMapping: dict[str, Callable] = {
    "quit": sysExit,
    "reload": lambda: None,
    "restart": lambda: None,
}

rootName = "webServer"


def singletonCallback(string: str) -> None:
    print("Received message: " + string)


def main():
    setConfigPath("~/." + rootName)
    config = ConfigInstance("main", configTemplate)
    if isFirstInstance(rootName):
        # start
        appList: dict[str, App] = {}
        threadList: dict[str, Process] = {}
        for name in config["webAppList"]:
            print("Initializing web app: " + name)
            appList[name] = App(name)
            threadList[name] = Process(target=appList[name].run)
            threadList[name].start()
            print("Web app: " + name + " initialized.")

        try:
            while True:
                pass
        except KeyboardInterrupt:
            for name, item in threadList.items():
                item.terminate()
            sysExit(0)
    else:
        # quit for now
        print("Another instance is running.")
        sysExit(0)


if __name__ == "__main__":
    main()