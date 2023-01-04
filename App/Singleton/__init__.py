from socket import AF_UNIX as _AF_UNIX
from socket import SOCK_STREAM as _SOCK_STREAM
from socket import socket as _socket

_socketHandler: _socket | None = None
def isFirstInstance(name: str) -> bool:
    global _socketHandler
    _socketHandler = _socket(_AF_UNIX, _SOCK_STREAM)
    try:
        _socketHandler.bind("\0" + name)
        return True
    except OSError:
        return False