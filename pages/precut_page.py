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

class Precut(Main_Page, BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def check_precut_preview(self, ground_truth_image, area):
        try:
            if not self.exist(L.precut.main_window):
                logger("No precut window in current view")
                raise Exception
            if area == 'designer window':
                designer_window = self.snapshot(L.precut.main_window)
                print(designer_window)
                result_verify = self.compare(ground_truth_image, designer_window, similarity=0.9)
                if result_verify:
                    return True
                else:
                    return False
            elif area == 'selected segments':
                selected_segments = self.snapshot(L.precut.multi_trim_selected_segment)
                print(selected_segments)
                result_verify = self.compare(ground_truth_image, selected_segments, similarity=0.95)
                if result_verify:
                    return True
                else:
                    return False
            elif area == 'thumbnail slider':
                thumbnail_slider = self.snapshot(L.precut.multi_trim_thumbnail_slider)
                print(thumbnail_slider)
                result_verify = self.compare(ground_truth_image, thumbnail_slider, similarity=0.95)
                if result_verify:
                    return True
                else:
                    return False
            elif area == 'in position thumbnail':
                in_position_thumbnail = self.snapshot(L.precut.single_trim_in_position_thumbnail)
                print(in_position_thumbnail)
                result_verify = self.compare(ground_truth_image, in_position_thumbnail, similarity=0.95)
                if result_verify:
                    return True
                else:
                    return False
            elif area == 'out position thumbnail':
                out_position_thumbnail = self.snapshot(L.precut.single_trim_out_position_thumbnail)
                print(out_position_thumbnail)
                result_verify = self.compare(ground_truth_image, out_position_thumbnail, similarity=0.95)
                if result_verify:
                    return True
                else:
                    return False
            else:
                logger('Input the wrong argument')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True


    def get_precut_title(self):
        try:
            if not self.exist(L.precut.main_window):
                logger("No precut window in current view")
                raise Exception
            title = self.exist(L.precut.main_window).AXTitle
            return title[9:]
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True
    
    @step('[Action][Precut] Click [Cancel] Button to leave [Precut] Window')
    def click_cancel(self):
        try:
            if not self.exist_click(L.precut.btn_cancel):
                raise Exception('Unable to find [Cancel] button in [Precut] window')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def get_precut_preview_timecode(self):
        try:
            if not self.exist(L.precut.precut_window_current_time):
                logger('Cannot find the timecode in precut preview window')
                raise Exception
            timecode = self.exist(L.precut.precut_window_current_time).AXValue
            return timecode
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Precut] Set Timecode')
    def set_precut_timecode(self, timecode):

        self.activate()
        elem = self.find(L.precut.precut_window_current_time)
        w, h = elem.AXSize
        x, y = elem.AXPosition

        pos_click = tuple(map(int, (x + w * 0.1, y + h * 0.5)))
        self.mouse.click(*pos_click)
        time.sleep(1)
        self.keyboard.send(timecode.replace("_", ""))
        self.keyboard.enter()

    @step('[Action][Precut] Switch [Trim Mode] in [Precut Window]')
    def edit_precut_switch_trim_mode(self, mode):
        if mode == 'Single':
            self.exist_click(L.precut.single_trim)
            return True
        elif mode == 'Multi':
            self.exist_click(L.precut.multi_trim)
            return True
        else:
            logger("Can't found the mode in precut window")
            raise Exception("Can't found the mode in precut window")

    def handle_changes_not_applied_want_continue(self):
        try:
            if not self.exist(L.precut.multi_trim_not_been_applied):
                logger("No [not applied...] msg in current window")
                raise Exception
            self.exist_click(L.precut.multi_trim_not_been_applied_ok)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def handle_save_change_before_leaving(self, option):
        '''
        option 0- Cancel, 1- No, 2- Yes
        '''
        if option == 0:
            self.exist_click(L.precut.save_before_leaving_cancel)
            return True
        elif option == 1:
            self.exist_click(L.precut.save_before_leaving_no)
            return True
        elif option == 2:
            self.exist_click(L.precut.save_before_leaving_yes)
            return True
        else:
            logger('Cannot find the option in this window')
            return False

    def edit_precut_single_trim_drag_slider(self, hour, minute, sec, min_sec):
        '''
        timecode = 'HH_MM_SS_mm'
        '''
        try:
            timecode = hour * 3600 + minute * 60 + sec * 30 + min_sec * 1
            self.exist(L.precut.single_trim_drag_slider).AXValue = int(timecode)
            precut_window_timecode = self.exist(L.precut.precut_window_current_time).AXValue
            print(precut_window_timecode)
            set_timecode = str(str(hour)+";"+str(minute)+";"+str(sec)+";"+str(min_sec))
            set_timecode0 = str('0'+str(hour)+';0'+str(minute)+';0'+str(sec)+';0'+str(min_sec))
            set_timecode1 = str('0'+str(hour)+';0'+str(minute)+';0'+str(sec)+';'+str(min_sec))
            set_timecode2 = str('0'+str(hour)+';0'+str(minute)+';'+str(sec)+';'+str(min_sec))
            set_timecode3 = str('0'+str(hour)+';'+str(minute)+';'+str(sec)+';'+str(min_sec))
            set_timecode4 = str(str(hour)+';0'+str(minute)+';0'+str(sec)+';0'+str(min_sec))
            set_timecode5 = str(str(hour)+';'+str(minute)+';0'+str(sec)+';0'+str(min_sec))
            set_timecode6 = str(str(hour)+';'+str(minute)+';'+str(sec)+';0'+str(min_sec))
            if set_timecode == precut_window_timecode:
                return True
            elif set_timecode0 == precut_window_timecode:
                return True
            elif set_timecode1 == precut_window_timecode:
                return True
            elif set_timecode2 == precut_window_timecode:
                return True
            elif set_timecode3 == precut_window_timecode:
                return True
            elif set_timecode4 == precut_window_timecode:
                return True
            elif set_timecode5 == precut_window_timecode:
                return True
            elif set_timecode6 == precut_window_timecode:
                return True
            else:
                return False
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True
    '''
    # occur depth bug (not page function bug) 
    def edit_precut_single_trim_drag_slider_yellow_left(self, duration_HH_MM_SS_mm):
        try:
            self.set_precut_timecode(duration_HH_MM_SS_mm)
            time.sleep(OPERATION_DELAY)
            # destination position
            pos = self.exist(L.precut.single_trim_drag_slider).AXPosition
            logger(pos)

            self.exist(L.precut.single_trim_drag_slider).AXValue = int(0)
            clip_start = self.exist(L.precut.yellow_left_slider)
            x, y = clip_start.AXPosition

            start_pos = [x+6, y+14]
            end_pos = [pos[0], y+14]
            self.mouse.move(x + 6, y + 14)
            self.mouse.drag(start_pos, end_pos)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True
    '''

    @step('[Action][Precut] Set [Single Trim Mark In]')
    def tap_single_trim_mark_in(self):
        try:
            if not self.exist(L.precut.single_trim_mark_in):
                logger("No [mark-in] btn in the window")
                raise Exception("No [mark-in] btn in the window")
            self.exist_click(L.precut.single_trim_mark_in)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Precut] Set [Single Trim Mark Out]')
    def tap_single_trim_mark_out(self):
        try:
            if not self.exist(L.precut.single_trim_mark_out):
                logger("No [mark-out] btn in the window")
                raise Exception("No [mark-out] btn in the window")
            self.exist_click(L.precut.single_trim_mark_out)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
    
    @step('[Action][Precut] Get [Single Trim] Duration')
    def get_precut_single_trim_duration(self):
        duration = self.exist(L.precut.single_trim_precut_duration).AXValue
        return duration

    def set_precut_single_trim_duration(self, duration):
        self.activate()
        elem = self.find(L.precut.single_trim_precut_duration)
        w, h = elem.AXSize
        x, y = elem.AXPosition

        pos_click = tuple(map(int, (x + w * 0.4, y + h * 0.5)))
        self.mouse.click(*pos_click)
        time.sleep(1)
        self.keyboard.send(duration.replace("_", ""))
        self.keyboard.enter()

    def click_precut_single_trim_duration_arrow_button(self, option):
        '''
        option: 0- Up, 1- Down
        '''
        try:
            if not self.exist(L.precut.single_trim_precut_duration):
                logger("No duration textfield in this window")
                raise Exception
            if option == 0:
                self.exist_click(L.precut.single_trim_precut_duration_up)
            elif option == 1:
                self.exist_click(L.precut.single_trim_precut_duration_down)
            else:
                logger("input the wrong aug")
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def get_single_trim_precut_in_position(self):
        value = self.exist(L.precut.single_trim_precut_in_position).AXValue
        return value

    @step('[Action][Precut] Set Single Trim Precut In Position')
    def set_single_trim_precut_in_position(self, value):
        self.activate()
        elem = self.find(L.precut.single_trim_precut_in_position)
        w, h = elem.AXSize
        x, y = elem.AXPosition

        pos_click = tuple(map(int, (x + w * 0.4, y + h * 0.5)))
        self.mouse.click(*pos_click)
        time.sleep(OPERATION_DELAY)
        self.keyboard.send(value.replace("_", ""))
        self.keyboard.enter()
        time.sleep(OPERATION_DELAY*0.5)

    def click_precut_single_trim_in_position_arrow_button(self, option):
        '''
        option: 0- Up, 1- Down
        '''
        try:
            if not self.exist(L.precut.single_trim_precut_in_position):
                logger("No in position textfield in this window")
                raise Exception
            if option == 0:
                self.exist_click(L.precut.single_trim_precut_in_position_up)
            elif option == 1:
                self.exist_click(L.precut.single_trim_precut_in_position_down)
            else:
                logger("input the wrong aug")
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def get_single_trim_precut_out_position(self):
        value = self.exist(L.precut.single_trim_precut_out_position).AXValue
        return value

    def set_single_trim_precut_out_position(self, value):
        self.activate()
        elem = self.find(L.precut.single_trim_precut_out_position)
        w, h = elem.AXSize
        x, y = elem.AXPosition

        pos_click = tuple(map(int, (x + w * 0.4, y + h * 0.5)))
        self.mouse.click(*pos_click)
        time.sleep(1)
        self.keyboard.send(value.replace("_", ""))
        self.keyboard.enter()

    def click_precut_single_trim_out_position_arrow_button(self, option):
        '''
        option: 0- Up, 1- Down
        '''
        try:
            if not self.exist(L.precut.single_trim_precut_out_position):
                logger("No out position textfield in this window")
                raise Exception
            if option == 0:
                self.exist_click(L.precut.single_trim_precut_out_position_up)
            elif option == 1:
                self.exist_click(L.precut.single_trim_precut_out_position_down)
            else:
                logger("input the wrong aug")
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def check_preview_timecode_sync_position_timecode(self, type):
        '''
        type: 0- Mark-in, 1- Mark-out
        '''
        try:
            if not self.exist(L.precut.precut_window_current_time):
                logger("Can't find the timecode in precut window")
                raise Exception
            if not self.exist(L.precut.single_trim_precut_in_position):
                logger("Can't find the in position textfield in precut window")
                raise Exception
            if not self.exist(L.precut.single_trim_precut_out_position):
                logger("Can't finde the out position textfield in precut window")

            if type == 0:
                self.exist_click(L.precut.single_trim_mark_in)
                timecode = self.exist(L.precut.precut_window_current_time).AXValue
                in_time = self.exist(L.precut.single_trim_precut_in_position).AXValue
                if timecode == in_time:
                    return True
                else:
                    return False
            elif type == 1:
                self.exist_click(L.precut.single_trim_mark_out)
                timecode = self.exist(L.precut.precut_window_current_time).AXValue
                out_time = self.exist(L.precut.single_trim_precut_out_position).AXValue
                if timecode == out_time:
                    return True
                else:
                    return False
            else:
                logger("Input the wrong augment")
                return False
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def get_lock_status(self):
        try:
            if not self.exist(L.precut.single_trim_precut_duration):
                logger("No duration textfield in this window")
                raise Exception
            if self.exist(L.precut.single_trim_precut_duration).AXEnabled == False:
                return True
            elif self.exist(L.precut.single_trim_precut_duration).AXEnabled == True:
                return False
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_precut_single_trim_lock_duration(self):
        try:
            if not self.exist(L.precut.single_trim_precut_duration):
                logger("No duration textfield in this window")
                raise Exception
            self.exist_click(L.precut.single_trim_lock_duration)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Precut] Set [Multi Trim Mark In]')
    def tap_multi_trim_mark_in(self):
        try:
            if not self.exist(L.precut.multi_trim_mark_in):
                logger("No mark-in button in multi trim page")
                raise Exception("No mark-in button in multi trim page")
            self.exist_click(L.precut.multi_trim_mark_in)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Precut] Set [Multi Trim Mark Out]')
    def tap_multi_trim_mark_out(self):
        try:
            if not self.exist(L.precut.multi_trim_mark_out):
                logger("No mark-out button in multi trim page")
                raise Exception("No mark-out button in multi trim page")
            self.exist_click(L.precut.multi_trim_mark_out)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def drag_multi_trim_slider(self, hour, min, sec, mini_sec):
        try:
            if not self.exist(L.precut.multi_trim_mark_in):
                logger("Didn't stay in multi trim page")
                raise Exception
            timecode = hour * 3600 + min * 60 + sec * 30 + mini_sec * 1
            self.exist(L.precut.multi_trim_drag_slider).AXValue = int(timecode)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def tap_multi_trim_invert_trim(self):
        try:
            if not self.exist(L.precut.multi_trim_mark_in):
                logger("Didn't stay in multi trim page")
                raise Exception
            self.exist_click(L.precut.multi_trim_invert_trim)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Precut] Click [Remove] Button in [Multi Trim] Window')
    def tap_multi_trim_remove(self):
        try:
            if not self.exist(L.precut.multi_trim_mark_in):
                logger("Didn't stay in multi trim page")
                raise Exception("Didn't stay in multi trim page")
            self.exist_click(L.precut.multi_trim_remove)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_multi_trim_segment(self, segment_index):
        try:
            if not self.exist(L.precut.multi_trim_mark_in):
                logger("Didn't stay in multi trim page")
                raise Exception
            self.exist_click({'AXIdentifier': 'VideoTrimSegmentCollectionViewItem', 'index': segment_index})
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def right_click_multi_trim_segment_remove_selected(self):
        self.right_click()
        self.exist_click(L.precut.multi_trim_remove_segment)

    def right_click_multi_trim_segment_invert_selection(self):
        self.right_click()
        self.exist_click(L.precut.multi_trim_invert_selection)

    def click_multi_trim_segment_unselect_segment(self):
        #x, y = self.mouse.position()
        #self.mouse.click(x, y+82)
        segment1 = self.exist({'AXIdentifier': 'VideoTrimSegmentCollectionViewItem', 'index': 0})
        x, y = segment1.AXPosition
        self.mouse.click(x, y-3)

    def tap_multi_trim_thumbnail_frame(self, index):
        try:
            if not self.exist(L.precut.multi_trim_mark_in):
                logger("Didn't show in multi trim window")
                raise Exception
            self.exist_click({'AXIdentifier': 'VideoTrimContinuousThumbnailCollectionViewItem', 'index': index})
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def precut_preview_operation(self, str_operation):
        try:
            #if not self.exist(L.precut.precut_play):
                #logger("No play button in precut window")
                #raise Exception
            if not self.exist(L.precut.precut_stop):
                logger("No stop button in precut window")
                raise Exception
            if not self.exist(L.precut.precut_previous_frame):
                logger("No previous frame button in precut window")
                raise Exception
            if not self.exist(L.precut.precut_next_frame):
                logger("No next frame button in precut window")
                raise Exception
            if str_operation == 'Play':
                self.exist_click(L.precut.precut_play)
                return True
            elif str_operation == 'Pause':
                self.exist_click(L.precut.precut_pause)
                return True
            elif str_operation == 'Stop':
                self.exist_click(L.precut.precut_stop)
                return True
            elif str_operation == 'Previous_Frame':
                self.exist_click(L.precut.precut_previous_frame)
                return True
            elif str_operation == 'Next_Frame':
                self.exist_click(L.precut.precut_next_frame)
                return True
            else:
                logger("Input the wrong augment")
                return False
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def switch_multi_trim_preview_mode(self, str_mode):
        try:
            if not self.exist(L.precut.multi_trim_mark_in):
                logger("Didn't stay in multi trim window")
                raise Exception
            if str_mode == 'Original':
                self.exist_click(L.precut.multi_trim_original)
                return True
            elif str_mode == 'Output':
                self.exist_click(L.precut.multi_trim_output)
                return True
            else:
                logger("Input the wrong augment")
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Precut] Click [OK] Button to leave Precut Window')
    def click_ok(self):
        try:
            self.exist_click(L.precut.btn_ok)
            time.sleep(OPERATION_DELAY)
            if self.exist(L.precut.main_window, 2):
                logger('Fail to close precut window')
                raise Exception('Fail to close precut window')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def get_precut_status(self, str_media):
        self.select_library_icon_view_media(str_media)
        self.right_click()
        if self.select_right_click_menu('Precut...') == True:
            self.exist_click(L.precut.btn_cancel)
            return True
        else:
            return False

    def click_window_max_restore_btn(self):
        try:
            if not self.exist(L.precut.main_window):
                logger("No main window show up")
                raise Exception
            self.exist_click(L.precut.btn_restore)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Precut] Close [Precut] Window')
    def close_precut_window(self, option= -1):
        try:
            if not self.exist(L.precut.main_window):
                logger("No main window show up")
                raise Exception
            self.exist_click(L.precut.btn_close)
            if option == 0:
                self.exist_click(L.precut.close_dialog_yes)
            elif option == 1:
                self.exist_click(L.precut.close_dialog_no)
            elif option == 2:
                self.exist_click(L.precut.close_dialog_cancel)
            elif option == -1:
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
