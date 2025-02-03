# install library
# $ pip install --upgrade pywin32

import os
import sys
import datetime
import atexit
import win32com.client

class TaskScheduler():
    def __init__(self, para_dict):
        try:
            scheduler = win32com.client.Dispatch('Schedule.Service')
            scheduler.Connect()
            self.root_folder = scheduler.GetFolder('\\')
            self.task_def = scheduler.NewTask(0)
            self.trigger_mode = para_dict['trigger_mode']  # trigger mode
            """
            TASK_TRIGGER_DAILY 2
            TASK_TRIGGER_WEEKLY 3
            TASK_TRIGGER_LOGON 9
            """
            self.task_creation_mode = 6  # TASK_CREATE_OR_UPDATE 6
            self.task_action_exe = 0  # TASK_ACTION_EXEC 0
            self.task_logon_token = 3  # TASK_LOGON_INTERACTIVE_TOKEN 3
            self.task_id = para_dict['task_name']
            self.task_description = para_dict['task_description']
            self.task_author = 'Create_by_AT'
            if para_dict['trigger_time_start'] == '':
                now = datetime.datetime.now() + datetime.timedelta(minutes=3)
                self.trigger_start_time = now.isoformat()
            else:
                self.trigger_start_time = datetime.datetime.strptime(para_dict['trigger_time_start'], r'%Y-%m-%d %H:%M:%S').isoformat()
            self.trigger_end_time = ''
            # if para_dict['trigger_time_end'] == '':
            #     later = datetime.datetime.now() + datetime.timedelta(days=3650)
            #     self.trigger_end_time = later.isoformat()
            # else:
            #     self.trigger_end_time = datetime.datetime.strptime(para_dict['trigger_time_end'], r'%Y-%m-%d %H:%M:%S').isoformat()
            if para_dict['trigger_days_interval'] == '':
                self.trigger_days_interval = 1
            else:
                self.trigger_days_interval = int(para_dict['trigger_days_interval'])
            if para_dict['trigger_days_of_week'] == '':
                self.trigger_days_of_week = 127
            else:
                self.trigger_days_of_week = int(para_dict['trigger_days_of_week'])  # days of week 1~64 1:sun, 2: mon, 3: sun+mon...
            if para_dict['trigger_weeks_interval'] == '':
                self.trigger_weeks_interval = 1
            else:
                self.trigger_weeks_interval = int(para_dict['trigger_weeks_interval'])
            self.action_id = "ActionId_AT"  # arbitrary action ID
            if para_dict['action_exe'] == '' and os.path.splitext(para_dict['action_argument'])[1] == '.py':
                self.action_path = sys.executable
            else:
                self.action_path = para_dict['action_exe']  # executable path (could be python.exe)
            self.action_arguments = para_dict['action_argument']  # arguments (could be something.py)
            self.action_workdir = ''  # working directory for action executable
            # self.action_workdir = para_dict['action_work_dir']  # working directory for action executable
        except Exception as e:
            err_msg = f'Exception occurs. Incorrect format of parameter or missing keys. ErrorLog={e}'
            print(err_msg)

    def start_time(self):
        try:
            coltriggers = self.task_def.Triggers
            trigger = coltriggers.Create(1)
            trigger.Id = 'Trigger_Time'
            trigger.StartBoundary = self.trigger_start_time
            trigger.EndBoundary = self.trigger_end_time
            trigger.Enabled = True
            colactions = self.task_def.Actions
            action = colactions.Create(self.task_action_exe)
            action.ID = self.action_id
            action.Path = self.action_path
            action.WorkingDirectory = self.action_workdir
            action.Arguments = self.action_arguments
            info = self.task_def.RegistrationInfo
            info.Author = self.task_author
            info.Description = self.task_description
            settings = self.task_def.Settings
            settings.Hidden = False
            task_result = self.root_folder.RegisterTaskDefinition(
                self.task_id, self.task_def, self.task_creation_mode, "", "", self.task_logon_token)
            return task_result
        except Exception as e:
            err_msg = f'Exception occurs. Unable to add task. ErrorLog={e}'
            print(err_msg)

    def start_day(self):
        try:
            coltriggers = self.task_def.Triggers
            trigger = coltriggers.Create(2)
            trigger.Id = 'Trigger_Day'
            trigger.StartBoundary = self.trigger_start_time
            trigger.EndBoundary = self.trigger_end_time
            trigger.DaysInterval = self.trigger_days_interval
            trigger.Enabled = True
            colactions = self.task_def.Actions
            action = colactions.Create(self.task_action_exe)
            action.ID = self.action_id
            action.Path = self.action_path
            action.WorkingDirectory = self.action_workdir
            action.Arguments = self.action_arguments
            info = self.task_def.RegistrationInfo
            info.Author = self.task_author
            info.Description = self.task_description
            settings = self.task_def.Settings
            settings.Hidden = False
            task_result = self.root_folder.RegisterTaskDefinition(
                self.task_id, self.task_def, self.task_creation_mode, "", "", self.task_logon_token)
            return task_result
        except Exception as e:
            err_msg = f'Exception occurs. Unable to add task. ErrorLog={e}'
            print(err_msg)

    def start_weekly(self):
        try:
            coltriggers = self.task_def.Triggers
            trigger = coltriggers.Create(3)
            trigger.Id = 'Trigger_Week'
            trigger.StartBoundary = self.trigger_start_time
            trigger.EndBoundary = self.trigger_end_time
            trigger.DaysOfWeek = self.trigger_days_of_week
            trigger.WeeksInterval = self.trigger_weeks_interval
            trigger.Enabled = True
            colactions = self.task_def.Actions
            action = colactions.Create(self.task_action_exe)
            action.ID = self.action_id
            action.Path = self.action_path
            action.WorkingDirectory = self.action_workdir
            action.Arguments = self.action_arguments
            info = self.task_def.RegistrationInfo
            info.Author = self.task_author
            info.Description = self.task_description
            settings = self.task_def.Settings
            settings.Hidden = False
            task_result = self.root_folder.RegisterTaskDefinition(
                self.task_id, self.task_def, self.task_creation_mode, "", "", self.task_logon_token)
            return task_result
        except Exception as e:
            err_msg = f'Exception occurs. Unable to add task. ErrorLog={e}'
            print(err_msg)

    def start_logon(self):
        try:
            coltriggers = self.task_def.Triggers
            trigger = coltriggers.Create(9)
            trigger.Id = 'Trigger_Logon'
            trigger.UserId = os.environ.get('USERNAME')  # current user account
            trigger.StartBoundary = self.trigger_start_time
            trigger.EndBoundary = self.trigger_end_time
            trigger.Enabled = True
            colactions = self.task_def.Actions
            action = colactions.Create(self.task_action_exe)
            action.ID = self.action_id
            action.Path = self.action_path
            action.WorkingDirectory = self.action_workdir
            action.Arguments = self.action_arguments
            info = self.task_def.RegistrationInfo
            info.Author = self.task_author
            info.Description = self.task_description
            settings = self.task_def.Settings
            settings.Hidden = False
            task_result = self.root_folder.RegisterTaskDefinition(
                self.task_id, self.task_def, self.task_creation_mode, "", "", self.task_logon_token)
            return task_result
        except Exception as e:
            err_msg = f'Exception occurs. Unable to add task. ErrorLog={e}'
            print(err_msg)

    def start_day_logon(self):
        try:
            coltriggers = self.task_def.Triggers
            trigger = coltriggers.Create(2)
            trigger.Id = 'Trigger_Day'
            trigger.StartBoundary = self.trigger_start_time
            trigger.EndBoundary = self.trigger_end_time
            trigger.DaysInterval = self.trigger_days_interval
            trigger.Enabled = True
            trigger = coltriggers.Create(9)
            trigger.Id = 'Trigger_Logon'
            trigger.UserId = os.environ.get('USERNAME')  # current user account
            trigger.StartBoundary = self.trigger_start_time
            trigger.EndBoundary = self.trigger_end_time
            trigger.Enabled = True
            colactions = self.task_def.Actions
            action = colactions.Create(self.task_action_exe)
            action.ID = self.action_id
            action.Path = self.action_path
            action.WorkingDirectory = self.action_workdir
            action.Arguments = self.action_arguments
            info = self.task_def.RegistrationInfo
            info.Author = self.task_author
            info.Description = self.task_description
            settings = self.task_def.Settings
            settings.Hidden = False
            task_result = self.root_folder.RegisterTaskDefinition(
                self.task_id, self.task_def, self.task_creation_mode, "", "", self.task_logon_token)
            return task_result
        except Exception as e:
            err_msg = f'Exception occurs. Unable to add task. ErrorLog={e}'
            print(err_msg)

    def start_day_disable_logon(self):
        try:
            coltriggers = self.task_def.Triggers
            trigger = coltriggers.Create(2)
            trigger.Id = 'Trigger_Day'
            trigger.StartBoundary = self.trigger_start_time
            trigger.EndBoundary = self.trigger_end_time
            trigger.DaysInterval = self.trigger_days_interval
            trigger.Enabled = True
            trigger = coltriggers.Create(9)
            trigger.Id = 'Trigger_Logon'
            trigger.UserId = os.environ.get('USERNAME')  # current user account
            trigger.StartBoundary = self.trigger_start_time
            trigger.EndBoundary = self.trigger_end_time
            trigger.Enabled = False
            colactions = self.task_def.Actions
            action = colactions.Create(self.task_action_exe)
            action.ID = self.action_id
            action.Path = self.action_path
            action.WorkingDirectory = self.action_workdir
            action.Arguments = self.action_arguments
            info = self.task_def.RegistrationInfo
            info.Author = self.task_author
            info.Description = self.task_description
            settings = self.task_def.Settings
            settings.Hidden = False
            task_result = self.root_folder.RegisterTaskDefinition(
                self.task_id, self.task_def, self.task_creation_mode, "", "", self.task_logon_token)
            return task_result
        except Exception as e:
            err_msg = f'Exception occurs. Unable to add task. ErrorLog={e}'
            print(err_msg)

    def start_weekly_logon(self):
        try:
            coltriggers = self.task_def.Triggers
            trigger = coltriggers.Create(3)
            trigger.Id = 'Trigger_Week'
            trigger.StartBoundary = self.trigger_start_time
            trigger.EndBoundary = self.trigger_end_time
            trigger.DaysOfWeek = self.trigger_days_of_week
            trigger.WeeksInterval = self.trigger_weeks_interval
            trigger.Enabled = True
            trigger = coltriggers.Create(9)
            trigger.Id = 'Trigger_Logon'
            trigger.UserId = os.environ.get('USERNAME')  # current user account
            trigger.StartBoundary = self.trigger_start_time
            trigger.EndBoundary = self.trigger_end_time
            trigger.Enabled = True
            colactions = self.task_def.Actions
            action = colactions.Create(self.task_action_exe)
            action.ID = self.action_id
            action.Path = self.action_path
            action.WorkingDirectory = self.action_workdir
            action.Arguments = self.action_arguments
            info = self.task_def.RegistrationInfo
            info.Author = self.task_author
            info.Description = self.task_description
            settings = self.task_def.Settings
            settings.Hidden = False
            task_result = self.root_folder.RegisterTaskDefinition(
                self.task_id, self.task_def, self.task_creation_mode, "", "", self.task_logon_token)
            return task_result
        except Exception as e:
            err_msg = f'Exception occurs. Unable to add task. ErrorLog={e}'
            print(err_msg)

    def start_weekly_disable_logon(self):
        try:
            coltriggers = self.task_def.Triggers
            trigger = coltriggers.Create(3)
            trigger.Id = 'Trigger_Week'
            trigger.StartBoundary = self.trigger_start_time
            trigger.EndBoundary = self.trigger_end_time
            trigger.DaysOfWeek = self.trigger_days_of_week
            trigger.WeeksInterval = self.trigger_weeks_interval
            trigger.Enabled = True
            trigger = coltriggers.Create(9)
            trigger.Id = 'Trigger_Logon'
            trigger.UserId = os.environ.get('USERNAME')  # current user account
            trigger.StartBoundary = self.trigger_start_time
            trigger.EndBoundary = self.trigger_end_time
            trigger.Enabled = False
            colactions = self.task_def.Actions
            action = colactions.Create(self.task_action_exe)
            action.ID = self.action_id
            action.Path = self.action_path
            action.WorkingDirectory = self.action_workdir
            action.Arguments = self.action_arguments
            info = self.task_def.RegistrationInfo
            info.Author = self.task_author
            info.Description = self.task_description
            settings = self.task_def.Settings
            settings.Hidden = False
            task_result = self.root_folder.RegisterTaskDefinition(
                self.task_id, self.task_def, self.task_creation_mode, "", "", self.task_logon_token)
            return task_result
        except Exception as e:
            err_msg = f'Exception occurs. Unable to add task. ErrorLog={e}'
            print(err_msg)


def create_update_task(para_dict):
    try:
        task = TaskScheduler(para_dict)
        task_disable = TaskScheduler(para_dict)
        if para_dict['trigger_mode'] == '1':
            if task.start_day_logon():
                atexit.register(task_disable.start_day_disable_logon)
                return True
        elif para_dict['trigger_mode'] == '2':
            if task.start_weekly_logon():
                atexit.register(task_disable.start_weekly_disable_logon)
                return True
    except Exception as e:
        err_msg = f'Exception occurs. Unable to add task. ErrorLog={e}'
        print(err_msg)


if __name__ == '__main__':
    para = {
        'task_name': 'AutoTest_Sample',  # Must fill
        'task_description': 'AutoTest_Sample_description',  # Optional
        'action_exe': '',  # Must fill
        'action_argument': 'my.py',  # Optional
        'trigger_mode': '1',  # Must fill, mode "1": daily, "2": weekly
        'trigger_time_start': '',  # Optional, leave empty will use current time
        'trigger_days_interval': '',  # Optional, leave empty will use 1 as default
        'trigger_days_of_week': '',  # Optional, leave empty will use Sun/Mon/Tue/Wed/Thu/Fri/Sat as default
        'trigger_weeks_interval': '',  # Optional, leave empty will use 1 as default
        }
    result = create_update_task(para)
    print(result)