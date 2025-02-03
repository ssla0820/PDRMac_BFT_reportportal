import time, datetime, os, copy

from .base_page import BasePage
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
from .locator import locator as L
from .main_page import Main_Page

DELAY_TIME = 1 # sec

class Audio_Editing(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.audio_ducking = self.Audio_Ducking(*args, **kwargs)
        self.audio_editor = self.Audio_Editor(*args, **kwargs)
        self.smart_fit = self.Smart_Fit(*args, **kwargs)

    class Audio_Ducking(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    class Smart_Fit(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def get_custom_new_duration(self):
            try:
                # Check if enter (Smart Fit) or not
                if self.is_not_exist(L.audio_editing.smart_fit.main_window):
                    raise Exception

                # If not find (new duration)'s timecode elem, raise Exception
                if self.is_not_exist(L.audio_editing.smart_fit.new_duration_timecode):
                    raise Exception

                timecode = self.exist(L.audio_editing.smart_fit.new_duration_timecode).AXValue
                return timecode
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        def set_custom_new_duration(self, timecode):
            try:
                # If not find (new duration)'s timecode elem, raise Exception
                if self.is_not_exist(L.audio_editing.smart_fit.new_duration_timecode):
                    raise Exception

                elem = self.find(L.audio_editing.smart_fit.new_duration_timecode, timeout=5)
                w, h = elem.AXSize
                x, y = elem.AXPosition

                pos_click = tuple(map(int, (x + w * 0.1, y + h * 0.5)))
                self.mouse.click(*pos_click)

                time.sleep(1)
                self.keyboard.send(timecode.replace("_", ""))
                self.keyboard.enter()
                time.sleep(DELAY_TIME)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        def get_current_timecode(self):
            try:
                # Check if enter (Smart Fit) or not
                if self.is_not_exist(L.audio_editing.smart_fit.main_window):
                    raise Exception

                # If not find timecode elem, raise Exception
                if self.is_not_exist(L.audio_editing.smart_fit.timecode):
                    raise Exception

                timecode = self.exist(L.audio_editing.smart_fit.timecode).AXValue
                return timecode
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        def click_custom_option(self):
            try:
                # Check if enter (Smart Fit) or not
                if self.is_not_exist(L.audio_editing.smart_fit.main_window):
                    raise Exception

                # If not find (custom duration option) elem, raise Exception
                if self.is_not_exist(L.audio_editing.smart_fit.radio_custom_duration):
                    raise Exception

                self.click(L.audio_editing.smart_fit.radio_custom_duration)
                return True
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        def click_org_option(self):
            try:
                # Check if enter (Smart Fit) or not
                if self.is_not_exist(L.audio_editing.smart_fit.main_window):
                    raise Exception

                # If not find (original duration option) elem, raise Exception
                if self.is_not_exist(L.audio_editing.smart_fit.radio_org_duration):
                    raise Exception

                self.click(L.audio_editing.smart_fit.radio_org_duration)
                return True
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        def get_custom_option_value(self):
            try:
                # Check if enter (Smart Fit) or not
                if self.is_not_exist(L.audio_editing.smart_fit.main_window):
                    raise Exception

                # If not find (custom duration option) elem, raise Exception
                if self.is_not_exist(L.audio_editing.smart_fit.radio_custom_duration):
                    raise Exception

                current_value = self.exist(L.audio_editing.smart_fit.radio_custom_duration).AXValue
                return current_value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        def click_ok(self):
            try:
                # Check if enter (Smart Fit) or not
                if self.is_not_exist(L.audio_editing.smart_fit.main_window):
                    raise Exception

                # If not find [OK] button, raise Exception
                if self.is_not_exist(L.audio_editing.smart_fit.btn_ok):
                    raise Exception

                self.click(L.audio_editing.smart_fit.btn_ok)
                time.sleep(DELAY_TIME*10)

                # Verify Step:
                if self.is_exist(L.audio_editing.smart_fit.main_window):
                    close_status = False
                else:
                    close_status = True
                return close_status

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

    class Audio_Editor(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def switch_single_channel(self, single_mode='yes'):
            # single_mode = yes, click [Edit Single Channel]
            # single_mode = no, click [Edit Multiple Channel]
            try:
                if single_mode == 'yes':
                    self.click(L.audio_editing.editor_window.btn_single_channel)
                elif single_mode == 'no':
                    self.click(L.audio_editing.editor_window.btn_multiple_channel)
                else:
                    logger('Error input parameter')
                    return False
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def open_special_effect_phone(self):
            try:
                # Check if enter (Audio Editor) or not
                if self.is_not_exist(L.audio_editing.editor_window.main_window):
                    raise Exception
                self.click(L.audio_editing.editor_window.btn_effect_phone)
                time.sleep(3)

                # Verify Step: Could find (Effect:Phone) window
                if self.is_not_exist(L.audio_editing.editor_window.effect_phone.main_window):
                    return False
                else:
                    return True
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        def apply_phone_effect(self):
            try:
                # Can find [Apply] button on Effect:Phone
                if self.is_not_exist(L.audio_editing.editor_window.effect_phone.btn_apply):
                    logger('Cannot find apply button, raise Exception')
                    raise Exception

                # Click [Apply]
                self.click(L.audio_editing.editor_window.effect_phone.btn_apply)
                time.sleep(3)

                # Verify Step: Could not find (Effect:Phone) window
                if self.is_exist(L.audio_editing.editor_window.effect_phone.main_window):
                    return False
                else:
                    return True
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        def get_current_timecode(self):
            try:
                # Check if enter (Audio Editor) or not
                if self.is_not_exist(L.audio_editing.editor_window.main_window):
                    raise Exception

                # If not find timecode elem, raise Exception
                if self.is_not_exist(L.audio_editing.editor_window.timecode):
                    raise Exception

                timecode = self.exist(L.audio_editing.editor_window.timecode).AXValue
                return timecode
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        def click_ok(self):
            try:
                # Check if enter (Audio Editor) or not
                if self.is_not_exist(L.audio_editing.editor_window.main_window):
                    raise Exception

                # If not find [OK] button, raise Exception
                if self.is_not_exist(L.audio_editing.editor_window.btn_ok):
                    raise Exception

                self.click(L.audio_editing.editor_window.btn_ok)
                time.sleep(DELAY_TIME)

                # Verify Step:
                if self.is_exist(L.audio_editing.editor_window.main_window):
                    return False
                else:
                    return True

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception