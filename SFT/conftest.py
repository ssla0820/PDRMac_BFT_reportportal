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


@pytest.fixture(scope='session')
def rp_logger():
    # 設定 logger class 為 RPLogger
    logging.setLoggerClass(RPLogger)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

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
        else:
            pytest.test_results[test_name] = False

# In your pytest configuration file or conftest.py
def pytest_runtest_makereport(item, call):
    if 'Skipping' in str(call.excinfo):
        # Check if the test was skipped due to a failed dependency
        if 'did not pass' in str(call.excinfo):
            item.add_marker(pytest.mark.issue(reason="skipped due to dependency test failure", issue_type="ND"))
