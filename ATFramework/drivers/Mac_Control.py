import atomac   # pip3 install git+https://github.com/pyatom/pyatom/
import inspect, time, os, sys
import pynput.mouse
from pynput.mouse import Button
import pynput.keyboard
from AppKit import NSWorkspace  # already in Xcode framework(components), including objc, appkt ,also need PyObjc module

from ATFramework.utils.log import logger
try:
    from PIL import ImageGrab, Image
except Exception as e:
    logger(f"[Warning] {e}")

# ==================================================================================================================
# Class: MWC
# Description: control mac windows
# Note: n/a
# Author: Terence
# Version: v1.0
# Release:
#           | v0.9, 1st version(2019/12/12)
#           | v1.0, add new functions/refine code(2020/5/20 ~ 6/24)
# ==================================================================================================================
# bundleID : in 'Info.plist'

# Mac Window Control

# need a subscriptable class
"""
class GetAttr(type):
    def __getitem__(cls, x):
        return getattr(cls, x)
"""
class MWC(object):
    mouse = pynput.mouse.Controller()
    keyboard = pynput.keyboard.Controller()
    Key = pynput.keyboard.Key
    """
    @classmethod
    def __getitem__(cls, x):
        return getattr(cls, x)

    @classmethod
    def __new__(cls, name, parents, dct):
        dct["__getitem__"] = cls.__getitem__  # <*****HERE
        return super().__new__(cls, name, parents, dct)
    """
    # initial
    def __init__(self, app_name, app_bundleID, app_path):
        self.el_type = None
        self.el_text = None
        self.app_name = app_name
        self.app_bundleID = app_bundleID
        self.app_path = app_path

    # =================================================Common functions================================================
    @staticmethod
    def func_name(stack=2):
        return inspect.stack()[stack].frame.f_code.co_name

    def logger(self, text):
        print(f'[{self.func_name()}]: {text}')

    # =================================================Mouse functions================================================
    def input_keyboard(self, key):
        """
        perform action, return Boolean
        ex:  MWC.input_keyboard('enter')
        """
        try:
            self.keyboard.press(eval(f'self.Key.{key}'))
            time.sleep(0.25)
            self.keyboard.release(eval(f'self.Key.{key}'))
            return True
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def input_combo_keyboard(self, key1, key2, key3=None):
        """
        perform action, return Boolean
        ex:  MWC.input_keyboard('enter')
        """
        try:
            self.keyboard.press(eval(f'self.Key.{key1}'))
            if len(key2) == 1:
                self.keyboard.press(key2)
                if key3 is None:
                    pass
                else:
                    if len(key3) == 1:
                        self.keyboard.press(key3)
                    else:
                        self.keyboard.press(eval(f'self.Key.{key3}'))
            else:
                self.keyboard.press(eval(f'self.Key.{key2}'))
                if key3 is None:
                    pass
                else:
                    if len(key3) == 1:
                        self.keyboard.press(key3)
                    else:
                        self.keyboard.press(eval(f'self.Key.{key3}'))
            time.sleep(1)
            self.keyboard.release(eval(f'self.Key.{key1}'))
            if len(key2) == 1:
                self.keyboard.release(key2)
                if key3 is None:
                    pass
                else:
                    if len(key3) == 1:
                        self.keyboard.release(key3)
                    else:
                        self.keyboard.release(eval(f'self.Key.{key3}'))
            else:
                self.keyboard.release(eval(f'self.Key.{key2}'))
                if key3 is None:
                    pass
                else:
                    if len(key3) == 1:
                        self.keyboard.release(key3)
                    else:
                        self.keyboard.release(eval(f'self.Key.{key3}'))
            return True

        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def multi_select(self, pos):
        """
        hold cmd  and click another pos
        :param pos:
        :return:
        """
        try:
            self.keyboard.press(self.Key.cmd_l)
            time.sleep(1)
            self.click_mouse(pos)
            time.sleep(1)
            self.keyboard.release(self.Key.cmd_l)
            return True
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def input_triple_keyboard(self, key1, key2, key3):
        """
        perform action, return Boolean
        ex:  MWC.input_keyboard('enter')
        """
        try:
            self.keyboard.press(eval(f'self.Key.{key1}'))
            if len(key2) == 1:
                self.keyboard.press(key2)
            else:
                self.keyboard.press(eval(f'self.Key.{key2}'))
            if len(key3) == 1:
                self.keyboard.press(key3)
            else:
                self.keyboard.press(eval(f'self.Key.{key3}'))
            time.sleep(1)
            self.keyboard.release(eval(f'self.Key.{key1}'))
            if len(key2) == 1:
                self.keyboard.release(key2)
            else:
                self.keyboard.release(eval(f'self.Key.{key2}'))
            if len(key3) == 1:
                self.keyboard.release(key3)
            else:
                self.keyboard.release(eval(f'self.Key.{key3}'))
            return True
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def input_text(self, text):
        try:
            text = str(text)
            for x in text:
                self.keyboard.press(x)
                self.keyboard.release(x)
            return True
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    # =================================================Mouse functions================================================
    def get_mouse_pos(self):
        """
        return position(int with tuple) or False
        Note: support Mac each scale
        """
        try:
            pos = tuple(map(int, self.mouse.position))
            self.logger(f'position: {pos}')
            return pos
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def move_mouse(self, destination):
        """
        Do action(return None) or False
        """
        try:
            current_pos = self.get_mouse_pos()
            dx = destination[0] - current_pos[0]
            dy = destination[1] - current_pos[1]
            self.logger(f'Move to ({destination[0]}, {destination[1]})')
            self.mouse.move(dx, dy)
            time.sleep(1)   # if continue action w/o sleep, pynput would jump to unexpected position
            return True
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def click_mouse(self, pos, button='left', times=1):
        try:
            if pos is not None:
                self.move_mouse(pos)
            time.sleep(1)
            self.mouse.click(eval(f'Button.{button}'), times)
            """ org
            for x in range(times):
                self.mouse.click(eval(f'Button.{button}'))
            return True
            """
            return True
        except Exception as e:
            self.logger(f'Exception. ({e})')
            return False

    def click(self, button='left', times=1):
        try:
            self.mouse.click(eval(f'Button.{button}'), times)
            return True
        except Exception as e:
            self.logger(f'Exception. ({e})')
            return False

    def scroll_mouse(self, direction='up', times=1):
        for x in range(times):
            if direction == 'up':
                self.mouse.scroll(0, 10)
            elif direction == 'down':
                self.mouse.scroll(0, -10)
            else:
                self.logger('incorrect parameter')
                return False
            time.sleep(1)
        time.sleep(1)
        return True

    def drag_mouse(self, start_pos, destination):
        """
        Do action(return None) or False
        """
        try:
            self.move_mouse(start_pos)
            time.sleep(1)
            self.mouse.press(Button.left)
            time.sleep(1)
            self.move_mouse(destination)
            time.sleep(1)
            self.logger(f'from {start_pos} to {destination}')
            time.sleep(1)
            self.click_mouse(self.get_mouse_pos())  # in order to enable some koan UI highlight
            time.sleep(1)
            self.mouse.release(Button.left)
            time.sleep(1)
            return True
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def drag_mouse_per_pixel(self, start_pos, destination):
        """
        Do action(return None) or False
        """
        try:
            pixel_x = destination[0] - start_pos[0]
            pixel_y = destination[1] - start_pos[1]
            self.move_mouse(start_pos)
            time.sleep(1)
            self.mouse.press(Button.left)
            time.sleep(1)
            self.logger(pixel_x)
            if pixel_x > 0:
                for x in range(abs(pixel_x)):
                    self.move_mouse((start_pos[0] + x, start_pos[1]))
            if pixel_x < 0:
                for x in range(abs(pixel_x)):
                    self.move_mouse((start_pos[0] - x, start_pos[1]))
            self.logger(pixel_y)
            if pixel_y > 0:
                for y in range(abs(pixel_y)):
                    self.move_mouse((destination[0], start_pos[1] + y))
            if pixel_x < 0:
                for y in range(abs(pixel_y)):
                    self.move_mouse((destination[0], start_pos[1] - y))
            time.sleep(1)
            self.logger(f'from {start_pos} to {destination}')
            time.sleep(1)
            self.click_mouse(self.get_mouse_pos())  # in order to enable some koan UI highlight
            time.sleep(1)
            self.mouse.release(Button.left)
            time.sleep(1)
            return True
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def drag_element_to(self, el1, el2):
        """
        drag el1 to el2
        :param el1:
        :param el2:
        :return: True/False
        """
        try:
            # get el1 & el2 pos
            pos_el1_mid = self.get_mid_pos(el1)
            pos_el2_mid = self.get_mid_pos(el2)
            if type(pos_el1_mid) is not tuple:
                self.logger(f'get el1 position fail')
                return False
            if type(pos_el2_mid) is not tuple:
                self.logger(f'get el2 position fail')
                return False
            # start to drag
            if self.drag_mouse(pos_el1_mid, pos_el2_mid):
                return True
            else:
                self.logger('drag fail')
                return False
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def tap_pos(self, pos):
        try:
            if self.click_mouse(pos):
                return True
            else:
                self.logger('click mouse fail')
                return False
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def tap_locator(self, locator):
        try:
            el = self.search_el(locator)
            if el is None:
                self.logger('search el fail')
                return False
            pos = self.get_mid_pos(el)
            if pos is False:
                self.logger('get pos fail')
                return False
            if self.tap_pos(pos):
                logger("tap success")
                return True
            else:
                self.logger('tap pos fail')
                return False
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def tap_element(self, element):
        try:
            pos = self.get_mid_pos(element)
            if pos is False:
                self.logger('get pos fail')
                return False
            if self.tap_pos(pos):
                return True
            else:
                self.logger('tap pos fail')
                return False
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def adjust_element_slider(self, element, value, min=1, max=100, edge=6, tolerance=None):
        """
        => adjust to the closest value => adjust 1 pixel by 1 till match
        Note: Support horizontal/vertical
        :param element:
        :param value:
        :param edge: the edge of slider
        :param tolerance: input with list, if match return true
        :return:
        """
        try:
            # make sure value is between min/max
            if value > max or \
                    value < min:
                self.logger('incorrect parameter')
                return False

            # make sure the type is slider
            if not self.get_axtype(element) == 'slider':
                self.logger('type is not slider')
                return False

            # check is Horizontal or vertical slider
            check_flag = element.AXOrientation

            # calculate the width/height(get pos)
            pos = self.get_pos(element)
            width_min = (int(pos[0] + edge), int(pos[1] + pos[3] / 2))
            width_max = (int(pos[0] + pos[2] - edge), int(pos[1] + pos[3] / 2))
            width_scale = int(pos[2]) - edge * 2
            height_min = (int(pos[0] + pos[2] / 2), int(pos[1] + pos[3]))
            height_max = (int(pos[0] + pos[2] / 2), int(pos[1]))
            height_scale = int(pos[3]) - edge * 2

            # check the current value
            current_value = self.get_axvalue(element)

            # define scale
            scale = abs(max - min)

            # target indicator position
            horizontal_indicator_target = (int(((value - min)/scale) * width_scale + pos[0] + edge), int(pos[1] + pos[3] / 2))
            vertical_indicator_target = (int(pos[0] + pos[2] / 2), int(height_scale - ((value - min) / scale) * height_scale) + pos[1] + edge)

            # determine the value & current value
            diff_value = value - current_value
            self.logger(diff_value)
            if diff_value == 0:
                return True
            if check_flag == 'AXHorizontalOrientation':
                for x in range(30):
                    # check the current value
                    current_value = self.get_axvalue(element)
                    if tolerance is not None:
                        if tolerance[0] <= current_value <= tolerance[1]:
                            self.logger(f'in tolerance range {tolerance}')
                            return True
                    # calculate current indicator position
                    horizontal_indicator_org = (int(((current_value - min) / scale) * width_scale + pos[0] + edge), int(pos[1] + pos[3] / 2))

                    # adjust large range
                    if abs(diff_value) >= int((max - min) / 10):
                        if diff_value < 0:
                            # decrease the value
                            self.drag_mouse(horizontal_indicator_org, horizontal_indicator_target)
                            # check the current value
                            current_value = self.get_axvalue(element)
                            diff_value = value - current_value
                            self.logger(diff_value)
                            if diff_value == 0:
                                return True
                        elif diff_value > 0:
                            # increase the value
                            self.drag_mouse(horizontal_indicator_org, horizontal_indicator_target)
                            # check the current value
                            current_value = self.get_axvalue(element)
                            diff_value = value - current_value
                            self.logger(diff_value)
                            if diff_value == 0:
                                return True
                        else:
                            self.logger('unexpected error(1)')
                            return False
                    elif abs(diff_value) <= int((max - min) / 10):
                        adjust_scale = 0
                        if x < 3:
                            adjust_scale = 2 * int(100 / (max - min))
                        else:
                            adjust_scale = 1 * int(100 / (max - min))
                        if diff_value < 0:
                            # decrease the value
                            self.drag_mouse(horizontal_indicator_org, (horizontal_indicator_org[0] - adjust_scale, horizontal_indicator_org[1]))
                            # check the current value
                            current_value = self.get_axvalue(element)
                            diff_value = value - current_value
                            self.logger(diff_value)
                            if diff_value == 0:
                                return True
                        elif diff_value > 0:
                            # increase the value
                            self.drag_mouse(horizontal_indicator_org, ((horizontal_indicator_org[0] + adjust_scale), horizontal_indicator_org[1]))
                            # check the current value
                            current_value = self.get_axvalue(element)
                            diff_value = value - current_value
                            self.logger(diff_value)
                            if diff_value == 0:
                                return True
                        else:
                            self.logger('unexpected error(1)')
                            return False
            elif check_flag == 'AXVerticalOrientation':
                for x in range(30):
                    # check the current value
                    current_value = self.get_axvalue(element)
                    if tolerance is not None:
                        if tolerance[0] <= current_value <= tolerance[1]:
                            self.logger(f'in tolerance range {tolerance}')
                            return True
                    # calculate current indicator position
                    vertical_indicator_org = (int(pos[0] + pos[2] / 2), int((height_scale - ((current_value - min) / scale) * height_scale)) + pos[1] + edge)
                    self.logger(f'org position: {vertical_indicator_org}')
                    # adjust large range
                    if abs(diff_value) >= int((max - min) / 10):
                        if diff_value < 0:
                            # decrease the value
                            self.drag_mouse(vertical_indicator_org, vertical_indicator_target)
                            # check the current value
                            current_value = self.get_axvalue(element)
                            diff_value = value - current_value
                            self.logger(diff_value)
                            if diff_value == 0:
                                return True
                        elif diff_value > 0:
                            # increase the value
                            self.drag_mouse(vertical_indicator_org, vertical_indicator_target)
                            # check the current value
                            current_value = self.get_axvalue(element)
                            diff_value = value - current_value
                            self.logger(diff_value)
                            if diff_value == 0:
                                return True
                        else:
                            self.logger('unexpected error(1)')
                            return False
                    elif abs(diff_value) <= int((max - min) / 10):
                        adjust_scale = 0
                        if x < 3:
                            adjust_scale = 2 * int(100 / (max - min))
                        else:
                            adjust_scale = 1 * int(100 / (max - min))
                        if diff_value < 0:
                            # decrease the value
                            self.drag_mouse(vertical_indicator_org, (vertical_indicator_org[0], vertical_indicator_org[1] + adjust_scale))
                            # check the current value
                            current_value = self.get_axvalue(element)
                            diff_value = value - current_value
                            self.logger(diff_value)
                            if diff_value == 0:
                                return True
                        elif diff_value > 0:
                            # increase the value
                            self.drag_mouse(vertical_indicator_org, (vertical_indicator_org[0], vertical_indicator_org[1] - adjust_scale))
                            # check the current value
                            current_value = self.get_axvalue(element)
                            diff_value = value - current_value
                            self.logger(diff_value)
                            if diff_value == 0:
                                return True
                        else:
                            self.logger('unexpected error(1)')
                            return False
            self.logger('unexpected error(2)')
            return False
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def adjust_locator_slider(self, locator, value, min=1, max=100, edge=6, tolerance=None):
        """
        => adjust to the closest value => adjust 1 pixel by 1 till match
        Note: Support horizontal/vertical
        :param locator:
        :param value:
        :param edge: the edge of slider
        :return:
        """
        try:
            # find element
            el = self.search_el(locator)
            if el is None:
                self.logger('get el fail')
                return False
            return self.adjust_element_slider(el, value, min, max, edge, tolerance)
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def set_text_on_locator(self, locator, text, press_enter=1, double_click=0):
        """
        select the locator_mid pos => cmd + a => delete => input text => press enter
        :param locator:
        :param text: target text
        :return:
        """
        try:
            # get pos
            pos = self.get_locator_mid_pos(locator)
            if pos is False:
                self.logger('get pos fail')
                return False
            if double_click == 0:
                # tap the locator mid pos
                if self.tap_locator(locator) is False:
                    self.logger('tap locator fail')
                    return False
                # cmd + a
                if not self.input_combo_keyboard('cmd', 'a'):
                    self.logger('input combo keyboard fail')
                    return False
                # delete
                if not self.input_keyboard('delete'):
                    self.logger('input keyboard fail')
                    return False
            elif double_click == 1:
                # sometimes cmd + a would fail(AP issue), workaround(double click mouse)
                if not self.click_mouse(pos, 'left', 2):
                    self.logger('double click mouse fail')
                    return False
            else:
                self.logger('incorrect parameter')
                return False
            # input
            if not self.input_text(text):
                self.logger('input text fail')
                return False
            # press enter
            if press_enter == 1:
                if not self.input_keyboard('enter'):
                    self.logger('input keyboard(enter) fail')
                    return False
            return True
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def set_text_on_element(self, element, text, press_enter=1, double_click=0):
        """
        select the element_mid pos => cmd + a => delete => input text => press enter
        :param locator:
        :param text: target text
        :return:
        """
        try:
            # get pos
            pos = self.get_mid_pos(element)
            if pos is False:
                self.logger('get pos fail')
                return False
            if double_click == 0:
                # tap the locator mid pos
                if self.tap_element(element) is False:
                    self.logger('tap element fail')
                    return False
                # cmd + a
                if not self.input_combo_keyboard('cmd', 'a'):
                    self.logger('input combo keyboard fail')
                    return False
                # delete
                if not self.input_keyboard('delete'):
                    self.logger('input keyboard fail')
                    return False
            elif double_click == 1:
                # sometimes cmd + a would fail(AP issue), workaround(double click mouse)
                if not self.click_mouse(pos, 'left', 2):
                    self.logger('double click mouse fail')
                    return False
            else:
                self.logger('incorrect parameter')
                return False
            # input
            if not self.input_text(text):
                self.logger('input text fail')
                return False
            # press enter
            if press_enter == 1:
                if not self.input_keyboard('enter'):
                    self.logger('input keyboard(enter) fail')
                    return False
            return True
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def set_text_on_pos(self, pos, text, press_enter=1, double_click=0):
        """
        select the locator_mid pos => cmd + a => delete => input text => press enter
        :param locator:
        :param text: target text
        :return:
        """
        try:
            if double_click == 0:
                # tap the locator mid pos
                if self.tap_pos(pos) is False:
                    self.logger('tap pos fail')
                    return False
                # cmd + a
                if not self.input_combo_keyboard('cmd', 'a'):
                    self.logger('input combo keyboard fail')
                    return False
                # delete
                if not self.input_keyboard('delete'):
                    self.logger('input keyboard fail')
                    return False
            elif double_click == 1:
                # sometimes cmd + a would fail(AP issue), workaround(double click mouse)
                if not self.click_mouse(pos, 'left', 2):
                    self.logger('double click mouse fail')
                    return False
            else:
                self.logger('incorrect parameter')
                return False
            # input
            if not self.input_text(text):
                self.logger('input text fail')
                return False
            # press enter
            if press_enter == 1:
                if not self.input_keyboard('enter'):
                    self.logger('input keyboard(enter) fail')
                    return False
            return True
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    # ===============================================Execution functions===============================================
    def launch_app(self, timeout=15, get_main_wnd=1, skip_exist=0):
        """
        Return Top el/False/True
            Check if App is not launched and then execute,
            after that, make sure atomac get top_element & window
            for only activate window: get_main_wnd=0, only execute launch and return True
        """
        try:
            if skip_exist == 0:
                # check if app opened
                if self.is_app_exist():
                    self.logger(f'APP({self.app_bundleID}) had been launched')
                    return False
            elif skip_exist == 1:
                pass
            else:
                self.logger('incorrect parameter')
                return False
            # execute app
            atomac.launchAppByBundleId(self.app_bundleID)
            self.logger(f'Launching APP({self.app_bundleID})...')
            if get_main_wnd == 1:
                # wait till get element & window (15sec.)
                wait_time = 0
                while wait_time < timeout:
                    top_el = self.get_current_wnd(self.get_top_element())
                    if not top_el:
                        self.logger(f'wait... {wait_time}sec.')
                        time.sleep(1)
                        wait_time += 1
                    else:
                        self.logger(f'Launch successfully')
                        return top_el
            elif get_main_wnd == 0:
                for x in range(timeout):
                    time.sleep(1)
                return True
        except RuntimeError as re:
            self.logger(f'RuntimeError({re})')
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def close_app(self, forcemode=0, timeout=15):
        """
        close success: return True, others: return False
        """
        try:
            # use force kill  (need app_bundleID)
            if forcemode == 1:
                try:
                    pid = os.popen(f'ps -ax | grep {self.app_path}').readlines()[0].split('??')[0].strip(' ')
                    if type(int(pid)) is not int:
                        raise Exception
                    self.logger(f'Ports(PID): {pid}')
                    os.popen(f"kill {pid}")
                except Exception as e:
                    self.logger(f'Exception. ({e})')
                    pass
            else:
                # use atomac
                atomac.terminateAppByBundleId(self.app_bundleID)
            # check if app is closed
            # wait till NOT get element & window
            wait_time = 0
            while wait_time < timeout:
                if self.get_current_wnd(self.get_top_element()) is False:
                    self.logger('Done')
                    return True
                else:
                    self.logger(f'wait... {wait_time}sec.')
                    time.sleep(1)
                    wait_time += 1
        except RuntimeError as re:
            self.logger(f'RuntimeError({re})')
            return False
        except Exception as e:
            self.logger(f'Exception2({e})')
            return False

    def is_app_exist(self):
        """
        :return: True/False
        """
        try:
            # check if app opened(2 methods: check top element / check alive(need to use if in another full screen) )
            # method 1:
            if self.get_current_wnd(self.get_top_element()):
                return True
            """
            else:
                # method 2:
                if self.get_pid() is not None or False:
                    return True
                return False
            """
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def get_pid(self):
        """
        :return:  None(not launch), PID, False
        """
        try:
            # check if app launched or not
            data = os.popen(f'ps -ax | grep {self.app_path}').readlines()[0]
            check_app_exist = data.split(':')[1][0:5]
            if check_app_exist == '00.00':
                self.logger('AP has not launch yet')
                return None
            else:
                pid = data.split('??')[0].strip(' ')
                if type(int(pid)) is not int:
                    raise Exception
                self.logger(f'PID({pid})')
                return pid
        except Exception as e:
            self.logger(f'Exception: ({e})')
            return False

    # ================================================Get functions===================================================
    def get_top_element(self):
        """
        return Atomac_element, else False
            Get the top level element for the application with the specified
            bundle ID, such as com.vmware.fusion.
        """
        try:
            # source code: NativeUIElement.getAppRefByBundleId
            top_native_el = atomac.getAppRefByBundleId(self.app_bundleID)
            #print(f'[{MWC.func_name()}]: Native_Element({top_native_el})')
            return top_native_el
        except ValueError as ve:
            self.logger(f'ValueError({ve})')
            return False
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def get_current_wnd(self, el):
        """
        return Atomac_element, else False
        """
        try:
            cur_win = el.windows()[0]
            self.logger(f'Current_Wnd({cur_win})')
            return cur_win
        except IndexError as ie:
            self.logger(f'IndexError({ie})')
            return False
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def get_child_wnd(self, el):
        """
        Return a list(Atomac elements), else False
        """
        try:
            result = el.AXChildren
            self.logger(f'Child_Wnd({len(result)};{result})')
            return result
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def get_parent_wnd(self, el):
        """
        Return a Atomac elements, else False
        """
        try:
            result = el.AXParent
            self.logger(f'Parent_Wnd({result})')
            return result
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def get_axtitle(self, el):
        """
        Return string, else False
        """
        try:
            result = el.AXTitle
            self.logger(f'AXTitle({result})')
            return result
        except:
            try:
                # description
                return el.AXRoleDescription
            except Exception as e:
                self.logger(f'Exception({e})')
                return False

    def get_axrole(self, el):
        """
        Return string, else False
        """
        try:
            # title
            result = el.AXRole
            self.logger(f'AXRole({result})')
            return result
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def get_axhelp(self, el):
        """
        Return string, else False
        """
        try:
            # title
            result = el.AXHelp
            self.logger(f'AXHelp({result})')
            return result
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def get_axvalue(self, el):
        """
        Return string, else False
        """
        try:
            result = el.AXValue
            self.logger(f'AXValue({result})')
            return result
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def get_axtype(self, el):
        """
        Return string, else False
        """
        try:
            result = el.AXRoleDescription
            self.logger(f'AXType({result})')
            return result
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def get_axlabel(self, el):
        """
        Return string, else False
        """
        try:
            result = el.AXDescription
            self.logger(f'AXDescription({result})')
            return result
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def get_axposition(self, el):
        """
        Return tuple, else False
        """
        try:
            result = el.AXPosition
            self.logger(f'AXPosition({result})')
            return result
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def get_axsize(self, el):
        """
        Return tuple, else False
        """
        try:
            result = el.AXSize
            self.logger(f'AXSize({result})')
            return result
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def get_pos(self, el, int_rule=1):
        """
        return a list with tuple(int(x), int(y), int(w), int(h)
        :param el:
        :return: tuple/False
        """
        try:
            x, y = el.AXPosition
            # sometimes there is no AXSize attribute, using AXframe
            w, h = el.AXSize
            pos = ''
            if int_rule == 1:
                pos = tuple(map(int, (x, y, w, h)))
                self.logger(f'pos is {pos}')
            elif int_rule != 1:
                pos = (x, y, w, h)
                self.logger(f'pos is {pos}')
            return pos
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def get_locator_pos(self, locator):
        try:
            el = self.search_el(locator)
            if el is None:
                self.logger('get el fail')
                return False
            return self.get_pos(el)
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def get_locator_mid_pos(self, locator):
        try:
            el = self.search_el(locator)
            if el is None:
                self.logger('get el fail')
                return False
            return self.get_mid_pos(el)
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def get_mid_pos(self, el):
        """
        return mid_pos else False
        """
        try:
            check_flag = el.getAttributes()
            if 'AXSize' in check_flag and \
                    'AXPosition' in check_flag:
                pass
            else:
                self.logger("Can't trigger AXSize or AXPosition")
                return False
            x, y = el.AXPosition
            dx, dy = el.AXSize
            mid_pos = (int(x + dx / 2), int(y + dy / 2))
            self.logger(f'mid position:{mid_pos}')
            return mid_pos
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def get_text(self, el):
        """
        get axvalue
        :param el:
        :return:    str/int, 'False'(STR)
        """
        try:
            result = self.get_axvalue(el)
            if type(result) is str or int:
                self.logger(f'get_text: ({result})')
                return result
            else:
                self.logger(f'unexpected result: ({result})')
                return 'False'
        except Exception as e:
            self.logger(f'Exception({e})')
            return 'False'

    def get_Attributes(self, el):
        """
        call module function directly
        return list, or str(False)
        Note: in order to distinguish return False in enabled...etc cases
        """
        try:
            attributes_list = el.getAttributes()
            self.logger(f'attributes_list: ({attributes_list})')
            return attributes_list
        except Exception as e:
            self.logger(f'Exception({e})')
            return 'False'

    def get_Actions(self, el):
        """
        call module function directly
        return list, or str(False)
        Note: in order to distinguish return False in enabled...etc cases
        """
        try:
            return el.getActions()
        except Exception as e:
            self.logger(f'Exception({e})')
            return 'False'

    # ===============================================determine functions===============================================
    def is_element_enabled(self, el):
        """
        get axenabled
        :param el:
        :return:  True/False(Bool), 'False'(STR)
        """
        try:
            result = el.AXEnabled
            self.logger(f'AXEnabled: ({result})')
            return result
        except Exception as e:
            self.logger(f'Exception({e})')
            return 'False'

    def is_element_selected(self, el):
        """
        get axvalue
        :param el:
        :return:    True/False(Bool), 'False'(STR)
        """
        try:
            result = self.get_axvalue(el)
            if result == 1:
                return True
            elif result == 0:
                return False
            else:
                self.logger(f'unexpected result: ({result})')
                return 'False'
        except Exception as e:
            self.logger(f'Exception({e})')
            return 'False'

    def is_element_ticked(self, el):
        """
        get axvalue
        :param el:
        :return:    True/False(Bool), 'False'(STR)
        """
        try:
            result = self.get_axvalue(el)
            if result == 1:
                return True
            elif result == 0:
                return False
            else:
                self.logger(f'unexpected result: ({result})')
                return 'False'
        except Exception as e:
            self.logger(f'Exception({e})')
            return 'False'

    # ===============================================APPKit functions===============================================
    def get_top_wnd_name(self):
        """
        call NSWorkspace to get top name
        """
        try:
            activeAppName = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
            return activeAppName
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    # ================================================Find functions===================================================
    def find_top_el_by_name(self, name):
        """
        return Atomac_element else False
            only can find 'top native element'
        """
        try:
            return atomac.getAppRefByLocalizedName(name)
        except ValueError as ve:
            self.logger(f'ValueError({ve})')
            return False
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    # ================================================wait functions=================================================
    def wait_to_appear(self, locator, timeout=15):
        """
        Return Boolean
        """
        try:
            for x in range(timeout):
                if self.search_el(locator) is not None:
                # if self.get_top_wnd_name() == self.app_name:
                    self.logger('found AP UI')
                    return True
                else:
                    if x == (timeout - 1):
                        return False
                    else:
                        self.logger(f'wait...{x + 1}sec.')
                        time.sleep(1)
        except Exception as e:
            self.logger(f'Exception({e})')
            return False
    # ================================================Search functions=================================================

    def search_child_el_by_title(self, el, title):
        """
        Return a element or list, including matching title atomac_elements
        """
        try:
            check_flag = self.get_child_wnd(el)
            if check_flag is False:
                self.logger('fail to get')
                return False
            result = []
            for x in range(len(check_flag)):
                if self.get_axtitle(check_flag[x]) == title:
                    result.append(check_flag[x])
            # Return element if only 1 else return a list
            if len(result) != 0:
                if len(result) == 1:
                    result = result[0]
                self.logger(f'(Keyword_title: {title}) is found. result is {result}')
                return result
        except Exception as e:
            self.logger(f'Exception({e})')
            return False
        self.logger(f'Search (target_title: {title}) fail')
        return False

    def search_child_el_by_role(self, el, axrole):
        """
        Return a element or list, including matching axrole atomac_elements
        """
        try:
            check_flag = self.get_child_wnd(el)
            if check_flag is False:
                self.logger('fail to get')
                return False
            result = []
            for x in range(len(check_flag)):
                if self.get_axrole(check_flag[x]) == axrole:
                    result.append(check_flag[x])
            # Return element if only 1 else return a list
            if len(result) != 0:
                if len(result) == 1:
                    result = result[0]
                self.logger(f'(Keyword_axrole: {axrole}) found result is {result}')
                return result
        except Exception as e:
            self.logger(f'Exception({e})')
            return False
        self.logger(f'Search (target_axrole: {axrole}) fail')
        return False

    def search_child_el_by_help(self, el, axhelp):
        """
        Return a element or list, including matching axrole atomac_elements
        """
        try:
            check_flag = self.get_child_wnd(el)
            if check_flag is False:
                self.logger('fail to get')
                return False
            result = []
            for x in range(len(check_flag)):
                if self.get_axhelp(check_flag[x]) == axhelp:
                    result.append(check_flag[x])
            # Return element if only 1 else return a list
            if len(result) != 0:
                if len(result) == 1:
                    result = result[0]
                self.logger(f'(Keyword_axhelp: {axhelp}) found result is {result}')
                return result
        except Exception as e:
            self.logger(f'Exception({e})')
            return False
        self.logger(f'Search (target_axhelp: {axhelp}) fail')
        return False


    def search_child_el_by_type(self, el, axtype):
        """
        Return a element or list, including matching axrole atomac_elements
        """
        try:
            check_flag = self.get_child_wnd(el)
            if check_flag is False:
                self.logger('fail to get')
                return False
            result = []
            for x in range(len(check_flag)):
                if self.get_axtype(check_flag[x]) == axtype:
                    # print(check_flag[x])
                    result.append(check_flag[x])
            # Return element if only 1 else return a list
            if len(result) != 0:
                if len(result) == 1:
                    result = result[0]
                self.logger(f'Keyword_axtype: {axtype}) found result is {result}')
                return result
        except Exception as e:
            self.logger(f'Exception({e})')
            return False
        self.logger(f'Search (target_axtype: {axtype}) fail')
        return False

    def search_child_el_by_label(self, el, axlabel):
        """
        Return a element or list, including matching axrole atomac_elements
        """
        try:
            check_flag = self.get_child_wnd(el)
            if check_flag is False:
                self.logger('fail to get')
                return False
            result = []
            for x in range(len(check_flag)):
                if self.get_axlabel(check_flag[x]) == axlabel:
                    # print(check_flag[x])
                    result.append(check_flag[x])
            # Return element if only 1 else return a list
            if len(result) != 0:
                if len(result) == 1:
                    result = result[0]
                self.logger(f'Keyword_axlabel: {axlabel}) found result is {result}')
                return result
        except Exception as e:
            self.logger(f'Exception({e})')
            return False
        self.logger(f'Search (target_axlabel: {axlabel}) fail')
        return False


    def search_child_el_by_property(self, el, property):
        """
        (Input)property: (x, y, w, h, role)
        Return a element or list, including matching axrole atomac_elements
        """
        try:
            check_flag = self.get_child_wnd(el)
            if check_flag is False:
                self.logger('fail to get')
                return False
            result = []
            for x in range(len(check_flag)):
                if self.get_axposition(check_flag[x]) == (property[0], property[1]):
                    if self.get_axsize(check_flag[x]) == (property[2], property[3]):
                        result.append(check_flag[x])
            # Return element if only 1 else return a list
            if len(result) != 0:
                if len(result) == 1:
                    result = result[0]
                self.logger(f'Keyword_property: {property}) found result is {result}')
                return result
        except Exception as e:
            self.logger(f'Exception({e})')
            return False
        self.logger(f'Search (target_property: {property}) fail')
        return False

    def count_child_index_by_property(self, el, property):
        """
        (Input)porperty: (x, y, w, h, axrole)
        Return a index(int) or list with index
        """
        try:
            check_flag = self.get_child_wnd(el)
            if check_flag is False:
                self.logger('fail to get')
                return False
            result = []
            for x in range(len(check_flag)):
                if self.get_axposition(check_flag[x]) == (property[0], property[1]):
                    if self.get_axsize(check_flag[x]) == (property[2], property[3]):
                        if self.get_axrole(check_flag[x]) == property[4]:
                            result.append(x)
            # Return element if only 1 else return a list
            if len(result) != 0:
                if len(result) == 1:
                    result = result[0]
                self.logger(f'Keyword_property: {property}) found result is {property}')
                return result
        except Exception as e:
            self.logger(f'Exception({e})')
            return False
        self.logger(f'Search (target_property: {property}) fail')
        return False

    def search_child_el(self, el, target, bywhat):
        """
        interface for search child by...
        :param el:
        :param bywhat:
        :return:
        """
        if bywhat not in ['label', 'type', 'role', 'title']:
            self.logger('incorrect parameter')
            return False
        selection = {
            'label': 'self.search_child_el_by_label(el, target)',
            'title': 'self.search_child_el_by_title(el, target)',
            'type': 'self.search_child_el_by_type(el, target)',
            'role': 'self.search_child_el_by_role(el, target)'
        }
        try:
            return eval(selection[bywhat])
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def search_child_el_by_index(self, el, index):
        """
        if locator has index, use index w/o using title
        index: 0, 1, 2, 3...
        :return:
        """
        el_list = self.get_child_wnd(el)
        if type(el_list) is not list:
            self.logger('get el_list fail')
            return False
        if index > 0:
            if len(el_list) < index + 1:
                self.logger(f'index out of len')
                return False
        elif index < 0:
            if len(el_list) < abs(index):
                self.logger(f'index out of len')
                return False
        return el_list[index]

    def search_el_by_path(self, locator):
        """
        Rule: if locator has index, search via index with priority (ignore title/name)
        search el by el path
        :param locator:
        :return:  el/False
        """
        try:
            # timeout 3sec
            timeout = 3
            for y in range(timeout):
                # get top el
                top_el = self.get_top_element()
                if top_el is False:
                    self.logger('get top el fail')
                    if y == timeout - 1:
                        return False
                    time.sleep(1)
                    continue
                result_el = None
                # locate element by path(title/role/) or (index)
                for x in range(len(locator)):
                    self.logger(f'===> start search [{x + 1}] layer\n       (target: {locator})')
                    if x == 0:
                        # check if has index
                        if len(locator[x]) == 2:
                            # search by title/role ....
                            result_el = self.search_child_el(top_el, locator[x][0], locator[x][1])
                        elif len(locator[x]) == 3:
                            # search by index ....
                            result_el = self.search_child_el_by_index(top_el, locator[x][2])
                        else:
                            self.logger('incorrect locator format')
                            if y == timeout - 1:
                                return False
                            time.sleep(1)
                            continue
                        if result_el is False:
                            self.logger(f'search el by path fail')
                            return False
                    else:
                        # check if has index
                        if len(locator[x]) == 2:
                            # search by title/role ....
                            result_el = self.search_child_el(result_el, locator[x][0], locator[x][1])
                        elif len(locator[x]) == 3:
                            # search by index ...
                            result_el = self.search_child_el_by_index(result_el, locator[x][2])
                        else:
                            self.logger('incorrect locator format')
                            if y == timeout - 1:
                                return False
                            time.sleep(1)
                            continue
                        if result_el is False:
                            self.logger(f'search el by path fail')
                            return False
                if result_el is False:
                    self.logger(f'search el by path fail')
                    if y == timeout - 1:
                        return False
                    time.sleep(1)
                    continue
                self.logger(f'Found: {result_el}')
                return result_el
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def search_el_by_ato_findFirstR(self, **kwargs):
        """
        find el by ato findFirstR
        :param kwargs:
        :return:
        """
        try:
            # timeout 5sec.
            timeout = 5
            for x in range(timeout):
                # get top el
                top_el = self.get_top_element()
                if top_el is False:
                    self.logger('get top el fail')
                    if x == timeout - 1:
                        return False
                    time.sleep(1)
                    continue
                result_el = top_el.findFirstR(**kwargs)
                self.logger(f'Found: {result_el}')
                return result_el
        except Exception as e:
            self.logger(f'Exception({e})')
            return False

    def search_all_el(self, locator, index=None):
        """
        find all elements match criterial
        :param locator:
        :param index: None -> return all with list, index return element
        :return:
        """
        try:
            top_el = self.get_top_element()
            if top_el is False:
                self.logger('get top el fail')
                return None
            result_el_list = top_el.findAllR(**locator)
            self.logger(f'Found List: {result_el_list}')
            if index is None:
                return result_el_list
            else:
                self.logger(f'target el: {result_el_list[index]}')
                return result_el_list[index]
        except Exception as e:
            self.logger(f'Exception({e})')
            return None

    def search_el(self, locator):
        """
        interface for checking locator format
        :param locator:
        :return:  atomac element/None
        """
        try:
            if type(locator) is list:
                result = self.search_el_by_path(locator)
                if result is not False:
                    return result
                else:
                    self.logger('get result fail(list)')
                    return None
            elif type(locator) is dict:
                result = self.search_el_by_ato_findFirstR(**locator)
                if result is not False:
                    return result
                else:
                    self.logger('get result fail(dict)')
                    return None
            else:
                locator(f'incorrect locator format')
                return None
        except Exception as e:
            self.logger(f'Exception({e})')
            return None

    # ================================================Actions functions============================================
    def Press(self, el):
        """
        call module function, return None
        """
        # AXClasss.py 's bug , it would get exception but action is executed
        return el.Press()

    def clickMouseButtonLeft(self, pos, interval=None):
        """
        call module function, return None
        """
        return self.clickMouseButtonLeft(pos, interval)

    def doubleClickMouse(self, pos):
        """
        call module function, return None
        """
        return self.doubleClickMouse(pos)

    def activate(self, el):
        """
        call module function(return None), in here, return boolean
        """
        return el.activate()

    # ================================================Generator functions==============================================
    # define verification function
    def generator_verify(self, locator_result, locator_org):
        try:
            el_result = self.search_el(locator_result)
            el_org = self.search_el(locator_org)
            if el_result == el_org:
                return True
            else:
                self.logger(f'result: {el_result}')
                self.logger(f'org: {el_org}')
                return False
        except Exception as e:
            self.logger(f'Exception: ({e})')
            return False

    def locator_generator(self, locator, forcemode='normal'):
        """
        Use position & size to generate locator with locator_dict or locator_path
        Input: dict with position & size (ex:  {'AXPosition': (2.0, 3.0), 'AXSize': (120.0, 130.0)}
        :param locator:
        :return:  locator(dict. or path) / None
        """
        try:
            # make sure input is dictionary
            if type(locator) is not dict:
                self.logger('parameter is not dictionary')
                return None
            # find out the element
            el = self.search_el(locator)
            if el is None:
                self.logger('search el fail')
                return None
            # initial the locator_dict or locator_path
            locator_dict = {}
            locator_path = []
            if forcemode == 'normal':
                # [1st Method: Use Dict.] try to find the unique item
                # Note: do not execute in dictionary(use str to describe) to avoid exception
                # Note: do not use AXPosition/AXSize/enable/ticked...etc due to status would be changed
                para_select = {
                    'AXIdentifier': 'el.AXIdentifier',
                    'AXRole': 'el.AXRole',
                    'AXSubrole': 'el.AXSubrole',
                    'AXValue': 'el.AXValue',
                    'AXTitle': 'el.AXTitle',
                    'AXRoleDescription': 'el.AXRoleDescription',
                    'AXSelectedTextRange': 'el.AXSelectedTextRange',
                    'AXNumberOfCharacters': 'el.AXNumberOfCharacters',
                    'AXInsertionPointLineNumber': 'el.AXInsertionPointLineNumber'
                }
                #self.logger(f'xxxxxxx   {[key for key in para_select.keys()][1]}')
                # [Add Identifier/Role...etc        Keys/Value of locator]
                for x in range(len(para_select.keys())):
                    key = ''
                    try:
                        key = f'{[key for key in para_select.keys()][x]}'
                        result = eval(para_select[key])
                    except:
                        self.logger(f'get {key} fail')
                        result = None
                    if result is not None:
                        locator_dict[key] = result
                    if self.generator_verify(locator_dict, locator):
                        self.logger(f'locator: dict: {locator_dict}')
                        return locator_dict
                    # jump to path method if can't locate
                    if x == len(para_select.keys()) - 1:
                        break
            elif forcemode == 'path':
                pass
            else:
                self.logger('incorrect parameter')
                return None
            # [2nd Method: Use Path] find the path
            # define property {'AXPosition': (2.0, 3.0), 'AXSize': (120.0, 130.0), 'AXRole': 'AXCell'}
            property = (locator['AXPosition'][0],
                        locator['AXPosition'][1],
                        locator['AXSize'][0],
                        locator['AXSize'][1],
                        locator['AXRole'])
            # Get the top element
            top_el = self.get_top_element()

            # Get all Value(type -> title -> role -> label)
            para2_select = {
                'type': 'self.get_axtype(el)',
                'title': 'self.get_axtitle(el)',
                'role': 'self.get_axrole(el)',
                'label': 'self.get_axlabel(el)'
            }
            # check 30-layers
            for z in range(30):
                # Get the parent
                el_parent = self.get_parent_wnd(el)
                self.logger(f'\n============================== Layer =============================: {z}')
                self.logger(f'Current locator_path(layer:{z - 1}_result): {locator_path}')
                for y in range(len(para2_select)):
                    #self.logger(f'====== {eval(para2_select["type"])}')
                    key = ''
                    key = f'{[key for key in para2_select.keys()][y]}'
                    result = eval(para2_select[key])
                    # if having value, break. ex: already have [['test', 'title']]
                    if result is False or result == '':
                        pass
                    else:
                        locator_path.append([result, key])
                    try:
                        if len(locator_path[z]) == 2:
                            break
                    except:
                        # list index out of range case
                        break
                # if still got None after checking all Value, remark 'noresult' for title(need to use index)
                if len(locator_path[z]) == 0:
                    locator_path.append(['noresult', 'title'])

                # add index if 'noresult' or parent has multi-child
                # [value method] (if return a list via value method, means can't locate, need to use index)
                el_child = self.search_child_el(el_parent, locator_path[z][0], locator_path[z][1])
                if type(el_child) is list:
                    # [index method]
                    # search child index by property to locate via index
                    index_of_child = self.count_child_index_by_property(el_parent, property)
                    # make sure index of child is int (if get list or False, means can't locate)
                    if index_of_child is False or type(index_of_child) is list:
                        self.logger(f"Can't locate the element")
                        return None
                    # append index to path
                    locator_path[z].append(index_of_child)
                    self.logger(f'============={locator_path}')
                if el_parent == top_el:
                    break
                el = el_parent
                try:
                    (new_x, new_y) = self.get_axposition(el)
                    (new_w, new_h) = self.get_axsize(el)
                    role = self.get_axrole(el)
                    property = (new_x, new_y, new_w, new_h, role)
                except Exception as e:
                    self.logger(f'Exception: Get property fail at {z} layer. ({e})')
                    return None
            # verify
            locator_path.reverse()
            self.logger(f'reverse:   {locator_path}')
            if self.generator_verify(locator_path, locator):
                self.logger(f'locator: path: {locator_path}')
                return locator_path
            return None
        except Exception as e:
            self.logger(f'Exception: ({e})')
            return None

    def get_screenshot_as_file(self, file_path):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            ImageGrab.grab().save(file_path)
            return True
        except Exception as e:
            logger(f'Exception: ({e})')
            return False


class MWCAction(object):
    def __init__(self, el=None):
        self.el = el

    def Press(self):
        """
        call module function, return None
        """
        # AXClasss.py 's bug , it would get exception but action is executed
        return self.el.Press()

    def clickMouseButtonLeft(self, pos, interval=None):
        """
        call module function, return None
        """
        return self.clickMouseButtonLeft(pos, interval)

    def doubleClickMouse(self, pos):
        """
        call module function, return None
        """
        return self.doubleClickMouse(pos)

    def activate(self):
        """
        call module function(return None), in here, return boolean
        """
        return self.el.activate()
