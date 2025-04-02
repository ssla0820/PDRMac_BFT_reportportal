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

class Pip_Designer(Main_Page, BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.express_mode = self.Express_Mode(*args, **kwargs)
        self.advanced = self.Advanced(*args, **kwargs)
        self.in_animation = self.In_Animation(*args, **kwargs)
        self.out_animation = self.In_Animation(*args, **kwargs)
        self.path = self.Path(*args, **kwargs)
        self.motion_blur = self.Motion_Blur(*args, **kwargs)
        self.simple_timeline = self.Simple_Timeline(*args, **kwargs)

    def check_pip_designer_preview(self, ground_truth_image, area, track_index=None):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No Pip designer window show up now")
                raise Exception
            if area == 'Properties':
                properties = self.snapshot(L.pip_designer.properties)
                #print(f'{properties=}')
                result_verify = self.compare(ground_truth_image, properties, similarity=0.95)
                if result_verify:
                    return True
                else:
                    return False
            elif area == 'Preview':
                preview = self.snapshot(L.pip_designer.preview)
                result_verify = self.compare(ground_truth_image, preview, similarity=0.95)
                if result_verify:
                    return True
                else:
                    return False
            elif area == 'Designer Track':
                track = self.snapshot([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW'}, {'AXRole': 'AXRow', 'index': track_index}]) # hardcode_20v3303: _NS:255 > IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW
                result_verify = self.compare(ground_truth_image, track, similarity=0.95)
                if result_verify:
                    return True
                else:
                    return False
            elif area == 'designer window':
                designer_window = self.snapshot(L.pip_designer.designer_window)
                result_verify = self.compare(ground_truth_image, designer_window, similarity=0.95)
                if result_verify:
                    return True
                else:
                    return False
            else:
                logger('Input the wrong augment')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def get_title(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            title = self.exist(L.pip_designer.designer_window).AXTitle
            return title[17:]
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def get_timecode(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            timecode = self.exist(L.pip_designer.timecode).AXValue
            return timecode
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True
    
    @step('[Action][Pip Designer] Get [Only show selected track] Checkbox Status')
    def get_selected_track_checkbox_status(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if not self.exist(L.pip_designer.show_the_selected_track):
                logger("No selected track checkbox")
                raise Exception("No selected track checkbox")
            selected_track = self.exist(L.pip_designer.show_the_selected_track).AXValue
            tick = 'Tick'
            untick = 'Untick'
            if selected_track == 1:
                return tick
            elif selected_track == 0:
                return untick
            else:
                return False
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def set_timecode(self, timecode):
        self.activate()
        elem = self.find(L.pip_designer.timecode)
        w, h = elem.AXSize
        x, y = elem.AXPosition

        pos_click = tuple(map(int, (x + w * 0.1, y + h * 0.5)))
        self.mouse.click(*pos_click)
        time.sleep(1)
        self.keyboard.send(timecode.replace("_", ""))
        self.keyboard.enter()

    def tap_menu_bar_help(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            self.exist_click(L.pip_designer.menu_bar_help)
            self.exist_click(L.pip_designer.menu_help)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def tap_undo_btn(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            self.exist_click(L.pip_designer.undo_btn)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def tap_redo_btn(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            self.exist_click(L.pip_designer.redo_btn)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True
    
    @step('[Action][Pip Designer] Resize Object on Canvas')
    def resize_on_canvas(self, drag_x=30, drag_y=30, direction='lt', is_large=True):
        try:
            target = self.exist(L.pip_designer.preview)
            ori_pos = target.AXPosition
            size_w, size_h = target.AXSize
            if not is_large:
                drag_x, drag_y = -drag_x, -drag_y
            des_pos = (ori_pos[0] - drag_x, ori_pos[1] - drag_y)
            if direction == 'rt':
                ori_pos = (ori_pos[0] + size_w, ori_pos[1])
                des_pos = (ori_pos[0] + drag_x, ori_pos[1] - drag_y)
            elif direction == 'lb':
                ori_pos = (ori_pos[0], ori_pos[1] + size_h)
                des_pos = (ori_pos[0] - drag_x, ori_pos[1] + drag_y)
            elif direction == 'rb':
                ori_pos = (ori_pos[0] + size_w, ori_pos[1] + size_h)
                des_pos = (ori_pos[0] + drag_x, ori_pos[1] + drag_y)
            self.mouse.drag_directly(ori_pos, des_pos)
            time.sleep(DELAY_TIME * 0.5)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Pip Designer] Move Object on Canvas')
    def move_to_left_on_canvas(self, drag_x=50):
        try:
            target = self.exist(L.pip_designer.preview)
            x, y = target.AXPosition
            size_w, size_h = target.AXSize

            ori_pos = (x + size_w * 0.45, y + size_h * 0.45)
            des_pos = (ori_pos[0] - drag_x, ori_pos[1])
            self.mouse.drag_directly(ori_pos, des_pos)
            time.sleep(DELAY_TIME * 0.5)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
    
    @step('[Action][Pip Designer] Add/ Remove Position Keyframe')
    def add_remove_position_current_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.position_add_remove_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Pip Designer] Reset Position Keyframe')
    def reset_position_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.position_reset_keyframe)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_yes_on_reset_all_keyframe_dialog(self):
        try:
            if not self.exist(L.pip_designer.object_setting.reset_dialog):
                logger("No reset dialog pop up")
                raise Exception
            self.exist_click(L.pip_designer.object_setting.btn_yes_reset_dialog)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True
    @step('[Action][Pip Designer] Switch to Previous Keyframe')
    def tap_position_previous_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.position_previous_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Pip Designer] Switch to Next Keyframe')
    def tap_position_next_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.position_next_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Pip Designer] Get X Position Value')
    def get_x_position_value(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if not self.exist(L.pip_designer.object_setting.x_position_value):
                raise Exception("No x position value")
            return self.exist(L.pip_designer.object_setting.x_position_value).AXValue
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    @step('[Action][Pip Designer] Input X Position Value')
    def input_x_position_value(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.click(L.pip_designer.object_setting.x_position_value)
            self.exist(L.pip_designer.object_setting.x_position_value).AXValue = str(value)
            time.sleep(DELAY_TIME)
            self.keyboard.enter()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
        ''' 
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            if float(value) < -2.000:
                logger("value can't less than -2")
                raise Exception
            elif float(value) > 2.000:
                logger("Value can't greater than 2")
                raise Exception
            self.exist_click(L.pip_designer.object_setting.x_position_value)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send('0')
            self.exist_click(L.pip_designer.object_setting.position)
            self.exist_click(L.pip_designer.object_setting.x_position_value)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(value)
            self.exist_click(L.pip_designer.object_setting.position)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True
        '''

    def click_x_position_arrow_btn(self, mode):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            if mode == 0:
                self.exist_click(L.pip_designer.object_setting.x_position_up)
            elif mode == 1:
                self.exist_click(L.pip_designer.object_setting.x_position_down)
            else:
                logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Pip Designer] Get Y Position Value')
    def get_y_position_value(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if not self.exist(L.pip_designer.object_setting.y_position_value):
                raise Exception("No y position value")
            return self.exist(L.pip_designer.object_setting.y_position_value).AXValue
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        
    @step('[Action][Pip Designer] Input Y Position Value')
    def input_y_position_value(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.click(L.pip_designer.object_setting.y_position_value)
            self.exist(L.pip_designer.object_setting.y_position_value).AXValue = str(value)
            time.sleep(DELAY_TIME)
            self.keyboard.enter()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
        '''
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            if float(value) < -2.000:
                logger("value can't less than -2")
                raise Exception
            elif float(value) > 2.000:
                logger("Value can't greater than 2")
                raise Exception
            self.exist_click(L.pip_designer.object_setting.y_position_value)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            time.sleep(1)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send('0')
            self.exist_click(L.pip_designer.object_setting.position)
            self.exist_click(L.pip_designer.object_setting.y_position_value)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(value)
            self.exist_click(L.pip_designer.object_setting.position)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True
        '''
    def click_y_position_arrow_btn(self, mode):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            if mode == 0:
                self.exist_click(L.pip_designer.object_setting.y_position_up)
            elif mode == 1:
                self.exist_click(L.pip_designer.object_setting.y_position_down)
            else:
                logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Pip Designer] Enable/ Disable Ease In Checkbox')
    def click_position_ease_in_checkbox(self, bCheck=1):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            value = self.exist(L.pip_designer.object_setting.ease_in_checkbox).AXValue
            if value == 1 and bCheck == 1:
                return True
            elif value == 1 and bCheck == 0:
                self.exist_click(L.pip_designer.object_setting.ease_in_checkbox)
            elif value == 0 and bCheck == 1:
                self.exist_click(L.pip_designer.object_setting.ease_in_checkbox)
            elif value == 0 and bCheck == 0:
                return True
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Pip Designer] Input Ease In Value')
    def input_position_ease_in_value(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            status = self.exist(L.pip_designer.object_setting.ease_in_checkbox).AXValue
            if status == 0:
                logger("Ease in box is unchecked")
                raise Exception("Ease in box is unchecked")
            else:
                if float(value) < 0.01:
                    logger("value can't less than 0.01")
                    raise Exception("value can't less than 0.01")
                elif float(value) > 1.00:
                    logger("value can't greater than 1")
                    raise Exception("value can't greater than 1")
                self.exist_click(L.pip_designer.object_setting.ease_in_value)
                self.mouse.click(times=2)
                self.keyboard.send(value)
                self.exist_click(L.pip_designer.object_setting.position)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_position_ease_in_arrow_btn(self, mode):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            status = self.exist(L.pip_designer.object_setting.ease_in_checkbox).AXValue
            if status == 0:
                logger("Ease in box is unchecked")
            else:
                if mode == 0:
                    self.exist_click(L.pip_designer.object_setting.ease_in_value_up)
                elif mode == 1:
                    self.exist_click(L.pip_designer.object_setting.ease_in_value_down)
                else:
                    logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
                    raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_position_ease_in_slider(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            status = self.exist(L.pip_designer.object_setting.ease_in_checkbox).AXValue
            if status == 0:
                logger("Ease in box is unchecked")
            else:
                self.exist(L.pip_designer.object_setting.ease_in_slider).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Pip Designer] Enable/ Disable Ease Out Checkbox')
    def click_position_ease_out_checkbox(self, bCheck=1):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            value = self.exist(L.pip_designer.object_setting.ease_out_checkbox).AXValue
            if value == 1 and bCheck == 1:
                return True
            elif value == 1 and bCheck == 0:
                self.exist_click(L.pip_designer.object_setting.ease_out_checkbox)
            elif value == 0 and bCheck == 1:
                self.exist_click(L.pip_designer.object_setting.ease_out_checkbox)
            elif value == 0 and bCheck == 0:
                return True
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Pip Designer] Input Ease Out Value')
    def input_position_ease_out_value(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            status = self.exist(L.pip_designer.object_setting.ease_out_checkbox).AXValue
            if status == 0:
                logger("Ease out box is unchecked")
                raise Exception("Ease out box is unchecked")
            else:
                if float(value) < 0.01:
                    logger("value can't less than 0.01")
                    raise Exception("value can't less than 0.01")
                elif float(value) > 1.00:
                    logger("value can't greater than 1")
                    raise Exception("value can't greater than 1")
                self.exist_click(L.pip_designer.object_setting.ease_out_value)
                self.mouse.click(times=2)
                self.keyboard.send(value)
                self.exist_click(L.pip_designer.object_setting.position)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_position_ease_out_arrow_btn(self, mode):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            status = self.exist(L.pip_designer.object_setting.ease_out_checkbox).AXValue
            if status == 0:
                logger("Ease out box is unchecked")
                raise Exception
            else:
                if mode == 0:
                    self.exist_click(L.pip_designer.object_setting.ease_out_value_up)
                elif mode == 1:
                    self.exist_click(L.pip_designer.object_setting.ease_out_value_down)
                else:
                    logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
                    raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_position_ease_out_slider(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            status = self.exist(L.pip_designer.object_setting.ease_out_checkbox).AXValue
            if status == 0:
                logger("Ease out box is unchecked")
            else:
                self.exist(L.pip_designer.object_setting.ease_out_slider).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Pip Designer] Add/ Remove Scale Keyframe')
    def add_remove_scale_current_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.scale.add_remove_current_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def reset_scale_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.scale.reset_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Pip Designer] Switch to Scale Previous Keyframe')
    def tap_scale_previous_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.scale.previous_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Pip Designer] Switch to Scale Next Keyframe')
    def tap_scale_next_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.scale.next_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Pip Designer] Get Scale Width Value')
    def get_scale_width_value(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            value = self.exist(L.pip_designer.object_setting.scale.width_value).AXValue
            return value
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        
    def input_scale_width_value(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.scale.width_value)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(value)
            self.exist_click(L.pip_designer.object_setting.scale.scale)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_scale_width_arrow_btn(self, mode):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            if mode == 0:
                self.exist_click(L.pip_designer.object_setting.scale.width_value_up)
            elif mode == 1:
                self.exist_click(L.pip_designer.object_setting.scale.width_value_down)
            else:
                logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_scale_width_slider(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist(L.pip_designer.object_setting.scale.width_slider).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Pip Designer] Get Scale Height Value')
    def get_scale_height_value(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No title designer window show up")
                raise Exception("No title designer window show up")
            value = self.exist(L.pip_designer.object_setting.scale.height_value).AXValue
            return value
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
    
    @step('[Action][Pip Designer] Input Scale Height Value')
    def input_scale_height_value(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.scale.height_value)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(value)
            self.exist_click(L.pip_designer.object_setting.scale.scale)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_scale_height_arrow_btn(self, mode):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            if mode == 0:
                self.exist_click(L.pip_designer.object_setting.scale.height_value_up)
            elif mode == 1:
                self.exist_click(L.pip_designer.object_setting.scale.height_value_down)
            else:
                logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_scale_height_slider(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist(L.pip_designer.object_setting.scale.height_slider).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_scale_maintain_aspect_ratio(self, bCheck=1):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            value = self.exist(L.pip_designer.object_setting.scale.maintain_aspect_ratio).AXValue
            if value == 1 and bCheck == 1:
                return True
            elif value == 1 and bCheck == 0:
                self.exist_click(L.pip_designer.object_setting.scale.maintain_aspect_ratio)
            elif value == 0 and bCheck == 1:
                self.exist_click(L.pip_designer.object_setting.scale.maintain_aspect_ratio)
            elif value == 0 and bCheck == 0:
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_scale_ease_in_checkbox(self, bCheck=1):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            value = self.exist(L.pip_designer.object_setting.scale.ease_in_checkbox).AXValue
            if value == 1 and bCheck == 1:
                return True
            elif value == 1 and bCheck == 0:
                self.exist_click(L.pip_designer.object_setting.scale.ease_in_checkbox)
            elif value == 0 and bCheck == 1:
                self.exist_click(L.pip_designer.object_setting.scale.ease_in_checkbox)
            elif value == 0 and bCheck == 0:
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def input_scale_ease_in_value(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            status = self.exist(L.pip_designer.object_setting.scale.ease_in_checkbox).AXValue
            if status == 0:
                logger("Ease in box is unchecked")
                raise Exception
            else:
                if float(value) < 0.01:
                    logger("value can't less than 0.01")
                    raise Exception
                elif float(value) > 1.00:
                    logger("value can't greater than 1")
                    raise Exception
                self.exist_click(L.pip_designer.object_setting.scale.ease_in_value)
                self.mouse.click(times=2)
                self.keyboard.send(value)
                self.exist_click(L.pip_designer.object_setting.scale.scale)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_scale_ease_in_arrow_btn(self, mode):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            status = self.exist(L.pip_designer.object_setting.scale.ease_in_checkbox).AXValue
            if status == 0:
                logger("Ease in box is unchecked")
                raise Exception
            else:
                if mode == 0:
                    self.exist_click(L.pip_designer.object_setting.scale.ease_in_value_up)
                elif mode == 1:
                    self.exist_click(L.pip_designer.object_setting.scale.ease_in_value_down)
                else:
                    logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
                    raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_scale_ease_in_slider(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            status = self.exist(L.pip_designer.object_setting.scale.ease_in_checkbox).AXValue
            if status == 0:
                logger("Ease in box is unchecked")
                raise Exception
            else:
                self.exist(L.pip_designer.object_setting.scale.ease_in_slider).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_scale_ease_out_checkbox(self, bCheck=1):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            value = self.exist(L.pip_designer.object_setting.scale.ease_out_checkbox).AXValue
            if value == 1 and bCheck == 1:
                return True
            elif value == 1 and bCheck == 0:
                self.exist_click(L.pip_designer.object_setting.scale.ease_out_checkbox)
            elif value == 0 and bCheck == 1:
                self.exist_click(L.pip_designer.object_setting.scale.ease_out_checkbox)
            elif value == 0 and bCheck == 0:
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def input_scale_ease_out_value(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            status = self.exist(L.pip_designer.object_setting.scale.ease_out_checkbox).AXValue
            if status == 0:
                logger("Ease out box is unchecked")
                raise Exception
            else:
                if float(value) < 0.01:
                    logger("value can't less than 0.01")
                    raise Exception
                elif float(value) > 1.00:
                    logger("value can't greater than 1")
                    raise Exception
                self.exist_click(L.pip_designer.object_setting.scale.ease_out_value)
                self.mouse.click(times=2)
                self.keyboard.send(value)
                self.exist_click(L.pip_designer.object_setting.scale.scale)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_scale_ease_out_arrow_btn(self, mode):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            status = self.exist(L.pip_designer.object_setting.scale.ease_out_checkbox).AXValue
            if status == 0:
                logger("Ease out box is unchecked")
                raise Exception
            else:
                if mode == 0:
                    self.exist_click(L.pip_designer.object_setting.scale.ease_out_value_up)
                elif mode == 1:
                    self.exist_click(L.pip_designer.object_setting.scale.ease_out_value_down)
                else:
                    logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
                    raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_scale_ease_out_slider(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            status = self.exist(L.pip_designer.object_setting.scale.ease_out_checkbox).AXValue
            if status == 0:
                logger("Ease in box is unchecked")
                raise Exception
            else:
                self.exist(L.pip_designer.object_setting.scale.ease_out_slider).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def add_remove_position_opacity_current_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.opacity.add_remove_current_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def reset_position_opacity_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.opacity.reset_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def tap_position_opacity_previous_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.opacity.previous_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def tap_position_opacity_next_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.opacity.next_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def input_position_opacity_value(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.opacity.opacity_value)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(value)
            self.exist_click(L.pip_designer.object_setting.opacity.opacity)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_position_opacity_arrow_btn(self, mode):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            if mode == 0:
                self.exist_click(L.pip_designer.object_setting.opacity.opacity_value_up)
            elif mode == 1:
                self.exist_click(L.pip_designer.object_setting.opacity.opacity_value_down)
            else:
                logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_position_opacity_slider(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist(L.pip_designer.object_setting.opacity.opacity_slider).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def set_blending_mode_normal(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.opacity.blending_mode)
            self.exist_click(L.pip_designer.object_setting.opacity.blending_mode_normal)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def set_blending_mode_overlay(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.opacity.blending_mode)
            self.exist_click(L.pip_designer.object_setting.opacity.blending_mode_overlay)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def set_blending_mode_multiply(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.opacity.blending_mode)
            self.exist_click(L.pip_designer.object_setting.opacity.blending_mode_multiply)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def set_blending_mode_screen(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.opacity.blending_mode)
            self.exist_click(L.pip_designer.object_setting.opacity.blending_mode_screen)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def set_blending_mode_lighten(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.opacity.blending_mode)
            self.exist_click(L.pip_designer.object_setting.opacity.blending_mode_lighten)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def set_blending_mode_darken(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.opacity.blending_mode)
            self.exist_click(L.pip_designer.object_setting.opacity.blending_mode_darken)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def set_blending_mode_difference(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.opacity.blending_mode)
            self.exist_click(L.pip_designer.object_setting.opacity.blending_mode_difference)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def set_blending_mode_hue(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.opacity.blending_mode)
            self.exist_click(L.pip_designer.object_setting.opacity.blending_mode_hue)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def add_remove_rotation_current_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.rotation.add_remove_current_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def reset_rotation_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.rotation.reset_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def tap_rotation_previous_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.rotation.previous_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Pip Designer] Input Rotation Degree Value')
    def input_rotation_degree_value(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            if float(value) < -9999.000:
                logger("value can't less than -9999")
                raise Exception("value can't less than -9999")
            elif float(value) > 9999.000:
                logger("Value can't greater than 9999")
                raise Exception("Value can't greater than 9999")

            self.exist_click(L.pip_designer.object_setting.rotation.degree_value)
            self.exist(L.pip_designer.object_setting.rotation.degree_value).AXValue = str(value)
            time.sleep(DELAY_TIME)
            self.press_enter_key()
            '''
            self.exist_click(L.pip_designer.object_setting.rotation.degree_value)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send('0')
            self.exist_click(L.pip_designer.object_setting.rotation.rotation)
            self.exist_click(L.pip_designer.object_setting.rotation.degree_value)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(value)
            self.exist_click(L.pip_designer.object_setting.rotation.rotation)
            '''
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Pip Designer] Switch to Rotation Next Keyframe')
    def tap_rotation_next_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            self.exist_click(L.pip_designer.object_setting.rotation.next_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_rotation_degree_arrow_btn(self, mode):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            if mode == 0:
                self.exist_click(L.pip_designer.object_setting.rotation.degree_value_up)
            elif mode == 1:
                self.exist_click(L.pip_designer.object_setting.rotation.degree_value_down)
            else:
                logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_rotation_ease_in_checkbox(self, bCheck=1):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            value = self.exist(L.pip_designer.object_setting.rotation.ease_in_checkbox).AXValue
            if value == 1 and bCheck == 1:
                return True
            elif value == 1 and bCheck == 0:
                self.exist_click(L.pip_designer.object_setting.rotation.ease_in_checkbox)
            elif value == 0 and bCheck == 1:
                self.exist_click(L.pip_designer.object_setting.rotation.ease_in_checkbox)
            elif value == 0 and bCheck == 0:
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def input_rotation_ease_in_value(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            status = self.exist(L.pip_designer.object_setting.rotation.ease_in_checkbox).AXValue
            if status == 0:
                logger("Ease in box is unchecked")
                raise Exception
            else:
                if float(value) < 0.01:
                    logger("value can't less than 0.01")
                    raise Exception
                elif float(value) > 1.00:
                    logger("value can't greater than 1")
                    raise Exception
                self.exist_click(L.pip_designer.object_setting.rotation.ease_in_value)
                self.mouse.click(times=2)
                self.keyboard.send(value)
                self.exist_click(L.pip_designer.object_setting.rotation.rotation)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_rotation_ease_in_arrow_btn(self, mode):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            status = self.exist(L.pip_designer.object_setting.rotation.ease_in_checkbox).AXValue
            if status == 0:
                logger("Ease in box is unchecked")
            else:
                if mode == 0:
                    self.exist_click(L.pip_designer.object_setting.rotation.ease_in_value_up)
                elif mode == 1:
                    self.exist_click(L.pip_designer.object_setting.rotation.ease_in_value_down)
                else:
                    logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
                    raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_rotation_ease_in_slider(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            status = self.exist(L.pip_designer.object_setting.rotation.ease_in_checkbox).AXValue
            if status == 0:
                logger("Ease in box is unchecked")
            else:
                self.exist(L.pip_designer.object_setting.rotation.ease_in_slider).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_rotation_ease_out_checkbox(self, bCheck=1):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            value = self.exist(L.pip_designer.object_setting.rotation.ease_out_checkbox).AXValue
            if value == 1 and bCheck == 1:
                return True
            elif value == 1 and bCheck == 0:
                self.exist_click(L.pip_designer.object_setting.rotation.ease_out_checkbox)
            elif value == 0 and bCheck == 1:
                self.exist_click(L.pip_designer.object_setting.rotation.ease_out_checkbox)
            elif value == 0 and bCheck == 0:
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def input_rotation_ease_out_value(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            status = self.exist(L.pip_designer.object_setting.rotation.ease_out_checkbox).AXValue
            if status == 0:
                logger("Ease out box is unchecked")
                raise Exception
            else:
                if float(value) < 0.01:
                    logger("value can't less than 0.01")
                    raise Exception
                elif float(value) > 1.00:
                    logger("value can't greater than 1")
                    raise Exception
                self.exist_click(L.pip_designer.object_setting.rotation.ease_out_value)
                self.mouse.click(times=2)
                self.keyboard.send(value)
                self.exist_click(L.pip_designer.object_setting.rotation.rotation)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_rotation_ease_out_arrow_btn(self, mode):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            status = self.exist(L.pip_designer.object_setting.rotation.ease_out_checkbox).AXValue
            if status == 0:
                logger("Ease out box is unchecked")
            else:
                if mode == 0:
                    self.exist_click(L.pip_designer.object_setting.rotation.ease_out_value_up)
                elif mode == 1:
                    self.exist_click(L.pip_designer.object_setting.rotation.ease_out_value_down)
                else:
                    logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
                    raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_rotation_ease_out_slider(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.object_setting.object_setting).AXValue == 0:
                self.exist_click(L.pip_designer.object_setting.object_setting)
            status = self.exist(L.pip_designer.object_setting.rotation.ease_out_checkbox).AXValue
            if status == 0:
                logger("Ease out box is unchecked")
            else:
                self.exist(L.pip_designer.object_setting.rotation.ease_out_slider).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Pip Designer] Enable/ Disable Chromakey')
    def apply_chromakey(self, bApply=1):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if self.exist(L.pip_designer.chromakey.chroma_key).AXValue == 0:
                self.exist_click(L.pip_designer.chromakey.chroma_key)
            value = self.exist(L.pip_designer.chromakey.chromakey_checkbox).AXValue
            if value == 1 and bApply == 1:
                return True
            elif value == 1 and bApply == 0:
                self.exist_click(L.pip_designer.chromakey.chromakey_checkbox)
            elif value == 0 and bApply == 1:
                self.exist_click(L.pip_designer.chromakey.chromakey_checkbox)
            elif value == 0 and bApply == 0:
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def add_chromakey_new_key(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.chromakey.chroma_key).AXValue == 0:
                self.exist_click(L.pip_designer.chromakey.chroma_key)
            self.exist_click(L.pip_designer.chromakey.add_new_key)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def tap_chromakey_remove_btn(self, index=0):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.chromakey.chroma_key).AXValue == 0:
                self.exist_click(L.pip_designer.chromakey.chroma_key)
            self.exist_click({'AXIdentifier': 'IDC_CHROMAKEY_BTN_REMOVE', 'AXRoleDescription': 'button', 'index': index})
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def input_color_range_value(self, value, index=0):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.chromakey.chroma_key).AXValue == 0:
                self.exist_click(L.pip_designer.chromakey.chroma_key)
            if int(value) < 0:
                logger("value can't less than 0")
                raise Exception
            elif int(value) > 60:
                logger("value can't greater than 60")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_CHROMAKEY_SPINEDIT_COLOR_RANGE', 'AXRoleDescription': 'group', 'index': index}, {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field'}])
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(value)
            self.exist_click(L.pip_designer.chromakey.chromakey_title)
            self.exist_click(L.pip_designer.chromakey.chromakey_title)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_color_range_arrow_btn(self, mode, index=0):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.chromakey.chroma_key).AXValue == 0:
                self.exist_click(L.pip_designer.chromakey.chroma_key)
            if mode == 0:
                self.exist_click([{'AXIdentifier': 'IDC_CHROMAKEY_SPINEDIT_COLOR_RANGE', 'AXRoleDescription': 'group', 'index': index}, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP', 'AXRoleDescription': 'button'}])
            elif mode == 1:
                self.exist_click([{'AXIdentifier': 'IDC_CHROMAKEY_SPINEDIT_COLOR_RANGE', 'AXRoleDescription': 'group', 'index': index}, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN', 'AXRoleDescription': 'button'}])
            else:
                logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_color_range_slider(self, value, index=0):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.chromakey.chroma_key).AXValue == 0:
                self.exist_click(L.pip_designer.chromakey.chroma_key)
            if int(value) < 0:
                logger("value can't less than 0")
                raise Exception
            elif int(value) > 60:
                logger("value can't greater than 60")
                raise Exception
            self.exist({'AXIdentifier': 'IDC_PIP_DESIGNER_CHROMAKEY_SLIDER_COLORRANGE', 'AXRoleDescription': 'slider', 'index': index}).AXValue = int(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def input_denoise_value(self, value, index=0):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.chromakey.chroma_key).AXValue == 0:
                self.exist_click(L.pip_designer.chromakey.chroma_key)
            if int(value) < 0:
                logger("value can't less than 0")
                raise Exception
            elif int(value) > 100:
                logger("value can't greater than 100")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_CHROMAKEY_SPINEDIT_DENOISE', 'AXRoleDescription': 'group', 'index': index}, {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field'}])
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(value)
            self.keyboard.pressed(self.keyboard.key.enter)
            self.exist_click(L.pip_designer.chromakey.chromakey_title)
            self.exist_click(L.pip_designer.chromakey.chromakey_title)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_denoise_arrow_btn(self, mode, index=0):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.chromakey.chroma_key).AXValue == 0:
                self.exist_click(L.pip_designer.chromakey.chroma_key)
            if mode == 0:
                self.exist_click([{'AXIdentifier': 'IDC_CHROMAKEY_SPINEDIT_DENOISE', 'AXRoleDescription': 'group', 'index': index}, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP', 'AXRoleDescription': 'button'}])
            elif mode == 1:
                self.exist_click([{'AXIdentifier': 'IDC_CHROMAKEY_SPINEDIT_DENOISE', 'AXRoleDescription': 'group', 'index': index}, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN', 'AXRoleDescription': 'button'}])
            else:
                logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_denoise_slider(self, value, index=0):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.chromakey.chroma_key).AXValue == 0:
                self.exist_click(L.pip_designer.chromakey.chroma_key)
            if int(value) < 0:
                logger("value can't less than 0")
                raise Exception
            elif int(value) > 100:
                logger("value can't greater than 100")
                raise Exception
            self.exist({'AXIdentifier': 'IDC_PIP_DESIGNER_CHROMAKEY_SLIDER_DENOISE', 'AXRoleDescription': 'slider', 'index': index}).AXValue = int(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Pip Designer] Enable/ Disable Border')
    def apply_border(self, bApply=1):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if self.exist(L.pip_designer.border.border).AXValue == 0:
                self.exist_click(L.pip_designer.border.border)
            value = self.exist(L.pip_designer.border.border_checkbox).AXValue
            if value == 1 and bApply == 1:
                return True
            elif value == 1 and bApply == 0:
                self.exist_click(L.pip_designer.border.border_checkbox)
            elif value == 0 and bApply == 1:
                self.exist_click(L.pip_designer.border.border_checkbox)
            elif value == 0 and bApply == 0:
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Pip Designer] Set [Border Size] by Slider')
    def drag_border_size_slider(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if self.exist(L.pip_designer.border.border).AXValue == 0:
                self.exist_click(L.pip_designer.border.border)
            if int(value) < 0:
                logger("value can't less than 0")
                raise Exception("value can't less than 0")
            elif int(value) > 10:
                logger("value can't greater than 10")
                raise Exception("value can't greater than 10")
            self.exist(L.pip_designer.border.size_slider).AXValue = int(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def input_border_size_value(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.border.border).AXValue == 0:
                self.exist_click(L.pip_designer.border.border)
            if int(value) < 0:
                logger("value can't less than 0")
                raise Exception
            elif int(value) > 10:
                logger("value can't greater than 10")
                raise Exception
            self.exist_click(L.pip_designer.border.size_value)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(value)
            self.exist_click(L.pip_designer.border.size_title)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_border_size_arrow_btn(self, mode):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.border.border).AXValue == 0:
                self.exist_click(L.pip_designer.border.border)
            if mode == 0:
                self.exist_click(L.pip_designer.border.size_value_up)
            elif mode == 1:
                self.exist_click(L.pip_designer.border.size_value_down)
            else:
                logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_border_blur_slider(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.border.border).AXValue == 0:
                self.exist_click(L.pip_designer.border.border)
            if int(value) < 0:
                logger("value can't less than 0")
                raise Exception
            elif int(value) > 20:
                logger("value can't greater than 20")
                raise Exception
            self.exist(L.pip_designer.border.blur_slider).AXValue = int(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Pip Designer] Input Border Blur Value')
    def input_border_blur_value(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if self.exist(L.pip_designer.border.border).AXValue == 0:
                self.exist_click(L.pip_designer.border.border)
            if int(value) < 0:
                logger("value can't less than 0")
                raise Exception("value can't less than 0")
            elif int(value) > 20:
                logger("value can't greater than 20")
                raise Exception("value can't greater than 20")
            self.exist_click(L.pip_designer.border.blur_value_box)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(value)
            self.exist_click(L.pip_designer.border.blur_title)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_border_blur_arrow_btn(self, mode):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.border.border).AXValue == 0:
                self.exist_click(L.pip_designer.border.border)
            if mode == 0:
                self.exist_click(L.pip_designer.border.blur_value_up)
            elif mode == 1:
                self.exist_click(L.pip_designer.border.blur_value_down)
            else:
                logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Pip Designer] Apply Border Opacity')
    def drag_border_opacity_slider(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if self.exist(L.pip_designer.border.border).AXValue == 0:
                self.exist_click(L.pip_designer.border.border)
            if int(value) < 0:
                logger("value can't less than 0")
                raise Exception("value can't less than 0")
            elif int(value) > 100:
                logger("value can't greater than 100")
                raise Exception("value can't greater than 100")
            self.exist(L.pip_designer.border.opacity_slider).AXValue = int(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def input_border_opacity_value(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.border.border).AXValue == 0:
                self.exist_click(L.pip_designer.border.border)
            if int(value) < 0:
                logger("value can't less than 0")
                raise Exception
            elif int(value) > 100:
                logger("value can't greater than 100")
                raise Exception
            self.exist_click(L.pip_designer.border.opacity_value)
            self.mouse.click(times=3)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(value)
            self.exist_click(L.pip_designer.border.opacity_title)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_border_opacity_arrow_btn(self, mode):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.border.border).AXValue == 0:
                self.exist_click(L.pip_designer.border.border)
            if mode == 0:
                self.exist_click(L.pip_designer.border.opacity_value_up)
            elif mode == 1:
                self.exist_click(L.pip_designer.border.opacity_value_down)
            else:
                logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Pip Designer] Apply [Border Uniform Color] by RGB code')
    def apply_border_uniform_color(self, red='255', green='255', blue='255'):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if self.exist(L.pip_designer.border.border).AXValue == 0:
                self.exist_click(L.pip_designer.border.border)
            self.exist_click(L.pip_designer.border.fill_type)
            self.exist_click(L.pip_designer.border.fill_type_uniform_color)
            self.exist_click(L.pip_designer.border.uniform_color)
            self.color_picker_switch_category_to_RGB() # switch to Colors > RGB sliders [20.0.3303]
            self.exist_click(L.pip_designer.border.red)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(red)
            self.exist_click(L.pip_designer.border.green)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(green)
            self.exist_click(L.pip_designer.border.blue)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(blue)
            self.exist_click(L.pip_designer.border.red)
            self.exist_click(L.pip_designer.border.uniform_color_close_button)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def apply_border_2_color(self, red1='255', green1='255', blue1='255', red2='255', green2='255', blue2='255'):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.border.border).AXValue == 0:
                self.exist_click(L.pip_designer.border.border)
            self.exist_click(L.pip_designer.border.fill_type)
            self.exist_click(L.pip_designer.border.fill_type_2_color_gradient)
            self.exist_click(L.pip_designer.border.begin_with)
            self.color_picker_switch_category_to_RGB()  # switch to Colors > RGB sliders [20.0.3303]
            self.exist_click(L.pip_designer.border.red)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(red1)
            self.exist_click(L.pip_designer.border.green)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(green1)
            self.exist_click(L.pip_designer.border.blue)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(blue1)
            self.exist_click(L.pip_designer.border.red)
            self.exist_click(L.pip_designer.border.uniform_color_close_button)
            self.exist_click(L.pip_designer.border.end_with)
            self.color_picker_switch_category_to_RGB()  # switch to Colors > RGB sliders [20.0.3303]
            self.exist_click(L.pip_designer.border.red)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(red2)
            self.exist_click(L.pip_designer.border.green)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(green2)
            self.exist_click(L.pip_designer.border.blue)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(blue2)
            self.exist_click(L.pip_designer.border.red)
            self.exist_click(L.pip_designer.border.uniform_color_close_button)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def apply_border_4_color(self, red1='255', green1='255', blue1='255', red2='255', green2='255',
                             blue2='255', red3='255', green3='255', blue3='255', red4='255', green4='255', blue4='255'):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.border.border).AXValue == 0:
                self.exist_click(L.pip_designer.border.border)
            self.exist_click(L.pip_designer.border.fill_type)
            self.exist_click(L.pip_designer.border.fill_type_4_color_gradient)
            four_color_gradient = self.exist(L.pip_designer.border.four_color_gradient)
            x, y = four_color_gradient.AXPosition
            self.mouse.move(int(x+5), int(y+5))
            self.mouse.click()
            self.color_picker_switch_category_to_RGB()  # switch to Colors > RGB sliders [20.0.3303]
            self.exist_click(L.pip_designer.border.red)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(red1)
            self.exist_click(L.pip_designer.border.green)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(green1)
            self.exist_click(L.pip_designer.border.blue)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(blue1)
            self.exist_click(L.pip_designer.border.red)
            self.exist_click(L.pip_designer.border.uniform_color_close_button)
            self.mouse.move(int(x + 170), int(y + 5))
            self.mouse.click()
            self.color_picker_switch_category_to_RGB()  # switch to Colors > RGB sliders [20.0.3303]
            self.exist_click(L.pip_designer.border.red)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(red2)
            self.exist_click(L.pip_designer.border.green)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(green2)
            self.exist_click(L.pip_designer.border.blue)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(blue2)
            self.exist_click(L.pip_designer.border.red)
            self.exist_click(L.pip_designer.border.uniform_color_close_button)
            self.mouse.move(int(x + 5), int(y + 57))
            self.mouse.click()
            self.color_picker_switch_category_to_RGB()  # switch to Colors > RGB sliders [20.0.3303]
            self.exist_click(L.pip_designer.border.red)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(red3)
            self.exist_click(L.pip_designer.border.green)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(green3)
            self.exist_click(L.pip_designer.border.blue)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(blue3)
            self.exist_click(L.pip_designer.border.red)
            self.exist_click(L.pip_designer.border.uniform_color_close_button)
            self.mouse.move(int(x + 170), int(y + 57))
            self.mouse.click()
            self.color_picker_switch_category_to_RGB()  # switch to Colors > RGB sliders [20.0.3303]
            self.exist_click(L.pip_designer.border.red)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(red4)
            self.exist_click(L.pip_designer.border.green)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(green4)
            self.exist_click(L.pip_designer.border.blue)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(blue4)
            self.exist_click(L.pip_designer.border.red)
            self.exist_click(L.pip_designer.border.uniform_color_close_button)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Pip Designer] Enable/ Disable Shadow')
    def apply_shadow(self, bApply=1):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if self.exist(L.pip_designer.shadow.shadow).AXValue == 0:
                self.exist_click(L.pip_designer.shadow.shadow)
            value = self.exist(L.pip_designer.shadow.shadow_checkbox).AXValue
            if value == 1 and bApply == 1:
                return True
            elif value == 1 and bApply == 0:
                self.exist_click(L.pip_designer.shadow.shadow_checkbox)
            elif value == 0 and bApply == 1:
                self.exist_click(L.pip_designer.shadow.shadow_checkbox)
            elif value == 0 and bApply == 0:
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def apply_shadow_to(self, index):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.shadow.shadow).AXValue == 0:
                self.exist_click(L.pip_designer.shadow.shadow)
            self.exist_click(L.pip_designer.shadow.apply_shadow_to)
            if index == 0:
                self.exist_click(L.pip_designer.shadow.apply_shadow_to_object_and_border)
            elif index == 1:
                self.exist_click(L.pip_designer.shadow.apply_shadow_to_object_only)
            elif index == 2:
                self.exist_click(L.pip_designer.shadow.apply_shadow_to_border_only)
            else:
                logger("Input the wrong augment")
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Pip Designer] Set [Shadow Distance] by Slider')
    def drag_shadow_distance_slider(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if self.exist(L.pip_designer.shadow.shadow).AXValue == 0:
                self.exist_click(L.pip_designer.shadow.shadow)
            if float(value) < 0.0:
                logger("value can't less than 0")
                raise Exception("value can't less than 0")
            elif float(value) > 100.0:
                logger("value can't greater than 100")
                raise Exception("value can't greater than 100")
            self.exist(L.pip_designer.shadow.distance_slider).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Pip Designer] Input Shadow Distance Value')
    def input_shadow_distance_value(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if self.exist(L.pip_designer.shadow.shadow).AXValue == 0:
                self.exist_click(L.pip_designer.shadow.shadow)
            if float(value) < 0.00:
                logger("value can't less than 0.0")
                raise Exception("value can't less than 0.0")
            elif float(value) > 100.00:
                logger("value can't greater than 100.0")
                raise Exception("value can't greater than 100.0")
            self.exist_click(L.pip_designer.shadow.distance_value_box)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(value)
            self.exist_click(L.pip_designer.shadow.distance_title)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_shadow_distance_arrow_btn(self, mode):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.shadow.shadow).AXValue == 0:
                self.exist_click(L.pip_designer.shadow.shadow)
            if mode == 0:
                self.exist_click(L.pip_designer.shadow.distance_value_up)
            elif mode == 1:
                self.exist_click(L.pip_designer.shadow.distance_value_down)
            else:
                logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_shadow_blur_slider(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.shadow.shadow).AXValue == 0:
                self.exist_click(L.pip_designer.shadow.shadow)
            if int(value) < 0:
                logger("value can't less than 0")
                raise Exception
            elif int(value) > 20:
                logger("value can't greater than 20")
                raise Exception
            self.exist(L.pip_designer.shadow.blur_slider).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def input_shadow_blur_value(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.shadow.shadow).AXValue == 0:
                self.exist_click(L.pip_designer.shadow.shadow)
            if int(value) < 0:
                logger("value can't less than 0")
                raise Exception
            elif int(value) > 20:
                logger("value can't greater than 20")
                raise Exception
            self.exist_click(L.pip_designer.shadow.blur_value_box)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(value)
            self.exist_click(L.pip_designer.shadow.blur_title)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_shadow_blur_arrow_btn(self, mode):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.shadow.shadow).AXValue == 0:
                self.exist_click(L.pip_designer.shadow.shadow)
            if mode == 0:
                self.exist_click(L.pip_designer.shadow.blur_value_up)
            elif mode == 1:
                self.exist_click(L.pip_designer.shadow.blur_value_down)
            else:
                logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_shadow_opacity_slider(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.shadow.shadow).AXValue == 0:
                self.exist_click(L.pip_designer.shadow.shadow)
            if int(value) < 0:
                logger("value can't less than 0")
                raise Exception
            elif int(value) > 100:
                logger("value can't greater than 100")
                raise Exception
            self.exist(L.pip_designer.shadow.opacity_slider).AXValue = int(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def input_shadow_opacity_value(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.shadow.shadow).AXValue == 0:
                self.exist_click(L.pip_designer.shadow.shadow)
            if int(value) < 0:
                logger("value can't less than 0")
                raise Exception
            elif int(value) > 100:
                logger("value can't greater than 100")
                raise Exception
            self.exist_click(L.pip_designer.shadow.opacity_value_box)
            self.mouse.click(times=3)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(value)
            self.exist_click(L.pip_designer.shadow.opacity_title)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_shadow_opacity_arrow_btn(self, mode):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.shadow.shadow).AXValue == 0:
                self.exist_click(L.pip_designer.shadow.shadow)
            if mode == 0:
                self.exist_click(L.pip_designer.shadow.opacity_value_up)
            elif mode == 1:
                self.exist_click(L.pip_designer.shadow.opacity_value_down)
            else:
                logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Pip Designer] Select [Shadow Color] by RGB color')
    def select_shadow_color(self, red='0', green='0', blue="0"):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.shadow.shadow).AXValue == 0:
                self.exist_click(L.pip_designer.shadow.shadow)
            self.exist_click(L.pip_designer.shadow.select_color)
            self.color_picker_switch_category_to_RGB()  # switch to Colors > RGB sliders [20.0.3303]
            self.exist_click(L.pip_designer.shadow.red)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(red)
            self.exist_click(L.pip_designer.shadow.green)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(green)
            self.exist_click(L.pip_designer.shadow.blue)
            self.mouse.click(times=2)
            self.keyboard.pressed(self.keyboard.key.delete)
            self.keyboard.send(blue)
            self.exist_click(L.pip_designer.shadow.select_color_close)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def apply_flip(self, bApply=1):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.flip.flip).AXValue == 0:
                self.exist_click(L.pip_designer.flip.flip)
            value = self.exist(L.pip_designer.flip.flip_checkbox).AXValue
            if value == 1 and bApply == 1:
                return True
            elif value == 1 and bApply == 0:
                self.exist_click(L.pip_designer.flip.flip_checkbox)
            elif value == 0 and bApply == 1:
                self.exist_click(L.pip_designer.flip.flip_checkbox)
            elif value == 0 and bApply == 0:
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def apply_flip_type(self, index):
        try:
            if self.exist(L.pip_designer.flip.flip_checkbox).AXValue == 0:
                logger("Flip didn't apply")
                raise Exception
            if self.exist(L.pip_designer.flip.flip).AXValue == 0:
                self.exist_click(L.pip_designer.flip.flip)
            if index == 0:
                self.exist_click(L.pip_designer.flip.upside_down)
            elif index == 1:
                self.exist_click(L.pip_designer.flip.left_to_right)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def apply_fades(self, bApply=1):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception
            if self.exist(L.pip_designer.fades.fades):
                value = self.exist(L.pip_designer.fades.fades_checkbox).AXValue
                if value == 1 and bApply == 1:
                   return True
                elif value == 1 and bApply == 0:
                   self.exist_click(L.pip_designer.fades.fades_checkbox)
                   return True
                elif value == 0 and bApply == 1:
                   self.exist_click(L.pip_designer.fades.fades_checkbox)
                   return True
                elif value == 0 and bApply == 0:
                   return True
            value1 = self.exist(L.pip_designer.fades.fades_express_checkbox).AXValue
            if value1 == 1 and bApply == 1:
                return True
            elif value1 == 1 and bApply == 0:
                self.exist_click(L.pip_designer.fades.fades_express_checkbox)
                return True
            elif value1 == 0 and bApply == 1:
                self.exist_click(L.pip_designer.fades.fades_express_checkbox)
                return True
            elif value1 == 0 and bApply == 0:
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Pip Designer] Apply Enable Fade In')
    def apply_enable_fade_in(self, bApply=1):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if self.exist(L.pip_designer.fades.fades):
                if self.exist(L.pip_designer.fades.fades).AXValue == 0:
                    self.exist_click(L.pip_designer.fades.fades)
                value = self.exist(L.pip_designer.fades.enable_fade_in).AXValue
                if value == 1 and bApply == 1:
                   return True
                elif value == 1 and bApply == 0:
                   self.exist_click(L.pip_designer.fades.enable_fade_in)
                   return True
                elif value == 0 and bApply == 1:
                   self.exist_click(L.pip_designer.fades.enable_fade_in)
                   return True
                elif value == 0 and bApply == 0:
                   return True
            else:
                if self.exist(L.pip_designer.flip.flip).AXValue == 0:
                    self.exist_click(L.pip_designer.flip.flip)
                value1 = self.exist(L.pip_designer.fades.enable_fade_in).AXValue
                if value1 == 1 and bApply == 1:
                    return True
                elif value1 == 1 and bApply == 0:
                    self.exist_click(L.pip_designer.fades.enable_fade_in)
                    return True
                elif value1 == 0 and bApply == 1:
                    self.exist_click(L.pip_designer.fades.enable_fade_in)
                    return True
                elif value1 == 0 and bApply == 0:
                    return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Pip Designer] Apply Enable Fade Out')
    def apply_enable_fade_out(self, bApply=1):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No pip designer window show up")
                raise Exception("No pip designer window show up")
            if self.exist(L.pip_designer.fades.fades):
                if self.exist(L.pip_designer.fades.fades).AXValue == 0:
                    self.exist_click(L.pip_designer.fades.fades)
                value = self.exist(L.pip_designer.fades.enable_fade_out).AXValue
                if value == 1 and bApply == 1:
                    return True
                elif value == 1 and bApply == 0:
                    self.exist_click(L.pip_designer.fades.enable_fade_out)
                    return True
                elif value == 0 and bApply == 1:
                    self.exist_click(L.pip_designer.fades.enable_fade_out)
                    return True
                elif value == 0 and bApply == 0:
                    return True
            else:
                if self.exist(L.pip_designer.flip.flip).AXValue == 0:
                    self.exist_click(L.pip_designer.flip.flip)
                value1 = self.exist(L.pip_designer.fades.enable_fade_out).AXValue
                if value1 == 1 and bApply == 1:
                    return True
                elif value1 == 1 and bApply == 0:
                    self.exist_click(L.pip_designer.fades.enable_fade_out)
                    return True
                elif value1 == 0 and bApply == 1:
                    self.exist_click(L.pip_designer.fades.enable_fade_out)
                    return True
                elif value1 == 0 and bApply == 0:
                    return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_viewer_zoom_dropdown_menu(self, value = 'Fit'):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            self.exist_click(L.pip_designer.viewer_ratio)
            self.exist_click({'AXRole': 'AXStaticText', 'AXValue': value})
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Pip Designer] Click Play/ Stop/ Pause/ Previous Frame/ Next Frame/ Fast Forward')
    def click_preview_operation(self, strOperation):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception("No designer window show up")
            if strOperation == 'Play':
                self.exist_click(L.pip_designer.preview_play)
            elif strOperation == 'Stop':
                self.exist_click(L.pip_designer.preview_stop)
            elif strOperation == 'Pause':
                self.exist_click(L.pip_designer.preview_pause)
            elif strOperation == 'Previous_Frame':
                self.exist_click(L.pip_designer.preview_previous_frame)
            elif strOperation == 'Next_Frame':
                self.exist_click(L.pip_designer.preview_next_frame)
            elif strOperation == 'Fast_Forward':
                self.exist_click(L.pip_designer.preview_fast_forward)
            else:
                logger("Input the wrong augment")
                raise Exception(f"Input the wrong augment {strOperation}, please input (Play/ Stop/ Pause/ Previous_Frame/ Next_Frame/ Fast_Forward)")
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def apply_snap_to_reference_lines(self, bApply):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            self.exist_click(L.pip_designer.toggle_grid_line_on_off)
            if self.exist(L.pip_designer.snap_to_reference_line).AXMenuItemMarkChar == '✓':
                if bApply == 1:
                    return True
                elif bApply == 0:
                    self.exist_click(L.pip_designer.snap_to_reference_line)
            else:
                if bApply == 1:
                    self.exist_click(L.pip_designer.snap_to_reference_line)
                elif bApply == 0:
                    return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def apply_grid_lines_format(self, index='1'):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            if int(index) > 10:
                logger(f'Invalid index value. {index=}')
                raise Exception
            self.exist_click(L.pip_designer.toggle_grid_line_on_off)
            self.exist_click(L.pip_designer.grid_lines)
            if index == '1':
                self.exist_click({'AXIdentifier': 'IDM_PIP_DESIGNER_GRID_LINE_MENU_GRID_LINES_NONE', 'AXTitle': 'None'}) # hardcode_20v3303: _NS:37 > IDM_PIP_DESIGNER_GRID_LINE_MENU_GRID_LINES_NONE
            # elif index == '2':
            #     self.exist_click({'AXIdentifier': 'IDM_PIP_DESIGNER_GRID_LINE_MENU_GRID_LINES_2x2', 'AXTitle': '2 x 2'}) # hardcode_20v3303: _NS:41 > IDM_PIP_DESIGNER_GRID_LINE_MENU_GRID_LINES_2x2
            # elif index == '3':
            #     self.exist_click({'AXIdentifier': '_NS:45', 'AXTitle': '3 x 3'})
            # elif index == '4':
            #     self.exist_click({'AXIdentifier': '_NS:49', 'AXTitle': '4 x 4'})
            # elif index == '5':
            #     self.exist_click({'AXIdentifier': '_NS:53', 'AXTitle': '5 x 5'})
            # elif index == '6':
            #     self.exist_click({'AXIdentifier': '_NS:57', 'AXTitle': '6 x 6'})
            # elif index == '7':
            #     self.exist_click({'AXIdentifier': '_NS:61', 'AXTitle': '7 x 7'})
            # elif index == '8':
            #     self.exist_click({'AXIdentifier': '_NS:65', 'AXTitle': '8 x 8'})
            # elif index == '9':
            #     self.exist_click({'AXIdentifier': '_NS:69', 'AXTitle': '9 x 9'})
            # elif index == '10':
            #     self.exist_click({'AXIdentifier': '_NS:73', 'AXTitle': '10 x 10'})
            else:
                self.exist_click({'AXIdentifier': f'IDM_PIP_DESIGNER_GRID_LINE_MENU_GRID_LINES_{index}x{index}'})
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def switch_timecode_mode(self, mode= 0):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            if mode == 0:
                self.exist_click(L.pip_designer.clip_timecode)
            elif mode == 1:
                self.exist_click(L.pip_designer.video_timecode)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def hide_timeline_mode(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            self.exist_click(L.pip_designer.hide_timeline_mode)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def display_timeline_mode(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            self.exist_click(L.pip_designer.display_timeline_mode)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    #def click_simple_track_specific_keyframe(self, track_index, keyframe_incex):
        #try:
            #if not self.exist(L.pip_designer.designer_window):
                #logger("No designer window show up")
                #raise Exception
            #self.exist_click(L.pip_designer.display_timeline_mode)
        #except Exception as e:
            #logger(f'Exception occurs. log={e}')
            #raise Exception
        #return True

    def add_remove_position_track_current_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            self.exist_click(L.pip_designer.simple_position_track.add_remove_current_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def tap_position_track_previous_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            self.exist_click(L.pip_designer.simple_position_track.previous_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def tap_position_track_next_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            self.exist_click(L.pip_designer.simple_position_track.next_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def add_remove_scale_track_current_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            self.exist_click(L.pip_designer.simple_scale_track.add_remove_current_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Pip Designer] Tap Scale Track Previous Keyframe')
    def tap_scale_track_previous_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception("No designer window show up")
            self.exist_click(L.pip_designer.simple_scale_track.previous_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Pip Designer] Tap Scale Track Next Keyframe')
    def tap_scale_track_next_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception("No designer window show up")
            self.exist_click(L.pip_designer.simple_scale_track.next_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action] Add/Remove Opacity Track Current Keyframe')
    def add_remove_opacity_track_current_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception("No designer window show up")
            self.exist_click(L.pip_designer.simple_opacity_track.add_remove_current_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action] Tap Opacity Track Previous Keyframe')
    def tap_opacity_track_previous_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception("No designer window show up")
            self.exist_click(L.pip_designer.simple_opacity_track.previous_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
    
    @step('[Action] Tap Opacity Track Next Keyframe')
    def tap_opacity_track_next_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception("No designer window show up")
            self.exist_click(L.pip_designer.simple_opacity_track.next_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action] Add/Remove Rotation Track Current Keyframe')
    def add_remove_rotation_track_current_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception("No designer window show up")
            self.exist_click(L.pip_designer.simple_rotation_track.add_remove_current_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def tap_rotation_track_previous_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            self.exist_click(L.pip_designer.simple_rotation_track.previous_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def tap_rotation_track_next_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            self.exist_click(L.pip_designer.simple_rotation_track.next_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def add_remove_freeform_track_current_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            self.exist_click(L.pip_designer.simple_freeform_track.add_remove_current_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def tap_freeform_track_previous_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            self.exist_click(L.pip_designer.simple_freeform_track.previous_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def tap_freeform_track_next_keyframe(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            self.exist_click(L.pip_designer.simple_freeform_track.next_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action] Click OK button on pip designer window')
    def click_ok(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception("No designer window show up")
            self.exist_click(L.pip_designer.ok_button)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
    
    @step('[Action] Input Template Name and Click OK')
    def input_template_name_and_click_ok(self, name):
        try:
            if not self.exist(L.pip_designer.save_as_template_dialog):
                logger("No save_as_template dialog show up")
                raise Exception("No save_as_template dialog show up")
            self.exist_click(L.pip_designer.save_as_textfield)
            self.keyboard.send(name)
            self.exist_click(L.pip_designer.save_as_ok)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
    
    def click_cancel(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
            self.exist_click(L.pip_designer.cancel_button)
            #if option == '1':
             #   self.exist_click(L.pip_designer.cancel_dialog_yes)
            #elif option == '2':
             #   self.exist_click(L.pip_designer.cancel_dialog_no)
            #elif option == '3':
             #   self.exist_click(L.pip_designer.cancel_dialog_cancel)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_cancel_yes(self):
        self.exist_click(L.pip_designer.cancel_dialog_yes)

    def click_cancel_no(self):
        self.exist_click(L.pip_designer.cancel_dialog_no)

    def click_cancel_cancel(self):
        self.exist_click(L.pip_designer.cancel_dialog_cancel)



    def save_as_name(self, name):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            self.exist_click(L.pip_designer.save_as_button)
            self.exist_click(L.pip_designer.save_as_textfield)
            self.keyboard.send(name)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def save_as_set_slider(self, value):
        try:
            if not self.exist(L.pip_designer.save_as_template_dialog):
                logger("No [save as template] dialog pop up")
                raise Exception
            self.exist(L.pip_designer.save_as_slider).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Pip Designer] Share to Cloud')
    def share_to_cloud(self, name, tags, collection, description, verify_dz_link=0, only_dz=0):
        # if verify_dz_link = 1, will check "DZ link" exist or not
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window pop up")
                raise Exception("No designer window pop up")
            self.exist_click(L.pip_designer.share_button)
            self.exist_click(L.pip_designer.save_as_textfield)
            self.keyboard.send(name)
            self.exist_click(L.pip_designer.save_as_ok)
            time.sleep(DELAY_TIME)
            if self.exist(L.pip_designer.auto_sign_in_to_DZ):
                self.exist_click(L.pip_designer.log_in_yes)
                time.sleep(DELAY_TIME*2)
            self.exist_click(L.pip_designer.upload.upload_to_box)
            if only_dz:
                self.exist_click(L.pip_designer.upload.dz)
            else:
                self.exist_click(L.pip_designer.upload.cloud_and_dz)
            time.sleep(DELAY_TIME * 2)
            self.exist_click(L.pip_designer.upload.tags)
            self.keyboard.send(tags)
            self.exist_click(L.pip_designer.upload.collection)
            self.keyboard.send(collection)
            self.exist_click(L.pip_designer.upload.description)
            self.keyboard.send(description)
            self.exist_click(L.pip_designer.upload.next_btn)
            time.sleep(DELAY_TIME)
            if self.exist(L.pip_designer.upload.confirm_disclaimer):
                self.exist_click(L.pip_designer.upload.confirm_disclaimer)
                self.exist_click(L.pip_designer.upload.next_btn)

            time.sleep(DELAY_TIME*3)
            for x in range(100):
                if not self.exist(L.pip_designer.upload.finish):
                    time.sleep(DELAY_TIME)
                elif self.exist(L.pip_designer.upload.finish).AXEnabled == False:
                    time.sleep(DELAY_TIME)
                else:
                    time.sleep(DELAY_TIME)
                    if verify_dz_link:
                        self.click(L.upload_cloud_dz.upload_view_DZ)
                        time.sleep(DELAY_TIME)
                        self.activate()
                        time.sleep(DELAY_TIME*2)
                    break
            self.click(L.pip_designer.upload.finish)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Pip Designer] Switch mode')
    def switch_mode(self, mode):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception("No designer window show up")
            if mode == 'Express':
                self.exist_click(L.pip_designer.express)
            elif mode == 'Advanced':
                self.exist_click(L.pip_designer.advanced)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_share(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            self.exist_click(L.pip_designer.share_button)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Pip Designer] Click [Maximize] button')
    def click_maximize_btn(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception("No designer window show up")
            self.exist_click(L.pip_designer.maximize_btn)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_restore_btn(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            self.exist_click(L.pip_designer.maximize_btn)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_close_btn(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            self.exist_click(L.pip_designer.close_btn)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Pip Designer] Click specific keyframe')
    def click_specific_keyframe(self, index):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception("No designer window show up")
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRoleDescription': 'outline'}, {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem', 'index': index}]) # hardcode_20v3303: _NS:255 > IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Pip Designer] Drag [Properties Scroll Bar]')
    def drag_properties_scroll_bar(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            self.exist(L.pip_designer.object_setting.scroll_bar).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_keyframe_scroll_bar(self, value):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            self.exist(L.pip_designer.keyframe_scrollbar).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Pip Designer] Drag timeline scroll bar to larger')
    def drag_simple_timeline_track_to_lager(self):
        try:
            x, y = self.exist(L.pip_designer.scroller_removed_scroll_view).AXPosition
            new_y = y - 3
            self.mouse.move(x, new_y)
            time.sleep(DELAY_TIME * 0.5)
            self.drag_mouse((x, new_y), (x, new_y-30))
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_zoom_in_btn(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            self.exist_click(L.pip_designer.btn_zoom_in)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_zoom_out_btn(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            self.exist_click(L.pip_designer.btn_zoom_out)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Pip Designer] Apply Flip Horizontally')
    def apply_flip_horizontally(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception("No designer window show up")
            self.click(L.pip_designer.btn_flip)
            time.sleep(DELAY_TIME*0.5)
            self.select_right_click_menu('Flip horizontally')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Pip Designer] Apply Flip Vertically')
    def apply_flip_vertically(self):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception("No designer window show up")
            self.click(L.pip_designer.btn_flip)
            time.sleep(DELAY_TIME*0.5)
            self.select_right_click_menu('Flip vertically')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_timeline_zoom_in_btn(self, times=1):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            x, y = self.exist(L.pip_designer.btn_timeline_zoom_in).AXPosition
            self.mouse.move(x,y)
            self.mouse.click(times=times)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_timeline_zoom_out_btn(self, times=1):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            x, y = self.exist(L.pip_designer.btn_timeline_zoom_out).AXPosition
            self.mouse.move(x,y)
            self.mouse.click(times=times)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def right_click_timeline_keyframe_context_menu(self, row_index, option_index):
        try:
            if not self.exist(L.pip_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            self.exist_click([{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW', 'AXRole': 'AXOutline'}, {'AXRole': 'AXRow', 'index': row_index}]) # hardcode_20v3303: _NS:255 > IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW
            self.right_click()
            if option_index == 1:
                self.exist_click(L.pip_designer.timeline_context_menu.remove_keyframe)
            elif option_index == 2:
                self.exist_click(L.pip_designer.timeline_context_menu.remove_all_keyframe)
            elif option_index == 3:
                self.exist_click(L.pip_designer.timeline_context_menu.duplicate_previous_keyframe)
            elif option_index == 4:
                self.exist_click(L.pip_designer.timeline_context_menu.duplicate_next_keyframe)
            elif option_index == 5:
                self.exist_click(L.pip_designer.timeline_context_menu.ease_in)
            elif option_index == 6:
                self.exist_click(L.pip_designer.timeline_context_menu.ease_out)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    class Express_Mode(Main_Page, BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
        
        @step('[Action][Pip Designer][Express Mode] Get current mode')
        def get_current_mode(self):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No designer window show up")
                    raise Exception("No designer window show up")
                a = 'Advanced Mode'
                b = 'Express Mode'
                if self.exist(L.pip_designer.display_timeline_mode):
                    return a
                elif self.exist(L.pip_designer.hide_timeline_mode):
                    return a
                else:
                    return b
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
        
        @step('[Action][Pip Designer][Express Mode] Fold/ Unfold Object Setting tab')
        def unfold_properties_object_setting_tab(self, unfold=1):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No designer window show up")
                    raise Exception("No designer window show up")
                value = self.exist(L.pip_designer.express_mode.btn_object_setting).AXValue
                if value == 0 and unfold == 0:
                    return True
                elif value == 0 and unfold == 1:
                    self.exist_click(L.pip_designer.express_mode.btn_object_setting)
                elif value == 1 and unfold == 0:
                    self.exist_click(L.pip_designer.express_mode.btn_object_setting)
                elif value == 1 and unfold == 1:
                    return True
                time.sleep(DELAY_TIME)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            
        @step('[Action][Pip Designer] Unfold Properties Chroma Key tab')
        def unfold_properties_chroma_key_tab(self, unfold=1):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No designer window show up")
                    raise Exception("No designer window show up")
                value = self.exist(L.pip_designer.chromakey.chroma_key).AXValue
                if value == 0 and unfold == 0:
                    return True
                elif value == 0 and unfold == 1:
                    self.exist_click(L.pip_designer.chromakey.chroma_key)
                    return True
                elif value == 1 and unfold == 0:
                    self.exist_click(L.pip_designer.chromakey.chroma_key)
                    return True
                elif value == 1 and unfold == 1:
                    return True
                return False
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        @step('[Action][Pip Designer][Express Mode] Fold/ Unfold Properties Border tab')
        def unfold_properties_border_tab(self, unfold=1):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No designer window show up")
                    raise Exception("No designer window show up")
                value = self.exist(L.pip_designer.border.border).AXValue
                if value == 0 and unfold == 0:
                    return True
                elif value == 0 and unfold == 1:
                    self.exist_click(L.pip_designer.border.border)
                elif value == 1 and unfold == 0:
                    self.exist_click(L.pip_designer.border.border)
                elif value == 1 and unfold == 1:
                    return True
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')

        @step('[Action][Pip Designer][Express Mode] Fold/ Unfold Properties Shadow tab')
        def unfold_properties_shadow_tab(self, unfold=1):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No designer window show up")
                    raise Exception("No designer window show up")
                value = self.exist(L.pip_designer.shadow.shadow).AXValue
                if value == 0 and unfold == 0:
                    return True
                elif value == 0 and unfold == 1:
                    self.exist_click(L.pip_designer.shadow.shadow)
                elif value == 1 and unfold == 0:
                    self.exist_click(L.pip_designer.shadow.shadow)
                elif value == 1 and unfold == 1:
                    return True
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')

        @step('[Action][Pip Designer][Express Mode] Fold/ Unfold Properties Fades tab')
        def unfold_properties_fades_tab(self, type, unfold=1):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No designer window show up")
                    raise Exception("No designer window show up")
                if type == 0:
                    value = self.exist(L.pip_designer.fades.fades_express).AXValue
                    if value == 0 and unfold == 0:
                        return True
                    elif value == 0 and unfold == 1:
                        self.exist_click(L.pip_designer.fades.fades_express)
                    elif value == 1 and unfold == 0:
                        self.exist_click(L.pip_designer.fades.fades_express)
                    elif value == 1 and unfold == 1:
                        return True
                    ''''''
                elif type == 1:
                    value_advanced = self.exist(L.pip_designer.fades.fades).AXValue
                    if value_advanced == 0 and unfold == 0:
                        return True
                    elif value_advanced == 0 and unfold == 1:
                        self.exist_click(L.pip_designer.fades.fades)
                    elif value_advanced == 1 and unfold == 0:
                        self.exist_click(L.pip_designer.fades.fades)
                    elif value_advanced == 1 and unfold == 1:
                        return True
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')

        def unfold_properties_flip_tab(self, unfold=1):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No designer window show up")
                    raise Exception
                value = self.exist(L.pip_designer.flip.flip).AXValue
                if value == 0 and unfold == 0:
                    return True
                elif value == 0 and unfold == 1:
                    self.exist_click(L.pip_designer.flip.flip)
                elif value == 1 and unfold == 0:
                    self.exist_click(L.pip_designer.flip.flip)
                elif value == 1 and unfold == 1:
                    return True
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        @step('[Action][Pip Designer][Express Mode] Get Object Setting -- Opacity value')
        def get_object_setting_opacity_value(self):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No designer window show up")
                    raise Exception("No designer window show up")
                value = self.exist(L.pip_designer.object_setting.opacity.opacity_value).AXValue
                return value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')

        @step('[Action][Pip Designer][Express Mode] Adjust Object Setting -- Opacity by slider')
        def drag_object_setting_opacity_slider(self, value):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No designer window show up")
                    raise Exception
                self.exist(L.pip_designer.object_setting.opacity.opacity_slider).AXValue = int(value)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        @step('[Action][Pip Designer][Express Mode] Adjust Object Setting -- Opacity by arrow')
        def click_object_setting_opacity_arrow_btn(self, mode, times=1):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception("No pip designer window show up")
                if mode == 0:
                    x, y = self.exist(L.pip_designer.object_setting.opacity.opacity_value_up).AXPosition
                    self.mouse.move(x,y)
                    self.mouse.click(times=times)
                elif mode == 1:
                    x, y = self.exist(L.pip_designer.object_setting.opacity.opacity_value_down).AXPosition
                    self.mouse.move(x, y)
                    self.mouse.click(times=times)
                else:
                    logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
                    raise Exception("Input the wrong augment, only support (0/1), 0= Up/1= Down")
                time.sleep(DELAY_TIME)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def set_check_chromakey(self, bCheck=1):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                value = self.exist(L.pip_designer.chromakey.chromakey_checkbox).AXValue
                if value == 1 and bCheck == 1:
                    return True
                elif value == 1 and bCheck == 0:
                    self.exist_click(L.pip_designer.chromakey.chromakey_checkbox)
                elif value == 0 and bCheck == 1:
                    self.exist_click(L.pip_designer.chromakey.chromakey_checkbox)
                elif value == 0 and bCheck == 0:
                    return True
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def get_chromakey_checkbox(self):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                value = self.exist(L.pip_designer.chromakey.chromakey_checkbox).AXValue
                if value == 1:
                    check = 'Check'
                    return check
                elif value == 0 :
                    uncheck = 'Uncheck'
                    return uncheck
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def get_chromakey_remove_status(self, index=0):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                value = self.exist({'AXIdentifier': 'IDC_CHROMAKEY_BTN_REMOVE', 'AXRoleDescription': 'button', 'index': index}).AXEnabled
                return value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True


        def click_chromakey_remove_btn(self, index=0):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                self.exist_click({'AXIdentifier': 'IDC_CHROMAKEY_BTN_REMOVE', 'AXRoleDescription': 'button', 'index': index})
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def click_chromakey_add_new_key_btn(self):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                self.exist_click(L.pip_designer.chromakey.add_new_key)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def set_border_checkbox(self, bCheck=1):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                value = self.exist(L.pip_designer.border.border_checkbox).AXValue
                if value == 1 and bCheck == 1:
                    return True
                elif value == 1 and bCheck == 0:
                    self.exist_click(L.pip_designer.border.border_checkbox)
                elif value == 0 and bCheck == 1:
                    self.exist_click(L.pip_designer.border.border_checkbox)
                elif value == 0 and bCheck == 0:
                    return True
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def get_border_checkbox(self):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                value = self.exist(L.pip_designer.border.border_checkbox).AXValue
                if value == 1:
                    check = 'Check'
                    return check
                elif value == 0 :
                    uncheck = 'Uncheck'
                    return uncheck
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def drag_border_size_slider(self, value):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                self.exist(L.pip_designer.border.size_slider).AXValue = int(value)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def input_border_size_value(self, value):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                self.exist_click(L.pip_designer.border.size_value)
                self.mouse.click(times=2)
                self.keyboard.pressed(self.keyboard.key.delete)
                self.keyboard.send(value)
                self.exist_click(L.pip_designer.border.size_title)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        @step('[Action][Pip Designer][Express Mode] Get Border Size value')
        def get_border_size_value(self):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception("No pip designer window show up")
                value = self.exist(L.pip_designer.border.size_value).AXValue
                return value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][Pip Designer][Express Mode] Click Border Size arrow button')
        def click_border_size_arrow_btn(self, mode, times=1):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception("No pip designer window show up")
                if mode == 0:
                    x, y = self.exist(L.pip_designer.border.size_value_up).AXPosition
                    self.mouse.move(x,y)
                    self.mouse.click(times=times)
                elif mode == 1:
                    x, y = self.exist(L.pip_designer.border.size_value_down).AXPosition
                    self.mouse.move(x, y)
                    self.mouse.click(times=times)
                else:
                    logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
                    raise Exception("Input the wrong augment, only support (0/1), 0= Up/1= Down")
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def drag_border_blur_slider(self, value):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                self.exist(L.pip_designer.border.blur_slider).AXValue = int(value)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def input_border_blur_value(self, value):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                self.exist_click(L.pip_designer.border.blur_value_box)
                self.mouse.click(times=2)
                self.keyboard.pressed(self.keyboard.key.delete)
                self.keyboard.send(value)
                self.exist_click(L.pip_designer.border.blur_title)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def click_border_blur_arrow_btn(self, mode, times=1):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                if mode == 0:
                    x, y = self.exist(L.pip_designer.border.blur_value_up).AXPosition
                    self.mouse.move(x,y)
                    self.mouse.click(times=times)
                elif mode == 1:
                    x, y = self.exist(L.pip_designer.border.blur_value_down).AXPosition
                    self.mouse.move(x, y)
                    self.mouse.click(times=times)
                else:
                    logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        @step('[Action][Pip Designer][Express Mode] Get Border Blur value')
        def get_border_blur_value(self):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception("No pip designer window show up")
                value = self.exist(L.pip_designer.border.blur_value).AXValue
                return value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')

        def click_border_opacity_arrow_btn(self, mode, times=1):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                if mode == 0:
                    x, y = self.exist(L.pip_designer.border.opacity_value_up).AXPosition
                    self.mouse.move(x,y)
                    self.mouse.click(times=times)
                elif mode == 1:
                    x, y = self.exist(L.pip_designer.border.opacity_value_down).AXPosition
                    self.mouse.move(x,y)
                    self.mouse.click(times=times)
                else:
                    logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def drag_border_opacity_slider(self, value):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                self.exist(L.pip_designer.border.opacity_slider).AXValue = float(value)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        @step('[Action][Pip Designer][Express Mode] Get Border Opacity value')
        def get_border_opacity_value(self):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception("No pip designer window show up")
                value = self.exist(L.pip_designer.border.opacity_value).AXValue
                return value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')

        def set_border_fill_type(self, option):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                self.exist_click(L.pip_designer.border.fill_type)
                if option == 1:
                    self.exist_click(L.pip_designer.border.fill_type_uniform_color)
                elif option == 2:
                    self.exist_click(L.pip_designer.border.fill_type_2_color_gradient)
                elif option == 4:
                    self.exist_click(L.pip_designer.border.fill_type_4_color_gradient)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def get_border_fill_type(self):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                value = self.exist(L.pip_designer.border.fill_type).AXTitle
                return value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def set_border_uniform_color(self, hexcolor):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                self.exist_click(L.pip_designer.border.fill_type)
                self.exist_click(L.pip_designer.border.fill_type_uniform_color)
                self.exist_click(L.pip_designer.border.uniform_color)
                self.color_picker_switch_category_to_RGB()  # switch to Colors > RGB sliders [20.0.3303]
                self.exist_click(L.pip_designer.express_mode.edittext_hex)
                self.mouse.click(times=3)
                self.keyboard.send(hexcolor)
                self.exist_click(L.pip_designer.border.red)
                self.exist_click(L.pip_designer.border.uniform_color_close_button)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def get_border_uniform_color(self):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                self.exist_click(L.pip_designer.border.fill_type)
                self.exist_click(L.pip_designer.border.fill_type_uniform_color)
                self.exist_click(L.pip_designer.border.uniform_color)
                value = self.exist(L.pip_designer.express_mode.edittext_hex).AXValue
                self.exist_click(L.pip_designer.border.uniform_color_close_button)
                return value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def set_shadow_checkbox(self, bCheck=1):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                value = self.exist(L.pip_designer.shadow.shadow_checkbox).AXValue
                if value == 1 and bCheck == 1:
                    return True
                elif value == 1 and bCheck == 0:
                    self.exist_click(L.pip_designer.shadow.shadow_checkbox)
                elif value == 0 and bCheck == 1:
                    self.exist_click(L.pip_designer.shadow.shadow_checkbox)
                elif value == 0 and bCheck == 0:
                    return True
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def get_shadow_checkbox(self):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                value = self.exist(L.pip_designer.shadow.shadow_checkbox).AXValue
                if value == 1:
                    check = 'Check'
                    return check
                elif value == 0:
                    uncheck = 'Uncheck'
                    return uncheck
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def set_shadow_apply_type(self, option):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                self.exist_click(L.pip_designer.shadow.apply_shadow_to)
                if option == 1:
                    self.exist_click(L.pip_designer.shadow.apply_shadow_to_object_and_border)
                elif option == 2:
                    self.exist_click(L.pip_designer.shadow.apply_shadow_to_object_only)
                elif option == 3:
                    self.exist_click(L.pip_designer.shadow.apply_shadow_to_border_only)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def get_shadow_apply_type(self):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                value = self.exist(L.pip_designer.shadow.apply_shadow_to).AXTitle
                return value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def input_shadow_distance_value(self, value):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                self.exist_click(L.pip_designer.shadow.distance_value_box)
                self.mouse.click(times=2)
                self.keyboard.pressed(self.keyboard.key.delete)
                self.keyboard.send(value)
                self.exist_click(L.pip_designer.shadow.distance_title)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def get_shadow_distance_value(self):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                value = self.exist(L.pip_designer.shadow.distance_value).AXValue
                return value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def drag_shadow_distance_slider(self, value):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                self.exist(L.pip_designer.shadow.distance_slider).AXValue = float(value)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def click_shadow_distance_arrow_btn(self, mode, times=1):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                if mode == 0:
                    x, y = self.exist(L.pip_designer.shadow.distance_value_up).AXPosition
                    self.mouse.move(x,y)
                    self.mouse.click(times=times)
                elif mode == 1:
                    x, y = self.exist(L.pip_designer.shadow.distance_value_down).AXPosition
                    self.mouse.move(x, y)
                    self.mouse.click(times=times)
                else:
                    logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def input_shadow_blur_value(self, value):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                self.exist_click(L.pip_designer.shadow.blur_value_box)
                self.mouse.click(times=2)
                self.keyboard.pressed(self.keyboard.key.delete)
                self.keyboard.send(value)
                self.exist_click(L.pip_designer.shadow.blur_title)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def get_shadow_blur_value(self):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                value = self.exist(L.pip_designer.shadow.blur_value).AXValue
                return value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def drag_shadow_blur_slider(self, value):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                self.exist(L.pip_designer.shadow.blur_slider).AXValue = int(value)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def click_shadow_blur_arrow_btn(self, mode, times=1):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                if mode == 0:
                    x, y = self.exist(L.pip_designer.shadow.blur_value_up).AXPosition
                    self.mouse.move(x,y)
                    self.mouse.click(times=times)
                elif mode == 1:
                    x, y = self.exist(L.pip_designer.shadow.blur_value_down).AXPosition
                    self.mouse.move(x, y)
                    self.mouse.click(times=times)
                else:
                    logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def get_shadow_opacity_value(self):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                value = self.exist(L.pip_designer.shadow.opacity_value).AXValue
                return value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def drag_shadow_opacity_slider(self, value):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                self.exist(L.pip_designer.shadow.opacity_slider).AXValue = int(value)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def click_shadow_opacity_arrow_btn(self, mode, times=1):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                if mode == 0:
                    x, y = self.exist(L.pip_designer.shadow.opacity_value_up).AXPosition
                    self.mouse.move(x,y)
                    self.mouse.click(times=times)
                elif mode == 1:
                    x, y = self.exist(L.pip_designer.shadow.opacity_value_down).AXPosition
                    self.mouse.move(x, y)
                    self.mouse.click(times=times)
                else:
                    logger("Input the wrong augment, only support (0/1), 0= Up/1= Down")
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def set_shadow_select_color(self, hexcolor):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                self.exist_click(L.pip_designer.shadow.select_color)
                self.exist_click(L.pip_designer.express_mode.edittext_hex)
                self.mouse.click(times=3)
                self.keyboard.send(hexcolor)
                self.exist_click(L.pip_designer.shadow.red)
                self.exist_click(L.pip_designer.shadow.select_color_close)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def get_shadow_select_color(self):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                self.exist_click(L.pip_designer.shadow.select_color)
                value = self.exist(L.pip_designer.express_mode.edittext_hex).AXValue
                self.exist_click(L.pip_designer.shadow.select_color_close)
                return value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def set_fades_checkbox(self, bCheck=1):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                value = self.exist(L.pip_designer.fades.fades_express_checkbox).AXValue
                if value == 1 and bCheck == 1:
                    return True
                elif value == 1 and bCheck == 0:
                    self.exist_click(L.pip_designer.fades.fades_express_checkbox)
                elif value == 0 and bCheck == 1:
                    self.exist_click(L.pip_designer.fades.fades_express_checkbox)
                elif value == 0 and bCheck == 0:
                    return True
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def get_fades_checkbox(self):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                value = self.exist(L.pip_designer.fades.fades_express_checkbox).AXValue
                if value == 1:
                    check = 'Check'
                    return check
                elif value == 0:
                    uncheck = 'Uncheck'
                    return uncheck
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def set_enable_fade_in_checkbox(self, bCheck=1):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                value = self.exist(L.pip_designer.fades.enable_fade_in).AXValue
                if value == 1 and bCheck == 1:
                    return True
                elif value == 1 and bCheck == 0:
                    self.exist_click(L.pip_designer.fades.enable_fade_in)
                elif value == 0 and bCheck == 1:
                    self.exist_click(L.pip_designer.fades.enable_fade_in)
                elif value == 0 and bCheck == 0:
                    return True
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def get_enable_fade_in_checkbox(self):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                value = self.exist(L.pip_designer.fades.enable_fade_in).AXValue
                if value == 1:
                    check = 'Check'
                    return check
                elif value == 0:
                    uncheck = 'Uncheck'
                    return uncheck
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def set_enable_fade_out_checkbox(self, bCheck=1):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                value = self.exist(L.pip_designer.fades.enable_fade_out).AXValue
                if value == 1 and bCheck == 1:
                    return True
                elif value == 1 and bCheck == 0:
                    self.exist_click(L.pip_designer.fades.enable_fade_out)
                elif value == 0 and bCheck == 1:
                    self.exist_click(L.pip_designer.fades.enable_fade_out)
                elif value == 0 and bCheck == 0:
                    return True
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def get_enable_fade_out_checkbox(self):
            try:
                if not self.exist(L.pip_designer.designer_window):
                    logger("No pip designer window show up")
                    raise Exception
                value = self.exist(L.pip_designer.fades.enable_fade_out).AXValue
                if value == 1:
                    check = 'Check'
                    return check
                elif value == 0:
                    uncheck = 'Uncheck'
                    return uncheck
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

    class Advanced(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        @step('[Action][Pip Designer][Advanced Mode] Switch to Motion tab')
        def switch_to_motion(self):
            try:
                if not self.exist(L.pip_designer.tab_motion):
                    raise Exception("No motion tab show up")
                self.click(L.pip_designer.tab_motion)
                time.sleep(DELAY_TIME)
                # Verify step
                if self.is_not_exist(L.pip_designer.path.path_title):
                    logger('Verify fail - cannot enter motion tab')
                    raise Exception('Verify fail - cannot enter motion tab')
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][Pip Designer][Advanced Mode] Switch to [Properties] tab')
        def switch_to_properties(self):
            try:
                if not self.exist(L.pip_designer.tab_properties):
                    raise Exception("No properties tab show up")
                self.click(L.pip_designer.tab_properties)

                time.sleep(DELAY_TIME)

                # Verify step
                if self.is_exist(L.pip_designer.path.path_title):
                    logger('Verify fail - stay in motion tab')
                    raise Exception('Verify fail - stay in motion tab')
                elif self.is_exist(L.pip_designer.in_animation.animation_title):
                    logger('Verify fail - stay in Animation tab')
                    raise Exception('Verify fail - stay in Animation tab')
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')

        @step('[Action][Pip Designer][Advanced Mode] Switch to [Animation] tab')
        def switch_to_animation(self):
            try:
                if not self.exist(L.pip_designer.tab_animation):
                    raise Exception("No animation tab show up")
                self.click(L.pip_designer.tab_animation)

                time.sleep(DELAY_TIME*3)

                # Verify step
                if self.is_not_exist(L.pip_designer.in_animation.animation_title):
                    logger('Verify fail - cannot enter in Animation tab')
                    raise Exception('Verify fail - cannot enter in Animation tab')
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][Pip Designer][Advanced Mode] Fold/ Unfold [in animation] menu')
        def unfold_in_animation_menu(self, set_unfold=1):
            try:
                current_value = self.exist(L.pip_designer.in_animation.btn_in_animation).AXValue
                if current_value != set_unfold:
                    self.exist_click(L.pip_designer.in_animation.btn_in_animation)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def unfold_out_animation_menu(self, set_unfold=1):
            try:
                current_value = self.exist(L.pip_designer.out_animation.btn_out_animation).AXValue
                if current_value != set_unfold:
                    self.exist_click(L.pip_designer.out_animation.btn_out_animation)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        @step('[Action][Pip Designer][Advanced Mode] Fold/ Unfold [Loop Animation] menu')
        def unfold_loop_animation_menu(self, set_unfold=1):
            try:
                current_value = self.exist(L.pip_designer.loop_animation.btn_loop_animation).AXValue
                if current_value != set_unfold:
                    self.exist_click(L.pip_designer.loop_animation.btn_loop_animation)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        @step('[Action][Pip Designer][Advanced Mode] Fold/ Unfold [Path] menu')
        def unfold_path_menu(self, set_unfold=1):
            try:
                current_value = self.exist(L.pip_designer.path.btn_path).AXValue
                if current_value != set_unfold:
                    self.exist_click(L.pip_designer.path.btn_path)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def get_path_unfold_status(self):
            try:
                if not self.exist(L.pip_designer.path.btn_path):
                    raise Exception
                current_value = self.exist(L.pip_designer.path.btn_path).AXValue

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return current_value

        @step('[Action][Pip Designer][Advanced Mode] Fold/ Unfold motion blur menu')
        def unfold_motion_blur_menu(self, set_unfold=1):
            try:
                current_value = self.exist(L.pip_designer.motion_blur.btn_motion_blur).AXValue
                if current_value != set_unfold:
                    self.exist_click(L.pip_designer.motion_blur.btn_motion_blur)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def get_motion_blur_unfold_status(self):
            try:
                if not self.exist(L.pip_designer.motion_blur.btn_motion_blur):
                    raise Exception
                current_value = self.exist(L.pip_designer.motion_blur.btn_motion_blur).AXValue

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return current_value

    class In_Animation(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def get_current_effect(self):
            try:
                if not self.exist(L.pip_designer.in_animation.cbx_effect_menu):
                    raise Exception
                current_value = self.exist(L.pip_designer.in_animation.cbx_effect_menu).AXTitle
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return current_value

        def select_effect(self, option):
            # option = All Content, General, Shape, Block, ...
            try:
                if not self.exist_click(L.pip_designer.in_animation.cbx_effect_menu):
                    raise Exception
                time.sleep(DELAY_TIME)
                target_menu = {'AXRole': 'AXStaticText', 'AXValue': f'{option}'}
                self.click(target_menu)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        @step('[Action][Pip Designer][In Animation] Select template')
        def select_template(self, index=1):
            try:
                if index < 1:
                    logger('Invalid parameter')
                    raise Exception('Invalid parameter')

                # select template with index
                elem_item = self.exist(L.pip_designer.in_animation.animation_template)
                current_index = index - 1
                if not self.exist(elem_item[current_index]):
                    raise Exception(f'Cannot find the template with {index}')
                self.el_click(elem_item[current_index])
                #logger(elem_item)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

    class Out_Animation(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    class Path(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def get_current_category(self):
            try:
                if not self.exist(L.pip_designer.path.cbx_path_menu):
                    raise Exception
                current_value = self.exist(L.pip_designer.path.cbx_path_menu).AXTitle
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return current_value

        def select_category(self, option):
            try:
                if not self.exist_click(L.pip_designer.path.cbx_path_menu):
                    raise Exception
                if option == 'all':
                    seleted_option = L.pip_designer.path.option_all
                elif option == 'default':
                    seleted_option = L.pip_designer.path.option_default
                elif option == 'custom':
                    seleted_option = L.pip_designer.path.option_custom
                else:
                    logger('Invalid parameter, please check again')
                    return False

                self.click(seleted_option)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        @step('[Action][Pip Designer][Path] Select certain template')
        def select_template(self, index=1):
            try:
                if index < 1:
                    logger('Invalid parameter')
                    raise Exception('Invalid parameter')

                # select template with index
                elem_item = self.exist(L.pip_designer.path.path_template)
                current_index = index - 1
                if not self.exist(elem_item[current_index]):
                    raise Exception(f'Cannot find the template with {index}')
                self.el_click(elem_item[current_index])
                #logger(elem_item)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def click_save_custom_btn(self):
            try:
                if not self.is_exist(L.pip_designer.path.btn_custom_path):
                    raise Exception
                self.click(L.pip_designer.path.btn_custom_path)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def remove_custom_template(self, index):
            # Step 0: enter Custom Paths category
            try:
                # Step 1: Select certain template
                self.select_template(index)
                time.sleep(DELAY_TIME)

                # Step 2: Right Click > Select "Remove path" on right click menu
                self.right_click()
                self.select_right_click_menu('Remove Path')

                # Step 3: pop up warning dialog
                if self.exist(L.pip_designer.remove_dialog):
                    self.click(L.pip_designer.remove_dialog_ok)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

    class Motion_Blur(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.length = self.Length(*args, **kwargs)
            self.density = self.Density(*args, **kwargs)

        def get_checkbox_status(self):
            check_status = self.exist(L.pip_designer.motion_blur.checkbox).AXValue
            return check_status
        
        @step('[Action][Pip Designer][Motion Blur] Tick/ Untick checkbox')
        def set_checkbox(self, tick=1):
            try:
                current_value = self.get_checkbox_status()
                if current_value != tick:
                    self.exist_click(L.pip_designer.motion_blur.checkbox)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        class Length(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            def get_value(self):
                current_value = self.exist(L.pip_designer.motion_blur.text_field_length)
                return current_value.AXValue

            @step('[Action][Pip Designer][Motion Blur][Length] Set value')
            def set_value(self, value):
                try:
                    if (value > 2) | (value < 0):
                        logger('Invalid parameter')
                        raise Exception('Invalid parameter')

                    if not self.is_exist(L.pip_designer.motion_blur.text_field_length):
                        raise Exception
                    self.click(L.pip_designer.motion_blur.text_field_length)
                    self.mouse.click(times=2)

                    self.exist(L.pip_designer.motion_blur.text_field_length).AXValue = str(value)
                    self.press_enter_key()
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception(f'Exception occurs. log={e}')
                return True

            def adjust_slider(self, value):
                try:
                    if (value > 2) | (value < 0):
                        logger('Invalid parameter')
                        return False

                    self.exist(L.pip_designer.motion_blur.indicator_length).AXValue = value
                    time.sleep(DELAY_TIME)
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def click_arrow(self, option, times=1):
                try:
                    if (option > 1) | (option < 0):
                        logger('Invalid parameter')
                        return False
                    for x in range(times):
                        if option == 0:
                            self.exist_click(L.pip_designer.motion_blur.arrow_up_btn_length)
                        elif option == 1:
                            self.exist_click(L.pip_designer.motion_blur.arrow_down_btn_length)

                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

        class Density(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            def get_value(self):
                current_value = self.exist(L.pip_designer.motion_blur.text_field_density)
                return current_value.AXValue

            def set_value(self, value):
                try:
                    if (value > 32) | (value < 2):
                        logger('Invalid parameter')
                        return False

                    if not self.is_exist(L.pip_designer.motion_blur.text_field_density):
                        raise Exception
                    self.click(L.pip_designer.motion_blur.text_field_density)
                    self.mouse.click(times=2)

                    self.exist(L.pip_designer.motion_blur.text_field_density).AXValue = str(value)
                    self.press_enter_key()
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True
            
            @step('[Action][Pip Designer][Motion Blur][Density] Adjust slider')
            def adjust_slider(self, value):
                try:
                    if (value > 32) | (value < 2):
                        logger('Invalid parameter')
                        raise Exception('Invalid parameter')

                    self.exist(L.pip_designer.motion_blur.indicator_density).AXValue = value
                    time.sleep(DELAY_TIME)
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception(f'Exception occurs. log={e}')
                return True

            def click_arrow(self, option, times=1):
                try:
                    if (option > 1) | (option < 0):
                        logger('Invalid parameter')
                        return False
                    for x in range(times):
                        if option == 0:
                            self.exist_click(L.pip_designer.motion_blur.arrow_up_btn_density)
                        elif option == 1:
                            self.exist_click(L.pip_designer.motion_blur.arrow_down_btn_density)

                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

    class Simple_Timeline(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.right_click_menu = self.Right_Click_Menu(*args, **kwargs)

        def click_image_track(self):
            try:
                object_track = self.exist(L.pip_designer.image_track)
                if not object_track:
                    logger("Cannot find the image track")
                    raise Exception
                else:
                    self.el_click(object_track)
                    time.sleep(DELAY_TIME*0.5)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        def set_image_seq_ends(self, option):
            '''
            parameter: loop, last, first, stop
            > loop (Loop Playback), last (Freeze on Last Frame), first (Freeze on First Frame), stop (Stop Playback)
            '''
            try:
                if option == 'loop':
                    custom_menu = 'Loop Playback'
                elif option == 'last':
                    custom_menu = 'Freeze on Last Frame'
                elif option == 'first':
                    custom_menu = 'Freeze on First Frame'
                elif option == 'stop':
                    custom_menu = 'Stop Playback'
                else:
                    logger('Invalid parameter')
                    return False
                self.click_image_track()
                self.right_click()
                self.select_right_click_menu('After Image Sequence Ends', f'{custom_menu}')

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def get_image_seq_ends(self):
            try:
                self.click_image_track()
                self.right_click()
                self.select_right_click_menu('After Image Sequence Ends')
                pos = self.mouse.position()

                if self.exist(L.pip_designer.option_loop).AXMenuItemMarkChar == '✓':
                    self.mouse.move(pos[0], pos[1] - 20)
                    self.mouse.click()
                    return 'Loop Playback'
                elif self.exist(L.pip_designer.option_last).AXMenuItemMarkChar == '✓':
                    self.mouse.move(pos[0], pos[1] - 20)
                    self.mouse.click()
                    return 'Freeze on Last Frame'
                elif self.exist(L.pip_designer.option_first).AXMenuItemMarkChar == '✓':
                    self.mouse.move(pos[0], pos[1] - 20)
                    self.mouse.click()
                    return 'Freeze on First Frame'
                elif self.exist(L.pip_designer.option_stop).AXMenuItemMarkChar == '✓':
                    self.mouse.move(pos[0], pos[1] - 20)
                    self.mouse.click()
                    return 'Stop Playback'
                else:
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        class Right_Click_Menu(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            def get_linear_status(self):
                try:
                    time.sleep(DELAY_TIME)
                    self.right_click()
                    time.sleep(DELAY_TIME)
                    current_result = self.exist(L.pip_designer.option_linear).AXMenuItemMarkChar
                    #logger(current_result)
                    self.right_click()
                    if current_result == '✓':
                        return 1
                    elif current_result == None:
                        return 0
                    else:
                        raise Exception
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception

            def set_linear_hold(self, option):
                try:
                    if option == 'linear':
                        check_menu = L.pip_designer.option_linear
                    elif option == 'hold':
                        check_menu = L.pip_designer.option_hold
                    else:
                        logger('Invalid parameter')
                        return False

                    self.right_click()
                    time.sleep(DELAY_TIME)
                    current_result = self.exist(check_menu).AXMenuItemMarkChar
                    #logger(current_result)

                    if current_result == '✓':
                        self.right_click()
                        return True
                    elif current_result == None:
                        self.click(check_menu)
                        return True
                    else:
                        raise Exception
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception

            def get_hold_status(self):
                try:
                    time.sleep(DELAY_TIME)
                    self.right_click()
                    time.sleep(DELAY_TIME)
                    current_result = self.exist(L.pip_designer.option_hold).AXMenuItemMarkChar
                    #logger(current_result)
                    self.right_click()
                    if current_result == '✓':
                        return 1
                    elif current_result == None:
                        return 0
                    else:
                        raise Exception
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception

            @step('[Action][Pip Designer][Simple Timeline] Get Ease In Status')
            def get_ease_in_status(self):
                try:
                    time.sleep(DELAY_TIME)
                    self.right_click()
                    time.sleep(DELAY_TIME)
                    current_enable = self.exist(L.pip_designer.option_ease_in).AXEnabled
                    current_result = self.exist(L.pip_designer.option_ease_in).AXMenuItemMarkChar
                    #logger(current_result)

                    # Close current (Right click menu)
                    # Get current pos
                    pos = self.mouse.position()
                    self.mouse.move(pos[0] - 20, pos[1] - 10)
                    time.sleep(2)
                    self.left_click()

                    if current_enable == False:
                        return None
                    elif current_result == '✓':
                        return 1
                    elif current_result == None:
                        return 0
                    else:
                        raise Exception('Unable to get the status of Ease In')
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception(f'Exception occurs. log={e}')

            @step('[Action][Pip Designer][Simple Timeline] Get Ease Out Status')
            def get_ease_out_status(self):
                try:
                    time.sleep(DELAY_TIME)
                    self.right_click()
                    time.sleep(DELAY_TIME)
                    current_enable = self.exist(L.pip_designer.option_ease_out).AXEnabled
                    current_result = self.exist(L.pip_designer.option_ease_out).AXMenuItemMarkChar
                    #logger(current_result)

                    # Close current (Right click menu)
                    # Get current pos
                    pos = self.mouse.position()
                    self.mouse.move(pos[0] - 20, pos[1] - 10)
                    time.sleep(2)
                    self.left_click()

                    if current_enable == False:
                        return None
                    elif current_result == '✓':
                        return 1
                    elif current_result == None:
                        return 0
                    else:
                        raise Exception('Unable to get the status of Ease Out')
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception(f'Exception occurs. log={e}')