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

class Library_Preview(Main_Page, BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @step('[Action][Library Preview] Click [Dock] button on [Preview Window]')
    def library_preview_click_dock(self):
        try:
            if not self.exist_click(L.library_preview.dock_preview_window):
                logger("Can't click the dock button")
                raise Exception("Can't click the dock button")
            time.sleep(DELAY_TIME)

            if not self.exist(L.library_preview.library_preview_window_close):
                return False

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Library Preview] Dock/ Undock [Preview Window]')
    def library_preview_click_undock(self):
        try:
            if not self.exist_click(L.library_preview.undock_preview_window):
                logger("Can't find the undock button")
                raise Exception("Can't find the undock button")
            if not self.exist(L.library_preview.dock_preview_window):
                return False

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Library Preview] Click [Close] button on [Preview Window]')
    def library_preview_click_close_preview(self):
        try:
            if not self.exist_click(L.library_preview.library_preview_window_close):
                logger("Can't click the close button")
                raise Exception("Can't click the close button")
            time.sleep(DELAY_TIME)

            # Verify Step
            if self.exist(L.library_preview.undock_preview_window):
                return False
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def library_preview_click_maximize(self):
        try:
            if not self.exist_click(L.library_preview.library_preview_window_maximize):
                logger("Can't click the maximize button")
                raise Exception
            time.sleep(DELAY_TIME)

            # Verify step (Maximize)
            if not self.exist(L.library_preview.upper_project_name):
                return False
            time.sleep(DELAY_TIME)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_preview_click_restoredown(self):
        try:
            if not self.exist_click(L.library_preview.library_preview_window_restoredown):
                logger("Can't click the restore down button")
                raise Exception
            time.sleep(DELAY_TIME)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Library Preview] Click [Minimize] button on [Preview Window]')
    def library_preview_click_minimize(self):
        try:
            if not self.exist_click(L.library_preview.library_preview_window_minimize):
                logger("Can't click the minimize button")
                raise Exception("Can't click the minimize button")
            time.sleep(DELAY_TIME)

            # Verify Step (Minimize)
            if self.exist(L.library_preview.dock_preview_window):
                return False
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Library Preview] Click [Show Library Preview] button when [Minimized window]')
    def library_preview_show_library_preview(self):
        try:
            if not self.exist_click(L.library_preview.show_minimized_window):
                logger("Can't find the button to show the minimized window")
                raise Exception("Can't find the button to show the minimized window")
            if not self.exist_click(L.library_preview.restore_minimized_window):
                logger("Can't show the library preview window")
                raise Exception("Can't show the library preview window")
            time.sleep(DELAY_TIME)

            # Verify
            if not self.exist(L.library_preview.dock_preview_window):
                return False

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def view_menu_show_library_preview_window(self):
        try:
            if not self.exist_click(L.library_preview.menu_bar_view_btn):
                logger("Can't find [View] in caption bar")
                raise Exception
            if not self.exist(L.library_preview.menu_bar_view_show_library_preview_window):
                logger("Can't find [Show library preview window] in [View]")
                raise Exception

            # Verify step
            if not self.exist(L.library_preview.menu_bar_view_show_library_preview_window).AXMenuItemMarkChar == str("✓"):
                logger("Didn't select the [Show library preview window]")
                return False
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Library Preview] Click Preview Operation for Play/ Pause/ Stop/ Previous Frame/ Next Frame/ Fast Forward')
    def library_preview_window_preview_operation(self, operation):
        try:
            #if not self.exist(L.library_preview.undock_preview_window):
                #logger("Didn't stay in dock status now")
                #raise Exception
            #time.sleep(DELAY_TIME)
           # if not self.exist(L.library_preview.dock_window.dock_window_play_btn) and not self.exist(L.library_preview.dock_window.dock_window_pause_btn):
               # logger("Didn't show the play/pause button in dock preview window")
               #raise Exception
            #time.sleep(DELAY_TIME)
            #if not self.exist(L.library_preview.dock_window.dock_window_stop_btn):
                #logger("Didn't show the stop button in dock preview window")
                #raise Exception
            #time.sleep(DELAY_TIME)
            #if not self.exist(L.library_preview.dock_window.dock_window_duration_section):
                #logger("Didn't show the duration section in dock preview window")
                #raise Exception
            #time.sleep(DELAY_TIME)
            #if not self.exist(L.library_preview.dock_window.dock_window_next_frame_btn):
                #logger("Didn't show the next_frame button in dock preview window")
                #raise Exception
            #time.sleep(DELAY_TIME)
            #if not self.exist(L.library_preview.dock_window.dock_window_previous_frame_btn):
                #logger("Didn't show the previous frame button in dock previous window")
                #raise Exception
            #time.sleep(DELAY_TIME)
            #if not self.exist(L.library_preview.dock_window.dock_window_fast_forward_btn):
                #logger("Didn't show the fast forward button in dock previous window")
                #raise Exception
            #time.sleep(DELAY_TIME)

            # operation 0- Play/Pause, 1- Stop, 2- Previous Frame, 3- Next Frame, 4- Fast Forward


            # Verify play button
            if operation == 0:
                current_duration_for_play = self.exist(L.library_preview.dock_window.dock_window_duration_section).AXValue
                logger(current_duration_for_play)

                #if current_duration_for_play == "--;--;--;--":
                    #logger("current file in preview window is a picture/BGM")
                    #return False
                if self.exist(L.library_preview.dock_window.dock_window_play_btn):
                    self.click(L.library_preview.dock_window.dock_window_play_btn)
                elif self.exist(L.library_preview.dock_window.dock_window_pause_btn):
                    self.click(L.library_preview.dock_window.dock_window_pause_btn)
                else:
                    logger("Preview window cannot find the button")
                    raise Exception("Preview window cannot find the button")

            # Verify stop button
            elif operation == 1:
                current_duration_for_stop = self.exist(L.library_preview.dock_window.dock_window_duration_section).AXValue
                logger(current_duration_for_stop)

                if current_duration_for_stop == "--;--;--;--":
                    logger("current file in preview window is a picture")
                    return False
                self.exist_click(L.library_preview.dock_window.dock_window_stop_btn)
                time.sleep(DELAY_TIME)

                after_duration_for_stop = self.exist(L.library_preview.dock_window.dock_window_duration_section).AXValue
                logger(after_duration_for_stop)

                if current_duration_for_stop == "00;00;00;00" and after_duration_for_stop == "00;00;00;00":
                    logger("Stay in the beginning currently")
                    return False
                elif current_duration_for_stop != "00;00;00;00" and current_duration_for_stop == after_duration_for_stop:
                    logger("Didn't stop the video normally")
                    return False
                else:
                    return True

            # Verify previous frame button
            elif operation == 2:
                current_duration_for_previous_frame = self.exist(L.library_preview.dock_window.dock_window_duration_section).AXValue
                logger(current_duration_for_previous_frame)

                if current_duration_for_previous_frame == "--;--;--;--":
                    logger("current file in preview window is a picture")
                    return False

                time.sleep(DELAY_TIME)
                self.exist_click(L.library_preview.dock_window.dock_window_previous_frame_btn)
                time.sleep(DELAY_TIME)
                after_duration_for_previous_frame = self.exist(L.library_preview.dock_window.dock_window_duration_section).AXValue
                logger(after_duration_for_previous_frame)

                if current_duration_for_previous_frame == "00;00;00;00":
                    logger("Stay in the beginning currently")
                    return False
                elif current_duration_for_previous_frame == after_duration_for_previous_frame:
                    logger("Didn't play the previous frame normally")
                    return False
                else:
                    return True

            # Verify next frame button
            elif operation == 3:
                current_duration_for_next_frame = self.exist(L.library_preview.dock_window.dock_window_duration_section).AXValue
                logger(current_duration_for_next_frame)

                if current_duration_for_next_frame == "--;--;--;--":
                    logger("current file in preview window is a picture")
                    return False

                time.sleep(DELAY_TIME)
                self.exist_click(L.library_preview.dock_window.dock_window_next_frame_btn)
                time.sleep(DELAY_TIME)
                after_duration_for_next_frame = self.exist(L.library_preview.dock_window.dock_window_duration_section).AXValue
                logger(after_duration_for_next_frame)

                if current_duration_for_next_frame == after_duration_for_next_frame:
                    logger("Didn't play the next frame normally")
                    return False
                else:
                    return True
            # Verify fast_forward
            elif operation == 4:
                current_duration_for_fast_forward = self.exist(L.library_preview.dock_window.dock_window_duration_section).AXValue
                logger(current_duration_for_fast_forward)

                if current_duration_for_fast_forward == "--;--;--;--":
                    logger("Current file in preview page is a picture")
                    return False

                fast_forward_btn = self.exist(L.library_preview.dock_window.dock_window_fast_forward_btn).AXEnabled
                if fast_forward_btn == False:
                    logger("Current file in preview page is a music")
                    return False
                time.sleep(DELAY_TIME)
                self.exist_click(L.library_preview.dock_window.dock_window_fast_forward_btn)
                time.sleep(1)
                after_duration_for_fast_forward = self.exist(L.library_preview.dock_window.dock_window_duration_section).AXValue
                logger(after_duration_for_fast_forward)

                if current_duration_for_fast_forward == after_duration_for_fast_forward:
                    logger("Didn't play fast forward normally")
                    return False
                else:
                    return True
            else:
                 logger("The clicked btn isn't play/stop/previous_frame/next_frame/fast forward")
                 raise Exception("The clicked btn isn't play/stop/previous_frame/next_frame/fast forward")

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def library_preview_window_click_take_snapshot_in_undocked_window(self):
        try:
            fast_forward_status = self.exist(L.library_preview.dock_window.dock_window_fast_forward_btn).AXEnabled
            logger(fast_forward_status)
            if fast_forward_status == False:
                logger("The file in preview window is a music/photo")
                raise Exception
            time.sleep(DELAY_TIME)

            # Verify for undocked preview window
            if self.exist(L.library_preview.dock_preview_window):
                logger("Current preview window is undocked")
            if not self.exist_click(L.library_preview.dock_window.undock_window_snapshot_btn):
                logger("Can't click the take_snapshot button in undocked preview window")
                raise Exception
            if not self.exist(L.library_preview.dock_window.dock_window_snapshot_save_btn):
                logger("Didn't pop up the [Save as] dialog")
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_preview_window_click_take_snapshot_in_docked_window(self):
        try:
            fast_forward_status = self.exist(L.library_preview.dock_window.dock_window_fast_forward_btn).AXEnabled
            logger(fast_forward_status)
            if fast_forward_status == False:
                logger("The file in preview window is a music/photo")
                raise Exception
            time.sleep(DELAY_TIME)
            # Verify step for docked window
            if not self.exist_click(L.library_preview.dock_window.dock_window_snapshot_btn):
                logger("Can't click the take_snapshot button in docked preview window")
                raise Exception
            if not self.exist(L.library_preview.dock_window.dock_window_snapshot_save_btn):
                logger("Didn't pop up the [Save as] dialog")
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def save_as_snapshot_filename(self, filename, full_path):
        try:
            #if not self.exist(L.library_preview.snapshot_save_as_maximize):
             #   self.exist_click(L.library_preview.snapshot_open_disclosure)
            #if not self.exist_click(L.library_preview.snapshot_filename_textfield):
                #logger("Can't click the textfield")
                #raise Exception
            #self.tap_SelectAll_hotkey()
            #self.tap_Remove_hotkey()
            #time.sleep(DELAY_TIME)

            #self.keyboard.send(filename)

            if not self.select_file(os.path.abspath(f"{full_path}/{filename}"), btn_confirm='Save'):
                logger("Can't find the target path to save snapshot")
                raise Exception
            if self.exist(L.library_preview.snapshot_filename_existed_dialog):
                #time.sleep(DELAY_TIME)
                self.exist_click(L.library_preview.snapshot_save_replace_btn)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_preview_window_adjust_volume_in_docked_window(self):
        try:
            if not self.exist_click(L.library_preview.dock_window_volume_btn):
                logger("Can't click the volume btn in docked window")
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_preview_window_adjust_volume_in_undocked_window(self):
        try:
            if not self.exist_click(L.library_preview.undock_window_volume_btn):
                logger("Can't click the volume button in undocked window")
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_preview_window_drag_volume_slider(self, value):
        try:
            self.exist(L.library_preview.library_preview_window_volume_slider).AXValue = float(value)
            if float(value) == self.exist(L.library_preview.library_preview_window_volume_slider).AXValue:
                return True
            else:
                return False
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def set_library_preview_window_timecode(self, timecode):
        '''
                :param timecode: "HH_MM_SS_mm" -> "01_00_59_99"
                :return: True/False
                '''
        self.activate()
        elem = self.find(L.library_preview.library_preview_window_duration_section)
        w, h = elem.AXSize
        x, y = elem.AXPosition

        pos_click = tuple(map(int, (x + w * 0.1, y + h * 0.5)))
        self.mouse.click(*pos_click)
        time.sleep(1)
        self.keyboard.send(timecode.replace("_", ""))
        self.keyboard.enter()

    @step('[Action][Library Preview] Click [Mark In]')
    def edit_library_preview_window_click_mark_in(self):
        try:
            if self.exist(L.library_preview.library_preview_window_markin).AXEnabled == True:
                if not self.exist_click(L.library_preview.library_preview_window_markin):
                    logger("Can't click mark-in btn")
                    raise Exception("Can't click mark-in btn")
            else:
                logger("Current mark-in btn is gray out")
                raise Exception("Current mark-in btn is gray out")
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Library Preview] Click [Mark Out]')
    def edit_library_preview_window_click_mark_out(self):
        try:
            if self.exist(L.library_preview.library_preview_window_markout).AXEnabled == True:
                if not self.exist_click(L.library_preview.library_preview_window_markout):
                    logger("Can't click mark-out btn")
                    raise Exception("Can't click mark-out btn")
            else:
                logger("Current mark-out btn is gray out")
                raise Exception("Current mark-out btn is gray out")
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Library Preview] Click [Insert] on selected track')
    def edit_library_preview_window_click_insert_on_selected_track(self):
        try:
            if self.exist(L.library_preview.library_preview_window_click_insert_on_selected_track).AXEnabled == True:
               if not self.exist_click(L.library_preview.library_preview_window_click_insert_on_selected_track):
                   logger("Can't click to insert on the selected track")
                   raise Exception("Can't click to insert on the selected track")
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def edit_library_preview_window_click_overwrite_on_selected_track(self):
        try:
            if self.exist(L.library_preview.library_preview_window_click_overwrite_on_selected_track).AXEnabled == True:
               if not self.exist_click(L.library_preview.library_preview_window_click_overwrite_on_selected_track):
                   logger("Can't click to overwrite on the selected track")
                   raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Library Preview] Click [Add Clip Marker]')
    def edit_library_preview_window_add_clip_marker(self):
        try:
            if self.exist(L.library_preview.library_preview_window_add_clip_marker).AXEnabled == True:
                if not self.exist_click(L.library_preview.library_preview_window_add_clip_marker):
                    logger("Can't click to add clip marker")
                    raise Exception("Can't click to add clip marker")
            else:
                logger("Current add clip marker btn is gray out")
                raise Exception("Current add clip marker btn is gray out")
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Library Preview] Input [Text] on [Modify Clip Marker]')
    def edit_library_preview_window_clip_marker_input_text(self, text):
        try:
            if not self.exist(L.library_preview.library_preview_window_modify_marker):
                logger("No modify marker dialog pop up")
                raise Exception("No modify marker dialog pop up")
            if not self.exist_click(L.library_preview.library_preview_window_add_clip_marker_text_field):
                logger("Can't find the clip marker text field")
                raise Exception("Can't find the clip marker text field")
            # Select all then press backspace (Delete all "old" clip marker text)
            self.tap_SelectAll_hotkey()
            self.press_backspace_key()
            time.sleep(DELAY_TIME)

            # Input Argument1
            self.keyboard.send(text)
            time.sleep(DELAY_TIME)
            if not self.exist_click(L.library_preview.library_preview_window_clip_marker_ok):
                logger("No OK button can be clicked in modify marker dialog")
                raise Exception("No OK button can be clicked in modify marker dialog")
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
    def edit_library_preview_window_undock_status_preview_operation(self, operation):
        # operation 0- Play, 1- Stop, 2- Previous Frame, 3- Next Frame, 4- Fast Forward
        try:
            if not self.exist(L.library_preview.library_preview_window_timecode):
                logger("Didn't find the library preview window")
                raise Exception

             # Verify play button
            if operation == 0:
                if not self.exist(L.library_preview.library_preview_window_play_btn):
                    logger("Preview window is playing")
                    raise Exception
                current_duration_for_play = self.exist_click(L.library_preview.library_preview_window_timecode).AXValue
                logger(current_duration_for_play)

                if current_duration_for_play == "--;--;--;--":
                    logger("current file in preview window is a picture")
                    return False
                self.exist_click(L.library_preview.library_preview_window_play_btn)
                time.sleep(2)

                self.exist_click(L.library_preview.library_preview_window_pause_btn)
                time.sleep(DELAY_TIME)
                after_duration_for_play = self.exist_click(L.library_preview.library_preview_window_timecode).AXValue
                logger(after_duration_for_play)

                if current_duration_for_play == after_duration_for_play:
                    logger("Didn't play the video normally")
                    return False
                else:
                    return True


                # Verify stop button
            elif operation == 1:
                current_duration_for_stop = self.exist_click(L.library_preview.library_preview_window_timecode).AXValue
                logger(current_duration_for_stop)

                if current_duration_for_stop == "--;--;--;--":
                    logger("current file in preview window is a picture")
                    return False
                self.exist_click(L.library_preview.library_preview_window_stop_btn)
                time.sleep(DELAY_TIME)

                after_duration_for_stop = self.exist_click(L.library_preview.library_preview_window_timecode).AXValue
                logger(after_duration_for_stop)

                if current_duration_for_stop == "00;00;00;00" and after_duration_for_stop == "00;00;00;00":
                    logger("Stay in the beginning currently")
                    return False
                elif current_duration_for_stop != "00;00;00;00" and current_duration_for_stop == after_duration_for_stop:
                    logger("Didn't stop the video normally")
                    return False
                else:
                    return True

                # Verify previous frame button
            elif operation == 2:
                current_duration_for_previous_frame = self.exist_click(L.library_preview.library_preview_window_timecode).AXValue
                logger(current_duration_for_previous_frame)

                if current_duration_for_previous_frame == "--;--;--;--":
                    logger("current file in preview window is a picture")
                    return False

                time.sleep(DELAY_TIME)
                self.exist_click(L.library_preview.library_preview_window_previous_frame_btn)
                time.sleep(DELAY_TIME)
                after_duration_for_previous_frame = self.exist_click(L.library_preview.library_preview_window_timecode).AXValue
                logger(after_duration_for_previous_frame)

                if current_duration_for_previous_frame == "00;00;00;00":
                    logger("Stay in the beginning currently")
                    return False
                elif current_duration_for_previous_frame == after_duration_for_previous_frame:
                    logger("Didn't play the previous frame normally")
                    return False
                else:
                    return True

            # Verify next frame button
            elif operation == 3:
                current_duration_for_next_frame = self.exist_click(L.library_preview.library_preview_window_timecode).AXValue
                logger(current_duration_for_next_frame)

                if current_duration_for_next_frame == "--;--;--;--":
                    logger("current file in preview window is a picture")
                    return False

                time.sleep(DELAY_TIME)
                self.exist_click(L.library_preview.library_preview_window_next_frame_btn)
                time.sleep(DELAY_TIME)
                after_duration_for_next_frame = self.exist_click(L.library_preview.library_preview_window_timecode).AXValue
                logger(after_duration_for_next_frame)

                if current_duration_for_next_frame == after_duration_for_next_frame:
                    logger("Didn't play the next frame normally")
                    return False
                else:
                    return True
            # Verify fast_forward
            elif operation == 4:
                current_duration_for_fast_forward = self.exist_click(L.library_preview.library_preview_window_timecode).AXValue
                logger(current_duration_for_fast_forward)

                if current_duration_for_fast_forward == "--;--;--;--":
                    logger("Current file in preview page is a picture")
                    return False

                fast_forward_btn = self.exist(L.library_preview.library_preview_window_timecode).AXEnabled
                if fast_forward_btn == False:
                    logger("Current file in preview page is a music")
                    return False
                time.sleep(DELAY_TIME)
                self.exist_click(L.library_preview.library_preview_window_fast_forward_btn)
                time.sleep(1)
                after_duration_for_fast_forward = self.exist_click(L.library_preview.library_preview_window_timecode).AXValue
                logger(after_duration_for_fast_forward)

                if current_duration_for_fast_forward == after_duration_for_fast_forward:
                    logger("Didn't play fast forward normally")
                    return False
                else:
                    return True
            else:
                logger("The clicked btn isn't play/stop/previous_frame/next_frame/fast forward")
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def library_preview_window_exist(self):
        if self.exist(L.library_preview.library_preview_window_close):
            return True
        elif self.exist(L.library_preview.dock_preview_window):
            return True
        #elif self.exist(L.library_preview.toolbar_last_btn):
            #return True
        try:
            if self.exist(L.library_preview.toolbar_last_btn):
                return True
        except IndexError:
            return False
        else:
            return False

    def get_library_preview_window_status(self):
        option_1 = 'Dock'
        option_2 = 'Undock'
        if self.exist(L.library_preview.undock_preview_window).AXEnabled == True:
            #print(self.exist(L.library_preview.undock_preview_window).AXEnabled)
            return option_1
        self.exist_click(L.library_preview.menu_bar_view_btn)
        if self.exist(L.library_preview.menu_bar_view_show_library_preview_window).AXMenuItemMarkChar == str("✓"):
            return option_2
        else:
            logger("Didn't show the library preview window")

    def get_project_name(self):
        name = self.exist(L.library_preview.text_project_name).AXValue
        return name



















