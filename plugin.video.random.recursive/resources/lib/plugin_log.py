import xbmc


class PluginLog:
    PREFIX = "plugin.video.random.recursive: "

    @staticmethod
    def log(message, level=xbmc.LOGINFO):
        xbmc.log(f"{PluginLog.PREFIX}{message}", level)

    @staticmethod
    def debug(message):
        PluginLog.log(message, xbmc.LOGDEBUG)

    @staticmethod
    def info(message):
        PluginLog.log(message)

    @staticmethod
    def error(message):
        PluginLog.log(message, xbmc.LOGERROR)
