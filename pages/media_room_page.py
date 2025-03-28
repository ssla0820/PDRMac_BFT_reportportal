import time, datetime, os, copy
import re

from .base_page import BasePage
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
# from AppKit import NSScreen
from .locator import locator as L
from reportportal_client import step

OPERATION_DELAY = 1 # sec

class Media_Room(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.svrt_info = SVRT_Info(*args, **kwargs)

    @step('[Action][Media Room] Import media for local file')
    def import_media_file(self, full_path): # full_path: /Users/...
        try:
            self.exist_click(L.media_room.btn_import_media)
            self.exist_click(L.media_room.import_media.option_import_media_file)
            self.select_file(full_path)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def import_media_folder(self, full_path): # full_path: /Users/...
        try:
            self.exist_click(L.media_room.btn_import_media)
            self.exist_click(L.media_room.import_media.option_import_media_folder)
            self.select_file(full_path)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Media Room] Import media from [CyberLink Cloud]')
    def import_media_from_cyberlink_cloud(self):
        try:
            self.exist_click(L.media_room.btn_import_media)
            self.exist_click(L.media_room.import_media.option_download_media_from_cyberlink_cloud)
            # verify if download media dialog pops up
            if not self.exist(L.media_room.download_media_dialog.btn_close, None, 3):
                logger('Fail to open download media window')
                raise Exception('Fail to open download media window')
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Media Room] Open [Shutterstock] dialog in media room')
    def import_media_from_shutterstock(self):
        try:
            self.exist_click(L.media_room.btn_import_media)
            self.exist_click(L.media_room.import_media.option_download_media_from_shutterstock)
            # verify if shutter stock dialog pops up
            if not self.exist(L.media_room.download_media_from_shutterstock_dialog.btn_close, None, 3):
                logger('Fail to open download media window')
                raise Exception('Fail to open download media window')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Media Room] Enter [Media Content] Category')
    def enter_media_content(self):
        try:
            self.exist_click(L.media_room.tag_media_content)
            if not self.exist(L.media_room.btn_import_media):
                logger('Fail to enter media content')
                raise Exception('Fail to enter media content')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Media Room] Enter [Color Boards]')
    def enter_color_boards(self):
        try:
            self.exist_click(L.media_room.tag_color_boards)
            if not self.exist(L.media_room.btn_create_new_color_board):
                logger('Fail to enter color boards')
                raise Exception('Fail to enter color boards')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    # BGM (From CL source)
    @step('[Action][Media Room] Enter [Background Music (CL)] Category')
    def enter_background_music_CL(self):
        try:
            self.exist_click(L.media_room.tag_background_music_CL)
            if not self.exist(L.media_room.scroll_area.list_icon_music):
                logger('Fail to enter background music')
                raise Exception('Fail to enter background music')
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    # BGM (Meta)
    @step('[Action][Media Room] Enter [Background Music (meta)] Category')
    def enter_background_music(self):
        try:
            self.exist_click(L.media_room.tag_background_music)
            if not self.exist(L.media_room.scroll_area.list_icon_music):
                logger('Fail to enter background music')
                raise Exception('Fail to enter background music')
            time.sleep(OPERATION_DELAY*2)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    # BGM (Soundstripe)
    def enter_background_soundstripe(self):
        try:
            self.exist_click(L.media_room.tag_background_music_soundstripe)
            if not self.exist(L.media_room.scroll_area.list_icon_music):
                logger('Fail to enter background music')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Media Room] Enter [Sound Clip] Category')
    def enter_sound_clips(self):
        try:
            self.exist_click(L.media_room.tag_sound_clips)
            time.sleep(OPERATION_DELAY * 4)
            if not self.exist(L.media_room.scroll_area.list_icon_music):
                logger('Fail to enter sound clips')
                raise Exception('Fail to enter sound clips')
            time.sleep(OPERATION_DELAY * 6)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Media Room] Enter [Download] Category')
    def enter_downloaded(self):
        try:
            time.sleep(OPERATION_DELAY)
            old_img = self.snapshot(L.media_room.tag_downloaded)

            self.exist_click(L.media_room.tag_downloaded)
            #if not self.wait_for_image_changes(old_img, locator=L.media_room.tag_downloaded, similarity=1):
            #    logger('Fail to enter downloaded, category highlight is not change')
            #    raise Exception
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_use_sample_media(self):
        try:
            # click [Use sample media]
            if self.is_exist(L.media_room.string_use_sample_media, timeout=7):
                self.click(L.media_room.string_use_sample_media)
                time.sleep(OPERATION_DELAY * 4)
            else:
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def media_filter_display_all(self):
        try:
            img_collection_view_before = self.snapshot(L.media_room.library_listview.main_frame)
            self.exist_click(L.media_room.btn_media_filter_all)
            time.sleep(OPERATION_DELAY)
            img_collection_view_after = self.snapshot(L.media_room.library_listview.main_frame)
            # verify is collection view frame is changed by snapshot
            print(f'{img_collection_view_before=}, {img_collection_view_after=}')
            result_verify = self.compare(img_collection_view_before, img_collection_view_after)
            '''
            if result_verify:
                logger('Fail to verify after clicked select all')
                raise Exception
            '''
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def media_filter_display_video_only(self):
        try:
            img_collection_view_before = self.snapshot(L.media_room.library_listview.main_frame)
            self.exist_click(L.media_room.btn_media_filter_display_video_only)
            time.sleep(OPERATION_DELAY)
            img_collection_view_after = self.snapshot(L.media_room.library_listview.main_frame)
            # verify is collection view frame is changed by snapshot
            result_verify = self.compare(img_collection_view_before, img_collection_view_after)
            '''
            if result_verify:
                logger('Fail to verify after clicked select all')
                raise Exception
            '''
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def media_filter_display_image_only(self):
        try:
            img_collection_view_before = self.snapshot(L.media_room.library_listview.main_frame)
            self.exist_click(L.media_room.btn_media_filter_display_image_only)
            time.sleep(OPERATION_DELAY)
            img_collection_view_after = self.snapshot(L.media_room.library_listview.main_frame)
            # verify is collection view frame is changed by snapshot
            result_verify = self.compare(img_collection_view_before, img_collection_view_after)
            if result_verify:
                logger('Fail to verify after clicked select all')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def media_filter_display_audio_only(self):
        try:
            img_collection_view_before = self.snapshot(L.media_room.library_listview.main_frame)
            self.exist_click(L.media_room.btn_media_filter_display_audio_only)
            time.sleep(OPERATION_DELAY)
            img_collection_view_after = self.snapshot(L.media_room.library_listview.main_frame)
            # verify is collection view frame is changed by snapshot
            result_verify = self.compare(img_collection_view_before, img_collection_view_after)
            if result_verify:
                logger('Fail to verify after clicked select all')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Media Room] Search library for (content name)')
    def search_library(self, name, intro_room=False):
        try:
            img_collection_view_before = self.snapshot(L.media_room.library_listview.main_frame)
            self.exist_click(L.media_room.input_search)
            self.keyboard.send(name)
            time.sleep(OPERATION_DELAY)
            self.press_enter_key()
            time.sleep(OPERATION_DELAY)
            if intro_room:
                # If enter intro room to search, should add more sec. to delay / wait for search result
                time.sleep(OPERATION_DELAY * 5)
            img_collection_view_after = self.snapshot(L.media_room.library_listview.main_frame)
            # verify is collection view frame is changed by snapshot
            result_verify = self.compare(img_collection_view_before, img_collection_view_after)
            if result_verify:
                logger('Fail to verify after clicked select all')
                raise Exception('Fail to verify after clicked select all')
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
    
    @step('[Action][Media Room] Search conponent in Media Room (Sound Effects) category')
    def search_SFX_library(self, name):
        # This function is only for Media Room (Sound Effects) category
        try:
            img_collection_view_before = self.snapshot(L.media_room.library_listview.table_view)
            self.exist_click(L.media_room.input_search)
            self.keyboard.send(name)
            self.press_enter_key()
            time.sleep(OPERATION_DELAY)
            img_collection_view_after = self.snapshot(L.media_room.library_listview.table_view)
            # verify is collection view frame is changed by snapshot
            result_verify = self.compare(img_collection_view_before, img_collection_view_after)
            if result_verify:
                logger('Fail to verify after clicked select all')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Media Room] Click [Cancel] button in search library')
    def search_library_click_cancel(self):
        try:
            self.exist_click(L.media_room.btn_search_cancel)
            time.sleep(OPERATION_DELAY)
            self.mouse.click() # Fix the v20.3.3630 bug (Note: v20.4.3918 is fine)
            if self.exist(L.media_room.btn_search_cancel, parent=None, timeout=3):
                logger('Fail to click search cancel button')
                raise Exception('Fail to click search cancel button')
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Media Room] Click [Display/Hide Explore View] button')
    def click_display_hide_explore_view(self):
        try:
            main_frame_size_before = self.exist(L.media_room.library_listview.main_frame).AXSize
            self.exist_click(L.media_room.library_listview.btn_display_hide_explore_view)
            # verify the collection view width change
            time.sleep(OPERATION_DELAY)
            main_frame_size_after = self.exist(L.media_room.library_listview.main_frame).AXSize
            if main_frame_size_after[0] == main_frame_size_before[0]:
                logger('Fail to click display/hide explore view button')
                raise Exception('Fail to click display/hide explore view button')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Media Room] Add new tag with name')
    def add_new_tag(self, name):
        try:
            el_count_before = -1
            el_count_after = -1
            tag_elements = self.exist_elements(L.media_room.unit_tag_room_text_field)
            if not tag_elements:
                logger(f'Fail to find element.')
                raise Exception(f'Fail to find element.')
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
                    raise Exception('Fail to verify element count after added.')
                el_count_after = len(tag_elements)
                if el_count_after > el_count_before:
                    break
            logger(f'{el_count_after=}')
            tag_name_new = tag_elements[-1].AXValue
            logger(f'{tag_name_new=}')
            if not tag_name_new == f'{name} (0)':
                logger(f'Fail to verify new tag name.')
                raise Exception(f'Fail to verify new tag name.')
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
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

    @step('[Action][Media Room] Delete tag by right click')
    def right_click_delete_tag(self, name, count=0): # tag format: name (count)
        logger(f'delete_tag start - {name=}, {count=}')
        try:
            el_count_before = -1
            el_count_after = -1
            tag_elements = self.exist_elements(L.media_room.unit_tag_room_text_field)
            if not tag_elements:
                logger(f'Fail to find element.')
                raise Exception(f'Fail to find element.')
            el_count_before = len(tag_elements)
            logger(f'{el_count_before=}')
            is_found = 0
            for el_tag in tag_elements:
                if el_tag.AXValue == f'{name} ({count})':
                    # mouse click the element
                    self.mouse.move(*el_tag.center)
                    time.sleep(OPERATION_DELAY)
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
                    raise Exception('Fail to verify element count after deleted.')
                el_count_after = len(tag_elements)
                if el_count_after < el_count_before:
                    break
            logger(f'{el_count_after=}')
            if not el_count_before - el_count_after == 1:
                logger(f'Fail to verify tag count. diff. is {el_count_before - el_count_after}')
                raise Exception(f'Fail to verify tag count. diff. is {el_count_before - el_count_after}')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Media Room] Rename tag by right click')
    def right_click_rename_tag(self, name, name_new, count=0):
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
                    time.sleep(OPERATION_DELAY)
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
                    raise Exception('Fail to verify element count after added.')
                el_count_after = len(tag_elements)
                if el_count_after > el_count_before:
                    break
            logger(f'{el_count_after=}')
            tag_name_new = tag_elements[-1].AXValue
            logger(f'{tag_name_new=}')
            if not tag_name_new == f'{name_new} ({count})':
                logger(f'Fail to verify new tag name.')
                raise Exception(f'Fail to verify new tag name.')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def tag_get_media_amount(self, tag_name):
        try:
            result = []
            pattern = '\((\d+)\)'
            tag_elements = self.exist_elements(L.media_room.unit_tag_room_text_field)
            for el_tag in tag_elements:
                if f'{tag_name} (' in el_tag.AXValue:
                    result = re.findall(pattern, el_tag.AXValue)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return int(result[0])

    def library_menu_sort_by(self, locator=None):
        try:
            self.exist_click(L.media_room.library_menu.btn_menu)
            self.exist_click(L.media_room.library_menu.option_sort_by)
            if locator:
                self.exist_click(locator)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_menu_display_as(self, locator=None):
        try:
            self.exist(L.media_room.library_menu.btn_menu).press()
            self.exist(L.media_room.library_menu.option_display_as).press()
            if locator:
                self.exist(locator).press()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Media Room] Sort by [Name] in [Library Menu]')
    def library_menu_sort_by_name(self):
        try:
            self.library_menu_sort_by(L.media_room.library_menu.option_sort_by_name)
            # verify if option is marked
            self.library_menu_sort_by()
            if self.exist(L.media_room.library_menu.option_sort_by_name).AXMenuItemMarkChar == '':
                logger('Fail to verify option mark')
                raise Exception('Fail to verify option mark')
            self.keyboard.esc()
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def library_menu_sort_by_duration(self):
        try:
            self.library_menu_sort_by(L.media_room.library_menu.option_sort_by_duration)
            # verify if option is marked
            self.library_menu_sort_by()
            if self.exist(L.media_room.library_menu.option_sort_by_duration).AXMenuItemMarkChar == '':
                logger('Fail to verify option mark')
                raise Exception
            self.keyboard.esc()
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True


    def library_menu_sort_by_file_size(self):
        try:
            self.library_menu_sort_by(L.media_room.library_menu.option_sort_by_file_size)
            # verify if option is marked
            self.library_menu_sort_by()
            if self.exist(L.media_room.library_menu.option_sort_by_file_size).AXMenuItemMarkChar == '':
                logger('Fail to verify option mark')
                raise Exception
            self.keyboard.esc()
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Media Room] Sort by [Created Date] in [Library Menu]')
    def library_menu_sort_by_created_date(self):
        try:
            self.library_menu_sort_by(L.media_room.library_menu.option_sort_by_created_date)
            # verify if option is marked
            self.library_menu_sort_by()
            if self.exist(L.media_room.library_menu.option_sort_by_created_date).AXMenuItemMarkChar == '':
                logger('Fail to verify option mark')
                raise Exception('Fail to verify option mark')
            self.keyboard.esc()
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def library_menu_sort_by_modified_date(self):
        try:
            self.library_menu_sort_by(L.media_room.library_menu.option_sort_by_modified_date)
            # verify if option is marked
            self.library_menu_sort_by()
            if self.exist(L.media_room.library_menu.option_sort_by_modified_date).AXMenuItemMarkChar == '':
                logger('Fail to verify option mark')
                raise Exception
            self.keyboard.esc()
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_menu_sort_by_type(self):
        try:
            self.library_menu_sort_by(L.media_room.library_menu.option_sort_by_type)
            # verify if option is marked
            self.library_menu_sort_by()
            if self.exist(L.media_room.library_menu.option_sort_by_type).AXMenuItemMarkChar == '':
                logger('Fail to verify option mark')
                raise Exception
            self.keyboard.esc()
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_menu_select_all(self):
        try:
            self.exist(L.media_room.library_menu.btn_menu).press()
            self.exist(L.media_room.library_menu.option_select_all).press()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_menu_extra_large_icons(self):
        try:
            self.exist(L.media_room.library_menu.btn_menu).press()
            self.exist(L.media_room.library_menu.option_extra_large_icons).press()
            time.sleep(OPERATION_DELAY)
            # verify if option is marked
            self.exist(L.media_room.library_menu.btn_menu).press()
            if self.exist(L.media_room.library_menu.option_extra_large_icons).AXMenuItemMarkChar == '':
                logger('Fail to verify option mark')
                raise Exception
            self.keyboard.esc()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_menu_large_icons(self):
        try:
            self.exist(L.media_room.library_menu.btn_menu).press()
            self.exist(L.media_room.library_menu.option_large_icons).press()
            time.sleep(OPERATION_DELAY)
            # verify if option is marked
            self.exist(L.media_room.library_menu.btn_menu).press()
            if self.exist(L.media_room.library_menu.option_large_icons).AXMenuItemMarkChar == '':
                logger('Fail to verify option mark')
                raise Exception
            self.keyboard.esc()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_menu_medium_icons(self):
        try:
            self.exist(L.media_room.library_menu.btn_menu).press()
            self.exist(L.media_room.library_menu.option_medium_icons).press()
            time.sleep(OPERATION_DELAY)
            # verify if option is marked
            self.exist(L.media_room.library_menu.btn_menu).press()
            if self.exist(L.media_room.library_menu.option_medium_icons).AXMenuItemMarkChar == '':
                logger('Fail to verify option mark')
                raise Exception
            self.keyboard.esc()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_menu_small_icons(self):
        try:
            self.exist(L.media_room.library_menu.btn_menu).press()
            self.exist(L.media_room.library_menu.option_small_icons).press()
            time.sleep(OPERATION_DELAY)
            # verify if option is marked
            self.exist(L.media_room.library_menu.btn_menu).press()
            if self.exist(L.media_room.library_menu.option_small_icons).AXMenuItemMarkChar == '':
                logger('Fail to verify option mark')
                raise Exception
            self.keyboard.esc()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_menu_empty_the_library(self):
        try:
            self.exist(L.media_room.library_menu.btn_menu).press()
            self.exist(L.media_room.library_menu.option_empty_the_library).press()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_menu_remove_all_unused_content_from_library(self):
        try:
            self.exist(L.media_room.library_menu.btn_menu).press()
            self.exist(L.media_room.library_menu.option_remove_all_unused_content_from_library).press()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    # color board ===================
    @step('[Action][Media Room] Modify [Color Board] Color')
    def library_menu_new_color_board(self, hex_color): # e.g. hex_color: FFFEEE
        try:
            self.exist(L.media_room.btn_create_new_color_board).press()
            self.exist(L.media_room.library_menu.option_new_color_board).press()
            self.color_board_switch_category_to_RGB()
            time.sleep(2)
            color_field = self.exist(L.media_room.colors.input_hex_color)
            self.mouse.click(*color_field.center)
            self.double_click()
            self.press_space_key()
            self.input_text(hex_color)
            time.sleep(1)
            self.keyboard.enter()
            self.exist(L.media_room.colors.btn_close).press()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Media Room] Set [Gradient Color]')
    def library_menu_new_gradient_color(self, hex_color): # e.g. hex_color: FFFEEE
        try:
            self.exist(L.media_room.btn_create_new_color_board).press()
            self.exist(L.media_room.library_menu.option_new_gradient_color).press()
            time.sleep(OPERATION_DELAY*2)

            # --- Handle Create Color Gradient ---
            self.handle_color_gradient(hex_color)

            # Handle (Save as Template)
            # Need to call follow page function
            # title_designer_page.click_custom_name_ok('custom_purple')
            time.sleep(OPERATION_DELAY)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Media Room] Handle Color Gradient')
    def handle_color_gradient(self, hex_color):
        # --- Handle Create Color Gradient ---
        self.exist(L.base.create_color_gradient.input_hex_color).press()
        time.sleep(OPERATION_DELAY)

        # --- Handle Colors window ---
        self.color_board_switch_category_to_RGB()
        time.sleep(2)
        color_field = self.exist(L.media_room.colors.input_hex_color)
        self.mouse.click(*color_field.center)
        self.double_click()
        self.press_space_key()
        self.input_text(hex_color)
        time.sleep(1)
        self.keyboard.enter()
        self.exist(L.media_room.colors.btn_close).press()

        # back to Create Color Gradient
        time.sleep(3)
        self.click(L.base.create_color_gradient.btn_ok)

    def library_menu_restore_to_defaults(self):
        try:
            self.exist(L.media_room.library_menu.btn_menu).press()
            self.exist(L.media_room.library_menu.option_restore_to_defaults).press()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_menu_sort_by_r(self):
        try:
            self.library_menu_sort_by(L.media_room.library_menu.option_sort_by_r)
            # verify if option is marked
            self.library_menu_sort_by()
            if self.exist(L.media_room.library_menu.option_sort_by_r).AXMenuItemMarkChar == '':
                logger('Fail to verify option mark')
                raise Exception
            self.keyboard.esc()
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_menu_sort_by_g(self):
        try:
            self.library_menu_sort_by(L.media_room.library_menu.option_sort_by_g)
            # verify if option is marked
            self.library_menu_sort_by()
            if self.exist(L.media_room.library_menu.option_sort_by_g).AXMenuItemMarkChar == '':
                logger('Fail to verify option mark')
                raise Exception
            self.keyboard.esc()
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_menu_sort_by_b(self):
        try:
            self.library_menu_sort_by(L.media_room.library_menu.option_sort_by_b)
            # verify if option is marked
            self.library_menu_sort_by()
            if self.exist(L.media_room.library_menu.option_sort_by_b).AXMenuItemMarkChar == '':
                logger('Fail to verify option mark')
                raise Exception
            self.keyboard.esc()
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_menu_sort_by_date(self):
        try:
            self.library_menu_sort_by(L.media_room.library_menu.option_sort_by_date)
            # verify if option is marked
            self.library_menu_sort_by()
            if self.exist(L.media_room.library_menu.option_sort_by_date).AXMenuItemMarkChar == '':
                logger('Fail to verify option mark')
                raise Exception
            self.keyboard.esc()
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_menu_display_as_extra_large_icons(self):
        try:
            self.library_menu_display_as(L.media_room.library_menu.option_extra_large_icons)
            # verify if option is marked
            self.library_menu_display_as()
            if self.exist(L.media_room.library_menu.option_extra_large_icons).AXMenuItemMarkChar == '':
                logger('Fail to verify option mark')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_menu_display_as_large_icons(self):
        try:
            self.library_menu_display_as(L.media_room.library_menu.option_large_icons)
            # verify if option is marked
            self.library_menu_display_as()
            if self.exist(L.media_room.library_menu.option_large_icons).AXMenuItemMarkChar == '':
                logger('Fail to verify option mark')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_menu_display_as_medium_icons(self):
        try:
            self.library_menu_display_as(L.media_room.library_menu.option_medium_icons)
            # verify if option is marked
            self.library_menu_display_as()
            if self.exist(L.media_room.library_menu.option_medium_icons).AXMenuItemMarkChar == '':
                logger('Fail to verify option mark')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_menu_display_as_small_icons(self):
        try:
            self.library_menu_display_as(L.media_room.library_menu.option_small_icons)
            # verify if option is marked
            self.library_menu_display_as()
            if self.exist(L.media_room.library_menu.option_small_icons).AXMenuItemMarkChar == '':
                logger('Fail to verify option mark')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    # background music ===================
    def library_menu_sort_by_category(self):
        try:
            self.library_menu_sort_by(L.media_room.library_menu.option_sort_by_category)
            # verify if option is marked
            self.library_menu_sort_by()
            if self.exist(L.media_room.library_menu.option_sort_by_category).AXMenuItemMarkChar == '':
                logger('Fail to verify option mark')
                raise Exception
            self.keyboard.esc()
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_menu_sort_by_download(self):
        try:
            self.library_menu_sort_by(L.media_room.library_menu.option_sort_by_download)
            # verify if option is marked
            self.library_menu_sort_by()
            if self.exist(L.media_room.library_menu.option_sort_by_download).AXMenuItemMarkChar == '':
                logger('Fail to verify option mark')
                raise Exception
            self.keyboard.esc()
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    # media content collection view
    def get_media_content_position(self, name):
        position = -1
        logger(f'get_content_position start. {name=}')
        try:
            # get collection list
            el_list = self.exist(L.media_room.library_listview.collection_list)
            if not el_list:
                logger('Fail to get unit_collection_view_item')
            els_unit = self.exist_elements(L.media_room.library_listview.unit_collection_view_item_text, el_list)
            # get target element
            is_found = 0
            for el_text in els_unit:
                if el_text.AXValue == name:
                    # get position and size
                    position = el_text.AXPosition + el_text.AXSize
                    is_found = 1
                    break
            if is_found == 0:
                logger(f'Fail to fund the {name=}')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return position

    def select_media_content(self, name): # support media content room and color board room
        try:
            x,y,w,h = self.get_media_content_position(name)
            self.mouse.click(int(x+int(w/2)),int(y+int(h/2)))
            time.sleep(OPERATION_DELAY)
            if not self.is_exist(L.main.tips_area.btn_insert_to_selected_track, None, 2):
                logger('Fail to select media')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def collection_view_right_click(self, locator=None):
        try:
            # get collection view frame
            el_collection_view = self.exist(L.media_room.library_listview.collection_list)
            self.mouse.right_click(el_collection_view.AXPosition[0]+10, el_collection_view.AXPosition[1]+40)
            if locator:
                self.exist_click(locator)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def collection_view_right_click_import_media_files(self, full_path):
        try:
            # get collection view frame
            img_collection_view_before = self.snapshot(L.media_room.library_listview.main_frame)
            self.collection_view_right_click()
            self.exist_click(L.media_room.library_menu.option_import_media_files)
            self.select_file(full_path)
            time.sleep(OPERATION_DELAY*2)
            self.exist_click(L.media_room.confirm_dialog.btn_no)
            img_collection_view_after = self.snapshot(L.media_room.library_listview.main_frame)
            # verify is collection view frame is changed by snapshot
            result_verify = self.compare(img_collection_view_before, img_collection_view_after, similarity=0.98)
            if result_verify:
                logger('Fail to verify after import file(s)')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def collection_view_right_click_import_a_media_folder(self, full_path):
        try:
            # get collection view frame
            img_collection_view_before = self.snapshot(L.media_room.library_listview.main_frame)
            self.collection_view_right_click()
            self.exist_click(L.media_room.library_menu.option_import_a_media_folder)
            self.select_file(full_path)
            time.sleep(OPERATION_DELAY*3)
            img_collection_view_after = self.snapshot(L.media_room.library_listview.main_frame)
            # verify is collection view frame is changed by snapshot
            result_verify = self.compare(img_collection_view_before, img_collection_view_after)
            if result_verify:
                logger('Fail to verify after import folder')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def collection_view_right_click_sort_by(self, locator=None):
        try:
            # get collection view frame
            self.collection_view_right_click()
            self.exist_click(L.media_room.library_menu.option_sort_by)
            if locator:
                self.exist_click(locator)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def collection_view_right_click_select_all(self):
        try:
            self.collection_view_right_click(L.media_room.library_menu.option_select_all)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def collection_view_right_click_empty_library(self):
        try:
            img_collection_view_before = self.snapshot(L.media_room.library_listview.main_frame)
            self.collection_view_right_click(L.media_room.library_menu.option_empty_the_library)
            time.sleep(OPERATION_DELAY)
            img_collection_view_after = self.snapshot(L.media_room.library_listview.main_frame)
            # verify is collection view frame is changed by snapshot
            result_verify = self.compare(img_collection_view_before, img_collection_view_after)
            if result_verify:
                logger('Fail to verify after clicked select all')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def collection_view_right_click_remove_all_unused_content_from_library(self):
        try:
            img_collection_view_before = self.snapshot(L.media_room.library_listview.main_frame)
            self.collection_view_right_click(L.media_room.library_menu.option_remove_all_unused_content_from_library)
            time.sleep(OPERATION_DELAY)
            img_collection_view_after = self.snapshot(L.media_room.library_listview.main_frame)
            # verify is collection view frame is changed by snapshot
            result_verify = self.compare(img_collection_view_before, img_collection_view_after)
            if result_verify:
                logger('Fail to verify after clicked select all')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def collection_view_right_click_dock_undock_library_window(self):
        try:
            self.collection_view_right_click(L.media_room.library_menu.option_dock_undock_library_window)
            time.sleep(OPERATION_DELAY)
            self.collection_view_right_click()
            if not self.exist(L.media_room.library_menu.option_reset_all_undocked_windows).AXEnabled:
                logger('Fail to verify click dock/undock library window.')
                raise Exception
            self.keyboard.esc()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def collection_view_right_click_reset_all_undocked_windows(self):
        try:
            self.collection_view_right_click(L.media_room.library_menu.option_reset_all_undocked_windows)
            time.sleep(OPERATION_DELAY)
            self.collection_view_right_click()
            if self.exist(L.media_room.library_menu.option_reset_all_undocked_windows).AXEnabled:
                logger('Fail to verify click reset all undocked windows.')
                raise Exception
            self.keyboard.esc()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def collection_view_right_click_download_from(self, locator=None):
        try:
            # get collection view frame
            self.collection_view_right_click()
            self.exist_click(L.media_room.library_menu.option_download_from)
            if locator:
                self.exist_click(locator)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def collection_view_right_click_sort_by_name(self):
        try:
            self.collection_view_right_click_sort_by(L.media_room.library_menu.option_sort_by_name)
            # verify if option is marked
            self.collection_view_right_click_sort_by()
            if self.exist(L.media_room.library_menu.option_sort_by_name).AXMenuItemMarkChar == '':
                logger('Fail to verify option mark')
                raise Exception
            self.keyboard.esc()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def collection_view_right_click_sort_by_duration(self):
        try:
            self.collection_view_right_click_sort_by(L.media_room.library_menu.option_sort_by_duration)
            # verify if option is marked
            self.collection_view_right_click_sort_by()
            if self.exist(L.media_room.library_menu.option_sort_by_duration).AXMenuItemMarkChar == '':
                logger('Fail to verify option mark')
                raise Exception
            self.keyboard.esc()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def collection_view_right_click_sort_by_created_date(self):
        try:
            self.collection_view_right_click_sort_by(L.media_room.library_menu.option_sort_by_created_date)
            # verify if option is marked
            self.collection_view_right_click_sort_by()
            if self.exist(L.media_room.library_menu.option_sort_by_created_date).AXMenuItemMarkChar == '':
                logger('Fail to verify option mark')
                raise Exception
            self.keyboard.esc()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def collection_view_right_click_sort_by_file_size(self):
        try:
            self.collection_view_right_click_sort_by(L.media_room.library_menu.option_sort_by_file_size)
            # verify if option is marked
            self.collection_view_right_click_sort_by()
            if self.exist(L.media_room.library_menu.option_sort_by_file_size).AXMenuItemMarkChar == '':
                logger('Fail to verify option mark')
                raise Exception
            self.keyboard.esc()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def collection_view_right_click_sort_by_modified_date(self):
        try:
            self.collection_view_right_click_sort_by(L.media_room.library_menu.option_sort_by_modified_date)
            # verify if option is marked
            self.collection_view_right_click_sort_by()
            if self.exist(L.media_room.library_menu.option_sort_by_modified_date).AXMenuItemMarkChar == '':
                logger('Fail to verify option mark')
                raise Exception
            self.keyboard.esc()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def collection_view_right_click_sort_by_type(self):
        try:
            self.collection_view_right_click_sort_by(L.media_room.library_menu.option_sort_by_type)
            # verify if option is marked
            self.collection_view_right_click_sort_by()
            if self.exist(L.media_room.library_menu.option_sort_by_type).AXMenuItemMarkChar == '':
                logger('Fail to verify option mark')
                raise Exception
            self.keyboard.esc()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def collection_view_right_click_download_from_cyberlink_cloud(self):
        try:
            # get collection view frame
            self.collection_view_right_click_download_from()
            self.exist_click(L.media_room.library_menu.option_download_from_cyberlink_cloud)
            # verify if download media dialog pops up
            if not self.exist(L.media_room.download_media_dialog.btn_close):
                logger('Fail to open download media dialog')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def close_download_media_window(self):
        try:
            self.exist_click(L.media_room.download_media_dialog.btn_close)
            # verify if download media window is closed
            time.sleep(OPERATION_DELAY)
            if self.exist(L.media_room.download_media_dialog.btn_close, None, 3):
                logger('Fail to close download media window')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Media Room] Add media to specific tag by right click')
    def library_clip_context_menu_add_to(self, tag_name):
        try:
            self.activate()
            tag_media_amount_before = self.tag_get_media_amount(tag_name)
            self.right_click()
            self.select_right_click_menu('Add to', tag_name)
            time.sleep(OPERATION_DELAY)
            tag_media_amount_after = self.tag_get_media_amount(tag_name)
            logger(f'{tag_media_amount_after=}')
            if not tag_media_amount_after - tag_media_amount_before == 1:
                logger('Fail to add media to tag')
                raise Exception('Fail to add media to tag')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Media Room] Insert clip in library to selected track')
    def library_clip_context_menu_insert_on_selected_track(self):
        try:
            self.activate()
            self.right_click()
            self.select_right_click_menu('Insert on Selected Track')
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def library_clip_context_menu_remove_from_library(self):
        try:
            img_collection_view_before = self.snapshot(L.media_room.library_listview.main_frame)
            self.activate()
            self.right_click()
            self.select_right_click_menu('Remove from Library')
            time.sleep(OPERATION_DELAY)
            img_collection_view_after = self.snapshot(L.media_room.library_listview.main_frame)
            result_verify = self.compare(img_collection_view_before, img_collection_view_after)
            if result_verify:
                logger('Fail to verify after clicked select all')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Media Room] Move clip in library to trash can')
    def library_clip_context_menu_move_to_trash_can(self):
        try:
            img_collection_view_before = self.snapshot(L.media_room.library_listview.main_frame)
            self.activate()
            self.right_click()
            self.select_right_click_menu('Move to Trash Can')
            time.sleep(OPERATION_DELAY)
            img_collection_view_after = self.snapshot(L.media_room.library_listview.main_frame)
            result_verify = self.compare(img_collection_view_before, img_collection_view_after)
            if result_verify:
                logger('Fail to verify after moved to trash can')
                raise Exception('Fail to verify after moved to trash can')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def library_clip_context_menu_find_in_timeline(self, name):
        try:
            self.activate()
            self.right_click()
            self.select_right_click_menu('Find in Timeline')
            time.sleep(OPERATION_DELAY*2)
            if not self.exist(L.media_room.library_media_find_in_timeline_confirm_dialog.static_text_file_name).AXValue == name:
                logger(f'Fail to find the {name} in timeline')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def close_library_clip_find_in_timeline_confirm_dialog(self):
        try:
            self.exist_click(L.media_room.library_media_find_in_timeline_confirm_dialog.btn_close)
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Media Room] Click [Precut...] from right click menu')
    def library_clip_context_menu_precut(self):
        try:
            self.activate()
            self.right_click()
            self.select_right_click_menu('Precut...')
            time.sleep(OPERATION_DELAY)
            if not self.exist(L.precut.main_window):
                logger(f'Fail to enter precut')
                raise Exception(f'Fail to enter precut')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def library_clip_context_menu_dock_undock_library_window(self):
        try:
            self.activate()
            btn_import_media_position_before = self.exist(L.media_room.btn_import_media)
            self.right_click()
            self.select_right_click_menu('Dock/Undock Library Window')
            time.sleep(OPERATION_DELAY*2)
            btn_import_media_position_after = self.exist(L.media_room.btn_import_media)
            if btn_import_media_position_after == btn_import_media_position_before:
                logger('Fail to dock/undock library window')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_clip_context_menu_reset_all_undocked_window(self):
        try:
            self.activate()
            btn_import_media_position_before = self.exist(L.media_room.btn_import_media)
            self.right_click()
            self.select_right_click_menu('Reset All Undocked Windows')
            time.sleep(OPERATION_DELAY*2)
            btn_import_media_position_after = self.exist(L.media_room.btn_import_media)
            if btn_import_media_position_after == btn_import_media_position_before:
                logger('Fail to dock/undock library window')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_clip_context_menu_view_properties(self):
        try:
            self.activate()
            self.right_click()
            self.select_right_click_menu('View Properties')
            time.sleep(OPERATION_DELAY*3)
            if not self.exist(L.media_room.properties_dialog.main_window):
                logger('Fail to open properties dialog')
                raise Exception
            self.exist_click(L.media_room.properties_dialog.btn_close)
            time.sleep(OPERATION_DELAY)
            if self.exist(L.media_room.properties_dialog.main_window, None, 2):
                logger('Fail to close properties dialog')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_clip_context_menu_rotate_to(self, direction='Right'):
        try:
            self.activate()
            img_collection_view_before = self.snapshot(L.media_room.library_listview.main_frame)
            self.right_click()
            self.select_right_click_menu(f'Rotate {direction}')
            time.sleep(OPERATION_DELAY*3)
            img_collection_view_after = self.snapshot(L.media_room.library_listview.main_frame)
            result_verify = self.compare(img_collection_view_before, img_collection_view_after)
            if result_verify:
                logger(f'Fail to rotate clip to {direction}')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_clip_context_menu_rotate_right(self):
        try:
            self.library_clip_context_menu_rotate_to('Right')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_clip_context_menu_rotate_left(self):
        try:
            self.library_clip_context_menu_rotate_to('Left')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_clip_context_menu_change_alias(self, name):
        try:
            self.color_board_context_menu_change_alias(name)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_clip_context_menu_reset_alias(self, verify_name):
        try:
            self.color_board_context_menu_reset_alias(verify_name)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_clip_context_menu_show_in_library_preview(self):
        try:
            self.activate()
            self.right_click()
            self.select_right_click_menu('Show in Library Preview Window')
            time.sleep(OPERATION_DELAY * 2)
            if not self.is_exist(L.main.library_preview_window.slider):
                logger('Fail to show clip in library preview')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Media Room] Open [File Location] from [Library Clip] context menu by right click')
    def library_clip_context_menu_open_file_location(self):
        try:
            from ATFramework.drivers.driver_factory import DriverFactory
            from pages.page_factory import PageFactory
            from types import SimpleNamespace
            from configs.app_config import Finder_cap
            app_finder = SimpleNamespace(**Finder_cap)
            self.activate()
            self.right_click()
            self.select_right_click_menu('Open File Location')
            time.sleep(OPERATION_DELAY * 3)
            img_collection_view_before = self.screenshot()
            # create finder window driver
            driver_finder = DriverFactory().get_mac_driver_object('mac', app_finder.app_name, app_finder.app_bundleID, app_finder.app_path)
            finder_main_page = PageFactory().get_page_object('main_page', driver_finder)
            if not finder_main_page.exist(L.base.finder_window.btn_close):
                logger('Fail to open finder window')
                raise Exception('Fail to open finder window')
            finder_main_page.exist_click(L.base.finder_window.btn_close)
            time.sleep(OPERATION_DELAY)
            img_collection_view_after = self.screenshot()
            result_verify = self.compare(img_collection_view_before, img_collection_view_after)
            if result_verify:
                logger(f'Fail to close finder window')
                raise Exception(f'Fail to close finder window')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def color_board_switch_category_to_RGB(self):
        try:
            # click (Color Slider) button
            el_color_sliders = self.exist(L.media_room.colors.btn_color_sliders)
            self.el_click(el_color_sliders)
            time.sleep(OPERATION_DELAY)

            # Switch Category to RGB Slider
            category = self.exist(L.media_room.colors.category)
            category._activate()
            self.mouse.click(*category.center)
            items = self.exist(L.media_room.colors.category_items)
            for item in items:
                if item.AXTitle == 'RGB Sliders':
                    self.mouse.click(*item.center)
                    return True
            return False
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True



###
    def color_board_create_new_color_board(self, hex_color): # e.g. hex_color: FFFEEE (related: library_menu_new_color_board)
        try:
            self.exist_click(L.media_room.btn_create_new_color_board)
            # click dropdown menu to switch category RBG Sliders
            self.color_board_switch_category_to_RGB()

            el_hex_color = self.exist(L.media_room.colors.input_hex_color)
            self.el_click(el_hex_color)
            time.sleep(OPERATION_DELAY * 0.5)
            el_hex_color.AXValue = hex_color
            time.sleep(OPERATION_DELAY * 0.5)
            self.keyboard.enter()
            self.exist_click(L.media_room.colors.btn_close)
            if self.is_exist(L.media_room.colors.input_hex_color, None, 3):
                logger('Fail to close create new color board')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True


    def select_color_slider_category(self, name):
        category = self.exist(L.media_room.slider_category)
        category._activate()
        self.mouse.click(*category.center)
        items = self.exist(L.media_room.slider_category_items)
        for item in items:
            if item.AXTitle == name:
                self.mouse.click(*item.center)
                return True
        return False

    def select_color_palettes_category(self, name):
        category = self.exist(L.media_room.color_palettes_category)
        category._activate()
        self.mouse.click(*category.center)
        items = self.exist(L.media_room.color_palettes_category_items)
        for item in items:
            if item.AXTitle == name:
                self.mouse.click(*item.center)
                return True
        return False

    def color_board_create_new_color_board_button(self):
        try:
            self.exist_click(L.media_room.btn_create_new_color_board)
            time.sleep(OPERATION_DELAY * 2)
            if not self.is_exist(L.media_room.btn_color_sliders, None, 3):
                logger('Fail to enter create new color board')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_color_board_color_palettes(self):
        try:
            self.exist_click(L.media_room.btn_color_palettes)
            time.sleep(OPERATION_DELAY * 2)
            #if not self.is_exist(L.media_room.color_palettes_category, None, 3):
            #    logger('Fail to enter create new color board')
            #    raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_color_board_color_sliders(self):
        try:
            self.exist_click(L.media_room.btn_color_sliders)
            time.sleep(OPERATION_DELAY * 2)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_color_board_color_patettes_by_search(self, name):
        try:
            searchbox = self.exist(L.media_room.input_color_palettes_search)
            self.el_click(searchbox)
            time.sleep(OPERATION_DELAY * 0.5)
            searchbox.AXValue = name

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_select_color_board_color_patettes(self, name):
        items = self.exist(L.media_room.color_palettes_scroll_area_items)
        for item in items:
            if item.AXValue == name:
                self.mouse.click(*item.center)
                return True
        return False

    def click_color_board_close(self):
        try:
            self.exist_click(L.media_room.colors.btn_close)
            if self.is_exist(L.media_room.colors.input_hex_color, None, 3):
                logger('Fail to close create new color board')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_color_board_color_sliders_cmyk_sliders(self, cyan=0, magenta=0, yellow=0, black=0):
        try:
            if not self.exist(L.media_room.cmyk_sliders.cyan):
                logger("No cmyk sliders show up")
                raise Exception
            time.sleep(OPERATION_DELAY * 0.5)
            self.exist(L.media_room.cmyk_sliders.cyan).AXValue = float(cyan)
            time.sleep(OPERATION_DELAY * 0.5)
            self.exist(L.media_room.cmyk_sliders.magenta).AXValue = float(magenta)
            time.sleep(OPERATION_DELAY * 0.5)
            self.exist(L.media_room.cmyk_sliders.yellow).AXValue = float(yellow)
            time.sleep(OPERATION_DELAY * 0.5)
            self.exist(L.media_room.cmyk_sliders.black).AXValue = float(black)
            time.sleep(OPERATION_DELAY * 0.5)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_color_board_color_sliders_hsb_sliders(self, hue=0, saturation=0, brightness=0):
        try:
            if not self.exist(L.media_room.hsb_sliders.hue):
                logger("No hsb sliders show up")
                raise Exception
            time.sleep(OPERATION_DELAY * 0.5)
            self.exist(L.media_room.hsb_sliders.hue).AXValue = float(hue)
            time.sleep(OPERATION_DELAY * 0.5)
            self.exist(L.media_room.hsb_sliders.saturation).AXValue = float(saturation)
            time.sleep(OPERATION_DELAY * 0.5)
            self.exist(L.media_room.hsb_sliders.brightness).AXValue = float(brightness)
            time.sleep(OPERATION_DELAY * 0.5)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

###

    def color_board_context_menu_insert_on_selected_track(self, name):
        try:
            self.activate()
            self.hover_library_media(name)
            self.right_click()
            self.select_right_click_menu("Insert on Selected Track")
            locator = L.main.timeline.clip_name_unit
            locator[1]['AXValue'] = name
            if not self.find(locator):
                raise Exception("Insert color board fail")
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def color_board_context_menu_remove_from_media_library(self):
        try:
            img_collection_view_before = self.snapshot(L.media_room.library_listview.main_frame)
            self.activate()
            self.right_click()
            self.select_right_click_menu('Remove from Media Library')
            time.sleep(OPERATION_DELAY)
            img_collection_view_after = self.snapshot(L.media_room.library_listview.main_frame)
            result_verify = self.compare(img_collection_view_before, img_collection_view_after)
            if result_verify:
                logger('Fail to verify after clicked select all')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def color_board_context_menu_reset_alias(self, name_verify):
        try:
            self.activate()
            self.right_click()
            self.select_right_click_menu('Reset Alias')
            time.sleep(OPERATION_DELAY*2)
            els_text = self.exist_elements(L.media_room.library_listview.unit_collection_view_item_text)
            if not els_text:
                logger('Fail to list clip name')
                raise Exception
            is_found = 0
            for el_text in els_text:
                if el_text.AXValue == name_verify:
                    is_found = 1
                    break
            if is_found == 0:
                logger('Fail to verify after reset alias')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def color_board_context_menu_change_alias(self, name):
        try:
            self.activate()
            self.right_click()
            self.select_right_click_menu('Change Alias')
            time.sleep(OPERATION_DELAY*2)
            self.keyboard.send(name)
            self.keyboard.enter()
            time.sleep(OPERATION_DELAY * 2)
            els_text = self.exist_elements(L.media_room.library_listview.unit_collection_view_item_text)
            if not els_text:
                logger('Fail to list clip name')
                raise Exception
            is_found = 0
            for el_text in els_text:
                if el_text.AXValue == name:
                    is_found = 1
                    break
            if is_found == 0:
                logger('Fail to verify after changed alias')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action] Select specific category')
    def select_specific_category(self, category_name): # support all rooms category selection
        try:
            if category_name == 'My Favorites':
                category_name = '♥ My Favorites'

            els_category = self.exist_elements(L.media_room.unit_tag_room_text_field)
            if '(' not in category_name:
                category_name = category_name + ' ('
            is_found = 0
            for tag in els_category:
                if category_name in tag.AXValue:
                    is_found = 1
                    self.mouse.click(*tag.center)
                    break
            if is_found == 0:
                logger(f'Fail to select the specific category {category_name}')
                raise Exception(f'Fail to select the specific category {category_name}')
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Media Room] Select specific category in meta by name')
    def select_specific_category_in_meta(self, category_name): # support all rooms category selection
        try:
            els_category = self.exist_elements(L.media_room.unit_tag_room_text_field)

            is_found = 0
            for tag in els_category:
                if category_name in tag.AXValue:
                    is_found = 1
                    self.mouse.click(*tag.center)
                    break
            if is_found == 0:
                logger(f'Fail to select the specific category {category_name}')
                raise Exception(f'Fail to select the specific category {category_name}')
            time.sleep(OPERATION_DELAY*2)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def category_get_media_amount(self, name):
        try:
            result = []
            els_category = self.exist_elements(L.media_room.unit_tag_room_text_field)
            pattern = r'\((\d+)\)'
            for tag in els_category:
                if f'{name} (' in tag.AXValue:
                    logger(f'found category: {tag.AXValue}')
                    result = re.findall(pattern, tag.AXValue)
                    break
            if not result:
                logger('Fail to get count of category')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            return -1
        return int(result[0])

    def category_get_media_bgm_amount(self, name):
        try:
            result = []
            els_category = self.exist_elements(L.media_room.unit_tag_room_bgm_text_field)
            pattern = r'\((\d+)\)'
            for tag in els_category:
                if f'{name} (' in tag.AXValue:
                    logger(f'found category: {tag.AXValue}')
                    result = re.findall(pattern, tag.AXValue)
                    break
            if not result:
                logger('Fail to get count of category')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            return -1
        return int(result[0])

    def background_music_context_menu_dock_undock_library_window(self):
        try:
            self.activate()
            btn_import_media_position_before = self.exist(L.media_room.library_menu.btn_menu).AXPosition
            el_table_view = self.exist(L.media_room.scroll_area.library_table_view)
            self.mouse.move(*el_table_view.center)
            time.sleep(OPERATION_DELAY)
            self.right_click()
            self.select_right_click_menu('Dock/Undock Library Window')
            time.sleep(OPERATION_DELAY)
            btn_import_media_position_after = self.exist(L.media_room.library_menu.btn_menu).AXPosition
            if btn_import_media_position_after == btn_import_media_position_before:
                logger('Fail to dock/undock library window')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def background_music_context_menu_reset_all_undocked_windows(self):
        try:
            self.activate()
            btn_import_media_position_before = self.exist(L.media_room.library_menu.btn_menu).AXPosition
            el_table_view = self.exist(L.media_room.scroll_area.library_table_view)
            self.mouse.move(*el_table_view.center)
            time.sleep(OPERATION_DELAY)
            self.right_click()
            self.select_right_click_menu('Reset All Undocked Windows')
            time.sleep(OPERATION_DELAY)
            btn_import_media_position_after = self.exist(L.media_room.library_menu.btn_menu).AXPosition
            if btn_import_media_position_after == btn_import_media_position_before:
                logger('Fail to reset all undocked windows')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def background_music_show_meta_list(self, number):
        try:
            # Save meta music to meta_music_list
            # Argument 1 : save meta "count"
            # if number = 3, only save 1st ~ 3rd meta music
            # if number = 10, save 1st ~ 10th meta music

            meta_music_list = []

            rows = self.exist([{'AXIdentifier': 'IDC_LIBRARY_TABLEVIEW_DETAILED'},
                              {'AXSubrole': 'AXTableRow', "get_all": True, "recursive": False}],timeout=0)

            find_count = 0
            for row in rows:
                if find_count == number:
                    break
                target = self.exist([{'AXRole': 'AXCell'}, {'AXIdentifier': 'DetailedViewItemTextField'}],
                                    parent=row,
                                    timeout=0)
                meta_music_list.append(target.AXValue)
                find_count = find_count + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return meta_music_list

    def sound_clips_hover_library_clip(self, name, is_wait_tip=True):
        try:
            img_before = self.snapshot(L.media_room.scroll_area.library_table_view)
            # locator = L.media_room.scroll_area.table_view_text_field_name
            # locator[1]['AXValue'] = name
            # el_name = self.exist(locator)
            rows = self.exist([{'AXIdentifier': 'IDC_LIBRARY_TABLEVIEW_DETAILED'},
                              {'AXSubrole': 'AXTableRow', "get_all": True, "recursive": False}],timeout=0)
            for row in rows:
                target = self.exist([{'AXRole': 'AXCell'}, {'AXIdentifier': 'DetailedViewItemTextField'}],
                                    parent=row,
                                    timeout=0)
                if target.AXValue == name:
                    logger(f"Found clip >> {name} <<")
                    el_name = target
                    break
            # calculate target location
            name_pos = el_name.AXPosition
            table_frame = self.exist(L.media_room.scroll_area.library_table_view)
            table_frame_size = table_frame.AXSize
            table_frame_pos = table_frame.AXPosition
            if name_pos[1] > table_frame_pos[1]+table_frame_size[1] or name_pos[1] < table_frame_pos[1]:
                table_detail_size = self.exist(L.media_room.scroll_area.library_table_view_detailed).AXSize
                #table_pos = self.exist(L.media_room.scroll_area.library_table_view_detailed).AXPosition
                total_offset_length = table_detail_size[1] - table_frame_size[1]  # <<
                offset_name_move_to_frame_center = abs(name_pos[1] - (table_frame_pos[1] + (table_frame_size[1] * 0.5)))
                if offset_name_move_to_frame_center < total_offset_length:
                    current_percentage_scroll_y = self.sound_clips_scroll_bar_vertical_get_value() # if current position is not at 0
                    if name_pos[1] < table_frame_pos[1]: # target is upper from frame
                        percentage_scroll_y = current_percentage_scroll_y - (offset_name_move_to_frame_center / total_offset_length)
                    else:
                        percentage_scroll_y = (offset_name_move_to_frame_center / total_offset_length) + current_percentage_scroll_y
                else:
                    percentage_scroll_y = 1
                self.drag_sound_clips_scroll_bar_vertical(str(percentage_scroll_y))
                time.sleep(OPERATION_DELAY * 2)
                # ----------------------------
            self.mouse.move(*el_name.center)
            time.sleep(OPERATION_DELAY)
            if is_wait_tip:
                time.sleep(OPERATION_DELAY * 4)
            img_after = self.snapshot(L.media_room.scroll_area.library_table_view)
            result_verify = self.compare(img_before, img_after, similarity=0.99999)
            #if result_verify:
            #    logger(f'Fail to verify hover library clip')
            #    raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Media Room] Select specific sound clips in library by name')
    def sound_clips_select_media(self, name):
        try:
            self.sound_clips_hover_library_clip(name, False)
            time.sleep(OPERATION_DELAY * 0.5)
            self.left_click()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def sound_clips_sort_button_click_duration(self):
        try:
            img_before = self.snapshot(L.media_room.scroll_area.library_table_view)
            self.exist_click(L.media_room.scroll_area.btn_sort_by_duration)
            time.sleep(OPERATION_DELAY)
            img_after = self.snapshot(L.media_room.scroll_area.library_table_view)
            result_verify = self.compare(img_before, img_after)
            if result_verify:
                logger(f'Fail to verify click sort by duration')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def sound_clips_sort_button_click_date(self):
        try:
            img_before = self.snapshot(L.media_room.scroll_area.library_table_view)
            self.exist_click(L.media_room.scroll_area.btn_sort_by_date)
            time.sleep(OPERATION_DELAY)
            img_after = self.snapshot(L.media_room.scroll_area.library_table_view)
            result_verify = self.compare(img_before, img_after)
            if result_verify:
                logger(f'Fail to verify click sort by date')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def sound_clips_sort_button_click_name(self):
        try:
            img_before = self.snapshot(L.media_room.scroll_area.library_table_view)
            self.exist_click(L.media_room.scroll_area.btn_sort_by_name)
            time.sleep(OPERATION_DELAY)
            img_after = self.snapshot(L.media_room.scroll_area.library_table_view)
            result_verify = self.compare(img_before, img_after)
            if result_verify:
                logger(f'Fail to verify click sort by name')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def sound_clips_sort_button_click_category(self):
        try:
            img_before = self.snapshot(L.media_room.scroll_area.library_table_view)
            self.exist_click(L.media_room.scroll_area.btn_sort_by_category)
            time.sleep(OPERATION_DELAY)
            img_after = self.snapshot(L.media_room.scroll_area.library_table_view)
            result_verify = self.compare(img_before, img_after)
            if result_verify:
                logger(f'Fail to verify click sort by category')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def sound_clips_sort_button_click_size(self):
        try:
            img_before = self.snapshot(L.media_room.scroll_area.library_table_view)
            self.exist_click(L.media_room.scroll_area.btn_sort_by_size)
            time.sleep(OPERATION_DELAY)
            img_after = self.snapshot(L.media_room.scroll_area.library_table_view)
            result_verify = self.compare(img_before, img_after)
            if result_verify:
                logger(f'Fail to verify click sort by size')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def sound_clips_sort_button_click_download(self):
        try:
            img_before = self.snapshot(L.media_room.scroll_area.library_table_view)
            self.exist_click(L.media_room.scroll_area.btn_sort_by_download)
            time.sleep(OPERATION_DELAY)
            img_after = self.snapshot(L.media_room.scroll_area.library_table_view)
            result_verify = self.compare(img_before, img_after)
            if result_verify:
                logger(f'Fail to verify click sort by download')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def sound_clips_context_menu_dock_undock_library_window(self):
        try:
            self.background_music_context_menu_dock_undock_library_window()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def sound_clips_context_menu_reset_all_undocked_windows(self):
        try:
            self.background_music_context_menu_reset_all_undocked_windows()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_sound_clips_scroll_bar_vertical(self, value): # value: 0(top) to 1(down)
        try:
            img_before = self.snapshot(L.media_room.scroll_area.library_table_view)
            self.exist(L.media_room.scroll_area.sound_clips_scroll_bar_vertical).AXValue = float(value)
            time.sleep(OPERATION_DELAY)
            img_after = self.snapshot(L.media_room.scroll_area.library_table_view)
            result_verify = self.compare(img_before, img_after)
            if result_verify:
                logger(f'Fail to verify table view content change')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def sound_clips_scroll_bar_vertical_get_value(self):
        try:
            value = self.exist(L.media_room.scroll_area.sound_clips_scroll_bar_vertical).AXValue
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return value

    def drag_sound_clips_scroll_bar_horizontal(self, value): # value: 0(left) to 1(right)
        try:
            img_before = self.snapshot(L.media_room.scroll_area.library_table_view)
            self.exist(L.media_room.scroll_area.sound_clips_scroll_bar_horizontal).AXValue = float(value)
            time.sleep(OPERATION_DELAY)
            img_after = self.snapshot(L.media_room.scroll_area.library_table_view)
            result_verify = self.compare(img_before, img_after)
            if result_verify:
                logger(f'Fail to verify table view content change')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_color_board_scroll_bar(self, value):
        try:
            img_before = self.snapshot(L.media_room.scroll_area.library_table_view)
            self.exist(L.media_room.scroll_area.table_view_scroll_bar_unit).AXValue = float(value)
            time.sleep(OPERATION_DELAY)
            img_after = self.snapshot(L.media_room.scroll_area.library_table_view)
            result_verify = self.compare(img_before, img_after)
            if result_verify:
                logger(f'Fail to verify table view content change')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_media_content_scroll_bar(self, value):
        try:
            self.drag_color_board_scroll_bar(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_background_music_scroll_bar_vertical(self, value):
        try:
            self.drag_sound_clips_scroll_bar_vertical(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_background_music_scroll_bar_horizontal(self, value):
        try:
            self.drag_sound_clips_scroll_bar_horizontal(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def background_music_meta_context_menu_download(self, name, timeout=20):
        try:
            self.sound_clips_select_media(name)
            time.sleep(OPERATION_DELAY)
            self.right_click()
            time.sleep(OPERATION_DELAY)
            self.select_right_click_menu('Download')
            time.sleep(timeout)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def background_music_clip_context_menu_download(self, name, timeout=30):
        try:
            download_count_before = self.category_get_media_bgm_amount('Downloaded')
            logger(download_count_before)
            self.sound_clips_select_media(name)
            time.sleep(OPERATION_DELAY)
            self.right_click()
            time.sleep(OPERATION_DELAY)
            self.select_right_click_menu('Download')
            time.sleep(OPERATION_DELAY * 3)
            time_start = time.time()
            is_completed = 0
            while time.time() - time_start < timeout:
                download_count_current = self.category_get_media_bgm_amount('Downloaded')
                check_result = download_count_current - download_count_before
                logger(check_result)
                if check_result == 1:
                    logger('Download OK')
                    is_completed = 1
                    break
            if is_completed == 0:
                logger('Fail to verify download')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def background_music_clip_context_menu_delete_from_disk(self, name, timeout=30):
        try:
            download_count_before = self.category_get_media_amount('Downloaded')
            self.sound_clips_select_media(name)
            time.sleep(OPERATION_DELAY)
            self.right_click()
            self.select_right_click_menu('Delete from Disk')
            self.exist_click(L.media_room.confirm_dialog.btn_yes)
            time_start = time.time()
            is_completed = 0
            while time.time() - time_start < timeout:
                if download_count_before - self.category_get_media_amount('Downloaded') == 1:
                    logger('Delete OK')
                    is_completed = 1
                    break
            if is_completed == 0:
                logger('Fail to verify download')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Verify][Media Room] Check [Download] mark if shown on BG music for specific music')
    def background_music_check_download_mark(self, name):
        try:
            els_row = self.exist_elements(L.media_room.scroll_area.table_view_row_unit)
            if not els_row:
                logger('Fail to list rows from table view')
                raise Exception('Fail to list rows from table view')
            is_found = 0
            logger(f'the {len(els_row)=}')
            for el_row in els_row:
                el_name = self.exist(L.media_room.scroll_area.table_view_text_field_name, el_row)
                if el_name.AXValue == name:
                    is_found = 1
                    # check if download ok exists
                    if not self.exist(L.media_room.scroll_area.table_view_text_field_download_button, el_row, timeout=8):
                        logger('Fail to verify download icon')
                        raise Exception('Fail to verify download icon')
                    break
            if is_found == 0:
                logger(f'Fail to verify download button of {name=}')
                raise Exception(f'Fail to verify download button of {name=}')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
    
    @step('[Verify][Media Room] Check [Download OK] mark if shown on BG music for specific music')
    def background_music_check_download_ok_mark(self, name):
        try:
            els_row = self.exist_elements(L.media_room.scroll_area.table_view_row_unit)
            if not els_row:
                logger('Fail to list rows from table view')
                raise Exception('Fail to list rows from table view')
            is_found = 0
            logger(f'the {len(els_row)=}')
            for el_row in els_row:
                el_name = self.exist(L.media_room.scroll_area.table_view_text_field_name, el_row)
                if el_name.AXValue == name:
                    is_found = 1
                    # check if download ok exists
                    if not self.exist(L.media_room.scroll_area.table_view_text_field_download_ok, el_row, timeout=8):
                        logger('Fail to verify download ok icon')
                        raise Exception('Fail to verify download ok icon')
                    logger('Verify download ok icon Pass')
                    break
            if is_found == 0:
                logger(f'Fail to verify download ok of {name=}')
                raise Exception(f'Fail to verify download ok of {name=}')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def background_music_get_download_icon_image(self, name):
        try:
            icon_image = ''
            els_row = self.exist_elements(L.media_room.scroll_area.table_view_row_unit)
            if not els_row:
                logger('Fail to list rows from table view')
                raise Exception
            is_found = 0
            logger(f'the {len(els_row)=}')
            for el_row in els_row:
                el_name = self.exist(L.media_room.scroll_area.table_view_text_field_name, el_row)
                if el_name.AXValue == name:
                    is_found = 1
                    # snapshot download icon image
                    el_download = self.exist(L.media_room.scroll_area.table_view_text_field_download, el_row)
                    icon_image = self.snapshot(el_download)
                    break
            if is_found == 0:
                logger(f'Fail to verify download ok of {name=}')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return icon_image

    def undock_library_window_click_minimize(self):
        try:
            img_before = self.screenshot()
            self.exist_click(L.media_room.undock_library_window.btn_minimize)
            time.sleep(OPERATION_DELAY)
            img_after = self.screenshot()
            result_verify = self.compare(img_before, img_after)
            if result_verify:
                logger(f'Fail to verify click minimize')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_show_minimized_library_window(self):
        try:
            img_before = self.screenshot()
            self.exist_click(L.media_room.top_tool_bar.btn_show_minimized_library_window)
            self.exist_click(L.media_room.top_tool_bar.option_media_library)
            time.sleep(OPERATION_DELAY)
            img_after = self.screenshot()
            result_verify = self.compare(img_before, img_after)
            if result_verify:
                logger(f'Fail to verify click minimize')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Media Room] Click [Up One Level] button in media content')
    def media_content_click_up_one_level(self):
        try:
            img_before = self.snapshot(L.media_room.scroll_area.library_table_view)
            self.select_media_content('..')
            time.sleep(OPERATION_DELAY)
            img_after = self.snapshot(L.media_room.scroll_area.library_table_view)
            result_verify = self.compare(img_before, img_after)
            if result_verify:
                logger(f'Fail to verify table view content change')
                raise Exception(f'Fail to verify table view content change')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def set_splitter_between_media_libaray_and_preview_window(self, percentage=55): # percentage: range - 50(center) to 70(right)
        try:
            el_splitter = self.exist(L.media_room.splitter_library_to_preview_window)
            value = int((el_splitter.AXMaxValue-el_splitter.AXMinValue)*percentage/100)
            print(f'{value=}')
            el_splitter.AXValue = value
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def sound_clips_clip_context_menu_download(self, name, timeout=30):
        try:
            if not self.background_music_clip_context_menu_download(name, timeout):
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def sound_clips_clip_context_menu_delete_from_disk(self, name, timeout=30):
        try:
            if not self.background_music_clip_context_menu_delete_from_disk(name, timeout):
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def sound_clips_check_download_mark(self, name):
        try:
            if not self.background_music_check_download_ok_mark(name):
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            return False
        return True

    def collection_view_deselected_media(self):
        try:
            #img_before = self.snapshot(L.media_room.scroll_area.library_table_view)
            el_collection_view = self.exist(L.media_room.library_listview.collection_list)
            self.mouse.click(el_collection_view.AXPosition[0] + 10, el_collection_view.AXPosition[1] + 40)
            time.sleep(OPERATION_DELAY)
            img_after = self.snapshot(L.media_room.scroll_area.library_table_view)
            #result_verify = self.compare(img_before, img_after)
            #if result_verify:
            #    logger(f'Fail to verify table view content change')
            #    raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def high_definition_video_confirm_dialog_click_no(self):
        try:
            # check Do not show again checkbox
            el_chx_do_not_show = self.exist(L.media_room.confirm_dialog.chx_do_not_show_again)
            chx_position = el_chx_do_not_show.AXPosition
            chx_size = el_chx_do_not_show.AXSize
            self.mouse.click(int(chx_position[0]+chx_size[0]/4), int(chx_position[1]+chx_size[1]/2))
            time.sleep(OPERATION_DELAY * 0.5)
            # click No
            img_before = self.screenshot()
            self.exist_click(L.media_room.confirm_dialog.btn_no)
            time.sleep(OPERATION_DELAY)
            img_after = self.screenshot()
            result_verify = self.compare(img_before, img_after)
            if result_verify:
                logger(f'Fail to verify screenshot change')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def aspect_ratio_conflict_dialog_click_option(self, option='no'): # option: yes, no
        try:
            # check Do not show again checkbox
            el_chx_do_not_show = self.exist(L.media_room.confirm_dialog.chx_do_not_show_again)
            chx_position = el_chx_do_not_show.AXPosition
            chx_size = el_chx_do_not_show.AXSize
            self.mouse.click(int(chx_position[0] + chx_size[0] / 4), int(chx_position[1] + chx_size[1] / 2))
            time.sleep(OPERATION_DELAY * 0.5)
            # click option
            img_before = self.screenshot()
            btn_option = eval(f'L.media_room.confirm_dialog.btn_{option}')
            self.exist_click(btn_option)
            time.sleep(OPERATION_DELAY)
            img_after = self.screenshot()
            result_verify = self.compare(img_before, img_after)
            if result_verify:
                logger(f'Fail to verify screenshot change')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def has_svrt_info_window(self,timeout=3):
        return self.is_exist(L.media_room.svrt_window.title, timeout=timeout)

    def is_show_high_definition_dialog(self):
        try:
            txt_description = self.exist(L.media_room.confirm_dialog.txt_description, 3).AXValue
            if 'High Definition Video' not in txt_description:
                logger('Fail to find the high definition dialog')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            return False
        return True
    @step('[Action][Media_Room] Handle high definition dialog')
    def handle_high_definition_dialog(self, option='no'):
        try:
            btn_option = eval(f'L.media_room.confirm_dialog.btn_{option}')
            self.exist_click(btn_option, timeout=7)
            time.sleep(OPERATION_DELAY * 2)
        except Exception as e:
            logger(f'Fail to click {option}. log={e}')
            raise Exception
        return True



    @step('[Action][Media_Room] Click [Meta] icon')
    def click_meta_icon(self):
        try:
            object_library_default_tag_tableview = self.exist(L.media_room.tag_main_frame)

            x, y = object_library_default_tag_tableview.AXPosition
            w, h = object_library_default_tag_tableview.AXSize

            # Click [Meta logo]
            new_x = x + w - 15
            new_y = y - 25

            self.mouse.move(new_x, new_y)
            self.mouse.click()
        except Exception as e:
            raise Exception(f'Exception occurs. log={e}')
    
    @step('[Verify][Media_Room] Check [Meta] webpage is opened after clicked [Meta] icon')
    def verify_after_click_meta_icon(self):
        try:
            #self.click(L.media_room.meta_music.icon_meta)
            time.sleep(OPERATION_DELAY * 5)

            if not 'Facebook' in self.check_chrome_page():
                logger('Fail to Facebook webpage.')
                self.close_chrome_page()
                return False

        except Exception as e:
            logger('Fail to click Meta button')
            self.close_chrome_page()
            return False
        self.close_chrome_page()
        self.activate()
        return True

class SVRT_Info(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def click_refresh(self):
        return self.click(L.media_room.svrt_window.btn_refresh)

    def click_close(self):
        return self.click(L.media_room.svrt_window.btn_close)

    def get_workload_reduced_percentage(self):
        return self.exist(L.media_room.svrt_window.field_work_reduced).AXValue

    def click_help(self):
        try:
            self.click(L.media_room.svrt_window.btn_help)
            time.sleep(OPERATION_DELAY * 0.5)
            self.select_right_click_menu('Help')
            time.sleep(OPERATION_DELAY * 5)
            if not 'SVRT' in self.check_chrome_page():
                logger('Fail to navigate to SVRT webpage.')
                self.close_chrome_page()
                return False
        except Exception as e:
            logger('Fail to click help button')
            self.close_chrome_page()
            return False
        self.close_chrome_page()
        self.activate()
        return True

    def open_tutorial_page(self):
        try:
            self.click(L.media_room.svrt_window.btn_help)
            time.sleep(OPERATION_DELAY * 0.5)
            self.select_right_click_menu('Profile analyzer and iSVRT tutorial')
            time.sleep(OPERATION_DELAY * 2)
            if not 'Tutorials' in self.check_chrome_page():
                logger('Fail to navigate to SVRT webpage.')
                self.close_chrome_page()
                return False
        except Exception as e:
            logger('Fail to click help button')
            self.close_chrome_page()
            return False
        self.close_chrome_page()
        self.activate()
        return True