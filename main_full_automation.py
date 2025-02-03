
import os
import subprocess
import sys
import platform
import re
from send_mail.send_report import send_report
from ATFramework.utils._ecl_operation import ecl_operation
from ATFramework.utils.cl_build_operation import install_build
from configs import app_config
import configparser

# Script Info.
script_name = 'MacPDR_SFT'
script_version = '1.0.0'

# Device Settings =======================================
device_udid = ['0000']

# Project Settings ======================================
project_name = 'ATFramework_MacPDR'
test_case_folder_name = 'SFT'
test_case_main_file = 'main.py'

# Build Info. (for Auto Download Build) ==========================================
# sr_no = 'VDM202102-01'
# sr_no = ''
# tr_no = 'TR210129-025'
# tr_no = ''
package_file_name = ""
# package_name = 'com.cyberlink.powerdirector'

# Mail Settings ========================================
title_project = 'MacPDR'
#receiver_list = ["jim_huang@cyberlink.com", "biaggi_li@cyberlink.com", "terence_chang@cyberlink.com"]
receiver_list = ["jim_huang@cyberlink.com"]

# Test Case Module Individual Execution Log Settings ======================================
enable_case_execution_log = 1
# ======================================================

#execute via pytest
def __run_test(udid, sr_no, tr_no, build_ver, build_num, build_file, device_os_ver, schedule_test_main=None, schedule_prod_ver=None, pdr_login_info=None):
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # test_case_path = os.path.normpath(os.path.join(dir_path, project_name, test_case_folder_name))
        test_case_path = os.path.normpath(os.path.join(dir_path, test_case_folder_name))
        cmd = f'pytest -s {os.path.normpath(os.path.join(test_case_path, "test_main.py" if schedule_test_main is None else schedule_test_main))} --color=yes '
        cmd += f'--udid={udid} --srNo={sr_no} --trNo={tr_no} --buildVer={build_ver} ' \
               f'--buildNum={build_num}{"" if schedule_prod_ver is None else f" --prodVer={schedule_prod_ver}"} --buildFile={build_file} --osVer={device_os_ver} ' \
               f'--enableCaseExeLog={enable_case_execution_log}'
        cmd += '' if pdr_login_info is None else f' --pdrLogInID={pdr_login_info[0]} --pdrLogInPW={pdr_login_info[1]}'
        print(cmd)
        print('start to run test ---')
        try:
            subprocess.Popen("color", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass
        stdout = os.popen(cmd).read()
        print(stdout)
    except Exception as e:
        print(f'Exception occurs - {e}')
        pass

def full_automation_module(schedule_para=None):
    from os.path import join

    # check version
    if sys.version_info < (3,8):
        print ("Please update Python to 3.8 +")
        sys.exit("Incorrect Python version.")

    # [NOTICES]
    # Before query SR, please use ATFramework/utils/_ecl_operation/password.py to pass clt account/password and OTP code,
    # and copy 'credential' and 'eclid' files beside this file.

    # check latest build by query SR
    # input dict. keys: prod_name, sr_no, tr_no, prog_path_sub, dest_path, work_dir
    # output dict. keys: result, err_msg, ver_type, build
    print('ecl_operation query build >> start')
    para_dict = {'prod_name': 'PowerDirector for Mac',  # [Must] the parameter for query eCL http service. e.g. PowerDirector
                 'prod_ver': '',  # [Option #1] the parameter for query eCL http service. e.g. 20.0
                 'prod_ver_type': '',  # [Option #2] the parameter for query eCL http service. e.g. Subscription
                 'custom_name': '',
                 # [Option] to filter sr list by SR CustName, e.g. 'CyberLink', 'OEM' (means all SRs except for CyberLink)
                 'filter_sr_keyword': '',
                 # [Option] to include SRs which include specified keyword (support multiple search 'VDE,PUS')
                 'query_mode': 0,
                 # to specify the query mode: 0 (Master SR ONLY)[Default], 1(Sub-SR Only), 2(Master+Sub-SR)
                 'sr_no': 'VDM220303-01',
                 # [Option] to specified Master SR/ SubSR for get last valid TR to download build
                 'tr_no': '',  # [Option] to specified TR for download build
                 'prog_path_sub': 'Compressed',
                 # [Option] the sub-folder of TR program path to copy e.g. Compressed, if no, keep it empty
                 'dest_path': join(os.path.dirname(os.path.abspath(__file__)), 'Install_Build'),
                 # the full path of local download build folder
                 'work_dir': os.path.dirname(os.path.abspath(__file__)),  # [Option] the full path of working folder for tr_db file
                 'mail_list': ['jim_huang@cyberlink.com']  # [Option] to send the result mail
                 }
    query_result = ecl_operation.get_latest_tr_build(para_dict)
    if query_result['result']:
        # Install Build
        print('start to install build...')
        para_dict_install = {'file_path': join(para_dict['dest_path'], 'CyberLink PowerDirector 365.pkg'),
                             'sudo_password': '1234'}
        install_result = install_build(para_dict_install)
        # if install_result: -- Cancel new build install successfully check, run AT whenever new build exists or not
    else:
        path = app_config.PDR_cap["app_path"]
        info_ini = os.path.join(path, "Contents", "Resources", "info.ini")
        info = configparser.ConfigParser()
        info.read(info_ini)
        query_result["build"] = info["Build_Info"]["Build"]
        query_result["sr_no"] = info["Build_Info"]["SR_No"]
        query_result["tr_no"] = ""
    # start test
    print('start test')
    build = ['', '']
    idx_version = 0
    idx_build_num = 1
    build[idx_version] = re.findall('(\d+\.\d+)', query_result['build'])[0] # e.g. 20.4
    build[idx_build_num] = re.findall('([\d]{4})', query_result['build'])[0] # e.g. 4008
    device_os_ver = platform.mac_ver()[0] # e.g. 12.0.1
    # print(f'BuildVer={build[0]}, BuildNo={build[1]}, OSVer={device_os_ver}')
    # __run_test(device_udid[0], sr_no, tr_no, build[0], build[1], package_file_name, device_os_ver)
    __run_test(device_udid[0], query_result['sr_no'], query_result['tr_no'], build[0], build[1], package_file_name, device_os_ver,
               None if schedule_para is None else schedule_para["exec_test_main"],
               None if len(schedule_para["schedule_name"].split("_")) < 2 else schedule_para["schedule_name"].split("_")[-1],
               None if schedule_para is None else schedule_para["pdr_login_info"])
    print('test complete.')

    #mail result
    # send_report(title_project, deviceid_list, test_case_path, receiver_list)
    # print('send report complete.')

if __name__ == '__main__':
    full_automation_module()