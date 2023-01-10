from logging import Formatter as _Formatter
from logging import Logger as _Logger
from logging import getLogger as _getLogger

_logger: _Logger | None = None


def init(name: str) -> None:
    if name == "":
        raise ValueError("name must not be empty")
    global _logger
    _logger = _getLogger(name)
    # set log format
    _logger.handlers[0].setFormatter(
        _Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))


def info(*args: object) -> None:
    if _logger is None:
        raise ValueError("logger not initialized")
    _logger.info(*args)

def warning(*args: object) -> None:
    if _logger is None:
        raise ValueError("logger not initialized")
    _logger.warning(*args)
    
def error(*args: object) -> None:
    if _logger is None:
        raise ValueError("logger not initialized")
    _logger.error(*args)
    
def debug(*args: object) -> None:
    if _logger is None:
        raise ValueError("logger not initialized")
    _logger.debug(*args)
    
def critical(*args: object) -> None:
    if _logger is None:
        raise ValueError("logger not initialized")
    _logger.critical(*args)
    
def exception(*args: object) -> None:
    if _logger is None:
        raise ValueError("logger not initialized")
    _logger.exception(*args)