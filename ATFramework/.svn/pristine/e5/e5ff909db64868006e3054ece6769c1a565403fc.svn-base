import importlib, winreg
import time,glob, sys
import os, inspect, ctypes

from os.path import basename
from tkinter import Tk
from ._report.report import MyReport
from .log import logger

from selenium.webdriver import Chrome , Firefox , Ie
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


def writeINI(array, file = os.getenv('LOCALAPPDATA')+"\\AutoWeb\\browserInfo.ini"):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, "w") as f:
        str = ""
        for data in array:
            str += data + "\n"
        f.write(str)

def readINI(index=0,file = os.getenv('LOCALAPPDATA')+"\\AutoWeb\\browserInfo.ini"):
    with open(file, "r") as f:
        ret = []
        for data in f:
            ret.append(data[:-1])
    return ret[index]

def create_driver_session(session_id, executor_url):
    # Save the original function, so we can revert our patch
    org_command_execute = RemoteWebDriver.execute
    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)
    # Patch the function before creating the driver object
    RemoteWebDriver.execute = new_command_execute
    new_driver = MyRemote(command_executor=executor_url, desired_capabilities=webdriver.DesiredCapabilities.FIREFOX)
    new_driver.session_id = session_id
    # Replace the patched function with original function
    RemoteWebDriver.execute = org_command_execute
    return new_driver
    
def require_adm():
    d = os.path.dirname
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    SW_HIDE = 0
    # target = d(d(__file__)) 
    hWnd = kernel32.GetConsoleWindow()
    try:
        is_adm = ctypes.windll.shell32.IsUserAnAdmin()
    except:
        is_adm = False
    if not is_adm:
        if hWnd: user32.ShowWindow(hWnd, SW_HIDE)
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable," -i " +  " ".join(sys.argv) , None, 1)
        sys.exit(0)
    else: return True
    
class Protocol():
    def __init__(self, is_prod):
        if is_prod:
            self.REG_PATH_1 = f"cyberlinku\\shell\\Open\\command"
            self.REG_PATH_2 = f"cyberlinku"
            self.value = r'"C:\ProgramData\CyberLink\U\U.exe" "%1"'
        else:
            self.REG_PATH_1 = f"cyberlinkubeta\\shell\\Open\\command"
            self.REG_PATH_2 = f"cyberlinkubeta"
            self.value = r'"C:\ProgramData\CyberLink\U Beta\UBeta.exe" "%1"'
    
    def enable(self):
        self._set_reg(self.REG_PATH_1, "", self.value)
        self._set_reg(self.REG_PATH_2, "URL Protocol", "")
    
    def disable(self):
        self._set_reg(self.REG_PATH_1,"",'')
        self._set_reg(self.REG_PATH_2, "URL Protocol", "")
        
    def _set_reg(self,path, name, value):
        try:
            winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, path)
            registry_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, path, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
            winreg.CloseKey(registry_key)
            return True
        except WindowsError:
            return False    
    def _get_reg(self,name):
        try:
            registry_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, path, 0, winreg.KEY_READ)
            value, regtype = winreg.QueryValueEx(registry_key, name)
            winreg.CloseKey(registry_key)
            return value
        except WindowsError:
            return None
            
def initialChrome(option,fake_media=True,options = None):
    if not options:
        print("[ERROR] Please set options")
        return None
    
    if option.get('participant', False):
        logger("Participant created")
        options.add_argument(f"--window-position={option.get('window_x',0)},{option.get('window_y',0)}")
        options.add_argument(f"--window-size={option['windowWidth']},{option['windowHeight']}")
        driver = MyChrome(option['chromePath'],options=options)
        # driver.set_window_size(option['windowWidth'],option['windowHeight'])
        # driver.set_window_position(option.get('window_x',0),option.get('window_y',0))
        driver.implicitly_wait(option['implicitly_wait'])
        driver.setimplicitlyWait(option['implicitly_wait']) # for get method if necessary. Using for restore implicitly_wait duration.
        return driver
    elif option.get('reconnect', False):
        logger("reconnected")
        print("reconnect: True")
        options.add_argument("--headless")
        driver = MyRemote(command_executor=readINI(),desired_capabilities=webdriver.DesiredCapabilities.CHROME,options=options)
        driver.implicitly_wait(option['implicitly_wait'])
        driver.setimplicitlyWait(option['implicitly_wait']) # for get method if necessary. Using for restore implicitly_wait duration.
        driver.session_id = readINI(1)
    else:
        logger("Host created")
        driver = MyChrome(option['chromePath'],options=options)
        driver.implicitly_wait(option['implicitly_wait'])
        driver.setimplicitlyWait(option['implicitly_wait']) # for get method if necessary. Using for restore implicitly_wait duration.
        writeINI([driver.command_executor._url,driver.session_id])
        if not option['report']:
            logger("Report instance is not created.")
            return driver
        driver.set_report(option['report'])
        
    driver.report_set_title(option['report_title'])
    driver.report_set_browser(driver.name)
    # print ("capability=",driver.capabilities)
    driver.report_set_browser_version(driver.capabilities['browserVersion'])
    return driver

def initialFirefox(option):
    _firefoxPath = option.get("firefoxPath",os.path.dirname(os.path.dirname(__file__))+"\\geckodriver.exe")
    _logPath = os.devnull #option.get("logPath",os.getenv('TEMP')+"\\server_log_path.log")
    if option.get('reconnect', False):
        driver = create_driver_session(readINI(1),readINI(0))
        try:
            driver.capabilities = eval(readINI(2))          #restore capabilities from previous connection, due to firefox issue
        except:
            print("Convert capabilities error.")
        driver.implicitly_wait(option['implicitly_wait'])
        driver.setimplicitlyWait(option['implicitly_wait']) # for get method if necessary. Using for restore implicitly_wait duration.
    else:
        # print (_logPath,"/",_firefoxPath)
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("intl.accept_languages", "en-us")
        firefox_profile.set_preference("geo.enabled", False);
        firefox_profile.set_preference("dom.webnotifications.enabled", False)
        firefox_profile.set_preference("geo.prompt.testing", False);
        firefox_profile.set_preference("geo.prompt.testing.allow", False);
        firefox_profile.update_preferences()
        driver = MyFirefox(service_log_path=_logPath,executable_path=_firefoxPath,firefox_profile=firefox_profile)
        driver.set_window_size(option['windowWidth'],option['windowHeight'])
        driver.implicitly_wait(option['implicitly_wait'])
        driver.setimplicitlyWait(option['implicitly_wait']) # for get method if necessary. Using for restore implicitly_wait duration.
        driver.get(option['webAddress'])
        writeINI([driver.command_executor._url,driver.session_id,str(driver.capabilities)])
    driver.report_set_title(option['report_title'])
    driver.report_set_browser(driver.name)
    # print ("capability=",driver.capabilities)
    driver.report_set_browser_version(driver.capabilities['browserVersion'])
    return driver

def initialIe(option):
    _iePath = option.get("iePath",os.path.dirname(os.path.dirname(__file__))+"\\IEDriverServer.exe")
    if option.get('reconnect', False):
        driver = create_driver_session(readINI(1),readINI(0))
        try:
            driver.capabilities = eval(readINI(2))          #restore capabilities from previous connection, due to ie issue
        except:
            print("Convert capabilities error.")
        driver.implicitly_wait(option['implicitly_wait'])
        driver.setimplicitlyWait(option['implicitly_wait']) # for get method if necessary. Using for restore implicitly_wait duration.
    else:
        # print (_logPath,"/",_firefoxPath)
        driver = MyIe(_iePath)
        driver.get(option['webAddress'])                #go to any page first to clear local storage
        driver.set_window_size(option['windowWidth'],option['windowHeight'])
        driver.execute_script('localStorage.clear();')   # IE won't clear local storage automatically
        driver.implicitly_wait(option['implicitly_wait'])
        driver.setimplicitlyWait(option['implicitly_wait']) # for get method if necessary. Using for restore implicitly_wait duration.
        driver.get(option['webAddress'])
        writeINI([driver.command_executor._url,driver.session_id,str(driver.capabilities)])
    driver.report_set_title(option['report_title'])
    driver.report_set_browser(driver.name)
    # print ("capability=",driver.capabilities)
    driver.report_set_browser_version(driver.capabilities['browserVersion'])
    return driver

''' add setCollapsed'''
def setCollapsed(self,collapsed):
    try:
        if self.get_attribute("collapsed") != str(collapsed).lower():
            el = self.find_element_by_css_selector("div > a")
            el.click()
    except:
        pass
    return self
WebElement.setCollapsed = setCollapsed


class MyClass():
    implicitlyWait = 0
    _web_element_cls = WebElement
    myReport = None
    startTime = time.time()
    wrapper_fail_log = ""
    wrapper_last_result=False
    
    def set_report(self,report):
        logger(f"Report appiled: {report=}")
        logger(f"{self=}")
        self.myReport = report
        logger(f"{self.myReport=}")
    
    def find(self, targets, found = None):
        if isinstance(targets,list):
            if found is not None:
                ret = found
            else:
                ret = super()
            for d in targets:
                if isinstance(d,dict):
                    ret = self._findInFound(d,ret)
                    if not ret :
                        return None # ToDO: add error log here
            return ret
    def wrapper(self,case,*aug):
        ret = importlib.import_module('._wrapper.'+case.lower(), __package__)
        #print("wrapper paremeter=" + str(aug))
        ret.Run(self,aug,case)
    def test_case(self,case):
        ret = importlib.import_module('._test_case.'+case.lower(), __package__)
        try:
            ret.Run(self)
        except Exception as e:
            print ("[error] " + str(e))
        return self
    def _findInFound(self, dict, found):
        ret = None
        try:
            if dict['multiple']:
                ret =  found.find_elements(dict['by'],dict['value'])[dict['index']]
            else:
                ret = found.find_element(dict['by'],dict['value'])
        except KeyError:
            #print ("return all elements")
            return found.find_elements(dict['by'],dict['value'])
        except:
            pass #print ("element is not found: " + str(dict))
        try:
            if dict['attribute'] != None:
                ret = ret.get_attribute(dict['attribute'])
        except:
            pass
        return ret
    def printValue(self,el,index=None,printIt = True):
        oldTime = time.time()
        # while (time.time()-oldTime < 5):
            # try:
                # result_text = self.find(el).text
                # if result_text != "":
                    # break
            # except:
                # pass
        # print ("Text=" + str(result_text) )        
        result_text = ""
        while (time.time()-oldTime < 5):
            try:
                if index is None:
                    element = self.find(el)
                    if isinstance(element,list):
                        element = element[0]
                else:
                    element = self.find(el)[index-1]
                if type(element) == str:
                    result_text = element # for attribute
                else:
                    result_text = element.text
            except:
                pass
            if result_text != "":
                break
        if printIt:
            print ("Text=" + result_text )
        else:
            return result_text
    def object_click(self,target):
        self.find(target).click()
        return target
    def object_drag_and_drop_offset(self,el,width=0,height=0):
        action = ActionChains(self)
        action.click_and_hold(el).perform()
        action.drag_and_drop_by_offset(el,width,height).perform()
        return el
    def debugWrapper(self,wrap,*augs):
        ret = self.wrapper(wrap, *augs)
    def object_equal(self,path,val,timeout = 0,index=1):
        oldTime = time.time()
        ret = False
        while True:
            el = self.find(path)
            if el is None:
                print ("object does not exist:")
                break
            el = el if not isinstance(el,list) else el[index-1]
            text = el if isinstance(el,str) else el.text
            if (text == val):
                ret = True
                break
            if (time.time()-oldTime > timeout):
                break
        # print ("[object_equal] Found text = " + el.text + "expect = " + str(val))
        self.wrapper_last_result=ret
        return ret
    def object_not_equal(self,path,val,timeout = 0,index=1):
        oldTime = time.time()
        ret = False
        while True:
            el = self.find(path)
            if el is None:
                print ("object does not exist:")
                break
            el = el if not isinstance(el,list) else el[index-1]
            text = el if isinstance(el,str) else el.text
            if (el.text != val):
                ret = True
            if (time.time()-oldTime > timeout):
                break
        #print ("[object_equal] Found text = " + el.text + "expect not equal " + str(val))
        self.wrapper_last_result=ret
        return ret
    def report(self, wrapper, result, id = None, log=None):
        frame_records = inspect.stack()[1]
        # print (frame_records.filename)        
        name = basename(wrapper).replace(".py","")
        if id is None:
            print ("[" +name+ "] = " + str(result) )
        else:
            pass
        if not result:
            self.wrapper_fail_log = '<font color="red">[{}] fail</font>'.format(name)
        self.wrapper_last_result=result
    def report_add(self,uuid,result,fail_log=None,log=""):
        fail_log = "Fail Log is not set." if not fail_log else fail_log
        name = basename(inspect.stack()[1].filename).replace(".py","") # replace better than [:-3]
        finalLog = "{} {} {}".format("" if result else str(fail_log),self.wrapper_fail_log,log)
        if self.wrapper_fail_log:
            self.wrapper_fail_log = ""            # reset wrapper fail log
        self.myReport.add_result(uuid,result,name,finalLog)
        return self
    def report_set_title(self,title):
        logger(f"report = {self.myReport}")
        self.myReport.add_ovinfo("title",title)
        return self
    def report_set_duration(self,duration):
        temp , sec = divmod(int(duration),60)
        hour , min = divmod(temp,60)
        self.myReport.add_ovinfo("duration", "{}:{:0>2d}:{:0>2d}".format(hour,min,sec))
        return self
    def report_set_browser(self,browser):
        self.myReport.add_ovinfo("browser",browser)
        return self
    def report_set_browser_version(self,version):
        self.myReport.add_ovinfo("version",version)
        return self
    def report_export(self):
        self.report_set_duration(time.time()-self.startTime)
        self.myReport.export().show()
        return self
    def report_title(self,title):
        self.myReport.add_ovinfo("title",title)
        return self
    def report_send_email(self,*augs):
        self.myReport.send_mail(*augs)
        return self
    def printValues(self,el):
        objs = self.find(el)
        for obj in objs:
            print (obj.text)
    def printObjs(self,el):
        el = el[0]
        print (super().find_elements(el['by'],el['value']))
    def object_exist(self,el,timeout=None):
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
        while (time.time()-oldTime < timeout):
            if result:
                break
            result = self.find(el)
        self.implicitly_wait(self.getimplicitlyWait())
        self.wrapper_last_result=True if result else False
        return True if result else False
    def object_not_exist(self,el,timeout=None):
        if timeout is None:
            timeout = self.implicitlyWait
        oldTime = time.time()
        ret = False
        while (time.time()-oldTime < timeout):
            self.implicitly_wait(0.5)
            result = self.find(el)
            if result is None:
                ret = True
                break
        self.implicitly_wait(self.getimplicitlyWait())
        self.wrapper_last_result= ret
        return ret
    def setimplicitlyWait(self,sec):
        self.implicitlyWait = sec
    def getimplicitlyWait(self):
        return self.implicitlyWait
    def clipboard_include(self,text):
        root = Tk()
        root.withdraw()
        textClipboard = root.clipboard_get()
        #print ("clipboard => " + textClipboard)
        return text in textClipboard
    def text_wait(self,text,timeout=None):
        if timeout is None:
            timeout = self.implicitlyWait
        oldTime = time.time()
        ret = False
        result = None
        while (time.time()-oldTime < timeout):
            self.implicitly_wait(0.5)
            try:
                result = super().find_element_by_xpath("//*[contains(text(),'" + text + "')]")
            except:
                pass
            if result is not None:
                ret = True
                break
        self.implicitly_wait(self.getimplicitlyWait())
        print (ret)
        self.wrapper_last_result= ret
        return ret
    def clear_local_storage(self):
        # super().execute(Command.CLEAR_LOCAL_STORAGE)
        super().execute_script('localStorage.clear();')
        return
    def css(self,css):
        return ("css selector", css)
        
    def xpath(self,xpath):
        return ("xpath", xpath)
        
    def el(self,locator):
        return self.find_element_by_css_selector(locator)
        
    def els(self,locator):
        return self.find_elements_by_css_selector(locator)
        
    def el_xpath(self,locator):
        return self.find_element_by_xpath(locator)
        
    def exist(self,locator,timeout=10):
        locator_css = self.css(locator)
        self.implicitly_wait(0.1)
        wait = WebDriverWait(self, timeout)
        timer_start = time.time()
        elem = None
        while (timer := time.time() - timer_start) < timeout:
            try:
                elem = wait.until(EC.presence_of_element_located(locator_css), "Locator still not exist: " + str(locator_css))
                # logger("[is_exist] found:" + str(time.time() - timer_start))
                break
            except:
                if timer != timer : logger("[is_exist] Not found:" + str(time.time() - timer_start))
        self.implicitly_wait(self.getimplicitlyWait())
        return elem
        
        
    def not_exist(self,locator,timeout=10):
        locator_css = self.css(locator)
        implicitly = self.getimplicitlyWait()
        self.implicitly_wait(0.1)
        wait = WebDriverWait(self, timeout)
        timer_start = time.time()
        result = False
        while time.time() - timer_start < timeout:
            try:
                elem = wait.until_not(EC.presence_of_element_located(locator_css), "Locator still exist: " + str(locator_css))
                result = True
                # logger("[is_not_exist] Vanished:" + str(time.time() - timer_start))
                break
            except Exception as e:
                # logger(f"{e=}")
                # logger("is_not_exist] not Vanished:" + str(time.time() - timer_start))
                ...
        self.implicitly_wait(implicitly)
        return result
        
    def is_exist(self,*aug,**kwaug):
        return bool(self.exist(*aug,**kwaug))
        
    def is_not_exist(self,*aug,**kwaug):
        return bool(self.not_exist(*aug,**kwaug))
        
    def exist_click(self,locator,timeout=10):
        if item := self.exist(locator,timeout):
            retry = 4
            while retry := retry -1:
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
        
    def select(self,locator,index=0):
        try:
            s = Select(self.el(locator))
            s.select_by_index(index)
            return True
        except:
            return False
            
    def new_tab(self):
        self.execute_script("window.open('');")
        self.switch_to.window(self.window_handles[-1])




class MyIe(MyClass,Ie):
    pass

class MyFirefox(MyClass,Firefox):
    pass

class MyChrome(MyClass,Chrome):
    pass

class MyRemote(MyClass,webdriver.Remote):
    pass
    
    
    


