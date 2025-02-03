import sys, os

from SFT.globals import update_report_info, get_enable_case_execution_log, google_sheet_execution_log_init, \
    google_sheet_execution_log_update_result

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
base_page = PageFactory().get_page_object('base_page', mwc)
media_room_page = PageFactory().get_page_object('media_room_page', mwc)
tips_area_page = PageFactory().get_page_object('tips_area_page', mwc)
timeline_page = PageFactory().get_page_object('timeline_page', mwc)
playback_window_page = PageFactory().get_page_object('playback_window_page',mwc)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mwc)
keyframe_room_page = PageFactory().get_page_object('keyframe_room_page', mwc)


# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Mark Clips that Have Been Inserted into Timeline.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder - Setup for Overall Project
Ground_Truth_Folder = app.ground_truth_root + '/Mark_Clips/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Mark_Clips/'
Test_Material_Folder = app.testing_material

# For Ground Truth / Test Material folder - Setup for Duncan personal testing
# Ground_Truth_Folder = '/Users/cl/Desktop/Duncan/SFT/GroundTruth/Title_Room/'
# Auto_Ground_Truth_Folder = '/Users/cl/Desktop/Duncan/SFT/ATGroundTruth/Title_Room/'
# Test_Material_Folder = '/Users/cl/Desktop/Duncan/Material/'

DELAY_TIME = 1

class Test_Mark_Clips():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        time.sleep(DELAY_TIME*4)
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
            google_sheet_execution_log_init('Mark_Clips')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"test case template result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           report.get_ovinfo('skip'),
                           report.get_ovinfo('duration'))
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                               report.get_ovinfo('skip'),
                               report.get_ovinfo('duration'))
        report.show()

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_1_1(self):
        with uuid("a001ea6a-2d3e-4d03-9277-0803eb067c95") as case:

            main_page.close_and_restart_app()
            time.sleep(3)

            # Insert Sample Photo clip case...
            # 1.1 General
            main_page.set_project_aspect_ratio_16_9()

            # Snapshot Photo clip icon from Library
            before_image = main_page.snapshot_library_insert_icon('Landscape 02.jpg', file_name=Auto_Ground_Truth_Folder + 'H10_Photo_Mark_Before.png')

            # Insert Photo clip to timeline
            main_page.insert_media('Landscape 02.jpg')

            # Snapshot Inserted Photo Clip icon from Library
            after_image = main_page.snapshot_library_insert_icon('Landscape 02.jpg', file_name=Auto_Ground_Truth_Folder + 'H10_Photo_Mark_After.png')
            logger(after_image)

            # Verify Mark Clip is correct or NOT
            compare_result = media_room_page.compare(after_image, before_image)
            case.result = not compare_result


        with uuid("12748311-73f3-4f0e-a106-c6ffc40666a7") as case:
            # Insert Sample Video clip case...
            # Undo
            main_page.click_undo()

            # Snapshot Video clip icon from Library
            before_image = main_page.snapshot_library_insert_icon('Skateboard 01.mp4', file_name=Auto_Ground_Truth_Folder + 'H11_Video_Mark_Before.png')

            # Insert Video clip to timeline
            main_page.insert_media('Skateboard 01.mp4')

            # Snapshot Inserted Video Clip icon from Library
            after_image = main_page.snapshot_library_insert_icon('Skateboard 01.mp4', file_name=Auto_Ground_Truth_Folder + 'H11_Video_Mark_After.png')
            logger(after_image)

            # Verify Mark Clip is correct or NOT
            compare_result = media_room_page.compare(after_image, before_image)
            case.result = not compare_result


        with uuid("3fe908da-b03f-4abf-93e9-6b313c2a4ccf") as case:
            # Insert Sample Audio clip case...
            # Undo
            main_page.click_undo()

            # Snapshot Audio clip icon from Library
            before_image = main_page.snapshot_library_insert_icon('Mahoroba.mp3', file_name=Auto_Ground_Truth_Folder + 'H12_Audio_Mark_Before.png')

            # Insert Audio clip to timeline
            main_page.insert_media('Mahoroba.mp3')

            # Snapshot Inserted Audio Clip icon from Library
            after_image = main_page.snapshot_library_insert_icon('Mahoroba.mp3', file_name=Auto_Ground_Truth_Folder + 'H12_Audio_Mark_After.png')
            logger(after_image)

            # Verify Mark Clip is correct or NOT
            compare_result = media_room_page.compare(after_image, before_image)
            case.result = not compare_result


        with uuid("16a3efa5-b2f1-4d23-9991-b5619504bdef") as case:
            # Insert "Sample Clip" case...
            # Undo
            main_page.click_undo()

            # Snapshot Sample clip icon from Library
            before_image = main_page.snapshot_library_insert_icon('Skateboard 02.mp4', file_name=Auto_Ground_Truth_Folder + 'H13_Sample_Mark_Before.png')

            # Insert Sample clip to timeline
            main_page.insert_media('Skateboard 02.mp4')

            # Snapshot Inserted Sample Clip icon from Library
            after_image = main_page.snapshot_library_insert_icon('Skateboard 02.mp4', file_name=Auto_Ground_Truth_Folder + 'H13_Sample_Mark_After.png')
            logger(after_image)

            # Verify Mark Clip is correct or NOT
            compare_result = media_room_page.compare(after_image, before_image)
            case.result = not compare_result


        with uuid("1fbb7dd1-e68a-4d89-b070-28df90516c90") as case:
            # Insert "Imported Clip" case...

            main_page.close_and_restart_app()
            time.sleep(2)

            # Import Video clip
            material_path = Test_Material_Folder + 'Mark_Clips/1.mp4'
            logger(material_path)
            media_room_page.import_media_file(material_path)

            """
            logger(material_path)
            media_room_page.import_media_file(material_path)
            media_room_page.high_definition_video_confirm_dialog_click_no()
            main_page.insert_media('1.mp4')
            """
            time.sleep(1)
            # Snapshot Imported Video Clip icon from Library
            before_image = main_page.snapshot_library_insert_icon('1.mp4', file_name=Auto_Ground_Truth_Folder + 'H14_Imported_Mark_Before.png')

            # Insert Imported Video clip to timeline
            main_page.insert_media('1.mp4')

            time.sleep(1)
            # Snapshot Inserted Imported Clip icon from Library
            after_image = main_page.snapshot_library_insert_icon('1.mp4', file_name=Auto_Ground_Truth_Folder + 'H14_Imported_Mark_After.png')
            logger(after_image)

            # Verify Mark Clip is correct or NOT
            compare_result = media_room_page.compare(after_image, before_image)
            case.result = not compare_result


        with uuid("27473d54-3719-4a66-99d3-642f360ca6d7") as case:
            # Insert "Single Clip" case...

            main_page.close_and_restart_app()
            time.sleep(2)

            # Snapshot Single clip icon from Library
            before_image = main_page.snapshot_library_insert_icon('Landscape 02.jpg', file_name=Auto_Ground_Truth_Folder + 'H15_Single_Mark_Before.png')

            # Insert Single clip to timeline
            main_page.insert_media('Landscape 02.jpg')

            time.sleep(1)
            # Snapshot Inserted Single Clip icon from Library
            after_image = main_page.snapshot_library_insert_icon('Landscape 02.jpg', file_name=Auto_Ground_Truth_Folder + 'H15_Single_Mark_After.png')
            logger(after_image)

            # Verify Mark Clip is correct or NOT
            compare_result = media_room_page.compare(after_image, before_image)
            case.result = not compare_result



        with uuid("7cde9daf-b1aa-492c-b3b1-583795d57a75") as case:
            # Insert "Multiple Clips" case...

            main_page.close_and_restart_app()
            time.sleep(2)

            # Snapshot Multiple clips icon from Library
            before_image1 = main_page.snapshot_library_insert_icon('Skateboard 01.mp4', file_name=Auto_Ground_Truth_Folder + 'H16_Sample1_Mark_Before.png')
            before_image2 = main_page.snapshot_library_insert_icon('Skateboard 02.mp4', file_name=Auto_Ground_Truth_Folder + 'H16_Sample2_Mark_Before.png')

            # Select Multiple clips and Insert to timeline
            main_page.select_library_icon_view_media("Skateboard 01.mp4")
            main_page.tap_command_and_hold()
            main_page.select_library_icon_view_media("Skateboard 02.mp4")
            tips_area_page.click_TipsArea_btn_insert()
            main_page.release_command_key()

            time.sleep(1)
            # Snapshot Inserted Multiple clips icon from Library
            after_image1 = main_page.snapshot_library_insert_icon('Skateboard 01.mp4', file_name=Auto_Ground_Truth_Folder + 'H16_Sample1_Mark_After.png')
            after_image2 = main_page.snapshot_library_insert_icon('Skateboard 02.mp4', file_name=Auto_Ground_Truth_Folder + 'H16_Sample2_Mark_After.png')

            # Verify Mark Clips are correct or NOT
            compare_result1 = media_room_page.compare(after_image1, before_image1)
            compare_result2 = media_room_page.compare(after_image2, before_image2)
            case.result = not compare_result1 and not compare_result2


        with uuid("20efa788-a616-4cfa-9c07-dc84bdddf084") as case:
            # Insert Clip to check "Undo" & "Redo" case..
            # Restart PDR
            main_page.close_and_restart_app()
            time.sleep(1)

            # Snapshot Sample clip icon from Library
            before_image = main_page.snapshot_library_insert_icon('Skateboard 01.mp4',
                                                                  file_name=Auto_Ground_Truth_Folder + 'H20_UndoRedo_Mark_Before.png')

            # Insert Sample clip to timeline
            main_page.insert_media('Skateboard 01.mp4')

            # Undo
            main_page.click_undo()

            time.sleep(1)
            # Snapshot Inserted Clip icon w/ Undo from Library
            after_image1 = main_page.snapshot_library_insert_icon('Skateboard 01.mp4',
                                                                 file_name=Auto_Ground_Truth_Folder + 'H20_Undo_Mark_After.png')
            logger(after_image1)

            # Redo
            main_page.click_redo()
            # Snapshot Inserted Clip icon w/ Undo + Redo from Library
            after_image2 = main_page.snapshot_library_insert_icon('Skateboard 01.mp4',
                                                                 file_name=Auto_Ground_Truth_Folder + 'H20_Redo_Mark_After.png')
            logger(after_image2)

            time.sleep(1)
            # Verify Mark Clip is correct or NOT
            compare_result1 = media_room_page.compare(after_image1, before_image1)
            compare_result2 = media_room_page.compare(after_image2, before_image2)
            case.result = compare_result1 and not compare_result2


    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid("040a0175-dbd3-4e80-8dae-44d7c5917f68") as case:
            # Insert Clip to check "Trim" case..
            # Snapshot Sample Video clip icon from Library
            before_image = main_page.snapshot_library_insert_icon('Skateboard 01.mp4', file_name=Auto_Ground_Truth_Folder + 'H18_Trim_Mark_Before.png')

            # Select Sample Video clip and Insert to timeline
            main_page.select_library_icon_view_media("Skateboard 01.mp4")
            tips_area_page.click_TipsArea_btn_insert()

            # Trim Sample Video clip
            timeline_operation_page.drag_timeline_clip('Last', 0.5, 0, 0)

            time.sleep(1)
            # Snapshot Inserted Clip icon from Library
            after_image = main_page.snapshot_library_insert_icon('Skateboard 01.mp4', file_name=Auto_Ground_Truth_Folder + 'H18_Trim_Mark_After.png')

            # Verify Mark Clip is correct or NOT
            compare_result = media_room_page.compare(after_image, before_image)
            case.result = not compare_result


        with uuid("055cb674-cd36-4ef4-b500-d424d6bca523") as case:
            # Insert Clip to check "Split" case..
            # Restart PDR
            main_page.close_and_restart_app()

            # Snapshot Sample Video clip icon from Library
            before_image = main_page.snapshot_library_insert_icon('Skateboard 01.mp4', file_name=Auto_Ground_Truth_Folder + 'H17_Split_Mark_Before.png')

            # Select Sample Video clip and Insert to timeline
            main_page.select_library_icon_view_media("Skateboard 01.mp4")
            tips_area_page.click_TipsArea_btn_insert()

            # Seek and Split Video clip
            playback_window_page.set_timecode_slidebar('00_00_03_00')
            tips_area_page.click_TipsArea_btn_split()
            time.sleep(3)

            time.sleep(1)
            # Snapshot Inserted Split Video clip icon from Library
            after_image = main_page.snapshot_library_insert_icon('Skateboard 01.mp4', file_name=Auto_Ground_Truth_Folder + 'H17_Split_Mark_After.png')
            logger (after_image)

            # Verify Mark Clip is correct or NOT
            compare_result = media_room_page.compare(after_image, before_image)
            case.result = not compare_result


        with uuid("ad8e79d5-ac7c-483b-a93d-a597e3affc97") as case:
            # Insert Clip to check "Keyframe" case..
            # Restart PDR
            main_page.close_and_restart_app()

            time.sleep(1)
            # Snapshot Sample Video clip icon from Library
            before_image = main_page.snapshot_library_insert_icon('Skateboard 01.mp4', file_name=Auto_Ground_Truth_Folder + 'H19_Keyframe_Mark_Before.png')

            # Select Sample Video clip and Insert to timeline
            main_page.select_library_icon_view_media("Skateboard 01.mp4")
            tips_area_page.click_TipsArea_btn_insert()

            # Keyframe > Color Adjustment
            # Contrast > Slider
            # Set Contrast of the current keyframe by slider
            # Close Keyframe
            main_page.tips_area_click_key_frame()
            keyframe_room_page.fix_enhance.color_adjustment.contrast.show()
            keyframe_room_page.fix_enhance.color_adjustment.contrast.set_slider(43)
            keyframe_room_page.click_close()

            time.sleep(1)
            # Snapshot Inserted Keyframe Clip icon from Library
            after_image = main_page.snapshot_library_insert_icon('Skateboard 01.mp4', file_name=Auto_Ground_Truth_Folder + 'H19_Keyframe_Mark_After.png')

            # Verify Mark Clip is correct or NOT
            compare_result = media_room_page.compare(after_image, before_image)
            case.result = not compare_result


        with uuid("98cc9d15-59fb-4ad3-8471-685f65b893cc") as case:
            # Insert Clip to check "Cut" case..
            # Restart PDR
            main_page.close_and_restart_app()

            time.sleep(1)
            # Snapshot Sample Video clip icon from Library
            before_image = main_page.snapshot_library_insert_icon('Skateboard 01.mp4', file_name=Auto_Ground_Truth_Folder + 'H21_Cut_Mark_Before.png')

            # Select Sample Video clip
            # Insert Sample Video clip to timeline
            main_page.select_library_icon_view_media("Skateboard 01.mp4")
            tips_area_page.click_TipsArea_btn_insert()

            # Cut Sample Video clip
            main_page.tap_Cut_hotkey()

            time.sleep(1)
            # Snapshot Cut Clip icon from Library
            after_image = main_page.snapshot_library_insert_icon('Skateboard 01.mp4', file_name=Auto_Ground_Truth_Folder + 'H21_Cut_Mark_After.png')

            # Verify Mark Clip is correct or NOT
            compare_result = media_room_page.compare(after_image, before_image)
            case.result = compare_result
                

        with uuid("52ba5aaa-9f8d-492a-b364-df6badee3967") as case:
            # Insert Clip to check "Remove" case..
            # Restart PDR
            main_page.close_and_restart_app()

            time.sleep(1)
            # Snapshot Sample Video clip icon from Library
            before_image = main_page.snapshot_library_insert_icon('Skateboard 01.mp4',
                                                                  file_name=Auto_Ground_Truth_Folder + 'H22_Remove_Mark_Before.png')
    
            # Select Sample Video clip
            # Insert Sample Video clip to timeline
            main_page.select_library_icon_view_media("Skateboard 01.mp4")
            tips_area_page.click_TipsArea_btn_insert()
    
            # Remove Sample Video clip
            main_page.tap_Remove_hotkey()

            time.sleep(1)
            # Snapshot Removed clip icon from Library
            after_image = main_page.snapshot_library_insert_icon('Skateboard 01.mp4',
                                                                 file_name=Auto_Ground_Truth_Folder + 'H22_Remove_Mark_After.png')

            # Verify Mark Clip is correct or NOT
            compare_result = media_room_page.compare(after_image, before_image)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        with uuid("0fd6205e-72a1-4556-9c7b-10d5a8111123") as case:
            # Insert Clip to check "Overwrite" case..

            # Snapshot Sample Clip1 & Clip2 icon from Library
            before_image1 = main_page.snapshot_library_insert_icon('Skateboard 01.mp4',
                                                                  file_name=Auto_Ground_Truth_Folder + 'H23_Overwrite1_Mark_Before.png')
            before_image2 = main_page.snapshot_library_insert_icon('Skateboard 02.mp4',
                                                                  file_name=Auto_Ground_Truth_Folder + 'H23_Overwrite2_Mark_Before.png')

            # Select Sample clip 1
            # Insert Clip 1 to timeline
            main_page.select_library_icon_view_media("Skateboard 01.mp4")
            tips_area_page.click_TipsArea_btn_insert()

            # Select Sample clip 2
            # Insert Clip 2 to timeline
            main_page.select_library_icon_view_media("Skateboard 02.mp4")
            tips_area_page.click_TipsArea_btn_insert(option=0)

            time.sleep(1)
            # Insert Sample clip 2 to timeline > "Overwrite"
            after_image1 = main_page.snapshot_library_insert_icon('Skateboard 01.mp4',
                                                                 file_name=Auto_Ground_Truth_Folder + 'H23_Overwrite1_Mark_After.png')
            after_image2 = main_page.snapshot_library_insert_icon('Skateboard 02.mp4',
                                                                 file_name=Auto_Ground_Truth_Folder + 'H23_Overwrite2_Mark_After.png')

            # Verify Mark Clip1 and Clip2 correct or NOT
            compare_result1 = media_room_page.compare(after_image1, before_image1)
            compare_result2 = media_room_page.compare(after_image2, before_image2)
            case.result = compare_result1 and not compare_result2


        with uuid("465b47cf-2fb6-4900-98eb-e46b6784a9f2") as case:
            # Insert Clip to check "Trim to Fit" case..
            # Restart PDR
            main_page.close_and_restart_app()

            time.sleep(1)
            # Snapshot Sample Clip1 & Clip2 icon from Library
            before_image1 = main_page.snapshot_library_insert_icon('Skateboard 01.mp4', file_name=Auto_Ground_Truth_Folder + 'H24_TrimToFit1_Mark_Before.png')
            before_image2 = main_page.snapshot_library_insert_icon('Skateboard 02.mp4', file_name=Auto_Ground_Truth_Folder + 'H24_TrimToFit2_Mark_Before.png')

            # Insert Sample Clip 1 to timeline
            # Drag to Move Clip 1
            main_page.insert_media('Skateboard 01.mp4')
            timeline_operation_page.drag_single_media_move_to(0, 0, 20)

            # Click Empty Area of Track 1
            # Seek Video clip
            main_page.timeline_select_track(track_no=1)
            playback_window_page.set_timecode_slidebar('00_00_00_00')

            # Select Sample Clip 2 > Insert on Selected Track via Context Menu
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            media_room_page.right_click()
            media_room_page.keyboard.down()
            media_room_page.keyboard.enter()

            # Select "Trim to Fit"
            media_room_page.keyboard.down()
            media_room_page.keyboard.down()
            media_room_page.keyboard.enter()

            time.sleep(1)
            # Snapshot Trim to Fit Clip icon from Library
            after_image1 = main_page.snapshot_library_insert_icon('Skateboard 01.mp4', file_name=Auto_Ground_Truth_Folder + 'H24_TrimToFit1_Mark_After.png')
            after_image2 = main_page.snapshot_library_insert_icon('Skateboard 02.mp4', file_name=Auto_Ground_Truth_Folder + 'H24_TrimToFit2_Mark_After.png')

            # Verify Mark Clip1 and Clip2 correct or NOT
            compare_result1 = media_room_page.compare(after_image1, before_image1)
            compare_result2 = media_room_page.compare(after_image2, before_image2)
            case.result = not compare_result1 and not compare_result2


        with uuid("306adbed-c34c-47ce-8c5e-d9ca2c93fb05") as case:
            # Insert Clip to check "Insert" case..
            # Restart PDR
            main_page.close_and_restart_app()

            time.sleep(1)
            # Snapshot Sample Clip 1 icon from Library
            # Snapshot Sample Clip 2 icon from Library
            before_image1 = main_page.snapshot_library_insert_icon('Skateboard 01.mp4', file_name=Auto_Ground_Truth_Folder + 'H25_Insert1_Mark_Before.png')
            before_image2 = main_page.snapshot_library_insert_icon('Skateboard 02.mp4', file_name=Auto_Ground_Truth_Folder + 'H25_Insert2_Mark_Before.png')

            # Insert Sample Clip 1 to timeline
            main_page.insert_media('Skateboard 01.mp4')

            # Insert Sample Clip 2 to timeline > "Insert"
            main_page.select_library_icon_view_media("Skateboard 02.mp4")
            main_page.tips_area_insert_media_to_selected_track(option=1)

            time.sleep(1)
            # Snapshot Inserted Clip1 icon from Library
            # Snapshot Inserted Clip2 icon from Library
            after_image1 = main_page.snapshot_library_insert_icon('Skateboard 01.mp4', file_name=Auto_Ground_Truth_Folder + 'H25_Insert1_Mark_After.png')
            after_image2 = main_page.snapshot_library_insert_icon('Skateboard 02.mp4', file_name=Auto_Ground_Truth_Folder + 'H25_Insert2_Mark_After.png')

            # Verify Mark Clip1 and Clip2 correct or NOT
            compare_result1 = media_room_page.compare(after_image1, before_image1)
            compare_result2 = media_room_page.compare(after_image2, before_image2)
            case.result = not compare_result1 and not compare_result2


        with uuid("fbb2e62f-7e8f-47cd-a45a-3520862df93c") as case:
            # Insert Clip to check "Insert and Move All Clips" case..
            # Restart PDR
            main_page.close_and_restart_app()

            time.sleep(1)
            # Snapshot Sample Clip 1 icon from Library
            # Snapshot Sample Clip 2 icon from Library
            before_image1 = main_page.snapshot_library_insert_icon('Skateboard 01.mp4', file_name=Auto_Ground_Truth_Folder + 'H26_InsertAndMoveAllClips1_Mark_Before.png')
            before_image2 = main_page.snapshot_library_insert_icon('Skateboard 02.mp4', file_name=Auto_Ground_Truth_Folder + 'H26_InsertAndMoveAllClips2_Mark_Before.png')

            # Insert Sample Clip 1 to timeline
            main_page.insert_media('Skateboard 01.mp4')

            # Insert Sample Clip 2 to timeline > "Insert and Move All Clips"
            main_page.select_library_icon_view_media("Skateboard 02.mp4")
            main_page.tips_area_insert_media_to_selected_track(option=2)

            time.sleep(1)
            # Snapshot Inserted Clip1 icon from Library
            # Snapshot Inserted Clip2 icon from Library
            after_image1 = main_page.snapshot_library_insert_icon('Skateboard 01.mp4', file_name=Auto_Ground_Truth_Folder + 'H26_InsertAndMoveAllClips1_Mark_After.png')
            after_image2 = main_page.snapshot_library_insert_icon('Skateboard 02.mp4', file_name=Auto_Ground_Truth_Folder + 'H26_InsertAndMoveAllClips2_Mark_After.png')

            # Verify Mark Clip1 and Clip2 correct or NOT
            compare_result1 = media_room_page.compare(after_image1, before_image1)
            compare_result2 = media_room_page.compare(after_image2, before_image2)
            case.result = not compare_result1 and not compare_result2



        with uuid("b0677ccf-b831-4f6b-a567-6005ca5662b5") as case:
            # Insert Clip to check "Crossfade" case..
            # Restart PDR
            main_page.close_and_restart_app()

            time.sleep(1)
            # Snapshot Sample clip 1 icon from Library
            # Snapshot Sample clip 2 icon from Library
            before_image1 = main_page.snapshot_library_insert_icon('Skateboard 01.mp4', file_name=Auto_Ground_Truth_Folder + 'H27_Crossfade1_Mark_Before.png')
            before_image2 = main_page.snapshot_library_insert_icon('Skateboard 02.mp4', file_name=Auto_Ground_Truth_Folder + 'H27_Crossfade2_Mark_Before.png')

            # Insert Sample clip 1 to timeline
            main_page.insert_media('Skateboard 01.mp4')

            # Insert Sample clip 2 to timeline > "Crossfade"
            main_page.select_library_icon_view_media("Skateboard 02.mp4")
            main_page.tips_area_insert_media_to_selected_track(option=3)

            time.sleep(1)
            # Snapshot Inserted Clip1 icon from Library
            # Snapshot Inserted Clip2 icon from Library
            after_image1 = main_page.snapshot_library_insert_icon('Skateboard 01.mp4', file_name=Auto_Ground_Truth_Folder + 'H27_Crossfade1_Mark_After.png')
            after_image2 = main_page.snapshot_library_insert_icon('Skateboard 02.mp4', file_name=Auto_Ground_Truth_Folder + 'H27_Crossfade2_Mark_After.png')

            # Verify Mark Clip1 and Clip2 correct or NOT
            compare_result1 = media_room_page.compare(after_image1, before_image1)
            compare_result2 = media_room_page.compare(after_image2, before_image2)
            case.result = not compare_result1 and not compare_result2

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        with uuid("8b7fcefb-bc19-41d1-b2cd-bd445ce42da9") as case:
            # Insert Clip to check "Copy Track Content to" case..

            # Snapshot Sample clip icon from Library
            before_image = main_page.snapshot_library_insert_icon('Skateboard 02.mp4', file_name=Auto_Ground_Truth_Folder + 'H28_CopyTrackContentTo_Mark_Before.png')

            # Insert Sample clip to timeline
            # Copy Track Content to another track
            main_page.insert_media('Skateboard 02.mp4')
            timeline_operation_page.right_click_menu_CopyTrackContent_to(1, 'Above track 2', 'OK')

            time.sleep(1)
            # Snapshot Inserted Sample Clip icon from Library
            after_image = main_page.snapshot_library_insert_icon('Skateboard 02.mp4', file_name=Auto_Ground_Truth_Folder + 'H28_CopyTrackContentTo.png')
            logger(after_image)

            # Verify Mark Clip1 and Clip2 correct or NOT
            compare_result = media_room_page.compare(after_image, before_image)
            case.result = not compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        with uuid("3b2a4c1c-56a1-4342-91db-db986fb29180") as case:
            # Insert "New Project" case...

            # Snapshot Photo clip icon from Library
            before_image = main_page.snapshot_library_insert_icon('Landscape 02.jpg', file_name=Auto_Ground_Truth_Folder + 'H7_NewProject_Before.png')

            # Insert Photo clip to timeline
            main_page.insert_media('Landscape 02.jpg')

            # New Project
            # Esc to exit w/o Saving
            main_page.tap_CreateNewProject_hotkey()
            time.sleep(1)
            main_page.press_esc_key()
            time.sleep(1)

            # Snapshot Inserted Photo Clip icon from Library
            after_image = main_page.snapshot_library_insert_icon('Landscape 02.jpg', file_name=Auto_Ground_Truth_Folder + 'H7_NewWorkspace_After.png')
            logger(after_image)

            # Verify Mark Clip is correct or NOT
            compare_result = media_room_page.compare(after_image, before_image)
            case.result = compare_result


        with uuid("ceb77244-44e5-4742-877f-889d8a9ac216") as case:
            # Insert "New Workspace" case...

            # Snapshot Photo clip icon from Library
            before_image = main_page.snapshot_library_insert_icon('Landscape 02.jpg', file_name=Auto_Ground_Truth_Folder + 'H8_NewWorkspace_Before.png')

            # Insert Photo clip to timeline
            main_page.insert_media('Landscape 02.jpg')

            # New Workspace
            # Esc to exit w/o Saving
            main_page.tap_NewWorkspace_hotkey()
            time.sleep(1)
            main_page.press_esc_key()
            time.sleep(1)

            # Snapshot Inserted Photo Clip icon from Library
            after_image = main_page.snapshot_library_insert_icon('Landscape 02.jpg', file_name=Auto_Ground_Truth_Folder + 'H8_NewWorkspace_After.png')
            logger(after_image)

            # Verify Mark Clip is correct or NOT
            compare_result = media_room_page.compare(after_image, before_image)
            case.result = compare_result


        with uuid("9bc58a46-a7d7-468b-a34e-5e62a2562fd2") as case:
            # Insert "Open + Save Project" case...

            time.sleep(2)
            main_page.close_and_restart_app()
            time.sleep(2)

            # Open project
            main_page.top_menu_bar_file_open_project()
            project_path = Test_Material_Folder + 'Mark_Clips/Mark.pds'
            main_page.handle_open_project_dialog(project_path)
            time.sleep(3)
            # "No" for Merge Dialog
            a = main_page.handle_merge_media_to_current_library_dialog(option='no')
            logger(a)
            time.sleep(3)

            # Snapshot Sample clip icon from Library
            before_image = main_page.snapshot_library_insert_icon('Landscape 02.jpg', file_name=Auto_Ground_Truth_Folder + 'H9_OpenProject_After.png')

            # Save Project
            main_page.tap_SaveProject_hotkey()
            time.sleep(2)

            # Snapshot Sample clip icon from Library
            after_image = main_page.snapshot_library_insert_icon('Landscape 02.jpg', file_name=Auto_Ground_Truth_Folder + 'H9_SaveProject_After.png')


            # Verify Mark Clip is correct or NOT
            compare_result = media_room_page.compare(after_image, before_image)
            case.result = compare_result
