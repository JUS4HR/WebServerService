from typing import Any as _Any
from typing import Callable as _Callable

CallableInputType = dict[str, _Any]  # json
CallbackReturnType = tuple[bool, str | None,
                           dict[str, _Any]]  # success?, reason, json

CallBackFunctionType = _Callable[[CallableInputType], CallbackReturnType]
ReloadCallbackType = _Callable[[], None]


class Plugin:

    def __init__(self) -> None:
        self.callbacksList: dict[str, CallBackFunctionType] = {}
        self.config: dict[str, _Any] = {}
