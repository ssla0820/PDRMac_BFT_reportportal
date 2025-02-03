import functools
import os
import subprocess
import re
import sys
import traceback
import webbrowser
import datetime
import platform
import inspect
import time
from datetime import timedelta
from contextlib import contextmanager
import base64
try:
    import cv2
    import numpy as np
except:
    cv2 = type('cv2', (object,), {"INTER_CUBIC":None})()

from .sendemail import send_mail as sendMail
from ..log import logger

class MyReport(object):
    uuid_queue = set()

    def __init__(self,udid = None,driver = None, html_name=None, log_cpu_memory=True):
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
        self.report_type = "Default"

        self.uuid_performance = {}
        self.log_cpu_memory=log_cpu_memory # Currently, for macOS only (2022/05/10)

    def set_path(self, html_name=None):
        # data path
        self.source_path = os.path.dirname(inspect.stack()[2].filename)
        # self.source_path =os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.base_path = os.path.dirname(__file__)
        self.sub_folder = self.source_path + "/check_list/"
        # report path
        self.output_path = self.source_path + "/report/" + self.udid
        if type(self.udid) is list: # for multi-devices
            self.output_path = self.source_path + "/report/" + self.udid[0]
        else:
            self.output_path = self.source_path + "/report/" + self.udid
        self.output_file = self.output_path + "/SFT_Report.html"
        self.csv_file = self.output_path + "/performance.csv"
        if self.html_name is None:
            self.output_file = self.output_path +"/SFT_Report.html"
        else:
            self.output_file = self.output_path + f'/{self.html_name.split(".")[0]}_Report.html'

    def set_driver(self,driver):
        # for multi-devices
        if type(driver) is list:
            self.driver = []
            for index in range(len(driver)):
                self.driver.append(driver[index].driver)
        else:
            try:
                self.driver = driver.driver
            except:
                self.driver = driver

    def get_driver(self, index = None):
        ret = self.driver if isinstance(self.driver, list) else [self.driver]
        return ret if index is None else ret[index]

    def add_driver(self,driver):
        if not isinstance(driver,list):
            driver = [driver]
        if not isinstance(self.driver,list):
            self.driver = [self.driver]
            self.driver.remove(None)
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
        if platform.system() == 'Darwin' and self.log_cpu_memory:
            self.uuid_performance.update({uuid: {"start": {"cpu": self.get_driver(0).cpu, "ram": self.get_driver(0).ram}}})
        try:
            if self.is_recording_enabled == 1 and self.start_recording_flag == 0:
                if type(self.driver) is list:
                    for index in range(len(self.driver)):
                        if hasattr(self.driver[index], "start_recording_screen"):
                            self.driver[index].start_recording_screen()
                else:
                    if hasattr(self.driver, "start_recording_screen"):
                        self.driver.start_recording_screen()
                self.start_recording_flag = 1
        except Exception as e:
            logger(f'Exception occurs. log={e}')
    def add_result(self, id, result, name, log="",fail_screenshot= True, level=2):
        if fail_screenshot: # dont show log if call from export()
            logger("Add Result = %s / %s / %s / %s" % (id,result,name,log), level=level)
        #remove from uuid_queue
        if id not in self.uuid_queue:
            logger("[Warning] UUID is not in running list. Do you forget start_uuid(%s)?" % id, level=level)
        else:
            self.uuid_queue.remove(id)
            if platform.system() == 'Darwin' and self.log_cpu_memory:
                self.uuid_performance[id].update({"end": {"cpu": self.get_driver(0).cpu, "ram": self.get_driver(0).ram}})
                s_cpu ,s_ram  = self.uuid_performance[id]["start"]["cpu"], self.uuid_performance[id]["start"]["ram"]
                e_cpu, e_ram = self.uuid_performance[id]["end"]["cpu"], self.uuid_performance[id]["end"]["ram"]

                if -1 in [ s_cpu, s_ram, e_cpu, e_ram]:
                    self.uuid_performance[id].update({"diff": {"cpu": "N/A", "ram": "N/A"}})
                else:
                    self.uuid_performance[id].update({"diff": {
                        "cpu": float(e_cpu) - float(s_cpu),
                        "ram": float(e_ram) - float(s_ram)}})
        if result == False and self.driver and fail_screenshot: # only screenshot if result == false and has self.driver (set_driver())
            if not isinstance(self.driver,list):
                self.driver = [self.driver]
                # self.driver.remove(None)
            os.makedirs(self.source_path + "/report/" + self.udid, exist_ok=True)
            self.pic_index += 1
            name = name.replace("<","").replace(">","")
            for i,item in enumerate(self.driver):
                if len(self.driver) == 1:
                    file_name = "%s_%s.png" % (str(self.pic_index), name)
                else:
                    file_name = "%s_%s_%s.png" % (str(self.pic_index),name,i)
                log = "%s / %s" % ( file_name, log)
                logger(f'Fail screenshot = {file_name}', level=level)
                file_path = "%s/%s" % (self.output_path, file_name)
                self.driver[0].get_screenshot_as_file(file_path)
        # print ("args=", id,result, name, log)
        myPass = '<span id="myPass">Pass</span>'
        myFail = '<span id="myFail">Fail</span>'
        myBypass = '<span id="myNA">N/A</span>'
        # self.bft = self.bft.replace("&lt;" + id + "&gt;", myPass if result else myFail,1)
        p=r'<td class="(s\d+)"([^>]*?)>([^<]*)<\/td><td class="(s\d+)"([^>]*?)>('+id+r')\W*?<\/td>\W*<td class="(s\d+)"([^>]*?)>([^<>]*)<\/td>\W*<td class="(s\d+)"([^>]*?)><\/td>'
        self.bft = re.sub( p , \
            r'<td class="\1"\2>{0}</td><td class="\4"\5>{1}</td><td class="\7"\8>{2}</td><td class="\10"\11></td>' \
            .format(name,myPass if result else myFail if result == False else myBypass ,log),self.bft,1)
            #(myPass if result else myFail)+r'<\/td><td class="\2">'+log+r'<\/td><td class="\4"><\/td>',self.bft,1)
        if result:
            self.ovInfo["pass"] += 1
        elif result == None:
            self.ovInfo['na'] += 1
        elif result == False:
            self.ovInfo["fail"] += 1
            logger(f'[Fail] ID = {id} , Screenshot = {fail_screenshot} , fail number = {self.ovInfo["fail"]}', level=level)
        return self
    def new_result(self,id,result,fail_log=None,log="",fail_screenshot= True, case_name = None, level=3):
        fail_log = "Fail Log is not set." if not fail_log else fail_log
        name = case_name or os.path.basename(inspect.stack()[1].function).replace("test_","") # remove extra strings
        if not result:
            log = "%s %s" % (str(fail_log),log)
        self.add_result(id,result,name,log,fail_screenshot, level=level)
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
            self.new_result(uuid,False,"Exception", fail_screenshot=False,case_name= "unknown")
        # self.bft = re.sub("(&lt;\d+\.+\d+\.+\d+\.+\d+\.+\d+\.+\d+&gt;)",mySkip,self.bft)
        repl.count = 0  # it won't intial if no skip case
        self.bft = re.sub(r"(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})",repl,self.bft)
        self.ovInfo["skip"] = repl.count
        self.ovInfo["duration"] = str(timedelta(seconds=report_elapsed_time))
        # output summary.txt
        if type(self.udid) == list:
            os.makedirs(self.source_path + "/report/" + self.udid[0], exist_ok=True)
        else:
            os.makedirs(self.source_path + "/report/" + self.udid, exist_ok=True)
        with open(os.path.join(os.path.dirname(self.output_file), "summary.txt"), 'w',encoding='utf-8') as data:
            data.write(str(self.ovInfo))
        self.ovInfo['fail_number'] = self.ovInfo["fail"]
        if self.ovInfo["fail"]:
            self.fail_number = self.ovInfo["fail"]
            self.ovInfo["_fail"] = self.ovInfo["fail"]
            self.ovInfo["fail_number"] = self.ovInfo["fail"]
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

        with open(self.output_file, "w",encoding='utf-8') as f:
            f.write(self.html_final)
        if platform.system() == 'Darwin' and self.log_cpu_memory:
            # with open(self.output_file,"w") as f, open(self.csv_file, "a") as csv:
            with open(self.csv_file, "a") as csv:
                # f.write(self.html_final)
                csv_data = [f'''{self.html_name.split(".")[0]}{f",'{'=' * 10}" * 6}\n''']   # Split by page name
                csv_data += [f"{k},{v['diff']['cpu']},{v['diff']['ram']},"
                             f"{v['start']['cpu']},{v['start']['ram']},"
                             f"{v['end']['cpu']},{v['end']['ram']}\n" for k,v in self.uuid_performance.items()]
                logger(f"{csv_data=}")
                csv.writelines(csv_data)
        return self

    def show(self):
        if platform.system() == "Windows":
            # win_chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
            # webbrowser.get(win_chrome_path).open(self.output_file)
            # 04/27/2022: Chrome path is changed, use default browser to open file
            webbrowser.open(self.output_file)
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
        @functools.wraps(func)
        def wrapper(*aug, **kwargs):
            try:
                return func(*aug, **kwargs)
            except Exception as e:
                # for multi-devices
                if type(self.udid) is list and type(self.driver) is list:
                    im_b64_list = []
                    file_full_path = self.output_path + "/[Exception]" + func.__name__ + ".png"
                    for index in range(len(self.udid)):
                        os.makedirs(self.source_path + "/report/" + self.udid[0], exist_ok=True)
                        im_b64_list.append(self.driver[index].get_screenshot_as_base64())
                    self.hconcat_resize_min(im_b64_list, file_full_path)
                    logger("Exception screenshot: %s" % file_full_path)
                else: # single
                    self.driver = self.driver if isinstance(self.driver, list) else [self.driver]
                    tb = sys.exc_info()[2]
                    lineno = traceback.extract_tb(tb)[-1].lineno
                    funcname = func.__name__ #.replace('test_','')
                    filename = os.path.basename(traceback.extract_tb(tb)[-1].filename)
                    file_full_path = self.output_path + f"/[Exception]{funcname}_{lineno}.png"
                    if type(self.udid) is list:
                        os.makedirs(self.source_path + "/report/" + self.udid[0], exist_ok=True)
                    else:
                        os.makedirs(self.source_path + "/report/" + self.udid, exist_ok=True)
                    self.driver[0].get_screenshot_as_file(file_full_path)
                    logger(f"Exception screenshot:{file_full_path}",line=lineno,file_name=filename,function=funcname)
                    if self.report_type == "ReportPortal":
                        # Attach screenshot to RP
                        self.attach_to_reportportal(
                            name=filename,
                            path=file_full_path,
                            content_type="image/png",
                        )
                logger("Exception: %s" % str(e), line=lineno, file_name=filename, function=funcname)
                # stop recording screen and save file
                if self.start_recording_flag == 1:
                    if type(self.udid) is list and type(self.driver) is list:
                        for index in range(len(self.udid)):
                            if hasattr(self.driver[index], "stop_recording_screen"):
                                base64_data = self.driver[index].stop_recording_screen()
                                file_path_record_video = self.output_path + "/[Exception]" + func.__name__ + f"({self.udid[index]}).mp4"
                                fh = open(file_path_record_video, "wb")
                                fh.write(base64.b64decode(base64_data))
                                fh.close()
                                logger("Exception recording video: %s" % file_path_record_video)
                                # update mediastore (for recording tmp file)
                                cmd = f'adb -s {self.udid[index]} shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///storage///emulated///0///'
                                self.shell(cmd)
                    else:
                        if hasattr(self.driver, "stop_recording_screen"):
                            base64_data = self.driver.stop_recording_screen()
                            file_path_record_video = self.output_path + "/[Exception]" + func.__name__ + ".mp4"
                            fh = open(file_path_record_video, "wb")
                            fh.write(base64.b64decode(base64_data))
                            fh.close()
                            logger("Exception recording video: %s" % file_path_record_video)
                            # update mediastore (for recording tmp file)
                            cmd = f'adb -s {self.udid} shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///storage///emulated///0///'
                            self.shell(cmd)
                    self.start_recording_flag = 0  # turn off the flag
                raise
        return wrapper
    
    def attach_screenshot(self, file_name, file_path):
        """
        Public method to attach an existing screenshot file to ReportPortal.
        """
        if not os.path.isfile(file_path):
            logger(f"File not found for attachment: {file_path}")
            return

        self.attach_to_reportportal(file_name, file_path, "image/png")

    def attach_to_reportportal(self, name, path, content_type):
        """
        Low-level method that actually calls rp_logger.info(..., attachment=...).
        """
        def rp_logger():
            import logging
            from reportportal_client import RPLogger
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.DEBUG)
            logging.setLoggerClass(RPLogger)
            return logger
        rp_logger = rp_logger()

        if not rp_logger:
            logger("rp_logger not set! Cannot attach to ReportPortal.")
            return

        if not os.path.isfile(path):
            logger(f"File not found: {path}")
            return

        try:
            with open(path, "rb") as f:
                content = f.read()

            rp_logger.info(
                f"Fail Screenshot: {name}",
                attachment={
                    "name": name,
                    "data": content,
                    "mime": content_type,
                },
            )
        except Exception as e:
            logger(f"Error: Failed to upload file to ReportPortal. {str(e)}")


    def exception_keep_records(self, func):
        @functools.wraps(func)
        def wrapper(*aug, **kwargs):
            try:
                if type(self.driver) is list:
                    for index in range(len(self.driver)):
                        self.driver[index].record_operations_start(func_name=func.__name__, file_path=self.source_path, udid=self.udid)
                else:
                    self.driver.record_operations_start(func_name=func.__name__, file_path=self.source_path, udid=self.udid)
                return func(*aug, **kwargs)
            except Exception as e:
                if type(self.driver) is list:
                    for index in range(len(self.driver)):
                        self.driver[index].record_operations_end(func_name=func.__name__, file_path=self.source_path, udid=self.udid, keep=True)
                else:
                    self.driver.record_operations_end(func_name=func.__name__, file_path=self.source_path, udid=self.udid, keep=True)
                raise
            finally:
                if type(self.driver) is list:
                    for index in range(len(self.driver)):
                        if self.driver[index].recording_flag is True:
                            self.driver[index].record_operations_end(func_name=func.__name__, file_path=self.source_path, udid=self.udid, keep=False)
                else:
                    if self.driver.recording_flag is True:
                        self.driver.record_operations_end(func_name=func.__name__, file_path=self.source_path, udid=self.udid, keep=False)
        return wrapper

    @contextmanager
    def uuid(self, *uuids):
        '''
            multiple uuid: ["xxx-xx-xx-xx","xxx-xxx-xx-xx"]
        '''
        _s = "[a-fA-F0-9]"
        patten = f"{_s}{{8}}(?:-{_s}{{4}}){{3}}-{_s}{{12}}"
        _uuids = []
        for _uuid in uuids:
            __uuids = re.findall(patten, _uuid)
            _uuids.extend(__uuids)
        for _uuid in _uuids:
            self.start_uuid(_uuid)
        self.result = None
        self.fail_log = ""
        self.log = ""
        yield self
        try:
            name = os.path.basename(inspect.stack()[2].function).replace("test_", "")
            for _uuid in _uuids:
                self.new_result(_uuid, self.result, fail_log=self.fail_log, case_name=name, level=5)
        except Exception as e:
            logger(f"[ERROR] no result is set! {uuids=}")
            logger(f'{e=}')

    def shell(self, command):    # return Ture/False
        import subprocess
        try:
            # if not "adb -s " in command: command = command.replace("adb","adb -s %s " % self.udid)
            logger("shell: %s" % command)
            subprocess.call(command)
            return True
        except Exception as e:
            logger("shell fail : %s" % str(e))
            return False

    # Concatenate images of different heights horizontally
    def hconcat_resize_min(self, im_b64_list, filename_out='D:\\out.png', interpolation=cv2.INTER_CUBIC):
        try:
            im_list = []
            # transfer from b64 string to numpy array structure
            for index in range(len(im_b64_list)):
                img_data = base64.b64decode(im_b64_list[index])
                nparr = np.frombuffer(img_data, np.uint8)
                img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                im_list.append(img_np)
            # im_list of numpy array structure
            h_min = min(im.shape[0] for im in im_list)
            im_list_resize = [
                cv2.resize(im, (int(im.shape[1] * h_min / im.shape[0]), h_min), interpolation=interpolation)
                for im in im_list]
            im_h_resize = cv2.hconcat(im_list_resize)
            cv2.imwrite(filename_out, im_h_resize)
        except Exception as e:
            print(f'Exception occurs - {e}')
            raise Exception
        return True
