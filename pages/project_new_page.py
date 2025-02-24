import time, datetime, os, copy
# from PIL import Image
import platform

from .base_page import BasePage
from .main_page import Main_Page
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
from .locator import locator as L
from reportportal_client import step

OPERATION_DELAY = 1 # sec


def is_os_ver_greater_than_or_equal_to(os_ver): # os_ver: e.g. 10.15.7 or 10.15
    try:
        curr_os_ver = platform.mac_ver()[0]
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        return False
    return curr_os_ver >= os_ver


class Project_New(Main_Page, BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.save_file = File_Picker('Save File', *args, **kwargs)
        self.pack_project = File_Picker('Pack Project Materials', *args, **kwargs)
        self.open_project = File_Picker('Open Project', *args, **kwargs)

    @staticmethod
    def echo():
        print('project_new_page')

    def _menu_bar_select_click_menu(self, *arg, is_enable=1, return_elem=False):
        item = None
        depth = len(arg)
        curr_depth = 0
        for item_name in arg:
            item = self.find({"AXRole": "AXMenuItem", "AXTitle": item_name}, parent=item)
            if not item: return False  # in case no sub menu item (preference can set item to 0)
            if not item.AXEnabled:
                self.mouse.click()
                return False
            item_pos = item.AXPosition
            item_size = item.AXSize
            if curr_depth == depth - 1:
                if (is_enable == 1 and not item.AXMenuItemMarkChar) or (is_enable == 0 and item.AXMenuItemMarkChar):
                    self.mouse.click(int(item_pos[0] + 30), int(item_pos[1] + item_size[1] / 2))
                else:
                    time.sleep(OPERATION_DELAY * 0.5)
                    self.keyboard.esc()
            else:
                self.mouse.click(int(item_pos[0] + 30), int(item_pos[1] + item_size[1] / 2))
                curr_depth += 1
        return item if return_elem else True

    def tap_menu_bar_file_save_project(self):
        try:
            self.exist_click(L.main.top_menu_bar.btn_file)
            self._menu_bar_select_click_menu(L.main.top_menu_bar.option_save_project)
            # verify if save file dialog pops up
            if not self.is_exist(L.main.save_file_dialog.main_window, None, OPERATION_DELAY * 5):
                logger('Fail to verify save project dialog pops up')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def tap_menu_bar_file_pack_project_materials(self):
        try:
            self.exist_click(L.main.top_menu_bar.btn_file)
            self._menu_bar_select_click_menu(L.main.top_menu_bar.option_pack_project_materials)
            # verify if save file dialog pops up
            if not self.is_exist(L.base.file_picker.main, None, OPERATION_DELAY * 5):
                logger('Fail to verify pack project materials dialog pops up')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def tap_menu_bar_file_open_project(self):
        try:
            self.exist_click(L.main.top_menu_bar.btn_file)
            self._menu_bar_select_click_menu(L.main.top_menu_bar.option_open_project)
            time.sleep(OPERATION_DELAY * 2)
            self.exist_click(L.base.quit_dialog.no, None, 'left', 3)
            # verify if save file dialog pops up
            if not self.is_exist(L.base.file_picker.main, None, OPERATION_DELAY * 5):
                logger('Fail to verify open project dialog pops up')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def open_pds_project(self, file_path):
        try:
            self.tap_menu_bar_file_open_project()
            time.sleep(OPERATION_DELAY * 0.5)
            self.handle_open_project_dialog(os.path.abspath(file_path))
            self.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='no')
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def open_pdk_project(self, file_path, uncompress_folder_path):
        try:
            self.tap_menu_bar_file_open_project()
            time.sleep(OPERATION_DELAY * 0.5)
            self.handle_open_project_dialog(os.path.abspath(file_path), uncompress_folder_path)
            self.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='no')
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def menu_bar_file_pack_project_materials(self, project_name, folder_path):
        try:
            self.tap_menu_bar_file_pack_project_materials()
            time.sleep(OPERATION_DELAY)
            self.save_file.handle_save_file(project_name, folder_path)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True


class File_Picker(BasePage):
    def __init__(self, dialog_name='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog_name = dialog_name
        self.locator_file_name = L.base.file_picker.file_name.copy()
        self.locator_tag_editbox = L.base.file_picker.tags_editbox.copy()
        self.locator_tag_item = L.base.file_picker.tag_item.copy()
        if is_os_ver_greater_than_or_equal_to('10.16'):
            self.locator_file_name = L.base.file_picker.file_name_big_sur.copy()
        self.new_folder = New_Folder(*args, **kwargs)
        self.merge_project_media_library = Confirm_Dialog(*args, **kwargs)
        self.file_missing = File_Missing_Dialog(*args, **kwargs)

    def clear_save_as(self):
        try:
            locator_filename = [L.base.file_picker.main, self.locator_file_name]
            #self.exist(locator_filename).AXValue = ''
            self.double_click(locator_filename)
            self.press_backspace_key()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def set_project_name(self, name, folder_path=''):
        try:
            self.exist(self.locator_file_name).AXValue = name
            time.sleep(OPERATION_DELAY)
            if folder_path:
                self.select_folder(folder_path, 'no_click')
                time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def handle_save_file(self, name, folder_path):
        try:
            self.select_file(os.path.abspath(f'{folder_path}/{name}'), 'Save')
            # handle if file already exists
            btn_replace = self.exist(L.main.save_file_dialog.btn_replace, OPERATION_DELAY * 3)
            if btn_replace:
                self.el_click(btn_replace)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_project(self, name, folder_path):
        return self.select_folder(os.path.abspath(f'{folder_path}/{name}'), 'no_click')

    def check_default_tags(self):
        try:
            locator_tag_item = self.locator_tag_item.copy()
            result = self.is_not_exist(locator_tag_item, None, 2)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            return False
        return result

    def set_tags_by_input_string(self, tag_name):
        try:
            self.click(self.locator_tag_editbox)
            time.sleep(OPERATION_DELAY)
            self.keyboard.send(tag_name)
            time.sleep(OPERATION_DELAY * 0.5)
            self.keyboard.enter()
            time.sleep(OPERATION_DELAY * 0.5)
            self.click(self.locator_file_name)
            time.sleep(OPERATION_DELAY * 0.5)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            return False
        return True

    def set_tags_by_press_space_key(self):
        try:
            self.click(self.locator_tag_editbox)
            time.sleep(OPERATION_DELAY)
            self.press_space_key()
            time.sleep(OPERATION_DELAY * 0.5)
            if self.exist(self.locator_tag_editbox).AXValue != ' ':
                logger('Fail to get the space character')
                return False
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            return False
        return True

    def _set_tags(self, value, is_click_save_as=True, is_click_tag_editbox=True):
        try:
            if is_click_tag_editbox:
                self.click(self.locator_tag_editbox)
                time.sleep(OPERATION_DELAY)
            option_tag = L.base.file_picker.unit_menu_option_tag.copy()
            option_tag[1]['AXValue'] = value
            self.click(option_tag)
            time.sleep(OPERATION_DELAY * 0.5)
            if is_click_save_as:
                self.click(self.locator_file_name)
                time.sleep(OPERATION_DELAY * 0.5)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def set_tag_to_red(self):
        return self._set_tags('Red')

    def set_tag_to_orange(self):
        return self._set_tags('Orange')

    def set_tag_to_yellow(self):
        return self._set_tags('Yellow')

    def set_tag_to_green(self):
        return self._set_tags('Green')

    def set_tag_to_blue(self):
        return self._set_tags('Blue')

    def set_tag_to_purple(self):
        return self._set_tags('Purple')

    def set_tag_to_gray(self):
        return self._set_tags('Gray')

    def click_tags_show_all(self):
        return self._set_tags('Show All…', False)

    def set_tag_to_work(self):
        try:
            self._set_tags('Show All…', False)
            self._set_tags('Work', True, False)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def unfold_window(self):
        return self.click(L.base.file_picker.show_more_options)

    def set_path(self, full_path):
        return self.select_folder(full_path, 'no_click')

    def click_previous_folder(self):
        try:
            el_button = self.exist(L.base.file_picker.btn_back)
            if not el_button.AXEnabled:
                logger('button is disabled.')
                return False
            self.el_click(el_button)
            time.sleep(OPERATION_DELAY * 0.5)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_next_folder(self):
        try:
            el_button = self.exist(L.base.file_picker.btn_forward)
            if not el_button.AXEnabled:
                logger('button is disabled.')
                return False
            self.el_click(el_button)
            time.sleep(OPERATION_DELAY * 0.5)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_grouping_menu_item(self, item_name, set_checked=True):
        try:
            time.sleep(1)
            logger('307')
            self.click(L.base.file_picker.btn_change_item_grouping)
            logger('309')
            time.sleep(OPERATION_DELAY)
            menu_item = {'AXRole': 'AXMenuItem', 'AXTitle': item_name}
            logger('312')
            el_menu_item = self.exist(menu_item)
            if (not el_menu_item.AXMenuItemMarkChar and set_checked) or \
                    (el_menu_item.AXMenuItemMarkChar and set_checked is False):
                self.click(menu_item)
                time.sleep(OPERATION_DELAY * 0.5)
            else:
                self.click(L.base.file_picker.btn_change_item_grouping)
                time.sleep(OPERATION_DELAY * 0.5)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_grouping_show_sidebar(self, is_enable=True):
        return self.click_grouping_menu_item('Show Sidebar', is_enable)

    def click_grouping_show_item_as_icons(self):
        return self.click_grouping_menu_item('Icons')

    def click_grouping_show_item_as_list(self):
        return self.click_grouping_menu_item('List')

    def click_grouping_show_item_as_columns(self):
        return self.click_grouping_menu_item('Columns')

    def click_grouping_item_by_size(self):
        return self.click_grouping_menu_item('Size')

    def click_grouping_item_by_tags(self):
        return self.click_grouping_menu_item('Tags')

    def click_top_new_folder(self):
        return self.click(L.base.file_picker.btn_top_new_folder)

    def click_bottom_new_folder(self):
        return self.click(L.base.file_picker.btn_bottom_new_folder)

    def click_cancel(self):
        return self.click(L.base.file_picker.btn_cancel)

    def click_save(self):
        try:
            self.click(L.base.file_picker.btn_save)
            time.sleep(OPERATION_DELAY)
            self.exist_click(L.base.file_picker.btn_replace_exist_file, None, 'left', 2)
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_sidebar_all_tags(self, scroll_times=3):
        try:
            pos_sidebar = self.exist(L.base.file_picker.sidebar).AXPosition
            size_sidebar = self.exist(L.base.file_picker.sidebar).AXSize
            self.mouse.move(pos_sidebar[0]+int(size_sidebar[0]/2), pos_sidebar[1]+int(size_sidebar[1]/2))
            time.sleep(OPERATION_DELAY)
            self.mouse.scroll('down', scroll_times)
            time.sleep(OPERATION_DELAY)
            locator_all_tags = L.base.file_picker.unit_sidebar_item.copy()
            locator_all_tags[1]['AXValue'] = 'All Tags…'
            self.click(locator_all_tags)
            time.sleep(OPERATION_DELAY * 0.5)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_open(self):
        return self.click(L.base.file_picker.btn_open)

    def check_file_missing_dialog(self):
        return self.is_exist(L.main.cyberlink_powerdirector_dialog.description_open_project_file_missing, None, 3)


class New_Folder(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def check_default_folder_name(self):
        try:
            name = self.exist(L.base.file_picker.new_folder.editbox_folder_name).AXValue
            result = True
            if name != 'untitled folder':
                result = False
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return result

    def set_name(self, name):
        try:
            self.exist(L.base.file_picker.new_folder.editbox_folder_name).AXValue = name
            time.sleep(OPERATION_DELAY * 0.5)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_cancel(self):
        return self.click(L.base.file_picker.new_folder.btn_cancel)

    def click_create(self):
        try:
            el_button = self.exist(L.base.file_picker.new_folder.btn_create)
            if not el_button.AXEnabled:
                logger('button is disabled')
                return False
            self.el_click(el_button)
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True


class Confirm_Dialog(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def click_yes(self):
        return self.click(L.base.confirm_dialog.btn_yes)

    def click_no(self):
        return self.click(L.base.confirm_dialog.btn_no)


class File_Missing_Dialog(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @step('[Action][Project_New][File Missing Dialog] Click [Browse] button')
    def click_browse(self):
        result = self.click(L.main.cyberlink_powerdirector_dialog.btn_browse)
        time.sleep(OPERATION_DELAY)
        return result

    def select_file(self, file_path): # to select the missing file after click browse button
        return self.select_folder(file_path)

    def click_ignore(self):
        return self.click(L.main.cyberlink_powerdirector_dialog.btn_ignore)

    def click_ignore_all(self):
        return self.click(L.main.cyberlink_powerdirector_dialog.btn_ignore_all)