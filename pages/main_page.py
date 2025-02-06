import time, datetime, os, copy
from reportportal_client import step

from .base_page import BasePage
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
from .locator import locator as L

OPERATION_DELAY = 1 # sec

class Main_Page(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start_app(self):
        try:
            self.launch_app(30)
            print('launch app ok')
            timeout = 30
            start_time = time.time()
            is_launch_ok = 0
            while time.time() - start_time < timeout:
                self.refresh_top()
                time.sleep(OPERATION_DELAY*2)
                self.click_CEIP_dialog()
                self.exist_click(L.main.activate_dialog.btn_activate, None, btn="left", timeout=3, no_warning=True)
                self.click_new_project_on_launcher()
                self.refresh_top()
                if self.is_exist(L.media_room.btn_import_media, None, 2):
                    is_launch_ok = 1

                    if self.exist(L.base.seasonal_bb_window.main, timeout=7):
                        # Close seasonal BB dialog
                        self.press_esc_key()
                        time.sleep(1)

                    if self.exist(L.media_room.string_use_sample_media, timeout=7):
                        self.click(L.media_room.string_use_sample_media)
                        time.sleep(OPERATION_DELAY * 4)
                    else:
                        logger('cannot find use sample media')

                    break
            if is_launch_ok == 0:
                raise Exception("Fail to launch app to main page")
        except Exception as e:
            raise Exception(f"Exception occurs. log={e}")
        return True

    step('[Action][Main_page] click Launch Free version button on Ess dialog')
    def launch_free_version(self):
        try:
            check_free_version = False
            for _ in range(10):
                # Click [Launch Free Version]
                free_version_link = self.exist({'AXTitle': 'LAUNCH FREE VERSION', 'AXRole': 'AXLink'})
                free_version_btn = self.exist({'AXTitle': 'Launch Free Version', 'AXRole': 'AXButton'})
                logger(f'{free_version_link=}, {free_version_btn=}')
                time.sleep(OPERATION_DELAY*3) # wait for the dialog is ready to click
                
                if free_version_link:
                    self.mouse.click(*free_version_link.center)
                    check_free_version = True
                    break
                elif free_version_btn:
                    self.mouse.click(*free_version_btn.center)
                    check_free_version = True
                    break
                    
        except Exception as e:
            raise Exception(f'Exception occurs. log={e}')
        return check_free_version


    def insert_media(self, name, aspect_ratio_conflict_option=None): # aspect_ratio_conflict_option - 'yes', 'no'
        self.activate()
        self.hover_library_media(name)
        self.right_click()
        self.select_right_click_menu("Insert on Selected Track")
        # handle aspect ratio conflict dialog
        if aspect_ratio_conflict_option:
            time.sleep(OPERATION_DELAY)
            self.handle_aspect_ratio_conflict(aspect_ratio_conflict_option)
        locator = L.main.timeline.clip_name_unit
        locator[1]['AXValue'] = name[:name.rfind(".")]
        if not self.find(locator):
            raise Exception(f"Insert media fail. {locator=}")
        return True

    def tap_TipsArea_Tools_menu(self, index):
        self.activate()
        tool = self.exist(L.main.tips_area.btn_tools)
        tool.press()
        time.sleep(3)
        if isinstance(index,int):
            tool.findAllR(AXRole="AXMenuItem")[index].press()
        elif isinstance(index,str):
            tool.findAllR(AXTitle=index)[0].press()
        else:
            raise Exception(f"type error: parameter must be int or str, not >>{type(index)}<<")
        return True

    @step('[Action][Main_page] Insert media to selected track')
    def tips_area_insert_media_to_selected_track(self, option=-1): # option: -1-None, 0-Overwrite, 1-Insert,
        # 2-insert_and_move_all_clips, 3-CrossFade, 4-Replace, 5-Trim_to_Fit, 6-Speed_up_to_Fit
        try:
            el_option = ['Overwrite', 'Insert', 'Move', 'Crossfade', 'Replace', 'Trim', 'Speed']
            self.exist_click(L.main.tips_area.btn_insert_to_selected_track)
            time.sleep(OPERATION_DELAY * 2)
            if not option == -1:
                # click by OCR
                menu_item1_pos = self.search_text_position(el_option[option], mouse_move=0, order=1)
                print(f'{menu_item1_pos=}')
                if menu_item1_pos is not False:
                    self.mouse.click(*menu_item1_pos)
                else:
                    logger('Fail to get the position of target')
                    raise Exception('Fail to get the position of target')
            if self.is_exist(L.main.tips_area.btn_insert_to_selected_track, None, 2):
                logger('Fail to add media to selected track')
                raise Exception('Fail to add media to selected track')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def timeline_trim_enlarge_drag_clip_edge_menu(self, option=1): # option: -1-None, 0-Overwrite,
        # 1-Trim and Move Clips, 2-Trim and Move All Clips
        try:
            el_option = ['Overwrite', 'Trim', 'All']
            if not option == -1:
                # click by OCR
                menu_item1_pos = self.search_text_position(el_option[option], mouse_move=0, order=1)
                print(f'{menu_item1_pos=}')
                if menu_item1_pos is not False:
                    self.mouse.click(*menu_item1_pos)
                else:
                    logger('Fail to get the position of target')
                    raise Exception('Fail to get the position of target')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def timeline_clip_marker_track_menu_selected_clip(self, clip_locator, option=0): # option: -1-None, 0-Add Clip Marker, 1-Remove Selected Clip Marker,
        # 2-Remove All Clip Markers, 3-Edit Clip Marker, 4-Dock/Undock Timeline Window, 5-Reset All Undocked Windows
        try:
            el_option = ['Add', 'Selected', 'Markers', 'Edit', 'Dock/Undock', 'Reset']
            self.exist_click(clip_locator)
            time.sleep(OPERATION_DELAY * 2)
            clip_pos = self.exist(clip_locator).AXPosition
            self.mouse.move(int(clip_pos[0] + 15), int(695))
            self.right_click()
            if not option == -1:
                # click by OCR
                menu_item1_pos = self.search_text_position('Add', mouse_move=0, order=1)
                print(f'{menu_item1_pos=}')
                if menu_item1_pos is not False:
                    self.mouse.click(*menu_item1_pos)
                else:
                    logger('Fail to get the position of target')
                    raise Exception('Fail to get the position of target')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def timeline_clip_marker_track_menu_unselected_clip(self, option=0): # option: -1-None, 0-Add Clip Marker, 1-Remove Selected Clip Marker,
        # 2-Remove All Clip Markers, 3-Edit Clip Marker, 4-Dock/Undock Timeline Window, 5-Reset All Undocked Windows
        try:
            el_option = ['Add', 'Selected', 'Markers', 'Edit', 'Dock/Undock', 'Reset']
            if self.exist(L.timeline_operation.timeline_vertical_scroll_bar):
                self.exist(L.timeline_operation.timeline_vertical_scroll_bar).AXValue = float(0)
            self.exist_click(L.timeline_operation.timeline_video_track1)
            time.sleep(OPERATION_DELAY * 2)
            id_pos = self.exist(L.timeline_operation.timeline_video_track1).AXPosition
            self.mouse.move(int(id_pos[0] + 300), int(id_pos[1] - 27))
            self.right_click()
            if not option == -1:
                # click by OCR
                menu_item1_pos = self.search_text_position(el_option[option], mouse_move=0, order=1)
                print(f'{menu_item1_pos=}')
                if menu_item1_pos is not False:
                    self.mouse.click(*menu_item1_pos)
                else:
                    logger('Fail to get the position of target')
                    raise Exception('Fail to get the position of target')
            #if self.is_exist(L.timeline_operation.timeline_video_track1):
                #logger('Fail to call the menu on clip marker track')
                #raise Exception(f'Exception occurs. log={e}')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def timeline_overlay_media_menu(self, option=0):# option: -1-None, 0-Overwrite, 1-Insert,
        # 2-Insert and Move All Clips, 3-Crossfade, 4-Replace
        try:
            el_option = ['Overwrite', 'Insert', 'Move', 'Crossfade', 'Replace']
            if not option == -1 and not option == 1:
            # click by OCR
                menu_item1_pos = self.search_text_position(el_option[option], mouse_move=0)
                print(f'{menu_item1_pos=}')
                if menu_item1_pos is not False:
                    self.mouse.click(*menu_item1_pos)
                else:
                    logger('Fail to get the position of target')
                    raise Exception(f'Exception occurs. log={e}')
            if option == 1:
            # click by OCR
                overwrite_option_pos = self.search_text_position(el_option[0], mouse_move=0, order=1)
                print(f'{overwrite_option_pos=}')
                if overwrite_option_pos is not False:
                    self.mouse.move(overwrite_option_pos[0], overwrite_option_pos[1])
                    self.mouse.move(int(overwrite_option_pos[0]), int(overwrite_option_pos[1] + 20))
                    self.keyboard.enter()
                else:
                    logger('Fail to get the position of target')
                    raise Exception('Fail to get the position of target')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def tips_area_click_designer(self, check_designer=1):
        try:
            # 1: title, 2: particle
            if check_designer == 2:
                designer_elem = L.particle_designer.designer_window
            else:
                designer_elem = L.title_designer.main_window

            self.exist_click(L.main.tips_area.btn_designer)
            if not self.exist(designer_elem, OPERATION_DELAY*10):

                logger('Fail to click designer button')
                raise Exception('Fail to click designer button')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def tips_area_click_fix_enhance(self):
        try:
            img_before = self.snapshot(L.media_room.library_frame)
            self.exist_click(L.main.tips_area.btn_fix_enhance)
            self.exist_click(L.media_room.confirm_dialog.btn_ok) # handle the confirm dialog click OK
            self.wait_for_image_changes(img_before, L.media_room.library_frame, OPERATION_DELAY*10)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def tips_area_click_key_frame(self):
        try:
            img_before = self.snapshot(L.media_room.library_frame)
            self.exist_click(L.main.tips_area.btn_key_frame)
            self.wait_for_image_changes(img_before, L.media_room.library_frame, OPERATION_DELAY*10)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def tips_area_click_more_feature(self):
        try:
            img_before = self.screenshot()
            self.exist_click(L.main.tips_area.btn_more_feature)
            self.wait_for_image_changes(img_before, None, OPERATION_DELAY * 10)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def tips_area_click_split(self, compare_similarity=0.99):
        try:
            img_before = self.snapshot(L.main.timeline.table_view)
            self.exist_click(L.main.tips_area.btn_split)
            self.wait_for_image_changes(img_before, L.main.timeline.table_view, OPERATION_DELAY*5, compare_similarity)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            return False
        return True

    def set_time_code(self, el_locator, duration, is_verify=True):
        try:
            logger(f'set_time_code - Input {duration=}')
            list_duration = duration.split('_')
            duration_pos = self.exist(L.main.duration_setting_dialog.txt_duration).AXPosition
            duration_size = self.exist(L.main.duration_setting_dialog.txt_duration).AXSize
            self.mouse.click(int(duration_pos[0] + duration_size[0] / 8), int(duration_pos[1] + duration_size[1] / 2))
            time.sleep(OPERATION_DELAY * 0.5)
            for unit in list_duration:
                self.keyboard.send(unit)
                time.sleep(OPERATION_DELAY * 0.5)
            self.keyboard.enter()
            #time.sleep(OPERATION_DELAY * 0.5)
            #value = el_locator.AXValue
            #logger(f'Final {value=}')
            #if is_verify:
                #expect_value = f'{list_duration[0]};{list_duration[1]};{list_duration[2]};{list_duration[3]}'
                #if not value == expect_value:
                    #logger('Fail to verify input duration')
                    #raise Exception(f'Exception occurs. log={e}')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def tips_area_click_set_length_of_selected_clip(self, duration): # duration: in format 'HH_MM_SS_mm', e.g. 00_00_20_00
        try:
            img_before = self.snapshot(L.main.timeline.table_view)
            self.exist_click(L.main.tips_area.btn_set_length_of_selected_clip)
            el_locator = self.exist(L.main.duration_setting_dialog.txt_duration)
            self.set_time_code(el_locator, duration)
            self.exist_click(L.main.duration_setting_dialog.btn_ok)
            #self.wait_for_image_changes(img_before, L.main.timeline.table_view, OPERATION_DELAY * 5, similarity=0.99)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Main_page] Set timeline timecode')
    def set_timeline_timecode(self, time_code, is_verify=True): # time_code: format 'HH_MM_SS_mm', e.g. 00_00_01_03
        try:
            el_locator = self.exist(L.main.duration_setting_dialog.txt_duration)
            self.set_time_code(el_locator, time_code, is_verify)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def get_timeline_timecode(self):
        return self.exist(L.main.duration_setting_dialog.txt_duration).AXValue

    def set_library_preview_timecode(self, time_code): # time_code: format 'HH_MM_SS_mm', e.g. 00_00_01_03
        try:
            self.activate()
            img_before = self.snapshot(L.main.library_preview_window.slider)
            el_locator = self.exist(L.main.library_preview_window.txt_time_code)
            self.set_time_code(el_locator, time_code)
            self.wait_for_image_changes(img_before, L.main.library_preview_window.slider, OPERATION_DELAY * 5)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Main_page] Enter Room')
    def enter_room(self, index): # 0:media, 1:title, 2:transition, 3:effect, 4:pip, 5:particle, 6:audio mixing, 7:voice-over, 8:subtitle
        try:
            room_list = ['media', 'title', 'transition', 'effect', 'pip', 'particle', 'audio_mixing', 'voice_over', 'subtitle']
            logger(f'Trying to enter {room_list[index]} room')
            el_locator = eval(f'L.main.room_entry.btn_{room_list[index]}_room')

            img_collection_view_before = self.snapshot(L.media_room.library_listview.main_frame)
            time.sleep(OPERATION_DELAY)
            self.exist_click(el_locator)
            time.sleep(OPERATION_DELAY)
            if index == 6:
                logger('Due to enter Audio mixing room: cannot find locator, skip verify step')
                return True
            img_collection_view_after = self.snapshot(L.media_room.library_listview.main_frame)
            # verify is collection view frame is changed by snapshot
            result_verify = self.compare(img_collection_view_before, img_collection_view_after)
            if result_verify:
                logger(f'Fail to enter {room_list[index]} room')
                raise Exception(f'Fail to enter {room_list[index]} room')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
    
    @step('[Action][Main_page] select media by library icon view')
    def select_library_icon_view_media(self, name):
        try:
            self.activate()
            self.hover_library_media(name)
            self.left_click()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def close_and_restart_app(self):
        try:
            self.close_app()
            time.sleep(OPERATION_DELAY*2)
            self.start_app()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_undo(self):
        try:
            self.exist_click(L.main.btn_undo)
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_redo(self):
        try:
            self.exist_click(L.main.btn_redo)
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_produce(self):
        try:
            self.exist_click(L.main.btn_produce)
            time.sleep(OPERATION_DELAY)
            # verify enter produce page
            if not self.is_exist(L.produce.btn_start_produce, None, OPERATION_DELAY*10):
                logger(f'Fail to enter produce page')
                raise Exception(f'Fail to enter produce page')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def select_timeline_media(self, name, index=0): # index: 0-based row first
        try:
            locator = L.main.timeline.clip_name_unit
            if name.rfind(".") < 0: # filename without file extension (e.g. .jpg)
                locator[1]['AXValue'] = name
                els_media = self.exist_elements(locator)
            else:
                locator[1]['AXValue'] = name[:name.rfind(".")]
                els_media = self.exist_elements(locator)
            self.mouse.click(*els_media[index].AXParent.center)
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Main_page] select target track on timeline')
    def timeline_select_track(self, track_no): # index: 1-based track number (1-3)
        try:
            self.activate()
            els_track = self.exist_elements(L.main.timeline.track_unit)
            if track_no > 1:
                track_no = (track_no - 1)*2
            else:
                track_no = track_no - 1
            self.mouse.click(*els_track[track_no].center)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_library_icon_view(self):
        try:
            img_before = self.snapshot(L.media_room.scroll_area.library_table_view)
            self.exist_click(L.main.btn_library_icon_view)
            img_after = self.snapshot(L.media_room.scroll_area.library_table_view)
            result_verify = self.compare(img_before, img_after)
            if result_verify:
                logger(f'Fail to verify click library icon view')
                raise Exception(f'Fail to verify click library icon view')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_library_details_view(self):
        try:
            img_before = self.snapshot(L.media_room.scroll_area.library_table_view)
            self.exist_click(L.main.btn_library_details_view)
            time.sleep(OPERATION_DELAY)
            img_after = self.snapshot(L.media_room.scroll_area.library_table_view)
            result_verify = self.compare(img_before, img_after)
            if result_verify:
                logger(f'Fail to verify click library details view')
                raise Exception(f'Fail to verify click library details view')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def set_project_aspect_ratio(self, str_aspect_ratio): # str_aspect_ratio: 16_9, 4_3, 9_16, 1_1
        try:
            img_before = self.snapshot(L.main.btn_project_aspect_ratio)
            self.exist_click(L.main.btn_project_aspect_ratio)
            time.sleep(OPERATION_DELAY)
            el_aspect_ratio = self.exist(eval(f'L.main.option_project_aspect_ratio_{str_aspect_ratio}'))
            print(el_aspect_ratio)
            # check if already selected
            if el_aspect_ratio.AXMenuItemMarkChar:
                logger(f'Already set as {str_aspect_ratio}')
                self.left_click()
                return True
            self.el_click(el_aspect_ratio)
            time.sleep(OPERATION_DELAY)
            img_after = self.snapshot(L.media_room.scroll_area.library_table_view)
            result_verify = self.compare(img_before, img_after)
            if result_verify:
                logger(f'Fail to verify set project aspect ratio')
                raise Exception(f'Fail to verify set project aspect ratio')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def set_project_aspect_ratio_16_9(self):
        try:
            self.set_project_aspect_ratio('16_9')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def set_project_aspect_ratio_4_3(self):
        try:
            self.set_project_aspect_ratio('4_3')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def set_project_aspect_ratio_9_16(self):
        try:
            self.set_project_aspect_ratio('9_16')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def set_project_aspect_ratio_1_1(self):
        try:
            self.set_project_aspect_ratio('1_1')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Main_page] Handle [Save Project] Dialog')
    def handle_save_file_dialog(self, name, folder_path):
        try:
            self.select_file(os.path.abspath(f'{folder_path}/{name}'), 'Save')
            # handle if file already exists
            btn_replace = self.exist(L.main.save_file_dialog.btn_replace, OPERATION_DELAY * 3)
            if btn_replace:
                self.el_click(btn_replace)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def handle_save_as_file_dialog(self, name, folder_path):
        try:
            self.select_file(os.path.abspath(f'{folder_path}/{name}'), 'Save')
            # handle if file already exists
            btn_replace = self.exist(L.main.save_as_file_dialog.btn_replace, OPERATION_DELAY * 3)
            if btn_replace:
                self.el_click(btn_replace)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def save_project(self, name, folder_path, timeout=10):
        try:
            self.activate()
            time.sleep(OPERATION_DELAY)
            self.tap_SaveProject_hotkey()
            self.handle_save_file_dialog(name, folder_path)
            # verify PDR title is changed as project name
            start_time = time.time()
            is_completed = 0
            while time.time() - start_time < timeout:
                if self.exist(L.main.top_project_name, None, 2).AXValue == name:
                    is_completed = 1
                    break
                time.sleep(1)
            if not is_completed:
                logger('Fail to verify the top project name')
                raise Exception('Fail to verify the top project name')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def top_menu_bar_select_click_menu(self, *arg, is_enable=1, return_elem=False):
        item = None
        depth = len(arg)
        curr_depth = 0
        for item_name in arg:
            item = self.find({"AXRole": "AXMenuItem", "AXTitle": item_name}, parent=item)
            if not item: return False # in case no sub menu item (preference can set item to 0)
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

    @step('[Action][Main_page] Open Project from top menu bar')
    def top_menu_bar_file_open_project(self, save_changes=None):
        try:
            self.exist_click(L.main.top_menu_bar.btn_file)
            self.top_menu_bar_select_click_menu(L.main.top_menu_bar.option_open_project)
            if save_changes is not None:
                btn_locator = L.main.merge_media_to_library_dialog.btn_no
                if save_changes == 'yes':
                    btn_locator = L.main.merge_media_to_library_dialog.btn_yes
                self.exist_click(btn_locator)
            # verify if open file dialog pops up
            if not self.is_exist(L.main.open_file_dialog.main_window, None, OPERATION_DELAY * 5):
                logger('Fail to verify open project dialog pops up')
                raise Exception('Fail to verify open project dialog pops up')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def top_menu_bar_help_help(self):
        # Only for designer's (menu bar) help
        try:
            self.exist_click(L.main.top_menu_bar.btn_help)
            self.top_menu_bar_select_click_menu(L.main.top_menu_bar.option_help)

            time.sleep(OPERATION_DELAY*3)
            # For Video Intro Designer (v20.7.4219) : press enter key to close error dialog
            self.keyboard.enter()

            title = self.check_chrome_page()
            logger(title)
            #self.close_chrome_page()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return title

    @step('[Action][Main_page] Deal with [Open Project] dialog')
    def handle_open_project_dialog(self, file_path, uncompress_folder_path=''):
        try:
            if os.path.exists(uncompress_folder_path):
                import shutil
                shutil.rmtree(uncompress_folder_path)
            self.select_file(file_path)
            time.sleep(4)
            if uncompress_folder_path:
                self.select_file(uncompress_folder_path)
                time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Main_page] Deal with merge media to current library dialog')
    def handle_merge_media_to_current_library_dialog(self, option='yes', do_not_show_again='yes', timeout=30):
        try:
            # img_before = self.screenshot()
            # handle if merge project media to current library
            if do_not_show_again == 'yes':
                el_chx_do_not_show = self.exist(L.main.merge_media_to_library_dialog.chx_do_not_show_again,
                                         OPERATION_DELAY * 3)
                chx_pos = el_chx_do_not_show.AXPosition
                chx_size = el_chx_do_not_show.AXSize
                self.mouse.click(int(chx_pos[0]+10), int(chx_pos[1]+chx_size[1]/2))
            btn_option = eval(f'L.main.merge_media_to_library_dialog.btn_{option}')
            self.exist_click(btn_option)
            # self.wait_for_image_changes(img_before)
            is_complete = 0
            start_time = time.time()
            while time.time() - start_time < timeout:
                # handle high definition dialog > click No button
                if self.is_exist(L.main.confirm_dialog.alter_msg):
                    time.sleep(OPERATION_DELAY)
                    if self.exist(L.main.confirm_dialog.alter_msg).AXValue.startswith('High Definition Video'):
                        self.exist_click(L.main.merge_media_to_library_dialog.btn_no)

                if self.is_exist(L.main.dlg_loading_project, 2):
                    time.sleep(OPERATION_DELAY)
                    continue
                is_complete = 1
                break
            # [Jamie modify]
            # Some special situation stuck at "verify step"
            # 2022-12-28 : Remove the verify step to avoid (error handing)
            #if not is_complete:
            #    logger('Fail to verify loading project')
            #    raise Exception(f'Exception occurs. log={e}')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def tips_area_click_video_collage(self):
        try:
            self.exist_click(L.main.tips_area.btn_video_collage)
            # verify if video collage window pops up
            if not self.exist(L.video_collage_designer.main_window):
                logger('Fail to verify video collage window')
                raise Exception('Fail to verify video collage window')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def tips_area_click_add_effect_to_track(self, option=-1): # option = -1(No pop up menu), 0(Overwrite), 1(Insert), 2(Insert and Move All Clips)
        try:
            el_option = ['Overwrite', 'Insert', 'Move']
            self.exist_click(L.main.tips_area.btn_add_to_effect_track)
            time.sleep(OPERATION_DELAY * 2)
            if not option == -1:
                # click by OCR
                menu_item1_pos = self.search_text_position(el_option[option], mouse_move=0, order=1)
                print(f'{menu_item1_pos=}')
                if menu_item1_pos is not False:
                    self.mouse.click(*menu_item1_pos)
                else:
                    logger('Fail to get the position of target')
                    raise Exception('Fail to get the position of target')
            if self.is_exist(L.main.tips_area.btn_add_to_effect_track, None, 2):
                logger('Fail to add effect to track')
                raise Exception('Fail to add effect to track')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def top_menu_bar_file_import_media_files(self):
        try:
            img_before = self.screenshot()
            self.exist_click(L.main.top_menu_bar.btn_file)
            self.top_menu_bar_select_click_menu(*L.main.top_menu_bar.option_import_media_files)
            self.wait_for_image_changes(img_before)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def top_menu_bar_file_import_media_folder(self):
        try:
            img_before = self.screenshot()
            self.exist_click(L.main.top_menu_bar.btn_file)
            self.top_menu_bar_select_click_menu(*L.main.top_menu_bar.option_import_media_folder)
            self.wait_for_image_changes(img_before)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def top_menu_bar_file_new_project(self):
        try:
            img_before = self.screenshot()
            self.exist_click(L.main.top_menu_bar.btn_file)
            self.top_menu_bar_select_click_menu(L.main.top_menu_bar.option_new_project)
            self.wait_for_image_changes(img_before)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Main_page] Save project as from top menu bar')
    def top_menu_bar_file_save_project_as(self):
        try:
            #img_before = self.screenshot()
            self.exist_click(L.main.top_menu_bar.btn_file)
            self.top_menu_bar_select_click_menu(L.main.top_menu_bar.option_save_project_as)
            #self.wait_for_image_changes(img_before)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def top_menu_bar_file_open_recent_projects(self, full_path=None): # full_path: None(only hover on it)
        try:
            img_before = self.screenshot()
            self.click(L.main.top_menu_bar.btn_file)
            time.sleep(OPERATION_DELAY)
            item = self.find({"AXRole": "AXMenuItem", "AXTitle": L.main.top_menu_bar.option_open_recent_projects})
            time.sleep(OPERATION_DELAY*3)
            if not item.AXEnabled:
                logger('Fail to click item due to it\'s disabled')
                self.mouse.click()
                return False    # in case recent projects is None, Jamie requests to return False
            item_pos = item.AXPosition
            item_size = item.AXSize
            self.mouse.move(int(item_pos[0] + 30), item_pos[1])
            time.sleep(OPERATION_DELAY)
            self.mouse.move(int(item_pos[0] + item_size[0]), item_pos[1])
            time.sleep(OPERATION_DELAY)

            if full_path:
                if not self.top_menu_bar_select_click_menu(full_path): return False # did not find the target
            self.wait_for_image_changes(img_before, similarity=0.98)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def handle_no_save_project_dialog(self, option='no'): # option: 'yes', 'no'
        try:
            btn_locator = eval(f'L.main.merge_media_to_library_dialog.btn_{option}')
            self.exist_click(btn_locator)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def check_undo_button_is_enabled(self):
        return self.exist(L.main.btn_undo).AXEnabled

    def top_menu_bar_file_import_download_media_from_cl_cloud(self):
        try:
            img_before = self.screenshot()
            self.exist_click(L.main.top_menu_bar.btn_file)
            self.top_menu_bar_select_click_menu(*L.main.top_menu_bar.option_import_media_from_cyberlink_cloud)
            # verify if download media dialog pops up
            self.wait_for_image_changes(img_before, None, OPERATION_DELAY * 10)
            time.sleep(OPERATION_DELAY * 2)
            if not self.is_exist(L.main.download_media_dialog.title):
                logger('Fail to verify download media dialog pops up')
                raise Exception('Fail to verify download media dialog pops up')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def top_menu_bar_file_pack_project_materials(self, project_path):
        try:
            img_before = self.screenshot()
            # remove folder if exists
            folder_path = project_path.replace('/' + project_path.split('/')[-1], '')
            if os.path.exists(folder_path):
                logger(f'{folder_path} exists. remove it.')
                import shutil
                shutil.rmtree(folder_path)
            self.exist_click(L.main.top_menu_bar.btn_file)
            self.top_menu_bar_select_click_menu(L.main.top_menu_bar.option_pack_project_materials)
            # verify if select folder dialog pops up
            self.wait_for_image_changes(img_before, None, OPERATION_DELAY * 5, similarity=0.98)
            if folder_path:
                time.sleep(OPERATION_DELAY)
                self.select_file(os.path.abspath(project_path), 'Save', 1)
            btn_replace = self.exist(L.main.save_file_dialog.btn_replace, OPERATION_DELAY * 3)
            if btn_replace:
                self.el_click(btn_replace)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def top_menu_bar_plugins_video_collage_designer(self):
        try:
            img_before = self.screenshot()
            self.exist_click(L.main.top_menu_bar.btn_plugins)
            self.top_menu_bar_select_click_menu(L.main.top_menu_bar.option_video_collage_designer)
            # verify if video collage designer pops up
            self.wait_for_image_changes(img_before, None, OPERATION_DELAY * 10)
            time.sleep(OPERATION_DELAY * 2)
            if not self.is_exist(L.video_collage_designer.main_window):
                logger('Fail to verify download media dialog pops up')
                raise Exception('Fail to verify download media dialog pops up')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def top_menu_bar_view_show_library_preview_window(self, is_enable=1):
        try:
            self.exist_click(L.main.top_menu_bar.btn_view)
            self.top_menu_bar_select_click_menu(L.main.top_menu_bar.option_show_library_preview_window, is_enable=is_enable)
            # verify if library preview window shows or disappear
            time.sleep(OPERATION_DELAY * 2)
            if is_enable:
                if not self.exist(L.main.library_preview_window.slider, OPERATION_DELAY * 2):
                    logger('Fail to verify library preview window visible')
                    raise Exception('Fail to verify library preview window visible')
            else:
                if self.exist(L.main.library_preview_window.slider, OPERATION_DELAY * 2):
                    logger('Fail to verify library preview window invisible')
                    raise Exception('Fail to verify library preview window invisible')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def top_menu_bar_view_show_timeline_preview_volume_meter(self):
        try:
            # img_before = self.snapshot(L.library_preview.display_panel)
            self.click(L.main.top_menu_bar.btn_view)
            time.sleep(OPERATION_DELAY*2)
            self.click(L.main.top_menu_bar.menu_show_library_preview_window)
            # # verify if volume meter shows
            # self.wait_for_image_changes(img_before, L.library_preview.display_panel, OPERATION_DELAY * 10)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
    
    @step('[Action][Main_page] Click [Set User Preferences]')
    def click_set_user_preferences(self):
        try:
            self.exist_click(L.main.btn_set_user_preferences)
            if not self.is_exist(L.preferences.main_window):
                logger('Fail to open user preferences window')
                raise Exception('Fail to open user preferences window')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def drag_current_pos_media_to_timeline_playhead_position(self, track_no=1): # track_no: 1, 2, 3
        try:
            # This page function only for BGM used
            # Step 0: Mouse click custom BGM (which does user want to drag to timeline)
            # Step 1: Get current mouse position

            # Get current media position
            start_pos = self.get_mouse_pos()
            logger(f'{start_pos=}')
            # get dest. y-axis by track_no
            els_row = self.exist_elements(L.main.timeline.track_unit)
            track_pos = els_row[(track_no - 1) * 2].center
            dest_y_axis = track_pos[1]
            logger(f'{dest_y_axis=}')
            # get dest x-axis by indicator position
            indicator_pos = self.exist(L.main.timeline.indicator).center
            dest_x_axis = indicator_pos[0]
            logger(f'{dest_x_axis=}')
            dest_pos = (dest_x_axis, dest_y_axis)
            # drag clip to destination
            self.drag_mouse(start_pos, dest_pos)
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
    
    @step('[Action][Main_page] Drag media to timeline playhead position')
    def drag_media_to_timeline_playhead_position(self, name, track_no=1): # track_no: 1, 2, 3
        try:
            # hover to media
            self.hover_library_media(name)
            strat_pos = self.get_mouse_pos()
            logger(f'{strat_pos=}')
            # get dest. y-axis by track_no
            els_row = self.exist_elements(L.main.timeline.track_unit)
            track_pos = els_row[(track_no - 1) * 2].center
            dest_y_axis = track_pos[1]
            logger(f'{dest_y_axis=}')
            # get dest x-axis by indicator position
            indicator_pos = self.exist(L.main.timeline.indicator).center
            dest_x_axis = indicator_pos[0]
            logger(f'{dest_x_axis=}')
            dest_pos = (dest_x_axis, dest_y_axis)
            # drag clip to destination
            self.drag_mouse(strat_pos, dest_pos)
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def drag_media_to_timeline_playhead_position_offset(self, name, track_no=1):  # track_no: 1, 2, 3
        try:
            # hover to media
            self.hover_library_media(name)
            strat_pos = self.get_mouse_pos()
            logger(f'{strat_pos=}')
            # get dest. y-axis by track_no
            els_row = self.exist_elements(L.main.timeline.track_unit)
            offset = 10
            track_pos = els_row[(track_no - 1) * 2].center
            dest_y_axis = track_pos[1]
            logger(f'{dest_y_axis=}')
            # get dest x-axis by indicator position
            indicator_pos = self.exist(L.main.timeline.indicator).center
            dest_x_axis = indicator_pos[0] + offset
            logger(f'{dest_x_axis=}')
            dest_pos = (dest_x_axis, dest_y_axis)
            # drag clip to destination
            self.drag_mouse(strat_pos, dest_pos)
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def get_project_name(self):
        try:
            return self.find(L.main.top_project_name).AXValue
        except:
            return None

    def timeline_media_get_position(self, name, index=0, type=0): # index: 0-based row first; type=0(center), 1(left), 2(right)
        try:
            if name.rfind(".") < 0: # filename without file extension (e.g. .jpg)
                locator = L.main.timeline.clip_name_unit
                locator[1]['AXValue'] = name
                els_media = self.exist_elements(locator)
            else:
                locator = L.main.timeline.clip_name_unit
                locator[1]['AXValue'] = name[:name.rfind(".")]
                els_media = self.exist_elements(locator)
            position = els_media[index].AXParent.center
            if type > 0:
                pos_x_y = els_media[index].AXParent.AXPosition
                pos_w_h = els_media[index].AXParent.AXSize
                if type == 1:
                    position = (int(pos_x_y[0]), int((pos_x_y[1]+pos_w_h[1]/2)))
                elif type == 2:
                    position = (int(pos_x_y[0] + pos_w_h[0]), int((pos_x_y[1] + pos_w_h[1]/2)))
                else:
                    logger(f'Incorrect type > {type=}, return center as default')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return position

    def drag_transition_handle_pos_to_timeline_clip(self, name, clip_index=0, pos_type=0, menu_option=-1): # clip_index=0, 1, 2, ...; pos_type: 0(center), 1(left), 2(right)
        try:
            strat_pos = self.get_mouse_pos()
            # get the timeline clip position
            dest_pos = self.timeline_media_get_position(name, clip_index, pos_type)

            # handle new position for drag timeline clip position (Overlap transition)
            new_x = dest_pos[0] + 1
            new_y = dest_pos[1] + 5
            new_pos = (new_x, new_y)
            self.drag_mouse(strat_pos, new_pos)
            time.sleep(OPERATION_DELAY * 3)

            # handle submenu
            menu_option_list = ['Overwrite', 'Insert', 'Move', 'Crossfade', 'Replace']
            if not menu_option == -1:
                # click by OCR
                menu_item1_pos = self.search_text_position(menu_option_list[menu_option], mouse_move=0, order=1)
                print(f'{menu_item1_pos=}')
                if menu_item1_pos is not False:
                    self.mouse.click(*menu_item1_pos)
                else:
                    logger('Fail to get the position of target menu item')
                    raise Exception('Fail to get the position of target menu item')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def drag_media_to_timeline_clip(self, name, clip_index=0, pos_type=0, menu_option=-1): # clip_index=0, 1, 2, ...; pos_type: 0(center), 1(left), 2(right)
        try:
            strat_pos = self.get_mouse_pos()
            # get the timeline clip position
            dest_pos = self.timeline_media_get_position(name, clip_index, pos_type)
            self.drag_mouse(strat_pos, dest_pos)
            time.sleep(OPERATION_DELAY * 3)
            # handle submenu
            menu_option_list = ['Overwrite', 'Insert', 'Move', 'Crossfade', 'Replace']
            if not menu_option == -1:
                # click by OCR
                menu_item1_pos = self.search_text_position(menu_option_list[menu_option], mouse_move=0, order=1)
                print(f'{menu_item1_pos=}')
                if menu_item1_pos is not False:
                    self.mouse.click(*menu_item1_pos)
                else:
                    logger('Fail to get the position of target menu item')
                    raise Exception('Fail to get the position of target menu item')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def drag_transition_to_timeline_clip(self, transition_name, clip_2nd_name, clip_index=0): # drag transition to the left of 2nd clip
        try:
            self.hover_library_media(transition_name)
            time.sleep(OPERATION_DELAY)
            # Update for v21.3.4929
            self.drag_transition_handle_pos_to_timeline_clip(clip_2nd_name, clip_index, 1)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def is_show_serious_frame_drop_dialog(self, timeout=5):
        try:
            el_description = self.exist(L.main.serious_frame_drop_decteced_dialog.description, timeout)
            if 'Serious Frame Drop' not in el_description.AXValue:
                logger('No serious frame drop dialog pops up')
                raise Exception('No serious frame drop dialog pops up')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            return False
        return True

    def serious_frame_drop_dialog_click_yes(self, timeout=5):
        try:
            if self.is_show_serious_frame_drop_dialog(timeout):
                img_before = self.screenshot()
                self.exist_click(L.main.serious_frame_drop_decteced_dialog.btn_yes)
                time.sleep(OPERATION_DELAY)
                # verify if serious frame drop dialog closed
                self.wait_for_image_changes(img_before, None, OPERATION_DELAY * 5)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def handle_aspect_ratio_conflict(self, option='no'):
        try:
            self.exist_click(eval(f'L.main.merge_media_to_library_dialog.btn_{option}'))
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def top_menu_bar_powerdirector_preferences(self):
        try:
            self.exist_click(L.main.top_menu_bar.btn_powerdirector)
            self.top_menu_bar_select_click_menu(L.main.top_menu_bar.option_preferences)
            # verify if preferences dialog pops up
            if not self.is_exist(L.preferences.main_window):
                logger('Fail to open user preferences window')
                raise Exception('Fail to open user preferences window')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_inteligent_svrt_information_close(self):
        return self.exist_click(L.main.inteligent_svrt_information.btn_close)

    def top_menu_bar_file_download_project_from_cyberlink_cloud(self):
        try:
            self.click(L.main.top_menu_bar.btn_file)
            time.sleep(2)
            self.top_menu_bar_select_click_menu(L.main.top_menu_bar.option_download_project_from_cyberlink_cloud)
            time.sleep(2)
            # verify if dialog pops up
            if not self.is_exist(L.main.download_cyberlink_cloud_project_window.main_window):
                logger('Fail to open download from cyberlink cloud project window')
                raise Exception('Fail to open download from cyberlink cloud project window')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def top_menu_bar_file_upload_project_to_cyberlink_cloud(self):
        try:
            self.exist_click(L.main.top_menu_bar.btn_file)
            self.top_menu_bar_select_click_menu(L.main.top_menu_bar.option_upload_project_to_cyberlink_cloud)
            # verify if dialog pops up
            if not self.is_exist(L.main.upload_project_to_cyberlink_cloud_window.main_window):
                logger('Fail to open upload project to cyberlink cloud window')
                raise Exception('Fail to open upload project to cyberlink cloud window')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def top_menu_bar_file_pack_project_and_upload_to_cyberlink_cloud(self):
        try:
            self.exist_click(L.main.top_menu_bar.btn_file)
            self.top_menu_bar_select_click_menu(L.main.top_menu_bar.option_pack_project_and_upload_to_cyberlink_cloud)
            # verify if dialog pops up
            if not self.is_exist(L.main.upload_project_to_cyberlink_cloud_window.main_window):
                logger('Fail to open upload project to cyberlink cloud window')
                raise Exception('Fail to open upload project to cyberlink cloud window')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def top_menu_bar_file_insert_project(self):
        try:
            self.exist_click(L.main.top_menu_bar.btn_file)
            self.top_menu_bar_select_click_menu(L.main.top_menu_bar.option_insert_project)
            # verify if open file dialog pops up
            if not self.is_exist(L.main.open_file_dialog.main_window, None, OPERATION_DELAY * 5):
                logger('Fail to verify open project dialog pops up')
                raise Exception(f'Exception occurs. log={e}')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def top_menu_bar_edit_undo(self):
        try:
            self.exist_click(L.main.top_menu_bar.btn_edit)
            time.sleep(0.5)
            elem = self.exist(L.main.top_menu_bar.menu_item_undo).AXPosition
            self.mouse.click(elem[0]+3, elem[1]+3)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def top_menu_bar_edit_redo(self):
        try:
            self.exist_click(L.main.top_menu_bar.btn_edit)
            time.sleep(0.5)
            elem = self.exist(L.main.top_menu_bar.menu_item_redo).AXPosition
            self.mouse.click(elem[0]+3, elem[1]+3)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def top_menu_bar_edit_remove(self):
        try:
            self.exist_click(L.main.top_menu_bar.btn_edit)
            time.sleep(0.5)
            elem = self.exist(L.main.top_menu_bar.menu_item_remove).AXPosition
            self.mouse.click(elem[0]+3, elem[1]+3)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action] Close AP and back to launcher')
    def click_close_then_back_to_launcher(self):
        result = self.click(L.main.main_window.btn_close)
        time.sleep(1)
        return result 