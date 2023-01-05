"""
Content file watcher for a web app.
Watches for changes in the content directory and calls the reload callback.
"""

from typing import Callable as _Callable

from watchdog.events import FileSystemEventHandler as _FileSystemEventHandler
from watchdog.observers import Observer as _Observer


class ContentFileWatcher:

    def __init__(self, reloadCallback: _Callable[[], None],
                 contentDirs: list[str]):
        self.__reloadCallback = reloadCallback
        self.__contentDirs = contentDirs

    def run(self):
        eventHandler = _FileSystemEventHandler()
        eventHandler.on_created = self.__onChange
        eventHandler.on_deleted = self.__onChange
        eventHandler.on_modified = self.__onChange
        # eventHandler.on_moved = self.__onChange
        self.__observer = _Observer()
        for contentDir in self.__contentDirs:
            self.__observer.schedule(eventHandler, contentDir, recursive=True)
        self.__observer.start()

    def stop(self):
        self.__observer.stop()
        self.__observer.join()

    def __onChange(self, event):
        if event.is_directory:
            return
        try:
            print("Reloading due to", event.event_type, "in", event.src_path)
            self.__reloadCallback()
        except Exception as e:  # in case of error, print it and continue
            print("Exception caught:", e)
