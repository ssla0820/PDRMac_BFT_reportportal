import os
import ctypes
import tempfile
import cv2
from PIL import ImageGrab
import uuid
import time
import pyautogui
import psutil
import uiautomation as auto
from ..utils import logger


user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
current_dpi = user32.GetDpiForSystem()
dpi_ratio = current_dpi / 96
screen_w, screen_h = int(user32.GetSystemMetrics(0) / dpi_ratio), int(user32.GetSystemMetrics(1) / dpi_ratio)

temp_dir = os.path.abspath(tempfile.gettempdir() + "/koan_driver_adr")
os.makedirs(temp_dir, exist_ok=True)

ACTION_DELAY = 1


class KoanUI:
    def __init__(self, app_path, process_name=''):
        self.app_path = app_path
        self.process_name = process_name
        self.image = Image()
        self.video = Audio()
        self.mouse = Mouse()
        self.keyboard = Keyboard()
        self.size = {"w": screen_w, "h": screen_h}
        self.file = File()
        self.driver_type = 'uiautomation'
        self.main_window_name = 'AudioDirector'

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

    def _genearte_call_item(self, locator):  # locator - {'ControlType': '', 'ClassName': '', 'AutomationId'= ''}
        element_property = ''
        func_category = f'{locator["ControlType"]}'
        for elem in locator.keys():
            if elem != 'ControlType':
                if element_property:
                    element_property += f',{elem}=\"{locator[elem]}\"'
                else:
                    element_property += f'{elem}=\"{locator[elem]}\"'
        call_item = f'{func_category}({element_property})'
        logger(f'{call_item=}')
        return call_item

    def _generate_call_sequence(self, locator):
        call_sequence = 'auto'
        if isinstance(locator, list):
            for sub_locator in locator:
                if call_sequence == 'auto':
                    call_sequence += f'{self._genearte_call_item(sub_locator)}'
                else:
                    call_sequence += f'.{self._genearte_call_item(sub_locator)}'
        else:
            call_sequence += f'.{self._genearte_call_item(locator)}'
        logger(f'{call_sequence=}')
        return call_sequence

    def exists(self, locator, timeout=5):
        obj_elem = eval(self._generate_call_sequence(locator))
        if not obj_elem.Exists(maxSearchSeconds=timeout):
            logger(f'Find element Fail')
            obj_elem = None
        return obj_elem

    def is_exist(self, locator, timeout=5):
        return bool(self.exists(locator, timeout))

    def is_not_exist(self, locator, timeout=5):
        result = False
        time_start = time.time()
        while time.time() - time_start < timeout:
            if not self.is_exist(locator, 1):
                result = True
                break
        return result

    def click(self, locator):
        return self.exists(locator).Click()

    @staticmethod
    def select_menu_item(name):  # using uiautomation driver
        auto.MenuItemControl(Name=f'{name}\t').Click()
        return True

    @staticmethod
    def select_combobox_item(name):
        auto.ListItemControl(Name=f'{name}\t').Click()


class Image:
    def __init__(self):
        pass

    @staticmethod
    def echo():
        print('echo Image class')
        return True

    @staticmethod
    def snapshot(file_name=None, x=0, y=0, w=screen_w - 1, h=screen_h - 1, format="png", raw=False, type=-1):
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


class Audio:
    def __init__(self):
        pass

    @staticmethod
    def echo():
        print('echo Audio class')
        return True

    def get_duration(self, source, target):
        return True

    def compare(self, source, target):
        return True


class Mouse:
    def __init__(self):
        pass

    @staticmethod
    def echo():
        print('echo Mouse class')
        return True

    @staticmethod
    def click(x=None, y=None, clicks=1, interval=0.0, button='LEFT'):
        pyautogui.click(x, y, clicks=clicks, interval=interval, button=button)
        time.sleep(ACTION_DELAY * 1)
        return True

    @staticmethod
    def move(x, y, duration=0.0):
        pyautogui.moveTo(x, y, duration=duration)
        return True

    @staticmethod
    def scroll(units=10, x=None, y=None):
        pyautogui.scroll(clicks=units, x=x, y=y)
        time.sleep(ACTION_DELAY * 1)
        return True

    @staticmethod
    def pos_exist(x=None, y=None):
        return pyautogui.onScreen(x=x, y=y)


class Keyboard:
    def __init__(self):
        pass

    @staticmethod
    def echo():
        print('echo Keyboard class')
        return True

    @staticmethod
    def send_text(text):
        pyautogui.write(text)
        time.sleep(ACTION_DELAY * 1)
        return True

    @staticmethod
    def copy():
        pyautogui.hotkey("ctrl", "c")
        return True

    @staticmethod
    def paste():
        pyautogui.hotkey("ctrl", "v")
        time.sleep(ACTION_DELAY * 1)
        return True

    @staticmethod
    def select_all():
        pyautogui.hotkey("ctrl", "a")
        return True


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
    def exist(file_path):
        return os.path.isfile(file_path)

    @staticmethod
    def rename(file_path, new_name):
        new_file_path = os.path.join(os.path.dirname(file_path), new_name)
        if os.path.exists(new_file_path):
            os.remove(new_file_path)
        if not os.path.exists(os.path.dirname(new_file_path)):
            os.makedirs(new_file_path, exist_ok=True)
        if os.path.isfile(file_path):
            os.rename(file_path, new_file_path)
        return True
