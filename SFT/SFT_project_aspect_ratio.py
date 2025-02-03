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
media_room_page = PageFactory().get_page_object('media_room_page', mwc)
effect_room_page = PageFactory().get_page_object('effect_room_page', mwc)
pip_room_page = PageFactory().get_page_object('pip_room_page', mwc)
particle_room_page = PageFactory().get_page_object('particle_room_page',mwc)
title_room_page = PageFactory().get_page_object('title_room_page',mwc)
transition_room_page = PageFactory().get_page_object('transition_room_page', mwc)

# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Project Aspect Ratio.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Project_Aspect_Ratio/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Project_Aspect_Ratio/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Project_Aspect_Ratio():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        yield mwc
        main_page.close_app()

    @classmethod
    def setup_class(cls):
        main_page.clear_cache()
        # for update the correct module start time of report (2021/04/20)
        now = datetime.datetime.now()
        report.add_ovinfo('time', now.time().strftime("%H:%M:%S"))
        report.start_time = time.time()
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_init('Project_Aspect_Ratio')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"Pre Cut result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
    def test_1_1_1_a(self):
        with uuid("1052c7f7-6f92-498d-8960-7d6c2bc83e81") as case:
            # 1.1.1 Original Project - 16by9 - Library preview should display correctly
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            main_page.insert_media('Skateboard 01.mp4')
            current_result = media_room_page.snapshot(locator = media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-1-1_OriginalProject_16by9.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-1_OriginalProject_16by9.png', current_result)
            case.result = compare_result
            main_page.save_project("Switch_16by9", app.testing_material + '/Project_Aspect_Ratio/')

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_1_b(self):
        with uuid("cbb5add3-f289-46ae-98a0-b4cca8372505") as case:
            # 1.1.1 Original Project - 4by3 - Library preview should display correctly
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            main_page.insert_media('Skateboard 01.mp4')
            main_page.set_project_aspect_ratio_4_3()
            current_result = media_room_page.snapshot(locator = media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-1-1_OriginalProject_4by3.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-1_OriginalProject_4by3.png', current_result)
            case.result = compare_result
            main_page.save_project("Switch_4by3", app.testing_material + '/Project_Aspect_Ratio/')

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_1_c(self):
        with uuid("27897322-acfe-4c55-985d-55e1f17e7867") as case:
            # 1.1.1 Original Project - 9by16 - Library preview should display correctly
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            main_page.insert_media('Skateboard 01.mp4')
            main_page.set_project_aspect_ratio_9_16()
            time.sleep(5)
            current_result = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-1-1_OriginalProject_9by16.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-1_OriginalProject_9by16.png', current_result)
            case.result = compare_result
            main_page.save_project("Switch_9by16", app.testing_material + '/Project_Aspect_Ratio/')

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_1_d(self):
        with uuid("ee55127b-3be8-48f6-8572-6517243dfff7") as case:
            # 1.1.1 Original Project - 1by1 - Library preview should display correctly
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            main_page.insert_media('Skateboard 01.mp4')
            main_page.set_project_aspect_ratio_1_1()
            time.sleep(5)
            current_result = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-1-1_OriginalProject_1by1.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-1_OriginalProject_1by1.png', current_result)
            case.result = compare_result
            main_page.save_project("Switch_1by1", app.testing_material + '/Project_Aspect_Ratio/')

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3_a(self):
        with uuid("cf88e29f-1f65-4149-91a6-e57081c6453d") as case:
            # 1.1.1 Save & Open Project - 4by3 - Able to save and open project with correct project aspect ratio
            time.sleep(5)
            main_page.tap_OpenProject_hotkey()
            main_page.handle_open_project_dialog(app.testing_material + '/Project_Aspect_Ratio/Switch_4by3.pds')
            main_page.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='no')
            time.sleep(5)
            current_result = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-1-1_OpenProject_4by3.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-1_OriginalProject_4by3.png', current_result)
            case.result = compare_result

        with uuid("984c9348-38e7-44a9-9af1-76162aa18464") as case:
            # 1.1.1 Save & Open Project - 4by3 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly
            time.sleep(5)
            current_result = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-1-1_OpenProject_4by3.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-1_OriginalProject_4by3.png', current_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3_b(self):
        with uuid("e78ea9b7-44ac-45a1-878e-22873af2d050") as case:
            # 1.1.1 Save & Open Project - 16by9 - Able to save and open project with correct project aspect ratio
            time.sleep(5)
            main_page.tap_OpenProject_hotkey()
            main_page.handle_open_project_dialog(app.testing_material + '/Project_Aspect_Ratio/Switch_16by9.pds')
            time.sleep(1)
            main_page.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='no')
            time.sleep(7)
            current_result = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-1-1_OpenProject_16by9.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-1_OriginalProject_16by9.png', current_result)
            case.result = compare_result

        with uuid("7d656a7d-3397-4ad0-84e2-f3732ad03434") as case:
            # 1.1.1 Save & Open Project - 16by9 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly
            time.sleep(5)
            current_result = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-1-1_OpenProject_16by9.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-1_OriginalProject_16by9.png', current_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3_c(self):
        with uuid("54a4377a-f7db-4016-b3ad-e27aa9183dd5") as case:
            # 1.1.1 Save & Open Project - 9by16 - Able to save and open project with correct project aspect ratio
            time.sleep(5)
            main_page.tap_OpenProject_hotkey()
            main_page.handle_open_project_dialog(app.testing_material + '/Project_Aspect_Ratio/Switch_9by16.pds')
            main_page.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='no')
            time.sleep(5)
            current_result = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-1-1_OpenProject_9by16.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-1_OriginalProject_9by16.png', current_result)
            case.result = compare_result

        with uuid("5e521814-11fc-4025-a3b2-2a67e3ba1d61") as case:
            # 1.1.1 Save & Open Project - 9by16 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly
            time.sleep(5)
            current_result = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-1-1_OpenProject_9by16.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-1_OriginalProject_9by16.png', current_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3_d(self):
        with uuid("5a0a9284-1637-4170-945e-cfe0a7c7d722") as case:
            # 1.1.1 Save & Open Project - 1by1 - Able to save and open project with correct project aspect ratio
            time.sleep(5)
            main_page.tap_OpenProject_hotkey()
            main_page.handle_open_project_dialog(app.testing_material + '/Project_Aspect_Ratio/Switch_1by1.pds')
            main_page.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='no')
            time.sleep(5)
            current_result = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-1-1_OpenProject_1by1.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-1_OriginalProject_1by1.png', current_result)
            case.result = compare_result

        with uuid("04518834-65a0-4738-9690-84aae4448b83") as case:
            # 1.1.1 Save & Open Project - 1by1 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly
            time.sleep(5)
            current_result = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-1-1_OpenProject_1by1.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-1_OriginalProject_1by1.png', current_result)
            case.result = compare_result


    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid("51412932-39f7-4a08-906a-32c6e99b2d90") as case:
            # 1.1.2 Add Clip to timeline & Switch Project - 16by9 - Switch project aspect ratio correctly
            time.sleep(5)
            main_page.insert_media('Skateboard 01.mp4', 'no')
            result_status = main_page.set_project_aspect_ratio_16_9()
            logger(result_status)
            case.result = result_status

        with uuid("3ea73749-5ede-47ad-87da-79c408de8666") as case:
            # 1.1.2 Add Clip to timeline & Switch Project - 16by9 - Timeline preview display correctly
            current_image = effect_room_page.snapshot(locator=L.main.timeline.table_view, file_name=Auto_Ground_Truth_Folder + '1-1-2_16by9_TimelinePreview.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '1-1-2_16by9_TimelinePreview.png', current_image)
            case.result = compare_result

        with uuid("588fa0cd-01c3-4cb9-9271-3cfc44910afd") as case:
            # 1.1.2 Add Clip to timeline & Switch Project - 4by3 - Switch project aspect ratio correctly
            result_status = main_page.set_project_aspect_ratio_4_3()
            logger(result_status)
            case.result = result_status

        with uuid("16dead13-992c-456f-adf1-be9f34473064") as case:
            # 1.1.2 Add Clip to timeline & Switch Project - 4by3 - Timeline preview display correctly
            current_image = effect_room_page.snapshot(locator=L.main.timeline.table_view, file_name=Auto_Ground_Truth_Folder + '1-1-2_4by3_TimelinePreview.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '1-1-2_4by3_TimelinePreview.png', current_image)
            case.result = compare_result

        with uuid("f6d00f16-d8ca-4a8a-80d1-a012363a8ee2") as case:
            # 1.1.2 Add Clip to timeline & Switch Project - 9by16 - Switch project aspect ratio correctly
            result_status = main_page.set_project_aspect_ratio_9_16()
            logger(result_status)
            case.result = result_status

        with uuid("00d90bf9-86e9-4c37-a2b2-736af9c69b7b") as case:
            # 1.1.2 Add Clip to timeline & Switch Project - 9by16 - Timeline preview display correctly
            current_image = effect_room_page.snapshot(locator=L.main.timeline.table_view, file_name=Auto_Ground_Truth_Folder + '1-1-2_9by16_TimelinePreview.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '1-1-2_9by16_TimelinePreview.png', current_image)
            case.result = compare_result

        with uuid("690b4e2b-96c2-4813-8b06-6cc2aed30471") as case:
            # 1.1.2 Add Clip to timeline & Switch Project - 1by1 - Switch project aspect ratio correctly
            result_status = main_page.set_project_aspect_ratio_1_1()
            logger(result_status)
            case.result = result_status

        with uuid("24a12258-341c-4d09-b3f0-c75d04f884c9") as case:
            # 1.1.2 Add Clip to timeline & Switch Project - 1by1 - Timeline preview display correctly
            current_image = effect_room_page.snapshot(locator=L.main.timeline.table_view, file_name=Auto_Ground_Truth_Folder + '1-1-2_1by1_TimelinePreview.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '1-1-2_1by1_TimelinePreview.png', current_image)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        with uuid("1f3167cf-3aa0-42f3-b5c0-e9e73d663b8d") as case:
            # 1.1.4 Add Sample to Timeline - 4by3 - Prompt a Aspect Ratio Conflict msg if the aspect ratio is different between sample and project aspect ratio
            time.sleep(5)
            main_page.set_project_aspect_ratio_4_3()
            media_room_page.import_media_file(app.testing_material + '/Project_Aspect_Ratio/9by16.mp4')
            media_room_page.high_definition_video_confirm_dialog_click_no()
            main_page.insert_media('9by16.mp4', 'no')
            case.result = True

        with uuid("640fed33-20bf-47b1-a897-1c0c422c5e7e") as case:
            # 1.1.4 Add Sample to Timeline - 4by3 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly no matter keep or change project aspect ratio
            current_result = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-1-4_ThumbnailPreview_4by3.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-4_ThumbnailPreview_4by3.png', current_result)
            case.result = compare_result

        with uuid("e466cd9d-68bc-4448-acb4-b7bacde5d12a") as case:
            # 1.1.4 Add Sample to Timeline - 16by9 - Prompt a Aspect Ratio Conflict msg if the aspect ratio is different between sample and project aspect ratio
            main_page.click_undo()
            main_page.set_project_aspect_ratio_16_9()
            main_page.insert_media('9by16.mp4', 'no')
            case.result = True

        with uuid("1a4122cb-96ff-4be2-b0df-4acbd1b64e36") as case:
            # 1.1.4 Add Sample to Timeline - 16by9 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly no matter keep or change project aspect ratio
            current_result = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-1-4_ThumbnailPreview_16by9.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-4_ThumbnailPreview_16by9.png', current_result)
            case.result = compare_result

        with uuid("2410971f-d1c1-4eba-966c-4af17356bae0") as case:
            # 1.1.4 Add Sample to Timeline - 1by1 - Prompt a Aspect Ratio Conflict msg if the aspect ratio is different between sample and project aspect ratio
            main_page.click_undo()
            main_page.set_project_aspect_ratio_1_1()
            main_page.insert_media('9by16.mp4', 'no')
            case.result = True

        with uuid("69b48ee8-2b3e-4f4a-b4ee-e4b9035b75ea") as case:
            # 1.1.4 Add Sample to Timeline - 1by1 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly no matter keep or change project aspect ratio
            current_result = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-1-4_ThumbnailPreview_1by1.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-4_ThumbnailPreview_1by1.png', current_result)
            case.result = compare_result

        with uuid("5011d568-f718-4519-9937-3cb57c668f35") as case:
            # 1.1.4 Add Sample to Timeline - 9by16 - Prompt a Aspect Ratio Conflict msg if the aspect ratio is different between sample and project aspect ratio
            main_page.click_undo()
            main_page.set_project_aspect_ratio_9_16()
            main_page.insert_media('Skateboard 01.mp4', 'no')
            case.result = True

        with uuid("836212d8-743d-4886-8a76-969c962865a0") as case:
            # 1.1.4 Add Sample to Timeline - 9by16 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly no matter keep or change project aspect ratio
            current_result = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-1-4_ThumbnailPreview_9by16.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-4_ThumbnailPreview_9by16.png', current_result)
            case.result = compare_result

        with uuid("bb0487c8-63bc-4c93-8638-52b36ae4664a") as case:
            # 1.1.4 Add Sample to Timeline - Prompt a Aspect Ratio Conflict msg --> [Yes] - Change project aspect ratio successfully
            main_page.click_undo()
            main_page.set_project_aspect_ratio_9_16()
            main_page.insert_media('Skateboard 01.mp4', 'yes')
            case.result = True

        with uuid("fc0dbe36-5b55-44e5-835e-3a88f8dceaa6") as case:
            # 1.1.4 Add Sample to Timeline - Prompt a Aspect Ratio Conflict msg --> [Yes] - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly after change project aspect ratio
            current_result = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-1-4_ChangeProjectAspectRatio.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-4_ChangeProjectAspectRatio.png', current_result)
            case.result = compare_result

        with uuid("f4a3a747-3aa7-42c6-9a1e-807184da0aa4") as case:
            # 1.1.4 Add Sample to Timeline - Prompt a Aspect Ratio Conflict msg --> [No] - Change project aspect ratio successfully
            main_page.click_undo()
            main_page.set_project_aspect_ratio_9_16()
            main_page.insert_media('Skateboard 01.mp4', 'no')
            case.result = True

        with uuid("51faefff-75ef-4f5c-bea4-de7ea6ead2c8") as case:
            # 1.1.4 Add Sample to Timeline - Prompt a Aspect Ratio Conflict msg --> [No] - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly after change project aspect ratio
            current_result = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + '1-1-4_KeepProjectAspectRatio.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + '1-1-4_KeepProjectAspectRatio.png', current_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):
        with uuid("18861671-b139-4dc6-9129-adf57e5488fd") as case:
            # 1.1.6 Add Effect to Timeline Clip - 4by3 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly
            time.sleep(5)
            main_page.set_project_aspect_ratio_4_3()
            main_page.insert_media('Skateboard 01.mp4', 'no')
            main_page.enter_room(3)
            effect_room_page.search_and_input_text('pop')
            effect_room_page.right_click_addto_timeline('Pop Art Wall')
            main_page.select_timeline_media('Pop Art Wall')
            current_image = effect_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '1-1-6_EffectRoom_4by3.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '1-1-6_EffectRoom_4by3.png', current_image)
            case.result = compare_result

        with uuid("9120e95e-5ff5-40b3-a835-20276267b366") as case:
            # 1.1.6 Add Effect to Timeline Clip - 16b9 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly
            main_page.set_project_aspect_ratio_16_9()
            current_image = effect_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '1-1-6_EffectRoom_16by9.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '1-1-6_EffectRoom_16by9.png', current_image)
            case.result = compare_result

        with uuid("39cafb9d-a987-4375-91de-c06efa8c02c7") as case:
            # 1.1.6 Add Effect to Timeline Clip - 9by16 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly
            main_page.set_project_aspect_ratio_9_16()
            current_image = effect_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '1-1-6_EffectRoom_9by16.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '1-1-6_EffectRoom_9by16.png', current_image)
            case.result = compare_result

        with uuid("1def137a-4213-45b7-85ed-9b8a4d10bded") as case:
            # 1.1.6 Add Effect to Timeline Clip - 1by1 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly
            main_page.set_project_aspect_ratio_1_1()
            current_image = effect_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '1-1-6_EffectRoom_1by1.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '1-1-6_EffectRoom_1by1.png', current_image)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_7(self):
        with uuid("9fc3b4b7-2561-4ee5-be2f-10c2494c1164") as case:
            # 1.1.7 Add PiP to Timeline - 4by3 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly
            time.sleep(5)
            main_page.enter_room(4)
            main_page.set_project_aspect_ratio_4_3()
            pip_room_page.hover_library_media('Dialog_06')
            pip_room_page.select_RightClickMenu_AddToTimeline()
            #main_page.set_timeline_timecode('00_00_02_00')
            time.sleep(1)
            current_image = pip_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '1-1-7_PIP_4by3.png')
            compare_result = pip_room_page.compare(Ground_Truth_Folder + '1-1-7_PIP_4by3.png', current_image)
            case.result = compare_result

        with uuid("14481a5e-75a9-4e38-8069-25202d69aafc") as case:
            # 1.1.7 Add PiP to Timeline - 16by9 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly
            main_page.set_project_aspect_ratio_16_9()
            current_image = pip_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '1-1-7_PIP_16by9.png')
            compare_result = pip_room_page.compare(Ground_Truth_Folder + '1-1-7_PIP_16by9.png', current_image)
            case.result = compare_result

        with uuid("b6785884-938d-4e97-9c80-a02ffa60b74d") as case:
            # 1.1.7 Add PiP to Timeline - 9by16 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly
            main_page.set_project_aspect_ratio_9_16()
            current_image = pip_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '1-1-7_PIP_9by16.png')
            compare_result = pip_room_page.compare(Ground_Truth_Folder + '1-1-7_PIP_9by16.png', current_image)
            case.result = compare_result

        with uuid("7f729d3c-a0e2-4236-9f91-76c8776e489b") as case:
            # 1.1.7 Add PiP to Timeline - 1by1 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly
            main_page.set_project_aspect_ratio_1_1()
            current_image = pip_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '1-1-7_PIP_1by1.png')
            compare_result = pip_room_page.compare(Ground_Truth_Folder + '1-1-7_PIP_1by1.png', current_image)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_8(self):
        with uuid("d99ddd76-ef84-40f7-8560-5d967080b6c5") as case:
            # 1.1.8 Add Particle to Timeline - 4by3 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly
            time.sleep(5)
            particle_room_page.tap_ParticleRoom_hotkey()
            main_page.set_project_aspect_ratio_4_3()
            media_room_page.select_media_content('Maple')
            particle_room_page.select_RightClickMenu_AddToTimeline()
            main_page.set_timeline_timecode('00_00_05_00')
            time.sleep(DELAY_TIME)
            current_image = particle_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '1-1-8_Particle_4by3.png')
            compare_result = particle_room_page.compare(Ground_Truth_Folder + '1-1-8_Particle_4by3.png', current_image)
            case.result = compare_result

        with uuid("296df3e4-72ec-4bbc-a127-9ba36bf40992") as case:
            # 1.1.8 Add Particle to Timeline - 16by9 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly
            main_page.set_project_aspect_ratio_16_9()
            time.sleep(DELAY_TIME)
            main_page.set_timeline_timecode('00_00_00_00')
            time.sleep(DELAY_TIME)
            main_page.set_timeline_timecode('00_00_05_00')
            time.sleep(DELAY_TIME)
            current_image = particle_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '1-1-8_Particle_16by9.png')
            compare_result = particle_room_page.compare(Ground_Truth_Folder + '1-1-8_Particle_16by9.png', current_image)
            case.result = compare_result

        with uuid("f68de71e-0eda-4b0b-bf46-bd934b94e1cc") as case:
            # 1.1.8 Add Particle to Timeline - 9by16 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly
            main_page.set_project_aspect_ratio_9_16()
            time.sleep(DELAY_TIME)
            main_page.set_timeline_timecode('00_00_00_00')
            time.sleep(DELAY_TIME)
            main_page.set_timeline_timecode('00_00_05_00')
            time.sleep(DELAY_TIME)
            current_image = particle_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '1-1-8_Particle_9by16.png')
            compare_result = particle_room_page.compare(Ground_Truth_Folder + '1-1-8_Particle_9by16.png', current_image)
            case.result = compare_result

        with uuid("dd221693-5eb0-467d-a62c-13ba46d9264e") as case:
            # 1.1.8 Add Particle to Timeline - 1by1 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly
            main_page.set_project_aspect_ratio_1_1()
            time.sleep(DELAY_TIME)
            main_page.set_timeline_timecode('00_00_00_00')
            time.sleep(DELAY_TIME)
            main_page.set_timeline_timecode('00_00_05_00')
            time.sleep(DELAY_TIME)
            current_image = particle_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '1-1-8_Particle_1by1.png')
            compare_result = particle_room_page.compare(Ground_Truth_Folder + '1-1-8_Particle_1by1.png', current_image)
            case.result = compare_result


    def test_1_1_9(self):
        with uuid("14161c5c-eab9-48b8-8f9b-1c35bee0af3f") as case:
            # 1.1.9 Add title to Timeline - 4by3 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            title_room_page.set_project_aspect_ratio_4_3()
            title_room_page.select_LibraryRoom_category('Text Only')
            media_room_page.select_media_content('Default')
            title_room_page.select_RightClickMenu_AddToTimeline()
            time.sleep(1)
            current_image = title_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '1-1-9_Title_4by3.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + '1-1-9_Title_4by3.png', current_image)
            case.result = compare_result

        with uuid("44a9907e-8713-4de3-b3f4-4fe1eef226b4") as case:
            # 1.1.9 Add title to Timeline - 16by9 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly
            title_room_page.set_project_aspect_ratio_16_9()
            time.sleep(1)
            current_image = title_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '1-1-9_Title_16by9.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + '1-1-9_Title_16by9.png', current_image)
            case.result = compare_result

        with uuid("7b7bf926-284e-4818-b3a3-44f5e8e5601a") as case:
            # 1.1.9 Add title to Timeline - 9by16 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly
            title_room_page.set_project_aspect_ratio_9_16()
            time.sleep(1)
            current_image = title_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '1-1-9_Title_9by16.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + '1-1-9_Title_9by16.png', current_image)
            case.result = compare_result

        with uuid("1726440d-6e01-437b-8ff9-6c5d5554f2d6") as case:
            # 1.1.9 Add title to Timeline - 1by1 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly
            title_room_page.set_project_aspect_ratio_1_1()
            time.sleep(1)
            current_image = title_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '1-1-9_Title_1by1.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + '1-1-9_Title_1by1.png', current_image)
            case.result = compare_result

    def test_1_1_10(self):
        with uuid("e2a912e5-8807-4bf6-9a87-944db8a6e7fe") as case:
            # 1.1.10 Add transition to Timeline - 16by9 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly
            time.sleep(5)
            main_page.set_project_aspect_ratio_16_9()
            main_page.hover_library_media('Skateboard 01.mp4')
            media_room_page.library_clip_context_menu_insert_on_selected_track()
            transition_room_page.tap_TransitionRoom_hotkey()
            time.sleep(1)
            transition_room_page.apply_LibraryMenu_Fading_Transition_to_all_video('Prefix')
            main_page.set_timeline_timecode('00_00_01_08')
            current_image = title_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '1-1-10_Transition_16by9.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + '1-1-10_Transition_16by9.png', current_image)
            case.result = compare_result

        with uuid("9975431a-3ed4-47fc-857f-9c2ef41a2558") as case:
            # 1.1.10 Add transition to Timeline - 4by3 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly
            time.sleep(5)
            main_page.set_project_aspect_ratio_4_3()
            time.sleep(DELAY_TIME)
            main_page.set_timeline_timecode('00_00_00_00')
            time.sleep(DELAY_TIME)
            main_page.set_timeline_timecode('00_00_01_08')
            time.sleep(DELAY_TIME)
            current_image = title_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '1-1-10_Transition_4by3.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + '1-1-10_Transition_4by3.png', current_image)
            case.result = compare_result

        with uuid("09ef0478-0f3d-49ac-ad01-89f7bde8506e") as case:
            # 1.1.10 Add transition to Timeline - 9by16 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly
            time.sleep(5)
            main_page.set_project_aspect_ratio_9_16()
            time.sleep(DELAY_TIME)
            main_page.set_timeline_timecode('00_00_00_00')
            time.sleep(DELAY_TIME)
            main_page.set_timeline_timecode('00_00_01_08')
            time.sleep(DELAY_TIME)
            current_image = title_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '1-1-10_Transition_9by16.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + '1-1-10_Transition_9by16.png', current_image)
            case.result = compare_result

        with uuid("6a05f0d0-b9c3-4199-8351-def4df21ddbd") as case:
            # 1.1.10 Add transition to Timeline - 1by1 - Thumbnail / Preview should fit aspect ratio project w/ 8 dot controls correctly
            time.sleep(5)
            main_page.set_project_aspect_ratio_1_1()
            time.sleep(DELAY_TIME)
            main_page.set_timeline_timecode('00_00_00_00')
            time.sleep(DELAY_TIME)
            main_page.set_timeline_timecode('00_00_01_08')
            time.sleep(DELAY_TIME)
            current_image = title_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '1-1-10_Transition_1by1.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + '1-1-10_Transition_1by1.png', current_image)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    52f8ff7f-0f53-47d3-8408-057bd6ed5bce
                    e64f6a0e-3a42-4328-8483-fc222408a6dc
                    0d7f4719-2548-4643-a6ad-c181a40431f2
                    5df1d166-5ae1-4c22-b006-7e3b325b8849
                    97fef79d-be6e-4b71-b946-33caf90b90dd
                    a01c3a56-64e2-4fe0-89ce-4743020b3b68
                    2631d16e-caf7-49b0-b01c-d61e7b0b9eac
                    7404f722-6242-47f8-a8e1-e953266785d3
                ''') as case:
            case.result = None
            case.fail_log = "*SKIP by AT*"