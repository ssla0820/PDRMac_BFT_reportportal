import os
import subprocess
import sys
import platform
import re
import time, datetime
import json
import shutil
import schedule
import main_full_automation
import collections.abc

def job(para):
    d = datetime.datetime.now()
    main_full_automation.full_automation_module(para)
    move_sour_report = join(os.path.dirname(os.path.abspath(__file__)), r"SFT/report")
    move_sour_log = join(os.path.dirname(os.path.abspath(__file__)), r"SFT/log")
    move_dest = join(os.path.dirname(os.path.abspath(__file__)), r"SFT/scheduled_all_MyReport", f"{'' if para['schedule_name'] is None else para['schedule_name']}_{d.strftime('%m%d')}_{para['exec_time_at']}")
    os.makedirs(move_dest, exist_ok=True)
    if os.path.exists(move_sour_report):
        shutil.move(move_sour_report, move_dest)
    if os.path.exists(move_sour_log):
        shutil.move(move_sour_log, move_dest)

if __name__ == '__main__':
    from os.path import join

    # check version
    if sys.version_info < (3,8):
        print ("Please update Python to 3.8 +")
        sys.exit("Incorrect Python version.")

    f = open(join(os.path.dirname(os.path.abspath(__file__)), r"configs/schedule_config.json"), encoding="UTF-8")
    schedule_configs = json.load(f)

    for schedule_data in schedule_configs:
        if schedule_data.get("exec_weekday") is not None and schedule_data.get("exec_time_at") is not None and schedule_data.get("exec_test_main") is not None:
            schedule_para = {
                "schedule_name": None if schedule_data.get("schedule_name") is None else schedule_data["schedule_name"],
                "exec_time_at": schedule_data["exec_time_at"].replace(":", ""),
                "exec_test_main": schedule_data["exec_test_main"],
                "pdr_login_info": None \
                    if (schedule_data.get("pdr_login_info") is None \
                    or type(schedule_data["pdr_login_info"]) is not list \
                    or len(schedule_data["pdr_login_info"]) != 2) \
                    else schedule_data["pdr_login_info"]
            }
            if type(schedule_data["exec_weekday"]) is list:
                for weekday in schedule_data["exec_weekday"]:
                    try:
                        exec_string = f"schedule.every().{weekday.lower()}.at(\"{schedule_data['exec_time_at']}\").do(job, schedule_para)"
                        print(exec_string)
                        eval(exec_string)
                    except Exception as e:
                        print(f"Exception occurs, {e}")
            if type(schedule_data["exec_weekday"]) is str:
                try:
                    exec_string = f"schedule.every().{schedule_data['exec_weekday'].lower()}.at(\"{schedule_data['exec_time_at']}\").do(job, schedule_para)"
                    print(exec_string)
                    eval(exec_string)
                except Exception as e:
                    print(f"Exception occurs, {e}")
        else:
            print("Lack of critical parameters.")
    while len(schedule.get_jobs()) > 0:
        try:
            schedule.run_pending()
            print('schedule checking...')
            time.sleep(20)
        except Exception as e:
            print(f'Exception occurs - {e}')
            break