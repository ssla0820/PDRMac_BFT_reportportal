# import importlib, winreg
import time, glob, sys
import os, inspect, ctypes

from os.path import basename
from tkinter import Tk
from ..utils import logger

from selenium.webdriver import Chrome, Firefox, Ie, Safari, Edge
# from msedge.selenium_tools import Edge  # Update to Selenium4 is built-in Edge
from selenium.webdriver.remote.webelement import WebElement
from appium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from pynput.mouse import Button as mouse_btn, Controller as Mouse_ctrl
from pynput.keyboard import Key as kb_key, Controller as Kb_ctrl, KeyCode
import uuid
import ctypes
import contextlib
import tempfile
import PIL.ImageGrab
from PIL import Image as PIL_Image
import cv2
from types import SimpleNamespace
import base64

# webdriver auto installer
import chromedriver_autoinstaller # pip install chromedriver-autoinstaller
import edgedriver_autoinstaller # pip isntall edgedriver-autoinstaller
from webdriver_manager.microsoft import EdgeChromiumDriverManager  # pip install webdriver-manager

# Define screen width and height
import platform
if platform.system() == 'Windows':
    user32 = ctypes.windll.user32
    screen_w, screen_h = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
else:
    from AppKit import NSScreen
    screen_w, screen_h = list(map(int, NSScreen.mainScreen().frame().size))

temp_dir = os.path.abspath(tempfile.gettempdir() + "/web_driver")
os.makedirs(temp_dir, exist_ok=True)


def initialRemote(option, options, desired_caps):
    driver = MyRemote('http://127.0.0.1:4723/wd/hub', desired_caps)
    print(f'current driver={driver}')
    driver.implicitly_wait(option['implicitly_wait'])
    driver.setimplicitlyWait(
        option['implicitly_wait'])  # for get method if necessary. Using for restore implicitly_wait duration.
    return driver


def setCollapsed(self, collapsed):
    try:
        if self.get_attribute("collapsed") != str(collapsed).lower():
            el = self.find_element_by_css_selector("div > a")
            el.click()
    except:
        pass
    return self


WebElement.setCollapsed = setCollapsed


class Mouse:
    mouse = Mouse_ctrl()

    def move(self, x, y, duration=0.5, interval=0.001, wait=0.2):
        # print(f"Move mouse to {x}, {y}")
        if 0 < x < 1: x = int(x * screen_w)
        if 0 < y < 1: y = int(y * screen_h)
        timer = time.time()
        pos = self.position()
        x_dist = x - pos[0]
        y_dist = y - pos[1]
        duration = duration - wait if duration > wait else interval
        step = duration / interval
        # print(f"{step=}")
        move_x = x_dist / step
        move_y = y_dist / step
        # print(f"{move_x=} / {move_y=}")
        # print(f"Current pos = {pos}")
        for i in range(int(step)):
            while time.time() - timer < interval:
                pass
            else:
                timer = time.time()
            tar_x = pos[0] + move_x * (i + 1)
            tar_y = pos[1] + move_y * (i + 1)
            # print(f"{tar_x=} / {tar_y=}")
            self.mouse.position = (tar_x, tar_y)
        time.sleep(wait)

    @contextlib.contextmanager
    def pressed(self, *args):
        for key in args:
            self.mouse.press(key)
        try:
            yield
        finally:
            for key in reversed(args):
                self.mouse.release(key)

    def shift(self, x=0, y=0):
        self.mouse.move(x, y)

    def position(self):
        return self.mouse.position

    def click(self, x=None, y=None, btn="left", times=1, **kwargs):
        btn_dict = {
            "left": mouse_btn.left,
            "right": mouse_btn.right,
            "middle": mouse_btn.middle,
        }
        target_btn = btn_dict[btn.lower()]

        if x is not None and y is not None: self.move(x, y, **kwargs)
        with self.mouse as mouse:
            for _ in range(times):
                mouse.press(target_btn)
                mouse.release(target_btn)

    def right_click(self, x=None, y=None, times=1):
        self.click(x, y, "right", times)

    def drag(self, src_pos, dest_pos, time_gap=0.5):  # time_gap: the time gap between opeartion
        self.move(*src_pos)
        time.sleep(time_gap)
        self.mouse.press(mouse_btn.left)
        time.sleep(time_gap)
        self.move(*dest_pos)
        time.sleep(time_gap)
        self.mouse.release(mouse_btn.left)

    def drag_directly(self,src_pos, dest_pos, time_gap=0.5):
        self.mouse._position_set(src_pos, 0)
        time.sleep(time_gap)
        self.mouse.press(mouse_btn.left)
        time.sleep(time_gap)
        self.mouse._position_set(dest_pos, 0)
        time.sleep(time_gap)
        self.mouse.release(mouse_btn.left)

    def scroll(self, direction='up', times=1):
        for x in range(times):
            if direction == 'up':
                self.mouse.scroll(0, 10)
            elif direction == 'down':
                self.mouse.scroll(0, -10)
            else:
                logger('incorrect parameter')
                return False
            time.sleep(0.3)
        time.sleep(1)
        return True


class Image:
    img_path = "./material/"
    mouse = Mouse()

    def get_file(self, name):
        for path in [os.path.abspath(name), os.path.abspath(self.img_path + name)]:
            # logger(f"{path=}")
            if os.path.isfile(path):
                return path
        return None

    def snapshot(self, file_name=None, format="png", x=0, y=0, w=screen_w - 1, h=screen_h - 1, raw=False, type=-1):
        try:
            if not file_name:
                file_fullname = f"{temp_dir}/{uuid.uuid4()}.{format}"
            else:
                file_fullname = os.path.abspath(f'{file_name}')
            os.makedirs(os.path.dirname(file_fullname), exist_ok=True)

            x, y, w, h = map(lambda n: int(max(n, 0)), [x, y, w, h])
            # logger(f'snapshot -> {file_fullname}')
            # cmd = f'screencapture -x -t {format} "{file_fullname}"'
            # logger(f"{cmd=}")
            # check_output(cmd, shell=True)
            im = PIL.ImageGrab.grab()
            im.save(file_fullname)
            img = cv2.imread(file_fullname, type)
            org_h, org_w = img.shape[:2]
            if screen_w != org_h or screen_h != org_w:
                img = cv2.resize(img, (screen_w, screen_h), interpolation=cv2.INTER_LINEAR)
            # logger(f'{y=} / {y+h=} / {x=} / {x+w=}')
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
        _source = self.get_file(source)
        _target = self.get_file(target)
        # print(f"{source=}/{target=}")
        s = cv2.imread(_source, [cv2.IMREAD_GRAYSCALE, cv2.IMREAD_COLOR][color])
        t = cv2.imread(_target, [cv2.IMREAD_GRAYSCALE, cv2.IMREAD_COLOR][color])
        # s_h, s_w = s.shape[:2]
        h, w = t.shape[:2]
        # s_resize = cv2.resize(s, (int(s_w * ratio), int(s_h * ratio)), interpolation=cv2.INTER_LINEAR)

        try:
            res = cv2.matchTemplate(s, t, _mode)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if max_val == 0:
                logger("Pure image detected, switch to advanced mode")
                ret = self.search(source, target, center, True, screen_ratio, _mode=2)
                max = ret.w * ret.h * 3 * 255 * 255
                logger(f"{ret=} / {max=}")
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

    def screen_search(self, file_name, similarity=0.95):
        screen = self.snapshot()
        ret = self.search(screen, file_name, screen_ratio=1)
        # print(f"{screen=} / {file_name=} / sim = {ret.similarity}")
        return ret if ret.similarity > similarity else None

    def click(self, file_name, similarity=0.95):
        ret = self.screen_search(file_name, similarity)
        # print(f"click -> {ret=}")
        if ret:
            self.mouse.click(ret.x, ret.y)
        else:
            raise Exception(f"image is not found")
        return True

    def exist(self, file_name, duration=5, similarity=0.95):
        global is_found, image
        period = 0.25
        tasks = int(duration / period)
        is_found = Value(c_bool, False)
        args = [(file_name, similarity, time.time() + x * period) for x in range(tasks)]
        # print(f"{args=}")
        with Pool(initializer=init, initargs=(is_found,)) as pool:
            rets = pool.starmap_async(_exist_timed, args)
            while not is_found.value and not rets.ready():
                pass
            else:
                # print(f"{is_found.value=}")
                pool.close()
            # print("wait complete")
            pool.join()
        # print("poll completed")
        if not is_found:
            # print("not found")
            return None
        # print("="*20)
        # print(f"{rets.get()=}")
        for result in rets.get():
            if result: return result

    def is_exist(self, *args, **kwargs):
        return bool(self.exist(*args, **kwargs))

    def exist_click(self, file_name, timeout=5, similarity=0.95):
        ret = self.exist(file_name, timeout, similarity)
        # print(f"exist_click -> {ret=}")
        if ret:
            self.mouse.click(ret.x, ret.y)
            return True
        else:
            logger(f"[Warning] Image was not found - {file_name} ")
            return False


class MyClass():

    implicitlyWait = 0
    _web_element_cls = WebElement
    myReport = None
    startTime = time.time()
    wrapper_fail_log = ""
    wrapper_last_result = False
    mouse = Mouse()
    image = Image()

    def switch_contexts(self, idx=1, locator=None):
        try:
            if locator is None:
                self.switch_to.context(self.contexts[idx])
            elif 'android.' in locator[1] or 'android:' in locator[1]:
                self.switch_to.context(self.contexts[0])
            else:
                self.switch_to.context(self.contexts[1])
            # logger(f'[switch_contexts] {self.current_context=}')
            time.sleep(1)
        except Exception as e:
            logger(f'Exception occurs. Error={e}')
            raise Exception

    def replace_id_to_css(self, locator):
        if 'android.' in locator[1] or 'android:' in locator[1]:
            pass
        elif locator[0] == 'id':
            locator = ('css selector', f"[id={locator[1]}]")
        return locator

    def find(self, targets, found=None): #targets: locator
        if isinstance(targets, list):
            if found is not None:
                ret = found
            else:
                ret = super()
            for d in targets:
                if isinstance(d, dict):
                    ret = self._findInFound(d, ret)
                    if not ret:
                        return None  # ToDO: add error log here
            return ret

    def _findInFound(self, dict, found): # related: find, found - parent object handle
        ret = None
        try:
            if dict['multiple']:
                ret = found.find_elements(dict['by'], dict['value'])[dict['index']]
            else:
                ret = found.find_element(dict['by'], dict['value'])
        except KeyError:
            # print ("return all elements")
            return found.find_elements(dict['by'], dict['value'])
        except:
            pass  # print ("element is not found: " + str(dict))
        try:
            if dict['attribute'] != None:
                ret = ret.get_attribute(dict['attribute'])
        except:
            pass
        return ret

    def printValue(self, el, index=None, printIt=True):
        old_time = time.time()
        result_text = ""
        while (time.time() - old_time < 5):
            try:
                if index is None:
                    element = self.find(el)
                    if isinstance(element, list):
                        element = element[0]
                else:
                    element = self.find(el)[index - 1]
                if type(element) == str:
                    result_text = element  # for attribute
                else:
                    result_text = element.text
            except:
                pass
            if result_text != "":
                break
        if printIt:
            print("Text=" + result_text)
        else:
            return result_text

    def click_element(self, target):
        self.find(target).click()
        return target

    def object_drag_and_drop_offset(self, el, width=0, height=0):
        action = ActionChains(self)
        action.click_and_hold(el).perform()
        action.drag_and_drop_by_offset(el, width, height).perform()
        return el

    # def debugWrapper(self, wrap, *augs):
    #     ret = self.wrapper(wrap, *augs)

    def object_equal(self, path, val, timeout=0, index=1):
        old_time = time.time()
        ret = False
        while True:
            el = self.find(path)
            if el is None:
                print("object does not exist:")
                break
            el = el if not isinstance(el, list) else el[index - 1]
            text = el if isinstance(el, str) else el.text
            if (text == val):
                ret = True
                break
            if (time.time() - old_time > timeout):
                break
        # print ("[object_equal] Found text = " + el.text + "expect = " + str(val))
        self.wrapper_last_result = ret
        return ret

    def object_not_equal(self, path, val, timeout=0, index=1):
        oldTime = time.time()
        ret = False
        while True:
            el = self.find(path)
            if el is None:
                print("object does not exist:")
                break
            el = el if not isinstance(el, list) else el[index - 1]
            text = el if isinstance(el, str) else el.text
            if (el.text != val):
                ret = True
            if (time.time() - oldTime > timeout):
                break
        # print ("[object_equal] Found text = " + el.text + "expect not equal " + str(val))
        self.wrapper_last_result = ret
        return ret

    def printValues(self, el):
        objs = self.find(el)
        for obj in objs:
            print(obj.text)

    def printObjs(self, el):
        el = el[0]
        print(super().find_elements(el['by'], el['value']))

    def object_exist(self, el, timeout=None):
        # try:
        # ret = self.find(el)
        # return ret != None
        # except:
        # return False
        if timeout is None:
            timeout = self.implicitlyWait
        oldTime = time.time()

        self.implicitly_wait(0.5)
        result = self.find(el)
        while (time.time() - oldTime < timeout):
            if result:
                break
            result = self.find(el)
        self.implicitly_wait(self.getimplicitlyWait())
        self.wrapper_last_result = True if result else False
        return True if result else False

    def object_not_exist(self, el, timeout=None):
        if timeout is None:
            timeout = self.implicitlyWait
        oldTime = time.time()
        ret = False
        while (time.time() - oldTime < timeout):
            self.implicitly_wait(0.5)
            result = self.find(el)
            if result is None:
                ret = True
                break
        self.implicitly_wait(self.getimplicitlyWait())
        self.wrapper_last_result = ret
        return ret

    def setimplicitlyWait(self, sec):
        self.implicitlyWait = sec

    def getimplicitlyWait(self):
        return self.implicitlyWait

    def clipboard_include(self, text):
        root = Tk()
        root.withdraw()
        textClipboard = root.clipboard_get()
        # print ("clipboard => " + textClipboard)
        return text in textClipboard

    def exist_text(self, text, timeout=None):
        if timeout is None:
            timeout = self.implicitlyWait
        oldTime = time.time()
        ret = False
        result = None
        while (time.time() - oldTime < timeout):
            self.implicitly_wait(0.5)
            try:
                result = super().find_element_by_xpath("//*[contains(text(),'" + text + "')]")
            except:
                pass
            if result is not None:
                ret = True
                break
        self.implicitly_wait(self.getimplicitlyWait())
        print(ret)
        self.wrapper_last_result = ret
        return ret

    def css(self, css):
        return ("css selector", css)

    def xpath(self, xpath):
        return ("xpath", xpath)

    def el(self, locator):
        self.switch_contexts(locator=locator)
        locator = self.replace_id_to_css(locator)
        el = self.find_element(*locator)
        return el

    def els(self, locator):
        self.switch_contexts(locator=locator)
        locator = self.replace_id_to_css(locator)
        el = self.find_elements(*locator)
        return el

    def el_xpath(self, locator):
        return self.find_element_by_xpath(locator)

    def exist(self, locator, timeout=10, log_flag=True):
        # locator_css = self.css(locator)
        self.switch_contexts(locator=locator)
        locator = self.replace_id_to_css(locator)
        self.implicitly_wait(0.1)
        wait = WebDriverWait(self, timeout)
        timer_start = time.time()
        elem = None
        while (timer := time.time() - timer_start) < timeout:
            try:
                # elem = wait.until(EC.presence_of_element_located(locator),
                #                   "Locator still not exist: " + str(locator))
                elem = wait.until(EC.visibility_of_element_located(locator),
                                  "Locator still not exist: " + str(locator))
                # logger("[is_exist] found:" + str(time.time() - timer_start))
                break
            except:
                if timer != timer: logger("[is_exist] Not found:" + str(time.time() - timer_start))
        self.implicitly_wait(self.getimplicitlyWait())
        if not elem:
            if log_flag: logger(f'Fail to find element: {locator}')
        return elem

    def not_exist(self, locator, timeout=10):
        # locator_css = self.css(locator)
        self.switch_contexts(locator=locator)
        locator = self.replace_id_to_css(locator)
        implicitly = self.getimplicitlyWait()
        self.implicitly_wait(0.1)
        wait = WebDriverWait(self, timeout)
        timer_start = time.time()
        result = False
        while time.time() - timer_start < timeout:
            try:
                # elem = wait.until_not(EC.presence_of_element_located(locator),
                #                       "Locator still exist: " + str(locator))
                elem = wait.until_not(EC.visibility_of_element_located(locator),
                                      "Locator still exist: " + str(locator))
                result = True
                # logger("[is_not_exist] Vanished:" + str(time.time() - timer_start))
                break
            except Exception as e:
                # logger(f"{e=}")
                # logger("is_not_exist] not Vanished:" + str(time.time() - timer_start))
                ...
        self.implicitly_wait(implicitly)
        return result

    def is_exist(self, *aug, **kwaug):
        return bool(self.exist(*aug, **kwaug))

    def is_not_exist(self, *aug, **kwaug):
        return bool(self.not_exist(*aug, **kwaug))

    def click(self, locator, timeout=10):
        try:
            if self.name == 'Safari':
                elem = self.exist(locator, timeout)
                self.execute_script("arguments[0].click()", elem)
            else:
                self.exist(locator, timeout).click()
        except Exception as e:
            logger(f'Exception occurs. Error={e}')
            raise Exception
        return True

    def exist_click(self, locator, timeout=10):
        if item := self.exist(locator, timeout):
            retry = 4
            while retry := retry - 1:
                try:
                    item.click()
                    break
                except:
                    pass
                time.sleep(2)
            else:
                logger("[ERROR] click element error.")
                return
            logger(f"[exist_click] Done. {locator}")
            return item
        else:
            return False

    def select_by_index(self, locator, index=0):
        try:
            s = Select(self.el(locator))
            s.select_by_index(index)
            return True
        except:
            return False

    def select_by_value(self, locator, value):
        try:
            s = Select(self.el(locator))
            s.select_by_value(value)
            return True
        except:
            return False

    def select_by_visible_text(self, locator, text):
        try:
            s = Select(self.el(locator))
            s.select_by_visible_text(text)
            return True
        except:
            return False

    def set_text(self, locator, text, timeout=10, clear_flag=True):
        try:
            text_area = self.exist(locator, timeout)
            if clear_flag is True:
                try:
                    text_area.clear()
                except Exception:
                    print("ERROR: %s page cannot clear the text field: %s" % (self, locator))
                    raise Exception
            try:
                return text_area.send_keys(text)
            except Exception:
                print("ERROR: %s page cannot set the text field: %s" % (self, locator))
                raise Exception
        except Exception:
            print("ERROR: %s page cannot find the text field: %s" % (self, locator))
            raise Exception

    def get_text(self, locator, timeout=10):
        try:
            text = self.exist(locator, timeout).text
        except Exception as e:
            logger(f'Exception occurs. Error={e}')
            raise Exception
        return text

    def get_all_options(self, locator, timeout):
        try:
            all_options = Select(self.exist(locator, timeout)).options
        except Exception as e:
            logger(f'Exception occurs. Error={e}')
            raise Exception
        return all_options

    def get_selected_option(self, locator, timeout):
        try:
            selected_option = Select(self.exist(locator, timeout)).all_selected_options
        except Exception as e:
            logger(f'Exception occurs. Error={e}')
            raise Exception
        return selected_option

    def get_firstselected_option(self, locator, timeout):
        try:
            firstselected_option = Select(self.exist(locator, timeout)).first_selected_option
        except Exception as e:
            logger(f'Exception occurs. Error={e}')
            raise Exception
        return firstselected_option

    def object_snapshot(self, locator, file_name=None, format="png"):
        locator = self.replace_id_to_css(locator)
        try:
            if not file_name:
                file_fullname = f"{temp_dir}/{uuid.uuid4()}.{format}"
            else:
                file_fullname = os.path.abspath(f'{file_name}')
            os.makedirs(os.path.dirname(file_fullname), exist_ok=True)
            super().find_element(*locator).screenshot(file_fullname)
        except Exception as e:
            logger(f'[Error] => {e}')
            return False
        return file_fullname

    def snapshot_full_page(self, file_path=None, locator=('xpath', '/html/body')):
        try:
            if not file_path:
                file_fullname = f"{temp_dir}/{uuid.uuid4()}.png"
            else:
                file_fullname = os.path.abspath(f'{file_path}')
            os.makedirs(os.path.dirname(file_fullname), exist_ok=True)

            # if isinstance(locator, tuple):
            #     locator = locator[1]

            # el = super().find_element_by_xpath(locator)
            el = self.exist(locator)
            if not el:
                logger(f'Fail to find locator {locator=}')
                raise Exception

            scrollbar_width = super().execute_script('return window.innerWidth - document.body.clientWidth;')
            # capture full page of webpage
            page_rect = super().execute_cdp_cmd('Page.getLayoutMetrics', {})
            data_image = super().execute_cdp_cmd(
                "Page.captureScreenshot",
                {
                    'captureBeyondViewport': True,
                    'fromSurface': True,
                    'clip': {
                        'width': page_rect['contentSize']['width']+scrollbar_width,
                        'height': page_rect['contentSize']['height'],
                        'x': 0,
                        'y': 0,
                        'scale': 1},
                }
            )
            with open(file_fullname, "wb") as file:
                file.write(base64.urlsafe_b64decode(data_image["data"]))

            # crop image for specific element
            left, top, right, bottom = int(el.location['x']), int(el.location['y']), int(
                el.location['x'] + el.size['width'])+scrollbar_width, int(el.location['y'] + el.size['height'])
            img_crop = PIL_Image.open(file_fullname)
            img_crop = img_crop.crop((left, top, right, bottom))
            img_crop.save(file_fullname)
            return file_fullname
        except Exception as e:
            logger(f'[Error] => {e}')
            return False


class MyRemote(MyClass, webdriver.Remote):
    pass





