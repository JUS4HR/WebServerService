"""
This file is a template demonstrating how to create a WebApp plugin. It is not intended to be used as a plugin.
A Plugin should contain its callback functions, with specific input and return types.
Functions should be stored in dict "callbacks". With {"function_A": function_A} in the dict, the callback will be called when url is "/?request=function_A",
and the json received with POST method will be passed to the function as the argument.
When the function returns, the json returned will be sent back to the client.
"""

### callback types definitions
from typing import Any as _Any
from typing import Callable as _Callable
from typing import Dict as _Dict
from typing import List as _List
from typing import Tuple as _Tuple

_CallableInputType = _Dict[str, _Any]  # json
_CallbackReturnType = _Tuple[bool, str | None,
                            _Dict[str, _Any]]  # success?, reason, json
_CallBackFunctionType = _Callable[[_CallableInputType], _CallbackReturnType]

### imports
from subprocess import Popen as _Popen, PIPE as _PIPE

### functions
def getOsInfoCallback(jsonInput: _CallableInputType) -> _CallbackReturnType:
    if jsonInput["type"] == "linux":
        p = _Popen(["uname", "-a"], stdout=_PIPE, stderr=_PIPE)
        return True, None, {"osInfo": p.stdout.read().decode("utf-8")}
    else:
        return False, "Unsupported OS.", {}


### the actual list read by the WebApp
callbacks: _Dict[str, _CallBackFunctionType] = {
    "getOsInfo": getOsInfoCallback,
#   [the request string]: [the callback function]
}