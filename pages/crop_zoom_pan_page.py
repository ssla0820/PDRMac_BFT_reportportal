import time, datetime, os, copy

from .base_page import BasePage
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
from AppKit import NSScreen
from .locator import locator as L
from reportportal_client import step

OPERATION_DELAY = 1 # sec

class Crop_Zoom_Pan(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyframe = self.Keyframe(*args, **kwargs)

    @step('[Action][Crop Zoom Pan] Close [Crop Zoom Pan] Window')
    def close_window(self):
        self.exist_click(L.crop_zoom_pan.close)
        return self.is_not_exist({'AXIdentifier': 'IDC_MAGIC_MOTION_DESIGNER_WINDOW'}, timeout=3)

    @step('[Verify][Crop Zoom Pan] Check if [Crop Zoom Pan] Window is shown')
    def is_enter_crop_zoom_pan(self):
        return self.is_exist({'AXIdentifier': 'IDC_MAGIC_MOTION_DESIGNER_WINDOW'}, timeout=3)

    def click_maximize_btn(self):
        self.exist_click(L.crop_zoom_pan.maximize)
        return

    @step('[Action][Crop Zoom Pan] Set Timecode')
    def set_timecode(self, timecode):
        self.activate()
        elem = self.find(L.crop_zoom_pan.timecode)
        w, h = elem.AXSize
        x, y = elem.AXPosition

        pos_click = tuple(map(int, (x + w * 0.1, y + h * 0.5)))
        self.mouse.click(*pos_click)
        time.sleep(1)
        self.keyboard.send(timecode.replace("_", ""))
        self.keyboard.enter()

    @step('[Action][Crop Zoom Pan] Get Timecode')
    def get_timecode(self):
        try:
            if not self.exist(L.crop_zoom_pan.window):
                logger("No crop zoom pan window show up")
                raise Exception("No crop zoom pan window show up")
            timecode = self.exist(L.crop_zoom_pan.timecode).AXValue
            return timecode
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def set_AspectRatio_4_3(self):
        self.exist_click(L.crop_zoom_pan.aspect_ratio_btn)
        items = self.exist(L.crop_zoom_pan.aspect_ratio_list)
        for item in items:
            if item.AXValue.strip() == '4:3':
                self.mouse.click(*item.center)
                return True
        return False

    def set_AspectRatio_16_9(self):
        self.exist_click(L.crop_zoom_pan.aspect_ratio_btn)
        items = self.exist(L.crop_zoom_pan.aspect_ratio_list)
        for item in items:
            if item.AXValue.strip() == '16:9':
                self.mouse.click(*item.center)
                return True
        return False

    def set_AspectRatio_9_16(self):
        self.exist_click(L.crop_zoom_pan.aspect_ratio_btn)
        items = self.exist(L.crop_zoom_pan.aspect_ratio_list)
        for item in items:
            if item.AXValue.strip() == '9:16':
                self.mouse.click(*item.center)
                return True
        return False

    @step('[Action][Crop Zoom Pan] Set [Aspect Ratio] to (1:1)')
    def set_AspectRatio_1_1(self):
        self.exist_click(L.crop_zoom_pan.aspect_ratio_btn)
        items = self.exist(L.crop_zoom_pan.aspect_ratio_list)
        for item in items:
            if item.AXValue.strip() == '1:1':
                self.mouse.click(*item.center)
                return True
        return False

    def set_AspectRatio_Freeform(self):
        self.exist_click(L.crop_zoom_pan.aspect_ratio_btn)
        items = self.exist(L.crop_zoom_pan.aspect_ratio_list)
        for item in items:
            if item.AXValue.strip() == 'Freeform':
                self.mouse.click(*item.center)
                return True
        return False

    def preview_operation(self, strOperation):
        try:
            if not self.exist(L.crop_zoom_pan.window):
                logger("No crop zoom pan window show up")
                raise Exception
            if strOperation == 'Play':
                self.exist_click(L.crop_zoom_pan.play)
            elif strOperation == 'Stop':
                self.exist_click(L.crop_zoom_pan.stop)
            elif strOperation == 'Previous_Frame':
                self.exist_click(L.crop_zoom_pan.previous_frame)
            elif strOperation == 'Next_Frame':
                self.exist_click(L.crop_zoom_pan.next_frame)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_grid_lines_format(self, index=1):
        self.exist_click(L.crop_zoom_pan.grid_line_btn)
        self.exist_click(L.crop_zoom_pan.grid_line)
        if index == 1:
            self.exist_click(L.crop_zoom_pan.grid_line_none)
            return True
        elif index == 2:
            self.exist_click(L.crop_zoom_pan.grid_line_2)
            return True
        elif index == 3:
            self.exist_click(L.crop_zoom_pan.grid_line_3)
            return True
        elif index == 4:
            self.exist_click(L.crop_zoom_pan.grid_line_4)
            return True
        elif index == 5:
            self.exist_click(L.crop_zoom_pan.grid_line_5)
            return True
        elif index == 6:
            self.exist_click(L.crop_zoom_pan.grid_line_6)
            return True
        elif index == 7:
            self.exist_click(L.crop_zoom_pan.grid_line_7)
            return True
        elif index == 8:
            self.exist_click(L.crop_zoom_pan.grid_line_8)
            return True
        elif index == 9:
            self.exist_click(L.crop_zoom_pan.grid_line_9)
            return True
        elif index == 10:
            self.exist_click(L.crop_zoom_pan.grid_line_10)
            return True
        else:
            logger("No crop zoom pan window show up")
            return False

    def click_viewer_zoom_menu(self, value='Fit'):
        self.exist_click(L.crop_zoom_pan.viewer_zoom_menu)
        items = self.exist(L.crop_zoom_pan.viewer_zoom_menu_list)
        for item in items:
            if item.AXValue.strip() == value:
                self.mouse.click(*item.center)
                return True
        return False

    def get_viewer_setting(self):
        return self.exist(L.crop_zoom_pan.viewer_zoom_menu).AXTitle

    @step('[Action][Crop Zoom Pan] Get [Aspect Ratio]')
    def get_current_AspectRatio(self):
        return self.exist(L.crop_zoom_pan.aspect_ratio_btn).AXTitle

    def click_undo(self, times=1):
        try:
            if not self.exist(L.crop_zoom_pan.window):
                logger("No crop zoom pan window show up")
                raise Exception
            self.exist_click(locator=L.crop_zoom_pan.undo, times=times)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_redo(self, times=1):
        try:
            if not self.exist(L.crop_zoom_pan.window):
                logger("No crop zoom pan window show up")
                raise Exception
            self.exist_click(locator=L.crop_zoom_pan.redo, times=times)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Crop Zoom Pan] Click [OK] Button to leave [Crop Zoom Pan] window')
    def click_ok(self):
        self.exist_click(L.crop_zoom_pan.ok)
        return self.is_not_exist(L.crop_zoom_pan.window, timeout=3)

    def click_cancel(self):
        self.exist_click(L.crop_zoom_pan.cancel)
        time.sleep(OPERATION_DELAY)
        return self.is_not_exist(L.crop_zoom_pan.window, timeout=3)

    def get_reset_status(self):
        return self.exist(L.crop_zoom_pan.reset).AXEnabled

    @step('[Action][Crop Zoom Pan] Click [Reset] Button')
    def click_reset(self):
        if self.get_reset_status():
            self.exist_click(L.crop_zoom_pan.reset)
            return True
        else:
            logger("Reset button is disabled")
            return False
        
    @step('[Action][Crop Zoom Pan] Get [Position X]')
    def get_position_x(self):
        return self.exist(L.crop_zoom_pan.position_x).AXValue

    @step('[Action][Crop Zoom Pan] Get [Position Y]')
    def get_position_y(self):
        return self.exist(L.crop_zoom_pan.position_y).AXValue

    @step('[Action][Crop Zoom Pan] Set [Position X]')
    def set_position_x(self, value):
        self.exist(L.crop_zoom_pan.position_x).AXValue = value
        self.press_enter_key()
        return True

    @step('[Action][Crop Zoom Pan] Set [Position Y]')
    def set_position_y(self, value):
        self.exist(L.crop_zoom_pan.position_y).AXValue = value
        self.press_enter_key()
        return True
    
    @step('[Action][Crop Zoom Pan] Set [Position X] by arrow')
    def click_position_x_arrow(self, default='up'):
        if default == 'up':
            self.exist_click(L.crop_zoom_pan.position_x_arrow_up)
            return True
        elif default == 'down':
            self.exist_click(L.crop_zoom_pan.position_x_arrow_down)
            return True
        else:
            logger("wrong input")
            return False
    @step('[Action][Crop Zoom Pan] Set [Position Y] by arrow')
    def click_position_y_arrow(self, default='up'):
        if default == 'up':
            self.exist_click(L.crop_zoom_pan.position_y_arrow_up)
            return True
        elif default == 'down':
            self.exist_click(L.crop_zoom_pan.position_y_arrow_down)
            return True
        else:
            logger("wrong input")
            return False

    def set_scale_width_slider(self, value):
        try:
            if not self.exist(L.crop_zoom_pan.window):
                logger("No crop zoom pan window show up")
                raise Exception
            self.exist(L.crop_zoom_pan.scale_width_slider).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def set_scale_height_slider(self, value):
        try:
            if not self.exist(L.crop_zoom_pan.window):
                logger("No crop zoom pan window show up")
                raise Exception
            self.exist(L.crop_zoom_pan.scale_height_slider).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True
    @step('[Action][Crop Zoom Pan] Set [Scale Width]')
    def set_scale_width(self, value):
        self.exist_click(L.crop_zoom_pan.scale_width)
        self.exist(L.crop_zoom_pan.scale_width).AXValue = value
        self.press_enter_key()
        return True
    @step('[Action][Crop Zoom Pan] Set [Scale Height]')
    def set_scale_height(self, value):
        self.exist_click(L.crop_zoom_pan.scale_height)
        self.exist(L.crop_zoom_pan.scale_height).AXValue = value
        self.press_enter_key()
        return True
    @step('[Action][Crop Zoom Pan] Get [Scale Width]')
    def get_scale_width(self):
        return self.exist(L.crop_zoom_pan.scale_width).AXValue
    @step('[Action][Crop Zoom Pan] Get [Scale Height]')
    def get_scale_height(self):
        return self.exist(L.crop_zoom_pan.scale_height).AXValue

    def click_scale_width_arrow(self, default='up'):
        if default == 'up':
            self.exist_click(L.crop_zoom_pan.scale_width_arrow_up)
            return True
        elif default == 'down':
            self.exist_click(L.crop_zoom_pan.scale_width_arrow_down)
            return True
        else:
            logger("wrong input")
            return False

    def click_scale_height_arrow(self, default='up'):
        if default == 'up':
            self.exist_click(L.crop_zoom_pan.scale_height_arrow_up)
            return True
        elif default == 'down':
            self.exist_click(L.crop_zoom_pan.scale_height_arrow_down)
            return True
        else:
            logger("wrong input")
            return False

    def set_rotation(self, value):
        self.exist_click(L.crop_zoom_pan.rotation)
        self.exist(L.crop_zoom_pan.rotation).AXValue = value
        self.press_enter_key()
        return True

    def set_maintain_aspect_ratio(self, bApply=1):
        check = self.exist(L.crop_zoom_pan.maintain_aspect_ratio).AXValue
        enable = self.exist(L.crop_zoom_pan.maintain_aspect_ratio).AXEnabled
        if enable == True:
            if bApply == check:
                return True
            elif bApply != check:
                self.exist_click(L.crop_zoom_pan.maintain_aspect_ratio)
                return True
        else:
            logger("checkbox is disabled")
            return False


    def apply_snap_ref_line(self, bApply=1):
        self.exist_click(L.crop_zoom_pan.grid_line_btn)
        enable = self.exist(L.crop_zoom_pan.snap_line).AXMenuItemMarkChar
        if enable == '✓':
            enable = 1
        else:
            enable = 0
        if enable == bApply:
            return True
        else:
            self.exist_click(L.crop_zoom_pan.snap_line)
            return True

    def click_rotation_arrow(self, default='up'):
        if default == 'up':
            self.exist_click(L.crop_zoom_pan.rotation_arrow_up)
            return True
        elif default == 'down':
            self.exist_click(L.crop_zoom_pan.rotation_arrow_down)
            return True
        else:
            logger("wrong input")
            return False

    def get_rotation(self):
        return self.exist(L.crop_zoom_pan.rotation).AXValue

    def set_preview_slider(self, value):
        item = self.exist(L.crop_zoom_pan.preview_slider).AXMaxValue
        position = item*float(value)
        self.exist(L.crop_zoom_pan.preview_slider).AXValue = position
        return True

    class Keyframe(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def add(self):
            enable = self.exist(L.crop_zoom_pan.keyframe.add).AXEnabled
            if enable == True:
                self.exist_click(L.crop_zoom_pan.keyframe.add)
                return True
            else:
                logger("button disabled")
                return False

        def remove(self):
            enable = self.exist(L.crop_zoom_pan.keyframe.remove).AXEnabled
            if enable == True:
                self.exist_click(L.crop_zoom_pan.keyframe.remove)
                return True
            else:
                logger("button disabled")
                return False

        def select_previous(self):
            enable = self.exist(L.crop_zoom_pan.keyframe.select_previous).AXEnabled
            if enable == True:
                self.exist_click(L.crop_zoom_pan.keyframe.select_previous)
                return True
            else:
                logger("button disabled")
                return False

        def select_next(self):
            enable = self.exist(L.crop_zoom_pan.keyframe.select_next).AXEnabled
            if enable == True:
                self.exist_click(L.crop_zoom_pan.keyframe.select_next)
                return True
            else:
                logger("button disabled")
                return False

        def duplicate_previous(self):
            enable = self.exist(L.crop_zoom_pan.keyframe.duplicate).AXEnabled
            if enable == True:
                self.click(L.crop_zoom_pan.keyframe.duplicate)
                time.sleep(1)
                if self.exist(L.crop_zoom_pan.keyframe.duplicate_previous).AXEnabled:
                    self.select_right_click_menu('Duplicate from Previous Keyframe')
                    time.sleep(1)
                    #self.click(L.crop_zoom_pan.keyframe.duplicate_previous)
                    return True
                else:
                    logger("disabled")
                    return False
            else:
                logger("button disabled")
                return False

        def duplicate_next(self):
            enable = self.exist(L.crop_zoom_pan.keyframe.duplicate).AXEnabled
            if enable == True:
                self.exist_click(L.crop_zoom_pan.keyframe.duplicate)
                if self.exist(L.crop_zoom_pan.keyframe.duplicate_next).AXEnabled:
                    self.exist_click(L.crop_zoom_pan.keyframe.duplicate_next)
                    return True
                else:
                    logger("disabled")
                    return False
            else:
                logger("button disabled")
                return False



'''
    def preview_operation(self, strOperation):
        try:
            if not self.exist(L.particle_designer.designer_window):
                logger("No particle designer window show up")
                raise Exception
            if strOperation == 'Play':
                self.exist_click(L.particle_designer.preview_play)
            elif strOperation == 'Stop':
                self.exist_click(L.particle_designer.preview_stop)
            elif strOperation == 'Pause':
                self.exist_click(L.particle_designer.preview_pause)
            elif strOperation == 'Previous_Frame':
                self.exist_click(L.particle_designer.preview_previous_frame)
            elif strOperation == 'Next_Frame':
                self.exist_click(L.particle_designer.preview_next_frame)
            elif strOperation == 'Fast_Forward':
                self.exist_click(L.particle_designer.preview_fast_forward)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True
'''










































































