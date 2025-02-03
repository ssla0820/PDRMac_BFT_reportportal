
import subprocess
import platform
import os
import sys
import shutil

try:
    from .log import logger
except:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))
    print(os.path.dirname(SCRIPT_DIR))
    from log import logger

# ==================================================================================================================
# Class: cl_build_operation
# Description: Support auto build installation
# Parameter: A dictionary of parameter
#           - file_path: the full path of target build file (e.g. .pkg)
#           - sudo_password: the password of sudo mode
# Return: True/False
# Note: Current version, it supports on Mac OS currently.
# Author: Jim Huang
# Revise: v1.0 (1st version) [2021/10/22]
# ==================================================================================================================
# Class: cl_build_operation
# Description: Support auto build installation & uninstallation
# Parameter Installation: A dictionary of parameter of installation
#           - file_path: the full path of target build file (e.g. .pkg)
#           - sudo_password: the password of sudo mode
#           - silent_cmd: silent mode for NSIS (for Win)
# Parameter Uninstallation: A dictionary of parameter of uninstallation
#           - app_path: full path of target app path (for macOS)
#           - guid': guid of app (C:\Program Files (x86)\NSIS Uninstall Information) (for Win)
#           - silent_cmd: silent mode for NSIS (for Win)
# Return: True/False
# Note: Support single product for NSIS under Win OS, PKG under Mac OS
# Author: Jim Huang, Volath Liu
# Revise: v2.0 [2022/11/29]
# ==================================================================================================================


def install_build(dict_para):
    try:
        if platform.system() == "Windows":
            command = [dict_para['file_path'], dict_para['silent_cmd']]
            p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, err = p.communicate()
            logger(f'{output=}, {err=}')
            if err:
                return False
        else:
            command = ['installer', '-pkg', dict_para['file_path'], '-target', '/']
            p1 = subprocess.Popen(['echo', dict_para['sudo_password']], stdout=subprocess.PIPE)
            p2 = subprocess.Popen(['sudo', '-S'] + command, stdin=p1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, err = p2.communicate()
            logger(f'{output=}, {err=}')
            if err:
                return False
    except Exception as e:
        logger(f'Exception occurs. error={e}')
        return False
    return True


def uninstall_build(dict_para):
    try:
        if platform.system() == "Windows":
            uninstall_path = os.path.join(os.environ["PROGRAMFILES(X86)"], "NSIS Uninstall Information", dict_para['guid'], 'Setup.exe')
            command = f'"{os.path.normpath(uninstall_path)}" {dict_para["silent_cmd"]} _?={os.path.normpath(os.path.dirname(uninstall_path))}'
            if os.path.exists(uninstall_path):
                os.system(command)
            else:
                logger(f'Cannot find {uninstall_path}')
        else:
            if os.path.exists(os.path.normpath(dict_para["app_path"])):
                shutil.rmtree(dict_para["app_path"], ignore_errors=True)
            else:
                logger(f'Cannot find {dict_para["app_path"]}')
    except Exception as e:
        logger(f'Exception occurs. error={e}')
        return False
    return True


if __name__ == '__main__':
    mac_dict_para = {   'file_path': '/Users/qadf-mbp3/Desktop/Mac Webinar Build/7.1 for Boomerage Test/CL_Mac.7.1.0.7013.944451_PLK210915-01_R7/UWebinar.pkg',
                        'sudo_password': '1234',
                        'silent_cmd': ''
                        }
    win_dict_para = {
                        'file_path': r'C:\Users\user\Desktop\FACEME GENERIC_Windows.FaceMe Platform Central 5.2.0_v1125_r24609_FAP221101-01_R5\Uncompressed\Setup.exe',
                        'sudo_password': '',
                        'silent_cmd': '-s'
                        }

    result = install_build(win_dict_para)
    if result:
        logger('complete to install build.')
    else:
        logger('Fail to install build.')

    mac_uninstall_para = {  'app_path': r'/Applications/PhotoDirector 365.app',
                            'guid': '',
                            'silent_cmd': ''}
    win_uninstall_para = {  'app_path': '',
                            'guid': '{2D78C4DE-A9EA-87FC-A529-912486ADCB42}',
                            'silent_cmd': '-s'}
    # central: '{39ADC45E-F6EA-82FC-9126-924888A14BDC}' work: '{2D78C4DE-A9EA-87FC-A529-912486ADCB42}'
    uninstall_result = uninstall_build(win_uninstall_para)
    if uninstall_result:
        logger('complete to uninstall build.')
    else:
        logger('Fail to uninstall build.')
