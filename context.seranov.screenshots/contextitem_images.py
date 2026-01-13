import sys

from resources.lib.fs import FS
from resources.lib.ui import UI

if __name__ == '__main__':
    fs = FS(sys.listitem)
    ui = UI(fs)
    ui.slide_show_open()
