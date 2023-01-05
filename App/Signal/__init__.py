from socket import AF_INET as _AF_INET
from socket import SO_REUSEADDR as _SO_REUSEADDR
from socket import SOCK_STREAM as _SOCK_STREAM
from socket import SOL_SOCKET as _SOL_SOCKET
from socket import socket as _socket
from threading import Thread as _Thread
from typing import Any as _Any
from typing import Callable as _Callable
from typing import Dict as _Dict

_socketHandleListen: _socket = _socket(_AF_INET, _SOCK_STREAM)
_callback: _Callable[[str, str], None] | None = None
_runningFlag: bool = True

def _generatePortWithName(name: str) -> int:
    # range: 30000 - 40000
    return 30000 + sum([ord(c) for c in name]) % 10000


def _listenThread() -> None:
    while _runningFlag:
        _socketHandleListen.settimeout(0.1)
        data: str = ""
        try:
            client, addr = _socketHandleListen.accept()
            data = client.recv(1024).decode()
        except:
            continue
        if data:
            dataSplitted = data.split(" ")
            if len(dataSplitted) == 2:
                if _callback:
                    _callback(dataSplitted[0], dataSplitted[1])


def setupServer(name: str) -> None:
    _socketHandleListen.bind(("", _generatePortWithName(name)))
    _socketHandleListen.setsockopt(_SOL_SOCKET, _SO_REUSEADDR, 1)
    _socketHandleListen.listen(1)
    _Thread(target=_listenThread).start()


def killServer() -> None:
    global _runningFlag
    _runningFlag = False
    _socketHandleListen.close()


def setCallback(callback: _Callable[[str, str], None]) -> None:
    global _callback
    _callback = callback


def signal(name: str, data0: str, data1: str) -> None:
    socketHandleSend: _socket = _socket(_AF_INET, _SOCK_STREAM)
    socketHandleSend.connect(("", _generatePortWithName(name)))
    socketHandleSend.send((data0 + " " + data1).encode())
    socketHandleSend.close()