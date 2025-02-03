import sys, os, time, inspect, math
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from ATFramework.drivers.base_driver import BaseDriver
from ATFramework.utils.log import logger, qa_log
import subprocess
import signal   # in order to limited the installation time
# from . import xcuitest_driver_ipad 


# =====if having top-folder includes the project=====
# sys.path.insert(0, os.path.join(os.path.dirname(os.getcwd()), os.pardir) + r'/configs')
# sys.path.insert(0, os.path.dirname(os.getcwd()) + r'/drivers')
# sys.path.insert(0, os.path.dirname(os.getcwd()) + r'/configs')
# sys.path.insert(0, os.path.dirname(os.getcwd()) + r'/pages')
# import app_config as AppConfig
# import driver_config as DriverConfig
# from base_driver import BaseDriver


# temp log function
'''
class LogTemp():
    def logger(self, content):
        print(content)

log = LogTemp()
'''

# setup time parameters
DEFAULT_TIMEOUT = 5
DEFAULT_POLL_TIME = 0.1
#DEVICE = DriverConfig.ios_device_iphone8plus
#DEVICE = DriverConfig.ios_device_iphone6
#DEVICE = DriverConfig.ios_device_iphone11plus
#DEVICE = DriverConfig.ios_device_iphoneXR


class Borg:
    # The borg design pattern is to share state
    # Src: http://code.activestate.com/recipes/66531/
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state

    def is_first_time(self):
        # Has the child class been invoked before?
        result_flag = False
        if len(self.__dict__) == 0:
            result_flag = True

        return result_flag


class AppiumXCUITestDriver(Borg, BaseDriver):
    def __init__(self, DriverConfig, AppConfig, server="local", desired_caps=None):
        if server == "local": server = "localhost" # for old script compatible
        # Constructor
        Borg.__init__(self)
        if self.is_first_time():
            self.DriverConfig = DriverConfig
            # Do these actions if this the first time this class is initialized
            pass

        # determine if app is installed,
        # if yes, initial the driver and set app as main session
        # if not, initial the driver with iOS-native app as main session
        funcname = inspect.currentframe().f_code.co_name
        try:
            if not desired_caps: desired_caps = {} 
            desired_caps.update(self.DriverConfig) if type(self.DriverConfig) == dict else logger(
                'Driver Capability is invalid.(Not dict)'
            )
            # TODO: need to set parameter for cap
            desired_caps.update(AppConfig) if type(
                AppConfig) == dict else logger(
                'App Capability is invalid.(Not dict)'
            )
            # TODO: need to set parameter for cap
            self.driver = webdriver.Remote(f"http://{server}:4723/wd/hub", desired_caps)
            self.driver.implicitly_wait(DEFAULT_TIMEOUT)
            logger('driver has been created (App already installed)\n')
        except:
            try:
                logger('initial driver fail')
                logger('create iOS native-app as master driver, please install app to get driver')
                desired_caps = {}
                desired_caps.update(self.DriverConfig) if type(self.DriverConfig) == dict else logger(
                    'Capability is invalid.(Not dict)'
                )
                # TODO: need to set parameter for cap
                desired_caps.update(AppConfig.safari_cap) if type(
                    AppConfig.safari_cap) == dict else logger(
                    'Capability is invalid.(Not dict)'
                )
                # TODO: need to set parameter for cap
                self.driver = webdriver.Remote(f"http://{server}:4723/wd/hub", desired_caps)
                self.driver.implicitly_wait(DEFAULT_TIMEOUT)
                # set safari as background
                self.driver.background_app(-1)
                # close safari
                # self.driver.close_app()   # do not use bcz master session would be closed
                logger('driver(Safari) has been created\n')

            except AssertionError:
                logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

            except EOFError as error:
                logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

            except Exception as exception:
                logger(exception)
        if not ("_implicitly_wait" in dir(self.driver)):
            self.driver._implicitly_wait = self.driver.implicitly_wait
            self.driver.implicitly_wait = self.implicitly_wait 
        self.driver.implicitly_wait(5)
        self.ta = TouchAction(self.driver)
# ***initial related functions***
    # ==================================================================================================================
    # Function: install_app
    # Description: install app
    # Parameters: path, package_name
    # Return: True/False
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def install_app(self, path, package_name):
        funcname = inspect.currentframe().f_code.co_name
        try:
            # check if app had been installed or not
            ''' (skip this for iPDR update cases)
            if self.driver.is_app_installed(package_name) == True:
                logger('App had been installed already')
                return False
            '''

            # set setting as background
            self.driver.background_app(-1)

            # check if *.ipa/*.app path existed or not
            # assert os.path.exists(path)  # disable for grid machanism
            start_time = int(time.time())
            logger('[{0}][{1}]: installing...'.format(__name__, funcname))
            try:
                self.driver.install_app(path, timeout=180000, allowTestPackages=True)   # 180sec.
            except Exception as e:
                # workarround for setup timeout (due to installation process is too long, and time out only surpport Android ver.)
                logger(f'takes long time to install. Workaround to continue installation {e}')
                time.sleep(10)
            elapsed_time = int(time.time()) - start_time
            logger('Takes {0}sec. to complete the installation'.format(elapsed_time))
            #time.sleep(DEFAULT_TIMEOUT)
            return self.driver.is_app_installed(package_name)

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('exception:', exception)

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False


    # ==================================================================================================================
    # Function: trust_app
    # Description: trust app(iOS, app management)
    # Parameters: n/a
    # Return: True/False
    # Note: Use HARDCORE
    # Author: Terence
    # ==================================================================================================================
    def trust_app(self):
        funcname = inspect.currentframe().f_code.co_name
        try:
            # create 'iOS-native app-settings" as master driver and start to trust our app
            desired_caps = {}
            desired_caps.update(trustapp_cap) if type(trustapp_cap) == dict else logger(
                'Capability is invalid.(Not dict)'
            )
            self.driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
            self.driver.implicitly_wait(DEFAULT_TIMEOUT)
            logger('driver has been created')

            # go setting to press trust  , HARDCORE to setup the "trust" flow
            # click general
            self.driver.execute_script("mobile: scroll", {"direction": "down"})
            self.driver.find_element_by_name('General').click()

            # click Device Management
            self.driver.execute_script("mobile: scroll", {"direction": "down"})
            self.driver.find_element_by_name('Device Management').click()

            # select 'CYBERLINK CORP.'
            self.driver.find_element_by_name('CYBERLINK CORP.').click()

            # click trust ''
            self.driver.find_element_by_name('Trust “CYBERLINK CORP.”').click()

            time.sleep(2)

            # press [Trust]
            self.driver.find_element_by_xpath('//*[@name="Trust"]').click()

            # set setting as background
            self.driver.background_app(-1)

            # close setting
            self.driver.close_app()
            # **** above is HARDCORE ****
            return True

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False


    # ==================================================================================================================
    # Function: stop_driver
    # Description: stop_driver
    # Parameters: n/a
    # Return: True/False
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def stop_driver(self):
        funcname = inspect.currentframe().f_code.co_name
        try:
            self.driver.quit()
            return True

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False


# *******app control*********
    # ==================================================================================================================
    # Function: activate_app
    # Description: active app
    # Parameters: package_name
    # Return: True/False
    # Note: Current the target app status. (Clients wrap the response properly)
    #       0: The current application state cannot be determined/is unknown
    #       1: The application is not running
    #       2: The application is running in the background and is suspended
    #       3: The application is running in the background and is not suspended
    #       4: The application is running in the foreground
    # Author: Terence
    # ==================================================================================================================
    def activate_app(self, package_name):
        funcname = inspect.currentframe().f_code.co_name
        try:
            self.driver.activate_app(package_name)
            result = self.driver.query_app_state(package_name)
            if result == 0:
                logger("App isn't installed")
                return False
            elif result > 1:
                logger('App status:(code={0})'.format(result))
                return True

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False


    # ==================================================================================================================
    # Function: start_app
    # Description: start_app
    # Parameters: package_name
    # Return: True/False
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def start_app(self, package_name):
        funcname = inspect.currentframe().f_code.co_name
        try:
            self.driver.launch_app()
            result = self.driver.query_app_state(package_name)
            if result == 0:
                logger("App isn't installed")
                return False
            elif result > 1:
                logger('App status:(return code={0})'.format(result))
                return True

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: remove_app
    # Description: remove_app
    # Parameters: package_name
    # Return: True/False
    # Note: iOS XCUITest only, need to STOP DRIVER before using!!
    # Author: Terence
    # ==================================================================================================================
    def remove_app(self, package_name):
        funcname = inspect.currentframe().f_code.co_name
        try:
            # check if app had been installed or not
            if self.driver.is_app_installed(package_name) is False:
                logger("App isn't installed already")
                return False

            # background app
            self.background_app()

            # make sure driver is removed
            assert self.stop_driver()

            # create 'iOS-native app-settings" as master driver and start to trust our app
            desired_caps = {}
            desired_caps.update(self.DriverConfig) if type(
                self.DriverConfig) == dict else logger(
                'Capability is invalid.(Not dict)'
            )
            # TODO: need to set parameter for cap
            desired_caps.update(AppConfig.safari_cap) if type(
                AppConfig.safari_cap) == dict else logger(
                'Capability is invalid.(Not dict)'
            )

            self.driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
            self.driver.implicitly_wait(DEFAULT_TIMEOUT)
            logger('driver(Safari) has been created')

            # start to remove app
            # self.driver.execute_script('mobile: removeApp', {'bundleId': '{}'.format(package)})
            start_time = int(time.time())
            self.driver.remove_app(package_name)
            elapsed_time = int(time.time()) - start_time
            logger('Takes {0}sec. to complete the uninstallation'.format(elapsed_time))

            # need to check if app is removed after a period time
            self.implicit_wait(10)
            if self.driver.is_app_installed(package_name) == 0:
                return True
            else:
                logger('[{0}][{1}]: App status is (code={2}).'.format(__name__, funcname, self.driver.query_app_state(package)))

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: background_app
    # Description: background_app
    # Parameters: duration
    # Return: True/False
    # Note: for master session(driver)
    # Author: Terence
    # ==================================================================================================================
    def background_app(self, duration=-1):
        funcname = inspect.currentframe().f_code.co_name
        try:
            self.driver.background_app(duration)
            return True

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: reset_app
    # Description: reset_app
    # Parameters: package
    # Return: True/False
    # Note: reset for master session(driver)
    # Author: Terence
    # ==================================================================================================================
    def reset_app(self, package=None):
        funcname = inspect.currentframe().f_code.co_name
        try:
            self.driver.reset()
            return True

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

# ****common control ******
    # ==================================================================================================================
    # Function: implicit_wait
    # Description: implicit_wait
    # Parameters: time
    # Return: True/False
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def implicit_wait(self, time):
        funcname = inspect.currentframe().f_code.co_name
        try:
            # make sure parameter is valid
            assert type(time) == int
            assert int(time) > 0
            # logger('[{0}][{1}]: Start to wait {2}sec.'.format(__name__, funcname, time))
            self.driver.implicitly_wait(time)
            return True

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

# ****status control ******
    # ==================================================================================================================
    # Function: get_orientation
    # Description: get_orientation
    # Parameters: n/a
    # Return: orientation(string)/False
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def get_orientation(self):
        funcname = inspect.currentframe().f_code.co_name
        try:
            orientation = self.driver.orientation()
            # make sure return a string
            assert orientation == str
            return orientation

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: set_orientation
    # Description: set_orientation
    # Parameters: orientation
    # Return: True/False
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def set_orientation(self, orientation):
        funcname = inspect.currentframe().f_code.co_name
        try:
            if orientation.upper() == 'LANDSCAPE':
                self.driver.orientation = "LANDSCAPE"
            elif orientation.upper() == 'PORTRAIT':
                self.driver.orientation = 'PORTRAIT'
            else:
                logger('[{0}]: incorrect parameter'.format(funcname))
                raise EOFError
            return True

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: get_window_size
    # Description: get_window_size
    # Parameters: n/a
    # Return: width & height(with dict.)/False
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def get_window_size(self):
        funcname = inspect.currentframe().f_code.co_name
        try:
            return self.driver.get_window_size()

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: open_notification
    # Description: open_notification
    # Parameters: n/a
    # Return: True/False
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def open_notification(self):
        funcname = inspect.currentframe().f_code.co_name
        # define TA
        TA = TouchAction(self.driver)
        try:
            wnd_w = self.get_window_size()['width']
            wnd_h = self.get_window_size()['height']
            TA.press(None, wnd_w/2, 0).wait(150).move_to(None, wnd_w/2, wnd_h*3/4).release().perform()
            return True

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: get_element_mid_pos
    # Description: get_element_mid_pos
    # Parameters: locator(tuple)
    # Return: el_mid_pos(list)[mid-x, mid-y]/False
    # Note: doesn't use 'rect' bcz rect doesn't support in ios
    # Author: Terence
    # ==================================================================================================================
    def get_element_mid_pos(self, locator):
        funcname = inspect.currentframe().f_code.co_name
        try:
            # assert locator format is correct, ex: (by, path)
            assert isinstance(locator,(tuple, webdriver.WebElement))

            # get element
            element = locator if isinstance(locator,webdriver.WebElement) else self.get_element(locator)

            # get location
            el_x = element.location['x']
            el_y = element.location['y']

            #logger(f'x:{el_x}, y:{el_y}')

            # get size
            el_w = element.size['width']
            el_h = element.size['height']

            #logger(f'w:{el_w}, h:{el_h}')

            el_mid_pos = [int(el_x + el_w/2), int(el_y + el_h/2)]
            return el_mid_pos

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

# ***Element control Functions***
    # ==================================================================================================================
    # Function: swipe_to_element
    # Description: swipe_to_element
    # Parameters: locator(tuple), direction, target_locator(tuple)
    # Return: True/False
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def swipe_to_element(self, locator, direction, target_locator):
        funcname = inspect.currentframe().f_code.co_name
        # define TA
        TA = TouchAction(self.driver)
        # error handling for finding element had been described in get_element
        try:
            # get window resolution
            wnd_size = self.get_window_size()
            assert type(wnd_size) == dict

            # get element
            element = self.get_element(locator)

            # assert locator format is correct, ex: (by, path)
            assert type(locator) == tuple

            # make sure element exists
            if element is None:
                raise EOFError

            # initial/define swipe point  (3/4 length)
            pos_mid = [divmod(wnd_size['width'], 2), divmod(wnd_size['height'], 2)]  # pos_mid is tuple (x,y)
            pos_left = 0
            pos_top = 0
            pos_right = wnd_size['width']
            pos_bottom = wnd_size['height']
            assert type(pos_left) == int
            assert type(pos_top) == int
            assert type(pos_right) == int
            assert type(pos_bottom) == int

            # make sure parameter is valid
            assert type(direction) == str

            # start to swipe element
            # get element mid position
            el_mid_x = self.get_element_mid_pos(locator)[0]
            el_mid_y = self.get_element_mid_pos(locator)[1]

            # define switch lambda
            switch_action = {
                'up': lambda: TA.press(None, el_mid_x, el_mid_y).wait(50).move_to(None, el_mid_x,
                                                                                  pos_top).release().perform(),
                'down': lambda: TA.press(None, el_mid_x, el_mid_y).wait(50).move_to(None, el_mid_x,
                                                                                    pos_bottom).release().perform(),
                'left': lambda: TA.press(None, el_mid_x, el_mid_y).wait(50).move_to(None, pos_left,
                                                                                    el_mid_y).release().perform(),
                'right': lambda: TA.press(None, el_mid_x, el_mid_y).wait(50).move_to(None, pos_right,
                                                                                     el_mid_y).release().perform()
            }
            execute_program = 'switch_action["{0}"]()'.format(direction.lower())
            eval(execute_program)

            if self.wait_until_element_exist(target_locator) is True:
                return True
            else:
                raise EOFError

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: swipe_element
    # Description: swipe_element
    # Parameters: locator(tuple), direction(up/down/left/right, offset=0.55)
    # Return: True/False
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def swipe_element(self, locator, direction, offset=0.55):
        funcname = inspect.currentframe().f_code.co_name
        # define TA
        TA = TouchAction(self.driver)
        # error handling for finding element had been described in get_element
        try:
            # get window resolution
            wnd_size = self.get_window_size()
            assert type(wnd_size) == dict

            # get element
            element = self.get_element(locator)

            # assert locator format is correct, ex: (by, path)
            assert type(locator) == tuple

            # make sure element exists
            if element is None:
                raise EOFError

            # initial/define swipe point  (3/4 length)
            pos_mid = [divmod(wnd_size['width'], 2), divmod(wnd_size['height'], 2)]  # pos_mid is tuple (x,y)
            pos_left = 0
            pos_top = 0
            pos_right = wnd_size['width']
            pos_bottom = wnd_size['height']
            assert type(pos_left) == int
            assert type(pos_top) == int
            assert type(pos_right) == int
            assert type(pos_bottom) == int

            # make sure parameter is valid
            assert type(direction) == str

            # start to swipe element
            # get element mid position
            el_mid_x = self.get_element_mid_pos(element)[0]
            el_mid_y = self.get_element_mid_pos(element)[1]

            # define switch lambda
            switch_action = {
                'up': lambda: TA.press(None, el_mid_x, el_mid_y).wait(50).move_to(None, el_mid_x, pos_top).release().perform(),
                'down': lambda: TA.press(None, el_mid_x, el_mid_y).wait(50).move_to(None, el_mid_x, pos_bottom).release().perform(),
                'left': lambda: TA.press(None, el_mid_x, el_mid_y).wait(50).move_to(None, pos_left, el_mid_y).release().perform(),
                'right': lambda: TA.press(None, el_mid_x, el_mid_y).wait(50).move_to(None, pos_right, el_mid_y).release().perform()
            }
            execute_program = 'switch_action["{0}"]()'.format(direction.lower())
            eval(execute_program)
            return True

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: swipe
    # Description: swipe
    # Parameters: direction(up/down/left/right), locator(tuple)
    # Return: True/False
    # Note: iOS XCUITest only
    # Author: Terence
    # ==================================================================================================================
    def swipe(self, direction, locator=None):
        funcname = inspect.currentframe().f_code.co_name
        # define TA
        TA = TouchAction(self.driver)
        # error handling for finding element had been described in get_element
        try:
            # get window resolution
            wnd_size = self.get_window_size()
            assert type(wnd_size) == dict

            # initial/define swipe point  (3/4 length)
            pos_mid = [divmod(wnd_size['width'], 2), divmod(wnd_size['height'], 2)]  # pos_mid is tuple (x,y)
            pos_left = 0
            pos_top = 0
            pos_right = wnd_size['width']
            pos_bottom = wnd_size['height']
            assert type(pos_left) == int
            assert type(pos_top) == int
            assert type(pos_right) == int
            assert type(pos_bottom) == int

            # make sure parameter is valid
            assert type(direction) == str

            # 2 cases , has element or none parameter
            if locator is None:
                # define switch lambda  (Note: iOS XCUITest only)
                switch_action = {
                    'up': lambda: self.driver.execute_script("mobile: swipe", {'direction': 'up'}),
                    'down': lambda: self.driver.execute_script("mobile: swipe", {'direction': 'down'}),
                    'left': lambda: self.driver.execute_script("mobile: swipe", {'direction': 'left'}),
                    'right': lambda: self.driver.execute_script("mobile: swipe", {'direction': 'right'})
                }
                execute_program = 'switch_action["{0}"]()'.format(direction.lower())
                eval(execute_program)
                return True

            elif locator is not None:
                # assert locator format is correct, ex: (by, path)
                assert type(locator) == tuple
                # check if element exists
                if self.get_element(locator) is None:
                    raise EOFError

                # get element location (x,y)
                location = self.get_element(locator).location

                # get element mid position
                el_mid_x = self.get_element_mid_pos(locator)[0]
                el_mid_y = self.get_element_mid_pos(locator)[1]

                # define switch lambda
                switch_actions = {
                    'up': lambda: TA.press(None, el_mid_x, el_mid_y).wait(50).move_to(None, el_mid_x, pos_top).release().perform(),
                    'down': lambda: TA.press(None, el_mid_x, el_mid_y).wait(50).move_to(None, el_mid_x, pos_bottom).release().perform(),
                    'left': lambda: TA.press(None, el_mid_x, el_mid_y).wait(50).move_to(None, pos_right, el_mid_y).release().perform(),
                    'right': lambda: TA.press(None, el_mid_x, el_mid_y).wait(50).move_to(None, pos_left, el_mid_y).release().perform()
                }
                execute_program = 'switch_actions["{0}"]()'.format(direction.lower())
                eval(execute_program)
                return True
            else:
                raise EOFError

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: drag_element
    # Description: drag_element
    # Parameters: locator(tuple), destination(tuple, (x,y)) or lacator(tuple)
    # Return: True/False
    # Note: iOS XCUITest only
    # Author: Terence
    # ==================================================================================================================
    def drag_element(self, locator, destination):
        funcname = inspect.currentframe().f_code.co_name
        # error handling for finding element had been described in get_element
        try:
            # define TA
            TA = TouchAction(self.driver)

            '''
            # test (works)
            element = self.driver.find_elements_by_accessibility_id('btn_small_crop_scale.png')
            x = element[3].location['x']
            y = element[3].location['y']
            print(type(x), x)
            #338, 535
            TA.press(None, x, y).wait(2000).move_to(None, destination[0], destination[1]).release().perform()
            '''

            # get window resolution
            wnd_size = self.get_window_size()
            assert type(wnd_size) == dict

            # make sure parameter is valid
            assert type(destination) == tuple
            if type(destination[0]) == int:
                destination_flag = 'pos'
            else:
                destination_flag = 'locator'
            # assert type(destination[0]) == int
            # assert type(destination[1]) == int

            # assert locator format is correct, ex: (by, path)
            assert type(locator) == tuple

            if type(locator[0]) is not int:
                # assign variable
                element = self.get_element(locator)
                # check if element exists
                if element is None:
                    raise EOFError
                # get element mid position
                el_mid_pos = self.get_element_mid_pos(locator)
                el_mid_x = el_mid_pos[0]
                el_mid_y = el_mid_pos[1]
            else:
                el_mid_x = locator[0]
                el_mid_y = locator[1]

            # start to drag
            if destination_flag == 'pos':
                # DO NOT USE element for press, the drag function would fail
                logger(f"Drag start from: {el_mid_x}, {el_mid_y}")
                logger(f"Drag to: {destination[0]}, {destination[1]}")
                #print(el_mid_x, el_mid_y)
                # !!Because raw ID isn't only one, need to use locator carefully
                TA.press(None, el_mid_x, el_mid_y).wait(1000).move_to(None, destination[0], destination[1]).release().perform()
                time.sleep(1)
                return True

            elif destination_flag == 'locator':
                element2 = self.get_element(destination)
                if element2 is None:
                    raise EOFError
                el2_mid_pos = self.get_element_mid_pos(destination)
                el2_mid_x = el2_mid_pos[0]
                el2_mid_y = el2_mid_pos[1]
                logger(f"Drag start from: {el_mid_x}, {el_mid_y}")
                #print(el_mid_x, el_mid_y)
                # start to swipe
                # DO NOT USE element for press, the drag function would fail
                TA.press(None, el_mid_x, el_mid_y).wait(1000).move_to(None, el2_mid_x, el2_mid_y).release().perform()
                time.sleep(1)
                return True
            else:
                raise EOFError

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))
            if str(exception).count('Connection aborted') > 0 or str(exception).count('server-side error') > 0:
            #if exception == "('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))":
                logger('try again drag function after 10sec.')
                time.sleep(10)
                try:
                    # define TA
                    TA = TouchAction(self.driver)

                    '''
                    # test (works)
                    element = self.driver.find_elements_by_accessibility_id('btn_small_crop_scale.png')
                    x = element[3].location['x']
                    y = element[3].location['y']
                    print(type(x), x)
                    #338, 535
                    TA.press(None, x, y).wait(2000).move_to(None, destination[0], destination[1]).release().perform()
                    '''

                    # get window resolution
                    wnd_size = self.get_window_size()
                    assert type(wnd_size) == dict

                    # make sure parameter is valid
                    assert type(destination) == tuple
                    if type(destination[0]) == int:
                        destination_flag = 'pos'
                    else:
                        destination_flag = 'locator'
                    # assert type(destination[0]) == int
                    # assert type(destination[1]) == int

                    # assert locator format is correct, ex: (by, path)
                    assert type(locator) == tuple

                    if type(locator[0]) is not int:
                        # assign variable
                        element = self.get_element(locator)
                        # check if element exists
                        if element is None:
                            raise EOFError
                        # get element mid position
                        el_mid_pos = self.get_element_mid_pos(locator)
                        el_mid_x = el_mid_pos[0]
                        el_mid_y = el_mid_pos[1]
                    else:
                        el_mid_x = locator[0]
                        el_mid_y = locator[1]

                    # start to drag
                    if destination_flag == 'pos':
                        # DO NOT USE element for press, the drag function would fail
                        logger(f"Drag start from: {el_mid_x}, {el_mid_y}")
                        logger(f"Drag to: {destination[0]}, {destination[1]}")
                        # print(el_mid_x, el_mid_y)
                        # !!Because raw ID isn't only one, need to use locator carefully
                        TA.press(None, el_mid_x, el_mid_y).wait(1000).move_to(None, destination[0],
                                                                              destination[1]).release().perform()
                        time.sleep(1)
                        return True

                    elif destination_flag == 'locator':
                        element2 = self.get_element(destination)
                        if element2 is None:
                            raise EOFError
                        el2_mid_pos = self.get_element_mid_pos(destination)
                        el2_mid_x = el2_mid_pos[0]
                        el2_mid_y = el2_mid_pos[1]
                        logger(f"Drag start from: {el_mid_x}, {el_mid_y}")
                        # print(el_mid_x, el_mid_y)
                        # start to swipe
                        # DO NOT USE element for press, the drag function would fail
                        TA.press(None, el_mid_x, el_mid_y).wait(1000).move_to(None, el2_mid_x,
                                                                              el2_mid_y).release().perform()
                        time.sleep(1)
                        return True
                    else:
                        raise EOFError
                except Exception as exception:
                    logger('[{0}][{1}]: Exception(2nd) ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: pinch_zoom_element
    # Description: pinch_zoom_element
    # Parameters: locator(tuple), scale( 0~1 pinch, >1 zoom)
    # Return: True/False
    # Note: iOS XCUITest only
    # Author: Terence
    # ==================================================================================================================
    def pinch_zoom_element(self, locator, scale):
        funcname = inspect.currentframe().f_code.co_name
        # error handling for finding element had been described in get_element
        try:
            # make sure parameter is valid
            assert scale > 0

            # assert locator format is correct, ex: (by, path)
            assert type(locator) == tuple

            # assign variable
            element = self.get_element(locator)

            # check if element exists
            if element is None:
                raise EOFError

            # get element location (x,y)
            location = element.location

            # start to pinch/zoom
            # velocity must be less than zero when scale is less than 1
            if scale >= 1:
                velocity = 2
            else:
                velocity = -2
            self.driver.execute_script(
                'mobile: pinch',
                {
                    'scale': scale,
                    'velocity': velocity,
                    'element': element
                }
            )
            return True

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: rotate_element
    # Description: rotate_element
    # Parameters: locator(tuple), angle
    # Return: True/False
    # Note: n/a
    # Author: Bill, Terence(modify)
    # ==================================================================================================================
    def rotate_element(self, locator, angle):
        funcname = inspect.currentframe().f_code.co_name


        # ************
        # Actually, rotate function should be use for loop and move with circle
        # Currently, the below algorithm is incorrect. need to implement in the future
        # ************

        """
        element_rect = self.get_element(locator).rect
        x1 = element_rect['x'] + element_rect['width'] / 2
        y1 = element_rect['y'] + element_rect['height'] / 2
        y2 = element_rect['y']
        a = angle * math.pi / 180
        ax2 = int((x2 - x1) * math.cos(a) - (y2 - y1) * math.sin(a)) + x1
        ay2 = int((y2 - y1) * math.cos(a) + (x2 - x1) * math.sin(a)) + y1

        try:
            a1 = TouchAction()
            a1.press(x1, y1)
            a1.move_to(x1, y1)
            a1.release()

            a2 = TouchAction()
            a2.press(x1, y2)
            a2.move_to(ax2, ay2)
            a2.release()

            ma = MultiAction(self.driver)
            ma.add(a1, a2)
            ma.perform()
            return True
        """
        return False

    # ==================================================================================================================
    # Function: pinch_element
    # Description: pinch_element
    # Parameters: locator(tuple), percent, steps
    # Return: True/False
    # Note: n/a
    # Author: Bill, Terence(modify)
    # ==================================================================================================================
    def pinch_element(self, locator, percent=200, steps=50):
        funcname = inspect.currentframe().f_code.co_name
        try:
            self.driver.pinch(self.get_element(locator), percent, steps)
            return True

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: zoom_element
    # Description: zoom_element
    # Parameters: locator(tuple), percent, steps
    # Return: True/False
    # Note: n/a
    # Author: Bill, Terence(modify)
    # ==================================================================================================================
    def zoom_element(self, locator, percent=200, steps=50):
        funcname = inspect.currentframe().f_code.co_name
        try:
            self.driver.zoom(self.get_element(locator), percent, steps)
            return True

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: set_checkbox
    # Description: set_checkbox
    # Parameters: locator(tuple), status(1 or 0)
    # Return: True/False
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def set_checkbox(self, locator, status):
        # error handling had been described in get_element
        funcname = inspect.currentframe().f_code.co_name
        try:
            # assign variable
            element = self.get_element(locator)

            # make sure element exists
            if element is None:
                raise EOFError

            # determine status parameter
            if status == 1:  # haven't ticked, start to tick
                # make sure check box is under unticked status
                if element.get_attribute('value').equals('unchecked') is True:
                    # start to tap
                    self.driver.execute_script(
                        'mobile: tap',
                        {
                            'element': element
                        }
                    )
                    # make sure the checkbox is ticked
                    return element.get_attribute('value').equals('checked')
                else:
                    logger('[{0}][{1}]: element is checked'.format(__name__, funcname))
                    raise EOFError
            elif status == 0:  # have ticked , try to untick
                # make sure check box is under 'ticked' status
                if element.get_attribute('value').equals('checked') is True:
                    # start to tap
                    self.driver.execute_script(
                        'mobile: tap',
                        {
                            'element': element
                        }
                    )
                    # make sure the checkbox is untick
                    return self.get_element(locator).get_attribute('value').equals('checked')
                else:
                    logger('[{0}][{1}]: element is unchecked'.format(__name__, funcname))
                    raise EOFError
            else:
                logger('[{0}][{1}]: parameter is incorrect'.format(__name__, funcname))
                raise EOFError

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: set_dropdown
    # Description: set_dropdown
    # Parameters: locator(tuple), index_or_name
    # Return: True/False
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def set_dropdown(self, locator, index_or_name):
        # error handling had been described in get_element
        funcname = inspect.currentframe().f_code.co_name
        try:
            # assign variable
            element = self.get_element(locator)

            # make sure element exists
            if element is None:
                raise EOFError

            # check parameter is int or string
            if type(index_or_name) is str:
                # start to choose item in combobox by name
                element.sendKeys(index_or_name)
                return True

            elif type(index_or_name) is int:
                assert index_or_name > 0
                # start to choose item in combobox by index
                for x in range(0, index_or_name):
                    self.driver.execute_script(
                        'mobile: selectPickerWheelValue',
                        {
                            'order': 'next',
                            'offset': '0.15',
                            'element': element
                        }
                    )
                return True
            else:
                logger('[{0}][{1}]: incorrect parameter'.format(__name__, funcname))
                raise EOFError

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: set_slider
    # Description: set_slider
    # Parameters: locator(tuple), percentage(float >= 0, (ex:0.2))
    # Return: True/False
    # Note: need verify the slider in page(value shows on different element)
    # Author: Terence
    # ==================================================================================================================
    def set_slider(self, locator, percentage):
        # error handling had been described in get_element
        funcname = inspect.currentframe().f_code.co_name
        try:
            # assign variable
            element = self.get_element(locator)

            # make sure element exists
            if element is None:
                raise EOFError

            element.send_keys(str(percentage))
            #element.set_value(str(percentage))
            return True
            '''
            # need to get the total length of XCUIelementTypeSlider and calculate the x value
            el_width = element.size['width']
            # currently in iPHD, the magic number is 16.82
            x = 16.82

            # formula
            # el_width*input-x = (output/100) * (el_width - 2x)

            # convert percentage as output
            input = (((percentage) * (el_width - 2 * x)) + x)/el_width
            print(input)

            # set value
            # assert percentage >= 0
            # print(str(input))
            # element.set_value(0.3)
            element.send_keys(str(input))

            # ensure value had been set
            value = element.get_attribute('value')
            print(value)
            check = round(int(value.split('%')[0])/100, 2)
            # tolerance +_ 0.01
            if check == percentage or (check + 0.01) == percentage or (check - 0.01) == percentage:
                return True
            else:
                logger("[{0}][{1}]: Value isn't the same as parameter. (App value: {2}) (para value: {3})".format(__name__, funcname, check, percentage))
                raise EOFError
            '''
        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))
            if str(exception).count('Connection aborted') > 0 or str(exception).count('server-side error') > 0:
                # if exception == "('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))":
                logger('try again set_slider function after 10sec.')
                time.sleep(10)
                try:
                    # assign variable
                    element = self.get_element(locator)

                    # make sure element exists
                    if element is None:
                        raise EOFError

                    element.send_keys(str(percentage))
                    # element.set_value(str(percentage))
                    return True
                except Exception as e:
                    logger('[{0}][{1}]: Exception(2nd) ({2})'.format(__name__, funcname, e))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: click_element
    # Description: click
    # Parameters: locator(tuple), times
    # Return: True/False
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def click_element(self, locator, times=1):
        # error handling had been described in get_element
        funcname = inspect.currentframe().f_code.co_name
        try:
            # assign variable
            element = self.get_element(locator)

            # check times is valid
            assert int(times) > 0

            # make sure element exists
            if element is not None:
                for x in range(0, int(times)):
                    element.click()
                    return True

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: tap_element
    # Description: tap
    # Parameters: locator(tuple)
    # Return: True/False
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def tap_element(self, locator):
        funcname = inspect.currentframe().f_code.co_name
        # error handling for finding element had been described in get_element
        try:
            # define TA
            TA = TouchAction(self.driver)

            # assert locator format is correct, ex: (by, path)
            assert type(locator) == tuple

            # check times is valid
            # assert int(times) > 0

            # assign variable
            element = self.get_element(locator)

            # make sure element exists
            if element is not None:
                TA.tap(element).perform()
                return True
            else:
                logger("can't find element")

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: double_tap_element
    # Description: double_tap_element
    # Parameters: locator(tuple), (opt) interval=0.2
    # Return: True/False
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def double_tap_element(self, locator, interval=0.2):
        funcname = inspect.currentframe().f_code.co_name
        # error handling for finding element had been described in get_element
        try:
            # define TA
            TA = TouchAction(self.driver)

            # assert locator format is correct, ex: (by, path)
            assert type(locator) == tuple

            # check times is valid
            assert interval > 0

            # assign variable
            element = self.get_element(locator)

            # make sure element exists
            if element is not None:
                for x in range(0, 2):
                    TA.tap(element).perform()
                    time.sleep(interval)
                return True

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: tap
    # Description: tap
    # Parameters: destination (tuple, (x,y))
    # Return: True/False
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def tap(self, destination):
        funcname = inspect.currentframe().f_code.co_name
        # error handling for finding element had been described in get_element
        try:
            # define TA
            TA = TouchAction(self.driver)
            # assert locator format is correct, ex: (by, path)
            if type(destination) != tuple:
                raise ValueError

            # check times is valid
            # assert int(times) > 0

            # start to tap
            TA.tap(None, int(destination[0]), int(destination[1]), 1).perform()
            return True

        except ValueError:
            logger('[{0}][{1}]: ValueError'.format(__name__, funcname))

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))
            if str(exception).count('Connection aborted') > 0 or str(exception).count('server-side error') > 0:
            #if exception == "('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))":
                logger('try again tap function after 10sec.')
                time.sleep(10)
                # ================
                try:
                    # define TA
                    TA = TouchAction(self.driver)
                    # assert locator format is correct, ex: (by, path)
                    if type(destination) != tuple:
                        raise ValueError

                    # check times is valid
                    # assert int(times) > 0

                    # start to tap
                    TA.tap(None, int(destination[0]), int(destination[1]), 1).perform()
                    return True

                except ValueError:
                    logger('[{0}][{1}]: ValueError'.format(__name__, funcname))

                except AssertionError:
                    logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

                except EOFError as error:
                    logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

                except Exception as exception:
                    logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: handle_alert
    # Description: handle_alert
    # Parameters: control (True: access/ False:dismiss)
    # Return: True/False
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def handle_alert(self, control):
        funcname = inspect.currentframe().f_code.co_name
        try:
            if control is True:
                self.driver.switch_to.alert.accept()
                return True
            elif control is False:
                self.driver.switch_to.alert.dismiss()
                return True
            else:
                logger('parameter is incorrect')
        except ValueError:
            logger('[{0}][{1}]: ValueError'.format(__name__, funcname))

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: long_press_element
    # Description: long_press_element
    # Parameters: locator(tuple)
    # Return: True/False
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def long_press_element(self, locator):
        funcname = inspect.currentframe().f_code.co_name
        # define TA
        TA = TouchAction(self.driver)
        # error handling for finding element had been described in get_element
        try:
            # assert locator format is correct, ex: (by, path)
            assert type(locator) == tuple
            # make sure parameter is valid
            # assert type(time) == int
            # assert int(time) > 0

            #conver to float
            # time = round(float(time), 1)

            # check if element exists
            element = self.get_element(locator)
            if element is not None:
                self.driver.execute_script(
                    "mobile: touchAndHold",
                    {
                        "element": element,
                        "duration": 1
                    }
                )
                return True

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: get_text
    # Description: get text
    # Parameters: locator(tuple)
    # Return: text(str)/False
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def get_text(self, locator):
        # error handling for finding element had been described in get_element
        funcname = inspect.currentframe().f_code.co_name
        try:
            # assert locator format is correct, ex: (by, path)
            assert type(locator) == tuple

            # assign variable
            element = self.get_element(locator)

            # make sure element exists
            if element is not None:
                text = element.text
            # make sure text is str
                assert type(text) == str
                # for verification if having keyboard UI popping up (handle on page or test case)
                '''
                try:
                    self.implicit_wait(5)
                    self.driver.hide_keyboard()
                except:
                    logger('no done btn')
                '''
                return text

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))
            if str(exception).count('server-side error') > 0 or str(exception).count('Connection aborted') > 0:
                logger('try again after 10sec.')
                time.sleep(10)
                try:
                    # assert locator format is correct, ex: (by, path)
                    assert type(locator) == tuple
                    # assign variable
                    element = self.get_element(locator)
                    # make sure element exists
                    if element is not None:
                        text = element.text
                        # make sure text is str
                        assert type(text) == str
                        # for verification if having keyboard UI popping up (handle on page or test case)
                        '''
                        try:
                            self.implicit_wait(5)
                            self.driver.hide_keyboard()
                        except:
                            logger('no done btn')
                        '''
                        return text
                except Exception as exception:
                    logger('[{0}][{1}]: Exception(2nd) ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: set_text
    # Description: add text
    # Parameters: locator(tuple)
    # Return: True/False
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def set_text(self, locator, text, clear_flag=0):
        # error handling for finding element had been described in get_element
        funcname = inspect.currentframe().f_code.co_name
        try:
            # assert locator format is correct, ex: (by, path)
            assert type(locator) == tuple

            # assign variable
            element = self.get_element(locator)

            # make sure element exists
            if element is not None:
                # doesn't need to clear
                if clear_flag == 0:
                    element.send_keys(text)
                    # for verification if having keyboard UI popping up (handle on page or test case)
                    '''
                    try:
                        self.implicit_wait(5)
                        self.driver.hide_keyboard()
                    except:
                        logger('no done btn')
                    '''
                    return True
                # need to clear
                elif clear_flag == 1:
                    element.click()
                    self.driver.hide_keyboard()  # [XCUITest]it's depend on keyboard layout(final button = right-bottom)
                    element.clear()
                    element.send_keys()
                    return True
                else:
                    logger('incorrect parameter(clear_flag)')
                    return False

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: put_file
    # Description: put_file
    # Parameters: path, filename
    # Return: True/False
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def put_file(self, path, filename):
        funcname = inspect.currentframe().f_code.co_name
        try:
            # assert parameter is valid
            assert os.path.isdir(path) is True
            assert os.path.exists(path) is True

            # put file
            self.driver.push_file(os.path.join(path, filename))
            return True

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: get_file
    # Description: get_file
    # Parameters: path, filename
    # Return: True/False
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def get_file(self, path, filename):
        funcname = inspect.currentframe().f_code.co_name
        try:
            # assert parameter is valid
            assert os.path.isdir(path) is True
            assert os.path.exists(path) is True

            # get file
            self.driver.pull_file(os.path.join(path, filename))
            return True

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: get_snapshot
    # Description: get_snapshot
    # Parameters: path(recommend to use *.png)
    # Return: True/False
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def get_snapshot(self, path):
        funcname = inspect.currentframe().f_code.co_name
        try:
            # old
            # assert parameter is valid
            #assert os.path.isdir(path) is True
            #assert os.path.exists(path) is True
            # snapshot and save to local
            # self.driver.save_screenshot(os.path.join(path, filename))

            # Xcode 10
            #self.driver.save_screenshot(path)

            # Xcode 11 (wordaround, due to snapshot takes too slow, appium is checking)
            if os.path.exists(path):
                os.remove(path)
            os.popen(f'idevicescreenshot {path}')
            for x in range(10):     # sometimes network is slow
                if os.path.exists(path):
                    return True
                else:
                    time.sleep(1)
            #time.sleep(5)  # wait 3sec. to get img
        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

# ***Element determine Functions***
    # ==================================================================================================================
    # Function: get_element
    # Description: get element
    # Parameters: locator(tuple), timeout, poll_frequency)
    # Return: Element/None
    # Note: Return element if found else None
    # Author: Terence
    # ==================================================================================================================
    def get_element(self, locator, timeout=DEFAULT_TIMEOUT, poll_frequency=DEFAULT_POLL_TIME):
        funcname = inspect.currentframe().f_code.co_name
        try:
            if poll_frequency is None:  # avoid to change base_page
                poll_frequency = DEFAULT_POLL_TIME
            #logger(f'driver layer: {timeout}, {poll_frequency}')
            # define wait
            wait = WebDriverWait(self.driver, timeout, poll_frequency)  # set timeout as 20 due to Xcode11 isn't stable(10sec. or 15sec. would fail)
            # assert locator format is correct, ex: (by, path)
            assert type(locator) == tuple
            # if get, return element object
            return wait.until(EC.presence_of_element_located(locator))

        except TimeoutException:
            logger("[{0}][{1}]: Timeout. Can't find ({2}) element".format(__name__, funcname, locator))
        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))
        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))
        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))
            if str(exception).count('Connection aborted') > 0 or str(exception).count('server-side error') > 0:
                logger('try again tap function after 10sec.')
                time.sleep(10)
                try:
                    # define wait
                    wait = WebDriverWait(self.driver, timeout,
                                         poll_frequency)  # set timeout as 20 due to Xcode11 isn't stable(10sec. or 15sec. would fail)
                    # assert locator format is correct, ex: (by, path)
                    assert type(locator) == tuple
                    # if get, return element object
                    return wait.until(EC.presence_of_element_located(locator))
                except Exception as e:
                    logger('[{0}][{1}]: Exception(2nd) ({2})'.format(__name__, funcname, e))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return None

    # ==================================================================================================================
    # Function: get_elements
    # Description: get elements
    # Parameters: locator(tuple), timeout, poll_frequency)
    # Return: Element(list)/None
    # Note: Return elements if found else None
    # Author: Terence
    # ==================================================================================================================
    def get_elements(self, locator, index, timeout=DEFAULT_TIMEOUT, poll_frequency=DEFAULT_POLL_TIME):
        funcname = inspect.currentframe().f_code.co_name
        # define wait
        wait = WebDriverWait(self.driver, timeout, poll_frequency)
        try:
            # assert locator is tuple
            assert type(locator) == tuple
            elements = wait.until(EC.presence_of_all_elements_located(locator))
            logger(f'element list: {elements}')
            return elements[index]

        except TimeoutException:
            logger("[{0}][{1}]: Timeout. Can't find ({2}) element".format(__name__, funcname, locator))

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return None

    # ==================================================================================================================
    # Function: is_element_highlighted
    # Description: is_element_highlighted
    # Parameters: locator(tuple)
    # Return:
    #           Value <== str (it's value)
    #           "1"   <== str means True
    #           None  <== means false
    #           "0"   <== str mean false (at switch)
    #           False <== exception
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def is_element_highlighted(self, locator):
        # error handling for finding element had been described in get_element
        funcname = inspect.currentframe().f_code.co_name
        try:
            # assert locator format is correct, ex: (by, path)
            assert type(locator) == tuple

            # assign variable
            element = self.get_element(locator)

            # make sure element exists
            if element is not None:
                value = element.get_attribute("value")
                return value
            else:
                logger(f'[{__name__}][{funcname}]: element is None')

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: is_element_enabled
    # Description: is_element_enabled
    # Parameters: locator(tuple)
    # Return:
    #           "true"   <== str means enabled
    #           "false"  <== str means disabled
    #           False <== exception
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def is_element_enabled(self, locator):
        # error handling for finding element had been described in get_element
        funcname = inspect.currentframe().f_code.co_name
        try:
            # assert locator format is correct, ex: (by, path)
            assert type(locator) == tuple

            # assign variable
            element = self.get_element(locator)

            # make sure element exists
            if element is not None:
                value = element.get_attribute("enabled")
                return value
            else:
                logger(f'[{__name__}][{funcname}]: element is None')

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

# Wait Element Functions
    # ==================================================================================================================
    # Function: wait_until_element_exist
    # Description: get wait_until_element_exist
    # Parameters: locator(tuple), timeout, poll_frequency)
    # Return: True/False
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def wait_until_element_exist(self, locator, timeout=DEFAULT_TIMEOUT, poll_frequency=DEFAULT_POLL_TIME):
        funcname = inspect.currentframe().f_code.co_name
        # define wait
        wait = WebDriverWait(self.driver, timeout, poll_frequency)
        try:
            # assert locator is tuple
            assert type(locator) == tuple
            element = wait.until(EC.presence_of_element_located(locator), '({0}) do not show up or exception'.format(locator[1]))
            return False if type(element) is str else True

        except TimeoutException:
            logger("[{0}][{1}]: Timeout. Can't find ({2}) element".format(__name__, funcname, locator))

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: wait_until_element_not_exist
    # Description: wait_until_element_not_exist
    # Parameters: locator(tuple), timeout, poll_frequency)
    # Return: True/False
    # Note: would check if elements exist and then start wait.until_not
    # Author: Terence
    # ==================================================================================================================
    def wait_until_element_not_exist(self, locator, timeout=DEFAULT_TIMEOUT, poll_frequency=DEFAULT_POLL_TIME):
        funcname = inspect.currentframe().f_code.co_name
        # define wait
        wait = WebDriverWait(self.driver, timeout, poll_frequency)
        try:
            # assert locator is tuple
            assert type(locator) == tuple
            element = wait.until_not(EC.presence_of_element_located(locator), '({0}) still exists or exception'.format(locator[1]))
            return False if type(element) is str else True

        except TimeoutException:
            logger("[{0}][{1}]: Timeout. ({2}) element still exists.".format(__name__, funcname, locator))

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: wait_until_element_selected
    # Description: wait_until_element_selected
    # Parameters: locator(tuple), timeout, poll_frequency)
    # Return: True/False
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def wait_until_element_selected(self, locator, timeout=DEFAULT_TIMEOUT, poll_frequency=DEFAULT_POLL_TIME):
        funcname = inspect.currentframe().f_code.co_name
        # define wait
        wait = WebDriverWait(self.driver, timeout, poll_frequency)
        try:
            element = self.get_element(locator)
            result = wait.until(EC.element_to_be_selected(element), "({}) can't be selected or exception".format(element))
            return False if type(result) is str else True

        except TimeoutException:
            logger("[{0}][{1}]: Timeout. ({2}) element can't be selected".format(__name__, funcname, locator))

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: wait_until_element_clickable
    # Description: wait_until_element_clickable
    # Parameters: locator(tuple), timeout, poll_frequency)
    # Return: True/False
    # Note: n/a
    # Author: Terence
    # ==================================================================================================================
    def wait_until_element_clickable(self, locator, timeout=DEFAULT_TIMEOUT, poll_frequency=DEFAULT_POLL_TIME):
        funcname = inspect.currentframe().f_code.co_name
        # define wait
        wait = WebDriverWait(self.driver, timeout, poll_frequency)
        try:
            # assert locator is tuple
            assert type(locator) == tuple
            result = wait.until(EC.element_to_be_clickable(locator), "The property of ({}) is unclickable or exception".format(locator[1]))
            return False if type(result) is str else True

        except TimeoutException:
            logger("[{0}][{1}]: Timeout. ({2}) element is unclickable".format(__name__, funcname, locator))

        except AssertionError:
            logger('[{0}][{1}]: AssertionError'.format(__name__, funcname))

        except EOFError as error:
            logger('[{0}][{1}]: EOFError ({2})'.format(__name__, funcname, error))

        except Exception as exception:
            logger('[{0}][{1}]: Exception ({2})'.format(__name__, funcname, exception))

        logger('[{0}][{1}]: Unexpected Error.'.format(__name__, funcname))
        return False

    # ==================================================================================================================
    # Function: Debug purpose
    # Description: Debug purpose
    # Note: functions would be changed for testing anytime
    # Author: Terence
    # ==================================================================================================================
    #def test(self):
    #   print('test')

    def implicitly_wait(self, time=None):
        try:
            result = self.implict_wait_value
        except:
            logger("<<No default implicitly_wait found, set it as 5>>")
            self.implict_wait_value = 5
        if time == None:
            return result
        else:
            self.implict_wait_value = time
        try:
            # logger("set new implicitly_wait: %s" % time )
            self.driver._implicitly_wait(time)
            return time
        except Exception:
            raise Exception
            
    def _swipe(self,x1,y1,x2,y2,time=1):
        logger(f'swipe from ({x1},{y1}) to ({x2},{y2})')
        self.ta.press(x=x1,y=y1).wait(time*1000+1000).move_to(x=x2,y=y2).release().perform()
        return self
    def swipe_up(self,percentage=0.5,time=2):
        try:
            size = self.driver.get_window_size()
            x1 = size['width'] * 0.5
            y1 = size['height'] * (0.5 + percentage/2)
            y2 = size['height'] * (0.5 - percentage/2)
            logger(f'{x1=}/{y1=}/{y2=}')
            self._swipe(x1, y1, x1, y2,time)
            return self
        except Exception as e:
            logger(e)
            return False
        
    def swipe_down(self,percentage=0.5,time=2):
        self.swipe_up(percentage*-1,time)
        
    def click_pos(self,x,y):
        self.ta.press(x=x,y=y).wait(100).release().perform()
        
