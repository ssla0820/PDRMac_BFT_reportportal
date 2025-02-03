
import os
import subprocess
import sys
from send_mail.send_report import send_report
from ATFramework.utils._ecl_operation import ecl_operation

# Local Mode Program
# Support Multi-device of Android

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
sr_no = 'VDM241202-01'
# sr_no = ''
tr_no = 'TR250102-018'
# tr_no = ''
package_file_name = ""
package_name = 'com.cyberlink.powerdirector'

# Mail Settings ========================================
title_project = 'MacPDR'
#receiver_list = ["jim_huang@cyberlink.com", "biaggi_li@cyberlink.com", "terence_chang@cyberlink.com"]
receiver_list = ["jim_huang@cyberlink.com"]

# Test Case Module Individual Execution Log Settings ======================================
enable_case_execution_log = 1
# ======================================================

#execute via pytest
def __run_test(udid, sr_no, tr_no, build_ver, build_num, build_file, device_os_ver):
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # test_case_path = os.path.normpath(os.path.join(dir_path, project_name, test_case_folder_name))
        test_case_path = os.path.normpath(os.path.join(dir_path, test_case_folder_name))
        cmd = f'pytest --reportportal -s {os.path.normpath(os.path.join(test_case_path, "test_main.py"))} -m "bft_check" --color=yes '
        # cmd = f'pytest --reportportal -s {os.path.normpath(os.path.join(test_case_path, "test_main.py"))} --color=yes '
        cmd += f'--udid={udid} --srNo={sr_no} --trNo={tr_no} --buildVer={build_ver} ' \
               f'--buildNum={build_num} --buildFile={build_file} --osVer={device_os_ver} ' \
               f'--enableCaseExeLog={enable_case_execution_log}'
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


def get_build_name(folder_path, prod_ver='Beta'):
    prod_version_beta = 'U-beta'
    prod_version_prod = r'U-production'
    file_extension = '.apk'

    prod_version = prod_version_beta
    if prod_ver != 'Beta':
        prod_version = prod_version_prod
    list_files = os.listdir(folder_path)
    target_file = ''
    for file in list_files:
        if file_extension in file and prod_version in file:
            target_file = file
            break
    return target_file


def shell(command, device_id=''):
    import subprocess
    erroutput = ''
    try:
        if "adb -s " not in command:
            command = command.replace("adb", f"adb -s {device_id}")
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdoutput, erroutput) = p.communicate()
        return stdoutput.decode('UTF-8').replace('\r\n', '')
    except Exception:
        print(erroutput)
        return -1


if __name__ == '__main__':
    from os.path import join

    # check version
    if sys.version_info < (3,8):
        print ("Please update Python to 3.8 +")
        sys.exit("Incorrect Python version.")

    # # check latest build by SR
    # # input dict. keys: prod_name, sr_no, tr_no, prog_path_sub, dest_path, work_dir
    # # output dict. keys: result, err_msg, ver_type, build
    # print('ecl_operation query build >> start')
    # para_dict = {'prod_name': 'U',
    #              'sr_no': sr_no,
    #              'tr_no': tr_no,
    #              'prog_path_sub': '',
    #              'dest_path': join(os.path.dirname(os.path.abspath(__file__)), r'ATFramework_aU\app'),
    #              'work_dir': os.path.dirname(os.path.abspath(__file__)),
    #              'mail_list': ['jim_huang@cyberlink.com']}
    # list_result = ecl_operation.get_latest_build(para_dict)
    # print(f'ecl_operation result={list_result}')
    # if not list_result['result']:
    #     exit(1)
    # build = list_result['build'].replace('U:', '').strip().split('_')
    # print(f'Complete. sr_num={sr_no}, build_ver={build[0]}, build_num={build[1]}')
    # # get the target build file name
    # print(f'taget_build default={package_file_name}')
    # target_folder = join(os.path.dirname(os.path.abspath(__file__)), r'ATFramework_aU\app')
    # package_file_name = get_build_name(target_folder, build_type)
    # print(f'target_build={package_file_name}')
    # # get os version of master device
    # cmd = f'adb shell getprop ro.build.version.release'
    # device_os_ver = str(shell(cmd, device_udid[0]))
    # print(f'Device OS Version={device_os_ver}')

    # start test
    print('start test')
    build = ['23.1', '7302']
    device_os_ver = '10.15'
    __run_test(device_udid[0], sr_no, tr_no, build[0], build[1], package_file_name, device_os_ver)
    print('test complete.')

    #mail result
    # send_report(title_project, deviceid_list, test_case_path, receiver_list)
    # print('send report complete.')