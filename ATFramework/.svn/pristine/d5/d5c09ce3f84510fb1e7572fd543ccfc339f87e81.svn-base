import autoit
import os
import ctypes
import tempfile
import cv2
import re
from PIL import ImageGrab
import uuid
import time
import win32gui
import psutil
import shutil
import stat
import winreg
import pyautogui
import threading
import numpy as np
from types import SimpleNamespace
import hashlib
import uiautomation as auto
from ..utils import logger
from ..utils import Pip

try:
    import ffmpeg_quality_metrics as ffqm
except:
    logger("Initial system, please wait")
    Pip().install("ffmpeg_quality_metrics").wait().apply("ffqm")

# for FFMpeg, install tool first
#  - https://www.gyan.dev/ffmpeg/builds/
# extract the zip file to C:\ and add the C:\ffmpeg\bin to system path

# disable uiautomation logging file
auto.Logger.SetLogFile('')
# disable uiautomation function exist()'s waiting log
UIAutomation_Exist_Log = False

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
current_dpi = user32.GetDpiForSystem()
dpi_ratio = current_dpi / 96
screen_w, screen_h = int(user32.GetSystemMetrics(0) / dpi_ratio), int(user32.GetSystemMetrics(1) / dpi_ratio)

temp_dir = os.path.abspath(tempfile.gettempdir() + "/win32_driver")
os.makedirs(temp_dir, exist_ok=True)

WM_USER = 1024
UM_AUTOTESTING_SET_CGBUTTON_CHECK   = WM_USER + 20010
UM_AUTOTESTING_IS_CTRL_ENABLE       = WM_USER + 20034


WIN_STATE_EXISTS = 1
WIN_STATE_VISIBLE = 2
WIN_STATE_ENABLED = 4
WIN_STATE_ACTIVE = 8
WIN_STATE_MINIMIZED = 16
WIN_STATE_MAXIMIZED = 32

# Locator structure
# - Base on list structure AutoIt style locator type
# - e.g. ["[CLASS:VIDEOEDITOR]"]
# - e.g. btn_media_room = ["[CLASS:VIDEOEDITOR]", "[ID:1982]"]


class Win32:
    def __init__(self, app_path, process_name=''):
        self.app_path = app_path
        self.process_name = process_name
        self.mouse = Mouse()
        self.image = Image()
        self.video = Video()
        self.keyboard = Keyboard()
        self.size = {"w": screen_w, "h": screen_h}
        self.file = File()
        self.driver_type = 'autoit'

    def check_if_process_running(self, process_name=''):
        '''
        Check if there is any running process that contains the given name processName.
        '''
        # Iterate over the all the running process
        if not process_name:
            process_name = self.process_name
        for proc in psutil.process_iter():
            try:
                # Check if process name contains the given name string.
                if process_name.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def close_process(self, process_name=''):
        if not process_name:
            process_name = self.process_name
        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == process_name:
                proc.kill()
        return True

    def exist(self, locator):
        control_handle = None
        try:
            if isinstance(locator, str) or (isinstance(locator, list) and len(locator) == 1):  # locator of windows
                if isinstance(locator, list):
                    locator = locator[0]
                control_handle = autoit.win_get_handle(locator)
            else:  # locator of control
                wnd_handle = autoit.win_get_handle(locator[0])
                sub_locator = locator[1:]
                if len(sub_locator) == 1:
                    control_handle = self.get_visible_control_handle(wnd_handle, *sub_locator)
                else:
                    for locator in sub_locator:  # locator - "[ID:xxxxx]"
                        logger(f'{wnd_handle=}, {locator=}, {control_handle=}')
                        control_handle = None
                        control_handle = self.get_visible_control_handle(wnd_handle, locator)
                        logger(f'get control handle={control_handle}')
                        wnd_handle = control_handle
        except Exception as e:
            # logger(f'Exception occurs. Error={e}')
            pass
        return control_handle

    @staticmethod
    def get_visible_control_handle(hwnd, control_id):
        h_ctrl = None
        controls = []
        control_id = int(re.findall(r"(\d+)", control_id)[0])
        # print(f'{control_id=}')

        def enum_controls(hwnd, lParam):
            tmp_ctrl_id = win32gui.GetDlgCtrlID(hwnd)
            controls.append((hwnd, tmp_ctrl_id))
            return True

        win32gui.EnumChildWindows(hwnd, enum_controls, None)

        for control in controls:
            hwnd, ctrl_id = control
            if ctrl_id == control_id and win32gui.IsWindowVisible(hwnd):
                h_ctrl = hwnd

        return h_ctrl

    def is_exist(self, locator):
        return bool(self.exist(locator))

    def wait_exist(self, locator, timeout=10, delay_sec=0):
        result = False
        handle = None
        time_start = time.time()
        while time.time() - time_start < timeout:
            handle = self.exist(locator)
            if handle:
                break
            time.sleep(delay_sec)
        return handle

    def wait_not_exist(self, locator, timeout=10, delay_sec=0):
        result = False
        time_start = time.time()
        while time.time() - time_start < timeout:
            if not self.is_exist(locator):
                result = True
                break
            time.sleep(delay_sec)
        return result

    def win_wait_state(self, locator, state=WIN_STATE_VISIBLE, timeout=10):
        try:
            start_time = time.time()
            is_match_state = False
            while time.time() - start_time < timeout:
                if handle := self.exist(locator):
                    if autoit.win_get_state_by_handle(handle) & state:
                        is_match_state = True
                        break
            if not is_match_state:
                logger(f'Window {locator} not match state - Timeout.')
                raise Exception(f'Window {locator} not match state - Timeout.')
        except Exception as e:
            logger(f'Exception occurs. Error={e}')
            raise
        return True

    def wait_visible(self, locator, timeout=10):
        try:
            self.win_wait_state(locator, WIN_STATE_VISIBLE, timeout)
        except:
            return False
        return True

    def wait_active(self, locator, timeout=10):
        return self.win_wait_state(locator, WIN_STATE_ACTIVE, timeout)

    def click(self, locator, offset_x=0, offset_y=0):
        try:
            rect = self.control_get_rect(locator)
            x = rect[0] + int(rect[2]/2)
            y = rect[1] + int(rect[3]/2)
            self.mouse.click(x+offset_x, y+offset_y)
        except Exception as e:
            logger(f'Exception occurs. Error={e}')
            raise
        return True

    def hover(self, locator, offset_x=0, offset_y=0):
        try:
            rect = self.control_get_rect(locator)
            x = rect[0] + int(rect[2]/2)
            y = rect[1] + int(rect[3]/2)
            self.mouse.move(x+offset_x, y+offset_y)
        except Exception as e:
            logger(f'Exception occurs. Error={e}')
            raise
        return True

    def control_get_rect(self, locator):
        try:
            # logger(f'{locator=}')
            handle_wnd = autoit.win_get_handle(locator[0])
            left_top_x_wnd, left_top_y_wnd, bottom_right_x_wnd, bottom_right_y_wnd = autoit.win_get_pos_by_handle(
                handle_wnd)
            x_wnd, y_wnd, w_wnd, h_wnd = left_top_x_wnd, left_top_y_wnd, bottom_right_x_wnd - left_top_x_wnd, bottom_right_y_wnd - left_top_y_wnd
            # logger(f'Wnd Handle={handle_wnd}, {x_wnd=}, {y_wnd=}, {w_wnd=}, {h_wnd=}')
            handle_control = self.exist(locator)
            left_top_x, left_top_y, bottom_right_x, bottom_right_y = autoit.control_get_pos_by_handle(handle_wnd,
                                                                                                      handle_control)
            x, y, w, h = left_top_x, left_top_y, bottom_right_x - left_top_x, bottom_right_y - left_top_y
            # logger(f'Control Handle={handle_control}, {x=}, {y=}, {w=}, {h=}')
        except Exception as e:
            logger(f'Exception occurs. Error={e}')
            raise
        return x+x_wnd, y+y_wnd, w, h

    def control_get_text(self, locator):
        text = ''
        try:
            if len(locator) == 2:
                hwnd = autoit.win_get_handle(locator[0])
            else:
                hwnd = self.exist(locator[:-1])
            h_ctrl = self.exist(locator)
            text = autoit.control_get_text_by_handle(hwnd, h_ctrl)
        except Exception as e:
            logger(f'Exception occurs. Error={e}')
            raise
        return text

    def control_set_text(self, locator, text):
        try:
            if len(locator) == 2:
                hwnd = autoit.win_get_handle(locator[0])
            else:
                hwnd = self.exist(locator[:-1])
            h_ctrl = self.exist(locator)
            autoit.control_set_text_by_handle(hwnd, h_ctrl, text)
        except Exception as e:
            logger(f'Exception occurs. Error={e}')
            raise
        return True

    def wnd_get_rect(self, locator):
        try:
            # logger(f'{locator=}')
            pos = autoit.win_get_pos(locator[0])  # left_top (x,y), bottom_right (x,y)
            # logger(f'Position={pos}')
            x, y, w, h = pos[0], pos[1], pos[2] - pos[0], pos[3] - pos[1]
            # logger(f'Wnd Handle={handle_wnd}, {x=}, {y=}, {w=}, {h=}')
        except Exception as e:
            logger(f'Exception occurs. Error={e}')
            raise
        return x, y, w, h

    def activate(self, locator):
        autoit.win_activate(locator[0])
        return True

    def win_wait_active(self, locator, timeout):
        autoit.win_wait_active(locator[0], timeout)
        return True

    def close(self, locator):
        autoit.win_close(locator[0])
        return True

    @staticmethod
    def select_menu_item(name):  # using uiautomation driver
        auto.MenuItemControl(Name=f'{name}\t').Click()
        return True

    @staticmethod
    def select_menu_item_v2(name):  # using uiautomation driver
        auto.MenuItemControl(Name=f'{name}').Click()
        return True

    def select_combobox_item(self, name):
        auto.ListItemControl(Name=f'{name}').Click()
        return True

    def _post_message(self, hwnd, i_msg, w_param=0, l_param=0):
        print(f'{hwnd=}, {i_msg=}, {w_param=}')
        user32.PostMessageW(hwnd, i_msg, w_param, l_param)
        return True

    def set_checkbox(self, hwnd, is_check=1):
        return self._post_message(hwnd, UM_AUTOTESTING_SET_CGBUTTON_CHECK, is_check)


class UIAutomation:
    def __init__(self, app_path, process_name):
        self.app_path = app_path
        self.process_name = process_name
        self.auto = auto
        self.mouse = Mouse()
        self.image = Image()
        self.video = Video()
        self.keyboard = Keyboard()
        self.win_registry = WinRegistry()
        self.size = {"w": screen_w, "h": screen_h}
        self.file = File()
        self.driver_type = 'uiautomation'
        self.recording_flag = False
        self.recording_thread = None

    def _generate_call_item(self, locator):  # locator - {'ControlType': '', 'ClassName': '', 'AutomationId'= ''}
        element_property = ''
        func_sibling_list = ['GetParentControl', 'GetFirstChildControl', 'GetLastChildControl', 'GetNextSiblingControl', 'GetPreviousSiblingControl']
        func_sibling = ''
        func_category = f'{locator["ControlType"]}'
        for elem in locator.keys():
            if elem in func_sibling_list:
                for i in range(locator[elem]):
                    func_sibling += f'.{elem}()'
            elif elem != 'ControlType':
                if element_property:
                    if isinstance(locator[elem], int):
                        element_property += f',{elem}={locator[elem]}'
                    else:
                        element_property += f',{elem}=\"{locator[elem]}\"'
                else:
                    if isinstance(locator[elem], int):
                        element_property += f'{elem}={locator[elem]}'
                    else:
                        element_property += f'{elem}=\"{locator[elem]}\"'
        call_item = f'{func_category}({element_property}){func_sibling}'
        # logger(f'{call_item=}')
        return call_item

    def _generate_call_sequence(self, locator, is_dict=True):
        call_sequence = 'auto' if is_dict else ''
        if isinstance(locator, dict):
            call_sequence += f'.{self._generate_call_item(locator)}'
        if isinstance(locator, list):
            for sub_locator in locator:
                call_sequence += self._generate_call_sequence(sub_locator, False)
        # logger(f'{call_sequence=}')
        return call_sequence

    def exist(self, locator, timeout=3, exist_flag=True):
        obj_elem = eval(self._generate_call_sequence(locator))
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                if obj_elem.Exists(maxSearchSeconds=0.5):
                    return obj_elem
                if UIAutomation_Exist_Log:
                    logger(f'Find element fail, retrying... {locator=}')
            except Exception as e:
                logger(f"Exception encountered: {e}, retrying...")
            # time.sleep(0.5)
        if exist_flag:
            logger(f'Find element Fail, {locator=}')
        return None

    def is_exist(self, locator, timeout=5):
        return bool(self.exist(locator, timeout, False))

    def is_not_exist(self, locator, timeout=5):
        result = False
        time_start = time.time()
        while time.time() - time_start < timeout:
            if not self.exist(locator, 1, False):
                result = True
                break
        return result

    def prev_exist(self, locator, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
            if not obj_elem:
                logger(f'Find element Fail, {locator=}')
                return None
        prev_obj_elem = obj_elem.GetPreviousSiblingControl()
        if not prev_obj_elem:
            logger(f'Find previous element Fail, {locator=}')
            prev_obj_elem = None
        return prev_obj_elem

    def next_exist(self, locator, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
            if not obj_elem:
                logger(f'Find element Fail, {locator=}')
                return None
        next_obj_elem = obj_elem.GetNextSiblingControl()
        if not next_obj_elem:
            logger(f'Find next element Fail, {locator=}')
            next_obj_elem = None
        return next_obj_elem

    def click(self, locator, timeout=5, mouse_move=True):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        return obj_elem.Click(simulateMove=mouse_move)

    def exist_click(self, locator, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if obj_elem:
            obj_elem.Click()
        return True

    def right_click(self, locator, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        return obj_elem.RightClick()

    def double_click(self, locator, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        return obj_elem.DoubleClick()

    def drag_locator(self, locator, offset_x, offset_y, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        x, y = obj_elem.GetPosition()
        des_x, des_y = x + offset_x, y + offset_y
        return auto.DragDrop(x, y, des_x, des_y)

    def drag_to(self, x, y, offset_x, offset_y):
        des_x, des_y = x + offset_x, y + offset_y
        return auto.DragDrop(x, y, des_x, des_y)

    def move_to_locator(self, locator, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        return obj_elem.MoveCursorToMyCenter()

    def move_to(self, x, y):
        return auto.MoveTo(x, y)

    def wheel_up(self, locator, wheel_time=1, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        return obj_elem.WheelUp(wheelTimes=wheel_time)

    def wheel_down(self, locator, wheel_time=1, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        return obj_elem.WheelDown(wheelTimes=wheel_time)

    def get_position(self, locator, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        return obj_elem.GetPosition()

    def get_rect(self, locator, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        return obj_elem.BoundingRectangle

    def get_name(self, locator, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        return obj_elem.Name

    def get_value(self, locator, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        return obj_elem.GetValuePattern().Value

    def get_enabled(self, locator, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        return bool(obj_elem.IsEnabled)

    def get_offscreen(self, locator, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        return bool(obj_elem.IsOffscreen)

    def get_state(self, locator, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        return obj_elem.GetLegacyIAccessiblePattern().State

    def get_selected(self, locator, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        return obj_elem.GetSelectionItemPattern().IsSelected

    def get_handle(self, locator, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        return obj_elem.NativeWindowHandle

    def get_range_value(self, locator, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        return obj_elem.GetRangeValuePattern().Value

    def select_item_in_cbx(self, locator, item_name, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if obj_elem:
            logger(f'Find element Fail, {locator=}')
        if not obj_elem.Select(item_name):
            logger(f'Select item Fail, {item_name=}')
            return False
        return True

    def get_child_control_list(self, locator, is_tree=False, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        if is_tree:
            child_control_list = []
            for c, d in self.auto.WalkControl(obj_elem, False):
                child_control_list.append(c)
            if not child_control_list:
                logger(f'No child control found, {locator=}')
                return None
            return child_control_list
        child_control_list = obj_elem.GetChildren()
        if not child_control_list:
            logger(f'No child control found, {locator=}')
            return None
        return child_control_list

    def get_sibling_control_list(self, locator, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        obj_elem_parent = obj_elem.GetParentControl()
        sibling_control_list = obj_elem_parent.GetChildren()
        if not sibling_control_list:
            logger(f'Find sibling element Fail, {locator=}')
            return None
        return sibling_control_list

    def get_sibling_control(self, locator, condition='condition_type', control_type='EditControl', control_name='', forward=True, idx=0, timeout=5):
        def condition_type(control):
            return control.ControlTypeName == control_type

        def condition_name(control):
            return control_name in control.Name

        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        control_list = []
        control_obj = obj_elem.GetSiblingControl(eval(condition), forward)
        control_list.append(control_obj)
        if not control_obj:
            logger(f"No element with {condition} of {control_type}/{control_name} with 1 item by {forward} direction.")
            return None
        i = 0
        while i < idx:
            control_obj = control_obj.GetSiblingControl(eval(condition), forward)
            if not control_obj:
                logger(f"No element with {condition} of {control_type}/{control_name} with {i+1} item by {forward} direction.")
                break
            control_list.append(control_obj)
            i += 1
        if not control_list:
            logger(f'No element with {condition} of {control_type}/{control_name} found, {locator=}')
            return None
        return control_list

    def get_parent_control(self, locator, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        parent_obj_elem = obj_elem.GetParentControl()
        if not parent_obj_elem:
            logger(f'Find parent element Fail, {locator=}')
            return None
        return parent_obj_elem

    def get_first_child_control(self, locator, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        parent_obj_elem = obj_elem.GetFirstChildControl()
        if not parent_obj_elem:
            logger(f'Find first child element Fail, {locator=}')
            return None
        return parent_obj_elem

    def get_last_child_control(self, locator, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        parent_obj_elem = obj_elem.GetLastChildControl()
        if not parent_obj_elem:
            logger(f'Find last child element Fail, {locator=}')
            return None
        return parent_obj_elem

    def capture_locator(self, locator, file_path, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        if not os.path.isdir(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        return obj_elem.CaptureToImage(file_path)

    def check_if_process_running(self, process_name=''):
        '''
        Check if there is any running process that contains the given name processName.
        '''
        # Iterate over the all the running process
        if not process_name:
            process_name = self.process_name
        for proc in psutil.process_iter():
            try:
                # Check if process name contains the given name string.
                if process_name.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def check_if_process_is_not_running(self, process_name='', timeout=5):
        """
        Check if there is any running process that contains the given name processName.
        """
        if not process_name:
            process_name = self.process_name
        for _ in range(timeout):
            if not self.check_if_process_running(process_name):
                return True
            time.sleep(1)
        return False

    def close_process(self, process_name=''):
        if not process_name:
            process_name = self.process_name
        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == process_name:
                proc.kill()
        return True

    def launch(self, program_path='', delay_sec=3):
        program_path = program_path or self.app_path
        try:
            cmd_list = f"\"{program_path}\""
            os.popen(cmd_list)
            time.sleep(delay_sec)
        except Exception as e:
            logger(f'Exception occurs. Error={e}')
            raise Exception
        return True

    def close(self, locator, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        if obj_elem.ControlTypeName != 'WindowControl':
            logger(f'Locator is not WindowControl type, {locator=}')
        return obj_elem.GetWindowPattern().Close()

    def focus(self, locator, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        return obj_elem.SetFocus()

    def maximize(self, locator, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        if not obj_elem.IsTopLevel():
            logger(f'Locator is not TopLevel type, {locator=}')
        return obj_elem.Maximize()

    def minimize(self, locator, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        if not obj_elem.IsTopLevel():
            logger(f'Locator is not TopLevel type, {locator=}')
        return obj_elem.Minimize()

    def restore(self, locator, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        if not obj_elem.IsTopLevel():
            logger(f'Locator is not TopLevel type, {locator=}')
        return obj_elem.Restore()

    def set_active(self, locator, timeout=5):
        obj_elem = locator
        if isinstance(locator, (list, dict)):
            obj_elem = self.exist(locator, timeout, False)
        if not obj_elem:
            logger(f'Find element Fail, {locator=}')
        if not obj_elem.IsTopLevel():
            logger(f'Locator is not TopLevel type, {locator=}')
        return obj_elem.SetActive()

    def get_screenshot_as_file(self, file_path):
        self.image.screenshot(file_path)

    def record_operations_start(self, func_name="default_name", file_path=os.getcwd(), udid="unknown"):
        if self.recording_flag is False:
            self.recording_flag = True
            self.recording_thread = threading.Thread(target=self.record_operations, args=(func_name, file_path, udid))
            self.recording_thread.start()
            time.sleep(0.5)

    def record_operations(self, func_name="default_name", file_path=os.getcwd(), udid="unknown"):
        # get screen size
        screen_size = tuple(pyautogui.size())
        # define the codec
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        # frames per second
        fps = 12
        # create the video path
        record_path = file_path + "/report/" + udid + "/screen_records"
        os.makedirs(record_path, exist_ok=True)
        # create the video writer object
        out = cv2.VideoWriter(record_path + "/" + func_name + ".mp4", fourcc, fps, screen_size)
        while True:
            for i in range(int(fps)):
                # make a screenshot
                img = pyautogui.screenshot()
                # convert these pixels to a proper numpy array to work with OpenCV
                frame = np.array(img)
                # convert colors from BGR to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # write the frame
                out.write(frame)
            # Stop recording loop depends on flag
            if self.recording_flag is False:
                break
        # make sure everything is closed when exited
        out.release()

    def record_operations_end(self, func_name="default_name", file_path=os.getcwd(), udid="unknown", keep=False):
        if self.recording_flag is True:
            self.recording_flag = False
            self.recording_thread.join()
        record_file = file_path + "/report/" + udid + "/screen_records/" + func_name + ".mp4"
        if os.path.exists(record_file) and not keep:
            os.remove(record_file)
        self.recording_thread = None


class Image:
    def __init__(self):
        pass

    @staticmethod
    def echo():
        print('echo Image class')
        return True

    def snapshot(self, file_name=None, x=0, y=0, w=screen_w - 1, h=screen_h - 1, format="png", raw=False, type=-1):
        try:
            if not file_name:
                file_fullname = f"{temp_dir}/{uuid.uuid4()}.{format}"
            else:
                file_fullname = os.path.abspath(f'{file_name}')
            os.makedirs(os.path.dirname(file_fullname), exist_ok=True)

            x, y, w, h = map(lambda n: int(max(n, 0)), [x, y, w, h])
            im = ImageGrab.grab()
            im.save(file_fullname)
            img = cv2.imread(file_fullname, type)
            org_h, org_w = img.shape[:2]
            if screen_w != org_h or screen_h != org_w:
                img = cv2.resize(img, (screen_w, screen_h), interpolation=cv2.INTER_LINEAR)
            img = img[y:y + h, x:x + w]
            if raw:
                return img
            else:
                cv2.imwrite(file_fullname, img)
                return file_fullname
        except Exception as e:
            logger(f'[Error] => {e}')
            return False

    def screenshot(self, *args, **kwargs):
        return self.snapshot(*args, **kwargs)

    def search(self, source, target, center=True, color=False, screen_ratio=1, _mode=5):
        """
        cv:: IMREAD_UNCHANGED = -1，
        cv:: IMREAD_GRAYSCALE = 0，
        cv:: IMREAD_COLOR = 1，
        cv:: IMREAD_ANYDEPTH = 2，
        cv:: IMREAD_ANYCOLOR = 4，
        cv:: IMREAD_LOAD_GDAL = 8
        """
        s = cv2.imread(source, [cv2.IMREAD_GRAYSCALE, cv2.IMREAD_COLOR][color])
        t = cv2.imread(target, [cv2.IMREAD_GRAYSCALE, cv2.IMREAD_COLOR][color])
        h, w = t.shape[:2]

        try:
            res = cv2.matchTemplate(s, t, _mode)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if max_val == 0:
                logger("Pure image detected, switch to advanced mode")
                ret = self.search(source, target, center, True, screen_ratio, _mode=2)
                max = ret.w * ret.h * 3 * 255 * 255
                # logger(f"{ret=} / {max=}")
                ret.similarity = (max - ret.similarity) / max
                return ret
        except:
            return None

        # print(min_val, max_val, min_loc, max_loc )
        ret = {
            "x": int((max_loc[0] + w / 2) / screen_ratio) if center else 0,
            "y": int((max_loc[1] + h / 2) / screen_ratio) if center else 0,
            "similarity": (max_val + 1) / 2,
            "w": int(w / screen_ratio),
            "h": int(h / screen_ratio),
        }
        return SimpleNamespace(**ret)


class Video:
    def __init__(self):
        pass

    @staticmethod
    def echo():
        print('echo Video class')
        return True

    def compare(self, source, target):
        source = os.path.abspath(source)
        target = os.path.abspath(target)
        try:
            psnr, ssim = [v for _, v in ffqm.FfmpegQualityMetrics(source, target).calculate(["ssim", "psnr"]).items()]
        except FileNotFoundError:
            logger("[ERROR] " + "*" * 65)
            logger("[ERROR] ** Please install FFmpeg via 'https://www.gyan.dev/ffmpeg/builds/' **")
            logger("[ERROR] " + "*" * 65)
            raise FileNotFoundError("Please install FFmpeg via 'https://www.gyan.dev/ffmpeg/builds/' ")

        ssim_avg = sum([x['ssim_avg'] for x in ssim]) / len(ssim)
        psnr_avg = sum([x['psnr_avg'] for x in psnr]) / len(ssim)
        logger(f"{psnr_avg=}, {ssim_avg=}, length = {ssim[-1]['n']} frames")
        return psnr_avg > 40.0 and ssim_avg > 0.9


class Mouse:
    def __init__(self):
        pass

    @staticmethod
    def echo():
        print('echo Mouse class')
        return True

    def click(self, x=None, y=None, clicks=1, speed=-1):
        if not x and not y:
            pos_cursor = self.get_cursor_pos()
            x = pos_cursor[0]
            y = pos_cursor[1]
        autoit.mouse_click('left', x, y, clicks=clicks, speed=speed)
        return True

    def right_click(self, x=None, y=None, clicks=1, speed=-1):
        if not x and not y:
            pos_cursor = self.get_cursor_pos()
            x = pos_cursor[0]
            y = pos_cursor[1]
        autoit.mouse_click('right', x, y, clicks=clicks, speed=speed)
        return True

    @staticmethod
    def mouse_down(button='left'):
        autoit.mouse_down(button)
        return True

    @staticmethod
    def mouse_up(button='left'):
        autoit.mouse_up(button)
        return True

    @staticmethod
    def move(x, y, speed=-1):
        autoit.mouse_move(x, y, speed=speed)
        return True

    @staticmethod
    def get_cursor_pos():
        pos = autoit.mouse_get_pos()
        return pos

    @staticmethod
    def scroll_up(clicks=1):
        autoit.mouse_wheel('up', clicks=clicks)
        return True

    @staticmethod
    def scroll_down(clicks=1):
        autoit.mouse_wheel('down', clicks=clicks)
        return True


class Keyboard:
    def __init__(self):
        pass

    @staticmethod
    def echo():
        print('echo Keyboard class')
        return True

    @staticmethod
    def send_text(text):
        autoit.send(text)
        return True

    @staticmethod
    def copy():
        autoit.send("^c")
        return True

    @staticmethod
    def paste():
        autoit.send("^v")
        return True

    @staticmethod
    def select_all():
        autoit.send("^a")
        return True

    @staticmethod
    def enter():
        autoit.send("{ENTER}")
        return True

    @staticmethod
    def esc():
        autoit.send("{ESC}")
        return True

    @staticmethod
    def up():
        autoit.send("{UP}")
        return True

    @staticmethod
    def down():
        autoit.send("{DOWN}")
        return True

    @staticmethod
    def delete():
        autoit.send("{DELETE}")
        return True


def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)


class File:
    def __init__(self):
        pass

    @staticmethod
    def echo():
        print('echo File class')
        return True

    @staticmethod
    def remove(file_path):
        if os.path.isfile(file_path):
            os.remove(file_path)
        return True

    @staticmethod
    def remove_folder(folder_path):
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path, onerror=remove_readonly)
        return True

    @staticmethod
    def file_list_in_folder(folder_path):
        if not os.path.isdir(folder_path):
            print(f'Folder {folder_path} not exist.')
            return False
        file_list = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
        return file_list

    @staticmethod
    def generate_md5_for_file(check_file_path):
        md5 = hashlib.md5()
        with open(check_file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                md5.update(chunk)
        result_value = md5.hexdigest()
        return result_value

    @staticmethod
    def copy_file(src_file, dst_file):
        shutil.copyfile(src_file, dst_file)
        return True


class WinRegistry:
    def __init__(self):
        pass

    @staticmethod
    def echo():
        print('echo WinReg class')
        return True

    @staticmethod
    def query_value(key, sub_key, key_name):
        if key == 'HKEY_CURRENT_USER':
            key = winreg.HKEY_CURRENT_USER
        elif key == 'HKEY_LOCAL_MACHINE':
            key = winreg.HKEY_LOCAL_MACHINE
        try:
            reg_key = winreg.OpenKey(key, sub_key)
            value, _ = winreg.QueryValueEx(reg_key, key_name)
            winreg.CloseKey(reg_key)
            return value
        except Exception as e:
            logger(f'Cannot find key {key_name} in {key}\\{sub_key}. Error={e}')
            return False

    @staticmethod
    def set_value(key, sub_key, key_name, key_type, value):
        if key == 'HKEY_CURRENT_USER':
            key = winreg.HKEY_CURRENT_USER
        elif key == 'HKEY_LOCAL_MACHINE':
            key = winreg.HKEY_LOCAL_MACHINE
        try:
            reg_key = winreg.OpenKey(key, sub_key, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(reg_key, key_name, 0, key_type, value)
            winreg.CloseKey(reg_key)
            return True
        except Exception as e:
            logger(f'Cannot set {value=} to {key_name} in {key}\\{sub_key}. Error={e}')
            return False
