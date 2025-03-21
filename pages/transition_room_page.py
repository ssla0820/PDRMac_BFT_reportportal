import time, datetime, os, copy

from .base_page import BasePage
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
# from AppKit import NSScreen
from .locator import locator as L
from reportportal_client import step

DELAY_TIME = 1 # sec

class Transition_room(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def find_specific_tag(self, name):
        tags = self.exist(L.base.tag_list)
        for tag in tags:
            if tag.AXValue.startswith(f"{name} ("):
                return True
        return False

    def add_transitionroom_new_tag(self, name):
        try:
            if not self.exist(L.transition_room.explore_view_region.Geometric_category):
                logger('Now is not in Transition Room')
                raise Exception

            # check current tags number
            if not self.exist(L.transition_room.explore_view_region.table_all_content_tags):
                logger('Fail to find table_all_content_tags')
                raise Exception

            tags_table = self.exist(L.transition_room.explore_view_region.table_all_content_tags).AXChildren
            before_add_tags_num = len(tags_table)
            logger(before_add_tags_num)

            # click (Add new tag)
            if not self.exist_click(L.transition_room.btn_add_new_tag):
                logger('Fail to find btn_add_new_tag')
                raise Exception
            time.sleep(DELAY_TIME*2)
            self.keyboard.send(name)
            time.sleep(DELAY_TIME)
            self.keyboard.enter()

            if self.exist(L.transition_room.warning_dialog.msg1):
                logger('add new tag [FAIL] - duplicate tag name')
                self.exist_click(L.transition_room.warning_dialog.ok)
                return False

            tags_table = self.exist(L.transition_room.explore_view_region.table_all_content_tags).AXChildren
            after_add_tags_num = len(tags_table)
            logger(after_add_tags_num)

            # Verify Step1.
            if after_add_tags_num != before_add_tags_num + 1:
                logger('Fail to add tag, count error after added.')
                raise Exception

            # Verify Step2.
            if not self.find_specific_tag(name):
                logger('Cannot find the tag [Verify FAIL]')
                return False

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def delete_tag(self, name):
        logger(f'delete tag {name} ')

        try:
            if not self.exist(L.transition_room.explore_view_region.Geometric_category):
                logger('Now is not in Transition Room')
                raise Exception

            # check current tags number
            if not self.exist(L.transition_room.explore_view_region.table_all_content_tags):
                logger('Fail to find table_all_content_tags')
                raise Exception

            tags_table = self.exist(L.transition_room.explore_view_region.table_all_content_tags).AXChildren
            current_tags_counts = len(tags_table)
            #logger(current_tags_counts)

            if not self.select_specific_tag(name):
                logger('Cannot find the tag')
                raise Exception("Cannot find the tag")
            if not self.exist_click(L.transition_room.btn_delete_tag):
                logger('Cannot find btn_delete_tag')
                raise Exception

            if self.exist(L.transition_room.warning_dialog.msg2):
                time.sleep(DELAY_TIME)
                self.exist_click(L.transition_room.warning_dialog.ok)

            time.sleep(DELAY_TIME)
            tags_table = self.exist(L.transition_room.explore_view_region.table_all_content_tags).AXChildren
            after_tags_counts = len(tags_table)
            #logger(after_tags_counts)

            # Verify Step
            if after_tags_counts != current_tags_counts - 1:
                logger('Fail to add tag, count error after added.')
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_RightClickMenu_Addto(self, name):
        # e.g. Add to > My Favorites :
        # select_RightClickMEnu_Addto('My Favorites')
        try:
            self.right_click()
            time.sleep(DELAY_TIME)
            if not self.select_right_click_menu('Add to', name):
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_RightClickMenu_RemoveFromFavorites(self):
        try:
            self.right_click()
            time.sleep(DELAY_TIME)
            if not self.select_right_click_menu('Remove from My Favorites'):
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_RightClickMenu_Delete(self):
        try:
            self.right_click()
            time.sleep(DELAY_TIME)
            if not self.select_right_click_menu('Delete (only for Custom/Downloaded)'):
                raise Exception

            time.sleep(DELAY_TIME*2)

            if self.exist(L.transition_room.warning_dialog.msg3):
                time.sleep(DELAY_TIME)

            # Verify Step
            if not self.exist_click(L.transition_room.warning_dialog.yes):
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_tag_RightClickMenu_DeleteTag(self, strTag):
        try:
            if not self.select_specific_tag(strTag):
                logger('Cannot find the tag')
                raise Exception("Cannot find the tag")

            self.right_click()
            time.sleep(DELAY_TIME)
            if not self.select_right_click_menu('Delete Tag'):
                raise Exception

            if not self.exist(L.transition_room.warning_dialog.msg2):
                raise Exception

            # Verify Step
            if not self.exist_click(L.transition_room.warning_dialog.ok):
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_tag_RightClickMenu_RenameTag(self, strTag, strRename):
        try:
            if not self.select_specific_tag(strTag):
                logger('Cannot find the tag')
                raise Exception("Cannot find the tag")

            self.right_click()
            time.sleep(DELAY_TIME)
            if not self.select_right_click_menu('Rename Tag'):
                raise Exception

            time.sleep(DELAY_TIME*2)
            self.keyboard.send(strRename)
            time.sleep(DELAY_TIME)
            self.keyboard.enter()

            # Verify Step
            if not self.find_specific_tag(strRename):
                logger('Rename FAIL')
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def check_is_in_special_category(self, strCategory, name):
        # e.g. Check "TRA6503" is in Downloaded category ?
        # check_is_in_special_category('Downloaded', 'TRA6503')
        try:
            if not self.select_specific_tag(f'{strCategory}'):
                raise Exception

            # select custom template w/ name
            if not self.find({'AXValue': f'{name}', 'AXRole': 'AXStaticText'}):
                return False

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_ImportTransitionTemplates(self, full_path):
        try:
            if not self.exist_click(L.transition_room.btn_import_media):
                logger('Cannot find btn_import_media')
                raise Exception('Cannot find btn_import_media')
            time.sleep(DELAY_TIME*2)
            if not self.exist_click(L.transition_room.btn_import_transition_objects):
                logger('Cannot find btn_import_transition_objects')
                raise Exception('Cannot find btn_import_transition_objects')
            time.sleep(DELAY_TIME*2)
            if not self.select_file(full_path):
                raise Exception('Cannot select file w/ full_path')

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_DownloadContent_from_DZCloud(self):
        try:
            if not self.exist_click(L.transition_room.btn_import_media):
                raise Exception
            time.sleep(DELAY_TIME*2)

            if not self.exist(L.transition_room.btn_import_transition_objects):
                logger('not in Transition Room')
                raise Exception

            if not self.exist_click(L.transition_room.btn_download_from_DZ_cloud):
                raise Exception
            time.sleep(DELAY_TIME*2)

            # Verify Step
            if not self.exist(L.transition_room.download_dialog.main):
                raise Exception
            # For v2922 workaround .. skip this check (exception -25200)
            #if not self.exist(L.transition_room.download_dialog.str_Title):
            #    raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def download_content_from_CL(self, name, close_win=True):
        try:
            # before_snapshot
            old_img = self.snapshot(self.area.library)

            # click (Download Content from DirectorZone/Cloud)
            if not self.click_DownloadContent_from_DZCloud():
                raise Exception
            # if not enter (Cyberlink Cloud) page, raise Exception
            item = self.exist(L.transition_room.download_dialog.cloud_tab)
            for x in range(100):
                if item.AXEnabled:
                    logger('break')
                    break
                if x == 99:
                    logger('Tab cannot active [Time out]')
                    raise Exception
                time.sleep(DELAY_TIME)

            # select custom template w/ name
            self.mouse.click(*self.find({'AXValue': f'{name}', 'AXRole': 'AXStaticText'}).center)

            # click download
            if not self.exist_click(L.transition_room.download_dialog.btn_download):
                raise Exception
            else:
                logger('click download')
            time.sleep(DELAY_TIME*3)

            # Verify Step:
            # For v2922 workaround .. skip this check (exception -25200)
            #if self.exist_click(L.transition_room.warning_dialog.msg4):
            #    time.sleep(DELAY_TIME)
            #    self.exist_click(L.transition_room.warning_dialog.ok)

            if close_win:
                self.exist_click(L.transition_room.download_dialog.btn_close)
                time.sleep(DELAY_TIME)

            # after_snapshot
            self.mouse.move(0, 0)
            new_img = self.snapshot(self.area.library)
            # if old_image == new_ image, library content does not change
            # check main window has been changed (Transition Room switch to download category & show content)
            if self.compare(old_img, new_img, similarity=0.99):
                return False

            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def delete_content_in_Download_category(self, name):
        # e.g. Delete "TRA6503" is in Downloaded category ?
        # delete_content_in_Download_category('TRA6503')
        try:
            if not self.select_specific_tag('Downloaded'):
                raise Exception

            time.sleep(DELAY_TIME)
            # select template w/ temp_name
            self.mouse.click(*self.find({'AXValue': f'{name}', 'AXRole': 'AXStaticText'}).center)
            time.sleep(DELAY_TIME)
            self.select_RightClickMenu_Delete()

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Transition Room] Drag [Scroll Bar] to (value)')
    def drag_TransitionRoom_Scroll_Bar(self, value):
        try:
            self.exist(L.transition_room.scroll_bar.scroll_elem).AXValue = float(value)
            time.sleep(DELAY_TIME)
            # Verify Step
            if float(value) == self.exist(L.transition_room.scroll_bar.scroll_elem).AXValue:
                return True
            else:
                return False
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def search_Transition_room_library(self, name=None):
        try:
            if not name:
                raise Exception
            time.sleep(DELAY_TIME)

            # if library field has content, should clear all
            self.exist_click(L.transition_room.btn_search_cancel)

            img_collection_view_before = self.snapshot(L.media_room.library_listview.main_frame)
            self.exist_click(L.transition_room.input_search)
            self.keyboard.send(name)
            time.sleep(DELAY_TIME)
            self.press_enter_key()
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

    def search_Transition_room_click_cancel(self):
        try:
            if not self.exist_click(L.transition_room.btn_search_cancel):
                logger('Fail to click search cancel button')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def apply_LibraryMenu_MyFavorite_Transition_to_all_video(self, strType=None):
        # parameter: Prefix, Postfix, Cross, Overlap
        try:
            if not strType:
                raise Exception
            # check parameter is valid or not
            list1 = ['Prefix', 'Postfix', 'Cross', 'Overlap']
            find_flag = 0
            for x in list1:
                if x == strType:
                    find_flag = 1
                    break
            if not find_flag:
                logger('parameter is invalid')
                raise Exception

            # click library menu button
            if not self.exist_click(L.media_room.library_menu.btn_menu):
                logger('Fail to click library menu button')
                raise Exception
            type1 = f'{strType} Transition'
            if not self.select_right_click_menu('Apply My Favorite Transition to All Videos', type1):
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def apply_LibraryMenu_Fading_Transition_to_all_video(self, strType=None):
        # parameter: Prefix, Postfix, Cross, Overlap
        try:
            if not strType:
                raise Exception
            # check parameter is valid or not
            list1 = ['Prefix', 'Postfix', 'Cross', 'Overlap']
            find_flag = 0
            for x in list1:
                if x == strType:
                    find_flag = 1
                    break
            if not find_flag:
                logger('parameter is invalid')
                raise Exception

            # click library menu button
            if not self.exist_click(L.media_room.library_menu.btn_menu):
                logger('Fail to click library menu button')
                raise Exception
            type2 = f'{strType} Transition'
            logger(type2)
            if not self.select_right_click_menu('Apply Fading Transition to All Videos', type2):
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def tap_TrainsitionRoom_LibraryMenu(self):
        try:
            # click library menu button
            if not self.exist_click(L.media_room.library_menu.btn_menu):
                logger('Fail to click library menu button')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def sort_by_name(self):
        try:
            if not self.exist_click(L.media_room.library_menu.btn_menu):
                raise Exception

            if not self.select_right_click_menu('Sort By', 'Name'):
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def sort_by_type(self):
        try:
            if not self.exist_click(L.media_room.library_menu.btn_menu):
                raise Exception

            if not self.select_right_click_menu('Sort By', 'Type'):
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_LibraryMenu_ExtraLargeIcons(self):
        try:
            if not self.exist_click(L.media_room.library_menu.btn_menu):
                raise Exception
            if not self.select_right_click_menu('Extra Large Icons'):
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_LibraryMenu_LargeIcons(self):
        try:
            if not self.exist_click(L.media_room.library_menu.btn_menu):
                raise Exception
            if not self.select_right_click_menu('Large Icons'):
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_LibraryMenu_MediumIcons(self):
        try:
            if not self.exist_click(L.media_room.library_menu.btn_menu):
                raise Exception
            if not self.select_right_click_menu('Medium Icons'):
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_LibraryMenu_SmallIcons(self):
        try:
            if not self.exist_click(L.media_room.library_menu.btn_menu):
                raise Exception
            if not self.select_right_click_menu('Small Icons'):
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_ExplorerView(self):
        try:
            # Verify Step1:
            # Check (Geometric) tag is find or not
            if not self.exist(L.transition_room.explore_view_region.Geometric_category):
                before_status = False
            else:
                before_status = self.exist(L.transition_room.explore_view_region.Geometric_category).AXValue.startswith("Geometric")
            #logger(f'Initial: Display status {before_status}')

            if not self.exist_click(L.transition_room.btn_explore_view):
                logger('Cannot find btn_explore_view')
                raise Exception
            time.sleep(DELAY_TIME)

            # Verify Step2:
            # Check (Geometric) tag again
            if not self.exist(L.transition_room.explore_view_region.Geometric_category):
                after_status = False
            else:
                after_status = self.exist(L.transition_room.explore_view_region.Geometric_category).AXValue.startswith("Geometric")
            #logger(f'Now: Display status {after_status}')

            # Verify Step3:
            if before_status == after_status:
                logger('Verify FAIL')
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True