#test
import sys, os
import tempfile
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time, inspect, datetime, pytest, re, configparser
os.chdir(os.path.dirname(__file__))
from types import SimpleNamespace

from ATFramework import MyReport, logger
from ATFramework.drivers.driver_factory import DriverFactory
from pages.page_factory import PageFactory
from configs.app_config import *
from pages.locator import locator as L


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
pip_designer_page = PageFactory().get_page_object('pip_designer_page', mwc)
media_room_page = PageFactory().get_page_object('media_room_page', mwc)
tips_area_page = PageFactory().get_page_object('tips_area_page',mwc)
voice_over_recording_page = PageFactory().get_page_object('voice_over_recording_page',mwc)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mwc)
preferences_page = PageFactory().get_page_object('preferences_page', mwc)
trim_page = PageFactory().get_page_object('trim_page', mwc)
particle_room_page = PageFactory().get_page_object('particle_room_page', mwc)
particle_designer_page = PageFactory().get_page_object('particle_designer_page', mwc)
produce_page = PageFactory().get_page_object('produce_page', mwc)
download_from_shutterstock_page = PageFactory().get_page_object('download_from_shutterstock_page', mwc)
effect_settings_page = PageFactory().get_page_object('effect_settings_page', mwc)
playback_window_page = PageFactory().get_page_object('playback_window_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Scan Effect Setting.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
#Ground_Truth_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/SFT/GroundTruth/Mask_Designer/'
Auto_Ground_Truth_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_M3_develop/SFT/ATGroundTruth/Particle_Designer/'
#Test_Material_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/Material/'

material_folder = main_page.get_project_path('Material')
Test_Material_Folder = material_folder+'/'

DELAY_TIME = 1

@pytest.fixture(scope="module", autouse= True)
def init():
    yield
    #report.export()
    #report.show()

class Test_Cutout_quality():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        # clear AI module
        main_page.clear_AI_module()

        main_page.start_app()
        time.sleep(DELAY_TIME * 4)
        yield mwc
        # tear down
        main_page.close_app()
        main_page.clear_cache()

    def apply_cutout_feature(self):

        # Media room > Enter (Downloads) category
        media_room_page.enter_downloaded()
        time.sleep(DELAY_TIME * 3)

        # Search library content
        media_room_page.search_library('472818079_fhd')
        time.sleep(DELAY_TIME * 2)

        # Insert 472818079_fhd.mov
        main_page.select_library_icon_view_media('472818079_fhd')
        time.sleep(DELAY_TIME * 2)
        media_room_page.library_clip_context_menu_insert_on_selected_track()

        # Set timecode
        main_page.set_timeline_timecode('00_00_01_00')
        time.sleep(DELAY_TIME * 2)

        # Click Split
        tips_area_page.click_TipsArea_btn_split()

        # View entire video
        timeline_operation_page.click_view_entire_video_btn()

        # Select clip # 1 of track 1 to remove
        timeline_operation_page.select_timeline_media(0,0)
        time.sleep(DELAY_TIME * 2)
        tips_area_page.more_features.remove(1)


        media_room_page.search_library_click_cancel()
        time.sleep(DELAY_TIME)

        # Search library content
        media_room_page.search_library('495531908_fhd')
        time.sleep(DELAY_TIME * 2)

        # Select timeline track 2
        main_page.timeline_select_track(2)
        time.sleep(DELAY_TIME * 2)

        # Set timecode
        main_page.set_timeline_timecode('00_00_07_00')
        time.sleep(DELAY_TIME * 2)

        # Insert 495531908_fhd.mov
        main_page.select_library_icon_view_media('495531908_fhd')
        time.sleep(DELAY_TIME * 2)
        media_room_page.library_clip_context_menu_insert_on_selected_track()

        # Click TipsArea > Pip Designer
        check_status = tips_area_page.tools.select_PiP_Designer()
        if not check_status:
            raise Exception

        # Apply cutout
        pip_designer_page.apply_chromakey()
        time.sleep(DELAY_TIME * 2)

        # Get cutout status
        cutout_button_object = main_page.exist(L.pip_designer.chromakey.cutout_button)
        logger(cutout_button_object.AXValue)
        if cutout_button_object.AXValue == 0:
            main_page.click(L.pip_designer.chromakey.cutout_button)
            time.sleep(DELAY_TIME * 2)

        # check current preview
        apply_cutout_result = main_page.snapshot(L.pip_designer.preview)
        logger(apply_cutout_result)

        # Move cutout object to left
        pip_designer_page.move_to_left_on_canvas(60)
        time.sleep(DELAY_TIME * 3)

        # Move cutout object to left
        pip_designer_page.move_to_left_on_canvas(60)
        time.sleep(DELAY_TIME * 2)

        # check current preview
        move_left_result = main_page.snapshot(L.pip_designer.preview)
        logger(move_left_result)


        # Click [OK]
        pip_designer_page.click_ok()
        time.sleep(DELAY_TIME * 2)

    @exception_screenshot
    def easy_cutout(self):
        # Bug regression (VDE235413-0028)
        # Insert Sport 01.jpg
        main_page.select_library_icon_view_media('Sport 02.jpg')
        time.sleep(DELAY_TIME * 2)
        media_room_page.library_clip_context_menu_insert_on_selected_track()

        # Click TipsArea > Pip Designer
        check_status = tips_area_page.tools.select_PiP_Designer()
        if not check_status:
            raise Exception

        # Switch to Advanced mode
        pip_designer_page.switch_mode('Advanced')
        time.sleep(DELAY_TIME * 2)

        # Switch (Motion) tab
        pip_designer_page.advanced.switch_to_motion()

        # Unfold path
        pip_designer_page.advanced.unfold_path_menu(set_unfold=1)

        # Apply one path
        pip_designer_page.path.select_template(4)

        # Switch (Animation) tab
        pip_designer_page.advanced.switch_to_animation()

        # Unfold (In Animation) then apply one (In Animation)
        pip_designer_page.advanced.unfold_in_animation_menu(set_unfold=1)

        # Apply one path
        pip_designer_page.in_animation.select_template(7)

        # Switch (Animation) tab
        pip_designer_page.advanced.switch_to_properties()

        # Apply cutout
        pip_designer_page.apply_chromakey()
        time.sleep(DELAY_TIME * 2)

        # Get cutout status then Enable Auto cutout
        cutout_button_object = main_page.exist(L.pip_designer.chromakey.cutout_button)
        logger(cutout_button_object.AXValue)
        if cutout_button_object.AXValue == 0:
            main_page.click(L.pip_designer.chromakey.cutout_button)
            time.sleep(DELAY_TIME * 25)

        # Click [OK]
        pip_designer_page.click_ok()
        time.sleep(DELAY_TIME * 2)

        # Select clip # 1 of track 1 to Enter Pip Designer again
        timeline_operation_page.select_timeline_media(0,0)
        time.sleep(DELAY_TIME * 2)

        # Click TipsArea > Pip Designer
        check_status = tips_area_page.tools.select_PiP_Designer()
        if not check_status:
            raise Exception

        # Click [OK]
        pip_designer_page.click_ok()
        time.sleep(DELAY_TIME * 2)

    @exception_screenshot
    def test_1_1_1(self):
        for x in range(50):
            logger('----')
            logger(x)
            self.easy_cutout()

            # new workspace
            main_page.tap_NewWorkspace_hotkey()
            main_page.handle_no_save_project_dialog('no')

            logger('----')