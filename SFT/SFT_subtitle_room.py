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
pip_designer_page = PageFactory().get_page_object('pip_designer_page', mac)
pip_room_page = PageFactory().get_page_object('pip_room_page', mac)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mac)
media_room_page = PageFactory().get_page_object('media_room_page', mac)
tips_area_page = PageFactory().get_page_object('tips_area_page',mac)
fix_enhance_page = PageFactory().get_page_object('fix_enhance_page',mac)
produce_page = PageFactory().get_page_object('produce_page', mac)
subtitle_room_page = PageFactory().get_page_object('subtitle_room_page', mac)
playback_window_page = PageFactory().get_page_object('playback_window_page',mac)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="Subtitle Room.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Subtitle_Room/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Subtitle_Room/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Subtitle_Room():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        time.sleep(DELAY_TIME*3)
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
            google_sheet_execution_log_init('Subtitle Room')

    @classmethod
    def teardown_class(cls):

        logger('teardown_class - export report')
        report.export()
        logger(
            f"Subtitle Room result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           report.get_ovinfo('skip'),
                           report.get_ovinfo('duration'))
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                               report.get_ovinfo('skip'), report.get_ovinfo('duration'))
        report.show()

    # Return current subtitle row number
    def get_total_subtitle_rows(self, timeout=15):
        # select first row
        subtitle_room_page.select_subtitle_row(1)

        # press [Down] repeatedly
        subtitle_count = 1
        for y in range(timeout):
            area = main_page.area.preview.main
            old_img = main_page.snapshot(area)
            main_page.input_keyboard(main_page.keyboard.key.down)
            time.sleep(0.5)
            new_img = main_page.snapshot(area)
            result = main_page.compare(old_img, new_img, 0.9999)
            #logger(result)
            if result:
                break
            else:
                subtitle_count = subtitle_count + 1
        return subtitle_count

    # 8 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_3(self):
        # Import video > Select template "CHT.aiff" to track1
        audio_path = Test_Material_Folder + 'Subtitle_Room/CHT.aiff'
        time.sleep(DELAY_TIME * 3)
        media_room_page.collection_view_right_click_import_media_files(audio_path)
        time.sleep(DELAY_TIME * 2)
        main_page.insert_media('CHT.aiff')

        # [F46]  2 Auto Transcribe Subtitle > 2.1 Entry > Timeline range selection > Context menu of timeline content
        with uuid('dffa75ab-b341-4b42-91d4-4fc92b781ab4') as case:

            # Select timeline range: 0 sec ~ 30 sec
            timeline_operation_page.set_range_markin_markout(0, 900)

            # Move mouse to CTI left position > Right click > Select menu
            timeline_operation_page.move_mouse_to_CTI_position(1, True)
            main_page.right_click()
            time.sleep(DELAY_TIME * 5)
            main_page.select_right_click_menu('Speech to Text')

            if main_page.exist(L.subtitle_room.btn_add_subtitle, timeout=6):
                enter_subtitle_room = True
            else:
                enter_subtitle_room = False
            case.result = enter_subtitle_room

        # [F68] 2.1 Transcribe selected range only "checkbox" > Enable
        with uuid('ed51f256-440f-4e8f-90df-eaf56e837c2c') as case:
            check_default = subtitle_room_page.auto_function.get_selected_range_status()
            if check_default:
                default_status = True
            else:
                default_status = False

            # set Checkbox to disable
            subtitle_room_page.auto_function.set_selected_range_only(0)
            # set Checkbox to enable
            subtitle_room_page.auto_function.set_selected_range_only(1)

            # Set result
            check_current = subtitle_room_page.auto_function.get_selected_range_status()
            if check_current:
                current_status = True
            else:
                current_status = False

            case.result = default_status and current_status

        # Set lang to CHT
        subtitle_room_page.auto_function.select_LANG('CHT')
        time.sleep(DELAY_TIME*2)
        subtitle_room_page.auto_function.click_create()

        # [F94] 3.1 Edit button > Adjust subtitle position > Status (Disable)
        with uuid('6323d437-b2ff-4f5f-b08f-f1254a606122') as case:
            # If no  subtitle is selected, status is False
            check_status = subtitle_room_page.click_adjust_pos_btn()
            case.result = not check_status

        # [F69] 2.1 Transcribe selected range only "checkbox" > Auto Transcribe work fine
        with uuid('85e223af-3fe5-434a-b137-c0d59f95a4ab') as case:
            # [F78] 2.1 Content > Auto Format > AIFF
            with uuid('d3ead026-17d2-478b-b624-e8c0c3ba7015') as case:
                time.sleep(DELAY_TIME*2)
                for x in range(200):
                    if main_page.exist(L.subtitle_room.handle_progress_dialog.btn_cancel, timeout=10):
                        time.sleep(DELAY_TIME)
                    else:
                        break

                # get total subtitle rows
                current_rows = self.get_total_subtitle_rows()

                if current_rows > 1:
                    case.result = True
                else:
                    case.result = False
                logger(current_rows)
            if current_rows > 1:
                case.result = True
            else:
                case.result = False

        # [F92] 3.1 Edit Buttons > Remove the selected subtitle marker > multi-select
        with uuid('bbd90036-8d62-40dc-a69a-c88fab56a3b2') as case:
            subtitle_room_page.multiple_select_subtitle_row(1, 2, 3)
            subtitle_room_page.click_del_btn()

            # get total subtitle rows
            after_delete_rows = self.get_total_subtitle_rows()
            check_result = current_rows - after_delete_rows

            if check_result == 3:
                case.result = True
            else:
                case.result = False

        # [F102] 3.1 Edit buttons > Adjust subtitle position > Adjustment method > Slider
        with uuid('0b5f750d-b305-4c36-a0bf-cbedcc7cdf48') as case:
            subtitle_room_page.click_adjust_pos_btn()
            time.sleep(DELAY_TIME)
            subtitle_room_page.position.set_x_slider(-0.42)
            subtitle_room_page.position.close_window()

            subtitle_room_page.click_adjust_pos_btn()
            time.sleep(DELAY_TIME)
            current_x = subtitle_room_page.position.get_x_value()
            logger(current_x)
            if current_x == '-0.42':
                case.result = True
            else:
                case.result = False
            subtitle_room_page.position.close_window()

        # [F136] 3.1 Edit buttons > Merge > Disable
        # Button will Enable (UX request: VDE224118-0004)
        with uuid('f763dd0d-5965-4ee4-9aa3-6d44193cba32') as case:
            check_status = subtitle_room_page.get_merge_btn()
            case.result = check_status

    # 6 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1(self):
        # [F8] General > Timeline View > No content
        with uuid('2aec314a-30bc-4962-b4f7-a23c88750ab1') as case:
            check_subtitle_room_result = subtitle_room_page.get_subtitle_room_status()

            main_page.timeline_select_track(1)
            main_page.right_click()
            if main_page.exist({"AXRole": "AXMenuItem", "AXTitle": "Show Subtitle Track"}).AXMenuItemMarkChar == '✓':
                enable_subtitle_track = True
            else:
                enable_subtitle_track = False
            main_page.right_click()
            case.result = (not check_subtitle_room_result) and (not enable_subtitle_track)

        # [F9] General > Timeline View > Have content
        with uuid('08180f13-b151-48df-9fe6-247feabaee30') as case:
            main_page.insert_media('Skateboard 01.mp4')
            check_subtitle_room_result = subtitle_room_page.get_subtitle_room_status()
            time.sleep(DELAY_TIME*0.5)
            case.result = check_subtitle_room_result

        # [F10] General > Timeline View > Hotkey (F12)
        with uuid('1fae5d1c-21ea-45f1-a223-bf9e822e9f79') as case:
            main_page.tap_SubtitleRoom_hotkey()
            if main_page.exist(L.subtitle_room.btn_add_subtitle, timeout=6):
                enter_subtitle_room = True
            else:
                enter_subtitle_room = False

            main_page.timeline_select_track(1)
            main_page.right_click()
            if main_page.exist({"AXRole": "AXMenuItem", "AXTitle": "Show Subtitle Track"}).AXMenuItemMarkChar == '✓':
                enable_subtitle_track = True
            else:
                enable_subtitle_track = False
            main_page.right_click()

            case.result = enter_subtitle_room and enable_subtitle_track

        # [F39] General > More and tips > What can I do in this Subtitle Room [Click]
        with uuid('f0a2f1d9-fd16-4ea0-b94a-12fc4eba0725') as case:
            case.result = subtitle_room_page.click_i_button()

        # [F12] General > Main Menu > Create Subtitle Manually
        with uuid('694086f2-2edc-4ef5-af16-b72f80351f7c') as case:
            subtitle_room_page.library_menu.click_manually_create()
            current_image = subtitle_room_page.snapshot(locator=L.subtitle_room.subtitle_region.main_content,
                                                      file_name=Auto_Ground_Truth_Folder + '012_subtitle_library.png')

            # logger(current_image)
            check_preview = subtitle_room_page.compare(Ground_Truth_Folder + '012_subtitle_library.png', current_image)
            case.result = check_preview

        # [F35] 1.3 > More > EXport an SRT File > Disable
        with uuid('24f44c63-091f-4fb5-848d-7c855ea69d60') as case:
            main_page.click(L.subtitle_room.btn_more)
            elem = main_page.exist({'AXTitle': 'Export as an SRT File', 'AXRole': 'AXMenuItem'})
            check_result = elem.AXEnabled
            case.result = not check_result
            time.sleep(DELAY_TIME*3)

    # 7 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_2(self):
        # Import video > Select template "ENG.m4a" to track1
        audio_path = Test_Material_Folder + 'Subtitle_Room/ENG.m4a'
        time.sleep(DELAY_TIME * 3)
        media_room_page.collection_view_right_click_import_media_files(audio_path)
        time.sleep(DELAY_TIME * 2)
        main_page.insert_media('ENG.m4a')

        # enter Subtitle Room
        main_page.click(L.subtitle_room.btn_subtitle_room)
        time.sleep(DELAY_TIME*2)

        # [F11] General > Main Menu > Auto Transcribe Subtitle
        with uuid('38fae2dd-c5c6-4494-b88d-60fa19918f91') as case:
            subtitle_room_page.library_menu.click_auto_transcribe()

            check_default_lang = subtitle_room_page.auto_function.get_LANG_status()
            if check_default_lang == "English (United States)":
                lang_OK = True
            else:
                lang_OK = False

            case.result = lang_OK

        # [F63] Auto Transcribe Subtitle > Language > English (United States)
        with uuid('dcc7e713-c859-41a3-b10f-2960417c2167') as case:
            # [F76] 2.1 Content > Audio Format > M4A
            with uuid('91c2c48f-8a1b-4741-a4ba-d64d1ce585fb') as case:
                subtitle_room_page.auto_function.click_create()

                for x in range(200):
                    if main_page.exist(L.subtitle_room.handle_progress_dialog.btn_cancel):
                        time.sleep(DELAY_TIME)
                    else:
                        break

                # get total subtitle rows
                current_rows = self.get_total_subtitle_rows()

                if current_rows > 1:
                    case.result = True
                else:
                    case.result = False
                logger(current_rows)

            if current_rows > 1:
                case.result = True
            else:
                case.result = False

        # [F90] 3 Create Subtitle Manually > 3.1 > Remove the selected subtitle marker > Status (Enable)
        with uuid('c91e1ecd-4a5c-4415-a061-967e89b2b284') as case:
            check_status = subtitle_room_page.click_del_btn(is_click=0)
            case.result = check_status

        # [F93]  3.1 > Remove the selected subtitle marker > Hotkey (Del)
        with uuid('1662bc42-0d79-491b-aa74-12b0d8a8bcff') as case:
            # [F89]  3.1 > Remove the selected subtitle marker > Status (Disable)
            with uuid('0647922c-167b-4268-b7f8-a948d7d407a5') as case:
                # Click Hotkey
                main_page.press_del_key()
                time.sleep(DELAY_TIME*0.5)

                check_status = subtitle_room_page.click_del_btn(is_click=0)
                case.result = not check_status

            # get total subtitle rows
            new_rows = self.get_total_subtitle_rows()
            logger(f'last row {new_rows}')

            value = current_rows - new_rows

            if value == 1:
                case.result = True
            else:
                case.result = False

        # [F151]  3.2 Subtitle List > [End Time] > Display > time modify
        with uuid('f97e3792-af83-4416-8900-bb4ce946a9cf') as case:
            subtitle_room_page.set_end_time(new_rows, '00_00_52_08')
            time.sleep(DELAY_TIME*0.5)
            result = subtitle_room_page.get_end_time(new_rows)
            if result == '00;00;52;08':
                case.result = True
            else:
                case.result = False

    # 12 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_4(self):
        # Import video > Select template "JPN.wav" to track1
        audio_path = Test_Material_Folder + 'Subtitle_Room/JPN.wav'
        time.sleep(DELAY_TIME * 3)
        media_room_page.collection_view_right_click_import_media_files(audio_path)
        time.sleep(DELAY_TIME * 2)
        main_page.insert_media('JPN.wav')

        # enter Subtitle Room
        main_page.click(L.subtitle_room.btn_subtitle_room)
        time.sleep(DELAY_TIME*2)

        # click [Create Subtitles Manually]
        subtitle_room_page.library_menu.click_manually_create()
        time.sleep(DELAY_TIME)
        default_empty_image = subtitle_room_page.snapshot(locator=L.subtitle_room.subtitle_region.main_content)
        #logger(default_empty_image)

        # [F33] 1.3 More [...] > Auto Transcribe Subtitle
        with uuid('69d2bc63-117b-4b08-8c51-e48457b59b89') as case:
            subtitle_room_page.more.click_auto_transcribe()
            time.sleep(DELAY_TIME)
            subtitle_room_page.auto_function.select_LANG('JPN')
            time.sleep(DELAY_TIME*0.5)
            check_result = subtitle_room_page.auto_function.get_LANG_status()
            if check_result == 'Japanese':
                case.result = True
            else:
                case.result = False

        subtitle_room_page.auto_function.click_create()

        # [F73] 2.1 Content > Timeline clip > Audio Track only
        with uuid('9774aeb8-01f6-4169-8de3-6abfd0789226') as case:
            # [F77] 2.1 Content > Auto Format > WAV
            with uuid('19a9f689-37f9-4154-8b05-cc9a69b2d026') as case:
                for x in range(200):
                    if main_page.exist(L.subtitle_room.handle_progress_dialog.btn_cancel):
                        time.sleep(DELAY_TIME)
                    else:
                        break

                # get total subtitle rows
                current_rows = self.get_total_subtitle_rows()

                if current_rows > 1:
                    case.result = True
                else:
                    case.result = False
                logger(current_rows)

            if current_rows > 1:
                case.result = True
            else:
                case.result = False

        # [F38] 1.3 More [...] > Clear All Subtitles > Enable
        with uuid('0a03ead2-df7a-4d7c-81bd-1b149e566df8') as case:
            subtitle_room_page.more.click_clear_all_subtitles()
            time.sleep(DELAY_TIME)
            current_image = subtitle_room_page.snapshot(locator=L.subtitle_room.subtitle_region.main_content)
            check_preview = subtitle_room_page.compare(default_empty_image, current_image, similarity=0.99)
            case.result = check_preview

        # [F37] 1.3 More [...] > Clear All Subtitles > Disable when no subtitle existed
        with uuid('d6f324c4-8c98-40f4-94e6-9036a5d4a9c2') as case:
            check_status = subtitle_room_page.more.get_clear_all_subtitle_status()
            case.result = not check_status

        main_page.click_undo()

        # [F139] 3.1 Edit buttons > Merge and Split > Split > Disable
        with uuid('6469d6f8-90fa-4565-8ef5-90d02e03a6ec') as case:
            subtitle_room_page.multiple_select_subtitle_row(1, 2, 3)
            check_status = subtitle_room_page.get_split_btn()
            case.result = not check_status

        # [F129] 3.1 Edit buttons > Change subtitle text format > Confirmation > OK
        with uuid('a4003d03-767c-473f-9db4-50da3c2c1868') as case:
            # [F126] 3.1 Edit buttons > Change subtitle text format > Border > Select with customize
            with uuid('b86d3223-2fed-4ea4-a57f-ce2f5d1d03b9') as case:
                subtitle_room_page.click_change_subtitle_format()
                subtitle_room_page.character.set_border_color('BC9E00')
                subtitle_room_page.character.click_ok()

                subtitle_room_page.select_subtitle_row(2)
                subtitle_room_page.click_change_subtitle_format()
                check_border = subtitle_room_page.character.get_border_color()
                if check_border == 'BC9E00':
                    case.result = True
                else:
                    case.result = False

            if check_border == 'BC9E00':
                case.result = True
            else:
                case.result = False
            subtitle_room_page.character.click_ok()

        # [F36] 1.3 > More [...] > Export an SRT File > Enable / Abile to export subtitle correctly
        with uuid('f5afd1b1-9ec7-4424-81a0-772231d67192') as case:
            srt_export_folder = Test_Material_Folder + 'Subtitle_Room/Export/no_font/'
            if main_page.exist_file(srt_export_folder + 'test_1_4_JPN_No_font.srt'):
                main_page.delete_folder(srt_export_folder)
            time.sleep(DELAY_TIME)
            subtitle_room_page.more.click_export_str(1)
            main_page.handle_save_file_dialog('test_1_4_JPN_No_font.srt', srt_export_folder)

            # Clear all subtitle
            subtitle_room_page.more.click_clear_all_subtitles()

            # Verify Step: Import srt directly
            # Import subtitle w/o style formatting
            subtitle_room_page.more.click_import_subtitle_file()
            main_page.handle_open_project_dialog(srt_export_folder +'test_1_4_JPN_No_font.srt')

            time.sleep(DELAY_TIME)

            # Verify step
            # get total subtitle rows
            check_current_rows = self.get_total_subtitle_rows()

            check_diff = check_current_rows - current_rows
            if check_diff == 0:
                case.result = True
            else:
                case.result = False

        # [F28] 1.2 > Export Subtitle > Export without style formatting > srt file is created correctly
        with uuid('f81d78ea-9f45-47b1-9af0-c036c0bedb7f') as case:
            if main_page.exist_file(srt_export_folder + 'test_1_4_JPN_No_font.srt'):
                case.result = True
            else:
                case.result = False

        # [F29] 1.2 > Export Subtitle > Export without style formatting > Import to check Bold are saved in SRT file
        with uuid('886f4c44-1ad3-4c4e-ac9e-f45b93b71f08') as case:
            subtitle_room_page.select_subtitle_row(2)
            subtitle_room_page.click_change_subtitle_format()
            check_border = subtitle_room_page.character.get_border_color()
            if check_border == '000000':
                case.result = True
            else:
                case.result = False

            subtitle_room_page.character.click_ok()

        # [F88] 3.1 Edit buttons > Add a subtitle > Error handling (gap is less then 0.2 sec)
        with uuid('9f8aee9a-9232-4765-b0af-4ec9b363ec32') as case:
            subtitle_room_page.select_subtitle_row(1)
            subtitle_room_page.click_add_btn()
            time.sleep(DELAY_TIME)
            case.result = subtitle_room_page.handle_mini_duration_warning_message()

    # 10 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_5(self):
        # [F72] 2.1 > Content > Timeline clip > Video Track only > show warning when Auto Transcribe Subtitle
        with uuid('56567cd3-52b2-4aeb-af47-fc85143d02a7') as case:
            # Select template "Landscape 01.jpg" to track1
            main_page.select_library_icon_view_media("Landscape 01.jpg")
            main_page.tips_area_insert_media_to_selected_track()

            # Press hotkey to enter (Subtitle Room)
            main_page.tap_SubtitleRoom_hotkey()

            # Click (Auto Transcribe Subtitle)
            subtitle_room_page.library_menu.click_auto_transcribe()

            # handle Warning message
            check_result = subtitle_room_page.handle_selected_track_no_audio_source()
            case.result = check_result

        # [F48] 2.1 > Window Control & Confirmation > Cancel
        with uuid('fd4f0f60-4902-4378-af24-d768cd105dbc') as case:
            subtitle_room_page.auto_function.click_cancel()
            time.sleep(DELAY_TIME)
            cancel_btn = main_page.exist(L.subtitle_room.speech_to_text_window.btn_cancel)
            if cancel_btn:
                case.result = False
            else:
                case.result = True

        main_page.tap_MediaRoom_hotkey()

        # Open project
        main_page.top_menu_bar_file_open_project('no')
        project_path = Test_Material_Folder + 'Subtitle_Room/Test_CHT_project.pds'
        main_page.handle_open_project_dialog(project_path)
        time.sleep(DELAY_TIME*2)
        main_page.handle_merge_media_to_current_library_dialog('no')

        # Select timeline range: 5 sec ~ 25 sec
        timeline_operation_page.set_range_markin_markout(150, 750)

        # Move mouse to CTI left position > Right click > Select menu
        timeline_operation_page.move_mouse_to_CTI_position(1, True)
        main_page.right_click()
        time.sleep(DELAY_TIME * 5)
        main_page.select_right_click_menu('Speech to Text')

        # [F66] 2.1 > Settings Dialog > Language > CHT
        with uuid('06afb82d-4247-43af-80a4-9163486b8006') as case:
            subtitle_room_page.auto_function.select_LANG('CHT')
            check_setting_lang = subtitle_room_page.auto_function.get_LANG_status()
            if check_setting_lang == "Mandarin Chinese (Taiwan)":
                lang_setting = True
            else:
                lang_setting = False

            subtitle_room_page.auto_function.click_create()

            for x in range(200):
                if main_page.exist(L.subtitle_room.handle_progress_dialog.btn_cancel):
                    time.sleep(DELAY_TIME)
                else:
                    break

            # get total subtitle rows
            current_rows = self.get_total_subtitle_rows()

            if current_rows > 1:
                auto_status = True
            else:
                auto_status = False

            case.result = lang_setting and auto_status

        # [F34] 1.3 > More > Import Subtitle from File
        with uuid('8b8d3771-be45-4fec-9b48-d080aeae8290') as case:
            # Cancel range selection
            main_page.timeline_select_track(2)

            # Import w/ additional style font SRT file
            subtitle_room_page.more.click_import_subtitle_file()
            srt_file_path = Test_Material_Folder + 'Subtitle_Room/Subtitle_CHT_SRT_font.srt'
            main_page.handle_open_project_dialog(srt_file_path)
            subtitle_room_page.handle_replace_all_existing_subtitle_text()
            time.sleep(DELAY_TIME*2)

            playback_window_page.set_timecode_slidebar('00_00_14_29')
            time.sleep(DELAY_TIME*1.5)
            current_image = subtitle_room_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'F34_preview.png')

            # logger(current_image)
            check_preview = subtitle_room_page.compare(Ground_Truth_Folder + 'F34_preview.png', current_image)
            case.result = check_preview

        # [F15] 1.2 > Subtitle Import > Srt > Font Size (Display correctly)
        with uuid('697041b9-fa31-4c5b-9794-956f0822be82') as case:
            subtitle_room_page.select_subtitle_row(7)
            subtitle_room_page.click_change_subtitle_format()
            check_size = subtitle_room_page.character.get_size()
            if check_size == '48':
                case.result = True
            else:
                case.result = False

            subtitle_room_page.character.click_ok()

        # [F114] 3.1 > Change subtitle text format > Size > Customize
        with uuid('1b817912-6d59-4581-ab4e-cb26139ff03b') as case:
            subtitle_room_page.click_change_subtitle_format()
            subtitle_room_page.character.apply_size('64')
            subtitle_room_page.character.click_ok()

            subtitle_room_page.click_change_subtitle_format()
            check_size = subtitle_room_page.character.get_size()
            if check_size == '64':
                case.result = True
            else:
                case.result = False

            subtitle_room_page.character.click_ok()

        # [F120] 3.1 > Change subtitle text format > Text Color > Customize
        with uuid('e430fea2-eac5-4885-9170-620a651641c4') as case:
            subtitle_room_page.select_subtitle_row(9)
            subtitle_room_page.click_change_subtitle_format()
            subtitle_room_page.character.set_text_color('B90015')
            subtitle_room_page.character.click_ok()

            subtitle_room_page.click_change_subtitle_format()
            check_size = subtitle_room_page.character.get_text_color()
            if check_size == 'B90015':
                case.result = True
            else:
                case.result = False

            subtitle_room_page.character.click_ok()

        # [F20] 1.2 > Export With Additional SubRip Stype information > Font Size
        with uuid('911fc024-f351-4d49-98a0-f575e396b0d0') as case:
            # [F22] 1.2 > Export With Additional SubRip Stype information > Font Color
            with uuid('bb4c2945-976e-41cb-b5c7-72a8a90f7e8e') as case:
                srt_export_folder = Test_Material_Folder + 'Subtitle_Room/Export/additional_font/'
                if main_page.exist_file(srt_export_folder+'test_1_5_extra_font.srt'):
                    main_page.delete_folder(srt_export_folder)
                time.sleep(DELAY_TIME)
                subtitle_room_page.more.click_export_str(0)
                main_page.handle_save_file_dialog('test_1_5_extra_font.srt', srt_export_folder)
                if main_page.exist_file(srt_export_folder + 'test_1_5_extra_font.srt'):
                    case.result = True
                else:
                    case.result = False

            if main_page.exist_file(srt_export_folder + 'test_1_5_extra_font.srt'):
                case.result = True
            else:
                case.result = False

        # [F30] 1.2 > Export subtitle > Custom File name > srt file is created correctly
        with uuid('ef34ba1b-4f20-4415-a50a-c9fbba53e193') as case:
            if main_page.exist_file(srt_export_folder + 'test_1_5_extra_font.srt'):
                case.result = True
            else:
                case.result = False

    # 10 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_6(self):
        # Import video > Select template "JPN.mp4" to track1
        audio_path = Test_Material_Folder + 'Subtitle_Room/JPN.mp4'
        time.sleep(DELAY_TIME * 3)
        media_room_page.collection_view_right_click_import_media_files(audio_path)
        time.sleep(DELAY_TIME * 2)
        main_page.insert_media('JPN.mp4')

        # Press hotkey to enter (Subtitle Room)
        main_page.tap_SubtitleRoom_hotkey()

        # Click (Auto Transcribe Subtitle)
        subtitle_room_page.library_menu.click_manually_create()
        time.sleep(DELAY_TIME)
        default_empty_image = subtitle_room_page.snapshot(locator=L.subtitle_room.subtitle_region.main_content)

        # More button > Click Auto Transcribe
        subtitle_room_page.more.click_auto_transcribe()

        # [F67] 2.1 > Settings Dialog > Transcribe selected range only checkbox > Disable
        with uuid('ebc50f93-3006-4e5d-9e1b-c941882cdd0a') as case:
            checkbox_result = subtitle_room_page.auto_function.get_selected_range_status()
            case.result = not checkbox_result

        # [F64] 2.1 > Settings Dialog > Language > JPN
        with uuid('258788eb-93d4-4861-afaa-6832b5203afd') as case:
            subtitle_room_page.auto_function.select_LANG('JPN')
            check_setting_lang = subtitle_room_page.auto_function.get_LANG_status()
            if check_setting_lang == "Japanese":
                lang_setting = True
            else:
                lang_setting = False

            # [F47] 2.1 > Settings Dialog > Window Control & Confirmation > X
            with uuid('440114cf-0201-4d72-be02-48e9bcd4a8b4') as case:
                subtitle_room_page.auto_function.click_close()
                time.sleep(DELAY_TIME)
                current_image = subtitle_room_page.snapshot(locator=L.subtitle_room.subtitle_region.main_content)
                check_preview = subtitle_room_page.compare(default_empty_image, current_image, similarity=0.99)
                case.result = check_preview

            # More button > Click Auto Transcribe
            subtitle_room_page.more.click_auto_transcribe()
            subtitle_room_page.auto_function.click_create()

            for x in range(250):
                if main_page.exist(L.subtitle_room.handle_progress_dialog.btn_cancel):
                    time.sleep(DELAY_TIME)
                else:
                    break

            # get total subtitle rows
            current_rows = self.get_total_subtitle_rows()

            if current_rows > 7:
                auto_status = True
            else:
                auto_status = False

            time.sleep(DELAY_TIME * 1.5)
            current_image = subtitle_room_page.snapshot(locator=main_page.area.preview.main,
                                                        file_name=Auto_Ground_Truth_Folder + 'F64_preview.png')

            # logger(current_image)
            check_preview = subtitle_room_page.compare(Ground_Truth_Folder + 'F64_preview.png', current_image, similarity=0.9)

            case.result = lang_setting and auto_status and check_preview

        # [F13] 1.1 > Main menu > Import subtitle from file
        with uuid('82e97f82-389e-41f8-9ed2-17a63b028f10') as case:
            # More > Clear all subtitle
            subtitle_room_page.more.click_clear_all_subtitles()
            time.sleep(DELAY_TIME)

            # Switch title room then back
            main_page.tap_TitleRoom_hotkey()
            time.sleep(DELAY_TIME)
            main_page.tap_SubtitleRoom_hotkey()

            # click main (Import subtitle from file)
            srt_file_path = Test_Material_Folder + 'Subtitle_Room/Export/additional_font/test_1_5_extra_font.srt'
            case.result = subtitle_room_page.library_menu.click_import_subtitle_file(srt_file_path)

        # [F21] 1.2 > Export subtitle > Export with Additional font > Import to check font size is correctly
        with uuid('283a5544-2b21-49b8-a753-6fff5dca6efb') as case:

            subtitle_room_page.select_subtitle_row(7)
            subtitle_room_page.click_change_subtitle_format()
            check_size = subtitle_room_page.character.get_size()
            if check_size == '64':
                 current_size = True
            else:
                current_size = False

            subtitle_room_page.character.click_ok()
            time.sleep(DELAY_TIME*1.5)
            current_image = subtitle_room_page.snapshot(locator=main_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'F21_preview.png')

            # logger(current_image)
            check_preview = subtitle_room_page.compare(Ground_Truth_Folder + 'F21_preview.png', current_image)
            case.result = current_size and check_preview

        # [F23] 1.2 > Export subtitle > Export with Additional font > Import to check font color is correctly
        with uuid('60bc7d9f-54ef-407e-a272-7007ccd924ee') as case:
            subtitle_room_page.select_subtitle_row(9)
            subtitle_room_page.click_change_subtitle_format()
            check_color = subtitle_room_page.character.get_text_color()
            if check_color == 'B90015':
                current_color = True
            else:
                current_color = False
            subtitle_room_page.character.click_ok()

            time.sleep(DELAY_TIME * 1.5)
            current_image = subtitle_room_page.snapshot(locator=main_page.area.preview.main,
                                                        file_name=Auto_Ground_Truth_Folder + 'F23_preview.png')

            # logger(current_image)
            check_preview = subtitle_room_page.compare(Ground_Truth_Folder + 'F23_preview.png', current_image)
            case.result = current_color and check_preview

        # Delete
        subtitle_room_page.click_del_btn()
        time.sleep(DELAY_TIME)
        # [F83] 3.1 > Edit buttons > Add a sbutitle marker at the current position > Multiple subtitle
        with uuid('44f71e2c-6956-422c-b29b-62a091bb800c') as case:
            subtitle_room_page.click_add_btn()
            subtitle_room_page.modify_subtitle_text(9, 'やすさにも', '許功蓋!@$こ~"だわりした')
            time.sleep(DELAY_TIME * 1.5)
            current_image = subtitle_room_page.snapshot(locator=main_page.area.preview.main,
                                                        file_name=Auto_Ground_Truth_Folder + 'F83_preview.png')

            # logger(current_image)
            check_preview = subtitle_room_page.compare(Ground_Truth_Folder + 'F83_preview.png', current_image, similarity=0.97)
            case.result = check_preview

        # [F124] 3.1 > Edit buttons > Change subtitle text format > shadow color > Select w/ customize
        with uuid('109e5608-a1cc-4131-a87c-74611b8b7743') as case:
            subtitle_room_page.click_change_subtitle_format()
            subtitle_room_page.character.set_shadow_checkbox()
            subtitle_room_page.character.set_shadow_color('0F22B5')
            subtitle_room_page.character.click_ok()

            subtitle_room_page.click_change_subtitle_format()
            check_size = subtitle_room_page.character.get_shadow_color()
            if check_size == '0F22B5':
                case.result = True
            else:
                case.result = False

        # [F117] 3.1 > Edit buttons > Change subtitle text format > Alignment > Center
        with uuid('2dff49f7-c7ee-4cf2-b871-f24007e57589') as case:
            subtitle_room_page.character.apply_align_center()
            subtitle_room_page.character.click_ok()
            time.sleep(DELAY_TIME * 1.5)
            current_image = subtitle_room_page.snapshot(locator=main_page.area.preview.main,
                                                        file_name=Auto_Ground_Truth_Folder + 'F117_preview.png')

            # logger(current_image)
            check_preview = subtitle_room_page.compare(Ground_Truth_Folder + 'F117_preview.png', current_image, similarity=0.97)
            case.result = check_preview

        # [F133] 3.1 > Edit buttons > Subtitle Search & Replace > Search > Unicode
        with uuid('3b89aae8-55e3-4f06-ae4f-fda56bd8987b') as case:
            default_status = subtitle_room_page.check_replace_button_status()
            logger(default_status)
            if default_status == False:
                default_result = True
            else:
                default_result = False
            subtitle_room_page.input_search_field('許功蓋')
            time.sleep(DELAY_TIME)
            check_search_search = subtitle_room_page.check_replace_button_status()
            logger(check_search_search)
            if check_search_search == True:
                search_result = True
            else:
                search_result = False
            case.result = default_result and search_result

    # 12 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_7(self):
        # Open project
        time.sleep(DELAY_TIME * 3)
        main_page.top_menu_bar_file_open_project()
        project_path = Test_Material_Folder + 'Subtitle_Room/Test_CHT_project.pds'
        main_page.handle_open_project_dialog(project_path)
        time.sleep(DELAY_TIME * 2)
        main_page.handle_merge_media_to_current_library_dialog('no')

        # Select timeline range: 25 sec ~ 47 sec
        timeline_operation_page.set_range_markin_markout(750, 1410)

        # [F44] 2.1 > Settings Dialog > Entry > Sbutitle Room > Open setting in subtitle room
        with uuid('1ce7206d-f7e0-4a5f-9fbf-7be7b72ab7e8') as case:
            main_page.tap_SubtitleRoom_hotkey()
            subtitle_room_page.library_menu.click_auto_transcribe()

            subtitle_room_page.auto_function.select_LANG('CHT')
            check_setting_lang = subtitle_room_page.auto_function.get_LANG_status()
            if check_setting_lang == "Mandarin Chinese (Taiwan)":
                lang_setting = True
            else:
                lang_setting = False

            time.sleep(DELAY_TIME*2)
            subtitle_room_page.auto_function.click_create()

            for x in range(200):
                if main_page.exist(L.subtitle_room.handle_progress_dialog.btn_cancel):
                    time.sleep(DELAY_TIME)
                else:
                    break

            # get total subtitle rows
            current_rows = self.get_total_subtitle_rows()

            if current_rows > 1:
                auto_status = True
            else:
                auto_status = False

            case.result = lang_setting and auto_status

        # [F108] 3.1 > Change subtitle text format > Font > Customize
        with uuid('22fe04ca-877d-4902-8125-e9b9675ace53') as case:
            subtitle_room_page.select_subtitle_row(1)
            time.sleep(DELAY_TIME*0.5)
            subtitle_room_page.click_change_subtitle_format()
            default_font = subtitle_room_page.character.get_font_type()
            logger(default_font)
            if default_font == 'Helvetica Regular':
                check_default = True
            else:
                check_default = False
            logger(check_default)

            check_setting = subtitle_room_page.character.apply_font_type('Hoefler Text Regular')
            subtitle_room_page.character.click_ok()
            time.sleep(DELAY_TIME * 0.5)
            logger(check_setting)

            case.result = check_default and check_setting

        # [F112] 3.1 > Change subtitle text format > Style > Bold Italic
        with uuid('2151151c-1ae5-40c3-becd-8a3f9c47f407') as case:

            subtitle_room_page.select_subtitle_row(1)
            time.sleep(DELAY_TIME * 0.5)
            subtitle_room_page.click_del_btn()
            playback_window_page.set_timecode_slidebar('00_00_00_00')
            time.sleep(DELAY_TIME * 1.5)
            subtitle_room_page.click_add_btn()
            subtitle_room_page.modify_subtitle_text(1, 'JDIMKVVG1Q3', 'WRx R^WE')

            subtitle_room_page.click_change_subtitle_format()
            subtitle_room_page.character.apply_Bold_Italic()
            time.sleep(DELAY_TIME * 0.5)
            check_style = subtitle_room_page.character.get_style_status()
            if check_style == 'Bold Italic':
                case.result = True
            else:
                case.result = False

        # [F118] 3.1 > Change subtitle text format > Alignment > Right
        with uuid('9191d886-2774-4521-8fe2-13dc3ccc0192') as case:
            subtitle_room_page.character.apply_size('48')
            subtitle_room_page.character.apply_align_right()
            subtitle_room_page.character.click_ok()
            time.sleep(DELAY_TIME * 1.5)
            current_image = subtitle_room_page.snapshot(locator=main_page.area.preview.main,
                                                        file_name=Auto_Ground_Truth_Folder + 'F118_preview.png')

            check_preview = subtitle_room_page.compare(Ground_Truth_Folder + 'F118_preview.png', current_image, similarity=0.97)
            case.result = check_preview

        # handle subtitle row 2, row 3, row 4, ...
        # modify subtitle content to the same string
        total_row = self.get_total_subtitle_rows()
        logger(total_row)
        x = 0
        round_times = total_row+1
        for x in range(round_times):
            if x <= 1:
                continue

            subtitle_room_page.select_subtitle_row(x)
            time.sleep(DELAY_TIME * 0.5)
            subtitle_room_page.click_del_btn()
            time.sleep(DELAY_TIME * 0.5)
            subtitle_room_page.click_add_btn()
            subtitle_room_page.modify_subtitle_text(x, 'JDIMKVVG1Q9A6')

        # [F128] 3.1 > Change subtitle text format > [Apply to All] button
        with uuid('6ac997d9-7593-41c2-9b23-450a398f60fc') as case:
            # modify subtitle 2
            subtitle_room_page.select_subtitle_row(2)
            time.sleep(DELAY_TIME * 0.5)
            subtitle_room_page.click_change_subtitle_format()

            subtitle_room_page.character.apply_font_type('Myanmar MN')
            subtitle_room_page.character.apply_size('64')
            subtitle_room_page.character.click_ok()
            time.sleep(DELAY_TIME * 0.5)

            # modify subtitle 3 font then [Apply to all]
            subtitle_room_page.select_subtitle_row(3)
            time.sleep(DELAY_TIME * 0.5)
            subtitle_room_page.click_change_subtitle_format()

            subtitle_room_page.character.apply_font_type('LaffRiotNF')
            subtitle_room_page.character.apply_size('72')
            subtitle_room_page.character.set_text_color('CBA7FF')
            subtitle_room_page.character.apply_to_all()
            time.sleep(DELAY_TIME * 0.5)

            # Verify Step
            # Check subtitle 1
            subtitle_room_page.select_subtitle_row(1)
            current_image = subtitle_room_page.snapshot(locator=main_page.area.preview.main,
                                                        file_name=Auto_Ground_Truth_Folder + 'F128_preview.png')

            check_timeline_preview = subtitle_room_page.compare(Ground_Truth_Folder + 'F128_preview.png', current_image,
                                                       similarity=0.97)

            # Check subtitle 2
            subtitle_room_page.select_subtitle_row(2)
            subtitle_room_page.click_change_subtitle_format()
            check_subtitle_size = subtitle_room_page.character.get_size()
            logger(check_subtitle_size)
            if check_subtitle_size == '72':
                check_size_OK = True
            else:
                check_size_OK = False

            check_subtitle_font = subtitle_room_page.character.get_font_type()
            logger(check_subtitle_font)
            logger(len(check_subtitle_font))
            if check_subtitle_font == 'LaffRiotNF Regular':
                check_font = True
            else:
                check_font = False

            check_subtitle_color = subtitle_room_page.character.get_text_color()
            logger(check_subtitle_color)
            if check_subtitle_color == 'CBA7FF':
                check_color = True
            else:
                check_color = False

            case.result = check_timeline_preview and check_size_OK and check_font and check_color
            subtitle_room_page.character.click_ok()

        # [F132] 3.1 > Subtitle Search & Replace > Search Character
        with uuid('cfa4d04b-3c49-46ac-869d-13ba6d1b6908') as case:
            default_status = subtitle_room_page.check_replace_button_status()
            logger(default_status)
            if default_status == False:
                default_result = True
            else:
                default_result = False
            subtitle_room_page.input_search_field('VVG1Q')
            time.sleep(DELAY_TIME)
            check_search_search = subtitle_room_page.check_replace_button_status()
            logger(check_search_search)
            if check_search_search == True:
                search_result = True
            else:
                search_result = False
            case.result = default_result and search_result

        # [F134] 3.1 > Subtitle Search & Replace > Replace selected
        with uuid('648cf89a-4cb4-4b9b-adda-402fa0c00ea6') as case:
            subtitle_room_page.click_replace_button()
            # 出門（泰文）
            subtitle_room_page.input_replace_field('ออกไป')

            # Apply 3rd subtitle (Click [NEXT] button twice)
            subtitle_room_page.click_next_button(times=2)
            subtitle_room_page.click_replace_single_button()

            # Verify Step
            # Check subtitle 3
            subtitle_room_page.select_subtitle_row(3)
            current_image = subtitle_room_page.snapshot(locator=main_page.area.preview.main,
                                                        file_name=Auto_Ground_Truth_Folder + 'F134_row3_preview.png')

            check_timeline_preview_3 = subtitle_room_page.compare(Ground_Truth_Folder + 'F134_row3_preview.png', current_image,
                                                       similarity=0.97)

            # Check subtitle 1
            subtitle_room_page.select_subtitle_row(1)
            time.sleep(DELAY_TIME*2)
            current_image = subtitle_room_page.snapshot(locator=main_page.area.preview.main,
                                                        file_name=Auto_Ground_Truth_Folder + 'F134_row1_preview.png')

            check_timeline_preview_1 = subtitle_room_page.compare(Ground_Truth_Folder + 'F134_row1_preview.png', current_image,
                                                       similarity=0.97)

            case.result = check_timeline_preview_3 and check_timeline_preview_1

        # [F135] 3.1 > Subtitle Search & Replace > Replace All
        with uuid('41ada33e-1de1-4794-8087-9247c5543354') as case:
            subtitle_room_page.cancel_search()
            subtitle_room_page.input_search_field('JDIMK')
            time.sleep(DELAY_TIME)
            #subtitle_room_page.click_replace_button()

            # 你好（泰文）
            subtitle_room_page.input_replace_field('สวัสดี')

            # Replace all
            subtitle_room_page.click_replace_all_button()

            # Verify Step
            # Check subtitle 3
            subtitle_room_page.select_subtitle_row(3)
            current_image = subtitle_room_page.snapshot(locator=main_page.area.preview.main,
                                                        file_name=Auto_Ground_Truth_Folder + 'F135_row3_preview.png')

            check_timeline_preview_3 = subtitle_room_page.compare(Ground_Truth_Folder + 'F135_row3_preview.png', current_image,
                                                       similarity=0.97)

            # Check subtitle 1
            subtitle_room_page.select_subtitle_row(1)
            current_image = subtitle_room_page.snapshot(locator=main_page.area.preview.main,
                                                        file_name=Auto_Ground_Truth_Folder + 'F135_row1_preview.png')

            check_timeline_preview_1 = subtitle_room_page.compare(Ground_Truth_Folder + 'F135_row1_preview.png', current_image,
                                                       similarity=0.97)

            case.result = check_timeline_preview_3 and check_timeline_preview_1

        # [F144] 3.2 > Subtitle List > Start time > Display
        with uuid('3c40c70a-bc20-4d06-9be2-6e4182796230') as case:
            get_current_time = subtitle_room_page.get_start_time(1)
            logger(get_current_time)

            if get_current_time == '00;00;25;00':
                case.result = True
            else:
                case.result = False

        # [F140] 3.1 > Merge and split > split enable (when selecting one subtitle)
        with uuid('621d5da0-6c05-4957-84cd-47ed03ce6712') as case:
            check_status = subtitle_room_page.get_split_btn()
            case.result = check_status

        # [F141] 3.1 > Merge and split > Sbutitle is able to split to two subtitle
        with uuid('b4f7d0ae-fa82-4549-8dc0-fc23c27fd657') as case:
            # Click [Split]
            subtitle_room_page.click_split_btn()

            # Verify Preview
            time.sleep(DELAY_TIME*2)
            current_image = subtitle_room_page.snapshot(locator=main_page.area.preview.main,
                                                        file_name=Auto_Ground_Truth_Folder + 'F141_row2_preview.png')

            check_timeline_preview_2 = subtitle_room_page.compare(Ground_Truth_Folder + 'F141_row2_preview.png',
                                                                  current_image,
                                                                  similarity=0.97)

            # Verify total rows
            current_total_row = self.get_total_subtitle_rows()
            check_diff = current_total_row - total_row
            if check_diff == 1:
                split_count = True
            else:
                split_count = False

            case.result = check_timeline_preview_2 and split_count

        # [F158] 3.2 > Subtitle Text > Text Input > Multiple lines
        with uuid('3897051f-b05d-4af2-85c6-358e278dd6ce') as case:
            # Check subtitle 1
            subtitle_room_page.select_subtitle_row(1)
            current_image = subtitle_room_page.snapshot(locator=main_page.area.preview.main,
                                                        file_name=Auto_Ground_Truth_Folder + 'F158_row1_preview.png')

            check_multiple_lines = subtitle_room_page.compare(Ground_Truth_Folder + 'F158_row1_preview.png', current_image,
                                                       similarity=0.97)
            case.result = check_multiple_lines

    # 9 uuid
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_8(self):
        # Import video > Select template "movie_music.m4a" to track1
        audio_path = Test_Material_Folder + 'Subtitle_Room/movie_music.m4a'
        time.sleep(DELAY_TIME * 3)
        media_room_page.collection_view_right_click_import_media_files(audio_path)
        time.sleep(DELAY_TIME * 2)
        main_page.insert_media('movie_music.m4a')

        # enter Subtitle Room
        main_page.click(L.subtitle_room.btn_subtitle_room)
        time.sleep(DELAY_TIME*2)

        # Main Menu > Auto Transcribe Subtitle
        subtitle_room_page.library_menu.click_auto_transcribe()

        # Set lang to CHT
        subtitle_room_page.auto_function.select_LANG('CHT')
        time.sleep(DELAY_TIME * 2)

        check_lang = subtitle_room_page.auto_function.get_LANG_status()
        if check_lang == "Mandarin Chinese (Taiwan)":
            lang_OK = True
        else:
            lang_OK = False

        time.sleep(DELAY_TIME*2)
        subtitle_room_page.auto_function.click_create()

        for x in range(200):
            if main_page.exist(L.subtitle_room.handle_progress_dialog.btn_cancel):
                time.sleep(DELAY_TIME)
            else:
                break

        # get total subtitle rows
        current_rows = self.get_total_subtitle_rows()

        if current_rows > 1:
            auto_status = True
        else:
            auto_status = False

        check_result = lang_OK and auto_status
        if not check_result:
            logger(f'Speech to text got some problem,  lang_OK:{lang_OK}, auto_status:{auto_status}')
            raise Exception
        logger(check_result)

        # [F162] 3.2 > Right click menu > Select all Sbutitles
        with uuid('47d9129c-7b19-4944-92ad-5e180b80cd04') as case:
            subtitle_room_page.select_subtitle_row(1)
            time.sleep(DELAY_TIME)
            main_page.right_click()
            main_page.select_right_click_menu('Select All Subtitles')

            time.sleep(DELAY_TIME)
            main_page.right_click()
            main_page.select_right_click_menu('Delete')
            time.sleep(DELAY_TIME)
            current_image = subtitle_room_page.snapshot(locator=L.subtitle_room.subtitle_region.main_content,
                                                      file_name=Auto_Ground_Truth_Folder + 'F141_subtitle_room.png')

            # Should delete all subtitle > Subtitle_Room should back to default empty (012_subtitle_library.png)
            check_preview = subtitle_room_page.compare(Ground_Truth_Folder + '012_subtitle_library.png', current_image)
            case.result = check_preview

        main_page.click_undo()
        # [F150] 3.2 > End Time > Display > Current Time
        with uuid('5a5e1e5c-4849-45ad-8e3d-982a5636c5fb') as case:
            subtitle_room_page.select_subtitle_row(current_rows)
            end_timecode = subtitle_room_page.get_end_time(current_rows)
            #logger(end_timecode.replace(":", "_"))
            playback_window_page.set_timecode_slidebar(end_timecode.replace(":", "_"))

            current_image = subtitle_room_page.snapshot(locator=main_page.area.preview.only_mtk_view,
                                                        file_name=Auto_Ground_Truth_Folder + 'F150_preview.png')

            check_preview = subtitle_room_page.compare(Ground_Truth_Folder + 'F150_preview.png', current_image, similarity=0.97)
            case.result = check_preview

        # [F138] 3.1 > Merge > Enable > Selected subtitle are able to merge correctly
        with uuid('d777492a-a972-4333-98ce-34bf4a682d71') as case:
            # [F137] 3.1 > Merge > Enable > Enable when selecting multiple subtitles
            with uuid('7010301f-4ec5-4771-931e-c034a95c9fb1') as case:
                subtitle_room_page.modify_subtitle_text(current_rows - 1, '特急で軽井沢へ')
                subtitle_room_page.click_change_subtitle_format()
                subtitle_room_page.character.apply_size('22')
                subtitle_room_page.character.set_text_color('9BFFAA')
                subtitle_room_page.character.click_ok()
                time.sleep(DELAY_TIME * 0.5)

                subtitle_room_page.modify_subtitle_text(current_rows, '期間限定クーポン販売中')

                subtitle_room_page.multiple_select_subtitle_row(current_rows - 1, current_rows)
                case.result = subtitle_room_page.get_merge_btn()

            subtitle_room_page.click_merge_btn()

            current_image = subtitle_room_page.snapshot(locator=main_page.area.preview.only_mtk_view,
                                                        file_name=Auto_Ground_Truth_Folder + 'F138_preview.png')

            check_preview = subtitle_room_page.compare(Ground_Truth_Folder + 'F138_preview.png', current_image)
            case.result = check_preview

        # [F157] 3.2 > Subtitle list > Subtitle Text > Text Input > Single line
        with uuid('aacb1753-bb54-447f-a30a-3a5ab08de751') as case:
            # 外面下著大雨路面積水 (泰文）
            subtitle_room_page.modify_subtitle_text(current_rows -1, 'ข้างนอกฝนตกหนักน้ำท่วมถนน')
            current_image = subtitle_room_page.snapshot(locator=main_page.area.preview.only_mtk_view,
                                                        file_name=Auto_Ground_Truth_Folder + 'F157_preview.png')

            check_preview = subtitle_room_page.compare(Ground_Truth_Folder + 'F157_preview.png', current_image)
            case.result = check_preview

        # [F145] 3.2 > Subtitle list > Start Time > Display > Time modify
        with uuid('dbffa43c-47e1-4d32-880b-c7c06a7d76df') as case:
            get_row_1_end_time = subtitle_room_page.get_end_time(1)
            get_row_2_start_time = subtitle_room_page.get_start_time(2)
            if get_row_1_end_time != get_row_2_start_time:
                subtitle_room_page.set_start_time(2, get_row_1_end_time.replace(":", "_"))
            else:
                logger('Cannot modify start time')

            get_row_2_start_time = subtitle_room_page.get_start_time(2)
            if get_row_2_start_time == get_row_1_end_time:
                case.result = True
            else:
                case.result = False

        # [F103] 3.1 Edit buttons > Adjust subtitle position > Adjustment method > Input
        with uuid('83d1ad3c-a169-4842-8e89-3a3a67dcd9e2') as case:
            subtitle_room_page.click_adjust_pos_btn()
            time.sleep(DELAY_TIME)
            subtitle_room_page.position.set_x_value(0.25)
            subtitle_room_page.position.set_y_value(0.13)
            subtitle_room_page.position.close_window()

            subtitle_room_page.click_adjust_pos_btn()
            time.sleep(DELAY_TIME)
            current_x = subtitle_room_page.position.get_x_value()
            current_y = subtitle_room_page.position.get_y_value()
            if current_x == '0.25' and current_y == '0.13':
                case.result = True
            else:
                case.result = False

            subtitle_room_page.position.close_window()

        # [F105] 3.1 Edit buttons > Adjust subtitle position > Adjustment method > Apply to All
        with uuid('818e9040-0e88-4989-935a-5c631c01e43e') as case:
            subtitle_room_page.click_adjust_pos_btn()
            time.sleep(DELAY_TIME)
            subtitle_room_page.position.apply_to_all()

            # Verify Step:
            subtitle_room_page.select_subtitle_row(current_rows - 1)
            subtitle_room_page.click_adjust_pos_btn()
            time.sleep(DELAY_TIME)
            current_x = subtitle_room_page.position.get_x_value()
            current_y = subtitle_room_page.position.get_y_value()
            if current_x == '0.25' and current_y == '0.13':
                check_setting = True
            else:
                check_setting = False
            subtitle_room_page.position.close_window()

            current_image = subtitle_room_page.snapshot(locator=main_page.area.preview.only_mtk_view,
                                                        file_name=Auto_Ground_Truth_Folder + 'F105_preview.png')
            check_preview = subtitle_room_page.compare(Ground_Truth_Folder + 'F105_preview.png', current_image)
            case.result = check_preview and check_setting

        # [F104] 3.1 Edit buttons > Adjust subtitle position > Adjustment method > Reset
        with uuid('21cc4b6a-6980-44f1-875a-72231a939b88') as case:
            subtitle_room_page.click_adjust_pos_btn()
            time.sleep(DELAY_TIME)

            subtitle_room_page.position.click_reset_btn()
            subtitle_room_page.position.close_window()

            # Verify Step: After reset, preview should be the same w/ F157
            current_image = subtitle_room_page.snapshot(locator=main_page.area.preview.only_mtk_view)
            check_preview = subtitle_room_page.compare(Ground_Truth_Folder + 'F157_preview.png', current_image)
            case.result = check_preview