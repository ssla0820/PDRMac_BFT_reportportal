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
mac = DriverFactory().get_mac_driver_object('mac', app.app_name, app.app_bundleID, app.app_path)
main_page = PageFactory().get_page_object('main_page', mac)
media_room_page = PageFactory().get_page_object('media_room_page', mac)
produce_page = PageFactory().get_page_object('produce_page', mac)
preferences_page = PageFactory().get_page_object('preferences_page', mac)
timeline_page = PageFactory().get_page_object('timeline_operation_page', mac)
tips_area_page = PageFactory().get_page_object('tips_area_page', mac)
mask_designer_page = PageFactory().get_page_object('mask_designer_page', mac)
transition_room_page = PageFactory().get_page_object('transition_room_page', mac)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="Produce_Local_M3.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
#Ground_Truth_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/SFT/GroundTruth/Pre_Cut/'
#Auto_Ground_Truth_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/SFT/ATGroundTruth/Pre_Cut/'
#Test_Material_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/Material/'
Ground_Truth_Folder = app.ground_truth_root + '/Produce_Local/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Produce_Local/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Produce_Local_M3():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        time.sleep(DELAY_TIME*4)
        yield mac
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
            google_sheet_execution_log_init('Produce_Local_M3')

    @classmethod
    def teardown_class(cls):

        logger('teardown_class - export report')
        report.export()
        logger(
            f"Produce Local result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           report.get_ovinfo('skip'),
                           report.get_ovinfo('duration'))
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                               report.get_ovinfo('skip'), report.get_ovinfo('duration'))
        report.show()


    def check_preferences_explore_folder(self):
        # Enter preferences > Get produce file path
        main_page.click_set_user_preferences()
        time.sleep(DELAY_TIME)
        preferences_page.switch_to_file()
        time.sleep(DELAY_TIME)
        check_preferences_default = preferences_page.file.default_locations_export_folder_get_path()
        preferences_page.click_ok()
        time.sleep(DELAY_TIME)
        return check_preferences_default

    def check_current_produced_full_path(self):
        try:
            file_path = preferences_page.exist(L.produce.edittext_output_folder).AXValue
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return file_path

    def check_dont_show_again_dialog(self, tick=1):
        # if find don't show again checkbox > tick Do not show again
        if produce_page.exist(L.media_room.confirm_dialog.chx_do_not_show_again):
            el_chx_do_not_show = produce_page.exist(L.media_room.confirm_dialog.chx_do_not_show_again)
            chx_position = el_chx_do_not_show.AXPosition
            chx_size = el_chx_do_not_show.AXSize
            if tick:
                produce_page.mouse.click(int(chx_position[0] + chx_size[0] / 4), int(chx_position[1] + chx_size[1] / 2))

            produce_page.exist_click(L.media_room.confirm_dialog.btn_no)
            time.sleep(DELAY_TIME)

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_22(self):
        main_page.insert_media('Skateboard 01.mp4')
        time.sleep(DELAY_TIME)
        main_page.select_library_icon_view_media('Skateboard 02.mp4')
        time.sleep(DELAY_TIME)
        main_page.tips_area_insert_media_to_selected_track(option=1)

        with uuid("d869198a-a872-485f-b015-838d5135bfc0") as case:
            # [G21] Show SVRT result for current timeline content
            main_page.SVRTInfo_hotkey()
            time.sleep(DELAY_TIME*6)
            current_library = preferences_page.snapshot(locator=L.effect_room.library,
                                                      file_name=Auto_Ground_Truth_Folder + 'G21.png')
            compare_result = preferences_page.compare(Ground_Truth_Folder + 'G21.png', current_library)
            case.result = compare_result

        with uuid("911587be-065d-4564-86ef-36498e372021") as case:
            # [G23] Able to open help page
            check_result = media_room_page.svrt_info.click_help()
            # Verify Step: (Can back to PDR)
            time.sleep(DELAY_TIME*2)
            current_library = preferences_page.snapshot(locator=L.effect_room.library,
                                                      file_name=Auto_Ground_Truth_Folder + 'G23.png')
            compare_result = preferences_page.compare(Ground_Truth_Folder + 'G23.png', current_library)
            case.result = check_result and compare_result

        with uuid("3949d25f-e758-48e3-a552-ac848578e1c0") as case:
            # [G24] Able to open video tutorial
            check_result = media_room_page.svrt_info.open_tutorial_page()
            # Verify Step: (Can back to PDR)
            time.sleep(DELAY_TIME*2)
            current_library = preferences_page.snapshot(locator=L.effect_room.library,
                                                      file_name=Auto_Ground_Truth_Folder + 'G24.png')
            compare_result = preferences_page.compare(Ground_Truth_Folder + 'G24.png', current_library)
            case.result = check_result and compare_result


        with uuid("04e86b38-c4ed-4974-9f9f-6adab1214f88") as case:
            # [G22] Able to Refresh detection after change timeline content structure
            check_default = main_page.exist(L.media_room.svrt_window.btn_refresh).AXEnabled
            if not check_default:
                check_default_status = True
            else:
                check_default_status = False

            timeline_page.select_timeline_media(track_index=0,clip_index=1)
            main_page.right_click()
            main_page.select_right_click_menu('Remove')
            time.sleep(DELAY_TIME)
            media_room_page.svrt_info.click_refresh()
            case.result = check_default_status

        with uuid("b74e9932-0ed0-479f-9b8a-77b63b1f4495") as case:
            # [G25] Leave SVRT information page
            media_room_page.svrt_info.click_close()
            time.sleep(DELAY_TIME*1)
            if produce_page.is_not_exist(L.media_room.svrt_window.btn_refresh):
                check_change = True
            else:
                check_change = False
            case.result = check_change

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_23(self):

        main_page.insert_media('Skateboard 01.mp4')
        main_page.enter_room(1)
        main_page.select_LibraryRoom_category('General')
        time.sleep(1)

        # Add Title : Clover_03
        main_page.select_library_icon_view_media('Clover_03')
        main_page.tips_area_insert_media_to_selected_track(option=1)

        # Add transition (Burning)
        main_page.enter_room(2)
        transition_room_page.search_Transition_room_library('Burning')
        time.sleep(DELAY_TIME*0.5)
        main_page.drag_transition_to_timeline_clip('Burning', 'Skateboard 01.mp4')

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("7991b11d-66d9-48e1-bdc5-1e7ada5a9e03") as case:
            # [G47] 1.3 Profile Editing > Delete > Enable if current profile is custom

            # Check Del button status
            check_default = main_page.exist(L.produce.local.btn_delete_custom_profile).AXEnabled
            if not check_default:
                check_default_status = True
            else:
                check_default_status = False

            # Click Custom profile w/o do any setting
            produce_page.local.click_create_a_new_profile()
            produce_page.local.quality_profile_setup.click_ok()

            # Click DEL button
            check_result = produce_page.local.click_delete_custom_profile()
            case.result = check_default_status and check_result

            if main_page.exist(L.produce.local.quality_profile_setup_dialog.alert.warning_message, timeout=4):
                main_page.exist_click(L.produce.local.quality_profile_setup_dialog.alert.btn_OK)

        with uuid("d8924930-aeab-4e3f-aaba-1fb86ad86bd6") as case:
            # [G143] 16:9 / H.264 M2TS / NTSC / AVC 1440 x 1080/60p (28Mbps)
            produce_page.local.select_file_extension('m2ts')
            time.sleep(DELAY_TIME)

            produce_page.local.select_profile_name(7)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'AVC 1440 x 1080/60p (28 Mbps)':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            for x in range(30):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify : Can find the produced file in Media Room
            verify_step1 = main_page.select_library_icon_view_media(explore_file)

            # Verify 2 : Set timecode to (00:00:10:13)
            main_page.set_timeline_timecode('00_00_10_13', is_verify=False)
            time.sleep(DELAY_TIME*3)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G143.png')
            verify_step2 = produce_page.compare(Ground_Truth_Folder + 'G143.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step1 and verify_step2

            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        with uuid("1060ff3a-3982-4a7f-b62f-a24141abb835") as case:
            # [G147] 16:9 / H.264 M2TS / NTSC / AVC 1920 x 1080/60p (28Mbps)
            main_page.click_produce()
            produce_page.check_enter_produce_page()
            time.sleep(DELAY_TIME)

            produce_page.local.select_profile_name(9)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'AVC 1920 x 1080/60p (28 Mbps)':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            for x in range(30):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Media Room > Right Click Menu > Check View Properties
            #main_page.select_library_icon_view_media('Landscape 02.jpg')
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media(explore_file)
            main_page.right_click()
            main_page.select_right_click_menu('View Properties')
            time.sleep(DELAY_TIME*2)
            current_image = produce_page.snapshot(locator=L.media_room.properties_dialog.main_window,
                                                      file_name=Auto_Ground_Truth_Folder + 'G147_Properties.png')
            verify_step1 = produce_page.compare(Ground_Truth_Folder + 'G147_Properties.png', current_image)
            time.sleep(DELAY_TIME)
            # close View Properties
            main_page.exist_click(L.media_room.properties_dialog.btn_close)
            time.sleep(DELAY_TIME)


            # Verify 2 : Set timecode to (00:00:09:25)
            main_page.set_timeline_timecode('00_00_09_25', is_verify=False)
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G147_preview.png')
            verify_step2 = produce_page.compare(Ground_Truth_Folder + 'G147_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step1 and verify_step2
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        main_page.timeline_select_track(2)
        main_page.insert_media('Food.jpg')
        time.sleep(DELAY_TIME)
        main_page.select_timeline_media('Food.jpg')
        main_page.right_click()
        main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Multiply')

        with uuid("98355660-64c9-41c9-a94d-b067c4121df2") as case:
            # [G149] 16:9 / H.264 M2TS / NTSC / AVC 2K 2048 x 1080/30p (40Mbps)
            main_page.click_produce()
            produce_page.check_enter_produce_page()

            time.sleep(DELAY_TIME)

            produce_page.local.select_profile_name(11)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'AVC 2K 2048 x 1080/30p (40 Mb...':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            for x in range(30):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Media Room > Can find the produced video
            time.sleep(DELAY_TIME * 2)
            verify_step1 = main_page.select_library_icon_view_media(explore_file)
            main_page.press_space_key()
            time.sleep(DELAY_TIME*5)
            main_page.press_space_key()

            # Verify 2 : Set timecode to (00:00:09:27)
            main_page.set_timeline_timecode('00_00_09_27', is_verify=False)
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G149_preview.png')
            verify_step2 = produce_page.compare(Ground_Truth_Folder + 'G149_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step1 and verify_step2
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_24(self):
        time.sleep(DELAY_TIME*2)
        video_path = Test_Material_Folder + 'Produce_Local/4978895.mov'
        media_room_page.collection_view_right_click_import_media_files(video_path)
        time.sleep(DELAY_TIME*2)
        main_page.insert_media('4978895.mov')
        time.sleep(DELAY_TIME*0.5)
        main_page.timeline_select_track(1)

        # Add transition (Burning)
        main_page.enter_room(2)
        main_page.select_LibraryRoom_category('Special')
        main_page.drag_transition_to_timeline_clip('Film Clip', '4978895')

        # Add Title : Radar
        main_page.timeline_select_track(2)
        main_page.enter_room(1)
        main_page.select_LibraryRoom_category('General')

        main_page.select_library_icon_view_media('Radar')
        time.sleep(DELAY_TIME)
        main_page.tips_area_insert_media_to_selected_track()

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("a3f5468d-134c-41bc-95aa-d49976cb469d") as case:
            # [G72] 1.5 Preview Panel > Seek preview
            check_default = produce_page.verify_preview(Ground_Truth_Folder + 'G72_default.png')
            logger(check_default)
            produce_page.drag_slider_to_timecode(timecode='00_00_01_00')
            time.sleep(DELAY_TIME)
            check_now = produce_page.verify_preview(Ground_Truth_Folder + 'G72_now.png', similarity=0.93)
            case.result = check_default and check_now

        with uuid("a3972a85-0fa8-45db-9ef8-7ac5ec6bb939") as case:
            # [G153] 16:9 / H.264 M2TS / NTSC / AVC 4K 4096 x 2160/30p (50Mbps)
            produce_page.local.select_file_extension('m2ts')
            time.sleep(DELAY_TIME)

            produce_page.local.select_profile_name(14)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'AVC 4K 4096 x 2160/30p (50 Mb...':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()

            with uuid("446d1238-582c-48c8-96b3-d272eed74719") as case:
                # [G97] Cancel Rendering > No
                produce_page.click_cancel_rendering()
                check_result = produce_page.click_confirm_cancel_rendering_dialog_no()
                case.result = check_result

            for x in range(30):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Media Room > Can find the produced video
            time.sleep(DELAY_TIME * 2)
            verify_step1 = main_page.select_library_icon_view_media(explore_file)
            main_page.press_space_key()
            time.sleep(DELAY_TIME*5)
            main_page.press_space_key()

            # Verify 2 : Set timecode to (00:00:11:06)
            main_page.set_timeline_timecode('00_00_01_10', is_verify=False)
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G151_preview.png')
            verify_step2 = produce_page.compare(Ground_Truth_Folder + 'G151_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step1 and verify_step2
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_25(self):
        time.sleep(DELAY_TIME * 2)
        video_path = Test_Material_Folder + 'Produce_Local/4978895.mov'
        media_room_page.collection_view_right_click_import_media_files(video_path)
        time.sleep(DELAY_TIME*2)
        main_page.insert_media('4978895.mov')

        # Add particle (Burning)
        main_page.timeline_select_track(2)
        main_page.enter_room(5)
        main_page.select_LibraryRoom_category('General')
        time.sleep(1)
        main_page.select_library_icon_view_media('Maple')
        main_page.tips_area_insert_media_to_selected_track()

        # Add Title : Motion Graphics 002
        main_page.timeline_select_track(3)
        main_page.enter_room(1)
        main_page.select_LibraryRoom_category('Motion Graphics')
        time.sleep(1)
        main_page.select_library_icon_view_media('Motion Graphics 002')
        main_page.tips_area_insert_media_to_selected_track()

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("d922b843-f9ec-4c9b-a4c7-f47ef047128c") as case:
            # [G158] 16:9 / H.264 M2TS / PAL / AVC 1280 x 720/50p (24Mbps)

            produce_page.local.select_file_extension('m2ts')
            time.sleep(DELAY_TIME)
            produce_page.local.select_country_video_format('pal')
            time.sleep(DELAY_TIME)
            produce_page.local.select_profile_name(4)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'AVC 1280 x 720/50p (24 Mbps)':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            for x in range(30):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Media Room > Right Click Menu > Check View Properties
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media(explore_file)
            main_page.right_click()
            main_page.select_right_click_menu('View Properties')
            time.sleep(DELAY_TIME*2)
            current_image = produce_page.snapshot(locator=L.media_room.properties_dialog.main_window,
                                                      file_name=Auto_Ground_Truth_Folder + 'G158_Properties.png')
            verify_step1 = produce_page.compare(Ground_Truth_Folder + 'G158_Properties.png', current_image)
            time.sleep(DELAY_TIME)
            # close View Properties
            main_page.exist_click(L.media_room.properties_dialog.btn_close)
            time.sleep(DELAY_TIME)

            # Verify 2 : Set timecode to (00:00:03:00)
            main_page.set_timeline_timecode('00_00_03_00', is_verify=False)
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G158_preview.png')
            verify_step2 = produce_page.compare(Ground_Truth_Folder + 'G158_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step1 and verify_step2
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        with uuid("12e26c3a-e1c4-4f8a-bd5a-e70427170ac9") as case:
            main_page.click_produce()
            produce_page.check_enter_produce_page()

            # [G159] 16:9 / H.264 M2TS / PAL / AVC 1280 x 720/120p (40Mbps)
            produce_page.local.select_profile_name(5)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'AVC 1280 x 720/120p (40 Mbps)':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()
            explore_full_path = self.check_current_produced_full_path()
            logger(explore_full_path)
            # Start : produce
            produce_page.click_start()
            for x in range(30):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Video compare
            main_page.select_library_icon_view_media(explore_file)
            video_compare_result = main_page.compare_video(explore_full_path, Test_Material_Folder + 'Produce_Local/Produce_G159.m2ts')
            logger(video_compare_result)

            # Verify 2 : Set timecode to (00:00:02:15)
            main_page.set_timeline_timecode('00_00_02_15', is_verify=False)
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G159_preview.png')
            verify_step2 = produce_page.compare(Ground_Truth_Folder + 'G159_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = video_compare_result and verify_step2
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        with uuid("8bf8c02c-d94c-4b9d-baa0-9bcfec02af80") as case:
            main_page.click_produce()
            produce_page.check_enter_produce_page()

            # [G172] 16:9 / H.264 M2TS / PAL / AVC 4K 3840 x 2160/25p (50Mbps)
            produce_page.local.select_profile_name(13)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'AVC 4K 3840 x 2160/25p (50 Mb...':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()
            explore_full_path = self.check_current_produced_full_path()
            logger(explore_full_path)
            # Start : produce
            produce_page.click_start()
            for x in range(30):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Video compare
            main_page.select_library_icon_view_media(explore_file)
            video_compare_result = main_page.compare_video(explore_full_path, Test_Material_Folder + 'Produce_Local/Produce_G172.m2ts')
            case.result = video_compare_result

            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # 1208
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_26(self):
        time.sleep(DELAY_TIME * 2)
        video_path = Test_Material_Folder + 'Produce_Local/Y man.mp4'
        media_room_page.collection_view_right_click_import_media_files(video_path)
        time.sleep(DELAY_TIME*2)
        main_page.insert_media('Y man.mp4')
        time.sleep(DELAY_TIME)
        main_page.timeline_select_track(2)

        # Add Title : Motion Graphics 003
        main_page.enter_room(1)
        main_page.select_LibraryRoom_category('Motion Graphics')
        time.sleep(1)
        main_page.select_library_icon_view_media('Motion Graphics 003')
        main_page.tips_area_insert_media_to_selected_track()

        main_page.click_produce()
        with uuid("63dadb88-27ac-4c53-b410-c111513b66cd") as case:
            # [G367] 16:9 / H.265 MKV / NTSC / HEVC 1280 x 720/24p (7Mbps)
            # File extension > H265
            produce_page.local.select_file_format(container='hevc')

            produce_page.local.select_file_extension('mkv')
            time.sleep(DELAY_TIME)

            produce_page.local.select_profile_name(3)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'HEVC 1280 x 720/24p (7 Mbps)':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()
            explore_full_path = self.check_current_produced_full_path()
            logger(explore_full_path)
            # Start : produce
            produce_page.click_start()
            for x in range(30):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Video compare
            main_page.select_library_icon_view_media(explore_file)
            video_compare_result = main_page.compare_video(explore_full_path,
                                                           Test_Material_Folder + 'Produce_Local/Produce_G367.mkv')
            case.result = video_compare_result
            logger(video_compare_result)

            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        main_page.click_produce()
        with uuid("0c57d4fa-58c4-4280-be8b-31ad42c1155a") as case:
            # [G369] 16:9 / H.265 MKV / NTSC / HEVC 1920x1080/24p (11Mbps)

            produce_page.local.select_profile_name(5)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'HEVC 1920 x 1080/24p (11 Mbps)':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            produce_page.click_start()
            for x in range(50):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)
            main_page.select_library_icon_view_media(explore_file)

            # Verify : Set timecode to (00:00:02:15)
            main_page.set_timeline_timecode('00_00_03_24', is_verify=False)
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G369_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G369_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        main_page.click_produce()
        with uuid("d678e3d7-876c-4d9e-9dde-fe545e3e180f") as case:
            # [G361] 16:9 / H.265 MP4 / PAL / MPEG-4 4K 3840 x 2160/25p (37Mbps)
            produce_page.local.select_file_extension('mp4')
            time.sleep(DELAY_TIME)

            produce_page.local.select_country_video_format('pal')
            time.sleep(DELAY_TIME)
            produce_page.local.select_profile_name(8)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 3840 x 2160/25p (37 Mb...':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            for x in range(30):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Media Room > Right Click Menu > Check View Properties
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media(explore_file)
            main_page.right_click()
            main_page.select_right_click_menu('View Properties')
            time.sleep(DELAY_TIME*2)
            current_image = produce_page.snapshot(locator=L.media_room.properties_dialog.video_info,
                                                      file_name=Auto_Ground_Truth_Folder + 'G361_Properties_video.png')
            verify_step1 = produce_page.compare(Ground_Truth_Folder + 'G361_Properties_video.png', current_image)
            time.sleep(DELAY_TIME)
            # close View Properties
            main_page.exist_click(L.media_room.properties_dialog.btn_close)
            time.sleep(DELAY_TIME)


            # Verify 2 : Set timecode to (00:00:11:06)
            main_page.set_timeline_timecode('00_00_05_15', is_verify=False)
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G361_preview.png')
            verify_step2 = produce_page.compare(Ground_Truth_Folder + 'G361_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step1 and verify_step2
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_27(self):
        time.sleep(DELAY_TIME*2)
        video_path = Test_Material_Folder + 'Produce_Local/girl.mp4'
        media_room_page.collection_view_right_click_import_media_files(video_path)
        time.sleep(DELAY_TIME*2)
        main_page.set_project_aspect_ratio_4_3()
        main_page.select_library_icon_view_media('Skateboard 02.mp4')
        media_room_page.library_clip_context_menu_insert_on_selected_track()
        # handle aspect ratio conflict
        main_page.handle_aspect_ratio_conflict()

        time.sleep(DELAY_TIME)
        main_page.timeline_select_track(2)
        main_page.select_library_icon_view_media('girl.mp4')
        media_room_page.library_clip_context_menu_insert_on_selected_track()
        # handle aspect ratio conflict
        main_page.handle_aspect_ratio_conflict()

        time.sleep(DELAY_TIME)
        main_page.tap_TipsArea_Tools_menu(1)
        time.sleep(DELAY_TIME*2)
        mask_designer_page.MaskDesigner_Apply_template(9)
        time.sleep(DELAY_TIME)
        mask_designer_page.Edit_MaskDesigner_ClickOK()

        main_page.click_produce()
        with uuid("79d5fe95-b420-4747-9acb-eb1b30cd6aa3") as case:
            # [G384] 4:3 / H.265 M2TS / NTSC / HEVC 2K 2048 x 1536/30p (30Mbps)

            # File extension > H265
            produce_page.local.select_file_format(container='hevc')

            produce_page.local.select_file_extension('m2ts')
            time.sleep(DELAY_TIME)

            produce_page.local.select_profile_name(3)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'HEVC 2K 2048 x 1536/30p (30 M...':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            produce_page.click_start()
            for x in range(50):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)
            main_page.select_library_icon_view_media(explore_file)

            # Verify : Set timecode to (00:00:02:15)
            main_page.set_timeline_timecode('00_00_03_24', is_verify=False)
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G384_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G384_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        main_page.click_produce()
        with uuid("014d0de3-e670-4d86-91a6-5c0d788fb809") as case:
            # [G271] 4:3 / H.264 MKV / NTSC /  AVC 720 x 576/24p (8Mbps)
            # File extension > H264
            produce_page.local.select_file_format(container='avc')

            produce_page.local.select_file_extension('mkv')
            time.sleep(DELAY_TIME)

            produce_page.local.select_profile_name(2)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'AVC 720 x 576/24p (8 Mbps)':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()
            explore_full_path = self.check_current_produced_full_path()
            logger(explore_full_path)
            # Start : produce
            produce_page.click_start()
            for x in range(30):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Video compare
            main_page.select_library_icon_view_media(explore_file)
            video_compare_result = main_page.compare_video(explore_full_path,
                                                           Test_Material_Folder + 'Produce_Local/Produce_G271.mkv')
            case.result = video_compare_result
            logger(video_compare_result)

            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        main_page.click_produce()
        with uuid("d48388e0-1d92-47fb-a6c8-bda8eda7fef5") as case:
            # [G390] 4:3 / H.265 MP4 / NTSC / MPEG-4 640 x 480/24p (5Mbps)
            # File extension > H265
            produce_page.local.select_file_format(container='hevc')

            produce_page.local.select_file_extension('mp4')
            time.sleep(DELAY_TIME)

            produce_page.local.select_profile_name(1)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 640 x 480/24p (5 Mbps)':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            for x in range(30):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)
            main_page.select_library_icon_view_media(explore_file)

            # Verify : Set timecode to (00:00:06:11)
            main_page.set_timeline_timecode('00_00_06_11', is_verify=False)
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G390_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G390_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step

            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_28(self):
        time.sleep(DELAY_TIME * 2)
        video_path = Test_Material_Folder + 'Produce_Local/Produce_G367.mkv'
        media_room_page.collection_view_right_click_import_media_files(video_path)
        time.sleep(DELAY_TIME)
        main_page.insert_media('Produce_G367.mkv')
        time.sleep(DELAY_TIME)

        # Add transition (Burning)
        main_page.enter_room(2)
        main_page.select_LibraryRoom_category('Alpha')
        main_page.drag_transition_to_timeline_clip('Sift 3', 'Produce_G367')
        time.sleep(DELAY_TIME)
        tips_area_page.click_TipsArea_btn_Duration()
        tips_area_page.apply_duration_settings("00_00_05_00")

        with uuid("52209ffa-b693-409e-a957-f0302b5cf62b") as case:
            main_page.click_produce()
            produce_page.check_enter_produce_page()

            produce_page.local.select_file_extension('m2ts')
            time.sleep(DELAY_TIME)

            # [G133] H264 / 16:9 M2TS / Profile description
            item = produce_page.find(L.produce.local.text_area_profile_description)
            if not item:
                case.result = False

            current_description = item.AXValue
            logger(current_description)
            if current_description != 'This profile encodes MPEG-4 AVC (H.264) video format in a high definition profile' \
                                      ' that is compatible with AVCHD. MPEG-4 AVC uses a better compression rate compared' \
                                      ' to MPEG-2, using less space to produce a video of similar quality.':
                case.result = False
            else:
                case.result = True

        with uuid("5ce72725-77fd-4467-af80-090c139d7dd7") as case:
            # [G163] 16:9 / H.264 M2TS / PAL / AVC 1440 x 1080/50p (28Mbps)
            produce_page.local.select_country_video_format('pal')
            time.sleep(DELAY_TIME)
            produce_page.local.select_profile_name(7)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'AVC 1440 x 1080/50p (28 Mbps)':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            for x in range(30):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)
            main_page.select_library_icon_view_media(explore_file)

            # Verify : Set timecode to (00:00:03:16)
            main_page.set_timeline_timecode('00_00_03_16', is_verify=False)
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G163_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G163_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step

            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        with uuid("c925d0aa-906b-4d20-bace-ce88d62f811c") as case:
            main_page.click_produce()
            produce_page.check_enter_produce_page()

            # [G167] 16:9 / H.264 M2TS / PAL / AVC 1920 x 1080/50p (28Mbps)
            produce_page.local.select_profile_name(9)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            logger(check_profile)
            if check_profile != 'AVC 1920 x 1080/50p (28 Mbps)':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()
            explore_full_path = self.check_current_produced_full_path()
            logger(explore_full_path)
            # Start : produce
            produce_page.click_start()
            for x in range(30):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Video compare
            main_page.select_library_icon_view_media(explore_file)
            video_compare_result = main_page.compare_video(explore_full_path,
                                                           Test_Material_Folder + 'Produce_Local/Produce_G167.m2ts')
            case.result = video_compare_result
            logger(video_compare_result)

            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        with uuid("44493d22-d54a-4339-9766-f5da7ab12c85") as case:
            main_page.click_produce()
            produce_page.check_enter_produce_page()
            # [G174] H264 / 16:9 M2Ts / Custom profile
            produce_page.local.click_create_a_new_profile()
            check_result = produce_page.local.quality_profile_setup.apply_profile_name('Mac AT Custom G174',
                                                                                       'SFT Profile G174')

            item = produce_page.find(L.produce.local.quality_profile_setup_dialog.profile_name.edittext_description)
            if produce_page.exist(item):
                AT_custom_description = item.AXValue
            if AT_custom_description == 'SFT Profile G174':
                check_custom_description = True
            else:
                check_custom_description = False

            produce_page.local.quality_profile_setup.switch_to_video_tab()
            produce_page.local.quality_profile_setup.set_video_profile(index_resolution=5, index_frame_rate=3)
            produce_page.local.quality_profile_setup.set_video_bitrate(40000)

            # click OK > close (Quality Profile Setup)
            produce_page.local.quality_profile_setup.click_ok()

            produce_page.local.click_details()
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=L.produce.local.details_dialog.main_window,
                                                  file_name=Auto_Ground_Truth_Folder + 'G174_detail.png')
            check_detail = produce_page.compare(Ground_Truth_Folder + 'G174_detail.png', current_image)
            produce_page.press_esc_key()

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            for x in range(30):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)
            main_page.select_library_icon_view_media(explore_file)

            # Verify : Set timecode to (00:00:04:01)
            time.sleep(DELAY_TIME * 2)
            main_page.set_timeline_timecode('00_00_04_01', is_verify=False)
            time.sleep(DELAY_TIME*4)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G174_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G174_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step and check_detail and check_custom_description

            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_29(self):
        main_page.timeline_select_track(2)
        video_path = Test_Material_Folder + 'Produce_Local/girl.mp4'
        media_room_page.collection_view_right_click_import_media_files(video_path)
        time.sleep(DELAY_TIME)
        main_page.select_library_icon_view_media('girl.mp4')
        media_room_page.library_clip_context_menu_insert_on_selected_track()

        with uuid("7e1a71ef-7dc9-491c-80c3-6d2e01f7884e") as case:
            main_page.click_produce()
            produce_page.check_enter_produce_page()
            # [G175] H264 / 16:9 MP4 / Profile description
            item = produce_page.find(L.produce.local.text_area_profile_description)
            if not item:
                case.result = False

            current_description = item.AXValue
            logger(current_description)
            if current_description != 'This profile encodes MPEG-4 video files. It uses a high bitrate, large frame size, ' \
                                      'full frame rate and the most advanced encoding techniques available to ensure the best encoded output.':
                case.result = False
            else:
                case.result = True

        with uuid("bb3b042a-7168-49ad-b42b-d0c8de653045") as case:
            # [G179] 16:9 / H.264 MP4 / NTSC / MPEG-4 1280 x 720/30p (16Mbps)

            produce_page.local.select_profile_name(4)
            time.sleep(DELAY_TIME)

            produce_page.local.click_details()
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=L.produce.local.details_dialog.main_window,
                                                  file_name=Auto_Ground_Truth_Folder + 'G179_detail.png')
            check_detail = produce_page.compare(Ground_Truth_Folder + 'G179_detail.png', current_image)
            produce_page.press_esc_key()

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            for x in range(300):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)
            main_page.select_library_icon_view_media(explore_file)

            # Verify : Set timecode to (00:00:07:15)
            main_page.set_timeline_timecode('00_00_07_15', is_verify=False)
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G179_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G179_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step and check_detail

            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        with uuid("e346b72f-1227-4a4d-ab9c-e2da99dcc000") as case:
            # Add transition (Burning)
            main_page.timeline_select_track(3)
            main_page.enter_room(4)
            time.sleep(DELAY_TIME)
            main_page.select_LibraryRoom_category('Shape')
            time.sleep(DELAY_TIME)
            main_page.select_library_icon_view_media('Shape 015')
            tips_area_page.click_TipsArea_btn_insert()
            time.sleep(DELAY_TIME)
            # [G181] 16:9 / H.264 MP4 / NTSC / MPEG-4 1280 x 720/120p (40Mbps)

            main_page.click_produce()
            produce_page.check_enter_produce_page()

            produce_page.local.select_profile_name(6)
            time.sleep(DELAY_TIME)

            produce_page.local.click_details()
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=L.produce.local.details_dialog.main_window,
                                                  file_name=Auto_Ground_Truth_Folder + 'G181_detail.png')
            check_detail = produce_page.compare(Ground_Truth_Folder + 'G181_detail.png', current_image)
            produce_page.press_esc_key()

          # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            for x in range(30):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)
            main_page.select_library_icon_view_media(explore_file)

            # Verify : Set timecode to (00:00:08:23)
            main_page.set_timeline_timecode('00_00_08_23', is_verify=False)
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G181_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G181_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step and check_detail

            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        with uuid("744fdddc-e8cb-4c8e-aefa-77013b67ae10") as case:
            # [G182] 16:9 / H.264 MP4 / NTSC / MPEG-4 1280 x 720/240p (40Mbps)

            main_page.click_produce()
            produce_page.check_enter_produce_page()

            produce_page.local.select_profile_name(7)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 1280 x 720/240p (40 Mb...':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()
            explore_full_path = self.check_current_produced_full_path()
            logger(explore_full_path)
            # Start : produce
            produce_page.click_start()
            for x in range(100):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Video compare
            main_page.select_library_icon_view_media(explore_file)
            video_compare_result = main_page.compare_video(explore_full_path,
                                                           Test_Material_Folder + 'Produce_Local/Produce_G182.mp4')
            case.result = video_compare_result
            logger(video_compare_result)

            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_30(self):
        main_page.timeline_select_track(2)
        video_path = Test_Material_Folder + 'Produce_Local/Produce_G167.m2ts'
        media_room_page.collection_view_right_click_import_media_files(video_path)
        time.sleep(DELAY_TIME)
        main_page.select_library_icon_view_media('Produce_G167.m2ts')
        media_room_page.library_clip_context_menu_insert_on_selected_track()

        with uuid("3b50a422-5bda-4f4b-8155-6681c14d3267") as case:
            # [G94] Produce Progress % > % displays normally when producing
            main_page.click_produce()
            produce_page.check_enter_produce_page()

            # File extension > H265
            produce_page.local.select_file_format(container='hevc')

            produce_page.local.select_profile_name(8)
            time.sleep(DELAY_TIME)

            produce_page.local.click_details()
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=L.produce.local.details_dialog.main_window,
                                                  file_name=Auto_Ground_Truth_Folder + 'G94_detail.png')
            # Want to generate GT folder file
            check_detail = produce_page.compare(Ground_Truth_Folder + 'G94_detail.png', current_image)
            produce_page.press_esc_key()

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()

            time.sleep(DELAY_TIME*4)

            # Click pause
            produce_page.click_pause()

            item = produce_page.exist(L.produce.txt_producing_video_progress)
            text_progress_bar = item.AXValue
            if text_progress_bar[21] == '%':
                current_value = int(text_progress_bar[19:21])
            elif text_progress_bar[20] == '%':
                current_value = int(text_progress_bar[19:20])
            else:
                current_value = 0
            if current_value > 0 and current_value < 100:
                logger(current_value)
                case.result = True
            else:
                case.result = False

        with uuid("6da8faa4-e897-46a3-8a73-bf06c2d2b3df") as case:
            # [G352] 16:9 / H.265 MP4 / NTSC /MPEG-4 4K 3840 x 2160/30p (37Mbps)
            produce_page.click_resume()

            for x in range(30):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)
            main_page.select_library_icon_view_media(explore_file)

            # Verify : Set timecode to (00:00:19:04)
            main_page.set_timeline_timecode('00_00_19_04', is_verify=False)
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G352_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G352_preview.png', current_image, similarity=0.97)
            check_detail = produce_page.compare(Ground_Truth_Folder + 'G94_detail.png', Auto_Ground_Truth_Folder + 'G94_detail.png')
            logger(check_detail)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step and check_detail

            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        with uuid("c5bb8b87-7f11-4699-a8b5-7bb526bf20dc") as case:
            # [G357] 16:9 / H.265 MP4 / PAL /MPEG-4 1280 x 720/25p (7Mbps)
            main_page.click_produce()
            produce_page.check_enter_produce_page()

            produce_page.local.select_country_video_format('pal')
            time.sleep(DELAY_TIME)
            produce_page.local.select_profile_name(4)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 1280 x 720/25p (7 Mbps)':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass


            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            for x in range(50):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Media Room > Right Click Menu > Check View Properties
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media(explore_file)
            main_page.right_click()
            main_page.select_right_click_menu('View Properties')
            time.sleep(DELAY_TIME*2)
            current_image = produce_page.snapshot(locator=L.media_room.properties_dialog.video_info,
                                                      file_name=Auto_Ground_Truth_Folder + 'G357_Properties_video.png')
            verify_step1 = produce_page.compare(Ground_Truth_Folder + 'G357_Properties_video.png', current_image)
            time.sleep(DELAY_TIME)
            # close View Properties
            main_page.exist_click(L.media_room.properties_dialog.btn_close)
            time.sleep(DELAY_TIME)


            # Verify 2 : Set timecode to (00:00:07:06)
            main_page.set_timeline_timecode('00_00_07_06', is_verify=False)
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G357_preview.png')
            verify_step2 = produce_page.compare(Ground_Truth_Folder + 'G357_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step1 and verify_step2
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_31(self):
        time.sleep(DELAY_TIME*2)
        video_path = Test_Material_Folder + 'Produce_Local/4978895.mov'
        media_room_page.collection_view_right_click_import_media_files(video_path)
        time.sleep(DELAY_TIME)
        main_page.insert_media('4978895.mov')
        time.sleep(DELAY_TIME)

        # Add music
        main_page.select_library_icon_view_media('Speaking Out.mp3')
        main_page.tips_area_insert_media_to_selected_track()

        # split music
        main_page.set_timeline_timecode(time_code='00_00_16_00', is_verify=False)
        main_page.tips_area_click_split()
        time.sleep(DELAY_TIME * 2)

        # select 2nd audio > remove
        timeline_page.select_timeline_media(1,1)
        time.sleep(DELAY_TIME)
        tips_area_page.more_features.remove()
        time.sleep(DELAY_TIME)

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("f1a1be96-2b99-445e-82ed-3da6097d802a") as case:
            # [G239] 16:9 / H.264 MKV / PAL / AVC 1920 x 1080/50p (28Mbps)

            produce_page.local.select_file_format(container='avc')

            produce_page.local.select_file_extension('mkv')
            time.sleep(DELAY_TIME)

            produce_page.local.select_country_video_format('pal')
            time.sleep(DELAY_TIME)

            produce_page.local.select_profile_name(9)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'AVC 1920 x 1080/50p (28 Mbps)':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            for x in range(30):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Media Room > Right Click Menu > Check View Properties
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media(explore_file)
            main_page.right_click()
            main_page.select_right_click_menu('View Properties')
            time.sleep(DELAY_TIME*2)
            current_image = produce_page.snapshot(locator=L.media_room.properties_dialog.video_info,
                                                      file_name=Auto_Ground_Truth_Folder + 'G239_Properties_video.png')
            verify_step1 = produce_page.compare(Ground_Truth_Folder + 'G239_Properties_video.png', current_image)
            time.sleep(DELAY_TIME)
            # close View Properties
            main_page.exist_click(L.media_room.properties_dialog.btn_close, timeout=10)
            time.sleep(DELAY_TIME)


            # Verify 2 : Set timecode to (00:00:13:00)
            main_page.set_timeline_timecode('00_00_13_00', is_verify=False)
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G239_preview.png')
            verify_step2 = produce_page.compare(Ground_Truth_Folder + 'G239_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step1 and verify_step2
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("239860b7-9923-4b35-981b-83e6cfe1d155") as case:
            # [G246] 16:9 / H.264 MKV / PAL / Custom profile
            produce_page.local.click_create_a_new_profile()
            check_result = produce_page.local.quality_profile_setup.apply_profile_name('Mac AT Custom G246',
                                                                                       'SFT Profile Test G246 custom profile')

            item = produce_page.find(L.produce.local.quality_profile_setup_dialog.profile_name.edittext_description)
            if produce_page.exist(item):
                AT_custom_description = item.AXValue
            if AT_custom_description == 'SFT Profile Test G246 custom profile':
                check_custom_description = True
            else:
                check_custom_description = False

            produce_page.local.quality_profile_setup.switch_to_video_tab()
            produce_page.local.quality_profile_setup.set_video_profile(index_resolution=8, index_frame_rate=8)
            produce_page.local.quality_profile_setup.set_video_bitrate(47300)

            # click OK > close (Quality Profile Setup)
            produce_page.local.quality_profile_setup.click_ok()

            produce_page.local.click_details()
            time.sleep(DELAY_TIME*2)
            current_image = produce_page.snapshot(locator=L.produce.local.details_dialog.main_window,
                                                  file_name=Auto_Ground_Truth_Folder + 'G246_detail.png')
            check_detail = produce_page.compare(Ground_Truth_Folder + 'G246_detail.png', current_image)
            produce_page.press_esc_key()

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            for x in range(90):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Media Room > Right Click Menu > Check View Properties
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media(explore_file)
            main_page.right_click()
            main_page.select_right_click_menu('View Properties')
            time.sleep(DELAY_TIME*2)
            current_image = produce_page.snapshot(locator=L.media_room.properties_dialog.video_info,
                                                      file_name=Auto_Ground_Truth_Folder + 'G246_Properties_video.png')
            verify_step1 = produce_page.compare(Ground_Truth_Folder + 'G246_Properties_video.png', current_image)
            time.sleep(DELAY_TIME)
            # close View Properties
            main_page.exist_click(L.media_room.properties_dialog.btn_close)
            time.sleep(DELAY_TIME)


            # Verify 2 : Set timecode to (00:00:03:00)
            main_page.set_timeline_timecode('00_00_03_00', is_verify=False)
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G246_preview.png')
            verify_step2 = produce_page.compare(Ground_Truth_Folder + 'G246_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step1 and verify_step2 and check_detail
            logger(f'{verify_step1}, {verify_step2}, {check_detail}')

            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        main_page.click_produce()
        with uuid("311c18e0-4b19-4637-b1c7-fb8dd6177a21") as case:
            # [G371] 16:9 / H.265 MKV / NTSC / HEVC 3840x2160/30p (37Mbps)
            # File extension > H265
            produce_page.local.select_file_format(container='hevc')
            time.sleep(DELAY_TIME)

            produce_page.local.select_file_extension('mkv')
            time.sleep(DELAY_TIME)

            produce_page.local.select_profile_name(7)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'HEVC 4K 3840 x 2160/30p (37 M...':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            for x in range(100):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Media Room > Right Click Menu > Check View Properties
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media(explore_file)
            main_page.right_click()
            main_page.select_right_click_menu('View Properties')
            time.sleep(DELAY_TIME*2)
            current_image = produce_page.snapshot(locator=L.media_room.properties_dialog.video_info,
                                                      file_name=Auto_Ground_Truth_Folder + 'G371_Properties_video.png')
            verify_step1 = produce_page.compare(Ground_Truth_Folder + 'G371_Properties_video.png', current_image)
            time.sleep(DELAY_TIME)
            # close View Properties
            main_page.exist_click(L.media_room.properties_dialog.btn_close)
            time.sleep(DELAY_TIME)


            # Verify 2 : Set timecode to (00:00:08:03)
            main_page.set_timeline_timecode('00_00_08_03', is_verify=False)
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G371_preview.png')
            verify_step2 = produce_page.compare(Ground_Truth_Folder + 'G371_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step1 and verify_step2 and check_detail
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_32(self):
        time.sleep(DELAY_TIME * 2)
        # Insert video from Material
        video_path = Test_Material_Folder + 'Produce_Local/Produce_G182.mp4'
        media_room_page.collection_view_right_click_import_media_files(video_path)
        time.sleep(DELAY_TIME)
        main_page.insert_media('Produce_G182.mp4')

        # Add music
        main_page.select_library_icon_view_media('Mahoroba.mp3')
        main_page.tips_area_insert_media_to_selected_track(0)

        # split music
        main_page.set_timeline_timecode(time_code='00_00_10_00', is_verify=False)
        main_page.tips_area_click_split()

        # select 2nd audio > remove
        timeline_page.select_timeline_media(1,1)
        tips_area_page.more_features.remove()

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("8912e188-9dca-45f1-8a38-f64ae866821f") as case:
            # [G183] 16:9 / H.264 MP4 / NTSC / MPEG-4 1920 x 1080/24p (16Mbps)
            produce_page.local.select_profile_name(8)
            time.sleep(DELAY_TIME)

            produce_page.local.click_details()
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=L.produce.local.details_dialog.main_window,
                                                  file_name=Auto_Ground_Truth_Folder + 'G183_detail.png')
            check_detail = produce_page.compare(Ground_Truth_Folder + 'G183_detail.png', current_image)
            produce_page.press_esc_key()

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            time.sleep(DELAY_TIME)
            for x in range(100):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media(explore_file)

            # Verify Preview : Set timecode to (00:00:01:11)
            main_page.set_timeline_timecode('00_00_01_11', is_verify=False)
            time.sleep(DELAY_TIME*2)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G183_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G183_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step and check_detail
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        main_page.click_produce()
        produce_page.check_enter_produce_page()
        with uuid("ba2887af-d60e-46cd-9084-025fe7dbe66c") as case:
            # [G184] 16:9 / H.264 MP4 / NTSC / MPEG-4 1920 x 1080/30p (16Mbps)
            produce_page.local.select_profile_name(9)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 1920 x 1080/30p (16 Mb...':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            time.sleep(DELAY_TIME)
            for x in range(120):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Media Room > Right Click Menu > Check View Properties
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media(explore_file)
            main_page.right_click()
            main_page.select_right_click_menu('View Properties')
            time.sleep(DELAY_TIME*2)
            current_image = produce_page.snapshot(locator=L.media_room.properties_dialog.video_info,
                                                      file_name=Auto_Ground_Truth_Folder + 'G184_Properties_video.png')
            verify_step1 = produce_page.compare(Ground_Truth_Folder + 'G184_Properties_video.png', current_image)
            time.sleep(DELAY_TIME)
            # close View Properties
            main_page.exist_click(L.media_room.properties_dialog.btn_close)
            time.sleep(DELAY_TIME)

            # Verify 2 : Set timecode to (00:00:03:22)
            main_page.set_timeline_timecode('00_00_03_22', is_verify=False)
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G184_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G184_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step and check_detail
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        # Add transition (Burning)
        main_page.enter_room(2)
        time.sleep(DELAY_TIME)
        main_page.select_LibraryRoom_category('Distortion')
        main_page.drag_transition_to_timeline_clip('Deform', 'Produce_G182')
        time.sleep(DELAY_TIME)
        tips_area_page.click_TipsArea_btn_Duration()
        tips_area_page.apply_duration_settings("00_00_05_00")

        main_page.click_produce()
        produce_page.check_enter_produce_page()
        with uuid("be4a85fc-1535-449c-95ff-f52f6dbd8f85") as case:
            # [G185] 16:9 / H.264 MP4 / NTSC / MPEG-4 1920 x 1080/60p (40Mbps)
            produce_page.local.select_profile_name(10)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 1920 x 1080/60p (40 Mb...':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            time.sleep(DELAY_TIME)
            for x in range(120):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Media Room > Right Click Menu > Check View Properties
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media(explore_file)
            main_page.right_click()
            main_page.select_right_click_menu('View Properties')
            time.sleep(DELAY_TIME*2)
            current_image = produce_page.snapshot(locator=L.media_room.properties_dialog.video_info,
                                                      file_name=Auto_Ground_Truth_Folder + 'G185_Properties_video.png')
            verify_step1 = produce_page.compare(Ground_Truth_Folder + 'G185_Properties_video.png', current_image)
            time.sleep(DELAY_TIME)
            # close View Properties
            main_page.exist_click(L.media_room.properties_dialog.btn_close)
            time.sleep(DELAY_TIME)

            # Verify : Set timecode to (00:00:02:18)
            main_page.set_timeline_timecode('00_00_02_18', is_verify=False)
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G185_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G185_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step and verify_step1
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_33(self):
        time.sleep(DELAY_TIME)
        main_page.insert_media('Skateboard 03.mp4')

        # Insert video from Material
        video_path = Test_Material_Folder + 'Produce_Local/Produce_G159.m2ts'
        media_room_page.collection_view_right_click_import_media_files(video_path)
        time.sleep(DELAY_TIME)
        main_page.timeline_select_track(2)
        main_page.insert_media('Produce_G159.m2ts')


        main_page.select_timeline_media('Produce_G159.m2ts')
        main_page.right_click()
        main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Overlay')

        main_page.click_produce()
        produce_page.check_enter_produce_page()
        with uuid("acd41c34-6a23-4317-a8c6-907c6cd83435") as case:
            # [G186] 16:9 / H.264 MP4 / NTSC / MPEG-4 1920 x 1080/120p (60Mbps)
            produce_page.local.select_profile_name(11)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 1920 x 1080/120p (60 M...':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            time.sleep(DELAY_TIME)
            for x in range(120):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Media Room > Right Click Menu > Check View Properties
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media(explore_file)
            main_page.right_click()
            main_page.select_right_click_menu('View Properties')
            time.sleep(DELAY_TIME*2)
            current_image = produce_page.snapshot(locator=L.media_room.properties_dialog.video_info,
                                                      file_name=Auto_Ground_Truth_Folder + 'G186_Properties_video.png')
            verify_step1 = produce_page.compare(Ground_Truth_Folder + 'G186_Properties_video.png', current_image)
            time.sleep(DELAY_TIME)
            # close View Properties
            main_page.exist_click(L.media_room.properties_dialog.btn_close)
            time.sleep(DELAY_TIME)

            # Verify : Set timecode to (00:00:04:10)
            main_page.set_timeline_timecode('00_00_04_10', is_verify=False)
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G186_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G186_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step and verify_step1
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        main_page.click_produce()
        produce_page.check_enter_produce_page()
        with uuid("0c27a6f1-2b02-4f42-babb-cc315c66092b") as case:
            # [G187] 16:9 / H.264 MP4 / NTSC / MPEG-4 2K 2048 x 1080/30p (40Mbps)
            produce_page.local.select_profile_name(12)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 2K 2048 x 1080/30p (40 ...':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            time.sleep(DELAY_TIME)
            for x in range(120):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Media Room > Right Click Menu > Check View Properties
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media(explore_file)
            main_page.right_click()
            main_page.select_right_click_menu('View Properties')
            time.sleep(DELAY_TIME*2)
            current_image = produce_page.snapshot(locator=L.media_room.properties_dialog.video_info,
                                                      file_name=Auto_Ground_Truth_Folder + 'G187_Properties_video.png')
            verify_step1 = produce_page.compare(Ground_Truth_Folder + 'G187_Properties_video.png', current_image)
            time.sleep(DELAY_TIME)
            # close View Properties
            main_page.exist_click(L.media_room.properties_dialog.btn_close)
            time.sleep(DELAY_TIME)

            # Verify : Set timecode to (00:00:06:18)
            main_page.set_timeline_timecode('00_00_06_18', is_verify=False)
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G187_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G187_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step and verify_step1
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        main_page.click_produce()
        produce_page.check_enter_produce_page()
        with uuid("46660a7f-c5e7-4bbb-bb54-8bf1a3bb32f5") as case:
            # [G188] 16:9 / H.264 MP4 / NTSC / MPEG-4 4K 3840 x 2160/30p (50Mbps)
            produce_page.local.select_profile_name(13)
            time.sleep(DELAY_TIME)

            produce_page.local.click_details()
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=L.produce.local.details_dialog.main_window,
                                                  file_name=Auto_Ground_Truth_Folder + 'G188_detail.png')
            check_detail = produce_page.compare(Ground_Truth_Folder + 'G188_detail.png', current_image)
            produce_page.press_esc_key()

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            time.sleep(DELAY_TIME)
            for x in range(120):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Media Room > Right Click Menu > Check View Properties
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media(explore_file)
            main_page.right_click()
            main_page.select_right_click_menu('View Properties')
            time.sleep(DELAY_TIME*2)
            current_image = produce_page.snapshot(locator=L.media_room.properties_dialog.video_info,
                                                      file_name=Auto_Ground_Truth_Folder + 'G188_Properties_video.png')
            verify_step1 = produce_page.compare(Ground_Truth_Folder + 'G188_Properties_video.png', current_image)
            time.sleep(DELAY_TIME)
            # close View Properties
            main_page.exist_click(L.media_room.properties_dialog.btn_close)
            time.sleep(DELAY_TIME)

            # Verify : Set timecode to (00:00:09:19)
            main_page.set_timeline_timecode('00_00_09_19', is_verify=False)
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G188_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G188_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step and verify_step1 and check_detail
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_34(self):
        time.sleep(DELAY_TIME * 2)
        video_path = Test_Material_Folder + 'Produce_Local/Y man.mp4'
        media_room_page.collection_view_right_click_import_media_files(video_path)
        time.sleep(DELAY_TIME)
        main_page.insert_media('Y man.mp4')
        time.sleep(DELAY_TIME)
        main_page.timeline_select_track(2)

        # Add Title : Motion Graphics 006
        main_page.enter_room(1)
        main_page.select_LibraryRoom_category('Motion Graphics')
        time.sleep(1)
        main_page.select_library_icon_view_media('Motion Graphics 006')
        main_page.tips_area_insert_media_to_selected_track()

        main_page.click_produce()
        produce_page.check_enter_produce_page()
        with uuid("b5068d44-a721-453c-b207-f6c29de8d91f") as case:
            # [G199] 16:9 / H.264 MP4 / PAL / MPEG-4 1920 x 1080/50p (40Mbps)
            produce_page.local.select_country_video_format('pal')
            time.sleep(DELAY_TIME)

            produce_page.local.select_profile_name(10)
            time.sleep(DELAY_TIME)

            produce_page.local.click_details()
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=L.produce.local.details_dialog.main_window,
                                                  file_name=Auto_Ground_Truth_Folder + 'G199_detail.png')
            check_detail = produce_page.compare(Ground_Truth_Folder + 'G199_detail.png', current_image)
            produce_page.press_esc_key()

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            time.sleep(DELAY_TIME)
            for x in range(120):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Media Room > Right Click Menu > Check View Properties
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media(explore_file)
            main_page.right_click()
            main_page.select_right_click_menu('View Properties')
            time.sleep(DELAY_TIME*2)
            current_image = produce_page.snapshot(locator=L.media_room.properties_dialog.video_info,
                                                      file_name=Auto_Ground_Truth_Folder + 'G199_Properties_video.png')
            verify_step1 = produce_page.compare(Ground_Truth_Folder + 'G199_Properties_video.png', current_image)
            time.sleep(DELAY_TIME)
            # close View Properties
            main_page.exist_click(L.media_room.properties_dialog.btn_close)
            time.sleep(DELAY_TIME)

            # Verify : Set timecode to (00:00:07:29)
            main_page.set_timeline_timecode('00_00_07_29', is_verify=False)
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G199_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G199_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step and verify_step1 and check_detail
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        main_page.click_produce()
        produce_page.check_enter_produce_page()
        with uuid("5716c2f4-503a-4421-8c82-c49c391dbf46") as case:
            # [G201] 16:9 / H.264 MP4 / PAL / MPEG-4 2K 2048 x 1080/25p (40Mbps)
            produce_page.local.select_country_video_format('pal')
            time.sleep(DELAY_TIME)

            produce_page.local.select_profile_name(12)
            time.sleep(DELAY_TIME)

            produce_page.local.click_details()
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=L.produce.local.details_dialog.main_window,
                                                  file_name=Auto_Ground_Truth_Folder + 'G201_detail.png')
            check_detail = produce_page.compare(Ground_Truth_Folder + 'G201_detail.png', current_image)
            produce_page.press_esc_key()

            # Get produced file name
            explore_file = produce_page.get_produced_filename()
            explore_full_path = self.check_current_produced_full_path()
            #logger(explore_full_path)

            # Start : produce
            produce_page.click_start()
            time.sleep(DELAY_TIME)
            for x in range(140):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Video compare
            main_page.select_library_icon_view_media(explore_file)
            video_compare_result = main_page.compare_video(explore_full_path, Test_Material_Folder + 'Produce_Local/Produce_G201.mp4')
            logger(video_compare_result)

            # Verify :  Media Room > Right Click Menu > Check View Properties
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media(explore_file)

            # Verify : Set timecode to (00:00:05:03)
            main_page.set_timeline_timecode('00_00_05_03', is_verify=False)
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G201_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G201_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step and video_compare_result
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        main_page.click_produce()
        produce_page.check_enter_produce_page()
        with uuid("21e9152e-067c-45a0-a020-e15ab1ca1d83") as case:
            # [G203] 16:9 / H.264 MP4 / PAL / MPEG-4 4K 4096 x 2160/25p (50Mbps)
            produce_page.local.select_country_video_format('pal')
            time.sleep(DELAY_TIME)

            produce_page.local.select_profile_name(14)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 4K 4096 x 2160/25p (50 ...':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            time.sleep(DELAY_TIME)
            for x in range(120):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Media Room > Right Click Menu > Check View Properties
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media(explore_file)
            main_page.right_click()
            main_page.select_right_click_menu('View Properties')
            time.sleep(DELAY_TIME*2)
            current_image = produce_page.snapshot(locator=L.media_room.properties_dialog.video_info,
                                                      file_name=Auto_Ground_Truth_Folder + 'G203_Properties_video.png')
            verify_step1 = produce_page.compare(Ground_Truth_Folder + 'G203_Properties_video.png', current_image)
            time.sleep(DELAY_TIME)
            # close View Properties
            main_page.exist_click(L.media_room.properties_dialog.btn_close)
            time.sleep(DELAY_TIME)

            # Verify : Set timecode to (00:00:02:15)
            main_page.set_timeline_timecode('00_00_02_15', is_verify=False)
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G203_preview.png')
            verify_preview = produce_page.compare(Ground_Truth_Folder + 'G203_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_preview and verify_step1
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_35(self):
        # Insert video 1 from Material
        video_path = Test_Material_Folder + 'Produce_Local/Test_4_3.m2ts'
        media_room_page.collection_view_right_click_import_media_files(video_path)
        time.sleep(DELAY_TIME)
        main_page.set_project_aspect_ratio_4_3()
        main_page.insert_media('Test_4_3.m2ts')
        time.sleep(DELAY_TIME)

        # Insert video 2 from Material
        video_path = Test_Material_Folder + 'Produce_Local/Produce_G201.mp4'
        media_room_page.collection_view_right_click_import_media_files(video_path)
        time.sleep(DELAY_TIME)
        main_page.timeline_select_track(2)
        main_page.insert_media('Produce_G201.mp4')
        time.sleep(DELAY_TIME)

        main_page.select_timeline_media('Produce_G201.mp4')
        main_page.right_click()
        main_page.select_right_click_menu('Set Clip Attributes', 'Set Blending Mode', 'Lighten')

        main_page.click_produce()
        produce_page.check_enter_produce_page()
        with uuid("8ede3f98-57bb-4705-878f-4e9153fef68f") as case:
            # [G275] 4:3 / H.264 MKV / NTSC / AVC 4K 4096 x 3072/30p (50Mbps)
            produce_page.local.select_file_extension('mkv')
            time.sleep(DELAY_TIME)

            produce_page.local.select_profile_name(5)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'AVC 4K 4096 x 3072/30p (50 Mb...':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            time.sleep(DELAY_TIME)
            for x in range(150):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Media Room > Right Click Menu > Check View Properties
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media(explore_file)
            main_page.right_click()
            main_page.select_right_click_menu('View Properties')
            time.sleep(DELAY_TIME*2)
            current_image = produce_page.snapshot(locator=L.media_room.properties_dialog.video_info,
                                                      file_name=Auto_Ground_Truth_Folder + 'G275_Properties_video.png')
            verify_step1 = produce_page.compare(Ground_Truth_Folder + 'G275_Properties_video.png', current_image)
            time.sleep(DELAY_TIME)
            # close View Properties
            main_page.exist_click(L.media_room.properties_dialog.btn_close)
            time.sleep(DELAY_TIME*2)

            # Verify : Set timecode to (00:00:03:20)
            main_page.set_timeline_timecode('00_00_03_20', is_verify=False)
            time.sleep(DELAY_TIME*3)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G275_preview.png')
            verify_preview = produce_page.compare(Ground_Truth_Folder + 'G275_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_preview and verify_step1
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        main_page.click_produce()
        produce_page.check_enter_produce_page()
        with uuid("72c99383-ee23-4cfe-8c74-679f58b7b2eb") as case:
            # [G399] 4:3 / H.265 MKV / NTSC / HEVC 720 x 576/24p (6Mbps)
            produce_page.local.select_file_format(container='hevc')
            time.sleep(DELAY_TIME)

            produce_page.local.select_file_extension('mkv')
            time.sleep(DELAY_TIME)

            produce_page.local.select_profile_name(2)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'HEVC 720 x 576/24p (6 Mbps)':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            time.sleep(DELAY_TIME)
            for x in range(150):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Media Room > Right Click Menu > Check View Properties
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media(explore_file)
            main_page.right_click()
            main_page.select_right_click_menu('View Properties')
            time.sleep(DELAY_TIME*2)
            current_image = produce_page.snapshot(locator=L.media_room.properties_dialog.video_info,
                                                      file_name=Auto_Ground_Truth_Folder + 'G399_Properties_video.png')
            verify_step1 = produce_page.compare(Ground_Truth_Folder + 'G399_Properties_video.png', current_image)
            time.sleep(DELAY_TIME)
            # close View Properties
            main_page.exist_click(L.media_room.properties_dialog.btn_close)
            time.sleep(DELAY_TIME)

            # Verify : Set timecode to (00:00:09:03)
            main_page.set_timeline_timecode('00_00_09_03', is_verify=False)
            time.sleep(DELAY_TIME*2)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G399_preview.png')
            verify_preview = produce_page.compare(Ground_Truth_Folder + 'G399_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_preview and verify_step1
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        main_page.click_produce()
        produce_page.check_enter_produce_page()
        with uuid("619d663e-ec30-4c7a-bfa8-13f21983d46b") as case:
            # [G400] 4:3 / H.265 MKV / NTSC / HEVC 2K 2048 x 1536/30p (30Mbps)
            produce_page.local.select_file_format(container='hevc')
            time.sleep(DELAY_TIME)

            produce_page.local.select_file_extension('mkv')
            time.sleep(DELAY_TIME)

            produce_page.local.select_profile_name(3)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'HEVC 2K 2048 x 1536/30p (30 M...':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            time.sleep(DELAY_TIME)
            for x in range(150):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Media Room > Right Click Menu > Check View Properties
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media(explore_file)
            main_page.right_click()
            main_page.select_right_click_menu('View Properties')
            time.sleep(DELAY_TIME*2)
            current_image = produce_page.snapshot(locator=L.media_room.properties_dialog.video_info,
                                                      file_name=Auto_Ground_Truth_Folder + 'G400_Properties_video.png')
            verify_step1 = produce_page.compare(Ground_Truth_Folder + 'G400_Properties_video.png', current_image)
            time.sleep(DELAY_TIME)
            # close View Properties
            main_page.exist_click(L.media_room.properties_dialog.btn_close)
            time.sleep(DELAY_TIME)

            # Verify : Set timecode to (00:00:07:09)
            main_page.set_timeline_timecode('00_00_07_09', is_verify=False)
            time.sleep(DELAY_TIME*3)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G400_preview.png')
            verify_preview = produce_page.compare(Ground_Truth_Folder + 'G400_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_preview and verify_step1
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_36(self):
        time.sleep(DELAY_TIME * 2)
        # Insert video 1 from Material
        video_path = Test_Material_Folder + 'Produce_Local/Test_4_3.m2ts'
        media_room_page.collection_view_right_click_import_media_files(video_path)
        time.sleep(DELAY_TIME)
        main_page.set_project_aspect_ratio_4_3()
        main_page.insert_media('Test_4_3.m2ts')
        time.sleep(DELAY_TIME)

        main_page.timeline_select_track(2)

        # Add Title : Motion Graphics 005
        main_page.enter_room(1)
        main_page.select_LibraryRoom_category('Motion Graphics')
        time.sleep(1)
        main_page.select_library_icon_view_media('Motion Graphics 005')
        main_page.tips_area_insert_media_to_selected_track()

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("7af3b683-7cc6-4618-91c9-0922dd23b69b") as case:
            # [G393] 4:3 / H.265 MP4 / NTSC / MPEG-4 4K 4096 x 3072/30p (37Mbps)
            produce_page.local.select_file_format(container='hevc')
            time.sleep(DELAY_TIME)

            produce_page.local.select_file_extension('mp4')
            time.sleep(DELAY_TIME)

            produce_page.local.select_profile_name(4)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 4K 4096 x 3072/30p (37...':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            time.sleep(DELAY_TIME)
            for x in range(150):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Media Room > Right Click Menu > Check View Properties
            time.sleep(DELAY_TIME * 5)
            main_page.select_library_icon_view_media(explore_file)
            main_page.right_click()
            main_page.select_right_click_menu('View Properties')
            time.sleep(DELAY_TIME*2)
            current_image = produce_page.snapshot(locator=L.media_room.properties_dialog.video_info,
                                                      file_name=Auto_Ground_Truth_Folder + 'G393_Properties_video.png')
            verify_step1 = produce_page.compare(Ground_Truth_Folder + 'G393_Properties_video.png', current_image)
            time.sleep(DELAY_TIME)
            # close View Properties
            main_page.exist_click(L.media_room.properties_dialog.btn_close)
            time.sleep(DELAY_TIME)

            # Verify : Set timecode to (00:00:06:04)
            main_page.set_timeline_timecode('00_00_06_04', is_verify=False)
            time.sleep(DELAY_TIME*3)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G393_preview.png')
            verify_preview = produce_page.compare(Ground_Truth_Folder + 'G393_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_preview and verify_step1
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_37(self):
        time.sleep(DELAY_TIME * 2)
        # Insert video 1 from Material
        video_path = Test_Material_Folder + 'Produce_Local/Test_4_3.m2ts'
        media_room_page.collection_view_right_click_import_media_files(video_path)
        time.sleep(DELAY_TIME)
        main_page.set_project_aspect_ratio_4_3()
        main_page.insert_media('Test_4_3.m2ts')
        time.sleep(DELAY_TIME)

        main_page.timeline_select_track(2)

        # Add Title : Motion Graphics 004
        main_page.enter_room(1)
        main_page.select_LibraryRoom_category('Motion Graphics')
        time.sleep(1)
        main_page.select_library_icon_view_media('Motion Graphics 004')
        main_page.tips_area_insert_media_to_selected_track()

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("cfc6fff8-1e15-4394-aaf8-a3324229c441") as case:
            # [G396] 4:3 / H.265 MP4 / PAL / MPEG-4 2K 2048 x 1536/25p (30Mbps)
            produce_page.local.select_file_format(container='hevc')
            time.sleep(DELAY_TIME)

            produce_page.local.select_file_extension('mp4')
            time.sleep(DELAY_TIME)

            produce_page.local.select_country_video_format('pal')
            time.sleep(DELAY_TIME)

            produce_page.local.select_profile_name(3)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 2K 2048 x 1536/25p (30 ...':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            time.sleep(DELAY_TIME)
            for x in range(150):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)

            # Verify :  Media Room > Right Click Menu > Check View Properties
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media(explore_file)
            main_page.right_click()
            main_page.select_right_click_menu('View Properties')
            time.sleep(DELAY_TIME*2)
            current_image = produce_page.snapshot(locator=L.media_room.properties_dialog.video_info,
                                                      file_name=Auto_Ground_Truth_Folder + 'G396_Properties_video.png')
            verify_step1 = produce_page.compare(Ground_Truth_Folder + 'G396_Properties_video.png', current_image)
            time.sleep(DELAY_TIME)
            # close View Properties
            main_page.exist_click(L.media_room.properties_dialog.btn_close)
            time.sleep(DELAY_TIME)

            # Verify : Set timecode to (00:00:07:15)
            main_page.set_timeline_timecode('00_00_07_15', is_verify=False)
            time.sleep(DELAY_TIME*4)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G396_preview.png')
            verify_preview = produce_page.compare(Ground_Truth_Folder + 'G396_preview.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_preview and verify_step1
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_38(self):
        main_page.insert_media('Skateboard 03.mp4')

        with uuid("1448cbd9-6503-4027-b3dd-f13a1627b124") as case:
            main_page.click_produce()
            produce_page.check_enter_produce_page()
            # [G205] H264 / 16:9 MKV / Profile description

            produce_page.local.select_file_extension('mkv')
            time.sleep(DELAY_TIME)

            item = produce_page.find(L.produce.local.text_area_profile_description)
            if not item:
                case.result = False

            if item.AXValue.startswith('This profile encodes MPEG-4 AVC (H.264) video format in a '
                                        'high definition profile that is compatible with AVCHD. MPEG-4'
                                        ' AVC uses a better compression rate compared to MPEG-2,'):
                case.result = True
            else:
                case.result = False