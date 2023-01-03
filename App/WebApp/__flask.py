"""
工作流程：
1. 查找url中的redirect变量. 若有, 先在redirectList中寻找对应template名, 后在renderMapping.csv中找到对应页面template名, 返回渲染指令
2. 查找url中的request变量. 若有, 将接收到的json传入对应的回调函数, 返回回调函数给出的json
3. 若同时存在redirect和request变量, 则仅执行redirect
4. 若都不存在, 则返回render 404页面

接受到的json格式:
{
    "uid": [16位数字uid](登陆页面为null),
    "token": [32位大小写字母+数字token](登陆页面为null),
    "json": {
        "json key 1": "json value 1",
        ...
    }
}
返回json的格式:
{
    "status": "ok" | "error",
    "error-reason": "error reason" | null,
    "json": {
        "json key 1": "json value 1",
        ...
    }
}
"""

from importlib import util as _importUtil
from os import listdir as _osListdir
from os import path as _osPath
from sys import path as _sysPath
from typing import Any as _Any
from typing import Dict as _Dict
from typing import List as _List
from typing import Optional as _Optional
from typing import Tuple as _Tuple

from flask import Flask as _flask
from flask import jsonify as _jsonify
from flask import render_template as _render_template
from flask import request as _request

from .__ssl import getSSLContext as _getSSLContext
from .__types import *
from .__exampleCreate import createExample as _createExample

_sysPath.append("..")

from Config import Config as _Config
from Config import ConfigInstance as _ConfigInstance

_configTemplate: _Config = {
    "port": (80, "The port to listen on."),
    "portWithSSL": (443, "The port to listen on with SSL."),
    "listenLan": (True, "Whether to listen on lan or not."),
    "htmlDirectory": ("", "The directory to html files. Use absolute path."),
    "staticFilesDirectory":
    ("",
     "The directory to static files. e.g. css, js, iamges, etc. Use absolute path."
     ),
    'sslCertDirectory':
    ("",
     "The directory to ssl certificate files. Requires .pem and .key files. Use absolute path. If not set, ssl will not be enabled."
     ),
    "debug": (False, "Whether to enable debug mode or not."),
    "pluginDirectory":
    ("",
     "The directory where plugins (.py files) are located. Use absolute path.")
}


def _callBackPlaceHolder(json: CallableInputType) -> CallbackReturnType:
    return False, "This is a placeholder function.", {}


class App():

    def __init__(self, name: _Optional[str] = None):

        self.__redirectList: _List[str] = []
        self.__callbackList: _Dict[str, CallBackFunctionType] = {}
        # create example config if name is "example"
        if name == "example":
            exampleConfigTemplate = _createExample()
            self.__config = _ConfigInstance(
                "webApp" + "-" + name if name is not None else "unnamed",
                exampleConfigTemplate)
        else:
            self.__config = _ConfigInstance(
                "webApp" + "-" + name if name is not None else "unnamed",
                _configTemplate)
        self.__getPages()
        self.__getPlugins()

        self.__app = _flask(
            name if name is not None else __name__,
            template_folder=self.__config["htmlDirectory"],
            static_folder=self.__config["staticFilesDirectory"])

        @self.__app.route('/', methods=['GET', 'POST'])
        def process():
            return self.__process(_request.args,
                                  _request.json if _request.is_json else None)

    def __process(self, args: _Dict[str, _Any],
                  json: _Dict[str, _Any] | None) -> _Any:
        if "redirect" in args:
            if args["redirect"] in self.__redirectList:
                return _render_template(args["redirect"] + ".html")
            else:
                return _render_template("404.html")
        elif "request" in args:
            return self.__callback(args["request"], json)
        else:
            if len(args) == 0:
                return _render_template("index.html")
            return _render_template("404.html")

    def __getPages(self) -> None:
        for pageDir in _osListdir(self.__config["htmlDirectory"]):
            if _osPath.isdir(pageDir):
                fileNames = _osListdir(pageDir)
                for file in fileNames:
                    if file.endswith(".html"):
                        self.__redirectList.append(file[:-5])

    def __callback(self, keyWord: str, json: _Dict[str, _Any] | None) -> _Any:
        if keyWord in self.__callbackList:
            success, reason, resultJson = self.__callbackList[keyWord](
                json if json is not None else {})
            return _jsonify({
                "status": "ok" if success else "error",
                "error-reason": reason,
                "json": resultJson
            })
        else:
            return _jsonify({
                "status": "error",
                "error-reason": "Request not found.",
                "json": {}
            })

    def __getPlugins(self) -> None:
        for fileName in _osListdir(self.__config["pluginDirectory"]):
            if not fileName.endswith(".py") or not _osPath.isfile(
                    _osPath.join(self.__config["pluginDirectory"], fileName)):
                pass
            moduleSpec = _importUtil.spec_from_file_location(
                fileName[:-3],
                _osPath.join(self.__config["pluginDirectory"], fileName))
            if moduleSpec is not None:
                module = _importUtil.module_from_spec(moduleSpec)
                if moduleSpec.loader is not None:
                    moduleSpec.loader.exec_module(module)
                    if hasattr(module, "callbacks"):
                        for key, callable in module.callbacks.items():
                            if key in self.__callbackList:
                                raise Exception("Callback key conflict: " + key)
                            self.__callbackList[key] = callable
                    else:
                        print("No callbacks found in " + fileName)

    def run(self) -> None:
        ssl_context: tuple[str, str] | None = None
        if self.__config["sslCertDirectory"] != "":
            try:
                ssl_context = _getSSLContext(self.__config["sslCertDirectory"])
            except Exception as e:
                print(e)
        port: int = self.__config[
            "port"] if ssl_context is None else self.__config["portWithSSL"]
        listenLan: bool = self.__config["listenLan"]
        debug: bool = self.__config["debug"]
        try:
            if ssl_context:
                print("SSL context is enabled: {}".format(ssl_context))
            self.__app.run(host="0.0.0.0" if listenLan else None,
                           port=port,
                           debug=debug,
                           ssl_context=ssl_context)

        except Exception as e:
            print("Exception: {}".format(e))