from socket import socket as _socket, AF_INET as _AF_INET, SOCK_STREAM as _SOCK_STREAM, SOL_SOCKET as _SOL_SOCKET, SO_REUSEADDR as _SO_REUSEADDR
from threading import Thread as _Thread
from typing import Callable as _Callable, Dict as _Dict, Any as _Any

_socketHandleListen: _socket = _socket(_AF_INET, _SOCK_STREAM)
_socketHandleSend: _socket = _socket(_AF_INET, _SOCK_STREAM)
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
    _socketHandleSend.close()
    _socketHandleListen.close()

def setCallback(callback: _Callable[[str, str], None]) -> None:
    global _callback
    _callback = callback


def signal(name: str, data0: str, data1: str) -> None:
    # setup client socket
    _socketHandleSend.connect(("", _generatePortWithName(name)))
    # send data
    _socketHandleSend.send((data0 + " " + data1).encode())