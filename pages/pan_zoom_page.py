import time, datetime, os, copy

from ATFramework.utils import logger
try:
    from PIL import Image
except Exception as e:
    logger(f"[Warning] {e}")
from pynput.mouse import Button as mouse_button, Controller as Mouse_controller

from .base_page import BasePage

from ATFramework.utils.Image_Search import CompareImage
from .locator import locator as L

OPERATION_DELAY = 1 # sec

class Pan_Zoom(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.magic_motion_designer = Magic_Motion_Designer(*args, **kwargs)

    def is_enter_pan_zoom(self):
        return self.is_exist(L.pan_zoom.title_pan_zoom)

    def click_close(self):
        try:
            self.click(L.pan_zoom.btn_close)
            time.sleep(OPERATION_DELAY)
            if not self.is_not_exist(L.pan_zoom.title_pan_zoom, None, 3):
                logger('Fail to close Pan Zoom window')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. error={e}')
            raise Exception
        return True

    def click_i_button(self):
        try:
            self.click(L.pan_zoom.btn_i)
            time.sleep(OPERATION_DELAY)
            if not self.is_exist(L.pan_zoom.what_is_pan_zoom.title_what_is):
                logger('Fail to click i button')
                raise Exception
            time.sleep(OPERATION_DELAY * 0.5)
            self.click(L.pan_zoom.what_is_pan_zoom.btn_close)
            time.sleep(OPERATION_DELAY * 0.5)
            if not self.is_not_exist(L.pan_zoom.what_is_pan_zoom.title_what_is, None, 3):
                logger('Fail to close what is Pan Zoom window')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. error={e}')
            raise Exception
        return True

    def click_reset(self):
        return self.click(L.pan_zoom.btn_reset)

    def click_motion_designer(self):
        return self.click(L.pan_zoom.btn_motion_designer)

    def click_apply_to_all(self):
        return self.click(L.pan_zoom.btn_apply_to_all)

    def is_enabled_motion_designer_btn(self):
        return self.exist(L.pan_zoom.btn_motion_designer).AXEnabled

    def snapshot_style(self, index): # index: 1-based
        image_file = ''
        try:
            els_image = self.exist(L.pan_zoom.unit_motion_style_image)
            image_file = self.snapshot(els_image[index-1])
        except Exception as e:
            logger(f'Exception occurs. error={e}')
            raise Exception
        return image_file

    def apply_motion_style(self, index):
        try:
            els_image = self.exist(L.pan_zoom.unit_motion_style_image)
            self.el_click(els_image[index-1])
            time.sleep(OPERATION_DELAY * 0.5)
        except Exception as e:
            logger(f'Exception occurs. error={e}')
            raise Exception
        return True

    def apply_user_defined_style(self):
        try:
            el_user_defined_text = self.exist(L.pan_zoom.txt_motion_style_name_user_defined)
            self.el_click(el_user_defined_text.AXParent)
            time.sleep(OPERATION_DELAY)
            if not self.is_exist(L.pan_zoom.magic_motion_designer.main_window):
                logger('Fail to apply user defined style')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. error={e}')
            raise Exception
        return True

    def get_applied_style_name(self):
        try:
            index_target = -1
            style_name_selected = ''
            result_A = {'rgb': '', 'count': 0, 'index': -1} # unit_dict: {'rgb': (x,y,z), 'count': 0}
            result_B = {'rgb': '', 'count': 0, 'index': -1}
            els_image = self.exist(L.pan_zoom.unit_motion_style_image)
            filename = self.screenshot()
            img = Image.open(filename)
            img_rgb = img.convert('RGB')

            for index in range(len(els_image)):
                el_pos = els_image[index].AXPosition
                rgb_pixel_value = img_rgb.getpixel((el_pos[0]-1,el_pos[1]-1))
                is_done = False
                if result_A['rgb']:
                    if rgb_pixel_value == result_A['rgb']:
                        result_A['count'] += 1
                        result_A['index'] = index
                        is_done = True
                else:
                    result_A['rgb'] = rgb_pixel_value
                    result_A['count'] += 1
                    result_A['index'] = index
                    is_done = True

                if is_done:
                    continue

                if result_B['rgb']:
                    if rgb_pixel_value == result_B['rgb']:
                        result_B['count'] += 1
                        result_B['index'] = index
                else:
                    result_B['rgb'] = rgb_pixel_value
                    result_B['count'] += 1
                    result_B['index'] = index

            if result_A['count'] == 1:
                index_target = result_A['index']
            elif result_B['count'] == 1:
                index_target = result_B['index']

            if index_target == -1:
                logger('Fail to find the selected sytle')
                return None

            els_style_name = self.exist(L.pan_zoom.unit_motion_style_name)
            style_name_selected = els_style_name[index_target].AXValue
        except Exception as e:
            logger(f'Exception occurs. error={e}')
            return False
        return style_name_selected


class Magic_Motion_Designer(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyframe = Keyframe(*args, **kwargs)
        self.preview_operation = Preview_Operation(*args, **kwargs)
        self.position_x = Stepper_Operation(L.pan_zoom.magic_motion_designer.position_x_stepper_group, 'x', *args, **kwargs)
        self.position_y = Stepper_Operation(L.pan_zoom.magic_motion_designer.position_y_stepper_group, 'y', *args, **kwargs)
        self.scale_width = Stepper_Operation(L.pan_zoom.magic_motion_designer.scale_width_stepper_group, 'width', *args, **kwargs)
        self.scale_height = Stepper_Operation(L.pan_zoom.magic_motion_designer.scale_height_stepper_group, 'height', *args, **kwargs)
        self.rotation = Stepper_Operation(L.pan_zoom.magic_motion_designer.rotation_stepper_group, 'rotation', *args, **kwargs)

    def is_enter(self):
        return self.is_exist(L.pan_zoom.magic_motion_designer.main_window)

    def get_caption_name(self):
        caption_name = ''
        try:
            locator = L.pan_zoom.magic_motion_designer.unit_text.copy()
            locator[1]['get_all'] = True
            els_text = self.exist(locator)
            pos_main_window = self.exist(L.pan_zoom.magic_motion_designer.main_window).AXPosition
            for el_text in els_text:
                if int(el_text.AXPosition[1]) - int(pos_main_window[1]) < 5:
                    caption_name = el_text.AXValue
                    break
        except Exception as e:
            logger(f'Exception occurs. error={e}')
            return False
        return caption_name

    def click_maximize(self):
        return self.click(L.pan_zoom.magic_motion_designer.btn_maximize)

    def click_close(self):
        return self.click(L.pan_zoom.magic_motion_designer.btn_close)

    def apply_snap_ref_line(self, is_apply=1):
        try:
            if not self.exist(L.pan_zoom.magic_motion_designer.main_window):
                logger("No magic motion designer window show up")
                raise Exception
            self.exist_click(L.pan_zoom.magic_motion_designer.grid_line.btn_toggle_grid_line,
                             L.pan_zoom.magic_motion_designer.main_window)
            value = self.exist(L.pan_zoom.magic_motion_designer.grid_line.option_snap_reference_lines).AXMenuItemMarkChar
            x, y = self.exist(L.pan_zoom.magic_motion_designer.grid_line.option_snap_reference_lines).AXPosition
            if value and is_apply:
                self.mouse.move(int(x-15), y)
                self.mouse.click(times=1)
                return True
            elif value and not is_apply:
                self.exist_click(L.pan_zoom.magic_motion_designer.grid_line.option_snap_reference_lines)
            elif not value and is_apply:
                self.exist_click(L.pan_zoom.magic_motion_designer.grid_line.option_snap_reference_lines)
            elif not value and not is_apply:
                self.mouse.move(int(x - 15), y)
                self.mouse.click(times=1)
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_grid_lines_format(self, index):
        try:
            if not self.exist(L.pan_zoom.magic_motion_designer.main_window):
                logger("No magic motion designer window show up")
                raise Exception
            self.exist_click(L.pan_zoom.magic_motion_designer.grid_line.btn_toggle_grid_line)
            self.exist_click(L.pan_zoom.magic_motion_designer.grid_line.option_grid_lines)
            if index == 1:
                el_option_3 = self.exist(L.pan_zoom.magic_motion_designer.grid_line.option_3x3)
                self.mouse.move(el_option_3.AXPosition[0]+int(el_option_3.AXSize[0]/2), el_option_3.AXPosition[1])
                self.exist_click(L.pan_zoom.magic_motion_designer.grid_line.option_none)
            else:
                if index == 2:
                    el_option_3 = self.exist(L.pan_zoom.magic_motion_designer.grid_line.option_3x3)
                    self.mouse.move(el_option_3.AXPosition[0]+int(el_option_3.AXSize[0]/2), el_option_3.AXPosition[1])
                self.exist_click(eval(f'L.pan_zoom.magic_motion_designer.grid_line.option_{index}x{index}'))
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def get_viewer_setting(self):
        return self.exist(L.pan_zoom.magic_motion_designer.btn_viewer_setting).AXTitle

    def set_aspect_ratio(self, option, btn_confirm=''): # btn_confirm: 'ok' or 'cancel' or keep empty string form skip
        try:
            self.click(L.pan_zoom.magic_motion_designer.btn_aspect_ratio)
            time.sleep(OPERATION_DELAY * 0.5)
            locator_menu_item = L.pan_zoom.magic_motion_designer.unit_menu_item_aspect_ratio.copy()
            locator_menu_item[1]['AXValue'] = option
            self.click(locator_menu_item)
            time.sleep(OPERATION_DELAY)
            if btn_confirm:
                self.exist_click(eval(f'L.base.confirm_dialog.btn_{btn_confirm}'))
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def set_aspect_ratio_4_3(self, btn_confirm=''):
        return self.set_aspect_ratio('4:3', btn_confirm)

    def set_aspect_ratio_16_9(self, btn_confirm=''):
        return self.set_aspect_ratio('16:9', btn_confirm)

    def set_aspect_ratio_9_16(self, btn_confirm=''):
        return self.set_aspect_ratio('9:16', btn_confirm)

    def set_aspect_ratio_1_1(self, btn_confirm=''):
        return self.set_aspect_ratio('1:1', btn_confirm)

    def set_aspect_ratio_freeform(self, btn_confirm=''):
        return self.set_aspect_ratio('Freeform', btn_confirm)

    def get_current_aspect_ratio(self):
        return self.exist(L.pan_zoom.magic_motion_designer.btn_aspect_ratio).AXTitle

    def set_maintain_aspect_ratio(self, is_check=1):
        try:
            el_chx = self.exist(L.pan_zoom.magic_motion_designer.chx_maintain_aspect_ratio)
            if is_check != el_chx.AXValue:
                self.el_click(el_chx)
                time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_undo(self):
        return self.click(L.pan_zoom.magic_motion_designer.btn_undo)

    def click_redo(self):
        return self.click(L.pan_zoom.magic_motion_designer.btn_redo)

    def click_ok(self):
        return self.click(L.pan_zoom.magic_motion_designer.btn_ok)

    def click_cancel(self):
        return self.click(L.pan_zoom.magic_motion_designer.btn_cancel)

    def click_reset(self):
        return self.click(L.pan_zoom.magic_motion_designer.btn_reset)

    def set_timecode(self, timecode):
        return self._set_timecode(timecode, L.pan_zoom.magic_motion_designer.timecode)

    def get_timecode(self):
        return self.exist(L.pan_zoom.magic_motion_designer.timecode).AXValue

    def move_preview_object(self, y_offset):
        try:
            pos_object = self.exist(L.pan_zoom.magic_motion_designer.preview_selected_object).AXPosition
            size_object = self.exist(L.pan_zoom.magic_motion_designer.preview_selected_object).AXSize
            pos_center_object = (pos_object[0]+int(size_object[0]/2), pos_object[1]+int(size_object[1]/2))
            y_value = self.position_y.get_value()
            logger(f'{y_value=}')
            self.drag_mouse(pos_center_object, (pos_center_object[0], pos_center_object[1]+y_offset))
            time.sleep(OPERATION_DELAY)
            y_value_after = self.position_y.get_value()
            logger(f'{y_value_after=}')
            if y_value == y_value_after:
                logger(f'Fail to verify after moved preview object. {y_value=}, {y_value_after=}')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_viewer_zoom(self, value='Fit'):
        try:
            self.click(L.pan_zoom.magic_motion_designer.btn_viewer_setting)
            locator_menu_item = L.pan_zoom.magic_motion_designer.unit_viewer_zoom_menu_item.copy()
            locator_menu_item[2]['get_all'] = True
            els_menu_item = self.exist(locator_menu_item)
            is_done = 0
            for menu_item in els_menu_item:
                item_value = self.exist({'AXRole': 'AXStaticText'}, menu_item).AXValue
                if value == item_value:
                    time.sleep(OPERATION_DELAY * 0.5)
                    self.el_click(menu_item)
                    is_done = 1
                    break
            if not is_done:
                logger('Fail to match menu item')
                raise Exception
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            return False
        return True

    def drag_preview_object_rotate_clockwise(self, radius=190): # only the rotate dot is on the top
        try:
            el_object = self.exist(L.pan_zoom.magic_motion_designer.preview_selected_object)
            el_object.activate()
            pos_canvas = el_object.AXPosition
            size_canvas = el_object.AXSize
            time.sleep(OPERATION_DELAY * 0.5)
            center_x = pos_canvas[0] + int(size_canvas[0]/2)
            center_y = pos_canvas[1] + int(size_canvas[1]/2)
            rotation_value = self.rotation.get_value()
            logger(f'{center_x=}, {center_y=}, {rotation_value=}')
            self.drag_mouse((center_x, center_y-radius), (center_x+radius, center_y))
            time.sleep(OPERATION_DELAY * 0.5)
            rotation_value_after = self.rotation.get_value()
            logger(f'{rotation_value_after=}')
            if rotation_value == rotation_value_after:
                logger('Fail to verify the rotation value after rotated preview object')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. error={e}')
            return False
        return True

    def check_snap_line(self, verify_rgb=(242, 139, 249)): # check RGB color: https://www.rapidtables.com/convert/color/rgb-to-hex.html
        try:
            mouse_ctrl = Mouse_controller()
            el_object = self.exist(L.pan_zoom.magic_motion_designer.preview_selected_object)
            el_object.activate()
            pos_canvas = el_object.AXPosition
            size_canvas = el_object.AXSize
            time.sleep(OPERATION_DELAY * 0.5)
            center_x = pos_canvas[0] + int(size_canvas[0] / 2)
            center_y = pos_canvas[1] + int(size_canvas[1] / 2)
            src_pos = (center_x, center_y)
            time_gap = 0.5
            self.driver.mouse.click(*src_pos)
            time.sleep(time_gap)
            mouse_ctrl.press(mouse_button.left)
            time.sleep(time_gap)
            mouse_ctrl.move(0, -30)
            time.sleep(time_gap)
            mouse_ctrl.move(0, 30)
            time.sleep(time_gap)
            # snapshot full screen
            filename = self.screenshot()
            mouse_ctrl.release(mouse_button.left)
            img = Image.open(filename)
            img_rgb = img.convert('RGB')
            rgb_pixel_value = img_rgb.getpixel((center_x, center_y + int(size_canvas[1]/2) + 1))
            print(f'pos=({center_x},{center_y + int(size_canvas[1]/2) + 1}), rgb={rgb_pixel_value}')
            # verify if snap line appears by rgb value
            if rgb_pixel_value != verify_rgb:
                logger(f'Fail to verify RGB colr: {verify_rgb}')
                raise Exception
            logger('Verify snap line OK.')
        except Exception as e:
            logger(f'Exception occurs. error={e}')
            return False
        return True

    def resize_crop_region_from_node(self, node='upper_left', x_move_offset=0, y_move_offset=0):
        try:
            el_object = self.exist(L.pan_zoom.magic_motion_designer.preview_selected_object)
            el_object.activate()
            pos_object = el_object.AXPosition
            size_object = el_object.AXSize
            # center_x = pos_object[0] + int(size_object[0] / 2)
            # center_y = pos_object[1] + int(size_object[1] / 2)
            src_pos = pos_object
            if node == 'upper_middle':
                src_pos = (pos_object[0] + int(size_object[0]/2), pos_object[1])
            elif node == 'upper_right':
                src_pos = (pos_object[0] + size_object[0], pos_object[1])
            elif node == 'middle_left':
                src_pos = (pos_object[0], pos_object[1] + int(size_object[1]/2))
            elif node == 'middle_right':
                src_pos = (pos_object[0] + size_object[0], pos_object[1] + int(size_object[1]/2))
            elif node == 'lower_left':
                src_pos = (pos_object[0], pos_object[1] + size_object[1])
            elif node == 'lower_middle':
                src_pos = (pos_object[0] + int(size_object[0]/2), pos_object[1] + size_object[1])
            elif node == 'lower_right':
                src_pos = (pos_object[0] + size_object[0], pos_object[1] + size_object[1])
            dest_pos = (src_pos[0] + x_move_offset, src_pos[1] + y_move_offset)
            self.drag_mouse(src_pos, dest_pos)
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. error={e}')
            return False
        return True

    def resize_crop_region_from_upper_middle(self, y_move_offset=30):
        return self.resize_crop_region_from_node('upper_middle', 0, y_move_offset)

    def resize_crop_region_from_upper_left(self, x_move_offset=30, y_move_offset=30):
        return self.resize_crop_region_from_node('upper_left', x_move_offset, y_move_offset)

    def resize_crop_region_from_upper_right(self, x_move_offset=-30, y_move_offset=30):
        return self.resize_crop_region_from_node('upper_right', x_move_offset, y_move_offset)

    def resize_crop_region_from_middle_left(self, x_move_offset=30):
        return self.resize_crop_region_from_node('middle_left', x_move_offset, 0)

    def resize_crop_region_from_middle_right(self, x_move_offset=-30):
        return self.resize_crop_region_from_node('middle_right', x_move_offset, 0)

    def resize_crop_region_from_lower_left(self, x_move_offset=30, y_move_offset=-30):
        return self.resize_crop_region_from_node('lower_left', x_move_offset, y_move_offset)

    def resize_crop_region_from_lower_middle(self, y_move_offset=-30):
        return self.resize_crop_region_from_node('lower_middle', 0, y_move_offset)

    def resize_crop_region_from_lower_right(self, x_move_offset=-30, y_move_offset=-30):
        return self.resize_crop_region_from_node('lower_right', x_move_offset, y_move_offset)


class Keyframe(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add(self):
        return self.click(L.pan_zoom.magic_motion_designer.btn_add_keyframe)

    def remove(self):
        return self.click(L.pan_zoom.magic_motion_designer.btn_remove_keyframe)

    def select_previous(self):
        return self.click(L.pan_zoom.magic_motion_designer.btn_select_previous_keyframe)

    def select_next(self):
        return self.click(L.pan_zoom.magic_motion_designer.btn_select_next_keyframe)

    def duplicate_previous(self):
        try:
            self.click(L.pan_zoom.magic_motion_designer.btn_duplicate_keyframe)
            time.sleep(OPERATION_DELAY * 0.5)
            self.click(L.pan_zoom.magic_motion_designer.option_duplicate_previous_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def duplicate_next(self):
        try:
            self.click(L.pan_zoom.magic_motion_designer.btn_duplicate_keyframe)
            time.sleep(OPERATION_DELAY * 0.5)
            self.click(L.pan_zoom.magic_motion_designer.option_duplicate_next_keyframe)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_node(self, index, offset=0): # index: 1-based, offset: >0 (drag to right), <0 (drag to left)
        try:
            node = L.pan_zoom.magic_motion_designer.unit_node_keyframe.copy()
            node[1]['get_all'] = True
            els_node = self.exist(node)
            pos_x = els_node[index - 1].AXPosition[0] + int(els_node[index-1].AXSize[0] / 2)
            pos_y = els_node[index - 1].AXPosition[1] + int(els_node[index - 1].AXSize[1] / 2)
            start_pos = (pos_x, pos_y)
            dest_pos = (pos_x+offset, pos_y)
            self.drag_mouse(start_pos, dest_pos)
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True


class Preview_Operation(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def click_play(self):
        return self.click(L.pan_zoom.magic_motion_designer.btn_preview_operation_play)

    def click_stop(self):
        return self.click(L.pan_zoom.magic_motion_designer.btn_preview_operation_stop)

    def click_go_to_previous_frame(self):
        return self.click(L.pan_zoom.magic_motion_designer.btn_preview_operation_go_to_previous_frame)

    def click_go_to_next_frame(self):
        return self.click(L.pan_zoom.magic_motion_designer.btn_preview_operation_go_to_next_frame)

class Stepper_Operation(BasePage):
    def __init__(self, locator_group, category, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.locator_group = locator_group
        self.category = category

    def get_value(self):
        el_parent = self.exist(self.locator_group)
        return self.exist(L.pan_zoom.magic_motion_designer.unit_stepper_value, el_parent).AXValue

    def set_value(self, value):
        try:
            el_parent = self.exist(self.locator_group)
            el_edittext_value = self.exist(L.pan_zoom.magic_motion_designer.unit_stepper_value, el_parent)
            self.el_click(el_edittext_value)
            time.sleep(OPERATION_DELAY * 0.3)
            el_edittext_value.AXValue = str(value)
            time.sleep(OPERATION_DELAY * 0.3)
            self.keyboard.enter()
            time.sleep(OPERATION_DELAY * 0.5)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_stepper_up(self, times=1):
        try:
            el_parent = self.exist(self.locator_group)
            el_stepper_up = self.exist(L.pan_zoom.magic_motion_designer.unit_stepper_up, el_parent)
            for x in range(times):
                self.el_click(el_stepper_up)
                time.sleep(0.3)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_stepper_down(self, times=1):
        try:
            el_parent = self.exist(self.locator_group)
            el_stepper_down = self.exist(L.pan_zoom.magic_motion_designer.unit_stepper_down, el_parent)
            for x in range(times):
                self.el_click(el_stepper_down)
                time.sleep(0.3)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def set_slider(self, value): # value: integer or float
        try:
            el_slider = self.exist(eval(f'L.pan_zoom.magic_motion_designer.scale_{self.category}_slider'))
            el_slider.AXValue = value
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True