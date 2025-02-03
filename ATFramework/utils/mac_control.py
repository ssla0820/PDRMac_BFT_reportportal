import atomac   # pip3 install git+https://github.com/pyatom/pyatom/
import inspect, time, os
import pynput.mouse
import pynput.keyboard
from AppKit import NSWorkspace  # already in Xcode framework(components), including objc, appkt

# ==================================================================================================================
# Class: MWC
# Description: control mac windows
# Note: n/a
# Author: Terence
# Date: 2019/12/12
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
    TIME_OUT = 15
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
    def __init__(self):
        self.el_type = None
        self.el_text = None

    # =================================================Common functions================================================
    @staticmethod
    def func_name():
        return inspect.stack()[1].frame.f_code.co_name

    # =================================================Mouse functions================================================
    @staticmethod
    def input_keyboard(key):
        """
        perform action, return Boolean
        """
        try:
            MWC.keyboard.press(eval(f'MWC.Key.{key}'))
            time.sleep(0.25)
            MWC.keyboard.release(eval(f'MWC.Key.{key}'))
            return True
        except Exception as e:
            print(f'[{MWC.func_name()}]: Exception. ({e})')
        return False

    # =================================================Mouse functions================================================
    @staticmethod
    def get_mouse_pos():
        """
        return position or False
        """
        try:
            return MWC.mouse.position
        except Exception as e:
            print(f'[{MWC.func_name()}]: Exception. ({e})')
        return False

    @staticmethod
    def move_mouse(destination):
        """
        Do action(return None) or False
        """
        try:
            current_pos = MWC.get_mouse_pos()
            dx = destination[0] - current_pos[0]
            dy = destination[1] - current_pos[1]
            print(f'[{MWC.func_name()}]: Move to ({destination[0]}, {destination[1]})')
            MWC.mouse.move(dx, dy)
        except Exception as e:
            print(f'[{MWC.func_name()}]: Exception. ({e})')
        return False

    # ===============================================Execution functions===============================================
    @classmethod
    def launch_app(cls, app, timeout=TIME_OUT):
        """
        Return True/False
            Check if App is not launched and then execute,
            after that, make sure atomac get top_element & window
        """
        try:
            # check if app opened
            if cls.get_current_wnd(cls.get_top_element(app)) is not False:
                print(f'[{MWC.func_name()}]: APP({app}) had been launched')
                return False
            # execute app
            atomac.launchAppByBundleId(app)
            print(f'[{MWC.func_name()}]: Launching APP({app})...')
            # wait till get element & window (15sec.)
            wait_time = 0
            while wait_time < timeout:
                if not cls.get_current_wnd(cls.get_top_element(app)):
                    print(f'wait... {wait_time}sec.')
                    time.sleep(1)
                    wait_time += 1
                else:
                    print(f'[{MWC.func_name()}]: Done')
                    return True
        except RuntimeError as re:
            print(f'[{MWC.func_name()}]: RuntimeError. ({re})')
        except Exception as e:
            print(f'[{MWC.func_name()}]: Exception. ({e})')
        return False

    @classmethod
    def close_app(cls, app, forcemode=0, app_name=None, timeout=TIME_OUT):
        """
        close success: return True, others: return False
        """
        try:
            # use force kill  (need app_name)
            if forcemode == 1:
                try:
                    pid = os.popen(f'ps -ax | grep {app_name}').readlines()[0].split('??')[0].strip(' ')
                    if type(int(pid)) is not int:
                        raise Exception
                    print(f"Ports(PID): {pid}")
                    os.popen(f"kill {pid}")
                except Exception:
                    pass
            else:
                # use atomac
                atomac.terminateAppByBundleId(app)
            # check if app is closed
            # wait till NOT get element & window
            wait_time = 0
            while wait_time < timeout:
                if cls.get_current_wnd(cls.get_top_element(app)) is False:
                    print(f'[{MWC.func_name()}]: Done')
                    return True
                else:
                    print(f'[{MWC.func_name()}]: wait... {wait_time}sec.')
                    time.sleep(1)
                    wait_time += 1
        except RuntimeError as re:
            print(f'[{MWC.func_name()}]: RuntimeError. ({re})')
        except Exception as e:
            print(f'[{MWC.func_name()}]: Exception. ({e})')
        return False

    @classmethod
    def is_app_exist(cls, app):
        try:
            if cls.get_current_wnd(cls.get_top_element(app)):
                return True
            else:
                return False
        except Exception as e:
            print(f'[{MWC.func_name()}]: Exception. ({e})')
        return False
    # ================================================Get functions===================================================
    @classmethod
    def get_top_element(cls, app):
        """
        return Atomac_element, else False
            Get the top level element for the application with the specified
            bundle ID, such as com.vmware.fusion.
        """
        try:
            # source code: NativeUIElement.getAppRefByBundleId
            top_native_el = atomac.getAppRefByBundleId(app)
            #print(f'[{MWC.func_name()}]: Native_Element({top_native_el})')
            return top_native_el
        except Exception as e:
            print(f'[{MWC.func_name()}]: Exception. ({e})')
        return False

    @staticmethod
    def get_current_wnd(el):
        """
        return Atomac_element, else False
        """
        try:
            cur_win = el.windows()[0]
            print(f'[{MWC.func_name()}]: Current_Wnd({cur_win})')
            return cur_win
        except IndexError as ie:
            print(f'[{MWC.func_name()}]: IndexError. {ie}')
            return False
        except Exception as e:
            print(f'[{MWC.func_name()}]: Exception. {e}')
            return False

    @staticmethod
    def get_child_wnd(el):
        """
        Return a list(Atomac elements), else False
        """
        try:
            result = el.AXChildren
            #print(f'[{MWC.func_name()}]: {result}')
            return result
        except Exception as e:
            print(f'[{MWC.func_name()}]: Exception. {e}')
            return False

    @staticmethod
    def get_axtitile(el):
        """
        Return string, else False
        """
        try:
            # title
            return el.AXTitle
        except:
            try:
                # description
                return el.AXRoleDescription
            except Exception as e:
                print(f'[{MWC.func_name()}]: Exception. {e}')
                return False

    @staticmethod
    def get_axrole(el):
        """
        Return string, else False
        """
        try:
            # title
            return el.AXRole
        except Exception as e:
            print(f'[{MWC.func_name()}]: Exception. {e}')
            return False

    @staticmethod
    def get_axvalue(el):
        """
        Return string, else False
        """
        try:
            # title
            return el.AXValue
        except Exception as e:
            print(f'[{MWC.func_name()}]: Exception. {e}')
            return False

    @staticmethod
    def get_axtype(el):
        """
        Return string, else False
        """
        try:
            # type
            return el.AXRoleDescription
        except Exception as e:
            print(f'[{MWC.func_name()}]: Exception. {e}')
            return False

    @staticmethod
    def get_axlabel(el):
        """
        Return string, else False
        """
        try:
            # type
            return el.AXDescription
        except Exception as e:
            print(f'[{MWC.func_name()}]: Exception. {e}')
            return False

    @staticmethod
    def get_mid_pos(el):
        """
        return mid_pos else False
        """
        try:
            check_flag = el.getAttributes()
            if 'AXSize' in check_flag and \
                    'AXPosition' in check_flag:
                pass
            else:
                print(f"[{MWC.func_name()}]: Can't trigger AXSize or AXPosition")
                return False
            x, y = el.AXPosition
            dx, dy = el.AXSize
            mid_pos = (int(x + dx / 2), int(y + dy / 2))
            return mid_pos
        except Exception as e:
            print(f'[{MWC.func_name()}]: Exception. {e}')
            return False

    # ===============================================APPKit functions===============================================
    @staticmethod
    def get_top_wnd_name():
        """
        call NSWorkspace to get top name
        """
        try:
            activeAppName = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
            return activeAppName
        except Exception as e:
            print(f'[{MWC.func_name()}]: Exception. {e}')
            return False

    # ================================================Find functions===================================================
    @staticmethod
    def find_top_el_byname(name):
        """
        return Atomac_element else False
            only can find 'top native element'
        """
        try:
            return atomac.getAppRefByLocalizedName(name)
        except ValueError as ve:
            print(f'[{MWC.func_name()}]: ValueError. {ve}')
            return False
        except Exception as e:
            print(f'[{MWC.func_name()}]: Exception. {e}')
            return False

    # ================================================wait functions=================================================
    @staticmethod
    def wait_to_appear(name, timeout=15):
        """
        Return Boolean
        """
        try:
            for x in range(timeout):
                if MWC.get_top_wnd_name() == name:
                    return True
                else:
                    if x == (timeout - 1):
                        return False
                    else:
                        print(f'[{MWC.func_name()}]: wait...{x + 1}sec.')
                        time.sleep(1)
        except Exception as e:
            print(f'[{MWC.func_name()}]: Exception. {e}')
            return False
    # ================================================Search functions=================================================

    @classmethod
    def search_child_el_bytitle(cls, el, title):
        """
        Return a element or list, including matching title atomac_elements
        """
        try:
            check_flag = MWC.get_child_wnd(el)
            if check_flag is False:
                print(f'[{MWC.func_name()}]: fail to get')
                return False
            result = []
            for x in range(len(check_flag)):
                if MWC.get_axtitile(check_flag[x]) == title:
                    #print(check_flag[x])
                    result.append(check_flag[x])
            # Return element if only 1 else return a list
            if len(result) != 0:
                if len(result) == 1:
                    result = result[0]
                print(f'[{MWC.func_name()}]: (Keyword_title: {title}) found result is {result}')
                return result
        except Exception as e:
            print(f'[{MWC.func_name()}]: Exception. {e}')
            return False
        print(f"[{MWC.func_name()}]: Search (target_title: {title}) fail")
        return False

    @classmethod
    def search_child_el_byrole(cls, el, axrole):
        """
        Return a element or list, including matching axrole atomac_elements
        """
        try:
            check_flag = MWC.get_child_wnd(el)
            if check_flag is False:
                print(f'[{MWC.func_name()}]: fail to get')
                return False
            result = []
            for x in range(len(check_flag)):
                if MWC.get_axrole(check_flag[x]) == axrole:
                    #print(check_flag[x])
                    result.append(check_flag[x])
            # Return element if only 1 else return a list
            if len(result) != 0:
                if len(result) == 1:
                    result = result[0]
                print(f'[{MWC.func_name()}]: (Keyword_axrole: {axrole}) found result is {result}')
                return result
        except Exception as e:
            print(f'[{MWC.func_name()}]: Exception. {e}')
            return False
        print(f"[{MWC.func_name()}]: Search (target_axrole: {axrole}) fail")
        return False

    @classmethod
    def search_child_el_bytype(cls, el, axtype):
        """
        Return a element or list, including matching axrole atomac_elements
        """
        try:
            check_flag = MWC.get_child_wnd(el)
            if check_flag is False:
                print(f'[{MWC.func_name()}]: fail to get')
                return False
            result = []
            for x in range(len(check_flag)):
                if MWC.get_axtype(check_flag[x]) == axtype:
                    # print(check_flag[x])
                    result.append(check_flag[x])
            # Return element if only 1 else return a list
            if len(result) != 0:
                if len(result) == 1:
                    result = result[0]
                print(f'[{MWC.func_name()}]: Keyword_axtype: {axtype}) found result is {result}')
                return result
        except Exception as e:
            print(f'[{MWC.func_name()}]: Exception. {e}')
            return False
        print(f"[{MWC.func_name()}]: Search (target_axtype: {axtype}) fail")
        return False

    @classmethod
    def search_child_el_bylabel(cls, el, axlabel):
        """
        Return a element or list, including matching axrole atomac_elements
        """
        try:
            check_flag = MWC.get_child_wnd(el)
            if check_flag is False:
                print(f'[{MWC.func_name()}]: fail to get')
                return False
            result = []
            for x in range(len(check_flag)):
                if MWC.get_axlabel(check_flag[x]) == axlabel:
                    # print(check_flag[x])
                    result.append(check_flag[x])
            # Return element if only 1 else return a list
            if len(result) != 0:
                if len(result) == 1:
                    result = result[0]
                print(f'[{MWC.func_name()}]: Keyword_axlabel: {axlabel}) found result is {result}')
                return result
        except Exception as e:
            print(f'[{MWC.func_name()}]: Exception. {e}')
            return False
        print(f"[{MWC.func_name()}]: Search (target_axlabel: {axlabel}) fail")
        return False
    # ================================================Control functions=================================================
    """
    Only describe, would not call from WMC
    """
    def getAttributes(self):
        """
        call module function, return None
            for debug
        """
        return self.getAttributes()

    def Press(self):
        """
        call module function, return None
        """
        # AXClasss.py 's bug , it would get exception but action is executed
        return self.Press()

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
        return self.activate()