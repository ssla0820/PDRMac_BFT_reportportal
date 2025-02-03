import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time, inspect, datetime, pytest, re, configparser
os.chdir(os.path.dirname(__file__))
from types import SimpleNamespace

from ATFramework import MyReport, logger
from ATFramework.drivers.driver_factory import DriverFactory
from pages.page_factory import PageFactory
from configs.app_config import *
# import pages.media_room_page
from pages.locator import locator as L
# Modify locator to hardcode_0408
#from pages.locator.hardcode_0408 import locator as L


#for update_report_info
from globals import *



# read PDR cap >>
app = SimpleNamespace(**PDR_cap)
# read PDR cap <<

# create driver & page >>
mac = DriverFactory().get_mac_driver_object('mac', app.app_name, app.app_bundleID, app.app_path)
main_page = PageFactory().get_page_object('main_page', mac)
base_page = PageFactory().get_page_object('base_page', mac)
preferences_page = PageFactory().get_page_object('preferences_page', mac)
media_room_page = PageFactory().get_page_object('media_room_page',mac)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mac)
playback_window_page = PageFactory().get_page_object('playback_window_page', mac)

# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="Preferences.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<



# For Ground Truth / Test Material folder
#======= (Mac Mini)
Ground_Truth_Folder = app.ground_truth_root + '/Preferences/' #'/Users/cl/Desktop/AT/PDR_SFT_fromSVN/SFT/GroundTruth/Preferences/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Preferences/' #'/Users/cl/Desktop/AT/PDR_SFT_fromSVN/SFT/ATGroundTruth/Preferences/'
Test_Material_Folder = app.testing_material #'/Users/cl/Desktop/AT/PDR_SFT_fromSVN/Material/'

#======= (iMac27")
#Ground_Truth_Folder = '/Users/qadf-imac27/Desktop/AT/SFT/GroundTruth/Preferences/'
#Auto_Ground_Truth_Folder = '/Users/qadf-imac27/Desktop/AT/SFT/ATGroundTruth/Preferences/'
#Test_Material_Folder = '/Users/qadf-imac27/Desktop/AT/Material/'

#======= (Ernesto)
#Ground_Truth_Folder = '/Users/clt/Desktop/Ernesto/SFT/GroundTruth/Media_Room/'
#Auto_Ground_Truth_Folder = '/Users/clt/Desktop/Ernesto/SFT/ATGroundTruth/Media_Room/'
#Test_Material_Folder = '/Users/clt/Desktop/Ernesto/Material/'


DELAY_TIME = 1



'''
@pytest.fixture(scope="module", autouse= True)
def init():
    yield
    report.export()
    report.show()
'''




class Test_Preferences():

    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        yield mac
        main_page.close_app()

    @classmethod
    def setup_class(cls):
        main_page.clear_cache()
        print('setup class - enter')
        # for update the correct module start time of report (2021/04/20)
        now = datetime.datetime.now()
        report.add_ovinfo('time', now.time().strftime("%H:%M:%S"))
        report.start_time = time.time()
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_init('Preferences')


    @classmethod
    def teardown_class(cls):

        #print('teardown_class - export report')
        #report.export()
        #print(
            #f"mask designer result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        #update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           #report.get_ovinfo('skip'),
                           #report.get_ovinfo('duration'))
        #report.show()
        logger('teardown_class - export report')
        report.export()
        logger(
            f"Preferences result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           report.get_ovinfo('skip'),
                           report.get_ovinfo('duration'))
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number,
                                                     report.get_ovinfo('na'),
                                                     report.get_ovinfo('skip'),
                                                     report.get_ovinfo('duration'))
        report.show()


    #@pytest.mark.skip
    @exception_screenshot
    def test1_1_a(self):
        with uuid("9fbc4bb9-8600-4cf5-8cdd-d4cb37bb8478") as case:
            media_room_page.media_filter_display_audio_only()
            time.sleep(2)
            result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame)
            logger(result)



    #@pytest.mark.skip
    @exception_screenshot
    def test1_1_1_1(self):
        #'''
        #5/6
        with uuid("a60b1575-3e62-43e2-ad8b-ae1d1b4e62f5") as case:
            # case1.1.1 : Open preferences dialog via menu / button
            # click "Preferences" button
            time.sleep(5)
            set_check = main_page.click_set_user_preferences()
            logger(set_check)

            # close Preferences page via Cancel button
            set_check1 = preferences_page.click_cancel()
            logger(set_check1)

            # Enter "Preferences" via file menu
            set_check2 = main_page.top_menu_bar_powerdirector_preferences()
            logger(set_check2)

            # close Preferences page via Cancel button
            set_check3 = preferences_page.click_cancel()
            logger(set_check3)

            # check case result
            case.result = set_check and set_check1 and set_check2 and set_check3


        #5/6
        with uuid("4b70b5db-1d5d-4b9e-85c4-aa132ef37194") as case:
            # case1.1.2 : Open preferences dialog via hotkey
            # click "command + ,"
            preferences_page.tap_Preferences_hotkey()
            time.sleep(3)
            #logger(set_check)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            #take snapshot
            preferences_open = preferences_page.snapshot(locator=L.preferences.main_window,
                                                        file_name=Auto_Ground_Truth_Folder + 'G1.1.2_preferences.png')
            logger(f"{preferences_open =}")
            compare_result = preferences_page.compare(
                Ground_Truth_Folder + 'G1.1.2_preferences.png', preferences_open)
            logger(compare_result)

            # close Preferences page via Cancel button
            set_check1 = preferences_page.click_cancel()
            logger(set_check1)

            # check case result
            case.result = set_check and set_check1 and compare_result


        #5/6
        with uuid("9d625363-fe8b-4344-8626-3bca27b5819c") as case:
            # case1.2.1 : click [x] button to close preferences dialog directly and change won't be applied
            # click "Preferences" button
            set_check = main_page.click_set_user_preferences()
            logger(set_check)

            # Adjust some options in preferences (undo_level, frame_rate, show_waveform, render_preview, UI language...etc)
            preferences_page.general.maximum_undo_levels_set_value('21')
            preferences_page.general.timeline_frame_rate_set_24_fps()
            preferences_page.general.show_sound_waveform_set_check(0)
            preferences_page.general.render_preview_in_uhd_preview_quality_set_check(1)
            # switch language setting to "user defined" and then switch to "DEU"
            preferences_page.general.language_use_uer_defined_set_apply()
            preferences_page.general.language_use_uer_defined_apply_deu()

            # take snapshot for the change
            preferences_setting = preferences_page.snapshot(locator=L.preferences.main_window,
                                                        file_name=Auto_Ground_Truth_Folder + 'G1.2.1_preferences_setting.png')
            logger(f"{preferences_setting =}")
            compare_result = preferences_page.compare(
                Ground_Truth_Folder + 'G1.2.1_preferences_setting.png', preferences_setting)
            logger(compare_result)

            # click [x] button to discard all changes
            set_check1 = preferences_page.click_close()
            logger(set_check1)

            # click "Preferences" button again
            set_check2 = main_page.click_set_user_preferences()
            logger(set_check2)
            time.sleep(3)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # take snapshot to check if all changes have been reset
            preferences_setting1 = preferences_page.snapshot(locator=L.preferences.main_window,
                                                        file_name=Auto_Ground_Truth_Folder + 'G1.2.1_preferences_setting_reset.png')
            logger(f"{preferences_setting1 =}")
            compare_result1 = preferences_page.compare(Ground_Truth_Folder + 'G1.2.1_preferences_setting_reset.png', preferences_setting1)
            logger(compare_result1)

            # check test result
            case.result = set_check and set_check1 and set_check2 and compare_result and compare_result1


        #5/6
        with uuid("ce4c06cf-7160-4662-8a49-e5cb339cc46d") as case:
            # case1.2.4 : click ESC to close preferences dialog directly and change won't be applied
            # click "Preferences" button
            set_check = main_page.click_set_user_preferences()
            logger(set_check)

            # Adjust some options in preferences (audio_channel, drop_frame_timecode, enable_audio_Scrubbing, ...etc)
            # General tab
            preferences_page.general.audio_channels_set_51_surround()
            preferences_page.general.use_drop_frame_timecode_set_option('no')
            preferences_page.general.play_audio_while_scrubbing_set_check(0)

            # take snapshot for General tab
            preferences_general = preferences_page.snapshot(locator=L.preferences.main_window,
                                                        file_name=Auto_Ground_Truth_Folder + 'G1.2.4_preferences_general.png')
            logger(f"{preferences_general =}")
            compare_result = preferences_page.compare(
                Ground_Truth_Folder + 'G1.2.4_preferences_general.png', preferences_general)
            logger(compare_result)

            # Editing tab
            preferences_page.switch_to_editing()
            time.sleep(2)
            # check if switch to editing tab correctly
            if not preferences_page.exist(L.preferences.editing.timeline.chx_reverse_timeline_track_order):
                logger('cannot switch to editing tab successfully')
            # Adjust setting under Editing tab
            preferences_page.editing.set_default_transition_behavior_apply_cross()

            preferences_page.editing.return_to_beginnings_of_video_after_preview_set_check(0)
            preferences_page.editing.reverse_timeline_track_order_set_check(1)

            # take snapshot for the change
            preferences_editing = preferences_page.snapshot(locator=L.preferences.main_window,
                                                        file_name=Auto_Ground_Truth_Folder + 'G1.2.4_preferences_editing.png')
            logger(f"{preferences_editing =}")
            compare_result1 = preferences_page.compare(
                Ground_Truth_Folder + 'G1.2.4_preferences_editing.png', preferences_editing)
            logger(compare_result1)

            # press ESE button to discard all changes
            preferences_page.press_esc_key()
            #logger(set_check1)

            # click "Preferences" button again
            set_check2 = main_page.click_set_user_preferences()
            logger(set_check2)
            time.sleep(3)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # take snapshot to check if all changes have been reset
            preferences_general1 = preferences_page.snapshot(locator=L.preferences.main_window,
                                                        file_name=Auto_Ground_Truth_Folder + 'G1.2.4_preferences_general_reset.png')
            logger(f"{preferences_general1 =}")
            compare_result2 = preferences_page.compare(Ground_Truth_Folder + 'G1.2.4_preferences_general_reset.png', preferences_general1)
            logger(compare_result2)

            # switch to Editing tab to snapshot
            preferences_page.switch_to_editing()
            time.sleep(2)

            preferences_editing1 = preferences_page.snapshot(locator=L.preferences.main_window,
                                                        file_name=Auto_Ground_Truth_Folder + 'G1.2.4_preferences_editing_reset.png')
            logger(f"{preferences_editing1 =}")
            compare_result3 = preferences_page.compare(Ground_Truth_Folder + 'G1.2.4_preferences_editing_reset.png', preferences_editing1)
            logger(compare_result3)

            # check test result
            case.result = set_check and set_check2 and compare_result and compare_result1 and compare_result2 and compare_result3



        #5/6
        with uuid("6c23b859-225b-46b8-aa6a-079c42c9af1e") as case:
            # case1.2.3 : click [Cancel] button to close preferences dialog directly and change won't be applied
            # click "Preferences" button
            set_check = main_page.click_set_user_preferences()
            logger(set_check)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # Adjust some options in preferences
            # Switch to File tab
            preferences_page.switch_to_file()
            time.sleep(2)

            preferences_page.file.filename_snapshot_set_file_format('png')
            preferences_page.file.filename_snapshot_set_file_destination('clipboard')

            # take snapshot for new settings
            preferences_file = preferences_page.snapshot(locator=L.preferences.main_window,
                                                        file_name=Auto_Ground_Truth_Folder + 'G1.2.3_preferences_file.png')
            logger(f"{preferences_file =}")
            compare_result = preferences_page.compare(Ground_Truth_Folder + 'G1.2.3_preferences_file.png', preferences_file)
            logger(compare_result)

            # click [Cancel] button to discard all changes
            set_check1 = preferences_page.click_cancel()
            logger(set_check1)

            # click "Preferences" button again
            set_check2 = main_page.click_set_user_preferences()
            logger(set_check2)
            time.sleep(3)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # Switch to File tab
            preferences_page.switch_to_file()
            time.sleep(2)

            # take snapshot to check if all changes have been reset
            preferences_file1 = preferences_page.snapshot(locator=L.preferences.main_window,
                                                        file_name=Auto_Ground_Truth_Folder + 'G1.2.3_preferences_file_reset.png')
            logger(f"{preferences_file1 =}")
            compare_result1 = preferences_page.compare(Ground_Truth_Folder + 'G1.2.3_preferences_file_reset.png', preferences_file1)
            logger(compare_result1)

            # click [Cancel] button to close preferences
            set_check1 = preferences_page.click_cancel()
            logger(set_check1)

            # check test result
            case.result = set_check and set_check1 and set_check2 and compare_result and compare_result1


        #5/6
        with uuid("efff194d-e9ce-4b1a-9342-dda3ac796c64") as case:
            # case 2.1.2 : set Maximum undo levels to '0' and user cannot undo any operation
            # click "Preferences" button
            set_check = main_page.click_set_user_preferences()
            logger(set_check)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # Adjust some options in preferences (undo_level, frame_rate, show_waveform, render_preview, UI language...etc)
            preferences_page.general.maximum_undo_levels_set_value('0')

            # click [OK] button to apply change
            preferences_page.click_ok()

            # add a sample clip to timeline
            main_page.insert_media('Food.jpg')

            # snapshot for undo/redo
            undo_btn = preferences_page.snapshot(locator=L.main.btn_undo,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.1.2_undo_btn.png')
            logger(f"{undo_btn =}")

            #redo_btn = preferences_page.snapshot(locator=L.main.btn_redo, file_name=Auto_Ground_Truth_Folder + 'G2.1.2_redo_btn.png')
            #logger(f"{redo_btn =}")

            compare_result1 = preferences_page.compare(Ground_Truth_Folder + 'G2.1.2_undo_btn.png', undo_btn)
            logger(compare_result1)

            #compare_result2 = preferences_page.compare(Ground_Truth_Folder + 'G2.1.2_redo_btn.png', redo_btn)
            #logger(compare_result2)

            # try to undo (by button & hotkey)
            main_page.click_undo()
            preferences_page.tap_Undo_hotkey()

            # snapshot timeline workspace (expect result: timeline clip should not be removed)
            timeline_status = preferences_page.snapshot(locator = L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + 'G2.1.2_timeline_workspace.png')
            logger(timeline_status)

            compare_result3 = preferences_page.compare(Ground_Truth_Folder + 'G2.1.2_timeline_workspace.png', timeline_status)
            logger(compare_result3)

            # check result
            case.result = set_check and timeline_status and compare_result3 and compare_result1


        #5/6
        with uuid("40413b21-06e5-4ebe-8329-06a6b1633946") as case:
            # case 2.1.4 : Add Maximum undo levels by "^" / "v" buttons
            # click "Preferences" button
            set_check = main_page.click_set_user_preferences()
            logger(set_check)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")


            # Set undo_level to "2" by using "^" button
            preferences_page.general.maximum_undo_levels_set_arrow_button('up', 2) # adjust from '0' to '2'

            # click [OK] button to apply change
            preferences_page.click_ok()

            # remove timeline clip
            main_page.select_timeline_media('Food.jpg',0)
            media_room_page.tap_Remove_hotkey()

            #add two sample clips to timeline
            time.sleep(DELAY_TIME*2)
            main_page.insert_media('Landscape 02.jpg')
            time.sleep(DELAY_TIME*2)
            main_page.insert_media('Mahoroba.mp3')

            # snapshot for undo/redo
            undo_btn = preferences_page.snapshot(locator=L.main.btn_undo,
                                                 file_name=Auto_Ground_Truth_Folder + 'G2.1.4_undo_btn.png')
            logger(f"{undo_btn =}")

            redo_btn = preferences_page.snapshot(locator=L.main.btn_redo, file_name=Auto_Ground_Truth_Folder + 'G2.1.4_redo_btn.png')
            logger(f"{redo_btn =}")

            compare_result1 = preferences_page.compare(Ground_Truth_Folder + 'G2.1.4_undo_btn.png', undo_btn)
            logger(compare_result1)

            compare_result2 = preferences_page.compare(Ground_Truth_Folder + 'G2.1.4_redo_btn.png', redo_btn)
            logger(compare_result2)

            # try to undo twice (by button & hotkey)
            main_page.click_undo()
            preferences_page.tap_Undo_hotkey()

            # snapshot for undo/redo again
            undo_btn1 = preferences_page.snapshot(locator=L.main.btn_undo,
                                                 file_name=Auto_Ground_Truth_Folder + 'G2.1.4_undo_btn_1.png')
            logger(f"{undo_btn1 =}")

            redo_btn1 = preferences_page.snapshot(locator=L.main.btn_redo, file_name=Auto_Ground_Truth_Folder + 'G2.1.4_redo_btn_1.png')
            logger(f"{redo_btn1 =}")

            compare_result3 = preferences_page.compare(Ground_Truth_Folder + 'G2.1.4_undo_btn_1.png', undo_btn)
            logger(compare_result3)

            compare_result4 = preferences_page.compare(Ground_Truth_Folder + 'G2.1.4_redo_btn_1.png', redo_btn)
            logger(compare_result4)

            # snapshot timeline workspace (expect result: there is no clips on timeline)
            timeline_status = preferences_page.snapshot(locator = L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + 'G2.1.4_timeline_workspace.png')
            logger(timeline_status)

            compare_result5 = preferences_page.compare(Ground_Truth_Folder + 'G2.1.4_timeline_workspace.png', timeline_status)
            logger(compare_result5)

            # try to undo again (hotkey) (expect result: nothing change)
            preferences_page.tap_Undo_hotkey()

            # snapshot timeline workspace (expect result: nothing change -- 'Food.jpg' should not be added back to timeline)
            timeline_status1 = preferences_page.snapshot(locator = L.timeline_operation.workspace, file_name=Auto_Ground_Truth_Folder + 'G2.1.4_timeline_workspace_undo_again.png')
            logger(timeline_status1)

            compare_result6 = preferences_page.compare(Ground_Truth_Folder + 'G2.1.4_timeline_workspace_undo_again.png',
                                                       timeline_status)
            logger(compare_result6)

            # click "Preferences" button
            set_check = main_page.click_set_user_preferences()
            logger(set_check)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # Set undo_level to "1" by using "v" button
            preferences_page.general.maximum_undo_levels_set_arrow_button('down', 1)  # adjust from '2' to '2'

            # take snapshot for the change
            preferences_setting = preferences_page.snapshot(locator=L.preferences.main_window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G2.1.4_preferences_setting.png')
            logger(f"{preferences_setting =}")
            compare_result = preferences_page.compare(
                Ground_Truth_Folder + 'G2.1.4_preferences_setting.png', preferences_setting)
            logger(compare_result)

            # click [OK] button to apply change
            preferences_page.click_ok()

            # check result
            case.result = set_check and compare_result1 and compare_result2 and compare_result3 and compare_result4 and compare_result5 and compare_result6 and compare_result
            

        #5/12
        with uuid("5dcd8c40-a0ac-4727-a1de-fa89ac810755") as case:
            # case 2.1.5 : set Maximum undo levels to '5' by input value
            # click "Preferences" button
            set_check = main_page.click_set_user_preferences()
            logger(set_check)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")


            # set undo levels to '5' by input value
            preferences_page.general.maximum_undo_levels_set_value('5') # adjust from '1' to '5'

            # click [OK] button to apply change
            preferences_page.click_ok()

            # Open preferences again
            main_page.click_set_user_preferences()
            time.sleep(DELAY_TIME)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # take snapshot
            preferences_open = preferences_page.snapshot(locator=L.preferences.general.input_text_maximum_undo_levels,
                                                             file_name=Auto_Ground_Truth_Folder + 'G2.1.5_preferences_set_undo_levels_to_5.png')
            logger(f"{preferences_open =}")
            compare_result = preferences_page.compare(Ground_Truth_Folder + 'G2.1.5_preferences_set_undo_levels_to_5.png', preferences_open)
            logger(compare_result)

            # click [OK] button to apply change
            preferences_page.click_ok()

            # check result
            case.result = set_check and compare_result

        #5/12
        with uuid("67a7d116-2298-42b8-88a6-56d0f47c8f06") as case:
            # case2.1.7 : Set audio channel to 5.1 ch
            # enable preview volume meter
            main_page.top_menu_bar_view_show_timeline_preview_volume_meter()

            # add video / audio clip to timeline
            main_page.insert_media('Mahoroba.mp3')

            # take snapshot
            playback_window = preferences_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G2.1.7_playback_window.png')
            logger(f"{playback_window =}")
            compare_result = preferences_page.compare(
                Ground_Truth_Folder + 'G2.1.7_playback_window.png', playback_window)
            logger(compare_result)

            # click "Preferences" button
            #time.sleep(5)
            set_check = main_page.click_set_user_preferences()
            logger(set_check)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # set audio channel to 5.1 ch
            preferences_page.general.audio_channels_set_51_surround()

            # click [OK] button to apply change
            preferences_page.click_ok()

            # take snapshot
            playback_window1 = preferences_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G2.1.7_playback_window_51ch.png')
            logger(f"{playback_window1 =}")
            compare_result1 = preferences_page.compare(
                Ground_Truth_Folder + 'G2.1.7_playback_window_51ch.png', playback_window1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result1

        #5/12
        with uuid("067fc6f8-4878-49e6-9ce5-8ab0f9f5af9d") as case:
            # case2.1.6 : Set audio channel to 2 ch
            # enable preview volume meter
            #main_page.top_menu_bar_view_show_timeline_preview_volume_meter()

            # add video / audio clip to timeline
            #main_page.insert_media('Mahoroba.mp3')

            # take snapshot
            #playback_window = preferences_page.snapshot(locator=L.playback_window.main,
                                                         #file_name=Auto_Ground_Truth_Folder + 'G2.1.7_playback_window.png')
            #logger(f"{playback_window =}")
            #compare_result = preferences_page.compare(Ground_Truth_Folder + 'G2.1.7_playback_window.png', playback_window)
            #logger(compare_result)

            # click "Preferences" button
            #time.sleep(5)
            set_check = main_page.click_set_user_preferences()
            logger(set_check)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # set audio channel to 5.1 ch
            preferences_page.general.audio_channels_set_stereo()

            # click [OK] button to apply change
            preferences_page.click_ok()

            # take snapshot
            playback_window1 = preferences_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G2.1.7_playback_window_2ch.png')
            logger(f"{playback_window1 =}")
            compare_result1 = preferences_page.compare(
                Ground_Truth_Folder + 'G2.1.7_playback_window_2ch.png', playback_window1)
            logger(compare_result1)

            # check result
            case.result = compare_result1

        #5/12
        with uuid("79d2e08d-3d90-452d-9a23-74d3dc8eb452") as case:
            # case2.1.8 : Set timeline frame rate to 24fps and update timeline scale correctly
            # remove clip from timeline
            main_page.select_timeline_media('Mahoroba.mp3', 0)
            media_room_page.tap_Remove_hotkey()

            # add sample video to timeline
            time.sleep(DELAY_TIME)
            main_page.insert_media('Skateboard 01.mp4')

            # zoom in timeline scale (click 3 times)
            timeline_operation_page.timeline_click_zoomin_btn()
            timeline_operation_page.timeline_click_zoomin_btn()
            timeline_operation_page.timeline_click_zoomin_btn()

            # snapshot timeline workspace (expect result: timeline clip should not be removed)
            timeline_status = preferences_page.snapshot(locator=L.timeline_operation.workspace,
                                                         file_name=Auto_Ground_Truth_Folder + 'G2.1.8_timeline_workspace_original.png')
            logger(timeline_status)

            compare_result = preferences_page.compare(Ground_Truth_Folder + 'G2.1.8_timeline_workspace_original.png',
                                                       timeline_status)
            logger(compare_result)

            # click "Preferences" button
            #time.sleep(5)
            set_check = main_page.click_set_user_preferences()
            logger(set_check)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # set timeline frame rate to 24 fps
            preferences_page.general.timeline_frame_rate_set_value('24')

            # click [OK] button to apply change
            preferences_page.click_ok()

            # snapshot timeline workspace (expect result: timeline clip should not be removed)
            timeline_status1 = preferences_page.snapshot(locator=L.timeline_operation.workspace,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.1.8_timeline_workspace_24fps.png')
            logger(timeline_status1)

            compare_result1 = preferences_page.compare(Ground_Truth_Folder + 'G2.1.8_timeline_workspace_24fps.png',
                                                       timeline_status1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result1

        #5/12
        with uuid("b0810a59-db56-4d69-8c95-bab62868bc13") as case:
            # case2.1.9 : Set timeline frame rate to 25fps and update timeline scale correctly
            # remove clip from timeline
            #main_page.select_timeline_media('Mahoroba.mp3', 0)
            #media_room_page.tap_Remove_hotkey()

            # add sample video to timeline
            #time.sleep(DELAY_TIME)
            #main_page.insert_media('Skateboard 01.mp4')

            # zoom in timeline scale (click 3 times)
            #timeline_operation_page.timeline_click_zoomin_btn()
            #timeline_operation_page.timeline_click_zoomin_btn()
            #timeline_operation_page.timeline_click_zoomin_btn()

            # snapshot timeline workspace (expect result: timeline clip should not be removed)
            timeline_status = preferences_page.snapshot(locator=L.timeline_operation.workspace,
                                                         file_name=Auto_Ground_Truth_Folder + 'G2.1.9_timeline_workspace_original.png')
            logger(timeline_status)

            compare_result = preferences_page.compare(Ground_Truth_Folder + 'G2.1.9_timeline_workspace_original.png',
                                                       timeline_status)
            logger(compare_result)

            # click "Preferences" button
            #time.sleep(5)
            set_check = main_page.click_set_user_preferences()
            logger(set_check)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # set timeline frame rate to 25 fps
            preferences_page.general.timeline_frame_rate_set_value('25')

            # click [OK] button to apply change
            preferences_page.click_ok()

            # snapshot timeline workspace (expect result: timeline clip should not be removed)
            timeline_status1 = preferences_page.snapshot(locator=L.timeline_operation.workspace,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.1.9_timeline_workspace_25fps.png')
            logger(timeline_status1)

            compare_result1 = preferences_page.compare(Ground_Truth_Folder + 'G2.1.9_timeline_workspace_25fps.png',
                                                       timeline_status1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result1


        #5/12
        with uuid("da4809c4-81da-49c5-af4c-f2389483a593") as case:
            # case2.1.10 : Set timeline frame rate to 30fps and update timeline scale correctly
            # remove clip from timeline
            #main_page.select_timeline_media('Mahoroba.mp3', 0)
            #media_room_page.tap_Remove_hotkey()

            # add sample video to timeline
            #time.sleep(DELAY_TIME)
            #main_page.insert_media('Skateboard 01.mp4')

            # zoom in timeline scale (click 3 times)
            #timeline_operation_page.timeline_click_zoomin_btn()
            #timeline_operation_page.timeline_click_zoomin_btn()
            #timeline_operation_page.timeline_click_zoomin_btn()

            # snapshot timeline workspace (expect result: timeline clip should not be removed)
            timeline_status = preferences_page.snapshot(locator=L.timeline_operation.workspace,
                                                         file_name=Auto_Ground_Truth_Folder + 'G2.1.10_timeline_workspace_original.png')
            logger(timeline_status)

            compare_result = preferences_page.compare(Ground_Truth_Folder + 'G2.1.10_timeline_workspace_original.png',
                                                       timeline_status)
            logger(compare_result)

            # click "Preferences" button
            #time.sleep(5)
            set_check = main_page.click_set_user_preferences()
            logger(set_check)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # set timeline frame rate to 30 fps
            preferences_page.general.timeline_frame_rate_set_value('30')

            # click [OK] button to apply change
            preferences_page.click_ok()

            # snapshot timeline workspace (expect result: timeline clip should not be removed)
            timeline_status1 = preferences_page.snapshot(locator=L.timeline_operation.workspace,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.1.10_timeline_workspace_30fps.png')
            logger(timeline_status1)

            compare_result1 = preferences_page.compare(Ground_Truth_Folder + 'G2.1.10_timeline_workspace_30fps.png',
                                                       timeline_status1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result1

        #5/12
        with uuid("cd721653-8a56-4b15-a76a-10f85fb43184") as case:
            # case2.1.11 : Set timeline frame rate to 50fps and update timeline scale correctly
            # remove clip from timeline
            #main_page.select_timeline_media('Mahoroba.mp3', 0)
            #media_room_page.tap_Remove_hotkey()

            # add sample video to timeline
            #time.sleep(DELAY_TIME)
            #main_page.insert_media('Skateboard 01.mp4')

            # zoom in timeline scale (click 3 times)
            #timeline_operation_page.timeline_click_zoomin_btn()
            #timeline_operation_page.timeline_click_zoomin_btn()
            #timeline_operation_page.timeline_click_zoomin_btn()

            # snapshot timeline workspace (expect result: timeline clip should not be removed)
            timeline_status = preferences_page.snapshot(locator=L.timeline_operation.workspace,
                                                         file_name=Auto_Ground_Truth_Folder + 'G2.1.11_timeline_workspace_original.png')
            logger(timeline_status)

            compare_result = preferences_page.compare(Ground_Truth_Folder + 'G2.1.11_timeline_workspace_original.png',
                                                       timeline_status)
            logger(compare_result)

            # click "Preferences" button
            #time.sleep(5)
            set_check = main_page.click_set_user_preferences()
            logger(set_check)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # set timeline frame rate to 50 fps
            preferences_page.general.timeline_frame_rate_set_value('50')

            # click [OK] button to apply change
            preferences_page.click_ok()

            # snapshot timeline workspace (expect result: timeline clip should not be removed)
            timeline_status1 = preferences_page.snapshot(locator=L.timeline_operation.workspace,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.1.11_timeline_workspace_50fps.png')
            logger(timeline_status1)

            compare_result1 = preferences_page.compare(Ground_Truth_Folder + 'G2.1.11_timeline_workspace_50fps.png',
                                                       timeline_status1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result1

        #5/12
        with uuid("e08c79aa-c200-4351-b404-903f10c94327") as case:
            # case2.1.12 : Set timeline frame rate to 60fps and update timeline scale correctly
            # remove clip from timeline
            #main_page.select_timeline_media('Mahoroba.mp3', 0)
            #media_room_page.tap_Remove_hotkey()

            # add sample video to timeline
            #time.sleep(DELAY_TIME)
            #main_page.insert_media('Skateboard 01.mp4')

            # zoom in timeline scale (click 3 times)
            #timeline_operation_page.timeline_click_zoomin_btn()
            #timeline_operation_page.timeline_click_zoomin_btn()
            #timeline_operation_page.timeline_click_zoomin_btn()

            # snapshot timeline workspace (expect result: timeline clip should not be removed)
            timeline_status = preferences_page.snapshot(locator=L.timeline_operation.workspace,
                                                         file_name=Auto_Ground_Truth_Folder + 'G2.1.12_timeline_workspace_original.png')
            logger(timeline_status)

            compare_result = preferences_page.compare(Ground_Truth_Folder + 'G2.1.12_timeline_workspace_original.png',
                                                       timeline_status)
            logger(compare_result)

            # click "Preferences" button
            #time.sleep(5)
            set_check = main_page.click_set_user_preferences()
            logger(set_check)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # set timeline frame rate to 60 fps
            preferences_page.general.timeline_frame_rate_set_value('60')

            # click [OK] button to apply change
            preferences_page.click_ok()

            # snapshot timeline workspace (expect result: timeline clip should not be removed)
            timeline_status1 = preferences_page.snapshot(locator=L.timeline_operation.workspace,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.1.12_timeline_workspace_60fps.png')
            logger(timeline_status1)

            compare_result1 = preferences_page.compare(Ground_Truth_Folder + 'G2.1.12_timeline_workspace_60fps.png',
                                                       timeline_status1)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result1

        #'''
        #pass


        #5/12
        with uuid("e78b08ed-e274-434e-95f8-cafa0ce152b1") as case:
            # case2.1.13 : Use drop frame timecode
            # remove clip from timeline
            timeline_operation_page.select_timeline_media(1, 0)
            #main_page.select_timeline_media('Skateboard 01.mp4', 0)
            media_room_page.tap_Remove_hotkey()
            time.sleep(DELAY_TIME*2)

            # import a video clip "AVC_The Simpsons.mp4"
            media_room_page.collection_view_right_click_import_media_files(Test_Material_Folder + 'AVC_The Simpsons.mp4')

            # add video to timeline
            time.sleep(DELAY_TIME)
            main_page.insert_media('AVC_The Simpsons.mp4')

            # zoom out timeline scale (click 3 times)
            timeline_operation_page.click_zoomout_btn()
            time.sleep(DELAY_TIME*2)
            timeline_operation_page.click_zoomout_btn()
            time.sleep(DELAY_TIME)
            #timeline_operation_page.click_zoomout_btn()


            # click "Preferences" button
            #time.sleep(5)
            set_check = main_page.click_set_user_preferences()
            logger(set_check)
            time.sleep(DELAY_TIME * 2)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")
            #time.sleep(DELAY_TIME*2)

            # take snapshot for drop frame timecode default setting
            preferences_setting = preferences_page.snapshot(locator=L.preferences.general.use_drop_frame_timecode.btn_combobox,
                                                            file_name=Auto_Ground_Truth_Folder + 'G2.1.13_dropframetimecode_yes.png')
            logger(f"{preferences_setting =}")
            compare_result = preferences_page.compare(
                Ground_Truth_Folder + 'G2.1.13_dropframetimecode_yes.png', preferences_setting)
            logger(compare_result)

            # set timeline frame rate to 30 fps
            preferences_page.general.timeline_frame_rate_set_value('30')

            # set drop frame timecode to "yes"
            #preferences_page.general.use_drop_frame_timecode_set_option('yes')

            # click [OK] button to apply change
            preferences_page.click_ok()

            # verify drop frame timecode behavior
            playback_window_page.set_timecode_slidebar('00_00_59_29')

            # snapshot for current playback window
            preview_result = preferences_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G2.1.13_playback_window1.png')
            logger(preview_result)

            compare_result1 = preferences_page.compare(Ground_Truth_Folder + 'G2.1.13_playback_window1.png',
                                                      preview_result)
            logger(compare_result1)

            # go to next frame
            set_check = playback_window_page.Edit_Timeline_PreviewOperation('Next_Frame')
            logger(set_check)
            time.sleep(DELAY_TIME)

            # snapshot for current playback window
            preview_result1 = preferences_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G2.1.13_PlaybackWindow_nextframe.png')
            logger(preview_result1)

            compare_result2 = preferences_page.compare(Ground_Truth_Folder + 'G2.1.13_PlaybackWindow_nextframe.png',
                                                      preview_result1)
            logger(compare_result2)

            #check result
            case.result = compare_result and compare_result1 and compare_result2


        #5/12
        with uuid("589cd9a8-5a88-462f-9540-639a2a647548") as case:
            # case2.1.14 : Not use drop frame timecode
            # remove clip from timeline
            #main_page.select_timeline_media('Skateboard 01.mp4', 0)
            #media_room_page.tap_Remove_hotkey()

            # import a video clip "AVC_The Simpsons.mp4"
            #media_room_page.collection_view_right_click_import_media_files(Test_Material_Folder + 'AVC_The Simpsons.mp4')

            # add video to timeline
            #time.sleep(DELAY_TIME)
            #main_page.insert_media('AVC_The Simpsons.mp4')

            # zoom out timeline scale (click 1 time)
            #timeline_operation_page.click_zoomout_btn()
            #timeline_operation_page.click_zoomout_btn()
            time.sleep(DELAY_TIME)

            # click "Preferences" button
            #time.sleep(5)
            set_check = main_page.click_set_user_preferences()
            logger(set_check)
            time.sleep(DELAY_TIME * 2)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # set drop frame timecode to "yes"
            preferences_page.general.use_drop_frame_timecode_set_option('no')

            # take snapshot for drop frame timecode default setting
            preferences_setting = preferences_page.snapshot(locator=L.preferences.general.use_drop_frame_timecode.btn_combobox,
                                                            file_name=Auto_Ground_Truth_Folder + 'G2.1.14_dropframetimecode_no.png')
            logger(f"{preferences_setting =}")
            compare_result = preferences_page.compare(
                Ground_Truth_Folder + 'G2.1.14_dropframetimecode_no.png', preferences_setting)
            logger(compare_result)

            # set timeline frame rate to 60 fps
            #preferences_page.general.timeline_frame_rate_set_value('60')

            # click [OK] button to apply change
            preferences_page.click_ok()

            # verify drop frame timecode behavior
            playback_window_page.set_timecode_slidebar('00_00_59_29')

            # snapshot for current playback window
            preview_result = preferences_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G2.1.14_playback_window.png')
            logger(preview_result)

            compare_result1 = preferences_page.compare(Ground_Truth_Folder + 'G2.1.14_playback_window.png',
                                                      preview_result)
            logger(compare_result1)

            # go to next frame
            set_check = playback_window_page.Edit_Timeline_PreviewOperation('Next_Frame')
            logger(set_check)
            time.sleep(DELAY_TIME)

            # snapshot for current playback window
            preview_result1 = preferences_page.snapshot(locator=L.playback_window.main,
                                                         file_name=Auto_Ground_Truth_Folder + 'G2.1.14_PlaybackWindow_nextframe.png')
            logger(preview_result1)

            compare_result2 = preferences_page.compare(Ground_Truth_Folder + 'G2.1.14_PlaybackWindow_nextframe.png',
                                                      preview_result1)
            logger(compare_result2)

            #check result
            case.result = compare_result and compare_result1 and compare_result2


        #5/13
        with uuid("09179ec2-cc6f-4000-9247-9a75c1643dd8") as case:
            # case2.1.15 : for video clip, check "show sound waveform..." is ticked as default in preferences
            # click "Preferences" button
            #time.sleep(5)
            set_check = main_page.click_set_user_preferences()
            logger(set_check)
            time.sleep(DELAY_TIME * 2)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # check "show sound waveform" is ticked as default
            set_check1 = preferences_page.snapshot(locator= L.preferences.general.chx_show_sound_waveform,
                                                   file_name=Auto_Ground_Truth_Folder + 'G2.1.15_show_waveform_default.png')
            logger(set_check1)

            compare_result = preferences_page.compare(Ground_Truth_Folder + 'G2.1.15_show_waveform_default.png',set_check1)
            logger(compare_result)

            # click [OK] button to apply change
            preferences_page.click_ok()

            # snapshot timeline workspace (expect result: waveform is displayed correctly)
            timeline_status = preferences_page.snapshot(locator=L.timeline_operation.workspace,
                                                         file_name=Auto_Ground_Truth_Folder + 'G2.1.15_waveform.png')
            logger(timeline_status)

            compare_result1 = preferences_page.compare(Ground_Truth_Folder + 'G2.1.15_waveform.png',
                                                       timeline_status)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result1 and set_check

        # 5/14
        with uuid("32cb9b64-ba60-47db-8bf0-b5e9d36055ef") as case:
            # case2.1.16 : for video clip, uncheck "show sound waveform..." in preferences
            # click "Preferences" button
            # time.sleep(5)
            set_check = main_page.click_set_user_preferences()
            logger(set_check)
            time.sleep(DELAY_TIME * 2)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # untick "show sound waveform"
            preferences_page.general.show_sound_waveform_set_check(0)

            # check "show sound waveform" is ticked as default
            set_check1 = preferences_page.snapshot(locator=L.preferences.general.chx_show_sound_waveform,
                                                    file_name=Auto_Ground_Truth_Folder + 'G2.1.16_no_show_waveform.png')
            logger(set_check1)

            compare_result = preferences_page.compare(Ground_Truth_Folder + 'G2.1.16_no_show_waveform.png',
                                                        set_check1)
            logger(compare_result)

            # click [OK] button to apply change
            preferences_page.click_ok()

            # snapshot timeline workspace (expect result: waveform is displayed correctly)
            timeline_status = preferences_page.snapshot(locator=L.timeline_operation.workspace,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.1.16_no_waveform.png')
            logger(timeline_status)

            compare_result1 = preferences_page.compare(Ground_Truth_Folder + 'G2.1.16_no_waveform.png',
                                                           timeline_status)
            logger(compare_result1)

            # tick "show sound waveform"
            main_page.click_set_user_preferences()

            time.sleep(DELAY_TIME * 2)

            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            preferences_page.general.show_sound_waveform_set_check(1)

            # click [OK] button to apply change
            preferences_page.click_ok()

            # check result
            case.result = compare_result and compare_result1 and set_check

        # 5/14
        with uuid("296c2453-07fa-41ec-8631-c68c476fd227") as case:
            # case2.1.23 : Show continuous thumbnails for timeline video clips.
            # click "Preferences" button
            # time.sleep(5)
            set_check = main_page.click_set_user_preferences()
            logger(set_check)
            time.sleep(DELAY_TIME * 2)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # check "enable continue thumbnail...." is ticked as default
            set_check1 = preferences_page.snapshot(locator=L.preferences.general.chx_enable_continuous_thumbnail_on_video,
                                                    file_name=Auto_Ground_Truth_Folder + 'G2.1.23_EnableContinueThumbnail_default.png')
            logger(set_check1)

            compare_result = preferences_page.compare(Ground_Truth_Folder + 'G2.1.23_EnableContinueThumbnail_default.png',
                                                        set_check1)
            logger(compare_result)

            # click [OK] button to apply change
            preferences_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            # snapshot timeline workspace (expect result: waveform is displayed correctly)
            timeline_status = preferences_page.snapshot(locator=L.timeline_operation.workspace,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.1.23_video_continue_thumb.png')
            logger(timeline_status)

            compare_result1 = preferences_page.compare(Ground_Truth_Folder + 'G2.1.23_video_continue_thumb.png',
                                                           timeline_status)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result1 and set_check

        # 5/14
        with uuid("32cb9b64-ba60-47db-8bf0-b5e9d36055ef") as case:
            # case2.1.24 : disable continuous thumbnails for timeline video clips

            # Set timecode to beginning
            playback_window_page.set_timecode_slidebar('00_00_00_00')

            # click "Preferences" button
            # time.sleep(5)
            set_check = main_page.click_set_user_preferences()
            logger(set_check)
            time.sleep(DELAY_TIME * 2)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # untick "show sound waveform"
            preferences_page.general.enable_continuous_thumbnail_on_video_set_check(0)

            # check "show sound waveform" is ticked as default
            set_check1 = preferences_page.snapshot(locator=L.preferences.general.chx_show_sound_waveform,
                                                    file_name=Auto_Ground_Truth_Folder + 'G2.1.24_video_DisableContinueThumbnail.png')
            logger(set_check1)

            compare_result = preferences_page.compare(Ground_Truth_Folder + 'G2.1.24_video_DisableContinueThumbnail.png',
                                                        set_check1)
            logger(compare_result)

            # click [OK] button to apply change
            preferences_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            # snapshot timeline workspace (expect result: waveform is displayed correctly)
            timeline_status = preferences_page.snapshot(locator=L.timeline_operation.workspace,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.1.24_video_no_continue_thumb.png')
            logger(timeline_status)

            compare_result1 = preferences_page.compare(Ground_Truth_Folder + 'G2.1.24_video_no_continue_thumb.png',
                                                           timeline_status)
            logger(compare_result1)

            # tick "show sound waveform"
            main_page.click_set_user_preferences()

            time.sleep(DELAY_TIME * 2)

            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            preferences_page.general.enable_continuous_thumbnail_on_video_set_check(1)

            # click [OK] button to apply change
            preferences_page.click_ok()



            # check result
            case.result = compare_result and compare_result1 and set_check


        #5/14
        with uuid("95888202-06a8-492d-9b9c-7d54a4d19d9b") as case:
            # case2.1.17 : for audio clip, check "show sound waveform..." is ticked as default in preferences
            # remove timeline clip
            time.sleep(DELAY_TIME * 3)
            main_page.timeline_select_track(1)
            timeline_operation_page.select_timeline_media(1, 0)
            #main_page.select_timeline_media('AVC_The Simpsons.mp4', 0)
            media_room_page.tap_Remove_hotkey()
            time.sleep(DELAY_TIME*2)

            # insert two audio clips to timeline
            main_page.insert_media('Mahoroba.mp3')
            main_page.timeline_select_track(2)
            main_page.insert_media('Speaking Out.mp3')

            # click "Preferences" button
            #time.sleep(5)
            set_check = main_page.click_set_user_preferences()
            logger(set_check)
            time.sleep(DELAY_TIME * 2)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # check "show sound waveform" is ticked as default
            set_check1 = preferences_page.snapshot(locator= L.preferences.general.chx_show_sound_waveform,
                                                   file_name=Auto_Ground_Truth_Folder + 'G2.1.17_audio_show_waveform_default.png')
            logger(set_check1)

            compare_result = preferences_page.compare(Ground_Truth_Folder + 'G2.1.17_audio_show_waveform_default.png',set_check1)
            logger(compare_result)

            # click [OK] button to apply change
            preferences_page.click_ok()

            # snapshot timeline workspace (expect result: waveform is displayed correctly)
            timeline_status = preferences_page.snapshot(locator=L.timeline_operation.workspace,
                                                         file_name=Auto_Ground_Truth_Folder + 'G2.1.17_audio_waveform.png')
            logger(timeline_status)

            compare_result1 = preferences_page.compare(Ground_Truth_Folder + 'G2.1.17_audio_waveform.png',
                                                       timeline_status)
            logger(compare_result1)

            # check result
            case.result = compare_result and compare_result1 and set_check

        # 5/14
        with uuid("24bf923e-fd29-4bae-94d0-ac098a4328fc") as case:
            # case2.1.18 : for audio clip, uncheck "show sound waveform..." in preferences
            # click "Preferences" button
            # time.sleep(5)
            set_check = main_page.click_set_user_preferences()
            logger(set_check)
            time.sleep(DELAY_TIME * 2)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # untick "show sound waveform"
            preferences_page.general.show_sound_waveform_set_check(0)

            # check "show sound waveform" is ticked as default
            set_check1 = preferences_page.snapshot(locator=L.preferences.general.chx_show_sound_waveform,
                                                    file_name=Auto_Ground_Truth_Folder + 'G2.1.18_audio_no_show_waveform.png')
            logger(set_check1)

            compare_result = preferences_page.compare(Ground_Truth_Folder + 'G2.1.18_audio_no_show_waveform.png',
                                                        set_check1)
            logger(compare_result)

            # click [OK] button to apply change
            preferences_page.click_ok()

            # snapshot timeline workspace (expect result: waveform is displayed correctly)
            timeline_status = preferences_page.snapshot(locator=L.timeline_operation.workspace,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.1.18_audio_no_waveform.png')
            logger(timeline_status)

            compare_result1 = preferences_page.compare(Ground_Truth_Folder + 'G2.1.18_audio_no_waveform.png',
                                                           timeline_status)
            logger(compare_result1)

            # tick "show sound waveform"
            main_page.click_set_user_preferences()

            time.sleep(DELAY_TIME * 2)

            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            preferences_page.general.show_sound_waveform_set_check(1)

            # click [OK] button to apply change
            preferences_page.click_ok()

            # check result
            case.result = compare_result and compare_result1 and set_check

        #5/14
        with uuid("3d8fa5cf-3735-481d-8347-f600f3c70225") as case:
            # case1.2.2 : Click [OK] to apply change of preferences page
            # click "Preferences" button
            #time.sleep(5)
            set_check = main_page.click_set_user_preferences()
            logger(set_check)
            time.sleep(DELAY_TIME * 2)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # check "show sound waveform" is ticked as default
            set_check1 = preferences_page.snapshot(locator= L.preferences.general.chx_show_sound_waveform,
                                                   file_name=Auto_Ground_Truth_Folder + 'G1.2.2_check_show_waveform.png')
            logger(set_check1)

            compare_result = preferences_page.compare(Ground_Truth_Folder + 'G1.2.2_check_show_waveform.png',set_check1)
            logger(compare_result)

            # click [OK] button to apply change
            preferences_page.click_ok()

            # snapshot timeline workspace (expect result: waveform is displayed correctly)
            timeline_status = preferences_page.snapshot(locator=L.timeline_operation.workspace,
                                                         file_name=Auto_Ground_Truth_Folder + 'G1.2.2_audio_waveform.png')
            logger(timeline_status)

            compare_result1 = preferences_page.compare(Ground_Truth_Folder + 'G1.2.2_audio_waveform.png',
                                                       timeline_status)
            logger(compare_result1)

            main_page.save_project('test', Test_Material_Folder)

            # check result
            case.result = compare_result and compare_result1 and set_check



    #@pytest.mark.skip
    @exception_screenshot
    def test1_1_1_2(self): #this section is for enabling shadow file but these cases are blocked in v2529 (VDE212529-0050)

        # 5/19
        with uuid("1114c80c-d395-4c3a-ab1e-a2f0ba728544") as case:
            # case2.1.27 : [720x480] Shadow file is generated correctly
            # import a video clip "AVC_The Simpsons.mp4"
            time.sleep(DELAY_TIME * 5)
            media_room_page.import_media_file(Test_Material_Folder + 'AVC-Avatar.mkv')
            #media_room_page.collection_view_right_click_import_media_files(Test_Material_Folder + 'AVC-Avatar.mkv')

            # close high definition dialogue
            time.sleep(DELAY_TIME * 5)
            media_room_page.high_definition_video_confirm_dialog_click_no()

            # add video to timeline
            time.sleep(DELAY_TIME)
            main_page.insert_media('AVC-Avatar.mkv')

            # save project
            main_page.save_project('test', Test_Material_Folder)

            # click "Preferences" button
            set_check = main_page.click_set_user_preferences()
            logger(set_check)
            time.sleep(DELAY_TIME * 2)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # Tick "Enable Shadow file" and set resolution to 720*480
            preferences_page.general.enable_shadow_file_set_check(1)
            set_check1 = preferences_page.general.shadow_file_apply_resolution(1)
            logger(set_check1)

            # click [OK] button to apply change and waiting for shadow file creation
            preferences_page.click_ok()
            time.sleep(DELAY_TIME * 10)

            # snapshot media library (expect result: shadow file indicator is displayed as green after proxy file is generated complete)
            library_status = preferences_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.1.27_ShadowFile_480p.png')
            logger(ibrary_status)

            compare_result = preferences_page.compare(Ground_Truth_Folder + 'G2.1.27_ShadowFile_480p.png',
                                                       library_status)
            logger(compare_result)

            # check result
            case.result = compare_result and set_check and set_check1 #blocked by VDE212529-0050

        # 5/19
        with uuid("14442223-8d12-4ca0-a653-08abab31a4d9") as case:
            # case2.1.28 : [720x480] Shadow file is generated and show correct frame on timeline preview window
            # remove clip from timeline
            #main_page.select_timeline_media('AVC_The Simpsons.mp4', 0)
            #media_room_page.tap_Remove_hotkey()

            # import a video clip "AVC_The Simpsons.mp4"
            #media_room_page.collection_view_right_click_import_media_files(Test_Material_Folder + 'AVC-Avatar.mkv')

            # close high definition dialogue
            #media_room_page.high_definition_video_confirm_dialog_click_no()

            # add video to timeline
            #time.sleep(DELAY_TIME)
            #main_page.insert_media('AVC-Avatar.mkv')

            # click "Preferences" button
            #set_check = main_page.click_set_user_preferences()
            #logger(set_check)
            #time.sleep(DELAY_TIME * 2)

            # check if preference's locator is found
            #if not preferences_page.exist(L.preferences.main_window):
                #logger("cannot find preferences main window")

            # Tick "Enable Shadow file" and set resolution to 720*480
            #preferences_page.general.enable_shadow_file_set_check(1)
            #set_check1 = preferences_page.general.shadow_file_apply_resolution(1)
            #logger(set_check1)

            # click [OK] button to apply change and waiting for shadow file creation
            #preferences_page.click_ok()
            #time.sleep(DELAY_TIME * 10)

            # snapshot media library (expect result: shadow file indicator is displayed as green after proxy file is generated complete)
            preview_status = preferences_page.snapshot(locator=L.playback_window.main,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.1.28_preview_window.png')
            logger(preview_status)

            compare_result = preferences_page.compare(Ground_Truth_Folder + 'G2.1.28_preview_window.png',
                                                      preview_status)
            logger(compare_result)

            # check result
            case.result = compare_result

        # 5/21
        with uuid("0a13ec83-d0d3-4257-9832-df03c502ed21") as case:
            # case2.1.29 : [1280x720] Shadow file is generated correctly
            # click "Preferences" button
            set_check = main_page.click_set_user_preferences()
            logger(set_check)
            time.sleep(DELAY_TIME * 2)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # Tick "Enable Shadow file" and set resolution to 1280*720
            #preferences_page.general.enable_shadow_file_set_check(1)
            set_check1 = preferences_page.general.shadow_file_apply_resolution(2)
            logger(set_check1)

            # click [OK] button to apply change and waiting for shadow file creation
            preferences_page.click_ok()
            time.sleep(DELAY_TIME * 10)

            # snapshot media library (expect result: shadow file indicator is displayed as green after proxy file is generated complete)
            library_status = preferences_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.1.29_ShadowFile_720p.png')
            logger(ibrary_status)

            compare_result = preferences_page.compare(Ground_Truth_Folder + 'G2.1.29_ShadowFile_720p.png',
                                                       library_status)
            logger(compare_result)

            # check result
            case.result = compare_result and set_check and set_check1 #blocked by VDE212529-0050

        # 5/21
        with uuid("12f6a236-a9fd-415a-a0e2-597056026a88") as case:
            # case2.1.30 : [1280x720] Shadow file is generated and show correct frame on timeline preview window
            preview_status = preferences_page.snapshot(locator=L.playback_window.main,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.1.30_preview_window.png')
            logger(preview_status)

            compare_result = preferences_page.compare(Ground_Truth_Folder + 'G2.1.30_preview_window.png',
                                                      preview_status)
            logger(compare_result)

            # check result
            case.result = compare_result

        # 5/21
        with uuid("ae9dd518-9250-4bdf-9f20-b709d1024ef6") as case:
            # case2.1.31 : [1920x1080] Shadow file is generated correctly
            # click "Preferences" button
            set_check = main_page.click_set_user_preferences()
            logger(set_check)
            time.sleep(DELAY_TIME * 2)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # Tick "Enable Shadow file" and set resolution to 1280*720
            #preferences_page.general.enable_shadow_file_set_check(1)
            set_check1 = preferences_page.general.shadow_file_apply_resolution(3)
            logger(set_check1)

            # click [OK] button to apply change and waiting for shadow file creation
            preferences_page.click_ok()
            time.sleep(DELAY_TIME * 10)

            # snapshot media library (expect result: shadow file indicator is displayed as green after proxy file is generated complete)
            library_status = preferences_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.1.31_ShadowFile_1080p.png')
            logger(ibrary_status)

            compare_result = preferences_page.compare(Ground_Truth_Folder + 'G2.1.31_ShadowFile_1080p.png',
                                                       library_status)
            logger(compare_result)

            # check result
            case.result = compare_result and set_check and set_check1 #blocked by VDE212529-0050


        # 5/21
        with uuid("0638d60a-377b-403f-93f0-e55792d68c18") as case:
            # case2.1.32 : [1920x1080] Shadow file is generated and show correct frame on timeline preview window
            preview_status = preferences_page.snapshot(locator=L.playback_window.main,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.1.32_preview_window.png')
            logger(preview_status)

            compare_result = preferences_page.compare(Ground_Truth_Folder + 'G2.1.32_preview_window.png',
                                                      preview_status)
            logger(compare_result)

            # check result
            case.result = compare_result


    #@pytest.mark.skip
    @exception_screenshot
    def test1_1_1_3(self):
        # 5/21
        with uuid("c01ea534-57c1-4984-946c-311f9f878871") as case:
            # case2.1.57 : Adjust input days of Auto Delete temporary files by '^' & 'v' buttons
            # click "Preferences" button
            time.sleep(DELAY_TIME*5)
            set_check = main_page.click_set_user_preferences()
            logger(set_check)
            time.sleep(DELAY_TIME * 2)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # set input days to '32'
            set_check1 = preferences_page.general.auto_delete_temporary_files_days_click_arrow_button('up', 2)
            logger(set_check1)

            check_value = 0
            if preferences_page.exist(L.preferences.general.auto_delete_temporary_files.input_days):
                # check if input box locator is found and assign new value to the check_value
                check_value = preferences_page.exist(L.preferences.general.auto_delete_temporary_files.input_days).AXValue
                logger(check_value)

                if check_value == '32':
                    result1 = True
                else:
                    result1 = False

            # set input days to '31'
            set_check2 = preferences_page.general.auto_delete_temporary_files_days_click_arrow_button('down', 1)
            logger(set_check2)
            check_value1 = 0
            if preferences_page.exist(L.preferences.general.auto_delete_temporary_files.input_days):
                # check if input box locator is found and assign new value to the check_value
                check_value1 = preferences_page.exist(L.preferences.general.auto_delete_temporary_files.input_days).AXValue
                logger(check_value1)

                if check_value1 == '31':
                    result2 = True
                else:
                    result2 = False

            # close preferences page
            preferences_page.click_ok()

            # check result
            case.result = result1 and result2

        # 5/21
        with uuid("461ccd86-c8b2-4298-94b3-5f56759c9c31") as case:
            # case2.1.58 : Adjust input days of Auto Delete temporary files by input number
            # click "Preferences" button
            set_check = main_page.click_set_user_preferences()
            logger(set_check)
            time.sleep(DELAY_TIME * 2)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # set input days to '30'
            set_check = preferences_page.general.auto_delete_temporary_files_days_input_value('30')
            logger(set_check)

            check_value = 0
            if preferences_page.exist(L.preferences.general.auto_delete_temporary_files.input_days):
                # check if input box locator is found and assign new value to the check_value
                check_value = preferences_page.exist(
                    L.preferences.general.auto_delete_temporary_files.input_days).AXValue
                logger(check_value)

                # close preferences page
                preferences_page.click_ok()

                if check_value == '30':
                    case.result = True
                else:
                    case.result = False
        '''
        # 5/21
        with uuid("064bcc8d-2d66-4213-be3a-bbd28e3422f1") as case:
            # case2.1.xx : Language - switch to User defined
            # click "Preferences" button
            set_check = main_page.click_set_user_preferences()
            logger(set_check)
            time.sleep(DELAY_TIME * 2)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # switch language settings to "user defined"
            set_check1 = preferences_page.general.language_use_uer_defined_set_apply('chs')
            logger(set_check1)

            # close preferences page
            preferences_page.click_ok()

            # close and re-launch PDR
            main_page.close_and_restart_app()

            time.sleep(DELAY_TIME*5)

            UI_status = preferences_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.1.xx_change_MUI.png')
            logger(UI_status)

            compare_result = preferences_page.compare(Ground_Truth_Folder + 'G2.1.xx_change_MUI.png',
                                                      UI_status)
            logger(compare_result)

            # check result
            case.result = compare_result
        '''
        pass #skip switching MUI test case for now

        # 5/24
        with uuid("fb34b32a-5ba2-44d9-bba2-62f7c949c0eb") as case:
            # case2.1.xx : Language - switch to system default
            # click "Preferences" button
            set_check = main_page.click_set_user_preferences()
            logger(set_check)
            time.sleep(DELAY_TIME * 2)

            # check if preference's locator is found
            if not preferences_page.exist(L.preferences.main_window):
                logger("cannot find preferences main window")

            # switch language settings to "system default"
            set_check1 = preferences_page.general.language_use_system_default_set_apply()
            logger(set_check1)

            # close preferences page
            preferences_page.click_ok()

            # close and re-launch PDR
            main_page.close_and_restart_app()

            time.sleep(DELAY_TIME * 5)

            UI_status = preferences_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.xx_change_MUI_to_default.png')
            logger(UI_status)

            compare_result = preferences_page.compare(Ground_Truth_Folder + 'G2.1.xx_change_MUI_to_default.png',
                                                      UI_status)
            logger(compare_result)

            # check result
            case.result = compare_result







