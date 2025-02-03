import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import time, inspect, datetime, pytest, re, configparser
os.chdir(os.path.dirname(__file__))
from types import SimpleNamespace


from ATFramework import MyReport, logger
from ATFramework.drivers.driver_factory import DriverFactory
from pages.page_factory import PageFactory
from configs.app_config import *
from pages.locator import locator as L
from globals import *


# read PDR cap >>
app = SimpleNamespace(**PDR_cap)
# read PDR cap <<

# create driver & page >>
mwc = DriverFactory().get_mac_driver_object('mac', app.app_name, app.app_bundleID, app.app_path)
main_page = PageFactory().get_page_object('main_page', mwc)
media_room_page = PageFactory().get_page_object('media_room_page', mwc)
voice_over_recording_page = PageFactory().get_page_object('voice_over_recording_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Voice-Over Recording Room.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Voice-Over_Recording/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Voice-Over_Recording/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Voice_Over_Recording():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        time.sleep(DELAY_TIME*4)
        yield mwc
        main_page.close_app()
        main_page.clear_cache()






    @classmethod
    def setup_class(cls):
        main_page.clear_cache()
        # for update the correct module start time of report (2021/04/20)
        now = datetime.datetime.now()
        report.add_ovinfo('time', now.time().strftime("%H:%M:%S"))
        report.start_time = time.time()
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_init('Voice-Over_Recording')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"video speed result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           report.get_ovinfo('skip'),
                           report.get_ovinfo('duration'))
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                               report.get_ovinfo('skip'), report.get_ovinfo('duration'))
        report.show()
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_1(self):
        with uuid('a0972f8a-98d9-44b1-b6f1-a52fcc01e876') as case:
            # [I8] Enter Voice-Over Recording Room
            result = main_page.enter_room(7)
            case.result = result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid("1ee8363a-508d-4a36-b4ef-a22f323c31c6") as case:
            # [I9] Hotkey enter (F10)
            voice_over_recording_page.tap_VoiceRecordRoom_hotkey()
            time.sleep(DELAY_TIME*2)
            # Check [Device] button existed
            check_result = voice_over_recording_page.exist(L.voice_over_recording.btn_device)
            if not check_result:
                case.result = False
            else:
                case.result = True



    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        with uuid("5922c949-e9fb-4e27-b640-1e1cc084e266") as case:
            voice_over_recording_page.tap_VoiceRecordRoom_hotkey()
            time.sleep(DELAY_TIME*2)
            # [I20] Display Device Name
            current_image = voice_over_recording_page.snapshot(locator=L.voice_over_recording.txt_audio_detect, file_name=Auto_Ground_Truth_Folder + 'I20_DeviceName.png')
            logger(f"{current_image=}")
            compare_result = voice_over_recording_page.compare(Ground_Truth_Folder + 'I20_DeviceName.png', current_image)
            #logger(compare_result)
            case.result = compare_result


