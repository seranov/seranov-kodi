import os
import sys
import pathlib
import re
import xbmc
import xbmcaddon
import xbmcvfs
import xml.etree.ElementTree as ET
from contextlib import closing
from kodi_six import xbmcvfs


class FS:
    """
    Класс для работы с файловой системой и файлами описания фильмов.
    """

    # Константы для имен файлов описания
    DESC_TXT = 'desc.txt'
    FILE_ID_DIZ = 'file_id.diz'
    MOVIE_NFO = 'movie.nfo'
    TXT_EXT = '.txt'

    # Константы для имен подпапок
    SUBDIR_UNDERSCORE = '_'
    SUBDIR_BDMV = 'bdmv'
    SUBDIR_VIDEO_TS = 'video_ts'
    SUBDIR_ABOUT = 'about'

    def select_movie_root(self, list_item):
        item_path = list_item.getVideoInfoTag().getPath()
        if not item_path:
            item_path = list_item.getPath()

        if os.path.isfile(item_path):
            item_path = os.path.dirname(item_path)

        no_slash = item_path.rstrip("/\\")
        last_part = os.path.basename(no_slash).lower()

        if last_part == self.SUBDIR_BDMV:
            item_path = item_path[:-5]
        elif last_part == self.SUBDIR_VIDEO_TS:
            item_path = item_path[:-9]
        elif last_part == self.SUBDIR_ABOUT:
            item_path = item_path[:-6]
        elif last_part.startswith('_t '):
            item_path = item_path[:-len(last_part) - 1]

        self.movie_root = item_path
        return self.movie_root

    def __init__(self, list_item, **kwargs):
        self.list_item = list_item
        self.addon = xbmcaddon.Addon()
        self.setting_include_non_jpg = self.addon.getSetting('include_non_jpg').lower() == 'true'
        self.setting_hide_small_jpg = self.addon.getSetting('hide_small_jpg').lower() == 'true'
        self.setting_minimum_jpg_size_percent = int(self.addon.getSetting('minimum_jpg_size_percent').lower())
        self.setting_hide_art_images = self.addon.getSetting('hide_art_images').lower() == 'true'
        self.movie_root = self.select_movie_root(self.list_item)
        self.nfo_file = None
        self.nfo_text = None
        self.diz_file = None
        self.diz_text = None
        self.artwork = None
        self.images = None
        self.jpeg_total_size = None
        self.jpeg_total_count = None

    def select_movie_nfo(self, movie_root):
        nfo_file_name = os.path.join(movie_root, self.MOVIE_NFO)
        nfo_file_exists = xbmcvfs.exists(nfo_file_name)
        if not nfo_file_exists:
            nfo_file_name = os.path.join(os.path.dirname(movie_root.rstrip("/\\")), self.MOVIE_NFO)
            nfo_file_exists = xbmcvfs.exists(nfo_file_name)
        if not nfo_file_exists:
            nfo_file_name = None
        self.nfo_file = nfo_file_name
        return self.nfo_file

    def select_file_id_diz(self, movie_root):
        """
        Выбирает файл описания только в текущей папке в порядке приоритета:
        1. Любой файл с расширением .txt (при наличии desc.txt отдаётся приоритет)
        2. file_id.diz
        """
        diz_file_name = None

        try:
            dirs, files = xbmcvfs.listdir(movie_root)
        except Exception:
            files = []

        # Приводим к lowercase для поиска, но сохраняем оригинальные имена
        lower_files = [f.lower() for f in files]

        # 1) Если есть точное имя desc.txt — используем его
        if self.DESC_TXT in lower_files:
            idx = lower_files.index(self.DESC_TXT)
            diz_file_name = os.path.join(movie_root, files[idx])
        else:
            # 2) Любой файл с расширением .txt
            for i, f in enumerate(files):
                if f.lower().endswith(self.TXT_EXT):
                    diz_file_name = os.path.join(movie_root, files[i])
                    break

        # 3) Если .txt не найден — ищем file_id.diz
        if not diz_file_name:
            if self.FILE_ID_DIZ in lower_files:
                idx = lower_files.index(self.FILE_ID_DIZ)
                diz_file_name = os.path.join(movie_root, files[idx])

        self.diz_file = diz_file_name
        return self.diz_file

    def read_movie_nfo(self, nfo_file_name):
        nfo_file_exists = xbmcvfs.exists(nfo_file_name)
        if nfo_file_exists:
            with closing(xbmcvfs.File(nfo_file_name)) as f:
                nfo_bytes = bytes(f.readBytes())
                nfo_text = nfo_bytes.decode("utf8")
            movie_element = ET.fromstring(nfo_text)
            nfo_text = movie_element.find('plot').text
        else:
            nfo_text = "File '{}'/movie.nfo not found".format(self.movie_root)
        self.nfo_text = nfo_text
        return self.nfo_text

    def read_file_id_diz(self, diz_file_name):
        """
        Читает содержимое файла описания.
        Использует кодировку windows-1251 для file_id.diz, иначе utf-8.
        """
        if not diz_file_name:
            diz_text = "File not found (searched: *.txt, file_id.diz in folder: ./)".format(self.movie_root)
            self.diz_text = diz_text
            return self.diz_text

        # Определяем кодировку по имени файла
        basename = os.path.basename(diz_file_name).lower()
        encoding = 'windows-1251' if basename == self.FILE_ID_DIZ else 'utf-8'

        diz_file_exists = xbmcvfs.exists(diz_file_name)
        if diz_file_exists:
            with closing(xbmcvfs.File(diz_file_name)) as f:
                diz_bytes = bytes(f.readBytes())
                diz_text = diz_bytes.decode(encoding, errors='replace')
        else:
            diz_text = "File '{}' not found (searched: *.txt, file_id.diz in folder: ./)".format(self.movie_root)

        self.diz_text = diz_text
        return self.diz_text

    def select_artwork(self):
        self.artwork = xbmc.getInfoLabel('ListItem.Art(fanart)')
        return self.artwork

    def get_all_images(self, item_path):
        images = []
        self.jpeg_total_count = 0
        self.jpeg_total_size = 0
        jpeg_ext = [".jpg", ".jpeg"]
        image_ext = jpeg_ext + [".png", ".tiff", ".bmp"]

        dirs, files = xbmcvfs.listdir(item_path)
        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            if ext in image_ext:
                filename_full = os.path.join(item_path, filename)
                path = pathlib.Path(filename_full)
                file_name = path.stem
                file_extension = path.suffix
                stat = xbmcvfs.Stat(filename_full)
                is_jpeg = ext in jpeg_ext
                if is_jpeg:
                    self.jpeg_total_count += 1
                    self.jpeg_total_size += stat.st_size()
                images.append({"path": filename_full, "name": file_name, "ext": file_extension, "size": stat.st_size(),
                               "is_jpeg": is_jpeg, "allowed": True})

        for sub_dir in dirs:
            sub_dir_full = os.path.join(item_path, sub_dir)
            sub_images = self.get_all_images(sub_dir_full)
            for sub_image in sub_images:
                images.append(sub_image)

        if not self.setting_include_non_jpg:
            for image in images:
                if not image["is_jpeg"]:
                    image["allowed"] = False

        if self.setting_hide_small_jpg:
            if self.jpeg_total_count > 0:
                mean_jpeg_size = self.jpeg_total_size / self.jpeg_total_count
            else:
                mean_jpeg_size = None
            for image in images:
                if image["is_jpeg"]:
                    size = image["size"]
                    size_percent = size * 100 / mean_jpeg_size
                    if size_percent < self.setting_minimum_jpg_size_percent:
                        image["allowed"] = False

        if self.setting_hide_art_images:
            for image in images:
                fn = image["name"].lower()
                is_art = ((fn == "folder"
                           or fn.endswith("banner") or fn.endswith("clearart") or fn.endswith("clearlogo")
                           or fn.endswith("discart") or fn.endswith("fanart") or fn.endswith("keyart")
                           or fn.endswith("landscape") or fn.endswith("poster"))
                          or re.search("fanart", fn) is not None or re.search("poster", fn) is not None)
                if is_art:
                    image["allowed"] = False

        xbmc.log("Selected images: '%s'" % images, xbmc.LOGDEBUG)
        self.images = images
        return self.images
