import xbmc


class PluginLog:
    PREFIX = "plugin.video.random.recursive: "

    @staticmethod
    def log(message, level=xbmc.LOGINFO):
        xbmc.log(f"{PluginLog.PREFIX}{message}", level)

    @staticmethod
    def debug(message):
        PluginLog.log(f"{PluginLog.PREFIX}{message}", xbmc.LOGDEBUG)

    @staticmethod
    def info(message):
        PluginLog.log(f"{PluginLog.PREFIX}{message}")

    @staticmethod
    def error(message):
        PluginLog.log(f"{PluginLog.PREFIX}{message}", xbmc.LOGERROR)
