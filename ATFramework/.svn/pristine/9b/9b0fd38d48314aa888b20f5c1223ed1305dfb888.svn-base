try:
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.common.action_chains import ActionChains
    from appium.webdriver.common.touch_action import TouchAction
    from appium.webdriver.common.mobileby import MobileBy
    from appium import webdriver
except:
    ...

class BaseDriver:
    DEFAULT_TIMEOUT = 10

    # Driver Functions
    def __init__(self):
        self.driver = None

    #def launch_app(self, timeout=15):
    #    return self.launch_app(timeout)

    def stop_driver(self):
        # To be implemented in sub class
        pass

    # App Management Functions
    def install_app(self, path, package):
        # To be implemented in sub class
        pass

    def remove_app(self, package, desired_cap=None):
        # To be implemented in sub class
        pass

    def start_app(self, package):
        # To be implemented in sub class
        pass

    def stop_app(self, package):
        # To be implemented in sub class
        pass

    def activate_app(self, package):
        # To be implemented in sub class
        pass

    def background_app(self, duration):
        # To be implemented in sub class
        pass

    def reset_app(self, package):
        # To be implemented in sub class
        pass

    # Orientation Control Functions
    def get_orientation(self):
        # To be implemented in sub class
        pass

    def set_orientation(self, orientation):
        # To be implemented in sub class
        pass

    def freeze_orientation(self, enable):
        # To be implemented in sub class
        pass

    # Misc. Operation Functions
    def implicit_wait(self, time):
        # To be implemented in sub class
        pass

    def open_notification(self):
        # To be implemented in sub class
        pass

    def put_file(self, src_path, dst_path):
        # To be implemented in sub class
        pass

    def get_file(self, src_path, dst_path):
        # To be implemented in sub class
        pass

    # Element Operation Functions
    def get_text(self, locator):
        # To be implemented in sub class
        pass

    def set_text(self, locator, text, clear_flag):
        # To be implemented in sub class
        pass

    def get_element(self, locator, timeout, options):
        # To be implemented in sub class
        pass

    def get_elements(self, locator, index, timeout, options):
        # To be implemented in sub class
        pass

    def click_element(self, locator):
        # To be implemented in sub class
        pass

    def tap_element(self, locator):
        # To be implemented in sub class
        pass

    def long_press_element(self, locator):
        # To be implemented in sub class
        pass

    def swipe_element(self, locator, direction, offset):
        # To be implemented in sub class
        pass

    def swipe_to_element(self, locator, direction, target_locator):
        # To be implemented in sub class
        pass

    def drag_element(self, src_locator, destination):
        # To be implemented in sub class
        pass

    def pinch_element(self, locator, percentage, steps):
        # To be implemented in sub class
        pass

    def zoom_element(self, locator, percentage, steps):
        # To be implemented in sub class
        pass

    def pinch_zoom_element(self, locator, scale):
        # To be implemented in sub class
        pass

    def rotate_element(self, locator, angle):
        # To be implemented in sub class
        pass

    def set_checkbox(self, locator, status):
        # To be implemented in sub class
        pass

    def set_dropdown(self, locator, item):
        # To be implemented in sub class
        pass

    def set_slider(self, locator, percentage):
        # To be implemented in sub class
        pass

    def get_toast_text(self):
        # To be implemented in sub class
        pass

    def handle_alert(self, flag):
        # To be implemented in sub class
        pass

    # Check Element Status Functions
    def is_element_displayed(self, locator):
        # To be implemented in sub class
        pass

    # Wait Element Functions
    def wait_until_element_exist(self, locator, timeout):
        # To be implemented in sub class
        pass

    def wait_until_element_not_exist(self, locator, timeout):
        # To be implemented in sub class
        pass

    def wait_until_element_selected(self, locator, timeout):
        # To be implemented in sub class
        pass

    def wait_until_element_clickable(self, locator, timeout):
        # To be implemented in sub class
        pass

    # Mobile Gesture Functions
    def swipe(self, start_x, start_y, end_x, end_y, duration=None):
        # To be implemented in sub class
        pass

    def drag_slider_from_center_to_left(self, locator):
        # To be implemented in sub class
        pass

    def drag_slider_from_center_to_right(self, locator):
        # To be implemented in sub class
        pass
