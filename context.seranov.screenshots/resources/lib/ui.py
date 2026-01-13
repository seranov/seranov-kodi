import xbmc
import xbmcgui

from resources.lib.fs import FS
from resources.lib.slide_show import SlideShow


class UI:
    def __init__(self, fs: FS, **kwargs):
        self.fs = fs
        self.slideshow = None
        self.image_tile = None

    def make_slide_show_items(self, media_fs: FS):
        items = []
        for image in media_fs.images:
            if image["allowed"]:
                item = xbmcgui.ListItem(image["path"])
                item.setArt({'img': image["path"]})
                # item.setProperty("image", image)
                items.append(item)
        return items

    def slide_show_run(self, media_fs: FS, items):
        if media_fs.nfo_file:
            text = media_fs.nfo_text
        else:
            text = media_fs.diz_text
        # xbmc.log(f"UI text: {text}", xbmc.LOGINFO)
        self.slideshow = SlideShow('slide-show.xml',
                                   media_fs.addon.getAddonInfo('path'),
                                   listitems=items,
                                   index=0,
                                   fanart=media_fs.artwork,
                                   text=text)
        self.slideshow.doModal()
        self.slideshow.swith_mode()
        self.slideshow = None

    def slide_show_open(self):
        self.fs.select_file_id_diz(self.fs.movie_root)
        self.fs.read_file_id_diz(self.fs.diz_file)
        self.fs.select_movie_nfo(self.fs.movie_root)
        self.fs.read_movie_nfo(self.fs.nfo_file)
        if not self.fs.artwork:
            self.fs.select_artwork()
        if not self.fs.images:
            self.fs.get_all_images(self.fs.movie_root)
        slide_show_items = self.make_slide_show_items(self.fs)
        self.slide_show_run(self.fs, slide_show_items)
