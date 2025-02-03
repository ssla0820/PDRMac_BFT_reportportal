"""
DriverFactory uses the factory design pattern.
get_mobile_driver_object() returns the appropriate mobile driver object.
get_web_driver_object() returns the appropriate web driver object.
Add elif clauses as and when you implement new drivers.
"""
try:
    # from selenium import webdriver
    # from ATFramework.drivers.appium_driver import AppiumU2Driver
    # from ATFramework.drivers.xcuitest_driver import AppiumXCUITestDriver
    # from appium_driver import AppiumU2Driver
    # from drivers.appium_driver import AppiumXCUITestDriver
    # from drivers.atx_driver import ATXU2Driver
    # from xcuitest_driver import AppiumXCUITestDriver
    import platform
    from ATFramework.utils.log import logger
    # from ATFramework import macos_12_monterey_patch
    # from ATFramework.drivers.Mac_Control import MWC
    # from ATFramework.drivers.mac_driver import Mac

except Exception as e:
    logger(f"{e=}")


class DriverFactory:
    """ DriverFactory uses the factory design pattern.  """

    @staticmethod
    def get_mobile_driver_object(driver_name, driver_config, app_config, test_mode='local', desired_caps={}, device_name="", package_name=""):
        # Return the appropriate driver object based on driver_name
        driver_obj = None
        driver_name = driver_name.lower()
        device_name = device_name.lower()
        package_name = package_name.lower()
        if driver_name == "appium u2":
            from ATFramework.drivers.appium_driver import AppiumU2Driver
            driver_obj = AppiumU2Driver(driver_config, app_config, test_mode, desired_caps)
        elif driver_name == "appium xcui":
            from ATFramework.drivers.xcuitest_driver import AppiumXCUITestDriver
            if driver_config.get("device_type","") == "iphone_se":
                from . import xcuitest_driver_iphone_se
            driver_obj = AppiumXCUITestDriver(driver_config, app_config, test_mode, desired_caps)
        # elif driver_name == "atx":
        #    driver_obj = ATXU2Driver()
        return driver_obj

    @staticmethod
    def get_web_driver_object(driver_name,**kw):
        # Return the appropriate driver object based on driver_name
        driver_obj = None
        driver_name = driver_name.lower()
        if driver_name == "chrome":
            from ATFramework.drivers.umeeting_lib import Host
            driver_obj = Host(kw['option']['option'],case=kw.get('case',None),account=kw.get('account',None))
        if driver_name == "chrome_participant":
            from ATFramework.drivers.umeeting_lib import Participant
            driver_obj = Participant(kw['option']['option'],case=kw.get('case',None),account=kw.get('account',None))
        return driver_obj

    @staticmethod
    def get_web_driver_v2_object(driver_name, option, options=None, desired_caps=None):
        # Return the appropriate driver object based on driver_name
        driver_obj = None
        driver_name = driver_name.lower()
        if driver_name == 'chrome':
            if platform.system() == 'Windows':
                from ATFramework.drivers.web_driver import initialChrome
            else:
                from ATFramework.drivers.web_driver_mac import initialChrome
            driver_obj = initialChrome(option, options, desired_caps)
        if driver_name == 'edge':
            from ATFramework.drivers.web_driver import initialEdge
            driver_obj = initialEdge(option, options)
        if driver_name == 'safari':
            from ATFramework.drivers.web_driver_mac import initialSafari
            driver_obj = initialSafari(option)
        if 'android' in driver_name:
            from ATFramework.drivers.web_driver_uiautomator2 import initialRemote
            driver_obj = initialRemote(option, options, desired_caps)
        if 'ios' in driver_name:
            from ATFramework.drivers.web_driver_xcuitest import initialRemote
            driver_obj = initialRemote(option, options, desired_caps)
        if driver_name == 'firefox':
            from ATFramework.drivers.web_driver import initialFirefox
            driver_obj = initialFirefox(option, options)
        if driver_name == 'healenium':
            from ATFramework.drivers.web_driver import initialHealenium
            driver_obj = initialHealenium(option, options)
        return driver_obj

    @staticmethod
    def get_mac_driver_object(driver_name, app_name=None, app_bundleID=None, app_path=None, element=None):
        driver_obj = None
        driver_name = driver_name.lower()
        if driver_name == 'mwc':
            from ATFramework.drivers.Mac_Control import MWC
            driver_obj = MWC(app_name, app_bundleID, app_path)
        elif driver_name == 'mac':
            from ATFramework.drivers.mac_driver import Mac
            driver_obj = Mac(app_bundleID, app_path, app_name)
        else:
            logger('incorrect driver_name')
            return None
        return driver_obj

    @staticmethod
    def get_win32_driver_object(app_path, app_process_name):
        driver_obj = None
        from ATFramework.drivers.win32_driver import Win32
        driver_obj = Win32(app_path, app_process_name)
        return driver_obj

    @staticmethod
    def get_uiautomation_driver_object(app_path, app_process_name):
        driver_obj = None
        from ATFramework.drivers.win32_driver import UIAutomation
        driver_obj = UIAutomation(app_path, app_process_name)
        return driver_obj

    @staticmethod
    def get_koan_driver_adr_object(app_path, app_process_name):
        driver_obj = None
        from ATFramework.drivers.koan_driver_adr import KoanUI
        driver_obj = KoanUI(app_path, app_process_name)
        return driver_obj
