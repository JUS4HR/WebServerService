Web server for multiple web apps running as systemd service
===
Usage
---
 1. Install dependencies
    ```
    pip install -r requirements.txt
    # or use conda or venv
    ```
    Run once to create the config.
    ```
    python ./App/main.py --test
    ```

 2. Edit config to setup your won web app.    
    Config is located at `~/.webServer/config.json` as default. ~~You can use the following launching parameter to manually set config path.~~(Buggy, don't use for now.) Note the config file name cannot be modified.
    ```
    python ./App/main.py --config-path [dir to config]
    ```
     - Config file is a json file. The following is an example.
    
        With each config item, a description is provided.
        ```
        {
            "main": {
                "debug": false,
                "debug-description": "Enable debug mode",
                "web-app-list": [
                    "test1", "test2"
                ],
                "web-app-list-description": "List of names of web apps"
            },
            "web-app-test1": {
                ... (Auto generated)
            },
            "web-app-test2": {
                ... (Auto generated)
            }
        }
        ```
     - `web-app-list` sets the list of web apps to run. In the example, `test1` and `test2` are set, so on the next run it will generate the following two configs for test1 and test2.    

        A web app config is a json object with the following fields:
        ```
        "web-app-home": {
            "debug": false,
            "debug-description": "Whether to enable debug mode or not.",
            "html-directory": "path/to/html/files",
            "html-directory-description": "The directory to html files. Use absolute path.",
            "listen-lan": true,
            "listen-lan-description": "Whether to listen on lan or not.",
            "plugin-directory": "path/to/plugin/files",
            "plugin-directory-description": "The directory where plugins (.py files) are located. Use absolute path.",
            "port": 20200,
            "port-description": "The port to listen on.",
            "port-with-ssl": 20200,
            "port-with-ssl-description": "The port to listen on with SSL.",
            "ssl-cert-directory": "path/to/ssl/cert",
            "ssl-cert-directory-description": "The directory to ssl certificate files. Requires .pem and .key files. Use absolute path. If not set, ssl will not be enabled.",
            "static-files-directory": "path/to/static/files",
            "static-files-directory-description": "The directory to static files. e.g. css, js, iamges, etc. Use absolute path.",
            "watch-html-change": true,
            "watch-html-change-description": "Whether to watch html changes or not.",
            "watch-plugin-change": true,
            "watch-plugin-change-description": "Whether to watch plugin changes or not.",
            "watch-ssl-cert-change": false,
            "watch-ssl-cert-change-description": "Whether to watch ssl certificate changes or not.",
            "watch-static-files-change": false,
            "watch-static-files-change-description": "Whether to watch static files changes or not."
        }
        ```
        
        - `debug` enables debug mode. WIP. __Debugging is not supported for now.__
        - `html-directory` sets the directory to html files. Use absolute path.
        - `listen-lan` enables listening on lan. If set to false, only localhost is listened.
        - `plugin-directory` sets the directory to plugin files. Use absolute path.
        - `port` sets the port to listen on.
        - `port-with-ssl` sets the port to listen on with SSL. If not set, SSL will not be enabled.
        - `ssl-cert-directory` sets the directory to ssl certificate files. Requires .pem and .key files. Use absolute path. If not set, ssl will not be enabled.
        - `static-files-directory` sets the directory to static files. e.g. css, js, iamges, etc. Use absolute path.
        - `watch-html-change` enables watching html changes. If set to true, the server will restart when html files are changed.
        - `watch-plugin-change` enables watching plugin changes. If set to true, the server will restart when plugin files are changed.
        - `watch-ssl-cert-change` enables watching ssl certificate changes. If set to true, the server will restart when ssl certificate files are changed.
        - `watch-static-files-change` enables watching static files changes. If set to true, the server will restart when static files are changed.
        
 3. When you finish editing the config, run the following command again to start the server. Only on instance of the server can be run at a time. ~~If you want to run multiple instances, you can use `--config-path` to specify different config files.~~(Buggy, don't use for now.)
    ```
    python ./App/main.py
    ```
 4. If you find your server running normally, you can install it as a systemd service.
    ```
    ./Scripts/installService.sh
    systemctl start webServer # or systemctl --user start webServer
    ```

 5. Other usage

    `--reload [app name]` When an instance is already running, run another instance with this parameter to reload the app. __Note__ the `main` part in the config is not reloaded.

    `--quit` When an instance is already running, run another instance with this parameter to quit the existing instance.

Example files
---
Located at `./ExampleSite`. Contains a simple web page to print host machine's system info. The example app is set to be run by default if config has just been created. You can use it as a template to create your own web app.

Tutorial
---
 - Page and redirecting

    If you want to redirect to another page inside the app, you can use the following code:
    ```
    <script>
        window.location = "/?redirect=[html file name without extension]";
    </script>
    ```
    The urls pointing to the static folder is the same as flask server, Refer to the example app for more details.

 - Post request and plugins

    If you want to send a post request to the server, you have to use json format. The way to send a post request is the same as a normal post request. The following is an example:
    ```
    $.ajax({
        url: "/?request=[plugin target name]",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            "name1": "val1",
            "name2": "val2",
        }),
        success: function (data) {
            console.log(data);
        }
    });
    ```
    The it comes to the plugins. Plugins are python files located at `plugin-directory` in the config. The file should contain the following variables:
    ```
    # the config setup for the plugin
    config: dict[str, tuple[any, str]] = {
        "yourConfigItem1": (yourConfigItem1DefaultValue, "yourConfigItem1Description"),
        "yourConfigItem2": (yourConfigItem2DefaultValue, "yourConfigItem2Description"),
        ...
    }

    # its functions
    def yourFunction1(jsonInput: dict[str, any]) -> str:
        return True, None, {[json to send back]}
        # returns are <success: bool, error: str, json: dict[str, any]>
    
    # the list for the server to read the functions
    callbacks: dict[str, Callable[[dict[str, any]], tuple[bool, str, dict[str, any]]]] = {
        "yourFunction1": yourFunction1,
        # the str should be your request target name, same as the one in the ajax request above.
        ...
    }
    ```

    The plugin now works like this:

    1. When the server starts, it reads the config variables and fill it with the values in the config file. If the config file does not exist, it will create one with default values. Created config entries in the config file looks like:
        ```
        "web-app-[web app name]-plugin-[config file name]": {
        ...    
        }
        ```
    2. When a post request is sent, the request will be passed to the plugin function with the name given, and the returned value will be converted to `{ "success": "ok" or "error", "error-reason": str, "json": dict[str, any] }` and sent back to the client.

