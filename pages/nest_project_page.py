import time, datetime, os, copy

from .base_page import BasePage
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
# from AppKit import NSScreen
from .locator import locator as L
from .main_page import Main_Page

DELAY_TIME = 1 # sec

class Nest_Project(Main_Page, BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def click_nest_project_main_tab(self):
        try:
            if not self.exist_click(L.nest_project.main_tab):
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_sub_project_tab(self, index=1):
        # index = 1 : 1st sub project tab
        # index = 2 : 2nd sub project tab
        # index = 3 : etc.
        try:
            if not self.exist_click({'AXIdentifier': 'NestedProjectCollectionViewItem', 'index': index}):
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def close_sub_project_tab(self, index=1):
        # index = 1 : 1st sub project tab
        # index = 2 : 2nd sub project tab
        # index = 3 : etc.
        try:
            if not self.exist({'AXIdentifier': 'NestedProjectCollectionViewItem', 'index': index}):
                raise Exception
            sub_tab = self.exist({'AXIdentifier': 'NestedProjectCollectionViewItem', 'index': index})
            if not self.exist_click(L.nest_project.btn_close_for_sub_tab, sub_tab):
                logger('Cannot find Close button')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def get_main_tab(self):
        try:
            if not self.exist(L.nest_project.main_tab):
                raise Exception
            main_tab_parent = self.exist(L.nest_project.main_tab)
            main_tab = self.exist({'AXRole': 'AXStaticText'}, main_tab_parent).AXValue
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return main_tab

    def hover_main_tab(self):
        try:
            if not self.exist(L.nest_project.main_tab):
                raise Exception
            x, y = self.exist(L.nest_project.main_tab).AXPosition
            self.mouse.move(x+5, y)
            time.sleep(DELAY_TIME*2)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def hover_sub_project_tab(self, index=1):
        # index = 1 : 1st sub project tab
        # index = 2 : 2nd sub project tab
        # index = 3 : etc.
        try:
            if not self.exist({'AXIdentifier': 'NestedProjectCollectionViewItem', 'index': index}):
                raise Exception
            x, y = self.exist({'AXIdentifier': 'NestedProjectCollectionViewItem', 'index': index}).AXPosition
            self.mouse.move(x+5, y)
            time.sleep(DELAY_TIME*2)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_btn_prev_scroll(self):
        try:
            if not self.exist_click(L.nest_project.btn_prev_scroll):
                raise Exception
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_btn_next_scroll(self):
        try:
            if not self.exist_click(L.nest_project.btn_next_scroll):
                raise Exception
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def get_timelineclip_reset_all_undock_window_status(self):
        try:
            if not self.exist(L.nest_project.menu_reset_all_undocked_windows):
                return None
            result = self.exist(L.nest_project.menu_reset_all_undocked_windows).AXEnabled
            self.right_click()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return result