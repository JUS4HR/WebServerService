from json import dump as _jsonDump
from json import load as _jsonLoad
from os import makedirs as _osMakedirs
from os import path as _osPath
from typing import Any as _Any
from typing import Dict as _Dict
from typing import List as _List
from typing import Tuple as _Tuple

_configSymbol = "-"
_configDescriptionPostfix: str = _configSymbol + "description"
_configNameList: _List[str] = []

_configFileName = "config.json"
_configPath: str | None = None

Config = _Dict[str, _Tuple[_Any, str]]

def setConfigPath(configPath: str) -> None:
    global _configPath
    if configPath.startswith("~/"):
        configPath = _osPath.expanduser(configPath)
    _configPath = _osPath.abspath(configPath)


def _getConfigFileFullPath() -> str:
    if _configPath is None:
        raise Exception("Config path not set")
    fullPath: str = _osPath.join(_configPath, _configFileName)
    if not _osPath.exists(fullPath):
        _osMakedirs(_configPath, exist_ok=True)
        with open(fullPath, "w") as configFile:
            _jsonDump({}, configFile)
    return fullPath


def _formatConfigItemName(configName: str) -> str:
    retStr = ""
    lastIsSymbol = False
    lastIsUpper = False
    for char in configName:
        if char.isalnum():
            lastIsSymbol = False
            if char.isupper():
                if lastIsUpper or retStr == "":
                    retStr += char.lower()
                else:
                    retStr += _configSymbol + char.lower()
                lastIsUpper = True
            else:
                retStr += char
                lastIsUpper = False
        elif not lastIsSymbol:
            lastIsSymbol = True
            retStr += _configSymbol
    return retStr


class ConfigInstance:
    """The class for the config instance, use this to get the config.
    """

    def __init__(self,
                 name: str,
                 contentList: Config = {}):
        """Constructing a config instance.

        Args:
            name (str): The name of the config instance, will be the entry in the config file.
            contentList (_Dict[str, _Tuple[_Any, str]], optional): The name, default value and description of the config items. Defaults to {}.

        Raises:
            ValueError: If the name is empty.
            ValueError: If the name is already in the current active config list.
        """
        name = _formatConfigItemName(name)
        if name == "":
            raise ValueError("Config name must not be \"\".")
        elif name in _configNameList:
            raise ValueError(
                "Config name {} is already in the current active config list.".
                format(name))
        self.__name = name
        _configNameList.append(name)
        self.__content: _Dict[str, _Any] = {}
        contentList = dict(sorted(contentList.items()))
        for item, content in contentList.items():
            formattedName = _formatConfigItemName(item)
            if formattedName.endswith(_configSymbol +
                                      _configDescriptionPostfix):
                raise ValueError(
                    "Config item name cannot end with \"{}\".".format(
                        _configSymbol + _configDescriptionPostfix))
            self.__content[formattedName] = content[0]
            if content[1] != "":
                self.__content[formattedName +
                            _configDescriptionPostfix] = content[1]
        self.__readConfig()

    def __readConfig(self):
        oldConf: _Dict[str, _Dict[str, _Any]] = {}
        with open(_getConfigFileFullPath(), "r") as configFile:
            try: # in case the config is corrupted
                oldConf = _jsonLoad(configFile)
            except Exception:
                with open(_getConfigFileFullPath() + ".corrupted", "w") as corruptedConfigFile:
                    corruptedConfigFile.write(configFile.read())
                # print in red
                print("\033[91mConfig file corrupted, backup created at " + _getConfigFileFullPath() + ".corrupted\033[0m")
                pass
        if self.__name in oldConf:
            for item in self.__content:
                if item in oldConf[self.__name]:
                    self.__content[item] = oldConf[self.__name][item]
        oldConf[self.__name] = self.__content
        oldConf = dict(sorted(oldConf.items()))
        with open(_getConfigFileFullPath(), "w") as configFile:
            _jsonDump(oldConf, configFile, indent=4)

    def reload(self):
        """Reload the config from the config file."""
        self.__readConfig()

    def setItem(self, key: str, value: _Any) -> None:
        self.__setitem__(key, value)

    def getItem(self, key: str) -> _Any:
        return self.__getitem__(key)

    def __getitem__(self, key: str) -> _Any:
        key = _formatConfigItemName(key)
        if key.endswith(_configDescriptionPostfix):
            return None
        return self.__content[key] if key in self.__content else None

    def __setitem__(self, key: str, value: _Any) -> None:
        key = _formatConfigItemName(key)
        if key.endswith(_configDescriptionPostfix):
            raise ValueError("Cannot set description item.")
        self.__content[key] = value

    def __str__(self) -> str:
        return self.__name + ": " + str(self.__content)


# test
if __name__ == "__main__":
    print(_formatConfigItemName("testTest, testTESTtest"))