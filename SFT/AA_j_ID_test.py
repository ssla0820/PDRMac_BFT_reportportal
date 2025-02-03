#test
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
mask_designer_page = PageFactory().get_page_object('mask_designer_page', mwc)
title_room_page = PageFactory().get_page_object('title_room_page', mwc)
title_designer_page = PageFactory().get_page_object('title_designer_page', mwc)
pip_room_page = PageFactory().get_page_object('pip_room_page', mwc)
media_room_page = PageFactory().get_page_object('media_room_page', mwc)
tips_area_page = PageFactory().get_page_object('tips_area_page',mwc)
voice_over_recording_page = PageFactory().get_page_object('voice_over_recording_page',mwc)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mwc)
preferences_page = PageFactory().get_page_object('preferences_page', mwc)
trim_page = PageFactory().get_page_object('trim_page', mwc)
particle_room_page = PageFactory().get_page_object('particle_room_page', mwc)
particle_designer_page = PageFactory().get_page_object('particle_designer_page', mwc)
produce_page = PageFactory().get_page_object('produce_page', mwc)
download_from_cl_dz_page = PageFactory().get_page_object('download_from_cl_dz_page', mwc)
crop_zoom_pan_page = PageFactory().get_page_object('crop_zoom_pan_page',mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Mask Designer.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
#Ground_Truth_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/SFT/GroundTruth/Mask_Designer/'
#Auto_Ground_Truth_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/SFT/ATGroundTruth/Mask_Designer/'
#Test_Material_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/Material/'

material_folder = main_page.get_project_path('Material')
Test_Material_Folder = material_folder+'/'
DELAY_TIME = 1

@pytest.fixture(scope="module", autouse= True)
def init():
    yield
    #report.export()
    #report.show()

class Test_clear_sign_in():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        #main_page.start_app()
        time.sleep(DELAY_TIME * 4)
        yield mwc
        # tear down

    def test_1_1(self):
        time.sleep(2)
        # Clear Cache (Clear sign in log) to become Essential build
        main_page.clear_log_in()

        # launch PDR
        logger('Launch PDR')
        main_page.launch_app()
        time.sleep(5)

        # Click [Launch Free Version]
        free_version_link = main_page.exist({'AXTitle': 'Launch Free Version', 'AXRole': 'AXLink'})
        free_version_btn = main_page.exist({'AXTitle': 'Launch Free Version', 'AXRole': 'AXButton'})
        if free_version_link:
            main_page.mouse.click(*free_version_link.center)
        elif free_version_btn:
            main_page.mouse.click(*free_version_btn.center)
        else:
            logger('cannot find it')

        # Click User icon
        main_page.click(L.main.btn_user_sign_in_icon)

        # Input E-mail field
        e_mail_field = main_page.exist({'AXRoleDescription': 'text field', 'AXRole': 'AXTextField'})
        main_page.mouse.click(*e_mail_field.center)
        email_string = get_pdr_login_id()
        main_page.keyboard.send(email_string)

        # Input PW field
        password_field = main_page.exist({'AXRoleDescription': 'secure text field', 'AXRole': 'AXTextField'})
        main_page.mouse.click(*password_field.center)
        password_string = get_pdr_login_pw()
        main_page.keyboard.send(password_string)

        # Click [Sign in]
        btn_sign_in = main_page.exist({'AXTitle': 'Sign in', 'AXRole': 'AXLink'})
        main_page.mouse.click(*btn_sign_in.center)

        # Pop up Activate limitation
        main_page.exist_click(L.main.activate_dialog.btn_activate, None, btn="left", timeout=6, no_warning=True)

        # Click [Restart]
        btn_restart = main_page.exist({'AXTitle': 'Restart', 'AXIdentifier': 'IDC_CLALERT_BUTTON_0', 'AXRole': 'AXButton'}, timeout=15)
        main_page.mouse.click(*btn_restart.center)

        # Pop up Activate limitation
        main_page.exist_click(L.main.activate_dialog.btn_activate, None, btn="left", timeout=6, no_warning=True)

        # Check restart ok
        for x in range(20):
            if main_page.is_exist(L.media_room.btn_import_media, None, 2):
                logger('Launch PDR ready')
                break
            else:
                time.sleep(DELAY_TIME)
        logger('Clear sign in info then sign in specific ID [done]')
        main_page.close_app()