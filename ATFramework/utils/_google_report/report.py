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
import datetime
from contextlib import contextmanager
import base64
import json
try:
    import cv2
    import numpy as np
except:
    cv2 = type('cv2', (object,), {"INTER_CUBIC":None})()

# from .sendemail import send_mail as sendMail
try:
    from ..log import logger
except:
    from .._log.log import logger
from .._google_api.google_api import GoogleApi

class MyGoogleReport(object):
    uuid_queue = set()

    def __init__(self,udid = None,driver = None, google_report_info=None, is_log_cpu_memory=True, is_fail_screenshot=True):
        self.driver = driver
        self.udid = udid or "unknown_device"
        # self.html_name = html_name
        self.src_spreadsheet_id = google_report_info['src_spreadsheet_id']
        self.src_sheet_name = google_report_info['src_sheet_name']
        self.dest_spreadsheet_id = google_report_info['dest_spreadsheet_id']
        now = datetime.datetime.now()
        self.dest_sheet_name = f'{self.src_sheet_name.replace("_Template", "")}_{now.strftime("%Y%m%d_%H%M%S")}'
        self.is_fail_screenshot = is_fail_screenshot
        self.set_path()
        self.result_range = google_report_info['range']
        self.result_list = self.read_result_list(google_report_info['range'])
        self.start_time = time.time()
        self.fail_number = 0
        self.ovInfo = {
            "title": "",
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "server": os.getenv('COMPUTERNAME', "Windows" if platform.system() == "Windows" else "Mac OS"),
            "os": "driver.capabilities['os']",
            "device": "driver.capabilities['device']",
            "version": "driver.capabilities['version']",
            "build_version": "",
            "script_version": "",
            "total_case": 0,
            "pass": 0,
            "fail": 0,
            "_fail": 0,
            "na": 0,
            "skip": 0,
            "duration": "00:00:00"
            }
        self.passNumber = 0
        self.failNumber = 0
        self.pic_index = 0
        self.start_recording_flag = 0
        self.is_recording_enabled = 0
        self.uuid_performance = {}
        self.is_log_cpu_memory = is_log_cpu_memory  # Currently, for macOS only (2022/05/10)
        self.summary_info = google_report_info['summary_info']
        self.url_report = ''
        logger(f'summary info original={self.summary_info}')

        self.summary_info['data']['date'] = self.ovInfo['date']
        self.summary_info['data']['start time'] = self.ovInfo['time']
        self.summary_info['data']['test cases'] = 0
        self.summary_info['data']['pass'] = 0
        self.summary_info['data']['fail'] = 0
        self.summary_info['data']['skip'] = 0
        self.summary_info['data']['na'] = 0
        self.summary_info['data']['elapsed time'] = ''
        self.curr_uuids = list()
        self.result_keyword = {'pass': 'PASS', 'fail': 'FAIL', 'na': 'N/A', 'skip': 'SKIP'}
        if 'result_keyword' in google_report_info.keys():
            for key in google_report_info['result_keyword']:
                if key in self.result_keyword.keys():
                    self.result_keyword[key] = google_report_info['result_keyword'][key]
        # remove summary.txt under report folder
        if os.path.isfile(os.path.join(os.path.dirname(self.output_file), 'summary.txt')):
            os.remove(os.path.join(os.path.dirname(self.output_file), 'summary.txt'))
            logger(f'remove summary.txt under report folder.')

    def set_path(self): # Done
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
        self.output_file = self.output_path + "/Report.csv"
        self.csv_file = self.output_path + "/performance.csv"
        if self.src_sheet_name is None:
            self.output_file = self.output_path +"/Report.csv"
        else:
            self.output_file = self.output_path + f'/{self.src_sheet_name}_Report.csv'

    def read_result_list(self, range_result): # read result list ['test case', 'uuid', 'note'] list from source google sheet, range: '!J3:L2242'
        try:
            list_result = list()
            obj_google_api = GoogleApi(self.src_sheet_name, [], 1, self.src_spreadsheet_id)
            ranges = f'{obj_google_api.sheet_name}!{range_result}'
            response = obj_google_api.service.spreadsheets().values().batchGet(
                spreadsheetId=obj_google_api.spreadsheet_id, ranges=ranges, majorDimension='ROWS').execute()

            for item in response['valueRanges'][0]['values']:
                item_temp = {'case': '', 'uuid': item[1] if len(item) > 0 else '', 'note': item[2] if len(item) == 3 else ''} # ['test case', 'uuid', 'note']
                list_result.append(item_temp)
        except Exception as e:
            logger(f'Exception occurs. Error={e}')
            raise
        return list_result

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

    def set_udid(self,udid): # no use
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
        if platform.system() == 'Darwin' and self.is_log_cpu_memory:
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
            return self  # by Jim (if no match uuid, return directly) [2022-10-24]
        else:
            self.uuid_queue.remove(id)
            if platform.system() == 'Darwin' and self.is_log_cpu_memory:
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

        # fill in Pass/ Fail/ N/A according to result (by Jim 2022-10-24)
        for item in self.result_list:
            if item['uuid'] == id:
                item['case'] = name  # case name
                item['uuid'] = self.result_keyword['pass'] if result else self.result_keyword['na'] if result is None else self.result_keyword['fail']
                item['note'] = f'\n{log}' if item['note'] else log

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

        #exist uuid change result to fail
        for uuid in self.uuid_queue.copy():
            self.new_result(uuid,False,"Exception", fail_screenshot=False,case_name= "unknown")

        cnt_skip = 0
        for item in self.result_list:
            if re.findall(r'(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})', item['uuid']):
                item['uuid'] = self.result_keyword['skip']
                cnt_skip += 1
        # self.ovInfo["skip"] = repl.count
        self.ovInfo["skip"] = cnt_skip
        self.ovInfo["duration"] = str(timedelta(seconds=report_elapsed_time))
        # output summary.txt
        if type(self.udid) == list:
            os.makedirs(self.source_path + "/report/" + self.udid[0], exist_ok=True)
        else:
            os.makedirs(self.source_path + "/report/" + self.udid, exist_ok=True)
        self.ovInfo['fail_number'] = self.ovInfo["fail"]
        if self.ovInfo["fail"]:
            self.fail_number = self.ovInfo["fail"]
            self.ovInfo["_fail"] = self.ovInfo["fail"]
            self.ovInfo["fail_number"] = self.ovInfo["fail"]
        self.ovInfo['total_case'] = self.ovInfo['pass'] + self.ovInfo['fail'] + self.ovInfo['skip'] + self.ovInfo['na']

        self.export_to_google_sheet()

        # Generate summary report
        self.summary_info['data']['url_report'] = self.url_report
        self.summary_info['data']['elapsed time'] = self.ovInfo["duration"]
        with open(os.path.join(os.path.dirname(self.output_file), "summary.txt"), 'w') as data:
            data.write(str(json.dumps(self.summary_info['data'], indent=2)))

        if platform.system() == 'Darwin' and self.is_log_cpu_memory:
            # with open(self.output_file,"w") as f, open(self.csv_file, "a") as csv:
            with open(self.csv_file, "a") as csv:
                # f.write(self.html_final)
                # csv_data = [f'''{self.html_name.split(".")[0]}{f",'{'=' * 10}" * 6}\n''']   # Split by page name
                csv_data = [f'''{self.src_sheet_name}{f",'{'=' * 10}" * 6}\n''']  # Split by page name
                csv_data += [f"{k},{v['diff']['cpu']},{v['diff']['ram']},"
                             f"{v['start']['cpu']},{v['start']['ram']},"
                             f"{v['end']['cpu']},{v['end']['ram']}\n" for k,v in self.uuid_performance.items()]
                logger(f"{csv_data=}")
                csv.writelines(csv_data)
        return self

    def export_to_google_sheet(self):
        try:
            sheet_header = list()
            obj_google_api = GoogleApi(self.src_sheet_name, sheet_header, 1, self.src_spreadsheet_id)
            src_sheet_id = obj_google_api.get_sheet_id_by_name(self.src_sheet_name)

            # Generate Summary Result
            self.summary_info['data']['test cases'] = self.ovInfo['pass'] + self.ovInfo['fail'] + self.ovInfo['skip'] + self.ovInfo['na']
            self.summary_info['data']['pass'] = self.ovInfo['pass']
            self.summary_info['data']['fail'] = self.ovInfo['fail']
            self.summary_info['data']['skip'] = self.ovInfo['skip']
            self.summary_info['data']['na'] = self.ovInfo['na']
            self.summary_info['data']['elapsed time'] = self.ovInfo['duration']
            logger(f'summary info={self.summary_info["data"]}')

            # Export report to JSON
            self._export_to_json()

            # copy template report and rename
            new_sheet_id = obj_google_api.copy_sheet_to_spreadsheet(self.src_spreadsheet_id, src_sheet_id,
                                                            self.dest_spreadsheet_id, self.dest_sheet_name)
            if not new_sheet_id:
                logger('Fail to copy google sheet to new spreadsheet.')
                raise Exception('Fail to copy google sheet to new spreadsheet.')
            self.url_report = rf'https://docs.google.com/spreadsheets/d/{self.dest_spreadsheet_id}/edit#gid={new_sheet_id}'
            logger(f'Report Url={self.url_report}')

            # fill in result
            obj_google_api.fill_test_result(self.result_list, self.dest_spreadsheet_id, self.dest_sheet_name,
                                            self.result_range)
            # fill in summary
            data = list(self.summary_info['data'].values())
            logger(f'summary data in list={data}')
            obj_google_api.fill_test_summary(data, self.dest_spreadsheet_id, self.dest_sheet_name,
                                             self.summary_info['range'])
        except Exception as e:
            logger(f'Exception occurs. Error={e}')
            return False
        return True

    def _export_to_json(self):
        try:
            logger('Export report to JSON Start.')
            data = dict()
            data['src_spreadsheet_id'] = self.src_spreadsheet_id
            data['src_sheet_name'] = self.src_sheet_name
            data['dest_spreadsheet_id'] = self.dest_spreadsheet_id
            data['dest_sheet_name'] = self.dest_sheet_name
            data['result_list'] = self.result_list
            data['result_range'] = self.result_range
            data['summary_info'] = self.summary_info

            logger(f'Export data={data}')
            with open(os.path.join(os.path.dirname(self.output_file), "report.json"), 'w') as report:
                report.write(json.dumps(data, indent=2))
            logger('Export report to JSON OK.')
        except Exception as e:
            logger(f'Exception occurs. Error={e}')
            return False
        return True

    def export_to_google_sheet_from_json(self, json_file=''):
        try:
            # Read Report JSON file
            with open(json_file) as file:
                json_content = file.read()
            obj_json_report = json.loads(json_content)
            logger(f'JSON Object={obj_json_report}')

            # Create Google api object
            sheet_header = list()
            self.src_sheet_name = obj_json_report['src_sheet_name']
            self.src_spreadsheet_id = obj_json_report['src_spreadsheet_id']
            self.dest_spreadsheet_id = obj_json_report['dest_spreadsheet_id']
            self.dest_sheet_name = obj_json_report['dest_sheet_name']
            self.result_list = obj_json_report['result_list']
            self.result_range = obj_json_report['result_range']
            self.summary_info = obj_json_report['summary_info']

            obj_google_api = GoogleApi(self.src_sheet_name, sheet_header, 1, self.src_spreadsheet_id)
            src_sheet_id = obj_google_api.get_sheet_id_by_name(self.src_sheet_name)
            obj_dest_google_api = GoogleApi('', sheet_header, 1, self.dest_spreadsheet_id)

            # delete destination report if exists
            list_sheet = obj_dest_google_api.get_sheets_title_list()
            if self.dest_sheet_name in list_sheet:
                logger(f'enter delete sheet')
                dest_sheet_id = obj_dest_google_api.get_sheet_id_by_name(self.dest_sheet_name)
                # delete target sheet
                obj_dest_google_api.delete_sheet(self.dest_spreadsheet_id, dest_sheet_id)
                logger(f'Delete sheet={self.dest_sheet_name} OK.')

            # copy template report and rename
            new_sheet_id = obj_google_api.copy_sheet_to_spreadsheet(self.src_spreadsheet_id, src_sheet_id,
                                                                    self.dest_spreadsheet_id, self.dest_sheet_name)
            if not new_sheet_id:
                logger('Fail to copy google sheet to new spreadsheet.')
                raise Exception('Fail to copy google sheet to new spreadsheet.')
            self.url_report = rf'https://docs.google.com/spreadsheets/d/{self.dest_spreadsheet_id}/edit#gid={new_sheet_id}'
            logger(f'Report Url={self.url_report}')

            # fill in result
            obj_google_api.fill_test_result(self.result_list, self.dest_spreadsheet_id, self.dest_sheet_name,
                                            self.result_range)
            # fill in summary
            data = list(self.summary_info['data'].values())
            logger(f'summary data in list={data}')
            obj_google_api.fill_test_summary(data, self.dest_spreadsheet_id, self.dest_sheet_name,
                                             self.summary_info['range'])
        except Exception as e:
            logger(f'Exception occurs. Error={e}')
            return False
        return True

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
        self.curr_uuids = _uuids
        for _uuid in _uuids:
            self.start_uuid(_uuid)
        self.result = None
        self.fail_log = ""
        self.log = ""
        yield self
        try:
            name = os.path.basename(inspect.stack()[2].function).replace("test_", "")
            for _uuid in _uuids:
                self.new_result(_uuid, self.result, fail_log=self.fail_log, log=self.log, fail_screenshot=self.is_fail_screenshot, case_name=name, level=5)
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

