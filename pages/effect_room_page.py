import time, datetime, os, copy

from .base_page import BasePage
from .bft_Main_Page import Main_Page
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
# from AppKit import NSScreen
from .locator import locator as L
from .main_page import Main_Page
#from .locator.hardcode_0408 import locator as L
from reportportal_client import step

DELAY_TIME = 1 # sec

class Effect_Room(Main_Page, BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def find_specific_tag_after_added(self, name):
        tags = self.exist(L.base.tag_list)
        for tag in tags:
            if tag.AXValue.startswith(f"{name} (1"):
                return True
        return False

    def find_specific_tag_delete(self, name):
        tags = self.exist(L.base.tag_list)
        for tag in tags:
            if tag.AXValue.startswith(f"{name} ("):
                return True
        return False

    def find_specific_tag(self, name):
        tags = self.exist(L.effect_room.effect_room_tag_list)
        for tag in tags:
            if tag.AXValue.startswith(f"{name} ("):
                return True
        return False

    @step('[Action][Effect Room] Find the specific tag and return tag object')
    def find_specific_tag_return_tag(self, name):
        tags = self.exist(L.effect_room.effect_room_tag_list)
        for tag in tags:
            if tag.AXValue.startswith(f"{name} ("):
                return tag
        return False

    def check_effect_room(self):
        try:
            if not self.exist(L.effect_room.style_effect_tag):
                raise Exception
        except Exception as e:
            logger("Didn't stay in effect room currently")
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


    @step('[Action][Effect Room] Import [CLUTs] with file path')
    def import_CLUTs(self, full_path):
        try:
            self.exist_click(L.effect_room.clut_effect_tag).AXValue
            current_amount = self.snapshot(L.effect_room.library)
            #logger(current_clut_amount)
            if not self.exist_click(L.effect_room.import_media.import_media):
                logger("Can't find the import button")
                raise Exception("Can't find the import button")
            if not self.exist_click(L.effect_room.import_media.import_media_clut):
                logger("Can't find the import CLUTs button")
                raise Exception("Can't find the import CLUTs button")
            if not self.select_file(full_path):
                logger("Can't select the CLUTs file")
                raise Exception("Can't select the CLUTs file")

            #after_clut_amount = self.exist(L.effect_room.clut_effect_tag).AXValue
            #logger(after_clut_amount)

            #Verify if the CLUT file is imported
            #if current_clut_amount == after_clut_amount:
                #logger("Import failed")
                #raise Exception
            start_time = time.time()
            time.sleep(6)
            after_amount = self.snapshot(L.effect_room.library)
            print(f'{current_amount=}, {after_amount=}')
            result_verify = self.compare(current_amount, after_amount, similarity=1)
            if result_verify:
                 logger('Fail to import the clut file.')
                 raise Exception('Fail to import the clut file.')
                #el_count_after = len(tag_elements)
                #if after_clut_amount != current_clut_amount:
                #break

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def displayhideexplorerview(self):
        try:
             if not self.exist_click(L.effect_room.btn_hide_explorer):
               logger("Can't find the hide explorer btn")
               raise Exception
             #if self.exist(L.effect_room.style_effect_tag):
               #logger("Didn't hide the explorer")
               #raise Exception
             #time.sleep(DELAY_TIME*2)
             #if not self.exist_click(L.effect_room.btn_display_explorer):
               #logger("Can't find the display explorer btn")
               #raise Exception
             #if not self.exist(L.effect_room.style_effect_tag):
               #logger("Didn't display the explorer")
        except Exception as e:
               logger(f'Exception occurs. log={e}')
               raise Exception
        return True

    def search_and_input_text(self, str_name):
        try:
            if not self.exist_click(L.effect_room.search.search_field):
                logger("Can't find the search field")
                raise Exception
            #input str
            self.keyboard.send(str_name)
            self.press_enter_key()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def cancel_input_text(self):
        try:
            if not self.exist_click(L.effect_room.search.search_field):
                logger("Can't find the search field")
                raise Exception
            if not self.exist(L.effect_room.search.search_cancel):
                logger("Didn't input the words in search field")
                raise Exception
            if not self.exist_click(L.effect_room.search.search_cancel):
                logger("Can't click the cancel button in search field")
                raise Exception
            if self.exist(L.effect_room.search.search_cancel):
                logger("Didn't cancel the input text completely")
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True
    def add_effectroom_new_tag(self, name):
        try:
            # check current tags number
            if not self.exist(L.effect_room.current_tag_amount):
                logger('Fail to find table_all_content_tags')
                raise Exception

            tags_table = self.exist(L.effect_room.current_tag_amount).AXChildren
            before_add_tags_num = len(tags_table)
            logger(before_add_tags_num)

            # click (Add new tag)
            if not self.exist_click(L.effect_room.tag.add_tag):
                logger('Fail to find btn_add_new_tag')
                raise Exception
            time.sleep(DELAY_TIME*2)
            self.keyboard.send(name)
            time.sleep(DELAY_TIME)
            self.keyboard.enter()

            if self.exist(L.effect_room.tag.duplicate_tag_msg):
                logger('add new tag [FAIL] - duplicate tag name')
                self.exist_click(L.effect_room.tag.duplicate_tag_msg_ok)
                return False

            tags_table = self.exist(L.effect_room.current_tag_amount).AXChildren
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

    def drag_EffectRoom_Scroll_Bar(self, value):
        try:
            self.exist(L.effect_room.scroll_bar.scroll_bar).AXValue = float(value)
            time.sleep(DELAY_TIME)
            # Verify Step
            if float(value) == self.exist(L.effect_room.scroll_bar.scroll_bar).AXValue:
                return True
            else:
                return False
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def right_click_addto_timeline(self, effect_name):
        """
        e.g. effect_name = {'AXIdentifier': 'CollectionViewItemTextField', 'AXValue': 'Aberration'}
        """
        try:
            if not self.exist_click({'AXIdentifier': 'CollectionViewItemTextField', 'AXValue': effect_name}):
                logger("Can't click the effect")
                raise Exception
            time.sleep(DELAY_TIME)
            self.right_click()
            time.sleep(DELAY_TIME)
            if not self.select_right_click_menu('Add to Timeline'):
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True



    def right_click_addto(self, name):
        try:
            self.right_click()
            #time.sleep(DELAY_TIME * 3)
            #if not self.select_right_click_menu('Add to', name):
            #    raise Exception
            #time.sleep(DELAY_TIME * 2)
            self.select_right_click_menu('Add to', name)
            #time.sleep(2)
            #self.exist_click({'AXRole': 'AXMenuItem', 'AXTitle': name})

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_deleted_tag(self, name):
        tags = self.exist(L.effect_room.effect_room_tag_list)
        for tag in tags:
            if tag.AXValue.startswith(f"{name} ("):
                self.mouse.click(*tag.center)
                return True

    def delete_tag(self, name):
        logger(f'effect room - delete tag {name} ')

        try:
            # check current tags number
            if not self.exist(L.effect_room.current_tag_amount):
                logger('Fail to find table_all_content_tags')
                raise Exception

            tags_table = self.exist(L.effect_room.current_tag_amount).AXChildren
            current_tags_counts = len(tags_table)
            logger(current_tags_counts)

            if not self.select_deleted_tag(name):
                logger('Cannot select the specific tag')
                raise Exception ('Cannot find the specific tag')


            if not self.exist_click(L.effect_room.tag.delete_tag.delete_tag):
                logger('Cannot find btn_delete_tag')
                raise Exception

            if self.exist(L.effect_room.tag.delete_tag.delete_tag_msg):
                time.sleep(DELAY_TIME)
                self.exist_click(L.effect_room.tag.delete_tag.delete_tag_ok)

            time.sleep(DELAY_TIME)
            tags_table = self.exist(L.effect_room.current_tag_amount).AXChildren
            after_tags_counts = len(tags_table)
            logger(after_tags_counts)

            # Verify Step
            if after_tags_counts != current_tags_counts - 1:
                logger('Fail to add tag, count error after added.')
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def remove_from_favorites(self):
        try:
            self.right_click()

            if not self.select_right_click_menu('Remove from My Favorites'):
                logger("Can't remove from my favorites")
                raise Exception
            time.sleep(DELAY_TIME)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def right_click_remove_clut(self):
        try:
            self.right_click()
            if not self.select_right_click_menu('Delete'):
                logger("Can't found delete button")
                raise Exception
            time.sleep(DELAY_TIME)

            if not self.exist(L.effect_room.effect_room_rightclick_delete_clut.delete):
                logger("No delete msg pop up")
                raise Exception

            if not self.exist_click(L.effect_room.effect_room_rightclick_delete_clut.delete_yes):
                logger("Can't click Yes in delete dialog")
                raise Exception
            time.sleep(DELAY_TIME)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def apply_effect_to_effecttrack(self, effect_name):
        '''
        effect_temp (Aberration) = {'AXIdentifier': 'CollectionViewItemTextField', 'AXValue': 'Aberration'}
        '''
        try:
            if not self.exist_click({'AXIdentifier': 'CollectionViewItemTextField', 'AXValue': effect_name}):
                logger("Can't click the target effect")
                raise Exception
            time.sleep(DELAY_TIME)

            if not self.exist_click(L.effect_room.add_to_effect_track):
                logger("Can't add to effect track")
                raise Exception
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def remove_from_custom_tag(self, tag_index, effect_name):
        try:
            if not self.exist_click([{'AXIdentifier': 'IDC_LIBRARY_ROOM_TAG_SCROLLVIEW'}, {'AXIdentifier': 'IDC_LIBRARY_ROOM_TAG_OUTLINEVIEW'}, {'AXRole': 'AXRow', 'index': tag_index}]):
                logger("Can't find the target tag")
                raise Exception
            self.exist_click({'AXIdentifier': 'CollectionViewItemTextField', 'AXValue': effect_name})
            self.right_click()
            self.select_right_click_menu('Remove from Custom Tag')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def right_click_rename_tag(self, tag_index, name):
        try:
            if not self.exist_click([{'AXIdentifier': 'IDD_LIBRARY'}, {'AXIdentifier': 'IDC_LIBRARY_ROOM_TAG_OUTLINEVIEW'}, {'AXRole': 'AXRow', 'index': tag_index}]):
                logger("Can't find the target tag")
                raise Exception
            self.right_click()
            self.select_right_click_menu('Rename Tag')
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(name)
            self.exist_click([{'AXIdentifier': 'IDD_LIBRARY'}, {'AXIdentifier': 'IDC_LIBRARY_ROOM_TAG_OUTLINEVIEW'}, {'AXRole': 'AXRow', 'index': 0}])
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def right_click_delete_tag(self, tag_index):
        try:
            if not self.exist_click([{'AXIdentifier': 'IDD_LIBRARY'}, {'AXIdentifier': 'IDC_LIBRARY_ROOM_TAG_OUTLINEVIEW'}, {'AXRole': 'AXRow', 'index': tag_index}]):
                logger("Can't find the target tag")
                raise Exception
            self.right_click()
            self.select_right_click_menu('Delete Tag')
            self.exist_click({'AXRole': 'AXButton', 'AXTitle': 'OK'})
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def right_click_add_to_my_favorites(self):
        try:
            current_favorites = self.exist([{'AXIdentifier': 'IDD_LIBRARY'}, {'AXIdentifier': 'IDC_LIBRARY_ROOM_TAG_OUTLINEVIEW'}, {'AXRole': 'AXRow', 'index': 0}, {'AXIdentifier': 'RoomTagOutlineViewTextField'}]).AXValue
            self.right_click()
            self.select_right_click_menu('Add to', 'My Favorites')
            time.sleep(DELAY_TIME)
            after_favorites = self.exist([{'AXIdentifier': 'IDD_LIBRARY'}, {'AXIdentifier': 'IDC_LIBRARY_ROOM_TAG_OUTLINEVIEW'}, {'AXRole': 'AXRow', 'index': 0}, {'AXIdentifier': 'RoomTagOutlineViewTextField'}]).AXValue
            if current_favorites == after_favorites:
                logger("Fail to add to [My Favorites]")
                raise Exception
            else:
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Effect Room] Remove from [Effect Settings]')
    def remove_from_effectsettings(self):
        return self.exist_click(L.effect_room.remove_effect_setting)

    def click_keyframe_btn(self):
        return self.exist_click(L.effect_room.btn_keyframe)

    def apply_effect_to_video(self, effect_name, track_index, clip_index):
        try:
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]):
                logger("No target clip on the track")
                raise Exception
            x, y = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]).AXPosition
            self.select_library_icon_view_media(effect_name)
            self.hover_library_media(effect_name)
            x1, y1 = self.mouse.position()
            self.mouse.drag((x1, y1), (int(x + 10), int(y + 10)))
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    # def apply_effect_to_videotrack(self, track_no, clip_index, effect_temp):
    #     try:
    #
    #         if not self.exist(effect_temp):
    #             logger("Can't find the target effect")
    #             raise Exception
    #         time.sleep(DELAY_TIME)
    #
    #         if self.exist_click(L.effect_room.selected_video_track).AXValue == float(track_no):
    #             logger("Can't find the target track")
    #             raise Exception
    #         time.sleep(DELAY_TIME)
    #
    #         if not self.drag_effect_to_timeline(effect_temp):
    #             logger("Can't drag to timeline")
    #             raise Exception
    #         time.sleep(DELAY_TIME)
    #
    #         if not self.exist(L.effect_room.selected_video_clip).AXIndex == float(clip_index):
    #             logger("Can't found a target clip")
    #             raise Exception
    #         time.sleep(DELAY_TIME)
    #
    #
    #         if not self.select_right_click_menu(L.effect_room.effect_room_add_to.add_to_timeline):
    #             logger("Can't add to timeline")
    #             raise Exception
    #         time.sleep(DELAY_TIME)
    #
    #         if self.exist(L.effect_room.effect_overwrite):
    #             logger("effect already apply on the target clip")
    #             self.exist_click(L.effect_room.effect_overwrite)
    #         time.sleep(DELAY_TIME)
    #
    #     except Exception as e:
    #         logger(f'Exception occurs. log={e}')
    #         raise Exception
    #     return True




































