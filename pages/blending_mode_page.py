import time, datetime, os, copy
import cv2
import numpy

from .base_page import BasePage
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
# from AppKit import NSScreen
from .locator.locator import blending_mode as L


def arrow(obj, button="up", times=1, locator=None):
    locator = locator[button.lower() == "up"]
    elem = obj.exist(locator)
    for _ in range(times):
        obj.mouse.click(*elem.center)
    return True

class AdjustSet:
    def __init__(self, driver, locators):
        self.driver = driver
        self.locators = locators

    def adjust_slider(self, value):
        self.driver.exist(self.locators[0]).AXValue = value
        return True

    def set_value(self, value):
        target = self.driver.exist(self.locators[1])
        self.driver.mouse.click(*target.center)
        target.AXValue = str(value)
        self.driver.keyboard.enter()
        return True

    def get_value(self):
        return self.driver.exist(self.locators[1]).AXValue

    def click_up(self, times=1):
        return arrow(self.driver, button="up", times=times, locator=self.locators[3:1:-1])

    def click_down(self, times=1):
        return arrow(self.driver, button="down", times=times, locator=self.locators[3:1:-1])

    def click_arrow(self, opt="up", times=1):
        option = ["down", "up"][opt.lower() == "up"]
        return self.__getattribute__(f"click_{option}")(times)

    def click_plus(self, times=1, _btn=True, _get_status=False):
        try:
            locator = self.locators[5:3:-1][bool(_btn)]
        except:
            logger("[Error] locator was not defined")
            return False
        target = self.driver.exist(locator)
        if _get_status:
            return target.AXEnabled
        else:
            self.driver.mouse.click(*target.center, times=times)
            return True

    def click_minus(self, times=1):
        return self.click_plus(times, False)

    def is_plus_enabled(self, btn=True):
        return self.click_plus(_get_status=True)

    def is_minus_enabled(self):
        return self.click_plus(_btn=False, _get_status=True)


def _set_checkbox(self, _locator, value=True, _get_status_only=False):
    target = self.exist(_locator)
    timer = time.time()
    while time.time() - timer < 5:
        try:
            current_value = bool(int(target.AXValue))
            if _get_status_only: return current_value
            if current_value == value:
                break
            else:
                target.press()
                time.sleep(1)
        except:
            logger("First round, force click it")
            if _get_status_only: target.press()
            target.press()
            time.sleep(1)
    else:
        return False
    return True


def hover_download(self, _btn=None):
    if _btn == -1: return True
    _btn = _btn or L.btn_download
    self.activate()
    dl = self.exist(_btn)
    self.mouse.move(*dl.center)
    return True


def verify_download_tooltip(self, ground_truth, _btn=None, _offset=(0, 20, 62, 20), _hover_it=True):
    if _hover_it: hover_download(self, _btn)
    time.sleep(1)
    _x, _y = self.mouse.position()
    x = _x + _offset[0]
    y = _y + _offset[1]
    img_path = self.image.snapshot(x=x, y=y, w=_offset[2], h=_offset[3])
    return self.compare(ground_truth, img_path)


class Blending(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_in_blending_mode(self, timeout=5):
        return self.is_exist(L.main_window, timeout=timeout)

    def click_ok(self):
        return bool(self.exist_press(L.btn_ok))

    def click_cancel(self):
        return bool(self.exist_press(L.btn_cancel))

    def get_blending_mode(self):
        mode = self.exist(L.menu_mode)
        return mode.AXTitle

    def set_blending_mode(self, value):
        target = L.menu_item_mode.copy()
        target.append({"AXValue": value})
        self.exist_click(L.menu_mode)
        return bool(self.exist_click(target))

