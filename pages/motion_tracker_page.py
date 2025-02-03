import time, datetime, os, copy

from .base_page import BasePage
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
# from AppKit import NSScreen
from .locator import locator as L
#from .locator.hardcode_0408 import locator as L
from .main_page import Main_Page

DELAY_TIME = 1 # sec

def _set_color(self, HexColor):
    try:
        self.color_picker_switch_category_to_RGB()
        self.double_click(L.title_designer.colors.input_hex_color)
        time.sleep(DELAY_TIME)
        self.exist(L.title_designer.colors.input_hex_color).sendKeys(HexColor)
        time.sleep(DELAY_TIME)
        self.keyboard.enter()
        time.sleep(DELAY_TIME*2)
        self.click(L.title_designer.colors.btn_close)
        time.sleep(DELAY_TIME)
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        return False
    return True

class Motion_Tracker(Main_Page, BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_in_motion_tracker(self):
        return self.exist(L.motion_tracker.main_window).AXTitle.startswith("Motion Tracker |")

    def click_object_track(self, delay_time=10):
        if not self.is_in_motion_tracker():
            logger('Not enter motion tracker. Raise Exception')
            raise Exception

        self.click(L.motion_tracker.btn_track)
        time.sleep(delay_time)
        return True

    def add_title_button(self):
        if not self.is_in_motion_tracker():
            logger('Not enter motion tracker. Raise Exception')
            raise Exception

        self.click(L.motion_tracker.btn_add_title)
        time.sleep(DELAY_TIME*2)

        # If pop up warning message (Are you sure you want) > click 'Yes'
        self.handle_removing_attached_object()

        # Verify Step: Can find text object
        if self.exist(L.motion_tracker.text_object):
            return True
        else:
            return False

    def edit_title(self, custom_title):
        self.click(L.motion_tracker.text_object)
        time.sleep(DELAY_TIME)
        self.input_text(custom_title)
        time.sleep(DELAY_TIME)

    def change_title_color(self, HexColor):
        self.click(L.motion_tracker.btn_change_color)
        return _set_color(self, HexColor)

    def handle_removing_attached_object(self, option=1):
        btn_no_yes = [L.base.confirm_dialog.btn_no, L.base.confirm_dialog.btn_yes]
        if self.exist(L.base.confirm_dialog.main_window):
            self.click(btn_no_yes[option])

    def add_pip_button(self):
        if not self.is_in_motion_tracker():
            logger('Not enter motion tracker. Raise Exception')
            raise Exception

        # Click [Add Pip] button
        self.click(L.motion_tracker.btn_add_pip)

        # If pop up warning message (Are you sure you want) > click 'Yes'
        self.handle_removing_attached_object()

        time.sleep(DELAY_TIME*2)
        # Verify Step: Can find text object
        if self.exist(L.motion_tracker.btn_import_media):
            return True
        else:
            return False

    def import_from_hard_drive(self, media_path):
        if not self.exist(L.motion_tracker.btn_import_media):
            logger('Cannot find import media clip button, raise Exception')
            raise Exception

        self.click(L.motion_tracker.btn_import_media)
        time.sleep(DELAY_TIME)
        self.select_right_click_menu('Import from Hard Drive...')
        time.sleep(DELAY_TIME)
        self.select_file(media_path)
        self.move_mouse_to_0_0()
        time.sleep(DELAY_TIME*2)

    def set_timecode(self, timecode):
        self.activate()
        elem = self.find(L.motion_tracker.timecode)
        w, h = elem.AXSize
        x, y = elem.AXPosition

        pos_click = tuple(map(int, (x + w * 0.1, y + h * 0.5)))
        self.mouse.click(*pos_click)
        time.sleep(1)
        self.keyboard.send(timecode.replace("_", ""))
        self.keyboard.enter()

    def add_effect_button(self):
        if not self.is_in_motion_tracker():
            logger('Not enter motion tracker. Raise Exception')
            raise Exception

        self.click(L.motion_tracker.btn_add_effect)
        time.sleep(DELAY_TIME*2)

        # If pop up warning message (Are you sure you want) > click 'Yes'
        self.handle_removing_attached_object()

        # Verify Step: Can find Mosaic menu
        if self.exist(L.motion_tracker.btn_cbo_mosaic):
            return True
        else:
            return False

    def add_a_tracker(self):
        if not self.is_in_motion_tracker():
            logger('Not enter motion tracker. Raise Exception')
            raise Exception

        self.click(L.motion_tracker.btn_add_a_tracker)
        time.sleep(DELAY_TIME)

    def click_ok(self):
        if not self.is_in_motion_tracker():
            logger('Not enter motion tracker. Raise Exception')
            raise Exception

        self.click(L.motion_tracker.btn_ok)
        time.sleep(DELAY_TIME*3)

        # Verify Step: Can find (Add Title) button
        if self.exist(L.motion_tracker.btn_add_title):
            return False
        else:
            return True

    def remove_tracker2(self):
        all_simple_track = self.exist(L.motion_tracker.text_trackers)
        if len(all_simple_track) < 2:
            logger('simple track only 1 track now.')
            return

        # Select track2 > Right click men > remove track
        track2_object = self.exist(L.motion_tracker.text_tracker2)
        #logger(track2_object.AXPosition)
        x, y = track2_object.AXPosition
        w, h = track2_object.AXSize
        new_x = x + w + 14
        new_y = y + 7
        self.mouse.click(new_x, new_y)
        self.right_click()

        self.select_right_click_menu('Remove Tracker')
        time.sleep(DELAY_TIME*2)
        self.handle_removing_attached_object()
        logger('Remove track 2 complete.')