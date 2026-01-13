import xbmc
import xbmcaddon
import xbmcvfs
import xbmcgui
import threading


class SlideShow(xbmcgui.WindowXMLDialog):
    # https://github.com/xbmc/xbmc/blob/master/xbmc/input/actions/ActionIDs.h
    ACTION_TAB = [18]
    ACTION_TEXT = [59, 215]
    ACTION_TILE = [60, 216]
    ACTION_SLIDE = [61, 217]
    ACTION_LEFT = [1, 14, 17]
    ACTION_RIGHT = [2, 6, 15, 16]
    ACTION_UP = [3]
    ACTION_DOWN = [4]
    ACTION_CHANEL_UP = [184]
    ACTION_CHANEL_DOWN = [185]
    ACTION_PAUSE = [12]
    ACTION_INFO = [11]
    ACTION_ENTER = [7, 22]
    ACTION_PREVIOUS_MENU = [9, 10, 92, 21]

    OFFSET_BOX_X = 50
    OFFSET_X = 2
    OFFSET_Y = 2

    ID_BACKGROUND = 5100

    ID_GROUP_SLIDE = 5101
    ID_LIST_PICTURES = 5102

    ID_GROUP_TEXT = 5201
    ID_TEXT_BOX = 5202

    ID_GROUP_TILE = 5301

    ID_BUTTON_TEXT = 5502
    ID_BUTTON_TILE = 5503
    ID_BUTTON_SLIDE = 5504

    IMAGE_BACKGROUND_DEFAULT = "background/black.png"

    MODE_TEXT = 0
    MODE_TILE = 1
    MODE_SLIDE = 2

    def __init__(self, *args, **kwargs):
        self.addon = xbmcaddon.Addon()
        self.setting_startup_mode = int(self.addon.getSetting('startup_mode'))
        self.setting_auto_scroll_delay_seconds = int(self.addon.getSetting('auto_scroll_delay_seconds'))
        self.setting_background_use_fanart = self.addon.getSetting('background_fanart').lower() == 'true'
        self.setting_background_image = self.addon.getSetting('background_image').lower()
        self.setting_background_tint = self.addon.getSetting('background_tint')
        self.action = None
        self.images = kwargs.get('listitems')
        self.index = kwargs.get('index')
        self.fanart = kwargs.get('fanart')
        self.text = kwargs.get('text')
        self.info_handler_function = kwargs.get('info_handler_function')
        self.enter_handler_function = kwargs.get('enter_handler_function')
        self.monitor = xbmc.Monitor()
        self.auto_list_timer = None
        self.auto_scroll_pause = True
        self.background = None
        self.mode = self.setting_startup_mode
        self.count_x = 1
        self.count_y = 1
        self.image_height = 1080 - 2 * self.OFFSET_Y
        self.image_width = 1920 - self.OFFSET_BOX_X - 2 * self.OFFSET_X
        self.tile_controls = []
        self.tile_control_ext = []

    def onInit(self):
        super().onInit()
        if not self.images:
            return None
        self.setup_background()
        self.setup_text()
        self.calculate_matrix_size()
        self.setup_tile_pictures()
        self.setup_list_pictures()
        self.swith_mode()
        self.auto_list_schedule()

    def add_tile_controls(self):
        try:
            self.addControls(self.tile_controls)
        except:
            pass

    def remove_tile_controls(self):
        try:
            self.removeControls(self.tile_controls)
        except:
            pass

    def swith_mode(self):
        if self.mode == self.MODE_SLIDE:
            self.remove_tile_controls()
            self.getControl(self.ID_GROUP_TEXT).setVisible(False)
            self.getControl(self.ID_GROUP_TILE).setVisible(False)
            self.getControl(self.ID_GROUP_SLIDE).setVisible(True)
            self.setFocusId(self.ID_LIST_PICTURES)
        elif self.mode == self.MODE_TILE:
            self.getControl(self.ID_GROUP_TEXT).setVisible(False)
            self.getControl(self.ID_GROUP_SLIDE).setVisible(False)
            self.getControl(self.ID_GROUP_TILE).setVisible(True)
            self.add_tile_controls()
        elif self.mode == self.MODE_TEXT:
            self.remove_tile_controls()
            self.getControl(self.ID_GROUP_TILE).setVisible(False)
            self.getControl(self.ID_GROUP_SLIDE).setVisible(False)
            self.getControl(self.ID_GROUP_TEXT).setVisible(True)
            self.setFocusId(self.ID_TEXT_BOX)
        else:
            self.remove_tile_controls()
            self.getControl(self.ID_GROUP_TEXT).setVisible(False)
            self.getControl(self.ID_GROUP_TILE).setVisible(False)
            self.getControl(self.ID_GROUP_SLIDE).setVisible(False)

    def setup_text(self):
        # xbmc.log(f"SlideShow text: {self.text}", xbmc.LOGINFO)
        self.getControl(self.ID_TEXT_BOX).setText(self.text)

    def setup_tile_pictures(self):
        index_x = 1
        index_y = 1
        for list_item in self.images:
            image_path = list_item.getArt('img')
            left = self.OFFSET_BOX_X + self.OFFSET_X * index_x + self.image_width * (index_x - 1)
            top = self.OFFSET_Y * index_y + self.image_height * (index_y - 1)
            ci = xbmcgui.ControlImage(left, top, self.image_width, self.image_height, image_path, aspectRatio=2)
            # ci = xbmcgui.ControlButton(left, top, self.image_width, self.image_height, "", noFocusTexture=image_path)
            if index_x < self.count_x:
                index_x += 1
            else:
                index_x = 1
                index_y += 1
            self.tile_controls.append(ci)
            self.tile_control_ext.append(
                {"control": ci,
                 "id": ci.getId(),
                 "index": (index_y - 1) * self.count_x})
        # xbmc.log(f"ImageTile setup_list_pictures", xbmc.LOGINFO)

    def calculate_matrix_size(self):
        self.count_x = 1
        self.count_y = 1
        while self.count_x * self.count_y < len(self.images):
            if self.count_x <= self.count_y:
                self.count_x += 1
            else:
                self.count_y += 1
        self.image_width = (1920 - self.OFFSET_BOX_X - (self.count_x + 1) * self.OFFSET_X) // self.count_x
        self.image_height = (1080 - (self.count_y + 1) * self.OFFSET_Y) // self.count_y
        xbmc.log(f"ImageTile matrix {self.count_x} x {self.count_y}; {self.image_width} x {self.image_height}",
                 xbmc.LOGINFO)

    def setup_background(self):
        if self.setting_background_use_fanart and xbmcvfs.exists(self.fanart):
            self.background = self.fanart
        elif xbmcvfs.exists(self.setting_background_image):
            self.background = self.setting_background_image
        else:
            self.background = self.IMAGE_BACKGROUND_DEFAULT
        self.getControl(self.ID_BACKGROUND).setImage(self.background)
        if self.setting_background_tint == '0':
            tint = '0xFFFFFFFF'
        elif self.setting_background_tint == '1':
            tint = '0xFF999999'
        elif self.setting_background_tint == '2':
            tint = '0xFF555555'
        elif self.setting_background_tint == '3':
            tint = '0xFF333333'
        elif self.setting_background_tint == '4':
            tint = '0xFF111111'
        else:
            tint = '0xFFFFFFFF'
        # xbmc.log("SlideShow tint: '%s'='%s'" % (self.setting_background_tint, tint), xbmc.LOGINFO)
        self.getControl(self.ID_BACKGROUND).setColorDiffuse(tint)

    def setup_list_pictures(self):
        self.getControl(self.ID_LIST_PICTURES).addItems(self.images)
        self.getControl(self.ID_LIST_PICTURES).selectItem(self.index)

    def select_prev_image(self):
        self.index = self.getControl(self.ID_LIST_PICTURES).getSelectedPosition()
        if self.index > 0:
            self.index = self.index - 1
        else:
            self.index = len(self.images) - 1
        self.getControl(self.ID_LIST_PICTURES).selectItem(self.index)

    def select_next_image(self):
        self.index = self.getControl(self.ID_LIST_PICTURES).getSelectedPosition()
        if self.index < len(self.images):
            self.index = self.index + 1
        else:
            self.index = 0
        self.getControl(self.ID_LIST_PICTURES).selectItem(self.index)

    def auto_list_timer_event(self):
        if not self.auto_scroll_pause:
            self.select_next_image()
        self.auto_list_schedule()

    def auto_list_schedule(self):
        if not self.auto_scroll_pause and not self.monitor.abortRequested():
            self.auto_list_timer = threading.Timer(self.setting_auto_scroll_delay_seconds, self.auto_list_timer_event)
            self.auto_list_timer.start()
        else:
            self.auto_list_timer = None

    def action_handler_close(self):
        self.index = self.getControl(self.ID_LIST_PICTURES).getSelectedPosition()
        self.auto_scroll_pause = True
        self.close()

    def action_handler_pause(self):
        self.auto_scroll_pause = not self.auto_scroll_pause
        self.auto_list_schedule()

    def action_handler_left(self):
        self.auto_scroll_pause = True
        self.select_prev_image()

    def action_handler_right(self):
        self.auto_scroll_pause = True
        self.select_next_image()

    def action_handler_up(self):
        self.mode -= 1
        if self.mode < 0:
            self.mode = self.MODE_SLIDE
        self.swith_mode()

    def action_handler_down(self):
        self.mode += 1
        if self.mode > self.MODE_SLIDE:
            self.mode = 0
        self.swith_mode()

    def action_handler_text(self):
        self.mode = self.MODE_TEXT
        self.swith_mode()

    def action_handler_tile(self):
        self.mode = self.MODE_TILE
        self.swith_mode()

    def action_handler_slide(self):
        self.mode = self.MODE_SLIDE
        self.swith_mode()

    def action_go_to_image(self, control_id):
        xbmc.log(f"SlideShow control_id: '{control_id}'", xbmc.LOGINFO)
        processed = False
        for control_ext in self.tile_control_ext:
            xbmc.log(f"SlideShow control_ext_id: '{control_ext['id']}'", xbmc.LOGINFO)
            if control_ext["id"] == control_id:
                processed = True
                self.index = control_ext["index"]
                xbmc.log(f"SlideShow index: '{self.index}'", xbmc.LOGINFO)
                self.getControl(self.ID_LIST_PICTURES).selectItem(self.index)
                self.mode = self.MODE_SLIDE
                self.swith_mode()
                break
        return processed

    def onAction(self, action):
        xbmc.log(f"SlideShow action id '{action.getId()}' code '{action.getButtonCode()}'", xbmc.LOGINFO)
        if action in self.ACTION_PREVIOUS_MENU:
            self.action_handler_close()
        elif action in self.ACTION_INFO:
            pass
        elif action in self.ACTION_ENTER:
            pass
        elif action in self.ACTION_PAUSE:
            self.action_handler_pause()
        elif action in self.ACTION_LEFT:
            self.action_handler_left()
        elif action in self.ACTION_RIGHT:
            self.action_handler_right()
        elif action in self.ACTION_TAB:
            self.action_handler_up()
        elif action in self.ACTION_UP:
            self.action_handler_up()
        elif action in self.ACTION_CHANEL_UP:
            self.action_handler_up()
        elif action in self.ACTION_DOWN:
            self.action_handler_down()
        elif action in self.ACTION_CHANEL_DOWN:
            self.action_handler_down()
        elif action in self.ACTION_TEXT:
            self.action_handler_text()
        elif action in self.ACTION_TILE:
            self.action_handler_tile()
        elif action in self.ACTION_SLIDE:
            self.action_handler_slide()

    def onClick(self, controlID):
        xbmc.log(f"SlideShow onClick controlID '{controlID}'", xbmc.LOGINFO)
        if controlID == 5502:
            self.action_handler_text()
            return
        elif controlID == 5503:
            self.action_handler_tile()
            return
        elif controlID == 5504:
            self.action_handler_slide()
            return
        elif self.action_go_to_image(controlID):
            return

    def onDoubleClick(self, controlId):
        xbmc.log(f"SlideShow onDoubleClick controlId '{controlId}'", xbmc.LOGINFO)

    def onControl(self, control):
        xbmc.log(f"SlideShow onControl Control '{control}'", xbmc.LOGINFO)
