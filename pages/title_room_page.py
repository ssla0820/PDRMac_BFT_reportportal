import time, datetime, os, copy

from .base_page import BasePage
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
# from AppKit import NSScreen
from .locator import locator as L
from .main_page import Main_Page

DELAY_TIME = 1 # sec

class Title_room(Main_Page, BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def find_specific_tag(self, name):
        tags = self.exist(L.base.tag_list)
        for tag in tags:
            if tag.AXValue.startswith(f"{name} ("):
                return True
        return False

   # ==============      For scan IAD category (Start)        ==================
    def find_all_category(self):
        tags = self.exist(L.base.tag_list_2)
        # category naming + (Number)
        categorylist=[]

        # Only category naming / Remove (Number)
        skip_parentheses=[]

        for tags in tags:
            current_string = tags.AXValue
            categorylist.append(current_string)
        for x in range(len(categorylist)):
            index = categorylist[x].find('(')
            if index > 1:
                index = index - 1
                node = {'name': categorylist[x][0:index], 'sub_category': []}
                skip_parentheses.append(node)

        return skip_parentheses

    def find_subcategory_children_count(self):
        # Final Parent + All children list
        final_list = []
        # Only Parent node:
        parent_list = self.find_all_category()
        logger(len(parent_list))
        final_list = parent_list.copy()

        # Find sub-category index info (Need to click triangle item in later by this index list)
        show_index_list_default = self.find_all_triangle_index()
        logger(show_index_list_default)

        # Take triangle index to click (Unfold) category
        # Unfold category => Current Node
        # Print all sub-category of (Current Node) then fold category
        for x in range(len(show_index_list_default)):
            # If (Current Node) is in lower position, should scroll down
            if show_index_list_default[x] > 15:
                self.exist(L.intro_video_room.category_scroll_bar).AXValue = 1

            # Unfold (Current Node)
            elem = self.exist(L.base.disclosure_triangle)
            self.mouse.click(*elem[x].center)
            target_pos = self.get_mouse_pos()
            time.sleep(DELAY_TIME*2)

            # Parent & Current node's children
            current_category_list = self.find_all_category()
            current_child_count = len(current_category_list) - len(parent_list)
            logger(f'Current child count = {current_child_count}')

            # Point inner loop
            current_access = show_index_list_default[x] + 1
            child_list = []
            for y in range(current_child_count):
                index = current_access + y
                logger(current_category_list[index])
                child_list.append(current_category_list[index])
            logger(child_list)

            # Fold
            self.mouse.click(target_pos)
            time.sleep(DELAY_TIME*2)
            # final_list.insert(show_index_list_default[x] + x + 1, child_list)
            final_list[show_index_list_default[x]]['sub_category'] = child_list
        logger("-----")
        logger(final_list)

    def find_all_triangle_index(self):
        # Find first category Y position
        first_category_y = self.exist(L.base.tag_outline_area).AXPosition[1]
        logger(first_category_y)

        # Find all triangle items
        elem = self.exist(L.base.disclosure_triangle)
        #logger(len(elem))

        # h size
        h = self.exist(L.base.uni_outline_row).AXSize[1]
        logger(h)

        # Save all index which has sub-category
        index_list = []
        for x in range(len(elem)):
            # Find and Calculate each triangle "Y position"
            index = (elem[x].AXPosition[1] - first_category_y) / h
            current_index = int(index)
            index_list.append(current_index)
        return index_list

    # ==============      For scan IAD category (End)        ==================

    def check_in_title_room(self):
        if not self.exist_click(L.title_room.btn_import_media):
            logger('Cannot find btn_import_media')
            raise Exception('Cannot find btn_import_media')
        time.sleep(DELAY_TIME * 1)
        if not self.exist(L.title_room.btn_import_title_templates):
            self.mouse.click(btn="right")
            logger('not enter Title Room now')
            return False
        else:
            self.mouse.click(btn="right")
            return True

    def check_enter_title_designer(self):
        # if return True, enter Title Designer now
        # if return False, not find Title Designer Window
        return self.exist(L.title_room.main_window).AXTitle.startswith("Title Designer |")

    def click_CreateNewTitle_btn(self):
        try:
            if not self.exist_click(L.title_room.btn_create_new_2d_title):
                logger('Fail to find btn_create_new_2d_title')
                raise Exception

            # Verify Step
            if not self.check_enter_title_designer():
                return False

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_ModifySelectedTitle_btn(self):
        try:
            if not self.exist_click(L.title_room.btn_modify_selected_title_template):
                logger('Fail to find btn_modify_selected_title_template')
                raise Exception

            # Verify Step
            if not self.check_enter_title_designer():
                return False

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def add_titleroom_new_tag(self, name):
        try:
            if not self.exist(L.title_room.explore_view_region.Motion_Graphics_category):
                logger('Now is not in title Room')
                raise Exception

            # check current tags number
            if not self.exist(L.title_room.explore_view_region.table_all_content_tags):
                logger('Fail to find table_all_content_tags')
                raise Exception

            tags_table = self.exist(L.title_room.explore_view_region.table_all_content_tags).AXChildren
            before_add_tags_num = len(tags_table)
            #logger(before_add_tags_num)

            # click (Add new tag)
            if not self.exist_click(L.title_room.btn_add_new_tag):
                logger('Fail to find btn_add_new_tag')
                raise Exception
            time.sleep(DELAY_TIME*2)
            self.keyboard.send(name)
            time.sleep(DELAY_TIME)
            self.keyboard.enter()

            if self.exist(L.title_room.warning_dialog.msg1):
                logger('add new tag [FAIL] - duplicate tag name')
                self.exist_click(L.title_room.warning_dialog.ok)
                return False

            tags_table = self.exist(L.title_room.explore_view_region.table_all_content_tags).AXChildren
            after_add_tags_num = len(tags_table)
            #logger(after_add_tags_num)

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
            if not self.exist(L.title_room.explore_view_region.Motion_Graphics_category):
                logger('Now is not in title Room')
                raise Exception

            # check current tags number
            if not self.exist(L.title_room.explore_view_region.table_all_content_tags):
                logger('Fail to find table_all_content_tags')
                raise Exception

            tags_table = self.exist(L.title_room.explore_view_region.table_all_content_tags).AXChildren
            current_tags_counts = len(tags_table)
            #logger(current_tags_counts)

            if not self.select_specific_tag(name):
                logger('Cannot find the tag')
                raise Exception("Cannot find the tag")
            if not self.exist_click(L.title_room.btn_delete_tag):
                logger('Cannot find btn_delete_tag')
                raise Exception

            if self.exist(L.title_room.warning_dialog.msg2):
                time.sleep(DELAY_TIME)
                self.exist_click(L.title_room.warning_dialog.ok)

            time.sleep(DELAY_TIME)
            tags_table = self.exist(L.title_room.explore_view_region.table_all_content_tags).AXChildren
            after_tags_counts = len(tags_table)
            #logger(after_tags_counts)

            # Verify Step
            if after_tags_counts != current_tags_counts - 1:
                logger('Fail to delete tag, count error after added.')
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_RightClickMenu_AddToTimeline(self):
        try:
            self.right_click()
            time.sleep(DELAY_TIME)
            if not self.select_right_click_menu('Add to Timeline'):
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_RightClickMenu_ChangeAlias(self, name):
        try:
            self.right_click()
            time.sleep(DELAY_TIME)
            if not self.select_right_click_menu('Change Alias'):
                raise Exception
            time.sleep(DELAY_TIME*2)
            if name == "":
                self.keyboard.press(self.keyboard.key.backspace)
                self.keyboard.enter()
            else:
                self.keyboard.send(name)
                time.sleep(DELAY_TIME)
                self.keyboard.enter()

                # Verify Step
                if not self.find({'AXValue': name, 'AXRole': 'AXTextField'}):
                    logger('Change Alias [FAIL]')
                    raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_RightClickMenu_ModifyTemplate(self):
        try:
            self.right_click()
            time.sleep(DELAY_TIME*2)
            if not self.select_right_click_menu('Modify Template'):
                raise Exception
            time.sleep(DELAY_TIME*2)

            # Verify Step
            if not self.check_enter_title_designer():
                logger('Not enter Title Designer')
                return False

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_RightClickMenu_Delete(self):
        try:
            self.right_click()
            time.sleep(DELAY_TIME*2)
            if not self.select_right_click_menu('Delete (only for Custom/Downloaded)'):
                raise Exception
            time.sleep(DELAY_TIME*2)

            if self.exist(L.title_room.warning_dialog.msg3):
                time.sleep(DELAY_TIME)

            # Verify Step
            if not self.exist_click(L.title_room.warning_dialog.yes):
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_RightClickMenu_Addto(self, name):
        try:
            self.right_click()
            time.sleep(DELAY_TIME)
            if not self.select_right_click_menu('Add to', name):
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_RightClickMenu_ShareUploadToInternet(self, close_win=True):
        try:
            self.right_click()
            time.sleep(DELAY_TIME*2)
            if not self.select_right_click_menu('Share and Upload to the Internet...'):
                raise Exception

            time.sleep(DELAY_TIME*2)
            if self.exist(L.title_room.cyberlink_power_director.msg):
                self.exist_click(L.title_room.cyberlink_power_director.yes)

            time.sleep(DELAY_TIME*5)
            if not self.exist(L.title_room.upload_dialog.step1):
                raise Exception

            if close_win:
                self.exist_click(L.title_room.upload_dialog.btn_close)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_ExplorerView(self):
        try:
            # Verify Step1:
            # Check (Motion Graphics) tag is find or not
            if not self.exist(L.title_room.explore_view_region.Motion_Graphics_category):
                before_status = False
            else:
                before_status = self.exist(L.title_room.explore_view_region.Motion_Graphics_category).AXValue.startswith("Motion Graphics")
            #logger(f'Initial: Display status {before_status}')

            if not self.exist_click(L.title_room.btn_explore_view):
                logger('Cannot find btn_explore_view')
                raise Exception

            # Verify Step2:
            # Check (Motion Graphics) tag again
            if not self.exist(L.title_room.explore_view_region.Motion_Graphics_category):
                after_status = False
            else:
                after_status = self.exist(L.title_room.explore_view_region.Motion_Graphics_category).AXValue.startswith("Motion Graphics")
            #logger(f'Now: Display status {after_status}')

            # Verify Step3:
            if before_status == after_status:
                logger('Verify FAIL')
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_ImportTitleTemplates(self, full_path):
        try:
            if not self.exist_click(L.title_room.btn_import_media):
                logger('Cannot find btn_import_media')
                raise Exception('Cannot find btn_import_media')
            time.sleep(DELAY_TIME*2)
            if not self.exist_click(L.title_room.btn_import_title_templates):
                logger('Cannot find btn_import_title_templates')
                raise Exception('Cannot find btn_import_title_templates')
            time.sleep(DELAY_TIME*2)
            if not self.select_file(full_path):
                raise Exception('Cannot select file w/ full_path')

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_DownloadContent_from_DZCL(self):
        try:
            if not self.exist_click(L.title_room.btn_import_media):
                raise Exception
            time.sleep(DELAY_TIME*2)

            if not self.exist(L.title_room.btn_import_title_templates):
                logger('not in Title Room')
                raise Exception

            if not self.exist_click(L.title_room.btn_download_from_DZ_cloud):
                raise Exception
            time.sleep(DELAY_TIME*2)

            # Verify Step
            if not self.exist(L.title_room.download_dialog.main):
                raise Exception
            # For v2922 workaround .. skip this check (exception -25200)
            #if not self.exist(L.title_room.download_dialog.str_Title):
            #    raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def download_content_from_cloud(self, name, close_win=True):
        try:
            # before_snapshot
            old_img = self.snapshot(self.area.library)

            # click (Download Content from DirectorZone/Cloud)
            if not self.click_DownloadContent_from_DZCL():
                raise Exception

            # if not enter (Cyberlink Cloud) page, raise Exception
            item = self.exist(L.title_room.download_dialog.cloud_tab)
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
            if not self.exist_click(L.title_room.download_dialog.btn_download):
                raise Exception
            else:
                logger('click download')
            time.sleep(DELAY_TIME*3)

            # Verify Step:
            # For v2922 workaround .. skip this check (exception -25200)
            #if self.exist_click(L.title_room.warning_dialog.msg4):
            #    time.sleep(DELAY_TIME)
            #    self.exist_click(L.title_room.warning_dialog.ok)

            if close_win:
                self.exist_click(L.title_room.download_dialog.btn_close)
                time.sleep(DELAY_TIME)

            # after_snapshot
            self.mouse.move(0, 0)
            new_img = self.snapshot(self.area.library)
            # if old_image == new_ image, library content does not change
            # check main window has been changed (Title Room switch to download category & show content)
            if self.compare(old_img, new_img, similarity=0.99):
                return False

            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def check_is_in_Downloaded_category(self, name):
        try:
            if not self.select_specific_tag('Downloaded'):
                raise Exception

            # select custom template w/ name
            if not self.find({'AXValue': f'{name}', 'AXRole': 'AXStaticText'}):
                return False

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def delete_in_Download_cateogry(self, temp_name):
        try:
            if not self.select_specific_tag('Downloaded'):
                raise Exception

            time.sleep(DELAY_TIME)
            # select template w/ temp_name
            self.mouse.click(*self.find({'AXValue': f'{temp_name}', 'AXRole': 'AXStaticText'}).center)
            time.sleep(DELAY_TIME)
            self.select_RightClickMenu_Delete()

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def delete_in_Custom_category(self, temp_name):
        try:
            if not self.select_specific_tag('Custom'):
                raise Exception

            time.sleep(DELAY_TIME)
            # select template w/ temp_name
            self.hover_library_media(f'{temp_name}')
            time.sleep(DELAY_TIME*2)
            self.select_RightClickMenu_Delete()

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def sort_by_name(self):
        try:
            if not self.exist_click(L.media_room.library_menu.btn_menu):
                raise Exception

            if not self.select_right_click_menu('Sort by', 'Name'):
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def sort_by_category(self):
        try:
            if not self.exist_click(L.media_room.library_menu.btn_menu):
                raise Exception

            if not self.select_right_click_menu('Sort by', 'Category'):
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def sort_by_createdate(self):
        try:
            if not self.exist_click(L.media_room.library_menu.btn_menu):
                raise Exception

            if not self.select_right_click_menu('Sort by', 'Created Date'):
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

    def click_upload_to_DZ_cloud(self, close_win=False):
        try:
            if not self.exist_click(L.title_room.btn_upload_to_DZ_cloud):
                raise Exception

            time.sleep(DELAY_TIME*2)
            if self.exist(L.title_room.cyberlink_power_director.msg):
                self.exist_click(L.title_room.cyberlink_power_director.yes)

            time.sleep(DELAY_TIME*5)
            if not self.exist(L.title_room.upload_dialog.step1):
                raise Exception

            if close_win:
                self.exist_click(L.title_room.upload_dialog.btn_close)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def search_Title_room_library(self, name=None):
        try:
            if not name:
                raise Exception
            time.sleep(DELAY_TIME)

            # if library field has content, should clear all
            self.exist_click(L.title_room.btn_search_cancel)

            img_collection_view_before = self.snapshot(L.media_room.library_listview.main_frame)
            self.exist_click(L.title_room.input_search)
            self.keyboard.send(name)
            time.sleep(DELAY_TIME)
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

    def search_Title_room_click_cancel(self):
        try:
            if not self.exist_click(L.title_room.btn_search_cancel):
                logger('Fail to click search cancel button')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_TitleRoom_Scroll_Bar(self, value):
        try:
            self.exist(L.title_room.scroll_bar.scroll_elem).AXValue = float(value)
            time.sleep(DELAY_TIME)
            # Verify Step
            if float(value) == self.exist(L.title_room.scroll_bar.scroll_elem).AXValue:
                return True
            else:
                return False
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_freeTemplate(self):
        try:
            # Select (All Content) category
            self.select_specific_tag('All Content')
            time.sleep(DELAY_TIME)

            # select (Free Templates)
            self.exist_click(L.title_room.library_free_template).center
            if not self.find(L.title_room.library_free_template):
                raise Exception

            # Verify Step: (Check DirectorZone website already open) then (close chrome page of DirectorZone)
            check_title = self.check_chrome_page()
            logger(check_title)
            if check_title != 'Free Video Effects, Photo Frames & Tutorials | DirectorZone - Google Chrome':
                logger(f'Verify Step: check open browse [FAIL]')
                return False
            else:
                self.close_chrome_page()
                time.sleep(DELAY_TIME)
                self.activate()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def check_chrome_page(self):
        try:
            chrome = self.driver.get_top("com.google.Chrome")
            #logger(chrome)
            for x in range(10):
                time.sleep(DELAY_TIME)
                if x == 9:
                    logger('Timeout to get Chrome title')
                    raise Exception

                title = chrome.windows()[0].AXTitle
                if title == 'Untitled - Google Chrome':
                    continue
                elif title:
                    logger(title)
                    break
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return title

    def close_chrome_page(self):
        try:
            logger('enter close_chrome_page')
            self.driver.get_top("com.google.Chrome").windows()[0].findAllR(AXTitle="Close", AXRole="AXButton")[-1].press()
            time.sleep(DELAY_TIME*2)
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

            if not self.exist(L.title_room.warning_dialog.msg2):
                raise Exception

            # Verify Step
            if not self.exist_click(L.title_room.warning_dialog.ok):
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

    def get_status_rightclickmenu_RenameTag(self):
        try:
            if not self.exist(L.title_room.right_click_menu.rename_Tag):
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return self.exist(L.title_room.right_click_menu.rename_Tag).AXEnabled