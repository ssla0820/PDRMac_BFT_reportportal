import os
import datetime

# Options and Desired_Capability

# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# Chrome ------------------------------------------------------
# desired_capability = DesiredCapabilities.CHROME
# desired_capability['goog:loggingPrefs'] = {'browser': 'ALL'}

# Edge --------------------------------------------------------
# from msedge.selenium_tools import EdgeOptions
# desired_capability = DesiredCapabilities.EDGE
# desired_capability['ms:loggingPrefs'] = {'browser': 'ALL'}
# desired_capability['acceptInsecureCerts'] = bool(True)
# options.set_capability("ms:edgeOptions", desired_capability)
# -------------------------------------------------------------


class BrowserConsoleLog:
    def __init__(self, driver, filename, folder_path=None):
        self.log_file = f'{filename}.log'
        if folder_path:
            self.log_file = f'{os.path.join(folder_path, filename)}.log'
        self.driver = driver

    @staticmethod
    def epoch_time_to_human_date(timestamp):
        datetime_obj = datetime.datetime.fromtimestamp(timestamp / 1000)
        datetime_str = datetime_obj.strftime("%Y-%m-%d  %H:%M:%S")
        return datetime_str

    def dump_console_log(self):
        log_content = []
        for entry in self.driver.get_log('browser'):
            line = f'[{self.epoch_time_to_human_date(entry["timestamp"])}] {entry}'
            log_content.append(line + '\n')

        f = open(self.log_file, 'w', encoding="utf-8")
        f.writelines(log_content)
        f.close()
        return True
