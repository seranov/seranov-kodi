import os
import sys
from urllib.parse import urlencode

import xbmc
import xbmcaddon
import xbmcgui

addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')

item_path = sys.listitem.getVideoInfoTag().getPath()

shoots_dir_about = os.path.join(item_path, addon.getSetting('about'))
xbmc.log("[%s] opening '%s'" % (addon.getAddonInfo('id'), shoots_dir_about), xbmc.LOGDEBUG)

params = {
    'path': shoots_dir_about,
    'isroot': 'true',
    'title': sys.listitem.getLabel(),
    'fanart': sys.listitem.getProperty('fanart_image'),
}
plugin_url = "plugin://context.item.extras/?" + urlencode(params)

# Set a string variable to use 
line1 = "Hello World! We can write anything we want here Using Python"

# Launch a dialog box in kodi showing the string variable 'line1' as the contents
xbmcgui.Dialog().ok(addonname, shoots_dir_about)
