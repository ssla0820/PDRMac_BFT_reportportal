import requests
from bs4 import BeautifulSoup
import sys
from os.path import dirname as _dir
sys.path.insert(0, _dir(__file__))
import re
import shutil
import browser_cookie3
import os
import inspect
import json
import hashlib
from configparser import ConfigParser
import subprocess
from password import Authorization
import getpass
import http.cookiejar
import base64
import platform

try:
    from ..log import logger
except:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))
    print(os.path.dirname(SCRIPT_DIR))
    from log import logger

debug_mode = False

# ==================================================================================================================
# Class: Ecl_Operation
# Description: eCL query SR/TR information service related functions
# Usage: Refer to test_script_03.py for example
# Interface: get_latest_build or get_latest_tr_build (are the same)
# parameter: a dictionary (in 3 groups - searching/filter SRs, specified SR/TR, path specify, mail list)
#            1) Searching/Filter SRs:
#               - prod_name [MUST], prod_ver, prod_ver_type, filter_sr_keyword, custom_name, query_mode
#            2) Specified SR/TR:
#               - sr_no, tr_no
#            3) Path Specify:
#               - prog_path_sub, dest_path, work_dir
#            4) Mail List:
#               - mail_list
# Return: True/False
# Note: For downloading TR build, should use password.py to generate credential file first.
# Author: Jim Huang
# Revise: v1.0 (1st version)
#         v1.1 (add more common functions for querying)    (2020/10/22)
#         v1.2 - add parameter key 'filter_sr_keyword'     (2021/12/10)
#              - add interface 'get_latest_tr_build' for downloading build directly and supports new parameters as below.
#              - parameter 'prod_ver' supports 20.0 and 20.0+ (equal and greater than 20.0)
#              - parameter 'filter_sr_keyword' and 'prod_ver_type' supports multiple conditions by using ','
#              - e.g. filter_sr_keyword = 'VDE,PUS'
#              - e.g. prod_ver_type = 'Subscription,Ultra'
#         v1.3 - to fix the loading cookie file fail for Chrome 96.x (2021/12/16)
#              - solution: to create cookie object to query TR page instead of loading Chrome cookie file
#         v1.4 - to fix the loading cookie file fail for Chrome 96.x (2021/12/21)
#              - to check if Chrome M96 new cookie file path exists or not, if yes, to specify the cookie file for M96
#              - to get the ECLID and write to eclid file and to load the ECLID from eclid file directly if it exists
#         v1.5 - to support SubSR for 365 project (2022/02/15)
#                > add parameter key 'query_mode' for searching SR (Master SR ONLY [Default]), 1 (Sub-SR ONLY), 2 (Master+Sub-SR)
#              - support 'OEM' SR searching
#                > add parameter key 'custom_name' (e.g. 'CyberLink', 'OEM' [means all SRs except for CyberLink])
#              - key 'sr_no' supports both Master SR and SubSR
#              - to save ECLID of chrome cookie to eclid file to prevent from otp code overdue
# ==================================================================================================================

class Ecl_Operation():
    def __init__(self, para_dict): # prod_name, sr_no, tr_no, prog_path_sub, dest_path, work_dir (for password and tr_db file), mail_list(list)
        try:
            self.user_name = ''
            self.password = ''
            self.prod_name = ''
            if 'prod_name' in para_dict.keys():
                self.prod_name = para_dict['prod_name']
            self.prod_ver = ''
            if 'prod_ver' in para_dict.keys():
                self.prod_ver = para_dict['prod_ver']
            self.prod_ver_type = ''
            if 'prod_ver_type' in para_dict.keys():
                self.prod_ver_type = para_dict['prod_ver_type']
            self.custom_name = ''
            if 'custom_name' in para_dict.keys():
                self.custom_name = para_dict['custom_name']
            self.filter_sr_keyword = ''
            if 'filter_sr_keyword' in para_dict.keys():
                self.filter_sr_keyword = para_dict['filter_sr_keyword']
            self.query_mode = 0 # query_mode = 0 (Master SR ONLY [Default]), 1 (Sub-SR ONLY), 2 (Master+Sub-SR)
            if 'query_mode' in para_dict.keys():
                self.query_mode = int(para_dict['query_mode'])
            self.sr_no = ''
            if 'sr_no' in para_dict.keys():
                self.sr_no = para_dict['sr_no']
            self.tr_no = ''
            if 'tr_no' in para_dict.keys():
                self.tr_no = para_dict['tr_no']
            self.work_dir = os.path.dirname(__file__)
            if 'work_dir' in para_dict.keys() and para_dict['work_dir']:
                self.work_dir = para_dict['work_dir']
            if debug_mode: print(f'Init - work_dir={self.work_dir}')
            self.program_path_subfolder = ''
            if 'prog_path_sub' in para_dict.keys():
                self.program_path_subfolder = para_dict['prog_path_sub']
            self.mail_list = ''
            if 'mail_list' in para_dict.keys():
                self.mail_list = para_dict['mail_list']
            self.dest_path = para_dict['dest_path']
            # self.cookies = browser_cookie3.chrome(domain_name='.cyberlink.com')
            self.cookies = self.create_chrome_cookie()
            self.password_file = 'password'
            self.tr_db_file = 'tr_db'
            self.err_msg = ''
            # decrypt the username/ password
            obj_authorization = Authorization(self.work_dir)
            passwd_list = obj_authorization.decryption_vigenere_clt_account()
            self.user_name = passwd_list[0]
            self.password = passwd_list[1]
        except Exception as e:
            err_msg = f'Exception occurs. Incorrect format of parameter or missing keys. ErrorLog={e}'
            logger(err_msg)
            self.err_msg = err_msg

    def create_chrome_cookie(self):
        eclid_value = self.read_eclid_file()
        if not eclid_value:
            return False
        host = '.cyberlink.com'
        path = '/'
        secure = True
        # This count starts at the Unix Epoch on January 1st, 1970 at UTC
        # expires = 1642046350.0547829 #  Thursday, January 13, 2022 11:59:10 AM GMT+08:00 (relative: a month)
        expires = None
        name = 'ECLID'
        value = eclid_value

        cj = http.cookiejar.CookieJar()
        c = http.cookiejar.Cookie(0, name, value, None, False, host, host.startswith('.'), host.startswith('.'),
                                  path, True, secure, expires, False, None, None, {})
        cj.set_cookie(c)
        return cj

    def read_eclid_file(self):
        # file_name = 'eclid'
        file_name = os.path.normpath(os.path.join(self.work_dir, 'eclid'))
        logger(f'eclid file path={file_name}')
        if debug_mode: print(f'eclid file path={file_name}')
        ECL_ID = ''
        if not os.path.exists(file_name):
            if debug_mode: print('eclid file does not exist')
            logger('eclid file does not exist')
            # get ECLID from CookieJar
            cookie_file = None
            if platform.system() == 'Windows':
                cookie_file = self.get_windows_cookie_file() # to handle the Windows Chrome M96 Cookie file path change issue
            cookie_jar = browser_cookie3.chrome(cookie_file=cookie_file, domain_name='.cyberlink.com')
            for cookie in cookie_jar:
                if cookie.name == 'ECLID':
                    ECL_ID = cookie.value
                    break
            if not ECL_ID:
                err_msg = 'Fail to load ECLID from CookieJar object'
                if debug_mode: print(err_msg)
                logger('Fail to load ECLID from CookieJar object')
                return False
            f = open(file_name, "wb")
            bytes_content = ECL_ID.encode('utf-8')
            encoded = base64.b64encode(bytes_content)
            f.write(encoded)
            f.close()
        else:
            # read ECLID from file
            if debug_mode: print('read eclid file')
            f = open(file_name, "rb")
            encoded = f.read()
            bytes_content = base64.b64decode(encoded)
            ECL_ID = bytes_content.decode('utf-8')
            logger('read eclid file successfully')
        if debug_mode: print(f'ECLID: {ECL_ID}')
        return ECL_ID

    def get_windows_cookie_file(self):
        windows_cookies = {'env': 'APPDATA', 'path': '..\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies'} # path for Chrome M96 (handle browser_cookie3 Chrome M96 issue)
        file_path = os.path.join(os.getenv(windows_cookies['env'], ''), windows_cookies['path'])
        if not os.path.isfile(file_path):
            file_path = None
        return file_path

    def _send_email(self):
        try:
            from sendemail import send_mail
            opts = {
                "account": "cyberlinkqamc@gmail.com"
                , "password": "qamc1234"
                , "from": "QAATServer <cyberlinkqamc@gmail.com>"
                , "to": self.mail_list
                , "subject": "[AT] Auto TR Build Download Module Error"
                , "text": "text_content"
                , "html": self.err_msg
                , "attachment": []
            }
            send_mail(opts)
        except Exception as e:
            print(f'Exception occurs. Error={e}')
            raise Exception
        return True

    def _get_tr_info(self,  html_cleantext, head, tail): # html_cleantext: from BeautifulSoup(r.text, "lxml").text
        try:
            pattern = rf'(?<={head})(.*)(?={tail})'
            result = re.search(pattern, html_cleantext, re.DOTALL)
        except Exception as e:
            print(f'Exception occurs. Error={e}')
            raise Exception
        return result

    def _md5(self, filename):
        try:
            md5_object = hashlib.md5()
            block_size = 128 * md5_object.block_size
            a_file = open(filename, 'rb')

            chunk = a_file.read(block_size)
            while chunk:
                md5_object.update(chunk)
                chunk = a_file.read(block_size)

            md5_hash = md5_object.hexdigest()
            if debug_mode: print(f'{md5_hash=}')
        except Exception as e:
            logger(f'Exception occurs. ErrLog={e}')
            raise Exception
        return md5_hash

    def _md5_check_folder(self, path_folder):
        try:
            file_md5 = 'Cyberlink.MD5'
            if os.name == 'nt':
                path_md5 = '\\'.join([path_folder, file_md5]) # for windows
            else: # mac
                path_md5 = '/'.join([path_folder, file_md5])
            if not os.path.isfile(path_md5):
                logger('No Cyberlink.MD5 file')
                return False

            config = ConfigParser()
            config.read(path_md5)
            section_name = 'Info'
            file_count = int(config[section_name]['Count'])
            # print(f'{file_count=}')
            list_keys = config.items(section_name)
            # print(f'{list_keys=}')
            file_count_pass = 0
            for index in range(len(list_keys)):
                if index == 0:
                    continue
                if os.name == 'nt':
                    file = ''.join([path_folder, list_keys[index][0]])
                else: # mac
                    sub_path = list_keys[index][0].replace('\\', '/')
                    file = ''.join([path_folder, sub_path])
                # print(file)
                if list_keys[index][1] == '':
                    file_count_pass += 1
                    continue
                if not os.path.isfile(file):
                    print(f'{file} doesn\'t exist.')
                    continue
                value = self._md5(file)
                if not value:
                    print(f'Generate MD5 checksum of {file}')
                    continue
                if value.upper() == list_keys[index][1].upper():
                    file_count_pass += 1
                else:
                    print(f'[_md5_check_folder] MD5 check FAIL. {file=}, MD5_expected={list_keys[index][1]}, MD5_check={value.upper()}')

            if not file_count_pass == file_count:
                err_msg = f'[_md5_check_folder] MD5 check is FAIL. Expected={file_count}, Passed={file_count_pass}, folder_path={path_folder}'
                print(err_msg)
                self.error_msg = err_msg
                return False
            print(f'MD5 check is Done. Expected={file_count}, Passed={file_count_pass}')
        except Exception:
            return False
        return True

    def retrieve_tr_info(self):
        try:
            dict_result = {'sr_no': '', 'tr_no': '', 'ver_type': '', 'build': '', 'prog_path': '', 'short_description': '', 'project': ''}
            dict_result['tr_no'] = self.tr_no
            if self.tr_no != '':
                url = f'https://ecl.cyberlink.com/TR/TRHandle/HandleMainTR.asp?IsFromMail=true&TRCode={self.tr_no}'
                r = requests.get(url, auth=(self.user_name, self.password), cookies=self.cookies)
                cleantext = BeautifulSoup(r.text, "lxml").text
                # TR Info. - Builder
                head = 'Creator:'
                tail = 'Creation Date:'
                result = self._get_tr_info(cleantext, head, tail)
                pos_start = result[0].find("(Builder:")
                if pos_start != -1:
                    dict_result['builder'] = result[0][0:pos_start].strip()
                else:
                    dict_result['builder'] = result[0].strip()
                # TR Info. - Creation Time
                head = 'Creation Date:'
                tail = 'TR Type:'
                result = self._get_tr_info(cleantext, head, tail)
                pos_start = result[0].find("(")
                if pos_start != -1:
                    dict_result['creation_time'] = result[0][0:pos_start].strip().replace(u'\u00a0', '') # replace the unicode character
                else:
                    dict_result['creation_time'] = result[0].strip().replace(u'\u00a0', '')
                dict_result['creation_time'] = dict_result['creation_time'].replace("/", "-")
                # TR Info. - Status
                # check if cancel or reject
                head = 'TR Code:'
                tail = 'Creator:'
                result = self._get_tr_info(cleantext, head, tail)
                pos_start = result[0].find("[")
                pos_end = result[0].find("]")
                if pos_start != -1 and pos_end != -1:
                    dict_result['status'] = result[0][pos_start + 1:pos_end].strip()
                else:
                    head = 'Creation Date:'
                    tail = 'TR Type:'
                    result = self._get_tr_info(cleantext, head, tail)
                    pos_start = result[0].find("(")
                    pos_end = result[0].find(")")
                    if pos_start != -1 and pos_end != -1:
                        dict_result['status'] = result[0][pos_start+1:pos_end].strip()
                    else:
                        dict_result['status'] = ""
                # TR Info. - Program Path
                head = 'Program Path'
                tail = 'Built by'
                result = self._get_tr_info(cleantext, head, tail)
                dict_result['prog_path'] = result[0].replace('(ex: Q:\PoweDVD\):', '').strip()
                # TR Info. - Build
                head = 'Build:'
                tail = 'Environment'
                result = self._get_tr_info(cleantext, head, tail)
                if 'Stage:' in result[0]:
                    dict_result['build'] = result[0].split('Stage:')[0].strip()
                elif 'Software' in result[0]:
                    dict_result['build'] = result[0].split('Software')[0].strip()
                elif 'Hardware' in result[0]:
                    dict_result['build'] = result[0].split('Hardware ')[0].strip()
                else:
                    dict_result['build'] = result[0].strip()
                # TR Info. - Version Type
                try:
                    head = 'Version Type:'
                    tail = 'Build:'
                    result = self._get_tr_info(cleantext, head, tail)
                    dict_result['ver_type'] = result[0].strip()
                except:
                    pass
                # TR Info. - SR No.
                head = 'SR NO:'
                tail = 'Due Date:'
                result = self._get_tr_info(cleantext, head, tail)
                dict_result['sr_no'] = result[0].strip()
                # TR Info. - Short Description.
                try:
                    head = 'Short Description'
                    tail = 'Detailed information'
                    result = self._get_tr_info(cleantext, head, tail)
                    dict_result['short_description'] = result[0].strip()
                except:
                    pass
                # TR Info. - Project
                try:
                    head = 'Project:'
                    tail = 'TR Code:'
                    result = self._get_tr_info(cleantext, head, tail)
                    dict_result['project'] = result[0].strip()
                except:
                    pass
        except Exception as e:
            err_msg = f'[retrieve_tr_info]Exception Occurs. ErrroLog={e}, Please check the if can reach TR page correctly.'
            logger(err_msg)
            self.err_msg = err_msg
            raise Exception
        return dict_result

    def get_sub_sr_list_by_master_sr_from_webpage(self, sr_no): # when no TR list is found from master, try this [from Webpage]
        sub_sr_list = []
        try:
            url = f'https://ecl.cyberlink.com/PC/ShowSRF/showSRFResult.asp?SRF_no={sr_no}'
            r = requests.get(url, auth=(self.user_name, self.password), cookies=self.cookies)
            cleantext = BeautifulSoup(r.text, "lxml").text
            # get section of sub-sr
            head = 'In-App SubSR'
            tail = 'Big Bang Definition'
            result = self._get_tr_info(cleantext, head, tail)
            if result:
                pattern = '([A-Z]{3}[\d]{6}-[\d]{2})'
                sub_sr_list = re.findall(pattern, result[0])
        except Exception as e:
            err_msg = f'[get_sub_sr_list]Exception Occurs. ErrroLog={e}, Please check the if can reach SR page correctly.'
            logger(err_msg)
            self.err_msg = err_msg
            raise Exception
        return sub_sr_list

    def get_last_valid_tr_by_sub_sr_from_webpage(self):
        self.tr_no = ''  # reset tr_no as empty
        try:
            url = f'https://ecl.cyberlink.com/PC/ShowSRF/IAU_Detail.asp?SubSR={self.sr_no}'
            r = requests.get(url, auth=(self.user_name, self.password), cookies=self.cookies)
            cleantext = BeautifulSoup(r.text, "lxml").text
            # get section of sub-sr
            head = 'Testing Request List :'
            tail = ''
            result = self._get_tr_info(cleantext, head, tail)
            # get TR list
            pattern_tr = '[A-Z]{2}[\d]{6}-[\d]{3}'
            tr_list = re.findall(pattern_tr, result[0])
            # print(f'Amount={len(tr_list)}, {tr_list=}')
            # split by TR number with index i.e. 2TR210929-003
            pattern_tr_with_index = '[\d]{1}[A-Z]{2}[\d]{6}-[\d]{3}'
            status_list = re.split(pattern_tr_with_index, result[0])
            del status_list[0] # remove first invalid record
            # print(f'Amount={len(status_list)}, {status_list=}')
            if tr_list and len(tr_list) == len(status_list):
                for item_tr, item_status in zip(tr_list[::-1], status_list[::-1]):  # list tr from end
                    # print(f'{item_tr=}, {item_status=}')
                    if 'Assigned' in item_status or 'NewCreated' in item_status:
                        if 'Cancel' not in item_status and 'Rejected' not in item_status:
                            self.tr_no = item_tr
                            break
                if self.tr_no == '':
                    self.err_msg = f'[get_last_valid_tr_by_sub_sr_from_webpage] No valid TR is found in Sub-SR={self.sr_no}'
                    return False
        except Exception as e:
            err_msg = f'[get_last_valid_tr_by_sub_sr_from_webpage]Exception Occurs. ErrroLog={e}.'
            logger(err_msg)
            self.err_msg = err_msg
            raise Exception
        return True

    def update_tr_to_db(self, tr_no, sr_no):
        print('Calling update_tr_to_db')
        try:
            tr_list = []
            if not tr_no:
                self.err_msg = 'Input tr_no is empty. SKIP it.'
                return tr_list
            # initial build_db file
            db_file_path = self.tr_db_file
            if self.work_dir != '':
                if os.name == 'nt':
                    db_file_path = self.work_dir + '\\' + self.tr_db_file
                else: # mac
                    db_file_path = self.work_dir + '/' + self.tr_db_file
            if not os.path.isfile(db_file_path):
                f = open(db_file_path, 'w')
                f.close()
            tr_db = ConfigParser()
            tr_db.optionxform = str  # make key as case sensitive
            tr_db.read(db_file_path)
            # check section - sr_no
            try:
                value = tr_db[sr_no][tr_no]
            except:
                tr_list.append(tr_no)
                if not tr_db.has_section(sr_no):
                    tr_db.add_section(sr_no)
                tr_db.set(sr_no, tr_no, '1')
                tr_db.write(open(db_file_path, 'w'))
        except Exception as e:
            err_msg = f'[update_tr_to_db]Exception occurs. ErrorLog={e}'
            logger(err_msg)
            self.err_msg = err_msg
            raise Exception
        return tr_list

    def add_tr_to_db(self, sr_no, tr_no):
        try:
            if not tr_no:
                self.err_msg = 'Input tr_no is empty. SKIP it.'
                logger('Input tr_no is empty. SKIP it.')
                return False
            # initial build_db file
            db_file_path = os.path.normpath(os.path.join(self.work_dir, self.tr_db_file))
            if not os.path.isfile(db_file_path):
                f = open(db_file_path, 'w')
                f.close()
            tr_db = ConfigParser()
            tr_db.optionxform = str  # make key as case sensitive
            tr_db.read(db_file_path)
            # check section - sr_no
            try:
                value = tr_db[sr_no][tr_no]
                if value == '0':
                    tr_db.set(sr_no, tr_no, '1')
                    tr_db.write(open(db_file_path, 'w'))
            except:
                if not tr_db.has_section(sr_no):
                    tr_db.add_section(sr_no)
                tr_db.set(sr_no, tr_no, '1')
                tr_db.write(open(db_file_path, 'w'))
        except Exception as e:
            err_msg = f'[update_tr_to_db]Exception occurs. ErrorLog={e}'
            print(err_msg)
            self.err_msg = err_msg
            raise Exception
        return True

    def check_if_tr_exists_in_db(self, tr_no, sr_no):
        try:
            tr_list = []
            if not tr_no:
                self.err_msg = 'Input tr_no is empty. SKIP it.'
                return tr_list
            # initial build_db file
            db_file_path = os.path.normpath(os.path.join(self.work_dir, self.tr_db_file))
            logger(f'tr_db file={db_file_path}')
            if not os.path.isfile(db_file_path):
                f = open(db_file_path, 'w')
                f.close()
            tr_db = ConfigParser()
            tr_db.optionxform = str  # make key as case sensitive
            tr_db.read(db_file_path)
            value = tr_db[sr_no][tr_no]
        except Exception as e:
            return False
        return bool(int(value))

    def query_sr_by_ecl_service(self): # return json object of sr/tr information
        query_content = ''
        try:
            # Query SR/TR list by http request
            prod_name = self.prod_name
            prod_ver = self.prod_ver
            prod_ver_type = self.prod_ver_type
            r = requests.get(
                f'https://ecl.cyberlink.com/WebService/BusinessService/ProductDevelopment/SR/SRService.asmx/QuerySRByProductName?ProdName={prod_name}&ProdVer={prod_ver}&ProdVerType={prod_ver_type}',
                auth=(self.user_name, self.password))
            query_content = r.text
            result = r.text.split('org/">')
            result = result[1].replace('</string>', '')
            # parse json
            ojson = json.loads(result)
        except Exception as e:
            logger(f'Excpetion occurs. Error={e}')
            logger(f'Query Result={query_content}')
            raise Exception('Please check do you have permission to access this page.')
        return ojson

    def get_sr_list(self, obj_json, sr_keyword='', sub_sr_list=None): # get the sr list from SR DB
        sr_list = []
        amount_sr = len(obj_json["SRForm"])
        if amount_sr > 0:
            for index in range(amount_sr):
                if sub_sr_list and obj_json['SRForm'][index]['SRF_no'] in sub_sr_list: # if current sr is sub_sr, skip it
                    continue
                if sr_keyword:
                    list_keyword = sr_keyword.split(',')
                    for keyword in list_keyword:
                        if keyword.strip() in obj_json['SRForm'][index]['SRF_no']:
                            sr_list.append(obj_json['SRForm'][index]['SRF_no'])
                            break
                else:
                    sr_list.append(obj_json['SRForm'][index]['SRF_no'])
        return sr_list

    def get_sub_sr_list(self, obj_json):
        sr_list = []
        amount_sr = len(obj_json["SRForm"])
        if debug_mode: print('SubSR from SRForm Level ====')
        if amount_sr > 0:
            for index in range(amount_sr):
                amount_sub_sr = len(obj_json['SRForm'][index]['IAU_SubSR'])
                if amount_sub_sr == 0:
                    continue
                for index_sub_sr in range(amount_sub_sr):
                    if debug_mode: print(f"[{index}] SubSR={obj_json['SRForm'][index]['IAU_SubSR'][index_sub_sr]['SubSR']}")
                    sr_list.append(obj_json['SRForm'][index]['IAU_SubSR'][index_sub_sr]['SubSR'])
        return sr_list

    def get_sub_sr_list_by_master_sr(self, obj_json, sr_num):
        sr_list = []
        amount_sr = len(obj_json["SRForm"])
        if amount_sr > 0:
            for index in range(amount_sr):
                if obj_json['SRForm'][index]['SRF_no'] == sr_num:
                    if obj_json['SRForm'][index]['IAU_SubSR']:
                        if debug_mode: print(f"[{index}] SR={obj_json['SRForm'][index]['SRF_no']}")
                        amount_sub_sr = len(obj_json['SRForm'][index]['IAU_SubSR'])
                        for index_sub in range(amount_sub_sr):
                            tmp_sub_sr_item = {'sub_sr': obj_json['SRForm'][index]['IAU_SubSR'][index_sub]['SubSR'], 'obj_sub_sr': obj_json['SRForm'][index]['IAU_SubSR'][index_sub]}
                            sr_list.append(tmp_sub_sr_item)
        return sr_list

    def get_last_valid_tr_by_sub_sr(self, sub_sr, skip_manual=False): # e.g. object of sub_sr = {'sr': 'VDE211008-02', 'obj_sub_sr': xxx}
        self.tr_no = ''  # reset tr_no as empty
        ojson_tr_list = sub_sr['obj_sub_sr']['TRList']
        if len(ojson_tr_list) > 0:
            for item_tr in ojson_tr_list[::-1]:  # list tr from end
                if 'Assigned' in item_tr['Status'] or 'NewCreated' in item_tr['Status']:
                    if 'Cancel' not in item_tr['Status'] and 'Rejected' not in item_tr['Status']:
                        self.tr_no = item_tr['TRCode']
                        tr_info = self.retrieve_tr_info()
                        logger("tr_info = ", tr_info)
                        if not skip_manual or tr_info["builder"] == "SR_AUTO":
                            logger("found")
                            break
                        else:
                            self.tr_no = ''
            if self.tr_no == '':
                self.err_msg = f'[get_last_valid_tr_by_sub_sr] No valid TR is found in SR={sub_sr["sub_sr"]}'
                return False
        else:
            err_msg = f'[get_last_valid_tr_by_sub_sr] NO TR List is found. SR_No={sub_sr["sub_sr"]}'
            if debug_mode: print(err_msg)
            self.err_msg = err_msg
            return False
        return True

    def get_last_valid_tr_with_done_by_sub_sr(self, sub_sr, skip_manual=False): # e.g. object of sub_sr = {'sr': 'VDE211008-02', 'obj_sub_sr': xxx}
        self.tr_no = ''  # reset tr_no as empty
        ojson_tr_list = sub_sr['obj_sub_sr']['TRList']
        if len(ojson_tr_list) > 0:
            for item_tr in ojson_tr_list[::-1]:  # list tr from end
                if 'Assigned' in item_tr['Status'] or 'NewCreated' in item_tr['Status'] or 'Done' in item_tr['Status']:
                    if 'Cancel' not in item_tr['Status'] and 'Rejected' not in item_tr['Status']:
                        self.tr_no = item_tr['TRCode']
                        tr_info = self.retrieve_tr_info()
                        logger("tr_info = ", tr_info)
                        if not skip_manual or tr_info["builder"] == "SR_AUTO":
                            logger("found")
                            break
                        else:
                            self.tr_no = ''
            if self.tr_no == '':
                self.err_msg = f'[get_last_valid_tr_by_sub_sr] No valid TR is found in SR={sub_sr["sub_sr"]}'
                return False
        else:
            err_msg = f'[get_last_valid_tr_by_sub_sr] NO TR List is found. SR_No={sub_sr["sub_sr"]}'
            if debug_mode: print(err_msg)
            self.err_msg = err_msg
            return False
        return True

    def filter_sr_list_by_prod_ver(self, obj_json, src_sr_list):
        sr_list = []
        if not self.prod_ver:
            return src_sr_list
        amount_src_sr = len(src_sr_list)
        if debug_mode: index = 0
        if amount_src_sr > 0:
            if '+' in self.prod_ver:
                filter_prod_ver = self.prod_ver.replace('+', '')
                for curr_sr in src_sr_list:
                    curr_prod_ver = self.get_prod_ver_by_sr(obj_json, curr_sr)
                    if debug_mode: print(f'[{index}] SR:{curr_sr}, Prod_Ver:{curr_prod_ver}')
                    try:
                        if float(curr_prod_ver) >= float(filter_prod_ver):
                            sr_list.append(curr_sr)
                    except:
                        if curr_prod_ver == filter_prod_ver:
                            sr_list.append(curr_sr)
                    if debug_mode: index += 1
            else:
                filter_prod_ver = self.prod_ver
                for curr_sr in src_sr_list:
                    curr_prod_ver = self.get_prod_ver_by_sr(obj_json, curr_sr)
                    if debug_mode: print(f'[{index}] SR:{curr_sr}, Prod_Ver:{curr_prod_ver}')
                    try:
                        if float(curr_prod_ver) == float(filter_prod_ver):
                            sr_list.append(curr_sr)
                    except:
                        if curr_prod_ver == filter_prod_ver:
                            sr_list.append(curr_sr)
                    if debug_mode: index += 1
        return sr_list

    def filter_sr_list_by_prod_ver_type(self, obj_json, src_sr_list):
        sr_list = []
        if not self.prod_ver_type:
            return src_sr_list
        amount_src_sr = len(src_sr_list)
        if debug_mode: index = 0
        if amount_src_sr > 0:
            filter_prod_ver_type = self.prod_ver_type.split(',')
            for curr_sr in src_sr_list:
                curr_prod_ver_type = self.get_prod_ver_type_by_sr(obj_json, curr_sr)
                if debug_mode: print(f'[{index}] SR:{curr_sr}, Prod_Ver_Type:{curr_prod_ver_type}')
                if curr_prod_ver_type in filter_prod_ver_type:
                    sr_list.append(curr_sr)
                if debug_mode: index += 1
        return sr_list

    def filter_sr_list_by_custom_name(self, obj_json, src_sr_list):
        sr_list = []
        if not self.custom_name:
            return src_sr_list
        amount_src_sr = len(src_sr_list)
        index = 0
        if amount_src_sr > 0:
            if self.custom_name == 'OEM':
                for curr_sr in src_sr_list:
                    curr_custom_name = self.get_custom_name_by_sr(obj_json, curr_sr)
                    if debug_mode: print(f'[{index}] SR:{curr_sr}, CustName:{curr_custom_name}')
                    if curr_custom_name != 'CyberLink':
                        sr_list.append(curr_sr)
                    index += 1
            else:
                for curr_sr in src_sr_list:
                    curr_custom_name = self.get_custom_name_by_sr(obj_json, curr_sr)
                    if debug_mode: print(f'[{index}] SR:{curr_sr}, CustName:{curr_custom_name}')
                    if curr_custom_name == self.custom_name:
                        sr_list.append(curr_sr)
                    index += 1
        return sr_list

    def get_prod_ver_type_by_sr(self, ojson, sr_num):
        amount_sr = len(ojson["SRForm"])
        index_target = -1
        version_type = -1
        for index in range(amount_sr):
            if sr_num == ojson['SRForm'][index]['SRF_no']:
                index_target = index
                break
        if index_target == -1:
            err_msg = f'[get_prod_ver_type_by_sr] No SR_Num is matched.'
            print(err_msg)
            self.err_msg = err_msg
            return False
        for index in range(len(ojson['SRForm'][index_target]['ProductList'])):
            if self.prod_name in ojson['SRForm'][index_target]['ProductList'][index]['Product']:
                version_type = ojson['SRForm'][index_target]['ProductList'][index]['Basic']['Version Type']
                break
        return version_type

    def get_prod_ver_by_sr(self, ojson, sr_num):
        amount_sr = len(ojson["SRForm"])
        index_target = -1
        version = -1
        for index in range(amount_sr):
            if sr_num == ojson['SRForm'][index]['SRF_no']:
                index_target = index
                break
        if index_target == -1:
            err_msg = f'[get_prod_ver_type_by_sr] No SR_Num is matched.'
            print(err_msg)
            self.err_msg = err_msg
            return False
        for index in range(len(ojson['SRForm'][index_target]['ProductList'])):
            if self.prod_name in ojson['SRForm'][index_target]['ProductList'][index]['Product']:
                version = ojson['SRForm'][index_target]['ProductList'][index]['Product'].replace(self.prod_name, '').strip()
                break
        return version

    def get_custom_name_by_sr(self, ojson, sr_num):
        amount_sr = len(ojson["SRForm"])
        index_target = -1
        for index in range(amount_sr):
            if sr_num == ojson['SRForm'][index]['SRF_no']:
                index_target = index
                break
        if index_target == -1:
            err_msg = f'[get_prod_ver_type_by_sr] No SR_Num is matched.'
            print(err_msg)
            self.err_msg = err_msg
            return False
        custom_name = ojson['SRForm'][index_target]['CustName']
        return custom_name

    def get_rdbuild_num_by_sr(self, ojson, sr_num):
        amount_sr = len(ojson["SRForm"])
        index_target = -1
        rd_build_no = -1
        for index in range(amount_sr):
            if sr_num == ojson['SRForm'][index]['SRF_no']:
                index_target = index
                break
        if index_target == -1:
            err_msg = f'[get_rdbuild_num_by_sr] No SR_Num is matched.'
            print(err_msg)
            self.err_msg = err_msg
            return False
        for index in range(len(ojson['SRForm'][index_target]['ProductList'])):
            rd_build_no = ojson['SRForm'][index_target]['ProductList'][index]['RDBuildNo']
            if not rd_build_no == -1:
                break
        return rd_build_no

    def get_last_valid_tr_by_sr(self, ojson, sr_num, skip_manual=False):
        # get TR list
        self.tr_no = '' # reset tr_no as empty
        amount_sr = len(ojson["SRForm"])
        index_target = -1
        if amount_sr > 0:
            for index in range(amount_sr):
                if sr_num == ojson['SRForm'][index]['SRF_no']:
                    index_target = index
                    break
            if index_target == -1:
                err_msg = f'[get_latest_valid_tr_by_sr] No SR_Num is matched.'
                print(err_msg)
                self.err_msg = err_msg
                return False
            ojson_tr_list = ojson['SRForm'][index_target]['TRList']
        else:
            err_msg = f'[get_latest_valid_tr_by_sr] NO SR List is found.'
            print(err_msg)
            self.err_msg = err_msg
            return False
        # get latest valid TR
        if len(ojson_tr_list) > 0:
            for item_tr in ojson_tr_list[::-1]:  # list tr from end
                if 'Assigned' in item_tr['Status'] or 'NewCreated' in item_tr['Status']:
                    if 'Cancel' not in item_tr['Status'] and 'Rejected' not in item_tr['Status']:
                        self.tr_no = item_tr['TRCode']
                        tr_info = self.retrieve_tr_info()
                        logger("tr_info = ", tr_info)
                        if not skip_manual or tr_info["builder"] == "SR_AUTO":
                            logger("found")
                            break
                        else:
                            self.tr_no = ''
            if self.tr_no == '':
                self.err_msg = f'[get_latest_valid_tr_by_sr] No valid TR is found in SR={sr_num}'
                return False
        else:
            err_msg = f'[get_latest_valid_tr_by_sr] NO TR List is found. SR_No={sr_num}'
            if debug_mode: print(err_msg)
            self.err_msg = err_msg
            return False
        return True

    def get_last_valid_tr_with_done_by_sr(self, ojson, sr_num, skip_manual=False):
        # get TR list
        self.tr_no = '' # reset tr_no as empty
        amount_sr = len(ojson["SRForm"])
        index_target = -1
        if amount_sr > 0:
            for index in range(amount_sr):
                if sr_num == ojson['SRForm'][index]['SRF_no']:
                    index_target = index
                    break
            if index_target == -1:
                err_msg = f'[get_latest_valid_tr_by_sr] No SR_Num is matched.'
                print(err_msg)
                self.err_msg = err_msg
                return False
            ojson_tr_list = ojson['SRForm'][index_target]['TRList']
        else:
            err_msg = f'[get_latest_valid_tr_by_sr] NO SR List is found.'
            print(err_msg)
            self.err_msg = err_msg
            return False
        # get latest valid TR
        if len(ojson_tr_list) > 0:
            for item_tr in ojson_tr_list[::-1]:  # list tr from end
                if 'Assigned' in item_tr['Status'] or 'NewCreated' in item_tr['Status'] or 'Done' in item_tr['Status']:
                    if 'Cancel' not in item_tr['Status'] and 'Rejected' not in item_tr['Status']:
                        self.tr_no = item_tr['TRCode']
                        tr_info = self.retrieve_tr_info()
                        logger("tr_info = ", tr_info)
                        if not skip_manual or tr_info["builder"] == "SR_AUTO":
                            logger("found")
                            break
                        else:
                            self.tr_no = ''
            if self.tr_no == '':
                self.err_msg = f'[get_latest_valid_tr_by_sr] No valid TR is found in SR={sr_num}'
                return False
        else:
            err_msg = f'[get_latest_valid_tr_by_sr] NO TR List is found. SR_No={sr_num}'
            if debug_mode: print(err_msg)
            self.err_msg = err_msg
            return False
        return True

    def query_latest_tr_by_sr(self): # prod_name, sr_no
        # return latest valid TR (NewCreated or Assigned with no canceled and reject)
        print('Calling query_latest_tr_by_sr')
        try:
            tr_no = ''
            # Query SR/TR list by http request
            prod_name = self.prod_name
            prod_ver = ''
            prod_ver_type = ''
            r = requests.get(
                f'https://ecl.cyberlink.com/WebService/BusinessService/ProductDevelopment/SR/SRService.asmx/QuerySRByProductName?ProdName={prod_name}&ProdVer={prod_ver}&ProdVerType={prod_ver_type}',
                auth=(self.user_name, self.password))
            result = r.text.split('org/">')
            result = result[1].replace('</string>', '')
            # parse json
            ojson = json.loads(result)
            # get TR list
            amount_sr = len(ojson["SRForm"])
            index_target = -1
            if amount_sr > 0:
                for index in range(amount_sr):
                    if self.sr_no == ojson['SRForm'][index]['SRF_no']:
                        index_target = index
                        break
                if index_target == -1:
                    err_msg = f'[query_latest_tr_by_sr] No SR_Num is matched. {prod_name=}'
                    print(err_msg)
                    self.err_msg = err_msg
                    raise Exception
                ojson_tr_list = ojson['SRForm'][index_target]['TRList']
            else:
                err_msg = f'[query_latest_tr_by_sr] NO SR List is found. {prod_name=}'
                print(err_msg)
                self.err_msg = err_msg
                raise Exception
            # get latest valid TR
            if len(ojson_tr_list) > 0:
                for item_tr in ojson_tr_list[::-1]: # list tr from end
                    if 'Assigned' in item_tr['Status'] or 'NewCreated' in item_tr['Status']:
                        if 'Cancel' not in item_tr['Status'] and 'Rejected' not in item_tr['Status']:
                            self.tr_no = item_tr['TRCode']
                            break
                if self.tr_no == '':
                    self.err_msg = '[query_latest_tr_by_sr] No valid TR is found.'
                    return False
            else:
                err_msg = f'[query_latest_tr_by_sr] NO TR List is found. SR_No={self.sr_no}'
                print(err_msg)
                self.err_msg = err_msg
                return False
        except Exception:
            raise Exception
        return True

    def download_tr_build(self, src_path, dest_path):
        logger('download_tr_build - Start')
        mount_local_folder = ''
        mount_server_path = r'//CLT-QASERVER/Testing'
        network_path = r'\\clt-qaserver'
        curr_user = ''
        try:
            # [0] check current os type
            curr_os = 'windows'
            if os.name != 'nt':
                curr_os = 'mac'
                curr_user = getpass.getuser()
                mount_local_folder = rf'/Users/{curr_user}/Desktop/my_mount'

            # [1] - Grant permission of clt-qaserver
            if curr_os == 'windows':
                if not os.path.exists(src_path):
                    print('Current OS: Windows')
                    cmd = 'NET USE ' + network_path + ' /User:' + self.user_name + ' ' + self.password
                    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                    stdout, stderr = process.communicate()
                    exit_code = process.wait()
                    print(stdout, stderr, exit_code)  # success - exit_code=0
            else:  # for mac
                print('Current OS: Mac')
                if not os.path.exists(mount_local_folder):
                    os.mkdir(mount_local_folder)
                if not os.path.ismount(mount_local_folder):
                    print('mount the local folder')
                    self.user_name = self.user_name.replace('clt\\', '')
                    os.system(f"mount_smbfs //{self.user_name}:{self.password}@clt-qaserver/Testing ~/Desktop/my_mount")
                print(f'Folder {mount_local_folder} is mounted.')

            # [2] Download build to local
            if os.path.exists(dest_path):
                shutil.rmtree(dest_path)
            if curr_os == 'mac':
                src_path = src_path.replace('\\', '/')
                src_path = src_path.replace(mount_server_path, mount_local_folder)
                print(f'{src_path=}')
            shutil.copytree(src_path, dest_path)

            # [3] Remove the permission/ unmount the folder
            if curr_os == 'mac':
                # for mac, unmount the folder and remove
                os.system(f'diskutil unmount {mount_local_folder}')
                os.rmdir(mount_local_folder)

            # do the MD5 check
            result = self._md5_check_folder(dest_path)
            if not result:
                self.err_msg = '[download_tr_build] MD5 check fail.'
                logger(f'{self.err_msg}')
                return False
        except Exception as e:
            logger(f'Exception occurs. ErrorLog={e}')
            if self.err_msg == '':
                self.err_msg = f'[download_tr_build] Exception occurs. ErrorLog={e}'
            return False
        return True

    def download_build_by_tr(self, tr_no=''):
        # Retrieve TR Info. Only support download build from \\CLT-QASERVER
        logger('download_build_by_tr - Start')
        if tr_no:
            self.tr_no = tr_no
        dict_tr_info = self.retrieve_tr_info()
        logger(f'{dict_tr_info=}')
        # Download TR Build to Destination
        src_path = dict_tr_info['prog_path']
        if 'CLT-QASERVER' not in src_path:
            self.err_msg = f'[download_build_by_tr] {src_path=} is not supported'
            logger(f'[download_build_by_tr] {src_path=} is not supported')
            return False
        if self.program_path_subfolder != '':
            src_path += '\\' + self.program_path_subfolder
        retry = 0
        result_download = False
        while retry < 3:
            if self.download_tr_build(src_path, self.dest_path):
                result_download = True
                break
            retry += 1
        if not result_download:
            return False
        logger('Download TR build completely.')
        return True

# def get_latest_build(para_dict): # only for specified tr_no or sr_no
#     print('enter get_latest_build func.')
#     dict_result = {'result': True, 'error_log': '', 'ver_type': '', 'build': ''}
#     oecl = ''
#     try:
#         # Initial object
#         oecl = Ecl_Operation(para_dict)
#         # print(f'user_name={oecl.user_name}, password={oecl.password}')
#         # Query Latest TR by SR
#         if oecl.tr_no == '':
#             oecl.query_latest_tr_by_sr()
#             # Check if TR is tested from db, if yes, skip it
#             if oecl.tr_no != '':
#                 if len(oecl.update_tr_to_db(oecl.tr_no, oecl.sr_no)) == 0:
#                     print('No new TR for testing.')
#                     dict_result['result'] = False
#                     dict_result['error_log'] = f'Latest TR {oecl.tr_no} is already tested'
#                     return dict_result # query a tr but it's already tested
#             else:
#                 dict_result['result'] = False
#                 dict_result['error_log'] = oecl.err_msg
#                 return dict_result # query no tr from sr
#         # Retrieve TR Info.
#         dict_tr_info = oecl.retrieve_tr_info()
#         dict_result['ver_type'] = dict_tr_info['ver_type']
#         dict_result['build'] = dict_tr_info['build']
#         print(f'{dict_tr_info=}')
#         # Download TR Build to Destination
#         src_path = dict_tr_info['prog_path']
#         if 'CLT-QASERVER' not in src_path:
#             print(f'[download_build_by_tr] {src_path=} is not supported')
#             dict_result['result'] = False
#             dict_result['error_log'] = f'[download_build_by_tr] {src_path=} is not supported'
#             return dict_result
#         if oecl.program_path_subfolder != '':
#             src_path += '\\' + oecl.program_path_subfolder
#         retry = 0
#         result_download = False
#         while retry < 3:
#             if oecl.download_tr_build(src_path, oecl.dest_path):
#                 result_download = True
#                 break
#             retry += 1
#         if not result_download:
#             raise Exception
#     except Exception as e:
#         print(f'Exception occurs. ErrorLog={e}')
#         dict_result['result'] = False
#         dict_result['error_log'] = oecl.err_msg
#         oecl._send_email()
#     return dict_result

def get_info_with_tr(para_dict):
    oecl = Ecl_Operation(para_dict)
    oecl.tr_no = para_dict['tr_no']
    dict_tr_info = oecl.retrieve_tr_info()

    return dict_tr_info


def get_latest_build(para_dict):
    return get_latest_tr_build(para_dict)


def get_latest_tr_build(para_dict):
    dict_result = {'result': True, 'error_log': '', 'ver_type': '', 'build': '', 'sr_no': '', 'tr_no': '',
                   'project': '', 'short_description': '', 'prog_path': ''}
    oecl = ''
    try:
        # Initial object
        oecl = Ecl_Operation(para_dict)
        if debug_mode: print(f'user_name={oecl.user_name}, password={oecl.password}')
        # Query SR DB by eCL service (w/ Product Name ONLY)
        prod_ver = oecl.prod_ver
        prod_ver_type = oecl.prod_ver_type
        oecl.prod_ver = ''
        oecl.prod_ver_type = ''
        obj_json_sr_db = oecl.query_sr_by_ecl_service()  # query sr db from ecl services
        oecl.prod_ver = prod_ver
        oecl.prod_ver_type = prod_ver_type
        sub_sr_list = oecl.get_sub_sr_list(obj_json_sr_db)
        sr_list = oecl.get_sr_list(obj_json_sr_db, oecl.filter_sr_keyword, sub_sr_list)
        if debug_mode: print(f'SR_Amount={len(obj_json_sr_db["SRForm"])}')
        if debug_mode: print(f'Total SR={len(sr_list)}')
        if debug_mode: print(f'Total SubSR={len(sub_sr_list)}')

        if oecl.sr_no == '' and oecl.tr_no == '':
            # filter by Prod_Ver, Prod_Ver_Type, Custom Name
            sr_list = oecl.filter_sr_list_by_prod_ver(obj_json_sr_db, sr_list)
            if debug_mode: print(f'[By Prod_Ver] Amount={len(sr_list)}, SR_List={sr_list}')

            sr_list = oecl.filter_sr_list_by_prod_ver_type(obj_json_sr_db, sr_list)
            if debug_mode: print(f'[By Prod_Ver_Type] Amount={len(sr_list)}, SR_List={sr_list}')

            sr_list = oecl.filter_sr_list_by_custom_name(obj_json_sr_db, sr_list)
            if debug_mode: print(f'[By Custom Name] Amount={len(sr_list)}, SR_List={sr_list}')

            # query last valid tr by sr (Sub-SR support - Not yet.)
            for curr_sr in sr_list:
                if debug_mode: print(f'Curr Master SR={curr_sr}')
                # query mode - Master SR ONLY
                if oecl.query_mode == 0:
                    if debug_mode: print(f'Query_Mode - Master SR ONLY')
                    if oecl.get_last_valid_tr_by_sr(obj_json_sr_db, curr_sr):
                        if debug_mode: print(f'New TR={oecl.tr_no} is Found.')
                        # check if TR already exists in SR DB
                        if oecl.check_if_tr_exists_in_db(oecl.tr_no, curr_sr):
                            if debug_mode: print(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                            logger(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                            continue
                        dict_result['sr_no'] = curr_sr
                        dict_result['tr_no'] = oecl.tr_no
                        break
                # query mode - Sub-SR ONLY
                elif oecl.query_mode == 1:
                    if debug_mode: print(f'Query_Mode - Sub-SR ONLY')
                    sub_sr_list = oecl.get_sub_sr_list_by_master_sr(obj_json_sr_db, curr_sr)
                    if debug_mode: print(f'{sub_sr_list=}')
                    is_found = False
                    for sub_sr in sub_sr_list:
                        if debug_mode: print(f'Curr Sub-SR={sub_sr["sub_sr"]}')
                        if oecl.get_last_valid_tr_by_sub_sr(sub_sr):
                            if debug_mode: print(f'New TR={oecl.tr_no} is Found.')
                            # check if TR already exists in SR DB
                            if oecl.check_if_tr_exists_in_db(oecl.tr_no, sub_sr['sub_sr']):
                                if debug_mode: print(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                logger(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                continue
                            is_found = True
                            dict_result['sr_no'] = sub_sr['sub_sr']
                            dict_result['tr_no'] = oecl.tr_no
                            break
                    if is_found:
                        break
                # query mode - Master+Sub-SR
                else:
                    if debug_mode: print(f'Query_Mode - Master+Sub SR')
                    is_found = False
                    if oecl.get_last_valid_tr_by_sr(obj_json_sr_db, curr_sr):
                        if debug_mode: print(f'New TR={oecl.tr_no} is Found.')
                        # check if TR already exists in SR DB
                        if oecl.check_if_tr_exists_in_db(oecl.tr_no, curr_sr):
                            if debug_mode: print(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                            logger(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                        else:
                            is_found = True
                            dict_result['sr_no'] = curr_sr
                            dict_result['tr_no'] = oecl.tr_no

                    if is_found:
                        break
                    else:
                        sub_sr_list = oecl.get_sub_sr_list_by_master_sr(obj_json_sr_db, curr_sr)
                        if sub_sr_list:
                            for sub_sr in sub_sr_list:
                                if debug_mode: print(f'Curr Sub-SR={sub_sr["sub_sr"]}')
                                if oecl.get_last_valid_tr_by_sub_sr(sub_sr):
                                    if debug_mode: print(f'New TR={oecl.tr_no} is Found.')
                                    # check if TR already exists in SR DB
                                    if oecl.check_if_tr_exists_in_db(oecl.tr_no, sub_sr['sub_sr']):
                                        if debug_mode: print(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                        logger(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                        continue
                                    is_found = True
                                    dict_result['sr_no'] = sub_sr['sub_sr']
                                    dict_result['tr_no'] = oecl.tr_no
                                    break
                            if is_found:
                                break

            if dict_result['tr_no'] == '': # query no new valid tr from sr
                dict_result['result'] = False
                dict_result['error_log'] = 'No new valid TR is found.'
                return dict_result
        else:
            # Query last valid TR by specified SR/ Sub-SR
            if oecl.tr_no == '':
                if oecl.sr_no != '':
                    # Specified SR is Master SR
                    if debug_mode: print(f'{sr_list=}')
                    is_found = False
                    if oecl.sr_no in sr_list:
                        if debug_mode: print(f'{oecl.sr_no} > Master SR')
                        if oecl.get_last_valid_tr_by_sr(obj_json_sr_db, oecl.sr_no):
                            if debug_mode: print(f'New TR={oecl.tr_no} is Found.')
                            # check if TR already exists in SR DB
                            if oecl.check_if_tr_exists_in_db(oecl.tr_no, oecl.sr_no):
                                if debug_mode: print(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                logger(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                dict_result['result'] = False
                                dict_result['error_log'] = 'No new valid TR is found.'
                                dict_result['sr_no'] = oecl.sr_no
                                return dict_result  # query no valid tr from sr
                            dict_result['sr_no'] = oecl.sr_no
                            dict_result['tr_no'] = oecl.tr_no
                            is_found = True
                        else:  # there is no valid TR in specified SR
                            dict_result['result'] = False
                            dict_result['error_log'] = 'No valid TR is found.'
                            dict_result['sr_no'] = oecl.sr_no
                            return dict_result  # query no valid tr from sr

                    # Specified SR is Sub-SR
                    if not is_found:
                        for master_sr in sr_list:
                            sub_sr_list = oecl.get_sub_sr_list_by_master_sr(obj_json_sr_db, master_sr)
                            for sub_sr in sub_sr_list:
                                if oecl.sr_no == sub_sr['sub_sr']:
                                    if debug_mode: print(f'{oecl.sr_no} > Sub-SR')
                                    is_found = True
                                    if oecl.get_last_valid_tr_by_sub_sr(sub_sr):
                                        if debug_mode: print(f'New TR={oecl.tr_no} is Found.')
                                        # check if TR already exists in SR DB
                                        if oecl.check_if_tr_exists_in_db(oecl.tr_no, oecl.sr_no):
                                            if debug_mode: print(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                            logger(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                            dict_result['result'] = False
                                            dict_result['error_log'] = 'No new valid TR is found.'
                                            dict_result['sr_no'] = oecl.sr_no
                                            return dict_result  # query no valid tr from sr
                                        dict_result['sr_no'] = oecl.sr_no
                                        dict_result['tr_no'] = oecl.tr_no
                                        break
                                    else:  # there is no valid TR in specified SR
                                        dict_result['result'] = False
                                        dict_result['error_log'] = 'No valid TR is found.'
                                        dict_result['sr_no'] = oecl.sr_no
                                        return dict_result  # query no valid tr from sr
                            if is_found:
                                break
                    if not is_found: # the specified SR is not in current sr list
                        dict_result['result'] = False
                        dict_result['error_log'] = 'Invalid SR (not in current list)'
                        dict_result['sr_no'] = oecl.sr_no
                        return dict_result

        # Retrieve TR Info.
        dict_tr_info = oecl.retrieve_tr_info()
        dict_result['ver_type'] = dict_tr_info['ver_type']
        dict_result['build'] = dict_tr_info['build']
        dict_result['sr_no'] = dict_tr_info['sr_no']
        dict_result['tr_no'] = dict_tr_info['tr_no']
        dict_result['project'] = dict_tr_info['project']
        dict_result['short_description'] = dict_tr_info['short_description']
        dict_result['prog_path'] = dict_tr_info['prog_path']
        logger(f'{dict_tr_info=}')
        if debug_mode:
            if oecl.tr_no:
                oecl.add_tr_to_db(dict_result['sr_no'], dict_result['tr_no'])
            return dict_result

        # Download TR Build to Destination
        src_path = dict_tr_info['prog_path']
        if 'CLT-QASERVER' not in src_path: # Currently, only support download from CLT-QASERVER
            if debug_mode: print(f'[download_build_by_tr] {src_path=} is not supported')
            dict_result['result'] = False
            dict_result['error_log'] = f'[download_build_by_tr] {src_path=} is not supported'
            return dict_result
        if oecl.program_path_subfolder != '':
            src_path += '\\' + oecl.program_path_subfolder
        retry = 0
        result_download = False
        while retry < 3:
            if oecl.download_tr_build(src_path, oecl.dest_path):
                result_download = True
                break
            retry += 1
        if not result_download:
            raise Exception
        # add tr_no to db after downloaded successfully
        oecl.add_tr_to_db(dict_result['sr_no'], dict_result['tr_no'])
    except Exception as e:
        logger(f'Exception occurs. ErrorLog={e}')
        dict_result['result'] = False
        dict_result['error_log'] = oecl.err_msg
    return dict_result


def get_latest_tr_data(para_dict, skip_manual=False):
    dict_result = {'result': True, 'error_log': '', 'ver_type': '', 'build': '', 'sr_no': '', 'tr_no': '',
                   'project': '', 'short_description': '', 'prog_path': ''}
    oecl = ''
    try:
        # Initial object
        oecl = Ecl_Operation(para_dict)
        if debug_mode: print(f'user_name={oecl.user_name}, password={oecl.password}')
        # Query SR DB by eCL service (w/ Product Name ONLY)
        prod_ver = oecl.prod_ver
        prod_ver_type = oecl.prod_ver_type
        oecl.prod_ver = ''
        oecl.prod_ver_type = ''
        obj_json_sr_db = oecl.query_sr_by_ecl_service()  # query sr db from ecl services
        oecl.prod_ver = prod_ver
        oecl.prod_ver_type = prod_ver_type
        sub_sr_list = oecl.get_sub_sr_list(obj_json_sr_db)
        sr_list = oecl.get_sr_list(obj_json_sr_db, oecl.filter_sr_keyword, sub_sr_list)
        if debug_mode: print(f'SR_Amount={len(obj_json_sr_db["SRForm"])}')
        if debug_mode: print(f'Total SR={len(sr_list)}')
        if debug_mode: print(f'Total SubSR={len(sub_sr_list)}')

        if oecl.sr_no == '' and oecl.tr_no == '':
            # filter by Prod_Ver, Prod_Ver_Type, Custom Name
            sr_list = oecl.filter_sr_list_by_prod_ver(obj_json_sr_db, sr_list)
            if debug_mode: print(f'[By Prod_Ver] Amount={len(sr_list)}, SR_List={sr_list}')

            sr_list = oecl.filter_sr_list_by_prod_ver_type(obj_json_sr_db, sr_list)
            if debug_mode: print(f'[By Prod_Ver_Type] Amount={len(sr_list)}, SR_List={sr_list}')

            sr_list = oecl.filter_sr_list_by_custom_name(obj_json_sr_db, sr_list)
            if debug_mode: print(f'[By Custom Name] Amount={len(sr_list)}, SR_List={sr_list}')

            # query last valid tr by sr (Sub-SR support - Not yet.)
            for curr_sr in sr_list:
                if debug_mode: print(f'Curr Master SR={curr_sr}')
                # query mode - Master SR ONLY
                if oecl.query_mode == 0:
                    if debug_mode: print(f'Query_Mode - Master SR ONLY')
                    if oecl.get_last_valid_tr_by_sr(obj_json_sr_db, curr_sr, skip_manual):
                        if debug_mode: print(f'New TR={oecl.tr_no} is Found.')
                        # check if TR already exists in SR DB
                        if oecl.check_if_tr_exists_in_db(oecl.tr_no, curr_sr):
                            if debug_mode: print(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                            logger(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                            continue
                        dict_result['sr_no'] = curr_sr
                        dict_result['tr_no'] = oecl.tr_no
                        break
                # query mode - Sub-SR ONLY
                elif oecl.query_mode == 1:
                    if debug_mode: print(f'Query_Mode - Sub-SR ONLY')
                    sub_sr_list = oecl.get_sub_sr_list_by_master_sr(obj_json_sr_db, curr_sr)
                    if debug_mode: print(f'{sub_sr_list=}')
                    is_found = False
                    for sub_sr in sub_sr_list:
                        if debug_mode: print(f'Curr Sub-SR={sub_sr["sub_sr"]}')
                        if oecl.get_last_valid_tr_by_sub_sr(sub_sr, skip_manual):
                            if debug_mode: print(f'New TR={oecl.tr_no} is Found.')
                            # check if TR already exists in SR DB
                            if oecl.check_if_tr_exists_in_db(oecl.tr_no, sub_sr['sub_sr']):
                                if debug_mode: print(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                logger(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                continue
                            is_found = True
                            dict_result['sr_no'] = sub_sr['sub_sr']
                            dict_result['tr_no'] = oecl.tr_no
                            break
                    if is_found:
                        break
                # query mode - Master+Sub-SR
                else:
                    if debug_mode: print(f'Query_Mode - Master+Sub SR')
                    is_found = False
                    if oecl.get_last_valid_tr_by_sr(obj_json_sr_db, curr_sr, skip_manual):
                        if debug_mode: print(f'New TR={oecl.tr_no} is Found.')
                        # check if TR already exists in SR DB
                        if oecl.check_if_tr_exists_in_db(oecl.tr_no, curr_sr):
                            if debug_mode: print(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                            logger(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                        else:
                            is_found = True
                            dict_result['sr_no'] = curr_sr
                            dict_result['tr_no'] = oecl.tr_no

                    if is_found:
                        break
                    else:
                        sub_sr_list = oecl.get_sub_sr_list_by_master_sr(obj_json_sr_db, curr_sr)
                        if sub_sr_list:
                            for sub_sr in sub_sr_list:
                                if debug_mode: print(f'Curr Sub-SR={sub_sr["sub_sr"]}')
                                if oecl.get_last_valid_tr_by_sub_sr(sub_sr, skip_manual):
                                    if debug_mode: print(f'New TR={oecl.tr_no} is Found.')
                                    # check if TR already exists in SR DB
                                    if oecl.check_if_tr_exists_in_db(oecl.tr_no, sub_sr['sub_sr']):
                                        if debug_mode: print(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                        logger(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                        continue
                                    is_found = True
                                    dict_result['sr_no'] = sub_sr['sub_sr']
                                    dict_result['tr_no'] = oecl.tr_no
                                    break
                            if is_found:
                                break

            if dict_result['tr_no'] == '': # query no new valid tr from sr
                dict_result['result'] = False
                dict_result['error_log'] = 'No new valid TR is found.'
                return dict_result
        else:
            # Query last valid TR by specified SR/ Sub-SR
            if oecl.tr_no == '':
                if oecl.sr_no != '':
                    # Specified SR is Master SR
                    if debug_mode: print(f'{sr_list=}')
                    is_found = False
                    if oecl.sr_no in sr_list:
                        if debug_mode: print(f'{oecl.sr_no} > Master SR')
                        if oecl.get_last_valid_tr_by_sr(obj_json_sr_db, oecl.sr_no, skip_manual):
                            if debug_mode: print(f'New TR={oecl.tr_no} is Found.')
                            # check if TR already exists in SR DB
                            if oecl.check_if_tr_exists_in_db(oecl.tr_no, oecl.sr_no):
                                if debug_mode: print(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                logger(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                dict_result['result'] = False
                                dict_result['error_log'] = 'No new valid TR is found.'
                                dict_result['sr_no'] = oecl.sr_no
                                return dict_result  # query no valid tr from sr
                            dict_result['sr_no'] = oecl.sr_no
                            dict_result['tr_no'] = oecl.tr_no
                            is_found = True
                        else:  # there is no valid TR in specified SR
                            dict_result['result'] = False
                            dict_result['error_log'] = 'No valid TR is found.'
                            dict_result['sr_no'] = oecl.sr_no
                            return dict_result  # query no valid tr from sr

                    # Specified SR is Sub-SR
                    if not is_found:
                        for master_sr in sr_list:
                            sub_sr_list = oecl.get_sub_sr_list_by_master_sr(obj_json_sr_db, master_sr)
                            for sub_sr in sub_sr_list:
                                if oecl.sr_no == sub_sr['sub_sr']:
                                    if debug_mode: print(f'{oecl.sr_no} > Sub-SR')
                                    is_found = True
                                    if oecl.get_last_valid_tr_by_sub_sr(sub_sr, skip_manual):
                                        if debug_mode: print(f'New TR={oecl.tr_no} is Found.')
                                        # check if TR already exists in SR DB
                                        if oecl.check_if_tr_exists_in_db(oecl.tr_no, oecl.sr_no):
                                            if debug_mode: print(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                            logger(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                            dict_result['result'] = False
                                            dict_result['error_log'] = 'No new valid TR is found.'
                                            dict_result['sr_no'] = oecl.sr_no
                                            return dict_result  # query no valid tr from sr
                                        dict_result['sr_no'] = oecl.sr_no
                                        dict_result['tr_no'] = oecl.tr_no
                                        break
                                    else:  # there is no valid TR in specified SR
                                        dict_result['result'] = False
                                        dict_result['error_log'] = 'No valid TR is found.'
                                        dict_result['sr_no'] = oecl.sr_no
                                        return dict_result  # query no valid tr from sr
                            if is_found:
                                break
                    if not is_found: # the specified SR is not in current sr list
                        dict_result['result'] = False
                        dict_result['error_log'] = 'Invalid SR (not in current list)'
                        dict_result['sr_no'] = oecl.sr_no
                        return dict_result

        # Retrieve TR Info.
        dict_tr_info = oecl.retrieve_tr_info()
        dict_result['ver_type'] = dict_tr_info['ver_type']
        dict_result['build'] = dict_tr_info['build']
        dict_result['sr_no'] = dict_tr_info['sr_no']
        dict_result['tr_no'] = dict_tr_info['tr_no']
        dict_result['project'] = dict_tr_info['project']
        dict_result['short_description'] = dict_tr_info['short_description']
        dict_result['prog_path'] = dict_tr_info['prog_path']
        dict_result['creation_time'] = dict_tr_info['creation_time']
        logger(f'{dict_tr_info=}')
    except Exception as e:
        logger(f'Exception occurs. ErrorLog={e}')
        dict_result['result'] = False
        dict_result['error_log'] = oecl.err_msg
    return dict_result


def get_latest_tr_with_done_data(para_dict, skip_manual=False):
    dict_result = {'result': True, 'error_log': '', 'ver_type': '', 'build': '', 'sr_no': '', 'tr_no': '',
                   'project': '', 'short_description': '', 'prog_path': ''}
    oecl = ''
    try:
        # Initial object
        oecl = Ecl_Operation(para_dict)
        if debug_mode: print(f'user_name={oecl.user_name}, password={oecl.password}')
        # Query SR DB by eCL service (w/ Product Name ONLY)
        prod_ver = oecl.prod_ver
        prod_ver_type = oecl.prod_ver_type
        oecl.prod_ver = ''
        oecl.prod_ver_type = ''
        obj_json_sr_db = oecl.query_sr_by_ecl_service()  # query sr db from ecl services
        oecl.prod_ver = prod_ver
        oecl.prod_ver_type = prod_ver_type
        sub_sr_list = oecl.get_sub_sr_list(obj_json_sr_db)
        sr_list = oecl.get_sr_list(obj_json_sr_db, oecl.filter_sr_keyword, sub_sr_list)
        if debug_mode: print(f'SR_Amount={len(obj_json_sr_db["SRForm"])}')
        if debug_mode: print(f'Total SR={len(sr_list)}')
        if debug_mode: print(f'Total SubSR={len(sub_sr_list)}')

        if oecl.sr_no == '' and oecl.tr_no == '':
            # filter by Prod_Ver, Prod_Ver_Type, Custom Name
            sr_list = oecl.filter_sr_list_by_prod_ver(obj_json_sr_db, sr_list)
            if debug_mode: print(f'[By Prod_Ver] Amount={len(sr_list)}, SR_List={sr_list}')

            sr_list = oecl.filter_sr_list_by_prod_ver_type(obj_json_sr_db, sr_list)
            if debug_mode: print(f'[By Prod_Ver_Type] Amount={len(sr_list)}, SR_List={sr_list}')

            sr_list = oecl.filter_sr_list_by_custom_name(obj_json_sr_db, sr_list)
            if debug_mode: print(f'[By Custom Name] Amount={len(sr_list)}, SR_List={sr_list}')

            # query last valid tr by sr (Sub-SR support - Not yet.)
            for curr_sr in sr_list:
                if debug_mode: print(f'Curr Master SR={curr_sr}')
                # query mode - Master SR ONLY
                if oecl.query_mode == 0:
                    if debug_mode: print(f'Query_Mode - Master SR ONLY')
                    if oecl.get_last_valid_tr_with_done_by_sr(obj_json_sr_db, curr_sr, skip_manual):
                        if debug_mode: print(f'New TR={oecl.tr_no} is Found.')
                        # check if TR already exists in SR DB
                        if oecl.check_if_tr_exists_in_db(oecl.tr_no, curr_sr):
                            if debug_mode: print(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                            logger(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                            continue
                        dict_result['sr_no'] = curr_sr
                        dict_result['tr_no'] = oecl.tr_no
                        break
                # query mode - Sub-SR ONLY
                elif oecl.query_mode == 1:
                    if debug_mode: print(f'Query_Mode - Sub-SR ONLY')
                    sub_sr_list = oecl.get_sub_sr_list_by_master_sr(obj_json_sr_db, curr_sr)
                    if debug_mode: print(f'{sub_sr_list=}')
                    is_found = False
                    for sub_sr in sub_sr_list:
                        if debug_mode: print(f'Curr Sub-SR={sub_sr["sub_sr"]}')
                        if oecl.get_last_valid_tr_with_done_by_sub_sr(sub_sr, skip_manual):
                            if debug_mode: print(f'New TR={oecl.tr_no} is Found.')
                            # check if TR already exists in SR DB
                            if oecl.check_if_tr_exists_in_db(oecl.tr_no, sub_sr['sub_sr']):
                                if debug_mode: print(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                logger(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                continue
                            is_found = True
                            dict_result['sr_no'] = sub_sr['sub_sr']
                            dict_result['tr_no'] = oecl.tr_no
                            break
                    if is_found:
                        break
                # query mode - Master+Sub-SR
                else:
                    if debug_mode: print(f'Query_Mode - Master+Sub SR')
                    is_found = False
                    if oecl.get_last_valid_tr_with_done_by_sr(obj_json_sr_db, curr_sr, skip_manual):
                        if debug_mode: print(f'New TR={oecl.tr_no} is Found.')
                        # check if TR already exists in SR DB
                        if oecl.check_if_tr_exists_in_db(oecl.tr_no, curr_sr):
                            if debug_mode: print(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                            logger(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                        else:
                            is_found = True
                            dict_result['sr_no'] = curr_sr
                            dict_result['tr_no'] = oecl.tr_no

                    if is_found:
                        break
                    else:
                        sub_sr_list = oecl.get_sub_sr_list_by_master_sr(obj_json_sr_db, curr_sr)
                        if sub_sr_list:
                            for sub_sr in sub_sr_list:
                                if debug_mode: print(f'Curr Sub-SR={sub_sr["sub_sr"]}')
                                if oecl.get_last_valid_tr_with_done_by_sub_sr(sub_sr, skip_manual):
                                    if debug_mode: print(f'New TR={oecl.tr_no} is Found.')
                                    # check if TR already exists in SR DB
                                    if oecl.check_if_tr_exists_in_db(oecl.tr_no, sub_sr['sub_sr']):
                                        if debug_mode: print(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                        logger(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                        continue
                                    is_found = True
                                    dict_result['sr_no'] = sub_sr['sub_sr']
                                    dict_result['tr_no'] = oecl.tr_no
                                    break
                            if is_found:
                                break

            if dict_result['tr_no'] == '': # query no new valid tr from sr
                dict_result['result'] = False
                dict_result['error_log'] = 'No new valid TR is found.'
                return dict_result
        else:
            # Query last valid TR by specified SR/ Sub-SR
            if oecl.tr_no == '':
                if oecl.sr_no != '':
                    # Specified SR is Master SR
                    if debug_mode: print(f'{sr_list=}')
                    is_found = False
                    if oecl.sr_no in sr_list:
                        if debug_mode: print(f'{oecl.sr_no} > Master SR')
                        if oecl.get_last_valid_tr_with_done_by_sr(obj_json_sr_db, oecl.sr_no, skip_manual):
                            if debug_mode: print(f'New TR={oecl.tr_no} is Found.')
                            # check if TR already exists in SR DB
                            if oecl.check_if_tr_exists_in_db(oecl.tr_no, oecl.sr_no):
                                if debug_mode: print(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                logger(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                dict_result['result'] = False
                                dict_result['error_log'] = 'No new valid TR is found.'
                                dict_result['sr_no'] = oecl.sr_no
                                return dict_result  # query no valid tr from sr
                            dict_result['sr_no'] = oecl.sr_no
                            dict_result['tr_no'] = oecl.tr_no
                            is_found = True
                        else:  # there is no valid TR in specified SR
                            dict_result['result'] = False
                            dict_result['error_log'] = 'No valid TR is found.'
                            dict_result['sr_no'] = oecl.sr_no
                            return dict_result  # query no valid tr from sr

                    # Specified SR is Sub-SR
                    if not is_found:
                        for master_sr in sr_list:
                            sub_sr_list = oecl.get_sub_sr_list_by_master_sr(obj_json_sr_db, master_sr)
                            for sub_sr in sub_sr_list:
                                if oecl.sr_no == sub_sr['sub_sr']:
                                    if debug_mode: print(f'{oecl.sr_no} > Sub-SR')
                                    is_found = True
                                    if oecl.get_last_valid_tr_with_done_by_sub_sr(sub_sr, skip_manual):
                                        if debug_mode: print(f'New TR={oecl.tr_no} is Found.')
                                        # check if TR already exists in SR DB
                                        if oecl.check_if_tr_exists_in_db(oecl.tr_no, oecl.sr_no):
                                            if debug_mode: print(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                            logger(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                            dict_result['result'] = False
                                            dict_result['error_log'] = 'No new valid TR is found.'
                                            dict_result['sr_no'] = oecl.sr_no
                                            return dict_result  # query no valid tr from sr
                                        dict_result['sr_no'] = oecl.sr_no
                                        dict_result['tr_no'] = oecl.tr_no
                                        break
                                    else:  # there is no valid TR in specified SR
                                        dict_result['result'] = False
                                        dict_result['error_log'] = 'No valid TR is found.'
                                        dict_result['sr_no'] = oecl.sr_no
                                        return dict_result  # query no valid tr from sr
                            if is_found:
                                break
                    if not is_found: # the specified SR is not in current sr list
                        dict_result['result'] = False
                        dict_result['error_log'] = 'Invalid SR (not in current list)'
                        dict_result['sr_no'] = oecl.sr_no
                        return dict_result

        # Retrieve TR Info.
        dict_tr_info = oecl.retrieve_tr_info()
        dict_result['ver_type'] = dict_tr_info['ver_type']
        dict_result['build'] = dict_tr_info['build']
        dict_result['sr_no'] = dict_tr_info['sr_no']
        dict_result['tr_no'] = dict_tr_info['tr_no']
        dict_result['project'] = dict_tr_info['project']
        dict_result['short_description'] = dict_tr_info['short_description']
        dict_result['prog_path'] = dict_tr_info['prog_path']
        dict_result['creation_time'] = dict_tr_info['creation_time']
        logger(f'{dict_tr_info=}')
    except Exception as e:
        logger(f'Exception occurs. ErrorLog={e}')
        dict_result['result'] = False
        dict_result['error_log'] = oecl.err_msg
    return dict_result


def get_valid_tr_data(para_dict, skip_manual=False):
    valid_tr_list = []
    dict_result = {'sr_no': '', 'tr_no': ''}
    oecl = ''
    try:
        # Initial object
        logger("para_dict = ", para_dict)
        oecl = Ecl_Operation(para_dict)
        if debug_mode: print(f'user_name={oecl.user_name}, password={oecl.password}')
        # Query SR DB by eCL service (w/ Product Name ONLY)
        prod_ver = oecl.prod_ver
        prod_ver_type = oecl.prod_ver_type
        oecl.prod_ver = ''
        oecl.prod_ver_type = ''
        obj_json_sr_db = oecl.query_sr_by_ecl_service()  # query sr db from ecl services
        oecl.prod_ver = prod_ver
        oecl.prod_ver_type = prod_ver_type
        sub_sr_list = oecl.get_sub_sr_list(obj_json_sr_db)
        sr_list = oecl.get_sr_list(obj_json_sr_db, oecl.filter_sr_keyword, sub_sr_list)
        if debug_mode: print(f'SR_Amount={len(obj_json_sr_db["SRForm"])}')
        if debug_mode: print(f'Total SR={len(sr_list)}')
        if debug_mode: print(f'Total SubSR={len(sub_sr_list)}')
        logger('sr_list = ', sr_list)
        logger('sub_sr_list = ', sub_sr_list)

        if oecl.sr_no == '' and oecl.tr_no == '':
            # filter by Prod_Ver, Prod_Ver_Type, Custom Name
            sr_list = oecl.filter_sr_list_by_prod_ver(obj_json_sr_db, sr_list)
            if debug_mode: print(f'[By Prod_Ver] Amount={len(sr_list)}, SR_List={sr_list}')

            sr_list = oecl.filter_sr_list_by_prod_ver_type(obj_json_sr_db, sr_list)
            if debug_mode: print(f'[By Prod_Ver_Type] Amount={len(sr_list)}, SR_List={sr_list}')

            sr_list = oecl.filter_sr_list_by_custom_name(obj_json_sr_db, sr_list)
            if debug_mode: print(f'[By Custom Name] Amount={len(sr_list)}, SR_List={sr_list}')

            # query last valid tr by sr (Sub-SR support - Not yet.)
            for curr_sr in sr_list:
                if debug_mode: print(f'Curr Master SR={curr_sr}')
                # query mode - Master SR ONLY
                if oecl.query_mode == 0:
                    if debug_mode: print(f'Query_Mode - Master SR ONLY')
                    if oecl.get_last_valid_tr_by_sr(obj_json_sr_db, curr_sr, skip_manual):
                        if debug_mode: print(f'New TR={oecl.tr_no} is Found.')
                        # check if TR already exists in SR DB
                        if oecl.check_if_tr_exists_in_db(oecl.tr_no, curr_sr):
                            if debug_mode: print(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                            logger(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                            continue
                        dict_result['sr_no'] = curr_sr
                        dict_result['tr_no'] = oecl.tr_no
                        dict_result['prod_ver'] = oecl.prod_ver
                        logger("dict_result = ", dict_result)
                        valid_tr_list.append(dict_result.copy())
                        continue
                # query mode - Sub-SR ONLY
                elif oecl.query_mode == 1:
                    if debug_mode: print(f'Query_Mode - Sub-SR ONLY')
                    sub_sr_list = oecl.get_sub_sr_list_by_master_sr(obj_json_sr_db, curr_sr)
                    if debug_mode: print(f'{sub_sr_list=}')
                    for sub_sr in sub_sr_list:
                        if debug_mode: print(f'Curr Sub-SR={sub_sr["sub_sr"]}')
                        if oecl.get_last_valid_tr_by_sub_sr(sub_sr, skip_manual):
                            if debug_mode: print(f'New TR={oecl.tr_no} is Found.')
                            # check if TR already exists in SR DB
                            if oecl.check_if_tr_exists_in_db(oecl.tr_no, sub_sr['sub_sr']):
                                if debug_mode: print(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                logger(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                logger("continue")
                                continue
                            dict_result['sr_no'] = sub_sr['sub_sr']
                            dict_result['tr_no'] = oecl.tr_no
                            dict_result['prod_ver'] = oecl.prod_ver
                            logger("dict_result = ", dict_result)
                            valid_tr_list.append(dict_result.copy())
                # query mode - Master+Sub-SR
                else:
                    if debug_mode: print(f'Query_Mode - Master+Sub SR')
                    if oecl.get_last_valid_tr_by_sr(obj_json_sr_db, curr_sr, skip_manual):
                        if debug_mode: print(f'New TR={oecl.tr_no} is Found.')
                        # check if TR already exists in SR DB
                        if oecl.check_if_tr_exists_in_db(oecl.tr_no, curr_sr):
                            if debug_mode: print(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                            logger(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                        else:
                            dict_result['sr_no'] = curr_sr
                            dict_result['tr_no'] = oecl.tr_no
                            dict_result['prod_ver'] = oecl.prod_ver
                            logger("dict_result = ", dict_result)
                            valid_tr_list.append(dict_result.copy())

                    sub_sr_list = oecl.get_sub_sr_list_by_master_sr(obj_json_sr_db, curr_sr)
                    if sub_sr_list:
                        for sub_sr in sub_sr_list:
                            if debug_mode: print(f'Curr Sub-SR={sub_sr["sub_sr"]}')
                            if oecl.get_last_valid_tr_by_sub_sr(sub_sr, skip_manual):
                                if debug_mode: print(f'New TR={oecl.tr_no} is Found.')
                                # check if TR already exists in SR DB
                                if oecl.check_if_tr_exists_in_db(oecl.tr_no, sub_sr['sub_sr']):
                                    if debug_mode: print(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                    logger(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                    continue
                                dict_result['sr_no'] = sub_sr['sub_sr']
                                dict_result['tr_no'] = oecl.tr_no
                                dict_result['prod_ver'] = oecl.prod_ver
                                logger("dict_result = ", dict_result)
                                valid_tr_list.append(dict_result.copy())
        else:
            # Query last valid TR by specified SR/ Sub-SR
            if oecl.tr_no == '':
                if oecl.sr_no != '':
                    # Specified SR is Master SR
                    if debug_mode: print(f'{sr_list=}')
                    is_found = False
                    if oecl.sr_no in sr_list:
                        if debug_mode: print(f'{oecl.sr_no} > Master SR')
                        if oecl.get_last_valid_tr_by_sr(obj_json_sr_db, oecl.sr_no, skip_manual):
                            if debug_mode: print(f'New TR={oecl.tr_no} is Found.')
                            # check if TR already exists in SR DB
                            if oecl.check_if_tr_exists_in_db(oecl.tr_no, oecl.sr_no):
                                if debug_mode: print(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                logger(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                            else:
                                dict_result['sr_no'] = oecl.sr_no
                                dict_result['tr_no'] = oecl.tr_no
                                dict_result['prod_ver'] = oecl.prod_ver
                                logger("dict_result = ", dict_result)
                                valid_tr_list.append(dict_result.copy())
                                is_found = True

                    # Specified SR is Sub-SR
                    if not is_found:
                        for master_sr in sr_list:
                            sub_sr_list = oecl.get_sub_sr_list_by_master_sr(obj_json_sr_db, master_sr)
                            for sub_sr in sub_sr_list:
                                if oecl.sr_no == sub_sr['sub_sr']:
                                    if debug_mode: print(f'{oecl.sr_no} > Sub-SR')
                                    is_found = True
                                    if oecl.get_last_valid_tr_by_sub_sr(sub_sr, skip_manual):
                                        if debug_mode: print(f'New TR={oecl.tr_no} is Found.')
                                        # check if TR already exists in SR DB
                                        if oecl.check_if_tr_exists_in_db(oecl.tr_no, oecl.sr_no):
                                            if debug_mode: print(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                            logger(f'TR={oecl.tr_no} already exists in DB. Skip it.')
                                            continue
                                        dict_result['sr_no'] = oecl.sr_no
                                        dict_result['tr_no'] = oecl.tr_no
                                        dict_result['prod_ver'] = oecl.prod_ver
                                        logger("dict_result = ", dict_result)
                                        valid_tr_list.append(dict_result.copy())
                                        continue
                    if not is_found: # the specified SR is not in current sr list
                        logger(f"the specified SR {oecl.sr_no} is not in current sr list")

        logger("valid_tr_list = ", valid_tr_list)
    except Exception as e:
        logger(f'Exception occurs. ErrorLog={e}')
    return valid_tr_list


def dump_sr_db(para_dict):
    oecl = ''
    try:
        # Initial object
        oecl = Ecl_Operation(para_dict)
        # Query SR DB by eCL service (w/ Product Name ONLY)
        prod_ver = oecl.prod_ver
        prod_ver_type = oecl.prod_ver_type
        oecl.prod_ver = ''
        oecl.prod_ver_type = ''
        obj_json_sr_db = oecl.query_sr_by_ecl_service()  # query sr db from ecl services
        oecl.prod_ver = prod_ver
        oecl.prod_ver_type = prod_ver_type
        sub_sr_list = oecl.get_sub_sr_list(obj_json_sr_db)
        sr_list = oecl.get_sr_list(obj_json_sr_db)
        prod_ver_type_list = set()

        print("="*10)
        print(f'<< Amount of SR (in Level #1): {len(obj_json_sr_db["SRForm"])} >>')
        print(" ")

        master_sr_list_in_level_1 = []
        sub_sr_list_in_level_1 = []
        master_sr_result = []
        master_sr_all_result = []
        sub_sr_result = []
        amount_of_sub_sr = 0

        # Master SR
        index = 0
        for sr in sr_list:
            # get level 1 Master SR and SubSR list
            if oecl.filter_sr_keyword in sr:
                if sr in sub_sr_list:
                    sub_sr_list_in_level_1.append(f'[{index}] {sr}')
                else:
                    master_sr_list_in_level_1.append(f'[{index}] {sr}')

            sub_sr_list_of_master = []
            if sr in sub_sr_list or oecl.filter_sr_keyword not in sr:
                index += 1
                continue
            oecl.get_last_valid_tr_by_sr(obj_json_sr_db, sr)
            prod_ver_type_list.add(oecl.get_prod_ver_type_by_sr(obj_json_sr_db, sr))
            value = f'[{index}] {sr} - RDBuildNo:{oecl.get_rdbuild_num_by_sr(obj_json_sr_db, sr)}, ProdVer:{oecl.get_prod_ver_by_sr(obj_json_sr_db, sr)}, ProdVerType:{oecl.get_prod_ver_type_by_sr(obj_json_sr_db, sr)}, TR:{oecl.tr_no}'
            master_sr_all_result.append(value)
            if oecl.tr_no:
                master_sr_result.append(value)

            # SubSR
            sub_sr_list_of_master = oecl.get_sub_sr_list_by_master_sr(obj_json_sr_db, sr)
            if sub_sr_list_of_master:
                for sub_sr in sub_sr_list_of_master:
                    oecl.get_last_valid_tr_by_sub_sr(sub_sr)
                    if oecl.tr_no:
                        sub_sr_record = f"[{index}] Master SR:{sr}, SubSR:{sub_sr['sub_sr']}, TR:{oecl.tr_no}"
                        sub_sr_result.append(sub_sr_record)
                    amount_of_sub_sr += 1
            index += 1

        # All SR in Level 1
        print(f'A. All SR in Level #1 [Amount: {len(sr_list)}]')
        index = 0
        for record in sr_list:
            print(f'[{index}] {record}')
            index += 1
        print('='*10)

        # filter SubSR in Level1
        sr_list = oecl.get_sr_list(obj_json_sr_db, oecl.filter_sr_keyword, sub_sr_list)
        print(f"\nB. Master SR (filtered with keyword: {oecl.filter_sr_keyword})  [Amount:{len(sr_list)}]")
        print(f'(1) SR List List in Level #1 [Amount:{len(master_sr_list_in_level_1)}]:')
        for record in master_sr_list_in_level_1:
            print(record)

        print(f'\n(2) SR List Info:')
        for record in master_sr_all_result:
            print(record)

        print(f'\n(3) SR List with valid TR:')
        for record in master_sr_result:
            print(record)

        print(f'\n(4) ProdVerType List of SR:')
        print(f'> {list(prod_ver_type_list)}')

        print('=' * 10)
        print('\n')
        print(f'C. SubSR  [Amount:{amount_of_sub_sr}]')
        print(f'(1) SubSR List in Level #1 [Amount:{len(sub_sr_list_in_level_1)}]:')
        for record in sub_sr_list_in_level_1:
            print(record)

        print(f'\n(2) SR List with valid TR:')
        for record in sub_sr_result:
            print(record)

    except Exception as e:
        print(f'Exception occurs. Error={e}')
        raise Exception
    return True

if __name__ == '__main__':
    if len(sys.argv) == 2:
        print(f'parameter={sys.argv[1]}')
        print(f'type(sys.argv[1])={type(sys.argv[1])}')
        para_dict = eval(sys.argv[1])
        print(f'type(para_dict)={type(para_dict)}')
        result_dict = get_latest_tr_build(para_dict)
        # output to return INI file
        print(f'{result_dict=}')
        conf = ConfigParser()
        cfgpath = '\\'.join([para_dict['work_dir'], 'result'])
        conf.add_section('RETURN')
        conf.set('RETURN', 'result', str(result_dict['result']))
        conf.set('RETURN', 'error_log', result_dict['error_log'])
        conf.set('RETURN', 'ver_type', result_dict['ver_type'])
        conf.set('RETURN', 'build', result_dict['build'])
        conf.set('RETURN', 'sr_no', result_dict['sr_no'])
        conf.set('RETURN', 'tr_no', result_dict['tr_no'])
        conf.write(open(cfgpath, "w"))
        sys.exit(0)
    else:
        print(f'Error parameter format. E.g. main.py str_in_dict_format. len(sys.argv[1])={len(sys.argv[1])}')
        sys.exit(1)