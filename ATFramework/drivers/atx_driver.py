import uiautomator2 as u2
from drivers.base_driver import BaseDriver
from appium.webdriver.common.mobileby import MobileBy
import configs.driver_config as DriverConfig
import configs.app_config as AppConfig
import time
import subprocess
import os
import urllib



class Borg:
    # The borg design pattern is to share state
    # Src: http://code.activestate.com/recipes/66531/
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state

    def is_first_time(self):
        # Has the child class been invoked before?
        result_flag = False
        if len(self.__dict__)==0:
            result_flag = True

        return result_flag

# Utilities Function
def sh(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(p.stdout.read())

def is_url(url):
    return urlparse.urlparse(url).scheme != ""


class ATXU2Driver(Borg, BaseDriver):
    DEFAULT_TIMEOUT = 10
    DEFAULT_POLL_TIME = 0.1

    def __init__(self):
        # Constructor
        Borg.__init__(self)
        if self.is_first_time():
            # Do these actions if this the first time this class is initialized
            pass

        self.driver = u2.connect('99c9d645') #TODO need to add parameter
        self.driver.healthcheck()
        self.driver.wait_timeout = 10
        self.driver.click_post_delay = 1.5
        if not self.driver.info.get('screenOn'):  # 判断当前屏幕是否打开
            self.driver.screen_on()
            time.sleep(3)  # 适当的加上延时，可以确保脚本的健壮，不容易崩溃
            self.driver.unlock()  # 这个解锁好像不是每个手机上都能用
            self.driver.swipe("up", steps=20)
        self.driver.set_fastinput_ime(True)
        self.driver.app_start("com.cyberlink.U") #TODO need to add parameter

    def stop_driver(self):
        self.driver.set_fastinput_ime(False)
        self.driver.service("uiautomator").stop()
        # self.driver.uiautomator.stop()

    # App Management Functions
    def install_app(self, apk, package=None):
        if apk.is_url():
            # Install app with apk URL and return package name if success
            try:
                self.driver.app_install(apk)
                return True
            except Exception:
                return False
        else:
            # Install app with apk PATH via adb command "adb install"
            adb_command = "adb install " + apk
            try:
                sh(adb_command)
                return True
            except Exception:
                return False

    def remove_app(self, package):
        # Remove app
        try:
            self.driver.app_uninstall(package)
            return True
        except Exception:
            return False

    def start_app(self, package):
        # Start app via specified package
        return self.driver.app_start(package)

    def stop_app(self, package):
        # Stop app via specified package
        return self.driver.app_stop(package)

    def stop_all(self):
        # Stop all running app except specified package
        return self.driver.app_stop_all()

    def activate_app(self, package):
        # Cannot find specific API use start_app instead
        return self.driver.start_app(package)

    def background_app(self, package):
        # Cannot find specific API yet
        pass

    def reset_app(self, package):
        # Reset app
        return self.driver.app_clear(package)

    # Orientation Control Functions
    def get_orientation(self):
        # To be implemented in sub class
        pass

    def set_orientation(self):
        # To be implemented in sub class
        pass

    def freeze_orientation(self):
        # To be implemented in sub class
        pass

    # Element Operation Functions
    def get_element(self, locator, timeout=DEFAULT_TIMEOUT, poll_frequency=None):
        # Return element if found else None
        element = None
        selector = locator[0]
        value = locator[1]
        if selector == MobileBy.ACCESSIBILITY_ID:
            element = self.driver(description=value)
        elif selector == MobileBy.ID:
            element = self.driver(resourceId=value)
        elif selector == MobileBy.NAME:
            element = self.driver(text=value)
        elif selector == MobileBy.CLASS_NAME:
            element = self.driver(className=value)
        elif selector == MobileBy.XPATH:
            element = self.driver.xpath(value)
        else:
            print("Selector not defined")
        return element

    def click_element(self, locator):
        try:
            return self.get_element(locator).click()
        except Exception:
            print(str(Exception))
        return None

    def double_click_element(self, locator):
        return self.get_element(locator).double_click()

    def tap_element(self, locator):
        return self.click_element(locator)

    def long_press_element(self, locator):
        return self.get_element(locator).long_click()

    def swipe_element(self, locator, direction):
        return self.get_element(locator).swipe(direction)

    def get_text(self, locator):
        # Return the text for a given locator or the 'None' object if the element is not found
        try:
            text = self.get_element(locator).get_text()
            return text.encode('utf-8')
        except Exception as e:
            print("ERROR: %s page cannot get text from %s element" % (self, locator))
        return None

    def set_text(self, locator, text, clear_flag=True):
        # Set the text for a given locator or the 'None' object if failed to set text to target element
        text_area = self.get_element(locator)
        if text_area:
            try:
                if clear_flag is True:
                    text_area.clear_text()
            except Exception:
                print("ERROR: %s page cannot clear the text field: %s" % (self, locator))

            try:
                return text_area.set_text(text)
            except Exception:
                print("ERROR: %s page cannot set the text field: %s" % (self, locator))
        else:
            print("ERROR: %s page cannot find the text field: %s" % (self, locator))
        return None

    def get_toast_text(self, timeout=DEFAULT_TIMEOUT):
        toast_msg = self.driver.toast.get_message(timeout)
        self.driver.toast.reset()
        return str(toast_msg)

    def reset(self):
        self.driver.reset()


