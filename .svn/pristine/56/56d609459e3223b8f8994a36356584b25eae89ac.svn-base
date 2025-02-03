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

class Test_GettyImage_music_download():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.clear_cache()
        main_page.start_app()
        time.sleep(DELAY_TIME * 4)
        yield mwc
        # tear down
        main_page.close_app()

    # For Background Music (Soundstripe)
    # Test script only run in Stage server (Due to premium content limitation)
    @exception_screenshot
    def test_1_1_1(self):
        # report path
        scan_meta_report_path = main_page.get_project_path('SFT/Report')+'/Download_soundstripe_report.txt'
        logger(scan_meta_report_path)
        f = open(scan_meta_report_path, 'w')
        f.write('---- Test start ----\n')

        # Enter Audio Mixing room to snapshot default preview
        main_page.enter_room(6)
        time.sleep(DELAY_TIME * 3)

        # Default volume meter preview
        audio_1_library_track = main_page.exist({'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': 0})
        audio_default_preview = main_page.snapshot(locator=audio_1_library_track)
        logger(audio_default_preview)

        # Enter BGM (Soundstripe)
        main_page.enter_room(0)
        time.sleep(DELAY_TIME * 3)
        media_room_page.enter_background_soundstripe()
        time.sleep(DELAY_TIME*5)

        # Get current Meta music items, Auto testing Scan music count = 30
        meta_list = media_room_page.background_music_show_meta_list(30)
        # Download 1st ~ 24th
        for x in range(24):
            # Step1: Get music name from meta_list
            current_music = meta_list[x]
            logger('------ Current status ------')
            logger(current_music)

            # Step2: Search music
            # if find cancel button, click x button on search bar
            if main_page.exist(L.media_room.btn_search_cancel):
                main_page.click(L.media_room.btn_search_cancel)
                time.sleep(9)

            # Search music
            media_room_page.search_library(current_music)
            time.sleep(5)

            # Step3: Download music
            media_room_page.background_music_meta_context_menu_download(current_music, timeout=70)

            # Step4: Insert music to timeline
            tips_area_page.click_TipsArea_btn_insert()

            # Step5: Check volume meter when play meta music
            # Switch to Audio mixing room
            main_page.enter_room(6)
            time.sleep(DELAY_TIME * 3)

            # Click [Play] to preview
            playback_window_page.Edit_Timeline_PreviewOperation('Play')
            time.sleep(DELAY_TIME * 6)
            playback_window_page.Edit_Timeline_PreviewOperation('Pause')
            time.sleep(DELAY_TIME * 2)

            # 5s volume meter preview
            audio_1_library_track = main_page.exist({'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': 0})
            audio_5s_preview = main_page.snapshot(locator=audio_1_library_track)
            logger(audio_5s_preview)

            volume_check_1 = not main_page.compare(audio_default_preview, audio_5s_preview, similarity=0.98)
            volume_update = main_page.compare(audio_default_preview, audio_5s_preview, similarity=0.7)
            check_result = volume_check_1 and volume_update
            if check_result == False:
                logger(f" {current_music}: False")
                f.write(f'{x}. - '+current_music+'[NG]\n')
            else:
                logger("PASS")
                f.write(f'{x}. - '+current_music+'[OK]\n')

            # Step6: Remove timeline audio clip
            timeline_operation_page.select_timeline_media(track_index=1, clip_index=0)
            time.sleep(DELAY_TIME * 2)
            main_page.right_click()
            time.sleep(DELAY_TIME * 2)
            main_page.select_right_click_menu('Remove')
            time.sleep(DELAY_TIME*2)

            # Step7: Back to Media Room (BGM)
            main_page.enter_room(0)
            time.sleep(DELAY_TIME * 10)

        # Download 25st ~ 30th
        for x in range(24, 30):
            # Step1: Get music name from meta_list
            current_music = meta_list[x]
            logger('------ Current status ------')
            logger(current_music)

            # Step2: Search music
            # if find cancel button, click x button on search bar
            if main_page.exist(L.media_room.btn_search_cancel):
                main_page.click(L.media_room.btn_search_cancel)
                time.sleep(9)

            # Search music
            media_room_page.search_library(current_music)
            time.sleep(5)

            # Step3: Download music
            media_room_page.background_music_meta_context_menu_download(current_music, timeout=40)

            # Step3 - 2: pop up [Upgrade Now] dialog > Click [No, thanks.]
            if main_page.is_exist(L.media_room.btn_upgrade_now, timeout=10):
                main_page.click(L.media_room.btn_no_thanks)
                time.sleep(3)
            else:
                logger(f'Download {x}th, No pop up warning message : Upgrade  Now')
                raise Exception

            # Step4: Insert music to timeline
            tips_area_page.click_TipsArea_btn_insert()

            # Step5: Check volume meter when play meta music
            # Switch to Audio mixing room
            main_page.enter_room(6)
            time.sleep(DELAY_TIME * 3)

            # Click [Play] to preview
            playback_window_page.Edit_Timeline_PreviewOperation('Play')
            time.sleep(DELAY_TIME * 6)
            playback_window_page.Edit_Timeline_PreviewOperation('Pause')
            time.sleep(DELAY_TIME * 2)

            # 5s volume meter preview
            audio_1_library_track = main_page.exist({'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': 0})
            audio_5s_preview = main_page.snapshot(locator=audio_1_library_track)
            logger(audio_5s_preview)

            volume_check_1 = not main_page.compare(audio_default_preview, audio_5s_preview, similarity=0.98)
            volume_update = main_page.compare(audio_default_preview, audio_5s_preview, similarity=0.7)
            check_result = volume_check_1 and volume_update
            if check_result == False:
                logger(f" {current_music}: False")
                f.write(f'{x}. - '+current_music+'[NG]\n')
            else:
                logger("PASS")
                f.write(f'{x}. - '+current_music+'[OK]\n')

            # Step6: Remove timeline audio clip
            timeline_operation_page.select_timeline_media(track_index=1, clip_index=0)
            time.sleep(DELAY_TIME * 2)
            main_page.right_click()
            time.sleep(DELAY_TIME * 2)
            main_page.select_right_click_menu('Remove')
            time.sleep(DELAY_TIME*2)

            # Step7: Back to Media Room (BGM)
            main_page.enter_room(0)
            time.sleep(DELAY_TIME * 10)

        f.write('---- Test end ----\n')
        f.close()


