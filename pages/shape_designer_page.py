import time, datetime, os, copy

from .base_page import BasePage, AdjustSet, KEComboSet
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
# from AppKit import NSScreen
from .locator import locator as L
from .main_page import Main_Page
from reportportal_client import step

DELAY_TIME = 1 # sec


def _get_attribute_index(obj, attribute_name):
    try:
        index_row = -1
        tar_row = -1
        locator_outline_row = L.shape_designer.simple_track.keyframe_header_outline_row.copy()
        locator_outline_row[2]['get_all'] = True
        tar_outline_row = obj.exist(locator_outline_row)
        locator_attribute_name = L.shape_designer.simple_track.keyframe_header_name.copy()
        locator_attribute_name['AXValue'] = attribute_name
        locator_outline_row.append(locator_attribute_name)
        target = obj.exist(locator_outline_row)
        pos_row = target.AXParent.AXParent.AXPosition
        for idx in range(len(tar_outline_row)):
            if tar_outline_row[idx].AXPosition == pos_row:
                index_row = idx
                tar_row = tar_outline_row[idx]
                break
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        raise Exception
    return index_row, tar_row


def _get_track_visible(obj, attribute_name):
    try:
        index_row, tar_row = _get_attribute_index(obj, attribute_name)
        locator_slider_zoom = L.shape_designer.simple_track.slider_zoom.copy()
        pos_track = tar_row.AXPosition[1] + tar_row.AXSize[1]
        pos_slider = obj.exist(locator_slider_zoom)
        if pos_track < pos_slider.AXPosition[1]:
            return False
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        raise Exception
    return True


def _control_keyframe(obj, attribute_name, locator_operation=None):
    try:
        if _get_track_visible(obj, attribute_name):
            logger(f'"{attribute_name}" track is not fully visible')
            raise Exception
        index_row, tar_row = _get_attribute_index(obj, attribute_name)
        if locator_operation:
            target_btn = obj.exist(locator_operation, tar_row)
            value = target_btn.AXEnabled
            if value:
                obj.el_click(target_btn)
            time.sleep(DELAY_TIME * 1)
        else:
            value = True
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        raise Exception
    return value


def _right_click_menu_keyframe(obj, attribute_name, locator_operation=None, index=-1):
    try:
        if _get_track_visible(obj, attribute_name):
            logger(f'"{attribute_name}" track is not fully visible')
            raise Exception
        index_row, tar_row = _get_attribute_index(obj, attribute_name)
        locator_outline_row = L.shape_designer.simple_track.keyframe_track_outline_row.copy()
        locator_outline_row[1]['get_all'] = True
        els_outline_row = obj.exist(locator_outline_row)
        locator_node_group = L.shape_designer.simple_track.keyframe_node_group.copy()
        locator_node_group['get_all'] = True
        els_node = obj.exist(locator_node_group, els_outline_row[index_row])
        obj.mouse.move(*els_node[index-1].center)
        time.sleep(DELAY_TIME * 1)
        obj.right_click()
        time.sleep(DELAY_TIME * 2)
        target_menu_item = obj.exist(locator_operation)
        if locator_operation and not index == -1:
            value = target_menu_item.AXEnabled
            if not value:
                obj.click(None)
                return False
            obj.el_click(target_menu_item)
            time.sleep(DELAY_TIME * 1)
        else:
            value = True
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        raise Exception
    return value


class Shape_Designer(Main_Page, BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.properties = self.Properties(*args, **kwargs)
        self.keyframe = Keyframe(*args, **kwargs)
        self.simple_timeline = self.Simple_Timeline(*args, **kwargs)
        self.save_as = self.SaveAs(*args, **kwargs)

    class Properties(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.shape_type = self.Shape_Type(*args, **kwargs)
            self.shape_preset = self.Shape_Preset(*args, **kwargs)
            self.shape_fill = self.Shape_Fill(*args, **kwargs)
            self.shape_outline = self.Shape_Outline(*args, **kwargs)
            self.shadow = self.Shadow(*args, **kwargs)
            self.title = self.Title(*args, **kwargs)
        @step('[Action][Properties] Fold/ Unfold Shape Type')
        def unfold_shape_type(self, set_unfold=1):
            try:
                current_value = self.exist(L.shape_designer.shape_type.btn_shape_type).AXValue
                if current_value != set_unfold:
                    self.exist_click(L.shape_designer.shape_type.btn_shape_type)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][Properties] Fold/ Unfold Shape Preset')
        def unfold_shape_preset(self, set_unfold=1):
            try:
                current_value = self.exist(L.shape_designer.shape_preset.btn_shape_preset).AXValue
                if current_value != set_unfold:
                    self.exist_click(L.shape_designer.shape_preset.btn_shape_preset)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][Properties] Fold/ Unfold Shape Fill')
        def unfold_shape_fill(self, set_unfold=1):
            try:
                current_value = self.exist(L.shape_designer.shape_fill.btn_shape_fill).AXValue
                if current_value != set_unfold:
                    self.exist_click(L.shape_designer.shape_fill.btn_shape_fill)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][Properties] Fold/ Unfold Shape Outline')
        def unfold_shape_outline(self, set_unfold=1):
            try:
                current_value = self.exist(L.shape_designer.shape_outline.btn_shape_outline).AXValue
                if current_value != set_unfold:
                    self.exist_click(L.shape_designer.shape_outline.btn_shape_outline)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][Properties] Fold/ Unfold Shadow')
        def unfold_shadow(self, set_unfold=1):
            try:
                current_value = self.exist(L.shape_designer.shadow.btn_shadow).AXValue
                if current_value != set_unfold:
                    self.exist_click(L.shape_designer.shadow.btn_shadow)
                time.sleep(DELAY_TIME)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def unfold_title(self, set_unfold=1):
            try:
                current_value = self.exist(L.shape_designer.title.btn_title).AXValue
                if current_value != set_unfold:
                    self.exist_click(L.shape_designer.title.btn_title)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        class Shape_Type(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            @step('[Action][Properties][Shape Type] Drag Scroll Bar')
            def drag_scroll_bar(self, value):
                try:
                    if not self.exist(L.shape_designer.shape_type.shape_type_collection_view):
                        logger("Not unfold shape type now")
                        raise Exception("Not unfold shape type now")
                    self.exist(L.shape_designer.shape_type.scroll_bar).AXValue = float(value)
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception(f'Exception occurs. log={e}')
                return True

            def get_unfold_status(self):
                check_status = self.exist(L.shape_designer.shape_type.btn_shape_type).AXValue
                return check_status

            @step('[Action][Properties][Shape Type] Apply Shape Type')
            def apply_type(self, index=1):
                # index = 1 (1st preset), 2 (2nd preset), 3 (3rd preset), ...
                try:
                    if not self.exist(L.shape_designer.shape_type.shape_type_collection_view):
                        logger("Not unfold shape type now")
                        raise Exception("Not unfold shape type now")
                    # apply type with index
                    current_index = index - 1
                    elem_item = L.shape_designer.shape_type.preset_collection_item.copy()
                    elem_item[1]['index'] = current_index
                    self.exist_click(elem_item)
                    time.sleep(DELAY_TIME)
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception(f'Exception occurs. log={e}')

        class Shape_Preset(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            def get_unfold_status(self):
                check_status = self.exist(L.shape_designer.shape_preset.btn_shape_preset).AXValue
                return check_status

            def check_index(self):
                menu_elem = self.exist(L.shape_designer.shape_preset.setting_outline_view_menu)
                pos_y = menu_elem.AXPosition[1]
                return pos_y
            
            @step('[Action][Properties][Shape Preset] Apply Shape Preset')
            def apply_preset(self, index=1):
                # index = 1 (1st preset), 2 (2nd preset), 3 (3rd preset), ...
                try:
                    check_pos_y = self.check_index()
                    setting_elem = L.shape_designer.left_panel_outline_view_parameter_setting.copy()
                    for x in range(6):
                        setting_elem[1]['index'] = x
                        current_y = self.get_position(setting_elem)
                        #logger(current_y['y'])
                        if current_y['y'] > check_pos_y:
                            logger("Find index")
                            break

                    current_index = index - 1
                    find_item = L.shape_designer.shape_preset.preset_collection_item.copy()
                    find_item[1]['index'] = current_index
                    elem_item = self.exist(find_item, parent=setting_elem)

                    if not self.el_click(elem_item):
                        raise Exception('Cannot find element')

                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception(f'Exception occurs. log={e}')
                return True

        class Shape_Fill(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.blur = self.Blur(*args, **kwargs)
                self.opacity = self.Opacity(*args, **kwargs)

            def get_unfold_status(self):
                check_status = self.exist(L.shape_designer.shape_fill.btn_shape_fill).AXValue
                return check_status

            def get_checkbox_status(self):
                check_status = self.exist(L.shape_designer.shape_fill.checkbox).AXValue
                return check_status

            @step('[Action][Properties][Shape Fill] Enable/ Disable Fill')
            def apply_checkbox(self, bCheck=1):
                try:
                    current_value = self.get_checkbox_status()
                    if current_value != bCheck:
                        self.exist_click(L.shape_designer.shape_fill.checkbox)
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception(f'Exception occurs. log={e}')
                return True

            def get_fill_type(self):
                try:
                    current_value = self.exist(L.shape_designer.shape_fill.fill_type_dropdown_menu)
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return current_value.AXTitle

            def set_fill_type(self, current_type=1):
                try:
                    if current_type == 1:
                        option = L.shape_designer.shape_fill.fill_type_Uniform
                    elif current_type == 2:
                        option = L.shape_designer.shape_fill.fill_type_Gradient
                    else:
                        logger('Invalid parameter')
                        return False

                    self.exist_click(L.shape_designer.shape_fill.fill_type_dropdown_menu)
                    self.exist_click(option)
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def set_uniform_color(self, hexcolor):
                try:
                    if not self.is_exist(L.shape_designer.shape_fill.fill_type_uniform_color):
                        logger('Cannot find fill_type_uniform_color locator')
                        raise Exception
                    self.click(L.shape_designer.shape_fill.fill_type_uniform_color)
                    self.color_picker_switch_category_to_RGB()

                    # Input hex color
                    self.double_click(L.media_room.colors.input_hex_color)
                    time.sleep(DELAY_TIME)
                    self.exist(L.media_room.colors.input_hex_color).sendKeys(hexcolor)
                    time.sleep(DELAY_TIME)
                    self.keyboard.enter()
                    self.exist(L.media_room.colors.btn_close).press()
                    time.sleep(DELAY_TIME)

                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True
            
            @step('[Action][Properties][Shape Fill] Set Gradient Begin Color')
            def set_gradient_begin(self, hexcolor):
                try:
                    if not self.is_exist(L.shape_designer.shape_fill.fill_type_gradient_begin_color):
                        logger('Cannot find fill_type_gradient_begin_color locator')
                        raise Exception('Cannot find fill_type_gradient_begin_color locator')
                    self.click(L.shape_designer.shape_fill.fill_type_gradient_begin_color)
                    self.color_picker_switch_category_to_RGB()

                    # Input hex color
                    self.double_click(L.media_room.colors.input_hex_color)
                    time.sleep(DELAY_TIME)
                    self.exist(L.media_room.colors.input_hex_color).sendKeys(hexcolor)
                    time.sleep(DELAY_TIME)
                    self.keyboard.enter()
                    self.exist(L.media_room.colors.btn_close).press()
                    time.sleep(DELAY_TIME)

                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception(f'Exception occurs. log={e}')
                return True

            @step('[Action][Properties][Shape Fill] Set Gradient End Color')
            def set_gradient_end(self, hexcolor):
                try:
                    if not self.is_exist(L.shape_designer.shape_fill.fill_type_gradient_end_color):
                        logger('Cannot find fill_type_gradient_end_color locator')
                        raise Exception('Cannot find fill_type_gradient_end_color locator')
                    self.click(L.shape_designer.shape_fill.fill_type_gradient_end_color)
                    self.color_picker_switch_category_to_RGB()

                    # Input hex color
                    self.double_click(L.media_room.colors.input_hex_color)
                    time.sleep(DELAY_TIME)
                    self.exist(L.media_room.colors.input_hex_color).sendKeys(hexcolor)
                    time.sleep(DELAY_TIME)
                    self.keyboard.enter()
                    self.exist(L.media_room.colors.btn_close).press()
                    time.sleep(DELAY_TIME)

                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception(f'Exception occurs. log={e}')
                return True
            '''
            def check_index(self):
                menu_elem = self.exist(L.shape_designer.shape_fill.setting_outline_view_menu)
                pos_y = menu_elem.AXPosition[1]
                return pos_y

            def get_parent(self, index=1):
                try:
                    check_pos_y = self.check_index()
                    setting_elem = L.shape_designer.left_panel_outline_view_parameter_setting.copy()
                    for x in range(6):
                        setting_elem[1]['index'] = x
                        current_y = self.get_position(setting_elem)
                        logger(current_y['y'])
                        if current_y['y'] > check_pos_y:
                            logger("Find index")
                            break

                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True
            '''
            class Blur(BasePage):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                @step('[Action][Properties][Shape Fill][Blur] Get Value')
                def get_value(self):
                    current_value = self.exist(L.shape_designer.shape_fill.text_field_blur, parent=L.shape_designer.left_panel_outline_view_parameter_setting)
                    return current_value.AXValue

                @step('[Action][Properties][Shape Fill][Blur] Set Value')
                def set_value(self, value):
                    try:
                        if (value > 20) | (value < 0):
                            logger('Invalid parameter')
                            raise Exception('Invalid parameter')

                        if not self.is_exist(L.shape_designer.shape_fill.text_field_blur):
                            raise Exception
                        self.click(L.shape_designer.shape_fill.text_field_blur)
                        self.mouse.click(times=2)

                        self.exist(L.shape_designer.shape_fill.text_field_blur).AXValue = str(value)
                        self.press_enter_key()
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception(f'Exception occurs. log={e}')
                    return True

                def set_slider(self, value):
                    try:
                        if (value > 20) | (value < 0):
                            logger('Invalid parameter')
                            return False

                        self.exist(L.shape_designer.shape_fill.slider_blur).AXValue = value
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
                                self.exist_click(L.shape_designer.shape_fill.arrow_up_btn_blur)
                            elif option == 1:
                                self.exist_click(L.shape_designer.shape_fill.arrow_down_btn_blur)

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception
                    return True
            class Opacity(BasePage):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                @step('[Action][Properties][Shape Fill][Opacity] Get Value')
                def get_value(self):
                    current_value = self.exist(L.shape_designer.shape_fill.text_field_opacity, parent=L.shape_designer.left_panel_outline_view_parameter_setting)
                    return current_value.AXValue

                def set_value(self, value):
                    try:
                        if (value > 100) | (value < 0):
                            logger('Invalid parameter')
                            return False

                        if not self.is_exist(L.shape_designer.shape_fill.text_field_opacity):
                            raise Exception
                        self.click(L.shape_designer.shape_fill.text_field_opacity)
                        self.mouse.click(times=2)

                        self.exist(L.shape_designer.shape_fill.text_field_opacity).AXValue = str(value)
                        self.press_enter_key()
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception
                    return True

                def set_slider(self, value):
                    try:
                        if (value > 100) | (value < 0):
                            logger('Invalid parameter')
                            return False

                        self.exist(L.shape_designer.shape_fill.slider_opacity).AXValue = value
                        time.sleep(DELAY_TIME)
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception
                    return True
                @step('[Action][Properties][Shape Fill][Opacity] Click Arrow to Adjust Value')
                def click_arrow(self, option, times=1):
                    try:
                        if (option > 1) | (option < 0):
                            logger('Invalid parameter')
                            raise Exception('Invalid parameter')
                        for x in range(times):
                            if option == 0:
                                self.exist_click(L.shape_designer.shape_fill.arrow_up_btn_opacity)
                            elif option == 1:
                                self.exist_click(L.shape_designer.shape_fill.arrow_down_btn_opacity)

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception(f'Exception occurs. log={e}')
                    return True

        class Shape_Outline(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.size = self.Size(*args, **kwargs)
                self.blur = self.Blur(*args, **kwargs)
                self.opacity = self.Opacity(*args, **kwargs)

            class Size(BasePage):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                @step('[Action][Properties][Shape Outline][Size] Get Value')
                def get_value(self):
                    current_value = self.exist(L.shape_designer.shape_outline.text_field_size, parent=L.shape_designer.left_panel_outline_view_parameter_setting)
                    return current_value.AXValue

                @step('[Action][Properties][Shape Outline][Size] Set Value')
                def set_value(self, value):
                    try:
                        if (value > 10) | (value < 0):
                            logger('Invalid parameter')
                            raise Exception('Invalid parameter')

                        if not self.is_exist(L.shape_designer.shape_outline.text_field_size):
                            raise Exception
                        self.click(L.shape_designer.shape_outline.text_field_size)
                        self.mouse.click(times=2)

                        self.exist(L.shape_designer.shape_outline.text_field_size).AXValue = str(value)
                        self.press_enter_key()
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception(f'Exception occurs. log={e}')
                    return True

                def set_slider(self, value):
                    try:
                        if (value > 10) | (value < 0):
                            logger('Invalid parameter')
                            return False

                        self.exist(L.shape_designer.shape_outline.slider_size).AXValue = value
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
                                self.exist_click(L.shape_designer.shape_outline.arrow_up_btn_size)
                            elif option == 1:
                                self.exist_click(L.shape_designer.shape_outline.arrow_down_btn_size)

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception
                    return True

            class Blur(BasePage):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                @step('[Action][Properties][Shape Outline][Blur] Get Value')
                def get_value(self):
                    current_value = self.exist(L.shape_designer.shape_outline.text_field_blur, parent=L.shape_designer.left_panel_outline_view_parameter_setting)
                    return current_value.AXValue

                def set_value(self, value):
                    try:
                        if (value > 20) | (value < 0):
                            logger('Invalid parameter')
                            return False

                        if not self.is_exist(L.shape_designer.shape_outline.text_field_blur):
                            raise Exception
                        self.click(L.shape_designer.shape_outline.text_field_blur)
                        self.mouse.click(times=2)

                        self.exist(L.shape_designer.shape_outline.text_field_blur).AXValue = str(value)
                        self.press_enter_key()
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception
                    return True
                @step('[Action][Properties][Shape Outline][Blur] Set Value by Slider')
                def set_slider(self, value):
                    try:
                        if (value > 20) | (value < 0):
                            logger('Invalid parameter')
                            raise Exception('Invalid parameter')

                        self.exist(L.shape_designer.shape_outline.slider_blur).AXValue = value
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
                                self.exist_click(L.shape_designer.shape_outline.arrow_up_btn_blur)
                            elif option == 1:
                                self.exist_click(L.shape_designer.shape_outline.arrow_down_btn_blur)

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception
                    return True

            class Opacity(BasePage):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                def get_value(self):
                    current_value = self.exist(L.shape_designer.shape_outline.text_field_opacity, parent=L.shape_designer.left_panel_outline_view_parameter_setting)
                    return current_value.AXValue

                def set_value(self, value):
                    try:
                        if (value > 100) | (value < 0):
                            logger('Invalid parameter')
                            return False

                        if not self.is_exist(L.shape_designer.shape_outline.text_field_opacity):
                            raise Exception
                        self.click(L.shape_designer.shape_outline.text_field_opacity)
                        self.mouse.click(times=2)

                        self.exist(L.shape_designer.shape_outline.text_field_opacity).AXValue = str(value)
                        self.press_enter_key()
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception
                    return True

                def set_slider(self, value):
                    try:
                        if (value > 100) | (value < 0):
                            logger('Invalid parameter')
                            return False

                        self.exist(L.shape_designer.shape_outline.slider_opacity).AXValue = value
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
                                self.exist_click(L.shape_designer.shape_outline.arrow_up_btn_opacity)
                            elif option == 1:
                                self.exist_click(L.shape_designer.shape_outline.arrow_down_btn_opacity)

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception
                    return True

            def get_unfold_status(self):
                check_status = self.exist(L.shape_designer.shape_outline.btn_shape_outline).AXValue
                return check_status

            def get_checkbox_status(self):
                check_status = self.exist(L.shape_designer.shape_outline.checkbox).AXValue
                return check_status

            @step('[Action][Properties][Shape Outline] Enable/ Disable Outline')
            def apply_checkbox(self, bCheck=1):
                try:
                    current_value = self.get_checkbox_status()
                    if current_value != bCheck:
                        self.exist_click(L.shape_designer.shape_outline.checkbox)
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception(f'Exception occurs. log={e}')
                return True

            @step('[Action][Properties][Shape Outline] Set Line Type')
            def set_line_type(self, index):
                try:
                    # index = 1 (Left side type), 2 (Middle type) , 3 (Right side type)
                    if index == 1:
                        self.click(L.shape_designer.shape_outline.line_type_1)
                        return True
                    elif index == 2:
                        self.click(L.shape_designer.shape_outline.line_type_2)
                        return True
                    elif index == 3:
                        self.click(L.shape_designer.shape_outline.line_type_3)
                        return True
                    else:
                        raise Exception('Invalid parameter')
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception(f'Exception occurs. log={e}')

            def snapshot_line_type(self, file_name=None):

                line_type = self.exist(L.shape_designer.shape_outline.line_type)
                if not self.exist(line_type[0]):
                    raise Exception
                w, h = line_type[0].AXSize
                x, y = line_type[0].AXPosition
                new_w = w * 3
                return self.screenshot(file_name=file_name, w=new_w, x=x, y=y, h=h)

            def get_join_type(self):
                try:
                    current_value = self.exist(L.shape_designer.shape_outline.join_type_menu)

                    # if dropdown menu : gray out, return None
                    if not current_value.AXEnabled:
                        return None
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return current_value.AXTitle

            def set_join_type(self, option):
                try:
                    if option == 'round':
                        apply_menu = L.shape_designer.shape_outline.join_type_round
                    elif option == 'flat':
                        apply_menu = L.shape_designer.shape_outline.join_type_flat
                    else:
                        logger('Invalid parameter')
                        return False

                    self.exist_click(L.shape_designer.shape_outline.join_type_menu)
                    self.exist_click(apply_menu)
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def set_begin_arrow_type(self, index):
                try:
                    if (index > 6) | (index < 1):
                        logger('Invalid parameter')
                        return False
                    arrow_type = self.exist(L.shape_designer.shape_outline.arrow_begin_type)

                    # arrow_begin_type :
                    # Note: 1st arrow is 8th child, 2nd ~ 6th are 3~7th child on this locator list
                    el_list = [-1, 8, 3, 4, 5, 6, 7]
                    current_index = el_list[index]

                    if not self.exist(arrow_type[current_index]):
                        raise Exception
                    self.el_click(arrow_type[current_index])

                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def snapshot_begin_arrow_type(self, file_name=None):

                arrow_type = self.exist(L.shape_designer.shape_outline.arrow_begin_type)
                if not self.exist(arrow_type[3]):
                    raise Exception
                w, h = arrow_type[3].AXSize
                x, y = arrow_type[3].AXPosition
                new_x = x - w
                new_w = w * 6
                return self.screenshot(file_name=file_name, w=new_w, x=new_x, y=y, h=h)

            def set_begin_arrow_size(self, index):
                try:
                    if (index > 6) | (index < 1):
                        logger('Invalid parameter')
                        return False
                    arrow_size = self.exist(L.shape_designer.shape_outline.arrow_begin_type)
                    #logger(arrow_size)
                    #for x in range(8, 15):
                    #    current_el = arrow_size[x]
                    #    logger(current_el.AXPosition)

                    # arrow_begin_size :
                    # Note: 1st arrow size is 9th child, 2nd ~ 6th are 10~14th child on this locator list
                    el_list = [-1, 9, 10, 11, 12, 13, 14]
                    current_index = el_list[index]

                    if not self.exist(arrow_size[current_index]):
                        raise Exception
                    self.el_click(arrow_size[current_index])

                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def snapshot_begin_arrow_size(self, file_name=None):

                arrow_type = self.exist(L.shape_designer.shape_outline.arrow_begin_type)
                if not self.exist(arrow_type[9]):
                    raise Exception
                w, h = arrow_type[9].AXSize
                x, y = arrow_type[9].AXPosition
                new_w = w * 6
                return self.screenshot(file_name=file_name, w=new_w, x=x, y=y, h=h)

            def set_end_arrow_type(self, index):
                try:
                    if (index > 6) | (index < 1):
                        logger('Invalid parameter')
                        return False
                    arrow_type = self.exist(L.shape_designer.shape_outline.arrow_begin_type)
                    #logger(arrow_type)

                    # end_begin_size :
                    # Note: 1st arrow size is 15th child, 2nd ~ 6th are 16~20th child on this locator list
                    el_list = [-1, 15, 16, 17, 18, 19, 20]
                    current_index = el_list[index]

                    if not self.exist(arrow_type[current_index]):
                        raise Exception
                    self.el_click(arrow_type[current_index])

                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def snapshot_end_arrow_type(self, file_name=None):

                arrow_type = self.exist(L.shape_designer.shape_outline.arrow_begin_type)
                if not self.exist(arrow_type[15]):
                    raise Exception
                w, h = arrow_type[15].AXSize
                x, y = arrow_type[15].AXPosition
                new_w = w * 6
                return self.screenshot(file_name=file_name, w=new_w, x=x, y=y, h=h)

            def set_end_arrow_size(self, index):
                try:
                    if (index > 6) | (index < 1):
                        logger('Invalid parameter')
                        return False
                    arrow_size = self.exist(L.shape_designer.shape_outline.arrow_begin_type)
                    #logger(arrow_size)

                    # arrow_begin_size :
                    # Note: 1st arrow size is 21th child, 2nd ~ 6th are 22~26th child on this locator list
                    el_list = [-1, 21, 22, 23, 24, 25, 26]
                    current_index = el_list[index]

                    if not self.exist(arrow_size[current_index]):
                        raise Exception
                    self.el_click(arrow_size[current_index])

                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def snapshot_end_arrow_size(self, file_name=None):

                arrow_size = self.exist(L.shape_designer.shape_outline.arrow_begin_type)
                if not self.exist(arrow_size[21]):
                    raise Exception
                w, h = arrow_size[21].AXSize
                x, y = arrow_size[21].AXPosition
                new_w = w * 6
                return self.screenshot(file_name=file_name, w=new_w, x=x, y=y, h=h)

            def get_fill_type(self):
                try:
                    current_value = self.exist(L.shape_designer.shape_outline.fill_type_dropdown_menu)
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return current_value.AXTitle

            def set_fill_type(self, current_type=1):
                try:
                    if current_type == 1:
                        option = L.shape_designer.shape_outline.fill_type_Uniform
                    elif current_type == 2:
                        option = L.shape_designer.shape_outline.fill_type_Gradient
                    else:
                        logger('Invalid parameter')
                        return False

                    self.exist_click(L.shape_designer.shape_outline.fill_type_dropdown_menu)
                    self.exist_click(option)
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            @step('[Action][Properties][Shape Outline] Set Uniform Color')
            def set_uniform_color(self, hexcolor):
                try:
                    if not self.is_exist(L.shape_designer.shape_outline.fill_type_uniform_color):
                        logger('Cannot find fill_type_uniform_color locator')
                        raise Exception('Cannot find fill_type_uniform_color locator')
                    self.click(L.shape_designer.shape_outline.fill_type_uniform_color)
                    self.color_picker_switch_category_to_RGB()

                    # Input hex color
                    self.double_click(L.media_room.colors.input_hex_color)
                    time.sleep(DELAY_TIME)
                    self.exist(L.media_room.colors.input_hex_color).sendKeys(hexcolor)
                    time.sleep(DELAY_TIME)
                    self.keyboard.enter()
                    self.exist(L.media_room.colors.btn_close).press()
                    time.sleep(DELAY_TIME)

                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception(f'Exception occurs. log={e}')
                return True

            def set_gradient_begin(self, hexcolor):
                try:
                    if not self.is_exist(L.shape_designer.shape_outline.fill_type_gradient_begin_color):
                        logger('Cannot find fill_type_gradient_begin_color locator')
                        raise Exception
                    self.click(L.shape_designer.shape_outline.fill_type_gradient_begin_color)
                    self.color_picker_switch_category_to_RGB()

                    # Input hex color
                    self.double_click(L.media_room.colors.input_hex_color)
                    time.sleep(DELAY_TIME)
                    self.exist(L.media_room.colors.input_hex_color).sendKeys(hexcolor)
                    time.sleep(DELAY_TIME)
                    self.keyboard.enter()
                    self.exist(L.media_room.colors.btn_close).press()
                    time.sleep(DELAY_TIME)

                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def set_gradient_end(self, hexcolor):
                try:
                    if not self.is_exist(L.shape_designer.shape_outline.fill_type_gradient_end_color):
                        logger('Cannot find fill_type_gradient_end_color locator')
                        raise Exception
                    self.click(L.shape_designer.shape_outline.fill_type_gradient_end_color)
                    self.color_picker_switch_category_to_RGB()

                    # Input hex color
                    self.double_click(L.media_room.colors.input_hex_color)
                    time.sleep(DELAY_TIME)
                    self.exist(L.media_room.colors.input_hex_color).sendKeys(hexcolor)
                    time.sleep(DELAY_TIME)
                    self.keyboard.enter()
                    self.exist(L.media_room.colors.btn_close).press()
                    time.sleep(DELAY_TIME)

                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

        class Shadow(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.distance = self.Distance(*args, **kwargs)
                self.blur = self.Blur(*args, **kwargs)
                self.opacity = self.Opacity(*args, **kwargs)
                self.fill_shadow = self.Fill_Shadow(*args, **kwargs)
                self.direction = self.Direction(*args, **kwargs)

            def get_unfold_status(self):
                check_status = self.exist(L.shape_designer.shadow.btn_shadow).AXValue
                return check_status

            def get_checkbox_status(self):
                check_status = self.exist(L.shape_designer.shadow.checkbox).AXValue
                return check_status

            @step('[Action][Properties][Shadow] Enable/ Disable Shadow')
            def apply_checkbox(self, bCheck=1):
                try:
                    current_value = self.get_checkbox_status()
                    if current_value != bCheck:
                        self.exist_click(L.shape_designer.shadow.checkbox)
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception(f'Exception occurs. log={e}')
                return True

            def get_apply_shadow_to(self):
                try:
                    current_title = self.exist(L.shape_designer.shadow.apply_shadow_dropdown_menu)

                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return current_title.AXTitle

            @step('[Action][Properties][Shadow] Set Apply Shadow To')
            def set_apply_shadow_to(self, current_type=1):
                try:
                    if current_type == 1:
                        option = L.shape_designer.shadow.shadow_type_both
                    elif current_type == 2:
                        option = L.shape_designer.shadow.shadow_type_outline
                    elif current_type == 3:
                        option = L.shape_designer.shadow.shadow_type_object
                    else:
                        logger('Invalid parameter')
                        raise Exception('Invalid parameter')

                    self.exist_click(L.shape_designer.shadow.apply_shadow_dropdown_menu)
                    self.exist_click(option)
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception(f'Exception occurs. log={e}')
                return True

            class Distance(BasePage):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                @step('[Action][Properties][Shadow][Distance] Get Value')
                def get_value(self):
                    current_value = self.exist(L.shape_designer.shadow.text_field_distance, parent=L.shape_designer.left_panel_outline_view_parameter_setting)
                    return current_value.AXValue

                @step('[Action][Properties][Shadow][Distance] Set Value')
                def set_value(self, value):
                    try:
                        if (value > 100) | (value < 0):
                            logger('Invalid parameter')
                            raise Exception('Invalid parameter')

                        if not self.is_exist(L.shape_designer.shadow.text_field_distance):
                            raise Exception
                        self.click(L.shape_designer.shadow.text_field_distance)
                        self.mouse.click(times=2)

                        self.exist(L.shape_designer.shadow.text_field_distance).AXValue = str(value)
                        self.press_enter_key()
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception(f'Exception occurs. log={e}')
                    return True

                def set_slider(self, value):
                    try:
                        if (value > 100) | (value < 0):
                            logger('Invalid parameter')
                            return False

                        self.exist(L.shape_designer.shadow.slider_distance).AXValue = value
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
                                self.exist_click(L.shape_designer.shadow.arrow_up_btn_distance)
                            elif option == 1:
                                self.exist_click(L.shape_designer.shadow.arrow_down_btn_distance)

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception
                    return True

            class Blur(BasePage):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                @step('[Action][Properties][Shadow][Blur] Get Value')
                def get_value(self):
                    current_value = self.exist(L.shape_designer.shadow.text_field_blur, parent=L.shape_designer.left_panel_outline_view_parameter_setting)
                    return current_value.AXValue

                @step('[Action][Properties][Shadow][Blur] Set Value')
                def set_value(self, value):
                    try:
                        if (value > 20) | (value < 0):
                            logger('Invalid parameter')
                            raise Exception('Invalid parameter')

                        if not self.is_exist(L.shape_designer.shadow.text_field_blur):
                            raise Exception
                        self.click(L.shape_designer.shadow.text_field_blur)
                        self.mouse.click(times=2)

                        self.exist(L.shape_designer.shadow.text_field_blur).AXValue = str(value)
                        self.press_enter_key()
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception(f'Exception occurs. log={e}')
                    return True

                def set_slider(self, value):
                    try:
                        if (value > 20) | (value < 0):
                            logger('Invalid parameter')
                            return False

                        self.exist(L.shape_designer.shadow.slider_blur).AXValue = value
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
                                self.exist_click(L.shape_designer.shadow.arrow_up_btn_blur)
                            elif option == 1:
                                self.exist_click(L.shape_designer.shadow.arrow_down_btn_blur)

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception
                    return True

            class Opacity(BasePage):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                @step('[Action][Properties][Shadow][Opacity] Get Value')
                def get_value(self):
                    current_value = self.exist(L.shape_designer.shadow.text_field_opacity, parent=L.shape_designer.left_panel_outline_view_parameter_setting)
                    return current_value.AXValue

                def set_value(self, value):
                    try:
                        if (value > 100) | (value < 0):
                            logger('Invalid parameter')
                            return False

                        if not self.is_exist(L.shape_designer.shadow.text_field_opacity):
                            raise Exception
                        self.click(L.shape_designer.shadow.text_field_opacity)
                        self.mouse.click(times=2)

                        self.exist(L.shape_designer.shadow.text_field_opacity).AXValue = str(value)
                        self.press_enter_key()
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception
                    return True

                @step('[Action][Properties][Shadow][Opacity] Set Value by Slider')
                def set_slider(self, value):
                    try:
                        if (value > 100) | (value < 0):
                            logger('Invalid parameter')
                            raise Exception('Invalid parameter')

                        self.exist(L.shape_designer.shadow.slider_opacity).AXValue = value
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
                                self.exist_click(L.shape_designer.shadow.arrow_up_btn_opacity)
                            elif option == 1:
                                self.exist_click(L.shape_designer.shadow.arrow_down_btn_opacity)

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception
                    return True

            class Fill_Shadow(BasePage):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                @step('[Action][Properties][Shadow][Fill Shadow] Get status of Fill Shadow')
                def get_checkbox(self):
                    current_value = self.exist(L.shape_designer.shadow.checkbox_fill_shadow, parent=L.shape_designer.left_panel_outline_view_parameter_setting)
                    return current_value.AXValue

                @step('[Action][Properties][Shadow][Fill Shadow] Enable/ Disable Fill Shadow')
                def apply_checkbox(self, bCheck=1):
                    try:
                        current_value = self.get_checkbox()
                        if current_value != bCheck:
                            self.exist_click(L.shape_designer.shadow.checkbox_fill_shadow)
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception
                    return True

                def set_color(self, hexcolor):
                    try:
                        if not self.is_exist(L.shape_designer.shadow.fill_shadow_custom_color):
                            logger('Cannot find fill_shadow_custom_color locator')
                            raise Exception
                        self.click(L.shape_designer.shadow.fill_shadow_custom_color)
                        self.color_picker_switch_category_to_RGB()

                        # Input hex color
                        self.double_click(L.media_room.colors.input_hex_color)
                        time.sleep(DELAY_TIME)
                        self.exist(L.media_room.colors.input_hex_color).sendKeys(hexcolor)
                        time.sleep(DELAY_TIME)
                        self.keyboard.enter()
                        self.exist(L.media_room.colors.btn_close).press()
                        time.sleep(DELAY_TIME)

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception
                    return True

            class Direction(BasePage):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                @step('[Action][Properties][Shadow][Direction] Get Value')
                def get_value(self):
                    current_value = self.exist(L.shape_designer.shadow.text_field_shadow_direction, parent=L.shape_designer.left_panel_outline_view_parameter_setting)
                    return current_value.AXValue

                @step('[Action][Properties][Shadow][Direction] Set Value')
                def set_value(self, value):
                    try:
                        '''
                        if (value > 100) | (value < 0):
                            logger('Invalid parameter')
                            return False
                        '''
                        if not self.is_exist(L.shape_designer.shadow.text_field_shadow_direction):
                            raise Exception('Cannot find text_field_shadow_direction locator')
                        self.click(L.shape_designer.shadow.text_field_shadow_direction)
                        self.mouse.click(times=2)

                        self.exist(L.shape_designer.shadow.text_field_shadow_direction).AXValue = str(value)
                        self.press_enter_key()
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
                                self.exist_click(L.shape_designer.shadow.arrow_up_btn_shadow_direction)
                            elif option == 1:
                                self.exist_click(L.shape_designer.shadow.arrow_down_btn_shadow_direction)

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception
                    return True

        class Title(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            def get_unfold_status(self):
                check_status = self.exist(L.shape_designer.title.btn_title).AXValue
                return check_status

            def get_title(self):
                try:
                    if not self.is_exist(L.shape_designer.title.txt_field):
                        raise Exception
                    current_title = self.exist(L.shape_designer.title.txt_field).AXValue
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return current_title

            def set_title(self, strText):
                try:
                    if not self.is_exist(L.shape_designer.title.txt_field):
                        raise Exception

                    self.click(L.shape_designer.title.txt_field)
                    self.mouse.click(times=2)
                    self.exist(L.shape_designer.title.txt_field).AXValue = str(strText)
                    self.press_esc_key()
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True
            
            @step('[Action][Properties][Title][Font Type] Get Font Type')
            def get_font_type(self):
                try:
                    if not self.is_exist(L.shape_designer.title.font_cbx_menu):
                        raise Exception
                    current_font = self.exist(L.shape_designer.title.font_cbx_menu).AXValue
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception(f'Exception occurs. log={e}')
                return current_font

            @step('[Action][Properties][Title][Font Type] Set Font Type')
            def set_font_type(self, strType):
                try:
                    if not self.is_exist(L.shape_designer.title.font_cbx_menu):
                        raise Exception('Cannot find font_cbx_menu locator')

                    self.click(L.shape_designer.title.font_cbx_menu)
                    self.mouse.click(times=3)
                    self.press_del_key()
                    self.keyboard.send(strType)
                    self.press_enter_key()
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception(f'Exception occurs. log={e}')
                return True

            def unfold_font_type_menu(self):
                try:
                    if not self.is_exist(L.shape_designer.title.font_type_triangle_button):
                        raise Exception
                    current_font = self.click(L.shape_designer.title.font_type_triangle_button)
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return current_font

            @step('[Action][Properties][Title][Font Size] Get Font Size')
            def get_font_size(self):
                try:
                    if not self.is_exist(L.shape_designer.title.size_cbx_menu):
                        raise Exception('Cannot find size_cbx_menu locator')
                    current_size = self.exist(L.shape_designer.title.size_cbx_menu).AXValue
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception(f'Exception occurs. log={e}')
                return current_size

            @step('[Action][Properties][Title][Font Size] Set Font Size')
            def set_font_size(self, strSize):
                try:
                    if not self.is_exist(L.shape_designer.title.size_cbx_menu):
                        raise Exception

                    self.click(L.shape_designer.title.size_cbx_menu)
                    self.mouse.click(times=3)
                    self.press_del_key()
                    self.keyboard.send(str(strSize))
                    self.press_enter_key()
                    time.sleep(DELAY_TIME)
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception(f'Exception occurs. log={e}')
                return True

            def unfold_font_size_menu(self):
                try:
                    if not self.is_exist(L.shape_designer.title.size_triangle_button):
                        raise Exception
                    current_font = self.click(L.shape_designer.title.size_triangle_button)
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return current_font

            @step('[Action][Properties][Title][Font Color] Get Font Color')
            def set_font_color(self, hexcolor):
                try:
                    if not self.is_exist(L.shape_designer.title.title_color):
                        logger('Cannot find title_color locator')
                        raise Exception('Cannot find title_color locator')
                    self.click(L.shape_designer.title.title_color)
                    self.color_picker_switch_category_to_RGB()

                    # Input hex color
                    self.double_click(L.media_room.colors.input_hex_color)
                    time.sleep(DELAY_TIME)
                    self.exist(L.media_room.colors.input_hex_color).sendKeys(hexcolor)
                    time.sleep(DELAY_TIME)
                    self.keyboard.enter()
                    self.exist(L.media_room.colors.btn_close).press()
                    time.sleep(DELAY_TIME)

                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception(f'Exception occurs. log={e}')
                return True

            def click_bold_btn(self):
                try:
                    if not self.is_exist(L.shape_designer.title.btn_bold):
                        raise Exception
                    self.click(L.shape_designer.title.btn_bold)
                    self.move_mouse_to_0_0()
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def get_bold_grayout_status(self):
                try:
                    # gray out : return True
                    # not gray out : return False
                    if not self.is_exist(L.shape_designer.title.btn_bold):
                        raise Exception
                    gray_status = self.exist(L.shape_designer.title.btn_bold).AXEnabled
                    result = not gray_status
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return result

            def click_italic_btn(self):
                try:
                    if not self.is_exist(L.shape_designer.title.btn_italic):
                        raise Exception
                    self.click(L.shape_designer.title.btn_italic)
                    self.move_mouse_to_0_0()
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def get_italic_grayout_status(self):
                try:
                    # gray out : return True
                    # not gray out : return False
                    if not self.is_exist(L.shape_designer.title.btn_italic):
                        raise Exception
                    gray_status = self.exist(L.shape_designer.title.btn_italic).AXEnabled
                    result = not gray_status
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return result

            def set_align(self, option):
                # option = left, center, right
                try:
                    if option == 'left':
                        self.click(L.shape_designer.title.btn_align_left)
                    elif option == 'center':
                        self.click(L.shape_designer.title.btn_align_center)
                    elif option == 'right':
                        self.click(L.shape_designer.title.btn_align_right)
                    else:
                        logger('Invalid parameter')
                        return False

                    self.move_mouse_to_0_0()
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def snapshot_align_status(self, file_name=None):
                try:
                    elem_image = self.exist(L.shape_designer.title.btn_align_left)
                    if not elem_image:
                        logger('Cannot find btn_align_left in Shape designer')
                        return None
                    else:
                        w, h = elem_image.AXSize
                        x, y = elem_image.AXPosition

                        new_w = w*3
                    return self.screenshot(file_name=file_name, w=new_w, x=x, y=y, h=h)

                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception

            def get_shrink_checkbox(self):
                current_value = self.exist(L.shape_designer.title.checkbox_shrink)
                return current_value.AXValue

            def set_shrink_checkbox(self, bCheck=1):
                try:
                    current_value = self.get_shrink_checkbox()
                    if current_value != bCheck:
                        self.exist_click(L.shape_designer.title.checkbox_shrink)
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

    def check_in_shape_designer(self):
        if not self.is_exist(L.shape_designer.designer_window):
            logger('not enter Shape Designer')
            return False

        # Verify Step:
        if not self.exist(L.shape_designer.designer_window).AXTitle.startswith('Shape Designer  |'):
            logger('Not enter Shape Designer now.')
            return False
        else:
            return True
    
    @step('[Action][Shape Designer] Maximize Shape Designer')
    def click_restore_btn(self):
        try:
            if not self.exist_click(L.shape_designer.btn_zoom):
                raise Exception('Cannot find Shape Designer Zoom button')
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_close_btn(self):
        try:
            if not self.exist_click(L.shape_designer.btn_close):
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Shape Designer] Click Undo')
    def click_undo(self):
        try:
            if not self.exist_click(L.shape_designer.btn_undo):
                raise Exception('Unable to find undo button')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_redo(self):
        try:
            if not self.exist_click(L.shape_designer.btn_redo):
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_zoom_in(self, times=1):
        try:
            if not self.exist(L.shape_designer.btn_zoom_in):
                raise Exception
            for x in range(times):
                self.exist_click(L.shape_designer.btn_zoom_in)
                time.sleep(DELAY_TIME*0.5)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_zoom_out(self, times=1):
        try:
            if not self.exist(L.shape_designer.btn_zoom_out):
                raise Exception
            for x in range(times):
                self.exist_click(L.shape_designer.btn_zoom_out)
                time.sleep(DELAY_TIME*0.5)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_viewer_zoom_menu(self, value='Fit'):
        '''
        :param value: Fit, 10%, 25%, 50%, 75%, 100%, ...
        '''
        try:
            if not self.check_in_shape_designer():
                raise Exception
            self.exist_click(L.shape_designer.cbx_viewer_zoom)
            self.exist_click({'AXRole': 'AXStaticText', 'AXValue': value})
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def get_viewer_setting(self):
        try:
            if not self.exist(L.shape_designer.cbx_viewer_zoom):
                raise Exception
            else:
                return self.exist(L.shape_designer.cbx_viewer_zoom).AXTitle
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
    
    @step('[Action][Shape Designer] Get Title Name')
    def get_title(self):
        try:
            if not self.exist(L.shape_designer.designer_window):
                logger('Not enter Shape Designer now')
                raise Exception('Not enter Shape Designer now')

            title = self.exist(L.shape_designer.designer_window).AXTitle
            return title[19:]
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
    
    @step('[Action][Shape Designer] Set Timecode')
    def set_timecode(self, timecode):
        self.activate()
        elem = self.find(L.shape_designer.timecode)
        w, h = elem.AXSize
        x, y = elem.AXPosition

        pos_click = tuple(map(int, (x + w * 0.1, y + h * 0.5)))
        self.mouse.click(*pos_click)
        time.sleep(1)
        self.keyboard.send(timecode.replace("_", ""))
        self.keyboard.enter()
        time.sleep(DELAY_TIME)

    @step('[Action][Shape Designer] Get Timecode')
    def get_timecode(self):
        try:
            if not self.exist(L.shape_designer.designer_window):
                logger("No shape designer window show up")
                raise Exception
            timecode = self.exist(L.shape_designer.timecode).AXValue
            return timecode
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def drag_properties_scroll_bar(self, value):
        try:
            if not self.exist(L.shape_designer.designer_window):
                logger("No Shape designer window show up")
                raise Exception
            self.exist(L.shape_designer.left_panel_scroll_bar).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Shape Designer] Click Properties Tab')
    def click_properties_tab(self):
        try:
            if not self.exist(L.shape_designer.designer_window):
                logger('Not enter Shape Designer now')
                raise Exception('Not enter Shape Designer now')

            if self.exist_click(L.shape_designer.properties_tab):
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    @step('[Action][Shape Designer] Click Keyframe Tab')
    def click_keyframe_tab(self):
        try:
            if not self.exist(L.shape_designer.designer_window):
                logger('Not enter Shape Designer now')
                raise Exception('Not enter Shape Designer now')

            if self.exist_click(L.shape_designer.keyframe_tab):
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    def handle_shape_outline_dialog(self):
        try:
            if not self.exist(L.shape_designer.alert_dialog.main):
                logger('Not pop up warning dialog')
                raise Exception

            # Verify Warning message
            if not self.exist(L.shape_designer.alert_dialog.shape_outline_warning_message):
                raise Exception
            else:
                self.exist_click(L.shape_designer.alert_dialog.btn_OK)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception

    def click_display_hide_timeline_mode(self):
        try:
            if not self.exist(L.shape_designer.designer_window):
                logger('No designer window show up')
                raise Exception

            if self.is_exist(L.shape_designer.btn_hide_timeline_mode):
                self.click(L.shape_designer.btn_hide_timeline_mode)
                time.sleep(0.5)
                # verify step
                if not self.is_exist(L.shape_designer.btn_hide_timeline_mode):
                    return True
                else:
                    logger("Verify fail, still exist btn_hide_timeline_mode")
                    return False
            elif self.is_exist(L.shape_designer.btn_show_timeline_mode):
                self.click(L.shape_designer.btn_show_timeline_mode)
                time.sleep(0.5)
                # verify step
                if not self.is_exist(L.shape_designer.btn_show_timeline_mode):
                    return True
                else:
                    logger("Verify fail, still exist btn_show_timeline_mode")
                    return False
            else:
                logger('Cannot find the button (Display/Hide timeline mode)')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception

    def check_timeline_mode_status(self):
        try:
            if not self.exist(L.shape_designer.designer_window):
                logger('No designer window show up')
                raise Exception

            if self.is_exist(L.shape_designer.btn_hide_timeline_mode):
                return True
            elif self.is_exist(L.shape_designer.btn_show_timeline_mode):
                return False
            else:
                logger('Cannot find the button (Display/Hide timeline mode)')
                return None
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception

    def switch_timecode_mode(self, mode=1):
        # parameter: mode = 1 (Click Clip mode), 2 (Click Movie mode)
        try:
            if not self.exist(L.shape_designer.designer_window):
                logger('No designer window show up')
                raise Exception

            if mode == 1:
                self.click(L.shape_designer.simple_track.btn_clip_mode)
                return True
            elif mode == 2:
                self.click(L.shape_designer.simple_track.btn_movie_mode)
                return True
            else:
                logger('Invalid parameter')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception

    def apply_snap_ref_line(self, bApply):
        try:
            if not self.exist(L.shape_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            self.exist_click(L.shape_designer.toggle_grid_line_on_off)
            if self.exist(L.shape_designer.snap_to_reference_line).AXMenuItemMarkChar == '✓':
                if bApply == 1:
                    self.right_click()
                    return True
                elif bApply == 0:
                    self.exist_click(L.shape_designer.snap_to_reference_line)
            else:
                if bApply == 1:
                    self.exist_click(L.shape_designer.snap_to_reference_line)
                elif bApply == 0:
                    self.right_click()
                    return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def get_ref_line_status(self):
        try:
            if not self.exist(L.shape_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            self.exist_click(L.shape_designer.toggle_grid_line_on_off)
            if self.exist(L.shape_designer.snap_to_reference_line).AXMenuItemMarkChar == '✓':
                self.right_click()
                return 1
            else:
                self.right_click()
                return 0

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception

    def select_grid_lines_format(self, index=1):
        try:
            if not self.exist(L.shape_designer.designer_window):
                logger("No designer window show up")
                raise Exception

            # Handle sub menu w/ index
            el_list = [-1, 'none', 2, 3, 4, 5, 6, 7, 8, 9, 10]
            sub_menu_locator = eval(f'L.shape_designer.menu_item_{el_list[index]}')
            self.click(L.shape_designer.toggle_grid_line_on_off)
            self.click(L.shape_designer.grid_lines)
            if index == 1:
                x,y = self.exist(L.shape_designer.menu_item_4).AXPosition
                self.mouse.move(x, y)

            self.exist_click(sub_menu_locator)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_preview_operation(self, operation):
        try:
            logger('1674')
            if not self.exist(L.shape_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            if operation == 'Play':
                self.exist_click(L.shape_designer.preview_play)
            elif operation == 'Pause':
                self.exist_click(L.shape_designer.preview_play)
            elif operation == 'Stop':
                self.exist_click(L.shape_designer.preview_stop)
            elif operation == 'Previous_Frame':
                self.exist_click(L.shape_designer.preview_previous_frame)
            elif operation == 'Next_Frame':
                self.exist_click(L.shape_designer.preview_next_frame)
            elif operation == 'Fast_Forward':
                self.exist_click(L.shape_designer.preview_fast_forward)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True
    
    @step('[Action][Shape Designer] Adjust object on Canvas to large')
    def adjust_object_on_Canvas_resize_to_large(self):
        try:
            if not self.exist(L.shape_designer.designer_window):
                logger("No designer window show up")
                raise Exception("No designer window show up")
            x,y = self.exist(L.shape_designer.canvas_object_shape).AXPosition
            size_w, size_h = self.exist(L.shape_designer.canvas_object_shape).AXSize
            new_x = x - (size_w*0.5)
            new_y = y - size_h
            logger(size_w)
            self.mouse.move(x,y)
            time.sleep(DELAY_TIME*0.5)
            self.drag_mouse((x, y), (new_x, new_y))
            time.sleep(DELAY_TIME*0.5)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Shape Designer] Move object on Canvas to left')
    def adjust_object_on_Canvas_move_to_left(self):
        try:
            if not self.exist(L.shape_designer.designer_window):
                logger("No designer window show up")
                raise Exception("No designer window show up")
            x,y = self.exist(L.shape_designer.canvas_object_shape).AXPosition
            size_w, size_h = self.exist(L.shape_designer.canvas_object_shape).AXSize
            new_x = x + (size_w*0.1)
            new_y = y + (size_h*0.3)
            dest_x = x - size_w*0.4
            self.mouse.move(new_x,new_y)
            time.sleep(DELAY_TIME*0.5)
            self.drag_mouse((new_x, new_y), (dest_x, new_y))
            time.sleep(DELAY_TIME*0.5)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def adjust_object_on_Canvas_move_to_right(self):
        try:
            if not self.exist(L.shape_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            x,y = self.exist(L.shape_designer.canvas_object_shape).AXPosition
            size_w, size_h = self.exist(L.shape_designer.canvas_object_shape).AXSize
            new_x = x + (size_w*0.1)
            new_y = y + (size_h*0.3)
            dest_x = x + size_w
            self.mouse.move(new_x,new_y)
            time.sleep(DELAY_TIME*0.5)
            self.drag_mouse((new_x, new_y), (dest_x, new_y))
            time.sleep(DELAY_TIME*0.5)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def adjust_object_on_Canvas_rotate_clockwise(self):
        try:
            if not self.exist(L.shape_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            x,y = self.exist(L.shape_designer.canvas_object_shape).AXPosition
            size_w, size_h = self.exist(L.shape_designer.canvas_object_shape).AXSize
            new_x = x + (size_w*0.5)
            new_y = y - (size_h*0.05)
            dest_x = x + size_w
            self.mouse.move(new_x,new_y)
            time.sleep(DELAY_TIME*0.5)
            self.drag_mouse((new_x, new_y), (dest_x, new_y))
            time.sleep(DELAY_TIME*0.5)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def unselect_on_Canvas(self):
        try:
            if not self.exist(L.shape_designer.designer_window):
                logger("No designer window show up")
                raise Exception
            x,y = self.exist(L.shape_designer.canvas_object_shape).AXPosition
            size_w, size_h = self.exist(L.shape_designer.canvas_object_shape).AXSize
            new_x = x - (size_w*0.1)

            self.mouse.click(new_x,y)
            time.sleep(DELAY_TIME*0.5)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Shape Designer] Unselect title on Canvas')
    def unselect_title_on_Canvas(self):
        try:
            if not self.exist(L.shape_designer.designer_window):
                logger("No designer window show up")
                raise Exception("No designer window show up")
            x,y = self.exist(L.shape_designer.canvas_object_shape).AXPosition
            size_w, size_h = self.exist(L.shape_designer.canvas_object_shape).AXSize
            new_x = x - (size_w*0.1)

            self.mouse.click(new_x,y)
            time.sleep(DELAY_TIME*0.5)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
    @step('[Action][Shape Designer] Click center on Canvas')
    def click_center_on_Canvas(self):
        try:
            if not self.exist(L.shape_designer.designer_window):
                logger("No designer window show up")
                raise Exception("No designer window show up")

            x,y = self.exist(L.shape_designer.canvas_split_view).AXPosition
            size_w, size_h = self.exist(L.shape_designer.canvas_split_view).AXSize
            new_x = x + (size_w*0.5)
            new_y = y + (size_h * 0.5)
            self.mouse.click(new_x, new_y)
            time.sleep(DELAY_TIME*0.5)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Shape Designer] Edit title on Canvas')
    def edit_title_on_Canvas(self, strTitle):
        try:
            if not self.exist(L.shape_designer.designer_window):
                logger("No designer window show up")
                raise Exception("No designer window show up")

            x,y = self.exist(L.shape_designer.canvas_object_shape).AXPosition
            size_w, size_h = self.exist(L.shape_designer.canvas_object_shape).AXSize
            new_x = x + (size_w*0.5)
            new_y = y + (size_h * 0.5)
            self.mouse.click(new_x, new_y, times=2)
            time.sleep(DELAY_TIME*0.5)
            self.keyboard.send(strTitle)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def adjust_shape_on_Canvas_linear(self):
        try:
            if not self.exist(L.shape_designer.designer_window):
                logger("No designer window show up")
                raise Exception

            x,y = self.exist(L.shape_designer.canvas_object_shape).AXPosition
            size_w, size_h = self.exist(L.shape_designer.canvas_object_shape).AXSize
            new_x = x - (size_w*0.5)
            new_y = y + (size_w * 0.5)

            self.mouse.move(x, y)
            time.sleep(DELAY_TIME*0.5)
            self.drag_mouse((x, y), (new_x, new_y))
            time.sleep(DELAY_TIME*0.5)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def adjust_shape_on_Canvas_general(self):
        try:
            if not self.exist(L.shape_designer.designer_window):
                logger("No designer window show up")
                raise Exception

            x,y = self.exist(L.shape_designer.canvas_object_shape).AXPosition
            size_w, size_h = self.exist(L.shape_designer.canvas_object_shape).AXSize
            new_x = x + (size_w*0.5)
            new_y = y + size_h

            dest_y = y + (size_w + size_h)
            self.mouse.move(new_x, new_y)
            time.sleep(DELAY_TIME*0.5)
            self.drag_mouse((new_x, new_y), (new_x, dest_y))
            time.sleep(DELAY_TIME*0.5)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Shape Designer] Click [OK] button on shape designer window')
    def click_ok(self):
        return bool(self.exist(L.shape_designer.btn_ok).press())

    @step('[Action][Shape Designer] Click Cancel to leave Shape Designer')
    def click_cancel(self, option=None):
        try:
            options = [L.shape_designer.alert_dialog.btn_yes,
                       L.shape_designer.alert_dialog.btn_no,
                       L.shape_designer.alert_dialog.btn_cancel]
            self.click(L.shape_designer.btn_cancel)
            time.sleep(DELAY_TIME)
            if self.exist(L.shape_designer.alert_dialog.main) and option is not None:
                self.click(options[option])
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            return False(f'Exception occurs. log={e}')
        return True
    
    @step('[Action][Shape Designer] Click Save to save the template')
    def click_save_as(self):
        return bool(self.exist(L.shape_designer.btn_save_as).press())

    class SaveAs(Main_Page, BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        @step('[Action][Shape Designer][Save As] Set Name')
        def set_name(self, name):
            try:
                self.exist(L.shape_designer.save_template_dialog.edittext_template_name).sendKeys(name)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                return False(f'Exception occurs. log={e}')
            return True

        def get_name(self):
            return self.exist(L.shape_designer.save_template_dialog.edittext_template_name).AXValue

        def set_slider(self, value):
            try:
                el = self.exist(L.shape_designer.save_template_dialog.slider_mark_frame)
                el.AXValue = float(value)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                return False
            return True

        def get_slider(self):
            return self.exist(L.shape_designer.save_template_dialog.slider_mark_frame).AXValue

        def click_cancel(self):
            return bool(self.exist(L.shape_designer.save_template_dialog.btn_cancel).press())

        @step('[Action][Shape Designer][Save As] Click OK')
        def click_ok(self):
            return bool(self.exist(L.shape_designer.save_template_dialog.btn_ok).press())

    class Simple_Timeline(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.position = self.Position(*args, **kwargs)
            self.scale = self.Scale(*args, **kwargs)
            self.opacity = self.Opacity(*args, **kwargs)
            self.rotation = self.Rotation(*args, **kwargs)

        def click_zoom_in(self, times=1):
            try:
                if not self.exist(L.shape_designer.designer_window):
                    logger("No designer window show up")
                    raise Exception

                for x in range(times):
                    self.exist_click(L.shape_designer.simple_track.btn_zoom_in)
                    time.sleep(DELAY_TIME * 0.5)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def click_zoom_out(self, times=1):
            try:
                if not self.exist(L.shape_designer.designer_window):
                    logger("No designer window show up")
                    raise Exception

                for x in range(times):
                    self.exist_click(L.shape_designer.simple_track.btn_zoom_out)
                    time.sleep(DELAY_TIME * 0.5)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def drag_zoom_slider(self, value):
            if (value > 1) | (value < 0):
                logger('Invalid parameter')
                return False

            self.exist(L.shape_designer.simple_track.indicator_zoom).AXValue = value
            time.sleep(DELAY_TIME)
            return True

        def get_zoom_slider(self):
            try:
                if not self.exist(L.shape_designer.designer_window):
                    logger("No designer window show up")
                    raise Exception
                if not self.exist(L.shape_designer.simple_track.indicator_zoom):
                    raise Exception
                value = self.exist(L.shape_designer.simple_track.indicator_zoom).AXValue
                result = round(value, 3)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return result

        def drag_scroll_bar(self, value):
            if (value > 1) | (value < 0):
                logger('Invalid parameter')
                return False

            self.exist(L.shape_designer.simple_track.indicator_vertical).AXValue = value
            time.sleep(DELAY_TIME)
            return True

        class Position(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.right_click_menu = self.RightClickMenu(*args, **kwargs)

            def add_keyframe(self):
                try:
                    if not self.exist(L.shape_designer.designer_window):
                        logger("No designer window show up")
                        raise Exception
                    self.exist_click(L.shape_designer.simple_position_track.add_remove_current_keyframe)
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def click_previous_keyframe(self):
                try:
                    if not self.exist(L.shape_designer.designer_window):
                        logger("No designer window show up")
                        raise Exception
                    self.exist_click(L.shape_designer.simple_position_track.previous_keyframe)
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            @step('[Action][Shape Designer][Simple Timeline][Position] Click Next Keyframe')
            def click_next_keyframe(self):
                try:
                    if not self.exist(L.shape_designer.designer_window):
                        logger("No designer window show up")
                        raise Exception("No designer window show up")
                    self.exist_click(L.shape_designer.simple_position_track.next_keyframe)
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception(f'Exception occurs. log={e}')
                return True

            class RightClickMenu(BasePage):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.attribute_name = 'Position'

                def remove_keyframe(self, index):
                    locator_operation = L.shape_designer.simple_track.right_click_menu.remove_keyframe
                    return bool(_right_click_menu_keyframe(self, self.attribute_name, locator_operation, index))

                def remove_all_keyframe(self, index):
                    locator_operation = L.shape_designer.simple_track.right_click_menu.remove_all_keyframe
                    return bool(_right_click_menu_keyframe(self, self.attribute_name, locator_operation, index))

                def duplicate_prev_frame(self, index):
                    locator_operation = L.shape_designer.simple_track.right_click_menu.duplicate_prev_keyframe
                    return bool(_right_click_menu_keyframe(self, self.attribute_name, locator_operation, index))

                def duplicate_next_frame(self, index):
                    locator_operation = L.shape_designer.simple_track.right_click_menu.duplicate_next_keyframe
                    return bool(_right_click_menu_keyframe(self, self.attribute_name, locator_operation, index))

                def ease_in(self, index):
                    locator_operation = L.shape_designer.simple_track.right_click_menu.ease_in
                    return bool(_right_click_menu_keyframe(self, self.attribute_name, locator_operation, index))

                def ease_out(self, index):
                    locator_operation = L.shape_designer.simple_track.right_click_menu.ease_out
                    return bool(_right_click_menu_keyframe(self, self.attribute_name, locator_operation, index))

        class Scale(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.attribute_name = 'Scale'
                self.right_click_menu = self.RightClickMenu(*args, **kwargs)

            def add_keyframe(self):
                locator_operation = L.shape_designer.simple_position_track.add_remove_current_keyframe
                return bool(_control_keyframe(self, self.attribute_name, locator_operation))

            def click_previous_keyframe(self):
                locator_operation = L.shape_designer.simple_position_track.previous_keyframe
                return bool(_control_keyframe(self, self.attribute_name, locator_operation))

            def click_next_keyframe(self):
                locator_operation = L.shape_designer.simple_position_track.next_keyframe
                return bool(_control_keyframe(self, self.attribute_name, locator_operation))

            class RightClickMenu(BasePage):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.attribute_name = 'Scale'

                def remove_keyframe(self, index):
                    locator_operation = L.shape_designer.simple_track.right_click_menu.remove_keyframe
                    return bool(_right_click_menu_keyframe(self, self.attribute_name, locator_operation, index))

                def remove_all_keyframe(self, index):
                    locator_operation = L.shape_designer.simple_track.right_click_menu.remove_all_keyframe
                    return bool(_right_click_menu_keyframe(self, self.attribute_name, locator_operation, index))

                def duplicate_prev_frame(self, index):
                    locator_operation = L.shape_designer.simple_track.right_click_menu.duplicate_prev_keyframe
                    return bool(_right_click_menu_keyframe(self, self.attribute_name, locator_operation, index))

                def duplicate_next_frame(self, index):
                    locator_operation = L.shape_designer.simple_track.right_click_menu.duplicate_next_keyframe
                    return bool(_right_click_menu_keyframe(self, self.attribute_name, locator_operation, index))

                def ease_in(self, index):
                    locator_operation = L.shape_designer.simple_track.right_click_menu.ease_in
                    return bool(_right_click_menu_keyframe(self, self.attribute_name, locator_operation, index))

                def ease_out(self, index):
                    locator_operation = L.shape_designer.simple_track.right_click_menu.ease_out
                    return bool(_right_click_menu_keyframe(self, self.attribute_name, locator_operation, index))

        class Opacity(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.attribute_name = 'Opacity'
                self.right_click_menu = self.RightClickMenu(*args, **kwargs)

            def add_keyframe(self):
                locator_operation = L.shape_designer.simple_position_track.add_remove_current_keyframe
                return bool(_control_keyframe(self, self.attribute_name, locator_operation))

            def click_previous_keyframe(self):
                locator_operation = L.shape_designer.simple_position_track.previous_keyframe
                return bool(_control_keyframe(self, self.attribute_name, locator_operation))

            def click_next_keyframe(self):
                locator_operation = L.shape_designer.simple_position_track.next_keyframe
                return bool(_control_keyframe(self, self.attribute_name, locator_operation))

            class RightClickMenu(BasePage):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.attribute_name = 'Opacity'

                def remove_keyframe(self, index):
                    locator_operation = L.shape_designer.simple_track.right_click_menu.remove_keyframe
                    return bool(_right_click_menu_keyframe(self, self.attribute_name, locator_operation, index))

                def remove_all_keyframe(self, index):
                    locator_operation = L.shape_designer.simple_track.right_click_menu.remove_all_keyframe
                    return bool(_right_click_menu_keyframe(self, self.attribute_name, locator_operation, index))

                def duplicate_prev_frame(self, index):
                    locator_operation = L.shape_designer.simple_track.right_click_menu.duplicate_prev_keyframe
                    return bool(_right_click_menu_keyframe(self, self.attribute_name, locator_operation, index))

                def duplicate_next_frame(self, index):
                    locator_operation = L.shape_designer.simple_track.right_click_menu.duplicate_next_keyframe
                    return bool(_right_click_menu_keyframe(self, self.attribute_name, locator_operation, index))

                def ease_in(self, index):
                    locator_operation = L.shape_designer.simple_track.right_click_menu.ease_in
                    return bool(_right_click_menu_keyframe(self, self.attribute_name, locator_operation, index))

                def ease_out(self, index):
                    locator_operation = L.shape_designer.simple_track.right_click_menu.ease_out
                    return bool(_right_click_menu_keyframe(self, self.attribute_name, locator_operation, index))

        class Rotation(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.attribute_name = 'Rotation'
                self.right_click_menu = self.RightClickMenu(*args, **kwargs)

            def add_keyframe(self):
                locator_operation = L.shape_designer.simple_position_track.add_remove_current_keyframe
                return bool(_control_keyframe(self, self.attribute_name, locator_operation))

            def click_previous_keyframe(self):
                locator_operation = L.shape_designer.simple_position_track.previous_keyframe
                return bool(_control_keyframe(self, self.attribute_name, locator_operation))

            def click_next_keyframe(self):
                locator_operation = L.shape_designer.simple_position_track.next_keyframe
                return bool(_control_keyframe(self, self.attribute_name, locator_operation))

            class RightClickMenu(BasePage):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.attribute_name = 'Rotation'

                def remove_keyframe(self, index):
                    locator_operation = L.shape_designer.simple_track.right_click_menu.remove_keyframe
                    return bool(_right_click_menu_keyframe(self, self.attribute_name, locator_operation, index))

                def remove_all_keyframe(self, index):
                    locator_operation = L.shape_designer.simple_track.right_click_menu.remove_all_keyframe
                    return bool(_right_click_menu_keyframe(self, self.attribute_name, locator_operation, index))

                def duplicate_prev_frame(self, index):
                    locator_operation = L.shape_designer.simple_track.right_click_menu.duplicate_prev_keyframe
                    return bool(_right_click_menu_keyframe(self, self.attribute_name, locator_operation, index))

                def duplicate_next_frame(self, index):
                    locator_operation = L.shape_designer.simple_track.right_click_menu.duplicate_next_keyframe
                    return bool(_right_click_menu_keyframe(self, self.attribute_name, locator_operation, index))

                def ease_in(self, index):
                    locator_operation = L.shape_designer.simple_track.right_click_menu.ease_in
                    return bool(_right_click_menu_keyframe(self, self.attribute_name, locator_operation, index))

                def ease_out(self, index):
                    locator_operation = L.shape_designer.simple_track.right_click_menu.ease_out
                    return bool(_right_click_menu_keyframe(self, self.attribute_name, locator_operation, index))


# Keyframe session
class Keyframe(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object_settings = ObjectSetting(*args, **kwargs)


class ObjectSetting(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.position = Position(args[0], L.shape_designer.keyframe.object_settings.position.ke_combo)
        self.scale = Scale(args[0], L.shape_designer.keyframe.object_settings.scale.ke_combo)
        self.opacity = Opacity(args[0], L.shape_designer.keyframe.object_settings.opacity.ke_combo)
        self.rotation = Rotation(args[0], L.shape_designer.keyframe.object_settings.rotation.ke_combo)

    def unfold_menu(self, unfold=True):
        elem = self.find(L.shape_designer.keyframe.object_settings.disclosure_triangle)
        elem.AXValue ^ unfold and elem.press()
        return True

    def get_unfold_status(self):
        elem = self.find(L.shape_designer.keyframe.object_settings.disclosure_triangle)
        return bool(elem.AXValue)


class Position(KEComboSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x = AdjustSet(self, L.shape_designer.keyframe.object_settings.position.x.group)
        self.y = AdjustSet(self, L.shape_designer.keyframe.object_settings.position.y.group)


class Scale(KEComboSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.w = AdjustSet(self, L.shape_designer.keyframe.object_settings.scale.width.group)
        self.h = AdjustSet(self, L.shape_designer.keyframe.object_settings.scale.height.group)
    
    @step('[Action][Shape Designer][Keyframe][Object Setting][Scale] Set Maintain Aspect Ratio Checkbox')
    def set_aspect_ratio_chx(self, value=1):
        target = self.exist(L.shape_designer.keyframe.object_settings.scale.maintain_aspect_ratio)
        int(target.AXValue) ^ value and target.press()
        return True
    
    @step('[Action][Shape Designer][Keyframe][Object Setting][Scale] Get Maintain Aspect Ratio Checkbox')
    def get_aspect_ratio_chx(self):
        target = self.exist(L.shape_designer.keyframe.object_settings.scale.maintain_aspect_ratio)
        return bool(target.AXValue)


class Opacity(KEComboSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = AdjustSet(self, L.shape_designer.keyframe.object_settings.opacity.value.group)


class Rotation(KEComboSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = AdjustSet(self, L.shape_designer.keyframe.object_settings.rotation.value.group)
