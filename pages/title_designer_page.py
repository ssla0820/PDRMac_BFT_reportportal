import time, datetime, os, copy

from .base_page import BasePage, AdjustSet, KEComboSet
from .bft_Main_Page import Main_Page
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
from AppKit import NSScreen
from .locator import locator as L
from .main_page import Main_Page
from reportportal_client import step
#from .locator.hardcode_0408 import locator as L

DELAY_TIME = 1 # sec

def _checkbox_status(self, _locator, value=1, get_status=False, get_enable=False):
    try:
        target = self.exist(_locator)
        current_value = int(target.AXValue)
        current_enabled = bool(target.AXEnabled)
        if get_status:
            return current_value
        if get_enable:
            return not current_enabled
        if current_value != value:
            target.press()
            time.sleep(DELAY_TIME*1)
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        return False(f'Exception occurs. log={e}')
    return True

def _set_slider(self, _locator, value, is_int=True):
    try:
        target = self.exist(_locator)
        if is_int:
            target.AXValue = int(value)
        else:
            target.AXValue = float(value)
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        return False
    return True

def _set_edittext(self, _locator, value):
    try:
        target = self.exist(_locator)
        self.el_click(target)
        time.sleep(DELAY_TIME*1)
        target.AXValue = str(value)
        time.sleep(DELAY_TIME*1)
        self.keyboard.enter()
        time.sleep(DELAY_TIME*1)
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        return False
    return True

def _set_radio(self, _locator_radio_group, option=1, get_status=False):
    try:
        target = self.exist(_locator_radio_group[option-1])
        result = bool(int(target.AXValue))
        if get_status:
            return int(result)+1
        if not result:
            target.press()
            time.sleep(DELAY_TIME*1)
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        raise Exception(f'Exception occurs. log={e}')
    return True

def _set_option(self, _locator_cbx, _locator_group, option=1, get_status=False, path=None):
    try:
        target = self.exist(_locator_cbx)
        current_title = str(target.AXTitle)
        if get_status:
            return current_title
        else:
            self.click(_locator_cbx)
            time.sleep(DELAY_TIME*1)
            self.click(_locator_group[option-1])
            time.sleep(DELAY_TIME*1)
        if path is not None:
            time.sleep(DELAY_TIME * 1)
            self.select_file(path)
            time.sleep(DELAY_TIME * 1)
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        raise Exception
    return True


def _set_color(self, HexColor):
    try:
        self.color_picker_switch_category_to_RGB()
        self.double_click(L.title_designer.colors.input_hex_color)
        time.sleep(DELAY_TIME)
        self.exist(L.title_designer.colors.input_hex_color).sendKeys(HexColor)
        time.sleep(DELAY_TIME)
        self.keyboard.enter()
        time.sleep(DELAY_TIME)
        self.exist(L.title_designer.colors.btn_close).press()
        time.sleep(DELAY_TIME)
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        return False
    return True

def _want_to_continue(self, dialog_locator, opt=1):
    try:
        btn_no_yes = [L.title_designer.backdrop.warning.btn_no, L.title_designer.backdrop.warning.btn_yes]
        self.exist(dialog_locator)
        self.exist_click(btn_no_yes[opt])
        time.sleep(DELAY_TIME*2)
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        return False(f'Exception occurs. log={e}')
    return True


class Title_Designer(Main_Page, BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mgt = self.Motion_Graphic_Title(*args, **kwargs)
        self.backdrop = self.Backdrop(*args, **kwargs)
        self.special_effects = SpecialEffect(*args, **kwargs)
        self.motion_blur = MotionBlur(*args, **kwargs)
        self.path = Path(*args, **kwargs)
        self.adjust_path_on_canvas = AdjustPathOnCanvas(*args, **kwargs)
        self.adjust_title_on_canvas = AdjustTitleOnCanvas(*args, **kwargs)
        self.simple_timeline = Simple_Timeline(*args, **kwargs)


    def check_title_designer_page(self, ground_truth_image, area, track_index=None):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No Title designer window show up now")
                raise Exception
            if area == 'Object':
                object = self.snapshot(L.title_designer.area.object)
                result_verify = self.compare(ground_truth_image, object, similarity=0.95)
                if result_verify:
                    return True
                else:
                    return False
            elif area == 'Animation':
                animation = self.snapshot(L.title_designer.area.animation)
                result_verify = self.compare(ground_truth_image, animation, similarity=0.95)
                if result_verify:
                    return True
                else:
                    return False
            elif area == 'Designer Tracks':
                track = self.snapshot([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW'}, {'AXRole': 'AXRow', 'index': track_index}])
                result_verify = self.compare(ground_truth_image, track, similarity=0.95)
                if result_verify:
                    return True
                else:
                    return False
            elif area == 'Preview':
                preview = self.snapshot(L.title_designer.area.frame_preview)
                result_verify = self.compare(ground_truth_image, preview, similarity=0.95)
                if result_verify:
                    return True
                else:
                    return False
            elif area == 'designer window':
                designer_window = self.snapshot(L.title_designer.area.window_title_designer)
                print(f'{designer_window=}')
                result_verify = self.compare(ground_truth_image, designer_window, similarity=0.95)
                if result_verify:
                    return True
                else:
                    return False
            else:
                logger('Input the wrong augment')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def get_title(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            title = self.exist(L.title_designer.area.window_title_designer).AXTitle
            return title[17:]
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def get_full_title(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            title = self.exist(L.title_designer.area.window_title_designer).AXTitle
            return title
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Maximize/ Minimize Title Designer Window')
    def click_maximize_btn(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_maximize)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_close_btn(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_close)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Set Time Code')
    def set_timecode(self, timecode):
        self.activate()
        elem = self.find(L.title_designer.area.timecode)
        w, h = elem.AXSize
        x, y = elem.AXPosition

        pos_click = tuple(map(int, (x + w * 0.1, y + h * 0.5)))
        self.mouse.click(*pos_click)
        time.sleep(1)
        self.keyboard.send(timecode.replace("_", ""))
        self.keyboard.enter()
        time.sleep(DELAY_TIME)

    def get_timecode(self):
        try:
            timecode = self.exist(L.title_designer.area.timecode).AXValue
            return timecode
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True
    
    @step('[Action][Title Designer] Get Title Text Content')
    def get_title_text_content(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            title_text = self.exist(L.title_designer.area.edittext_text_content).AXValue
            return title_text
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    @step('[Action][Title Designer] Drag Vertical Slider')
    def drag_object_vertical_slider(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist(L.title_designer.object.slider_vertical_track).AXValue = float(value)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def drag_animation_vertical_slider(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist(L.title_designer.animation.slider_vertical_track).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_simple_track_vertical_slider(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist(L.title_designer.simple_track.slider_vertical_track).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_simple_timeline_track_to_lager(self, height=30):
        try:
            x, y = self.exist(L.pip_designer.scroller_removed_scroll_view).AXPosition
            new_y = y - 3
            self.mouse.move(x, new_y)
            time.sleep(DELAY_TIME * 0.5)
            self.drag_mouse((x, new_y), (x, new_y - height))
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_specific_simple_track(self, track_index):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW'}, {'AXRole': 'AXRow', 'index': track_index}])
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True
    
    @step('[Action][Title Designer] Insert Title')
    def insert_title(self, text):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_insert_title)
            #self.exist(L.title_designer.area.edittext_text_content).AXValue = str(text)
            self.keyboard.send(text)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True
    
    @step('[Action][Title Designer] Edit Title')
    def edit_object_title(self, strText):
        target = self.exist(L.title_designer.area.edittext_text_content)
        self.el_click(target)
        self.tap_SelectAll_hotkey()
        time.sleep(DELAY_TIME)
        target.AXValue = str(strText)
        time.sleep(DELAY_TIME * 1.5)

    @step('[Action][Title Designer] Click [Insert Particle] Button')
    def click_insert_particle_btn(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_insert_particle)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Insert Particle')
    def insert_particle(self, menu_index, particle_index):
        try:
            if not self.exist(L.title_designer.particle.window_insert_particle):
                logger("No insert particle window show up")
                raise Exception("No insert particle window show up")
            time.sleep(DELAY_TIME*3)
            self.exist_click(L.title_designer.particle.chx_particle_menu)
            if menu_index == 0:
                self.click(L.title_designer.particle.option_all_content)
            elif menu_index == 1:
                self.click(L.title_designer.particle.option_custom)
            elif menu_index == 2:
                self.click(L.title_designer.particle.option_downloaded)
            elif menu_index == 3:
                self.click(L.title_designer.particle.option_general)
            elif menu_index == 4:
                self.click(L.title_designer.particle.option_holidays)
            elif menu_index == 5:
                self.click(L.title_designer.particle.option_nature)
            elif menu_index == 6:
                self.click(L.title_designer.particle.option_frame)
            elif menu_index == 7:
                self.click(L.title_designer.particle.option_love)
            elif menu_index == 8:
                self.click(L.title_designer.particle.option_weather)
            else:
                logger("Input the wrong menu_index")
                raise Exception("Input the wrong menu_index")
            time.sleep(DELAY_TIME * 2)
            self.click({'AXIdentifier': 'EntityCollectionViewItem', 'index': particle_index})

            for x in range(500):
                check_ok_btn = self.exist(L.title_designer.particle.btn_ok)
                if check_ok_btn.AXEnabled:
                    break
                else:
                    time.sleep(DELAY_TIME)

            if not check_ok_btn.AXEnabled:
                logger('IAD template cannot download ready after delay 500 sec')
                raise Exception('IAD template cannot download ready after delay 500 sec')
            self.click(L.title_designer.particle.btn_ok)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Click [Insert Image] Button')
    def click_insert_image_btn(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_insert_image)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Insert Image')
    def insert_image(self, file_path):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_insert_image)
            time.sleep(DELAY_TIME*2)
            self.select_file(file_path)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Click [Insert Background] Button')
    def click_insert_background_btn(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_insert_background)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Insert Background')
    def insert_background(self, file_path):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            time.sleep(DELAY_TIME * 2)
            self.click(L.title_designer.btn_insert_background)
            time.sleep(DELAY_TIME * 2)
            self.select_file(file_path)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Adjust setting for [Insert Background]')
    def insert_background_adjust_setting(self, index):
        try:
            if not self.exist(L.title_designer.background.window_background_adjust_setting):
                logger("No background adjust setting window")
                raise Exception("No background adjust setting window")
            if index == 0:
                self.exist_click(L.title_designer.background.btn_stretch)
            elif index == 1:
                self.exist_click(L.title_designer.background.btn_letterbox)
            elif index == 2:
                self.exist_click(L.title_designer.background.btn_crop)
            time.sleep(DELAY_TIME*2)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Click [Delete Background] Button')
    def click_delete_background_btn(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_delete_background)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Switch mode')
    def switch_mode(self, mode=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            if mode == 1:
                self.exist_click(L.title_designer.btn_basic)
            elif mode == 2:
                self.exist_click(L.title_designer.btn_advanced)
            time.sleep(DELAY_TIME*2)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def get_current_mode(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            a = 'Express'
            b = 'Advanced'
            if self.exist(L.title_designer.btn_align_object):
                return b
            else:
                return a
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception


    def switch_timecode_mode(self, mode=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            if mode == 1:
                self.exist_click(L.title_designer.btn_clip_timecode)
            elif mode == 2:
                self.exist_click(L.title_designer.btn_video_timecode)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Click [Object] Tab')
    def click_object_tab(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_object)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
    
    @step('[Action][Title Designer] Click animation tab')
    def click_animation_tab(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_animation)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Click [Motion] Tab')
    def click_motion_tab(self):
        return bool(self.exist_click(L.title_designer.btn_motion))

    @step('[Action][Title Designer] Click [OK] button')
    def click_ok(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_ok)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
    @step('[Action][Title Designer] Set template name when saving template')
    def click_custom_name_ok(self, name):
        try:
            if not self.exist(L.title_designer.save_as_template.window_save_as_template, timeout=10):
                logger("No save as template window show up")
                raise Exception("No save as template window show up")
            self.exist_click(L.title_designer.save_as_template.edittext_save_as_template)
            self.keyboard.send(name)
            self.exist_click(L.title_designer.save_as_template.btn_ok)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Click [Cancel] Button')
    def click_cancel(self, option=None):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_cancel)
            if self.exist(L.title_designer.cancel.text_dialog_description):
                if option == 0:
                   self.exist_click(L.title_designer.cancel.btn_yes)
                elif option == 1:
                   self.exist_click(L.title_designer.cancel.btn_no)
                elif option == 2:
                   self.exist_click(L.title_designer.cancel.btn_cancel)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Save template as')
    def save_as_name(self, name, click_ok=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_save_as)
            self.exist_click(L.title_designer.save_as_template.edittext_save_as_template)
            self.keyboard.send(name)
            if click_ok:
                self.click(L.title_designer.save_as_template.btn_ok)
                time.sleep(DELAY_TIME * 1.5)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def save_as_set_slider(self, value):
        try:
            if not self.exist(L.title_designer.save_as_template.window_save_as_template):
                logger("No save as template window show up")
                raise Exception
            self.exist(L.title_designer.save_as_template.slider).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def save_as_click_cancel(self):
        try:
            if not self.exist(L.title_designer.save_as_template.window_save_as_template):
                logger("No save as template window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_save_as_cancel)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Share to DZ')
    def share_to_dz(self, name, upload_option, style, tags, collection, description, verify_dz_link=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_share)
            if self.exist(L.title_designer.save_as_template.edittext_save_as_template, timeout=10):
                self.exist_click(L.title_designer.save_as_template.edittext_save_as_template)
            self.keyboard.send(name)
            self.exist_click(L.title_designer.save_as_template.btn_ok)
            if self.exist(L.title_designer.share.text_auto_signin):
                self.exist_click(L.title_designer.share.btn_yes_auto_signin)
            while not self.exist(L.title_designer.share.window_upload):
                time.sleep(1)
            self.exist_click(L.title_designer.share.cbx_upload_to)
            if upload_option == 0:
                self.exist_click(L.title_designer.share.option_cloud_directzone)
            elif upload_option == 1:
                self.exist_click(L.title_designer.share.option_cloud)
            elif upload_option == 2:
                self.exist_click(L.title_designer.share.option_directzone)
            self.exist_click(L.title_designer.share.cbx_style)
            self.exist_click({'AXRole': 'AXStaticText', 'AXValue': style})
            self.exist_click(L.title_designer.share.edittext_tags)
            self.keyboard.send(tags)
            self.exist_click(L.title_designer.share.edittext_collection)
            self.keyboard.send(collection)
            self.exist_click(L.title_designer.share.edittext_description)
            self.keyboard.send(description)
            self.exist_click(L.title_designer.share.btn_next)
            if self.exist(L.title_designer.share.chx_confirm):
                if self.exist(L.title_designer.share.chx_confirm).AXValue == 0:
                    self.exist_click(L.title_designer.share.chx_confirm)
                    time.sleep(DELAY_TIME)
                    self.exist_click(L.title_designer.share.btn_next)
            while self.exist(L.title_designer.share.btn_next):
                time.sleep(1)
            for x in range(500):
                if self.exist(L.title_designer.share.btn_finish):
                    time.sleep(1)
                    if verify_dz_link:
                        self.click(L.upload_cloud_dz.upload_view_DZ)
                        time.sleep(DELAY_TIME*3)
                        self.activate()
                        time.sleep(DELAY_TIME*6)
                    self.click(L.title_designer.share.btn_finish)
                    break
                else:
                    time.sleep(1)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_share(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_share)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_viewer_zoom_menu(self, value='Fit'):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.viewer_zoom.cbx_viewer_zoom)
            self.exist_click({'AXRole': 'AXStaticText', 'AXValue': value})
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_zoom_out(self, times=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            x, y = self.exist(L.title_designer.btn_zoom_out).AXPosition
            self.mouse.move(x,y)
            self.mouse.click(times=times)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_zoom_in(self, times=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            x, y = self.exist(L.title_designer.btn_zoom_in).AXPosition
            self.mouse.move(x, y)
            self.mouse.click(times=times)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Click preview operation -- play, pause, stop, previous frame, next frame, fast forward')
    def click_preview_operation(self, operation):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            if operation == 'Play':
                self.exist_click(L.title_designer.operation.btn_play)
            elif operation == 'Pause':
                self.exist_click(L.title_designer.operation.btn_pause)
            elif operation == 'Stop':
                self.exist_click(L.title_designer.operation.btn_stop)
            elif operation == 'Previous_Frame':
                self.exist_click(L.title_designer.operation.btn_previous_frame)
            elif operation == 'Next_Frame':
                self.exist_click(L.title_designer.operation.btn_next_frame)
            elif operation == 'Fast_Forward':
                self.exist_click(L.title_designer.operation.btn_fast_forward)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
    
    @step('[Action][Title Designer] Apply Character Presets')
    def apply_character_presets(self, index, character_type=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.character_presets.btn_character_presets).AXValue == 0:
                self.exist_click(L.title_designer.character_presets.btn_character_presets)
            self.exist_click(L.title_designer.character_presets.cbx_character_types)
            if character_type == 1:
                self.exist_click(L.title_designer.character_presets.option_default)
            elif character_type == 2:
                self.exist_click(L.title_designer.character_presets.option_my_presets)
            self.exist_click({'AXIdentifier': 'TitleCharPresetCollectionViewItem', 'index': index})
            time.sleep(DELAY_TIME*2)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Set Font Type')
    def set_font_type(self, type):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.font_paragraph.btn_font_paragraph).AXValue == 0:
                self.exist_click(L.title_designer.font_paragraph.btn_font_paragraph)
            self.exist_click(L.title_designer.font_paragraph.cbx_font)
            self.mouse.click(times=3)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(type)
            self.exist_click(L.title_designer.font_paragraph.btn_font)
            self.exist_click(L.title_designer.font_paragraph.btn_font)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Set Font Size')
    def set_font_size(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.font_paragraph.btn_font_paragraph).AXValue == 0:
                self.exist_click(L.title_designer.font_paragraph.btn_font_paragraph)
            self.exist_click(L.title_designer.font_paragraph.cbx_font_size)
            self.mouse.click(times=3)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(value)
            self.exist_click(L.title_designer.font_paragraph.btn_font_size)
            self.exist_click(L.title_designer.font_paragraph.btn_font_size)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Set Line Spacing Amount')
    def set_line_spacing_amount(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.font_paragraph.btn_font_paragraph).AXValue == 0:
                self.exist_click(L.title_designer.font_paragraph.btn_font_paragraph)
            self.exist_click(L.title_designer.font_paragraph.cbx_line_spacing_amount)
            self.mouse.click(times=3)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(value)
            self.exist_click(L.title_designer.font_paragraph.btn_line_spacing_amount)
            self.exist_click(L.title_designer.font_paragraph.btn_line_spacing_amount)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Set Text Spacing Amount')
    def set_text_spacing_amount(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.font_paragraph.btn_font_paragraph).AXValue == 0:
                self.exist_click(L.title_designer.font_paragraph.btn_font_paragraph)
            self.exist_click(L.title_designer.font_paragraph.cbx_text_spacing_amount)
            self.mouse.click(times=3)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(value)
            self.exist_click(L.title_designer.font_paragraph.btn_text_spacing_amount)
            self.exist_click(L.title_designer.font_paragraph.btn_text_spacing_amount)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Set Font Face Color')
    def set_font_face_color(self, red='255', green='255', blue='255'):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.font_paragraph.btn_font_paragraph).AXValue == 0:
                self.exist_click(L.title_designer.font_paragraph.btn_font_paragraph)
            self.exist_click(L.title_designer.font_paragraph.btn_font_color)
            self.color_picker_switch_category_to_RGB()
            self.exist_click(L.title_designer.font_paragraph.edittext_red)
            self.mouse.click(times=2)
            self.keyboard.send(red)
            self.exist_click(L.title_designer.font_paragraph.edittext_green)
            self.mouse.click(times=2)
            self.keyboard.send(green)
            self.exist_click(L.title_designer.font_paragraph.edittext_blue)
            self.mouse.click(times=2)
            self.keyboard.send(blue)
            self.press_enter_key()
            self.exist_click(L.title_designer.font_paragraph.btn_close)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Set Kerning Check')
    def set_kerning_check(self, bCheck=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.font_paragraph.btn_font_paragraph).AXValue == 0:
                self.exist_click(L.title_designer.font_paragraph.btn_font_paragraph)
            value = self.exist(L.title_designer.font_paragraph.chx_kerning).AXValue
            if value == 1 and bCheck == 1:
                return True
            elif value == 0 and bCheck == 1:
                self.exist_click(L.title_designer.font_paragraph.chx_kerning)
            elif value == 1 and bCheck == 0:
                self.exist_click(L.title_designer.font_paragraph.chx_kerning)
            elif value == 0 and bCheck == 0:
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_bold_btn(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.font_paragraph.btn_font_paragraph).AXValue == 0:
                self.exist_click(L.title_designer.font_paragraph.btn_font_paragraph)
            self.exist_click(L.title_designer.font_paragraph.btn_bold)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_italic_btn(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.font_paragraph.btn_font_paragraph).AXValue == 0:
                self.exist_click(L.title_designer.font_paragraph.btn_font_paragraph)
            self.exist_click(L.title_designer.font_paragraph.btn_italic)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Set Align')
    def set_align(self, type):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.font_paragraph.btn_font_paragraph).AXValue == 0:
                self.exist_click(L.title_designer.font_paragraph.btn_font_paragraph)
            if type == 1:
                self.exist_click(L.title_designer.font_paragraph.btn_align_left)
            elif type == 2:
                self.exist_click(L.title_designer.font_paragraph.btn_align_center)
            elif type == 3:
                self.exist_click(L.title_designer.font_paragraph.btn_align_right)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Set Check Font Face')
    def set_check_font_face(self, bCheck=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_object)
            value = self.exist(L.title_designer.font_face.chx_font_face).AXValue
            if value == 1 and bCheck == 1:
                return True
            elif value == 0 and bCheck == 1:
                self.exist_click(L.title_designer.font_face.chx_font_face)
            elif value == 1 and bCheck == 0:
                self.exist_click(L.title_designer.font_face.chx_font_face)
            elif value == 0 and bCheck == 0:
                return True
            time.sleep(DELAY_TIME * 2)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
    @step('[Action][Title Designer] Enable/ Disable Check Shadow')
    def set_check_shadow(self, bCheck=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_object)
            value = self.exist(L.title_designer.shadow.chx_shadow).AXValue
            if value == 1 and bCheck == 1:
                return True
            elif value == 0 and bCheck == 1:
                self.exist_click(L.title_designer.shadow.chx_shadow)
            elif value == 1 and bCheck == 0:
                self.exist_click(L.title_designer.shadow.chx_shadow)
            elif value == 0 and bCheck == 0:
                return True
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def set_check_border(self, bCheck=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            value = self.exist(L.title_designer.border.chx_border).AXValue
            if value == 1 and bCheck == 1:
                return True
            elif value == 0 and bCheck == 1:
                self.exist_click(L.title_designer.border.chx_border)
            elif value == 1 and bCheck == 0:
                self.exist_click(L.title_designer.border.chx_border)
            elif value == 0 and bCheck == 0:
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_font_face_blur_slider(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.font_face.btn_font_face).AXValue == 0:
                self.exist_click(L.title_designer.font_face.btn_font_face)
            self.exist(L.title_designer.font_face.slider_blur).AXValue = int(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def input_font_face_blur_value(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.font_face.btn_font_face).AXValue == 0:
                self.exist_click(L.title_designer.font_face.btn_font_face)
            self.exist_click(L.title_designer.font_face.edittext_blur)
            self.mouse.click(times=3)
            self.keyboard.send(value)
            self.exist_click(L.title_designer.font_face.text_blur)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_font_face_blur_arrow_btn(self, option):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.font_face.btn_font_face).AXValue == 0:
               self.exist_click(L.title_designer.font_face.btn_font_face)
            if option == 0:
                self.exist_click(L.title_designer.font_face.stepper_blur_levels_up)
            elif option == 1:
                self.exist_click(L.title_designer.font_face.stepper_blur_levels_down)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_font_face_opacity_slider(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.font_face.btn_font_face).AXValue == 0:
                self.exist_click(L.title_designer.font_face.btn_font_face)
            self.exist(L.title_designer.font_face.slider_opacity).AXValue = int(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def input_font_face_opacity_value(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.font_face.btn_font_face).AXValue == 0:
                self.exist_click(L.title_designer.font_face.btn_font_face)
            self.exist_click(L.title_designer.font_face.edittext_opacity)
            self.mouse.click(times=3)
            self.keyboard.send(value)
            self.exist_click(L.title_designer.font_face.text_opacity)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_font_face_opacity_arrow_btn(self, option):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.font_face.btn_font_face).AXValue == 0:
               self.exist_click(L.title_designer.font_face.btn_font_face)
            if option == 0:
                self.exist_click(L.title_designer.font_face.stepper_opacity_levels_up)
            elif option == 1:
                self.exist_click(L.title_designer.font_face.stepper_opacity_levels_down)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def apply_font_face_uniform_color(self, red='255', green='255', blue='255'):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.font_face.btn_font_face).AXValue == 0:
               self.exist_click(L.title_designer.font_face.btn_font_face)
            self.exist_click(L.title_designer.font_face.cbx_fill_type)
            self.exist_click(L.title_designer.font_face.option_uniform_color)
            self.exist_click(L.title_designer.font_face.btn_uniform_color)
            self.color_picker_switch_category_to_RGB()
            self.exist_click(L.title_designer.font_face.edittext_red)
            self.mouse.click(times=2)
            self.keyboard.send(red)
            self.exist_click(L.title_designer.font_face.edittext_green)
            self.mouse.click(times=2)
            self.keyboard.send(green)
            self.exist_click(L.title_designer.font_face.edittext_blue)
            self.mouse.click(times=2)
            self.keyboard.send(blue)
            self.exist_click(L.title_designer.font_face.edittext_red)
            self.exist_click(L.title_designer.font_face.btn_close)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def apply_font_face_2_color(self, red1='255', green1='255', blue1='255', red2='255', green2='255', blue2='255'):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.font_face.btn_font_face).AXValue == 0:
               self.exist_click(L.title_designer.font_face.btn_font_face)
            self.exist_click(L.title_designer.font_face.cbx_fill_type)
            self.exist_click(L.title_designer.font_face.option_gradient_color)
            self.exist_click(L.title_designer.font_face.btn_begin_with)
            self.color_picker_switch_category_to_RGB()
            self.exist_click(L.title_designer.font_face.edittext_red)
            self.mouse.click(times=2)
            self.keyboard.send(red1)
            self.exist_click(L.title_designer.font_face.edittext_green)
            self.mouse.click(times=2)
            self.keyboard.send(green1)
            self.exist_click(L.title_designer.font_face.edittext_blue)
            self.mouse.click(times=2)
            self.keyboard.send(blue1)
            self.exist_click(L.title_designer.font_face.edittext_red)
            self.exist_click(L.title_designer.font_face.btn_close)
            self.exist_click(L.title_designer.font_face.btn_end_with)
            self.color_picker_switch_category_to_RGB()
            self.exist_click(L.title_designer.font_face.edittext_red)
            self.mouse.click(times=2)
            self.keyboard.send(red2)
            self.exist_click(L.title_designer.font_face.edittext_green)
            self.mouse.click(times=2)
            self.keyboard.send(green2)
            self.exist_click(L.title_designer.font_face.edittext_blue)
            self.mouse.click(times=2)
            self.keyboard.send(blue2)
            self.exist_click(L.title_designer.font_face.edittext_red)
            self.exist_click(L.title_designer.font_face.btn_close)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def apply_font_face_4_color(self, left_top_hex, right_top_hex, left_bottom_hex, right_bottom_hex):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.click(L.title_designer.font_face.colorpicker_left_top)
            _set_color(self, left_top_hex)
            self.click(L.title_designer.font_face.colorpicker_right_top)
            _set_color(self, right_top_hex)
            self.click(L.title_designer.font_face.colorpicker_left_bottom)
            _set_color(self, left_bottom_hex)
            self.click(L.title_designer.font_face.colorpicker_right_bottom)
            _set_color(self, right_bottom_hex)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def apply_font_face_fill_type_to_gradient(self):
        if self.exist(L.title_designer.font_face.btn_font_face).AXValue == 0:
            self.exist_click(L.title_designer.font_face.btn_font_face)
        self.click(L.title_designer.font_face.cbx_fill_type)
        self.click(L.title_designer.font_face.option_gradient_color)
        time.sleep(DELAY_TIME)

    def apply_font_face_gradient_style(self, option):
        # option = 1: Linear, 2: Radial, 3: Corner
        if (option < 1) or (option > 3):
            logger(f'Invalid paramter {option}')
            return False
        btn_select_style = [0, L.title_designer.font_face.option_gradient_linear, L.title_designer.font_face.option_gradient_radial, L.title_designer.font_face.option_gradient_corner]
        self.click(btn_select_style[option])
        time.sleep(DELAY_TIME)
    
    @step('[Action][Title Designer] Enable/Disable Border')
    def apply_border(self, bApply):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_object)
            value = self.exist(L.title_designer.border.chx_border).AXValue
            if value == 0 and bApply == 0:
                return True
            elif value == 0 and bApply == 1:
                self.exist_click(L.title_designer.border.chx_border)
            elif value == 1 and bApply == 1:
                return True
            elif value == 1 and bApply == 0:
                self.exist_click(L.title_designer.border.chx_border)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def drag_border_size_slider(self, value, image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if image == 0:
                if self.exist(L.title_designer.border.btn_border).AXValue == 0:
                    self.exist_click(L.title_designer.border.btn_border)
            elif image == 1:
                if self.exist(L.title_designer.border.btn_image_border).AXValue == 0:
                    self.exist_click(L.title_designer.border.btn_image_border)
            self.exist(L.title_designer.border.slider_size).AXValue = int(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def input_border_size_value(self, value, image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if image == 0:
                if self.exist(L.title_designer.border.btn_border).AXValue == 0:
                    self.exist_click(L.title_designer.border.btn_border)
            elif image == 1:
                if self.exist(L.title_designer.border.btn_image_border).AXValue == 0:
                    self.exist_click(L.title_designer.border.btn_image_border)
            self.exist_click(L.title_designer.border.edittext_size)
            self.mouse.click(times=3)
            self.keyboard.send(value)
            self.exist_click(L.title_designer.border.text_size)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_size_value_arrow_btn(self, value, image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if image == 0:
                if self.exist(L.title_designer.border.btn_border).AXValue == 0:
                    self.exist_click(L.title_designer.border.btn_border)
            elif image == 1:
                if self.exist(L.title_designer.border.btn_image_border).AXValue == 0:
                    self.exist_click(L.title_designer.border.btn_image_border)
            if value == 0:
                self.exist_click(L.title_designer.border.stepper_size_value_up)
            elif value == 1:
                self.exist_click(L.title_designer.border.stepper_size_value_down)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_border_depth_slider(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception

            self.exist(L.title_designer.border.slider_depth).AXValue = int(value)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_border_blur_slider(self, value, image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if image == 0:
                if self.exist(L.title_designer.border.btn_border).AXValue == 0:
                    self.exist_click(L.title_designer.border.btn_border)
            elif image == 1:
                if self.exist(L.title_designer.border.btn_image_border).AXValue == 0:
                    self.exist_click(L.title_designer.border.btn_image_border)
            self.exist(L.title_designer.border.slider_blur).AXValue = int(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def input_border_blur_value(self, value, image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if image == 0:
                if self.exist(L.title_designer.border.btn_border).AXValue == 0:
                    self.exist_click(L.title_designer.border.btn_border)
                self.exist_click(L.title_designer.border.edittext_blur)
                self.mouse.click(times=3)
                self.keyboard.send(value)
                self.exist_click(L.title_designer.border.text_blur)
            elif image == 1:
                if self.exist(L.title_designer.border.btn_image_border).AXValue == 0:
                    self.exist_click(L.title_designer.border.btn_image_border)
                self.exist_click(L.title_designer.border.edittext_image_blur)
                self.mouse.click(times=3)
                self.keyboard.send(value)
                self.exist_click(L.title_designer.border.text_blur)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_border_blur_arrow_btn(self, value, image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if image == 0:
                if self.exist(L.title_designer.border.btn_border).AXValue == 0:
                    self.exist_click(L.title_designer.border.btn_border)
                if value == 0:
                    self.exist_click(L.title_designer.border.stepper_blur_value_up)
                elif value == 1:
                    self.exist_click(L.title_designer.border.stepper_blur_value_down)
            elif image == 1:
                if self.exist(L.title_designer.border.btn_image_border).AXValue == 0:
                    self.exist_click(L.title_designer.border.btn_image_border)
                if value == 0:
                    self.exist_click(L.title_designer.border.stepper_image_blur_value_up)
                elif value == 1:
                    self.exist_click(L.title_designer.border.stepper_image_blur_value_down)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_border_opacity_slider(self, value, image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if image == 0:
                if self.exist(L.title_designer.border.btn_border).AXValue == 0:
                    self.exist_click(L.title_designer.border.btn_border)
            elif image == 1:
                if self.exist(L.title_designer.border.btn_image_border).AXValue == 0:
                    self.exist_click(L.title_designer.border.btn_image_border)
            self.exist(L.title_designer.border.slider_opacity).AXValue = int(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def input_border_opacity_value(self, value, image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if image == 0:
                if self.exist(L.title_designer.border.btn_border).AXValue == 0:
                    self.exist_click(L.title_designer.border.btn_border)
            elif image == 1:
                if self.exist(L.title_designer.border.btn_image_border).AXValue == 0:
                    self.exist_click(L.title_designer.border.btn_image_border)
            self.exist_click(L.title_designer.border.edittext_opacity)
            self.mouse.click(times=3)
            self.keyboard.send(value)
            self.exist_click(L.title_designer.border.text_opacity)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_border_opacity_value_arrow_btn(self, value, image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if image == 0:
                if self.exist(L.title_designer.border.btn_border).AXValue == 0:
                    self.exist_click(L.title_designer.border.btn_border)
            elif image == 1:
                if self.exist(L.title_designer.border.btn_image_border).AXValue == 0:
                    self.exist_click(L.title_designer.border.btn_image_border)
            if value == 0:
                self.exist_click(L.title_designer.border.stepper_opacity_value_up)
            elif value == 1:
                self.exist_click(L.title_designer.border.stepper_opacity_value_down)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def apply_border_uniform_color(self, red='255', green='255', blue='255', image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if image == 0:
                if self.exist(L.title_designer.border.btn_border).AXValue == 0:
                    self.exist_click(L.title_designer.border.btn_border)
            elif image == 1:
                if self.exist(L.title_designer.border.btn_image_border).AXValue == 0:
                    self.exist_click(L.title_designer.border.btn_image_border)
            self.exist_click(L.title_designer.border.cbx_fill_type)
            self.exist_click(L.title_designer.border.option_uniform_color)
            self.exist_click(L.title_designer.border.btn_uniform_color)
            self.color_picker_switch_category_to_RGB()
            self.exist_click(L.title_designer.border.edittext_red)
            self.mouse.click(times=2)
            self.keyboard.send(red)
            self.exist_click(L.title_designer.border.edittext_green)
            self.mouse.click(times=2)
            self.keyboard.send(green)
            self.exist_click(L.title_designer.border.edittext_blue)
            self.mouse.click(times=2)
            self.keyboard.send(blue)
            self.exist_click(L.title_designer.border.edittext_red)
            self.exist_click(L.title_designer.border.btn_close)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def apply_border_2_color(self, red1='255', green1='255', blue1='255', red2='255', green2='255', blue2='255', image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if image == 0:
                if self.exist(L.title_designer.border.btn_border).AXValue == 0:
                    self.exist_click(L.title_designer.border.btn_border)
            elif image == 1:
                if self.exist(L.title_designer.border.btn_image_border).AXValue == 0:
                    self.exist_click(L.title_designer.border.btn_image_border)
            self.exist_click(L.title_designer.border.cbx_fill_type)
            self.exist_click(L.title_designer.border.option_2_color_gradient)
            self.exist_click(L.title_designer.border.btn_begin_with)
            self.color_picker_switch_category_to_RGB()
            self.exist_click(L.title_designer.border.edittext_red)
            self.mouse.click(times=2)
            self.keyboard.send(red1)
            self.exist_click(L.title_designer.border.edittext_green)
            self.mouse.click(times=2)
            self.keyboard.send(green1)
            self.exist_click(L.title_designer.border.edittext_blue)
            self.mouse.click(times=2)
            self.keyboard.send(blue1)
            self.exist_click(L.title_designer.border.edittext_red)
            self.exist_click(L.title_designer.border.btn_close)
            self.exist_click(L.title_designer.border.btn_end_with)
            self.color_picker_switch_category_to_RGB()
            self.exist_click(L.title_designer.border.edittext_red)
            self.mouse.click(times=2)
            self.keyboard.send(red2)
            self.exist_click(L.title_designer.border.edittext_green)
            self.mouse.click(times=2)
            self.keyboard.send(green2)
            self.exist_click(L.title_designer.border.edittext_blue)
            self.mouse.click(times=2)
            self.keyboard.send(blue2)
            self.exist_click(L.title_designer.border.edittext_red)
            self.exist_click(L.title_designer.border.btn_close)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def apply_border_4_color(self, red1='255', green1='255', blue1='255', red2='255', green2='255', blue2='255',
                      red3='255', green3='255', blue3='255', red4='255', green4='255', blue4='255', image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if image == 0:
                if self.exist(L.title_designer.border.btn_border).AXValue == 0:
                    self.exist_click(L.title_designer.border.btn_border)
            elif image == 1:
                if self.exist(L.title_designer.border.btn_image_border).AXValue == 0:
                    self.exist_click(L.title_designer.border.btn_image_border)
            self.exist_click(L.title_designer.border.cbx_fill_type)
            self.exist_click(L.title_designer.border.option_4_color_gradient)
            x, y = self.exist(L.title_designer.border.text_4_color).AXPosition
            self.mouse.move(int(x+10), int(y+30))
            self.mouse.click()
            self.color_picker_switch_category_to_RGB()
            self.exist_click(L.title_designer.border.edittext_red)
            self.mouse.click(times=2)
            self.keyboard.send(red1)
            self.exist_click(L.title_designer.border.edittext_green)
            self.mouse.click(times=2)
            self.keyboard.send(green1)
            self.exist_click(L.title_designer.border.edittext_blue)
            self.mouse.click(times=2)
            self.keyboard.send(blue1)
            self.exist_click(L.title_designer.border.edittext_red)
            self.exist_click(L.title_designer.border.btn_close)
            self.mouse.move(int(x+170), int(y+30))
            self.mouse.click()
            self.color_picker_switch_category_to_RGB()
            self.exist_click(L.title_designer.border.edittext_red)
            self.mouse.click(times=2)
            self.keyboard.send(red2)
            self.exist_click(L.title_designer.border.edittext_green)
            self.mouse.click(times=2)
            self.keyboard.send(green2)
            self.exist_click(L.title_designer.border.edittext_blue)
            self.mouse.click(times=2)
            self.keyboard.send(blue2)
            self.exist_click(L.title_designer.border.edittext_red)
            self.exist_click(L.title_designer.border.btn_close)
            self.mouse.move(int(x + 10), int(y + 75))
            self.mouse.click()
            self.color_picker_switch_category_to_RGB()
            self.exist_click(L.title_designer.border.edittext_red)
            self.mouse.click(times=2)
            self.keyboard.send(red3)
            self.exist_click(L.title_designer.border.edittext_green)
            self.mouse.click(times=2)
            self.keyboard.send(green3)
            self.exist_click(L.title_designer.border.edittext_blue)
            self.mouse.click(times=2)
            self.keyboard.send(blue3)
            self.exist_click(L.title_designer.border.edittext_red)
            self.exist_click(L.title_designer.border.btn_close)
            self.mouse.move(int(x + 170), int(y + 75))
            self.mouse.click()
            self.color_picker_switch_category_to_RGB()
            self.exist_click(L.title_designer.border.edittext_red)
            self.mouse.click(times=2)
            self.keyboard.send(red4)
            self.exist_click(L.title_designer.border.edittext_green)
            self.mouse.click(times=2)
            self.keyboard.send(green4)
            self.exist_click(L.title_designer.border.edittext_blue)
            self.mouse.click(times=2)
            self.keyboard.send(blue4)
            self.exist_click(L.title_designer.border.edittext_red)
            self.exist_click(L.title_designer.border.btn_close)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True
    @step('[Action][Title Designer] Enable/ Disable Check Shadow') 
    def apply_shadow(self, bApply):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_object)
            value = self.exist(L.title_designer.shadow.chx_shadow).AXValue
            if value == 0 and bApply == 0:
                return True
            elif value == 0 and bApply == 1:
                self.exist_click(L.title_designer.shadow.chx_shadow)
            elif value == 1 and bApply == 1:
                return True
            elif value == 1 and bApply == 0:
                self.exist_click(L.title_designer.shadow.chx_shadow)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def apply_shadow_to(self, index, image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if image == 0:
                if self.exist(L.title_designer.shadow.btn_shadow).AXValue == 0:
                    self.exist_click(L.title_designer.shadow.btn_shadow)
            elif image == 1:
                if self.exist(L.title_designer.shadow.btn_image_shadow).AXValue == 0:
                    self.exist_click(L.title_designer.shadow.btn_image_shadow)
            self.exist_click(L.title_designer.shadow.cbx_apply_shadow_to)
            if index == 0:
                self.exist_click(L.title_designer.shadow.option_text_and_border)
            elif index == 1:
                self.exist_click(L.title_designer.shadow.option_text_only)
            elif index == 2:
                self.exist_click(L.title_designer.shadow.option_border_only)
            elif index == 3:
                self.exist_click(L.title_designer.shadow.option_object_and_border)
            elif index == 4:
                self.exist_click(L.title_designer.shadow.option_object_only)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Drag Shadow Distance Slider')
    def drag_shadow_distance_slider(self, value, image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_object)
            if image == 0:
                if self.exist(L.title_designer.shadow.btn_shadow).AXValue == 0:
                    self.exist_click(L.title_designer.shadow.btn_shadow)
            elif image == 1:
                if self.exist(L.title_designer.shadow.btn_image_shadow).AXValue == 0:
                    self.exist_click(L.title_designer.shadow.btn_image_shadow)
            self.exist(L.title_designer.shadow.slider_distance).AXValue = float(value)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def input_shadow_distance_value(self, value, image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if image == 0:
                if self.exist(L.title_designer.shadow.btn_shadow).AXValue == 0:
                    self.exist_click(L.title_designer.shadow.btn_shadow)
            elif image == 1:
                if self.exist(L.title_designer.shadow.btn_image_shadow).AXValue == 0:
                    self.exist_click(L.title_designer.shadow.btn_image_shadow)
            self.exist_click(L.title_designer.shadow.edittext_distance)
            self.mouse.click(times=3)
            self.keyboard.send(value)
            self.exist_click(L.title_designer.shadow.text_distance)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Click Shadow Distance Arrow Button')
    def click_shadow_distance_arrow_btn(self, index, image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_object)
            if image == 0:
                if self.exist(L.title_designer.shadow.btn_shadow).AXValue == 0:
                    self.exist_click(L.title_designer.shadow.btn_shadow)
            elif image == 1:
                if self.exist(L.title_designer.shadow.btn_image_shadow).AXValue == 0:
                    self.exist_click(L.title_designer.shadow.btn_image_shadow)
            if index == 0:
                self.exist_click(L.title_designer.shadow.stepper_distance_value_up)
            elif index == 1:
                self.exist_click(L.title_designer.shadow.stepper_distance_value_down)
            time.sleep(DELAY_TIME*0.5)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def drag_shadow_blur_slider(self, value, image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if image == 0:
                if self.exist(L.title_designer.shadow.btn_shadow).AXValue == 0:
                    self.exist_click(L.title_designer.shadow.btn_shadow)
            elif image == 1:
                if self.exist(L.title_designer.shadow.btn_image_shadow).AXValue == 0:
                    self.exist_click(L.title_designer.shadow.btn_image_shadow)
            self.exist(L.title_designer.shadow.slider_blur).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Input Shadow Blur Value')
    def input_shadow_blur_value(self, value, image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_object)
            if image == 0:
                if self.exist(L.title_designer.shadow.btn_shadow).AXValue == 0:
                    self.exist_click(L.title_designer.shadow.btn_shadow)
            elif image == 1:
                if self.exist(L.title_designer.shadow.btn_image_shadow).AXValue == 0:
                    self.exist_click(L.title_designer.shadow.btn_image_shadow)
            self.exist_click(L.title_designer.shadow.edittext_blur)
            self.mouse.click(times=3)
            self.keyboard.send(value)
            self.exist_click(L.title_designer.shadow.text_blur)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_shadow_blur_arrow_btn(self, index, image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if image == 0:
                if self.exist(L.title_designer.shadow.btn_shadow).AXValue == 0:
                    self.exist_click(L.title_designer.shadow.btn_shadow)
            elif image == 1:
                if self.exist(L.title_designer.shadow.btn_image_shadow).AXValue == 0:
                    self.exist_click(L.title_designer.shadow.btn_image_shadow)
            if index == 0:
                self.exist_click(L.title_designer.shadow.stepper_blur_value_up)
            elif index == 1:
                self.exist_click(L.title_designer.shadow.stepper_blur_value_down)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Drag Shadow Opacity Slider')
    def drag_shadow_opacity_slider(self, value, image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_object)
            if image == 0:
                if self.exist(L.title_designer.shadow.btn_shadow).AXValue == 0:
                    self.exist_click(L.title_designer.shadow.btn_shadow)
            elif image == 1:
                if self.exist(L.title_designer.shadow.btn_image_shadow).AXValue == 0:
                    self.exist_click(L.title_designer.shadow.btn_image_shadow)
            self.exist(L.title_designer.shadow.slider_opacity).AXValue = float(value)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Input Shadow Opacity Value')
    def input_shadow_opacity_value(self, value, image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_object)
            if image == 0:
                if self.exist(L.title_designer.shadow.btn_shadow).AXValue == 0:
                    self.exist_click(L.title_designer.shadow.btn_shadow)
            elif image == 1:
                if self.exist(L.title_designer.shadow.btn_image_shadow).AXValue == 0:
                    self.exist_click(L.title_designer.shadow.btn_image_shadow)
            self.exist_click(L.title_designer.shadow.edittext_opacity)
            self.mouse.click(times=3)
            self.keyboard.send(value)
            self.exist_click(L.title_designer.shadow.text_opacity)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_shadow_opacity_arrow_btn(self, index, image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if image == 0:
                if self.exist(L.title_designer.shadow.btn_shadow).AXValue == 0:
                    self.exist_click(L.title_designer.shadow.btn_shadow)
            elif image == 1:
                if self.exist(L.title_designer.shadow.btn_image_shadow).AXValue == 0:
                    self.exist_click(L.title_designer.shadow.btn_image_shadow)
            if index == 0:
                self.exist_click(L.title_designer.shadow.stepper_opacity_value_up)
            elif index == 1:
                self.exist_click(L.title_designer.shadow.stepper_opacity_value_down)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Enable/ Disable Check Fill Shadow')
    def set_check_shadow_fill_shadow(self, bCheck=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.shadow.btn_shadow).AXValue == 0:
                self.exist_click(L.title_designer.shadow.btn_shadow)
            value = self.exist(L.title_designer.shadow.chx_fill_shadow).AXValue
            if bCheck == 0 and value == 1:
                self.exist_click(L.title_designer.shadow.chx_fill_shadow)
            elif bCheck == 0 and value == 0:
                return True
            elif bCheck == 1 and value == 0:
                self.exist_click(L.title_designer.shadow.chx_fill_shadow)
            elif bCheck == 1 and value == 1:
                return True
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Set Shadow Fill Shadow Color')
    def set_shadow_fill_shadow_color(self, red='255', green='255', blue='255', image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_object)
            if image == 0:
                if self.exist(L.title_designer.shadow.btn_shadow).AXValue == 0:
                    self.exist_click(L.title_designer.shadow.btn_shadow)
                self.exist_click(L.title_designer.shadow.btn_fill_shadow_color)
                self.color_picker_switch_category_to_RGB()
                self.exist_click(L.title_designer.shadow.edittext_red)
                self.mouse.click(times=3)
                self.keyboard.send(red)
                self.exist_click(L.title_designer.shadow.edittext_green)
                self.mouse.click(times=3)
                self.keyboard.send(green)
                self.exist_click(L.title_designer.shadow.edittext_blue)
                self.mouse.click(times=3)
                self.keyboard.send(blue)
                self.exist_click(L.title_designer.shadow.edittext_red)
                self.exist_click(L.title_designer.shadow.btn_close)
            elif image == 1:
                if self.exist(L.title_designer.shadow.btn_image_shadow).AXValue == 0:
                    self.exist_click(L.title_designer.shadow.btn_image_shadow)
                self.exist_click(L.title_designer.shadow.btn_select_shadow_color)
                self.color_picker_switch_category_to_RGB()
                self.exist_click(L.title_designer.shadow.edittext_red)
                self.mouse.click(times=3)
                self.keyboard.send(red)
                self.exist_click(L.title_designer.shadow.edittext_green)
                self.mouse.click(times=3)
                self.keyboard.send(green)
                self.exist_click(L.title_designer.shadow.edittext_blue)
                self.mouse.click(times=3)
                self.keyboard.send(blue)
                self.exist_click(L.title_designer.shadow.edittext_red)
                self.exist_click(L.title_designer.shadow.btn_close)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def input_shadow_direction_value(self, value):
        try:
            text_field_elem = self.exist(L.title_designer.shadow.text_field_direction)
            if text_field_elem:
                self.mouse.click(*text_field_elem.center)
                self.double_click()
                self.keyboard.send(value)
                time.sleep(DELAY_TIME)
                self.press_enter_key()
            else:
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_shadow_direction_arrow_btn(self,option):
        # option = 0, click [Up] arrow button
        # option = 1, click [Down] arrow button
        try:
            if option == 0:
                self.exist_click(L.title_designer.shadow.btn_direction_up)
            elif option == 1:
                self.exist_click(L.title_designer.shadow.btn_direction_down)
            time.sleep(DELAY_TIME*0.5)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_menu_bar_edit(self, index):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.menu_option.menu_bar_item_edit)
            if index == 1:
                self.exist_click(L.title_designer.menu_option.menu_option_undo)
            elif index == 2:
                self.exist_click(L.title_designer.menu_option.menu_option_redo)
            elif index == 3:
                self.exist_click(L.title_designer.menu_option.menu_option_cut)
            elif index == 4:
                self.exist_click(L.title_designer.menu_option.menu_option_copy)
            elif index == 5:
                self.exist_click(L.title_designer.menu_option.menu_option_paste)
            elif index == 6:
                self.exist_click(L.title_designer.menu_option.menu_option_remove)
            elif index == 7:
                self.exist_click(L.title_designer.menu_option.menu_option_select_all)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_menu_bar_help(self, index):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.menu_option.menu_option_help)
            if index == 1:
                self.exist_click(L.title_designer.menu_option.menu_option_help1)
            elif index == 2:
                self.exist_click(L.title_designer.menu_option.menu_option_title_designer_tutorial)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Click Undo button')  
    def click_undo_btn(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_undo)
            time.sleep(DELAY_TIME*2)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_redo_btn(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_redo)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_align_object_btn(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_advanced)
            self.exist_click(L.title_designer.btn_align_object)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def apply_snap_ref_line(self, bApply):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.grid_line.btn_toggle_grid_line)
            value = self.exist(L.title_designer.grid_line.option_snap_reference_lines).AXMenuItemMarkChar
            x, y = self.exist(L.title_designer.grid_line.option_snap_reference_lines).AXPosition
            if value == '✓' and bApply == 1:
                self.mouse.move(int(x-15), y)
                self.mouse.click(times=1)
                return True
            elif value == '✓' and bApply == 0:
                self.exist_click(L.title_designer.grid_line.option_snap_reference_lines)
            elif value == None and bApply == 1:
                self.exist_click(L.title_designer.grid_line.option_snap_reference_lines)
            elif value == None and bApply == 0:
                self.mouse.move(int(x - 15), y)
                self.mouse.click(times=1)
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_grid_lines_format(self, index):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.grid_line.btn_toggle_grid_line)
            self.exist_click(L.title_designer.grid_line.option_grid_lines)
            if index == 1:
                self.exist_click(L.title_designer.grid_line.option_none)
            elif index == 2:
                self.exist_click(L.title_designer.grid_line.option_2x2)
            elif index == 3:
                self.exist_click(L.title_designer.grid_line.option_3x3)
            elif index == 4:
                self.exist_click(L.title_designer.grid_line.option_4x4)
            elif index == 5:
                self.exist_click(L.title_designer.grid_line.option_5x5)
            elif index == 6:
                self.exist_click(L.title_designer.grid_line.option_6x6)
            elif index == 7:
                self.exist_click(L.title_designer.grid_line.option_7x7)
            elif index == 8:
                self.exist_click(L.title_designer.grid_line.option_8x8)
            elif index == 9:
                self.exist_click(L.title_designer.grid_line.option_9x9)
            elif index == 10:
                self.exist_click(L.title_designer.grid_line.option_10x10)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Add Keyframe Control')
    def click_object_setting_position_add_keyframe_control(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.btn_position_keyframe_control)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Reset Keyframe Control in Position')
    def click_object_setting_position_reset_keyframe_control(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.btn_position_reset_keyframe)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Click Previous Keyframe Control in Position')
    def click_object_setting_position_previous_keyframe(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.btn_position_previous_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Click Next Keyframe Control in Position')
    def click_object_setting_position_next_keyframe(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.btn_position_next_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Input Object Setting Position X Value')
    def input_object_setting_x_position_value(self, value, image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.edittext_position_x)
            self.mouse.click(times=3)
            self.keyboard.send(value)
            if image == 0:
                self.exist_click(L.title_designer.object_setting.text_x)
            elif image == 1:
                self.exist_click(L.title_designer.object_setting.text_image_x)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Click Object Setting Position X Arrow Button')
    def click_object_setting_x_position_arrow_btn(self, index):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            if index == 0:
                self.exist_click(L.title_designer.object_setting.stepper_position_x_up)
            elif index == 1:
                self.exist_click(L.title_designer.object_setting.stepper_position_x_down)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
    
    @step('[Action][Title Designer] Input Object Setting Position Y Value')
    def input_object_setting_y_position_value(self, value, image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.edittext_position_y)
            self.mouse.click(times=3)
            self.keyboard.send(value)
            if image == 0:
                self.exist_click(L.title_designer.object_setting.text_y)
            elif image == 1:
                self.exist_click(L.title_designer.object_setting.text_image_y)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_object_setting_y_position_arrow_btn(self, index):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            if index == 0:
                self.exist_click(L.title_designer.object_setting.stepper_position_y_up)
            elif index == 1:
                self.exist_click(L.title_designer.object_setting.stepper_position_y_down)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_object_setting_tutorial_btn(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.btn_tutorial)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def set_check_object_setting_position_ease_in(self, bCheck=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            value = self.exist(L.title_designer.object_setting.chx_ease_in).AXValue
            if value == 0 and bCheck == 1:
                self.exist_click(L.title_designer.object_setting.chx_ease_in)
            elif value == 0 and bCheck == 0:
                return True
            elif value == 1 and bCheck == 1:
                return True
            elif value == 1 and bCheck == 0:
                self.exist_click(L.title_designer.object_setting.chx_ease_in)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def input_object_setting_position_ease_in_value(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.edittext_position_ease_in)
            self.mouse.click(times=3)
            self.keyboard.send(value)
            self.exist_click(L.title_designer.object_setting.text_x)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_object_setting_position_ease_in_arrow_btn(self, index):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            if index == 0:
                self.exist_click(L.title_designer.object_setting.stepper_position_ease_in_up)
            elif index == 1:
                self.exist_click(L.title_designer.object_setting.stepper_position_ease_in_down)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_object_setting_position_ease_in_slider(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist(L.title_designer.object_setting.slider_ease_in).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def set_check_object_setting_position_ease_out(self, bCheck=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            value = self.exist(L.title_designer.object_setting.chx_ease_out).AXValue
            if value == 0 and bCheck == 1:
                self.exist_click(L.title_designer.object_setting.chx_ease_out)
            elif value == 0 and bCheck == 0:
                return True
            elif value == 1 and bCheck == 1:
                return True
            elif value == 1 and bCheck == 0:
                self.exist_click(L.title_designer.object_setting.chx_ease_out)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def input_object_setting_position_ease_out_value(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.edittext_position_ease_out)
            self.mouse.click(times=3)
            self.keyboard.send(value)
            self.exist_click(L.title_designer.object_setting.text_x)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_object_setting_position_ease_out_arrow_btn(self, index):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            if index == 0:
                self.exist_click(L.title_designer.object_setting.stepper_position_ease_out_up)
            elif index == 1:
                self.exist_click(L.title_designer.object_setting.stepper_position_ease_out_down)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_object_setting_position_ease_out_slider(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist(L.title_designer.object_setting.slider_ease_out).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Add Keyframe Control in Scale')
    def click_object_setting_scale_add_keyframe_control(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.btn_scale_keyframe_control)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Reset Keyframe Control in Scale')
    def click_object_setting_scale_reset_keyframe_control(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.btn_scale_reset_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Click Previous Keyframe Control in Scale')
    def click_object_setting_scale_previous_keyframe(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            #self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.btn_scale_previous_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_object_setting_scale_next_keyframe(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.btn_scale_next_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def input_object_setting_scale_width_value(self, value, image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.edittext_scale_width)
            self.mouse.click(times=3)
            self.keyboard.send(value)
            if image == 0:
                self.exist_click(L.title_designer.object_setting.text_scale)
            elif image == 1:
                self.exist_click(L.title_designer.object_setting.text_image_scale)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Get Object Setting Scale Width Value')
    def get_object_setting_scale_width_value(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")

            width_elem = self.exist(L.title_designer.object_setting.edittext_scale_width)
            if width_elem:
                return width_elem.AXValue
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_object_setting_scale_width_arrow_btn(self, index):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            if index == 0:
                self.exist_click(L.title_designer.object_setting.stepper_scale_width_up)
            elif index == 1:
                self.exist_click(L.title_designer.object_setting.stepper_scale_width_down)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Input Object Setting Scale Height Value')
    def input_object_setting_scale_height_value(self, value, image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            #self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.edittext_scale_height)
            self.mouse.click(times=3)
            self.keyboard.send(value)
            if image == 0:
                self.exist_click(L.title_designer.object_setting.text_scale)
            elif image == 1:
                self.exist_click(L.title_designer.object_setting.text_image_scale)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Get Object Setting Scale Height Value')
    def get_object_setting_scale_height_value(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception

            width_elem = self.exist(L.title_designer.object_setting.edittext_scale_height)
            if width_elem:
                return width_elem.AXValue
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_object_setting_scale_height_arrow_btn(self, index):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            if index == 0:
                self.exist_click(L.title_designer.object_setting.stepper_scale_height_up)
            elif index == 1:
                self.exist_click(L.title_designer.object_setting.stepper_scale_height_down)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def set_check_object_setting_scale_maintain_aspect_ratio(self, bCheck=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            value = self.exist(L.title_designer.object_setting.chx_maintain_aspect_ratio).AXValue
            if value == 0 and bCheck == 0:
                return True
            elif value == 0 and bCheck == 1:
                self.exist_click(L.title_designer.object_setting.chx_maintain_aspect_ratio)
            elif value == 1 and bCheck == 0:
                self.exist_click(L.title_designer.object_setting.chx_maintain_aspect_ratio)
            elif value == 1 and bCheck == 1:
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Set Check Object Setting Scale Ease In')
    def set_check_object_setting_scale_ease_in(self, bCheck=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            #self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            value = self.exist(L.title_designer.object_setting.chx_scale_ease_in).AXValue
            if value == 0 and bCheck == 0:
                return True
            elif value == 0 and bCheck == 1:
                self.exist_click(L.title_designer.object_setting.chx_scale_ease_in)
            elif value == 1 and bCheck == 0:
                self.exist_click(L.title_designer.object_setting.chx_scale_ease_in)
            elif value == 1 and bCheck == 1:
                return True
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def input_object_setting_scale_ease_in_value(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.edittext_scale_ease_in)
            self.mouse.click(times=3)
            self.keyboard.send(value)
            self.exist_click(L.title_designer.object_setting.text_height)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_object_setting_scale_ease_in_arrow_btn(self, index):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            if index == 0:
                self.exist_click(L.title_designer.object_setting.stepper_scale_ease_in_up)
            elif index == 1:
                self.exist_click(L.title_designer.object_setting.stepper_scale_ease_in_down)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Drag Object Setting -- Scale -- Ease In Slider')
    def drag_object_setting_scale_ease_in_slider(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            #self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist(L.title_designer.object_setting.slider_scale_ease_in).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Get Object Setting -- Scale -- Ease In Value')
    def get_object_setting_scale_ease_in_value(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")

            check_elem = self.exist(L.title_designer.object_setting.slider_scale_ease_in)
            if check_elem:
                return check_elem.AXValue
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Set Check Object Setting -- Scale -- Ease Out')
    def set_check_object_setting_scale_ease_out(self, bCheck=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            #self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            value = self.exist(L.title_designer.object_setting.chx_scale_ease_out).AXValue
            if value == 0 and bCheck == 0:
                return True
            elif value == 0 and bCheck == 1:
                self.exist_click(L.title_designer.object_setting.chx_scale_ease_out)
            elif value == 1 and bCheck == 0:
                self.exist_click(L.title_designer.object_setting.chx_scale_ease_out)
            elif value == 1 and bCheck == 1:
                return True
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def input_object_setting_scale_ease_out_value(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.edittext_scale_ease_out)
            self.mouse.click(times=3)
            self.keyboard.send(value)
            self.exist_click(L.title_designer.object_setting.text_height)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Get Object Setting -- Scale -- Ease Out Value')
    def get_object_setting_scale_ease_out_value(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")

            check_elem = self.exist(L.title_designer.object_setting.edittext_scale_ease_out)
            if check_elem:
                return check_elem.AXValue
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_object_setting_scale_ease_out_arrow_btn(self, index):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            if index == 0:
                self.exist_click(L.title_designer.object_setting.stepper_scale_ease_out_up)
            elif index == 1:
                self.exist_click(L.title_designer.object_setting.stepper_scale_ease_out_down)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Drag Object Setting -- Scale -- Ease Out Slider')
    def drag_object_setting_scale_ease_out_slider(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            #self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist(L.title_designer.object_setting.slider_scale_ease_out).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Add Keyframe Control in Opacity')
    def click_object_setting_opacity_add_keyframe_control(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            #self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.btn_opacity_keyframe_control)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_object_setting_opacity_reset_keyframe_control(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.btn_opacity_reset_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_object_setting_opacity_previous_keyframe(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.btn_opacity_previous_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_object_setting_opacity_next_keyframe(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.btn_opacity_next_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Drag Object Setting -- Opacity Slider')
    def drag_object_setting_opacity_slider(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            #self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist(L.title_designer.object_setting.slider_opacity).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_object_setting_opacity_arrow_btn(self, index):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            if index == 0:
                self.exist_click(L.title_designer.object_setting.stepper_opacity_up)
            elif index == 1:
                self.exist_click(L.title_designer.object_setting.stepper_opacity_down)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def input_object_setting_opacity_value(self, value, image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.edittext_opacity)
            self.mouse.click(times=3)
            self.keyboard.send(value)
            if image == 0:
                self.exist_click(L.title_designer.object_setting.text_opacity)
            elif image == 1:
                self.exist_click(L.title_designer.object_setting.text_image_opacity)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True
    
    @step('[Action][Title Designer] Add Keyframe Control in Rotation')
    def click_object_setting_rotation_add_keyframe_control(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            #self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.btn_rotation_keyframe_control)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_object_setting_rotation_reset_keyframe_control(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.btn_rotation_reset_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_object_setting_rotation_previous_keyframe(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.btn_rotation_previous_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Click Next Keyframe Control in Rotation')
    def click_object_setting_rotation_next_keyframe(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            #self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.btn_rotation_next_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_object_setting_rotation_arrow_btn(self, index):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            if index == 0:
                self.exist_click(L.title_designer.object_setting.stepper_rotation_up)
            elif index == 1:
                self.exist_click(L.title_designer.object_setting.stepper_rotation_down)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Input Object Setting Rotation Value')
    def input_object_setting_rotation_value(self, value, image=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            #self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.edittext_rotation)
            self.mouse.click(times=3)
            self.keyboard.send(value)
            '''
            if image == 0:
                self.exist_click(L.title_designer.object_setting.text_rotation)
            elif image == 1:
                self.exist_click(L.title_designer.object_setting.text_image_rotation)
            '''
            self.press_enter_key()
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Get Object Setting Rotation Value')
    def get_object_setting_rotation_value(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception

            rotate_elem = self.exist(L.title_designer.object_setting.edittext_rotation)
            if rotate_elem:
                return rotate_elem.AXValue
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def set_check_object_setting_rotation_ease_in(self, bCheck=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            value = self.exist(L.title_designer.object_setting.chx_rotation_ease_in).AXValue
            if value == 0 and bCheck == 0:
                return True
            elif value == 0 and bCheck == 1:
                self.exist_click(L.title_designer.object_setting.chx_rotation_ease_in)
            elif value == 1 and bCheck == 0:
                self.exist_click(L.title_designer.object_setting.chx_rotation_ease_in)
            elif value == 1 and bCheck == 1:
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def input_object_setting_rotation_ease_in_value(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.edittext_rotation_ease_in)
            self.mouse.click(times=3)
            self.keyboard.send(value)
            #self.exist_click(L.title_designer.object_setting.text_rotation)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_object_setting_rotation_ease_in_arrow_btn(self, index):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            if index == 0:
                self.exist_click(L.title_designer.object_setting.stepper_rotation_ease_in_up)
            elif index == 1:
                self.exist_click(L.title_designer.object_setting.stepper_rotation_ease_in_down)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_object_setting_rotation_ease_in_slider(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist(L.title_designer.object_setting.slider_rotation_ease_in).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Set Check Object Setting -- Rotation -- Ease Out')
    def set_check_object_setting_rotation_ease_out(self, bCheck=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            #self.exist_click(L.title_designer.btn_object)
            #if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
            #    self.exist_click(L.title_designer.object_setting.btn_object_setting)
            value = self.exist(L.title_designer.object_setting.chx_rotation_ease_out).AXValue
            if value == 0 and bCheck == 0:
                return True
            elif value == 0 and bCheck == 1:
                self.exist_click(L.title_designer.object_setting.chx_rotation_ease_out)
            elif value == 1 and bCheck == 0:
                self.exist_click(L.title_designer.object_setting.chx_rotation_ease_out)
            elif value == 1 and bCheck == 1:
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Input Object Setting -- Rotation -- Ease Out Value')
    def input_object_setting_rotation_ease_out_value(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            #self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist_click(L.title_designer.object_setting.edittext_rotation_ease_out)
            self.mouse.click(times=3)
            self.keyboard.send(value)
            self.press_enter_key()
            #self.exist_click(L.title_designer.object_setting.text_rotation)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def get_object_setting_rotation_ease_out_value(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception

            rotate_elem = self.exist(L.title_designer.object_setting.edittext_rotation_ease_out)
            if rotate_elem:
                return rotate_elem.AXValue
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_object_setting_rotation_ease_out_arrow_btn(self, index):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            if index == 0:
                self.exist_click(L.title_designer.object_setting.stepper_rotation_ease_out_up)
            elif index == 1:
                self.exist_click(L.title_designer.object_setting.stepper_rotation_ease_out_down)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_object_setting_rotation_ease_out_slider(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            #self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.object_setting.btn_object_setting).AXValue == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            self.exist(L.title_designer.object_setting.slider_rotation_ease_out).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def set_object_setting_render_method(self, index):
        target_option = L.title_designer.object_setting.method_group
        return bool(_set_option(self, L.title_designer.object_setting.cbx_render_method, target_option, option=index))

    def get_object_setting_render_method(self):
        target = self.is_exist(L.title_designer.object_setting.cbx_render_method)
        logger(target)
        if target:
            object = self.exist(L.title_designer.object_setting.cbx_render_method)
            return object.AXTitle
        else:
            return None
        
    @step('[Action][Title Designer] Apply in Animation Effect')
    def select_animation_in_animation_effect(self, category_index, select_tmp_index):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click(L.title_designer.btn_animation)
            if self.exist(L.title_designer.in_animation.btn_in_animation).AXValue == 0:
                self.exist_click(L.title_designer.in_animation.btn_in_animation)
            self.exist_click(L.title_designer.in_animation.cbx_effect)
            if category_index == 1:
                self.exist_click(L.title_designer.in_animation.option_all_effects)
            elif category_index == 2:
                self.exist_click(L.title_designer.in_animation.option_fly)
            elif category_index == 3:
                self.exist_click(L.title_designer.in_animation.option_no_effect)
            elif category_index == 4:
                self.exist_click(L.title_designer.in_animation.option_popup)
            elif category_index == 5:
                self.exist_click(L.title_designer.in_animation.option_roll_and_crawl)
            elif category_index == 6:
                self.exist_click(L.title_designer.in_animation.option_slide)
            elif category_index == 7:
                self.exist_click(L.title_designer.in_animation.option_special)
            elif category_index == 8:
                self.exist_click(L.title_designer.in_animation.option_video_rotation)
            elif category_index == 9:
                self.exist_click(L.title_designer.in_animation.option_wipe)
            self.exist_click({'AXIdentifier': 'TitleEffectCollectionViewItem', 'index': select_tmp_index})
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def select_animation_out_animation_effect(self, category_index, select_tmp_index):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_animation)
            if self.exist(L.title_designer.out_animation.btn_out_animation).AXValue == 0:
                self.exist_click(L.title_designer.out_animation.btn_out_animation)
            self.exist_click(L.title_designer.out_animation.cbx_effect)
            '''
            if category_index == 1:
                self.exist_click(L.title_designer.out_animation.option_all_effects)
            elif category_index == 2:
                self.exist_click(L.title_designer.out_animation.option_fly)
            elif category_index == 3:
                self.exist_click(L.title_designer.out_animation.option_no_effect)
            elif category_index == 4:
                self.exist_click(L.title_designer.out_animation.option_popup)
            elif category_index == 5:
                self.exist_click(L.title_designer.out_animation.option_roll_and_crawl)
            elif category_index == 6:
                self.exist_click(L.title_designer.out_animation.option_slide)
            elif category_index == 7:
                self.exist_click(L.title_designer.out_animation.option_special)
            elif category_index == 8:
                self.exist_click(L.title_designer.out_animation.option_video_rotation)
            elif category_index == 9:
                self.exist_click(L.title_designer.out_animation.option_wipe)
            '''
            self.exist_click({'AXIdentifier': 'TitleEffectCollectionViewItem', 'index': select_tmp_index})
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def apply_chromakey(self, bApply=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            value = self.exist(L.title_designer.chromakey.chx_chromakey).AXValue
            if value == 0 and bApply == 0:
                return True
            elif value == 0 and bApply == 1:
                self.exist_click(L.title_designer.chromakey.chx_chromakey)
            elif value == 1 and bApply == 1:
                return True
            elif value == 1 and bApply == 0:
                self.exist_click(L.title_designer.chromakey.chx_chromakey)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_chromakey_add_new_key(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No titile designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.chromakey.btn_chromakey).AXValue == 0:
                self.exist_click(L.title_designer.chromakey.btn_chromakey)
            self.exist_click(L.title_designer.chromakey.btn_add_new_key)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_chromakey_remove_btn(self, index=0):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No titile designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.chromakey.btn_chromakey).AXValue == 0:
                self.exist_click(L.title_designer.chromakey.btn_chromakey)
            self.exist_click({'AXIdentifier': 'IDC_CHROMAKEY_BTN_REMOVE', 'AXRole': 'AXButton', 'index': index})
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def input_chromakey_color_range_value(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No titile designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.chromakey.btn_chromakey).AXValue == 0:
                self.exist_click(L.title_designer.chromakey.btn_chromakey)
            self.exist_click(L.title_designer.chromakey.edittext_color_range)
            self.mouse.click(times=3)
            self.keyboard.send(value)
            self.exist_click(L.title_designer.chromakey.btn_chromakey)
            self.exist_click(L.title_designer.chromakey.btn_chromakey)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_chromakey_color_range_arrow_btn(self, index):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.chromakey.btn_chromakey).AXValue == 0:
                self.exist_click(L.title_designer.chromakey.btn_chromakey)
            if index == 0:
                self.exist_click(L.title_designer.chromakey.stepper_color_range_up)
            elif index == 1:
                self.exist_click(L.title_designer.chromakey.stepper_color_range_down)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_chromakey_color_range_slider(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.chromakey.btn_chromakey).AXValue == 0:
                self.exist_click(L.title_designer.chromakey.btn_chromakey)
            self.exist(L.title_designer.chromakey.slider_color_range).AXValue = int(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def input_chromakey_denoise_value(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No titile designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.chromakey.btn_chromakey).AXValue == 0:
                self.exist_click(L.title_designer.chromakey.btn_chromakey)
            self.exist_click(L.title_designer.chromakey.edittext_denoise)
            self.mouse.click(times=3)
            self.keyboard.send(value)
            self.exist_click(L.title_designer.chromakey.btn_chromakey)
            self.exist_click(L.title_designer.chromakey.btn_chromakey)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_chromakey_denoise_arrow_btn(self, index):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.chromakey.btn_chromakey).AXValue == 0:
                self.exist_click(L.title_designer.chromakey.btn_chromakey)
            if index == 0:
                self.exist_click(L.title_designer.chromakey.stepper_denoise_up)
            elif index == 1:
                self.exist_click(L.title_designer.chromakey.stepper_denoise_down)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_chromakey_denoise_slider(self, value):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.chromakey.btn_chromakey).AXValue == 0:
                self.exist_click(L.title_designer.chromakey.btn_chromakey)
            self.exist(L.title_designer.chromakey.slider_denoise).AXValue = int(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def apply_flip(self, bApply=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            value = self.exist(L.title_designer.flip.chx_flip).AXValue
            if value == 0 and bApply == 0:
                return True
            elif value == 0 and bApply == 1:
                self.exist_click(L.title_designer.flip.chx_flip)
            elif value == 1 and bApply == 1:
                return True
            elif value == 1 and bApply == 0:
                self.exist_click(L.title_designer.flip.chx_flip)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def set_flip_apply_type(self, index):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            if self.exist(L.title_designer.flip.btn_flip).AXValue == 0:
                self.exist_click(L.title_designer.flip.btn_flip)
            if index == 1:
                self.exist_click(L.title_designer.flip.rdb_upside_down)
            elif index == 2:
                self.exist_click(L.title_designer.flip.rdb_left_to_right)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def apply_fade(self, bApply=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            value = self.exist(L.title_designer.fade.chx_fade).AXValue
            if value == 0 and bApply == 0:
                return True
            elif value == 0 and bApply == 1:
                self.exist_click(L.title_designer.fade.chx_fade)
            elif value == 1 and bApply == 1:
                return True
            elif value == 1 and bApply == 0:
                self.exist_click(L.title_designer.fade.chx_fade)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def set_fade_enable_fade_in(self, bApply=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.fade.btn_fade).AXValue == 0:
                self.exist_click(L.title_designer.fade.btn_fade)
            value = self.exist(L.title_designer.fade.chx_enable_fade_in).AXValue
            if value == 0 and bApply == 0:
                return True
            elif value == 0 and bApply == 1:
                self.exist_click(L.title_designer.fade.chx_enable_fade_in)
            elif value == 1 and bApply == 1:
                return True
            elif value == 1 and bApply == 0:
                self.exist_click(L.title_designer.fade.chx_enable_fade_in)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def set_fade_enable_fade_out(self, bApply=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_object)
            if self.exist(L.title_designer.fade.btn_fade).AXValue == 0:
                self.exist_click(L.title_designer.fade.btn_fade)
            value = self.exist(L.title_designer.fade.chx_enable_fade_out).AXValue
            if value == 0 and bApply == 0:
                return True
            elif value == 0 and bApply == 1:
                self.exist_click(L.title_designer.fade.chx_enable_fade_out)
            elif value == 1 and bApply == 1:
                return True
            elif value == 1 and bApply == 0:
                self.exist_click(L.title_designer.fade.chx_enable_fade_out)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_display_timeline_mode_btn(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_display_timeline_mode)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_hide_timeline_mode_btn(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click(L.title_designer.btn_hide_timeline_mode)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_simple_track_extend_shrink(self, track_no, extend):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            value = self.exist([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW', 'AXRole': 'AXOutline'}, {'AXRole': 'AXRow', 'index': track_no},
                           {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRole': 'AXDisclosureTriangle'}]).AXValue
            if value == 0 and extend == 0:
                return True
            elif value == 0 and extend == 1:
                self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW', 'AXRole': 'AXOutline'}, {'AXRole': 'AXRow', 'index': track_no},
                           {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRole': 'AXDisclosureTriangle'}])
            elif value == 1 and extend == 0:
                self.exist_click(
                    [{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW', 'AXRole': 'AXOutline'}, {'AXRole': 'AXRow', 'index': track_no},
                     {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRole': 'AXDisclosureTriangle'}])
            elif value == 1 and extend == 1:
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_simple_track_specific_keyframe(self, index):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRole': 'AXOutline'}, {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem', 'index': index}])
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_simple_track_position_keyframe_control(self, track_no):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW', 'AXRole': 'AXOutline'},
                                       {'AXRole': 'AXRow', 'index': track_no},
                                       {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_ADD_REMOVE_KEYFRAME',
                                        'AXRole': 'AXButton'}])
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_simple_track_position_previous_keyframe(self, track_no):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW', 'AXRole': 'AXOutline'},
                                       {'AXRole': 'AXRow', 'index': track_no},
                                       {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_PREV_KEYFRAME',
                                        'AXRole': 'AXButton'}])
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_simple_track_position_next_keyframe(self, track_no):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW', 'AXRole': 'AXOutline'},
                                       {'AXRole': 'AXRow', 'index': track_no},
                                       {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_NEXT_KEYFRAME',
                                        'AXRole': 'AXButton'}])
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_simple_track_scale_keyframe_control(self, track_no):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW', 'AXRole': 'AXOutline'},
                                       {'AXRole': 'AXRow', 'index': track_no},
                                       {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_ADD_REMOVE_KEYFRAME',
                                        'AXRole': 'AXButton'}])
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_simple_track_scale_previous_keyframe(self, track_no):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW', 'AXRole': 'AXOutline'},
                                       {'AXRole': 'AXRow', 'index': track_no},
                                       {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_PREV_KEYFRAME',
                                        'AXRole': 'AXButton'}])
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_simple_track_scale_next_keyframe(self, track_no):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW', 'AXRole': 'AXOutline'},
                                       {'AXRole': 'AXRow', 'index': track_no},
                                       {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_NEXT_KEYFRAME',
                                        'AXRole': 'AXButton'}])
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Title Designer] Click Object Settings -- Simple Track Opacity -- Keyframe Control')
    def click_simple_track_opacity_keyframe_control(self, track_no):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW', 'AXRole': 'AXOutline'},
                                       {'AXRole': 'AXRow', 'index': track_no},
                                       {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_ADD_REMOVE_KEYFRAME',
                                        'AXRole': 'AXButton'}])
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Click Object Settings -- Simple Track Opacity -- Previous Keyframe')
    def click_simple_track_opacity_previous_keyframe(self, track_no):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW', 'AXRole': 'AXOutline'},
                                       {'AXRole': 'AXRow', 'index': track_no},
                                       {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_PREV_KEYFRAME',
                                        'AXRole': 'AXButton'}])
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Title Designer] Click Object Settings -- Simple Track Opacity -- Next Keyframe')
    def click_simple_track_opacity_next_keyframe(self, track_no):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW', 'AXRole': 'AXOutline'},
                                       {'AXRole': 'AXRow', 'index': track_no},
                                       {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_NEXT_KEYFRAME',
                                        'AXRole': 'AXButton'}])
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_simple_track_rotation_keyframe_control(self, track_no):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW', 'AXRole': 'AXOutline'},
                                       {'AXRole': 'AXRow', 'index': track_no},
                                       {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_ADD_REMOVE_KEYFRAME',
                                        'AXRole': 'AXButton'}])
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_simple_track_rotation_previous_keyframe(self, track_no):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW', 'AXRole': 'AXOutline'},
                                       {'AXRole': 'AXRow', 'index': track_no},
                                       {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_PREV_KEYFRAME',
                                        'AXRole': 'AXButton'}])
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_simple_track_rotation_next_keyframe(self, track_no):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW', 'AXRole': 'AXOutline'},
                                       {'AXRole': 'AXRow', 'index': track_no},
                                       {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_NEXT_KEYFRAME',
                                        'AXRole': 'AXButton'}])
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_simple_track_image_fade_in_duration(self, track_no, duration):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            x, y = self.exist([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW'}, {'AXRole': 'AXRow', 'index': track_no}, {'AXIdentifier': '_NS:12', 'AXRole': 'AXScrollArea'},
                                         {'AXIdentifier': '_NS:47', 'AXRole': 'AXImage'}]).AXPosition
            w, h = self.exist([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW'}, {'AXRole': 'AXRow', 'index': track_no}, {'AXIdentifier': '_NS:12', 'AXRole': 'AXScrollArea'},
                                         {'AXIdentifier': '_NS:47', 'AXRole': 'AXImage'}]).AXSize
            self.mouse.drag((int(x+w-2), int(y+10)), (int(x+w-2+int(duration)), int(y+10)))
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_simple_track_image_fade_out_duration(self, track_no, duration):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            x, y = self.exist([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW'}, {'AXRole': 'AXRow', 'index': track_no}, {'AXIdentifier': '_NS:12', 'AXRole': 'AXScrollArea'},
                                         {'AXIdentifier': '_NS:55', 'AXRole': 'AXImage'}]).AXPosition
            self.mouse.drag((int(x+2), int(y+10)), (int(x+2+int(duration)), int(y+10)))
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def remove_simple_particle_track(self, track_no):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            x, y = self.exist([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW', 'AXRole': 'AXOutline'},{'AXRole': 'AXRow', 'index': track_no}]).AXPosition
            self.mouse.move(int(x+20), int(y+15))
            self.mouse.click(times=1)
            self.right_click()
            self.exist_click(L.title_designer.option_remove_track)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def set_check_simple_track(self, track_no, bCheck=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            x, y = self.exist(
                [{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW', 'AXRole': 'AXOutline'}, {'AXRole': 'AXRow', 'index': track_no}]).AXPosition
            self.mouse.move(int(x + 20), int(y + 15))
            self.mouse.click(times=1)
            self.right_click()
            self.exist_click(L.title_designer.option_enable_all_track)
            if bCheck == 1:
                return True
            elif bCheck == 0:
                self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW', 'AXRole': 'AXOutline'}, {'AXRole': 'AXRow', 'index': track_no},
                                {'AXIdentifier': '_NS:9', 'AXRole': 'AXButton'}])
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def right_click_simple_track_header(self, track_no):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            x, y = self.exist([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW', 'AXRole': 'AXOutline'},{'AXRole': 'AXRow', 'index': track_no}]).AXPosition
            self.mouse.move(int(x+20), int(y+15))
            self.mouse.click(times=1)
            self.right_click()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_simple_track_to(self, track_no, n):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            x, y = self.exist([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW', 'AXRole': 'AXOutline'},{'AXRole': 'AXRow', 'index': track_no}]).AXPosition
            w, h = self.exist([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW', 'AXRole': 'AXOutline'},{'AXRole': 'AXRow', 'index': track_no}]).AXSize
            self.mouse.move(int(x+20), int(y+15))
            self.mouse.click(times=1)
            self.mouse.drag((int(x+20), int(y+15)), (int(x+20), int(y+15+int(n*h))))
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def unfold_object_character_presets_tab(self, unfold=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            value = self.exist(L.title_designer.character_presets.btn_character_presets).AXValue
            if value == 0 and unfold == 0:
                return True
            elif value == 0 and unfold == 1:
                self.exist_click(L.title_designer.character_presets.btn_character_presets)
            elif value == 1 and unfold == 0:
                self.exist_click(L.title_designer.character_presets.btn_character_presets)
            elif value == 1 and unfold == 1:
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def unfold_object_font_paragraph_tab(self, unfold=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            value = self.exist(L.title_designer.font_paragraph.btn_font_paragraph).AXValue
            if value == 0 and unfold == 0:
                return True
            elif value == 0 and unfold == 1:
                self.exist_click(L.title_designer.font_paragraph.btn_font_paragraph)
            elif value == 1 and unfold == 0:
                self.exist_click(L.title_designer.font_paragraph.btn_font_paragraph)
            elif value == 1 and unfold == 1:
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True
    
    @step('[Action][TitleDesigner] Fold or Unfold [Font Face] Tab')
    def unfold_object_font_face_tab(self, unfold=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            value = self.exist(L.title_designer.font_face.btn_font_face).AXValue
            if value == 0 and unfold == 0:
                return True
            elif value == 0 and unfold == 1:
                self.exist_click(L.title_designer.font_face.btn_font_face)
            elif value == 1 and unfold == 0:
                self.exist_click(L.title_designer.font_face.btn_font_face)
            elif value == 1 and unfold == 1:
                return True
            time.sleep(DELAY_TIME * 2)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def unfold_object_border_tab(self, unfold=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            value = self.exist(L.title_designer.border.btn_border).AXValue
            if value == 0 and unfold == 0:
                return True
            elif value == 0 and unfold == 1:
                self.exist_click(L.title_designer.border.btn_border)
            elif value == 1 and unfold == 0:
                self.exist_click(L.title_designer.border.btn_border)
            elif value == 1 and unfold == 1:
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][TitleDesigner] Fold/ Unfold [Shadow] Tab')
    def unfold_object_shadow_tab(self, unfold=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            value = self.exist(L.title_designer.shadow.btn_shadow).AXValue
            if value == 0 and unfold == 0:
                return True
            elif value == 0 and unfold == 1:
                self.exist_click(L.title_designer.shadow.btn_shadow)
            elif value == 1 and unfold == 0:
                self.exist_click(L.title_designer.shadow.btn_shadow)
            elif value == 1 and unfold == 1:
                return True
            time.sleep(DELAY_TIME * 2)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][TitleDesigner] Fold/ Unfold [Object Setting] Tab')
    def unfold_object_object_setting_tab(self, unfold=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            value = self.exist(L.title_designer.object_setting.btn_object_setting).AXValue
            if value == 0 and unfold == 0:
                return True
            elif value == 0 and unfold == 1:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            elif value == 1 and unfold == 0:
                self.exist_click(L.title_designer.object_setting.btn_object_setting)
            elif value == 1 and unfold == 1:
                return True
            time.sleep(DELAY_TIME*2)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][TitleDesigner] Fold/ Unfold [In Animation] Tab')
    def unfold_animation_in_animation_tab(self, unfold=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            value = self.exist(L.title_designer.in_animation.btn_in_animation).AXValue
            if value == 0 and unfold == 0:
                return True
            elif value == 0 and unfold == 1:
                self.exist_click(L.title_designer.in_animation.btn_in_animation)
            elif value == 1 and unfold == 0:
                self.exist_click(L.title_designer.in_animation.btn_in_animation)
            elif value == 1 and unfold == 1:
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][TitleDesigner] Fold/ Unfold [Out Animation] Tab')
    def unfold_animation_out_animation_tab(self, unfold=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            value = self.exist(L.title_designer.out_animation.btn_out_animation).AXValue
            if value == 0 and unfold == 0:
                return True
            elif value == 0 and unfold == 1:
                self.exist_click(L.title_designer.out_animation.btn_out_animation)
            elif value == 1 and unfold == 0:
                self.exist_click(L.title_designer.out_animation.btn_out_animation)
            elif value == 1 and unfold == 1:
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def get_font_type(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            text = self.exist(L.title_designer.font_paragraph.cbx_font).AXValue
            return text
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def get_font_size(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            text = self.exist(L.title_designer.font_paragraph.cbx_font_size).AXValue
            return text
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def apply_font_face_color(self, HexColor):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            if self.exist(L.title_designer.font_face.btn_uniform_color).AXEnabled == False:
                return False
            else:
                self.exist_click(L.title_designer.font_face.btn_uniform_color)
                self.color_picker_switch_category_to_RGB()
                self.exist_click(L.title_designer.font_face.edittext_hex)
                self.mouse.click(times= 3)
                self.keyboard.send(HexColor)
                self.exist_click(L.title_designer.font_face.edittext_red)
                self.exist_click(L.title_designer.font_face.btn_close)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def get_font_face_color(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            if self.exist(L.title_designer.font_face.btn_uniform_color).AXEnabled == False:
                return False
            else:
                self.exist_click(L.title_designer.font_face.btn_uniform_color)
                value = self.exist(L.title_designer.font_face.edittext_hex).AXValue
                self.exist_click(L.title_designer.font_face.btn_close)
                return value
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def apply_border_color(self, HexColor):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            if self.exist(L.title_designer.border.btn_uniform_color).AXEnabled == False:
                return False
            else:
                self.exist_click(L.title_designer.border.btn_uniform_color)
                self.color_picker_switch_category_to_RGB()
                self.exist_click(L.title_designer.border.edittext_hex)
                self.mouse.click(times= 3)
                self.keyboard.send(HexColor)
                self.exist_click(L.title_designer.border.edittext_red)
                self.exist_click(L.title_designer.border.btn_close)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def get_border_color(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            if self.exist(L.title_designer.border.btn_uniform_color).AXEnabled == False:
                return False
            else:
                self.exist_click(L.title_designer.border.btn_uniform_color)
                value = self.exist(L.title_designer.border.edittext_hex).AXValue
                self.exist_click(L.title_designer.border.btn_close)
                return value
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def apply_shadow_color(self, HexColor):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            if self.exist(L.title_designer.shadow.btn_fill_shadow_color).AXEnabled == False:
                return False
            else:
                self.exist_click(L.title_designer.shadow.btn_fill_shadow_color)
                self.color_picker_switch_category_to_RGB()
                self.exist_click(L.title_designer.shadow.edittext_hex)
                self.mouse.click(times= 3)
                self.keyboard.send(HexColor)
                self.exist_click(L.title_designer.shadow.edittext_red)
                self.exist_click(L.title_designer.shadow.btn_close)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def get_shadow_color(self):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            if self.exist(L.title_designer.shadow.btn_fill_shadow_color).AXEnabled == False:
                return False
            else:
                self.exist_click(L.title_designer.shadow.btn_fill_shadow_color)
                value = self.exist(L.title_designer.shadow.edittext_hex).AXValue
                self.exist_click(L.title_designer.shadow.btn_close)
                return value
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_simple_timeline_position_right_click_menu_remove_keyframe(self, index=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRole': 'AXOutline'}, {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem', 'index': index}])
            self.right_click()
            self.exist_click(L.title_designer.timeline_context_menu.remove_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_simple_timeline_position_right_click_menu_remove_all_keyframe(self, index=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRole': 'AXOutline'}, {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem', 'index': index}])
            self.right_click()
            self.exist_click(L.title_designer.timeline_context_menu.remove_all_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_simple_timeline_position_right_click_menu_duplicate_previous_keyframe(self, index=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRole': 'AXOutline'}, {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem', 'index': index}])
            self.right_click()
            self.exist_click(L.title_designer.timeline_context_menu.duplicate_previous_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_simple_timeline_position_right_click_menu_duplicate_next_keyframe(self, index=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRole': 'AXOutline'}, {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem', 'index': index}])
            self.right_click()
            self.exist_click(L.title_designer.timeline_context_menu.duplicate_next_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_simple_timeline_position_right_click_menu_ease_in(self, index=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRole': 'AXOutline'}, {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem', 'index': index}])
            self.right_click()
            self.exist_click(L.title_designer.timeline_context_menu.ease_in)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_simple_timeline_position_right_click_menu_ease_out(self, index=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRole': 'AXOutline'}, {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem', 'index': index}])
            self.right_click()
            self.exist_click(L.title_designer.timeline_context_menu.ease_out)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_simple_timeline_scale_right_click_menu_remove_keyframe(self, index=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRole': 'AXOutline'}, {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem', 'index': index}])
            self.right_click()
            self.exist_click(L.title_designer.timeline_context_menu.remove_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_simple_timeline_scale_right_click_menu_remove_all_keyframe(self, index=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRole': 'AXOutline'}, {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem', 'index': index}])
            self.right_click()
            self.exist_click(L.title_designer.timeline_context_menu.remove_all_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_simple_timeline_scale_right_click_menu_duplicate_previous_keyframe(self, index=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRole': 'AXOutline'}, {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem', 'index': index}])
            self.right_click()
            self.exist_click(L.title_designer.timeline_context_menu.duplicate_previous_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_simple_timeline_scale_right_click_menu_duplicate_next_keyframe(self, index=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRole': 'AXOutline'}, {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem', 'index': index}])
            self.right_click()
            self.exist_click(L.title_designer.timeline_context_menu.duplicate_next_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_simple_timeline_scale_right_click_menu_ease_in(self, index=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRole': 'AXOutline'}, {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem', 'index': index}])
            self.right_click()
            self.exist_click(L.title_designer.timeline_context_menu.ease_in)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_simple_timeline_scale_right_click_menu_ease_out(self, index=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRole': 'AXOutline'}, {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem', 'index': index}])
            self.right_click()
            self.exist_click(L.title_designer.timeline_context_menu.ease_out)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_simple_timeline_opacity_right_click_menu_remove_keyframe(self, index=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRole': 'AXOutline'},
                              {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem', 'index': index}])
            self.right_click()
            self.exist_click(L.title_designer.timeline_context_menu.remove_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_simple_timeline_opacity_right_click_menu_remove_all_keyframe(self, index=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRole': 'AXOutline'},
                              {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem', 'index': index}])
            self.right_click()
            self.exist_click(L.title_designer.timeline_context_menu.remove_all_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_simple_timeline_opacity_right_click_menu_duplicate_previous_keyframe(self, index=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRole': 'AXOutline'},
                              {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem', 'index': index}])
            self.right_click()
            self.exist_click(L.title_designer.timeline_context_menu.duplicate_previous_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_simple_timeline_opacity_right_click_menu_duplicate_next_keyframe(self, index=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRole': 'AXOutline'},
                              {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem', 'index': index}])
            self.right_click()
            self.exist_click(L.title_designer.timeline_context_menu.duplicate_next_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_simple_timeline_opacity_right_click_menu_ease_in(self, index=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRole': 'AXOutline'},
                              {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem', 'index': index}])
            self.right_click()
            self.exist_click(L.title_designer.timeline_context_menu.ease_in)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_simple_timeline_opacity_right_click_menu_ease_out(self, index=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRole': 'AXOutline'},
                              {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem', 'index': index}])
            self.right_click()
            self.exist_click(L.title_designer.timeline_context_menu.ease_out)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_simple_timeline_rotation_right_click_menu_remove_keyframe(self, index=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRole': 'AXOutline'},
                              {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem', 'index': index}])
            self.right_click()
            self.exist_click(L.title_designer.timeline_context_menu.remove_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_simple_timeline_rotation_right_click_menu_remove_all_keyframe(self, index=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRole': 'AXOutline'},
                              {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem', 'index': index}])
            self.right_click()
            self.exist_click(L.title_designer.timeline_context_menu.remove_all_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_simple_timeline_rotation_right_click_menu_duplicate_previous_keyframe(self, index=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRole': 'AXOutline'},
                              {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem', 'index': index}])
            self.right_click()
            self.exist_click(L.title_designer.timeline_context_menu.duplicate_previous_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_simple_timeline_rotation_right_click_menu_duplicate_next_keyframe(self, index=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRole': 'AXOutline'},
                              {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem', 'index': index}])
            self.right_click()
            self.exist_click(L.title_designer.timeline_context_menu.duplicate_next_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_simple_timeline_rotation_right_click_menu_ease_in(self, index=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRole': 'AXOutline'},
                              {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem', 'index': index}])
            self.right_click()
            self.exist_click(L.title_designer.timeline_context_menu.ease_in)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_simple_timeline_rotation_right_click_menu_ease_out(self, index=1):
        try:
            if not self.exist(L.title_designer.area.window_title_designer):
                logger("No title designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRole': 'AXOutline'},
                              {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem', 'index': index}])
            self.right_click()
            self.exist_click(L.title_designer.timeline_context_menu.ease_out)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def save_as_new_preset(self):
        return bool(self.exist_click(L.title_designer.character_presets.btn_save_as_new_preset))

    class Motion_Graphic_Title(Main_Page, BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        @step('[Action][TitleDesigner][MGT] Check if warning message show up and deal with dont show again option')
        def handle_warning_msg(self, tick_option=1):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                msg = self.exist(L.title_designer.motion_graphic_title.waring_dialog_msg).AXValue
                value = self.exist(L.title_designer.motion_graphic_title.chx_dont_show_again).AXValue
                if value == 0 and tick_option == 1:
                    x, y = self.exist(L.title_designer.motion_graphic_title.chx_dont_show_again).AXPosition
                    self.mouse.move(int(x+10), int(y+10))
                    self.mouse.click(times=1)
                if msg != L.title_designer.motion_graphic_title.warning_dialog_msg_content:
                    return False
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][TitleDesigner][MGT] Click OK button on warning message dialog')
        def click_warning_msg_ok(self):
            try:
                if not self.exist(L.title_designer.motion_graphic_title.waring_dialog_msg):
                    logger("No warning dialog show up")
                    raise Exception("No warning dialog show up")
                self.exist_click(L.title_designer.motion_graphic_title.btn_ok)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][TitleDesigner][MGT] Select title track')
        def select_title_track(self, value):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                self.exist_click(L.title_designer.title.cbx_select_title)
                self.exist_click({'AXRole': 'AXStaticText', 'AXValue': value})
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][TitleDesigner][MGT] Input title text')
        def input_title_text(self, text):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                target = self.exist(L.title_designer.title.edittext_title_text)
                self.exist_click(L.title_designer.title.edittext_title_text)
                self.mouse.click(times=3)
                target.AXValue = str(text)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def get_title_editbox(self):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception
                value = self.exist(L.title_designer.title.edittext_title_text).AXValue
                return value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        @step('[Action][TitleDesigner][MGT] Apply font type')
        def apply_font_type(self, text):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                self.exist_click(L.title_designer.title.btn_font_type)
                x, y = self.exist(L.title_designer.title.cbx_font_type).AXPosition
                self.mouse.move(int(x+20), int(y+10))
                self.mouse.click(times=4)
                self.keyboard.pressed(self.keyboard.key.delete)
                self.keyboard.send(text)
                self.mouse.move(int(x-25), int(y+10))
                time.sleep(1)
                self.mouse.click(times=1)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][TitleDesigner][MGT] Click Bold button')
        def click_bold_btn(self):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                self.exist_click(L.title_designer.title.btn_bold)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def click_italic_btn(self):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception
                self.exist_click(L.title_designer.title.btn_italic)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        @step('[Action][TitleDesigner][MGT] Apply font face color')
        def apply_font_face_color(self, HexColor):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                self.exist_click(L.title_designer.title.btn_font_color)
                self.color_picker_switch_category_to_RGB()
                self.exist_click(L.title_designer.title.edittext_hex)
                self.mouse.click(times=3)
                self.keyboard.send(HexColor)
                self.exist_click(L.title_designer.title.edittext_red)
                self.exist_click(L.title_designer.title.btn_color_close)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][TitleDesigner][MGT] Apply Graphics Color')
        def apply_graphics_color(self, group_no, HexColor):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                self.exist_click({'AXIdentifier': 'IDC_ELEGANT_TITLE_DESIGNER_BTN_COLOR_PICKER_'+ str(group_no), 'AXRole': 'AXButton'})
                self.color_picker_switch_category_to_RGB()
                self.exist_click(L.title_designer.graphic_color.edittext_hex)
                self.mouse.click(times=3)
                self.keyboard.send(HexColor)
                self.exist_click(L.title_designer.graphic_color.edittext_red)
                self.exist_click(L.title_designer.graphic_color.btn_color_close)
                time.sleep(DELAY_TIME)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def get_graphics_color(self, group_no):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception
                self.exist_click({'AXIdentifier': 'IDC_ELEGANT_TITLE_DESIGNER_BTN_COLOR_PICKER_'+ str(group_no), 'AXRole': 'AXButton'})
                value = self.exist(L.title_designer.graphic_color.edittext_hex).AXValue
                self.exist_click(L.title_designer.graphic_color.btn_color_close)
                return value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        @step('[Action][TitleDesigner][MGT] Set Position X value')
        def set_position_x_value(self, value):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                self.exist_click(L.title_designer.mgt_object_settings.edittext_position_x)
                self.mouse.click(times=3)
                self.keyboard.send(value)
                self.exist_click(L.title_designer.mgt_object_settings.text_position)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][TitleDesigner][MGT] Get position x value')
        def get_position_x_value(self):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                value = self.exist(L.title_designer.mgt_object_settings.edittext_position_x).AXValue
                return value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][TitleDesigner][MGT] Click position x arrow button')
        def click_position_x_arrow_btn(self, index, times=1):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                if index == 0:
                    x, y = self.exist(L.title_designer.mgt_object_settings.stepper_position_x_up).AXPosition
                    self.mouse.move(x,y)
                    self.mouse.click(times=times)
                elif index == 1:
                    x, y = self.exist(L.title_designer.mgt_object_settings.stepper_position_x_down).AXPosition
                    self.mouse.move(x, y)
                    self.mouse.click(times=times)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][TitleDesigner][MGT] Set Position Y value')
        def set_position_y_value(self, value):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                self.exist_click(L.title_designer.mgt_object_settings.edittext_position_y)
                self.mouse.click(times=3)
                self.keyboard.send(value)
                self.exist_click(L.title_designer.mgt_object_settings.text_position)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][TitleDesigner][MGT] Get position y value')
        def get_position_y_value(self):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                value = self.exist(L.title_designer.mgt_object_settings.edittext_position_y).AXValue
                return value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][TitleDesigner][MGT] Click position y arrow button')
        def click_position_y_arrow_btn(self, index, times=1):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                if index == 0:
                    x, y = self.exist(L.title_designer.mgt_object_settings.stepper_position_y_up).AXPosition
                    self.mouse.move(x,y)
                    self.mouse.click(times=times)
                elif index == 1:
                    x, y = self.exist(L.title_designer.mgt_object_settings.stepper_position_y_down).AXPosition
                    self.mouse.move(x, y)
                    self.mouse.click(times=times)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def set_scale_width_value(self, value):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception
                self.exist_click(L.title_designer.mgt_object_settings.edittext_width)
                self.mouse.click(times=3)
                self.keyboard.send(value)
                self.exist_click(L.title_designer.mgt_object_settings.text_scale)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True
        
        @step('[Action][TitleDesigner][MGT] Get scale width value')
        def get_scale_width_value(self):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                value = self.exist(L.title_designer.mgt_object_settings.edittext_width).AXValue
                return value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True
        
        @step('[Action][TitleDesigner][MGT] Click scale width arrow button')
        def click_scale_width_arrow_btn(self, index, times=1):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                if index == 0:
                    x, y = self.exist(L.title_designer.mgt_object_settings.stepper_width_up).AXPosition
                    self.mouse.move(x,y)
                    self.mouse.click(times=times)
                elif index == 1:
                    x, y = self.exist(L.title_designer.mgt_object_settings.stepper_width_down).AXPosition
                    self.mouse.move(x, y)
                    self.mouse.click(times=times)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][TitleDesigner][MGT] Drag scale width slider')
        def drag_scale_width_slider(self, value):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                self.exist(L.title_designer.mgt_object_settings.slider_width).AXValue = float(value)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][TitleDesigner][MGT] Set scale height value')
        def set_scale_height_value(self, value):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                self.exist_click(L.title_designer.mgt_object_settings.edittext_height)
                self.mouse.click(times=3)
                self.keyboard.send(value)
                self.exist_click(L.title_designer.mgt_object_settings.text_scale)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][TitleDesigner][MGT] Get scale height value')
        def get_scale_height_value(self):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                value = self.exist(L.title_designer.mgt_object_settings.edittext_height).AXValue
                return value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][TitleDesigner][MGT] Click scale height arrow button')
        def click_scale_height_arrow_btn(self, index, times=1):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                if index == 0:
                    x, y = self.exist(L.title_designer.mgt_object_settings.stepper_height_up).AXPosition
                    self.mouse.move(x,y)
                    self.mouse.click(times=times)
                elif index == 1:
                    x, y = self.exist(L.title_designer.mgt_object_settings.stepper_height_down).AXPosition
                    self.mouse.move(x, y)
                    self.mouse.click(times=times)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][TitleDesigner][MGT] Drag scale height slider')
        def drag_scale_height_slider(self, value):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                self.exist(L.title_designer.mgt_object_settings.slider_height).AXValue = float(value)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][TitleDesigner][MGT] Tick/ Untick Maintain Aspect Ratio')
        def click_maintain_aspect_ratio(self, bCheck=1):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                value = self.exist(L.title_designer.mgt_object_settings.chx_maintain_aspect_ratio).AXValue
                if value == 0 and bCheck == 0:
                    return True
                elif value == 0 and bCheck == 1:
                    self.exist_click(L.title_designer.mgt_object_settings.chx_maintain_aspect_ratio)
                elif value == 1 and bCheck == 0:
                    self.exist_click(L.title_designer.mgt_object_settings.chx_maintain_aspect_ratio)
                elif value == 1 and bCheck == 1:
                    return True
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def set_rotation_value(self, value):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception
                self.exist_click(L.title_designer.mgt_object_settings.edittext_rotation)
                self.mouse.click(times=3)
                self.keyboard.send(value)
                time.sleep(1)
                self.press_enter_key()
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def get_rotation_value(self):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception
                value = self.exist(L.title_designer.mgt_object_settings.edittext_rotation).AXValue
                return value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def click_rotation_arrow_btn(self, index, times=1):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception
                if index == 0:
                    x, y = self.exist(L.title_designer.mgt_object_settings.stepper_rotation_up).AXPosition
                    self.mouse.move(x,y)
                    self.mouse.click(times=times)
                elif index == 1:
                    x, y = self.exist(L.title_designer.mgt_object_settings.stepper_rotation_down).AXPosition
                    self.mouse.move(x, y)
                    self.mouse.click(times=times)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        @step('[Action][TitleDesigner][MGT] Fold/ Unfold Title Tab')
        def unfold_title_tab(self, unfold=1):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                value = self.exist(L.title_designer.motion_graphic_title.btn_title).AXValue
                if value == 0 and unfold == 0:
                    return True
                elif value == 0 and unfold == 1:
                    self.exist_click(L.title_designer.motion_graphic_title.btn_title)
                elif value == 1 and unfold == 0:
                    self.exist_click(L.title_designer.motion_graphic_title.btn_title)
                elif value == 1 and unfold == 1:
                    return True
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def unfold_graphics_color_tab(self, unfold=1):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception
                value = self.exist(L.title_designer.motion_graphic_title.btn_graphics_color).AXValue
                if value == 0 and unfold == 0:
                    return True
                elif value == 0 and unfold == 1:
                    self.exist_click(L.title_designer.motion_graphic_title.btn_graphics_color)
                elif value == 1 and unfold == 0:
                    self.exist_click(L.title_designer.motion_graphic_title.btn_graphics_color)
                elif value == 1 and unfold == 1:
                    return True
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        @step('[Action][TitleDesigner][MGT] Fold/ Unfold Object Setting Tab')
        def unfold_object_setting_tab(self, unfold=1):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                value = self.exist(L.title_designer.motion_graphic_title.btn_object_setting).AXValue
                if value == 0 and unfold == 0:
                    return True
                elif value == 0 and unfold == 1:
                    self.exist_click(L.title_designer.motion_graphic_title.btn_object_setting)
                elif value == 1 and unfold == 0:
                    self.exist_click(L.title_designer.motion_graphic_title.btn_object_setting)
                elif value == 1 and unfold == 1:
                    return True
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][TitleDesigner][MGT] Set zoom value by menu')
        def click_viewer_zoom_menu(self, value='Fit'):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                self.exist_click(L.title_designer.viewer_zoom.cbx_viewer_zoom)
                self.exist_click({'AXRole': 'AXStaticText', 'AXValue': value})
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][TitleDesigner][MGT] Click Zoom in button')
        def click_zoom_in(self, times=1):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                x, y = self.exist(L.title_designer.btn_zoom_in).AXPosition
                self.mouse.move(x, y)
                self.mouse.click(times=times)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True
        @step('[Action][Title Designer][MGT] Click preview operation -- play, pause, stop, previous frame, next frame, fast forward')
        def click_preview_operation(self, operation):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                if operation == 'Play':
                    self.exist_click(L.title_designer.operation.btn_play)
                elif operation == 'Pause':
                    self.exist_click(L.title_designer.operation.btn_pause)
                elif operation == 'Stop':
                    self.exist_click(L.title_designer.operation.btn_stop)
                elif operation == 'Previous_Frame':
                    self.exist_click(L.title_designer.operation.btn_previous_frame)
                elif operation == 'Next_Frame':
                    self.exist_click(L.title_designer.operation.btn_next_frame)
                elif operation == 'Fast_Forward':
                    self.exist_click(L.title_designer.operation.btn_fast_forward)
                else:
                    logger(f'Invalid operation: {operation}')
                    raise Exception(f'Invalid operation: {operation}, please input (Play, Pause, Stop, Previous_Frame, Next_Frame, Fast_Forward)')
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def click_menu_bar_edit(self, index):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception
                self.exist_click(L.title_designer.menu_option.menu_bar_item_edit)
                if index == 1:
                    self.exist_click(L.title_designer.menu_option.menu_option_undo)
                elif index == 2:
                    self.exist_click(L.title_designer.menu_option.menu_option_redo)
                elif index == 3:
                    self.exist_click(L.title_designer.menu_option.menu_option_cut)
                elif index == 4:
                    self.exist_click(L.title_designer.menu_option.menu_option_copy)
                elif index == 5:
                    self.exist_click(L.title_designer.menu_option.menu_option_paste)
                elif index == 6:
                    self.exist_click(L.title_designer.menu_option.menu_option_remove)
                elif index == 7:
                    self.exist_click(L.title_designer.menu_option.menu_option_select_all)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True
        @step('[Action][TitleDesigner][MGT] Click Undo button')
        def click_undo_btn(self):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                self.exist_click(L.title_designer.mgt_function_buttons.undo)
                time.sleep(DELAY_TIME)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True
    
        def click_redo_btn(self):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception
                self.exist_click(L.title_designer.mgt_function_buttons.redo)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        @step('[Action][TitleDesigner][MGT] Click Zoom out button')
        def click_zoom_out_btn(self, times=1):
            try:
                if not self.exist(L.title_designer.area.window_title_designer):
                    logger("No title designer window show up")
                    raise Exception("No title designer window show up")
                self.exist_click(locator=L.title_designer.mgt_function_buttons.zoom_out, times=times)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

    def handle_keyframe_want_to_continue(self, option=1):
        return _want_to_continue(self, L.title_designer.backdrop.warning.dialog, option)

    def handle_effect_want_to_continue(self, option=1):
        return _want_to_continue(self, L.title_designer.backdrop.warning.dialog, option)

    @step('[Action][TitleDesigner][MotionGraphic] Handle special effect want to continue dialog')
    def handle_special_effect_want_to_continue(self, option=1):
        return _want_to_continue(self, L.title_designer.backdrop.warning.dialog, option)

    class Backdrop(Main_Page, BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.image = self.Image(*args, *kwargs)
            self.width = self.Width(*args, *kwargs)
            self.height = self.Height(*args, *kwargs)
            self.opacity = self.Opacity(*args, *kwargs)
            self.offset_x = self.OffsetX(*args, *kwargs)
            self.offset_y = self.OffsetY(*args, *kwargs)
            self.curve_radius = self.CurveRadius(*args, *kwargs)

        @step('[Action][TitleDesigner][Backdrop] Fold/ Unfold the tab')
        def set_unfold_tab(self, unfold=1):
            return _checkbox_status(self, L.title_designer.backdrop.btn_backdrop, unfold, get_status=False)

        def get_tab_status(self):
            return _checkbox_status(self, L.title_designer.backdrop.btn_backdrop, get_status=True)
        
        @step('[Action][TitleDesigner][Backdrop] Enable/ Disable the checkbox')
        def set_checkbox(self, bApply):
            return bool(_checkbox_status(self, L.title_designer.backdrop.chx_backdrop, bApply, get_status=False))

        def get_checkbox_status(self):
            return bool(_checkbox_status(self, L.title_designer.backdrop.chx_backdrop, get_status=True))

        def set_type(self, index, fit_type=None):
            target_radio = L.title_designer.backdrop.radio_group
            target_option = L.title_designer.backdrop.fit_with_title_group
            _set_radio(self, target_radio, option=index)
            if index > 1 and fit_type is not None:
                _set_option(self, L.title_designer.backdrop.cbx_fit_with_title, target_option, fit_type)
            time.sleep(DELAY_TIME*2)
        
        @step('[Action][TitleDesigner][Backdrop] Get the type of backdrop')
        def get_type(self):
            target_radio = L.title_designer.backdrop.radio_group
            return _set_radio(self, target_radio, option=2, get_status=True)
        
        @step('[Action][TitleDesigner][Backdrop] Get the status of width')
        def check_width_disable(self):
            return bool(_checkbox_status(self, L.title_designer.backdrop.width.slider, get_enable=True))

        def check_offset_x_disable(self):
            return bool(_checkbox_status(self, L.title_designer.backdrop.offset_x.slider, get_enable=True))

        def check_curve_radius_disable(self):
            return bool(_checkbox_status(self, L.title_designer.backdrop.curve_radius.slider, get_enable=True))

        def set_fill_type(self, index, image_path=None):
            target_option = L.title_designer.backdrop.fill_type_group
            return bool(_set_option(self, L.title_designer.backdrop.cbx_fill_type, target_option, option=index,
                                    path=image_path))

        def get_fill_type(self):
            target_option = L.title_designer.backdrop.fill_type_group
            return _set_option(self, L.title_designer.backdrop.cbx_fill_type, target_option, get_status=True)

        @step('[Action][TitleDesigner][Backdrop] Apply color to backdrop')
        def apply_uniform_color(self, HexColor):
            self.click(L.title_designer.backdrop.btn_uniform_color)
            return _set_color(self, HexColor)

        def apply_gradient_begin(self, HexColor):
            self.click(L.title_designer.backdrop.btn_begin_with)
            return _set_color(self, HexColor)

        def apply_gradient_end(self, HexColor):
            self.click(L.title_designer.backdrop.btn_end_with)
            return _set_color(self, HexColor)

        '''
        # Need RD support backdoor
        def apply_gradient_direction(self):
        
        '''
        class Image(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.keep_aspect_ratio = self.KeepAspectRatio(*args, *kwargs)
                self.flip_upside_down = self.FlipUpsideDown(*args, *kwargs)
                self.flip_left_right = self.FlipLeftRight(*args, *kwargs)

            class KeepAspectRatio(BasePage):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                def set_checkbox(self, bApply):
                    return bool(_checkbox_status(self, L.title_designer.backdrop.image.chx_keep_aspect_ratio, bApply,
                                                 get_status=False))

                def get_checkbox_status(self):
                    return bool(_checkbox_status(self, L.title_designer.backdrop.image.chx_keep_aspect_ratio,
                                                 get_status=True))

            class FlipUpsideDown(BasePage):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                def set_checkbox(self, bApply):
                    return bool(_checkbox_status(self, L.title_designer.backdrop.image.chx_flip_upside_down, bApply,
                                                 get_status=False))

                def get_checkbox_status(self):
                    return bool(_checkbox_status(self, L.title_designer.backdrop.image.chx_flip_upside_down,
                                                 get_status=True))

            class FlipLeftRight(BasePage):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                def set_checkbox(self, bApply):
                    return bool(_checkbox_status(self, L.title_designer.backdrop.image.chx_flip_left_to_right, bApply,
                                                 get_status=False))

                def get_checkbox_status(self):
                    return bool(_checkbox_status(self, L.title_designer.backdrop.image.chx_flip_left_to_right,
                                                 get_status=True))

        class Width(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.value = AdjustSet(self, L.title_designer.backdrop.width.value.group)

        class Height(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.value = AdjustSet(self, L.title_designer.backdrop.height.value.group)

        @step('[Action][TitleDesigner][Backdrop] Enable/ Disable maintain aspect ratio')
        def set_maintain_aspect_ratio(self, bApply):
            return _checkbox_status(self, L.title_designer.backdrop.chx_maintain_aspect_ratio, bApply, get_status=False)

        def get_maintain_aspect_ratio(self):
            return bool(_checkbox_status(self, L.title_designer.backdrop.chx_maintain_aspect_ratio, get_status=True))

        class Opacity(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.value = AdjustSet(self, L.title_designer.backdrop.opacity.value.group)

        class OffsetX(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.value = AdjustSet(self, L.title_designer.backdrop.offset_x.value.group)

        class OffsetY(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.value = AdjustSet(self, L.title_designer.backdrop.offset_y.value.group)

        class CurveRadius(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.value = AdjustSet(self, L.title_designer.backdrop.curve_radius.value.group)


class SpecialEffect(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size = Size(args[0], L.title_designer.special_effect.size.key_set)
        self.tail_size = TailSize(args[0], L.title_designer.special_effect.tail_size.key_set)
        self.tail_color = TailColor(args[0], L.title_designer.special_effect.tail_color.key_set)
        self.head_size = HeadSize(args[0], L.title_designer.special_effect.head_size.key_set)
        self.head_color = HeadColor(args[0], L.title_designer.special_effect.head_color.key_set)
        self.color = Color(args[0], L.title_designer.special_effect.color.key_set)
        self.length = Length(args[0], L.title_designer.special_effect.length.key_set)
        self.period = Period(args[0], L.title_designer.special_effect.period.key_set)
        self.density = AdjustSet(self, L.title_designer.special_effect.density.value.group)

    @step('[Action][TitleDesigner][SpecialEffect] Fold/ Unfold the tab')
    def set_unfold_tab(self, unfold=1):
        return _checkbox_status(self, L.title_designer.special_effect.btn_special_effect, unfold, get_status=False)

    @step('[Action][TitleDesigner][SpecialEffect] Apply effect')
    def apply_effect(self, index):
        target_locator = L.title_designer.special_effect.effect.thumb_template
        target_locator['index'] = index
        self.click(target_locator)
        time.sleep(DELAY_TIME)
        return True

    @step('[Action][TitleDesigner][SpecialEffect] Set the look of effect')
    def set_look_menu(self, index):
        target_option = L.title_designer.special_effect.look.look_group
        return bool(_set_option(self, L.title_designer.special_effect.look.cbx_look, target_option, option=index))

    def get_look_menu(self):
        target_option = L.title_designer.special_effect.look.look_group
        return _set_option(self, L.title_designer.special_effect.look.cbx_look, target_option, get_status=True)


class Size(KEComboSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = AdjustSet(self, L.title_designer.special_effect.size.value.group)


class TailSize(KEComboSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = AdjustSet(self, L.title_designer.special_effect.tail_size.value.group)


class TailColor(KEComboSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_color(self, HexColor):
        self.click(L.title_designer.special_effect.tail_color.btn_color)
        return _set_color(self, HexColor)


class HeadSize(KEComboSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = AdjustSet(self, L.title_designer.special_effect.head_size.value.group)


class HeadColor(KEComboSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_color(self, HexColor):
        self.click(L.title_designer.special_effect.head_color.btn_color)
        return _set_color(self, HexColor)


class Color(KEComboSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_color(self, HexColor):
        self.click(L.title_designer.special_effect.color.btn_color)
        return _set_color(self, HexColor)


class Length(KEComboSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = AdjustSet(self, L.title_designer.special_effect.length.value.group)


class Period(KEComboSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = AdjustSet(self, L.title_designer.special_effect.period.value.group)


class MotionBlur(Main_Page, BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.blur_length = AdjustSet(self, L.title_designer.motion_blur.blur_length.value.group)
        self.blur_density = AdjustSet(self, L.title_designer.motion_blur.blur_density.value.group)

    def set_unfold(self, unfold=1):
        return _checkbox_status(self, L.title_designer.motion_blur.btn_motion_blur, unfold, get_status=False)

    def get_tab_status(self):
        return _checkbox_status(self, L.title_designer.motion_blur.btn_motion_blur, get_status=True)

    def set_checkbox(self, bApply):
        return bool(_checkbox_status(self, L.title_designer.motion_blur.chx_motion_blur, bApply, get_status=False))

    def get_checkbox_status(self):
        return bool(_checkbox_status(self, L.title_designer.motion_blur.chx_motion_blur, get_status=True))


class Path(Main_Page, BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @step('[Action][TitleDesigner][Path] Fold/ Unfold the tab')
    def set_unfold(self, unfold=1):
        return _checkbox_status(self, L.title_designer.path.btn_path, unfold, get_status=False)

    def get_tab_status(self):
        return _checkbox_status(self, L.title_designer.path.btn_path, get_status=True)

    def select_dropdown_menu(self, index):
        target_option = L.title_designer.path.paths.path_group
        return _set_option(self, L.title_designer.path.paths.cbx_paths, target_option, option=index)

    def get_menu_status(self):
        target_option = L.title_designer.path.paths.path_group
        return _set_option(self, L.title_designer.path.paths.cbx_paths, target_option, get_status=True)

    def click_save_custom_button(self):
        self.exist_click(L.title_designer.path.btn_save_custom_path)
        time.sleep(DELAY_TIME * 1.5)
        return True

    @step('[Action][TitleDesigner][Path] Select and apply the path')
    def select_path(self, index):
        target_locator = L.title_designer.path.paths.thumb_template
        target_locator['index'] = index-1
        self.exist_click(target_locator)
        time.sleep(DELAY_TIME)
        return True

    def remove_custom_template(self, index):
        target_locator = L.title_designer.path.paths.thumb_template
        target_locator['index'] = index - 1
        self.exist_click(target_locator)
        self.right_click(target_locator)
        time.sleep(DELAY_TIME * 1.5)
        self.exist_click(L.title_designer.path.menu_remove_custom_path)
        time.sleep(DELAY_TIME * 1.5)
        self.exist_click(L.title_designer.backdrop.warning.btn_yes)
        time.sleep(DELAY_TIME * 1.5)
        return True


class AdjustPathOnCanvas(Main_Page, BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.adjust_in_canvas = AdjustInCanvas(*args, **kwargs)

    def resize_to_small(self, x, y, dot='lt'):
        return bool(self.adjust_in_canvas.resize(x, y, direction=dot, is_title=False))

    def resize_to_large(self, x, y, dot='lt'):
        return bool(self.adjust_in_canvas.resize(x, y, direction=dot, is_title=False, is_large=True))

    def drag_move_to_left(self, x):
        return bool(self.adjust_in_canvas.move(x, is_title=False, is_left=True))

    def drag_move_to_right(self, x):
        return bool(self.adjust_in_canvas.move(x, is_title=False, is_left=False))


class AdjustTitleOnCanvas(Main_Page, BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.adjust_in_canvas = AdjustInCanvas(*args, **kwargs)

    @step('[Action][TitleDesigner][AdjustTitleOnCanvas] Resize the title to small')
    def resize_to_small(self, x, y, dot='lt'):
        return bool(self.adjust_in_canvas.resize(x, y, direction=dot, is_title=True))

    def resize_to_large(self, x, y, dot='lt'):
        return bool(self.adjust_in_canvas.resize(x, y, direction=dot, is_title=True, is_large=True))

    @step('[Action][TitleDesigner][AdjustTitleOnCanvas] Move the title to left')
    def drag_move_to_left(self, x):
        return bool(self.adjust_in_canvas.move(x, is_title=True, is_left=True))

    @step('[Action][TitleDesigner][AdjustTitleOnCanvas] Move the title to right')
    def drag_move_to_right(self, x):
        return bool(self.adjust_in_canvas.move(x, is_title=True, is_left=False))

    @step('[Action][TitleDesigner][AdjustTitleOnCanvas] Rotate the title clockwise')
    def drag_rotate_clockwise(self, angle):
        return bool(self.adjust_in_canvas.rotate(angle=angle, is_title=False, is_clock=True))

    @step('[Action][TitleDesigner][AdjustTitleOnCanvas] Rotate the title anticlockwise')
    def drag_rotate_anticlockwise(self, angle):
        return bool(self.adjust_in_canvas.rotate(angle=angle, is_title=False, is_clock=False))

    @step('[Action][TitleDesigner][AdjustTitleOnCanvas] Move the title to right')
    def drag_move_MGT_to_right(self, drag_x=50, mouse_default_multiple=0.5):
        try:
            target = self.exist(L.title_designer.area.obj_title)
            x, y = target.AXPosition
            size_w, size_h = target.AXSize

            ori_pos = (x + size_w * mouse_default_multiple, y + size_h * mouse_default_multiple)
            des_pos = (ori_pos[0] + drag_x, ori_pos[1])
            self.mouse.drag_directly(ori_pos, des_pos)
            time.sleep(DELAY_TIME * 0.5)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            return False
        return True

    def drag_move_particle_to_left(self, x):
        return bool(self.adjust_in_canvas.move_particle(x, is_left=True))

class AdjustInCanvas(Main_Page, BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def remove_locator_by_size_and_position(self, title_locator_group,
                                            ref_locator=L.title_designer.area.frame_video_preview,
                                            ref_size=(200.0, 200.0)):
        try:
            el_group = self.exist_elements(title_locator_group)
            ref_pos = self.find(ref_locator).AXPosition[0]
            for el in el_group:
                if el.AXPosition[0] == ref_pos and el.AXSize == ref_size:
                    el_group.remove(el)
                    return el_group
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception

    def find_title_path_by_perimeter(self, find_title=True):
        try:
            perimeter = []
            el_new = self.remove_locator_by_size_and_position(L.title_designer.area.obj_title)
            if len(el_new) == 1:
                return el_new
            else:
                for el in el_new:
                    perimeter.append(sum(list(el.AXSize)))
                if find_title:
                    return el_new[perimeter.index(min(perimeter))]
                else:
                    return el_new[perimeter.index(max(perimeter))]
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception

    def find_title_path_by_index(self, find_title=False):
        try:
            el_new = self.remove_locator_by_size_and_position(L.title_designer.area.obj_title)
            if len(el_new) == 1:
                return el_new
            else:
                if find_title:
                    return el_new[-1]
                else:
                    return el_new[0]
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception

    def resize(self, drag_x=30, drag_y=30, direction='lt', is_title=False, is_large=False):
        try:
            # target = self.find_title_path_by_perimeter(is_title)
            #target = self.find_title_path_by_index(is_title)
            target = self.exist(L.title_designer.area.obj_title)
            ori_pos = target.AXPosition
            size_w, size_h = target.AXSize
            if not is_large:
                drag_x, drag_y = -drag_x, -drag_y
            des_pos = (ori_pos[0] - drag_x, ori_pos[1] - drag_y)
            if direction == 'rt':
                ori_pos = (ori_pos[0] + size_w, ori_pos[1])
                des_pos = (ori_pos[0] + drag_x, ori_pos[1] - drag_y)
            elif direction == 'lb':
                ori_pos = (ori_pos[0], ori_pos[1] + size_h)
                des_pos = (ori_pos[0] - drag_x, ori_pos[1] + drag_y)
            elif direction == 'rb':
                ori_pos = (ori_pos[0] + size_w, ori_pos[1] + size_h)
                des_pos = (ori_pos[0] + drag_x, ori_pos[1] + drag_y)
            self.mouse.drag_directly(ori_pos, des_pos)
            time.sleep(DELAY_TIME * 0.5)
        except Exception as e:
            raise Exception(f'Exception occurs. log={e}')
        return True

    def move(self, drag_x=50, is_title=False, is_left=False):
        try:
            # target = self.find_title_path_by_perimeter(is_title)
            #target = self.find_title_path_by_index(is_title)
            target = self.exist(L.title_designer.area.obj_title)
            x, y = target.AXPosition
            size_w, size_h = target.AXSize
            if is_left:
                drag_x = -drag_x
            ori_pos = (x + size_w * 0.45, y + size_h * 0.45)
            des_pos = (ori_pos[0] + drag_x, ori_pos[1])
            self.mouse.drag_directly(ori_pos, des_pos)
            time.sleep(DELAY_TIME * 0.5)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            return False(f'Exception occurs. log={e}')
        return True

    def move_particle(self, drag_x=50, is_left=False):
        try:
            target = self.exist(L.title_designer.area.view_title)
            x, y = target.center

            if is_left:
                drag_x = -drag_x
            ori_pos = (x , y)
            self.mouse.move(ori_pos[0], ori_pos[1])
            time.sleep(DELAY_TIME * 2)

            des_pos = (ori_pos[0] + drag_x, ori_pos[1])
            self.mouse.drag_directly(ori_pos, des_pos)
            time.sleep(DELAY_TIME * 0.5)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            return False
        return True

    def rotate(self, angle=45, pos_rotate_btn=12,  is_title=False, is_clock=False):
        try:
            # target = self.find_title_path_by_perimeter(is_title)
            #target = self.find_title_path_by_index(is_title)
            target = self.exist(L.title_designer.area.obj_title)
            x, y = target.AXPosition
            size_w, size_h = target.AXSize
            ori_pos = (x + size_w * 0.5, y - pos_rotate_btn)
            drag_x = size_w*0.5
            if not is_clock:
                drag_x = -drag_x
            if angle == 90:
                des_pos = (ori_pos[0] + drag_x, ori_pos[1] + size_h*0.5+12)
            elif angle == 135:
                des_pos = (ori_pos[0] + drag_x, ori_pos[1] + size_h*1)
            elif angle == 180:
                des_pos = (ori_pos[0], ori_pos[1] + size_h*1.1)
            else:
                des_pos = (ori_pos[0] + drag_x, ori_pos[1])
            self.mouse.drag_directly(ori_pos, des_pos)
            time.sleep(DELAY_TIME * 0.5)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            return False(f'Exception occurs. log={e}')
        return True


class Simple_Timeline(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.position = Keyframe_Operation(self, 'Position')
        self.scale = Keyframe_Operation(self, 'Scale')
        self.opacity = Keyframe_Operation(self, 'Opacity')
        self.rotation = Keyframe_Operation(self, 'Rotation')
        self.size = Keyframe_Operation(self, 'Size')
        self.color = Keyframe_Operation(self, 'Color')
        self.length = Keyframe_Operation(self, 'Length')
        self.period = Keyframe_Operation(self, 'Period')
        self.tail_size = Keyframe_Operation(self, 'Tail Size')
        self.tail_color = Keyframe_Operation(self, 'Tail Color')
        self.head_size = Keyframe_Operation(self, 'Head Size')
        self.head_color = Keyframe_Operation(self, 'Head Color')

    def select_keyframe_node_by_outline_row(self, index_outline_row=0, index_node=0):
        try:
            locator_outline_row = L.title_designer.simple_track.unit_keyframe_outline_row.copy()
            locator_outline_row[1]['get_all'] = True
            els_outline_row = self.exist(locator_outline_row)
            locator_node = L.title_designer.simple_track.keyframe_node_group.copy()
            locator_node['get_all'] = True
            els_node = self.exist(locator_node, els_outline_row[index_outline_row])
            el_node = els_node[index_node]
            if index_node == 0:
                self.el_click(el_node, 2, 0)  # special handing for first node
            elif index_node == len(els_node) - 1:
                self.el_click(el_node, -2, 0)  # special handing for last node
            else:
                self.el_click(el_node)
        except Exception as e:
            logger(f'Exception occurs: {e}')
            raise Exception
        return True

    def get_outline_row_by_attribute(self, attribute_name):  # get the outline row of category button
        try:
            index_row = -1
            el_row = -1
            locator_outline_row = L.title_designer.simple_track.unit_keyframe_attribute_outline_row.copy()
            locator_outline_row[2]['get_all'] = True
            el_outline_row = self.exist(locator_outline_row)
            locator_attribute_name = L.title_designer.simple_track.unit_attribute_name.copy()
            locator_attribute_name['AXValue'] = attribute_name
            locator_outline_row.append(locator_attribute_name)
            el_target = self.exist(locator_outline_row)
            pos_outline_row = el_target.AXParent.AXParent.AXPosition
            for idx_row in range(len(el_outline_row)):
                if el_outline_row[idx_row].AXPosition == pos_outline_row:
                    index_row = idx_row
                    el_row = el_outline_row[idx_row]
                    break
        except Exception as e:
            logger(f'Exception occurs: {e}')
            raise Exception
        return index_row, el_row

    # step 1: select specified keyframe node if index_keyframe_node is not equal to -1
    # step 2: click next keyframe
    def click_attribute_keyframe_operation(self, attribute_name, locator_operation=None, index_keyframe_node=-1):
        try:
            self.set_scrollbar_to_top() # reset scroll bar to top
            time.sleep(DELAY_TIME*0.5)
            self.set_attribute_visible(attribute_name) # workaround for v3630 select keyframe node issue
            # select keyframe node if specified index is not -1
            index_row, el_row = self.get_outline_row_by_attribute(attribute_name)
            logger(f'set value: {index_row=}, {el_row=}')
            if not index_keyframe_node == -1:
                self.select_keyframe_node_by_outline_row(index_row, index_keyframe_node)
                time.sleep(DELAY_TIME * 2)
                self.set_attribute_visible(attribute_name) # workaround for v3630 issue, attribute will out-off range after clicked keyframe
            if locator_operation:
                el_button = self.exist(locator_operation, el_row)
                self.el_click(el_button)
                time.sleep(DELAY_TIME * 0.5)
                value = el_button.AXEnabled
            else:
                value = True
        except Exception as e:
            logger(f'Exception occurs: {e}')
            raise Exception
        return value

    def drag_scroll_bar(self, locator, value):
        try:
            logger(f'input {value=}')
            if value < 0:
                value = 0
                logger(f'transfer value to {value}')
            elif value > 1:
                value = 1
                logger(f'transfer value to {value}')
            else:
                pass
            el_scrollbar = self.exist(locator)
            el_scrollbar.AXValue = value
            time.sleep(DELAY_TIME)
            # verify
            if not el_scrollbar.AXValue == value:
                logger('Fail to verify scroll bar value')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs: {e}')
            return False
        return True

    def get_scroll_bar_value(self, locator):
        try:
            el_scrollbar = self.exist(locator)
            value = el_scrollbar.AXValue
        except Exception as e:
            logger(f'Exception occurs: {e}')
            return False
        return value

    def set_outline_row_visible(self, el_row):
        try:
            # calculate the slider position
            row_pos = el_row.AXPosition
            row_size = el_row.AXSize
            scroll_area = L.title_designer.simple_track.scroll_area
            el_frame = self.exist(scroll_area)
            # print(f'Frame Info.: {el_frame.AXPosition=}, {el_frame.AXSize=}')
            table_frame_size = el_frame.AXSize
            table_frame_pos = el_frame.AXPosition
            percentage_scroll_y = 0
            is_drag_scroll_bar = 0
            if row_pos[1] > table_frame_pos[1] + table_frame_size[1] or \
                    (row_pos[1] + row_size[1]) > (table_frame_pos[1] + table_frame_size[
                1]):  # target or target bottom-side is lower than frame bottom-side
                # track_header_outline_view = L.title_designer.simple_timeline.track_header_outline_view
                logger(f'target bottom-side is lower than frame bottom-side')
                track_header_outline_view = L.title_designer.simple_track.track_header_outline_view.copy()
                # track_header_outline_view = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW'}
                table_detail_size = self.exist(track_header_outline_view).AXSize
                total_offset_length = table_detail_size[1] - table_frame_size[1]  # <<
                offset_row_move_to_frame_inside = (row_size[1] + row_pos[1]) - (
                            table_frame_pos[1] + table_frame_size[1])
                if offset_row_move_to_frame_inside < total_offset_length:
                    current_percentage_scroll_y = self.get_scroll_bar_value(scroll_area)  # if current position is not at 0
                    percentage_scroll_y = (
                                                      offset_row_move_to_frame_inside / total_offset_length) + current_percentage_scroll_y
                else:
                    percentage_scroll_y = 1
                is_drag_scroll_bar = 1
            elif row_pos[1] < table_frame_pos[1]:  # target is upper than frame up-side
                print(f'target up-side is upper than frame up-side')
                track_header_outline_view = L.title_designer.simple_track.track_header_outline_view.copy()
                # track_header_outline_view = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW'}
                table_detail_size = self.exist(track_header_outline_view).AXSize
                total_offset_length = table_detail_size[1] - table_frame_size[1]  # <<
                offset_row_move_to_frame_inside = table_frame_pos[1] - row_pos[1]
                if offset_row_move_to_frame_inside < total_offset_length:
                    current_percentage_scroll_y = self.get_scroll_bar_value(scroll_area)  # if current position is not at 0
                    percentage_scroll_y = current_percentage_scroll_y - (
                                offset_row_move_to_frame_inside / total_offset_length)
                else:
                    percentage_scroll_y = 1
                is_drag_scroll_bar = 1
            else:
                print(f'target is inside the frame')
                pass

            print(f'{percentage_scroll_y=}')
            if is_drag_scroll_bar:
                # print(f'{percentage_scroll_y=}')
                if percentage_scroll_y < 0:
                    percentage_scroll_y = 0
                self.drag_scroll_bar(scroll_area, percentage_scroll_y)
                time.sleep(DELAY_TIME * 2)
            # ----------------------------
        except Exception as e:
            logger(f'Exception occurs: {e}')
            return False
        return True

    def set_attribute_visible(self, attribute_name):
        try:
            # get attribute row information
            index_row, el_row = self.get_outline_row_by_attribute(attribute_name)
            self.set_outline_row_visible(el_row)
        except Exception as e:
            logger(f'Exception occurs: {e}')
            return False
        return True

    def set_scrollbar_to_top(self):
        return self.drag_scroll_bar(L.title_designer.simple_track.scroll_area, 0)


class Keyframe_Operation(BasePage):
    def __init__(self, driver, attribute_name):
        self.driver = driver
        self.attribute_name = attribute_name
        self.mouse_position = None

    def click_next_keyframe(self, index_keyframe_node=-1):
        locator_operation = L.title_designer.simple_track.btn_next_keyframe
        # locator_operation = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_NEXT_KEYFRAME'}
        return self.driver.click_attribute_keyframe_operation(self.attribute_name, locator_operation, index_keyframe_node-1)

    def click_add_remove_keyframe(self, index_keyframe_node=0):
        locator_operation = L.title_designer.simple_track.btn_add_remove_keyframe
        # locator_operation = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_ADD_REMOVE_KEYFRAME'}
        return self.driver.click_attribute_keyframe_operation(self.attribute_name, locator_operation, index_keyframe_node-1)

    def click_previous_keyframe(self, index_keyframe_node=0):
        locator_operation = L.title_designer.simple_track.btn_previous_keyframe
        # locator_operation = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_PREV_KEYFRAME'}
        return self.driver.click_attribute_keyframe_operation(self.attribute_name, locator_operation, index_keyframe_node-1)

    def right_click_menu_item(self, locator_option, index_keyframe_node=0):
        try:
            self.driver.click_attribute_keyframe_operation(self.attribute_name, None, index_keyframe_node - 1)
            time.sleep(DELAY_TIME)
            self.mouse_position = self.get_mouse_pos()
            self.driver.right_click()
            el_option = self.driver.exist(locator_option)
            if not el_option.AXEnabled:
                self.driver.click(None)
                return False
            if el_option.AXMenuItemMarkChar == '✓': # for Hold and Linear
                self.driver.click(None)
                return True
            self.driver.el_click(el_option)
        except Exception as e:
            logger(f'Exception occurs: {e}')
            return False
        return True

    def get_right_click_menu_item_status(self, locator_option, index_keyframe_node=0): # check AXMenuItemMarkChar
        try:
            self.driver.click_attribute_keyframe_operation(self.attribute_name, None, index_keyframe_node - 1)
            time.sleep(DELAY_TIME)
            self.mouse_position = self.get_mouse_pos()
            self.driver.right_click()
            el_option = self.driver.exist(locator_option)
            if not el_option.AXMenuItemMarkChar == '✓':  # for Hold and Linear
                return False
        except Exception as e:
            logger(f'Exception occurs: {e}')
            return False
        finally:
            self.driver.click(None)
        return True

    def right_click_menu_remove_keyframe(self, index_keyframe_node=1):
        try:
            self.right_click_menu_item(L.title_designer.timeline_context_menu.remove_keyframe, index_keyframe_node)
            self.driver.set_attribute_visible(self.attribute_name)
            time.sleep(DELAY_TIME)
            self.driver.mouse.move(*self.mouse_position)
            self.driver.right_click()
            el_option = self.driver.exist(L.title_designer.timeline_context_menu.remove_keyframe)
            if not el_option.AXTitle == 'Add New Keyframe': # to verify the 'Add New Keyframe' option exists
                raise Exception
        except Exception as e:
            logger(f'Exception occurs: {e}')
            return False
        finally:
            self.driver.click(None)
        return True

    def right_click_menu_remove_all_keyframes(self, index_keyframe_node=1):
        try:
            self.right_click_menu_item(L.title_designer.timeline_context_menu.remove_all_keyframe, index_keyframe_node)
            # click [Yes] of confirm dialog
            time.sleep(DELAY_TIME)
            self.driver.exist_click(locator=L.base.confirm_dialog.btn_yes, timeout=3)
            time.sleep(DELAY_TIME)
            self.driver.set_attribute_visible(self.attribute_name)
            time.sleep(DELAY_TIME*0.5)
            self.driver.mouse.move(*self.mouse_position)
            self.driver.right_click()
            el_option = self.driver.exist(L.title_designer.timeline_context_menu.remove_all_keyframe)
            if el_option.AXEnabled:  # to verify the 'Remove All Keyframes' option is disabled
                raise Exception
        except Exception as e:
            logger(f'Exception occurs: {e}')
            return False
        finally:
            self.driver.click(None)
        return True

    def right_click_menu_duplicate_previous_keyframe(self, index_keyframe_node=1):
        return self.right_click_menu_item(L.title_designer.timeline_context_menu.duplicate_previous_keyframe, index_keyframe_node)

    def right_click_menu_duplicate_next_keyframe(self, index_keyframe_node=1):
        return self.right_click_menu_item(L.title_designer.timeline_context_menu.duplicate_next_keyframe, index_keyframe_node)

    def right_click_menu_apply_hold(self, index_keyframe_node=1):
        return self.right_click_menu_item(L.title_designer.timeline_context_menu.hold, index_keyframe_node)

    def right_click_menu_get_hold_status(self, index_keyframe_node=1):
        return self.get_right_click_menu_item_status(L.title_designer.timeline_context_menu.hold, index_keyframe_node)

    def right_click_menu_apply_linear(self, index_keyframe_node=1):
        return self.right_click_menu_item(L.title_designer.timeline_context_menu.linear, index_keyframe_node)

    def right_click_menu_get_linear_status(self, index_keyframe_node=1):
        return self.get_right_click_menu_item_status(L.title_designer.timeline_context_menu.linear, index_keyframe_node)

    def show(self):
        return self.driver.set_attribute_visible(self.attribute_name)

