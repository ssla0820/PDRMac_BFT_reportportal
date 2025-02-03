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
precut_page = PageFactory().get_page_object('precut_page', mac)

# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="Pre Cut.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
#Ground_Truth_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/SFT/GroundTruth/Pre_Cut/'
#Auto_Ground_Truth_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/SFT/ATGroundTruth/Pre_Cut/'
#Test_Material_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/Material/'
Ground_Truth_Folder = app.ground_truth_root + '/Pre_Cut/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Pre_Cut/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Pre_Cut():
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

    @classmethod
    def setup_class(cls):
        main_page.clear_cache()
        # for update the correct module start time of report (2021/04/20)
        now = datetime.datetime.now()
        report.add_ovinfo('time', now.time().strftime("%H:%M:%S"))
        report.start_time = time.time()
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_init('Pre_Cut')

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
    def test_1_1_1(self):
        with uuid("bbbc69fe-0af2-4d74-91a5-9b8a6752fc89") as case:
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            current_result = media_room_page.library_clip_context_menu_precut()
            # [I8] Right Click Menu > Select (Precut...)
            case.result = current_result

        with uuid("2d81bdfc-5997-45eb-a386-518b74b053cd") as case:
            # [I9] Check open PreCut Window
            if not precut_page.exist(L.precut.main_window):
                case.result = False
            # Check find Single Trim tab
            if not precut_page.exist(L.precut.single_trim):
                case.result = False
            else:
                case.result = True

        with uuid("ffbcd621-9c3e-4c69-8501-e9648566e9d2") as case:
            # [I12] Check Caption bar
            str_Title = precut_page.get_precut_title()
            if str_Title == 'Skateboard 01.mp4':
                case.result = True
            else:
                case.result = False

        with uuid("35240ff2-7d4c-4adf-932c-1065ec290fb8") as case:
            # [I13] Maximize/restore window size
            img_before = precut_page.screenshot()
            precut_page.click_window_max_restore_btn()
            current_result = precut_page.wait_for_image_changes(img_before)
            case.result = current_result
            if current_result is True:
                precut_page.click_window_max_restore_btn()

        with uuid("4fe5eaf7-3120-4fe7-b3f5-698b312c9c03") as case:
            # [I14] Close dialog without changes
            current_result = precut_page.close_precut_window()
            case.result = current_result


    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid("8a4cf651-3cd0-41dd-bf39-2f59ffa7091b") as case:
            # [I10] Pre Cut function should disable for photo content.
            current_result = precut_page.get_precut_status('Food.jpg')
            if current_result is False:
                case.result = True
            else:
                case.result = False

        with uuid("1702fe57-697e-43d5-8fa2-7c4cc403bc87") as case:
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            media_room_page.library_clip_context_menu_precut()
            item = precut_page.exist(L.precut.single_trim)
            if item.AXEnabled is not True:
                logger('Enter PreCut, Single Trim tab is not enabled.')
                raise Exception

            # [I25] 1. Move indicator to the beginning point then click hotkey "I"
            precut_page.edit_precut_single_trim_drag_slider(0, 0, 3, 0)
            precut_page.tap_MarkIn_onLibraryPreview_hotkey()
            check_in_pos = precut_page.get_single_trim_precut_in_position()
            if check_in_pos == '00;00;03;00':
                case.result = True
            else:
                case.result = False

        with uuid("3f14a926-fffa-4017-b60e-221df09660bc") as case:
            # [I26] 2. Clip duration would be update correctly
            check_duration = precut_page.get_precut_single_trim_duration()
            if check_duration == '00;00;07;00':
                case.result = True
            else:
                case.result = False

        with uuid("e3a34871-4f9c-438e-a187-04455ee79f08") as case:
            # [I34] 1. Trim duration is not fixed
            precut_page.edit_precut_single_trim_drag_slider(0, 0, 1, 18)
            precut_page.tap_MarkIn_onLibraryPreview_hotkey()
            check_duration = precut_page.get_precut_single_trim_duration()
            if check_duration == '00;00;08;12':
                case.result = True
            else:
                case.result = False

        with uuid("f884fe06-9f6a-4ff8-9cf3-edf4f9b940d6") as case:
            # [I27] 3. In position timecode & instant preview would be updated correctly
            check_in_pos = precut_page.get_single_trim_precut_in_position()
            if check_in_pos == '00;00;01;18':
                check_in_pos = True
            else:
                check_in_pos = False

            time.sleep(2)
            current_image = precut_page.snapshot(locator=L.precut.single_trim_in_position_thumbnail,
                                                 file_name=Auto_Ground_Truth_Folder + 'I27.png')

            logger(current_image)
            check_thumbnail = precut_page.compare(Ground_Truth_Folder + 'I27.png', current_image)
            # logger(check_thumbnail)
            case.result = check_in_pos and check_thumbnail
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        with uuid("931e7b37-2112-4a5e-af6b-47d7c4605317") as case:
            # [I17] Switch between Single and Multi Trim correctly
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            media_room_page.library_clip_context_menu_precut()
            item = precut_page.exist(L.precut.single_trim)
            if item.AXEnabled is not True:
                logger('Enter PreCut, Single Trim tab is not enabled.')
                raise Exception
            precut_page.edit_precut_switch_trim_mode('Multi')
            item = precut_page.exist(L.precut.multi_trim)
            current_result = item.AXEnabled
            case.result = current_result

        with uuid("79c839e5-3476-46c4-a1b8-ac3ee45a055f") as case:
            # [I94] Move indicator to the beginning point then click mark in button
            img_before = precut_page.snapshot(locator=L.precut.main_window)
            precut_page.drag_multi_trim_slider(0, 0, 3, 0)
            precut_page.wait_for_image_changes(img_before, locator=L.precut.main_window)

            current_result = precut_page.tap_multi_trim_mark_in()
            case.result = current_result

        with uuid("56171f54-f084-437e-9916-7f6182cdfc70") as case:
            # [I97] Move indicator to the ending point then click mark out button
            img_before = precut_page.snapshot(locator=L.precut.main_window)
            precut_page.drag_multi_trim_slider(0, 0, 7, 0)
            precut_page.wait_for_image_changes(img_before, locator=L.precut.main_window)

            current_result = precut_page.tap_multi_trim_mark_out()
            case.result = current_result

        with uuid("417fa8e3-4c00-4ad9-ab95-cf28026d58ad") as case:
            # [I96] Mark in at another position for multi trim correctly
            with uuid("5ef8e260-c2fb-4c40-a594-0935cb6da5a3") as case:
                # [I95] Move indicator to the beginning point then click hotkey "I"
                img_before = precut_page.snapshot(locator=L.precut.main_window)
                precut_page.drag_multi_trim_slider(0, 0, 8, 3)
                precut_page.wait_for_image_changes(img_before, locator=L.precut.main_window)

                precut_page.tap_MarkIn_onLibraryPreview_hotkey()
                current_image = precut_page.snapshot(locator=L.precut.multi_trim_slider, file_name=Auto_Ground_Truth_Folder + 'I95.png')
                logger(f"{current_image=}")
                compare_result = precut_page.compare(Ground_Truth_Folder + 'I95.png', current_image)
                case.result = compare_result
            case.result = compare_result

        with uuid("e0e93ace-12f0-428d-a45f-a467be017f9e") as case:
            # [I99] Mark out at another position for multi trim correctly
            with uuid("09dc92bf-22fa-41ef-8cc8-ba2151b1acac") as case:
                # [I98] Move indicator to the ending point then click hotkey "O"
                img_before = precut_page.snapshot(locator=L.precut.main_window)
                precut_page.drag_multi_trim_slider(0, 0, 10, 0)
                precut_page.wait_for_image_changes(img_before, locator=L.precut.main_window)

                precut_page.tap_MarkOut_onLibraryPreview_hotkey()
                current_image = precut_page.snapshot(locator=L.precut.multi_trim_slider, file_name=Auto_Ground_Truth_Folder + 'I98.png')
                logger(f"{current_image=}")
                compare_result = precut_page.compare(Ground_Truth_Folder + 'I98.png', current_image)
                case.result = compare_result
            case.result = compare_result

        with uuid("4b9287fb-4762-4c61-afc1-1c8262416388") as case:
            # [I18] Show warning to remind user if interrupt multi trim process
            precut_page.edit_precut_switch_trim_mode('Single')
            precut_page.handle_changes_not_applied_want_continue()
            item = precut_page.exist(L.precut.single_trim)
            current_result = item.AXEnabled
            case.result = current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        # Select Skateboard 03.mp4
        main_page.select_library_icon_view_media('Skateboard 03.mp4')
        media_room_page.library_clip_context_menu_precut()
        item = precut_page.exist(L.precut.single_trim)
        if item.AXEnabled is not True:
            logger('Enter PreCut, Single Trim tab is not enabled.')
            raise Exception

        with uuid("44135c83-6220-4b15-bc17-a9f2a76fd1c0") as case:
            # [I22] 1. Move indicator to the beginning point then click mark in button
            precut_page.edit_precut_single_trim_drag_slider(0, 0, 4, 10)
            precut_page.tap_single_trim_mark_in()

            # Note: locator "multi_trim_slider" = single trim > slider
            current_image = precut_page.snapshot(locator=L.precut.multi_trim_slider,
                                                 file_name=Auto_Ground_Truth_Folder + 'I22.png')
            #logger(f"{current_image=}")
            compare_result = precut_page.compare(Ground_Truth_Folder + 'I22.png', current_image)
            case.result = compare_result
        with uuid("1324cdcc-3666-43b2-b6da-b686eb714f1f") as case:
            # [I23] 2. Clip duration would be update correctly
            current_duration = precut_page.get_precut_single_trim_duration()
            #logger(current_duration)
            if current_duration == '00;00;05;20':
                case.result = True
            else:
                case.result = False

        with uuid("0d901e47-d32c-4226-9982-cb6bf1349b0b") as case:
            # [I24] 3. In position timecode & instant preview would be updated correctly
            if precut_page.get_single_trim_precut_in_position() == '00;00;04;10':
                check_timecode = True
            else:
                check_timecode = False
            #logger(check_timecode)
            current_image = precut_page.snapshot(locator=L.precut.single_trim_in_position_thumbnail,
                                                 file_name=Auto_Ground_Truth_Folder + 'I24.png')

            check_thumbnail = precut_page.compare(Ground_Truth_Folder + 'I24.png', current_image)
            #logger(check_thumbnail)
            case.result = check_timecode and check_thumbnail

        with uuid("b7ee0178-93d3-4768-8f6b-4c7376c1185b") as case:
            # [I28] 1. Move indicator to the ending point then click mark out button
            precut_page.edit_precut_single_trim_drag_slider(0, 0, 6, 10)
            precut_page.tap_single_trim_mark_out()

            # Note: locator "multi_trim_slider" = single trim > slider
            current_image = precut_page.snapshot(locator=L.precut.multi_trim_slider,
                                                 file_name=Auto_Ground_Truth_Folder + 'I28.png')
            #logger(f"{current_image=}")
            compare_result = precut_page.compare(Ground_Truth_Folder + 'I28.png', current_image)
            case.result = compare_result

        with uuid("db15e4c1-eafa-4361-87bd-436caa947a02") as case:
            # [I29] 2. Clip duration would be update correctly
            current_duration = precut_page.get_precut_single_trim_duration()
            #logger(current_duration)
            if current_duration == '00;00;02;00':
                case.result = True
            else:
                case.result = False

        with uuid("2f0e9ef6-e1be-4f1b-a062-a9fb61166d6d") as case:
            # [I30] 3. Out position timecode & instant preview would be updated correctly
            if precut_page.get_single_trim_precut_in_position() == '00;00;04;10':
                check_timecode = True
            else:
                check_timecode = False
            #logger(check_timecode)
            current_image = precut_page.snapshot(locator=L.precut.single_trim_out_position_thumbnail,
                                                 file_name=Auto_Ground_Truth_Folder + 'I30.png')

            check_thumbnail = precut_page.compare(Ground_Truth_Folder + 'I30.png', current_image)
            #logger(check_thumbnail)
            case.result = check_timecode and check_thumbnail

        with uuid("427db4ff-1cf8-40f6-ace0-60fb33f2fa51") as case:
            # [I135] Cancel > Single Trim > Close Pre Cut window and trim result is not applied
            precut_page.click_cancel()
            precut_page.handle_save_change_before_leaving(option=1)

            if not precut_page.exist(L.precut.single_trim):
                current_library = precut_page.snapshot(locator=precut_page.area.library_icon_view, file_name=Auto_Ground_Truth_Folder + 'I135.png')

            logger(current_library)
            check_library_preview = precut_page.compare(Ground_Truth_Folder + 'I135.png', current_library)
            case.result = check_library_preview

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        with uuid("c1b5e15a-8c4b-4a9a-8bd7-600b5674dba9") as case:
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            media_room_page.library_clip_context_menu_precut()
            item = precut_page.exist(L.precut.single_trim)
            if item.AXEnabled is not True:
                logger('Enter PreCut, Single Trim tab is not enabled.')
                raise Exception

            # [I64] 1. Set 00:00:00:00 as default
            check_default = precut_page.get_single_trim_precut_in_position()
            if check_default == '00;00;00;00':
                case.result = True
            else:
                case.result = False

        with uuid("a8ac3fce-3af3-4fb7-8fc6-cb346f936700") as case:
            # [I63] Is 00:00:00:00
            precut_page.click_precut_single_trim_in_position_arrow_button(1)
            check_default = precut_page.get_single_trim_precut_in_position()
            if check_default == '00;00;00;00':
                case.result = True
            else:
                case.result = False

        with uuid("286230be-01f3-497e-89e1-60c3830548cb") as case:
            # [I60] 1. In position would increase 1 frame for each click and update the preview thumbnail
            for x in range(25):
                precut_page.click_precut_single_trim_in_position_arrow_button(0)

            time.sleep(DELAY_TIME)
            current_image = precut_page.snapshot(locator=L.precut.single_trim_in_position_thumbnail,
                                                 file_name=Auto_Ground_Truth_Folder + 'I60.png')

            logger(current_image)
            check_thumbnail = precut_page.compare(Ground_Truth_Folder + 'I60.png', current_image)
            case.result = check_thumbnail

        with uuid("8d4d1a2e-7645-4326-a897-9f7f6606e454") as case:
            # [I66] Max: Total Duration - 1 frame
            with uuid("11ea33d4-d606-448e-896d-6d419d62e626") as case:
                # [I54] 1. Input new in position timecode by keyboard
                precut_page.set_single_trim_precut_in_position(value='00_10_30')
                check_default = precut_page.get_single_trim_precut_in_position()
                if check_default == '00;00;09;29':
                    case.result = True
                else:
                    case.result = False
            if check_default == '00;00;09;29':
                case.result = True
            else:
                case.result = False

        with uuid("2314b6ec-bd44-4dd4-93c9-13c8734e8f4b") as case:
            # [I78] 1. Display original clip duration for 1st entry
            check_default = precut_page.get_single_trim_precut_out_position()
            if check_default == '00;00;10;00':
                case.result = True
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):
        with uuid("257eed2b-fd65-4b7a-ad4c-a970e8e72f78") as case:
            main_page.select_library_icon_view_media('Skateboard 03.mp4')
            media_room_page.library_clip_context_menu_precut()
            item = precut_page.exist(L.precut.single_trim)
            if item.AXEnabled is not True:
                logger('Enter PreCut, Single Trim tab is not enabled.')
                raise Exception

            # [I55] 2. Clip duration would also be updated accordingly
            check_default = precut_page.get_single_trim_precut_in_position()
            if check_default != '00;00;00;00':
                raise Exception
            precut_page.set_single_trim_precut_in_position(value='00_05_00')
            check_duration = precut_page.get_precut_single_trim_duration()
            if check_duration == '00;00;05;00':
                case.result = True
            else:
                case.result = False

        with uuid("b2e1634a-2642-4a6d-ae2e-8347096f27c4") as case:
            # [I56] 3. Mark in icon would be updated accordingly

            # Note: locator "multi_trim_slider" = single trim > slider
            current_image = precut_page.snapshot(locator=L.precut.multi_trim_slider, file_name=Auto_Ground_Truth_Folder + 'I56.png')
            logger(f"{current_image=}")

            compare_result = precut_page.compare(Ground_Truth_Folder + 'I56.png', current_image)
            case.result = compare_result

        with uuid("885b7485-693c-4c9c-bebb-7991efb3d8ce") as case:
            # [I57] 1. In position would decrease 1 frame for each click and update the preview thumbnail
            precut_page.click_precut_single_trim_in_position_arrow_button(1)
            check_in_pos = precut_page.get_single_trim_precut_in_position()
            if check_in_pos == '00;00;04;29':
                result_1 = True
            else:
                result_1 = False

            current_image = precut_page.snapshot(locator=L.precut.single_trim_in_position_thumbnail,
                                                 file_name=Auto_Ground_Truth_Folder + 'I57.png')

            check_thumbnail = precut_page.compare(Ground_Truth_Folder + 'I57.png', current_image)
            case.result = result_1 and check_thumbnail

        with uuid("8313860a-90a2-423f-944d-384d2e131ac1") as case:
            # [I58] 2. Clip duration would also be updated accordingly
            check_duration = precut_page.get_precut_single_trim_duration()
            if check_duration == '00;00;05;01':
                case.result = True
            else:
                case.result = False

        with uuid("bf75cbdf-ce20-4aa6-942d-b83584eb415d") as case:

            # Adjust (In position) time code to (00;00;04;20)
            for x in range(9):
                precut_page.click_precut_single_trim_in_position_arrow_button(1)

            # [I59] 3. Mark in icon would be updated accordingly
            time.sleep(DELAY_TIME)
            # Note: locator "multi_trim_slider" = single trim > slider
            current_image = precut_page.snapshot(locator=L.precut.multi_trim_slider, file_name=Auto_Ground_Truth_Folder + 'I59.png')
            logger(f"{current_image=}")

            compare_result = precut_page.compare(Ground_Truth_Folder + 'I59.png', current_image)
            #logger(compare_result)
            case.result = compare_result

        with uuid("f063dcbf-aa4d-42c7-af46-a595660d36af") as case:
            # [I50] Duration > Min: 1 frame
            with uuid("48e7f9de-9f5f-403b-9056-41381394133f") as case:
                # [I77] [Out position] inputbox > Min: 1 frame
                # Adjust (In position) time code to (00;00;00;00)
                precut_page.set_single_trim_precut_in_position(value='00_00_00')
                check_in_pos = precut_page.get_single_trim_precut_in_position()

                # Check (Out position) mini value
                if check_in_pos == '00;00;00;00':
                    precut_page.set_single_trim_precut_out_position(value='00_00_00')
                    check_out_pos = precut_page.get_single_trim_precut_out_position()
                if check_out_pos == '00;00;00;01':
                    case.result = True
                else:
                    case.result = False
            check_duration = precut_page.get_precut_single_trim_duration()
            if check_duration == '00;00;00;01':
                case.result = True
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_7(self):
        with uuid("59f6ca22-b29a-4b3c-8b24-238261ba83fe") as case:
            # [70] 4. Larger than [In position]
            with uuid("6de4d425-c35d-40ba-99bf-328d870555ad") as case:
                main_page.select_library_icon_view_media('Skateboard 01.mp4')
                media_room_page.library_clip_context_menu_precut()
                item = precut_page.exist(L.precut.single_trim)
                if item.AXEnabled is not True:
                    logger('Enter PreCut, Single Trim tab is not enabled.')
                    raise Exception

                # [I67] 1. Input new out position timecode by keyboard
                precut_page.set_single_trim_precut_in_position(value='00_03_00')

                check_default = precut_page.get_single_trim_precut_out_position()
                if check_default != '00;00;10;00':
                    raise Exception
                precut_page.set_single_trim_precut_out_position(value='00_02_00')
                check_duration = precut_page.get_single_trim_precut_out_position()
                if check_duration == '00;00;03;01':
                    case.result = True
                else:
                    case.result = False
            if check_duration == '00;00;03;01':
                case.result = True
            else:
                case.result = False

        with uuid("ec5b026d-f343-4f7a-a1e9-412670d69695") as case:
            # [I68] 2. Clip duration would also be updated accordingly
            check_duration = precut_page.get_precut_single_trim_duration()
            if check_duration == '00;00;00;01':
                case.result = True
            else:
                case.result = False

        with uuid("66d4dac7-3f29-4b32-8392-be047363d9b7") as case:
            # [I69] 3. Mark out icon would be updated accordingly

            # Note: locator "multi_trim_slider" = single trim > slider
            current_image = precut_page.snapshot(locator=L.precut.multi_trim_slider, file_name=Auto_Ground_Truth_Folder + 'I69.png')
            logger(f"{current_image=}")

            compare_result = precut_page.compare(Ground_Truth_Folder + 'I69.png', current_image)
            #logger(compare_result)
            case.result = compare_result

        with uuid("81e06ad9-ff3d-422f-9854-12f5569f4cee") as case:
            # [I74] Out position would increase 1 frame for each click and update the preview thumbnail
            for x in range(10):
                precut_page.click_precut_single_trim_out_position_arrow_button(0)

            check_out_pos = precut_page.get_single_trim_precut_out_position()
            if check_out_pos != '00;00;03;11':
                check_pos = False
            else:
                check_pos = True

            current_image = precut_page.snapshot(locator=L.precut.single_trim_out_position_thumbnail,
                                                 file_name=Auto_Ground_Truth_Folder + 'I74.png')

            check_thumbnail = precut_page.compare(Ground_Truth_Folder + 'I74.png', current_image)
            #logger(check_thumbnail)
            case.result = check_pos and check_thumbnail

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_8(self):
        with uuid("46367ca5-6ae7-405e-8b45-e3f298bed7a5") as case:
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            media_room_page.library_clip_context_menu_precut()
            item = precut_page.exist(L.precut.single_trim)
            if item.AXEnabled is not True:
                logger('Enter PreCut, Single Trim tab is not enabled.')
                raise Exception

            # [I51] Duration > 1. Display original clip duration for 1st entry
            check_default = precut_page.get_precut_single_trim_duration()
            if check_default == '00;00;10;00':
                case.result = True
            else:
                case.result = False

        with uuid("70f40a71-8527-4cc5-8394-015ff0e767b9") as case:
            # [I61] 2. Clip duration would also be updated accordingly
            for x in range(5):
                precut_page.click_precut_single_trim_in_position_arrow_button(0)

            check_duration = precut_page.get_precut_single_trim_duration()
            if check_duration == '00;00;09;25':
                case.result = True
            else:
                case.result = False

        with uuid("48bab6b4-6791-4220-881c-803eccbd931e") as case:
            # [I62] 3. Mark in icon would be updated accordingly

            # Note: locator "multi_trim_slider" = single trim > slider
            current_image = precut_page.snapshot(locator=L.precut.multi_trim_slider, file_name=Auto_Ground_Truth_Folder + 'I62.png')
            logger(f"{current_image=}")

            compare_result = precut_page.compare(Ground_Truth_Folder + 'I62.png', current_image)
            #logger(compare_result)
            case.result = compare_result

        with uuid("51c09fe2-9f51-40c6-b82c-f87a0128fee8") as case:
            # [I80] Max: Total duration
            precut_page.set_precut_single_trim_duration(duration='00_12_30')

            check_duration = precut_page.get_precut_single_trim_duration()
            if check_duration == '00;00;10;00':
                result_1 = True
            else:
                result_1 = False

            check_in_pos = precut_page.get_single_trim_precut_in_position()
            if check_in_pos == '00;00;00;00':
                result_2 = True
            else:
                result_2 = False
            case.result = result_1 and result_2

        with uuid("da239f04-1ac0-4d4c-b6df-c584706645ac") as case:
            # [I71] 1. Out position would decrease 1 frame for each click and update the preview thumbnail
            for x in range(12):
                precut_page.click_precut_single_trim_out_position_arrow_button(1)

            check_out_pos = precut_page.get_single_trim_precut_out_position()
            if check_out_pos == '00;00;09;18':
                result_1 = True
            else:
                result_1 = False

            current_image = precut_page.snapshot(locator=L.precut.single_trim_out_position_thumbnail,
                                                 file_name=Auto_Ground_Truth_Folder + 'I71.png')

            check_thumbnail = precut_page.compare(Ground_Truth_Folder + 'I71.png', current_image)
            #logger(check_thumbnail)
            case.result = result_1 and check_thumbnail

        with uuid("7db31917-b660-4570-a863-193b5e43a357") as case:
            # [I72] 2. Clip duration would also be updated accordingly
            check_duration = precut_page.get_precut_single_trim_duration()
            if check_duration == '00;00;09;18':
                case.result = True
            else:
                case.result = False

        with uuid("38de8d10-4d15-4d4b-a335-ac5be7188542") as case:
            # [I73] 3. Mark out icon would be updated accordingly

            # Note: locator "multi_trim_slider" = single trim > slider
            current_image = precut_page.snapshot(locator=L.precut.multi_trim_slider, file_name=Auto_Ground_Truth_Folder + 'I73.png')
            logger(f"{current_image=}")

            compare_result = precut_page.compare(Ground_Truth_Folder + 'I73.png', current_image)
            #logger(compare_result)
            case.result = compare_result

        with uuid("7c57a2b2-cfe3-4727-835b-4ddee8e05ce5") as case:
            # [I75] 2. Clip duration would also be updated accordingly
            for x in range(9):
                precut_page.click_precut_single_trim_out_position_arrow_button(0)

            check_duration = precut_page.get_precut_single_trim_duration()
            if check_duration == '00;00;09;27':
                case.result = True
            else:
                case.result = False

        with uuid("aa64e971-6330-4023-b4a0-e412f71c0b20") as case:
            # [I76] 3. Mark out icon would be updated accordingly

            # Note: locator "multi_trim_slider" = single trim > slider
            current_image = precut_page.snapshot(locator=L.precut.multi_trim_slider, file_name=Auto_Ground_Truth_Folder + 'I76.png')
            logger(f"{current_image=}")

            compare_result = precut_page.compare(Ground_Truth_Folder + 'I76.png', current_image)
            #logger(compare_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_9(self):
        with uuid("fbd8408a-dbbe-46fe-b648-2d9193c246b3") as case:
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            media_room_page.library_clip_context_menu_precut()
            item = precut_page.exist(L.precut.single_trim)
            if item.AXEnabled is not True:
                logger('Enter PreCut, Single Trim tab is not enabled.')
                raise Exception

            # [I41] 1. Input new clip duration by keyboard
            check_default = precut_page.get_precut_single_trim_duration()
            if check_default != '00;00;10;00':
                raise Exception

            precut_page.set_precut_single_trim_duration(duration='00_06_00')

            check_duration = precut_page.get_precut_single_trim_duration()
            if check_duration == '00;00;06;00':
                case.result = True
            else:
                case.result = False

        with uuid("cd5e61db-59ab-4739-b68e-2a28da3b483d") as case:
            # [I42] 2. Out position would also be updated accordingly
            check_out_pos = precut_page.get_single_trim_precut_out_position()
            if check_out_pos == '00;00;06;00':
                case.result = True
            else:
                case.result = False

        with uuid("d8365cd6-a7ab-41d5-9d78-9776e9165de8") as case:
            # [I43] 3. Mark out icon would be updated accordingly

            # Note: locator "multi_trim_slider" = single trim > slider
            current_image1 = precut_page.snapshot(locator=L.precut.multi_trim_slider, file_name=Auto_Ground_Truth_Folder + 'I43_slider.png')
            #logger(f"{current_image1=}")
            compare_slider = precut_page.compare(Ground_Truth_Folder + 'I43_slider.png', current_image1)

            current_image2 = precut_page.snapshot(locator=L.precut.main_window, file_name=Auto_Ground_Truth_Folder + 'I43_precut_window.png')
            #logger(f"{current_image2=}")
            compare_Precut_window = precut_page.compare(Ground_Truth_Folder + 'I43_precut_window.png', current_image2)

            case.result = compare_slider and compare_Precut_window

        with uuid("73c5ff68-8cfc-4eab-9fea-36756efc912c") as case:
            # [I123] 1. Move indicator to the previous frame
            for x in range(5):
                precut_page.precut_preview_operation('Previous_Frame')

            time.sleep(DELAY_TIME)
            # Note: locator "multi_trim_slider" = single trim > slider
            current_image = precut_page.snapshot(locator=L.precut.multi_trim_slider, file_name=Auto_Ground_Truth_Folder + 'I123.png')
            #logger(f"{current_image=}")

            compare_result = precut_page.compare(Ground_Truth_Folder + 'I123.png', current_image)
            case.result = compare_result

        with uuid("b4ffd30e-34b0-4955-917c-b6515f04af7a") as case:
            # [I130] 1. Base on slider position to show current time correctly

            current_time = precut_page.get_precut_preview_timecode()
            #logger(current_time)
            if current_time == '00;00;05;25':
                case.result = True
            else:
                case.result = False

        with uuid("74ee611d-cad0-48e7-acaf-ec6a931d51b9") as case:
            # [I124] 2. Preview update accordingly
            # Current time : (00;00;05;25)

            # check1 : Compare snapshot w/ Ground Truth Folder
            current_image = precut_page.snapshot(locator=L.precut.main_window, file_name=Auto_Ground_Truth_Folder + 'I124.png')
            #logger(f"{current_image=}")
            check_1 = precut_page.compare(Ground_Truth_Folder + 'I124.png', current_image)

            # check2 : Compare Current Preview (00;00;05;25) is different w/ previous frame Preview (00:00:06:00)
            # if compare is false, it means (Preview is updated)
            check_2 = precut_page.compare(Auto_Ground_Truth_Folder + 'I124.png', Auto_Ground_Truth_Folder + 'I43_precut_window.png', similarity=0.99)
            #logger(check_2)
            case.result = check_1 and (not check_2)

        with uuid("244d9b86-7ed1-42d1-8cb7-cb376774fe45") as case:
            # [I125] 1. Move indicator to the next frame
            # Adjust current time to (00;00;06;01)
            for x in range(6):
                precut_page.precut_preview_operation('Next_Frame')

            time.sleep(DELAY_TIME)
            # Note: locator "multi_trim_slider" = single trim > slider
            current_image = precut_page.snapshot(locator=L.precut.multi_trim_slider, file_name=Auto_Ground_Truth_Folder + 'I125.png')
            #logger(f"{current_image=}")

            compare_result = precut_page.compare(Ground_Truth_Folder + 'I125.png', current_image)
            case.result = compare_result

        with uuid("0f9d7ada-5e8d-41c5-8c53-a51ba9ba47d5") as case:
            # [I126] 2. Preview update accordingly
            # Current time : (00;00;06;01)

            # check1 : Compare snapshot w/ Ground Truth Folder
            current_image = precut_page.snapshot(locator=L.precut.main_window, file_name=Auto_Ground_Truth_Folder + 'I126.png')
            #logger(f"{current_image=}")
            check_1 = precut_page.compare(Ground_Truth_Folder + 'I126.png', current_image)

            # check2 : Compare Current Preview (00;00;06;01) is different w/ previous frame Preview (00:00:05:25)
            # if compare is false, it means (Preview is updated)
            check_2 = precut_page.compare(Auto_Ground_Truth_Folder + 'I126.png', Auto_Ground_Truth_Folder + 'I124.png', similarity=0.99)
            #logger(check_2)
            case.result = check_1 and (not check_2)

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_10(self):
        with uuid("f6ef5963-4e63-46b8-8e46-2fe3bff60506") as case:
            main_page.select_library_icon_view_media('Skateboard 03.mp4')
            media_room_page.library_clip_context_menu_precut()
            item = precut_page.exist(L.precut.single_trim)
            if item.AXEnabled is not True:
                logger('Enter PreCut, Single Trim tab is not enabled.')
                raise Exception
            # [I118] Pause preview at current position
            precut_page.precut_preview_operation('Play')
            time.sleep(DELAY_TIME*4.5)
            precut_page.precut_preview_operation('Pause')
            # Current time code : 00;00;04;00 ~ 00:00:04:xx
            temp = precut_page.get_precut_preview_timecode()
            if temp.startswith('00;00;04'):
                check_timecode = True
            else:
                check_timecode = False

            #logger(temp)
            current_image = precut_page.snapshot(locator=L.precut.main_window, file_name=Auto_Ground_Truth_Folder + 'I118.png')
            check_preview = precut_page.compare(Ground_Truth_Folder + 'I118.png', current_image)

            case.result = check_timecode and check_preview

        with uuid("4f1c4e4a-938f-45a9-a802-62b285ffca89") as case:
            # [I115] Playback whole video from the beginning to the end smoothly

            # Set preview time code to 00;00;07;00
            precut_page.set_precut_timecode('00_00_07_00')
            precut_page.precut_preview_operation('Play')
            time.sleep(DELAY_TIME*4)
            # Current time code : 00;00;00;00
            temp = precut_page.get_precut_preview_timecode()
            if temp == '00;00;00;00':
                check_timecode = True
            else:
                check_timecode = False

            time.sleep(DELAY_TIME)
            current_image = precut_page.snapshot(locator=L.precut.main_window, file_name=Auto_Ground_Truth_Folder + 'I115.png')
            check_preview = precut_page.compare(Ground_Truth_Folder + 'I115.png', current_image)
            case.result = check_timecode and check_preview
            #if case.result is False:
            #    case.fail_log = 'AT sometimes met preview not sync'

        with uuid("d605ad2a-7e20-4a07-89f9-d82674c58dff") as case:
            # [I119] 1. Stop preview
            precut_page.precut_preview_operation('Play')
            time.sleep(DELAY_TIME*3.5)
            precut_page.precut_preview_operation('Stop')

            current_image = precut_page.snapshot(locator=L.precut.main_window, file_name=Auto_Ground_Truth_Folder + 'I119.png')
            # Compare Current preview w/ [I115] playback end preview
            check_preview = precut_page.compare(Auto_Ground_Truth_Folder + 'I115.png', Auto_Ground_Truth_Folder + 'I119.png')

            case.result = check_preview

        with uuid("f85af715-89eb-4c2d-917d-82f93b481331") as case:
            # [I131] 2. Seek frame by input timecode directly then preview would be updated
            # Set preview time code to 00;00;08;02
            precut_page.set_precut_timecode('00_00_08_02')

            current_image = precut_page.snapshot(locator=L.precut.main_window, file_name=Auto_Ground_Truth_Folder + 'I131.png')
            # Compare Current preview w/ [I115] playback end preview
            check_preview = precut_page.compare(Ground_Truth_Folder + 'I131.png', Auto_Ground_Truth_Folder + 'I131.png')
            case.result = check_preview

        with uuid("1df15cc8-51d4-4aca-93be-50a4f6835ddc") as case:
            # [I44] Duration > 1. Decrease 1 frame for each click
            for x in range(10):
                precut_page.click_precut_single_trim_duration_arrow_button(1)
            check_duration = precut_page.get_precut_single_trim_duration()
            if check_duration == '00;00;09;20':
                case.result = True
            else:
                case.result = False

        with uuid("a6d80b59-6a71-4e40-8536-d1bd61616f7b") as case:
            # [I45] 2. Out position would also decrease 1 frame and update the preview thumbnail
            if precut_page.get_single_trim_precut_out_position() == '00;00;09;20':
                check_out_pos = True
            else:
                check_out_pos = False

            current_image = precut_page.snapshot(locator=L.precut.single_trim_out_position_thumbnail,
                                                 file_name=Auto_Ground_Truth_Folder + 'I45.png')

            check_thumbnail = precut_page.compare(Ground_Truth_Folder + 'I45.png', current_image)
            #logger(check_thumbnail)
            case.result = check_out_pos and check_thumbnail

        with uuid("f865ec01-4816-476f-9342-6ffa848db263") as case:
            # [I46] 3. Mark out icon would be updated accordingly

            # Note: locator "multi_trim_slider" = single trim > slider
            current_image = precut_page.snapshot(locator=L.precut.multi_trim_slider, file_name=Auto_Ground_Truth_Folder + 'I46.png')
            logger(f"{current_image=}")

            compare_result = precut_page.compare(Ground_Truth_Folder + 'I46.png', current_image)
            #logger(compare_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_11(self):
        with uuid("97527183-2c12-4eb6-8f4e-cd88b65c3d8b") as case:
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            media_room_page.library_clip_context_menu_precut()
            item = precut_page.exist(L.precut.single_trim)
            if item.AXEnabled is not True:
                logger('Enter PreCut, Single Trim tab is not enabled.')
                raise Exception
            # [I31] 1. Move indicator to the ending point then click hotkey "O"
            # Move indicator to (00:00:07:00)
            precut_page.set_precut_timecode('00_00_07_00')

            # Note: locator "multi_trim_slider" = single trim > slider
            current_image = precut_page.snapshot(locator=L.precut.multi_trim_slider, file_name=Auto_Ground_Truth_Folder + 'I31.png')
            #logger(f"{current_image=}")
            compare_before = precut_page.compare(Ground_Truth_Folder + 'I31.png', current_image)

            # Press hotkey
            precut_page.tap_MarkOut_onLibraryPreview_hotkey()
            current_image = precut_page.snapshot(locator=L.precut.multi_trim_slider,
                                                 file_name=Auto_Ground_Truth_Folder + 'I31_2.png')
            compare_after = precut_page.compare(Ground_Truth_Folder + 'I31_2.png', current_image)
            case.result = compare_before and compare_after

        with uuid("21ef56e3-9bb5-4854-b60a-3fb7bd0aff56") as case:
            # [I32] 2. Clip duration would be update correctly
            current_duration = precut_page.get_precut_single_trim_duration()
            if current_duration == '00;00;07;00':
                case.result = True
            else:
                case.result = False

        with uuid("e70f22ce-0b54-4c6b-a3f5-b320383871ed") as case:
            # [I33] 3. Out position timecode & instant preview would be updated
            current_out_pos = precut_page.get_single_trim_precut_out_position()
            if current_out_pos == '00;00;07;00':
                result_1 = True
            else:
                result_1 = False

            current_image = precut_page.snapshot(locator=L.precut.single_trim_out_position_thumbnail,
                                                 file_name=Auto_Ground_Truth_Folder + 'I33.png')

            check_thumbnail = precut_page.compare(Ground_Truth_Folder + 'I33.png', current_image)
            case.result = result_1 and check_thumbnail

        with uuid("71367944-5271-4787-a6ad-851c3effcb53") as case:
            # [I52] [Duration] inputbox > 2. Display trimmed clip duration for re-entry
            with uuid("68d5d930-d446-4ca1-9367-558648727a19") as case:
                # [I47] 1. Increase 1 frame for each click
                for x in range(6):
                    precut_page.click_precut_single_trim_duration_arrow_button(0)

                time.sleep(DELAY_TIME)

                current_duration = precut_page.get_precut_single_trim_duration()
                if current_duration == '00;00;07;06':
                    case.result = True
                else:
                    case.result = False
            if current_duration == '00;00;07;06':
                case.result = True
            else:
                case.result = False

        with uuid("6d9de9f1-1d1e-4dd4-ade5-7245450c4a27") as case:
            # [I48] 2. Out position would also increase 1 frame and update the preview thumbnail
            current_out_pos = precut_page.get_single_trim_precut_out_position()
            if current_out_pos == '00;00;07;06':
                result_1 = True
            else:
                result_1 = False

            current_image = precut_page.snapshot(locator=L.precut.single_trim_out_position_thumbnail,
                                                 file_name=Auto_Ground_Truth_Folder + 'I48.png')

            check_thumbnail = precut_page.compare(Ground_Truth_Folder + 'I48.png', current_image)
            case.result = result_1 and check_thumbnail

        with uuid("92326e1c-0e3d-4234-8fc3-1a94c22c8ae9") as case:
            # [I49] 3. Mark out icon would be updated accordingly
            current_image = precut_page.snapshot(locator=L.precut.multi_trim_slider,
                                                 file_name=Auto_Ground_Truth_Folder + 'I49.png')
            compare_result = precut_page.compare(Ground_Truth_Folder + 'I49.png', current_image)
            case.result = compare_result

        with uuid("fcf79d2b-a90b-432b-b911-3997990ca548") as case:
            # [I53] Max: untrimmed clip duration
            precut_page.set_precut_single_trim_duration('00_15_00')
            current_duration = precut_page.get_precut_single_trim_duration()
            if current_duration == '00;00;10;00':
                case.result = True
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_12(self):
        with uuid("25c35251-d826-4e1e-b808-9f078de7935b") as case:
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            media_room_page.library_clip_context_menu_precut()
            item = precut_page.exist(L.precut.single_trim)
            if item.AXEnabled is not True:
                logger('Enter PreCut, Single Trim tab is not enabled.')
                raise Exception

            precut_page.edit_precut_switch_trim_mode('Multi')
            item = precut_page.exist(L.precut.multi_trim)
            current_result = item.AXEnabled
            case.result = current_result

            # [I101] Switch frame and show current frame in viewer correctly
            precut_page.tap_multi_trim_thumbnail_frame(2)
            precut_page.tap_MarkIn_onLibraryPreview_hotkey()
            time.sleep(DELAY_TIME)
            precut_page.tap_multi_trim_thumbnail_frame(5)
            precut_page.tap_MarkOut_onLibraryPreview_hotkey()

            current_image = precut_page.snapshot(locator=L.precut.multi_trim_thumbnail_slider,
                                                 file_name=Auto_Ground_Truth_Folder + 'I101.png')
            compare_result = precut_page.compare(Ground_Truth_Folder + 'I101.png', current_image)
            case.result = compare_result

        with uuid("4ee92f7b-a834-4413-a739-e4cf36cb5d81") as case:
            # [I103] One segment > Show correct result in slide bar and Selected Segments
            current_before = precut_page.snapshot(locator=L.precut.multi_trim_slider,
                                                 file_name=Auto_Ground_Truth_Folder + 'I103_1.png')
            compare_before = precut_page.compare(Ground_Truth_Folder + 'I103_1.png', current_before)

            precut_page.tap_multi_trim_invert_trim()
            current_after = precut_page.snapshot(locator=L.precut.multi_trim_slider,
                                                 file_name=Auto_Ground_Truth_Folder + 'I103_2.png')
            compare_after = precut_page.compare(Ground_Truth_Folder + 'I103_2.png', current_after)

            case.result = compare_before and compare_after

        with uuid("0b608b10-3a3d-486d-89ec-6756bea784cf") as case:
            # [I109] Show correct segment in this panel
            current_image = precut_page.snapshot(locator=L.precut.multi_trim_selected_segment,
                                                 file_name=Auto_Ground_Truth_Folder + 'I109.png')
            compare_result = precut_page.compare(Ground_Truth_Folder + 'I109.png', current_image)
            case.result = compare_result

        with uuid("18e7ba83-e421-418e-a6bb-0e830abe2cb1") as case:
            # [I122] 2. Indicator would be moved to the beginning of clip
            with uuid("eeb87155-9a61-47dd-ae59-c72fb4b51c79") as case:
                # [I121] Outpout mode > 1. Stop preview
                # Switch to Output mode
                precut_page.switch_multi_trim_preview_mode('Output')

                # Click "Stop"
                precut_page.precut_preview_operation('Stop')
                time.sleep(DELAY_TIME)
                current_image = precut_page.snapshot(locator=L.precut.main_window,
                                                     file_name=Auto_Ground_Truth_Folder + 'I121.png')
                compare_result = precut_page.compare(Ground_Truth_Folder + 'I121.png', current_image)
                case.result = compare_result
            current_image = precut_page.snapshot(locator=L.precut.multi_trim_slider,
                                                 file_name=Auto_Ground_Truth_Folder + 'I122.png')
            compare_result = precut_page.compare(Ground_Truth_Folder + 'I122.png', current_image)
            case.result = compare_result

        with uuid("ea55c700-0d6b-4033-b4f7-711097598b3c") as case:
            # [I116] Playback trimmed video from mark in to mark out
            # Adjust indicator to begin > Play video w/ 2s > Then, Pause to check Preview (Play 1st trim)
            time.sleep(DELAY_TIME)
            precut_page.press_space_key()
            time.sleep(DELAY_TIME*2)
            precut_page.press_space_key()

            current_image = precut_page.snapshot(locator=L.precut.multi_trim_slider,
                                                 file_name=Auto_Ground_Truth_Folder + 'I116_1.png')
            compare_1st = precut_page.compare(Ground_Truth_Folder + 'I116_1.png', current_image)

            # Play video w/ 3s > Then, Pause to check Preview (Play 2nd trim)
            precut_page.press_space_key()
            time.sleep(DELAY_TIME*3)
            precut_page.press_space_key()
            current_image = precut_page.snapshot(locator=L.precut.multi_trim_slider,
                                                 file_name=Auto_Ground_Truth_Folder + 'I116_2.png')
            compare_2nd = precut_page.compare(Ground_Truth_Folder + 'I116_2.png', current_image, similarity=0.90)

            case.result = compare_1st and compare_2nd

        with uuid("69f1bfd3-0621-42cd-a51c-ea2b020d4e67") as case:
            # [I136] Cancel > Multi Trim > Close Pre Cut window and trim result is not applied
            precut_page.click_cancel()
            precut_page.handle_save_change_before_leaving(option=1)

            if not precut_page.exist(L.precut.single_trim):
                current_library = precut_page.snapshot(locator=precut_page.area.library_icon_view, file_name=Auto_Ground_Truth_Folder + 'I136.png')

            logger(current_library)
            check_library_preview = precut_page.compare(Ground_Truth_Folder + 'I136.png', current_library)
            case.result = check_library_preview

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_13(self):
        with uuid("b549d902-b6c0-4529-9b2e-d2370e2b5ead") as case:
            # [I79] 2. Display Out Position time code for trimmed clip
            with uuid("26477187-14bd-4693-a7de-3bae34287eaa") as case:
                # [I65] 2. Display In Position time code for trimmed clip
                with uuid("00456d6a-ee89-4656-b75e-09ccfb3576f6") as case:
                    main_page.select_library_icon_view_media('Skateboard 01.mp4')
                    media_room_page.library_clip_context_menu_precut()
                    item = precut_page.exist(L.precut.multi_trim)
                    if item.AXEnabled is not True:
                        logger('Enter PreCut, Multi Trim tab is not enabled.')
                        raise Exception

                    # Switch to Single trim
                    precut_page.edit_precut_switch_trim_mode('Single')

                    # [I35] 2. Mark in and Mark out button are not disabled

                    # Single Trim > Mark in (Hotkey)
                    precut_page.edit_precut_single_trim_drag_slider(0, 0, 5, 0)
                    precut_page.tap_single_trim_mark_in()
                    check_1 = precut_page.get_single_trim_precut_in_position()
                    if check_1 == '00;00;05;00':
                        result_1 = True
                    else:
                        result_1 = False

                    time.sleep(DELAY_TIME)
                    precut_page.edit_precut_single_trim_drag_slider(0, 0, 6, 12)
                    precut_page.tap_single_trim_mark_in()
                    check_2 = precut_page.get_single_trim_precut_in_position()
                    if check_2 == '00;00;06;12':
                        result_2 = True
                    else:
                        result_2 = False

                    time.sleep(DELAY_TIME)
                    precut_page.edit_precut_single_trim_drag_slider(0, 0, 7, 20)
                    precut_page.tap_single_trim_mark_out()
                    check_3 = precut_page.get_single_trim_precut_out_position()
                    if check_3 == '00;00;07;20':
                        result_3 = True
                    else:
                        result_3 = False

                    time.sleep(DELAY_TIME)
                    precut_page.edit_precut_single_trim_drag_slider(0, 0, 9, 25)
                    precut_page.tap_single_trim_mark_out()
                    check_4 = precut_page.get_single_trim_precut_out_position()
                    if check_4 == '00;00;09;25':
                        result_4 = True
                    else:
                        result_4 = False
                    case.result = result_1 and result_2 and result_3 and result_4
                case.result = result_1 and result_2
            case.result = result_3 and result_4

        with uuid("3f2ebd02-15a7-4451-929a-9ce61c04fd58") as case:
            # [I39] 4. [Duration] can't modify
            with uuid("ccd59f4e-a0db-4ede-987e-39f635959a5e") as case:
                # [I36] 1. Trim duration is fixed
                before_duration = precut_page.get_precut_single_trim_duration()
                precut_page.click_precut_single_trim_lock_duration()

                time.sleep(DELAY_TIME)
                precut_page.edit_precut_single_trim_drag_slider(0, 0, 2, 20)
                precut_page.tap_single_trim_mark_in()

                after_duration = precut_page.get_precut_single_trim_duration()
                if before_duration == after_duration:
                    case.result = True
                else:
                    case.result = False
            if before_duration == after_duration:
                case.result = True
            else:
                case.result = False

        with uuid("db786856-01ca-4952-b869-570fd590b501") as case:
            # [I37] 2. Fixed segment can be moved position on slide bar
            check_lock_status = precut_page.get_lock_status()

            time.sleep(DELAY_TIME)
            # Note: locator "multi_trim_slider" = single trim > slider
            current_image = precut_page.snapshot(locator=L.precut.multi_trim_slider, file_name=Auto_Ground_Truth_Folder + 'I37.png')
            #logger(f"{current_image=}")

            compare_result = precut_page.compare(Ground_Truth_Folder + 'I37.png', current_image)
            case.result = compare_result and check_lock_status

        with uuid("6fa617bd-9073-41c6-b96f-0c973be2d1bf") as case:
            # [I120] 2. Indicator would be moved to the beginning of clip
            check_result = precut_page.precut_preview_operation('Stop')
            current_image = precut_page.snapshot(locator=L.precut.main_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'I120.png')
            #logger(f"{current_image=}")
            compare_result = precut_page.compare(Ground_Truth_Folder + 'I120.png', current_image)
            case.result = compare_result and check_result

        with uuid("411c345b-c2be-4b93-86db-37fbfd0d514a") as case:
            # [I133] Close Pre Cut window and trim result is correct in library scene folder
            precut_page.click_ok()
            time.sleep(DELAY_TIME)

            if not precut_page.exist(L.precut.single_trim):
                current_library = precut_page.snapshot(locator=precut_page.area.library_icon_view,
                                                       file_name=Auto_Ground_Truth_Folder + 'I133.png')

            #logger(current_library)
            check_library_preview = precut_page.compare(Ground_Truth_Folder + 'I133.png', current_library)
            case.result = check_library_preview

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_14(self):
        with uuid("5d1407c9-0ca9-4829-a479-05668b769bcf") as case:
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            media_room_page.library_clip_context_menu_precut()
            item = precut_page.exist(L.precut.single_trim)
            if item.AXEnabled is not True:
                logger('Enter PreCut, Single Trim tab is not enabled.')
                raise Exception

            precut_page.edit_precut_switch_trim_mode('Multi')
            item = precut_page.exist(L.precut.multi_trim)
            if item.AXEnabled is not True:
                logger('Enter PreCut, Multi Trim tab is not enabled.')
                raise Exception

            # [I108] Show correct segment in this panel
            # Adjust to trim three segments
            # segment 1
            precut_page.tap_multi_trim_thumbnail_frame(0)
            precut_page.tap_MarkIn_onLibraryPreview_hotkey()
            time.sleep(DELAY_TIME)
            precut_page.tap_multi_trim_thumbnail_frame(1)
            precut_page.tap_MarkOut_onLibraryPreview_hotkey()

            # segment 2
            precut_page.tap_multi_trim_thumbnail_frame(2)
            precut_page.tap_MarkIn_onLibraryPreview_hotkey()
            time.sleep(DELAY_TIME)
            precut_page.tap_multi_trim_thumbnail_frame(3)
            precut_page.tap_MarkOut_onLibraryPreview_hotkey()

            # segment 3
            precut_page.tap_multi_trim_thumbnail_frame(4)
            precut_page.tap_MarkIn_onLibraryPreview_hotkey()
            time.sleep(DELAY_TIME)
            precut_page.tap_multi_trim_thumbnail_frame(5)
            precut_page.tap_MarkOut_onLibraryPreview_hotkey()

            time.sleep(DELAY_TIME)

            current_image = precut_page.snapshot(locator=L.precut.multi_trim_selected_segment,
                                                 file_name=Auto_Ground_Truth_Folder + 'I108.png')
            compare_result = precut_page.compare(Ground_Truth_Folder + 'I108.png', current_image)
            case.result = compare_result

        with uuid("e8a3467e-4d35-435b-9aa0-db68618b48c2") as case:
            # [I104] Show correct result in slide bar and Selected Segments

            precut_page.tap_multi_trim_invert_trim()
            current_image = precut_page.snapshot(locator=L.precut.multi_trim_slider,
                                                 file_name=Auto_Ground_Truth_Folder + 'I104_1.png')
            compare_slider = precut_page.compare(Ground_Truth_Folder + 'I104_1.png', current_image)

            current_image = precut_page.snapshot(locator=L.precut.multi_trim_selected_segment,
                                                 file_name=Auto_Ground_Truth_Folder + 'I104_2.png')
            compare_segment = precut_page.compare(Ground_Truth_Folder + 'I104_2.png', current_image)

            case.result = compare_slider and compare_segment

        with uuid("d766d9e7-5702-4fe6-b5f5-6e970a1bc186") as case:
            # [I111] [Selected Segments] panel > Remove > Select > Delete selected segemnt correcctly
            time.sleep(DELAY_TIME)
            precut_page.tap_multi_trim_remove()
            time.sleep(DELAY_TIME)
            current_image = precut_page.snapshot(locator=L.precut.main_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'I111.png')
            compare_result = precut_page.compare(Ground_Truth_Folder + 'I111.png', current_image)
            case.result = compare_result


        with uuid("7bd43e84-5c33-4b2c-8cf5-4d53e439b980") as case:
            # [I110] [Selected Segments] panel > Remove > Unselect > No segment will be removed
            precut_page.click_multi_trim_segment_unselect_segment()
            time.sleep(DELAY_TIME)
            precut_page.tap_multi_trim_remove()

            current_image = precut_page.snapshot(locator=L.precut.main_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'I110.png')
            # AT Ground Truth folder : I111.png is similar with I110.png (Different is only unselect segment)
            compare_result = precut_page.compare(Auto_Ground_Truth_Folder + 'I111.png', current_image)
            case.result = compare_result

        with uuid("38b40774-cb13-45ee-aa34-5d4ee09b2234") as case:
            # [I113] [Selected Segments] panel > Context menu > Invert Selection
            # Select segment 2
            precut_page.click_multi_trim_segment(1)
            precut_page.right_click_multi_trim_segment_invert_selection()
            time.sleep(DELAY_TIME)
            current_image = precut_page.snapshot(locator=L.precut.main_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'I113.png')
            compare_result = precut_page.compare(Ground_Truth_Folder + 'I113.png', current_image)
            case.result = compare_result

        with uuid("b00c77fd-cc15-4176-b561-c3da71facc98") as case:
            # [I112] [Selected Segments] panel > Context menu > Remove selected clip
            # Select segment 3
            precut_page.click_multi_trim_segment(2)
            precut_page.right_click_multi_trim_segment_remove_selected()
            time.sleep(DELAY_TIME)
            current_image = precut_page.snapshot(locator=L.precut.main_window,
                                                 file_name=Auto_Ground_Truth_Folder + 'I112.png')
            compare_result = precut_page.compare(Ground_Truth_Folder + 'I112.png', current_image)
            case.result = compare_result

        with uuid("50dfb5a2-18e7-4072-9d7c-1ff533904004") as case:
            # [I134] Close Pre Cut window and trim result is correct in library scene folder
            precut_page.click_ok()
            time.sleep(DELAY_TIME)

            if not precut_page.exist(L.precut.multi_trim):
                current_library = precut_page.snapshot(locator=precut_page.area.library_icon_view,
                                                       file_name=Auto_Ground_Truth_Folder + 'I134.png')

            #logger(current_library)
            check_library_preview = precut_page.compare(Ground_Truth_Folder + 'I134.png', current_library)
            case.result = check_library_preview