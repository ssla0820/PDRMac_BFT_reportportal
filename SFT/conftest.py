from time import localtime, strftime

import pytest
import sys,os
import subprocess
from os.path import dirname as _dir, isfile
sys.path.insert(0,(_dir(_dir(_dir(__file__)))))
sys.path.insert(0,(_dir(_dir(__file__))))

from ATFramework.utils import MyReport
from ATFramework.utils.log import logger
from ATFramework.utils import GoogleApi
import main



# PACKAGE_NAME = main.package_name
# PACKAGE_FILE_PATH = _dir(_dir(__file__)) + "\\app\\" + main.package_file_name
PACKAGE_FILE_PATH = ''
PROJECT_INFO_PATH = _dir(_dir(__file__)) + "\\app"

SCRIPT_NAME = main.script_name
SCRIPT_VERSION = main.script_version

# Init google api instance
GOOGLE_SHEET_NAME = 'MacPDR_SFT'
GOOGLE_SPREADSHEET_ID = '14MJuTrKKNi8ntlVFxzEYzYsbLcicir6_1Og3jXO5s4U'
# GOOGLE_SHEET_HEADER = ['Date', 'Time', 'SR', 'Build_Type', 'Build_No', 'Server', 'OS', 'Device', 'Version', 'Pass', 'Fail', 'Skip', 'N/A', 'Total time']
# for 2021 new header, default = ['Date', 'Time', 'Script_Name', 'Script_Ver', 'SR_No', 'TR_No', 'Build_No', 'Build_Type', 'Build_Ver_Type', 'OS', 'OS_Ver', 'Device_ID']
GOOGLE_SHEET_HEADER = ['Server', 'Pass', 'Fail', 'Skip', 'N/A', 'Total time']
GOOGLE_API_INSTANCE = GoogleApi(GOOGLE_SHEET_NAME, GOOGLE_SHEET_HEADER, 1, GOOGLE_SPREADSHEET_ID)

def pytest_addoption(parser):
    parser.addoption("--udid", action="store", default="auto", help="device unique udid")
    parser.addoption("--srNo", action="store", default="", help="SR Number")
    parser.addoption("--trNo", action="store", default="", help="TR Number")
    parser.addoption("--buildVer", action="store", default="", help="Build version")
    parser.addoption("--buildNum", action="store", default="", help="Build number")
    parser.addoption("--prodVer", action="store", default="", help="Prod Version")
    parser.addoption("--buildFile", action="store", default="", help="Build filename")
    parser.addoption("--osVer", action="store", default="", help="OS version")
    parser.addoption("--enableCaseExeLog", action="store", default="", help="Test Case Execution Log")
    parser.addoption("--pdrLogInID", action="store", default="", help="Login ID for specific build")
    parser.addoption("--pdrLogInPW", action="store", default="", help="Login PW for specific build")

@pytest.fixture(scope='session')
def udid(request):
    return request.config.getoption("udid")

@pytest.fixture(scope='session')
def srNo(request):
    return request.config.getoption("srNo")

@pytest.fixture(scope='session')
def trNo(request):
    return request.config.getoption("trNo")

@pytest.fixture(scope='session')
def buildVer(request):
    return request.config.getoption("buildVer")

@pytest.fixture(scope='session')
def buildNum(request):
    return request.config.getoption("buildNum")

@pytest.fixture(scope='session')
def prodVer(request):
    return request.config.getoption("prodVer")

@pytest.fixture(scope='session')
def buildFile(request):
    return request.config.getoption("buildFile")

@pytest.fixture(scope='session')
def osVer(request):
    return request.config.getoption("osVer")

@pytest.fixture(scope='session')
def enableCaseExeLog(request):
    return request.config.getoption("enableCaseExeLog")

@pytest.fixture(scope='session')
def pdrLogInID(request):
    return request.config.getoption("pdrLogInID")

@pytest.fixture(scope='session')
def pdrLogInPW(request):
    return request.config.getoption("pdrLogInPW")

@pytest.fixture(scope='session', autouse=True)
def get_project_info(srNo, trNo, buildNum, buildVer, prodVer, buildFile, osVer, pdrLogInID, pdrLogInPW):
    # import os
    # import re
    # global PROJECT_INFO_PATH
    from globals import get_version, get_sr_number, get_tr_number, get_build_number, get_prod_version, get_package_file_path, get_os_version, get_pdr_login_id, get_pdr_login_pw
    from globals import set_version, set_sr_number, set_tr_number, set_build_number, set_prod_version, set_package_file_path, set_os_version, set_pdr_login_id, set_pdr_login_pw
    global PACKAGE_FILE_PATH
    #
    # is_find_sr = False
    # is_find_version = False
    # is_find_build_no = False
    # try:
    #     logger(f'PROJECT_INFO_PATH={PROJECT_INFO_PATH}')
    #     files = [f for f in os.listdir(PROJECT_INFO_PATH) if re.match(r'^\[.*\].*\.txt$', f)]
    #     for f in files:
    #         if is_find_sr == False:
    #             tmp = re.findall(r'[A-Z]{3}[0-9]{6}-[0-9]{2}', f)
    #             if tmp != []:
    #                 set_sr_number(tmp[0])
    #                 is_find_sr = True
    #                 continue
    #         if is_find_version == False:
    #             tmp = re.findall(r'[\d]+\.[\d]+\.[\d]+', f)
    #             if tmp != []:
    #                 # version = tmp[0]
    #                 set_version(tmp[0])
    #                 is_find_version = True
    #                 continue
    #         if is_find_build_no == False:
    #             tmp = re.findall(r'[0-9]{6}', f)
    #             if tmp != []:
    #                 set_build_number(tmp[0])
    #                 is_find_build_no = True
    #                 continue
    #     if not (is_find_sr and is_find_version and is_find_build_no):
    #         logger(f'[Error] get project info. error. SR_No={get_sr_number()}, VERSION={get_version()}, Build_No={get_build_number()}')
    #     logger(f'[Project Info] SR_No={get_sr_number()}, VERSION={get_version()}, Build_No={get_build_number()}')
    # except Exception as e:
    #     print(f'error - {e}')
    set_sr_number(srNo)
    set_tr_number(trNo)
    set_version(buildVer)
    set_build_number(buildNum)
    set_prod_version(prodVer)
    set_package_file_path(_dir(_dir(__file__)) + "\\app\\" + buildFile)
    set_os_version(osVer)
    set_pdr_login_id(pdrLogInID)
    set_pdr_login_pw(pdrLogInPW)
    logger(f'[Project Info] SR_No={get_sr_number()}, TR_No={get_tr_number()}, VERSION={get_version()}, '
           f'Build_No={get_build_number()}, Build_File={get_package_file_path()}, OS_Version={get_os_version()}')

    #export build info to performance.csv, mark it to disable recording performance feature
    record_performance(srNo, trNo, buildNum, buildVer, osVer)
    return True


def record_performance(srNo, trNo, buildNum, buildVer, osVer):
    output_path = f'{_dir(__file__)}/report/MyReport'   # force export to MyReport .....
    os.makedirs(output_path, exist_ok=True)
    default_full_path = f'{output_path}/performance.csv'
    if isfile(default_full_path):
        with open(default_full_path, "r") as f: timestamp = f.readline().strip().replace("create_time=", "")
        os.rename(default_full_path, f'{output_path}/performance_{timestamp}.csv')
    with open(default_full_path, "w") as f:
        data = [f"create_time={strftime('%Y%m%d_%H%M%S', localtime())}", f"{srNo=}", f"{trNo=}", f"{buildNum=}",
                f"{buildVer=}", f"{osVer=}", "", "UUID,DIFF_CPU,DIFF_RAM,START_CPU,START_RAM,END_CPU,END_RAM"]
        f.writelines([f"{x}\n" for x in data])


@pytest.fixture(scope='session', autouse=True)
def set_enable_case_exe_log(enableCaseExeLog):
    from globals import set_enable_case_execution_log
    set_enable_case_execution_log(enableCaseExeLog)
    return True

# for report portal
from reportportal_client import RPLogger
import logging


# Uncomment the following lines to get full HTTP logging in console
# from http.client import HTTPConnection
# HTTPConnection.debuglevel = 1


@pytest.fixture(scope='session')
def rp_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logging.setLoggerClass(RPLogger)
    return logger


@pytest.fixture(autouse=True)
def skip_by_mark(request):
    if request.node.get_closest_marker('fixture_skip'):
        pytest.skip('skip by fixture')


@pytest.fixture(scope='session')
def rp_launch_id(request):
    if hasattr(request.config, "py_test_service"):
        return request.config.py_test_service.rp.launch_uuid


@pytest.fixture(scope='session')
def rp_endpoint(request):
    if hasattr(request.config, "py_test_service"):
        return request.config.py_test_service.rp.endpoint


@pytest.fixture(scope='session')
def rp_project(request):
    if hasattr(request.config, "py_test_service"):
        return request.config.py_test_service.rp.project


# Global dictionary to store test results
pytest.test_results = {}

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test outcomes for all tests with simplified keys.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":  # Capture the actual test call phase
        # Extract the method name (last part of the nodeid)
        test_name = item.nodeid.split("::")[-1]

        if report.passed:
            pytest.test_results[test_name] = True
        # elif report.failed:
        #     # Capture exception message if available
        #     # if call.excinfo:
        #     #     pytest.test_results[test_name] = f"Exception: {call.excinfo.exconly()}"
        #     # else:
        #     pytest.test_results[test_name] = False
        # elif report.skipped:
        #     pytest.test_results[test_name] = False
        else:
            pytest.test_results[test_name] = False

# import functools
# import os
# import subprocess
# import sys
# import traceback
# import base64
# import inspect

# import functools
# import os
# import sys
# import traceback
# import base64
# import inspect
# import pytest

# from ATFramework.utils.log import logger  # your custom logger
# # from reportportal_client import RPLogger  # you might already have it

# class ReportPortal_screenshot:
#     """
#     A helper class to handle taking/attaching screenshots to ReportPortal.
#     """

#     def __init__(self, udid=None, driver=None, rp_logger=None):
#         """
#         :param udid: Unique device ID (string or list).
#         :param driver: The Appium or Selenium driver (could be a list).
#         :param rp_logger: The logger fixture that supports attachments.
#         """
#         self.driver = driver
#         self.udid = udid or "unknown_device"
#         self.start_recording_flag = 0

#         # Keep a reference to the ReportPortal logger
#         self.rp_logger = rp_logger

#         # Data path
#         self.source_path = os.path.dirname(inspect.stack()[2].filename)

#         # Set up the report path
#         if isinstance(self.udid, list):  # multi-devices
#             self.output_path = f"{self.source_path}/report/{self.udid[0]}"
#         else:
#             self.output_path = f"{self.source_path}/report/{self.udid}"

#     def exception_screenshot(self, func):
#         """
#         Decorator that automatically takes a screenshot on exception,
#         then attaches it to ReportPortal.
#         """
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             try:
#                 return func(*args, **kwargs)
#             except Exception as e:
#                 # If driver is a single instance, make it a list for uniform handling
#                 driver_list = self.driver if isinstance(self.driver, list) else [self.driver]

#                 # Extract traceback info
#                 tb = sys.exc_info()[2]
#                 lineno = traceback.extract_tb(tb)[-1].lineno
#                 funcname = func.__name__
#                 filename = os.path.basename(traceback.extract_tb(tb)[-1].filename)

#                 # Ensure the folder exists
#                 os.makedirs(self.output_path, exist_ok=True)

#                 screenshot_file = f"[Exception]{funcname}_{lineno}.png"
#                 screenshot_path = os.path.join(self.output_path, screenshot_file)

#                 # Take screenshot on the first driver
#                 if driver_list[0] and hasattr(driver_list[0], "get_screenshot_as_file"):
#                     driver_list[0].get_screenshot_as_file(screenshot_path)

#                 # Log with your local logger
#                 logger(f"Exception screenshot: {screenshot_path}",
#                        line=lineno, file_name=filename, function=funcname)
#                 # get rp_logger from *args
#                 rp_logger = args[0].rp_logger if args and hasattr(args[0], "rp_logger") else None

#                 # Attach screenshot to RP
#                 self.attach_to_reportportal(
#                     name=screenshot_file,
#                     path=screenshot_path,
#                     content_type="image/png",
#                 )

#                 # If screen recording is active, stop & attach
#                 if self.start_recording_flag == 1:
#                     self.stop_and_attach_video(func.__name__)

#                 raise  # re-raise the exception
#         return wrapper

#     def attach_screenshot(self, file_name, file_path):
#         """
#         Public method to attach an existing screenshot file to ReportPortal.
#         """
#         if not os.path.isfile(file_path):
#             logger(f"File not found for attachment: {file_path}")
#             return

#         self.attach_to_reportportal(file_name, file_path, "image/png")

#     def attach_to_reportportal(self, name, path, content_type):
#         """
#         Low-level method that actually calls rp_logger.info(..., attachment=...).
#         """
#         def rp_logger():
#             logger = logging.getLogger(__name__)
#             logger.setLevel(logging.DEBUG)
#             logging.setLoggerClass(RPLogger)
#             return logger
#         rp_logger = rp_logger()

#         if not rp_logger:
#             logger("rp_logger not set! Cannot attach to ReportPortal.")
#             return

#         if not os.path.isfile(path):
#             logger(f"File not found: {path}")
#             return

#         try:
#             with open(path, "rb") as f:
#                 content = f.read()

#             rp_logger.info(
#                 f"Uploading file to ReportPortal: {name}",
#                 attachment={
#                     "name": name,
#                     "data": content,
#                     "mime": content_type,
#                 },
#             )
#         except Exception as e:
#             logger(f"Error: Failed to upload file to ReportPortal. {str(e)}")

#     def stop_and_attach_video(self, func_name):
#         """
#         Stop screen recording (if the driver supports it), save, then attach to RP.
#         """
#         driver_list = self.driver if isinstance(self.driver, list) else [self.driver]

#         for idx, drv in enumerate(driver_list):
#             if drv and hasattr(drv, "stop_recording_screen"):
#                 base64_data = drv.stop_recording_screen()
#                 # Build file name for each device
#                 device_suffix = self.udid[idx] if isinstance(self.udid, list) else self.udid
#                 video_file = f"[Exception]{func_name}({device_suffix}).mp4"
#                 video_path = os.path.join(self.output_path, video_file)

#                 with open(video_path, "wb") as fh:
#                     fh.write(base64.b64decode(base64_data))

#                 logger(f"Exception recording video: {video_path}")

#                 # Attach the MP4 to ReportPortal
#                 self.attach_to_reportportal(video_file, video_path, "video/mp4")

#                 # Optional: If you want to run an ADB command to refresh media store
#                 # cmd = f'adb -s {device_suffix} shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///storage///emulated///0///'
#                 # self.shell(cmd)

#         # Turn off the flag after stopping
#         self.start_recording_flag = 0
