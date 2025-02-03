import time, datetime, os, copy

from .base_page import BasePage
from ATFramework.utils import logger
from .locator import locator as L

DELAY_TIME = 1 # sec

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
        raise Exception
    return True

def _set_option(self, _locator_cbx, _locator_group, option=1, get_status=False, path=None):
    try:
        target = self.exist(_locator_cbx)
        current_title = str(target.AXTitle)
        if get_status:
            return current_title
        else:
            # self.click(_locator_cbx)
            # time.sleep(DELAY_TIME*1)
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
        time.sleep(DELAY_TIME*2)
        self.click(L.title_designer.colors.btn_close)
        time.sleep(DELAY_TIME)
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        return False
    return True

def _get_color(self):
    try:
        self.color_picker_switch_category_to_RGB()
        time.sleep(DELAY_TIME)
        current_hex = self.exist(L.title_designer.colors.input_hex_color)
        time.sleep(DELAY_TIME)
        self.exist(L.title_designer.colors.btn_close).press()
        time.sleep(DELAY_TIME)
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        return False
    return current_hex.AXValue

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

def _adjust_slider(self, _locator, value):
    target = self.exist(_locator)
    target.AXValue = float(value)
    return True

def _set_value(self, value):
    target = self.driver.exist(self.locators[1])
    self.driver.mouse.click(*target.center)
    target.AXValue = str(value)
    self.driver.keyboard.enter()
    return True

class Subtitle_Room(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.library_menu = self.Library_Menu(*args, **kwargs)
        self.more = self.More_Button(*args, **kwargs)
        self.auto_function = self.Auto_Function(*args, **kwargs)
        self.position = self.Position(*args, **kwargs)
        self.character = self.Character(*args, **kwargs)

    class Library_Menu(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def click_auto_transcribe(self):
            result = self.exist(L.subtitle_room.library_menu.btn_speech_to_text)
            if result:
                self.click(L.subtitle_room.library_menu.btn_speech_to_text)

                # Verify step (Check to pop up Speech to text window)
                if self.exist(L.subtitle_room.speech_to_text_window.main_window, timeout=6):
                    return True
                else:
                    logger('Cannot find (Speech to text) button')
                    return False
            else:
                logger('Cannot find (Speech to text) button')
                return False

        def click_manually_create(self):
            result = self.exist(L.subtitle_room.library_menu.btn_create_manually)
            if result:
                self.click(L.subtitle_room.library_menu.btn_create_manually)
                time.sleep(DELAY_TIME*1.5)

                # Verify step (Check the button [btn_create_manually] disappear)
                if not self.exist(L.subtitle_room.library_menu.btn_create_manually):
                    return True
                else:
                    logger('Verify NG - Still find the button [btn_create_manually]')
                    return False
            else:
                logger('Cannot find the button [btn_create_manually]')
                return False

        def click_import_subtitle_file(self, full_path):
            try:
                result = self.exist(L.subtitle_room.library_menu.btn_import_file)
                if result:
                    self.click(L.subtitle_room.library_menu.btn_import_file)
                    time.sleep(DELAY_TIME)

                    if not self.select_file(full_path):
                        raise Exception('Cannot select file w/ full_path')
                else:
                    return False

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

    class More_Button(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def click_auto_transcribe(self):
            self.click(L.subtitle_room.btn_more)
            time.sleep(DELAY_TIME*0.5)
            self.select_right_click_menu('Speech to Text')

        def click_clear_all_subtitles(self):
            self.click(L.subtitle_room.btn_more)
            time.sleep(DELAY_TIME*0.5)
            self.select_right_click_menu('Clear All Subtitles')

        def click_import_subtitle_file(self):
            self.click(L.subtitle_room.btn_more)
            time.sleep(DELAY_TIME * 0.5)
            self.select_right_click_menu('Import subtitles from SRT/TXT file')

        def click_export_str(self, no_font=1):
            # Argument:
            # no_font = 1 : select "Export Without Style Formatting"
            # no_font = 0 : select "Export With Additional SubRip Style Information"

            # For example:
            # srt_folder = Test_Material_Folder + 'Subtitle_Room'
            # subtitle_room_page.more.click_export_str(0)
            # main_page.handle_save_file_dialog('Subtitle_test_additional_font.srt', srt_folder)

            try:
                font_list = ['Export With Additional SubRip Style Information', 'Export Without Style Formatting']
                self.click(L.subtitle_room.btn_more)
                time.sleep(DELAY_TIME * 0.5)
                self.select_right_click_menu('Export as an SRT File')
                time.sleep(DELAY_TIME * 0.5)
                self.select_right_click_menu(font_list[no_font])

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        def get_clear_all_subtitle_status(self):
            self.click(L.subtitle_room.btn_more)
            time.sleep(DELAY_TIME * 0.5)
            menu = self.exist({'AXTitle': 'Clear All Subtitles', 'AXRole': 'AXMenuItem'})
            time.sleep(DELAY_TIME * 0.5)

            self.right_click()
            return menu.AXEnabled

    class Auto_Function(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def select_location(self, down_times=1, up_times=0):
            self.click(L.subtitle_room.speech_to_text_window.btn_location)
            if down_times:
                x = 0
                for x in range(down_times):
                    self.keyboard.press(self.keyboard.key.down)
                    time.sleep(DELAY_TIME*0.5)
            if up_times:
                y = 0
                for y in range(up_times):
                    self.keyboard.press(self.keyboard.key.up)
                    time.sleep(DELAY_TIME*0.5)

            self.press_enter_key()
            time.sleep(DELAY_TIME * 0.5)

        def get_location_status(self):
            elem = self.exist(L.subtitle_room.speech_to_text_window.btn_location)
            if elem:
                return elem.AXTitle
            else:
                return None

        def select_LANG(self, option):
            el_option = ['ENG', 'JPN', 'CHT']
            # el_menu = ['English (United States)', 'Japanese', 'Mandarin Chinese (Taiwan)']

            # [2025/01/15] update for new UI flow of select langugae
            target_option = L.subtitle_room.speech_to_text_window.lan_with_title_group

            if option not in el_option:
                logger(f'Cannot find {option} category')
                return False
            
            index = el_option.index(option)+1

            logger(f'index={index}, start to select')
            self.click(L.subtitle_room.speech_to_text_window.btn_language)
            time.sleep(DELAY_TIME * 1)

            self.mouse.move(1920/2, 1080/2)

            if index == 1:
                self.keyboard.press(self.keyboard.key.page_up)
            elif index == 2 or index==3:
                self.keyboard.press(self.keyboard.key.page_down)
            _set_option(self, L.subtitle_room.speech_to_text_window.btn_language, target_option, index)

            # [2025/01/15] Leave the old version of code for reference
            # loop_times = [0, 10,13]

            # custom_language = -1
            # for x in range(3):
            #     if el_option[x] == option:
            #         custom_language = x
            #         break

            # if custom_language == -1:
            #     logger(f'Cannot Find {option} category')
            #     raise Exception
            # logger(el_menu[x])

            # # IF apply ENG, can skip follow steps
            # if loop_times[x] < 1:
            #     return

            # self.click(L.subtitle_room.speech_to_text_window.btn_language)

            # elem = self.exist({'AXValue': f'{el_menu[x]}', 'AXRole': 'AXStaticText'})
            # logger(elem.AXPosition)
            # for x in range(loop_times[x]):
            #     self.keyboard.press(self.keyboard.key.down)
            #     time.sleep(DELAY_TIME * 0.5)

            # self.press_enter_key()
            # time.sleep(DELAY_TIME * 0.5)


        def get_LANG_status(self):
            elem = self.exist(L.subtitle_room.speech_to_text_window.btn_language)
            if elem:
                return elem.AXTitle
            else:
                return None

        def get_selected_range_status(self):
            elem = self.exist(L.subtitle_room.speech_to_text_window.checkbox_selected_range)
            if elem:
                return elem.AXValue
            else:
                return None

        def set_selected_range_only(self, option=1):
            current_value = self.get_selected_range_status()
            if current_value != option:
                self.click(L.subtitle_room.speech_to_text_window.checkbox_selected_range)

        def click_cancel(self):
            self.click(L.subtitle_room.speech_to_text_window.btn_cancel)

        def click_close(self):
            self.click(L.subtitle_room.speech_to_text_window.btn_close)

        def click_create(self):
            self.click(L.subtitle_room.speech_to_text_window.btn_create)

    class Position(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def set_x_slider(self, value):
            _adjust_slider(self, L.subtitle_room.position.x_slider, value)
            time.sleep(DELAY_TIME)

        def set_x_value(self, value):
            target = L.subtitle_room.position.editbox_x_field
            _set_edittext(self, target, value)

        def get_x_value(self):
            elem = L.subtitle_room.position.editbox_x_field
            target = self.exist(elem)
            return target.AXValue

        def set_y_slider(self, value):
            _adjust_slider(self, L.subtitle_room.position.y_slider, value)
            time.sleep(DELAY_TIME)

        def set_y_value(self, value):
            target = L.subtitle_room.position.editbox_y_field
            _set_edittext(self, target, value)

        def get_y_value(self):
            elem = L.subtitle_room.position.editbox_y_field
            target = self.exist(elem)
            return target.AXValue

        def apply_to_all(self):
            self.click(L.subtitle_room.position.btn_apply_to_all)
            time.sleep(DELAY_TIME * 0.5)

        def click_reset_btn(self):
            self.click(L.subtitle_room.position.btn_reset)
            time.sleep(DELAY_TIME * 0.5)

        def close_window(self):
            self.click(L.subtitle_room.position.btn_close)

    class Character(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def get_font_type(self):
            target_elem = self.exist(L.subtitle_room.character.cbx_font)
            if not target_elem:
                raise Exception
            else:
                return target_elem.AXValue

        def apply_font_type(self, font_type):
            try:
                if not self.exist(L.subtitle_room.character.cbx_font):
                    raise Exception
                target_elem = self.exist(L.subtitle_room.character.cbx_font)
                ori_pos = target_elem.AXPosition
                size_w, size_h = target_elem.AXSize
                new_pos = (ori_pos[0] + size_w * (0.5), ori_pos[1] + size_h * (0.5))

                self.mouse.move(new_pos[0], new_pos[1])
                self.mouse.click(times=2)
                self.press_backspace_key()

                current_font = self.get_font_type()
                while current_font:
                    self.mouse.click(times=2)
                    self.press_backspace_key()
                    time.sleep(0.5)
                    current_font = self.get_font_type()

                self.keyboard.send(font_type)
                self.click(L.subtitle_room.character.cbx_font_pop_up_cell)
                self.press_enter_key()

                # Verify step:
                current_font = self.get_font_type()
                if current_font == font_type:
                    return True
                else:
                    return False

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        def get_style_status(self):
            try:
                target_elem = self.exist(L.subtitle_room.character.cbx_style)
                if not target_elem:
                    raise Exception
                else:
                    return target_elem.AXTitle

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        def apply_Bold_Italic(self):
            try:
                target_elem = self.exist(L.subtitle_room.character.cbx_style)
                if not target_elem:
                    raise Exception

                self.click(L.subtitle_room.character.cbx_style)
                time.sleep(0.5)
                self.click(L.subtitle_room.character.option_bold_italic)

                # Verify Step
                result = self.get_style_status()
                if result != 'Bold Italic':
                    raise Exception

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def get_size(self):
            try:
                target_elem = self.exist(L.subtitle_room.character.cbx_size)
                if not target_elem:
                    raise Exception
                else:
                    return target_elem.AXTitle

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        def apply_size(self, value):
            # parameter: value should be string type
            # e.g. apply_size('36')
            try:
                target_elem = self.exist(L.subtitle_room.character.cbx_size)
                if not target_elem:
                    raise Exception
                self.click(L.subtitle_room.character.cbx_size)
                self.keyboard.send(value)
                self.press_enter_key()

                # Verify Step
                result = self.get_size()
                if result != value:
                    return False

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def get_alignment(self):
            try:
                target_elem = self.exist(L.subtitle_room.character.cbx_alignment)
                if not target_elem:
                    raise Exception
                else:
                    return target_elem.AXTitle

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        def apply_align_center(self):
            try:
                target_elem = self.exist(L.subtitle_room.character.cbx_alignment)
                if not target_elem:
                    raise Exception
                else:
                    self.click(L.subtitle_room.character.cbx_alignment)
                    time.sleep(0.5)
                    self.click(L.subtitle_room.character.option_align_center)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        def apply_align_right(self):
            try:
                target_elem = self.exist(L.subtitle_room.character.cbx_alignment)
                if not target_elem:
                    raise Exception
                else:
                    self.click(L.subtitle_room.character.cbx_alignment)
                    time.sleep(0.5)
                    self.click(L.subtitle_room.character.option_align_right)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        def get_text_checkbox(self):
            try:
                target_elem = self.exist(L.subtitle_room.character.checkbox_text)
                if not target_elem:
                    raise Exception
                else:
                    return target_elem.AXValue

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        def set_text_checkbox(self, bCheck=1):
            try:
                target_elem = self.exist(L.subtitle_room.character.checkbox_text)
                if not target_elem:
                    raise Exception

                if target_elem.AXValue != bCheck:
                    self.click(L.subtitle_room.character.checkbox_text)
                    time.sleep(0.5)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        def get_shadow_checkbox(self):
            try:
                target_elem = self.exist(L.subtitle_room.character.checkbox_shadow)
                if not target_elem:
                    raise Exception
                else:
                    return target_elem.AXValue

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        def set_shadow_checkbox(self, bCheck=1):
            try:
                target_elem = self.exist(L.subtitle_room.character.checkbox_shadow)
                if not target_elem:
                    raise Exception

                if target_elem.AXValue != bCheck:
                    self.click(L.subtitle_room.character.checkbox_shadow)
                    time.sleep(0.5)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        def get_border_checkbox(self):
            try:
                target_elem = self.exist(L.subtitle_room.character.checkbox_border)
                if not target_elem:
                    raise Exception
                else:
                    return target_elem.AXValue

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        def set_border_checkbox(self, bCheck=1):
            try:
                target_elem = self.exist(L.subtitle_room.character.checkbox_border)
                if not target_elem:
                    raise Exception

                if target_elem.AXValue != bCheck:
                    self.click(L.subtitle_room.character.checkbox_border)
                    time.sleep(0.5)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        def set_text_color(self, HexColor):
            try:
                if not self.exist(L.subtitle_room.character.colorpicker_text):
                    logger("No text colorpicker")
                    raise Exception
                self.click(L.subtitle_room.character.colorpicker_text)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return _set_color(self, HexColor)

        def get_text_color(self):
            self.click(L.subtitle_room.character.colorpicker_text)
            return _get_color(self)

        def set_shadow_color(self, HexColor):
            try:
                if not self.exist(L.subtitle_room.character.colorpicker_shadow):
                    logger("No text colorpicker")
                    raise Exception
                self.click(L.subtitle_room.character.colorpicker_shadow)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return _set_color(self, HexColor)

        def get_shadow_color(self):
            self.click(L.subtitle_room.character.colorpicker_shadow)
            return _get_color(self)

        def set_border_color(self, HexColor):
            try:
                if not self.exist(L.subtitle_room.character.colorpicker_border):
                    logger("No text colorpicker")
                    raise Exception
                self.click(L.subtitle_room.character.colorpicker_border)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return _set_color(self, HexColor)

        def get_border_color(self):
            self.click(L.subtitle_room.character.colorpicker_border)
            return _get_color(self)

        def apply_to_all(self):
            self.click(L.subtitle_room.character.btn_apply_all)
            time.sleep(DELAY_TIME * 0.5)

        def click_ok(self):
            self.click(L.subtitle_room.character.btn_ok)
            time.sleep(DELAY_TIME * 0.5)

    def handle_selected_track_no_audio_source(self):
        elem = self.exist(L.main.confirm_dialog.alter_msg)
        if elem.AXValue.startswith("The selected track has no audio source."):
            self.click(L.main.confirm_dialog.btn_ok)
            return True
        else:
            return False

    def handle_replace_all_existing_subtitle_text(self, option_cancel=0):
        # 0 : click Continue
        # 1 : click Cancel
        if option_cancel:
            selected_button = L.main.confirm_dialog.btn_no
        else:
            selected_button = L.main.confirm_dialog.btn_continue

        elem = self.exist(L.main.confirm_dialog.alter_msg)
        if elem.AXValue.startswith("This will replace all the existing subtitle text."):
            self.click(selected_button)

    def handle_mini_duration_warning_message(self):
        elem = self.exist(L.main.confirm_dialog.alter_msg)
        if elem.AXValue.startswith("There is a minimum duration for subtitles."):
            self.click(L.main.confirm_dialog.btn_ok)
            return True
        else:
            return False

    def check_to_show_speech_progress_bar(self):
        if self.exist(L.subtitle_room.handle_progress_dialog.btn_cancel):
            return True
        else:
            return False

    def click_i_button(self):
        self.click(L.subtitle_room.btn_i)
        time.sleep(DELAY_TIME)

        # Verify step and Click [Close] button
        if self.exist(L.subtitle_room.subtitle_editing_tips.txt_title):
            self.click(L.subtitle_room.subtitle_editing_tips.btn_close)
            return True
        else:
            logger('Verify NG - Cannot find the string (How to edit in subtitle room?)')
            return False

    def click_add_btn(self, is_click=1):
        elem = self.exist(L.subtitle_room.btn_add_subtitle)
        #logger(elem.AXEnabled)
        # Button gray out > return False
        if not elem.AXEnabled:
            return False
        else:
            if is_click:
                self.click(L.subtitle_room.btn_add_subtitle)
            return True

    def click_del_btn(self, is_click=1):
        elem = self.exist(L.subtitle_room.btn_del_subtitle)
        #logger(elem.AXEnabled)
        # Button gray out > return False
        if not elem.AXEnabled:
            return False
        else:
            if is_click:
                self.click(L.subtitle_room.btn_del_subtitle)
            return True

    def click_change_subtitle_format(self):
        elem = self.exist(L.subtitle_room.btn_change_format)
        #logger(elem.AXEnabled)
        # Button gray out > return False
        if not elem.AXEnabled:
            return False
        else:
            self.click(L.subtitle_room.btn_change_format)
            return True

    def select_subtitle_row(self, no):
        # no = 1, select 1st subtitle text
        # no = 2, select 2nd subtitle text

        table_row_list = self.find(L.subtitle_room.subtitle_region.rows_clip)
        index = no -1
        target_elem = table_row_list[index]
        #logger(target_elem)

        if target_elem:
            ori_pos = target_elem.AXPosition
            size_w, size_h = target_elem.AXSize
            new_pos = (ori_pos[0] + size_w * (0.5), ori_pos[1] + size_h * (0.5))
            self.mouse.move(new_pos[0], new_pos[1])
            self.mouse.click()
            time.sleep(0.5)
            return True
        else:
            logger(f"Cannot find the {no}th subtitle")
            return False

    def multiple_select_subtitle_row(self, no1, no2, no3=None):
        self.select_subtitle_row(no1)
        self.tap_command_and_hold()
        self.select_subtitle_row(no2)
        if no3:
            self.select_subtitle_row(no3)
        self.release_command_key()
        time.sleep(0.5)

    def get_start_time(self, no):
        # no = 1, select 1st subtitle text
        # no = 2, select 2nd subtitle text

        table_row_list = self.find(L.subtitle_room.subtitle_region.rows_clip)
        index = no - 1
        target_elem = table_row_list[index]
        # logger(target_elem)

        if target_elem:
            elem = target_elem.AXChildren[1].AXChildren[0].AXChildren[0]
            return elem.AXValue
        else:
            logger("Cannot find the elem")
            return None

    def set_start_time(self, no, timecode):
        try:
            # no = 1, select 1st subtitle text
            # no = 2, select 2nd subtitle text

            table_row_list = self.find(L.subtitle_room.subtitle_region.rows_clip)
            index = no - 1
            target_elem = table_row_list[index]

            if not target_elem:
                raise Exception
            end_time_elem = target_elem.AXChildren[1].AXChildren[0].AXChildren[0]
            w, h = end_time_elem.AXSize
            x, y = end_time_elem.AXPosition

            pos_click = tuple(map(int, (x + w * 0.1, y + h * 0.5)))
            self.mouse.click(*pos_click)
            self.mouse.click()
            time.sleep(1)
            self.keyboard.send(timecode.replace("_", ""))
            self.keyboard.enter()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception

    def get_end_time(self, no):
        # no = 1, select 1st subtitle text
        # no = 2, select 2nd subtitle text

        table_row_list = self.find(L.subtitle_room.subtitle_region.rows_clip)
        index = no - 1
        target_elem = table_row_list[index]
        # logger(target_elem)

        if target_elem:
            elem = target_elem.AXChildren[2].AXChildren[0].AXChildren[0]
            return elem.AXValue
        else:
            logger("Cannot find the elem")
            return None

    def set_end_time(self, no, timecode):
        try:
            # no = 1, select 1st subtitle text
            # no = 2, select 2nd subtitle text

            table_row_list = self.find(L.subtitle_room.subtitle_region.rows_clip)
            index = no - 1
            target_elem = table_row_list[index]

            if not target_elem:
                raise Exception
            end_time_elem = target_elem.AXChildren[2].AXChildren[0].AXChildren[0]
            w, h = end_time_elem.AXSize
            x, y = end_time_elem.AXPosition

            pos_click = tuple(map(int, (x + w * 0.1, y + h * 0.5)))
            self.mouse.click(*pos_click)
            self.mouse.click()
            time.sleep(1)
            self.keyboard.send(timecode.replace("_", ""))
            self.keyboard.enter()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception

    def modify_subtitle_text_without_clear_old_text(self, no, string1, right_times=0):
        # This page function [Only for Bug regression] used:
        # When click subtitle no. to edit mode "without" clear all
        # if right_times > 0, it can press right key several times to move cursor position
        try:
            # no = 1, select 1st subtitle text
            # no = 2, select 2nd subtitle text
            # string1 : First row subtitle
            # string2 : Second row subtitle

            table_row_list = self.find(L.subtitle_room.subtitle_region.rows_clip)
            index = no - 1
            target_elem = table_row_list[index]

            if not target_elem:
                raise Exception
            end_time_elem = target_elem.AXChildren[3]
            logger(end_time_elem.AXPosition)

            w, h = end_time_elem.AXSize
            x, y = end_time_elem.AXPosition

            pos_click = tuple(map(int, (x + 5, y + h * 0.1)))
            self.mouse.click(*pos_click)
            time.sleep(1)
            # Move cursor to right position
            if right_times:
                for x in range(right_times):
                    self.keyboard.right()
                    time.sleep(0.5)
            self.keyboard.send(string1)

            # Leave (Edit mode)
            #self.mouse.click(x - 5, y)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception

    def modify_subtitle_text(self, no, string1, string2=None):
        try:
            # no = 1, select 1st subtitle text
            # no = 2, select 2nd subtitle text
            # string1 : First row subtitle
            # string2 : Second row subtitle

            table_row_list = self.find(L.subtitle_room.subtitle_region.rows_clip)
            index = no - 1
            target_elem = table_row_list[index]

            if not target_elem:
                raise Exception
            end_time_elem = target_elem.AXChildren[3]
            logger(end_time_elem.AXPosition)

            w, h = end_time_elem.AXSize
            x, y = end_time_elem.AXPosition
            

            pos_click = tuple(map(int, (x + 5, y + h * 0.1)))
            self.mouse.click(*pos_click)
            self.double_click()
            time.sleep(1)
            self.tap_SelectAll_hotkey()
            self.tap_Remove_hotkey()
            time.sleep(1)
            self.keyboard.send(string1)
            if string2:
                self.keyboard.enter()
                self.keyboard.send(string2)

            # Leave (Edit mode)
            self.mouse.click(x - 5, y)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception

    def click_adjust_pos_btn(self):
        elem = self.exist(L.subtitle_room.btn_adjust_pos)
        #logger(elem.AXEnabled)
        # Button gray out > return False
        if not elem.AXEnabled:
            return False
        else:
            self.click(L.subtitle_room.btn_adjust_pos)
            return True

    def drag_scroll_bar(self, value):
        try:
            time.sleep(DELAY_TIME)
            self.exist(L.subtitle_room.scroll_bar).AXValue = float(value)
            time.sleep(DELAY_TIME)
            # Verify Step
            if float(value) == self.exist(L.subtitle_room.scroll_bar).AXValue:
                return True
            else:
                return False
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def input_search_field(self, strText):
        target = self.exist(L.subtitle_room.search_field)
        self.el_click(target)
        self.mouse.click(times=2)
        time.sleep(DELAY_TIME)
        target.AXValue = str(strText)
        time.sleep(DELAY_TIME * 0.5)
        self.press_enter_key()
        time.sleep(DELAY_TIME * 1)

    def cancel_search(self):
        self.click(L.subtitle_room.cancel_button)
        time.sleep(DELAY_TIME)

    def click_replace_button(self):
        self.click(L.subtitle_room.btn_replace)
        time.sleep(DELAY_TIME)

    def check_replace_button_status(self):
        elem = self.exist(L.subtitle_room.btn_replace)
        if elem:
            return elem.AXEnabled
        else:
            return None

    def input_replace_field(self, strText):
        target = self.exist(L.subtitle_room.replace_txt_field)
        self.el_click(target)
        self.mouse.click(times=2)
        time.sleep(DELAY_TIME)
        target.AXValue = str(strText)
        time.sleep(DELAY_TIME * 0.5)
        self.press_enter_key()
        time.sleep(DELAY_TIME * 1)

    def click_replace_single_button(self):
        self.click(L.subtitle_room.btn_replace_single)
        time.sleep(DELAY_TIME)

    def click_replace_all_button(self):
        self.click(L.subtitle_room.btn_replace_all)
        time.sleep(DELAY_TIME)

    def click_next_button(self, times=1):
        for x in range(times):
            self.click(L.subtitle_room.btn_next)
            time.sleep(DELAY_TIME*0.6)

    def click_split_btn(self):
        elem = self.exist(L.subtitle_room.btn_split)
        #logger(elem.AXEnabled)
        # Button gray out > return False
        if not elem.AXEnabled:
            return False
        else:
            self.click(L.subtitle_room.btn_split)
            return True

    def get_split_btn(self):
        elem = self.exist(L.subtitle_room.btn_split)
        #logger(elem.AXEnabled)
        return elem.AXEnabled

    def click_merge_btn(self):
        elem = self.exist(L.subtitle_room.btn_merge)
        #logger(elem.AXEnabled)
        # Button gray out > return False
        if not elem.AXEnabled:
            return False
        else:
            self.click(L.subtitle_room.btn_merge)
            return True

    def get_merge_btn(self):
        elem = self.exist(L.subtitle_room.btn_merge)
        #logger(elem.AXEnabled)
        return elem.AXEnabled

    def get_subtitle_room_status(self):
        elem = self.exist(L.subtitle_room.btn_subtitle_room)
        #logger(elem.AXEnabled)
        return elem.AXEnabled