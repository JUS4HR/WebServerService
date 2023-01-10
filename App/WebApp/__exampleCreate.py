from typing import Any as _Any, Dict as _Dict


def createExample() -> _Dict[str, _Any]:
    return {
        "anImportantNote": ("This is an example config file. Please change the values to your own. And dont use relative path like this one.", ""),
        "port": (20200, "The port to listen on."),
        "portWithSSL": (20201, "The port to listen on with SSL."),
        "listenLan": (True, "Whether to listen on lan or not."),
        "htmlDirectory": ("ExampleSite/html",
                          "The directory to html files. Use absolute path."),
        "staticFilesDirectory":
        ("ExampleSite/static",
         "The directory to static files. e.g. css, js, iamges, etc. Use absolute path."
         ),
        'sslCertDirectory':
        ("",
         "The directory to ssl certificate files. Requires .pem and .key files. Use absolute path. If not set, ssl will not be enabled."
         ),
        "debug": (False, "Whether to enable debug mode or not."),
        "pluginDirectory":
        ("ExampleSite/plugin",
         "The directory where plugins (.py files) are located. Use absolute path."
         )
    }
