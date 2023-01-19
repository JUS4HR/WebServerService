"""
Log format: [YYYY-MM-DD HH:MM:SS] [LEVEL] [message]
"""

from logging import CRITICAL as _CRITICAL
from logging import DEBUG as _DEBUG
from logging import ERROR as _ERROR
from logging import INFO as _INFO
from logging import WARNING as _WARNING
from logging import FileHandler as _FileHandler
from logging import Logger as _Logger
from logging import StreamHandler as _StreamHandler
from logging import basicConfig as _basicConfig
from logging import getLogger as _getLogger
from sys import path as _sysPath
from os import path as _osPath, makedirs as _osMakedirs

_sysPath.append("..")

from Config import Config as _Config
from Config import ConfigInstance as _ConfigInstance

_configTemplate: _Config = {
    "name": ("webServer", "The name of the logger."),
    "logPath": ("~/.webServer/log/", "The path to store all log files."),
    "logLevel": ("info", "Which logs will be sotred to console."),
    "logFileLevel": ("info", "Which logs will be sotred to file."),
}

_configInstance: _ConfigInstance | None = None

_logger: _Logger | None = None
_initialized: bool = False


def init() -> None:
    global _logger, _initialized
    if _initialized:
        return
    _configInstance = _ConfigInstance("logger", _configTemplate)
    if _configInstance["logPath"].startswith("~/"):
        _configInstance["logPath"] = _osPath.expanduser(
            _configInstance["logPath"])
    logPath = _osPath.abspath(_configInstance["logPath"])
    if not _osPath.exists(logPath) and not _osPath.isdir(logPath):
        _osMakedirs(logPath)
    print(logPath)
    _logger = _getLogger(_configInstance["name"])
    streamHandler = _StreamHandler()
    streamHandler.setLevel(_getLogLevel(_configInstance["logLevel"]))
    fileHandler = _FileHandler(
        _osPath.join(logPath, _configInstance["name"] + ".log"))
    fileHandler.setLevel(_getLogLevel(_configInstance["logFileLevel"]))
    _basicConfig(
        level=_getLogLevel(_configInstance["logLevel"]),
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            streamHandler,
            fileHandler,
        ],
    )
    _initialized = True


def _getLogLevel(level: str) -> int:
    level = level.lower().strip()
    if level == "debug":
        return _DEBUG
    elif level == "info":
        return _INFO
    elif level == "warning":
        return _WARNING
    elif level == "error":
        return _ERROR
    elif level == "critical":
        return _CRITICAL
    else:
        raise ValueError("Invalid log level: " + level + ".")


def _log(level: int, *args: object) -> None:
    global _logger
    if not _initialized or _logger is None:
        raise Exception("_Logger not initialized.")
    _logger.log(level, " ".join([str(arg) for arg in args]))


def debug(*args: object) -> None:
    _log(_DEBUG, *args)


def info(*args: object) -> None:
    _log(_INFO, *args)


def warning(*args: object) -> None:
    _log(_WARNING, *args)


def error(*args: object) -> None:
    _log(_ERROR, *args)


def critical(*args: object) -> None:
    _log(_CRITICAL, *args)