
# from .conftest import BUILD_TYPE
# from .conftest import U_ACCOUNT_ALIAS
import re
from ATFramework.utils import GoogleApi

version = ''
sr_number = ''
tr_number = ''
build_number = ''
prod_version = ''
package_file_path = ''
os_version = ''
report_info = {'pass': 0, 'fail': 0, 'na': 0, 'skip': 0, 'duration': '0:0:0'}

google_api_instance_for_module = None
enable_case_execution_log = 0 # for test case module update individual google sheet execution log
pdr_login_id = ""
pdr_login_pw = ""

"""
Global variables setter section
"""
def set_version(value):
    global version
    version = value
    return True

def set_sr_number(value):
    global sr_number
    sr_number = value
    return True

def set_tr_number(value):
    global tr_number
    tr_number = value
    return True

def set_build_number(value):
    global build_number
    build_number = value
    return True

def set_prod_version(value):
    global prod_version
    prod_version = value
    return True

def set_package_file_path(value):
    global package_file_path
    package_file_path = value
    return True

def set_os_version(value):
    global os_version
    os_version = value
    return True

def update_report_info(cnt_pass, cnt_fail, cnt_na, cnt_skip, duration): # duration: 0:0:0
    global report_info
    if type(cnt_fail) is str:
        pattern = r'<b>(\d+)</b>'
        result = re.findall(pattern, cnt_fail)
        cnt_fail = int(result[0])
    print(f'update_report_info: fail number={cnt_fail}')
    report_info['pass'] += cnt_pass
    report_info['fail'] += cnt_fail
    report_info['na'] += cnt_na
    report_info['skip'] += cnt_skip
    # calculate duration
    time_list = [report_info['duration'], duration]
    totalSecs = 0
    for tm in time_list:
        timeParts = [int(s) for s in tm.split(':')]
        totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60 + timeParts[2]
    totalSecs, sec = divmod(totalSecs, 60)
    hr, min = divmod(totalSecs, 60)
    report_info['duration'] = "%d:%02d:%02d" % (hr, min, sec)
    return True

def set_enable_case_execution_log(value):
    global enable_case_execution_log
    enable_case_execution_log = value
    return True

def set_pdr_login_id(value):
    global pdr_login_id
    pdr_login_id = value
    return True

def set_pdr_login_pw(value):
    global pdr_login_pw
    pdr_login_pw = value
    return True

"""
Global variables getter section
"""
def get_version():
    global version
    return version

def get_sr_number():
    global sr_number
    return sr_number

def get_tr_number():
    global tr_number
    return tr_number

def get_build_number():
    global build_number
    return build_number

def get_prod_version():
    global prod_version
    return prod_version

def get_package_file_path():
    global package_file_path
    return package_file_path

def get_os_version():
    global os_version
    return os_version

def get_report_info(key):
    global report_info
    return report_info[key]

def get_enable_case_execution_log():
    global enable_case_execution_log
    return enable_case_execution_log

def get_pdr_login_id():
    global pdr_login_id
    return pdr_login_id
    
def get_pdr_login_pw():
    global pdr_login_pw
    return pdr_login_pw

def google_sheet_execution_log_init(module_name):
    import datetime
    global google_api_instance_for_module
    # Init google api instance
    sheet_name = 'MacPDR_SFT_Case'
    spreadsheet_id = '14MJuTrKKNi8ntlVFxzEYzYsbLcicir6_1Og3jXO5s4U'
    sheet_header = ['Server', 'Pass', 'Fail', 'Skip', 'N/A', 'Total time']
    google_api_instance_for_module = GoogleApi(sheet_name, sheet_header, 1, spreadsheet_id)

    now = datetime.datetime.now()
    new_record = {'Date': now.date().strftime("%Y-%m-%d"),
                  'Time': now.time().strftime("%H:%M:%S"),
                  'Script_Name': f'MacPDR_SFT[{module_name}]',
                  'Script_Ver': '1.0',
                  'SR_No': get_sr_number(),
                  'TR_No': get_tr_number(),
                  'Prod_Ver': get_prod_version(),
                  'Build_No': get_build_number(),
                  'OS': 'MacOS',
                  'OS_Ver': get_os_version(),
                  }
    google_api_instance_for_module.add_new_record(new_record)
    print(f'Usage Log Init - add new record to row: {google_api_instance_for_module.row_prev_record}')
    return True

def google_sheet_execution_log_update_result(pass_cnt, fail_cnt, na_cnt, skip_cnt, duration):
    import time
    global google_api_instance_for_module
    data = {'Pass': pass_cnt, 'Fail': fail_cnt, 'Skip': skip_cnt,
            'N/A': na_cnt, 'Total time': duration}
    google_api_instance_for_module.update_columns(data)
    print(f'Usage Log end - update record to row: {google_api_instance_for_module.row_prev_record}')
    time.sleep(5)
    return True