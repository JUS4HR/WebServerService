from typing import Any as _Any
from typing import Callable as _Callable
from typing import Dict as _Dict
from typing import List as _List
from typing import Tuple as _Tuple

CallableInputType = _Dict[str, _Any]  # json
CallbackReturnType = _Tuple[bool, str | None,
                            _Dict[str, _Any]]  # success?, reason, json

CallBackFunctionType = _Callable[[CallableInputType], CallbackReturnType]
