#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin


def main():
    """Main addon entry point"""
    addon = xbmcaddon.Addon()
    addon_name = addon.getAddonInfo('name')
    addon_version = addon.getAddonInfo('version')
    
    # Get addon handle if available
    addon_handle = None
    if len(sys.argv) > 1:
        try:
            addon_handle = int(sys.argv[1])
        except (ValueError, IndexError):
            pass
    
    # Show a simple dialog with addon information
    xbmcgui.Dialog().ok(
        addon_name,
        addon.getLocalizedString(32010).format(addon_version) + '\n\n'
        + addon.getLocalizedString(32011) + '\n\n'
        + addon.getLocalizedString(32012)
    )
    
    if addon_handle:
        xbmcplugin.endOfDirectory(addon_handle)


if __name__ == '__main__':
    main()
