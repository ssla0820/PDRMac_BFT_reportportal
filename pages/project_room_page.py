import time, datetime, os, copy

from .base_page import BasePage
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
# from AppKit import NSScreen
from .locator import locator as L
#from .locator.hardcode_0408 import locator as L
from .main_page import Main_Page
from reportportal_client import step

DELAY_TIME = 1 # sec


class Project_Room(Main_Page, BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.upload_project = self.upload_project(*args, **kwargs)
        #self.pack_project = self.pack_project(*args, **kwargs)
        #self.designer_upload_template = self.designer_upload_template(*args, **kwargs)

    @step('[Action][Project_Room] Enter [My Project]')
    def enter_project_room(self):
        #self.exist_click(L.project_room.button_project_room)
        try:
            if not self.exist(L.project_room.check_My_Project):
                logger("Not find My Project")
                raise Exception("Not find My Project")
            else:
                self.click(L.project_room.check_My_Project)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def check_in_Project_Room(self):
        try:
            if not self.exist(L.project_room.check_My_Project):
                logger("Not enter project room")
                raise Exception("Not enter project room")
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def import_pds_project(self, full_path):  # full_path: /Users/...
        try:
            if not self.exist(L.project_room.check_My_Project):
                logger("Not enter project room")
                raise Exception
            self.exist_click(L.project_room.button_import_project)
            time.sleep(2)
            self.select_file(full_path)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def import_pdk_project(self, full_path, extract_path):  # full_path: /Users/...
        try:
            if not self.exist(L.project_room.check_My_Project):
                logger("Not enter project room")
                raise Exception
            self.exist_click(L.project_room.button_import_project)
            self.select_file(full_path)
            self.select_file(extract_path)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def add_projectroom_new_tag(self, name):
        try:
            el_count_before = -1
            el_count_after = -1
            tag_elements = self.exist_elements(L.media_room.unit_tag_room_text_field)
            if not tag_elements:
                logger(f'Fail to find element.')
                raise Exception
            el_count_before = len(tag_elements)
            logger(f'{el_count_before=}')
            # click add new tag
            self.exist_click(L.media_room.btn_add_new_tag)
            self.exist(L.media_room.input_new_tag).sendKeys(name)
            self.keyboard.enter()
            # chek if confirm duplicated tag name dialog pops
            el_ok = self.exist(L.media_room.confirm_dialog.btn_ok)
            if el_ok:
                el_ok.press()
                logger('Warning: Duplicated tag name dialog pops up')
                return False
            # verify the last tag name
            # verify the tag count after add
            start_time = time.time()
            while time.time() - start_time < 3:  # timeout: 3 secs for waiting update tags
                tag_elements = self.exist_elements(L.media_room.unit_tag_room_text_field)
                if not tag_elements:
                    logger('Fail to verify element count after added.')
                    raise Exception
                el_count_after = len(tag_elements)
                if el_count_after > el_count_before:
                    break
            logger(f'{el_count_after=}')
            tag_name_new = tag_elements[-1].AXValue
            logger(f'{tag_name_new=}')
            if not tag_name_new == f'{name} (0)':
                logger(f'Fail to verify new tag name.')
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def delete_tag(self, name, count=0): # tag format: name (count)
        logger(f'delete_tag start - {name=}, {count=}')
        try:
            el_count_before = -1
            el_count_after = -1
            tag_elements = self.exist_elements(L.media_room.unit_tag_room_text_field)
            if not tag_elements:
                logger(f'Fail to find element.')
                raise Exception
            el_count_before = len(tag_elements)
            logger(f'{el_count_before=}')
            is_found = 0
            for el_tag in tag_elements:
                if el_tag.AXValue == f'{name} ({count})':
                    # mouse click the element
                    self.el_click(el_tag)
                    self.exist(L.media_room.btn_delete_tag).press()
                    # handle the confirm dialog
                    self.exist(L.media_room.confirm_dialog.btn_ok).press()
                    # time.sleep(1)
                    is_found = 1
            if is_found == 0:
                logger('Fail to find element #2.')
            # verify the tag count after deleted
            start_time = time.time()
            while time.time() - start_time < 3: # timeout: 3 secs for waiting update tags
                tag_elements = self.exist_elements(L.media_room.unit_tag_room_text_field)
                if not tag_elements:
                    logger('Fail to verify element count after deleted.')
                    raise Exception
                el_count_after = len(tag_elements)
                if el_count_after < el_count_before:
                    break
            logger(f'{el_count_after=}')
            if not el_count_before - el_count_after == 1:
                logger(f'Fail to verify tag count. diff. is {el_count_before - el_count_after}')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            return False
        return True

    def select_tag_RightClickMenu_DeleteTag(self, name, count=0): # tag format: name (count)
        logger(f'delete_tag start - {name=}, {count=}')
        try:
            el_count_before = -1
            el_count_after = -1
            tag_elements = self.exist_elements(L.media_room.unit_tag_room_text_field)
            if not tag_elements:
                logger(f'Fail to find element.')
                raise Exception
            el_count_before = len(tag_elements)
            logger(f'{el_count_before=}')
            is_found = 0
            for el_tag in tag_elements:
                if el_tag.AXValue == f'{name} ({count})':
                    # mouse click the element
                    self.mouse.move(*el_tag.center)
                    self.right_click()
                    self.select_right_click_menu('Delete Tag')
                    self.exist(L.media_room.btn_delete_tag).press()
                    # handle the confirm dialog
                    self.exist(L.media_room.confirm_dialog.btn_ok).press()
                    # time.sleep(1)
                    is_found = 1
            if is_found == 0:
                logger('Fail to find element #2.')
            # verify the tag count after deleted
            start_time = time.time()
            while time.time() - start_time < 3: # timeout: 3 secs for waiting update tags
                tag_elements = self.exist_elements(L.media_room.unit_tag_room_text_field)
                if not tag_elements:
                    logger('Fail to verify element count after deleted.')
                    raise Exception
                el_count_after = len(tag_elements)
                if el_count_after < el_count_before:
                    break
            logger(f'{el_count_after=}')
            if not el_count_before - el_count_after == 1:
                logger(f'Fail to verify tag count. diff. is {el_count_before - el_count_after}')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            return False
        return True

    def select_tag_RightClickMenu_RenameTag(self, name, name_new, count=0):
        try:
            el_count_after = -1
            tag_elements = self.exist_elements(L.media_room.unit_tag_room_text_field)
            if not tag_elements:
                logger(f'Fail to find element.')
                raise Exception
            el_count_before = len(tag_elements)
            logger(f'{el_count_before=}')
            is_found = 0
            for el_tag in tag_elements:
                if el_tag.AXValue == f'{name} ({count})':
                    # mouse click the element
                    self.mouse.move(*el_tag.center)
                    self.right_click()
                    self.select_right_click_menu('Rename Tag')
                    self.exist(L.media_room.input_new_tag).sendKeys(name_new)
                    self.keyboard.enter()
                    # chek if confirm duplicated tag name dialog pops
                    el_ok = self.exist(L.media_room.confirm_dialog.btn_ok)
                    if el_ok:
                        el_ok.press()
                        logger('Warning: Duplicated tag name dialog pops up')
                        return False
            # verify the last tag name
            # verify the tag count after add
            start_time = time.time()
            while time.time() - start_time < 3:  # timeout: 3 secs for waiting update tags
                tag_elements = self.exist_elements(L.media_room.unit_tag_room_text_field)
                if not tag_elements:
                    logger('Fail to verify element count after added.')
                    raise Exception
                el_count_after = len(tag_elements)
                if el_count_after > el_count_before:
                    break
            logger(f'{el_count_after=}')
            tag_name_new = tag_elements[-1].AXValue
            logger(f'{tag_name_new=}')
            if not tag_name_new == f'{name_new} ({count})':
                logger(f'Fail to verify new tag name.')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            return False
        return True

    def drag_project_into_certain_tag(self, strProject, strtag, count=0):
        try:
            x_project, y_project = self.exist({"AXIdentifier": "CollectionViewItemTextField", "AXValue": strProject}).AXParent.center
            tag_elements = self.exist_elements(L.media_room.unit_tag_room_text_field)
            if not tag_elements:
                logger(f'Fail to find element.')
                raise Exception
            for el_tag in tag_elements:
                if el_tag.AXValue == f'{strtag} ({count})':
                    self.mouse.drag((x_project, y_project), (el_tag.center))
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            return False
        return True

    def find_specific_tag(self, name):
        tags = self.exist(L.base.tag_list)
        for tag in tags:
            if tag.AXValue.startswith(f"{name} ("):
                return True
        return False

    def get_rightclickmenu_RenameTag_status(self):
        try:
            if not self.exist(L.pip_room.right_click_menu.rename_Tag):
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return self.exist(L.pip_room.right_click_menu.rename_Tag).AXEnabled

    def get_rightclickmenu_DeleteTag_status(self):
        try:
            if not self.exist(L.pip_room.right_click_menu.delete_Tag):
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return self.exist(L.pip_room.right_click_menu.delete_Tag).AXEnabled

    def get_DeleteSelectedTag_status(self):
        try:
            if not self.exist(L.pip_room.btn_delete_tag):
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return self.exist(L.pip_room.btn_delete_tag).AXEnabled

    def click_display_hide_explore_view(self):
        try:
            if not self.exist_click(L.pip_room.btn_explore_view):
                logger('Cannot find btn_explore_view')
                raise Exception
            time.sleep(DELAY_TIME)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def get_rightclickmenu_OpenFileLocation_status(self):
        try:
            from ATFramework.drivers.driver_factory import DriverFactory
            from pages.page_factory import PageFactory
            from types import SimpleNamespace
            from configs.app_config import Finder_cap
            app_finder = SimpleNamespace(**Finder_cap)
            self.activate()
            self.right_click()
            self.select_right_click_menu('Open File Location')
            img_collection_view_before = self.screenshot()
            # create finder window driver
            driver_finder = DriverFactory().get_mac_driver_object('mac', app_finder.app_name, app_finder.app_bundleID, app_finder.app_path)
            finder_main_page = PageFactory().get_page_object('main_page', driver_finder)
            if not finder_main_page.exist(L.base.finder_window.btn_close):
                logger('Fail to open finder window')
                raise Exception
            finder_main_page.exist_click(L.base.finder_window.btn_close)
            img_collection_view_after = self.screenshot()
            result_verify = self.compare(img_collection_view_before, img_collection_view_after)
            if result_verify:
                logger(f'Fail to close finder window')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def context_menu_dock_undock_library_window(self):
        try:
            self.activate()
            btn_import_media_position_before = self.exist(L.media_room.btn_import_media)
            self.right_click()
            self.select_right_click_menu('Dock/Undock Library Window')
            btn_import_media_position_after = self.exist(L.media_room.btn_import_media)
            if btn_import_media_position_after == btn_import_media_position_before:
                logger('Fail to dock/undock library window')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def context_menu_reset_all_undock_window(self):
        try:
            self.activate()
            btn_import_media_position_before = self.exist(L.media_room.btn_import_media)
            self.right_click()
            self.select_right_click_menu('Reset All Undocked Windows')
            btn_import_media_position_after = self.exist(L.media_room.btn_import_media)
            if btn_import_media_position_after == btn_import_media_position_before:
                logger('Fail to dock/undock library window')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def get_rightclickmenu_ResetAllUndock_status(self):
        try:
            self.activate()
            self.right_click()
            if not self.exist(L.project_room.reset_all_undock_windows):
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return self.exist(L.project_room.reset_all_undock_windows).AXEnabled

    @step('[Action][Project_Room] Insert Project to seleted track')
    def tips_area_insert_project_to_selected_track(self):
        try:
            self.exist_click(L.project_room.btn_add_to_track)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
