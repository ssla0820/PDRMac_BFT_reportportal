import os
import subprocess
import re
import webbrowser
import datetime
import platform
import inspect
import time
import traceback
from datetime import timedelta
import base64
from contextlib import contextmanager

from .sendemail import send_mail as sendMail
from ..log import logger

class MyReport(object):
    uuid_queue = set()
    
    def __init__(self,udid = None,driver = None, html_name=None):
        self.driver = driver
        self.udid = udid or "unknown_device"
        self.html_name = html_name
        self.set_path(self.html_name)
        
        # report data
        self.body = self.read("body.rep")
        self.css = self.read("sheet.rep")
        self.js = self.read("script.rep")
        self.replace_bft = self.read("rep_bft.rep")
        self.replace_bft2 = self.read("rep_bft2.rep")
        if self.html_name is None:
            self.bft = self.read_custom("SFT.html")
        else:
            self.bft = self.read_custom(html_name)
        self.ov = self.read_custom("ov.rep")
        self.cssDownload = self.read_custom("sheet.css")

        self.start_time = time.time()
        
        self.fail_number = 0
        now = datetime.datetime.now()
        self.ovInfo = {
            "title" : "",
            "date" : now.date().strftime("%Y-%m-%d"),
            "time" : now.time().strftime("%H:%M:%S"),
            "server" : os.getenv('COMPUTERNAME', "Windows" if platform.system() == "Windows" else "Mac OS"),
            "os" : "driver.capabilities['os']",
            "device" : "driver.capabilities['device']",
            "version" : "driver.capabilities['version']",
            "pass" : 0,
            "fail" : 0,
            "_fail" : 0,
            "na" : 0,
            "skip" : 0,
            "duration" : "00:00:00"
            }
        self.passNumber = 0
        self.failNumber = 0
        self.pic_index = 0
        self.start_recording_flag = 0
        self.is_recording_enabled = 0
    def set_path(self, html_name=None):
        # data path
        self.source_path = os.path.dirname(inspect.stack()[2].filename)
        # self.source_path =os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.base_path = os.path.dirname(__file__)
        self.sub_folder = self.source_path + "/check_list/"
        # report path
        self.output_path = self.source_path + "/report/" + self.udid
        self.output_file = self.output_path + "/SFT_Report.html"
        if self.html_name is None:
            self.output_file = self.output_path +"/SFT_Report.html"
        else:
            self.output_file = self.output_path + f'/{self.html_name.split(".")[0]}_Report.html'

    def set_driver(self,driver):
        self.driver =driver
    def add_driver(self,driver):
        if not isinstance(driver,list):
            driver = [driver]
        if not isinstance(self.driver,list):
            self.driver = [self.driver]
            # self.driver.remove(None)
        self.driver.extend(driver)
    def del_driver(self,driver):
        if not isinstance(driver,list):
            driver = [driver]
        for item in driver:
            try:
                self.driver.remove(item)
            except:
                ...
    def set_udid(self,udid):
        self.udid = udid
        self.set_path()
    def set_enable_recording(self):
        self.is_recording_enabled = 1
    def start_uuid(self,uuid):
        # checking format
        pattern_uuid = r"(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})"
        if not re.match(pattern_uuid,uuid):
            logger("[Error] Input uuid is incorrect: %s" % str(uuid) )
            return
        if uuid in self.uuid_queue:
            logger(f"[Warning] Duplicate UUID found. {uuid}")
        self.uuid_queue.add(uuid)
        try:
            if self.is_recording_enabled == 1 and self.start_recording_flag == 0:
                self.driver.start_recording_screen()
                self.start_recording_flag = 1
        except Exception as e:
            logger(f'Exception occurs. log={e}')
    def add_result(self, id, result, name, log="",fail_screenshot= True):
        if fail_screenshot: # dont show log if call from export()
            logger("Add Result = %s / %s / %s / %s" % (id,result,name,log))
        #remove from uuid_queue
        if id not in self.uuid_queue:
            logger("[Warning] UUID is not in running list. Do you forget start_uuid(%s)?" % id)
        else:
            self.uuid_queue.remove(id)
        if result == False and self.driver and fail_screenshot: # only screenshot if result == false and has self.driver (set_driver())
            if not isinstance(self.driver,list):
                self.driver = [self.driver]
                try:
                    self.driver.remove(None)
                except:
                    ...
            os.makedirs(self.source_path + "/report/" + self.udid, exist_ok=True)
            self.pic_index += 1
            name = name.replace("<","").replace(">","")
            for i,item in enumerate(self.driver):
                file_name = "%s_%s_%s.png" % (str(self.pic_index),name,i)
                log = "%s / %s" % ( file_name, log)
                file_path = "%s/%s" % (self.output_path, file_name)
                logger(f'Fail screenshot = {file_path}')
                logger(f'{item=}')
                item.get_screenshot_as_file(file_path)

            # stop recording and save file if result is False (by Jim) ===========
            if self.start_recording_flag == 1:
                base64_data = self.driver.stop_recording_screen()
                file_name_record_video = file_name.replace('png', 'mp4')
                file_path_record_video = "%s/%s" % (self.output_path, file_name_record_video)
                fh = open(file_path_record_video, "wb")
                fh.write(base64.b64decode(base64_data))
                fh.close()
                self.start_recording_flag = 0 # turn off the flag
                logger(f"Fail recording video: {file_name.replace('png', 'mp4')}")
                # update mediastore (for recording tmp file) [Android]
                cmd = f'adb -s {self.udid} shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///storage///emulated///0///'
                self.shell(cmd)
        else: # stop recording and no save file (by Jim)
            if self.start_recording_flag == 1:
                self.driver.stop_recording_screen()
                self.start_recording_flag = 0  # turn off the flag
                # update mediastore (for recording tmp file) [Android]
                cmd = f'adb -s {self.udid} shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///storage///emulated///0///'
                self.shell(cmd)

        # print ("args=", id,result, name, log)
        myPass = '<span id="myPass">Pass</span>'
        myFail = '<span id="myFail">Fail</span>'
        myBypass = '<span id="myNA">N/A</span>'
        # self.bft = self.bft.replace("&lt;" + id + "&gt;", myPass if result else myFail,1)
        p=r'<td class="(s\d+)"([^>]*?)>([^<]*)<\/td><td class="(s\d+)"([^>]*?)>('+id+r')\W*?<\/td>\W*<td class="(s\d+)"([^>]*?)>([^<>]*)<\/td>\W*<td class="(s\d+)"><\/td>'
        self.bft = re.sub( p , \
            r'<td class="\1"\2>{0}</td><td class="\4"\5>{1}</td><td class="\7"\8>{2}</td><td class="\10"></td>' \
            .format(name,myPass if result else myFail if result == False else myBypass ,log),self.bft,1)
            #(myPass if result else myFail)+r'<\/td><td class="\2">'+log+r'<\/td><td class="\4"><\/td>',self.bft,1)
        if result:
            self.ovInfo["pass"] += 1
        elif result == None:
            self.ovInfo['na'] += 1
        elif result == False:
            self.ovInfo["fail"] += 1
            logger(f'[Fail] ID = {id} , Screenshot = {fail_screenshot} , fail number = {self.ovInfo["fail"]}')
        return self
    def new_result(self,id,result,fail_log=None,log="",fail_screenshot= True, case_name = None):
        fail_log = "Fail Log is not set." if not fail_log else fail_log
        name = case_name or os.path.basename(inspect.stack()[1].function).replace("test_","") # remove extra strings
        if not result:
            log = "%s %s" % (str(fail_log),log)
        self.add_result(id,result,name,log,fail_screenshot)
    def add_ovinfo(self, key, value = ""):
        if  type(key) is dict:
            for x,y in key.items():
                self.ovInfo[x] = y
        else:
            self.ovInfo[key] = value
        return self
    def get_ovinfo(self, key):
        return self.ovInfo[key]
    def export(self,output_file = None):
        report_elapsed_time = int(time.time() - self.start_time)
        if output_file:
            self.output_file = output_file
        def repl(matchObj=None):
            try:
                repl.count += 1
            except:
                repl.count = 1
            return '<span id="mySkip">Skip</span>'
        #exist uuid change result to fail
        for uuid in self.uuid_queue.copy():
            self.new_result(uuid,False,"Exception",fail_screenshot=False)
        # self.bft = re.sub("(&lt;\d+\.+\d+\.+\d+\.+\d+\.+\d+\.+\d+&gt;)",mySkip,self.bft)
        repl.count = 0  # it won't intial if no skip case
        self.bft = re.sub(r"(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})",repl,self.bft)
        self.ovInfo["skip"] = repl.count
        self.ovInfo["duration"] = str(timedelta(seconds=report_elapsed_time))
        # output summary.txt
        os.makedirs(self.source_path + "/report/" + self.udid, exist_ok=True)
        with open(os.path.join(os.path.dirname(self.output_file), "summary.txt"), 'w') as data:
            data.write(str(self.ovInfo))
        if self.ovInfo["fail"]: 
            self.ovInfo["_fail"] = self.ovInfo["fail"]
            self.fail_number = self.ovInfo["fail"]
            self.ovInfo["fail"] = '<font color="red"><b>{}</b></font>'.format(self.ovInfo["fail"])
        self.bft = self.bft.replace("</style>",self.replace_bft)
        self.bft = self.bft.replace('<table class="waffle"',self.replace_bft2)
        self.body = self.body.replace("this_is_bft",self.bft)       # switch tab style
        for x,y in self.ovInfo.items():
            self.ov = self.ov.replace("#" + x + "#", str(y))
        self.body = self.body.replace("this_is_overview",self.ov)   # switch tab style
        self.body = self.ov + self.bft                              # all in one style
        # self.css = self.css.replace("this_is_css",self.cssDownload) #merge to below write
        self.html_final = self.css.replace("this_is_css",self.cssDownload)+self.body+self.js
        with open(self.output_file,"w") as f:
            f.write(self.html_final)
        return self
    def show(self):
        
        
        if platform.system() == "Windows":
            win_chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
            webbrowser.get(win_chrome_path).open(self.output_file)
        elif platform.system() == "Darwin":
            # Not working
            # mac_chrome_path = '/Applications/Google\ Chrome.app %s'
            webbrowser.open('file://' + self.output_file)
        else:
            return self
        return self
    def read(self,filename):
        with open(self.base_path+"/"+filename,"r",encoding="utf-8") as f:
            return f.read()
    def read_custom(self,filename):
        with open(self.source_path+"/check_list/"+filename,"r",encoding="utf-8") as f:
            return f.read()
    def send_mail(self,acc,pw,displayName,emailTo):
        if not isinstance(emailTo, (list,tuple)):
            print ("emailTo should be dictionary.")
            return False
        result = "PASS" if self.ovInfo["fail"] == 0 else str(self.fail_number)+ " FAIL"
        opts = {
            "account": acc
            ,"password": pw #"6uWHKTZpUK6Fmgm"
            ,"from": displayName+" <clsignupstress@gmail.com>"
            ,"to": emailTo
            ,"subject": "[UWeb AT] Report <{}> {} {}".format(result,self.ovInfo["date"],self.ovInfo["time"])
            ,"text": "this is UWeb BFT report"
            ,"html": self.css+self.ov
            ,"attachment": self.html_final
        }
        sendMail(opts)
        
    def exception_screenshot(self,func):
        def wrapper(*aug):
            try:
                return func(*aug)
            except Exception as e:
                file_full_path = self.output_path + "/[Exception]" + func.__name__ + ".png"
                os.makedirs(self.source_path + "/report/" + self.udid, exist_ok=True)
                self.driver.get_screenshot_as_file(file_full_path)
                logger("Exception screenshot: %s" % file_full_path)
                logger("Exception: %s" % str(e))
                logger(f"code: {traceback.format_exc()}")
                # stop recording screen and save file
                if self.start_recording_flag == 1:
                    base64_data = self.driver.stop_recording_screen()
                    file_path_record_video = self.output_path + "/[Exception]" + func.__name__ + ".mp4"
                    fh = open(file_path_record_video, "wb")
                    fh.write(base64.b64decode(base64_data))
                    fh.close()
                    self.start_recording_flag = 0  # turn off the flag
                    logger("Exception recording video: %s" % file_path_record_video)
                    # update mediastore (for recording tmp file)
                    cmd = f'adb -s {self.udid} shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///storage///emulated///0///'
                    self.shell(cmd)
                raise
        return wrapper
    
    @contextmanager
    def uuid(self,uuid):
        '''
            multiple uuid: ["xxx-xx-xx-xx","xxx-xxx-xx-xx"]
        '''
        uuids = uuid if isinstance(uuid, (list, tuple)) else [uuid]
        for _uuid in uuids:
            self.start_uuid(uuid)
        self.result = None
        self.fail_log = ""
        yield self
        try:
            name = os.path.basename(inspect.stack()[2].function).replace("test_","")
            for _uuid in uuids:
                self.new_result(_uuid,self.result,fail_log=self.fail_log,case_name = name)
        except:
            logger(f"[ERROR] no result is set! {uuids=}")
    
    def shell(self,command):    # return Ture/False
        import subprocess
        try:
            if not "adb -s " in command: command = command.replace("adb","adb -s %s " % self.udid)
            logger("shell: %s" % command)
            subprocess.call(command)
            return True
        except Exception as e:
            logger("shell fail : %s" % str(e))
            return False
        
