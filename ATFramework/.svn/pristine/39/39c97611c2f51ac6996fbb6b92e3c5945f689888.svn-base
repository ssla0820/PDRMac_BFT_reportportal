import time
from .. import initial_chrome
# from .. import common, department
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium import webdriver
class Base():
    def __init__(self,driver):
        self.act = ActionChains(driver)
        self._close = driver.close
        self.__class__ = type('_Base',(self.__class__,driver.__class__),driver.__dict__.copy())
        
    def close(self):
        print("close driver!")
        if self.option.get("report",None):
            self.option['report'].del_driver(self)
        self._close()
        
    def login(self,account,is_prod=False):
        self.get(f"https://{'u' if is_prod else 'u-demo'}.cyberlink.com/user/signin")
        self.el('input[name="plemail"]').clear()
        self.el('input[name="plemail"]').send_keys(account['name'])
        self.el('input[name="plpassword"]').send_keys(account['password'])
        self.el('span.submit-text.ng-scope').click()
        return self.is_exist('#signout')
        
    def enter_meeting(self,meeting_id,name="Chrome AT",e2ee=False,block=False):
        self.get(f'https://u-demo.cyberlink.com/meeting/{meeting_id}')
        self.el('a[href="#join"]').click()
        try:
            self.el(".name>input").clear()
            self.el(".name>input").send_keys(name)
            self.el(".btn-link").click()
        except:
            pass
        if e2ee:
            return self.is_exist('.not-support',10)
        if block:
            return not self.is_exist("#hangup-btn",10)
        
        return self.is_exist("#hangup-btn",5)
    
    def right_click(self,locator,xoffset=None,yoffset=None):
        self.mouse_move(locator,xoffset,yoffset)
        self.act.w3c_actions.pointer_action.context_click()
        self.act.w3c_actions.perform()
        self.act.w3c_actions.devices[0].clear_actions()
        
    def mouse_move(self,locator,xoffset=None,yoffset=None):
        elem = self.el(locator)
        h,w,x,y = elem.rect.values()
        xoffset = xoffset or int(w/2)
        yoffset = yoffset or int(h/2)
        self.act.move_to_element_with_offset(elem,xoffset,yoffset)
        self.act.w3c_actions.perform()
        self.act.w3c_actions.devices[0].clear_actions()
        
    def center(self,locator):
        elem = self.el(locator)
        h,w,x,y = elem.rect.values()
        return (int(x+w/2),int(y+w/2))
        
    def mute(self,mute=True):
        speaker = self.el('#volume-btn.volume-btn')
        if ("mute-btn" in speaker.get_attribute('class')) != mute:
            speaker.click()
    
    def unmute(self,unmute=True):
        self.mute(not unmute)
        
    def stop_share_desktop(self):
        self.execute_script('localStream.cancelDesktopSharing()')
        
        
class Main(Base):
    def __init__(self,*aug):
        super().__init__(*aug)
    def click_enter_meeting(self):
        self.el('a[href="#join"]').click()
        
    def set_name(self,name):
        self.el(".name>input").clear()
        self.el(".name>input").send_keys(name)
        
    def click_join(self):
        self.el(".btn-link").click()
        
class Meeting(Base):
    def __init__(self,*aug):
        super().__init__(*aug)
        
class Host(Base):
    def __init__(self,option,account=None,fake=True,options = None, case=None):
        if case:
            (option := option.copy()).update({'webAddress':None})
        options = options or get_options(case)
        driver = initial_chrome(option,fake_media=fake,options = options)
        super().__init__(driver)
        # print(f'{self.__class__=}\n{driver.__class__=}\n{driver=}\n{driver.__dict__=}')
        self.__class__ = type('_Host',(self.__class__,driver.__class__),driver.__dict__.copy())
        self._close = driver.close
        self.option = option
        if r:=option.get('report',None):
            r.add_driver(self)
        if account: 
            print("== login ==")
            self.login(account,is_prod=option['is_prod'])
        if option['webAddress']: self.get(option['webAddress'])
        
        
class Participant(Base):
    def __init__(self,option,account=None,fake=True,options = None, case=None):
        option['report_title'] = "NA"
        option['participant'] = True
        if case:
            (option := option.copy()).update({'webAddress':None})
        options = options or get_options(case)
        driver = initial_chrome(option,fake_media=fake,options = options)
        super().__init__(driver)
        self.__class__ = type('_Participant',(self.__class__,driver.__class__),driver.__dict__.copy())
        self._close = driver.close
        self.option = option
        if r:=option.get('report',None):
            r.add_driver(self)
        if account: self.login(account,is_prod=option['is_prod'])
        if option['webAddress']: self.get(option['webAddress'])
        self.enter_meeting(option['meeting_id'])
    
    
            


'''
if elem := is_ready('//*[@id="hangup-btn"]'):
    print (f"In meeting room now, wait {wait_in_meeting} sec")
    time.sleep(wait_in_meeting)
    s("#hangup-btn").click()
    s(".modal-button.remove-button").click()
    print (f"End meeting, wait {wait_when_end} sec")
    time.sleep(wait_when_end)
'''

'''
types.MethodType( barFighters, a )
'''

def get_options(type=None):
    options = webdriver.ChromeOptions()
    options.add_argument("--lang=en-us")
    options.add_argument("--window-size=1280,800")
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    options.add_argument('log-level=3')
    
    if type == "camera_permission":
        options.add_argument("use-fake-device-for-media-stream")
        prefs = {
            "hardware.audio_capture_allowed_urls" : ['u.cyberlink.com','u-demo.cyberlink.com'],
            "protocol_handler": {
                "allowed_origin_protocol_pairs" : {
                    'https://u.cyberlink.com':{'cyberlinku': True},
                    'https://u-demo.cyberlink.com':{'cyberlinkubeta': True},
                    }
                }
            }
        options.add_experimental_option('prefs',prefs)
    
    elif type == "microphone_permission":
        options.add_argument("use-fake-device-for-media-stream")
        prefs = {
            "hardware.audio_capture_allowed_urls" : ['u.cyberlink.com','u-demo.cyberlink.com'],
            "protocol_handler": {
                "allowed_origin_protocol_pairs" : {
                    'https://u.cyberlink.com':{'cyberlinku': True},
                    'https://u-demo.cyberlink.com':{'cyberlinkubeta': True},
                    }
                }
            }
        options.add_experimental_option('prefs',prefs)
    
    elif type == "block_media":
        # print("block_media")
        options.add_argument("use-fake-device-for-media-stream")
        options.add_argument("--disable-infobars")
        prefs = {
            "profile.managed_default_content_settings.media_stream":2,
            "protocol_handler": {
                "allowed_origin_protocol_pairs" : {
                    'https://u.cyberlink.com':{'cyberlinku': True},
                    'https://u-demo.cyberlink.com':{'cyberlinkubeta': True},
                    }
                }
            }
        # prefs = {
         # "profile.managed_default_content_settings.images":2,
         # "profile.default_content_setting_values.notifications":2,
         # "profile.managed_default_content_settings.stylesheets":2,
         # "profile.managed_default_content_settings.cookies":2,
         # "profile.managed_default_content_settings.javascript":1,
         # "profile.managed_default_content_settings.plugins":1,
         # "profile.managed_default_content_settings.popups":2,
         # "profile.managed_default_content_settings.geolocation":2,
         # "profile.managed_default_content_settings.media_stream":2,
         # }
        options.add_experimental_option('prefs',prefs)
    
    elif type == "allow_media":
        # print("allow_media")
        options.add_argument("use-fake-device-for-media-stream")
        options.add_argument("--disable-infobars")
        prefs = {
            "profile.managed_default_content_settings.media_stream":1,
            "protocol_handler": {
                "allowed_origin_protocol_pairs" : {
                    'https://u.cyberlink.com':{'cyberlinku': True},
                    'https://u-demo.cyberlink.com':{'cyberlinkubeta': True},
                    }
                }
            }
        options.add_experimental_option('prefs',prefs)
        
    elif type == "block_camera":
        options.add_argument("use-fake-device-for-media-stream")
        prefs = {
            "hardware.audio_capture_allowed_urls" : ['u.cyberlink.com','u-demo.cyberlink.com'],
            "profile.managed_default_content_settings.media_stream":2,
            "protocol_handler": {
                "allowed_origin_protocol_pairs" : {
                    'https://u.cyberlink.com':{'cyberlinku': True},
                    'https://u-demo.cyberlink.com':{'cyberlinkubeta': True},
                    }
                }
            }
        options.add_experimental_option('prefs',prefs)
        
    elif type == "block_microphone":
        options.add_argument("use-fake-device-for-media-stream")
        prefs = {
            "hardware.video_capture_allowed_urls" : ['u.cyberlink.com','u-demo.cyberlink.com'],
            "profile.managed_default_content_settings.media_stream":2,
            "protocol_handler": {
                "allowed_origin_protocol_pairs" : {
                    'https://u.cyberlink.com':{'cyberlinku': True},
                    'https://u-demo.cyberlink.com':{'cyberlinkubeta': True},
                    }
                }
            }
        options.add_experimental_option('prefs',prefs)
    elif type == "true_media":
        # options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-certificate-errors-spki-list')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument("-test-type")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_argument("--window-position=0,0")
        
        # options.add_argument("use-fake-ui-for-media-stream")
        # options.add_argument("use-fake-device-for-media-stream")
        prefs = {
            "hardware.audio_capture_allowed_urls" : ['u.cyberlink.com','u-demo.cyberlink.com'],
            "hardware.video_capture_allowed_urls" : ['u.cyberlink.com','u-demo.cyberlink.com'],
            'profile.default_content_setting_values' :  {  
                'notifications' : 1  
            },  
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": False,
            "credentials_enable_service": False,
            "protocol_handler": {
                "allowed_origin_protocol_pairs" : {
                    'https://u.cyberlink.com':{'cyberlinku': True},
                    'https://u-demo.cyberlink.com':{'cyberlinkubeta': True},
                }
            }
        }    
        options.add_experimental_option('prefs',prefs)
        # options.add_experimental_option("excludeSwitches", ['enable-automation',"enable-logging"])
        # options.add_experimental_option("excludeSwitches", ["enable-logging"])
        #options.add_argument("--headless")
        
    elif type == "share_dt":
        print("share_dt")
        options.add_argument("use-fake-device-for-media-stream")
        options.add_argument('--auto-select-desktop-capture-source=Screen 1')
        options.add_argument("use-fake-ui-for-media-stream")
        prefs = {
            "hardware.audio_capture_allowed_urls" : ['u.cyberlink.com','u-demo.cyberlink.com'],
            "hardware.video_capture_allowed_urls" : ['u.cyberlink.com','u-demo.cyberlink.com'],
            "profile.password_manager_enabled": False,
            "credentials_enable_service": False,
            "protocol_handler": {
                "allowed_origin_protocol_pairs" : {
                    'https://u.cyberlink.com':{'cyberlinku': True},
                    'https://u-demo.cyberlink.com':{'cyberlinkubeta': True},
                }
            }
        }
        options.add_experimental_option('prefs',prefs)
    else:
        # options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-certificate-errors-spki-list')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument("-test-type")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_argument("--window-position=0,0")
        
        options.add_argument("use-fake-ui-for-media-stream")
        options.add_argument("use-fake-device-for-media-stream")
        prefs = {
            "hardware.audio_capture_allowed_urls" : ['u.cyberlink.com','u-demo.cyberlink.com'],
            "hardware.video_capture_allowed_urls" : ['u.cyberlink.com','u-demo.cyberlink.com'],
            'profile.default_content_setting_values' :  {  
                'notifications' : 1  
            },  
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": False,
            "credentials_enable_service": False,
            "protocol_handler": {
                "allowed_origin_protocol_pairs" : {
                    'https://u.cyberlink.com':{'cyberlinku': True},
                    'https://u-demo.cyberlink.com':{'cyberlinkubeta': True},
                }
            }
        }    
        options.add_experimental_option('prefs',prefs)
        # options.add_experimental_option("excludeSwitches", ['enable-automation',"enable-logging"])
        # options.add_experimental_option("excludeSwitches", ['enable-automation'])
        # options.add_argument('log-level=3')
# options.add_experimental_option("excludeSwitches", ["enable-logging"])
        #options.add_argument("--headless")
    return options