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

def select_combobox_item(obj, locator_combobox, locator_option):
    try:
        locator = locator_option
        el_cbx = obj.exist(locator_combobox)
        if el_cbx.AXTitle != locator['AXValue']:
            obj.el_click(el_cbx)
            time.sleep(DELAY_TIME * 0.5)
            obj.exist_click(locator)
            time.sleep(DELAY_TIME * 0.5)
            # verify if apply correctly
            if obj.exist(locator_combobox).AXTitle != locator['AXValue']:
                logger(f'Fail to verify apply combobox setting.')
                raise Exception(f'Fail to verify apply combobox setting.')
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        raise Exception(f'Exception occurs. log={e}')
    return True

class Timeline_Operation(Main_Page, BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.undock_timeline = self.Undock_Timeline(*args, **kwargs)
        self.timeline_marker = self.Timeline_Marker(*args, **kwargs)

    def edit_timeline_render_preview(self):
        try:
            img_workspace_before_render_preview = self.snapshot(L.timeline_operation.workspace)
            if self.exist(L.timeline_operation.render_preview_button).AXEnabled == True:
                self.exist_click(L.timeline_operation.render_preview_button)
                time.sleep(3)
                img_workspace_after_render_preview = self.snapshot(L.timeline_operation.workspace)
                print(f'{img_workspace_before_render_preview=}, {img_workspace_after_render_preview}')
                result_verify = self.compare(img_workspace_before_render_preview, img_workspace_after_render_preview, similarity=1)
                if result_verify:
                    logger("Can't render preview successfully")
                    raise Exception("Can't render preview successfully")
                time.sleep(3)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def get_render_preview_btn_status(self):
        try:
            result = self.exist(L.timeline_operation.render_preview_button).AXEnabled
            return result
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    def timeline_click_zoomin_btn(self):
        try:
            img_timeline_before = self.snapshot(L.timeline_operation.workspace)
            if not self.exist_click(L.timeline_operation.timeline_zoomin_button):
                logger("Didn't find the zoom in button to click")
                raise Exception("Didn't find the zoom in button to click")

            # Verify Step
            img_timeline_after = self.snapshot(L.timeline_operation.workspace)
            print(f'{img_timeline_before=}, {img_timeline_after=}')
            result_verify = self.compare(img_timeline_before, img_timeline_after)
            if result_verify:
                logger("Didn't click the zoom in btn/ slider already set on the maximum")
                #raise Exception(f'Exception occurs. log={e}')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_zoomout_btn(self):
        try:
            img_timeline_before = self.snapshot(L.timeline_operation.workspace)
            if not self.exist_click(L.timeline_operation.timeline_zoomout_button):
                logger("Didn't find the zoom out button to click")
                raise Exception("Didn't find the zoom out button to click")

            # Verify Step
            img_timeline_after = self.snapshot(L.timeline_operation.workspace)
            print(f'{img_timeline_before=}, {img_timeline_after=}')
            result_verify = self.compare(img_timeline_before, img_timeline_after)
            if result_verify:
                logger("Didn't click the zoom out btn/ slider already set on the minimum")
                #raise Exception(f'Exception occurs. log={e}')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def drag_zoom_sliderbar(self, value):
        try:
            self.exist(L.timeline_operation.zoom_slider_bar).AXValue = float(value)
            time.sleep(DELAY_TIME)
            # Verify Step
            if float(value) == self.exist(L.timeline_operation.zoom_slider_bar).AXValue:
                return True
            else:
                return False
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def get_zoom_indicator(self):
        value = self.exist(L.timeline_operation.zoom_slider_bar).AXValue
        logger(value)
        return value

    def right_click_remove_empty_tracks(self):
        try:
            if not self.exist_click(L.timeline_operation.workspace):
                logger("No timeline show up")
                raise Exception("No timeline show up")
            self.right_click()
            time.sleep(DELAY_TIME)
            if not self.select_right_click_menu('Remove Empty Tracks'):
                logger("Can't click [Remove Empty Tracks]")
                raise Exception("Can't click [Remove Empty Tracks]")
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def right_click_show_clip_marker_track(self):
        try:
            img_timeline_before = self.snapshot(L.timeline_operation.workspace)
            if not self.exist_click(L.timeline_operation.workspace):
                logger("No timeline show up")
                raise Exception("No timeline show up")
            self.right_click()
            time.sleep(DELAY_TIME)
            if not self.select_right_click_menu('Show Clip Marker Track'):
                logger("Can't click [Show Clip Marker Track] button")
                raise Exception("Can't click [Show Clip Marker Track] button")
            img_timeline_after = self.snapshot(L.timeline_operation.workspace)
            print(f'{img_timeline_before=}, {img_timeline_after=}')
            # Verify Step
            result_verify = self.compare(img_timeline_before, img_timeline_after)
            if result_verify:
                logger("Didn't show the clip marker track successfully")
                raise Exception("Didn't show the clip marker track successfully")

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def right_click_add_tracks(self):
        try:
            if not self.exist_click(L.timeline_operation.workspace):
                logger("No timeline show up")
                raise Exception("No timeline show up")
            self.right_click()
            time.sleep(DELAY_TIME)
            if not self.select_right_click_menu('Add Tracks...'):
                logger("Can't click [Add Tracks...] button")
                raise Exception("Can't click [Add Tracks...] button")
            time.sleep(DELAY_TIME)
            if not self.exist(L.timeline_operation.track_manager_dialog):
                logger("Didn't show the track manager dialog")
                raise Exception("Didn't show the track manager dialog")

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def mouse_move_to_video_track1(self):
        try:
            if not self.exist(L.timeline_operation.timeline_video_track1):
                logger("Can't found the video track 1")
                raise Exception("Can't found the video track 1")
            video_track1 = self.exist(L.timeline_operation.timeline_video_track1)
            self.mouse.move(*video_track1.center)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action] Click the [View Entire Video] button')
    def click_view_entire_video_btn(self):
        try:
            if not self.exist_click(L.timeline_operation.view_entire_video):
                logger("Can't click the [View Entire Video] btn")
                raise Exception("Can't click the [View Entire Video] btn")
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def drag_timeline_horizontal_scroll_bar(self, value):
        try:
            self.exist(L.timeline_operation.timeline_horizontal_scroll_bar).AXValue = float(value)
            time.sleep(DELAY_TIME)
            # Verify Step
            if float(value) == self.exist(L.timeline_operation.timeline_horizontal_scroll_bar).AXValue:
                return True
            else:
                return False
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def drag_timeline_vertical_scroll_bar(self, value):
        try:
            self.exist(L.timeline_operation.timeline_vertical_scroll_bar).AXValue = float(value)
            time.sleep(DELAY_TIME)
            # Verify Step
            if float(value) == self.exist(L.timeline_operation.timeline_vertical_scroll_bar).AXValue:
                return True
            else:
                return False
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True


    def set_clipmarker_time(self, timecode):
        self.activate()
        elem = self.find(L.timeline_operation.clipmarker_timecode)
        w, h = elem.AXSize
        x, y = elem.AXPosition

        pos_click = tuple(map(int, (x + w * 0.1, y + h * 0.5)))
        self.mouse.click(*pos_click)
        time.sleep(1)
        self.keyboard.send(timecode.replace("_", ""))
        self.keyboard.enter()

        self.exist_click(L.timeline_operation.clipmarker_ok)

    def set_clipmarker_note(self, string):
        self.exist_click(L.timeline_operation.clipmarker_textfield)
        self.tap_SelectAll_hotkey()
        self.tap_Remove_hotkey()
        self.keyboard.send(string)
        time.sleep(1)
        self.exist_click(L.timeline_operation.clipmarker_ok)

    def hover_timeline_media(self, track_index, clip_index):
        '''
        e.g. first video track's second clip = [{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}]
        '''
        try:
            target_clip = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}])
            if not self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]):
                logger("Can't find the target clip on timeline")
                raise Exception("Can't find the target clip on timeline")
            self.mouse.move(*target_clip.center)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def get_video_clip_name(self, track_index, clip_index):
        '''
        e.g. first video track's second clip = [{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}]
        '''
        try:
            if not self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]):
                logger("Can't find the target clip on timeline")
                raise Exception("Can't find the target clip on timeline")
            time.sleep(DELAY_TIME)
            self.right_click()
            self.select_right_click_menu('Edit Clip Alias', 'Change Alias...')
            target_clip_name = self.exist_click(L.timeline_operation.clip_alias).AXValue
            self.exist_click(L.timeline_operation.alias_ok)
            return target_clip_name

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def get_audio_clip_name(self, track_index, clip_index):
        '''
        e.g. first audio track's second clip = [{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 1}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}]
        '''
        try:
            if not self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]):
                logger("Can't find the target clip on timeline")
                raise Exception("Can't find the target clip on timeline")
            time.sleep(DELAY_TIME)
            self.right_click()
            self.select_right_click_menu('Edit Clip Alias', 'Change Alias...')
            target_clip_name = self.exist_click(L.timeline_operation.clip_alias).AXValue
            self.exist_click(L.timeline_operation.alias_ok)
            return target_clip_name
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def get_effect_clip_name(self, track_index, clip_index):
        '''
        e.g. first audio track's second clip = [{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 1}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}]
        '''
        try:
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]):
                logger("Can't find the effect clip on timeline")
                raise Exception("Can't find the effect clip on timeline")
            time.sleep(DELAY_TIME)
            #self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}, {'AXIdentifier': '_NS:66', 'AXRole': 'AXStaticText'}])
            effect_name = self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}, {'AXIdentifier': 'IDC_VIDEOCELL_ALIAS', 'AXRole': 'AXStaticText'}]).AXValue
            return effect_name

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def hover_i_mark(self, track_index, clip_index):
        '''
        e.g. first audio track's second clip = [{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 1}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}]
        '''
        try:
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]):
                logger("Can't find the clip on timeline")
                raise Exception("Can't find the clip on timeline")
            time.sleep(DELAY_TIME)
            i_mark = self.find([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            self.mouse.move(*i_mark.center)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def snapshot_i_mark_tooltip(self, track_index, clip_index):
        '''
        e.g. first audio track's second clip = [{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 1}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}]
        '''
        try:
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]):
                logger("Can't find the clip on timeline")
                raise Exception("Can't find the clip on timeline")
            time.sleep(DELAY_TIME)
            clip = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}])
            track = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}])
            x, _ = clip.AXPosition
            _, y = track.AXPosition
            w, _ = clip.AXSize
            _, h = track.AXSize
            i_mark = self.find([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}], {'AXIdentifier': 'IDC_VIDEOCELL_INFO_ICON', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
            self.mouse.move(*i_mark.center)
            time.sleep(1)
            full_path = self.image.snapshot(x= x, y=int(y+96), w=w, h=h)
            #logger(f'{full_path=}')
            return full_path

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def drag_single_media_move_to(self, track_index, clip_index, distance):
        try:
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]):
                logger("Can't find the clip on timeline")
                raise Exception("Can't find the clip on timeline")
            time.sleep(DELAY_TIME)
            clip = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}])
            clip_pos = clip.AXPosition

            self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}])
            self.mouse.drag((int(clip_pos[0]+10), int(clip_pos[1]+30)), (int(clip_pos[0]+10+distance), int(clip_pos[1]+30)))
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def drag_single_audio_move_to(self, track_index, clip_index, distance):
        try:
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]):
                logger("Can't find the clip on timeline")
                raise Exception("Can't find the clip on timeline")
            time.sleep(DELAY_TIME)
            clip = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}])
            clip_pos = clip.AXPosition
            clip_length = clip.AXSize

            self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}])
            self.mouse.drag((int(clip_pos[0]+clip_length[0]*0.5), int(clip_pos[1]+clip_length[1]*0.5)), (int(clip_pos[0]+clip_length[0]*0.5+distance), int(clip_pos[1]+clip_length[1]*0.5)))
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def get_clip_size(self, track_index, clip_index):
        try:
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]):
                logger("Can't find the clip on timeline")
                raise Exception("Can't find the clip on timeline")
            time.sleep(DELAY_TIME)
            clip = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}])
            clip_length = clip.AXSize
            return clip_length[0]

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def drag_multi_media_move_to(self, media1_track_index, media1_clip_index, media2_track_index, media2_clip_index, distance):
        try:
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': media1_track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': media1_clip_index}]):
                logger("Can't find the clip1 on timeline")
                raise Exception("Can't find the clip1 on timeline")
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': media2_track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': media2_clip_index}]):
                logger("Can't find the clip2 on timeline")
                raise Exception("Can't find the clip2 on timeline")
            time.sleep(DELAY_TIME)
            clip = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': media2_track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': media2_clip_index}])
            clip_pos = clip.AXPosition

            self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': media1_track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': media1_clip_index}])
            self.keyboard.press(self.keyboard.key.cmd)
            self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': media2_track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': media2_clip_index}])
            self.keyboard.release(self.keyboard.key.cmd)
            self.mouse.drag((int(clip_pos[0]+10), int(clip_pos[1]+30)), (int(clip_pos[0]+10+distance), int(clip_pos[1]+30)))
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
    def drag_single_media_to_other_track(self, track_index, clip_index, distance, track_num):
        try:
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]):
                logger("Can't find the clip on timeline")
                raise Exception("Can't find the clip on timeline")
            time.sleep(DELAY_TIME)
            clip = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}])
            clip_pos = clip.AXPosition

            self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}])
            self.mouse.drag((int(clip_pos[0]+10), int(clip_pos[1]+30)), (int(clip_pos[0]+10+distance), int(clip_pos[1]+60+48*track_num)))
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def drag_multi_media_move_to_other_track(self, media1_track_index, media1_clip_index, media2_track_index, media2_clip_index, distance, track_num):
        try:
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': media1_track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': media1_clip_index}]):
                logger("Can't find the clip1 on timeline")
                raise Exception("Can't find the clip1 on timeline")
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': media2_track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': media2_clip_index}]):
                logger("Can't find the clip2 on timeline")
                raise Exception("Can't find the clip2 on timeline")
            time.sleep(DELAY_TIME)
            clip = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': media2_track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': media2_clip_index}])
            clip_pos = clip.AXPosition

            self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': media1_track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': media1_clip_index}])
            self.keyboard.press(self.keyboard.key.cmd)
            self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': media2_track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': media2_clip_index}])
            self.keyboard.release(self.keyboard.key.cmd)
            self.mouse.drag((int(clip_pos[0]+10), int(clip_pos[1]+30)), (int(clip_pos[0]+10+distance), int(clip_pos[1]+60+48*track_num)))
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def trim_enlarge_drag_clip_edge(self, clip_index, distance, index=1):
        try:
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]):
                logger("Can't find the clip1 on timeline")
                raise Exception("Can't find the clip1 on timeline")
            clip = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}])
            x, y = clip.AXPosition
            x1, _ = clip.AXSize
            self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}])
            self.mouse.move(x+x1, int(y+30))
            try:
                self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},{'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},{'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': int(clip_index + 1)}])
                clip2 = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},{'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},{'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': int(clip_index + 1)}])
                x2, y2 = clip2.AXPosition
                #print(x2, y2)
                interval = int(x2 - (x + x1))
                self.mouse.drag((int(x + x1 - 5), int(y + 30)), (int(x + x1 + distance), int(y + 30)))
                if distance > interval:
                   self.timeline_trim_enlarge_drag_clip_edge_menu(index)
            except IndexError:
                self.mouse.drag((int(x + x1 - 5), int(y + 30)), (int(x + x1 + distance), int(y + 30)))
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
    def apply_video_speed(self, track_index, clip_index, speed_value):
        try:
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]):
                logger("Can't find the clip1 on timeline")
                raise Exception("Can't find the clip1 on timeline")
            clip = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}])
            x, y = clip.AXPosition
            x1, _ = clip.AXSize
            self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}])
            self.mouse.move(int(x+2), int(y+15))
            self.keyboard.press(self.keyboard.key.ctrl)
            self.mouse.drag((int(x+2), int(y+15)), (int(x + 2 - float(speed_value) * x1), int(y+15)))
            self.keyboard.release(self.keyboard.key.ctrl)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def drag_snap_feature(self, clip1_index):
        try:
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index}]):
                logger("Can't find the clip1 on timeline")
                raise Exception("Can't find the clip1 on timeline")
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index+1}]):
                logger("Can't find the clip2 on timeline")
                raise Exception("Can't find the clip2 on timeline")
            clip1 = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index}])
            clip2 = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index+1}])
            x, y = clip1.AXPosition
            x1, _ = clip1.AXSize
            x2, y2 = clip2.AXPosition
            self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index}])
            self.mouse.move(int(x+x1-10), int(y+15))
            self.mouse.drag((int(x+x1-10), int(y+15)), (int(x2-13), int(y+15)))
            clip1_current = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index}])
            clip2_current = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index+1}])
            x_current, y_current = clip1_current.AXPosition
            x1_current, _ = clip1_current.AXSize
            x2_current, y2_current = clip2_current.AXPosition
            if int(x2_current - (x_current+x1_current)) < 1:
                print('Pass')
                return True
            else:
                print('Fail')
                return False
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def drag_no_snap(self, clip1_index):
        try:
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index}]):
                logger("Can't find the clip1 on timeline")
                raise Exception("Can't find the clip1 on timeline")
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index+1}]):
                logger("Can't find the clip2 on timeline")
                raise Exception("Can't find the clip2 on timeline")
            clip1 = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index}])
            clip2 = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index+1}])
            x, y = clip1.AXPosition
            x1, _ = clip1.AXSize
            x2, y2 = clip2.AXPosition
            self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index}])
            self.mouse.move(int(x+x1-10), int(y+15))
            self.keyboard.press(self.keyboard.key.alt)
            self.mouse.drag((int(x+x1-10), int(y+15)), (int(x2-13), int(y+15)))
            self.keyboard.release(self.keyboard.key.alt)
            clip1_current = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index}])
            clip2_current = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index+1}])
            x_current, y_current = clip1_current.AXPosition
            x1_current, _ = clip1_current.AXSize
            x2_current, y2_current = clip2_current.AXPosition
            if int(x2_current - (x_current+x1_current)) < 1:
                print('Fail')
                return False
            else:
                print('Pass')
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def trim_snap_feature(self, clip1_index, clip2_index):
        try:
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index}]):
                logger("Can't find the clip1 on timeline")
                raise Exception("Can't find the clip1 on timeline")
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip2_index}]):
                logger("Can't find the clip2 on timeline")
                raise Exception("Can't find the clip2 on timeline")
            clip1 = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index}])
            clip2 = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip2_index}])
            x, y = clip1.AXPosition
            x1, _ = clip1.AXSize
            x2, y2 = clip2.AXPosition
            self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index}])
            self.mouse.move(int(x+x1-5), int(y+15))
            self.mouse.drag((int(x+x1-5), int(y+15)), (int(x2-12), int(y+15)))
            clip1_current = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index}])
            clip2_current = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip2_index}])
            x_current, y_current = clip1_current.AXPosition
            x1_current, _ = clip1_current.AXSize
            x2_current, y2_current = clip2_current.AXPosition
            if int(x2_current - (x_current+x1_current)) < 1:
                print('Pass')
                return True
            else:
                print('Fail')
                return False
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def trim_no_snap(self, clip1_index, clip2_index):
        try:
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index}]):
                logger("Can't find the clip1 on timeline")
                raise Exception("Can't find the clip1 on timeline")
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip2_index}]):
                logger("Can't find the clip2 on timeline")
                raise Exception("Can't find the clip2 on timeline")
            clip1 = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index}])
            clip2 = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip2_index}])
            x, y = clip1.AXPosition
            x1, _ = clip1.AXSize
            x2, y2 = clip2.AXPosition
            self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index}])
            self.mouse.move(int(x+x1-5), int(y+15))
            self.keyboard.press(self.keyboard.key.alt)
            self.mouse.drag((int(x+x1-5), int(y+15)), (int(x2-13), int(y+15)))
            self.keyboard.release(self.keyboard.key.alt)
            clip1_current = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index}])
            clip2_current = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip2_index}])
            x_current, y_current = clip1_current.AXPosition
            x1_current, _ = clip1_current.AXSize
            x2_current, y2_current = clip2_current.AXPosition
            if int(x2_current - (x_current+x1_current)) < 1:
                print('Fail')
                return False
            else:
                print('Pass')
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def trim_timeline_clips(self, ratio, track_index, clip1_index, clip2_index= None):
        try:
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index}]):
                logger("Didn't found the clip1")
                raise Exception("Didn't found the clip1")
            clip1 = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index}])
            x, y = clip1.AXPosition
            x1, _ = clip1.AXSize
            self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index}])
            self.right_click()
            if self.select_right_click_menu('Link/Unlink Video and Audio') == False:
                option_1 = 'Image'
                print(option_1)
            else:
                self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                  {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                                  {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index}])
                self.right_click()
                self.select_right_click_menu('Link/Unlink Video and Audio')
                option_1 = 'Video'
                print(option_1)
            if clip2_index == None and option_1 == 'Video':
                logger('selected clip is a video')
                raise Exception('selected clip is a video')
            if clip2_index == None and option_1 == 'Image':
                self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                  {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                                  {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index}])
                if float(ratio) > 0:
                    self.mouse.move(int(x + x1 - 6), int(y + 15))
                    self.mouse.drag((int(x+x1-6), int(y+15)), (int(x+x1-6 + float(ratio*x1)), int(y+15)))
                if float(ratio) < 0:
                    self.mouse.move(int(x + 4), int(y + 15))
                    self.mouse.drag((int(x + 4), int(y+15)), (int(x+4 - float(ratio*x1)), int(y+15)))
            if clip2_index != None:
                clip2 = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                                {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip2_index}])
                x2, y2 = clip2.AXPosition
                x3, _ = clip2.AXSize
                self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                  {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                                  {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip2_index}])
                self.right_click()
                if self.select_right_click_menu('Link/Unlink Video and Audio') == False:
                    option_2 = 'Image'
                    print(option_2)
                else:
                    self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                      {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                                      {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip2_index}])
                    self.right_click()
                    self.select_right_click_menu('Link/Unlink Video and Audio')
                    option_2 = 'Video'
                    print(option_2)
                if option_1 == 'Video' and option_2 == 'Video':
                    logger("Selected clips are videos")
                    raise Exception("Selected clips are videos")
                if option_1 == 'Video' and option_2 == 'Image':
                    self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                      {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                                      {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index}])
                    self.keyboard.press(self.keyboard.key.cmd)
                    self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                      {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                                      {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip2_index}])
                    self.keyboard.release(self.keyboard.key.cmd)
                    if float(ratio) > 0:
                       self.mouse.move(int(x2+x3-6), int(y2+15))
                       self.mouse.drag((int(x2+x3-6), int(y2+15)), (int(x2+x3-6 + float(ratio*x3)), int(y2+15)))
                    if float(ratio) < 0:
                       self.mouse.move(int(x2+x3-6), int(y2+15))
                       self.mouse.drag((int(x2+x3-6), int(y2+15)), (int(x2+x3-6 + float(ratio*x3)), int(y2+15)))
                if option_1 == 'Image' and option_2 == 'Video':
                    self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                      {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                                      {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip1_index}])
                    self.keyboard.press(self.keyboard.key.cmd)
                    self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                      {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                                      {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip2_index}])
                    self.keyboard.release(self.keyboard.key.cmd)
                    if float(ratio) > 0:
                       self.mouse.move(int(x+4), int(y+15))
                       self.mouse.drag((int(x+4), int(y+15)), (int(x+4 - float(ratio*x1)), int(y+15)))
                    if float(ratio) < 0:
                       self.mouse.move(int(x+4), int(y+15))
                       self.mouse.drag((int(x+4), int(y+15)), (int(x+4 - float(ratio*x1)), int(y+15)))
                if option_1 == 'Image' and option_2 == 'Image':
                    logger('Selected clips are images')
                    raise Exception('Selected clips are images')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def drag_timeline_clip(self, mode, ratio, track_index1, clip_index1, track_index2=None, clip_index2=None):
        try:
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index1},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index1}]):
                logger("Didn't found the clip1")
                raise Exception("Didn't found the clip1")
            clip1 = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index1},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index1}])
            x, y = clip1.AXPosition
            x1, y1 = clip1.AXSize
            self.click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index1},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index1}])
            if clip_index2 == None:
                if mode == 'Front':
                    self.mouse.move(int(x + 4), int(y + 15))
                    self.mouse.drag((int(x+4), int(y+15)), (int(x+4 + int(float(ratio)*x1)), int(y+15)))
                if mode == 'Last':
                    self.mouse.move(int(x + x1-1), int(y + 15))
                    time.sleep(DELAY_TIME)
                    self.mouse.drag((int(x + x1-1), int(y+15)), (int(x+x1-1 - int(float(ratio)*x1)), int(y+15)))
            if clip_index2 != None:
                clip2 = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index2},
                                {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index2}])
                x2, y2 = clip2.AXPosition
                x3, y3 = clip2.AXSize
                self.click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                  {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index1},
                                  {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index1}])
                self.keyboard.press(self.keyboard.key.cmd)
                time.sleep(DELAY_TIME)
                self.click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                  {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index2},
                                  {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index2}])
                self.keyboard.release(self.keyboard.key.cmd)
                if mode == 'Front':
                    self.mouse.move(int(x+4), int(y+15))
                    self.mouse.drag((int(x+4), int(y+15)), (int(x+4 + int(float(ratio)*x1)), int(y+15)))
                if mode == 'Last':
                    self.mouse.move(int(x2+x3-6), int(y2+15))
                    self.mouse.drag((int(x2+x3-6), int(y2+15)), (int(x2+x3-6 - int(float(ratio)*x3)), int(y2+15)))
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def drag_timeline_clip1_to_clip2_middle(self, track_index1, clip_index1, track_index2, clip_index2):
        try:
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index1},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index1}]):
                logger("Didn't found the clip1")
                raise Exception("Didn't found the clip1")
            clip1 = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index1},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index1}])
            x, y = clip1.AXPosition
            x1, _ = clip1.AXSize
            clip2 = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index2},
                                {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index2}])
            x2, y2 = clip2.AXPosition
            x3, _ = clip2.AXSize
            self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                              {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index1},
                              {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index1}])
            self.mouse.move(int(x+int(x1*0.5)), int(y+15))
            self.mouse.drag((int(x+int(x1*0.5)), int(y+15)), (int(x2+(0.5*x3)), int(y+15)))
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def drag_to_change_speed(self, track_index, clip_index, mode, direction, ratio):
        try:
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]):
                logger("Didn't found the clip")
                raise Exception("Didn't found the clip")
            clip1 = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}])
            x, y = clip1.AXPosition
            x1, _ = clip1.AXSize
            self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                               {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                               {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}])
            self.keyboard.press(self.keyboard.key.ctrl)
            if mode == 'Front':
                if direction == 'Left':
                    self.mouse.move(int(x + 4), int(y + 15))
                    self.mouse.drag((int(x + 4), int(y + 15)), (int(x + 4 - int(float(ratio) * x1)), int(y + 15)))
                    self.keyboard.release(self.keyboard.key.ctrl)
                elif direction == 'Right':
                    self.mouse.move(int(x + 4), int(y + 15))
                    self.mouse.drag((int(x + 4), int(y + 15)), (int(x + 4 + int(float(ratio) * x1)), int(y + 15)))
                    self.keyboard.release(self.keyboard.key.ctrl)
            elif mode == 'Last':
                if direction == 'Left':
                    self.mouse.move(int(x+x1-1), int(y+15))
                    self.mouse.drag((int(x + x1 -1), int(y+15)), (int(x+x1-1 - int(float(ratio)*x1)), int(y+15)))
                    self.keyboard.release(self.keyboard.key.ctrl)
                elif direction == 'Right':
                    self.mouse.move(int(x + x1 - 1), int(y + 15))
                    self.mouse.drag((int(x + x1 - 1), int(y + 15)), (int(x+x1-1 + int(float(ratio) * x1)), int(y + 15)))
                    self.keyboard.release(self.keyboard.key.ctrl)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Timeline] Select a clip on timeline')
    def select_timeline_media(self, track_index, clip_index):
        try:
            if not self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]):
                logger("Can't find the target clip on timeline")
                raise Exception("Can't find the target clip on timeline")
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def select_multiple_timeline_media(self, media1_track_index, media1_clip_index, media2_track_index, media2_clip_index):
        '''
        e.g. first audio track's second clip = [{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 1}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}]
        '''
        try:
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': media1_track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': media1_clip_index}], [{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': media2_track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': media2_clip_index}]):
                logger("Can't find the target clip 1 on timeline")
                raise Exception("Can't find the target clip 1 on timeline")
            time.sleep(DELAY_TIME)
            self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': media1_track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': media1_clip_index}])
            self.keyboard.press(self.keyboard.key.cmd)
            if not self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': media2_track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': media2_clip_index}]):
                logger("Can't find the target clip 2 on timeline")
                raise Exception("Can't find the target clip 2 on timeline")
            self.keyboard.release(self.keyboard.key.cmd)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def edit_track_manager_add_track(self, video_nums, audio_nums, effect_nums):
        try:
            if not self.exist(L.timeline_operation.track_manager_dialog):
                logger("Can't find the track manager")
                raise Exception(f'Exception occurs. log={e}')
            self.exist(L.timeline_operation.track_manager.video_track).AXValue = str(video_nums)
            self.exist(L.timeline_operation.track_manager.audio_track).AXValue = str(audio_nums)
            self.exist(L.timeline_operation.track_manager.effect_track).AXValue = str(effect_nums)
            if str(video_nums) == self.exist(L.timeline_operation.track_manager.video_track).AXValue and str(audio_nums) == self.exist(L.timeline_operation.track_manager.audio_track).AXValue and str(effect_nums) == self.exist(L.timeline_operation.track_manager.effect_track).AXValue:
                print("True")
            else:
                logger('video/audio/effect nums exceeds the maximum')
                raise Exception('video/audio/effect nums exceeds the maximum')
            time.sleep(DELAY_TIME)
            self.exist_click(L.timeline_operation.track_manager_ok)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def edit_track_manager_add_track_position(self, video_nums, video_pos, audio_nums, audio_pos, effect_nums, effect_pos):
        try:
            if not self.exist(L.timeline_operation.track_manager_dialog):
                logger("Can't find the track manager")
                raise Exception("Can't find the track manager")
            self.exist(L.timeline_operation.track_manager.video_track).AXValue = str(video_nums)
            self.exist(L.timeline_operation.track_manager.audio_track).AXValue = str(audio_nums)
            self.exist(L.timeline_operation.track_manager.effect_track).AXValue = str(effect_nums)

            self.exist_click(L.timeline_operation.track_manager.video_position_drop_down_menu)
            self.exist_click([{'AXIdentifier': 'IDC_TRACKMANAGER_BTN_ADDVIDEOTRACK_POS'}, {'AXRole': 'AXStaticText', 'AXValue': video_pos}])
            self.exist_click(L.timeline_operation.track_manager.audio_position_drop_down_menu)
            self.exist_click([{'AXIdentifier': 'IDC_TRACKMANAGER_BTN_ADDAUDIOTRACK_POS'}, {'AXRole': 'AXStaticText', 'AXValue': audio_pos}])
            self.exist_click([{'AXIdentifier': 'IDC_TRACKMANAGER_BTN_ADDEFFECTTRACK_POS'}, {'AXRole': 'AXStaticText', 'AXValue': effect_pos}])

            if str(video_nums) == self.exist(L.timeline_operation.track_manager.video_track).AXValue and str(audio_nums) == self.exist(L.timeline_operation.track_manager.audio_track).AXValue and str(effect_nums) == self.exist(L.timeline_operation.track_manager.effect_track).AXValue:
                print("True")
            else:
                logger('video/audio/effect nums exceeds the maximum')
                raise Exception('video/audio/effect nums exceeds the maximum')
            time.sleep(DELAY_TIME)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_track_manager_ok(self):
        try:
            # Track Manager window > Click OK button
            self.exist_click(L.timeline_operation.track_manager_ok)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_track_manager_cancel(self):
        try:
            # Track Manager window > Click Cancel button
            self.exist_click(L.timeline_operation.track_manager_cancel)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_rightclickmenu_link_unlink_videoandaudio(self, track_index, clip_index):
        '''
        e.g. first video track's second clip = [{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}]
        '''
        try:
            if not self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]):
                logger("Can't find the target clip on timeline")
                raise Exception(f'Exception occurs. log={e}')
            time.sleep(DELAY_TIME)
            self.right_click()
            self.select_right_click_menu('Link/Unlink Video and Audio')

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def exist_transition_effect(self, track_index, clip_index):
        '''
        e.g. first audio track's second clip = [{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 1}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}]
        '''
        try:
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]):
                logger("Can't find the clip on timeline")
                raise Exception("Can't find the clip on timeline")
            time.sleep(DELAY_TIME)
            transition_effect = [[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}], {'AXIdentifier': 'IDC_VIDEOCELL_PRE_TRANSITION', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}]
            if not self.exist(transition_effect):
                logger("This clip didn't exist the transition effect")
                return False
            else:
                return True

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    def snapshot_timeline_videoclip(self, track_index, clip_index):
        '''
        e.g. first audio track's second clip = [{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 1}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}]
        '''
        try:
            if not self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]):
                logger("Can't click the clip on timeline")
                raise Exception("Can't click the clip on timeline")
            time.sleep(DELAY_TIME)
            video_clip_snapshot = self.snapshot([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}])
            #print(f'{video_clip_snapshot}')
            return video_clip_snapshot

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    def get_video_trackname(self, track_index):
        '''
        e.g. track_no (first video track) = [{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': 0}]
        '''
        try:
            if not self.find([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}]):
                logger("Can't find the target track")
                raise Exception("Can't find the target track")
            track_name = [[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}], {'AXIdentifier': 'IDC_TRACKHEADER_ALIAS'}]
            if not self.exist(track_name):
                logger("Didn't show the track name")
                raise Exception("Didn't show the track name")
            target_track_name = self.exist(track_name).AXValue
            return target_track_name
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    def edit_video_trackname(self, track_index, name):
        '''
        e.g. track_no (first video track) = [{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': 0}]
        '''
        try:
            track_name = [[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}], {'AXIdentifier': 'IDC_TRACKHEADER_ALIAS'}]
            self.exist(track_name).AXValue = str(name)

            if str(name) == self.exist(track_name).AXValue:
                return True
            else:
                return False
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    @step('[Action][Timeline Operation] Set the track lock/unlock')
    def edit_specific_video_track_set_lock_unlock(self, track_index):
        '''
        e.g. track_no (first video track) = [{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': 0}]
        '''
        try:
            lock_icon = [[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}], {'AXIdentifier': 'IDC_TRACKHEADER_LOCK_BTN'}]
            if not self.exist_click(lock_icon):
                logger("Can't click the lock icon")
                raise Exception("Can't click the lock icon")
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def edit_specific_audio_track_set_lock_unlock(self, track_index):
        '''
        e.g. track_no (first audio track) = [{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': 1}]
        '''
        try:
            lock_icon = [[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}], {'AXIdentifier': 'IDC_TRACKHEADER_LOCK_BTN'}]
            if not self.exist_click(lock_icon):
                logger("Can't click the lock icon")
                raise Exception("Can't click the lock icon")
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def edit_specific_effect_track_set_lock_unlock(self, track_index):
        '''
        e.g. track_no (first audio track) = [{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': 1}]
        '''
        try:
            lock_icon = [[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}], {'AXIdentifier': 'IDC_TRACKHEADER_LOCK_BTN'}]
            if not self.exist_click(lock_icon):
                logger("Can't click the lock icon")
                raise Exception("Can't click the lock icon")
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def drag_to_show_track_name(self):
        try:
            if not self.exist(L.timeline_operation.timeline_splitter):
                logger("No splitter show up")
                raise Exception("No splitter show up")
            self.exist(L.timeline_operation.timeline_splitter).AXValue = int(277)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    def drag_to_hide_track_name(self):
        try:
            if not self.exist(L.timeline_operation.timeline_splitter):
                logger("No splitter show up")
                raise Exception("No splitter show up")
            self.exist(L.timeline_operation.timeline_splitter).AXValue = int(120)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    def right_click_menu_add_clip_marker(self, track_index, clip_index):
        '''
        e.g. first video track's second clip = [{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}]
        '''
        # option: -1-None, 0-Add Clip Marker, 1-Remove Selected Clip Marker,
        # 2-Remove All Clip Markers, 3-Edit Clip Marker, 4-
        # Dock/Undock Timeline Window, 5-Reset All Undocked Windows
        try:
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]):
               logger("Can't find the target clip on timeline")
               raise Exception("Can't find the target clip on timeline")
            targer_clip = [{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]
            self.exist_click(targer_clip)
            track1_id = self.exist(L.timeline_operation.timeline_video_track1)
            _, y = track1_id.AXPosition
            x, _ = self.exist(targer_clip).AXPosition
            self.mouse.move(int(x + 15), int(y - 25))
            self.right_click()
            self.mouse.move(int(x + 25), int(y - 25))
            self.mouse.click(times=1)
            #self.timeline_clip_marker_track_menu_selected_clip(clip_locator= targer_clip, option=0)
            #clip_pos = self.exist(clip_locator).AXPosition
            #self.mouse.move(int(clip_pos[0] + 5), int(715))
            #self.right_click()
            #self.select_right_click_menu('Add Clip Marker')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def right_click_menu_clip_marker_track_selected_clip(self, track_index, clip_index):
        '''
        e.g. first video track's second clip = [{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': 1}]
        '''
        try:
             if not self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]):
                 logger("Can't find the target clip on timeline")
                 raise Exception("Can't find the target clip on timeline")
             clip_pos = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]).AXPosition
             track1_id = self.exist(L.timeline_operation.timeline_video_track1)
             _, y = track1_id.AXPosition
             self.mouse.move(int(clip_pos[0] + 5), int(y-25))
             self.right_click()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    def right_click_menu_clip_marker_track_unselected_clip(self):
        try:
            if self.exist(L.timeline_operation.timeline_vertical_scroll_bar):
                self.exist(L.timeline_operation.timeline_vertical_scroll_bar).AXValue = float(0)
            if not self.exist_click(L.timeline_operation.timeline_video_track1):
               logger("Can't click the first video track id on timeline")
               raise Exception("Can't click the first video track id on timeline")
            id_pos = self.exist(L.timeline_operation.timeline_video_track1).AXPosition
            self.mouse.move(int(id_pos[0] + 300), int(id_pos[1] - 27))
            self.right_click()

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    def right_click_menu_clip_marker_track_dock_undock_timeline_window(self):
        # option: -1-None, 0-Add Clip Marker, 1-Remove Selected Clip Marker,
        # 2-Remove All Clip Markers, 3-Edit Clip Marker, 4-Dock/Undock Timeline Window, 5-Reset All Undocked Windows
        try:
            self.timeline_clip_marker_track_menu_unselected_clip(option=4)
            #track1_id = self.exist(L.timeline_operation.timeline_video_track1)
            #x, y = track1_id.AXPosition
            #self.mouse.move(int(x + 150), int(y - 25))
            #self.right_click()
            #self.mouse.move(int(x + 160), int(y + 65))
            #self.mouse.click(times=1)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    def right_click_menu_clip_marker_track_reset_all_undocked_window(self):
        # option: -1-None, 0-Add Clip Marker, 1-Remove Selected Clip Marker,
        # 2-Remove All Clip Markers, 3-Edit Clip Marker, 4-Dock/Undock Timeline Window, 5-Reset All Undocked Windows
        try:
            self.timeline_clip_marker_track_menu_unselected_clip(option=5)
            #track1_id = self.exist(L.timeline_operation.timeline_video_track1)
            #x, y = track1_id.AXPosition
            #self.mouse.move(int(x + 150), int(y - 25))
            #self.right_click()
            #self.mouse.move(int(x + 160), int(y + 85))
            #self.mouse.click(times=1)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    def click_right_click_menu_remove_all_clips_marker(self):
         # option: -1-None, 0-Add Clip Marker, 1-Remove Selected Clip Marker,
         # 2-Remove All Clip Markers, 3-Edit Clip Marker, 4-Dock/Undock Timeline Window, 5-Reset All Undocked Windows
        try:
            self.timeline_clip_marker_track_menu_unselected_clip(option=2)
            #track1_id = self.exist(L.timeline_operation.timeline_video_track1)
            #x, y = track1_id.AXPosition
            #self.mouse.move(int(x+150), int(y-25))
            #self.right_click()
            #self.mouse.move(int(x+160), int(y+15))
            #self.mouse.click(times=1)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    def drag_media_to_timeline_overlay_clip(self, strmedia, clip_index, index):
        # index: -1-None, 0-Overwrite, 1-Insert,
        # 2-Insert and Move All Clips, 3-Crossfade, 4-Replace
        try:
            clip = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}])
            x1, y1 = clip.AXPosition
            self.select_library_icon_view_media(strmedia)
            self.hover_library_media(strmedia)
            x, y = self.mouse.position()
            self.mouse.drag((x, y), (int(x1+10), int(y1+10)))
            self.timeline_overlay_media_menu(option=index)
            #if index == 0:
             #   self.mouse.move(int(x1+20), int(y1+10))
             #   self.mouse.click(times=1)
            #elif index == 1:
             #   self.mouse.move(int(x1 + 20), int(y1 + 35))
             #   self.mouse.click(times=1)
            #elif index == 2:
             #   self.mouse.move(int(x1 + 20), int(y1 + 60))
             #   self.mouse.click(times=1)
            #elif index == 3:
             #   self.mouse.move(int(x1 + 20), int(y1 + 85))
             #   self.mouse.click(times=1)
            #elif index == 4:
             #   self.mouse.move(int(x1 + 20), int(y1 + 110))
              #  self.mouse.click(times=1)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    def drag_media_to_timeline_overlay_clip_to_specific_position(self, strmedia, clip_index, index, position):
        # index: -1-None, 0-Overwrite, 1-Insert,
        # 2-Insert and Move All Clips, 3-Crossfade, 4-Replace
        try:
            clip = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': 0}, {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}])
            x1, y1 = clip.AXPosition
            w, h = clip.AXSize
            self.select_library_icon_view_media(strmedia)
            self.hover_library_media(strmedia)
            x, y = self.mouse.position()
            if position == 'Front':
                self.mouse.drag((x,y), (int(x1+3), int(y1+10)))
                self.timeline_overlay_media_menu(option=index)
            elif position == 'Middle':
                self.mouse.drag((x,y), (int(x1+3+0.5*w), int(y1+10)))
                self.timeline_overlay_media_menu(option=index)
            elif position == 'Last':
                self.mouse.drag((x,y), (int(x1+w-8), int(y1+10)))
                self.timeline_overlay_media_menu(option=index)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')


    def set_add_tracks_video(self, number, position):
        try:
            #if self.exist(L.timeline_operation.timeline_vertical_scroll_bar):
             #  self.exist(L.timeline_operation.timeline_vertical_scroll_bar).AXValue = float(0)
            if not self.exist(L.timeline_operation.timeline_video_track1):
                logger("Can't find the track table")
                raise Exception(f'Exception occurs. log={e}')
            else:
                self.click(L.timeline_operation.timeline_track1)

            self.right_click()
            self.select_right_click_menu('Add Tracks...')
            if not self.find(L.timeline_operation.track_manager_dialog):
                logger("Can't find the track manager")
                raise Exception("Can't find the track manager")
            self.exist(L.timeline_operation.track_manager.video_track).AXValue = str(number)
            self.exist(L.timeline_operation.track_manager.audio_track).AXValue = str(0)
            self.exist_click(L.timeline_operation.track_manager.video_position_drop_down_menu)
            self.exist_click([{'AXIdentifier': 'IDC_TRACKMANAGER_BTN_ADDVIDEOTRACK_POS'}, {'AXRole': 'AXStaticText', 'AXValue': position}])
            self.exist_click(L.timeline_operation.track_manager_ok)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    def set_add_tracks_audio(self, number, position):
        try:
            #if self.exist(L.timeline_operation.timeline_vertical_scroll_bar):
             #   self.exist(L.timeline_operation.timeline_vertical_scroll_bar).AXValue = float(0)
            if not self.exist(L.timeline_operation.timeline_video_track1):
                logger("Can't find the track table")
                raise Exception("Can't find the track table")
            else:
                self.click(L.timeline_operation.timeline_track1)

            self.right_click()
            self.select_right_click_menu('Add Tracks...')
            if not self.find(L.timeline_operation.track_manager_dialog):
                logger("Can't find the track manager")
                raise Exception("Can't find the track manager")
            self.exist(L.timeline_operation.track_manager.video_track).AXValue = str(0)
            self.exist(L.timeline_operation.track_manager.audio_track).AXValue = str(number)
            self.exist_click(L.timeline_operation.track_manager.audio_position_drop_down_menu)
            self.exist_click([{'AXIdentifier': 'IDC_TRACKMANAGER_BTN_ADDAUDIOTRACK_POS'}, {'AXRole': 'AXStaticText', 'AXValue': position}])
            self.exist_click(L.timeline_operation.track_manager_ok)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def set_add_tracks_effect(self, number, position):
        try:
            #if self.exist(L.timeline_operation.timeline_vertical_scroll_bar):
                #self.exist(L.timeline_operation.timeline_vertical_scroll_bar).AXValue = float(0)
            if not self.exist(L.timeline_operation.timeline_video_track1):
                logger("Can't find the track table")
                raise Exception("Can't find the track table")
            else:
                self.click(L.timeline_operation.timeline_track1)

            self.right_click()
            self.select_right_click_menu('Add Tracks...')
            if not self.find(L.timeline_operation.track_manager_dialog):
                logger("Can't find the track manager")
                raise Exception("Can't find the track manager")
            self.exist(L.timeline_operation.track_manager.video_track).AXValue = str(0)
            self.exist(L.timeline_operation.track_manager.audio_track).AXValue = str(0)
            self.exist(L.timeline_operation.track_manager.effect_track).AXValue = str(number)
            self.exist_click(L.timeline_operation.track_manager.effect_position_drop_down_menu)
            time.sleep(DELAY_TIME*2)
            self.exist_click([{'AXIdentifier': 'IDC_TRACKMANAGER_BTN_ADDEFFECTTRACK_POS'}, {'AXRole': 'AXStaticText', 'AXValue': position}])
            self.exist_click(L.timeline_operation.track_manager_ok)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    def get_specific_video_track_lock_status(self, track_index):
        option_1 = 'Lock'
        option_2 = 'Unlock'
        self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'index': track_index}])
        self.right_click()
        if self.find(L.timeline_operation.timeline_add_track):
            self.exist_click(L.timeline_operation.timeline_vertical_scroll_bar)
            return option_2
        else:
            return option_1

    def get_specific_audio_track_lock_status(self, track_index):
        option_1 = 'Lock'
        option_2 = 'Unlock'
        self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'index': track_index}])
        self.right_click()
        if self.find(L.timeline_operation.timeline_add_track):
            self.exist_click(L.timeline_operation.timeline_vertical_scroll_bar)
            return option_2
        else:
            return option_1

    def get_specific_effect_track_lock_status(self, track_index):
        option_1 = 'Lock'
        option_2 = 'Unlock'
        self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'index': track_index}])
        self.right_click()
        if self.find(L.timeline_operation.timeline_add_track):
            self.exist_click(L.timeline_operation.timeline_vertical_scroll_bar)
            return option_2
        else:
            return option_1

    def click_timeline_track_visible_button(self, track_index):
        # video track 1 : track_index = 0, audio track 1 : track_index = 1
        # video track 2 : track_index = 2, audio track 2 : track_index = 3
        # video track 2 : track_index = 4, audio track 3 : track_index = 5
        self.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}], {'AXIdentifier': 'IDC_TRACKHEADER_VISIBLE_BTN'}])


    def edit_specific_video_track_set_enable(self, track_index, option):
        # 0-disable 1-enable
        try:
            if not self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}]):
                logger("Can't find the target track")
                raise Exception("Can't find the target track")
            current_status = self.snapshot([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}], {'AXIdentifier': 'IDC_TRACKHEADER_VISIBLE_BTN'}])
            self.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}], {'AXIdentifier': 'IDC_TIMELINE_LABEL_TRACKID'}])
            self.right_click()
            self.select_right_click_menu('Enable Selected Track Only')
            enable_status = self.snapshot([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}], {'AXIdentifier': 'IDC_TRACKHEADER_VISIBLE_BTN'}])
            print(f'{current_status= }, {enable_status= }')
            status_compare = self.compare(current_status, enable_status, similarity=0.99)
            if option == 1 and status_compare:
                logger("target track is enabled")
            elif option == 1 and not status_compare:
                logger("target track is enabled now")
            elif option == 0 and status_compare:
                self.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}], {'AXIdentifier': 'IDC_TRACKHEADER_VISIBLE_BTN'}])
            elif option == 0 and not status_compare:
                self.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}], {'AXIdentifier': 'IDC_TRACKHEADER_VISIBLE_BTN'}])
            else:
                logger("Failed to judge the track status")
                raise Exception("Failed to judge the track status")
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    def edit_specific_track_set_enable(self, track_index, option):
        # 0-disable 1-enable
        try:
            if not self.exist_click(
                    [{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}]):
                logger("Can't find the target track")
                raise Exception(f'Exception occurs. log={e}')
            current_status = self.snapshot(
                [[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}],
                 {'AXIdentifier': 'IDC_TRACKHEADER_VISIBLE_BTN'}])
            self.exist_click(
                [[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}],
                 {'AXIdentifier': 'IDC_TIMELINE_LABEL_TRACKID'}])
            self.right_click()
            self.select_right_click_menu('Enable Selected Track Only')
            enable_status = self.snapshot(
                [[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}],
                 {'AXIdentifier': 'IDC_TRACKHEADER_VISIBLE_BTN'}])
            print(f'{current_status= }, {enable_status= }')
            status_compare = self.compare(current_status, enable_status, similarity=0.99)
            if option == 1 and status_compare:
                logger("target track is enabled")
            elif option == 1 and not status_compare:
                logger("target track is enabled now")
            elif option == 0 and status_compare:
                self.exist_click(
                    [[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}],
                     {'AXIdentifier': 'IDC_TRACKHEADER_VISIBLE_BTN'}])
            elif option == 0 and not status_compare:
                self.exist_click(
                    [[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}],
                     {'AXIdentifier': 'IDC_TRACKHEADER_VISIBLE_BTN'}])
            else:
                logger("Failed to judge the track status")
                raise Exception("Failed to judge the track status")
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    def edit_specific_audio_track_set_enable(self, track_index, option):
        # 0-disable 1-enable
        try:
            if not self.exist_click(
                    [{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}]):
                logger("Can't find the target track")
                raise Exception(f'Exception occurs. log={e}')
            current_status = self.snapshot(
                [[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}],
                 {'AXIdentifier': 'IDC_TRACKHEADER_VISIBLE_BTN'}])
            self.exist_click(
                [[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}],
                 {'AXIdentifier': 'IDC_TIMELINE_LABEL_TRACKID'}])
            self.right_click()
            self.select_right_click_menu('Enable Selected Track Only')
            enable_status = self.snapshot(
                [[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}],
                 {'AXIdentifier': 'IDC_TRACKHEADER_VISIBLE_BTN'}])
            print(f'{current_status= }, {enable_status= }')
            status_compare = self.compare(current_status, enable_status, similarity=0.99)
            if option == 1 and status_compare:
                logger("target track is enabled")
            elif option == 1 and not status_compare:
                logger("target track is enabled now")
            elif option == 0 and status_compare:
                self.exist_click(
                    [[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}],
                     {'AXIdentifier': 'IDC_TRACKHEADER_VISIBLE_BTN'}])
            elif option == 0 and not status_compare:
                self.exist_click(
                    [[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}],
                     {'AXIdentifier': 'IDC_TRACKHEADER_VISIBLE_BTN'}])
            else:
                logger("Failed to judge the track status")
                raise Exception("Failed to judge the track status")
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    def edit_specific_effect_track_set_enable(self, track_index, option):
        # 0-disable 1-enable
        try:
            if not self.exist_click(
                    [{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}]):
                logger("Can't find the target track")
                raise Exception(f'Exception occurs. log={e}')
            current_status = self.snapshot(
                [[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}],
                 {'AXIdentifier': 'IDC_TRACKHEADER_VISIBLE_BTN'}])
            self.exist_click(
                [[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}],
                 {'AXIdentifier': 'IDC_TIMELINE_LABEL_TRACKID'}])
            self.right_click()
            self.select_right_click_menu('Enable Selected Track Only')
            enable_status = self.snapshot(
                [[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}],
                 {'AXIdentifier': 'IDC_TRACKHEADER_VISIBLE_BTN'}])
            print(f'{current_status= }, {enable_status= }')
            status_compare = self.compare(current_status, enable_status, similarity=0.99)
            if option == 1 and status_compare:
                logger("target track is enabled")
            elif option == 1 and not status_compare:
                logger("target track is enabled now")
            elif option == 0 and status_compare:
                self.exist_click(
                    [[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}],
                     {'AXIdentifier': 'IDC_TRACKHEADER_VISIBLE_BTN'}])
            elif option == 0 and not status_compare:
                self.exist_click(
                    [[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}],
                     {'AXIdentifier': 'IDC_TRACKHEADER_VISIBLE_BTN'}])
            else:
                logger("Failed to judge the track status")
                raise Exception("Failed to judge the track status")
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    def get_specific_video_track_enable_status(self, track_index):
        try:
            if not self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}]):
                logger("Can't find the target track")
                raise Exception("Can't find the target track")
            option_1 = 'Enable'
            option_2 = 'Disable'
            current_status = self.snapshot([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}], {'AXIdentifier': 'IDC_TRACKHEADER_VISIBLE_BTN'}])
            self.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}], {'AXIdentifier': 'IDC_TIMELINE_LABEL_TRACKID'}])
            self.right_click()
            self.select_right_click_menu('Enable Selected Track Only')
            enable_status = self.snapshot([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}], {'AXIdentifier': 'IDC_TRACKHEADER_VISIBLE_BTN'}])
            print(f'{current_status= }, {enable_status= }')
            status_compare = self.compare(current_status, enable_status, similarity=0.99)
            if status_compare:
                return option_1
            else:
                return option_2
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    def get_specific_audio_track_enable_status(self, track_index):
        try:
            if not self.exist_click(
                    [{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}]):
                logger("Can't find the target track")
                raise Exception("Can't find the target track")
            option_1 = 'Enable'
            option_2 = 'Disable'
            current_status = self.snapshot(
                [[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}],
                 {'AXIdentifier': 'IDC_TRACKHEADER_VISIBLE_BTN'}])
            self.exist_click(
                [[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}],
                 {'AXIdentifier': 'IDC_TIMELINE_LABEL_TRACKID'}])
            self.right_click()
            self.select_right_click_menu('Enable Selected Track Only')
            enable_status = self.snapshot(
                [[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}],
                 {'AXIdentifier': 'IDC_TRACKHEADER_VISIBLE_BTN'}])
            print(f'{current_status= }, {enable_status= }')
            status_compare = self.compare(current_status, enable_status, similarity=0.99)
            if status_compare:
                return option_1
            else:
                return option_2
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    def get_specific_effect_track_enable_status(self, track_index):
        try:
            self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}])
            option_1 = 'Enable'
            option_2 = 'Disable'
            current_status = self.snapshot([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}], {'AXIdentifier': 'IDC_TRACKHEADER_VISIBLE_BTN'}])
            self.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}], {'AXIdentifier': 'IDC_TIMELINE_LABEL_TRACKID'}])
            self.right_click()
            self.select_right_click_menu('Enable Selected Track Only')
            enable_status = self.snapshot([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD'}, {'AXRole': 'AXRow', 'index': track_index}], {'AXIdentifier': 'IDC_TRACKHEADER_VISIBLE_BTN'}])
            print(f'{current_status= }, {enable_status= }')
            status_compare = self.compare(current_status, enable_status, similarity=0.99)
            if status_compare:
                return option_1
            else:
                return option_2
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    def highlight_transition_effect(self, track_index, clip_index, mode):
        '''
        mode: 0- Prefix, 1- Postfix, 2- Cross, 3- Overlay
        '''
        try:
            if mode == 0:
                if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                   {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                                   {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]):
                    logger("Can't find the target clip on the track")
                    raise Exception("Can't find the target clip on the track")
                self.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                   {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                                   {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}],
                                  {'AXIdentifier': 'IDC_VIDEOCELL_PRE_TRANSITION', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
                return True
            elif mode == 1:
                if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                   {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                                   {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]):
                    logger("Can't find the target clip on the track")
                    raise Exception("Can't find the target clip on the track")
                self.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                   {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                                   {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}],
                                   {'AXIdentifier': 'IDC_VIDEOCELL_POST_TRANSITION', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
                return True
            elif mode == 2:
                if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                   {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                                   {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]):
                    logger("Can't find the target clip on the track")
                    raise Exception("Can't find the target clip on the track")
                self.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                   {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                                   {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}],
                                   {'AXIdentifier': 'IDC_VIDEOCELL_POST_TRANSITION', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
                return True
            elif mode == 3:
                if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                   {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                                   {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]):
                   logger("Can't find the target clip on the track")
                   raise Exception("Can't find the target clip on the track")
                self.exist_click([[{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                   {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                                   {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}],
                                   {'AXIdentifier': 'IDC_VIDEOCELL_POST_TRANSITION', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}])
                return True
            else:
                return False
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    def get_clips_amount(self, track_index, sleep_time=5):
        # sleep_time = 5 (Default)
        # parameter Description : If you want to get more time to generate SVRT file, can assign sleep time

        self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}])
        self.right_click()
        if not self.exist({'AXIdentifier': 'menuShowSVRTTrack'}).AXMenuItemMarkChar == str("✓"):
            self.select_right_click_menu('Show SVRT Track')
            time.sleep(DELAY_TIME*sleep_time)
        self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                          {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}])
        self.right_click()
        if not self.exist({'AXIdentifier': 'menuShowSubtitleTrack'}).AXMenuItemMarkChar == str("✓"):
            self.select_right_click_menu('Show Subtitle Track')
        self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                          {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}])
        self.right_click()
        if not self.exist({'AXIdentifier': 'menuShowClipMarkerTrack'}).AXMenuItemMarkChar == str("✓"):
            self.select_right_click_menu('Show Clip Marker Track')
        self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                          {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}])
        track = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}, {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}, {'AXIdentifier': 'IDC_TIMELINE_COLLECTIONVIEW_VIDEOTRACK'}, {'AXRole': 'AXList', 'AXOrientation': 'AXHorizontalOrientation'}])
        amount = len(track.AXChildren)
        self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                          {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}])
        self.right_click()
        if self.exist({'AXIdentifier': 'menuShowSVRTTrack'}).AXMenuItemMarkChar == str("✓"):
            self.select_right_click_menu('Show SVRT Track')
        self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                          {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}])
        self.right_click()
        if self.exist({'AXIdentifier': 'menuShowSubtitleTrack'}).AXMenuItemMarkChar == str("✓"):
            self.select_right_click_menu('Show Subtitle Track')
        self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                          {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}])
        self.right_click()
        if self.exist({'AXIdentifier': 'menuShowClipMarkerTrack'}).AXMenuItemMarkChar == str("✓"):
            self.select_right_click_menu('Show Clip Marker Track')
        self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                          {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index}])
        return amount

    def deselect_clip(self, track_index, last_clip_index, movement):
        last_clip = self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                   {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                                   {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': last_clip_index}])
        x, y = last_clip.AXPosition
        w, _ = last_clip.AXSize
        self.mouse.click(int(x+w+movement), int(y+20))

    def snapshot_timeline_render_clip(self, track_index, clip_index, file_name=None):
        '''
        First, point out the clip (which one to take a snapshot)
        :parameter
        track_index = 0 (video track 1), 1 (audio track 1), 2 (video track 2), ...
        clip_index = 0 (1st clip of this track), 1 (2nd clip), ...
        file_name = "the saved file name" when snapshot ready
        '''
        try:
            if not self.exist([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                     {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                                     {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}]):
                logger("Can't find the target clip on timeline")
                return None
            else:
                elem = self.exist_click([{'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'},
                                     {'AXRole': 'AXRow', 'AXRoleDescription': 'table row', 'index': track_index},
                                     {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup', 'index': clip_index}])
                # target clip of timeline info:
                w, h = elem.AXSize

                # Timeline indicator element:
                elem_timeline_indicator = self.get_position(locator=L.timeline_operation.timeline_indicator)

                # Only snapshot timeline "render preview region" (green area)
                return self.screenshot(file_name=file_name, w=w+elem_timeline_indicator['w']/2,
                                       x=elem_timeline_indicator['x'], y=elem_timeline_indicator['y'],
                                       h=elem_timeline_indicator['h'])
        except Exception as e:
            logger(f"[Warning] : {e}")
            return None

    def right_click_menu_CopyTrackContent_to(self, track_index, strName , Option):
        '''
        e.g. right_click_menu_CopyTrackContent_to(1, 'Above track 3', 'OK')

        :parameter
        track_index = 1 (track 1), 2 (track 2), ...
        strName = Above track 1, Above track 2, ...
        Option = Cancel, OK
        '''
        try:
            self.timeline_select_track(track_index)
            time.sleep(DELAY_TIME)
            self.right_click()
            self.select_right_click_menu('Copy Track Content to...')
            time.sleep(DELAY_TIME)

            if not self.exist(L.timeline_operation.copy_track_content.main_window):
                raise Exception(f'Exception occurs. log={e}')

            locator_combobox = L.timeline_operation.copy_track_content.cbx_menu
            locator_option = {'AXRoleDescription': 'text', 'AXValue': strName}
            select_combobox_item(self, locator_combobox, locator_option)

            time.sleep(DELAY_TIME)
            item = eval(f'L.timeline_operation.copy_track_content.btn_{Option}')
            self.click(item)
            return True
        except Exception as e:
            logger(f"[Warning] : {e}")
            raise Exception(f'Exception occurs. log={e}')

    def move_mouse_to_CTI_position(self, track_index, left_position=False):
        '''
        :parameter
        track_index = 0 (video track 1), 1 (audio track 1), 2 (video track 2), ...
        '''
        try:
            # Find target track position
            els_track = self.exist_elements(L.main.timeline.track_unit)
            logger(els_track)
            track_x, track_y = els_track[track_index].AXPosition

            # Timeline indicator element:
            elem_timeline_indicator = self.get_position(locator=L.timeline_operation.timeline_indicator)
            if left_position:
                new_x = elem_timeline_indicator['x']-10
            else:
                new_x = elem_timeline_indicator['x']+10

            new_y = track_y+5

            # move mouse to new position (new_x, new_y)
            self.mouse.move(new_x, new_y)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f"[Warning] : {e}")
            raise Exception(f'Exception occurs. log={e}')

    def right_click_menu_MoveTrackContent_to(self, track_index, strName , Option):
        '''
        e.g. right_click_menu_MoveTrackContent_to(1, 'Above track 3', 'OK')

        :parameter
        track_index = 1 (track 1), 2 (track 2), ...
        strName = Above track 1, Below track 3, ...
        Option = Cancel, OK
        '''
        try:
            self.timeline_select_track(track_index)
            time.sleep(DELAY_TIME)
            self.right_click()
            self.select_right_click_menu('Move Track Content to...')
            time.sleep(DELAY_TIME)

            if not self.exist(L.timeline_operation.move_track_content.main_window):
                raise Exception(f'Exception occurs. log={e}')

            locator_combobox = L.timeline_operation.move_track_content.cbx_menu
            locator_option = {'AXRoleDescription': 'text', 'AXValue': strName}
            select_combobox_item(self, locator_combobox, locator_option)

            time.sleep(DELAY_TIME)
            item = eval(f'L.timeline_operation.move_track_content.btn_{Option}')
            self.click(item)
            return True
        except Exception as e:
            logger(f"[Warning] : {e}")
            raise Exception(f'Exception occurs. log={e}')

    def seek_timeline(self, amount_frame):
        return self.backdoor.seek_timeline(amount_frame)

    def right_click_range_select_menu(self, option_1, option_2=''):
        pos_mark_in = self.exist(L.timeline_operation.timeline_scale_left).AXPosition
        pos_mark_out = self.exist(L.timeline_operation.timeline_scale_right).AXPosition
        self.mouse.move(int((pos_mark_in[0]+pos_mark_out[0])/2), pos_mark_in[1]+60)
        time.sleep(DELAY_TIME)
        self.right_click()
        self.select_right_click_menu(option_1, option_2)
        time.sleep(DELAY_TIME)
        return True

    def set_range_markin_markout(self, frame_mark_in, frame_mark_out):
        return self.backdoor.set_range_select_time(frame_mark_in, frame_mark_out)

    def right_click_timecode_menu(self, option_1):
        self.click(L.timeline_operation.timeline_indicator)
        time.sleep(DELAY_TIME)
        self.right_click()
        self.select_right_click_menu(option_1)
        time.sleep(DELAY_TIME)
        return True

    def handle_keyframe_settings_dialog(self, do_not_show_again='no', option='ok'):
        try:
            message = self.exist(L.timeline_operation.keyframe_settings_warning.txt_message, timeout=30)
            if not message.AXValue.startswith('The current keyframe settings will be'):
                logger('cannot find keyframe settings warning message')
                raise Exception('cannot find keyframe settings warning message')
            logger('find message')
            if do_not_show_again == 'no':
                set_value = 0
            else:
                set_value = 1
            logger(set_value)
            if self.exist(L.timeline_operation.keyframe_settings_warning.cbx_dont_show_again).AXValue != set_value:
                new_x, new_y = self.exist(L.timeline_operation.keyframe_settings_warning.cbx_dont_show_again).AXPosition
                # move mouse to new position (new_x, new_y)
                self.mouse.move(new_x + 15, new_y + 4)
                self.mouse.click()

            btn_option = eval(f'L.timeline_operation.keyframe_settings_warning.btn_{option}')
            self.exist_click(btn_option)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    class Undock_Timeline(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def click_min_btn(self):
            try:
                if not self.exist_click(L.timeline_operation.undock_window.btn_min):
                    raise Exception(f'Exception occurs. log={e}')

                # verify step:
                if not self.exist(L.main.btn_show_minimized_window):
                    logger('Verify step: Error')
                    raise Exception(f'Exception occurs. log={e}')
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def click_zoom_btn(self):
            try:
                if not self.exist_click(L.timeline_operation.undock_window.btn_zoom):
                    raise Exception(f'Exception occurs. log={e}')
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def click_dock_btn(self):
            try:
                if not self.exist_click(L.timeline_operation.undock_window.btn_dock):
                    raise Exception(f'Exception occurs. log={e}')

                # verify step:
                if self.find(L.timeline_operation.undock_window.btn_zoom):
                    raise Exception(f'Exception occurs. log={e}')

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def click_show_timeline_window(self):
            try:
                if not self.exist_click(L.main.btn_show_minimized_window):
                    raise Exception(f'Exception occurs. log={e}')

                if not self.exist_click(L.main.btn_menu_timeline):
                    raise Exception(f'Exception occurs. log={e}')

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def check_timeline_window_minimize_status(self):
            # check toolbar Children amount = 8 (minimal status)
            check_child = self.exist(L.main.top_toolbar).AXChildren
            if len(check_child) == 8:
                return True
            else:
                logger(len(check_child))
                return False

    class Timeline_Marker(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def edit_timecode(self, no=1, bTick=1, timecode=0):
            # e.g. timeline_operation_page.timeline_marker.edit_timecode(no=1, bTick=1, timecode='00_00_17_21') [Can Tick/Untick + Edit timecode]
            #      timeline_operation_page.timeline_marker.edit_timecode(no=3, bTick=1) [Only Tick/Untick]

            find_chx_elem = self.exist(L.timeline_operation.edit_timeline_marker.cbx_no)
            index = no - 1

            find_timecode_elem = self.exist(L.timeline_operation.edit_timeline_marker.timecode_item)

            if find_chx_elem[index].AXTitle == str(no):
                locator_c = find_chx_elem[index]
                current_chx_value = find_chx_elem[index].AXValue

                # Tick/Untick checkbox
                if current_chx_value != bTick:
                    pos = find_chx_elem[index].AXPosition
                    self.mouse.move(pos[0]+2, pos[1]+2)
                    self.mouse.click()

                # Edit Timeocde
                if timecode != 0:
                    logger(find_timecode_elem[index].AXValue)
                    w, h = find_timecode_elem[index].AXSize
                    x, y = find_timecode_elem[index].AXPosition

                    pos_click = tuple(map(int, (x + w * 0.1, y + h * 0.5)))
                    self.mouse.click(*pos_click, times=2)
                    time.sleep(2)
                    self.left_click()
                    self.left_click()
                    self.left_click()
                    self.keyboard.send(timecode.replace("_", ""))
                    self.keyboard.enter()
            return True

        def edit_note(self, no=1, strnote=0):
            # timeline_operation_page.timeline_marker.edit_note(no=2, strnote='W$%^FGg456')
            index = no - 1
            find_note_elem = self.exist(L.timeline_operation.edit_timeline_marker.note_item)
            logger(find_note_elem[index].AXValue)

            if strnote != 0:
                pos = find_note_elem[index].AXPosition
                self.mouse.move(pos[0]+2, pos[1]+2)
                self.mouse.click(times=2)
                self.keyboard.send(strnote)
                self.keyboard.enter()
            return True

        def click_select_all(self):
            if self.exist_click(L.timeline_operation.edit_timeline_marker.btn_select_all):
                return True
            else:
                return False

        def click_deselect_all(self):
            if self.exist_click(L.timeline_operation.edit_timeline_marker.btn_deselect_all):
                return True
            else:
                return False

        def click_delete_selected(self):
            if self.exist_click(L.timeline_operation.edit_timeline_marker.btn_delete_selected):
                return True
            else:
                return False

        def click_ok(self):
            if self.exist_click(L.timeline_operation.edit_timeline_marker.btn_OK):
                return True
            elif self.exist_click(L.timeline_operation.edit_timeline_marker.btn_modify_OK):
                return True
            else:
                return False




















