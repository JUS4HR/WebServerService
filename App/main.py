from sys import exit as sysExit
from threading import Thread

from Config import Config, ConfigInstance, setConfigPath
from WebApp import App

configTemplate: Config = {
    "debug": (False, "Enable debug mode"),
    "webAppList": (["example"], "List of names of web apps"),
}


def main():
    setConfigPath("~/." + "webServer")
    config = ConfigInstance("main", configTemplate)

    appList: dict[str, App] = {}
    threadList: dict[str, Thread] = {}
    for name in config["webAppList"]:
        print("Initializing web app: " + name)
        appList[name] = App(name)
        threadList[name] = Thread(target=appList[name].run)
        threadList[name].start()
        print("Web app: " + name + " initialized.")

    while True:
        try:
            input()
        except KeyboardInterrupt:
            sysExit(0)


if __name__ == "__main__":
    main()