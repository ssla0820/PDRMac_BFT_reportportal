import os
import sys
import time
import datetime
import base64

from selenium.webdriver import Chrome, Edge
from selenium.webdriver import ChromeOptions, EdgeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.service import Service as edgeService
from selenium.webdriver.support.ui import Select

# 2024/8/6 Volath: for check selenium version
try:
    import pkg_resources

    selenium_ver = pkg_resources.get_distribution("selenium").version
    if tuple(map(int, selenium_ver.split('.'))) < tuple(map(int, '4.16.0'.split('.'))):
        raise Exception('Please check selenium is equal 4.16.0 or above')
except Exception as e:
    raise Exception(f'{e}')

from os.path import dirname as _dir
sys.path.insert(0, _dir(__file__))
from password import Authorization

try:
    from ..log import logger
except:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))
    print(f'Add {os.path.dirname(SCRIPT_DIR)} to system path, Please put log.py under the same folder of this file', )
    from log import logger


# locator of TR/QR website
option_report_type = ("xpath", "//select[@name='QRtmpid']")
btn_create = ("xpath", "//select[@name='QRtmpid']/following-sibling::input[@type='submit']")
btn_create_qr = ("xpath", "//input[@value='Create' and @class='BTN']")
txt_short = ("xpath", "//input[@name='ShortDescription']")
txt_build_day = ("xpath", "//td[contains(text(), 'Build Day')]//input[@type='text']")
txt_test_result = ("xpath", "//td[contains(text(), 'Test Result(Ex: OK, Fail, Find Major Bugs)')]//input[@type='text']")
txt_test_detail = ("xpath", "//textarea")
btn_add_file = ("xpath", "//a[@onclick='addFile()']")
btn_file = ("xpath", "//input[@type='File']")
btn_save = ("xpath", "//input[@type='Submit']")
link_qr_from_tr = ("xpath", "(//*[text()='QA Report: ']/parent::*/parent::*/parent::*/parent::*/parent::*/tr//a)[last()-1]")
link_qr_from_qr = ("xpath", "//a[contains(text(), 'QR')]")
edit_comments_area = ("xpath", "//td/textarea")
btn_save_comments = ("xpath", "//input[@value='Save Comments']")
btn_upload_in_tr = ("xpath", "//input[@value=' Upload/Delete Files ']")
btn_choose_file = ("xpath", "//input[@type='File']")
btn_upload_file = ("xpath", "//input[@value='Upload File(s) & Delete File(s)']")

debug_mode = False


class Qr_Operation():
    def __init__(self, para_dict): # prod_name, sr_no, tr_no, prog_path_sub, dest_path, work_dir (for password and tr_db file), mail_list(list)
        try:
            self.user_name = ''
            self.password = ''
            self.tr_no = ''
            if 'tr_no' in para_dict.keys():
                self.tr_no = para_dict['tr_no']
            self.qr_dict = {'short_description': 'AutoTest Report',
                            'build_day': datetime.date.today().strftime('%m%d'),
                            'test_result': 'AutoTest Report Result',
                            'test_result_details': 'AutoTest Report Result Detail',
                            'upload_files_1': '',
                            'upload_files_2': '',
                            'upload_files_3': '', }
            if 'qr_dict' in para_dict.keys():
                self.qr_dict = para_dict['qr_dict']
            self.tr_dict = {'comments': 'AutoTest Comment Test',
                            'upload_files': '', }
            if 'tr_dict' in para_dict.keys():
                self.tr_dict = para_dict['tr_dict']
            self.work_dir = os.path.dirname(__file__)
            if 'work_dir' in para_dict.keys() and para_dict['work_dir']:
                self.work_dir = para_dict['work_dir']
            if debug_mode: print(f'Init - work_dir={self.work_dir}')
            self.cookies = {'domain': '.cyberlink.com', 'httpOnly': True, 'name': 'ECLID', 'path': '/', 'secure': True,
                            'value': self.read_eclid_file()}
            self.password_file = 'password'
            self.err_msg = ''
            # decrypt the username/ password
            obj_authorization = Authorization(self.work_dir)
            passwd_list = obj_authorization.decryption_vigenere_clt_account()
            self.user_name = passwd_list[0]
            self.password = passwd_list[1]
            # initial browser
            self.options = EdgeOptions() if para_dict["browser"] == 'edge' else ChromeOptions()
            self.options.add_experimental_option("excludeSwitches", ['enable-automation', 'ignore-certificate-errors', 'enable-logging', 'disable-popup-blocking'])  # 新版本關閉“chrome正受到自動測試軟件的控製”信息
            self.options.add_argument("--no-first-run")
            self.options.add_argument('--disable-gpu')
            self.options.add_argument('--no-sandbox')
            self.options.add_argument('--allow-insecure-localhost')
            self.options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
            self.driver = Edge(service=edgeService(), options=self.options) if para_dict["browser"] == 'edge' else Chrome(service=Service(), options=self.options)
            self.driver.implicitly_wait(10)
        except Exception as e:
            err_msg = f'Exception occurs. Incorrect format of parameter or missing keys. Error={e}'
            logger(err_msg)
            self.err_msg = err_msg

    def read_eclid_file(self):
        # file_name = 'eclid'
        file_name = os.path.normpath(os.path.join(self.work_dir, 'eclid'))
        logger(f'eclid file path={file_name}')
        if debug_mode: print(f'eclid file path={file_name}')
        ECL_ID = ''
        if not os.path.exists(file_name):
            if debug_mode: print('eclid file does not exist')
            logger('eclid file does not exist')
        else:
            # read ECLID from file
            if debug_mode: print('read eclid file')
            f = open(file_name, "rb")
            encoded = f.read()
            bytes_content = base64.b64decode(encoded)
            ECL_ID = bytes_content.decode('utf-8')
            logger('read eclid file successfully')
        if debug_mode: print(f'ECLID: {ECL_ID}')
        return ECL_ID

    def el(self, locator):
        if debug_mode: print(locator)
        return self.driver.find_element(*locator)

    def els(self, locator):
        if debug_mode: print(locator)
        return self.driver.find_elements(*locator)

    def is_el(self, locator):
        try:
            self.el(locator)
        except Exception as e:
            self.err_msg = e
            if debug_mode: print(e)
            return False
        return True

    def click(self, locator):
        try:
            self.el(locator).click()
        except Exception as e:
            self.err_msg = e
            if debug_mode: print(e)
            raise Exception
        return True

    def select_by_visible_text(self, locator, value):
        try:
            s = Select(self.el(locator))
            s.select_by_visible_text(value)
            return True
        except Exception as e:
            self.err_msg = e
            if debug_mode: print(e)
            return False

    def set_text(self, locator, text, clear_flag=True):
        try:
            text_area = self.el(locator)
            if clear_flag is True:
                try:
                    text_area.clear()
                except Exception as e:
                    self.err_msg = e
                    if debug_mode: print("ERROR: %s page cannot clear the text field: %s" % (self, locator))
                    raise Exception
            try:
                return text_area.send_keys(text)
            except Exception as e:
                self.err_msg = e
                if debug_mode: print("ERROR: %s page cannot set the text field: %s" % (self, locator))
                raise Exception
        except Exception as e:
            self.err_msg = e
            if debug_mode: print("ERROR: %s page cannot find the text field: %s" % (self, locator))
            raise Exception

    def add_file(self, locator, file_path):
        try:
            if not os.path.isfile(file_path):
                logger('File is missing')
                return False
            file_locator = self.el(locator)
            file_locator.send_keys(file_path)
            return True
        except Exception as e:
            self.err_msg = e
            if debug_mode: print(e)
            return False

    def select_qr_type(self, text='Standard Report'):
        return self.select_by_visible_text(option_report_type, text)

    def click_btn_create(self):
        return self.click(btn_create)

    def input_short_description(self, text):
        return self.set_text(txt_short, text)

    def input_build_day(self, text):
        if not self.is_el(txt_build_day):
            return False
        return self.set_text(txt_build_day, text)

    def input_test_result(self, text):
        return self.set_text(txt_test_result, text)

    def input_test_detail(self, text):
        return self.set_text(txt_test_detail, text)

    def input_file(self, index, file_path):
        locator_file = (btn_file[0], f'({btn_file[1]})[{index}]')
        return self.add_file(locator_file, file_path)

    def input_file_in_tr(self, file_path):
        return self.add_file(btn_choose_file, file_path)

    def click_btn_save(self):
        return self.click(btn_save)

    def get_qr_link(self, from_qr=True, timeout=30):
        current_time = time.time()
        result = ''
        while current_time - time.time() < timeout:
            if from_qr:
                try:
                    link_locator = self.el(link_qr_from_qr)
                    result = link_locator.get_attribute("href")
                except:
                    pass
                if result:
                    break
                time.sleep(1)
            else:
                try:
                    link_locator_list = self.els(link_qr_from_qr)
                    result = link_locator_list[-2].get_attribute("href")
                except:
                    pass
                if result:
                    break
                time.sleep(1)
        return result

    def refresh_webpage(self):
        self.driver.refresh()
        result = True
        time.sleep(1)
        return result

    def close_browser(self):
        return self.driver.close()

    def qr_operation(self):
        try:
            self.user_name = self.user_name.replace('clt\\', '')
            url_authorize = f'https://{self.user_name}:{self.password}@ecl.cyberlink.com/TR/TRHandle/HandleMainTR.asp?TRCode={self.tr_no}'
            url_tr = f'https://ecl.cyberlink.com/TR/TRHandle/HandleMainTR.asp?TRCode={self.tr_no}'
            self.driver.get(url_authorize)
            self.driver.add_cookie(self.cookies)
            time.sleep(1)
            self.driver.get(url_tr)
            main_page = self.driver.current_window_handle
            time.sleep(2)
            self.select_qr_type('Standard Report')
            self.click_btn_create()
            time.sleep(5)
            browser_tabs = self.driver.window_handles
            self.driver.switch_to.window(browser_tabs[1])
            time.sleep(1)
            self.input_short_description(self.qr_dict['short_description'])
            self.input_build_day(self.qr_dict['build_day'])
            self.input_test_result(self.qr_dict['test_result'])
            self.input_test_detail(self.qr_dict['test_result_details'])
            if self.qr_dict.get('upload_files_1'):
                self.input_file(1, self.qr_dict['upload_files_1'])
            if self.qr_dict.get('upload_files_2'):
                self.input_file(2, self.qr_dict['upload_files_2'])
            if self.qr_dict.get('upload_files_3'):
                self.input_file(3, self.qr_dict['upload_files_3'])
            print(f'Save Report') if debug_mode else self.click_btn_save()
            time.sleep(20) if debug_mode else time.sleep(5)
            # self.driver.switch_to.window(main_page)
            # self.refresh_webpage()
            qr_link = self.get_qr_link(from_qr=True) if not debug_mode else url_tr
            return qr_link
        except Exception as e:
            self.err_msg = e
            logger(f'Exception occurs. Error={e}')

    def tr_operation(self):
        try:
            self.user_name = self.user_name.replace('clt\\', '')
            url_authorize = f'https://{self.user_name}:{self.password}@ecl.cyberlink.com/TR/TRHandle/HandleMainTR.asp?TRCode={self.tr_no}'
            url_tr = f'https://ecl.cyberlink.com/TR/TRHandle/HandleMainTR.asp?TRCode={self.tr_no}'
            self.driver.get(url_authorize)
            self.driver.add_cookie(self.cookies)
            time.sleep(1)
            self.driver.get(url_tr)
            time.sleep(2)
            self.set_text(edit_comments_area, self.tr_dict['comments'])
            self.click(btn_save_comments)
            time.sleep(3)
            self.click(btn_upload_in_tr)
            self.add_file(btn_choose_file, self.tr_dict['upload_file'])
            self.click(btn_upload_file)
            time.sleep(20) if debug_mode else time.sleep(3)
        except Exception as e:
            self.err_msg = e
            logger(f'Exception occurs. Error={e}')
            return False
        return True


def create_qr(para_dict):
    dict_result = {'result': True, 'error_log': '', 'qr_link': ''}
    oqr = ''
    try:
        oqr = Qr_Operation(para_dict)
        dict_result['qr_link'] = oqr.qr_operation()
        oqr.close_browser()
        if not dict_result['qr_link']:
            dict_result['result'] = False
            dict_result['error_log'] = 'Get QR link failed'
    except Exception as e:
        oqr.err_msg = e
        dict_result['result'] = False
        dict_result['error_log'] = oqr.err_msg
    logger(f'{dict_result=}')
    return dict_result


def tr_comment(para_dict):
    dict_result = {'result': True, 'error_log': ''}
    oqr = ''
    try:
        oqr = Qr_Operation(para_dict)
        dict_result['result'] = oqr.tr_operation()
        oqr.close_browser()
        if not dict_result['result']:
            dict_result['result'] = False
            dict_result['error_log'] = 'Comment on TR failed'
    except Exception as e:
        oqr.err_msg = e
        dict_result['result'] = False
        dict_result['error_log'] = oqr.err_msg
    logger(f'{dict_result=}')
    return dict_result


if __name__ == '__main__':
    print('Start QR Creation')
    test_para_dict = {'browser': 'chrome',
                      'tr_no': 'TR221214-001',
                      'qr_dict': {'short_description': 'AutoTest Report 111',
                                  'build_day': datetime.date.today().strftime('%m%d'),
                                  'test_result': 'AutoTest Report Result 111',
                                  'test_result_details': 'AutoTest Report Result Detail 111',
                                  'upload_files_1': r"C:\Users\QAAT\Downloads\test1.txt",
                                  'upload_files_2': r"C:\Users\QAAT\Downloads\test2.txt",
                                  'upload_files_3': "", },
                      'tr_dict': {'comments': 'AutoTest Comment Test 111',
                                  'upload_file': r"C:\Users\volath_liu\Downloads\PDR_Content Pack_AT Proposal_Jason_v1.00.pptx", },
                      'work_dir': os.path.dirname(__file__),
                      }
    # print(create_qr(test_para_dict))
    print(tr_comment(test_para_dict))
