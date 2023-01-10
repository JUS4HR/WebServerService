"""
This file is a template demonstrating how to create a WebApp plugin. It is not intended to be used as a plugin.
A Plugin should contain the following items (variable name should be identical):
    config: dict[str, tuple[any, str]] # items are [name], [default value], [description string]. Config will be filled when the module is loaded,
            and will NEVER be refreshed. To refresh the config, you need to reload the app.
            When the config is filled, its type will be changed. Use config["item name"] to access the value.
            The name of the config item should be identical, and not ends with "description". Also, it's better not to contain repeated uppercase
            letters that indicates a acronym. E.g. "nameOfIML" will be parsed to the config file as "name-of-im-l".
    callbacks: dict[str, _CallBackFunctionType] # (type is shown below at line 12-15) A dict containing all the callback functions with their names.
               The given names of the callbacks are used in the WebApp to call the functions. To access a function named "getOsInfo" in the WebApp, 
               the URL would be like: http://localhost:5000/?request=getOsInfo, and the JSON delivered through the POST request would be passed to
               the function.
"""

### callback types definitions
from typing import Any as _Any
from typing import Callable as _Callable

_CallableInputType = dict[str, _Any]  # json
_CallbackReturnType = tuple[bool, str | None,
                            dict[str, _Any]]  # success?, reason, json
_CallBackFunctionType = _Callable[[_CallableInputType], _CallbackReturnType]

### imports
from subprocess import Popen as _Popen, PIPE as _PIPE

### config
config: dict[str, tuple[_Any, str]] = {
    "supportedPlatformList": (["linux"], "The list of supported platforms.")
    # [name], [default value], [description string]
}

### functions
def getOsInfoCallback(jsonInput: _CallableInputType) -> _CallbackReturnType:
    if jsonInput["type"] in config["supportedPlatformList"]: # how you access the config values
        out = _Popen(["uname", "-a"], stdout=_PIPE, stderr=_PIPE).stdout
        if out is not None:
            result = out.read().decode("utf-8")
            return True, None, {"osInfo": result}
        else:
            return False, "Result is None", {}
    else:
        return False, "Unsupported OS.", {}


### the actual list read by the WebApp
callbacks: dict[str, _CallBackFunctionType] = {
    "getOsInfo": getOsInfoCallback,
#   [the request string]: [the callback function]
}