from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import requests
import urllib
from datetime import datetime, timedelta
from .log import logger
import os
import re
import platform
import chromedriver_autoinstaller # pip install chromedriver-autoinstaller
import pandas as pd # dependency - pip install openpyxl

# ==========================================================================================
# Description: the common module for querying boomerang record from backend server
# Revise:
# v1.00 - first version (2021/10/15)
# ==========================================================================================

def get_url_file_size(url):
    r = requests.head(url)
    print(f"{r.headers['Content-Length']} bytes")
    return int(r.headers['Content-Length'])

def get_fake_email():
    datetime_dt = datetime.today()
    datetime_str = datetime_dt.strftime("%Y%m%d_%H%M%S")
    return f'{datetime_str}@gmail.com'

def datetime_get_today():
    datetime_dt = datetime.today()
    datetime_str = datetime_dt.strftime("%Y-%m-%d")
    return datetime_str

def datetime_get_yesterday():
    yesterday = datetime.now() - timedelta(1)
    datetime_str = yesterday.strftime("%Y-%m-%d")
    return datetime_str


# Sign-in Page
edittext_account = "//input[@id='email']"
edittext_password = "//input[@id='password']"
btn_sign_in = "//button[@id='Sign-in']"
cbx_product_name = "//select"
cbx_product_version = "(//select)[2]"
btn_advance = "//img[@class='gwt-Image']"
edittext_email = "(//input[@class='gwt-TextBox'])[10]"
edittext_start_date = "(//input[@class='gwt-DateBox'])[1]"
edittext_end_date = "(//input[@class='gwt-DateBox'])[2]"
edittext_app_version = "(//input[@class='gwt-TextBox'])[3]"
btn_search = "//button[@class='gwt-Button']"
wnd_loading_dialog = "//tr[@class='dialogMiddle']"
btn_export_log_to_excel = "(//button[@class='gwt-Button'])[4]"
# first record of main query page
col_id_of_first_record = "//table[@class='custCellTable']/tbody/tr[@class='GBG2FFLDPC']/td[3]/div/a"
# detail record page
btn_download_log = "//tbody//table[@class='custCellTable']//td[@class='GBG2FFLDOC GBG2FFLDAD nowrap'][2]//a"

# ((//table[@class='custCellTable'])[3]//tbody/tr)[2]//td[23] > email
# detail row
row_unit = "(//table[@class='custCellTable'])[3]//tbody/tr"
col_email = "//td[23]/div"
col_note = "//td[24]/div"
col_download_log = "//td[14]//a"
btn_last_page_of_detail_result = "(//body/table/tbody/tr[3]//table)[6]/tbody/tr/td[5]"

# default chrome download path
default_browser_download_path = ''
# boomerage log:
# - 2021/10/01 15:47 send log > query log time 2021/10/01 00:47 => 差了15個小時


class QueryBackendBoomerang:
    def __init__(self, account, passwd, email, start_date='', end_date='', note='', browser_default_download_path=''):
        # self.chromedriver = f'{os.path.dirname(os.path.abspath(__file__))}/chrome_driver/for_macos/chromedriver'
        self.chromedriver = 'chromedriver'
        # self.driver = webdriver.Chrome(self.chromedriver)
        # self.driver = None
        self.account = account
        self.passwd = passwd
        self.email = email
        self.start_date = start_date
        self.end_date = end_date
        if self.start_date == '':
            self._set_start_date()
        if self.end_date == '':
            self._set_end_date()
        self.log_file_size = 0
        self.log_file_name = ''
        self.url_record_detail = ''
        self.record_id = ''
        self.note = note
        self.errmsg_check_log_file = ''
        self.browser_default_download_path = browser_default_download_path

        # change the chromedriver for windows
        if platform.system() == 'Windows':
            # self.chromedriver = f'{os.path.dirname(os.path.abspath(__file__))}/chrome_driver/for_windows/chromedriver.exe'
            self.chromedriver = 'chromedriver.exe'

        webdriver_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils', 'chrome_driver')
        chromedriver_autoinstaller.install(False, os.path.normpath(
            webdriver_path))  # Check if the current version of chromedriver exists
        # and if it doesn't exist, download it automatically,
        # then add chromedriver to path
        self.driver = webdriver.Chrome(self.chromedriver)
        self.driver.implicitly_wait(10)

    def _set_start_date(self, day_before=2):
        datetime_dt = datetime.now() - timedelta(day_before)
        self.start_date = datetime_dt.strftime("%Y-%m-%d")
        return True

    def _set_end_date(self):
        datetime_dt = datetime.today()
        datetime_str = datetime_dt.strftime("%Y-%m-%d")
        self.end_date = datetime_str
        return True

    def _set_edittext_value(self, locator, value, is_click_enter=1):
        input_start_date = self.find_element_by_xpath(locator)  # set start date
        input_start_date.send_keys(value)
        if is_click_enter:
            input_start_date.send_keys(Keys.ENTER)
        time.sleep(1)
        return True

    def _select_combobox_option(self, locator, text):
        select = Select(self.find_element_by_xpath(locator))
        select.select_by_visible_text(text)
        return True

    def _select_product(self, name):
        return self._select_combobox_option(cbx_product_name, name)

    def _select_product_version(self, txt_version):
        return self._select_combobox_option(cbx_product_version, txt_version)

    def find_element_by_xpath(self, locator):
        return self.driver.find_element(By.XPATH, locator)

    def find_elements_by_xpath(self, locator):
        return self.driver.find_elements(By.XPATH, locator)

    def _get_url_file_size(self, url):
        try:
            self.log_file_size = 0 # initialize
            r = requests.head(url)
            logger(f"{r.headers['Content-Length']} bytes")
            self.log_file_size = int(r.headers['Content-Length'])
        except Exception as e:
            logger(f'Exception occurs. error={e}')
            return False
        return True

    def _get_url_file_name(self, url):
        pattern = r"(\d+.zip)"
        result = re.findall(pattern, url)
        filename = result[0]
        if '.zip' not in filename:
            logger(f'Fail to get the file name from url. {filename=}')
            return False
        self.log_file_name = filename
        logger(f'log_file_name={self.log_file_name}')
        return True

    def _is_no_loading_dialog(self, timeout=30):
        start_time = time.time()
        is_loading_ok = False
        while time.time() - start_time < timeout:
            try:
                self.find_element_by_xpath(wnd_loading_dialog)
                logger('loading dialog is found')
                time.sleep(1)
            except:
                logger('No Loading dialog is on top')
                is_loading_ok = True
                break

        if not is_loading_ok:
            logger('Timeout. Search record FAIL.')
            return False
        logger('Search record OK.')
        return True

    def _check_first_record(self): # expect only one record is shown after searching by fake email
        try:
            col_id_of_record = self.find_element_by_xpath(col_id_of_first_record)
            self.record_id = col_id_of_record.text
            logger(f'record is found. {self.record_id=}')
            self.url_record_detail = col_id_of_record.get_attribute("href")
            logger(f'hyperlink_detail={self.url_record_detail}')
        except:
            logger('No record is found.')
            return False
        return [self.record_id, self.url_record_detail]

    def _check_uploaded_log_size_of_record(self, mode=1): # criterial: size of log must > 0 bytes, get row by email
        try:
            self.errmsg_check_log_file = ''
            if mode == 1:
                col_unit = col_email
                verify_value = self.email
            else:
                col_unit = col_note
                verify_value = self.note
            self.driver.get(self.url_record_detail)
            self.driver.implicitly_wait(5)
            if not self._is_no_loading_dialog():
                self.driver.close()
                return False
            # click the last page button to go to last page
            time.sleep(3)
            self.find_element_by_xpath(btn_last_page_of_detail_result).click()
            # get the row by checking email
            time.sleep(3)
            els_row = self.find_elements_by_xpath(row_unit)
            logger(f'the amount of row={len(els_row)}')
            target_row = -1
            for row in range(len(els_row)):
                try:
                    col_value = self.find_element_by_xpath(f'({row_unit})[{row+1}]{col_unit}')
                    logger(f'email #{row+1}={col_value.text}')
                    if verify_value == col_value.text:
                        target_row = row+1
                        break
                except:
                    continue
            if target_row == -1:
                logger(f'Fail to find record with email {self.email}.')
                self.errmsg_check_log_file = f'[Check LOGFILE]Fail to find record with email {self.email}.'
                return False
            logger(f'{target_row=}')
            url_log = self.find_element_by_xpath(f'({row_unit})[{target_row}]{col_download_log}').get_attribute("href")
            logger(f'download log url={url_log}')
            # get the file name from url
            self._get_url_file_name(url_log)
            # get the log file size from header
            result_log_size = self._get_url_file_size(url_log) # in bytes
            logger(f'{self.log_file_size=} byte(s)')
            if result_log_size:
                if self.log_file_size > 0:
                    logger('Log size OK.')
                else:
                    logger(f'Invalid log size={self.log_file_size}. It should be > 0 bytes')
                    self.errmsg_check_log_file = f'[Check LOGFILE] Invalid log size={self.log_file_size}. It should be > 0 bytes'
                    return False
            else:
                logger('Fail to get log size')
                self.errmsg_check_log_file = f'[Check LOGFILE] Fail to get log size'
                return False
        except Exception as e:
            logger(f'Exception occurs. error={e}')
            self.errmsg_check_log_file = f'[Check LOGFILE] Exception occurs. error={e}'
            return False
        return True

    def _generate_fake_email(self):
        datetime_dt = datetime.today()
        datetime_str = datetime_dt.strftime("%Y%m%d_%H%M%S")
        return f'{datetime_str}@gmail.com'

    def query(self, mode=1): # in deatail page, find donwload url by col email (fake email)
        try:
            # navigate to backend boomerage page
            logger('Start to query backend boomerang record')
            self.driver.get(f"http://{self.account}:{self.passwd}@backend2.gocyberlink.com/boomerang/")
            # Click [Advance] > Input eMail
            self.find_element_by_xpath(btn_advance).click()  # click advance image to extend
            time.sleep(1)
            self._set_edittext_value(edittext_email, self.email, 0)
            # Input Start/ End Date
            self._set_edittext_value(edittext_start_date, self.start_date)
            self._set_edittext_value(edittext_end_date, self.end_date)
            # click [Search]
            self.find_element_by_xpath("//button[@class='gwt-Button']").click()
            time.sleep(3)
            # check if loading dialog is on top
            if not self._is_no_loading_dialog():
                self.driver.close()
                return False
            # get the id & hyperlink of 1st record
            list_result = self._check_first_record()
            if not list_result:
                self.driver.close()
                return False
            # navigate to record detail page > check the uploaded log size (should > 0 bytes)
            if not self._check_uploaded_log_size_of_record(mode) and 'Fail to find record' in self.errmsg_check_log_file:
                self.driver.close()
                return False
        except Exception as e:
            logger(f'Exception occurs. error={e}')
            return False
        # time.sleep(5)
        logger('Finish to query backend boomerang record')
        self.driver.close()
        return True

    def query_v2(self, prod_name, version, app_ver):
        try:
            # navigate to backend boomerage page
            logger('Start to query backend boomerang record')
            retry = 0
            while True:
                logger(f'Connect to Boomerang page - {retry}')
                try:
                    # self.driver.get(f"https://{self.account}:{self.passwd}@backend2.cyberlink.com/boomerang/")
                    self.driver.get("https://backend2.cyberlink.com/boomerang/")
                    # input Account/ Password to sign in
                    self._set_edittext_value(edittext_account, self.account, False)
                    self._set_edittext_value(edittext_password, self.passwd, False)
                    self.find_element_by_xpath(btn_sign_in).click()
                    time.sleep(5)
                    if self.find_element_by_xpath(cbx_product_name):
                        logger('Enter page correctly.')
                        break
                except Exception as e:
                    retry += 1
                    time.sleep(3)
                    if retry > 5:
                        raise
            # Select Product and version
            self._select_product(prod_name)
            time.sleep(3)
            self._select_product_version(version)
            # Input Start/ End Date
            self._set_edittext_value(edittext_start_date, self.start_date)
            self._set_edittext_value(edittext_end_date, self.end_date)
            # Click [Advance]
            self.find_element_by_xpath(btn_advance).click()  # click advance image to extend
            time.sleep(1)
            # app version
            self._set_edittext_value(edittext_app_version, app_ver, 0)
            # click [Search]
            self.find_element_by_xpath(btn_search).click()
            time.sleep(3)
            # check if loading dialog is on top
            if not self._is_no_loading_dialog():
                self.driver.close()
                return False
        except Exception as e:
            logger(f'Exception occurs. error={e}')
            return False
        # time.sleep(5)
        logger('Finish to query backend boomerang record')
        # self.driver.close()
        return True

    def close_webpage(self):
        return self.driver.close()

    def export_log_to_excel(self, timeout=30):
        logger(f'export_log_to_excel - Start')
        # remove exist excel log file
        log_file = os.path.join(self.browser_default_download_path, 'exportlogs.xlsx')
        if os.path.exists(log_file):
            os.remove(log_file)
            logger('remove exist log file')
        retry = 0
        is_completed = False
        while True:
            self.find_element_by_xpath(btn_export_log_to_excel).click()
            start_time = time.time()
            is_completed = False
            while time.time() - start_time < timeout:
                if os.path.exists(log_file):
                    logger('Export excel log file OK.')
                    is_completed = True
                    break
                time.sleep(2)
            retry += 1
            if is_completed or retry > 5:
                break
        if not is_completed:
            logger('Fail to file export log file.')
            return False
        return True

    def get_top_n_from_export_log(self, top_n=5, filter_col='FUNCTION'):
        dict_result = dict()
        list_top_n = list()
        log_file = os.path.join(self.browser_default_download_path, 'exportlogs.xlsx')
        if not os.path.exists(log_file):
            logger(f'No log file is found.')
            return list_top_n
        df = pd.read_excel(log_file, sheet_name='exportLog', usecols=[filter_col])
        logger(f'len df={len(df)}')

        for index in range(len(df)):
            item = df.at[index, filter_col]
            if item not in dict_result.keys():
                dict_result[item] = 1
                continue
            dict_result[item] += 1

        # Sort dict. by value
        dict_result_sorted = dict(sorted(dict_result.items(), key=lambda item: item[1], reverse=True))
        # get Top 5 modules
        logger(f'Top 5 {filter_col} ======')
        amount = 0
        for key in dict_result_sorted.keys():
            logger(f'[{amount + 1}] {key}[{dict_result_sorted[key]}]')
            list_top_n.append(str(key)) # handle nan of FUNCTION as empty <float> type
            amount += 1
            if amount > 4:
                break
        logger(f'{list_top_n=}')
        return list_top_n
