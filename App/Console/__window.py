"""
Window layout
log
log
log
...
log
command input
"""

from curses import initscr as _initscr, wrapper as _wrapper


class Window:

    def __init__(self):
        self.__screen = _initscr()
        self.__size: tuple[int, int] = (0, 0)
        
    def _refreshSize(self) -> None:
        self.__size = self.__screen.getmaxyx()
