import time, datetime, os, copy

from .base_page import BasePage
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
from .locator import locator as L
from reportportal_client import step

OPERATION_DELAY = 1 # sec


def close_chrome_page(obj):
    try:
        logger('enter close_chrome_page')
        obj.driver.get_top("com.google.Chrome").windows()[0].findAllR(AXSubrole="AXCloseButton")[0].press()
        time.sleep(OPERATION_DELAY*2)
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        raise Exception
    return True


def combobox_select_by_index(obj, el_combobox, index): # index: 1-based, e.g. 1, 2, ...
    try:
        logger(f'{index=}')
        obj.el_click(el_combobox)
        time.sleep(OPERATION_DELAY)
        el_menu = obj.exist(L.produce.combobox_menu.menu)
        els_menu_item = obj.exist_elements(L.produce.combobox_menu.menu_item, el_menu)
        select_option_text = obj.exist(L.produce.combobox_menu.menu_item_text, els_menu_item[index - 1]).AXValue
        logger(f'current select={select_option_text}')
        obj.el_click(els_menu_item[index - 1])
        time.sleep(OPERATION_DELAY * 0.5)
        # verify the result
        if el_combobox.AXTitle.replace('...', '') not in select_option_text:
            logger(f'Fail to verify selected combobox item. {el_combobox.AXTitle}')
            raise Exception
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        raise Exception
    return True


def set_category_fold_enable(obj, category, value): # category: fix, clip, volume; value: 0(close), 1(open)
    try:
        locator = L.keyframe_room.unit_setting_category.copy()
        locator[1]['get_all'] = True
        locator.append({'AXTitle': category})
        el_item = obj.exist(locator)
        el_outline_row = el_item.AXParent.AXParent  # outline_row
        el_triangle = obj.exist(L.keyframe_room.disclosure_triangle, el_outline_row)
        if not el_triangle.AXValue == value:
            el_triangle.press()
            time.sleep(OPERATION_DELAY)
        time.sleep(OPERATION_DELAY*0.5)
    except Exception as e:
        logger(f'Exception occurs: {e}')
        raise Exception
    return True


def get_category_fold_status(obj, category):
    try:
        locator = L.keyframe_room.unit_setting_category.copy()
        locator[1]['get_all'] = True
        locator.append({'AXTitle': category})
        el_item = obj.exist(locator)
        el_outline_row = el_item.AXParent.AXParent  # outline_row
        el_triangle = obj.exist(L.keyframe_room.disclosure_triangle, el_outline_row)
    except Exception as e:
        logger(f'Exception occurs: {e}')
        raise Exception
    return el_triangle.AXValue


def category_select_right_click_menu(obj, category, menu_item):
    try:
        locator = L.keyframe_room.unit_setting_category.copy()
        locator[1]['get_all'] = True
        locator.append({'AXTitle': category})
        el_item = obj.exist(locator)
        el_outline_row = el_item.AXParent.AXParent  # outline_row
        obj.mouse.move(*el_outline_row.center)
        # right click menu
        obj.right_click()
        obj.select_right_click_menu(menu_item)
        time.sleep(OPERATION_DELAY)
        # if menu_item is Paste
        if menu_item == 'Paste':
            obj.exist_click(L.base.confirm_dialog.btn_ok)
    except Exception as e:
        logger(f'Exception occurs: {e}')
        raise Exception
    return True


def select_keyframe_node_by_outline_row(obj, index_outline_row=0, index_node=0):
    try:
        locator_outline_row = L.keyframe_room.unit_keyframe_outline_row.copy()
        locator_outline_row[1]['get_all'] = True
        els_outline_row = obj.exist(locator_outline_row)
        locator_node = L.keyframe_room.unit_keyframe_node.copy()
        locator_node['index'] = index_node
        el_node = obj.exist(locator_node, els_outline_row[index_outline_row])
        if index_node == 0:
            obj.el_click(el_node, 2, 0) # special handing for first node
        else:
            obj.el_click(el_node)
    except Exception as e:
        logger(f'Exception occurs: {e}')
        return False
    return True

# attribute_type - if the located string type is AXTitle/checkbox, should set it to non-empty
# e.g. Fix Enhance > Lighting Adjustment > Extreme backlight
def get_outline_row_by_attribute(obj, attribute_name, category_name='', attribute_type=''): # fix for v3310 fix_enhance.audio_denoise.degree
    try:
        index_row = -1
        el_row = -1
        index_category_row = -1
        locator_outline_row = L.keyframe_room.unit_setting_category.copy()
        locator_outline_row[1]['get_all'] = True
        el_outline_row = obj.exist(locator_outline_row)

        # get category_name row index first if specified
        pos_outline_row_category = -1
        pos_outline_row = -1
        if category_name != '':
            locator_outline_row_category = L.keyframe_room.unit_setting_category.copy()
            locator_outline_row_category.append({'AXTitle': category_name})
            pos_outline_row_category = obj.exist(locator_outline_row_category).AXParent.AXParent.AXPosition

        if attribute_type == '':
            locator_attribute_name = L.keyframe_room.unit_attribute_name.copy()
            locator_attribute_name['AXValue'] = attribute_name
        else:
            locator_attribute_name = L.keyframe_room.unit_attribute_name_checkbox.copy()
            locator_attribute_name['AXTitle'] = attribute_name
        if category_name != '':
            locator_attribute_name['get_all'] = True
            locator_outline_row.append(locator_attribute_name)
            els_target = obj.exist(locator_outline_row)
            for el_target in els_target:
                if el_target.AXPosition[1] > pos_outline_row_category[1]:
                    pos_outline_row = el_target.AXParent.AXParent.AXPosition
                    break
        else:
            locator_outline_row.append(locator_attribute_name)
            el_target = obj.exist(locator_outline_row)
            pos_outline_row = el_target.AXParent.AXParent.AXPosition
        for idx_row in range(len(el_outline_row)):
            if el_outline_row[idx_row].AXPosition == pos_outline_row:
                index_row = idx_row
                el_row = el_outline_row[idx_row]
                break
    except Exception as e:
        logger(f'Exception occurs: {e}')
        return -1
    return index_row, el_row


def get_outline_row_by_category(obj, category_name): # get the outline row of category button
    try:
        index_row = -1
        el_row = -1
        locator_outline_row = L.keyframe_room.unit_setting_category.copy()
        locator_outline_row[1]['get_all'] = True
        el_outline_row = obj.exist(locator_outline_row)
        locator_category_name = L.keyframe_room.unit_category_name.copy()
        locator_category_name['AXTitle'] = category_name
        locator_outline_row.append(locator_category_name)
        el_target = obj.exist(locator_outline_row)
        pos_outline_row = el_target.AXParent.AXParent.AXPosition
        for idx_row in range(len(el_outline_row)):
            if el_outline_row[idx_row].AXPosition == pos_outline_row:
                index_row = idx_row
                el_row = el_outline_row[idx_row]
                break
    except Exception as e:
        logger(f'Exception occurs: {e}')
        return -1
    return index_row, el_row


# step 1: select specified keyframe node if index_keyframe_node is not equal to -1
# step 2: set the edittext value
# locator_group, index_group: the group of edittext and stepper (for Clip Attributes category using)
def set_attribute_edittext_value(obj, attribute_name, value, index_keyframe_node=-1, locator_group=None, index_group=-1, category_name=''):  # 0 - 100
    try:
        # select keyframe node if specified index > 0
        index_row, el_row = get_outline_row_by_attribute(obj, attribute_name, category_name)
        if not index_keyframe_node == -1:
            select_keyframe_node_by_outline_row(obj, index_row, index_keyframe_node)
            time.sleep(OPERATION_DELAY * 2)
        locator_edittext = L.keyframe_room.unit_edittext_slider_value.copy()
        if not locator_group: # for one edittext in one outline row
            el_edittext_value = obj.exist(locator_edittext, el_row)
        else:
            target_group = locator_group.copy()
            target_group['index'] = index_group
            el_group = obj.exist(target_group, el_row)
            el_edittext_value = obj.exist(locator_edittext, el_group)
        obj.el_click(el_edittext_value)
        time.sleep(OPERATION_DELAY * 0.3)
        el_edittext_value.AXValue = str(value)
        time.sleep(OPERATION_DELAY * 0.3)
        obj.keyboard.enter()
        time.sleep(OPERATION_DELAY * 0.5)
    except Exception as e:
        logger(f'Exception occurs: {e}')
        return -1
    return True

# step 1: select specified keyframe node if index_keyframe_node is not equal to -1
# step 2: get the edittext value
# locator_group, index_group: the group of edittext and stepper (for Clip Attributes category using)
def get_attribute_edittext_value(obj, attribute_name, index_keyframe_node=-1, locator_group=None, index_group=-1, category_name=''):
    try:
        value = -1
        # select keyframe node if specified index > 0
        index_row, el_row = get_outline_row_by_attribute(obj, attribute_name, category_name)
        if not index_keyframe_node == -1:
            select_keyframe_node_by_outline_row(obj, index_row, index_keyframe_node)
            time.sleep(OPERATION_DELAY * 2)
        # el_edittext_value = obj.exist(L.keyframe_room.unit_edittext_slider_value, el_row)
        locator_edittext = L.keyframe_room.unit_edittext_slider_value.copy()
        if not locator_group:  # for one edittext in one outline row
            el_edittext_value = obj.exist(locator_edittext, el_row)
        else:
            target_group = locator_group.copy()
            target_group['index'] = index_group
            el_group = obj.exist(target_group, el_row)
            el_edittext_value = obj.exist(locator_edittext, el_group)
        value = el_edittext_value.AXValue
    except Exception as e:
        logger(f'Exception occurs: {e}')
        return -1
    return value

# step 1: select specified keyframe node if index_keyframe_node is not equal to -1
# step 2: set the edittext value of slider
# locator_slider: the specified locator of slider (for Clip Attributes category using)
def set_attribute_slider_value(obj, attribute_name, value, index_keyframe_node=-1, locator_slider=None, index_slider=-1, category_name=''):  # 0 - 1
    try:
        # select keyframe node if specified index > 0
        index_row, el_row = get_outline_row_by_attribute(obj, attribute_name, category_name)
        print(f'set value: {index_row=}, {el_row=}')
        if not index_keyframe_node == -1:
            select_keyframe_node_by_outline_row(obj, index_row, index_keyframe_node)
            time.sleep(OPERATION_DELAY * 2)
        if not locator_slider:
            if index_slider == -1:
                el_slider = obj.exist(L.keyframe_room.unit_slider, el_row)
            else:
                locator = L.keyframe_room.unit_slider.copy()
                locator['get_all'] = True
                el_slider = obj.exist(locator, el_row)[index_slider]
        else:
            el_slider = obj.exist(locator_slider, el_row)
        el_slider.AXValue = value
        time.sleep(OPERATION_DELAY)
    except Exception as e:
        logger(f'Exception occurs: {e}')
        return -1
    return True

# step 1: click reset keyframe
def click_attribute_reset_keyframe(obj, attribute_name, category_name='', attribute_type=''):
    try:
        index_row, el_row = get_outline_row_by_attribute(obj, attribute_name, category_name, attribute_type)
        print(f'set value: {index_row=}, {el_row=}')
        el_button = obj.exist(L.keyframe_room.btn_reset_keyframe, el_row)
        obj.el_click(el_button)
        time.sleep(OPERATION_DELAY)
    except Exception as e:
        logger(f'Exception occurs: {e}')
        return False
    return True

# step 1: select specified keyframe node if index_keyframe_node is not equal to -1
# step 2: click next keyframe
def click_attribute_next_keyframe(obj, attribute_name, index_keyframe_node=-1, category_name='', attribute_type=''):
    try:
        # select keyframe node if specified index is not -1
        index_row, el_row = get_outline_row_by_attribute(obj, attribute_name, category_name, attribute_type)
        print(f'set value: {index_row=}, {el_row=}')
        if not index_keyframe_node == -1:
            select_keyframe_node_by_outline_row(obj, index_row, index_keyframe_node)
            time.sleep(OPERATION_DELAY * 2)
        el_button = obj.exist(L.keyframe_room.btn_next_keyframe, el_row)
        obj.el_click(el_button)
        time.sleep(OPERATION_DELAY * 0.5)
        value = el_button.AXEnabled
    except Exception as e:
        logger(f'Exception occurs: {e}')
        return False
    return value


# step 1: select specified keyframe node if index_keyframe_node is not equal to -1
# step 2: click previous keyframe
def click_attribute_previous_keyframe(obj, attribute_name, index_keyframe_node=-1, category_name='', attribute_type=''):
    try:
        # select keyframe node if specified index is not -1
        index_row, el_row = get_outline_row_by_attribute(obj, attribute_name, category_name, attribute_type)
        print(f'set value: {index_row=}, {el_row=}')
        if not index_keyframe_node == -1:
            select_keyframe_node_by_outline_row(obj, index_row, index_keyframe_node)
            time.sleep(OPERATION_DELAY * 2)
        el_button = obj.exist(L.keyframe_room.btn_previous_keyframe, el_row)
        obj.el_click(el_button)
        time.sleep(OPERATION_DELAY * 0.5)
        value = el_button.AXEnabled
    except Exception as e:
        logger(f'Exception occurs: {e}')
        return False
    return value


# step 1: select specified keyframe node if index_keyframe_node is not equal to -1
# step 2: click add/remove keyframe
def click_attribute_add_remove_keyframe(obj, attribute_name, index_keyframe_node=-1, category_name='', attribute_type=''):
    try:
        # select keyframe node if specified index is not -1
        index_row, el_row = get_outline_row_by_attribute(obj, attribute_name, category_name, attribute_type)
        # print(f'set value: {index_row=}, {el_row=}')
        if not index_keyframe_node == -1:
            select_keyframe_node_by_outline_row(obj, index_row, index_keyframe_node)
            time.sleep(OPERATION_DELAY * 2)
        el_button = obj.exist(L.keyframe_room.btn_add_remove_keyframe, el_row)
        obj.el_click(el_button)
        time.sleep(OPERATION_DELAY * 0.5)
        value = el_button.AXEnabled
    except Exception as e:
        logger(f'Exception occurs: {e}')
        return False
    return value


# step 1: select specified keyframe node if index_keyframe_node is not equal to -1
# step 2: click stepper up/ down
# locator_group, index_group: the group of edittext and stepper (for Clip Attributes category using)
def click_attribute_stepper(obj, attribute_name, option='up', times=1, index_keyframe_node=-1, locator_group=None, index_group=-1, category_name=''):
    try:
        # select keyframe node if specified index is not -1
        index_row, el_row = get_outline_row_by_attribute(obj, attribute_name, category_name)
        print(f'set value: {index_row=}, {el_row=}')
        if not index_keyframe_node == -1:
            select_keyframe_node_by_outline_row(obj, index_row, index_keyframe_node)
            time.sleep(OPERATION_DELAY * 2)
        locator_stepper = eval(f'L.keyframe_room.btn_stepper_{option}')
        if not locator_group: # for one stepper_up/ stepper_down in one outline row
            el_button = obj.exist(locator_stepper, el_row)
        else:
            target_group = locator_group.copy()
            target_group['index'] = index_group
            el_group = obj.exist(target_group, el_row)
            el_button = obj.exist(locator_stepper, el_group)
        for cnt in range(times):
            obj.el_click(el_button)
            time.sleep(OPERATION_DELAY * 0.5)
    except Exception as e:
        logger(f'Exception occurs: {e}')
        return False
    return True


# step 1: select specified keyframe node if index_keyframe_node is not equal to -1
# step 2: select the combobox option
def select_attribute_combobox_option(obj, attribute_name, index_option=1, index_keyframe_node=-1):
    try:
        target_dict = {'Noise type:': 'noise_type', 'Opacity': 'blending_mode'}
        # select keyframe node if specified index is not -1
        index_row, el_row = get_outline_row_by_attribute(obj, attribute_name)
        print(f'set value: {index_row=}, {el_row=}')
        if not index_keyframe_node == -1:
            select_keyframe_node_by_outline_row(obj, index_row, index_keyframe_node)
            time.sleep(OPERATION_DELAY * 2)
        # select combobox option
        el_combobox = obj.exist(eval(f'L.keyframe_room.btn_{target_dict[attribute_name]}_combobox'), el_row)
        combobox_select_by_index(obj, el_combobox, index_option)
        time.sleep(OPERATION_DELAY * 0.5)
    except Exception as e:
        logger(f'Exception occurs: {e}')
        return False
    return True

# step 1: select specified keyframe node if index_keyframe_node is not equal to -1
# step 2: get the combobox option value
def get_attribute_combobox_option(obj, attribute_name, index_keyframe_node=-1):
    try:
        target_dict = {'Noise type:': 'noise_type', 'Opacity': 'blending_mode'}
        # select keyframe node if specified index is not -1
        index_row, el_row = get_outline_row_by_attribute(obj, attribute_name)
        print(f'set value: {index_row=}, {el_row=}')
        if not index_keyframe_node == -1:
            select_keyframe_node_by_outline_row(obj, index_row, index_keyframe_node)
            time.sleep(OPERATION_DELAY * 2)
        # select combobox option
        el_combobox = obj.exist(eval(f'L.keyframe_room.btn_{target_dict[attribute_name]}_combobox'), el_row)
        value = el_combobox.AXTitle
        time.sleep(OPERATION_DELAY * 0.5)
    except Exception as e:
        logger(f'Exception occurs: {e}')
        return False
    return value


# step 1: select specified keyframe node if index_keyframe_node is not equal to -1
# step 2: set checkbox checked/ unchecked
# locator_checkbox: the locator of checkbox (for Clip Attributes category using)
# set_status: 1(checked), 0(unchecked)
def set_attribute_checkbox(obj, attribute_name, locator_checkbox, set_status=1, index_keyframe_node=-1, attribute_type=''):
    try:
        # select keyframe node if specified index is not -1
        index_row, el_row = get_outline_row_by_attribute(obj, attribute_name, '', attribute_type)
        print(f'set value: {index_row=}, {el_row=}')
        if not index_keyframe_node == -1:
            select_keyframe_node_by_outline_row(obj, index_row, index_keyframe_node)
            time.sleep(OPERATION_DELAY * 2)
        el_button = obj.exist(locator_checkbox, el_row)
        if not el_button.AXEnabled:
            logger('[Error]The target checkbox is not enabled.')
            raise Exception
        if not el_button.AXValue == set_status:
            obj.el_click(el_button)
            time.sleep(OPERATION_DELAY * 0.5)
    except Exception as e:
        logger(f'Exception occurs: {e}')
        return False
    return True


def get_attribute_checkbox(obj, attribute_name, locator_checkbox, index_keyframe_node=-1, attribute_type=''):
    try:
        # select keyframe node if specified index is not -1
        index_row, el_row = get_outline_row_by_attribute(obj, attribute_name, '', attribute_type)
        print(f'set value: {index_row=}, {el_row=}')
        if not index_keyframe_node == -1:
            select_keyframe_node_by_outline_row(obj, index_row, index_keyframe_node)
            time.sleep(OPERATION_DELAY * 2)
        el_button = obj.exist(locator_checkbox, el_row)
        if not el_button.AXEnabled:
            logger('[Error]The target checkbox is not enabled.')
            raise Exception
    except Exception as e:
        logger(f'Exception occurs: {e}')
        return -1
    return bool(el_button.AXValue)


def drag_scroll_bar(obj, value):
    try:
        logger(f'input {value=}')
        if value < 0:
            value = 0
            logger(f'transfer value to {value}')
        elif value > 1:
            value = 1
            logger(f'transfer value to {value}')
        else:
            pass
        locator = L.keyframe_room.scrollbar_vertical
        el_scrollbar = obj.exist(locator)
        el_scrollbar.AXValue = value
        time.sleep(OPERATION_DELAY)
        #verify
        # logger(f'Current Scrollbar value: {el_scrollbar.AXValue}')
        if not el_scrollbar.AXValue == value:
            logger('Fail to verify scroll bar value')
            raise Exception
    except Exception as e:
        logger(f'Exception occurs: {e}')
        return False
    return True


def get_scroll_bar_value(obj):
    try:
        locator = L.keyframe_room.scrollbar_vertical
        el_scrollbar = obj.exist(locator)
        value = el_scrollbar.AXValue
    except Exception as e:
        logger(f'Exception occurs: {e}')
        return False
    return value


def set_outline_row_visible(obj, el_row):
    try:
        # calculate the slider position
        row_pos = el_row.AXPosition
        row_size = el_row.AXSize
        el_frame = obj.exist(L.keyframe_room.frame_setting_panel_scroll_area)
        # print(f'Frame Info.: {el_frame.AXPosition=}, {el_frame.AXSize=}')
        table_frame_size = el_frame.AXSize
        table_frame_pos = el_frame.AXPosition
        percentage_scroll_y = 0
        is_drag_scroll_bar = 0
        if row_pos[1] > table_frame_pos[1]+table_frame_size[1] or \
            (row_pos[1] + row_size[1]) > (table_frame_pos[1] + table_frame_size[1]): # target or target bottom-side is lower than frame bottom-side
            table_detail_size = obj.exist(L.keyframe_room.frame_setting_panel).AXSize
            total_offset_length = table_detail_size[1] - table_frame_size[1] # <<
            offset_row_move_to_frame_inside = (row_size[1] + row_pos[1]) - (table_frame_pos[1] + table_frame_size[1])
            if offset_row_move_to_frame_inside < total_offset_length:
                current_percentage_scroll_y = get_scroll_bar_value(obj)  # if current position is not at 0
                percentage_scroll_y = (offset_row_move_to_frame_inside / total_offset_length) + current_percentage_scroll_y
            else:
                percentage_scroll_y = 1
            is_drag_scroll_bar = 1
        elif row_pos[1] < table_frame_pos[1]: # target is upper than frame up-side
            table_detail_size = obj.exist(L.keyframe_room.frame_setting_panel).AXSize
            total_offset_length = table_detail_size[1] - table_frame_size[1]  # <<
            offset_row_move_to_frame_inside = table_frame_pos[1] - row_pos[1]
            if offset_row_move_to_frame_inside < total_offset_length:
                current_percentage_scroll_y = get_scroll_bar_value(obj)  # if current position is not at 0
                percentage_scroll_y = current_percentage_scroll_y - (offset_row_move_to_frame_inside / total_offset_length)
            else:
                percentage_scroll_y = 1
            is_drag_scroll_bar = 1
        else:
            pass

        if is_drag_scroll_bar:
            # print(f'{percentage_scroll_y=}')
            if percentage_scroll_y < 0:
                percentage_scroll_y = 0
            drag_scroll_bar(obj, percentage_scroll_y)
            time.sleep(OPERATION_DELAY * 2)
        # ----------------------------
    except Exception as e:
        logger(f'Exception occurs: {e}')
        return False
    return True

def set_attribute_visible(obj, attribute_name, category_name='', attribute_type=''):
    try:
        # get attribute row information
        index_row, el_row = get_outline_row_by_attribute(obj, attribute_name, category_name, attribute_type)
        # print(f'Attribute Info.: {index_row=}, {el_row.AXPosition=}, {el_row.AXSize=}')
        set_outline_row_visible(obj, el_row)
    except Exception as e:
        logger(f'Exception occurs: {e}')
        return False
    return True

def set_category_visible(obj, category_name):
    try:
        # get attribute row information
        index_row, el_row = get_outline_row_by_category(obj, category_name)
        # print(f'Attribute Info.: {index_row=}, {el_row.AXPosition=}, {el_row.AXSize=}')
        set_outline_row_visible(obj, el_row)
    except Exception as e:
        logger(f'Exception occurs: {e}')
        return False
    return True


class KeyFrame_Page(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fix_enhance = self.Fix_Enhance(*args, **kwargs)
        self.clip_attributes = self.Clip_Attributes(*args, **kwargs)
        self.volume = self.Volume(*args, **kwargs)
        self.effect = self.Effect(*args, **kwargs)

    def click_close(self):
        return self.exist_click(L.keyframe_room.btn_close)

    def is_enter_keyframe_settings(self):
        return self.is_exist(L.keyframe_room.btn_close, None, 3)

    @step('[Action][KeyFrame] Drag scroll bar')
    def drag_scroll_bar(self, value):
        try:
            logger(f'input {value=}')
            if value < 0:
                value = 0
                logger(f'transfer value to {value}')
            elif value > 1:
                value = 1
                logger(f'transfer value to {value}')
            else:
                pass
            locator = L.keyframe_room.scrollbar_vertical
            el_scrollbar = self.exist(locator)
            el_scrollbar.AXValue = value
            time.sleep(OPERATION_DELAY)
            # verify
            # logger(f'Current Scrollbar value: {el_scrollbar.AXValue}')
            if not el_scrollbar.AXValue == value:
                logger('Fail to verify scroll bar value')
                raise Exception('Fail to verify scroll bar value')
        except Exception as e:
            logger(f'Exception occurs: {e}')
            raise Exception(f'Exception occurs: {e}')
        return True

    def select_keyframe_node_by_outline_row(self, index_outline_row=0, index_node=0):
        try:
            locator_outline_row = L.keyframe_room.unit_keyframe_outline_row.copy()
            locator_outline_row[1]['get_all'] = True
            els_outline_row = self.exist(locator_outline_row)
            locator_node = L.keyframe_room.unit_keyframe_node.copy()
            locator_node['index'] = index_node
            el_node = self.exist(locator_node, els_outline_row[index_outline_row])
            if index_node == 0:
                self.el_click(el_node, 2, 0)  # special handing for first node
            else:
                self.el_click(el_node)
        except Exception as e:
            logger(f'Exception occurs: {e}')
            return False
        return True

    def get_outline_row_by_attribute(self, attribute_name):
        try:
            index_row = -1
            el_row = -1
            locator_outline_row = L.keyframe_room.unit_setting_category.copy()
            locator_outline_row[1]['get_all'] = True
            el_outline_row = self.exist(locator_outline_row)
            locator_attribute_name = L.keyframe_room.unit_attribute_name.copy()
            locator_attribute_name['AXValue'] = attribute_name
            locator_outline_row.append(locator_attribute_name)
            el_target = self.exist(locator_outline_row)
            pos_outline_row = el_target.AXParent.AXParent.AXPosition
            # print(f'{pos_outline_row=}')
            for idx_row in range(len(el_outline_row)):
                if el_outline_row[idx_row].AXPosition == pos_outline_row:
                    index_row = idx_row
                    el_row = el_outline_row[idx_row]
                    break
        except Exception as e:
            logger(f'Exception occurs: {e}')
            return -1
        return index_row, el_row

    def get_category_fold_status(self, category):
        try:
            locator = L.keyframe_room.unit_setting_category.copy()
            locator[1]['get_all'] = True
            locator.append({'AXTitle': category})
            el_item = self.exist(locator)
            el_outline_row = el_item.AXParent.AXParent  # outline_row
            el_triangle = self.exist(L.keyframe_room.disclosure_triangle, el_outline_row)
        except Exception as e:
            logger(f'Exception occurs: {e}')
            raise Exception
        return el_triangle.AXValue

    def set_category_fold_enable(self, category, value):  # category: fix, clip, volume; value: 0(close), 1(open)
        try:
            locator = L.keyframe_room.unit_setting_category.copy()
            locator[1]['get_all'] = True
            locator.append({'AXTitle': category})
            el_item = self.exist(locator)
            el_outline_row = el_item.AXParent.AXParent  # outline_row
            el_triangle = self.exist(L.keyframe_room.disclosure_triangle, el_outline_row)
            if not el_triangle.AXValue == value:
                el_triangle.press()
                time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs: {e}')
            raise Exception
        return True

    def set_outline_row_visible(self, el_row):
        try:
            # calculate the slider position
            row_pos = el_row.AXPosition
            row_size = el_row.AXSize
            el_frame = self.exist(L.keyframe_room.frame_setting_panel_scroll_area)
            print(f'Frame Info.: {el_frame.AXPosition=}, {el_frame.AXSize=}')
            table_frame_size = el_frame.AXSize
            table_frame_pos = el_frame.AXPosition
            percentage_scroll_y = 0
            is_drag_scroll_bar = 0
            if row_pos[1] > table_frame_pos[1]+table_frame_size[1] or \
                (row_pos[1] + row_size[1]) > (table_frame_pos[1] + table_frame_size[1]): # target or target bottom-side is lower than frame bottom-side
                table_detail_size = self.exist(L.keyframe_room.frame_setting_panel).AXSize
                total_offset_length = table_detail_size[1] - table_frame_size[1] # <<
                offset_row_move_to_frame_inside = (row_size[1] + row_pos[1]) - (table_frame_pos[1] + table_frame_size[1])
                if offset_row_move_to_frame_inside < total_offset_length:
                    current_percentage_scroll_y = get_scroll_bar_value(self)  # if current position is not at 0
                    percentage_scroll_y = (offset_row_move_to_frame_inside / total_offset_length) + current_percentage_scroll_y
                else:
                    percentage_scroll_y = 1
                is_drag_scroll_bar = 1
            elif row_pos[1] < table_frame_pos[1]: # target is upper than frame up-side
                table_detail_size = self.exist(L.keyframe_room.frame_setting_panel).AXSize
                total_offset_length = table_detail_size[1] - table_frame_size[1]  # <<
                offset_row_move_to_frame_inside = table_frame_pos[1] - row_pos[1]
                if offset_row_move_to_frame_inside < total_offset_length:
                    current_percentage_scroll_y = get_scroll_bar_value(self)  # if current position is not at 0
                    percentage_scroll_y = current_percentage_scroll_y - (offset_row_move_to_frame_inside / total_offset_length)
                else:
                    percentage_scroll_y = 1
                is_drag_scroll_bar = 1
            else:
                print('no need to drag scroll bar')

            if is_drag_scroll_bar:
                print(f'{percentage_scroll_y=}')
                drag_scroll_bar(self, percentage_scroll_y)
                time.sleep(OPERATION_DELAY * 2)
            # ----------------------------
        except Exception as e:
            logger(f'Exception occurs: {e}')
            return False
        return True

    def set_attribute_visible(self, attribute_name):
        try:
            # get attribute row information
            index_row, el_row = get_outline_row_by_attribute(self, attribute_name)
            print(f'Attribute Info.: {index_row=}, {el_row.AXPosition=}, {el_row.AXSize=}')
            set_outline_row_visible(self, el_row)
        except Exception as e:
            logger(f'Exception occurs: {e}')
            return False
        return True

    def set_category_visible(self, category_name):
        try:
            # get attribute row information
            index_row, el_row = get_outline_row_by_category(self, category_name)
            print(f'Attribute Info.: {index_row=}, {el_row.AXPosition=}, {el_row.AXSize=}')
            set_outline_row_visible(self, el_row)
        except Exception as e:
            logger(f'Exception occurs: {e}')
            return False
        return True

    def get_left_panel_duration(self):
        value = -1
        try:
            locator_text = L.keyframe_room.txt_top_left_duration.copy()
            locator_text[1]['get_all'] = True
            els_static_text = self.exist(locator_text)
            for el_text in els_static_text:
                if len(el_text.AXValue.split(';')) == 4:
                    value = el_text.AXValue
                    break
        except Exception as e:
            logger(f'Exception occurs: {e}')
            return False
        return value


    class Fix_Enhance(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.category_name = 'Fix*'
            self.lighting_adjustment = self.Lighting_Adjustment(self.category_name, *args, **kwargs)
            self.video_denoise = self.Video_Denoise(self.category_name, *args, **kwargs)
            self.audio_denoise = self.Audio_Denoise(self.category_name, *args, **kwargs)
            self.color_adjustment = self.Color_Adjustment(self.category_name, *args, **kwargs)
            self.white_balance = self.White_Balance(self.category_name, *args, **kwargs)
            self.color_enhancement = self.Color_Enhancement(self.category_name, *args, **kwargs)
            self.split_toning = self.Split_Toning(self.category_name, *args, **kwargs)
            self.hdr_effect = self.HDR_Effect(self.category_name, *args, **kwargs)

        @step('[Action][KeyFrame Page][Fix_Enhance] Unfold [Fix Enhance] tab')
        def unfold_tab(self, value=1): # value: 1(unfold), 0(fold)
            return set_category_fold_enable(self, self.category_name, value)

        def get_unfold_status(self): # True: unfold, False: fold
            return bool(get_category_fold_status(self, self.category_name))

        def right_click_menu(self, menu_item): # menu_item: Copy, Paste, Select All
            return category_select_right_click_menu(self, self.category_name, menu_item)

        def show(self):
            return set_category_visible(self, self.category_name)

        class Lighting_Adjustment(BasePage):
            def __init__(self, root_category, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.root_category = root_category
                self.category_name = 'Lighting Adjust*'
                self.extreme_backlight = self.Extreme_Backlight(self.root_category, self.category_name, *args, **kwargs)
                self.degree = self.Degree(self.root_category, self.category_name, *args, **kwargs)

            def unfold_tab(self, value=1):  # value: 1(unfold), 0(fold)
                return set_category_fold_enable(self, self.category_name, value)

            def get_unfold_status(self):  # True: unfold, False: fold
                return bool(get_category_fold_status(self, self.category_name))

            def show(self):
                set_category_fold_enable(self, self.root_category, 1)
                set_category_visible(self, self.category_name)
                return True

            class Extreme_Backlight(BasePage):
                def __init__(self, root_category, category_name, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.root_category = root_category
                    self.category_name = category_name
                    self.attribute_name = 'Extreme backlight'

                def set_checkbox(self, set_status=1, index_node=-1):
                    locator_checkbox = L.keyframe_room.unit_attribute_name_checkbox
                    return set_attribute_checkbox(self, self.attribute_name, locator_checkbox, set_status, index_node, 'type_checkbox')

                def get_checkbox(self, index_node=-1):
                    locator_checkbox = L.keyframe_room.unit_attribute_name_checkbox
                    return get_attribute_checkbox(self, self.attribute_name, locator_checkbox, index_node, 'type_checkbox')

                def reset_keyframe(self):
                    return click_attribute_reset_keyframe(self, self.attribute_name, '', 'type_checkbox')

                def add_remove_keyframe(self, index_node=-1):
                    return click_attribute_add_remove_keyframe(self, self.attribute_name, index_node, '', 'type_checkbox')

                def previous_keyframe(self, index_node=-1):
                    return click_attribute_previous_keyframe(self, self.attribute_name, index_node, '', 'type_checkbox')

                def next_keyframe(self, index_node=-1):
                    return click_attribute_next_keyframe(self, self.attribute_name, index_node, '', 'type_checkbox')

                def show(self):
                    set_category_fold_enable(self, self.root_category, 1)
                    set_category_fold_enable(self, self.category_name, 1)
                    set_attribute_visible(self, self.attribute_name, self.category_name, 'type_checkbox')

            class Degree(BasePage):
                def __init__(self, root_category, category_name, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.root_category = root_category
                    self.category_name = category_name
                    self.attribute_name = 'Degree:'
                @step('[Action][KeyFrame Page][Fix_Enhance][Lighting_Adjustment][Degree] Set value')
                def set_value(self, value, index_node=-1): # 0 - 100
                    return set_attribute_edittext_value(self, self.attribute_name, value, index_node, None, -1, self.category_name)
                @step('[Action][KeyFrame Page][Fix_Enhance][Lighting_Adjustment][Degree] Get value')
                def get_value(self, index_node=-1):
                    return get_attribute_edittext_value(self, self.attribute_name, index_node, None, -1, self.category_name)

                def set_slider(self, value, index_node=-1): # value: 0 - 100
                    return set_attribute_slider_value(self, self.attribute_name, value, index_node, None, -1, self.category_name)

                def reset_keyframe(self):
                    return click_attribute_reset_keyframe(self, self.attribute_name, self.category_name)

                def add_remove_keyframe(self, index_node=-1):
                    return click_attribute_add_remove_keyframe(self, self.attribute_name, index_node, self.category_name)
                @step('[Action][KeyFrame Page][Fix_Enhance][Lighting_Adjustment][Degree] Click [Previous Keyframe]')
                def previous_keyframe(self, index_node=-1):
                    return click_attribute_previous_keyframe(self, self.attribute_name, index_node, self.category_name)
                @step('[Action][KeyFrame Page][Fix_Enhance][Lighting_Adjustment][Degree] Click [Next Keyframe]')
                def next_keyframe(self, index_node=-1):
                    return click_attribute_next_keyframe(self, self.attribute_name, index_node, self.category_name)

                def click_stepper_up(self, times=1, index_node=-1):
                    return click_attribute_stepper(self, self.attribute_name, 'up', times, index_node, None, -1, self.category_name)

                def click_stepper_down(self, times=1, index_node=-1):
                    return click_attribute_stepper(self, self.attribute_name, 'down', times, index_node, None, -1, self.category_name)

                def show(self):
                    set_category_fold_enable(self, self.root_category, 1)
                    set_category_fold_enable(self, self.category_name, 1)
                    set_attribute_visible(self, self.attribute_name)

        class Video_Denoise(BasePage):
            def __init__(self, root_category, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.root_category = root_category
                self.category_name = 'Video De*'
                self.degree = self.Degree(self.root_category, self.category_name, *args, **kwargs)

            def unfold_tab(self, value=1):  # value: 1(unfold), 0(fold)
                return set_category_fold_enable(self, self.category_name, value)

            def get_unfold_status(self):  # True: unfold, False: fold
                return bool(get_category_fold_status(self, self.category_name))

            def show(self):
                set_category_fold_enable(self, self.root_category, 1)
                set_category_visible(self, self.category_name)
                return True

            class Degree(BasePage):
                def __init__(self, root_category, category_name, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.root_category = root_category
                    self.category_name = category_name
                    self.attribute_name = 'Degree:'
                @step('[Action][KeyFrame Page][Fix Enhance][Video Denoise][Degree] Set value')
                def set_value(self, value, index_node=-1): # 0 - 100
                    return set_attribute_edittext_value(self, self.attribute_name, value, index_node, None, -1, self.category_name)
                @step('[Action][KeyFrame Page][Fix Enhance][Video Denoise][Degree] Get value')
                def get_value(self, index_node=-1):
                    return get_attribute_edittext_value(self, self.attribute_name, index_node, None, -1, self.category_name)
                @step('[Action][KeyFrame Page][Fix Enhance][Video Denoise][Degree] Set value by slider')
                def set_slider(self, value, index_node=-1): # value: 0 - 100
                    return set_attribute_slider_value(self, self.attribute_name, value, index_node, None, -1, self.category_name)
                @step('[Action][KeyFrame Page][Fix Enhance][Video Denoise][Degree] Reset [Keyframe]')
                def reset_keyframe(self):
                    return click_attribute_reset_keyframe(self, self.attribute_name, self.category_name)
                @step('[Action][KeyFrame Page][Fix Enhance][Video Denoise][Degree] Add/Remove [Keyframe]')
                def add_remove_keyframe(self, index_node=-1):
                    return click_attribute_add_remove_keyframe(self, self.attribute_name, index_node, self.category_name)
                @step('[Action][KeyFrame Page][Fix Enhance][Video Denoise][Degree] Click [Previous Keyframe]')
                def previous_keyframe(self, index_node=-1):
                    return click_attribute_previous_keyframe(self, self.attribute_name, index_node, self.category_name)
                @step('[Action][KeyFrame Page][Fix Enhance][Video Denoise][Degree] Click [Next Keyframe]')
                def next_keyframe(self, index_node=-1):
                    return click_attribute_next_keyframe(self, self.attribute_name, index_node, self.category_name)
                @step('[Action][KeyFrame Page][Fix Enhance][Video Denoise][Degree] Click [Stepper Up] button')
                def click_stepper_up(self, times=1, index_node=-1):
                    return click_attribute_stepper(self, self.attribute_name, 'up', times, index_node, None, -1, self.category_name)
                @step('[Action][KeyFrame Page][Fix Enhance][Video Denoise][Degree] Click [Stepper Down] button')
                def click_stepper_down(self, times=1, index_node=-1):
                    return click_attribute_stepper(self, self.attribute_name, 'down', times, index_node, None, -1, self.category_name)

                def show(self):
                    set_category_fold_enable(self, self.root_category, 1)
                    set_category_fold_enable(self, self.category_name, 1)
                    set_attribute_visible(self, self.attribute_name)

        class Audio_Denoise(BasePage):
            def __init__(self, root_category, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.root_category = root_category
                self.category_name = 'Audio De*'
                self.noise = self.Noise(self.root_category, self.category_name, *args, **kwargs)
                self.degree = self.Degree(self.root_category, self.category_name, *args, **kwargs)

            def unfold_tab(self, value=1):  # value: 1(unfold), 0(fold)
                return set_category_fold_enable(self, self.category_name, value)

            def get_unfold_status(self):  # True: unfold, False: fold
                return bool(get_category_fold_status(self, self.category_name))

            def show(self):
                set_category_fold_enable(self, self.root_category, 1)
                set_category_visible(self, self.category_name)
                return True

            class Noise(BasePage):
                def __init__(self, root_category, category_name, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.root_category = root_category
                    self.category_name = category_name
                    self.attribute_name = 'Noise type:'

                def set_type(self, index_option=1, index_node=-1):
                    return select_attribute_combobox_option(self, self.attribute_name, index_option, index_node)

                def get_type(self, index_node=-1):
                    return get_attribute_combobox_option(self, self.attribute_name, index_node)

                def reset_keyframe(self):
                    return click_attribute_reset_keyframe(self, self.attribute_name)

                def add_remove_keyframe(self, index_node=-1):
                    return click_attribute_add_remove_keyframe(self, self.attribute_name, index_node)

                def previous_keyframe(self, index_node=-1):
                    return click_attribute_previous_keyframe(self, self.attribute_name, index_node)

                def next_keyframe(self, index_node=-1):
                    return click_attribute_next_keyframe(self, self.attribute_name, index_node)

                def show(self):
                    set_category_fold_enable(self, self.root_category, 1)
                    set_category_fold_enable(self, self.category_name, 1)
                    set_attribute_visible(self, self.attribute_name)

            class Degree(BasePage):
                def __init__(self, root_category, category_name, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.root_category = root_category
                    self.category_name = category_name
                    self.attribute_name = 'Degree:'
                @step('[Action][KeyFrame Page][Fix Enhance][Audio Denoise][Degree] Set value')
                def set_value(self, value, index_node=-1): # 0 - 100
                    return set_attribute_edittext_value(self, self.attribute_name, value, index_node, None, -1, self.category_name)
                @step('[Action][KeyFrame Page][Fix Enhance][Audio Denoise][Degree] Get value')
                def get_value(self, index_node=-1):
                    return get_attribute_edittext_value(self, self.attribute_name, index_node, None, -1, self.category_name)

                def set_slider(self, value, index_node=-1): # value: 0 - 100
                    return set_attribute_slider_value(self, self.attribute_name, value, index_node, None, -1, self.category_name)

                def reset_keyframe(self):
                    return click_attribute_reset_keyframe(self, self.attribute_name, self.category_name)

                def add_remove_keyframe(self, index_node=-1):
                    return click_attribute_add_remove_keyframe(self, self.attribute_name, index_node, self.category_name)

                def previous_keyframe(self, index_node=-1):
                    return click_attribute_previous_keyframe(self, self.attribute_name, index_node, self.category_name)

                def next_keyframe(self, index_node=-1):
                    return click_attribute_next_keyframe(self, self.attribute_name, index_node, self.category_name)
                @step('[Action][KeyFrame Page][Fix Enhance][Audio Denoise][Degree] Click [Stepper Up] button')
                def click_stepper_up(self, times=1, index_node=-1):
                    return click_attribute_stepper(self, self.attribute_name, 'up', times, index_node, None, -1, self.category_name)
                @step('[Action][KeyFrame Page][Fix Enhance][Audio Denoise][Degree] Click [Stepper Down] button')
                def click_stepper_down(self, times=1, index_node=-1):
                    return click_attribute_stepper(self, self.attribute_name, 'down', times, index_node, None, -1, self.category_name)

                def show(self):
                    set_category_fold_enable(self, self.root_category, 1)
                    set_category_fold_enable(self, self.category_name, 1)
                    set_attribute_visible(self, self.attribute_name)

        class Color_Adjustment(BasePage):
            def __init__(self, root_category, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.root_category = root_category
                self.category_name = 'Color Adjust*'
                self.exposure = self.Unit_CAOperation(self.root_category, self.category_name, 'Exposure', *args, **kwargs)
                self.brightness = self.Unit_CAOperation(self.root_category, self.category_name, 'Brightness', *args, **kwargs)
                self.contrast = self.Unit_CAOperation(self.root_category, self.category_name, 'Contrast', *args, **kwargs)
                self.hue = self.Unit_CAOperation(self.root_category, self.category_name, 'Hue', *args, **kwargs)
                self.saturation = self.Unit_CAOperation(self.root_category, self.category_name, 'Saturation', *args, **kwargs)
                self.vibrancy = self.Unit_CAOperation(self.root_category, self.category_name, 'Vibrancy', *args, **kwargs)
                self.highlight = self.Unit_CAOperation(self.root_category, self.category_name, 'Highlight*', *args, **kwargs)
                self.shadow = self.Unit_CAOperation(self.root_category, self.category_name, 'Shadow', *args, **kwargs)
                self.sharpness = self.Unit_CAOperation(self.root_category, self.category_name, 'Sharpness*', *args, **kwargs)

            def unfold_tab(self, value=1):  # value: 1(unfold), 0(fold)
                return set_category_fold_enable(self, self.category_name, value)

            def get_unfold_status(self):  # True: unfold, False: fold
                return bool(get_category_fold_status(self, self.category_name))

            def show(self):
                set_category_fold_enable(self, self.root_category, 1)
                set_category_visible(self, self.category_name)
                return True

            class Unit_CAOperation(BasePage):
                def __init__(self, root_category, category_name, attribute_name, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.root_category = root_category
                    self.category_name = category_name
                    self.attribute_name = attribute_name
                @step('[Action][KeyFrame Page][Fix Enhance][Color Adjustment][Unit CAOperation] Set value')
                def set_value(self, value, index_node=-1): # 0 - 100
                    return set_attribute_edittext_value(self, self.attribute_name, value, index_node)
                @step('[Action][KeyFrame Page][Fix Enhance][Color Adjustment][Unit CAOperation] Get value')
                def get_value(self, index_node=-1):
                    return get_attribute_edittext_value(self, self.attribute_name, index_node)
                @step('[Action][KeyFrame Page][Fix Enhance][Color Adjustment][Unit CAOperation] Set value by slider')
                def set_slider(self, value, index_node=-1): # value: 0 - 100
                    return set_attribute_slider_value(self, self.attribute_name, value, index_node)

                def reset_keyframe(self):
                    return click_attribute_reset_keyframe(self, self.attribute_name)
                @step('[Action][KeyFrame Page][Fix Enhance][Color Adjustment][Unit CAOperation] Add/ Remove keyframe')
                def add_remove_keyframe(self, index_node=-1):
                    return click_attribute_add_remove_keyframe(self, self.attribute_name, index_node)
                @step('[Action][KeyFrame Page][Fix Enhance][Color Adjustment][Unit CAOperation] Click [Previous Keyframe] button')
                def previous_keyframe(self, index_node=-1):
                    return click_attribute_previous_keyframe(self, self.attribute_name, index_node)
                @step('[Action][KeyFrame Page][Fix Enhance][Color Adjustment][Unit CAOperation] Click [Next Keyframe] button')
                def next_keyframe(self, index_node=-1):
                    return click_attribute_next_keyframe(self, self.attribute_name, index_node)

                def click_stepper_up(self, times=1, index_node=-1):
                    return click_attribute_stepper(self, self.attribute_name, 'up', times, index_node)

                def click_stepper_down(self, times=1, index_node=-1):
                    return click_attribute_stepper(self, self.attribute_name, 'down', times, index_node)

                def show(self):
                    set_category_fold_enable(self, self.root_category, 1)
                    set_category_fold_enable(self, self.category_name, 1)
                    set_attribute_visible(self, self.attribute_name)

        class White_Balance(BasePage):
            def __init__(self, root_category, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.root_category = root_category
                self.category_name = 'White Balance'
                self.attribute_name = 'Tint'
                self.color_temperature = self.Unit_WBOperation(self.root_category, self.category_name, self.attribute_name,
                                                               L.keyframe_room.group_edittext_stepper_color_temperature, 0, 0, *args, **kwargs)
                self.tint = self.Unit_WBOperation(self.root_category, self.category_name, self.attribute_name,
                                                               L.keyframe_room.group_edittext_stepper_tint, 0, 1, *args, **kwargs)
                self.white_calibration = self.White_Calibration(self.root_category, self.category_name, self.attribute_name, *args, **kwargs)

            def unfold_tab(self, value=1):  # value: 1(unfold), 0(fold)
                return set_category_fold_enable(self, self.category_name, value)

            def get_unfold_status(self):  # True: unfold, False: fold
                return bool(get_category_fold_status(self, self.category_name))

            def reset_keyframe(self):
                return click_attribute_reset_keyframe(self, self.attribute_name)

            def add_remove_keyframe(self, index_node=-1):
                return click_attribute_add_remove_keyframe(self, self.attribute_name, index_node)

            def previous_keyframe(self, index_node=-1):
                return click_attribute_previous_keyframe(self, self.attribute_name, index_node)

            def next_keyframe(self, index_node=-1):
                return click_attribute_next_keyframe(self, self.attribute_name, index_node)

            def show(self):
                set_category_fold_enable(self, self.root_category, 1)
                set_category_visible(self, self.category_name)
                return True

            def select_color_temperature(self):
                return self.exist_click(L.keyframe_room.rdb_color_temperature)

            def select_white_calibration(self):
                return self.exist_click(L.keyframe_room.rdb_white_calibration)

            def get_current_select_option(self):
                list_locator = [L.keyframe_room.rdb_color_temperature, L.keyframe_room.rdb_white_calibration]
                list_name = ['Color temperature/Tint', 'White calibration']
                current_select = -1
                for index in range(len(list_name)):
                    if self.exist(list_locator[index]).AXValue:
                        current_select = list_name[index]
                        break
                return current_select

            class Unit_WBOperation(BasePage):
                def __init__(self, root_category, category_name, attribute_name, locator_group, index_group, index_slider, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.root_category = root_category
                    self.category_name = category_name
                    self.attribute_name = attribute_name
                    self.locator_group = locator_group
                    self.index_group = index_group
                    self.index_slider = index_slider
                @step('[Action][KeyFrame Page][Fix Enhance][White Balance][Unit WBOperation] Set value')
                def set_value(self, value, index_node=-1): # 0 - 100
                    return set_attribute_edittext_value(self, self.attribute_name, value, index_node, self.locator_group, self.index_group)
                @step('[Action][KeyFrame Page][Fix Enhance][White Balance][Unit WBOperation] Get value')
                def get_value(self, index_node=-1):
                    return get_attribute_edittext_value(self, self.attribute_name, index_node, self.locator_group, self.index_group)
                
                def set_slider(self, value, index_node=-1): # value: 0 - 100
                    return set_attribute_slider_value(self, self.attribute_name, value, index_node, None, self.index_slider)

                def click_stepper_up(self, times=1, index_node=-1):
                    return click_attribute_stepper(self, self.attribute_name, 'up', times, index_node, self.locator_group, self.index_group)

                def click_stepper_down(self, times=1, index_node=-1):
                    return click_attribute_stepper(self, self.attribute_name, 'down', times, index_node, self.locator_group, self.index_group)

                def show(self):
                    set_category_fold_enable(self, self.root_category, 1)
                    set_category_fold_enable(self, self.category_name, 1)
                    set_attribute_visible(self, self.attribute_name)

            class White_Calibration(BasePage):
                def __init__(self, root_category, category_name, attribute_name, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.root_category = root_category
                    self.category_name = category_name
                    self.attribute_name = attribute_name

                def show(self):
                    set_category_fold_enable(self, self.root_category, 1)
                    set_category_fold_enable(self, self.category_name, 1)
                    set_attribute_visible(self, self.attribute_name)

                def click_i_button(self, is_close_all=True):
                    self.exist_click(L.keyframe_room.btn_white_calibration)
                    time.sleep(OPERATION_DELAY * 0.5)
                    self.exist_click(L.keyframe_room.white_calibration_dialog.btn_information)
                    time.sleep(OPERATION_DELAY * 0.5)
                    if self.exist(L.keyframe_room.what_is_white_calibration_dialog.main_window):
                        result = True
                    else:
                        result = False
                    if is_close_all:
                        self.exist_click(L.keyframe_room.what_is_white_calibration_dialog.btn_close)
                        time.sleep(OPERATION_DELAY * 0.5)
                        self.exist_click(L.keyframe_room.white_calibration_dialog.btn_close)
                    return result

        class Color_Enhancement(BasePage):
            def __init__(self, root_category, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.root_category = root_category
                self.category_name = 'Color Enhance*'
                self.degree = self.Degree(self.root_category, self.category_name, *args, **kwargs)

            def unfold_tab(self, value=1):  # value: 1(unfold), 0(fold)
                return set_category_fold_enable(self, self.category_name, value)

            def get_unfold_status(self):  # True: unfold, False: fold
                return bool(get_category_fold_status(self, self.category_name))

            def show(self):
                set_category_fold_enable(self, self.root_category, 1)
                set_category_visible(self, self.category_name)
                return True

            class Degree(BasePage):
                def __init__(self, root_category, category_name, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.root_category = root_category
                    self.category_name = category_name
                    self.attribute_name = 'Degree:'

                def set_value(self, value, index_node=-1): # 0 - 100
                    return set_attribute_edittext_value(self, self.attribute_name, value, index_node, None, -1, self.category_name)

                def get_value(self, index_node=-1):
                    return get_attribute_edittext_value(self, self.attribute_name, index_node, None, -1, self.category_name)

                def set_slider(self, value, index_node=-1): # value: 0 - 100
                    return set_attribute_slider_value(self, self.attribute_name, value, index_node, None, -1, self.category_name)

                def reset_keyframe(self):
                    return click_attribute_reset_keyframe(self, self.attribute_name, self.category_name)

                def add_remove_keyframe(self, index_node=-1):
                    return click_attribute_add_remove_keyframe(self, self.attribute_name, index_node, self.category_name)

                def previous_keyframe(self, index_node=-1):
                    return click_attribute_previous_keyframe(self, self.attribute_name, index_node, self.category_name)

                def next_keyframe(self, index_node=-1):
                    return click_attribute_next_keyframe(self, self.attribute_name, index_node, self.category_name)
                @step('[Action][KeyFrame Page][Fix Enhance][Color Enhancement][Degree] Click [Stepper Up] button')
                def click_stepper_up(self, times=1, index_node=-1):
                    return click_attribute_stepper(self, self.attribute_name, 'up', times, index_node, None, -1, self.category_name)
                @step('[Action][KeyFrame Page][Fix Enhance][Color Enhancement][Degree] Click [Stepper Down] button')
                def click_stepper_down(self, times=1, index_node=-1):
                    return click_attribute_stepper(self, self.attribute_name, 'down', times, index_node, None, -1, self.category_name)

                def show(self):
                    set_category_fold_enable(self, self.root_category, 1)
                    set_category_fold_enable(self, self.category_name, 1)
                    set_attribute_visible(self, self.attribute_name, self.category_name)

        class Split_Toning(BasePage):
            def __init__(self, root_category, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.root_category = root_category
                self.category_name = 'Split Toning'
                self.highlights_hue = self.Unit_STOperation(self.root_category, self.category_name, 'Highlights hue:', *args, **kwargs)
                self.highlights_saturation = self.Unit_STOperation(self.root_category, self.category_name, 'Highlights saturation:', *args, **kwargs)
                self.balance = self.Unit_STOperation(self.root_category, self.category_name, 'Balance:', *args, **kwargs)
                self.shadow_hue = self.Unit_STOperation(self.root_category, self.category_name, 'Shadow hue:', *args, **kwargs)
                self.shadow_saturation = self.Unit_STOperation(self.root_category, self.category_name, 'Shadow saturation:', *args, **kwargs)

            def unfold_tab(self, value=1):  # value: 1(unfold), 0(fold)
                return set_category_fold_enable(self, self.category_name, value)

            def get_unfold_status(self):  # True: unfold, False: fold
                return bool(get_category_fold_status(self, self.category_name))

            def show(self):
                set_category_fold_enable(self, self.root_category, 1)
                set_category_visible(self, self.category_name)
                return True

            class Unit_STOperation(BasePage):
                def __init__(self, root_category, category_name, attribute_name, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.root_category = root_category
                    self.category_name = category_name
                    self.attribute_name = attribute_name
                @step('[Action][KeyFrame Page][Fix Enhance][Split Toning][Unit STOperation] Set value')
                def set_value(self, value, index_node=-1): # 0 - 100
                    return set_attribute_edittext_value(self, self.attribute_name, value, index_node)
                @step('[Action][KeyFrame Page][Fix Enhance][Split Toning][Unit STOperation] Get value')
                def get_value(self, index_node=-1):
                    return get_attribute_edittext_value(self, self.attribute_name, index_node)
                @step('[Action][KeyFrame Page][Fix Enhance][Split Toning][Unit STOperation] Set value by slider')
                def set_slider(self, value, index_node=-1): # value: 0 - 100
                    return set_attribute_slider_value(self, self.attribute_name, value, index_node)
                @step('[Action][KeyFrame Page][Fix Enhance][Split Toning][Unit STOperation] Reset [Keyframe]')
                def reset_keyframe(self):
                    return click_attribute_reset_keyframe(self, self.attribute_name)
                @step('[Action][KeyFrame Page][Fix Enhance][Split Toning][Unit STOperation] Add/ Remove [Keyframe]')
                def add_remove_keyframe(self, index_node=-1):
                    return click_attribute_add_remove_keyframe(self, self.attribute_name, index_node)
                @step('[Action][KeyFrame Page][Fix Enhance][Split Toning][Unit STOperation] Click [Previous Keyframe]')
                def previous_keyframe(self, index_node=-1):
                    return click_attribute_previous_keyframe(self, self.attribute_name, index_node)
                @step('[Action][KeyFrame Page][Fix Enhance][Split Toning][Unit STOperation] Click [Next Keyframe]')
                def next_keyframe(self, index_node=-1):
                    return click_attribute_next_keyframe(self, self.attribute_name, index_node)

                def click_stepper_up(self, times=1, index_node=-1):
                    return click_attribute_stepper(self, self.attribute_name, 'up', times, index_node)

                def click_stepper_down(self, times=1, index_node=-1):
                    return click_attribute_stepper(self, self.attribute_name, 'down', times, index_node)

                def show(self):
                    set_category_fold_enable(self, self.root_category, 1)
                    set_category_fold_enable(self, self.category_name, 1)
                    set_attribute_visible(self, self.attribute_name)

        class HDR_Effect(BasePage):
            def __init__(self, root_category, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.root_category = root_category
                self.category_name = 'HDR Effect'
                self.glow_strength = self.Unit_HEOperation(self.root_category, self.category_name, 'Glow strength:', *args, **kwargs)
                self.glow_radius = self.Unit_HEOperation(self.root_category, self.category_name, 'Glow radius:', *args, **kwargs)
                self.glow_balance = self.Unit_HEOperation(self.root_category, self.category_name, 'Glow balance:', *args, **kwargs)
                self.edge_strength = self.Unit_HEOperation(self.root_category, self.category_name, 'Edge strength:', *args, **kwargs)
                self.edge_radius = self.Unit_HEOperation(self.root_category, self.category_name, 'Edge radius:', *args, **kwargs)
                self.edge_balance = self.Unit_HEOperation(self.root_category, self.category_name, 'Edge balance:', *args, **kwargs)

            def unfold_tab(self, value=1):  # value: 1(unfold), 0(fold)
                return set_category_fold_enable(self, self.category_name, value)

            def get_unfold_status(self):  # True: unfold, False: fold
                return bool(get_category_fold_status(self, self.category_name))

            def show(self):
                set_category_fold_enable(self, self.root_category, 1)
                set_category_visible(self, self.category_name)
                return True

            class Unit_HEOperation(BasePage):
                def __init__(self, root_category, category_name, attribute_name, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.root_category = root_category
                    self.category_name = category_name
                    self.attribute_name = attribute_name
                @step('[Action][KeyFrame Page][Fix Enhance][HDR Effect][Unit HEOperation] Set value')
                def set_value(self, value, index_node=-1): # 0 - 100
                    return set_attribute_edittext_value(self, self.attribute_name, value, index_node)
                @step('[Action][KeyFrame Page][Fix Enhance][HDR Effect][Unit HEOperation] Get value')
                def get_value(self, index_node=-1):
                    return get_attribute_edittext_value(self, self.attribute_name, index_node)
                @step('[Action][KeyFrame Page][Fix Enhance][HDR Effect][Unit HEOperation] Set value by slider')
                def set_slider(self, value, index_node=-1): # value: 0 - 100
                    return set_attribute_slider_value(self, self.attribute_name, value, index_node)
                @step('[Action][KeyFrame Page][Fix Enhance][HDR Effect][Unit HEOperation] Reset [Keyframe]')
                def reset_keyframe(self):
                    return click_attribute_reset_keyframe(self, self.attribute_name)
                @step('[Action][KeyFrame Page][Fix Enhance][HDR Effect][Unit HEOperation] Add/ Remove [Keyframe]')
                def add_remove_keyframe(self, index_node=-1):
                    return click_attribute_add_remove_keyframe(self, self.attribute_name, index_node)
                @step('[Action][KeyFrame Page][Fix Enhance][HDR Effect][Unit HEOperation] Click [Previous Keyframe]')
                def previous_keyframe(self, index_node=-1):
                    return click_attribute_previous_keyframe(self, self.attribute_name, index_node)
                @step('[Action][KeyFrame Page][Fix Enhance][HDR Effect][Unit HEOperation] Click [Next Keyframe]')
                def next_keyframe(self, index_node=-1):
                    return click_attribute_next_keyframe(self, self.attribute_name, index_node)
                @step('[Action][KeyFrame Page][Fix Enhance][HDR Effect][Unit HEOperation] Click [Stepper Up]')
                def click_stepper_up(self, times=1, index_node=-1):
                    return click_attribute_stepper(self, self.attribute_name, 'up', times, index_node)
                @step('[Action][KeyFrame Page][Fix Enhance][HDR Effect][Unit HEOperation] Click [Stepper Down]')
                def click_stepper_down(self, times=1, index_node=-1):
                    return click_attribute_stepper(self, self.attribute_name, 'down', times, index_node)

                def show(self):
                    set_category_fold_enable(self, self.root_category, 1)
                    set_category_fold_enable(self, self.category_name, 1)
                    set_attribute_visible(self, self.attribute_name)

    class Clip_Attributes(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.category_name = 'Clip Attributes'
            self.position = self.Position(self.category_name, *args, **kwargs)
            self.scale = self.Scale(self.category_name, *args, **kwargs)
            self.opacity = self.Opacity(self.category_name, *args, **kwargs)
            self.rotation = self.Rotation(self.category_name, *args, **kwargs)
            self.freeform = self.Freeform(self.category_name, *args, **kwargs)
        @step('[Action][KeyFrame Page][Clip Attributes] Fold/ Unfold [Clip Attributes] tab')
        def unfold_tab(self, value=1): # value: 1(unfold), 0(fold)
            return set_category_fold_enable(self, self.category_name, value)

        def get_unfold_status(self): # True: unfold, False: fold
            return bool(get_category_fold_status(self, self.category_name))

        def right_click_menu(self, menu_item): # menu_item: Copy, Paste, Select All
            return category_select_right_click_menu(self, self.category_name, menu_item)

        class Position(BasePage):
            def __init__(self, category, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.category_name = category
                self.attribute_name = 'Position'
                self.x = self.X(self.attribute_name, *args, **kwargs)
                self.y = self.Y(self.attribute_name, *args, **kwargs)
                self.ease_in = self.Ease_In(self.attribute_name, *args, **kwargs)
                self.ease_out = self.Ease_Out(self.attribute_name, *args, **kwargs)

            def show(self):
                set_category_fold_enable(self, self.category_name, 1)
                set_attribute_visible(self, self.attribute_name)
                return True

            def add_remove_keyframe(self, index_node=-1):
                return click_attribute_add_remove_keyframe(self, self.attribute_name, index_node)

            def reset_keyframe(self):
                return click_attribute_reset_keyframe(self, self.attribute_name)

            def previous_keyframe(self, index_node=-1):
                return click_attribute_previous_keyframe(self, self.attribute_name, index_node)

            def next_keyframe(self, index_node=-1):
                return click_attribute_next_keyframe(self, self.attribute_name, index_node)

            def click_tutorial_btn(self):
                result = True
                try:
                    self.click(L.keyframe_room.btn_tutorial)
                    time.sleep(OPERATION_DELAY)
                    title = self.check_chrome_page()
                    if 'Free Video Effects' not in title:
                        logger('Fail to open tutorial page')
                        result = False
                    close_chrome_page(self)
                    time.sleep(OPERATION_DELAY)
                except Exception as e:
                    logger(f'Exception occurs: {e}')
                    return False
                return result

            class X(BasePage):
                def __init__(self, attribute_name, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.attribute_name = attribute_name
                @step('[Action][KeyFrame Page][Clip Attributes][Position][X] Set value')
                def set_value(self, value, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_xy
                    return set_attribute_edittext_value(self, self.attribute_name, value, index_node, locator_group, 0)
                @step('[Action][KeyFrame Page][Clip Attributes][Position][X] Get value')
                def get_value(self, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_xy
                    return get_attribute_edittext_value(self, self.attribute_name, index_node, locator_group, 0)
                @step('[Action][KeyFrame Page][Clip Attributes][Position][X] Click [Stepper Up] button')
                def click_stepper_up(self, times=1, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_xy
                    return click_attribute_stepper(self, self.attribute_name, 'up', times, index_node, locator_group, 0)
                @step('[Action][KeyFrame Page][Clip Attributes][Position][X] Click [Stepper Down] button')
                def click_stepper_down(self, times=1, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_xy
                    return click_attribute_stepper(self, self.attribute_name, 'down', times, index_node, locator_group, 0)

            class Y(BasePage):
                def __init__(self, attribute_name, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.attribute_name = attribute_name
                @step('[Action][KeyFrame Page][Clip Attributes][Position][Y] Set value')
                def set_value(self, value, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_xy
                    return set_attribute_edittext_value(self, self.attribute_name, value, index_node, locator_group, 1)
                @step('[Action][KeyFrame Page][Clip Attributes][Position][Y] Get value')
                def get_value(self, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_xy
                    return get_attribute_edittext_value(self, self.attribute_name, index_node, locator_group, 1)
                @step('[Action][KeyFrame Page][Clip Attributes][Position][Y] Click [Stepper Up] button')
                def click_stepper_up(self, times=1, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_xy
                    return click_attribute_stepper(self, self.attribute_name, 'up', times, index_node, locator_group, 1)
                @step('[Action][KeyFrame Page][Clip Attributes][Position][Y] Click [Stepper Down] button')
                def click_stepper_down(self, times=1, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_xy
                    return click_attribute_stepper(self, self.attribute_name, 'down', times, index_node, locator_group, 1)

            class Ease_In(BasePage):
                def __init__(self, attribute_name, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.attribute_name = attribute_name

                def set_checkbox(self, set_status=1, index_node=-1):
                    locator_checkbox = L.keyframe_room.chx_ease_in
                    return set_attribute_checkbox(self, self.attribute_name, locator_checkbox, set_status, index_node)

                def set_slider(self, value, index_node=-1):
                    locator_slider = L.keyframe_room.slider_ease_in
                    return set_attribute_slider_value(self, self.attribute_name, value, index_node, locator_slider)

                def set_value(self, value, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_ease_in_out
                    return set_attribute_edittext_value(self, self.attribute_name, value, index_node, locator_group, 0)

                def get_value(self, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_ease_in_out
                    return get_attribute_edittext_value(self, self.attribute_name, index_node, locator_group, 0)

                def click_stepper_up(self, times=1, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_ease_in_out
                    return click_attribute_stepper(self, self.attribute_name, 'up', times, index_node, locator_group, 0)

                def click_stepper_down(self, times=1, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_ease_in_out
                    return click_attribute_stepper(self, self.attribute_name, 'down', times, index_node, locator_group,
                                                   0)

            class Ease_Out(BasePage):
                def __init__(self, attribute_name, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.attribute_name = attribute_name

                def set_checkbox(self, set_status=1, index_node=-1):
                    locator_checkbox = L.keyframe_room.chx_ease_out
                    return set_attribute_checkbox(self, self.attribute_name, locator_checkbox, set_status, index_node)

                def set_slider(self, value, index_node=-1):
                    locator_slider = L.keyframe_room.slider_ease_out
                    return set_attribute_slider_value(self, self.attribute_name, value, index_node, locator_slider)

                def set_value(self, value, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_ease_out
                    return set_attribute_edittext_value(self, self.attribute_name, value, index_node, locator_group, 0)

                def get_value(self, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_ease_out
                    return get_attribute_edittext_value(self, self.attribute_name, index_node, locator_group, 0)

                def click_stepper_up(self, times=1, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_ease_out
                    return click_attribute_stepper(self, self.attribute_name, 'up', times, index_node, locator_group, 0)

                def click_stepper_down(self, times=1, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_ease_out
                    return click_attribute_stepper(self, self.attribute_name, 'down', times, index_node, locator_group, 0)

        class Scale(BasePage):
            def __init__(self, category, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.category_name = category
                self.attribute_name = 'Width'
                self.width = self.Unit_Width_Height_Operation(self.attribute_name, L.keyframe_room.group_edittext_stepper_width, 0, 0, *args, **kwargs)
                self.height = self.Unit_Width_Height_Operation(self.attribute_name, L.keyframe_room.group_edittext_stepper_height, 0, 1, *args, **kwargs)
                self.ease_in = self.Ease_In(self.attribute_name, *args, **kwargs)
                self.ease_out = self.Ease_Out(self.attribute_name, *args, **kwargs)

            def show(self):
                set_category_fold_enable(self, self.category_name, 1)
                set_attribute_visible(self, self.attribute_name)
                return True
            @step('[Action][KeyFrame Page][Clip Attributes][Scale] Add/ Remove [Keyframe]')
            def add_remove_keyframe(self, index_node=-1):
                return click_attribute_add_remove_keyframe(self, self.attribute_name, index_node)
            @step('[Action][KeyFrame Page][Clip Attributes][Scale] Reset [Keyframe]')
            def reset_keyframe(self):
                return click_attribute_reset_keyframe(self, self.attribute_name)
            @step('[Action][KeyFrame Page][Clip Attributes][Scale] Click [Previous Keyframe]')
            def previous_keyframe(self, index_node=-1):
                return click_attribute_previous_keyframe(self, self.attribute_name, index_node)
            @step('[Action][KeyFrame Page][Clip Attributes][Scale] Click [Next Keyframe]')
            def next_keyframe(self, index_node=-1):
                return click_attribute_next_keyframe(self, self.attribute_name, index_node)
            @step('[Action][KeyFrame Page][Clip Attributes][Scale] Set [Maintain Aspect Ratio]')
            def set_maintain_aspect_ratio(self, set_status=1, index_node=-1):
                locator_checkbox = L.keyframe_room.chx_maintain_aspect_ratio
                return set_attribute_checkbox(self, self.attribute_name, locator_checkbox, set_status, index_node)

            class Unit_Width_Height_Operation(BasePage):
                def __init__(self, attribute_name, locator_group, index_group, index_slider, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.attribute_name = attribute_name
                    self.locator_group = locator_group
                    self.index_group = index_group
                    self.index_slider = index_slider
                @step('[Action][KeyFrame Page][Clip Attributes][Scale][Unit Width Height Operation] Set value by slider')
                def set_slider(self, value, index_node=-1):
                    return set_attribute_slider_value(self, self.attribute_name, value, index_node, None, self.index_slider)
                @step('[Action][KeyFrame Page][Clip Attributes][Scale][Unit Width Height Operation] Get value')
                def set_value(self, value, index_node=-1):
                    return set_attribute_edittext_value(self, self.attribute_name, value, index_node, self.locator_group, self.index_group)
                @step('[Action][KeyFrame Page][Clip Attributes][Scale][Unit Width Height Operation] Get value')
                def get_value(self, index_node=-1):
                    return get_attribute_edittext_value(self, self.attribute_name, index_node, self.locator_group, self.index_group)
                @step('[Action][KeyFrame Page][Clip Attributes][Scale][Unit Width Height Operation] Click [Stepper Up] button')
                def click_stepper_up(self, times=1, index_node=-1):
                    return click_attribute_stepper(self, self.attribute_name, 'up', times, index_node, self.locator_group, self.index_group)
                @step('[Action][KeyFrame Page][Clip Attributes][Scale][Unit Width Height Operation] Click [Stepper Down] button')
                def click_stepper_down(self, times=1, index_node=-1):
                    return click_attribute_stepper(self, self.attribute_name, 'down', times, index_node, self.locator_group, self.index_group)

            class Ease_In(BasePage):
                def __init__(self, attribute_name, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.attribute_name = attribute_name

                def set_checkbox(self, set_status=1, index_node=-1):
                    locator_checkbox = L.keyframe_room.chx_ease_in
                    return set_attribute_checkbox(self, self.attribute_name, locator_checkbox, set_status, index_node)

                def set_slider(self, value, index_node=-1):
                    locator_slider = L.keyframe_room.slider_ease_in
                    return set_attribute_slider_value(self, self.attribute_name, value, index_node, locator_slider)

                def set_value(self, value, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_ease_in_out
                    return set_attribute_edittext_value(self, self.attribute_name, value, index_node, locator_group, 0)

                def get_value(self, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_ease_in_out
                    return get_attribute_edittext_value(self, self.attribute_name, index_node, locator_group, 0)

                def click_stepper_up(self, times=1, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_ease_in_out
                    return click_attribute_stepper(self, self.attribute_name, 'up', times, index_node, locator_group, 0)

                def click_stepper_down(self, times=1, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_ease_in_out
                    return click_attribute_stepper(self, self.attribute_name, 'down', times, index_node, locator_group, 0)

            class Ease_Out(BasePage):
                def __init__(self, attribute_name, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.attribute_name = attribute_name

                def set_checkbox(self, set_status=1, index_node=-1):
                    locator_checkbox = L.keyframe_room.chx_ease_out
                    return set_attribute_checkbox(self, self.attribute_name, locator_checkbox, set_status, index_node)

                def set_slider(self, value, index_node=-1):
                    locator_slider = L.keyframe_room.slider_ease_out
                    return set_attribute_slider_value(self, self.attribute_name, value, index_node, locator_slider)

                def set_value(self, value, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_ease_out
                    return set_attribute_edittext_value(self, self.attribute_name, value, index_node, locator_group, 0)

                def get_value(self, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_ease_out
                    return get_attribute_edittext_value(self, self.attribute_name, index_node, locator_group, 0)

                def click_stepper_up(self, times=1, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_ease_out
                    return click_attribute_stepper(self, self.attribute_name, 'up', times, index_node, locator_group, 0)

                def click_stepper_down(self, times=1, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_ease_out
                    return click_attribute_stepper(self, self.attribute_name, 'down', times, index_node, locator_group, 0)


        class Opacity(BasePage):
            def __init__(self, category, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.category_name = category
                self.attribute_name = 'Opacity'

            def show(self):
                set_category_fold_enable(self, self.category_name, 1)
                set_attribute_visible(self, self.attribute_name)
                return True
            @step('[Action][KeyFrame Page][Clip Attributes][Opacity] Set value')
            def set_value(self, value, index_node=-1):  # 0 - 100
                return set_attribute_edittext_value(self, self.attribute_name, value, index_node)
            @step('[Action][KeyFrame Page][Clip Attributes][Opacity] Get value')
            def get_value(self, index_node=-1):
                return get_attribute_edittext_value(self, self.attribute_name, index_node)
            @step('[Action][KeyFrame Page][Clip Attributes][Opacity] Set value by slider')
            def set_slider(self, value, index_node=-1):  # value: 0 - 100
                return set_attribute_slider_value(self, self.attribute_name, value, index_node)
            @step('[Action][KeyFrame Page][Clip Attributes][Opacity] Reset [Keyframe]')
            def reset_keyframe(self):
                return click_attribute_reset_keyframe(self, self.attribute_name)
            @step('[Action][KeyFrame Page][Clip Attributes][Opacity] Add/ Remove [Keyframe]')
            def add_remove_keyframe(self, index_node=-1):
                return click_attribute_add_remove_keyframe(self, self.attribute_name, index_node)
            @step('[Action][KeyFrame Page][Clip Attributes][Opacity] Click [Previous Keyframe]')
            def previous_keyframe(self, index_node=-1):
                return click_attribute_previous_keyframe(self, self.attribute_name, index_node)
            @step('[Action][KeyFrame Page][Clip Attributes][Opacity] Click [Next Keyframe]')
            def next_keyframe(self, index_node=-1):
                return click_attribute_next_keyframe(self, self.attribute_name, index_node)
            @step('[Action][KeyFrame Page][Clip Attributes][Opacity] Click [Stepper Up] button')
            def click_stepper_up(self, times=1, index_node=-1):
                return click_attribute_stepper(self, self.attribute_name, 'up', times, index_node)
            @step('[Action][KeyFrame Page][Clip Attributes][Opacity] Click [Stepper Down] button')
            def click_stepper_down(self, times=1, index_node=-1):
                return click_attribute_stepper(self, self.attribute_name, 'down', times, index_node)
            @step('[Action][KeyFrame Page][Clip Attributes][Opacity] Set [Blending Mode]')
            def set_blending_mode(self, index_option=1, index_node=-1):
                return select_attribute_combobox_option(self, self.attribute_name, index_option, index_node)
            @step('[Action][KeyFrame Page][Clip Attributes][Opacity] Get [Blending Mode]')
            def get_blending_mode(self, index_node=-1):
                return get_attribute_combobox_option(self, self.attribute_name, index_node)

        class Rotation(BasePage):
            def __init__(self, category, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.category_name = category
                self.attribute_name = 'Rotation'
                self.ease_in = self.Ease_In(self.attribute_name, *args, **kwargs)
                self.ease_out = self.Ease_Out(self.attribute_name, *args, **kwargs)

            def show(self):
                set_category_fold_enable(self, self.category_name, 1)
                set_attribute_visible(self, self.attribute_name)
                return True
            @step('[Action][KeyFrame Page][Clip Attributes][Rotation] Add/ Remove [Keyframe]')
            def add_remove_keyframe(self, index_node=-1):
                return click_attribute_add_remove_keyframe(self, self.attribute_name, index_node)
            @step('[Action][KeyFrame Page][Clip Attributes][Rotation] Reset [Keyframe]')
            def reset_keyframe(self):
                return click_attribute_reset_keyframe(self, self.attribute_name)
            @step('[Action][KeyFrame Page][Clip Attributes][Rotation] Click [Previous Keyframe]')
            def previous_keyframe(self, index_node=-1):
                return click_attribute_previous_keyframe(self, self.attribute_name, index_node)
            @step('[Action][KeyFrame Page][Clip Attributes][Rotation] Click [Next Keyframe]')
            def next_keyframe(self, index_node=-1):
                return click_attribute_next_keyframe(self, self.attribute_name, index_node)
            @step('[Action][KeyFrame Page][Clip Attributes][Rotation] Set value')
            def set_value(self, value, index_node=-1):
                return set_attribute_edittext_value(self, self.attribute_name, value, index_node)
            @step('[Action][KeyFrame Page][Clip Attributes][Rotation] Set value by slider')
            def get_value(self, index_node=-1):
                return get_attribute_edittext_value(self, self.attribute_name, index_node)
            @step('[Action][KeyFrame Page][Clip Attributes][Rotation] Click [Stepper Up] button')
            def click_stepper_up(self, times=1, index_node=-1):
                return click_attribute_stepper(self, self.attribute_name, 'up', times, index_node)
            @step('[Action][KeyFrame Page][Clip Attributes][Rotation] Click [Stepper Down] button')
            def click_stepper_down(self, times=1, index_node=-1):
                return click_attribute_stepper(self, self.attribute_name, 'down', times, index_node)

            class Ease_In(BasePage):
                def __init__(self, attribute_name, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.attribute_name = attribute_name

                def set_checkbox(self, set_status=1, index_node=-1):
                    locator_checkbox = L.keyframe_room.chx_ease_in
                    return set_attribute_checkbox(self, self.attribute_name, locator_checkbox, set_status, index_node)

                def set_slider(self, value, index_node=-1):
                    locator_slider = L.keyframe_room.slider_ease_in
                    return set_attribute_slider_value(self, self.attribute_name, value, index_node, locator_slider)

                def set_value(self, value, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_ease_in_out
                    return set_attribute_edittext_value(self, self.attribute_name, value, index_node, locator_group, 0)

                def get_value(self, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_ease_in_out
                    return get_attribute_edittext_value(self, self.attribute_name, index_node, locator_group, 0)

                def click_stepper_up(self, times=1, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_ease_in_out
                    return click_attribute_stepper(self, self.attribute_name, 'up', times, index_node, locator_group, 0)

                def click_stepper_down(self, times=1, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_ease_in_out
                    return click_attribute_stepper(self, self.attribute_name, 'down', times, index_node, locator_group, 0)

            class Ease_Out(BasePage):
                def __init__(self, attribute_name, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.attribute_name = attribute_name

                def set_checkbox(self, set_status=1, index_node=-1):
                    locator_checkbox = L.keyframe_room.chx_ease_out
                    return set_attribute_checkbox(self, self.attribute_name, locator_checkbox, set_status, index_node)

                def set_slider(self, value, index_node=-1):
                    locator_slider = L.keyframe_room.slider_ease_out
                    return set_attribute_slider_value(self, self.attribute_name, value, index_node, locator_slider)

                def set_value(self, value, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_ease_out
                    return set_attribute_edittext_value(self, self.attribute_name, value, index_node, locator_group, 0)

                def get_value(self, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_ease_out
                    return get_attribute_edittext_value(self, self.attribute_name, index_node, locator_group, 0)

                def click_stepper_up(self, times=1, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_ease_out
                    return click_attribute_stepper(self, self.attribute_name, 'up', times, index_node, locator_group, 0)

                def click_stepper_down(self, times=1, index_node=-1):
                    locator_group = L.keyframe_room.group_edittext_stepper_ease_out
                    return click_attribute_stepper(self, self.attribute_name, 'down', times, index_node, locator_group, 0)

        class Freeform(BasePage):
            def __init__(self, category, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.category_name = category
                self.attribute_name = 'Freeform*'
                self.top_left_x = self.Adjust_Operation(0, *args, **kwargs)
                self.top_left_y = self.Adjust_Operation(1, *args, **kwargs)
                self.top_right_x = self.Adjust_Operation(2, *args, **kwargs)
                self.top_right_y = self.Adjust_Operation(3, *args, **kwargs)
                self.bottom_left_x = self.Adjust_Operation(4, *args, **kwargs)
                self.bottom_left_y = self.Adjust_Operation(5, *args, **kwargs)
                self.bottom_right_x = self.Adjust_Operation(6, *args, **kwargs)
                self.bottom_right_y = self.Adjust_Operation(7, *args, **kwargs)

            def show(self):
                set_category_fold_enable(self, self.category_name, 1)
                set_attribute_visible(self, self.attribute_name)
                return True

            def reset_keyframe(self):
                return click_attribute_reset_keyframe(self, self.attribute_name)

            def add_remove_keyframe(self, index_node=-1):
                return click_attribute_add_remove_keyframe(self, self.attribute_name, index_node)

            def previous_keyframe(self, index_node=-1):
                return click_attribute_previous_keyframe(self, self.attribute_name, index_node)
            @step('[Action][KeyFrame Page][Clip Attributes][Freeform] Click [Next Keyframe]')
            def next_keyframe(self, index_node=-1):
                return click_attribute_next_keyframe(self, self.attribute_name, index_node)

            class Adjust_Operation(BasePage):
                def __init__(self, index_group, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.attribute_name = 'Freeform*'
                    self.locator_group = L.keyframe_room.group_edittext_stepper_xy
                    self.index_group = index_group
                @step('[Action][KeyFrame Page][Clip Attributes][Freeform][Adjust Operation] Set value')
                def set_value(self, value, index_node=-1):
                    return set_attribute_edittext_value(self, self.attribute_name, value, index_node, self.locator_group, self.index_group)
                @step('[Action][KeyFrame Page][Clip Attributes][Freeform][Adjust Operation] Get value')
                def get_value(self, index_node=-1):
                    return get_attribute_edittext_value(self, self.attribute_name, index_node, self.locator_group, self.index_group)
                @step('[Action][KeyFrame Page][Clip Attributes][Freeform][Adjust Operation] Click [Stepper Up] button')
                def click_stepper_up(self, times=1, index_node=-1):
                    return click_attribute_stepper(self, self.attribute_name, 'up', times, index_node, self.locator_group, self.index_group)
                @step('[Action][KeyFrame Page][Clip Attributes][Freeform][Adjust Operation] Click [Stepper Down] button')
                def click_stepper_down(self, times=1, index_node=-1):
                    return click_attribute_stepper(self, self.attribute_name, 'down', times, index_node, self.locator_group, self.index_group)

    class Volume(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.category_name = 'Volume'
            self.attribute_name = 'dB'

        @step('[Action][KeyFrame Page][Volume] Unfold/ Fold [Volume] Tab')
        def unfold_tab(self, value=1): # value: 1(unfold), 0(fold)
            return set_category_fold_enable(self, self.category_name, value)

        def get_unfold_status(self): # True: unfold, False: fold
            return bool(get_category_fold_status(self, self.category_name))

        def show(self):
            set_category_fold_enable(self, self.category_name, 1)
            set_attribute_visible(self, self.attribute_name)
            return True

        def reset_keyframe(self):
            return click_attribute_reset_keyframe(self, self.attribute_name)

        def add_remove_keyframe(self, index_node=-1):
            return click_attribute_add_remove_keyframe(self, self.attribute_name, index_node)

        def previous_keyframe(self, index_node=-1):
            return click_attribute_previous_keyframe(self, self.attribute_name, index_node)

        def next_keyframe(self, index_node=-1):
            return click_attribute_next_keyframe(self, self.attribute_name, index_node)

        def set_slider(self, value, index_node=-1):  # value: 0 - 100 (0: -∞, 1:-28, 25:0, 100:12)
            return set_attribute_slider_value(self, self.attribute_name, value, index_node)
        @step('[Action][KeyFrame Page][Volume] Set [Volume] Value')
        def set_value(self, value, index_node=-1):
            return set_attribute_edittext_value(self, self.attribute_name, value, index_node)

        @step('[Action][KeyFrame Page][Volume] Get [Volume] Value')
        def get_value(self, index_node=-1):
            return get_attribute_edittext_value(self, self.attribute_name, index_node)

        def click_stepper_up(self, times=1, index_node=-1):
            return click_attribute_stepper(self, self.attribute_name, 'up', times, index_node)

        def click_stepper_down(self, times=1, index_node=-1):
            return click_attribute_stepper(self, self.attribute_name, 'down', times, index_node)

    class Effect(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.category_name = 'Effect'
            self.aberration = self.Aberration(self.category_name, *args, **kwargs)

        def unfold_tab(self, value=1): # value: 1(unfold), 0(fold)
            return set_category_fold_enable(self, self.category_name, value)

        def get_unfold_status(self): # True: unfold, False: fold
            return bool(get_category_fold_status(self, self.category_name))

        def show(self):
            set_category_visible(self, self.category_name)
            return True

        class Aberration(BasePage):
            def __init__(self, root_category, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.root_category = root_category
                self.category_name = 'Aberration'
                self.frequency = self.Unit_Operation(self.root_category, self.category_name, 'Frequency', *args, **kwargs)
                self.strength = self.Unit_Operation(self.root_category, self.category_name, 'Strength', *args, **kwargs)

            def show(self):
                set_category_fold_enable(self, self.root_category, 1)
                set_category_visible(self, self.category_name)
                return True

            class Unit_Operation(BasePage):
                def __init__(self, root_category, category_name, attribute_name, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.root_category = root_category
                    self.category_name = category_name
                    self.attribute_name = attribute_name

                def set_value(self, value, index_node=-1): # 0 - 100
                    return set_attribute_edittext_value(self, self.attribute_name, value, index_node)

                def get_value(self, index_node=-1):
                    return get_attribute_edittext_value(self, self.attribute_name, index_node)

                def set_slider(self, value, index_node=-1): # value: 0 - 100
                    return set_attribute_slider_value(self, self.attribute_name, value, index_node)

                def reset_keyframe(self):
                    return click_attribute_reset_keyframe(self, self.attribute_name)

                def add_remove_keyframe(self, index_node=-1):
                    return click_attribute_add_remove_keyframe(self, self.attribute_name, index_node)

                def previous_keyframe(self, index_node=-1):
                    return click_attribute_previous_keyframe(self, self.attribute_name, index_node)

                def next_keyframe(self, index_node=-1):
                    return click_attribute_next_keyframe(self, self.attribute_name, index_node)

                def click_stepper_up(self, times=1, index_node=-1):
                    return click_attribute_stepper(self, self.attribute_name, 'up', times, index_node)

                def click_stepper_down(self, times=1, index_node=-1):
                    return click_attribute_stepper(self, self.attribute_name, 'down', times, index_node)

                def show(self):
                    set_category_fold_enable(self, self.root_category, 1)
                    set_category_fold_enable(self, self.category_name, 1)
                    set_attribute_visible(self, self.attribute_name)