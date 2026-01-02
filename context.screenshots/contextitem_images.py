#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import xbmc
import xbmcaddon
import xbmcgui


def show_screenshots():
    """Show screenshots for the selected item"""
    try:
        # Get the selected list item
        if hasattr(sys, 'listitem'):
            listitem = sys.listitem
            path = listitem.getPath()
            
            addon = xbmcaddon.Addon()
            addon_name = addon.getAddonInfo('name')
            
            xbmcgui.Dialog().notification(
                addon_name,
                addon.getLocalizedString(32013).format(path),
                xbmcgui.NOTIFICATION_INFO,
                5000
            )
            
            # Here you would implement the actual screenshot slideshow logic
            # This is a placeholder implementation
            xbmc.log('[context.screenshots] Show screenshots for: ' + path, xbmc.LOGINFO)
        else:
            xbmc.log('[context.screenshots] No listitem available', xbmc.LOGERROR)
            
    except Exception as e:
        xbmc.log('[context.screenshots] Error: ' + str(e), xbmc.LOGERROR)
        addon = xbmcaddon.Addon()
        xbmcgui.Dialog().notification(
            addon.getLocalizedString(32014),
            addon.getLocalizedString(32015),
            xbmcgui.NOTIFICATION_ERROR,
            5000
        )


if __name__ == '__main__':
    show_screenshots()
