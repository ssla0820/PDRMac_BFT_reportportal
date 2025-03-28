import copy
import inspect
import os
import time
import shutil
import platform
from reportportal_client import step

from ATFramework.pages.base_page import BasePage
from ATFramework.utils import logger

from .locator import locator as L

OPERATION_DELAY = 1  # sec


class BasePage(BasePage):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.driver = arg[0]
        self.mouse = self.driver.mouse
        self.keyboard = self.driver.keyboard
        self.image = self.driver.image
        # self.top = None #self.driver.get_top()
        self.size = self.driver.size
        self.area = L.base.Area()
        self.file = self.driver.file
        self.backdoor = Backdoor(self.driver)

    def is_os_version(self, version="10.16"):
        return self.driver.is_os_version(version)

    def is_os_version_greater_than_or_equal_to(self, version='10.16'):
        return self.driver.is_os_version_greater_than_or_equal_to(version)

    def is_apple_cpu(self):
        return "Apple" in self.driver.get_cpu_brand()

    def is_intel_cpu(self):
        return "Intel" in self.driver.get_cpu_brand()

    def get_top(self):
        return self.driver.get_top()

    def refresh_top(self):  # to refresh the hierarchy top
        self.driver.get_top()
        return True

    def activate(self, timeout=5):
        timer = time.time()
        while time.time() - timer < timeout:
            self.driver.activate()
            if self.driver.is_active(): break
        else:
            return False
        return True

    def find(self, locator, parent=None, timeout=3):  # reutrn single element
        ret = self.exist(locator, parent, timeout)
        if ret:
            return ret
        else:
            raise Exception(f"Element is not found. {locator}")

    def find_elements(self, locator, parent=None):  # return elements as list
        return self.exist_elements(locator, parent, timeout=0)

    def find_str(self, string, extra):
        self.find("{AX}")  # TODO

    def el_click(self, el, x_offset=0, y_offset=0):  # el = self.exist(locator, parent)
        el_position = el.AXPosition
        el_size = el.AXSize
        x_axis = el_position[0] + int(el_size[0] / 2) + x_offset
        y_axis = el_position[1] + int(el_size[1] / 2) + y_offset
        self.mouse.click(x_axis, y_axis)
        return True

    def exist(self, locator, parent=None, timeout=5, interval=0.25, no_warning=False, refresh_top=True):
        try:
            parent.activate()
        except:
            if refresh_top:
                parent = self.get_top()
            else:
                return None
        if not isinstance(locator, (dict, list)): return parent
        locator = locator.copy()
        if isinstance(locator, dict):
            # logger(f'{parent=}')
            # logger(f'{locator=}')
            index = int(locator.pop("index", 0))
            recursive = bool(locator.pop("recursive", True))
            get_all = bool(locator.pop("get_all", False))
            # logger(f'{index=}')
            method = [[parent.findFirst, parent.findAll],
                      [parent.findFirstR, parent.findAllR]][recursive][bool(index or get_all)]
            timer = time.time()
            while time.time() - timer < timeout:
                ret = method(**locator)[index] if index and not get_all else method(**locator)
                if ret:
                    if not isinstance(ret, list): ret.activate()
                    return ret
                time.sleep(interval)
            else:
                ret = method(**locator)[index] if index and not get_all else method(**locator)
                if (not ret) and (not no_warning): logger(f"[Locator] The element is not found via >> {locator} <<")
                return ret

        if isinstance(locator, list):
            for item in locator:
                parent = self.exist(item, parent, timeout, interval, no_warning, refresh_top=refresh_top)
                if not parent: return None
            return parent

    def exist_elements(self, locator, parent=None, timeout=5, interval=0.25):
        parent = parent or self.get_top()
        if not isinstance(locator, (dict, list)): return parent
        locator = locator.copy()
        if isinstance(locator, dict):
            method = parent.findAllR
            timer = time.time()
            while time.time() - timer < timeout:
                ret = method(**locator)
                if ret:
                    ret[0].activate()
                    return ret
                time.sleep(interval)
            else:
                return method(**locator)
        if isinstance(locator, list):
            for index in range(len(locator)):
                if index < len(locator) - 1:
                    parent = self.exist(locator[index], parent)
                    if not parent: return None
                else:
                    parent = self.exist_elements(locator[index], parent)
                    if not parent: return None
            return parent

    @step("[Action] Base_page: Compare Images")
    def compare(self, source_path, target_path, similarity=0.95, color=False):
        logger(f"{source_path=}\n{target_path=}\n{similarity=}")
        try:
            if not os.path.exists(source_path):
                logger(f"[Ground Truth] Generating >> {source_path} <<")
                os.makedirs(os.path.dirname(source_path), exist_ok=True)
                shutil.copyfile(target_path, source_path)
                return
            ret = self.image.search(source_path, target_path, color=color)
            logger(f"Result similarity = {ret.similarity}")
            return True if ret.similarity > similarity else False
        except Exception as e:
            logger(f"compare fail -> {e}")

    def compare_video(self, source_path, target_path):
        if not os.path.exists(source_path) or not os.path.exists(target_path):
            logger("file is not found")
            return
        return self.driver.video.compare(source_path, target_path)

    def is_exist(self, locator, parent=None, timeout=5, interval=0.25):
        return bool(self.exist(locator, parent, timeout, interval, no_warning=True))

    def is_not_exist(self, locator, parent=None, timeout=5, interval=0.25):
        timer = time.time()
        while time.time() - timer < timeout:
            if not self.exist(locator, parent, 0.5, interval, no_warning=True): return True
        else:
            return False

    def exist_click(self, locator, parent=None, btn="left",
                    timeout=5, interval=0.25, times=1, _mouse_click=True, no_warning=False, refresh_top=True):
        elem = self.exist(locator, parent, timeout, interval, no_warning=no_warning, refresh_top=refresh_top)
        if elem:
            if _mouse_click:
                self.mouse.click(*elem.center, btn, times=times)
            else:
                for _ in range(times):
                    elem.press()
        return elem

    def exist_press(self, locator, parent=None, timeout=5, interval=0.25, times=1,
                    _mouse_click=False, no_warning=False):
        return self.exist_click(locator, parent, None, timeout, interval, times, _mouse_click, no_warning)

    def click(self, locator, btn="left", times=1):
        if locator is None:
            self.mouse.click(btn=btn, times=times)
        else:
            if not self.exist_click(locator, btn=btn, times=times):
                logger(f"Unable to click {locator=}")
                raise Exception(f"Unable to click {locator=}")
        return True

    def press(self, locator, times=1):
        for _ in range(times):
            self.find(locator).press()
        return True

    def wait(self, locator, timeout=5):
        return bool(self.exist(locator, timeout=timeout))

    def search(self, image, area=None, similarity=0.95):
        source_dict = {"x": 0, "y": 0, "h": self.size["h"], "w": self.size["w"]}
        if area:
            elem = self.find(area)
            x, y = elem.AXPosition
            w, h = elem.AXSize
            source_dict.update({"x": x, "y": y, "w": w, "h": h})
        source = self.image.snapshot(**source_dict)
        ret = self.image.search(source, image)
        return {"x": ret.x, "y": ret.y, "w": ret.w, "h": ret.h} if ret.similarity > similarity else None

    def screenshot(self, **kwargs):
        return self.image.screenshot(**kwargs)

    @step("[Action] Base_page: Snapshot")
    def snapshot(self, locator, file_name=None):
        try:
            if isinstance(locator, (list, dict)):
                elem = self.find(locator)
            else:
                elem = locator
            w, h = elem.AXSize
            x, y = elem.AXPosition
            return self.screenshot(file_name=file_name, w=w, x=x, y=y, h=h)
        except Exception as e:
            logger(f"[Warning] : {e}")
            return None

    def snapshot_library_insert_icon(self, name, file_name=None):
        try:
            # If find Template > Find his parent
            elem = self.exist({"AXIdentifier": "CollectionViewItemTextField", "AXValue": name}).AXParent
            # Find the child (which has AXImage attribute)
            elem_image = self.exist(locator={"AXRole": "AXImage"}, parent=elem)

            if not elem_image:
                logger('Cannot find the Template name in Media Room')
                return None
            else:
                w, h = elem_image.AXSize
                x, y = elem_image.AXPosition

                # snapshot region is (right top corner) of Thumbnail, size: 15*25
                # Only snapshot "tick icon (v)"
                new_x = x + w - 15
            return self.screenshot(file_name=file_name, w=15, x=new_x, y=y, h=25)
        except Exception as e:
            logger(f"[Warning] : {e}")
            return None

    def snapshot_my_favorites_left_panel(self, file_name=None, is_project_room=0):
        try:

            # Find import button
            elem_btn = self.exist(L.media_room.btn_import_media)

            if not elem_btn:
                logger('Cannot find the import button')
                return None
            else:
                w, h = elem_btn.AXSize
                x, y = elem_btn.AXPosition

                # snapshot region (Region: From import button to My Favorites)
                new_x = x - 14
                new_y = y
                new_w = w + 126
                if is_project_room:
                    new_h = h + 75
                else:
                    new_h = h + 34
            return self.screenshot(file_name=file_name, w=new_w, x=new_x, y=new_y, h=new_h)
        except Exception as e:
            logger(f"[Warning] : {e}")
            return None

    @step("[Action][Base Page] Snapshot [Heart Icon] on thumbnail (name)")
    def snapshot_library_heart_icon(self, name, file_name=None):
        try:
            # If find Template > Find his parent
            elem = self.exist({"AXIdentifier": "CollectionViewItemTextField", "AXValue": name}).AXParent
            # Find the child (which has AXImage attribute)
            elem_image = self.exist(locator={"AXRole": "AXImage"}, parent=elem)

            if not elem_image:
                logger('Cannot find the Template name in Current Room')
                return None
            else:
                x, y = elem_image.AXPosition

                # snapshot region is (bottom right) of Thumbnail, size: 20*30 for 16:9 aspect ratio
                # Only snapshot "heart icon"
                new_x = x + 91
                new_y = y + 59

            return self.screenshot(file_name=file_name, w=20, x=new_x, y=new_y, h=20)
        except Exception as e:
            logger(f"[Warning] : {e}")
            return None

    def click_template_its_heart_icon(self, name):
        try:
            # If find Template > Find his parent
            elem = self.exist({"AXIdentifier": "CollectionViewItemTextField", "AXValue": name}).AXParent
            # Find the child (which has AXImage attribute)
            elem_image = self.exist(locator={"AXRole": "AXImage"}, parent=elem)

            if not elem_image:
                logger('Cannot find the Template name in Current Room')
                return False
            else:
                x, y = elem_image.AXPosition

                new_x = x + 92
                new_y = y + 50
                self.mouse.move(new_x, new_y)
                time.sleep(1)
                self.mouse.click()
                self.move_mouse_to_0_0()
                time.sleep(1)
        except Exception as e:
            logger(f"[Warning] : {e}")
            return True

    def click_square_template_its_heart_icon(self, name):
        try:
            # If find Template > Find his parent
            elem = self.exist({"AXIdentifier": "CollectionViewItemTextField", "AXValue": name}).AXParent
            # Find the child (which has AXImage attribute)
            elem_image = self.exist(locator={"AXRole": "AXImage"}, parent=elem)

            if not elem_image:
                logger('Cannot find the Template name in Current Room')
                return False
            else:
                x, y = elem_image.AXPosition

                new_x = x + 93
                new_y = y + 70
                self.mouse.move(new_x, new_y)
                time.sleep(1)
                self.mouse.click()
                self.move_mouse_to_0_0()
                time.sleep(1)
        except Exception as e:
            logger(f"[Warning] : {e}")
            return True

    def check_current_preview(self, full_path, locator, similarity=0.95):
        return self.compare(full_path, locator, similarity)

    def unfold(self, locator, unfold=True):
        triangle = self.find(locator)
        if triangle.AXValue != unfold: triangle.press()
        timer = time.time()
        while time.time() - timer < 3:
            if self.find(locator).AXValue == unfold: return True
        else:
            return False

    def fold(self, locator):
        return self.unfold(locator, unfold=False)

    @step("[Action][Base_page] Double click")
    def double_click(self, locator=None, btn="left"):
        self.click(locator, btn, times=2)

    @step("[Action][Base_page] Right Click")
    def right_click(self, locator=None, btn="right"):
        self.click(locator, btn)

    def left_click(self, locator=None, btn="left"):
        self.click(locator, btn)

    @step("[Action][Base_page] Select specific tag with name")
    def select_specific_tag(self, name):
        tags = self.exist(L.base.tag_list)
        tags_2 = self.exist(L.base.tag_list_2)
        if tags_2: tags.extend(tags_2)
        for tag in tags:
            if tag.AXValue.startswith(f"{name} ("):
                self.mouse.click(*tag.center)
                return True

    @step("[Action][Base_page] Select Library Room category")
    def select_LibraryRoom_category(self, name):
        category = self.exist(L.base.category)
        category._activate()
        self.mouse.click(*category.center)
        items = self.exist(L.base.category_items)
        for item in items:
            if item.AXValue == name:
                self.mouse.click(*item.center)
                return True
        time.sleep(OPERATION_DELAY)
        return False
    
    @step("[Action][Base_page] Unfold [CLUT] category")
    def unfold_clut_category(self):
        try:
            # unfold CLUT category
            tags_2 = self.exist(L.base.tag_list_2)
            for tag in tags_2:
                if tag.AXValue.startswith(f"Color LUT ("):
                    x, y = tag.AXPosition  # 61, 267
                    # w, h = 143, 16

                    new_x = x + 18
                    new_y = y - 2
                    self.mouse.move(new_x, new_y)
                    self.mouse.click()
                    break
            time.sleep(OPERATION_DELAY * 2)
        except Exception as e:
            logger(f"[Warning] : {e}")
            raise Exception("Unfold CLUT category failed")

    def _close_menu(self):
        x, y = self.mouse.position()
        self.mouse.move(0, self.size["h"] - 1, duration=0.01, wait=0.01)
        self.mouse.click()
        self.mouse.move(x, y, duration=0.01, wait=0.01)

    @step("[Action][Base_page] Select right click menu")
    def select_right_click_menu(self, *arg, return_elem=False, click_it=True, return_is_selected=False):
        if return_elem or return_is_selected: click_it = False
        item = None
        arg_list = list(arg)
        try:
            while item_name := arg_list.pop(0):
                item = self.find({"AXRole": "AXMenuItem", "AXTitle": item_name}, parent=item)
                # print(f"{item=}")
                if not item.AXEnabled:
                    self._close_menu()
                    return False
                if arg_list or click_it:
                    self.mouse.move(item.center[0], self.mouse.position()[1])
                    self.mouse.click(*item.center)
                elif return_elem:
                    return item
                elif return_is_selected:
                    ret = bool(item.AXMenuItemMarkChar)
                    self._close_menu()
                    return ret
                else:
                    self._close_menu()
                    return True
        except IndexError:
            return True
    # def select_right_click_menu(self, *arg, return_elem=False, click_it=True, return_is_selected=False):
    #     if return_elem or return_is_selected: click_it = False
    #     item = None
    #     arg_list = list(arg)
    #     logger(f'arg_list= {arg_list}')
    #     index = len(arg_list)-1
    #     try:
    #         while index >=0:
    #             item_name = arg_list[index]
    #         # while item_name := arg_list.pop(0):
    #             item = self.find({"AXRole": "AXMenuItem", "AXTitle": item_name}, parent=item)
    #             # print(f"{item=}")
    #             if not item.AXEnabled:
    #                 self._close_menu()
    #                 return False
    #             if arg_list or click_it:
    #                 self.mouse.move(item.center[0], self.mouse.position()[1])
    #                 self.mouse.click(*item.center)
    #             elif return_elem:
    #                 return item
    #             elif return_is_selected:
    #                 ret = bool(item.AXMenuItemMarkChar)
    #                 self._close_menu()
    #                 return ret
    #             else:
    #                 self._close_menu()
    #                 return True
    #             index -=1
    #     except IndexError:
    #         raise Exception("Item is not found")
        

    def is_right_click_menu_enabled(self, *arg):
        return self.select_right_click_menu(*arg, return_elem=False, click_it=False)

    @step("[Action][Base_page] Select file in file picker")
    def select_file(self, full_path, btn_confirm=None, click_times=2):  # btn_confirm: 'Open', 'Save'
        btn_confirms = [btn_confirm] if btn_confirm else ["Open", "Save", "Select"]
        full_path = os.path.abspath(full_path)
        if not os.path.exists(full_path):
            logger(f"[Warning] Target path >> {full_path} << is not found")
        if not full_path.startswith("/Users/"):
            logger(f"[Error] Path must starts with '/Users/'")
            raise Exception("Path path incorrect")
        path = full_path.lstrip("/Users").split("/")
        '''
        # force switch to column view
        if not (opt := self.exist(L.base.file_picker.view_options)):
            raise Exception("[Error] File picker window is not exist")
        if opt.AXDescription != "column view":
            logger("Force switch to column view")
            self.mouse.click(*opt.center)
            self.mouse.click(*self.find(L.base.file_picker.column_view).center)
            time.sleep(0.2)
        '''
        if self.is_os_version_greater_than_or_equal_to("10.16"):
            _file_name = L.base.file_picker.file_name_big_sur
            time.sleep(1.5)
        else:
            _file_name = L.base.file_picker.file_name
        self.exist(L.base.file_picker.popup_button)

        try:
            if show_more := self.exist(L.base.file_picker.show_more_options, timeout=5):
                if not show_more.AXValue:
                    show_more.press()
                    time.sleep(5)
                self.find(_file_name).AXValue = path.pop(-1)
        except:
            logger("Disclosure Triangle is not found")

        base = "/Users/" + path.pop(0)

        dialog_list = [
            {"AXSubrole": "AXDialog"},
            {"AXRole": "AXSheet"}
        ]
        for dialog_locator in dialog_list:
            try:
                if self.exist(dialog_locator):
                    self.exist([dialog_locator, {"AXRole": "AXList", "index": -1}], timeout=0).AXFocused = True
                    break
            except:
                logger("search next dialog")
            if dialog_locator == dialog_list[-1]: raise Exception("File picker is not found")
        with self.keyboard.pressed(self.keyboard.key.cmd, self.keyboard.key.shift, "h"):
            time.sleep(1)
        for name in path:
            if os.path.exists(base := os.path.abspath(f"{base}/{name}")):
                self.keyboard.right()
                logger(f"{base=}")
                with self.keyboard.pressed(*name):
                    time.sleep(0.5)
            else:
                logger(f"folder is not exist: {base=} / {name=}")
                self.find({"AXRole": "AXButton", "AXTitle": "New Folder"}).press()
                time.sleep(1)
                if self.is_os_version_greater_than_or_equal_to("10.16"):
                    locators = [[{"AXIdentifier": "open-panel"}, {"AXRole": "AXSheet"}, {"AXRole": "AXTextField"}],
                                [{"AXIdentifier": "save-panel"}, {"AXRole": "AXSheet"}, {"AXRole": "AXTextField"}]]
                else:
                    locators = [[{'AXTitle': 'New Folder'}, {"AXRole": "AXTextField"}]]
                for locator in locators:
                    try:
                        input_text = self.exist(locator, timeout=1)
                        current_text = input_text.AXValue
                        break
                    except:
                        logger(f"not found - {locator}")
                        pass
                if current_text != name: input_text.AXValue = name
                time.sleep(1)
                self.find({"AXRole": "AXButton", "AXTitle": "Create"}).press()
                time.sleep(1)
                self.keyboard.right()
                time.sleep(0.5)
        for btn_name in btn_confirms:
            if btn := self.exist([
                dialog_locator,
                {"AXTitle": btn_name, "AXRole": "AXButton"},
            ], timeout=0, no_warning=True):
                self.mouse.click(*btn.center)
                return True
        return False

    def select_folder(self, full_path, btn_confirm=None):  # for select file/folder ONLY in file picker with full_path
        btn_confirms = [btn_confirm] if btn_confirm else ["Open", "Save", "Select"]
        full_path = os.path.abspath(full_path)
        if not os.path.exists(full_path):
            logger(f"[Warning] Target path >> {full_path} << is not found")
        if not full_path.startswith("/Users/"):
            logger(f"[Error] Path must starts with '/Users/'")
            raise Exception("Path path incorrect")
        path = full_path.lstrip("/Users").split("/")

        try:
            if show_more := self.exist(L.base.file_picker.show_more_options, timeout=0):
                if not show_more.AXValue:
                    show_more.press()
                    time.sleep(1)
        except:
            logger("Disclosure Triangle is not found")

        base = "/Users/" + path.pop(0)

        dialog_list = [
            {"AXSubrole": "AXDialog"},
            {"AXRole": "AXSheet"}
        ]
        for dialog_locator in dialog_list:
            try:
                if self.exist(dialog_locator):
                    self.exist([dialog_locator, {"AXRole": "AXList", "index": -1}], timeout=0).AXFocused = True
                    break
            except:
                logger("search next dialog")
            if dialog_locator == dialog_list[-1]: raise Exception("File picker is not found")
        with self.keyboard.pressed(self.keyboard.key.cmd, self.keyboard.key.shift, "h"):
            time.sleep(1)
        for name in path:
            if os.path.exists(base := os.path.abspath(f"{base}/{name}")):
                self.keyboard.right()
                logger(f"{base=}")
                with self.keyboard.pressed(*name):
                    time.sleep(0.5)
            else:
                logger(f"folder is not exist: {base=} / {name=}")
                self.find({"AXRole": "AXButton", "AXTitle": "New Folder"}).press()
                time.sleep(1)
                if self.is_os_version_greater_than_or_equal_to("10.16"):
                    locators = [[{"AXIdentifier": "open-panel"}, {"AXRole": "AXSheet"}, {"AXRole": "AXTextField"}],
                                [{"AXIdentifier": "save-panel"}, {"AXRole": "AXSheet"}, {"AXRole": "AXTextField"}]]
                else:
                    locators = [[{'AXTitle': 'New Folder'}, {"AXRole": "AXTextField"}]]
                for locator in locators:
                    try:
                        input_text = self.exist(locator, timeout=1)
                        current_text = input_text.AXValue
                        break
                    except:
                        logger(f"not found - {locator}")
                        pass
                if current_text != name: input_text.AXValue = name
                time.sleep(1)
                self.find({"AXRole": "AXButton", "AXTitle": "Create"}).press()
                time.sleep(1)
                self.keyboard.right()
                time.sleep(0.5)
        if btn_confirm != 'no_click':
            for btn_name in btn_confirms:
                if btn := self.exist([
                    dialog_locator,
                    {"AXTitle": btn_name, "AXRole": "AXButton"},
                ], timeout=0, no_warning=True):
                    self.mouse.click(*btn.center)
                    return True
        return False

    def get_position(self, locator):
        try:
            elem = self.find(locator)
            x, y = elem.AXPosition
            w, h = elem.AXSize
            return {"x": x, "y": y, "w": w, "h": h}
        except:
            return None

    @step("[Action][Base_page] Move mouse to position (0, 0)")
    def move_mouse_to_0_0(self):
        try:
            pos = self.mouse.position()
            self.mouse.move(0, 0)
            time.sleep(OPERATION_DELAY*0.5)
            return pos
        except:
            return None

    @step("[Action][Base_page] [Undo] via hotkey")
    def tap_Undo_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.cmd, "z"): pass

    def tap_Redo_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.shift, self.keyboard.key.cmd, "z"): pass

    def input_combo_keyboard_2(self, key_1, key_2):
        self.keyboard.press(key_1)
        self.keyboard.press(key_2)
        self.keyboard.release(key_2)
        self.keyboard.release(key_1)

    def input_combo_keyboard_3(self, key_1, key_2, key_3):
        self.keyboard.press(key_1)
        self.keyboard.press(key_2)
        self.keyboard.press(key_3)
        self.keyboard.release(key_3)
        self.keyboard.release(key_2)
        self.keyboard.release(key_1)

    @step("[Action][Base_page] Input keyboard")
    def input_keyboard(self, key):
        self.keyboard.press(key)
        self.keyboard.release(key)

    @step("[Action][Base_page] Input text")
    def input_text(self, text):
        self.keyboard.send(text)

    def press_del_key(self):
        # self.keyboard.tap(self.keyboard.key.delete)
        self.keyboard.tap(self.keyboard.key.backspace)  # It shows "delete" on MacBook
        
    @step("[Action][Base_page] Press [Backspace] key")
    def press_backspace_key(self):
        self.keyboard.tap(self.keyboard.key.backspace)

    def press_command_key(self):
        self.keyboard.tap(self.keyboard.key.cmd)

    def tap_command_and_hold(self):
        self.keyboard.press(self.keyboard.key.cmd)

    def release_command_key(self):
        self.keyboard.release(self.keyboard.key.cmd)

    @step("[Action][Base_page] Press [Esc] key")
    def press_esc_key(self):
        self.keyboard.tap(self.keyboard.key.esc)

    @step("[Action][Base_page] Press [Enter] key")
    def press_enter_key(self):
        self.keyboard.tap(self.keyboard.key.enter)

    @step("[Action][Base_page] Press [Space] key")
    def press_space_key(self):
        self.keyboard.tap(self.keyboard.key.space)

    def tap_Ctrl_and_hold(self):
        self.keyboard.press(self.keyboard.key.ctrl)

    def release_Ctrl_key(self):
        self.keyboard.release(self.keyboard.key.ctrl)

    @step("[Action][Base_page] Hover on button on launcher")
    def hover_launcher_btn(self, locator):
        launcher_btn = self.exist(locator)
        self.mouse.move(*launcher_btn.center)

    def hover_library_media(self, name):
        x, y = self.exist({"AXIdentifier": "CollectionViewItemTextField", "AXValue": name}).AXParent.center
        self.mouse.move(x, y)

    def tap_Preferences_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.cmd, ","):
            pass

    def tap_HidePDR_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.cmd, "h"):
            pass

    def tap_QuitPDR_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.cmd, "q"):
            pass

    def tap_CreateNewProject_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.cmd, "n"):
            pass
    
    @step('[Action][Base_page] Open [New Workspace] via hotkey')
    def tap_NewWorkspace_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.shift, self.keyboard.key.cmd, "w"):
            time.sleep(OPERATION_DELAY*0.5)

    def tap_OpenProject_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.cmd, "o"):
            pass

    def tap_SaveProject_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.cmd, "s"):
            pass

    def tap_SaveProjectAs_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.shift, self.keyboard.key.cmd, "s"):
            pass

    def tap_Cut_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.cmd, "x"):
            pass

    def tap_Copy_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.cmd, "c"):
            pass

    def tap_Paste_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.cmd, "v"):
            pass

    def tap_Remove_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.backspace):
            pass

    @step('[Action][Base_page] Tap [Select All] via hotkey')
    def tap_SelectAll_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.cmd, "a"):
            pass

    def EnterFullScreen_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.ctrl, self.keyboard.key.cmd, "f"):
            pass

    def SVRTInfo_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.alt, self.keyboard.key.cmd, "s"):
            pass

    # ======
    def tap_MinimizeWindow_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.cmd, "m"):
            pass

    def tap_MediaRoom_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.f3):
            pass
    
    @step('[Action][Base_page] Enter [Effect Room] via hotkey')
    def tap_EffectRoom_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.f4):
            pass
    
    @step('[Action][Base_page] Enter [PiP Room] via hotkey')
    def tap_PiPRoom_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.f5):
            pass

    def tap_ParticleRoom_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.f6):
            pass
    
    @step('[Action][Base_page] Enter [Title Room] via hotkey')
    def tap_TitleRoom_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.f7):
            pass

    @step('[Action][Base_page] Enter [Transition Room] via hotkey')
    def tap_TransitionRoom_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.f8):
            pass

    def tap_AudioMixingRoom_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.f9):
            pass

    def tap_VoiceRecordRoom_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.f10):
            pass

    def tap_SubtitleRoom_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.f12):
            pass

    def tap_Stop_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.cmd, "/"):
            pass

    def tap_NextFrame_hotkey(self):
        with self.keyboard.pressed("."):
            pass

    def tap_PreviousFrame_hotkey(self):
        with self.keyboard.pressed(","):
            pass

    def tap_FastForward_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.cmd, "f"):
            pass

    def tap_Snapshot_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.cmd, "p"):
            pass

    def tap_MarkIn_onLibraryPreview_hotkey(self):
        with self.keyboard.pressed("i"):
            pass

    def tap_MarkOut_onLibraryPreview_hotkey(self):
        with self.keyboard.pressed("o"):
            pass

    @step('[Action][Base_page] Enter [Split] via hotkey')
    def tap_Split_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.cmd, "t"):
            pass

    def tap_Trim_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.alt, self.keyboard.key.cmd, "t"):
            pass

    def tap_close_chrome_tab_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.cmd, "w"):
            pass
    
    @step("[Action][Base_page] Check if the preview window is different when playing")
    def Check_PreviewWindow_is_different(self, area=None, sec=1):
        area = area or self.area.preview.main
        old_img = self.snapshot(area)
        time.sleep(sec)
        new_img = self.snapshot(area)
        return not self.compare(old_img, new_img, 0.9999)

    @step("[Action][Base_page] Delete folder")
    def delete_folder(self, path):
        # Check if the local folder exists before deleting
        if os.path.exists(path):
            #  Execute shell command on the remote device
            self.driver.shell(f"rm -rf {path}")
        else:
            print(f"Warning: The path '{path}' does not exist locally.")

        return True


    @step("[Verify][Base_page] Check if the file exists")
    def exist_file(self, path):
        return os.path.exists(path)

    def click_OK_onEffectExtractor(self, timeout=10):
        is_pressed = False
        bundle_id = "com.cyberlink.EffectExtractor"
        timer = time.time()
        while (time.time() - timer < timeout) and not is_pressed:
            apps = self.driver.getRunningAppRefsByBundleId(bundle_id)
            for app in apps:
                btn = app.findAllR(AXTitle="OK", AXRole="AXButton")
                if btn:
                    time.sleep(0.2)
                    btn[0].press()
                    is_pressed = True
            if is_pressed:
                return True
            time.sleep(0.2)
        else:
            return False

    def click_OK_on_EffectExtractor(self, *args):
        return self.click_OK_onEffectExtractor(*args)

    def close_app(self, timeout=5):
        try:
            self.activate()
        except Exception as e:
            logger(f'app is not exist')
            return True

        timer = time.time()
        while time.time() - timer < timeout:
            if not self.is_alive(): break
            self.driver.terminate()
            time.sleep(0.5)
            if self.exist_click(L.base.quit_dialog.no, timeout=1, no_warning=True, refresh_top=False): break

        else:
            logger("Force close")
            self.driver.force_terminate()

    def is_alive(self, bundle_id="com.cyberlink.powerdirector"):
        try:
            return bool(self.driver.get_top(timeout=-1))
        except:
            return False

    @step("[Action][Base_page] Clear [AI Module] files")
    def clear_AI_module(self):
        # Clear AI module
        # /Users/qadf_12/Library/Group Containers/FPY8L862BK.com.cyberlink.powerdirector/Library/Shared Library/AI Component
        self.driver.shell(f"rm -r ~/Library/Group\ Containers/FPY8L862BK.com.cyberlink.powerdirector/Library/Shared\ Library/AI\ Component")

    def delete_custom_file(self, file_path):
        self.driver.shell(f"rm -r {file_path}")

    @step("[Action][Base_page] Clear [Remix] file")
    def clear_remix_file(self,file_name):
        # Clear Voice-Over Recording file
        self.driver.shell(f"rm -r ~/Movies/PowerDirector/{file_name}")

    @step("[Initial][Base Page] Clear capture file")
    def clear_capture_file(self):
        # Clear Voice-Over Recording file
        self.driver.shell(f"rm -r ~/Movies/PowerDirector/Capture.m4a")

    @step("[Initial][Base Page] Clear login account cache")
    def clear_log_in(self):
        logger("Clear login account cache")
        file_list= ["~Downloads/.Cyberlink/.CSE",
                    "~Downloads/.Cyberlink/.EvoParser", 
                    "~/Library/Group\ Containers/FPY8L862BK.com.cyberlink.powerdirector/Library/APREG"]
        self.driver.shell(f"rm -r ~/Downloads/.Cyberlink/.CSE")
        #self.driver.shell(f"rm -r ~/Downloads/.Cyberlink/.CBE")
        #self.driver.shell(f"rm -r ~/Downloads/.Cyberlink/.CLRC")
        self.driver.shell(f"rm -r ~/Downloads/.Cyberlink/.EvoParser")
        self.driver.shell(f"rm -r ~/Library/Group\ Containers/FPY8L862BK.com.cyberlink.powerdirector/Library/APREG")

        # # check if all file are deleted, if still exist, time.sleep(1) and check again until 5 times
        # for _ in range(10):
        #     if any([self.exist_file(file) for file in file_list]):
        #         for file in file_list:
        #             if self.exist_file(file):
        #                 logger(f"file {file} is not deleted, start to delete it")
        #                 self.driver.shell(f"rm -r {file}")
        #         time.sleep(OPERATION_DELAY)
        return True
    

    @step("[Initial] clear cache and GDPR")
    def clear_cache_and_gdpr(self):
        self.driver.shell(r'''
            defaults delete com.cyberlink.powerdirector
            defaults delete com.cyberlink.powerdirector.aspectRatio
            defaults delete com.cyberlink.powerdirector.mergeMediaLibrary
            defaults delete com.cyberlink.powerdirector.preferences
            defaults delete com.cyberlink.powerdirector.produceProfile
            defaults delete com.cyberlink.powerdirector.SubtitleTextSetting
            rm ~/Library/Application\ Support/com.cyberlink.powerdirector/UserConfigure/Profile.json
            rm -r ~/Library/Caches/com.cyberlink.powerdirector
            rm -r ~/Documents/Cyberlink/
            rm -r ~/Library/Application\ Support/com.cyberlink.powerdirector/cloudDB
            rm -r ~/Library/Application\ Support/com.cyberlink.powerdirector/GDPR
            rm -r ~/Library/Containers/com.cyberlink.powerdirectormac/Data/Library/Application\ Support/com.cyberlink.powerdirectormac/GDPR
            rm -r ~/Library/Containers/com.cyberlink.powerdirector/Data/Library/Application\ Support/com.cyberlink.powerdirector/GDPR
            rm -r ~/Library/Application\ Support/com.cyberlink.powerdirector/GDPR
            rm -r ~/Library/Application\ Support/com.cyberlink.powerdirector/UserConfigure/SimpleContainer
            rm ~/Library/Application\ Support/com.cyberlink.powerdirector/UserConfigure/Precut.json
            rm -r ~/Downloads/.Cyberlink/.CBE
            rm -r ~/Downloads/.Cyberlink/.EvoParser
            rm ~/Library/Application\ Support/com.cyberlink.powerdirector/UserConfigure/ClipMarkerCache/ClipMarker_0.json
            rm -r ~/Library/Application\ Support/com.cyberlink.powerdirector/Assets
            rm -r ~/Library/Application\ Support/com.cyberlink.powerdirector/UserConfigure
            rm -r ~/Library/Application\ Support/com.cyberlink.powerdirector/MyPinPs
            rm -r ~/Library/Application\ Support/com.cyberlink.powerdirector/MyCollage
            rm -r ~/Library/Application\ Support/com.cyberlink.powerdirector/MyParticles
            rm -r ~/Library/Application\ Support/com.cyberlink.powerdirector/MyTitles
            rm -r ~/Library/Application\ Support/com.cyberlink.powerdirector/ColorDirector\ presets
            rm -r ~/Library/Application\ Support/com.cyberlink.powerdirector/DZAPICache
            rm -r ~/Library/Application\ Support/com.cyberlink.powerdirector/cloudDB
            rm -r ~/Library/Group\ Containers/FPY8L862BK.com.cyberlink.powerdirector/Document/CyberLink
            rm -r ~/LocalAppData/CyberLink
            rm -r ~/Movies/CyberLink
            rm -r ~/Movies/PowerDirector
            rm -r ~/Movies/.Cache\ Files\ 01
            rm -r ~/Movies/.Cache\ Files\ 02
            rm -r ~/Music/Cyberlink/Downloaded\ Audio/.Cache\ Files\ 01
            rm -r ~/Library/Group\ Containers/rddf.com.cyberlink.powerdirector/Library/Caches/Preview\ Cache\ Files
            rm -r ~/Library/Group\ Containers/rddf.com.cyberlink.powerdirector/Library/Caches/ShadowEditFiles
            rm -r ~/Library/Group\ Containers/FPY8L862BK.com.cyberlink.powerdirector/Library/Caches/Preview\ Cache\ Files
            rm -r ~/Library/Group\ Containers/FPY8L862BK.com.cyberlink.powerdirector/Library/Caches/ShadowEditFiles
            rm -r ~/Library/Group\ Containers/FPY8L862BK.com.cyberlink.powerdirector/Library/Caches/Assets
            rm -r ~/Library/Group\ Containers/FPY8L862BK.com.cyberlink.powerdirector/Library/Application\ Support/
            rm -r ~/Library/Group\ Containers/FPY8L862BK.com.cyberlink.powerdirector/Library/Caches/MyProjectFiles.json
            rm -r ~/Pictures/CyberLink/InAppDownload\ Templates 
            ''')
        return True

    @step("[Initial] clear cache")
    def clear_cache(self):
        self.driver.shell(r'''
            defaults delete com.cyberlink.powerdirector
            defaults delete com.cyberlink.powerdirector.aspectRatio
            defaults delete com.cyberlink.powerdirector.mergeMediaLibrary
            defaults delete com.cyberlink.powerdirector.preferences
            defaults delete com.cyberlink.powerdirector.produceProfile
            defaults delete com.cyberlink.powerdirector.SubtitleTextSetting
            rm ~/Library/Application\ Support/com.cyberlink.powerdirector/UserConfigure/Profile.json
            rm -r ~/Library/Caches/com.cyberlink.powerdirector
            rm -r ~/Documents/Cyberlink/
            rm -r ~/Library/Application\ Support/com.cyberlink.powerdirector/cloudDB
            rm -r ~/Library/Application\ Support/com.cyberlink.powerdirector/UserConfigure/SimpleContainer
            rm ~/Library/Application\ Support/com.cyberlink.powerdirector/UserConfigure/Precut.json
            rm -r ~/Downloads/.Cyberlink/.CBE
            rm -r ~/Downloads/.Cyberlink/.EvoParser
            rm ~/Library/Application\ Support/com.cyberlink.powerdirector/UserConfigure/ClipMarkerCache/ClipMarker_0.json
            rm -r ~/Library/Application\ Support/com.cyberlink.powerdirector/Assets
            rm -r ~/Library/Application\ Support/com.cyberlink.powerdirector/UserConfigure
            rm -r ~/Library/Application\ Support/com.cyberlink.powerdirector/MyPinPs
            rm -r ~/Library/Application\ Support/com.cyberlink.powerdirector/MyCollage
            rm -r ~/Library/Application\ Support/com.cyberlink.powerdirector/MyParticles
            rm -r ~/Library/Application\ Support/com.cyberlink.powerdirector/MyTitles
            rm -r ~/Library/Application\ Support/com.cyberlink.powerdirector/ColorDirector\ presets
            rm -r ~/Library/Application\ Support/com.cyberlink.powerdirector/DZAPICache
            rm -r ~/Library/Application\ Support/com.cyberlink.powerdirector/cloudDB
            rm -r ~/Library/Group\ Containers/FPY8L862BK.com.cyberlink.powerdirector/Document/CyberLink
            rm -r ~/LocalAppData/CyberLink
            rm -r ~/Movies/CyberLink
            rm -r ~/Movies/PowerDirector
            rm -r ~/Movies/.Cache\ Files\ 01
            rm -r ~/Movies/.Cache\ Files\ 02
            rm -r ~/Music/Cyberlink/Downloaded\ Audio/.Cache\ Files\ 01
            rm -r ~/Library/Group\ Containers/rddf.com.cyberlink.powerdirector/Library/Caches/Preview\ Cache\ Files
            rm -r ~/Library/Group\ Containers/rddf.com.cyberlink.powerdirector/Library/Caches/ShadowEditFiles
            rm -r ~/Library/Group\ Containers/FPY8L862BK.com.cyberlink.powerdirector/Library/Caches/Preview\ Cache\ Files
            rm -r ~/Library/Group\ Containers/FPY8L862BK.com.cyberlink.powerdirector/Library/Caches/ShadowEditFiles
            rm -r ~/Library/Group\ Containers/FPY8L862BK.com.cyberlink.powerdirector/Library/Caches/Assets
            rm -r ~/Library/Group\ Containers/FPY8L862BK.com.cyberlink.powerdirector/Library/Application\ Support/
            rm -r ~/Library/Group\ Containers/FPY8L862BK.com.cyberlink.powerdirector/Library/Caches/MyProjectFiles.json
            rm -r ~/Pictures/CyberLink/InAppDownload\ Templates 
            ''')
        return True

    def wait_for_image_changes(self, img_before, locator=None, timeout=5,
                               similarity=0.95):  # locator = None if compare screenshot image
        try:
            is_complete = 0
            start_time = time.time()
            while time.time() - start_time < timeout:
                if locator:
                    img_after = self.snapshot(locator)
                else:
                    img_after = self.screenshot()
                if not img_after:
                    time.sleep(1)
                    continue
                result_verify = self.compare(img_before, img_after, similarity)
                if result_verify:
                    time.sleep(1)
                    continue
                is_complete = 1
                break
            if is_complete == 0:
                logger(f'Fail to verify image change')
                raise Exception(f'Fail to verify image change')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
    
    @step("[Action][Base_page] Drag Mouse")
    def drag_mouse(self, start_pos, dest_pos):
        return self.driver.mouse.drag(start_pos, dest_pos)

    def get_mouse_pos(self):
        x, y = self.driver.mouse.position()
        return (int(x), int(y))

    def is_pdr_hide(self):
        try:
            return self.get_top().AXHidden
        except:
            return None

    def is_pdr_exist(self):
        try:
            self.driver.activate()
            return True
        except:
            return False

    def hide_pdr_by_hotkey(self, timeout=5):
        self.tap_HidePDR_hotkey()
        timer = time.time()
        while time.time() - timer < timeout:
            if self.is_pdr_hide(): return True
        else:
            return False

    def is_full_screen(self, timeout=3, _is_full=True):
        timer = time.time()
        while time.time() - timer < timeout:
            if self.find(L.base.main_window).AXFullScreen == _is_full:
                return True
        else:
            return self.find(L.base.main_window).AXFullScreen == _is_full

    def is_not_full_screen(self, timeout=3):
        return self.is_full_screen(timeout=timeout, _is_full=False)

    def is_minimize(self, timeout=3, _is_mini=True):
        timer = time.time()
        while time.time() - timer < timeout:
            if self.find(L.base.main_window).AXMinimized == _is_mini:
                return True
        else:
            return self.find(L.base.main_window).AXMinimized == _is_mini

    def is_not_minimize(self, timeout=3):
        return self.is_minimize(timeout=timeout, _is_mini=False)

    def tap_cut_and_leave_gap_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.shift, "x"): pass

    def tap_cut_and_fill_gap_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.ctrl, self.keyboard.key.alt, "x"): pass

    def tap_cut_fill_gap_and_move_all_clips_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.alt, "x"): pass

    def tap_remove_and_leave_gap_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.shift, self.keyboard.key.backspace): pass

    def tap_remove_and_fill_gap_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.ctrl, self.keyboard.key.backspace): pass

    def tap_remove_fill_gap_and_move_all_clips_hotkey(self):
        with self.keyboard.pressed(self.keyboard.key.alt, self.keyboard.key.backspace): pass

    def check_chrome_page(self):
        try:
            chrome = self.driver.get_top("com.google.Chrome")
            # logger(chrome)
            for x in range(10):
                time.sleep(OPERATION_DELAY)
                if x == 9:
                    logger('Timeout to get Chrome title')
                    raise Exception

                title = chrome.windows()[0].AXTitle
                if title == 'Untitled - Google Chrome':
                    continue
                elif title:
                    logger(title)
                    break
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return title

    def close_chrome_page(self):
        try:
            logger('enter close_chrome_page')
            #self.driver.get_top("com.google.Chrome").windows()[0].findAllR(AXSubrole="AXCloseButton", AXRole="AXButton")[-1].press()
            self.driver.get_top("com.google.Chrome").windows()[0].findAllR(AXDescription="Close", AXRole="AXButton")[-1].press()
            time.sleep(OPERATION_DELAY * 2)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def get_project_path(self, relative_path="/"):
        base_path = os.path.abspath(os.path.dirname(__file__) + "/..")
        final_path = os.path.abspath(f"{base_path}/{relative_path}")
        return final_path

    def _set_timecode(self, timecode, locator=None):
        locator = locator or L.base.timecode
        elem = self.exist(locator)
        w, h = elem.AXSize
        x, y = elem.AXPosition

        pos_click = tuple(map(int, (x + w * 0.1, y + h * 0.5)))
        self.mouse.click(*pos_click)
        time.sleep(1)
        self.keyboard.send(timecode.replace("_", ""))
        self.keyboard.enter()
        return True

    def adjust_duration_settings(self, timecode, close_win=True, locator=None):
        try:
            self.activate()
            self._set_timecode(timecode, locator)
            if close_win: self.exist_click(L.base.button_ok)
            return True
        except:
            return False

    def color_picker_switch_category_to_RGB(self):
        try:
            # click (Color Slider) button
            el_color_sliders = self.exist(L.base.colors.btn_color_sliders)
            self.el_click(el_color_sliders)
            time.sleep(OPERATION_DELAY)
            # Switch Category to RGB Slider
            category = self.exist(L.base.colors.category)
            category._activate()
            if category.AXValue != 'RGB Sliders':
                self.mouse.click(*category.center)
                items = self.exist(L.base.colors.category_items)
                is_done = 0
                for item in items:
                    if item.AXTitle == 'RGB Sliders':
                        self.mouse.click(*item.center)
                        is_done = 1
                        break
                if not is_done:
                    logger('Fail to select RGB Sliders from drop-down list')
                    return False
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step("[Action][Base Page] Click [CEIP] dialog")
    def click_CEIP_dialog(self):
        # if find CEIP dialog
        if self.is_exist(L.base.ceip_dialog, timeout=20):
            # click (No, thank you) checkbox
            self.click(L.base.radio_button_no_on_ceip)
            time.sleep(OPERATION_DELAY * 0.5)

            # click [Close] button
            self.exist_click(L.base.button_close_on_ceip)
            time.sleep(OPERATION_DELAY)

    # For Launcher related pages ------>
    @step("[Action][Base_page] click 'New Project' button on Launcher")
    def click_new_project_on_launcher(self):
        # if find launcher
        if self.is_exist(L.base.launcher_window.main):
            if self.click(L.base.launcher_window.btn_new_project):
                return True
        return False

    def check_WOW_content_OK_on_launcher(self):
        # Cannot find launcher
        if not self.is_exist(L.base.launcher_window.main):
            logger('Cannot find launcher')
            return False

        # Check WOW content is exist?
        if not self.is_exist(L.base.launcher_window.image_WOW):
            logger('Cannot find WOW area')
            return False

        return self.Check_PreviewWindow_is_different(area=L.base.launcher_window.image_WOW, sec=3)

    @step("[Verify] Get the value of 'Show launcher after closing program' checkbox")
    def get_value_in_checkbox_show_launcher(self):
        for _ in range(5):
            if self.is_exist(L.base.launcher_window.chx_show_launcher):
                return self.exist(L.base.launcher_window.chx_show_launcher).AXValue
            time.sleep(OPERATION_DELAY)
        logger('Cannot find checkbox of (Show launcher after closing program)')
        return None # prevent value ==0 would be the same as False, so return None in this condition


    def hover_first_recently_project(self):
        if not self.is_exist(L.base.launcher_window.img_recently_icon):
            logger('Cannot find 1st recently project')
            return False

        # Hover 1st recently project icon
        elem = self.exist(L.base.launcher_window.img_recently_icon)
        x, y = elem.AXPosition
        w, h = elem.AXSize
        self.mouse.move(*elem.center)
        time.sleep(OPERATION_DELAY * 2)
        return x, y, w, h

    @step("[Action][Base_page] Delte 1st recently project")
    def delete_first_recently_project(self):
        # in Launcher
        x, y, w, h = self.hover_first_recently_project()

        # (...) object
        pos_click = tuple(map(int, (x + w * 0.9, y + h * 0.1)))
        self.mouse.click(*pos_click)
        time.sleep(OPERATION_DELAY * 2)

        # click [Remove] menu
        self.select_right_click_menu('Remove')
        time.sleep(OPERATION_DELAY * 2)

        return True

    @step("[Action][Base_page] Apply [Sample Clip] on [AI Module Import dialog] on Launcher")
    def apply_sample_clip_when_open_AI_import_dialog(self):
        if self.is_not_exist(L.base.launcher_window.txt_try_sample_clip):
            logger('CANNOT find txt_try_sample_clip locator')
            return False
        # find String "Try with sample clip"
        target_string = self.exist(L.base.launcher_window.txt_try_sample_clip)

        x, y = target_string.AXPosition
        w, h = target_string.AXSize
        new_x = x + (0.5 * w)
        new_y = y - (3 * h)
        logger(new_x)
        logger(new_y)
        self.mouse.move(new_x, new_y)
        time.sleep(1)
        self.mouse.click()
        time.sleep(3)

        return True

    @step("[Action][Base_page] Click [Import] button on [AI Module Import dialog] on Launcher and import media")
    def click_to_import_media_when_open_AI_import_dialog(self, full_path):
        if self.is_not_exist(L.base.launcher_window.import_dialog):
            logger('CANNOT find txt_try_sample_clip locator')
            return False
        # find AI module "Import dialog"
        targe_obj = self.exist(L.base.launcher_window.import_dialog)
        self.mouse.move(*targe_obj.center)
        time.sleep(1)
        self.mouse.click()
        time.sleep(2)

        self.select_file(full_path)
        time.sleep(1)
        return True

    # For Launcher related pages <------

    # handle sign in process
    @step(f"[Action] Sign in to PDR")
    def handle_sign_in(self, account, pw):
        # Click User icon
        self.click(L.main.btn_user_sign_in_icon)
        time.sleep(10)

        # Input E-mail field
        e_mail_field = self.exist({'AXRoleDescription': 'text field', 'AXRole': 'AXTextField'})
        self.mouse.click(*e_mail_field.center)
        email_string = account
        self.keyboard.send(email_string)
        time.sleep(1)

        # Input PW field
        password_field = self.exist({'AXRoleDescription': 'secure text field', 'AXRole': 'AXTextField'})
        self.mouse.click(*password_field.center)
        password_string = pw
        self.keyboard.send(password_string)

        # Click [Sign in]
        btn_sign_in = self.exist({'AXTitle': 'Sign in', 'AXRole': 'AXLink'})
        self.mouse.click(*btn_sign_in.center)
        time.sleep(2)

        return True

    @step("[Action][Base_page] Click [Try for Free] button")
    def click_btn_try_for_free(self, option_dont_show_again=0):
        # Step1: Check to find premium icon
        if not self.is_exist(L.base.try_for_free_dialog.icon_premium):
            logger('Verify NG, cannot find premium icon')
            raise Exception('Verify NG, cannot find premium icon')
        # Click the checkbox of (don't show again) to fit custom setting
        current_value = self.exist(L.base.try_for_free_dialog.chx_do_not_show_again).AXValue
        time.sleep(OPERATION_DELAY)
        if current_value != option_dont_show_again:
            self.click(L.base.try_for_free_dialog.chx_do_not_show_again)
            time.sleep(OPERATION_DELAY * 2)

        # Click [Try for Free]
        self.click(L.base.try_for_free_dialog.btn_try_for_free)
        return True

    @step("[Action][Base_page] Click [Try Once] button")
    def click_btn_try_once(self):
        # Step1: Check to find premium icon
        if not self.is_exist(L.base.try_for_free_dialog.icon_premium):
            logger('Verify NG, cannot find premium icon')
            raise Exception('Verify NG, cannot find premium icon')

        # Click [Try Once]
        self.click(L.base.try_for_free_dialog.btn_try_once)
        return True

def arrow(obj, button="up", times=1, locator=None):
    locator = locator[button.lower() == "up"]
    elem = obj.exist(locator)
    for _ in range(times):
        obj.mouse.click(*elem.center)
        time.sleep(OPERATION_DELAY*0.5)
    return True


class AdjustSet:
    def __init__(self, driver, locators):
        self.driver = driver
        self.locators = locators  # slider, value, arrow_up, arrow_down

    @step("[Action][Base_page][AdjustSet] Adjust slider value")
    def adjust_slider(self, value):
        self.driver.exist(self.locators[0]).AXValue = value
        return True
    @step("[Action][Base_page][AdjustSet] Set value")
    def set_value(self, value):
        target = self.driver.exist(self.locators[1])
        self.driver.mouse.click(*target.center)
        target.AXValue = str(value)
        self.driver.keyboard.enter()
        return True

    @step("[Action][Base_page][AdjustSet] Get value")
    def get_value(self):
        return self.driver.exist(self.locators[1]).AXValue

    def click_up(self, times=1):
        return arrow(self.driver, button="up", times=times, locator=self.locators[3:1:-1])

    def click_down(self, times=1):
        return arrow(self.driver, button="down", times=times, locator=self.locators[3:1:-1])

    def click_arrow(self, opt="up", times=1):
        index = opt if isinstance(opt, int) else opt.lower() == "down"
        option = ["up", "down"][index]
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


class EaseSet(AdjustSet):
    def __init__(self, *args):
        super().__init__(*args)

    @step("[Action][Base_page][EaseSet] Enable/ Disable ease checkbox")
    def set_checkbox(self, value=1):
        target = self.driver.exist(self.locators[4])
        int(target.AXValue) ^ value and target.press()
        return True
    
    @step("[Action][Base_page][EaseSet] Get status of ease checkbox")
    def get_checkbox(self):
        target = self.driver.exist(self.locators[4])
        return bool(target.AXValue)


class KeyframeSet:
    def __init__(self, driver, locators):
        self.driver = driver
        self.locators = locators

    def _click_keyframe(self, locator):
        el = self.driver.find(locator)
        if el.AXEnabled:
            el.press()
            return True
        else:
            return False

    def click_reset(self):
        ret = self._click_keyframe(self.locators[0])
        if ret: self.driver.exist_click(self.locators[4], timeout=3)  # reset confirmation
        return ret

    @step("[Action][Base_page][KeyframeSet] Click previous keyframe")
    def click_previous(self): 
        return self._click_keyframe(self.locators[1])

    def click_add_remove(self):
        return self._click_keyframe(self.locators[2])
    
    @step("[Action][Base_page][KeyframeSet] Click next keyframe")
    def click_next(self):
        return self._click_keyframe(self.locators[3])


class KEComboSet(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(args[0], **kwargs)
        self.keyframe = KeyframeSet(self, args[1].group_keyframe.group)
        self.ease_in = EaseSet(self, args[1].group_ease.group_in)
        self.ease_out = EaseSet(self, args[1].group_ease.group_out)

    def scroll_to_screen(self):
        scroll_bar = self.find(L.mask_designer.tab_scroll)
        parent = self.find(L.mask_designer.property_frame)
        frame = self.find(L.mask_designer.tab_content)
        el_down = self.find(self.arg.group_ease.group_out[0][0])  # frame of ease_in & ease out
        el_top = self.find(self.arg.previous_keyframe[0])  # frame of keyframe

        bottom = lambda x: int(x.AXPosition[1] + x.AXSize[1])
        scrollable_len = parent.AXSize[1] - frame.AXSize[1]
        percent = None
        if bottom(el_down) - bottom(frame) > 0:
            percent = 1 - ((bottom(parent) - bottom(el_down)) / scrollable_len)
            logger(f"screen down. {percent}")
        elif frame.AXPosition[1] - el_top.AXPosition[1] > 0:
            percent = (el_top.AXPosition[1] + frame.AXSize[1]) / scrollable_len
            logger(f"screen up. {percent}")
        if percent: scroll_bar.AXValue = percent
        return True


class Backdoor:
    def __init__(self, driver):
        self.driver = driver

    def test(self):
        logger(self.seek_timeline(900))
        logger(self.get_movie_duration())
        logger(self.select_track_by_type(1, 1))
        logger(self.is_track_selectable_by_type(1, 1))
        logger(self.get_track_count_by_type(1))
        logger(self.select_clip_by_object_Type(1, 1, 0, 0))
        logger(self.get_track_clips_count_by_object_type(1, 1, 0))

    def seek_timeline(self, seekTo):
        return self.driver.backdoor("TimelineSeek")

    def get_movie_duration(self):
        return self.driver.backdoor("GetMovieDuration", True)

    def select_track_by_type(self, trackType, trackIdx):
        return self.driver.backdoor("SelectTrackByType")

    def is_track_selectable_by_type(self, trackType, trackIdx):
        ret = self.driver.backdoor("QueryIsTrackSelectableByType", True)
        return [False, True, None][ret]

    def get_track_count_by_type(self, trackType):
        return self.driver.backdoor("GetTrackCountByType", True)

    def select_clip_by_object_Type(self, objectType, trackType, objectIdx, trackIdx):
        return self.driver.backdoor("SelectClipByObjectType")

    def get_track_clips_count_by_object_type(self, objectType, trackType, trackIdx):
        return self.driver.backdoor("GetTrackClipsCountByObjectType", True)

    def move_track(self, dstTrackType, srcTrackType, dstTrackIdx, srcTrackIdx):
        return self.driver.backdoor("MoveTrack")

    def add_effect_to_video_track(self, objectIdx, videoTrackIdx):
        return self.driver.backdoor("AddEffectToVideoTrack")

    def get_track_clips_count_by_link_group_type(self, stateType, trackType, trackIdx):
        return self.driver.backdoor("GetTrackClipsCountByLinkGroupType", True)

    def select_clip_by_link_group_type(self, stateType, trackType, objectIdx, trackIdx):
        return self.driver.backdoor("SelectClipByLinkGroupType")

    def move_selected_clips(self, moveTo):
        return self.driver.backdoor("MoveSelectedClips")

    def set_range_select_time(self, left, right):
        return self.driver.backdoor("SetRangeSelectTime")

    def get_trans_count_by_type(self, transType, videoTrackIdx):
        return self.driver.backdoor("GetTransCountByType", True)

    def select_trans_by_type(self, transType, objectIdx, videoTrackIdx):
        return self.driver.backdoor("SelectTransByType")

    def get_trans_bucket_count_by_type(self, transType, videoTrackIdx):
        return self.driver.backdoor("GetTransBucketCountByType", True)

    def add_trans_by_type(self, transType, bucketIdx, trackType, trackIdx):
        return self.driver.backdoor("AddTransByType")

    def get_trim_bound(self, isTrimRight):
        return self.driver.backdoor("GetTrimBound", True)

    def get_clip_begin_end(self, stateType, transType, objectIdx, trackIdx):
        return self.driver.backdoor("GetClipBeginEnd", True)

    def trim_clip(self, isTrimRight, trimPosition):
        return self.driver.backdoor("TrimClip")

    def unselect_all(self):
        return self.driver.backdoor("UnselectAll")

    def get_signIn_url(self):
        return self.driver.backdoor("GetSignInUrl", True)
