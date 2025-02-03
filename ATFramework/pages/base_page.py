# This is the base page which defines attributes and methods that all other pages will share

try:
    import unittest
    import datetime
    import inspect
    import os
    import time
    from reportportal_client import step

    from ATFramework.utils.log import logger
    from ATFramework.utils.ocr import OCR
    from ATFramework.utils.Image_Search import CompareImage

    from AppKit import NSScreen

    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    from PIL import ImageGrab, Image

except Exception as e:
    logger(f"[Warning] {e}")

# class Borg:
#     # The borg design pattern is to share state
#     # Src: http://code.activestate.com/recipes/66531/
#     __shared_state = {}
#
#     def __init__(self):
#         self.__dict__ = self.__shared_state
#
#     def is_first_time(self):
#         # Has the child class been invoked before?
#         result_flag = False
#         if len(self.__dict__) == 0:
#             result_flag = True
#
#         return result_flag



class BasePage(unittest.TestCase):
    DEFAULT_TIMEOUT = 5
    DEFAULT_POLL_TIME = 0.1
    default_wait = 5
    default_timeout = 30

    def __init__(self, driver):
        # Borg.__init__(self)
        unittest.TestCase.__init__(self)
        self.driver = driver

    # Driver Functions
    def get_driver(self):
        return self.driver

    def set_driver(self, driver):
        self.driver = driver

    def stop_driver(self):
        return self.driver.stop_driver()

    # App Management Functions
    def install_app(self, path, package):
        return self.driver.install_app(path, package)

    def remove_app(self, package):
        return self.driver.remove_app(package)

    def start_app(self, package):
        return self.driver.start_app(package)

    def stop_app(self, package):
        return self.driver.stop_app(package)

    def activate_app(self, package):
        return self.driver.activate_app(package)

    def background_app(self, package):
        return self.driver.background_app(package)

    def reset_app(self, package):
        return self.driver.reset_app(package)

    # Orientation Control Functions
    def get_orientation(self):
        return self.driver.get_orientation()

    def set_orientation(self, orientation):
        return self.driver.set_orientation(orientation)

    def freeze_orientation(self):
        return self.driver.freeze_orientation()

    # Misc. Operation Functions
    def implicit_wait(self, time):
        return self.driver.implicit_wait(time)

    def open_notification(self):
        return self.driver.open_notification()

    def put_file(self, path, file):
        return self.driver.put_file(path, file)

    def get_file(self, path):
        return self.driver.get_file(path)

    def get_snapshot(self, path):
        return self.driver.get_snapshot(path)

    # Mobile Gesture Functions
    def swipe(self, start_x, start_y, end_x, end_y, duration=None):
        return self.driver.swipe(start_x, start_y, end_x, end_y, duration)

    # Element Operation Functions
    def get_text(self, locator):
        return self.driver.get_text(locator)

    def set_text(self, locator, text, clear_flag=0):
        return self.driver.set_text(locator, text, clear_flag)

    def get_element(self, locator, timeout=DEFAULT_TIMEOUT, options=None):
        return self.driver.get_element(locator, timeout, options)

    def get_elements(self, locator, index, timeout=DEFAULT_TIMEOUT, options=None):
        return self.driver.get_elements(locator, index, timeout, options)

    def click_element(self, locator):
        return self.driver.click_element(locator)

    def tap_element(self, locator):
        return self.driver.tap_element(locator)

    def tap(self, pos):
        return self.driver.tap(pos)

    def tap_screen_center(self, x=0, y=0):
        return self.driver.tap_screen_center(x, y)

    def double_tap_element(self, locator, interval=0.2):
        return self.driver.double_tap_element(locator, interval)

    def long_press_element(self, locator):
        return self.driver.long_press_element(locator)

    def swipe_element(self, locator, direction,offset=0.55):
        return self.driver.swipe_element(locator, direction,offset)

    def swipe_to_element(self, locator, direction, target_locator):
        return self.driver.swipe_to_element(locator, direction, target_locator)

    def drag_element(self, src_locator, dst_locator):
        return self.driver.drag_element(src_locator, dst_locator)

    def pinch_element(self, locator, percentage, steps):
        return self.driver.pinch_element(locator, percentage, steps)

    def zoom_element(self, locator, percentage, steps):
        return self.driver.zoom_element(locator, percentage, steps)

    def pinch_zoom_element(self, locator, scale):
        return self.driver.pinch_zoom_element(locator, scale)

    def rotate_element(self, locator, angle):
        return self.driver.rotate_element(locator, angle)

    def set_checkbox(self, locator, status):
        return self.driver.set_checkbox(locator, status)

    def set_dropdown(self, locator, item):
        return self.driver.set_combobox(locator, item)

    def set_slider(self, locator, percentage):
        return self.driver.set_slider(locator, percentage)

    def get_toast_text(self):
        return self.driver.get_toast_text()

    def handle_alert(self, flag):
        return self.driver.handle_alert(flag)

    # Check Element Status Functions
    def is_element_displayed(self, locator):
        return self.driver.is_element_displayed(locator)

    def is_element_highlighted(self, locator):
        return self.driver.is_element_highlighted(locator)

    def is_element_enabled(self, locator):
        return self.driver.is_element_enabled(locator)

    # Wait Element Functions
    def wait_until_element_exist(self, locator, timeout=DEFAULT_TIMEOUT):
        return self.driver.wait_until_element_exist(locator, timeout)

    def wait_until_element_not_exist(self, locator, timeout=DEFAULT_TIMEOUT):
        return self.driver.wait_until_element_not_exist(locator, timeout)

    def wait_until_element_selected(self, locator, timeout=DEFAULT_TIMEOUT):
        return self.driver.wait_until_element_selected(locator, timeout)

    def wait_until_element_clickable(self, locator, timeout=DEFAULT_TIMEOUT):
        return self.driver.wait_until_element_clickable(locator, timeout)

    def drag_slider_from_center_to_left(self, locator):
        return self.driver.drag_slider_from_center_to_left(locator)

    def drag_slider_from_center_to_right(self, locator):
        return self.driver.drag_slider_from_center_to_right(locator)

    # =============================== for snapshot/ocr ===================================
    rename_file = datetime.datetime.now().strftime(f'%m%d_%H%M%S_Error.png')
    temp_img_path = os.path.dirname(os.getcwd()) + f'/Material/screenshot.png'
    temp_img_folder = os.path.dirname(os.getcwd()) + f'/Material/'
    rename_img_path = os.path.dirname(os.getcwd()) + f'/log/{rename_file}'
    def get_screenshot_as_file(self, file_path):
        self.snapshot(file_path)

    def snapshot(self, path=None, crop=None):
        """
        crop area input: (x, y, w, h), need parameter:(x, y, x + w, y + h)
        :param path:
        :param crop:
        :return:
        """
        try:
            if os.path.isfile(self.temp_img_path):
                self.remove_snapshot()
            if path is None:
                path = self.temp_img_path
            logger(os.path.exists(self.temp_img_folder))
            if os.path.exists(self.temp_img_folder) is False:
                os.mkdir(self.temp_img_folder)
            ImageGrab.grab().save(path)
            #os.system(f"screencapture {path}")
            if crop:
                # resize to handle scale problem
                w = int(NSScreen.mainScreen().frame().size.width)
                h = int(NSScreen.mainScreen().frame().size.height)
                im = Image.open(path)
                pos_re = im.size
                def resize(pos, org_sharp, re_sharp):
                    pos = (int(pos[0] * org_sharp[0] / re_sharp[0]),
                           int(pos[1] * org_sharp[1] / re_sharp[1]),
                           int(pos[2] * org_sharp[0] / re_sharp[0]),
                           int(pos[3] * org_sharp[1] / re_sharp[1]))
                    return pos
                crop = (crop[0], crop[1], crop[0] + crop[2], crop[1] + crop[3])
                crop = resize(crop, pos_re, (w, h))
                im_crop = im.crop(crop)
                im_crop.save(path)
            logger(f'snapshot - {path}')
            return True
        except Exception as e:
            logger(f'Exception: ({e})')
            return False

    def compare(self, img1, img2, rate=4):  # img1: snapshot , img2: base
        new_path1 = img1 if os.path.isfile(img1) else os.path.dirname(os.getcwd()) + r'/BFT/' + img1
        new_path2 = img2 if os.path.isfile(img2) else os.path.dirname(os.getcwd()) + r'/BFT/' + img2
        return CompareImage(new_path1, new_path2, rate).compare_image()

    def remove_snapshot(self, path=None):
        """
        Need to assert file exists or exception
        :return: None
        """
        try:
            if path is None:
                path = self.temp_img_path
                os.remove(path)
            else:
                os.remove(path)
        except Exception as e:
            logger(f'Exception: ({e})')

    def rename_snapshot(self):
        """
        :return:
        """
        for x in range(10):
            try:
                logger(f'{self.temp_img_path}\n'
                       f'{self.rename_img_path}')
                os.rename(self.temp_img_path, self.rename_img_path)
                return True
            except:
                logger(f'rename fail at {x + 1}-times')
            time.sleep(1)
        return False

    def search_text_position(self, text, mouse_move=1, order=1):
        if mouse_move == 1:
            self.move_mouse((1, 1))
        time.sleep(1)
        if self.driver.image.snapshot(self.temp_img_path):
            pos = OCR(self.temp_img_path, text).get_pos(order)
            if pos is not False:
                logger(f'pos(before resize): ({pos})')
                # resize to handle scale problem
                w = int(NSScreen.mainScreen().frame().size.width)
                h = int(NSScreen.mainScreen().frame().size.height)
                im = Image.open(self.temp_img_path)
                pos_re = im.size
                logger(f'pos(after resize): ({(int(pos[0] * w / pos_re[0]), int(pos[1] * h / pos_re[1]))})')
                #self.remove_snapshot()
                return (int(pos[0] * w / pos_re[0]), int(pos[1] * h / pos_re[1]))
            else:
                #self.rename_snapshot()
                logger('get pos fail')
                return False
        else:
            logger('snapshot fail')
        return False

    def search_pos_from_image(self, target_name, ground_truth_folder, mouse_move=1, order=1):
        # /Users/terencechang/Dropbox/MyATproject/2_Mac_AT/Project_PDR_Mac_AT/SFT/Material/MBP16/indicator.png
        # ground truth folder
        ground_truth_folder = self.temp_img_folder + f'{ground_truth_folder}/'
        target_img_path = ground_truth_folder + f'{target_name}'
        logger(target_img_path)
        logger(ground_truth_folder)
        # make sure ground truth img exists
        if not os.path.exists(target_img_path):
            logger(f"Can't find ground truth img. ({target_img_path})")
            return False
        # start to snapshot tmp
        if mouse_move == 1:
            self.move_mouse((1, 1))
        time.sleep(1)
        if self.snapshot():
            pos = CompareImage(self.temp_img_path, target_img_path, 3).search_image(order=order)
            if pos is not False:
                logger(f'pos(before resize): ({pos})')
                # resize to handle scale problem
                w = int(NSScreen.mainScreen().frame().size.width)
                h = int(NSScreen.mainScreen().frame().size.height)
                im = Image.open(self.temp_img_path)
                pos_re = im.size
                logger(f'pos(after resize): ({(int(pos[0] * w / pos_re[0]), int(pos[1] * h / pos_re[1]))})')
                self.remove_snapshot()
                return (int(pos[0] * w / pos_re[0]), int(pos[1] * h / pos_re[1]))
            else:
                self.rename_snapshot()
                logger('get pos fail')
                return False
        else:
            logger('snapshot fail')
        return False

    # ==================================================================

    def input_keyboard(self, key):
        return self.driver.input_keyboard(key)

    def input_combo_keyboard(self, key1, key2, key3=None):
        return self.driver.input_combo_keyboard(key1, key2, key3)

    def multi_select(self, pos):
        return self.driver.multi_select(pos)

    def input_triple_keyboard(self, key1, key2, key3):
        return self.driver.input_triple_keyboard(key1, key2, key3)

    def input_text(self, text):
        return self.driver.input_text(text)

    def get_mouse_pos(self):
        return self.driver.get_mouse_pos()

    def click(self, button='left', times=1):
        return self.driver.click(button, times)

    def move_mouse(self, destination):
        return self.driver.move_mouse(destination)

    def drag_mouse(self, start_pos, destination):
        return self.driver.drag_mouse(start_pos, destination)

    def drag_mouse_per_pixel(self, start_pos, destination):
        return self.driver.drag_mouse_per_pixel(start_pos, destination)

    def drag_element_to(self, el1, el2):
        return self.driver.drag_element_to(el1, el2)

    def tap_pos(self, pos):
        return self.driver.tap_pos(pos)

    def tap_locator(self, locator):
        return self.driver.tap_locator(locator)

    def tap_element(self, element):
        return self.driver.tap_element(element)

    def adjust_element_slider(self, element, value, min=1, max=100, edge=6, tolerance=None):
        return self.driver.adjust_element_slider(element, value, min, max, edge, tolerance)

    def adjust_locator_slider(self, locator, value, min=1, max=100, edge=6, tolerance=None):
        return self.driver.adjust_locator_slider(locator, value, min, max, edge, tolerance)

    def set_text_on_locator(self, locator, text, press_enter=1, double_click=0):
        return self.driver.set_text_on_locator(locator, text, press_enter, double_click)

    def set_text_on_element(self, element, text, press_enter=1, double_click=0):
        return self.driver.set_text_on_element(element, text, press_enter, double_click)

    def set_text_on_pos(self, pos, text, press_enter=1, double_click=0):
        return self.driver.set_text_on_pos(pos, text, press_enter, double_click)

    # ==== execution functions ====
    @step('[Action] Launch App')
    def launch_app(self, timeout=15):
        if self.is_app_exist(2): self.close_app()
        return self.driver.launch_app(timeout)

    @step('[Action] Close App')
    def close_app(self, forcemode=0, timeout=15):
        return self.driver.close_app(forcemode, timeout)

    @step('[Verify] Check if App Exist')
    def is_app_exist(self, timeout=10):
        for _ in range(timeout):
            if self.driver.is_app_exist():
                return True
            time.sleep(1)

    def get_pid(self):
        return self.driver.get_pid()

    # ==== Get functions ====
    def get_top_element(self):
        return self.driver.get_top_element()

    def get_current_wnd(self, el):
        return self.driver.get_current_wnd(el)

    def get_child_wnd(self, el):
        return self.driver.get_child_wnd(el)

    def get_parent_wnd(self, el):
        return self.driver.get_parent_wnd(el)

    def get_axtitle(self, el):
        return self.driver.get_axtitle(el)

    def get_axrole(self, el):
        return self.driver.get_axrole(el)

    def get_axvalue(self, el):
        return self.driver.get_axvalue(el)

    def get_axtype(self, el):
        return self.driver.get_axtype(el)

    def get_axlabel(self, el):
        return self.driver.get_axlabel(el)

    def get_axhelp(self, el):
        return self.driver.get_axhelp(el)

    def get_axposition(self, el):
        return self.driver.get_axposition(el)

    def get_axsize(self, el):
        return self.driver.get_axsize(el)

    def get_pos(self, el, int_rule=1):
        return self.driver.get_pos(el, int_rule)

    def get_mid_pos(self, el):
        return self.driver.get_mid_pos(el)

    def get_locator_pos(self, locator):
        return self.driver.get_locator_pos(locator)

    def get_locator_mid_pos(self, locator):
        return self.driver.get_locator_mid_pos(locator)

    def get_text(self, el):
        return self.driver.get_text(el)

    # ==== APPKit functions ====
    def get_top_wnd_name(self):
        return self.driver.get_top_wnd_name()

    # ==== Find functions ====
    def find_top_el_by_name(self, name):
        return self.driver.find_top_el_by_name(name)

    def wait_to_appear(self, locator, timeout=15):
        return self.driver.wait_to_appear(locator, timeout)

    def search_child_el_by_title(self, el, title):
        return self.driver.search_child_el_by_title(el, title)

    def search_child_el_by_role(self, el, axrole):
        return self.driver.search_child_el_by_role(el, axrole)

    def search_child_el_by_type(self, el, axtype):
        return self.driver.search_child_el_by_type(el, axtype)

    def search_child_el_by_label(self, el, axlabel):
        return self.driver.search_child_el_by_label(el, axlabel)

    def search_child_el_by_help(self, el, axhelp):
        return self.driver.search_child_el_by_label(el, axhelp)

    def search_child_el_by_property(self, el, property):
        return self.driver.search_child_el_by_property(el, property)

    def search_child_el(self, el, target, bywhat):
        return self.driver.search_child_el(el, target, bywhat)

    def search_child_el_by_index(self, el, index):
        return self.driver.search_child_el_by_index(el, index)

    def count_child_index_by_property(self, el, property):
        return self.driver.count_child_index_by_property(el, property)

    def search_el_by_path(self, locator):
        return self.driver.search_el_by_path(locator)

    def search_el_by_ato_findFirstR(self, **kwargs):
        return self.driver.search_el_by_ato_findFirstR(**kwargs)

    def search_el(self, locator):
        return self.driver.search_el(locator)

    def search_all_el(self, locator, index=None):
        return self.driver.search_all_el(locator, index)

    # ==== investigate functions ====
    def get_Attributes(self, el):
        return self.driver.get_Attributes(el)

    def get_Actions(self, el):
        return self.driver.get_Actions(el)

    # ==== MWC Action class ====
    def Press(self, el):
        return el.Press()

    def click_mouse(self, pos, button='left', times=1):
        return self.driver.click_mouse(pos, button, times)

    def clickMouseButtonLeft(self, pos, interval=None):
        return self.driver.clickMouseButtonLeft(pos, interval)

    def doubleClickMouse(self, pos):
        return self.driver.doubleClickMouse(pos)

    def activate(self, el):
        return el.activate()

    def is_element_enabled(self, el):
        return self.driver.is_element_enabled(el)

    def is_element_selected(self, el):
        return self.driver.is_element_selected(el)

    def is_element_ticked(self, el):
        return self.driver.is_element_ticked(el)

    # ==== generator functions ====
    def generator_verify(self, locator_result, locator_org):
        return self.driver.generator_verify(locator_result, locator_org)

    def locator_generator(self, locator, forcemode='normal'):
        return self.driver.locator_generator(locator, forcemode)
