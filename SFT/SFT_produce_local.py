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
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="Produce_Local.html")
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

class Test_Produce_Local():
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
            google_sheet_execution_log_init('Produce_Local')

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
        if produce_page.find(L.media_room.confirm_dialog.chx_do_not_show_again):
            el_chx_do_not_show = produce_page.exist(L.media_room.confirm_dialog.chx_do_not_show_again)
            chx_position = el_chx_do_not_show.AXPosition
            chx_size = el_chx_do_not_show.AXSize
            if tick:
                produce_page.mouse.click(int(chx_position[0] + chx_size[0] / 4), int(chx_position[1] + chx_size[1] / 2))

            produce_page.exist_click(L.media_room.confirm_dialog.btn_no)
            time.sleep(DELAY_TIME)

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_7(self):
        # Open project
        main_page.top_menu_bar_file_open_project()
        project_path = Test_Material_Folder + 'Produce_Local/Test_A.pds'
        main_page.handle_open_project_dialog(project_path)

        # handle open project
        self.check_dont_show_again_dialog(tick=0)
        # handle high_definition_video_confirm_dialog_click_no
        self.check_dont_show_again_dialog(tick=0)

        main_page.click_produce()
        # File extension > H265
        produce_page.local.select_file_format(container='hevc')

        # NTSC
        produce_page.local.select_country_video_format('ntsc')

        # select profile name - HEVC 4096x2160/30p (37Mbps)
        produce_page.local.select_profile_name(9)

        check_profile = produce_page.local.get_profile_name()
        if check_profile != 'MPEG-4 4096 x 2160/30p (37 M...':
            logger('profile setting [Verify Fail]')
            raise Exception

        with uuid("b04dcdec-3702-4c07-8f17-ec0b47c14a73") as case:
            # [G88] Click Start

            # Start : produce
            check_result = produce_page.click_start()
            case.result = check_result

        # check default remain size
        default_remain_size = produce_page.get_pie_chart_remaining_size()

        # check default produced size
        default_produced_size = produce_page.get_pie_chart_produced_size()

        # check default remain time
        default_remain_time = produce_page.get_pie_chart_time_remaining()

        # check default elapsed time
        default_elapsed_time = produce_page.get_pie_chart_time_elapsed()
        with uuid("e45d443a-934e-4d8a-8287-5048458aaba0") as case:
            # [G90] Pause
            time.sleep(DELAY_TIME*2)
            produce_page.click_pause()
            time.sleep(DELAY_TIME)
            with uuid("affffad7-c709-4675-9b4a-f7a4c3eb87f8") as case:
                # [G79] Pie chart > Remaining
                current_remain_size = produce_page.get_pie_chart_remaining_size()
                if default_remain_size > current_remain_size:
                    case.result = True
                else:
                    case.result = False

                with uuid("6e5410e5-f7b3-455d-8757-fe21077a208e") as case:
                    current_produced_size = produce_page.get_pie_chart_produced_size()
                    # [G80] Pie chart > produced
                    if current_produced_size > default_produced_size:
                        case.result = True
                    else:
                        case.result = False

                    with uuid("1b17b43d-6371-4c9d-ba51-5969a9f0c5c8") as case:
                        # [G82] Pie chart > Time remain
                        current_time_remain = produce_page.get_pie_chart_time_remaining()
                        if current_time_remain > default_remain_time:
                            case.result = True
                        else:
                            case.result = False

                        with uuid("946a75c1-2f3a-457c-82fb-eaa239407bea") as case:
                            # [G83] Pie chart > Time elapsed
                            current_time_elapsed = produce_page.get_pie_chart_time_elapsed()
                            if current_time_elapsed > default_elapsed_time:
                                case.result = True
                            else:
                                case.result = False
            produce_page.click_resume()
            if produce_page.exist(L.produce.btn_pause_produce, timeout=6):
                case.result = True
            else:
                case.result = False

        with uuid("318e95dc-bd83-4c68-92c0-06cf7674603c") as case:
            # [G91] Cancel Produce > Yes
            # build v2922 / v3026 bug if no clear cache
            produce_page.click_cancel_rendering()
            produce_page.click_confirm_cancel_rendering_dialog_yes()
            check_result = produce_page.is_exist(locator=L.produce.btn_start_produce, timeout=6)
            case.result = check_result

        # .......
        # Handle [G326] Profile setting
        # M2TS > HEVC 1920x1080/24p (11Mbps)
        produce_page.local.select_file_extension('m2ts')
        time.sleep(DELAY_TIME)

        # select profile name - HEVC 1920x1080/24p (11Mbps)
        produce_page.local.select_profile_name(5)
        time.sleep(DELAY_TIME)
        check_profile = produce_page.local.get_profile_name()
        #logger(check_profile)
        if check_profile != 'HEVC 1920 x 1080/24p (11 Mbps)':
            logger('Check profile setting error')
            raise Exception
        else:
            pass

        # Get produced file name
        explore_file = produce_page.get_produced_filename()

        # Start : produce
        produce_page.click_start()

        with uuid("f9c4094a-3486-4de7-8e04-caab3314d765") as case:
            # [G96] [Complete] stage > Message
            check_result = False
            for x in range(30):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)
            case.result = check_result

        with uuid("b22f579f-cef4-4531-af1f-bb177e6d7224") as case:
            # [G97] Back to the Edit page
            check_result = produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 3)
            case.result = check_result

        # handle high_definition_video_confirm_dialog_click_no
        self.check_dont_show_again_dialog(tick=0)
        with uuid("fbe46cea-8f1a-4de8-be62-4b7ee0e9860a") as case:
            # [G326] Profile setting : M2TS > HEVC 1920x1080/24p (11Mbps)
            main_page.select_library_icon_view_media('Food.jpg')
            time.sleep(DELAY_TIME)
            check_media_room_result = main_page.select_library_icon_view_media(explore_file)


            main_page.set_timeline_timecode('00_00_07_10', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G326.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G326.png', current_image)

            case.result = verify_step
            logger(verify_step)
            # Final: Remove the produce file if test case is True
            if check_media_room_result is True:
                main_page.select_library_icon_view_media(explore_file)
                media_room_page.library_clip_context_menu_move_to_trash_can()
                time.sleep(DELAY_TIME)

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_1(self):
        check_preferences_default = self.check_preferences_explore_folder()
        with uuid("93769391-8cab-4ad5-ba5f-a33816d21c6d") as case:
            # [G8] [Produce] Tab > Disable
            item = produce_page.find(L.main.btn_produce)
            btn_status = item.AXEnabled
            #logger(btn_status)
            if btn_status is False:
                case.result = True
            else:
                case.result = False

        with uuid("e84cdeca-62f7-43f7-85ec-d34cee2bf3d2") as case:
            # [G9] [Produce] Tab > Enable
            # Insert Skateboard 01.mp4
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            media_room_page.library_clip_context_menu_insert_on_selected_track()
            main_page.click_produce()
            check_result = produce_page.check_enter_produce_page()
            case.result = check_result

        with uuid("ef8667cb-f5ea-41cf-8cf1-01dfc3a6eb6c") as case:
            # [G60] 1.5 Preview Panel > Play / Pause
            produce_page.click_preview_operation('play')
            time.sleep(DELAY_TIME*2)
            produce_page.click_preview_operation('pause')
            case.result = True

        with uuid("2586e253-02a7-4b5d-9a5c-af903095de49") as case:
            #[G39] Profile Editing > Edit (Default disable)

            # File extension > H264
            produce_page.local.select_file_format(container='avc')

            item = produce_page.find(L.produce.local.btn_edit_custom_profile)
            btn_status = item.AXEnabled
            if btn_status is False:
                case.result = True
            else:
                case.result = False

        with uuid("a9e838a5-6f7b-4140-8cfa-2609d024e82f") as case:
            #[G71] Explore folder > Default
            # Get produce path
            explore_folder_path = produce_page.exist(L.produce.edittext_output_folder).AXValue
            explore_file = produce_page.get_produced_filename()
            skip_string = f'/{explore_file}'
            logger(skip_string)
            produce_page_current_path = explore_folder_path.replace(skip_string,'')

            if produce_page_current_path == check_preferences_default:
                case.result = True
            else:
                case.result = False

        with uuid("f8454411-c900-49f0-a85f-0c78750fa17e") as case:
            #[G72] Explore folder > Custom path
            produce_page.select_output_folder(Auto_Ground_Truth_Folder+'test')
            time.sleep(DELAY_TIME)
            explore_folder_path = produce_page.exist(L.produce.edittext_output_folder).AXValue

            check_custom_path = Auto_Ground_Truth_Folder+'test.mp4'
            if check_custom_path == explore_folder_path:
                case.result = True
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid("9e730f8c-a53e-4397-91b2-2c67ffe58731") as case:
            # [G15] Intelligent SVRT > Source Format H264 MP4
            # Insert Skateboard 01.mp4
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            media_room_page.library_clip_context_menu_insert_on_selected_track()
            main_page.click_produce()
            produce_page.check_enter_produce_page()

            with uuid("c1e91225-fcb6-4d9a-a1fc-76f9a7ffe624") as case:
                # [G19] Intelligent SVRT > Detection Result > Custom profile
                produce_page.local.click_profile_analyzer()
                time.sleep(DELAY_TIME*5)
                check_profile_name = produce_page.local.profile_analyzer.get_profile_name(index=1)
                #logger(check_profile_name)
                if check_profile_name == 'Custom Profile -1':
                    case.result = True
                else:
                    case.result = False

            if check_profile_name == 'Custom Profile -1':
                case.result = True
            else:
                case.result = False

        with uuid("50bafb1b-4486-4d98-9c01-35bd1eeffbb5") as case:
            # [G21] Control buttons > X button
            check_result = produce_page.local.profile_analyzer.click_close()
            case.result = check_result

        with uuid("65c1eb47-9533-4499-9151-b7da11f970b5") as case:
            # [G41] Profile Editing > Delete > Disable
            item = produce_page.find(L.produce.local.btn_delete_custom_profile)
            btn_status = item.AXEnabled
            # logger(btn_status)
            if btn_status is False:
                case.result = True
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        # Open project
        main_page.top_menu_bar_file_open_project()
        project_path = Test_Material_Folder + 'Produce_Local/AVC_M2ts.pds'
        main_page.handle_open_project_dialog(project_path)
        check_result = media_room_page.high_definition_video_confirm_dialog_click_no()
        logger(check_result)
        check_result = media_room_page.high_definition_video_confirm_dialog_click_no()
        logger(check_result)

        main_page.click_produce()
        produce_page.check_enter_produce_page()
        with uuid("de26389c-4ebf-4c89-8e18-d3122caf92ce") as case:
            # [G16] Intelligent SVRT > Source Format H264 M2TS
            produce_page.local.click_profile_analyzer()
            time.sleep(DELAY_TIME * 5)
            check_profile_name = produce_page.local.profile_analyzer.get_profile_name(index=1)
            # logger(check_profile_name)
            if check_profile_name == 'Custom Profile -1':
                case.result = True
            else:
                case.result = False

        with uuid("e26e63a4-6652-4f79-a260-28a0f9595724") as case:
            # [G20] Intelligent SVRT > Details (Edit)
            # PDR20.0.3303 Bug (Exception is due to Verify Step [FAIL]
            # Bug code : VDE213308-0012
            check_result = produce_page.local.profile_analyzer.click_detail()
            time.sleep(DELAY_TIME*2)
            #logger(check_result)

            current_image = produce_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G20.png')
            compare_result = produce_page.compare(Ground_Truth_Folder + 'G20.png', current_image)
            #logger(compare_result)

            case.result = check_result and compare_result

        with uuid("3865cf88-639f-4507-8ef0-d3d814a15634") as case:
            # [G27] Profile type > All
            main_page.click_produce()
            produce_page.check_enter_produce_page()
            check_result = produce_page.local.select_profile_type('all')
            case.result = check_result

        with uuid("95eeca47-0799-4769-a4fd-18abc496071c") as case:
            # [G29] H264 + M2TS
            produce_page.local.select_file_extension('m2ts')
            time.sleep(DELAY_TIME)
            explore_file = produce_page.get_produced_filename()
            if explore_file == 'AVC_M2ts.m2ts':
                case.result = True
            else:
                case.result = False

            # Get produced file full path
            current_explore_file = self.check_current_produced_full_path()
            #logger(current_explore_file)

        with uuid("cc781e56-1c4e-49ae-977c-63cce0a62131") as case:
            # [G132] M2TS > NTSC AVC 1280 x 720/24p (16Mbps)

            # Adjust AVC 1280 x 720/24p (16Mbps)
            produce_page.local.select_profile_name(index=3)
            time.sleep(DELAY_TIME)
            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'AVC 1280 x 720/24p (16 Mbps)':
                logger('Check profile setting error')
                raise Exception
            else:
                pass

            produce_page.click_start()
            time.sleep(DELAY_TIME*5)
            check_produce_result_1 = produce_page.click_back_to_edit()
            if check_produce_result_1:
                time.sleep(DELAY_TIME*3)
                check_media_room_result = main_page.select_library_icon_view_media(explore_file)

            case.result = check_media_room_result

            # Final: Remove the produce file (AVC_M2ts.m2ts) if test case is True
            if check_media_room_result is True:
                media_room_page.library_clip_context_menu_move_to_trash_can()
                time.sleep(DELAY_TIME)

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        with uuid("affbd2f0-672e-49f8-be6c-ab682ad2c1eb") as case:
            # [G106] 2.1 XAVC S > 16:9 Project > NTSC (MP4) > XAVC S 1280x720/30p (17Mbps)
            main_page.select_library_icon_view_media('Skateboard 03.mp4')
            media_room_page.library_clip_context_menu_insert_on_selected_track()
            main_page.click_produce()
            produce_page.check_enter_produce_page()

            # click XAVC S
            produce_page.local.select_file_format(container='xavc_s')

            # select profile name
            produce_page.local.select_profile_name(2)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'XAVC S 1280 x 720/30p (17 Mbps)':
                logger('Check profile setting error')
                raise Exception
            else:
                pass
            logger('pass')

            # Get produced file full path & explore file name
            explore_file = produce_page.get_produced_filename()
            current_explore_file = self.check_current_produced_full_path()

            # Start : produce
            produce_page.click_start()
            for x in range(10):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME*3)
            check_result = main_page.select_library_icon_view_media(explore_file)
            case.result = check_result

        with uuid("66e0b7a3-b189-47f3-a907-a06efe58d2d3") as case:
            # [G18] Intelligent SVRT > Detection Result > Default profile

            # Step1: remote timeline clip
            timeline_page.select_timeline_media(track_index=0, clip_index=0)
            tips_area_page.more_features.remove()

            # Add produced clip to timeline > Enter Produce page
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_insert_on_selected_track()
            main_page.click_produce()
            produce_page.check_enter_produce_page()

            produce_page.local.click_profile_analyzer()
            time.sleep(DELAY_TIME * 5)
            check_profile_name = produce_page.local.profile_analyzer.get_profile_name(index=1)
            logger(check_profile_name)
            if check_profile_name == check_profile:
                case.result = True
            else:
                case.result = False

        with uuid("403fc859-0f45-4dba-9e89-a0a7876cf200") as case:
            # [G22] Control buttons > Cancel
            produce_page.local.profile_analyzer.click_cancel()
            time.sleep(DELAY_TIME)
            # Verify : Check if close "Profile Analyzer" window
            if produce_page.exist(L.produce.local.profile_analyzer.btn_cancel):
                case.result = False
            else:
                case.result = True

            # Back to Media room to remove the produced file
            produce_page.click_edit()
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        # Open project
        main_page.top_menu_bar_file_open_project()
        project_path = Test_Material_Folder + 'Produce_Local/AVC_MKV.pds'
        main_page.handle_open_project_dialog(project_path)

        # handle open project > don't show again
        self.check_dont_show_again_dialog(tick=0)

        main_page.click_produce()
        produce_page.check_enter_produce_page()
        with uuid("34b9b70e-b6ef-4c6b-97bf-e2b8568b08a6") as case:
            # [G17] Intelligent SVRT > Source Format H264 MKV
            produce_page.local.click_profile_analyzer()
            time.sleep(DELAY_TIME * 5)
            check_profile_name = produce_page.local.profile_analyzer.get_profile_name(index=1)
            # logger(check_profile_name)
            if check_profile_name == 'Custom Profile -1':
                case.result = True
            else:
                case.result = False

            # click Cancel to close (Profile Analyzer) window
            produce_page.local.profile_analyzer.click_cancel()
            time.sleep(DELAY_TIME)

        with uuid("7e13ef50-4196-4555-af49-12b77fade24f") as case:
            # [G30] File extension > H265
            check_result = produce_page.local.select_file_format(container='hevc')
            case.result = check_result

        with uuid("8f588a20-5ba3-4080-a4f0-226e677bcecb") as case:
            # [G31] File extension > H265 > MKV
            check_result = produce_page.local.select_file_extension('mkv')
            case.result = check_result

            time.sleep(DELAY_TIME)
            explore_file = produce_page.get_produced_filename()
            if explore_file == 'AVC_MKV.mkv':
                case.result = True
            else:
                case.result = False

            # Get produced file full path
            current_explore_file = self.check_current_produced_full_path()
            logger(current_explore_file)

        with uuid("8c3193b5-9986-4ae6-824d-1b703eb62e46") as case:
            # [G45] Country/video format of disk  > PAL
            check_result = produce_page.local.select_country_video_format('pal')
            case.result = check_result

        with uuid("43228a68-025f-4b57-8d06-eed6d4571ddc") as case:
            # [G375] HEVC 4096x2160/25p (37Mbps)
            # select profile name
            produce_page.local.select_profile_name(8)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            logger(check_profile)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'HEVC 4K 4096 x 2160/25p (37 M...':
                logger('Check profile setting error')
                raise Exception
            else:
                pass
            logger('pass')

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
            time.sleep(DELAY_TIME * 3)

            # if find don't show again checkbox > tick Do not show again
            if produce_page.find(L.media_room.confirm_dialog.chx_do_not_show_again):
                el_chx_do_not_show = produce_page.exist(L.media_room.confirm_dialog.chx_do_not_show_again)
                chx_position = el_chx_do_not_show.AXPosition
                chx_size = el_chx_do_not_show.AXSize
                produce_page.mouse.click(int(chx_position[0] + chx_size[0] / 4), int(chx_position[1] + chx_size[1] / 2))

                # click no
                produce_page.exist_click(L.media_room.confirm_dialog.btn_no)
                time.sleep(DELAY_TIME)

            time.sleep(DELAY_TIME * 2)

            # Verify : Can find the produced file in Media Room
            verify_step1 = main_page.select_library_icon_view_media(explore_file)
            case.result = verify_step1
            # Verify 2 : Set timecode to (00:00:05:00)
            #main_page.set_timeline_timecode('00_00_05_00', is_verify=False)
            #time.sleep(DELAY_TIME * 5)
            #current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
            #                                          file_name=Auto_Ground_Truth_Folder + 'G375.png')
            #verify_step2 = produce_page.compare(Ground_Truth_Folder + 'G375.png', current_image)
            #time.sleep(DELAY_TIME*2)
            #case.result = verify_step1 and verify_step2
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):
        # Insert Skateboard 02.mp4
        main_page.select_library_icon_view_media('Skateboard 02.mp4')
        media_room_page.library_clip_context_menu_insert_on_selected_track()
        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("6d24d54d-6b0b-45ba-aa15-5c87ceb9912c") as case:
            # [G44] NTSC
            produce_page.local.select_country_video_format('pal')
            time.sleep(DELAY_TIME)
            check_result = produce_page.local.select_country_video_format('ntsc')
            case.result = check_result

            # select AVC
            produce_page.local.select_file_format(container='avc')
        with uuid("fdb1be7f-fad8-4f93-a52f-b0a2d857c1da") as case:
            # [G32] Create a new profile > Able to set profile name
            with uuid("928692bc-8f48-44a0-aab6-bbdee0183ffb") as case:
                # [G33] Create a new profile > Able to set description
                produce_page.local.click_create_a_new_profile()
                check_result = produce_page.local.quality_profile_setup.apply_profile_name('Mac AT Custom Profile', 'SFT Profile Description')

                item = produce_page.find(L.produce.local.quality_profile_setup_dialog.profile_name.edittext_description)
                if produce_page.exist(item):
                    check_result = item.AXValue
                if check_result == 'SFT Profile Description':
                    case.result = True
                else:
                    case.result = False

            item = produce_page.find(L.produce.local.quality_profile_setup_dialog.profile_name.edittext_profile_name)
            if produce_page.exist(item):
                check_result = item.AXValue
            if check_result == 'Mac AT Custom Profile':
                case.result = True
            else:
                case.result = False

        with uuid("cf0d42b3-134d-41a2-8ebb-2a0860bee865") as case:
            # [G34] Able to select video setting
            # to adjust the [G173] AVC MPEG-4 1280 x 720/24p (16Mbps)
            produce_page.local.quality_profile_setup.switch_to_video_tab()
            check_result_1 = produce_page.local.quality_profile_setup.set_video_profile(index_resolution=2, index_frame_rate=3, index_profile_type=2)
            check_result_2 = produce_page.local.quality_profile_setup.set_video_bitrate(16000)
            case.result = check_result_1 and check_result_2

        with uuid("8353988a-5468-4d08-bfec-8eb30d863235") as case:
            # [G35] Able to select audio setting
            # LPCM / Stereo / 1536Kbps
            produce_page.local.quality_profile_setup.switch_to_audio_tab()
            check_result = produce_page.local.quality_profile_setup.set_audio_profile(index_compression=2, index_channel=1, index_compression_rate=1)
            case.result = check_result

        with uuid("067bff63-3e2d-49d6-9376-8f7af7bae44f") as case:
            # [G38] Create a new profile > Click OK
            produce_page.local.quality_profile_setup.click_ok()
            time.sleep(DELAY_TIME)
            if not produce_page.find(L.produce.local.quality_profile_setup_dialog.audio.cbx_compression):
                case.result = True
            else:
                case.result = False

        with uuid("dbf90575-1100-4db7-8ec8-96e868e9be5b") as case:
            # [G43] Details
            verify_step1 = produce_page.local.click_details()
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=L.produce.local.details_dialog.main_window,
                                                      file_name=Auto_Ground_Truth_Folder + 'G43.png')
            verify_step2 = produce_page.compare(Ground_Truth_Folder + 'G43.png', current_image)
            case.result = verify_step1 and verify_step2

            produce_page.press_esc_key()

        with uuid("5ef29c34-d93a-4ae0-8b29-167fdda951cf") as case:
            # [G47] Unselect (SW encoder)
            produce_page.local.set_fast_video_rendering(is_checked=0)

            #verify
            item = produce_page.find(L.produce.local.chx_fast_video_rendering)
            check_result = -1
            if produce_page.exist(item):
                check_result = item.AXValue

            if check_result == 0:
                case.result = True
            else:
                case.result = False

        # G173 / G25 /G26 is group (M1 chip cannot run these cases)
        with uuid("ef26849d-bb22-4b9e-b180-a1c51d7c5883") as case:
            check_M1 = produce_page.is_apple_cpu()
            if check_M1:
                case.result = None
                case.fail_log = "Skip (M1 chip)"
            else:
                # [G173] AVC MPEG-4 1280 x 720/24p (16Mbps)

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
                time.sleep(DELAY_TIME * 3)

                # Verify : Can find the produced file in Media Room
                verify_step1 = main_page.select_library_icon_view_media(explore_file)

                # Verify 2 : Set timecode to (00:00:05:00)
                main_page.set_timeline_timecode('00_00_06_10', is_verify=False)
                current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                          file_name=Auto_Ground_Truth_Folder + 'G173.png')
                verify_step2 = produce_page.compare(Ground_Truth_Folder + 'G173.png', current_image)
                time.sleep(DELAY_TIME*2)
                case.result = verify_step1 and verify_step2
                # Remove the produced file
                main_page.select_library_icon_view_media(explore_file)
                media_room_page.library_clip_context_menu_move_to_trash_can()

        with uuid("6208d75c-efa3-4cef-81e1-227c627a1acc") as case:
            check_M1 = produce_page.is_apple_cpu()
            if check_M1:
                case.result = None
                case.fail_log = "Skip (M1 chip)"
            else:
                # [G25] Profile type > Default
                main_page.click_produce()
                produce_page.check_enter_produce_page()
                check_result = produce_page.local.select_profile_type('default')
                case.result = check_result

        with uuid("c8f4eb20-70c5-41d6-97b7-89101028cd63") as case:
            check_M1 = produce_page.is_apple_cpu()
            if check_M1:
                case.result = None
                case.fail_log = "Skip (M1 chip)"
            else:
                # [G26] Profile type > Default
                check_result = produce_page.local.select_profile_type('custom')
                case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_8(self):
        # 4:3 project
        main_page.set_project_aspect_ratio_4_3()

        # Insert Skateboard 03.mp4
        main_page.select_library_icon_view_media('Skateboard 03.mp4')
        media_room_page.library_clip_context_menu_insert_on_selected_track()

        # handle aspect ratio conflict
        main_page.handle_aspect_ratio_conflict()

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("b004050a-3c1e-433e-b165-0a2220d8f70e") as case:
            # [G252] 4:3 Project > M2TS > PAL > AVC 2K 2048 x 1536/25p (40Mbps)
            produce_page.local.select_file_extension('m2ts')
            time.sleep(DELAY_TIME)

            produce_page.local.select_country_video_format('pal')

            #AVC 2K 2048 x 1536/25p (40Mbps)
            Check_M1 = produce_page.is_apple_cpu()
            if Check_M1:
                produce_page.local.select_profile_name(1)
            else:
                produce_page.local.select_profile_name(3)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            logger(check_profile)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'AVC 2K 2048 x 1536/25p (40 Mb...':
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

            # Verify 2 : Set timecode to (00:00:09:16)
            main_page.set_timeline_timecode('00_00_09_16', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G252.png')
            verify_step2 = produce_page.compare(Ground_Truth_Folder + 'G252.png', current_image, similarity=0.97)
            time.sleep(DELAY_TIME*2)
            case.result = verify_step1 and verify_step2
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        with uuid("2de9f2e0-80bd-4571-a056-5331d874632d") as case:
            check_M1 = produce_page.is_apple_cpu()
            if check_M1:
                case.result = None
                case.fail_log = "Skip (M1 chip)"
            else:

                main_page.click_produce()
                # [G247] 4:3 Project > M2TS > NTSC > AVC 2K 2048 x 1536/60p (40Mbps)
                produce_page.local.select_file_extension('m2ts')
                time.sleep(DELAY_TIME)

                produce_page.local.select_country_video_format('ntsc')

                #AVC 2K 2048 x 1536/60p (40Mbps)
                produce_page.local.select_profile_name(4)
                time.sleep(DELAY_TIME)

                check_profile = produce_page.local.get_profile_name()
                logger(check_profile)

                check_profile = produce_page.local.get_profile_name()

                if check_profile != 'AVC 2K 2048 x 1536/60p (40 Mb...':
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

                # Verify 2 : Set timecode to (00:00:05:04)
                main_page.set_timeline_timecode('00_00_05_04', is_verify=False)
                current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                          file_name=Auto_Ground_Truth_Folder + 'G247.png')
                verify_step2 = produce_page.compare(Ground_Truth_Folder + 'G247.png', current_image, similarity=0.97)
                time.sleep(DELAY_TIME*2)
                case.result = verify_step1 and verify_step2
                # Remove the produced file
                main_page.select_library_icon_view_media(explore_file)
                media_room_page.library_clip_context_menu_move_to_trash_can()

        with uuid("1a49caf9-4243-4e02-a2db-c018aedac6ca") as case:
            check_M1 = produce_page.is_apple_cpu()
            if check_M1:
                case.result = None
                case.fail_log = "Skip (M1 chip)"
            else:

                main_page.select_library_icon_view_media('Mahoroba.mp3')
                tips_area_page.click_TipsArea_btn_insert(0)

                main_page.click_produce()

                # [G245] 4:3 Project > M2TS > NTSC > AVC 2K 2048 x 1536/30p (40Mbps)
                produce_page.local.select_file_extension('m2ts')
                time.sleep(DELAY_TIME)

                produce_page.local.select_country_video_format('ntsc')

                # AVC 2K 2048 x 1536/30p (40Mbps)
                produce_page.local.select_profile_name(3)
                time.sleep(DELAY_TIME)

                check_profile = produce_page.local.get_profile_name()
                logger(check_profile)

                check_profile = produce_page.local.get_profile_name()

                if check_profile != 'AVC 2K 2048 x 1536/30p (40 Mb...':
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

                # Verify 2 : Set timecode to (00:00:01:11)
                main_page.set_timeline_timecode('00_00_01_11', is_verify=False)
                current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                          file_name=Auto_Ground_Truth_Folder + 'G245.png')
                verify_step2 = produce_page.compare(Ground_Truth_Folder + 'G245.png', current_image)
                time.sleep(DELAY_TIME*2)
                case.result = verify_step1 and verify_step2
                # Remove the produced file
                main_page.select_library_icon_view_media(explore_file)
                media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_9(self):
        # Open project
        main_page.top_menu_bar_file_open_project()
        project_path = Test_Material_Folder + 'Produce_Local/AVC_MKV.pds'
        main_page.handle_open_project_dialog(project_path)

        # handle open project > don't show again
        self.check_dont_show_again_dialog(tick=0)

        # 4:3 project
        main_page.set_project_aspect_ratio_4_3()

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("07dc7804-1197-4b5d-8423-54f1754208ff") as case:
            # [G256] 4:3 Project > MP4 > NTSC > MPEG-4 640 x 480/30p (6Mbps)
            produce_page.local.select_file_extension('mp4')
            time.sleep(DELAY_TIME)

            produce_page.local.select_country_video_format('ntsc')

            # 640 x 480/30p (6Mbps)
            produce_page.local.select_profile_name(2)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            logger(check_profile)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 640 x 480/30p (6 Mbps)':
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

            # Verify :  Media Room > Right Click Menu > Check View Properties
            main_page.select_library_icon_view_media('Landscape 02.jpg')
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media(explore_file)
            main_page.right_click()
            main_page.select_right_click_menu('View Properties')
            time.sleep(DELAY_TIME*2)
            current_image = produce_page.snapshot(locator=L.media_room.properties_dialog.main_window,
                                                      file_name=Auto_Ground_Truth_Folder + 'G256.png')
            verify_step1 = produce_page.compare(Ground_Truth_Folder + 'G256.png', current_image)
            time.sleep(DELAY_TIME)
            # close View Properties
            main_page.exist_click(L.media_room.properties_dialog.btn_close)
            time.sleep(DELAY_TIME)

            #Verify: check preview
            main_page.set_timeline_timecode('00_00_25_29', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G256_preview.png')
            verify_step2 = produce_page.compare(Ground_Truth_Folder + 'G256_preview.png', current_image, similarity=0.97)
            case.result = verify_step1 and verify_step2
            logger(verify_step1)
            logger(verify_step2)
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("ece47fd2-23c0-4114-ad35-69439a514068") as case:
            # [G257] 4:3 Project > MP4 > NTSC > MPEG-4 640 x 480/24p (6Mbps)
            produce_page.local.select_file_extension('mp4')
            time.sleep(DELAY_TIME)

            produce_page.local.select_country_video_format('ntsc')

            # MPEG-4 640 x 480/24p (6Mbps)
            produce_page.local.select_profile_name(1)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            logger(check_profile)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 640 x 480/24p (6 Mbps)':
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

            # Verify : check preview
            main_page.select_library_icon_view_media('Landscape 02.jpg')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.set_timeline_timecode('00_00_16_13', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G257_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G257_preview.png', current_image, similarity=0.97)
            case.result = verify_step
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("a19f12ee-d0ec-4db5-aa52-adf42fe0e982") as case:
            # [G258] 4:3 Project > MP4 > MPEG-4 2K 2048 x 1536/30p (40Mbps)
            produce_page.local.select_file_extension('mp4')
            time.sleep(DELAY_TIME)

            produce_page.local.select_country_video_format('ntsc')

            # MPEG-4 2K 2048 x 1536/30p (40Mbps)
            produce_page.local.select_profile_name(3)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            logger(check_profile)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 2K 2048 x 1536/30p (40...':
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

            # Verify : check preview
            main_page.select_library_icon_view_media('Landscape 02.jpg')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 5)
            main_page.press_space_key()
            main_page.set_timeline_timecode('00_00_14_00', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G258_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G258_preview.png', current_image, similarity=0.97)
            case.result = verify_step
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_10(self):
        main_page.select_library_icon_view_media('Landscape 02.jpg')
        media_room_page.library_clip_context_menu_insert_on_selected_track()
        main_page.select_library_icon_view_media('Speaking Out.mp3')
        media_room_page.library_clip_context_menu_insert_on_selected_track()

        main_page.enter_room(1)
        time.sleep(DELAY_TIME)
        main_page.drag_media_to_timeline_playhead_position(name='Motion Graphics 007', track_no=2)

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("8ad81e07-cda6-4e69-b209-f7b3ed479fb4") as case:
            # [G225] 16:9 Project > MKV > PAL > AVC 1280 x 720/50p (24Mbps)
            produce_page.local.select_file_extension('mkv')
            time.sleep(DELAY_TIME)

            produce_page.local.select_country_video_format('pal')

            # AVC 1280 x 720/50p (24Mbps)
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
            for x in range(50):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # Verify : check preview
            main_page.select_library_icon_view_media('Landscape 02.jpg')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 2)
            main_page.press_space_key()
            main_page.set_timeline_timecode('00_00_04_00', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G225_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G225_preview.png', current_image, similarity=0.97)
            case.result = verify_step
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("90a4b21f-bf6e-463d-899c-5804a6b07d81") as case:
            # [G230] 16:9 Project > MKV > PAL > AVC 1440 x 1080/50p (28Mbps)
            produce_page.local.select_file_extension('mkv')
            time.sleep(DELAY_TIME)

            produce_page.local.select_country_video_format('pal')

            # AVC AVC 1440 x 1080/50p (28Mbps)
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

            # Verify : check preview
            main_page.select_library_icon_view_media('Landscape 02.jpg')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.set_timeline_timecode('00_00_02_15', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G230_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G230_preview.png', current_image, similarity=0.97)
            case.result = verify_step
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()
        
        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("2ed6d6ff-776e-4b97-98f3-8cb6cfb4d3bf") as case:
            # [G214] 16:9 Project > MKV > NTSC > AVC 1920 x 1080/60p (28Mbps)
            produce_page.local.select_file_extension('mkv')
            time.sleep(DELAY_TIME)

            produce_page.local.select_country_video_format('ntsc')

            # AVC 1920 x 1080/60p (28Mbps)
            produce_page.local.select_profile_name(9)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            logger(check_profile)
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

            # Verify : check preview
            main_page.select_library_icon_view_media('Landscape 02.jpg')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.right_click()
            main_page.select_right_click_menu('View Properties')
            time.sleep(DELAY_TIME*2)
            current_image = produce_page.snapshot(locator=L.media_room.properties_dialog.main_window,
                                                      file_name=Auto_Ground_Truth_Folder + 'G214.png')
            verify_step1 = produce_page.compare(Ground_Truth_Folder + 'G214.png', current_image, similarity=0.9)
            time.sleep(DELAY_TIME)
            # close View Properties
            main_page.exist_click(L.media_room.properties_dialog.btn_close)
            time.sleep(DELAY_TIME)

            #Verify: check preview
            main_page.set_timeline_timecode('00_00_05_27', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G214_preview.png')
            verify_step2 = produce_page.compare(Ground_Truth_Folder + 'G214_preview.png', current_image, similarity=0.97)
            case.result = verify_step1 and verify_step2
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_11(self):
        # 2
        # Open project
        main_page.top_menu_bar_file_open_project()
        project_path = Test_Material_Folder + 'Produce_Local/AVC_MKV.pds'
        main_page.handle_open_project_dialog(project_path)

        # handle open project > don't show again
        self.check_dont_show_again_dialog(tick=0)

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("765a1a0b-b374-4bcd-958e-0c89997de8e8") as case:
            # [G216] 16:9 Project > MKV > NTSC > AVC 2K 2048 x 1080/30p (40Mbps)
            produce_page.local.select_file_extension('mkv')
            time.sleep(DELAY_TIME)

            produce_page.local.select_country_video_format('ntsc')

            # AVC 2K 2048 x 1080/30p (40Mbps)
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
            time.sleep(DELAY_TIME * 2)

            # Verify : check preview
            main_page.select_library_icon_view_media('Landscape 02.jpg')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.set_timeline_timecode('00_00_06_17', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G216_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G216_preview.png', current_image, similarity=0.97)
            case.result = verify_step
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("e48b254c-d6cd-495c-90c7-63494ae63a33") as case:
            # [G219] 16:9 Project > MKV > NTSC > AVC 4K 3840 x 2160/30p (50Mbps)
            produce_page.local.select_file_extension('mkv')
            time.sleep(DELAY_TIME)

            produce_page.local.select_country_video_format('ntsc')

            # AVC 4K 3840 x 2160/30p (50Mbps)
            produce_page.local.select_profile_name(13)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'AVC 4K 3840 x 2160/30p (50 Mb...':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            for x in range(200):
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

            # Verify : check preview
            main_page.select_library_icon_view_media('Landscape 02.jpg')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.set_timeline_timecode('00_00_10_19', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G219_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G219_preview.png', current_image, similarity=0.97)
            case.result = verify_step
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_12(self):
        # 4
        # Open project
        main_page.top_menu_bar_file_open_project()
        project_path = Test_Material_Folder + 'Produce_Local/Test_A.pds'
        main_page.handle_open_project_dialog(project_path)

        # handle open project
        self.check_dont_show_again_dialog(tick=0)
        # handle high_definition_video_confirm_dialog_click_no
        self.check_dont_show_again_dialog(tick=0)

        main_page.click_produce()

        # click XAVC S
        produce_page.local.select_file_format(container='xavc_s')

        with uuid("d48a8125-687f-4519-bf7f-7c6a711e572e") as case:
            # [G115] 16:9 Project > PAL > XAVC S 1280x720/25p (17Mbps)

            produce_page.local.select_country_video_format('pal')
            # select profile name
            produce_page.local.select_profile_name(2)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'XAVC S 1280 x 720/25p (17 Mbps)':
                logger('Check profile setting error')
                raise Exception
            else:
                pass
            logger('pass')

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

            # Verify : check preview
            main_page.select_library_icon_view_media('Landscape 02.jpg')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.set_timeline_timecode('00_00_02_18', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G115_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G115_preview.png', current_image)
            case.result = verify_step
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()
        
        main_page.click_produce()

        with uuid("7166ed5f-4763-4a13-9b89-47260e64d348") as case:
            # [G118] 16:9 Project > PAL > XAVC S 1920x1080/25p (17Mbps)

            produce_page.local.select_country_video_format('pal')
            # select profile name
            produce_page.local.select_profile_name(5)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'XAVC S 1920 x 1080/25p (17 Mbps)':
                logger('Check profile setting error')
                raise Exception
            else:
                pass
            logger('pass')

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
            time.sleep(DELAY_TIME * 2)

            # Verify : check preview
            main_page.select_library_icon_view_media('Sport 01.jpg')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.set_timeline_timecode('00_00_04_10', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G118_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G118_preview.png', current_image)
            case.result = verify_step
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        main_page.click_produce()
        with uuid("1460b520-7277-4c15-9189-819a3928b63c") as case:
            # [G122] 16:9 Project > PAL > XAVC S 3840x2160/50p (60Mbps)

            produce_page.local.select_country_video_format('pal')
            # select profile name
            produce_page.local.select_profile_name(9)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'XAVC S 3840 x 2160/50p (60 Mb...':
                logger(check_profile)
                logger('Check profile setting error')
                raise Exception
            else:
                pass
            logger('pass')

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
            time.sleep(DELAY_TIME * 2)

            # Verify : check preview
            main_page.select_library_icon_view_media('Sport 02.jpg')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 5)
            main_page.press_space_key()
            main_page.set_timeline_timecode('00_00_11_07', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G122_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G122_preview.png', current_image)
            case.result = verify_step
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()
        
        main_page.click_produce()

        with uuid("9e5f13ed-18ff-458d-853e-37f08e40bf9e") as case:
            # [G133] 16:9 Project > M2TS > NTSC > AVC 1280 x 720/60p (24Mbps)

            # click AVC
            produce_page.local.select_file_format(container='avc')

            produce_page.local.select_country_video_format('ntsc')

            produce_page.local.select_file_extension('m2ts')
            time.sleep(DELAY_TIME)

            # select profile name
            produce_page.local.select_profile_name(4)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'AVC 1280 x 720/60p (24 Mbps)':
                logger('Check profile setting error')
                raise Exception
            else:
                pass
            logger('pass')

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

            # Verify : check preview
            main_page.select_library_icon_view_media('Travel 02.jpg')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.set_timeline_timecode('00_00_13_28', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G133_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G133_preview.png', current_image)
            case.result = verify_step
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_13(self):
        main_page.select_library_icon_view_media('Skateboard 02.mp4')
        media_room_page.library_clip_context_menu_insert_on_selected_track()

        main_page.enter_room(1)
        time.sleep(DELAY_TIME)
        media_room_page.select_LibraryRoom_category('General')
        main_page.drag_media_to_timeline_playhead_position(name='Radar', track_no=2)

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("a457287d-9e46-4ab4-bb60-697b1aea802a") as case:
            # [G49] Fast video rendering technology > Hardware video encoder
            check_result = produce_page.local.set_fast_video_rendering_hardware_encode()

            #verify : Check hard code value
            item = produce_page.exist(L.produce.local.rdb_fast_video_rendering_hardware_encode)
            check_value = item.AXValue

            case.result = check_result and check_value

        with uuid("94f0e209-321b-4305-8aeb-ca541a4fbc4b") as case:
            # [G63] Preview Panel > Next Frame
            for x in range(10):
                produce_page.click_preview_operation(operation='next_frame')
                time.sleep(DELAY_TIME)

            timecode_result = produce_page.get_preview_timecode()
            if timecode_result == '00_00_00_10':
                check_timecode = True
            else:
                check_timecode = False
            current_image = produce_page.snapshot(locator=L.base.main_window,
                                                  file_name=Auto_Ground_Truth_Folder + 'G63.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G63.png', current_image)
            case.result = check_timecode and verify_step

        with uuid("556e0f56-961b-492a-b631-9c8924571978") as case:
            # [65] Timecode > Display
            with uuid("c73a2f45-45c2-42ce-ab12-fcfe5b2dfb73") as case:
                # [G61] Preview Panel > Stop
                produce_page.click_preview_operation(operation='stop')
                time.sleep(DELAY_TIME)

                timecode_result = produce_page.get_preview_timecode()
                if timecode_result == '00_00_00_00':
                    case.result = True
                else:
                    case.result = False

            if timecode_result == '00_00_00_00':
                case.result = True
            else:
                case.result = False

        with uuid("5bea2f93-8a0a-4a9d-9262-d280ed0dd7c7") as case:
            # [G323] 16:9 Project > M2TS > NTSC > HEVC 720x576/24p (6Mbps)
            produce_page.local.select_file_format(container='hevc')
            produce_page.local.select_country_video_format('ntsc')
            produce_page.local.select_file_extension('m2ts')
            time.sleep(DELAY_TIME)

            # select profile name
            produce_page.local.select_profile_name(2)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'HEVC 720 x 576/24p (6 Mbps)':
                logger(check_profile)
                logger('Check profile setting error')
                raise Exception
            else:
                pass
            logger('pass')

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            with uuid("24786966-9daa-43dd-8c9a-537310f62109") as case:
                # [G51] Surround sound > AAC 5.1 > Disable/Hide
                if not produce_page.is_exist(L.produce.local.rdb_surround_sound_ac51):
                    case.result = True
                else:
                    case.result = False

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

            # Verify : check preview
            main_page.select_library_icon_view_media('Travel 02.jpg')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.set_timeline_timecode('00_00_01_15', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G323_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G323_preview.png', current_image)
            case.result = verify_step
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_14(self):
        main_page.select_library_icon_view_media('Speaking Out.mp3')
        tips_area_page.click_TipsArea_btn_insert()
        main_page.enter_room(4)
        time.sleep(DELAY_TIME)
        media_room_page.select_LibraryRoom_category('General')
        time.sleep(1)
        main_page.select_library_icon_view_media('Dialog_03')
        tips_area_page.click_TipsArea_btn_insert()
        media_room_page.select_LibraryRoom_category('Romance')
        main_page.drag_media_to_timeline_playhead_position(name='Wedding 2', track_no=2)

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("84ef764f-5770-419c-a3c1-f5aefa161b54") as case:
            # [G324] 16:9 Project > M2TS > NTSC > HEVC 1280x720/24p (7Mbps)
            produce_page.local.select_file_format(container='hevc')
            produce_page.local.select_country_video_format('ntsc')
            produce_page.local.select_file_extension('m2ts')
            time.sleep(DELAY_TIME)

            # select profile name
            produce_page.local.select_profile_name(3)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'HEVC 1280 x 720/24p (7 Mbps)':
                logger(check_profile)
                logger('Check profile setting error')
                raise Exception
            else:
                pass
            logger('pass')

            with uuid("b607089d-a14c-4518-8608-2cf03875540b") as case:
                # [G55] Surround sound > TrueTheater Surround > Theater
                produce_page.local.set_surround_sound()
                check_result = produce_page.local.set_surround_sound_true_theater_option_theater()

                # verify step
                produce_page.exist_click(L.produce.local.btn_surround_sound_true_theater_dialog)
                item = produce_page.exist(L.produce.local.true_theater_settings_dialog.rdb_theater)
                check_value = item.AXValue
                case.result = check_value
                time.sleep(DELAY_TIME)
                produce_page.exist_click(L.produce.local.true_theater_settings_dialog.btn_ok)
                time.sleep(DELAY_TIME)

            # Start : produce
            produce_page.click_start()
            for x in range(50):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # Verify : check preview
            main_page.select_library_icon_view_media('Food.jpg')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.set_timeline_timecode('00_00_01_29', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G324_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G324_preview.png', current_image)
            case.result = verify_step
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        with uuid("01644599-5868-4d45-9365-2334063f7900") as case:
            # [G279] 9:16 Project > MP4 > NTSC > MPEG-4 720 x 1280/30p (6Mbps)
            main_page.set_project_aspect_ratio_9_16()

            main_page.click_produce()
            produce_page.check_enter_produce_page()

            produce_page.local.select_file_format(container='avc')
            produce_page.local.select_country_video_format('ntsc')
            produce_page.local.select_file_extension('mp4')
            time.sleep(DELAY_TIME)

            # select profile name
            produce_page.local.select_profile_name(2)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 720 x 1280/30p (6 Mbps)':
                logger(check_profile)
                logger('Check profile setting error')
                raise Exception
            else:
                pass
            logger('pass')

            with uuid("dc542386-76c8-463f-9823-fdfaf9ff0e9b") as case:
                # [G66] Timecode > Input
                produce_page.local.set_preview_timecode('00_00_02_05')
                time.sleep(DELAY_TIME)
                timecode_result = produce_page.get_preview_timecode()
                if timecode_result == '00_00_02_05':
                    check_timecode = True
                else:
                    check_timecode = False

                current_image = produce_page.snapshot(locator=L.base.main_window,
                                                      file_name=Auto_Ground_Truth_Folder + 'G66.png')
                verify_step = produce_page.compare(Ground_Truth_Folder + 'G66.png', current_image)

                case.result = check_timecode and verify_step


            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            for x in range(80):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # Verify : check preview
            main_page.select_library_icon_view_media('Food.jpg')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.set_timeline_timecode('00_00_01_04', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G279_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G279_preview.png', current_image)
            case.result = verify_step
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_15(self):
        main_page.set_project_aspect_ratio_9_16()
        main_page.select_library_icon_view_media('Skateboard 02.mp4')
        # Insert to timeline
        tips_area_page.exist_click(L.main.tips_area.btn_insert_to_selected_track)
        # handle aspect ratio conflict
        main_page.handle_aspect_ratio_conflict()

        time.sleep(DELAY_TIME)
        main_page.enter_room(4)
        time.sleep(DELAY_TIME)
        media_room_page.select_LibraryRoom_category('Romance')
        main_page.drag_media_to_timeline_playhead_position(name='Wedding 2', track_no=2)

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("e11393b5-b58e-4555-b745-fc3df402c683") as case:
            # [G282] 9:16 Project > MP4 > NTSC > MPEG-4 720 x 1280/240p (45Mbps)
            produce_page.local.select_file_format(container='avc')
            produce_page.local.select_country_video_format('ntsc')
            produce_page.local.select_file_extension('mp4')
            time.sleep(DELAY_TIME)

            # select profile name
            produce_page.local.select_profile_name(5)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 720 x 1280/240p (45 Mb...':
                logger(check_profile)
                logger('Check profile setting error')
                raise Exception
            else:
                pass
            logger('pass')

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            for x in range(80):
                check_result = produce_page.check_produce_complete()
                if check_result is True:
                    break
                else:
                    time.sleep(DELAY_TIME)

            with uuid("f7d3e9e5-c299-47bb-b7c5-cefd7ed3dad6") as case:
                # [G99] [Complete] stage > Back to previous page
                check_result_1 = produce_page.click_previous()
                time.sleep(DELAY_TIME)
                check_result_2 = produce_page.click_edit()
                case.result = check_result_1 and check_result_2
                time.sleep(DELAY_TIME * 2)

            # Verify : check preview
            main_page.select_library_icon_view_media('Food.jpg')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.set_timeline_timecode('00_00_04_16', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G282_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G282_preview.png', current_image, similarity=0.98)
            case.result = verify_step
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        with uuid("81573ebb-5ff8-4a16-8572-feb92d3dfaa4") as case:
            # [G284] 9:16 Project > MP4 > NTSC > MPEG-4 1080 x 1920/60p (25Mbps)
            main_page.click_produce()
            produce_page.check_enter_produce_page()

            produce_page.local.select_file_format(container='avc')
            produce_page.local.select_country_video_format('ntsc')
            produce_page.local.select_file_extension('mp4')
            time.sleep(DELAY_TIME)

            # select profile name
            produce_page.local.select_profile_name(7)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 1080 x 1920/60p (25 Mb...':
                logger(check_profile)
                logger('Check profile setting error')
                raise Exception
            else:
                pass
            logger('pass')

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
            for x in range(80):
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

            # Verify :  Media Room > Right Click Menu > Check View Properties
            main_page.select_library_icon_view_media('Landscape 02.jpg')
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media(explore_file)
            main_page.right_click()
            main_page.select_right_click_menu('View Properties')
            time.sleep(DELAY_TIME*2)
            current_image = produce_page.snapshot(locator=L.media_room.properties_dialog.main_window,
                                                      file_name=Auto_Ground_Truth_Folder + 'G284.png')
            verify_step1 = produce_page.compare(Ground_Truth_Folder + 'G284.png', current_image, similarity=0.94)
            time.sleep(DELAY_TIME)
            # close View Properties
            main_page.exist_click(L.media_room.properties_dialog.btn_close)
            time.sleep(DELAY_TIME)

            # Verify : check preview
            main_page.select_library_icon_view_media(explore_file)
            main_page.set_timeline_timecode('00_00_03_10', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G284_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G284_preview.png', current_image, similarity=0.98)
            case.result = verify_step
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("51ed6db4-f760-4c76-9d42-bcfc46e53503") as case:
            # [G286] 9:16 Project > MP4 > NTSC > MPEG-4 1080 x 1920/240p (90Mbps)
            produce_page.local.select_file_format(container='avc')
            produce_page.local.select_country_video_format('ntsc')
            produce_page.local.select_file_extension('mp4')
            time.sleep(DELAY_TIME)

            # select profile name
            produce_page.local.select_profile_name(9)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 1080 x 1920/240p (90 M...':
                logger(check_profile)
                logger('Check profile setting error')
                raise Exception
            else:
                pass
            logger('pass')

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
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
            time.sleep(DELAY_TIME * 2)

            # Verify : check preview
            main_page.select_library_icon_view_media('Food.jpg')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.set_timeline_timecode('00_00_01_19', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G286_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G286_preview.png', current_image, similarity=0.98)
            case.result = verify_step
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_16(self):
        # Open project
        main_page.top_menu_bar_file_open_project()
        project_path = Test_Material_Folder + 'Produce_Local/Test_A.pds'
        main_page.handle_open_project_dialog(project_path)

        # handle open project
        self.check_dont_show_again_dialog(tick=0)
        # handle high_definition_video_confirm_dialog_click_no
        self.check_dont_show_again_dialog(tick=0)

        main_page.set_project_aspect_ratio_9_16()

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("d5689da8-2f89-472e-bdd1-aad00d65a497") as case:
            # [G288] 9:16 Project > MP4 > NTSC > MPEG-4 2160 x 3840/30p (40Mbps)
            produce_page.local.select_file_format(container='avc')
            produce_page.local.select_country_video_format('ntsc')
            produce_page.local.select_file_extension('mp4')
            time.sleep(DELAY_TIME)

            # select profile name
            produce_page.local.select_profile_name(11)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 4K 2160 x 3840/30p (40...':
                logger(check_profile)
                logger('Check profile setting error')
                raise Exception
            else:
                pass
            logger('pass')

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
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
            time.sleep(DELAY_TIME * 2)

            # Verify : check preview
            main_page.select_library_icon_view_media('Food.jpg')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.set_timeline_timecode('00_00_02_25', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G288_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G288_preview.png', current_image, similarity=0.98)
            case.result = verify_step
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        with uuid("0c40b144-3766-4fd1-a5ac-f3fefc920614") as case:
            # [G305] 1:1 Project > MP4 > NTSC > MPEG-4 720x720/30p (6Mbps)
            main_page.set_project_aspect_ratio_1_1()

            main_page.click_produce()
            produce_page.check_enter_produce_page()

            produce_page.local.select_file_format(container='avc')
            produce_page.local.select_country_video_format('ntsc')
            produce_page.local.select_file_extension('mp4')
            time.sleep(DELAY_TIME)

            # select profile name
            produce_page.local.select_profile_name(4)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 720 x 720/30p (6 Mbps)':
                logger(check_profile)
                logger('Check profile setting error')
                raise Exception
            else:
                pass
            logger('pass')

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
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
            time.sleep(DELAY_TIME * 2)

            # Verify : check preview
            main_page.select_library_icon_view_media('Food.jpg')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.set_timeline_timecode('00_00_10_23', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G305_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G305_preview.png', current_image, similarity=0.98)
            case.result = verify_step
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_17(self):
        main_page.set_project_aspect_ratio_1_1()

        main_page.enter_room(1)
        time.sleep(DELAY_TIME)
        media_room_page.select_LibraryRoom_category('General')
        main_page.select_library_icon_view_media('Clover_03')
        main_page.right_click()
        main_page.select_right_click_menu('Add to Timeline')

        main_page.drag_media_to_timeline_playhead_position(name='Radar', track_no=2)

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("1921a067-9f0a-40a6-ae88-53b396d25b8d") as case:
            # [85] Upload a copy to cyberlink Cloud > Unselect (default)
            #L.produce.local.chx_upload_copy_to_cyberlink_cloud
            if produce_page.local.check_visible_upload_copy_to_cyberlink_cloud():
                item = produce_page.find(L.produce.local.chx_upload_copy_to_cyberlink_cloud)
                case.result = not(item.AXValue)
            else:
                logger('Cannot find locator of [Upload a copy to cyberlink Cloud]')
                raise Exception

        with uuid("8bd5d2af-1f4e-4f8d-9fbf-9497197b4ad5") as case:
            # [G306] 1:1 Project > MP4 > NTSC > MPEG-4 1080x1080/24p (12Mbps)
            produce_page.local.select_file_format(container='avc')
            produce_page.local.select_country_video_format('ntsc')
            produce_page.local.select_file_extension('mp4')
            time.sleep(DELAY_TIME)

            # select profile name
            produce_page.local.select_profile_name(5)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 1080 x 1080/24p (12 Mb...':
                logger(check_profile)
                logger('Check profile setting error')
                raise Exception
            else:
                pass
            logger('pass')

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
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
            time.sleep(DELAY_TIME * 2)

            # Verify : check preview
            main_page.select_library_icon_view_media('Food.jpg')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.set_timeline_timecode('00_00_07_23', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G306_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G306_preview.png', current_image, similarity=0.98)
            case.result = verify_step
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        main_page.click_produce()
        produce_page.check_enter_produce_page()
        with uuid("08a09c31-f00c-42f7-9797-38f81b591e41") as case:
            # [G309] 1:1 Project > MP4 > NTSC > MPEG-4 1440x1440/30p (16Mbps)

            produce_page.local.select_file_format(container='avc')
            produce_page.local.select_country_video_format('ntsc')
            produce_page.local.select_file_extension('mp4')
            time.sleep(DELAY_TIME)

            # select profile name
            produce_page.local.select_profile_name(8)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 1440 x 1440/30p (16 Mb...':
                logger(check_profile)
                logger('Check profile setting error')
                raise Exception
            else:
                pass
            logger('pass')

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
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
            time.sleep(DELAY_TIME * 2)

            # Verify : check preview
            main_page.select_library_icon_view_media('Food.jpg')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.set_timeline_timecode('00_00_06_19', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G309_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G309_preview.png', current_image, similarity=0.98)
            case.result = verify_step
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("0eb97a38-88db-47a2-9320-d1c551c8c11b") as case:
            # [G311] 1:1 Project > MP4 > NTSC > MPEG-4 2160x2160/30p (40Mbps)
            produce_page.local.select_file_format(container='avc')
            produce_page.local.select_country_video_format('ntsc')
            produce_page.local.select_file_extension('mp4')
            time.sleep(DELAY_TIME)

            # select profile name
            produce_page.local.select_profile_name(10)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 2K 2160 x 2160/30p (40 ...':
                logger(check_profile)
                logger('Check profile setting error')
                raise Exception
            else:
                pass
            logger('pass')

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
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
            time.sleep(DELAY_TIME * 2)

            # Verify : check preview
            main_page.select_library_icon_view_media('Food.jpg')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.set_timeline_timecode('00_00_08_04', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G311_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G311_preview.png', current_image, similarity=0.98)
            case.result = verify_step
            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_18(self):

        main_page.select_library_icon_view_media('Skateboard 03.mp4')
        # Insert to timeline
        tips_area_page.exist_click(L.main.tips_area.btn_insert_to_selected_track)

        time.sleep(DELAY_TIME)
        main_page.enter_room(3)
        time.sleep(DELAY_TIME)
        main_page.select_library_icon_view_media('Band Noise')
        main_page.right_click()
        main_page.select_right_click_menu('Add to Timeline')

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("62cab236-08fe-4a5c-83f7-b93fd1800895") as case:
            # [G344] 16:9 Project > HEVC > MP4 > NTSC > MPEG-4 1920 x 1080/24p (11Mbps)
            produce_page.local.select_file_format(container='hevc')
            produce_page.local.select_country_video_format('ntsc')
            produce_page.local.select_file_extension('mp4')
            time.sleep(DELAY_TIME)

            # select profile name
            produce_page.local.select_profile_name(5)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 1920 x 1080/24p (11 Mb...':
                logger(check_profile)
                logger('Check profile setting error')
                raise Exception
            else:
                pass
            logger('pass')

            with uuid("f9966ce8-aa03-4f2c-a69c-2132dc445f25") as case:
            # [G50] Surround sound > Enable AAC 5.1
                produce_page.local.set_surround_sound()
                check_result = produce_page.local.set_surround_sound_aac51()

                # verify step
                item = produce_page.exist(L.produce.local.rdb_surround_sound_ac51)
                check_value = item.AXValue
                case.result = check_value and check_result
                time.sleep(DELAY_TIME)

            # Get produced file name
            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
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
            time.sleep(DELAY_TIME * 2)

            # Verify : check preview
            main_page.select_library_icon_view_media('Mahoroba.mp3')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.set_timeline_timecode('00_00_02_22', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G344_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G344_preview.png', current_image, similarity=0.98)
            case.result = verify_step

        with uuid("5644926e-35fe-4c71-86df-9c1831ca4ecf") as case:
            # [G14] Intelligent SVRT > Source format > HEVC MP4
            timeline_page.drag_timeline_vertical_scroll_bar(0)
            main_page.timeline_select_track(track_no=1)
            main_page.select_library_icon_view_media(explore_file)
            main_page.tips_area_insert_media_to_selected_track(option=0)
            time.sleep(DELAY_TIME)

            main_page.click_produce()
            produce_page.check_enter_produce_page()

            produce_page.local.click_profile_analyzer()
            time.sleep(DELAY_TIME*5)
            check_profile_name = produce_page.local.profile_analyzer.get_profile_name(index=1)
            logger(check_profile_name)
            if check_profile_name == 'MPEG-4 1920 x 1080/24p (11 Mbps)':
                case.result = True
            else:
                case.result = False
                logger('Current profile is '+ check_profile_name)

        with uuid("c1676a2b-b78d-46b0-8a20-afe123e1283d") as case:
            # [G23] Control buttons > OK
            produce_page.local.profile_analyzer.click_ok()
            check_result = produce_page.is_exist(L.produce.local.profile_analyzer.unit_table_row)
            case.result = not (check_result)

        with uuid("9004c39c-f9d3-4bbe-bc31-fbdd27288330") as case:
            # [G48] Fast video rendering technology > Enable SVRT
            produce_page.local.set_fast_video_rendering_svrt()
            check_set_result = produce_page.local.get_fast_video_rendering_svrt_status()

            explore_file_2 = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
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
            time.sleep(DELAY_TIME * 2)

            # Verify : check preview
            main_page.select_library_icon_view_media('Mahoroba.mp3')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file_2)
            main_page.set_timeline_timecode('00_00_04_08', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G48_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G48_preview.png', current_image, similarity=0.98)
            case.result = verify_step and check_set_result

        # Remove the produced file
        main_page.select_library_icon_view_media(explore_file)
        media_room_page.library_clip_context_menu_move_to_trash_can()
        main_page.select_library_icon_view_media(explore_file_2)
        media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_19(self):

        main_page.select_library_icon_view_media('Skateboard 02.mp4')
        # Insert to timeline
        tips_area_page.exist_click(L.main.tips_area.btn_insert_to_selected_track)

        time.sleep(DELAY_TIME)
        main_page.enter_room(3)
        time.sleep(DELAY_TIME)
        main_page.select_library_icon_view_media('Abstractionism')
        main_page.right_click()
        main_page.select_right_click_menu('Add to Timeline')

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("d6405d64-8022-47d5-a401-b74ea3699da0") as case:
            # [G62] Preview Panel > Buttons > Previous Frame
            produce_page.local.set_preview_timecode('00_00_02_00')
            time.sleep(DELAY_TIME)

            for x in range(10):
                produce_page.click_preview_operation(operation='previous_frame')
                time.sleep(DELAY_TIME)

            timecode_result = produce_page.get_preview_timecode()
            if timecode_result == '00_00_01_20':
                check_timecode = True
            else:
                check_timecode = False
            current_image = produce_page.snapshot(locator=L.base.main_window,
                                                  file_name=Auto_Ground_Truth_Folder + 'G62.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G62.png', current_image)
            case.result = check_timecode and verify_step

        with uuid("9167698f-47c2-461b-876f-25e2edc90b85") as case:
            # [G28] File extension > Enable H264
            check_result = produce_page.local.select_file_format(container='avc')
            case.result = check_result
        with uuid("b4b038f9-9514-459e-8734-f4f665bb570d") as case:
            # [G134] H264 > 16:9 > M2TS > NTSC > AVC 1280 x 720/120p (40Mbps)
            produce_page.local.select_file_extension('m2ts')
            time.sleep(DELAY_TIME)

            produce_page.local.select_country_video_format('ntsc')

            time.sleep(DELAY_TIME)

            # select profile name
            produce_page.local.select_profile_name(5)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'AVC 1280 x 720/120p (40 Mbps)':
                logger(check_profile)
                logger('Check profile setting error')
                raise Exception
            else:
                pass
            logger('pass')

            explore_file = produce_page.get_produced_filename()

            with uuid("c35c4a03-d454-4cfc-9574-d3aa228bba33") as case:
                # [G56] Surround sound > TrueTheater Surround > Stadium
                produce_page.local.set_surround_sound()
                check_result = produce_page.local.set_surround_sound_true_theater_option_stadium()

                # verify step
                produce_page.exist_click(L.produce.local.btn_surround_sound_true_theater_dialog)
                item = produce_page.exist(L.produce.local.true_theater_settings_dialog.rdb_stadium)
                check_value = item.AXValue
                case.result = check_value and check_result
                time.sleep(DELAY_TIME)
                produce_page.exist_click(L.produce.local.true_theater_settings_dialog.btn_ok)
                time.sleep(DELAY_TIME)

            # Start : produce
            produce_page.click_start()
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
            #self.check_dont_show_again_dialog(tick=0)
            #time.sleep(DELAY_TIME * 2)

            # Verify : check preview
            main_page.select_library_icon_view_media('Mahoroba.mp3')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.set_timeline_timecode('00_00_04_00', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G134_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G134_preview.png', current_image, similarity=0.98)
            case.result = verify_step

        # Remove the produced file
        main_page.select_library_icon_view_media(explore_file)
        media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_20(self):

        main_page.select_library_icon_view_media('Skateboard 03.mp4')
        # Insert to timeline
        tips_area_page.exist_click(L.main.tips_area.btn_insert_to_selected_track)

        time.sleep(DELAY_TIME)
        main_page.enter_room(3)
        time.sleep(DELAY_TIME)
        main_page.select_library_icon_view_media('Back Light')
        main_page.right_click()
        main_page.select_right_click_menu('Add to Timeline')

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        # [G109] XAVCS > 16:9 > NTSC (MP4) > XAVC S 1920x1080/30p (17Mbps)
        # click XAVC S
        produce_page.local.select_file_format(container='xavc_s')

        produce_page.local.select_country_video_format('ntsc')
        # select profile name
        produce_page.local.select_profile_name(5)
        time.sleep(DELAY_TIME)

        check_profile = produce_page.local.get_profile_name()
        logger(check_profile)
        if check_profile != 'XAVC S 1920 x 1080/30p (17 Mbps)':
            logger('Check profile setting error')
            raise Exception
        else:
            pass
        logger('pass')

        explore_file = produce_page.get_produced_filename()

        with uuid("d8878c88-9cc4-4f6b-b20f-b56392e40aba") as case:
            # [G54] Surround sound > TrueTheater Surround > Living Room
            produce_page.local.set_surround_sound()
            check_result = produce_page.local.set_surround_sound_true_theater_option_living_room()

            # verify step
            produce_page.exist_click(L.produce.local.btn_surround_sound_true_theater_dialog)
            item = produce_page.exist(L.produce.local.true_theater_settings_dialog.rdb_living_room)
            check_value = item.AXValue
            case.result = check_value and check_result
            time.sleep(DELAY_TIME)
            produce_page.exist_click(L.produce.local.true_theater_settings_dialog.btn_ok)
            time.sleep(DELAY_TIME)

        # Start : produce
        produce_page.click_start()
        for x in range(150):
            check_result = produce_page.check_produce_complete()
            if check_result is True:
                break
            else:
                time.sleep(DELAY_TIME)

        with uuid("4f12eaa6-fa0c-4307-8ff0-e8806a11f2e4") as case:
            # [G100] [Complete] stage > Movie Preview
            main_page.press_space_key()
            time.sleep(DELAY_TIME * 3)
            main_page.press_space_key()
            produce_page.local.set_preview_timecode('00_00_04_10')

            timecode_result = produce_page.get_preview_timecode()
            if timecode_result == '00_00_04_10':
                check_timecode = True
            else:
                check_timecode = False

            verify_step = produce_page.verify_preview(Ground_Truth_Folder + 'G100_manual.png')
            case.result = check_timecode and verify_step

        with uuid("21f54672-2779-4a28-91a4-9f559c49c7ae") as case:
            # [G109] XAVCS > 16:9 > NTSC (MP4) > XAVC S 1920x1080/30p (17Mbps)
            # adjustment line 2802-2817

            # Back to Edit
            produce_page.click_back_to_edit()
            time.sleep(DELAY_TIME * 2)

            # handle high_definition_video_confirm_dialog_click_no
            self.check_dont_show_again_dialog(tick=0)
            time.sleep(DELAY_TIME * 2)

            # Verify : check preview
            main_page.select_library_icon_view_media('Mahoroba.mp3')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.set_timeline_timecode('00_00_05_00', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G109_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G109_preview.png', current_image, similarity=0.98)
            case.result = verify_step

        # Remove the produced file
        main_page.select_library_icon_view_media(explore_file)
        media_room_page.library_clip_context_menu_move_to_trash_can()
        time.sleep(DELAY_TIME)
        timeline_page.drag_timeline_vertical_scroll_bar(0)
        main_page.timeline_select_track(track_no=1)
        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("00701109-1251-4287-8a18-24e8bbe624be") as case:
            # [G147] AVC > 16:9 > M2TS > NTSC > AVC 4K 3840 x 2160/30p (50Mbps)
            produce_page.local.select_file_format(container='avc')

            produce_page.local.select_file_extension('m2ts')
            time.sleep(DELAY_TIME)

            produce_page.local.select_country_video_format('ntsc')
            # select profile name
            produce_page.local.select_profile_name(13)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            logger(check_profile)
            if check_profile != 'AVC 4K 3840 x 2160/30p (50 Mb...':
                logger('Check profile setting error')
                raise Exception
            else:
                pass

            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
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
            time.sleep(DELAY_TIME * 2)

            # Verify : check preview
            main_page.select_library_icon_view_media('Food.jpg')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.set_timeline_timecode('00_00_02_00', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G147_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G147_preview.png', current_image,
                                               similarity=0.98)
            case.result = verify_step

        # Remove the produced file
        main_page.select_library_icon_view_media(explore_file)
        media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_21(self):
        main_page.enter_room(1)
        time.sleep(DELAY_TIME)
        media_room_page.select_LibraryRoom_category('General')
        main_page.select_library_icon_view_media('Clover_03')
        main_page.right_click()
        main_page.select_right_click_menu('Add to Timeline')

        main_page.drag_media_to_timeline_playhead_position(name='Radar', track_no=2)

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("5ace945c-6ac8-4857-b831-89b397b99daf") as case:
            # [G121] XAVCS > 16:9 > PAL (MP4) > XAVC S 3840x2160/25p (60Mbps)

            # click XAVC S
            produce_page.local.select_file_format(container='xavc_s')

            produce_page.local.select_country_video_format('pal')
            # select profile name
            produce_page.local.select_profile_name(8)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            logger(check_profile)
            if check_profile != 'XAVC S 3840 x 2160/25p (60 Mb...':
                logger('Check profile setting error')
                raise Exception
            else:
                pass
            logger('pass')

            explore_file = produce_page.get_produced_filename()

            # Start : produce
            produce_page.click_start()
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
            time.sleep(DELAY_TIME * 2)

            # Verify : check preview
            main_page.select_library_icon_view_media('Food.jpg')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.set_timeline_timecode('00_00_01_24', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G121_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G121_preview.png', current_image,
                                               similarity=0.98)
            case.result = verify_step

        # Remove the produced file
        main_page.select_library_icon_view_media(explore_file)
        media_room_page.library_clip_context_menu_move_to_trash_can()

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("a021d5ef-6c12-482f-8184-6c284074e0ef") as case:
            # [G113] XAVCS > 16:9 > NTSC (MP4) > XAVC S 3840x2160/60p (60Mbps)
            # click XAVC S
            produce_page.local.select_file_format(container='xavc_s')

            produce_page.local.select_country_video_format('ntsc')
            # select profile name
            produce_page.local.select_profile_name(9)
            time.sleep(DELAY_TIME)

            check_profile = produce_page.local.get_profile_name()
            logger(check_profile)
            if check_profile != 'XAVC S 3840 x 2160/60p (60 Mb...':
                logger('Check profile setting error')
                raise Exception
            else:
                pass
            logger('pass')

            explore_file = produce_page.get_produced_filename()
            # Start : produce
            produce_page.click_start()
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
            time.sleep(DELAY_TIME * 2)

            # Verify : check preview
            main_page.select_library_icon_view_media('Sport 01.jpg')
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media(explore_file)
            main_page.set_timeline_timecode('00_00_02_27', is_verify=False)
            current_image = produce_page.snapshot(locator=produce_page.area.preview.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G113_preview.png')
            verify_step = produce_page.compare(Ground_Truth_Folder + 'G113_preview.png', current_image,
                                               similarity=0.98)
            case.result = verify_step

        # Remove the produced file
        main_page.select_library_icon_view_media(explore_file)
        media_room_page.library_clip_context_menu_move_to_trash_can()

        main_page.click_produce()
        produce_page.check_enter_produce_page()

        with uuid("bb342cc8-770a-4f71-adfa-b82e33fdb537") as case:
            # [G123] Custom profile
            produce_page.local.click_create_a_new_profile()
            check_result = produce_page.local.quality_profile_setup.apply_profile_name('Mac AT Custom XAVC',
                                                                                       'SFT Profile XAVC')

            item = produce_page.find(L.produce.local.quality_profile_setup_dialog.profile_name.edittext_description)
            if produce_page.exist(item):
                AT_custom_description = item.AXValue
            if AT_custom_description == 'SFT Profile XAVC':
                check_custom_description = True
            else:
                check_custom_description = False

            produce_page.local.quality_profile_setup.switch_to_video_tab()
            produce_page.local.quality_profile_setup.set_video_profile(index_resolution=3, index_frame_rate=4)
            produce_page.local.quality_profile_setup.set_video_bitrate(39000)

            # click OK > close (Quality Profile Setup)
            produce_page.local.quality_profile_setup.click_ok()

            produce_page.local.click_details()
            time.sleep(DELAY_TIME)
            current_image = produce_page.snapshot(locator=L.produce.local.details_dialog.main_window,
                                                  file_name=Auto_Ground_Truth_Folder + 'G123.png')
            check_detail = produce_page.compare(Ground_Truth_Folder + 'G123.png', current_image)
            produce_page.press_esc_key()

            explore_file = produce_page.get_produced_filename()
            # Start : produce
            produce_page.click_start()
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
            time.sleep(DELAY_TIME * 2)

            # Verify :  Media Room > Right Click Menu > Check View Properties
            main_page.select_library_icon_view_media('Landscape 02.jpg')
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media(explore_file)
            main_page.right_click()
            main_page.select_right_click_menu('View Properties')
            time.sleep(DELAY_TIME*2)
            current_image = produce_page.snapshot(locator=L.media_room.properties_dialog.main_window,
                                                      file_name=Auto_Ground_Truth_Folder + 'G123_properties.png')
            verify_properties = produce_page.compare(Ground_Truth_Folder + 'G123_properties.png', current_image)
            case.result = verify_properties and check_detail and check_custom_description
            produce_page.press_esc_key()

            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

        main_page.click_produce()
        produce_page.check_enter_produce_page()
        with uuid("cb36701f-d717-434a-8525-c917befc87a5") as case:
            # [G37] Create a new profile > Cancel button
            produce_page.local.click_create_a_new_profile()
            time.sleep(DELAY_TIME)
            produce_page.local.quality_profile_setup.click_cancel()
            check_result = produce_page.is_exist(L.produce.local.quality_profile_setup_dialog.main_window)
            case. result = not check_result

        with uuid("f1426fb8-bbae-4ba1-9e29-b1f4646b00ba") as case:
            # [G40] Profile Editing > Edit (Enable)
            check_result = produce_page.local.click_edit_custom_profile()

            item = produce_page.find(L.produce.local.quality_profile_setup_dialog.profile_name.edittext_description)
            if produce_page.exist(item):
                AT_custom_description = item.AXValue
            if AT_custom_description == 'SFT Profile XAVC':
                check_custom_description = True
            else:
                check_custom_description = False

            case.result = check_result and check_custom_description

        with uuid("0ca54d37-bda8-4aca-ab96-1519b0648ece") as case:
            # [G36] Create a new profile > X button
            produce_page.local.quality_profile_setup.click_close()
            check_result = produce_page.is_exist(L.produce.local.quality_profile_setup_dialog.main_window)
            case. result = not check_result