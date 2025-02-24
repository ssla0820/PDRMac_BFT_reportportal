import time, datetime, os, copy
import re

from .base_page import BasePage
from .main_page import Main_Page
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
# from AppKit import NSScreen
from .locator import locator as L
from reportportal_client import step

OPERATION_DELAY = 1 # sec

class Trim(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @step('[Verify][Trim Page] Check if enter [Trim] Window')
    def check_in_Trim(self):
        try:
            if not self.exist(L.trim.main_window):
                raise Exception("Not in Trim Window")
            if self.exist(L.trim.main_window).AXTitle.startswith('Trim |'):
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    def get_trim_title(self):
        try:
            if not self.exist(L.trim.main_window):
                logger("No trim window in current view")
                raise Exception
            title = self.exist(L.trim.main_window).AXTitle
            return title[7:]
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception

    def handle_effects_are_ignored(self, Option):
        '''
        :parameter
        Option = Yes, No
        '''
        try:
            if not self.exist(L.trim.alert_dialog.warning_msg):
                logger("Not found warning message")
                raise Exception
            item = eval(f'L.trim.alert_dialog.btn_{Option}')
            self.click(item)
            time.sleep(OPERATION_DELAY)

            # verify step:
            if self.exist(L.trim.alert_dialog.warning_msg):
                logger('Verify Fail')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True


