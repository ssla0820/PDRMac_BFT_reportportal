import time, datetime, os, copy

from .base_page import BasePage
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
from AppKit import NSScreen
from .locator import locator as L
from reportportal_client import step

DELAY_TIME = 1 # sec

class Crop_Image(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aspect_ratio = self.Aspect_Ratio(*args, **kwargs)
        self.crop_size = self.Crop_Size(*args, **kwargs)

    @step('[Action][Crop Image] Click [OK] button to leave [Crop Image] window')
    def click_ok(self):
        try:
            if not self.is_exist(L.crop_image.crop_window):
                logger('CANNOT find the crop image window')
                raise Exception('CANNOT find the crop image window')
            self.exist_click(L.crop_image.ok_button)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    class Aspect_Ratio(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        @step('[Action][Crop Image][Aspect Ratio] Set [Crop Aspect Ratio] to (4:3)')
        def set_4_3(self):
            self.exist_click(L.crop_image.aspect_ratio.aspect_ratio_btn)
            items = self.exist(L.crop_image.aspect_ratio.aspect_ratio_list)
            for item in items:
                if item.AXValue.strip() == '4:3':
                    self.mouse.click(*item.center)
                    return True
            return False

        def set_9_16(self):
            self.exist_click(L.crop_image.aspect_ratio.aspect_ratio_btn)
            items = self.exist(L.crop_image.aspect_ratio.aspect_ratio_list)
            for item in items:
                if item.AXValue.strip() == '9:16':
                    self.mouse.click(*item.center)
                    return True
            return False

        def set_1_1(self):
            self.exist_click(L.crop_image.aspect_ratio.aspect_ratio_btn)
            items = self.exist(L.crop_image.aspect_ratio.aspect_ratio_list)
            for item in items:
                if item.AXValue.strip() == '1:1':
                    self.mouse.click(*item.center)
                    return True
            return False

        def set_custom(self):
            self.exist_click(L.crop_image.aspect_ratio.aspect_ratio_btn)
            items = self.exist(L.crop_image.aspect_ratio.aspect_ratio_list)
            for item in items:
                if item.AXValue.strip() == 'Custom':
                    self.mouse.click(*item.center)
                    return True
            return False

        def click_width_arrow(self, option, times=1):
            try:
                if (option > 1) | (option < 0):
                    logger('Invalid parameter')
                    return False
                for x in range(times):
                    if option == 0:
                        self.exist_click(L.crop_image.aspect_ratio.arrow_up_btn_width)
                    elif option == 1:
                        self.exist_click(L.crop_image.aspect_ratio.arrow_down_btn_width)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def click_height_arrow(self, option, times=1):
            try:
                if (option > 1) | (option < 0):
                    logger('Invalid parameter')
                    return False
                for x in range(times):
                    if option == 0:
                        self.exist_click(L.crop_image.aspect_ratio.arrow_up_btn_height)
                    elif option == 1:
                        self.exist_click(L.crop_image.aspect_ratio.arrow_down_btn_height)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

    class Crop_Size(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def set_width_value(self, value):
            try:

                if not self.is_exist(L.crop_image.crop_window):
                    logger('CANNOT find the crop image window')
                    raise Exception
                self.click(L.crop_image.crop_size.text_field_width)
                self.mouse.click(times=2)

                self.exist(L.crop_image.crop_size.text_field_width).AXValue = str(value)
                self.press_enter_key()
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def set_height_value(self, value):
            try:

                if not self.is_exist(L.crop_image.crop_window):
                    logger('CANNOT find the crop image window')
                    raise Exception
                self.click(L.crop_image.crop_size.text_field_height)
                self.mouse.click(times=2)

                self.exist(L.crop_image.crop_size.text_field_height).AXValue = str(value)
                self.press_enter_key()
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True





































































