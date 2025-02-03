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
base_page = PageFactory().get_page_object('base_page', mac)
media_room_page = PageFactory().get_page_object('media_room_page', mac)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mac)
playback_window_page = PageFactory().get_page_object('playback_window_page', mac)
precut_page = PageFactory().get_page_object('precut_page', mac)
tips_area_page = PageFactory().get_page_object('tips_area_page', mac)
library_preview_page = PageFactory().get_page_object('library_preview_page', mac)
project_room_page = PageFactory().get_page_object('project_room_page', mac)
pip_room_page = PageFactory().get_page_object('pip_room_page', mac)

# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="Project Room.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
#Ground_Truth_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/SFT/GroundTruth/Pre_Cut/'
#Auto_Ground_Truth_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/SFT/ATGroundTruth/Pre_Cut/'
#Test_Material_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/Material/'
Ground_Truth_Folder = app.ground_truth_root + '/project_room/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/project_room/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_project_room():
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
            google_sheet_execution_log_init('project_room')

    @classmethod
    def teardown_class(cls):

        logger('teardown_class - export report')
        report.export()
        logger(
            f"project room result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
        #Enter Project Room
        with uuid("daf23b9d-dd75-4bcc-aa7a-a1c9d5547618") as case:
            case.result = project_room_page.enter_project_room()

        #Show project in Project room after save project
        with uuid("4a061dd3-45ce-4674-9c14-e2ebd8f3be46") as case:
            project_room_page.import_pds_project(app.testing_material + 'project_room/test.pds/')
            if main_page.exist({'AXIdentifier': 'IDD_CLALERT'}):
                main_page.handle_merge_media_to_current_library_dialog()
            project_room_page.enter_project_room()
            case.result = main_page.select_library_icon_view_media('test')

        #Show project in Project room after open project
        with uuid("56fde3b9-408d-4699-af95-0058527bc9eb") as case:
            main_page.press_del_key()
            main_page.top_menu_bar_file_open_project(save_changes=False)
            main_page.handle_open_project_dialog(app.testing_material + 'project_room/test.pds/')
            if main_page.exist({'AXIdentifier': 'IDD_CLALERT'}):
                main_page.handle_merge_media_to_current_library_dialog()
            project_room_page.enter_project_room()
            case.result = main_page.select_library_icon_view_media('test')

        #Show project in preview window
        with uuid("68ea1896-0308-4410-971f-4c1dcaa5e65e") as case:
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_1_1.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_1_1.png',
                                               playback_window_snap)

        #Library preview window should not be enabled in project room
        with uuid("18bfdb58-a65f-43d1-b96f-bf83aa1c7751") as case:
            case.result = main_page.top_menu_bar_view_show_library_preview_window(0)

        #Play/Pause
        with uuid("a6fcc63c-4dac-498a-a76a-7b8f9fcedf54") as case:
            playback_window_page.context.click_play_pause()
            time.sleep(3)
            playback_window_page.context.click_play_pause()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_1_1_2.png')
            logger(playback_window_snap)
            case.result = main_page.compare(Ground_Truth_Folder + '1_1_1_2.png',
                                            playback_window_snap)
        #stop
        with uuid("717c8535-033b-428a-b20c-bba6fccd5391") as case:
            current_result = playback_window_page.context.click_stop()
            timecode_result = True if playback_window_page.get_timecode_slidebar() == "00;00;00;00" else False
            case.result = current_result and timecode_result

        #next frame
        with uuid("d7e198a0-abc2-4fc3-8160-f4ced453945a") as case:
            current_result = playback_window_page.context.click_next_frame()
            timecode_result = True if playback_window_page.get_timecode_slidebar() == "00;00;00;01" else False
            case.result = current_result and timecode_result

        #previous frame
        with uuid("486d77d5-16dd-45d2-afb7-9870f9f1f96d") as case:
            current_result = playback_window_page.context.click_previous_frame()
            timecode_result = True if playback_window_page.get_timecode_slidebar() == "00;00;00;00" else False
            case.result = current_result and timecode_result


        #fastforward
        with uuid("7a5791c2-7125-49ee-9527-73f18d63ea13") as case:
            time.sleep(2)
            original_timecode = playback_window_page.get_timecode_slidebar()
            playback_window_page.context.click_fastforward()
            time.sleep(2)
            after_fastforward_timecode = playback_window_page.get_timecode_slidebar()
            if not original_timecode != after_fastforward_timecode:
                case.result = True
            else:
                case.result = False

        #preview_volume_meter
        with uuid("6e83d07f-fa1e-4fbb-ab6d-c0a2fdb2e118") as case:
            case.result = main_page.top_menu_bar_view_show_timeline_preview_volume_meter()

        #PreviewQuality
        with uuid("a7d8bdd8-9398-4737-b0ca-4ddb4acb2791") as case:
            playback_window_page.Edit_TimelinePreview_SetPreviewQuality('Ultra HD')
            if playback_window_page.Edit_TimelinePreview_GetPreviewQuality() != 'Ultra HD':
                case.result = True
            else:
                case.result = False

        #render_preview_button
        with uuid("99397b68-1237-42c6-8a04-afd93b7baf9f") as case:
            case.result = not main_page.exist(L.timeline_operation.render_preview_button).AXEnabled


    @exception_screenshot
    def test_1_2_1(self):
        #Able to select project to import
        with uuid("b3c4f928-a975-4dc9-8ae0-eeb918cc4b69") as case:
            project_room_page.enter_project_room()
            project_room_page.import_pds_project(app.testing_material + 'project_room/test.pds/')
            if main_page.exist({'AXIdentifier': 'IDD_CLALERT'}):
                main_page.handle_merge_media_to_current_library_dialog()
            project_room_page.enter_project_room()
            project_room_page.import_pds_project(app.testing_material + 'project_room/Untitled.pds/')
            if main_page.exist({'AXIdentifier': 'IDD_CLALERT'}):
                main_page.handle_merge_media_to_current_library_dialog()
            project_room_page.enter_project_room()
            case.result = main_page.select_library_icon_view_media('Untitled')

        #Thumbnails show as Details
        with uuid("aad51c88-1f75-4ee8-b47f-c753722a7d49") as case:
            current_result = main_page.click_library_details_view()
            time.sleep(3)
            library_result = media_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_2_1_1.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1_2_1_1.png',
                                                     library_result)
            case.result = current_result and compare_result

        #Thumbnails show as Icon
        with uuid("6cf168eb-b13a-46a3-a6df-a924a4ee99e5") as case:
            current_result = main_page.click_library_icon_view()
            time.sleep(3)
            library_result = media_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_2_1_2.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1_2_1_2.png',
                                                     library_result)
            case.result = current_result and compare_result

        # right click sort by created date
        with uuid("57fafa9f-c78f-4e81-8293-097cb666bff7") as case:
            current_result = media_room_page.library_menu_sort_by_date()
            time.sleep(3)
            library_result = media_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_2_1_3.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1_2_1_3.png',
                                                     library_result)
            case.result = compare_result and current_result

        # right click sort by file size
        with uuid("285f94c4-c76c-4d55-a72a-a970871cd925") as case:
            current_result = media_room_page.collection_view_right_click_sort_by_file_size()
            time.sleep(3)
            library_result = media_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_2_1_4.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1_2_1_4.png',
                                                     library_result)
            case.result = compare_result and current_result

        # right click sort by duration
        with uuid("eaa4a8f5-0f4b-4244-9122-84021b1491ba") as case:
            current_result = media_room_page.collection_view_right_click_sort_by_duration()
            time.sleep(3)
            library_result = media_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_2_1_5.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1_2_1_5.png',
                                                     library_result)
            case.result = compare_result and current_result

        # right click sort by name
        with uuid("97eb9541-1bbb-4986-9760-ffab33d80d08") as case:
            current_result = media_room_page.collection_view_right_click_sort_by_name()
            time.sleep(3)
            library_result = media_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_2_1_6.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1_2_1_6.png',
                                                     library_result)
            case.result = compare_result and current_result

        #select all
        with uuid("003d52d7-1cc0-439c-a10d-526b15f09d1d") as case:
            current_result = media_room_page.library_menu_select_all()
            time.sleep(3)
            library_result = media_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_2_1_7.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1_2_1_7.png',
                                                     library_result)
            case.result = current_result and compare_result

        # library menu medium icon
        with uuid("c1211cad-41e6-4c5c-bdfe-6a4c8fdec8c4") as case:
            time.sleep(DELAY_TIME * 2)
            main_page.exist(L.media_room.library_menu.btn_menu).press()
            time.sleep(3)
            library_result1 = media_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_2_1_110.png')
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + '1_2_1_110.png',
                                                     library_result1)
            media_room_page.library_menu_extra_large_icons()
            current_result = media_room_page.library_menu_medium_icons()
            time.sleep(3)
            library_result = media_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_2_1_11.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1_2_1_11.png',
                                                     library_result)
            case.result = current_result and compare_result and compare_result1

        # library menu extra large icon
        with uuid("c3aafd44-7cd7-4b62-96a1-b937c3d1d270") as case:
            current_result = media_room_page.library_menu_extra_large_icons()
            time.sleep(3)
            library_result = media_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_2_1_8.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1_2_1_8.png',
                                                     library_result)
            case.result = current_result and compare_result

        # library menu large icon
        with uuid("8e684d31-145e-4838-b181-2d8f5364995f") as case:
            current_result = media_room_page.library_menu_large_icons()
            time.sleep(3)
            library_result = media_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_2_1_9.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1_2_1_9.png',
                                                     library_result)
            case.result = current_result and compare_result

        # library menu small icon
        with uuid("6afb345f-4bd3-442d-b9e4-2ce891246c53") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.library_menu_small_icons()
            time.sleep(3)
            library_result = media_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_2_1_10.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1_2_1_10.png',
                                                     library_result)
            case.result = current_result and compare_result

        #search box
        with uuid("00595d5e-8fcd-4e97-a1db-aa1ecd1f3c44") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.search_library('Untitled')
            time.sleep(3)
            library_result = media_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_2_1_12.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1_2_1_12.png',
                                                     library_result)
            case.result = current_result and compare_result

        # cancel search
        with uuid("347af7f3-8cc9-4807-9e50-1794ebc0884d") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.search_library_click_cancel()
            case.result = current_result

        # Hide explorer view
        with uuid("aa2484e8-c51e-4fa6-bd1e-53b96a11dfba") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.click_display_hide_explore_view()
            time.sleep(3)
            case.result = current_result

        # Display explorer view
        with uuid("a5f6d797-a95a-4c3e-81be-aabce0611f9b") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.click_display_hide_explore_view()
            time.sleep(3)
            case.result = current_result

        # add new tag
        with uuid("10528f27-712b-449d-84d9-86dbf16f271b") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.add_new_tag('abc')
            time.sleep(3)
            main_page.timeline_select_track(0)
            library_result = media_room_page.snapshot(locator=L.media_room.tag_scroll_view_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_2_1_16.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1_2_1_16.png',
                                                     library_result)
            case.result = current_result and compare_result

        # add new tag with exist name
        with uuid("1a94f6a1-aa52-43dd-8693-e02f85ad67c7") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.add_new_tag('abc')
            time.sleep(3)
            main_page.timeline_select_track(0)
            library_result = media_room_page.snapshot(locator=L.media_room.tag_scroll_view_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_2_1_17.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1_2_1_17.png',
                                                     library_result)
            case.result = (not current_result) and compare_result

        # add new tag with long char
        with uuid("9e6d23e0-e9e7-4265-a841-73103c30dcf2") as case:
            time.sleep(DELAY_TIME * 2)
            media_room_page.add_new_tag('abcaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            SetCheck_result = project_room_page.find_specific_tag('abcaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            main_page.timeline_select_track(0)
            library_result2 = media_room_page.snapshot(locator=L.media_room.tag_scroll_view_frame,
                                                       file_name=Auto_Ground_Truth_Folder + '1_2_1_171.png')
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + '1_2_1_171.png',
                                                      library_result2)
            if not SetCheck_result:
                current_result = False
            else:
                current_result = True

            case.result = compare_result2 and current_result

        # add new tag with Symbo
        with uuid("8969fad0-3c40-48a2-8b1c-904df838aa54") as case:
            time.sleep(DELAY_TIME * 3)
            media_room_page.add_new_tag('@')
            SetCheck_result = project_room_page.find_specific_tag('@')
            main_page.timeline_select_track(0)
            library_result2 = media_room_page.snapshot(locator=L.media_room.tag_scroll_view_frame,
                                                       file_name=Auto_Ground_Truth_Folder + '1_2_1_172.png')
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + '1_2_1_172.png',
                                                      library_result2)
            if not SetCheck_result:
                current_result = False
            else:
                current_result = True

            case.result = compare_result2 and current_result

        # add new tag with Unicode
        with uuid("4faed1cb-ddd5-484a-9050-32b0927b3159") as case:
            time.sleep(DELAY_TIME * 3)
            media_room_page.add_new_tag('???')
            SetCheck_result = project_room_page.find_specific_tag('???')
            main_page.timeline_select_track(0)
            library_result2 = media_room_page.snapshot(locator=L.media_room.tag_scroll_view_frame,
                                                       file_name=Auto_Ground_Truth_Folder + '1_2_1_173.png')
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + '1_2_1_173.png',
                                                      library_result2)
            if not SetCheck_result:
                current_result = False
            else:
                current_result = True

            case.result = compare_result2 and current_result

        # delete default tag (gray out)
        with uuid("86c57933-00a0-4fc3-8569-dbcb696592bd") as case:
            time.sleep(DELAY_TIME * 2)
            main_page.timeline_select_track(0)

            library_result = media_room_page.snapshot(locator=L.media_room.btn_delete_tag,
                                                      file_name=Auto_Ground_Truth_Folder + '1_2_1_19.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1_2_1_19.png',
                                                     library_result)
            case.result = compare_result

        # delete tag
        with uuid("ac4a2fd2-1ba9-4cad-b60d-76b1bff42b1f") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.delete_tag('abc')
            time.sleep(DELAY_TIME * 2)
            main_page.timeline_select_track(0)
            case.result = current_result

        #Rename the tag
        with uuid("0c98668d-8b73-426d-8769-9dd6770440a8") as case:
            time.sleep(DELAY_TIME * 2)
            media_room_page.add_new_tag('abcd')
            current_result = media_room_page.right_click_rename_tag('abcd', '1234')
            main_page.timeline_select_track(0)
            library_result = media_room_page.snapshot(locator=L.media_room.tag_scroll_view_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_2_1_21.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1_2_1_21.png',
                                                     library_result)
            case.result = current_result and compare_result

        #Right click to delete_tag
        with uuid("c1775655-914b-4d96-af4f-1e4d91618f78") as case:
            current_result = media_room_page.right_click_delete_tag('1234')
            main_page.timeline_select_track(0)
            library_result = media_room_page.snapshot(locator=L.media_room.tag_scroll_view_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_2_1_22.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1_2_1_22.png',
                                                     library_result)
            case.result = current_result and compare_result

        #tooltips
        with uuid("b57b6e0c-3b47-48db-be11-489889eff1c9") as case:
            main_page.hover_library_media('test')
            time.sleep(1)
            library_result = media_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_2_1_23.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1_2_1_23.png',
                                                     library_result)
            case.result = compare_result

        with uuid("fbf57ef8-3bce-45b9-b7bf-f978bbbb04e9") as case:
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1_2_1_23.png',
                                                     Auto_Ground_Truth_Folder + '1_2_1_23.png')
            case.result = compare_result

        with uuid("1fb2532f-9881-480a-a70e-e181f1ad8496") as case:
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1_2_1_23.png',
                                                     Auto_Ground_Truth_Folder + '1_2_1_23.png')
            case.result = compare_result

        #open_file_location
        with uuid("0ad4eed4-882b-4889-a3dd-946efb96b100") as case:
            main_page.select_library_icon_view_media('test')
            case.result = media_room_page.library_clip_context_menu_open_file_location()

        #Show correct project name
        with uuid("bc5030ae-6bce-4cfb-a92a-46b8991ad8fe") as case:
            current_result = main_page.select_library_icon_view_media('Untitled')
            library_result = media_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_2_1_26.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1_2_1_26.png',
                                                     library_result)
            case.result = current_result and compare_result

        #Able to add into custom tag
        with uuid("dc76d64b-af67-42bc-8c14-8f21bd2bfab6") as case:
            main_page.select_library_icon_view_media('Untitled')
            main_page.right_click()
            main_page.select_right_click_menu("Add to Custom Tag", "New Tag")
            time.sleep(DELAY_TIME * 2)
            media_room_page.select_specific_category('New Tag')
            library_result1 = media_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_2_1_27.png')
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + '1_2_1_27.png',
                                                     library_result1)
            case.result = compare_result1 and current_result

        #Remove from project room directly
        with uuid("82daf827-718d-4a7c-8d1a-ffdf1c4538df") as case:
            main_page.select_library_icon_view_media('Untitled')
            main_page.press_del_key()
            case.result = True if not main_page.exist({"AXIdentifier": "CollectionViewItemTextField", "AXValue": 'Untitled'}) else False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_3_1(self):
        #Multi project able to add into custom tag
        with uuid("aaa694d4-445b-466a-8777-c1d2176671ad") as case:
            project_room_page.enter_project_room()
            project_room_page.import_pds_project(app.testing_material + 'project_room/test.pds/')
            if main_page.exist({'AXIdentifier': 'IDD_CLALERT'}):
                main_page.handle_merge_media_to_current_library_dialog()
            project_room_page.enter_project_room()
            project_room_page.import_pds_project(app.testing_material + 'project_room/Untitled.pds/')
            project_room_page.enter_project_room()
            media_room_page.add_new_tag('New Tag')
            main_page.select_library_icon_view_media('test')
            main_page.tap_command_and_hold()
            main_page.select_library_icon_view_media('Untitled')
            main_page.release_command_key()
            main_page.right_click()
            current_result = main_page.select_right_click_menu("Add to Custom Tag", "New Tag")
            time.sleep(DELAY_TIME * 2)
            media_room_page.select_specific_category('New Tag')
            library_result1 = media_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_3_1_1.png')
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + '1_3_1_1.png',
                                                     library_result1)
            case.result = compare_result1 and current_result

        #Multi project disable to open file location
        with uuid("9dd67e28-1be1-44dd-8252-d1f59dbb9dfe") as case:
            main_page.tap_command_and_hold()
            main_page.select_library_icon_view_media('Untitled')
            main_page.release_command_key()
            main_page.right_click()
            item = main_page.exist({"AXRole": "AXMenuItem", "AXTitle": 'Open File Location'})
            if not item.AXEnabled:
                case.result = True
            else:
                case.result = False

        #Multi project remove from project room directly
        with uuid("0ae514b4-2ba7-43c7-a1f3-ac573f00a64e") as case:
            main_page.select_right_click_menu('Remove')
            case.result = True if not main_page.exist({"AXIdentifier": "CollectionViewItemTextField", "AXValue": 'Untitled'}) else False


        # Dock/Undock Library Window
        with uuid("15c0a5e4-1d06-44e3-89ff-88a112b87f2c") as case:
            current_result = pip_room_page.select_RightClickMenu_DockUndock_LibraryWindow()

            case.result = current_result

        # Reset All Undocked Windows
        with uuid("c8911074-915a-4555-9195-f808f547b336") as case:
            current_result = media_room_page.library_clip_context_menu_reset_all_undocked_window()
            case.result = current_result

        # Select all hotkey
        with uuid("7dd3ea88-9f5f-4ae8-9d3f-07b0d54a9f9f") as case:
            main_page.exist_click(L.project_room.check_My_Project)
            main_page.tap_SelectAll_hotkey()
            library_result = media_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_3_1_6.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1_3_1_6.png',
                                                     library_result)
            case.result = compare_result

        # Multi select hotkey
        with uuid("e208c5b0-a463-420a-96aa-5080492c5ab8") as case:
            main_page.select_library_icon_view_media('test')
            main_page.tap_command_and_hold()
            current_result = main_page.select_library_icon_view_media('Untitled')
            main_page.release_command_key()
            library_result = media_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_3_1_7.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1_3_1_7.png',
                                                     library_result)
            case.result = compare_result and current_result

        # Delete hotkey
        with uuid("df7fc89a-601d-4b29-8636-26816536b36f") as case:
            main_page.press_del_key()
            case.result = True if not main_page.exist({"AXIdentifier": "CollectionViewItemTextField", "AXValue": 'test'}) else False


    # @pytest.mark.skip
    @exception_screenshot
    def test_1_4_1(self):
        #Single project [Add to track] button
        with uuid("b53e3311-4713-49cc-9fec-c21dcd2c10d8") as case:
            project_room_page.enter_project_room()
            project_room_page.import_pds_project(app.testing_material + 'project_room/test.pds/')
            time.sleep(2)
            if main_page.exist({'AXIdentifier': 'IDD_CLALERT'}):
                main_page.handle_merge_media_to_current_library_dialog()
            project_room_page.enter_project_room()
            project_room_page.import_pds_project(app.testing_material + 'project_room/Untitled.pds/')
            time.sleep(2)
            project_room_page.enter_project_room()
            main_page.select_library_icon_view_media('test')
            current_result = project_room_page.tips_area_insert_project_to_selected_track()

            case.result = current_result

        #Multi project [Add to track] button
        with uuid("2bb64c66-da07-4b39-b8fa-bb73bd19885f") as case:
            main_page.click_undo()
            main_page.select_library_icon_view_media('test')
            main_page.tap_command_and_hold()
            current_result = main_page.select_library_icon_view_media('Untitled')
            main_page.release_command_key()
            playback_window_snap = main_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + '1_4_1_2.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_4_1_2.png',
                                               playback_window_snap)

            case.result = compare_result and current_result

        #tooltips
        with uuid("3b00359a-665f-4645-99ee-5a216c4297bf") as case:
            main_page.click_undo()
            pos = main_page.get_position(L.project_room.btn_add_to_track)
            main_page.mouse.move(pos["x"], pos["y"])
            time.sleep(1)
            playback_window_snap = main_page.snapshot(locator=L.project_room.btn_add_to_track,
                                                      file_name=Auto_Ground_Truth_Folder + '1_4_1_3.png')
            logger(playback_window_snap)
            compare_result = main_page.compare(Ground_Truth_Folder + '1_4_1_3.png',
                                               playback_window_snap)

            case.result = compare_result and current_result

        #Single project drag to timeline
        with uuid("c07d5325-2e44-4f61-997f-538de655487e") as case:
            main_page.select_library_icon_view_media('test')
            current_result = project_room_page.tips_area_insert_project_to_selected_track()
            time.sleep(2)

            case.result = current_result

        #Multi project drag to timeline
        with uuid("942d3586-7b9b-49b2-8248-f62df01a176c") as case:
            main_page.click_undo()
            main_page.select_library_icon_view_media('test')
            main_page.tap_command_and_hold()
            current_result = main_page.select_library_icon_view_media('Untitled')
            main_page.release_command_key()

            case.result = current_result

        #Undo
        with uuid("2dc7808f-9367-4828-8a9f-01c006c33623") as case:
            current_result = main_page.click_undo()
            library_result = media_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_4_1_6.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1_4_1_6.png',
                                                     library_result)
            case.result = compare_result and current_result

        #Redo
        with uuid("0b533b55-bfa3-4beb-aa91-00fba6a3df7e") as case:
            current_result = main_page.click_redo()
            library_result = media_room_page.snapshot(locator=L.media_room.library_frame,
                                                      file_name=Auto_Ground_Truth_Folder + '1_4_1_7.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1_4_1_7.png',
                                                     library_result)
            case.result = compare_result and current_result

        #Project should keep in project room after relaunch PDR
        with uuid("57f23565-a05e-49b7-ad96-5aec5e22672b") as case:
            main_page.close_and_restart_app()
            project_room_page.enter_project_room()
            media_room_page.add_new_tag("New Tag")
            case.result = main_page.select_library_icon_view_media('test')
            main_page.right_click()
            main_page.select_right_click_menu("Add to Custom Tag", "New Tag")

        #tag should keep in project room after relaunch PDR
        with uuid("0cd3ba37-3cc2-46c0-a243-c10b08ffa87d") as case:
            main_page.close_and_restart_app()
            project_room_page.enter_project_room()
            media_room_page.library_menu_select_all()
            main_page.press_del_key()
            case.result = project_room_page.find_specific_tag('New Tag')

    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
        cce23ca9-72cd-4d4c-bf5c-5dc2dcfece90
        16e242e5-5abf-4551-8b35-557451e54057
        805d3da9-2aae-4b93-99fc-d1692e65ccb6
        283056f2-8acc-4727-b4e2-37db099852a4
        61be872b-8b65-44fc-adea-131437224ec7
                        ''') as case:
            case.result = None
            case.fail_log = "*SKIP by AT*"










