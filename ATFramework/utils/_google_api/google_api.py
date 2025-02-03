# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# install library
# $ pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

# [START sheets_quickstart]
from __future__ import print_function
import pickle
import os.path
import time

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pygsheets

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
TOKEN_FILE = 'token.pickle'
CREDENTIALS_FILE = 'credentials.json'
client_secret = os.path.join(os.path.dirname(__file__), "spreadsheet_client_secret.json")
service_account_file = os.path.join(os.path.dirname(__file__), "spreadsheet_service.json")

class GoogleApi():

    # header_list: a list of report header. e.g. ['Date', 'Time', 'Server', 'OS', 'Device', 'Version', 'Pass', 'Fail', 'Skip', 'N/A', 'Total time']
    # row_start: the row of header
    def __init__(self, sheet_name='sample', header_custom=[], row_start=1, spreadsheet_id='1lLDSYlLj8X8dGtGebeybbkgRTJm79ZhDUvhGBH9F97I', header_main=[]):
        try:
            print('Google_Api __init__ start')
            header_template = ['Date', 'Time', 'Script_Name', 'Script_Ver', 'SR_No', 'TR_No', 'Build_No', 'Prod_Ver', 'Prod_Ver_Type', 'OS', 'OS_Ver', 'Device_ID']
            if header_main:
                header_template = header_main
            header_list = header_template + header_custom
            # init. row dict (for batch update values)
            row_dict = {}
            for key in header_list:
                row_dict[key] = ''
            creds = None
            # The file token.pickle stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            file_path_token = os.path.join(os.path.dirname(__file__), TOKEN_FILE)
            file_path_credentials = os.path.join(os.path.dirname(__file__), CREDENTIALS_FILE)
            if os.path.exists(file_path_token):
                with open(file_path_token, 'rb') as token:
                    creds = pickle.load(token)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        file_path_credentials, SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open(file_path_token, 'wb') as token:
                    pickle.dump(creds, token)

            self.service = build('sheets', 'v4', credentials=creds)
            self.row_start=row_start
            self.spreadsheet_id = spreadsheet_id
            self.sheet_name = sheet_name
            # self.create_new_sheet(sheet_name)
            self.row_prev_record = row_start
            self.header = {}
            self.header_list = header_list
            self.set_header(header_list, row_start)
            self.row_dict = row_dict # for batch update
            print('service is built.')
        except Exception as e:
            print(e)
            raise Exception

    def set_header(self, header_list, row=1):
        try:
            header_dict = {}
            column_num = 1
            for value in header_list:
                header_dict[chr(ord('@')+column_num)] = value
                column_num += 1
            self.header = header_dict
            print(self.header)
            # check if header already exists
            response = self.get_columns(row)
            if 'values' in list(response['valueRanges'][0].keys()):
                return True
            print('No header is found. Create it.')
            sheet = self.service.spreadsheets()
            last_key_of_header = list(self.header.keys())[-1]
            print(f'last key of dict:{last_key_of_header}')
            # set batch structure
            body = {
                "valueInputOption": 'USER_ENTERED',
                "data": [{
                    "range": self.sheet_name + f'!A{row}:{last_key_of_header}',
                    "majorDimension": "ROWS",
                    "values": [header_list]
                }]
            }
            sheet.values().batchUpdate(spreadsheetId=self.spreadsheet_id, body=body).execute()
            # # batch update cell format
            # # > get sheet id by name
            # spreadsheet = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
            # sheet_id = None
            # for _sheet in spreadsheet['sheets']:
            #     if _sheet['properties']['title'] == self.sheet_name:
            #         sheet_id = _sheet['properties']['sheetId']
            #
            # print(f"{self.sheet_name}={sheet_id}")
            # batch_update_spreadsheet_request_body = {
            #     'requests': {
            #         "repeatCell": {
            #             "cell": {
            #                 "userEnteredFormat": {
            #                     "backgroundColor": {
            #                         "red": 0,
            #                         "green": 0,
            #                         "blue": 0,
            #                         "alpha": 1
            #                     },
            #                     "horizontalAlignment": "CENTER",
            #                     "verticalAlignment": "MIDDLE",
            #                     "textFormat": {
            #                         "foregroundColor": {
            #                             "red": 1,
            #                             "green": 1,
            #                             "blue": 1,
            #                             "alpha": 1
            #                         },
            #                         "fontSize": 12,
            #                         "bold": True,
            #                     },
            #                 }
            #             },
            #             "range": {
            #                 "sheetId": sheet_id,
            #                 "startRowIndex": row - 1,
            #                 "endRowIndex": row,
            #                 "startColumnIndex": 0,
            #                 "endColumnIndex": len(self.header.keys()),
            #             },
            #             "fields": "userEnteredFormat"
            #         }
            #     }
            # }
            # self.service.spreadsheets().batchUpdate(
            #     spreadsheetId=self.spreadsheet_id, body=batch_update_spreadsheet_request_body).execute()
        except Exception as e:
            print(e)
            raise Exception
        return True

    def create_new_sheet(self, sheet_name):
        try:
            sheets_list = self.get_sheets_title_list()
            if sheet_name not in sheets_list:
                sheet = self.service.spreadsheets()
                request_body = {
                    'requests': [{
                        'addSheet': {
                            'properties': {
                                'title': sheet_name,
                            }
                        }
                    }]
                }

                response = sheet.batchUpdate(
                    spreadsheetId=self.spreadsheet_id,
                    body=request_body
                ).execute()

                return response
            else:
                print(f'{sheet_name=} already exists.')
                return True
        except Exception as e:
            print(e)

    def get_sheets_title_list(self):
        try:
            sheet = self.service.spreadsheets()
            sheet_metadata = sheet.get(spreadsheetId=self.spreadsheet_id).execute()
            sheets = sheet_metadata.get('sheets', '')
            title_list = []
            for index in range(len(sheets)):
                title = sheets[index].get("properties", {}).get("title", "Sheet1")
                title_list.append(title)
            return title_list
        except Exception as e:
            print(e)

    def get_sheet_id_by_name(self, name):
        sheet_id = ''
        try:
            sheet = self.service.spreadsheets()
            sheet_metadata = sheet.get(spreadsheetId=self.spreadsheet_id).execute()
            sheets = sheet_metadata.get('sheets', '')
            for index in range(len(sheets)):
                sheet_property = sheets[index].get("properties", {})
                if sheet_property['title'] == name:
                    sheet_id = sheet_property['sheetId']
                    break
            print(f'{sheet_id=}')
        except Exception as e:
            print(e)
        return sheet_id

    def copy_sheet_to_spreadsheet(self, src_spreadsheet_id, src_sheet_id, dest_spreadsheet_id, dest_sheet_name):
        new_sheet_id = 0
        try:
            # copy sheet to spreadsheet
            copy_sheet_to_another_spreadsheet_request_body = {
                'destination_spreadsheet_id': dest_spreadsheet_id,
            }
            request = self.service.spreadsheets().sheets().copyTo(spreadsheetId=src_spreadsheet_id, sheetId=src_sheet_id,
                                                                            body=copy_sheet_to_another_spreadsheet_request_body)
            response = request.execute()
            print(f'sheetId={response["sheetId"]}')
            new_sheet_id = response["sheetId"]

            # rename new sheet
            batch_update_spreadsheet_request_body = {
                'requests': [{
                    'updateSheetProperties': {
                        "properties": {
                            "sheetId": response["sheetId"],
                            "title": dest_sheet_name,
                        },
                        "fields": 'title'
                    }
                }]
            }
            request = self.service.spreadsheets().batchUpdate(spreadsheetId=dest_spreadsheet_id,
                                                                        body=batch_update_spreadsheet_request_body)
            response = request.execute()
            print(response)
        except Exception as e:
            print(e)
            return False
        return new_sheet_id

    def delete_sheet(self, spreadsheet_id, sheet_id):
        try:
            request_body = {
                "requests": [
                    {
                      "deleteSheet": {
                        "sheetId": sheet_id
                      }
                    }
                ]
            }
            request = self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=request_body)
            response = request.execute()
            print(response)
        except Exception as e:
            print(e)
            return False
        return True

    def fill_test_result(self, data_list, spreadsheet_id, sheet_name, result_range):  # row sample: ['case_name', 'result', 'note']
        try:
            list_values = list()
            for unit_result in data_list: # data_list is list of dict
                list_values.append(list(unit_result.values()))

            body = {
                "valueInputOption": 'USER_ENTERED',
                "data": [{
                    "range": f'{sheet_name}!{result_range}',
                    "majorDimension": "ROWS",
                    "values": list_values
                }]
            }
            self.service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
        except Exception as e:
            print(e)
            return False
        return True

    def fill_test_summary(self, data_list, spreadsheet_id, sheet_name, result_range):  # data_list: [['date, start_time', 'platform', 'build_ver', 'script_ver', 'total case', 'pass', 'fail', 'skip', 'elapsed time']]
        try:
            body = {
                "valueInputOption": 'USER_ENTERED',
                "data": [{
                    "range": f'{sheet_name}!{result_range}',
                    "majorDimension": "COLUMNS",
                    "values": [data_list]
                }]
            }
            self.service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
        except Exception as e:
            print(e)
            return False
        return True

    def add_new_record(self, data): # data: dictionary e.g. {'Date': '2020/08/14_11:34'}
        try:
            sheet = self.service.spreadsheets()
            # reset row_dict
            for key in self.row_dict.keys():
                self.row_dict[key] = ''
            for key in data.keys():
                if key in self.row_dict.keys():
                    self.row_dict[key] = data[key]
            print(self.row_dict)
            data_list = list(self.row_dict.values())
            print(data_list)
            last_key_of_header = list(self.header.keys())[-1]
            print(f'last key of dict:{last_key_of_header}')
            #get the last row
            result = sheet.values().get(spreadsheetId=self.spreadsheet_id,
                                        range=self.sheet_name).execute()
            values = result.get('values', [])
            target_row = self.row_start + len(values)
            self.row_prev_record = target_row
            print(f'{target_row=}')
            # set batch structure
            body = {
                "valueInputOption": 'USER_ENTERED',
                "data": [{
                    "range": self.sheet_name + f'!A{target_row}:{last_key_of_header}',
                    "majorDimension": "ROWS",
                    "values": [data_list]
                }]
            }
            sheet.values().batchUpdate(spreadsheetId=self.spreadsheet_id, body=body).execute()
        except Exception as e:
            print(e)
            raise Exception
        return target_row

    def update_column(self, column_name, data, target_row=-1): # data: string
        try:
            sheet = self.service.spreadsheets()
            record_list = [[data],]
            content_body = {
                "values": record_list
            }
            if target_row == -1:
                target_row = self.row_prev_record
            range_name = self.sheet_name + f'!{column_name}{target_row}'
            result = sheet.values().update(
                spreadsheetId=self.spreadsheet_id, range=range_name,
                valueInputOption='USER_ENTERED', body=content_body).execute() # 2020/12/23 modify valueInputOption from 'RAW' to 'USER_ENTERED' as Bill's request
        except Exception as e:
            print(e)
            raise Exception
        return True

    def update_columns(self, data, target_row=-1): # data - dictionary e.g. data = {'B':'FAIL', 'C':'1:33:22'}
        try:
            sheet = self.service.spreadsheets()
            if target_row == -1:
                target_row = self.row_prev_record
            print(f'{target_row=}')
            for key in data.keys():
                if key in self.row_dict.keys():
                    self.row_dict[key] = data[key]
            print(self.row_dict)
            data_list = list(self.row_dict.values())
            print(data_list)
            last_key_of_header = list(self.header.keys())[-1]
            print(f'last key of dict:{last_key_of_header}')
            body = {
                    "valueInputOption": 'USER_ENTERED',
                    "data": [{
                        "range": self.sheet_name + f'!A{target_row}:{last_key_of_header}',
                        "majorDimension": "ROWS",
                        "values": [data_list]
                    }]
            }
            sheet.values().batchUpdate(spreadsheetId=self.spreadsheet_id, body=body).execute()
        except Exception as e:
            print(e)
            raise Exception
        return True

    def get_columns(self, target_row=-1): # for single row
        try:
            last_key_of_header = list(self.header.keys())[-1]
            if target_row == -1:
                target_row = self.row_prev_record
            ranges = self.sheet_name + f'!A{target_row}:{last_key_of_header}'
            response = self.service.spreadsheets().values().batchGet(spreadsheetId=self.spreadsheet_id, ranges=ranges, majorDimension='ROWS').execute()
        except Exception as e:
            print(e)
            raise Exception
        return response

    def get_columns_of_range(self, target_row=-1): # for multi-row
        try:
            last_key_of_header = list(self.header.keys())[-1]
            if target_row == -1:
                return []
            ranges = self.sheet_name + f'!A{self.row_start+1}:{last_key_of_header}{target_row}'
            response = self.service.spreadsheets().values().batchGet(spreadsheetId=self.spreadsheet_id, ranges=ranges, majorDimension='ROWS').execute()
        except Exception as e:
            print(e)
            raise Exception
        return response

    def get_first_empty_row(self):
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.spreadsheet_id,
                                    range=self.sheet_name).execute()
        values = result.get('values', [])
        target_row = self.row_start + len(values)
        print(f'{target_row=}')
        return target_row


    def update_result(self, data, target_row=-1):
        try:
            self.update_columns(data, target_row)
        except Exception:
            raise Exception
        return True


def create_spread_sheet(spreadsheet_name, writer_mail):
    if not os.path.exists(client_secret) or not os.path.exists(service_account_file):
        print("[create_spread_sheet] Crential json file for spreadsheet is not exists")
        return False

    gc = pygsheets.authorize(client_secret=client_secret, service_account_file=service_account_file)
    spreadsheet_key = ""
    spreadsheets_list = gc.spreadsheet_titles()

    if spreadsheet_name in spreadsheets_list:
        sh = gc.open(spreadsheet_name)
        spreadsheet_key = sh.id
        print(f"[create_spread_sheet] spreadsheet {spreadsheet_name} is existed")
    else:
        sh = gc.create(title=spreadsheet_name)
        if isinstance(writer_mail, str):
            sh.share(writer_mail, role="writer", type="user")
            print("single")
        elif isinstance(writer_mail, list):
            print("multiple")
            for mail in writer_mail:
                sh.share(mail, role="writer", type="user")
        sh.share("", role="writer", type="anyone")
        spreadsheet_key = sh.id
    print("[create_spread_sheet] spread sheet list = ", gc.spreadsheet_titles())
    survey_url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_key}/'
    print(f"[create_spread_sheet] survey_url = {survey_url}")

    return spreadsheet_key


def delete_spread_sheet(spreadsheet_name):
    if not os.path.exists(client_secret) or not os.path.exists(service_account_file):
        print("[delete_spread_sheet] Crential json file for spreadsheet is not exists")
        return False
    gc = pygsheets.authorize(client_secret=client_secret, service_account_file=service_account_file)
    spreadsheets_list = gc.spreadsheet_titles()

    if spreadsheet_name in spreadsheets_list:
        sh = gc.open(spreadsheet_name)
        sh.delete()
        return True

    print(f"[delete_spread_sheet] spreadsheet {spreadsheet_name} is not existed")
    return False


def get_spread_sheet_list():
    if not os.path.exists(client_secret) or not os.path.exists(service_account_file):
        print("[get_spread_sheet_list] Crential json file for spreadsheet is not exists")
        return False
    gc = pygsheets.authorize(client_secret=client_secret, service_account_file=service_account_file)
    spreadsheets_list = gc.spreadsheet_titles()
    print("[get_spread_sheet_list] spreadsheets_list = ", spreadsheets_list)

    return spreadsheets_list


def delete_work_sheet(spreadsheet_name, work_sheet_name):
    if not os.path.exists(client_secret) or not os.path.exists(service_account_file):
        print("[delete_spread_sheet] Crential json file for spreadsheet is not exists")
        return False
    gc = pygsheets.authorize(client_secret=client_secret, service_account_file=service_account_file)
    spreadsheets_list = gc.spreadsheet_titles()

    if spreadsheet_name in spreadsheets_list:
        sh = gc.open(spreadsheet_name)
        work_sheet = sh.worksheet_by_title(work_sheet_name)
        sh.del_worksheet(work_sheet)
        return True

    print(f"[delete_work_sheet] worksheet {work_sheet_name} of {spreadsheet_name} is not existed")
    return False


if __name__ == '__main__':
    # Test Code ==========================
    # initial google_api object
    spreadsheet_id = '1iQsmn5QOddwovzaxb5fcQt3gR2Ts__6iajQm4CSd4Oo' # google_sheet_api_test
    sheet_name = 'test_sheet'
    header_custom = ['Pass', 'Fail', 'Skip', 'N/A', 'Total time']
    obj_google_api = GoogleApi(sheet_name, header_custom, 1, spreadsheet_id)

    # add new record w/ test information
    import datetime
    now = datetime.datetime.now()
    new_record = {'Date': now.date().strftime("%Y-%m-%d"),
                  'Time': now.time().strftime("%H:%M:%S"),
                  'Script_Name': 'aU_SFT',
                  'Script_Ver': '1.0.0',
                  'SR_No': 'YOU200722-05',
                  'TR_No': '',
                  'Build_No': '209176',
                  'Prod_Ver': '6.2.0',
                  'Prod_Ver_Type': 'Prod',
                  'OS': 'Android',
                  'OS_Ver': '10.0',
                  'Device_ID': '98TAY16WK9'}
    obj_google_api.add_new_record(new_record)

    # update result of previous record
    data = {'Pass': '111', 'Fail': '0', 'Skip': '1', 'N/A': '0', 'Total time': '3:31:55'}
    obj_google_api.update_result(data)

    print(f'Done.')