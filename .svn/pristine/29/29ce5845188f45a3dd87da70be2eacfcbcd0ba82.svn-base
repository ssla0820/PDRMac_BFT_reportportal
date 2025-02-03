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
mask_designer_page = PageFactory().get_page_object('title_designer_page', mwc)
media_room_page = PageFactory().get_page_object('media_room_page', mwc)
title_room_page = PageFactory().get_page_object('title_room_page', mwc)
title_designer_page = PageFactory().get_page_object('title_designer_page', mwc)
timeline_page = PageFactory().get_page_object('timeline_operation_page', mwc)
tips_area_page = PageFactory().get_page_object('tips_area_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Motion Graphics Title.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Motion_Graphics_Title/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Motion_Graphics_Title/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Motion_Graphics_Title():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
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
            google_sheet_execution_log_init('Motion_Graphics_Title_2')

    @classmethod
    def teardown_class(cls):

        logger('teardown_class - export report')
        report.export()
        logger(
            f"Motion Graphics Title result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
        # modify 4_3 mgt from title room
        with uuid("466872b4-ff50-439d-b694-aadc1fc6eafe") as case:
            time.sleep(4)
            main_page.set_project_aspect_ratio_4_3()
            main_page.enter_room(1)
            title_room_page.select_specific_tag('Motion Graphics')
            result_status = title_room_page.click_ModifySelectedTitle_btn()
            logger(result_status)
            case.result = result_status

        with uuid("03011590-3a87-428d-876b-ca7e0606a641") as case:
            # show warning at 1st time entry
            time.sleep(1)
            result_status = title_designer_page.mgt.click_warning_msg_ok()
            logger(result_status)
            case.result = result_status

        with uuid("16c20ac4-fb31-4e37-b546-35e9c513a4f8") as case:
            # check 4_3 mgt template in preview
            time.sleep(1)
            title_designer_page.click_maximize_btn()
            title_designer_page.set_timecode('00_00_05_00')
            time.sleep(1)
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + '4_3_snapshot.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + '4_3_snapshot.png', image_result)
            case.result = compare_result

        with uuid("637f0fe0-b7e5-4103-82cb-300b08c7b36a") as case:
            # still show waning at next entry
            title_designer_page.click_cancel()
            main_page.set_project_aspect_ratio_16_9()
            media_room_page.select_media_content('Motion Graphics 002')
            title_room_page.click_ModifySelectedTitle_btn()
            time.sleep(1)
            title_designer_page.mgt.handle_warning_msg(1)
            result_status = title_designer_page.mgt.click_warning_msg_ok()
            logger(result_status)
            case.result = result_status

        with uuid("5b3d9bff-4a71-4980-8292-a7aebbc46e3f") as case:
            # check 16_9 mgt template in preview, case 1~5
            time.sleep(1)
            title_designer_page.set_timecode('00_00_05_00')
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + '16_9_snapshot.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + '16_9_snapshot.png', image_result)
            case.result = compare_result

        with uuid("b3598e65-0705-48cc-9f76-0a17fa412965") as case:
            # No warning at next entry
            time.sleep(1)
            title_designer_page.click_cancel()
            main_page.set_project_aspect_ratio_9_16()
            media_room_page.select_media_content('Motion Graphics 003')
            title_room_page.click_ModifySelectedTitle_btn()
            time.sleep(1)
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + 'No_warning.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + 'No_warning.png', image_result)
            case.result = compare_result

        with uuid("da426bbe-a3da-4155-8e52-caeeb1fc072e") as case:
            # check 9_16 mgt template in preview
            time.sleep(1)
            title_designer_page.set_timecode('00_00_05_00')
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + '9_16_snapshot.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + '9_16_snapshot.png', image_result)
            case.result = compare_result

        with uuid("31b57dad-49fb-46a0-aac3-6c38dd146c08") as case:
            # check 1_1 mgt template in preview
            title_designer_page.click_cancel()
            main_page.set_project_aspect_ratio_1_1()
            media_room_page.select_media_content('Motion Graphics 004')
            title_room_page.click_ModifySelectedTitle_btn()
            title_designer_page.set_timecode('00_00_05_00')
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + '1_1_snapshot.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + '1_1_snapshot.png', image_result)
            case.result = compare_result

    #/ Users / qadf / Desktop / SFT_M2 / GroundTruth
    #/ Users / qadf / Desktop / SFT_M2 / SFT / GroundTruth
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        # check mgt context menu - add to timeline
        with uuid("d590259c-5497-47f5-85e9-bd3c812899b1") as case:
            time.sleep(4)
            main_page.enter_room(1)
            title_room_page.select_specific_tag('Motion Graphics')
            media_room_page.select_media_content('Motion Graphics 005')
            title_room_page.select_RightClickMenu_AddToTimeline()
            main_page.set_timeline_timecode('00_00_02_00')
            current_image = title_room_page.snapshot(locator=L.library_preview.display_panel,
                                                     file_name=Auto_Ground_Truth_Folder + 'Add_to_timeline.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'Add_to_timeline.png', current_image)
            case.result = compare_result

        with uuid("c535ced5-abf7-4a88-94f7-d01c8709ff81") as case:
            # modify mgt template from context menu, case 6~10
            time.sleep(1)
            media_room_page.select_media_content('Motion Graphics 006')
            title_room_page.select_RightClickMenu_ModifyTemplate()
            title_designer_page.mgt.click_warning_msg_ok()
            title_designer_page.set_timecode('00_00_05_00')
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + 'Modify_contextmenu.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + 'Modify_contextmenu.png', image_result)
            case.result = compare_result

        with uuid("898a2349-f7b3-4d9a-8335-5aa1e1658e80") as case:
            time.sleep(1)
            title_designer_page.click_cancel()
            # change alias is disable in context menu
            time.sleep(1)
            media_room_page.select_media_content('Motion Graphics 006')
            title_room_page.right_click()
            time.sleep(1)
            result_status = title_room_page.select_right_click_menu('Change Alias')
            logger(result_status)
            case.result = not result_status

        with uuid("3c86834c-a8cc-4758-b3d2-50ec498cb589") as case:
            # share and upload to the internet is disable in context menu
            time.sleep(1)
            title_room_page.right_click()
            time.sleep(1)
            result_status = title_room_page.select_right_click_menu('Share and Upload to the Internet...')
            logger(result_status)
            case.result = not result_status

        with uuid("a8502d82-b7c7-4c90-871d-fe465772b6c0") as case:
            # delete (only for Custom/Downloaded) is disable in context menu
            time.sleep(1)
            title_room_page.right_click()
            time.sleep(1)
            result_status = title_room_page.select_right_click_menu('Delete (only for Custom/Downloaded)')
            logger(result_status)
            case.result = not result_status

        with uuid("3cd46559-f225-4ae5-979e-9fb6c1aa206f") as case:
            # add mgt template to new tag
            time.sleep(1)
            title_room_page.add_titleroom_new_tag('PDR_Mac_AT')
            title_room_page.select_specific_tag('Motion Graphics')
            media_room_page.select_media_content('Motion Graphics 006')
            result_status = title_room_page.select_RightClickMenu_Addto('PDR_Mac_AT')
            logger(result_status)
            case.result = result_status

        with uuid("00593252-a44f-46cb-b04f-a9e51f80118b") as case:
            # delete mgt from new tag and library is empty, case 11~15
            time.sleep(1)
            title_room_page.select_specific_tag('PDR_Mac_AT')
            media_room_page.select_media_content('Motion Graphics 006')
            title_room_page.right_click()
            time.sleep(1)
            title_room_page.keyboard.up()
            title_room_page.keyboard.up()
            title_room_page.keyboard.enter()
            time.sleep(1)
            current_image = title_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                     file_name=Auto_Ground_Truth_Folder + 'Empty.png')
            # logger(f"{current_image=}")
            compare_result = title_room_page.compare(Ground_Truth_Folder + 'Empty.png', current_image)
            case.result = compare_result

    def test_1_1_3(self):
        # open designer from tips area_designer button, CASE 16~20
        with uuid("13e05b65-93ba-45a9-9f84-5e0c9e6397c4") as case:
            time.sleep(4)
            main_page.enter_room(1)
            title_room_page.select_specific_tag('Motion Graphics')
            media_room_page.select_media_content('Motion Graphics 007')
            title_room_page.select_RightClickMenu_AddToTimeline()
            time.sleep(1)
            tips_area_page.click_TipsArea_btn_Designer('title')
            time.sleep(1)
            title_designer_page.mgt.handle_warning_msg(1)
            title_designer_page.mgt.click_warning_msg_ok()
            title_designer_page.click_maximize_btn()
            title_designer_page.set_timecode('00_00_05_00')
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + 'FromTipArea_Designer.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + 'FromTipArea_Designer.png', image_result)
            case.result = compare_result

        with uuid("edef2676-ed4b-4f88-8c5e-e33f0d0ea084") as case:
            # open designer from more features
            time.sleep(1)
            title_designer_page.click_cancel()
            time.sleep(1)
            main_page.tap_NewWorkspace_hotkey()
            time.sleep(1)
            main_page.press_esc_key()
            media_room_page.select_media_content('Motion Graphics 008')
            tips_area_page.click_TipsArea_btn_insert(-1)
            tips_area_page.more_features.edit_title()
            time.sleep(1)
            title_designer_page.set_timecode('00_00_05_00')
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + 'FromTipArea_More.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + 'FromTipArea_More.png', image_result)
            case.result = compare_result

        with uuid("fe275342-06b6-44df-9b0d-dc32753f3afb") as case:
            # open designer from right click menu
            time.sleep(1)
            title_designer_page.click_cancel()
            time.sleep(1)
            main_page.tap_NewWorkspace_hotkey()
            time.sleep(1)
            main_page.press_esc_key()
            media_room_page.select_media_content('Motion Graphics 009')
            tips_area_page.click_TipsArea_btn_insert(-1)
            timeline_page.select_timeline_media(track_index=0, clip_index=0)
            timeline_page.right_click()
            time.sleep(1)
            timeline_page.keyboard.up()
            timeline_page.keyboard.up()
            timeline_page.keyboard.up()
            timeline_page.keyboard.enter()
            time.sleep(1)
            title_designer_page.set_timecode('00_00_05_00')
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + 'From_RClick_menu.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + 'From_RClick_menu.png', image_result)
            case.result = compare_result

        with uuid("3eadc795-8889-470c-a603-fc1f384d7ac3") as case:
            # open designer from double click template
            time.sleep(1)
            title_designer_page.click_cancel()
            time.sleep(1)
            main_page.tap_NewWorkspace_hotkey()
            time.sleep(1)
            main_page.press_esc_key()
            media_room_page.select_media_content('Motion Graphics 010')
            tips_area_page.click_TipsArea_btn_insert(-1)
            timeline_page.select_timeline_media(track_index=0, clip_index=0)
            timeline_page.double_click()
            time.sleep(1)
            title_designer_page.set_timecode('00_00_05_00')
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + 'From_timeline_DClick.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + 'From_timeline_DClick.png', image_result)
            case.result = compare_result

        with uuid("b6b04178-16a0-4706-9a83-7673b244bd0d") as case:
            # open designer from hotkey f2
            time.sleep(1)
            title_designer_page.click_cancel()
            time.sleep(1)
            main_page.tap_NewWorkspace_hotkey()
            time.sleep(1)
            main_page.press_esc_key()
            media_room_page.select_media_content('Motion Graphics 011')
            tips_area_page.click_TipsArea_btn_insert(-1)
            timeline_page.select_timeline_media(track_index=0, clip_index=0)
            timeline_page.input_keyboard('F2')
            time.sleep(1)
            title_designer_page.set_timecode('00_00_05_00')
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                         file_name=Auto_Ground_Truth_Folder + 'From_timeline_F2.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + 'From_timeline_F2.png',
                                                          image_result)
            case.result = compare_result

    def test_1_1_4(self):
        # CASE 21~25
        with uuid("6308fb38-ef82-490a-80d6-90e43b3cbfe0") as case:
            # can't close pdr by hotkey when enter designer
            time.sleep(4)
            main_page.enter_room(1)
            title_room_page.select_specific_tag('Motion Graphics')
            media_room_page.select_media_content('Motion Graphics 002')
            title_room_page.select_RightClickMenu_ModifyTemplate()
            title_designer_page.mgt.handle_warning_msg(1)
            title_designer_page.mgt.click_warning_msg_ok()
            title_designer_page.click_maximize_btn()
            title_designer_page.tap_QuitPDR_hotkey()
            time.sleep(1)
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.window_title_designer,
                                                         file_name=Auto_Ground_Truth_Folder + '012.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + '012.png',
                                                         image_result)
            case.result = compare_result

        with uuid("f3906bd7-ac8d-4e1c-b0e8-c4bd1236198a") as case:
            # undo from edit menu
            time.sleep(1)
            title_designer_page.mgt.unfold_object_setting_tab()
            title_designer_page.mgt.set_rotation_value('45')
            title_designer_page.click_menu_bar_edit(1)
            time.sleep(1)
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + 'Undo_By_EditTab.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + 'Undo_By_EditTab.png',
                                                         image_result)
            case.result = compare_result

        with uuid("22af4ee6-b787-4e08-8a39-58480fe64806") as case:
            # redo from edit menu
            time.sleep(1)
            title_designer_page.click_menu_bar_edit(2)
            time.sleep(1)
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + 'Redo_By_EditTab.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + 'Redo_By_EditTab.png',
                                                         image_result)
            case.result = compare_result

        with uuid("f8780f82-6d2c-4d32-bbc6-0eb2df7649c9") as case:
            # undo by hotkey
            time.sleep(1)
            title_designer_page.tap_Undo_hotkey()
            time.sleep(1)
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + 'Undo_By_hotkey.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + 'Undo_By_hotkey.png',
                                                         image_result)
            case.result = compare_result

        with uuid("a7ab6d5e-0c6d-4669-90da-6c6da030d178") as case:
            # redo by hotkey f2
            time.sleep(2)
            title_designer_page.tap_Redo_hotkey()
            time.sleep(1)
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + 'Redo_By_hotkey.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + 'Redo_By_hotkey.png',
                                                         image_result)
            case.result = compare_result

    def test_1_1_5(self):
        # CASE 26~35
        with uuid("e0961dac-3fb5-44b3-9638-03b48bcada56") as case:
            # check title name
            time.sleep(4)
            main_page.enter_room(1)
            title_room_page.select_specific_tag('Motion Graphics')
            media_room_page.select_media_content('Motion Graphics 008')
            title_room_page.select_RightClickMenu_ModifyTemplate()
            title_designer_page.mgt.handle_warning_msg(1)
            title_designer_page.mgt.click_warning_msg_ok()
            title_designer_page.click_maximize_btn()
            time.sleep(1)
            a = title_designer_page.get_title()
            if a == 'Motion Graphics 008':
                case.result = True
            else:
                case.result = False

        with uuid("8bff303b-47c0-4b5a-9139-e3b5de89a583") as case:
            # open help
            time.sleep(1)
            result_status = title_designer_page.click_menu_bar_help(1)
            case.result = result_status

        with uuid("d3ca6c14-0719-4afc-b850-32619ad37ccf") as case:
            # zoom to 10% by zoom menu
            time.sleep(1)
            title_designer_page.mgt.click_viewer_zoom_menu('10%')
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + 'zoom_10.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + 'zoom_10.png',
                                                         image_result)
            case.result = compare_result

        with uuid("f6090b3e-389a-44e6-a033-4d0332ad0d93") as case:
            # zoom to 25% by zoom menu
            time.sleep(1)
            title_designer_page.mgt.click_viewer_zoom_menu('25%')
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + 'zoom_25.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + 'zoom_25.png',
                                                         image_result)
            case.result = compare_result

        with uuid("f1261dc8-20bc-4404-9806-b1ec1d7d9fd1") as case:
            # zoom to 50% by zoom menu
            time.sleep(1)
            title_designer_page.mgt.click_viewer_zoom_menu('50%')
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + 'zoom_50.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + 'zoom_50.png',
                                                         image_result)
            case.result = compare_result

        with uuid("8b6a6275-a1a8-4ee7-ba0b-9aa35a1917d4") as case:
            # zoom to 75% by zoom menu
            time.sleep(1)
            title_designer_page.mgt.click_viewer_zoom_menu('75%')
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + 'zoom_75.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + 'zoom_75.png',
                                                         image_result)
            case.result = compare_result

        with uuid("42618ed2-d60a-4f04-b62a-f7af6d01ef4a") as case:
            # zoom to 100% by zoom menu
            time.sleep(1)
            title_designer_page.mgt.click_viewer_zoom_menu('100%')
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + 'zoom_100.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + 'zoom_100.png',
                                                         image_result)
            case.result = compare_result

        with uuid("17429483-e728-4229-aa5f-490139c9db7f") as case:
            # zoom to 200% by zoom menu
            time.sleep(1)
            title_designer_page.mgt.click_viewer_zoom_menu('200%')
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + 'zoom_200.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + 'zoom_200.png',
                                                         image_result)
            case.result = compare_result

        with uuid("5acf6575-5bd7-4323-b7ef-9b439f6632fc") as case:
            # zoom to 300% by zoom menu
            time.sleep(1)
            title_designer_page.mgt.click_viewer_zoom_menu('300%')
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + 'zoom_300.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + 'zoom_300.png',
                                                         image_result)
            case.result = compare_result

        with uuid("4caa0415-648a-48e0-a111-313b6ceb2973") as case:
            # zoom to 400% by zoom menu
            time.sleep(1)
            title_designer_page.mgt.click_viewer_zoom_menu('400%')
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + 'zoom_400.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + 'zoom_400.png',
                                                         image_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_21(self):
        with uuid("""d123305c-297a-4c27-8ca3-c5a210414734
bf323ef4-0fc7-455f-880d-1f1e170e2459
8f5f61b8-5113-43c9-8a86-f42ba7ef5db6
975f2012-f58d-4856-93a3-8d662573029c
5669edea-2e7e-46ab-9ffb-bb5f40be49fc
278eb33e-348c-40ef-b7fc-ca07c8387703
67b1ae49-a292-418d-b1a4-dc52b336acea
bd1bbed8-8d38-43c0-a63b-32312484decc
362dab7a-2a45-4575-8eff-a3126300f890
ebb3f6df-ec29-4206-aa00-3a2015d622bc
5b6dce0c-bc6c-4f46-80d2-faf158f82385
65bb20fb-967e-4409-b3b1-570113f68ddf
3943bf43-d1f0-45da-8be7-767372386dc0
5cc0780f-08e3-4287-91d7-c5e9bf8d501d
95cdd00b-58e5-4ae1-8c90-e255210ea350
2b79fdac-ee86-4469-ac45-a5a58a99126b
cb5cdabe-ee93-4114-8722-2e134c8d79af
8dd0b798-0a69-42c2-afeb-49c942ca07ac
75ca0614-655f-4374-9681-11298855430a
2359a7e6-94a6-4d89-87c4-fae7ed2e0ff2
3e6ac88a-fc6e-4e72-bdd3-476366855615
84217281-2b15-4f7f-8263-dfa44297532b
29ca3003-dd08-4684-a2d1-8c367e80801f
9c5929c4-0e13-4e38-89bf-5089a0f46c2f
234fe143-1663-4f24-b6e3-e676b68007d5
531d0668-5015-41e4-a8cb-7ddc0a258d94
72e950df-588c-4b3f-94b4-cc0d801bbc84
61b422c7-70a9-4c78-8657-46e75ac36e0c
9bfe114d-08f0-4bca-b83d-dc3731add235
8631e135-ff6e-4733-9672-6b941c380856
01726d8e-a199-4588-8298-b6cae1b43a4b
d7952f75-677e-42ab-8974-a0c374f22c30
db32a353-30b6-45dd-be59-95ed4ab362b0
24099712-2cbd-4df5-b0e4-ed6beecdc370
0249110d-ca27-4db6-b0ae-85aefe673483
a8866c40-7f73-4c0c-a7c0-956608649d12
fbed6d3a-cfbb-4641-906f-930c4ce67dab
c06c1043-f3d3-4298-9689-2dab01f2d0a1
58ff77c7-523c-4ab0-9b6a-7b8edfbe1de5
1f9276d4-3b0a-40a3-ac3e-4a4e01818009
dc4f80fc-1ce5-4c27-93b9-f494946e23e1
a2e0c688-7ad9-43b4-bc1d-8bd0beffa025
e5bd8605-85c1-4d04-a298-84a7bb84ba11
65b65055-3be8-48a4-b12d-97990196fca9
d0ea5cc6-f4d2-40d7-b68f-1b49d5276616
deb813e3-97dc-4b70-91ec-cafb25741fb3
01a9e60a-947b-48d2-adf2-c4c6045e97a3
a7dccf5e-afdf-4260-b842-c3a3dca9458a
35733491-0e75-4eba-9bbd-6d46a021f14b
658a4865-b4e9-44c0-8dc9-3d01d32a931b
ec3f696b-20f7-4e5b-99ce-d40a2ecd31f8
8b7e4a95-e53a-4a51-9b96-b099531b8e66
4dc05475-1fdc-4e8a-add8-cd11654d0241
61e8394d-c886-4cc4-9436-d591adcc542d
13bf2d51-65c4-4d0b-a44c-0dd4aabf740c
093a1861-c22d-46b9-a3b0-173e00357d17
66fe1237-1e68-489d-bcdf-c599997b8bda
701c17ef-4de5-4ab7-8474-405de362fdd0
63c3796f-660a-445c-98fe-145dd35000d5
c3899941-0321-4e80-8a6a-5e48d93d3783
e806ec34-4b20-4814-84d3-615ea5166bc5
caa26d13-0d7a-4b56-b1f5-0511288be608
fae0ee13-af7c-4d23-b4eb-e8dea2bf1ad9
c9150327-e789-424d-90e0-ce8288068dd6
c65d28eb-10fe-4d3c-83d8-98b2a974321d
c540c40b-135d-43e3-adcd-25b972565a9e
1eb31f65-7a9d-4ed0-9e9e-801c2e91efbd
27b78552-87b3-462f-a6e7-7e111be86471
08ebdf05-af06-45d0-965e-d7096dcd541a
bf959a23-e03f-45c0-92a8-624c48cf9fb8
6142a6d7-1e93-45b2-a87b-dc6e9d47c443
29a93025-65d5-4636-a6b6-724484f2c827
ef59e0e5-933d-459d-a2c8-5e362847f517
6c3a4308-bcb9-4e41-8804-6f36373ff061
e160e697-867e-4c29-af99-56fdc903f9b7
cd3e4059-d054-46b4-be8f-d570f9d9a30a
c8c31dfc-ccb9-41d7-a228-474fabdf465d
da142049-c35f-4cae-94db-3dc03f317f20
70d2009d-fc14-4ea3-a9f3-3ff890484126""") as case:
            case.result = None
            case.fail_log = "*SKIP by AT*"