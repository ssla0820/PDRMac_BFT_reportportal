import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time, inspect, datetime, pytest, re, configparser
os.chdir(os.path.dirname(__file__))
from types import SimpleNamespace

from ATFramework.pages.base_page import BasePage
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
mwc = DriverFactory().get_mac_driver_object('mac', app.app_name, app.app_bundleID, app.app_path)
main_page = PageFactory().get_page_object('main_page', mwc)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mwc)
playback_window_page = PageFactory().get_page_object('playback_window_page', mwc)
media_room_page = PageFactory().get_page_object('media_room_page', mwc)
effect_room_page = PageFactory().get_page_object('effect_room_page', mwc)
pip_room_page = PageFactory().get_page_object('pip_room_page', mwc)
particle_room_page = PageFactory().get_page_object('particle_room_page', mwc)
title_room_page = PageFactory().get_page_object('title_room_page', mwc)
transition_room_page = PageFactory().get_page_object('transition_room_page', mwc)
video_speed_page = PageFactory().get_page_object('video_speed_page', mwc)
#blending_mode_page = PageFactory().get_page_object('blending_mode_page',mwc)
tips_area_page = PageFactory().get_page_object('tips_area_page',mwc)
produce_page = PageFactory().get_page_object('produce_page',mwc)
video_collage_designer_page = PageFactory().get_page_object('video_collage_designer_page',mwc)
trim_page = PageFactory().get_page_object('trim_page',mwc)
fix_enhance_page = PageFactory().get_page_object('fix_enhance_page',mwc)
crop_zoom_pan_page = PageFactory().get_page_object('crop_zoom_pan_page',mwc)
library_preview_page = PageFactory().get_page_object('library_preview_page',mwc)
title_designer_page = PageFactory().get_page_object('title_designer_page',mwc)
pip_designer_page = PageFactory().get_page_object('pip_designer_page',mwc)
mask_designer_page = PageFactory().get_page_object('mask_designer_page',mwc)
blending_mode_page = PageFactory().get_page_object('blending_mode_page',mwc)
project_new_page = PageFactory().get_page_object('project_new_page', mwc)
nest_project_page = PageFactory().get_page_object('nest_project_page', mwc)
project_room_page = PageFactory().get_page_object('project_room_page', mwc)
download_from_cl_dz_page = PageFactory().get_page_object('download_from_cl_dz_page', mwc)
upload_cloud_dz_page = PageFactory().get_page_object('upload_cloud_dz_page', mwc)
preferences_page = PageFactory().get_page_object('preferences_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="GIF Import.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/GIF_Import/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/GIF_Import/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_GIF_Import():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        time.sleep(DELAY_TIME * 3)
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
            google_sheet_execution_log_init('Test_GIF_Import')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"GIF Import result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           report.get_ovinfo('skip'),
                           report.get_ovinfo('duration'))
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                               report.get_ovinfo('skip'), report.get_ovinfo('duration'))
        report.show()

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
    def test_1_1_1(self):
        #1/23
        with uuid('4bdd34a7-d224-4f36-85fd-f4dac51865bc') as case:
            # session 1 : Entry
            # case1.1 : Media Room > Media Preview
            # Import animated png (GIF) into media room
            time.sleep(DELAY_TIME * 5)
            main_page.set_project_aspect_ratio_1_1()
            import_media = media_room_page.import_media_file(
                Test_Material_Folder + 'GIF_Import/loop.gif')
            logger(import_media)
            time.sleep(DELAY_TIME * 5)
            main_page.select_library_icon_view_media('loop.gif')
            #main_page.insert_media('PNG_noBG_009.png')

            # snapshot preview window
            time.sleep(DELAY_TIME * 2)
            preview_window = tips_area_page.snapshot(locator=L.playback_window.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'G1.1.1_Preview_Window_1st_frame.png')
            logger(preview_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.1.1_Preview_Window_1st_frame.png', preview_window)
            logger(compare_result)

            #seek animated GIF via preview window
            time.sleep(DELAY_TIME)
            set_timecode = main_page.set_timeline_timecode('00_00_02_02')
            logger(set_timecode)

            # snapshot preview window
            time.sleep(DELAY_TIME * 2)
            preview_window = tips_area_page.snapshot(locator=L.playback_window.main,
                                                           file_name=Auto_Ground_Truth_Folder + 'G1.1.1_Preview_Window_after_seek.png')
            logger(preview_window)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.1.1_Preview_Window_1st_frame.png', preview_window)
            logger(compare_result1)

            if compare_result1 == False:
                result = True
                logger(result)
            else:
                result = False
                logger(result)

            case.result = compare_result and result

        # 1/23
        with uuid('22aa5159-cb06-4867-8f1f-511c34a3d20c') as case:
            # session 1 : Entry
            # case1.1.2 : Timeline > Timeline Preview
            # Add animated png (GIF) into Timeline and check preview window
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media('loop.gif')
            main_page.insert_media('loop.gif')
            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('loop.gif')

            # seek animated GIF via preview window
            time.sleep(DELAY_TIME)
            set_timecode = main_page.set_timeline_timecode('00_00_02_02')
            logger(set_timecode)

            # snapshot preview window
            time.sleep(DELAY_TIME * 2)
            preview_window = tips_area_page.snapshot(locator=L.playback_window.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'G1.1.2_Timeline_Preview_Window_after_seek.png')
            logger(preview_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.1.2_Timeline_Preview_Window_after_seek.png', preview_window)
            logger(compare_result)

            case.result = compare_result

        # 1/23
        with uuid('483f4430-08d6-4d67-b7fd-e3a6d6059b97') as case:
            # session 1 : Entry
            # case1.1.3.1 : Video Collage > Media Library > Display
            # Select timeline clip and enter video collage
            select_track = main_page.timeline_select_track(1)
            logger(select_track)
            time.sleep(DELAY_TIME)

            # select video on timeline
            main_page.select_timeline_media('loop.gif')
            time.sleep(DELAY_TIME*2)

            # enter video collage
            main_page.top_menu_bar_plugins_video_collage_designer()
            time.sleep(DELAY_TIME*5)

            # import gif
            video_collage_designer_page.media.import_media(Test_Material_Folder + 'GIF_Import/' + 'a_mountains.gif')
            time.sleep(DELAY_TIME*2)
            check_result_1 = video_collage_designer_page.media.is_exist_media('a_mountains.gif')
            logger(check_result_1)

            #snapshot
            current_preview = video_collage_designer_page.snapshot(
                locator=L.video_collage_designer.media_library, file_name=Auto_Ground_Truth_Folder + 'G1.1.3.1_VideoCollage_Imported_GIF.png')
            logger(current_preview)

            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.1.3.1_VideoCollage_Imported_GIF.png', current_preview)
            logger(compare_result)

            case.result = check_result_1 and compare_result
            time.sleep(DELAY_TIME)

        # 1/23
        with uuid('93e3429a-1580-4bf5-8fcb-49c953051586') as case:
            # session 1 : Entry
            # case1.1.3.2 : Video Collage > Media Library > Preview
            # Preview animated GIF photo correctly
            # select gif
            video_collage_designer_page.media.select_media('loop.gif')
            time.sleep(DELAY_TIME * 1.5)

            # auto fill the empty slots from media room
            video_collage_designer_page.media.click_auto_fill()
            time.sleep(DELAY_TIME)

            # input number then seek to correct position
            video_collage_designer_page.set_timecode('00_00_03_00')
            check_duration = video_collage_designer_page.exist(L.video_collage_designer.time_code).AXValue
            result = False if not check_duration == '00;00;03;00' else True
            logger(result)

            # snapshot
            time.sleep(DELAY_TIME * 2)
            VC_Preview_window = tips_area_page.snapshot(locator=L.video_collage_designer.main_window,
                                                           file_name=Auto_Ground_Truth_Folder + 'G1.1.3.2_VideoCollage_Preview_Window.png')
            logger(VC_Preview_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.1.3.2_VideoCollage_Preview_Window.png', VC_Preview_window)
            logger(compare_result)

            case.result = compare_result and result

        # 1/23
        with uuid('93f7d616-bbc0-4c38-99ce-d2eca18c5fcb') as case: #crash occurs after setting "*.raf" as interclip texture
            # session 1 : Entry
            # case1.1.3.4 : Video Collage > Media Library > Interclip Texture
            # Check if animated GIF photo can be set as 'interclip texture'
            # image file is selected and displays correctly
            time.sleep(DELAY_TIME * 2)
            video_collage_designer_page.click_preview_operation('Stop')
            time.sleep(DELAY_TIME * 2)
            video_collage_designer_page.border.set_fill_type(1)
            #import_animatedGIF_result = video_collage_designer_page.border.select_interclip_texture(Test_Material_Folder + 'GIF_Import/' + 'tenor.gif') # gif is filtered out in this case
            #logger(import_animatedGIF_result)

            import_animatedPNG_result = video_collage_designer_page.border.select_interclip_texture(
                Test_Material_Folder + 'GIF_Import/' + 'PNG_noBG_001.png')
            logger(import_animatedPNG_result)

            # snapshot
            time.sleep(DELAY_TIME * 2)
            VC_Preview_window = tips_area_page.snapshot(locator=L.video_collage_designer.main_window,
                                                        file_name=Auto_Ground_Truth_Folder + 'G1.1.3.4_VideoCollage_Preview_Window_Interclip_Texture.png')
            logger(VC_Preview_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.1.3.4_VideoCollage_Preview_Window_Interclip_Texture.png', VC_Preview_window)
            logger(compare_result)

            case.result = compare_result and import_animatedPNG_result #and not import_animatedGIF_result

        # 1/23
        with uuid('1b704b97-3508-41eb-8c9e-e0c9c9808230') as case:
            # session 1 : Entry
            # case1.1.3.3 : Video Collage > Media Library > Apply
            # Apply Video Collage with animated GIF photo correctly
            # save the setting and show effect on timeline
            time.sleep(DELAY_TIME * 2)
            check_result_1 = video_collage_designer_page.click_ok()
            time.sleep(DELAY_TIME * 3)
            logger(check_result_1)

            # seek animated GIF via preview window
            time.sleep(DELAY_TIME)
            set_timecode = main_page.set_timeline_timecode('00_00_03_02')
            logger(set_timecode)

            # snapshot for preview window
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G1.1.3.3_Apply_VC_with_animatedGIF.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.1.3.3_Apply_VC_with_animatedGIF.png', preview_wnd)
            logger(compare_result)

            case.result = compare_result

        # 1/23
        with uuid('727dc43b-cf2e-4e36-b78a-6cb13fecb0e2') as case:
            # session 1 : Entry
            # case1.1.1.2 : Media Room > Library Preview
            # select gif in media library
            main_page.select_library_icon_view_media('loop.gif')
            time.sleep(DELAY_TIME * 2)

            # enable Library Preview window
            main_page.top_menu_bar_view_show_library_preview_window()
            time.sleep(DELAY_TIME * 2)
            current_result = library_preview_page.library_preview_window_exist()
            logger(current_result)

            # seek video in library preview window
            library_preview_page.set_library_preview_window_timecode('00_00_03_00')
            time.sleep(DELAY_TIME * 2)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.library_preview.display_panel,
                                                  file_name=Auto_Ground_Truth_Folder + 'G1.1.1.2_library_preview.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.1.1.2_library_preview.png', preview_wnd, similarity=0.85)
            logger(compare_result)

            case.result = current_result and compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        #1/23
        with uuid('249942e9-ddac-4ff9-965d-58501c791968') as case:
            # session 1 : Entry
            # case1.1.4.1 : Title Designer > Insert Image
            # Insert Image with animated png (GIF)
            time.sleep(DELAY_TIME * 5)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME * 2)
            main_page.select_LibraryRoom_category('General')
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media('Clover_01')
            time.sleep(DELAY_TIME * 1)
            current_result = title_room_page.select_RightClickMenu_ModifyTemplate()
            logger(current_result)
            time.sleep(DELAY_TIME * 3)

            # switch to advanced mode
            switch_mode = title_designer_page.switch_mode(2)
            logger(switch_mode)

            # insert image with animated GIF
            # open import image dialog to insert gif
            title_designer_page.click_insert_image_btn()
            time.sleep(DELAY_TIME * 2)
            current_result1 = title_designer_page.insert_image(Test_Material_Folder + 'GIF_Import/' + 'tenor.gif')
            logger(current_result1)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.title_designer.main_window,
                                                  file_name=Auto_Ground_Truth_Folder + 'G1.1.4.1_title_designer_warning.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.1.4.1_title_designer_warning.png', preview_wnd)
            logger(compare_result)
            time.sleep(DELAY_TIME*2)
            main_page.press_enter_key() # close warning
            time.sleep(DELAY_TIME*1)

            case.result = current_result and current_result1 and compare_result

        #1/23
        with uuid('1d1ff7b8-eebc-4005-88e3-936944db1139') as case:
            # session 1 : Entry
            # case1.1.4.2 : Title Designer > Insert Background > Stretch
            # Insert background with animated png (GIF)
            # open import image dialog to insert gif as background
            title_designer_page.click_insert_background_btn()
            time.sleep(DELAY_TIME * 2)
            current_result1 = title_designer_page.insert_background(Test_Material_Folder + 'GIF_Import/' + 'tenor.gif')
            logger(current_result1)

            check_result = title_designer_page.insert_background_adjust_setting(index=0)  # stretch
            logger(check_result)
            time.sleep(DELAY_TIME*3)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.title_designer.area.frame_video_preview,
                                                  file_name=Auto_Ground_Truth_Folder + 'G1.1.4.2_title_designer_Insert_BG_Stretch.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.1.4.2_title_designer_Insert_BG_Stretch.png', preview_wnd)
            logger(compare_result)

            case.result = current_result1 and check_result and compare_result

        #1/23
        with uuid('54e3140b-6ca0-4a7e-856f-255f1dc57eac') as case:
            # session 1 : Entry
            # case1.1.4.3 : Title Designer > Insert Background > Letterbox
            # Insert background with animated png (GIF)
            # open import image dialog to insert gif as background
            title_designer_page.click_insert_background_btn()
            time.sleep(DELAY_TIME * 2)
            current_result1 = title_designer_page.insert_background(Test_Material_Folder + 'GIF_Import/' + 'tenor.gif')
            logger(current_result1)

            check_result = title_designer_page.insert_background_adjust_setting(index=1)  # letterbox
            logger(check_result)
            time.sleep(DELAY_TIME*3)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.title_designer.area.frame_video_preview,
                                                  file_name=Auto_Ground_Truth_Folder + 'G1.1.4.3_title_designer_Insert_BG_letterbox.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.1.4.3_title_designer_Insert_BG_letterbox.png', preview_wnd)
            logger(compare_result)

            case.result = current_result1 and check_result and compare_result

        #1/23
        with uuid('135203e3-0c7b-43b1-927e-8128540a0450') as case:
            # session 1 : Entry
            # case1.1.4.4 : Title Designer > Insert Background > Crop
            # Insert background with animated png (GIF)
            # open import image dialog to insert gif as background
            title_designer_page.click_insert_background_btn()
            time.sleep(DELAY_TIME * 2)
            current_result1 = title_designer_page.insert_background(Test_Material_Folder + 'GIF_Import/' + 'tenor.gif')
            logger(current_result1)

            check_result = title_designer_page.insert_background_adjust_setting(index=2)  # crop
            logger(check_result)
            time.sleep(DELAY_TIME*3)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.title_designer.area.frame_video_preview,
                                                  file_name=Auto_Ground_Truth_Folder + 'G1.1.4.4_title_designer_Insert_BG_crop.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.1.4.4_title_designer_Insert_BG_crop.png', preview_wnd)
            logger(compare_result)

            # click [cancel] to close title designer
            title_designer_page.click_cancel(option=1)
            time.sleep(DELAY_TIME*3)

            case.result = current_result1 and check_result and compare_result

        #1/23
        with uuid('9c6568c8-cfbf-4b58-b62c-5cb97676b963') as case:
            # session 1 : Entry
            # case1.1.5 : PiP Designer > Create new template with GIF
            # Enter PiP room to create new template with GIF
            #main_page.select_library_icon_view_media('Food.jpg')
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 4)
            pip_room_page.click_CreateNewPiP_btn(Test_Material_Folder + 'GIF_Import/' + 'tenor.gif')

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.base.quit_dialog.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G1.1.5_pip_designer_warning.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.1.5_pip_designer_warning.png', preview_wnd)
            logger(compare_result)
            time.sleep(DELAY_TIME * 2)
            main_page.press_enter_key()  # close warning
            time.sleep(DELAY_TIME * 1)

            case.result = compare_result

        #1/23
        with uuid('bd1c468d-26e0-48eb-bace-704d0331ce6b') as case:
            # session 1 : Entry
            # case1.1.6.1 : Mask Designer > Create new template with GIF (Alpha Channel)
            # Create a custom mask with GIF
            # Insert Food.jpg to timeline > Enter Mask Designer
            main_page.enter_room(0)
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media('Food.jpg')
            main_page.insert_media("Food.jpg")
            time.sleep(DELAY_TIME * 2)
            main_page.tap_TipsArea_Tools_menu(1)
            time.sleep(DELAY_TIME * 4)

            mask_designer_page.Edit_MaskDesigner_CreateImageMask(Test_Material_Folder + 'GIF_Import/' + 'purple.gif')
            time.sleep(DELAY_TIME * 2)

            current_result = mask_designer_page.set_MaskDesigner_timecode("00_00_02_00")
            logger(current_result)
            time.sleep(DELAY_TIME * 2)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.mask_designer.preview_window,
                                                  file_name=Auto_Ground_Truth_Folder + 'G1.1.6.1_mask_designer_custom_image_GIF_Alpha_Channel.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.1.6.1_mask_designer_custom_image_GIF_Alpha_Channel.png', preview_wnd)
            logger(compare_result)
            time.sleep(DELAY_TIME * 2)

            case.result = compare_result

        #1/23
        with uuid('07b82324-7926-4006-a9de-b8c9c3fbe696') as case:
            # session 1 : Entry
            # case1.1.6.2 : Mask Designer > Create new template with GIF (Grayscale)
            # Create a custom mask with GIF
            # Change custom mask
            mask_designer_page.Edit_MaskDesigner_CreateImageMask(Test_Material_Folder + 'GIF_Import/' + 'purple.gif')
            time.sleep(DELAY_TIME * 2)

            current_result = mask_designer_page.set_MaskDesigner_timecode("00_00_02_00")
            logger(current_result)
            time.sleep(DELAY_TIME * 2)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.mask_designer.preview_window,
                                                  file_name=Auto_Ground_Truth_Folder + 'G1.1.6.2_mask_designer_custom_image_GIF_GrayScale.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G1.1.6.2_mask_designer_custom_image_GIF_GrayScale.png', preview_wnd)
            logger(compare_result)
            time.sleep(DELAY_TIME * 2)

            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        #1/28
        with uuid('c5bde90e-2661-4ee1-90f9-e7c0d3637055') as case:
            # session 2 : GIF Edit
            # case2.1 : GIF Edit > Split
            time.sleep(DELAY_TIME * 5)
            main_page.set_project_aspect_ratio_1_1()
            import_media = media_room_page.import_media_file(
                Test_Material_Folder + 'GIF_Import/loop.gif')
            logger(import_media)

            # insert .gif to timeline
            time.sleep(DELAY_TIME * 5)
            main_page.select_library_icon_view_media('loop.gif')
            main_page.insert_media('loop.gif')
            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('loop.gif')

            # seek animated GIF via preview window
            time.sleep(DELAY_TIME)
            set_timecode = main_page.set_timeline_timecode('00_00_02_02')
            logger(set_timecode)

            # split *.gif
            split_func = tips_area_page.tips_area_click_split()
            logger(split_func)

            after_split = tips_area_page.get_btn_split_status()
            logger(after_split)

            if after_split:
                case.result = False
            else:
                case.result = True


        #1/28
        with uuid('3440ac65-6c23-456c-ae60-feca58d1cc28') as case:
            # session 2 : GIF Edit
            # case2.1.3 : GIF Edit > PiP Designer
            # undo changes
            #main_page.click_undo()

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('loop.gif')

            # Enter PiP Designer
            timeline_operation_page.double_click()
            enter_pip_designer = pip_room_page.check_in_PiP_designer()
            logger(enter_pip_designer)

            # switch to "Advanced" mode
            pip_designer_page.switch_mode('Advanced')
            pip_designer_page.exist_click(L.pip_designer.object_setting.object_setting)

            # unfold object setting
            pip_designer_page.express_mode.unfold_properties_object_setting_tab()

            # adjust position & height
            pip_designer_page.input_x_position_value('0.500')
            time.sleep(DELAY_TIME * 1)
            pip_designer_page.input_y_position_value('0.600')
            time.sleep(DELAY_TIME * 1)
            pip_designer_page.drag_scale_height_slider(value=0.5)
            time.sleep(DELAY_TIME * 1)

            '''
            # Apply border & shadow
            pip_designer_page.apply_border(1)
            time.sleep(DELAY_TIME * 1)
            pip_designer_page.drag_border_size_slider('8')
            time.sleep(DELAY_TIME * 1)
            pip_designer_page.apply_shadow(1)
            '''

            # apply all changes
            pip_designer_page.click_ok()
            time.sleep(DELAY_TIME*3)

            # snapshot for preview window
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.3_Edit_Gif_By_PiP_Designer.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.3_Edit_Gif_By_PiP_Designer.png', preview_wnd, similarity=0.85)
            logger(compare_result)

            case.result = compare_result

        # 1/28
        with uuid('c2677988-467c-4509-9ce7-48e09715ff4c') as case:
            # session 2 : GIF Edit
            # case2.1.4 : GIF Edit > Mask Designer
            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('loop.gif')

            # Enter Mask Designer
            main_page.tap_TipsArea_Tools_menu(1)
            time.sleep(DELAY_TIME * 5)

            # Apply template (6th)
            mask_designer_page.MaskDesigner_Apply_template(5)

            # Adjust feather & object position
            adjust_feather = mask_designer_page.Edit_MaskDesigner_Feather_radius_Slider(6)
            logger(adjust_feather)
            move_scrollbar = mask_designer_page.drag_Mask_Settings_Scroll_Bar(0.5)
            logger(move_scrollbar)
            set_position = mask_designer_page.object_settings.set_position_x(-0.8)
            logger(set_position)

            # Apply all adjustments
            leave_MaskDesigner = mask_designer_page.Edit_MaskDesigner_ClickOK()
            logger(leave_MaskDesigner)
            time.sleep(DELAY_TIME*2)

            # snapshot for preview window
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.4_Edit_Gif_By_Mask_Designer.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.4_Edit_Gif_By_Mask_Designer.png', preview_wnd, similarity=0.85)
            logger(compare_result)

            case.result = compare_result

        # 1/28
        with uuid('ccff980a-0d70-439d-982e-7af985b6c91e') as case:
            # session 2 : GIF Edit
            # case2.1.5 : GIF Edit > Crop/Zoom/Pan
            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('loop.gif')

            # Enter crop/zoom/pan
            tips_area_page.tools.select_CropZoomPan()
            time.sleep(DELAY_TIME * 5)

            # set rotation to -220
            #rotation_degree = crop_zoom_pan_page.set_rotation('-220')
            #logger(rotation_degree)

            # snapshot for crop/zoom/pan window
            time.sleep(DELAY_TIME * 2)
            crop_zoom_pan_window = tips_area_page.snapshot(locator=L.crop_zoom_pan.window,
                                                            file_name=Auto_Ground_Truth_Folder + 'G2.1.5_crop_zoom_pan_rotation.png')
            logger(crop_zoom_pan_window)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.5_crop_zoom_pan_rotation.png', crop_zoom_pan_window)
            logger(compare_result)

            crop_zoom_pan_page.click_ok()
            time.sleep(DELAY_TIME * 5)

            case.result = compare_result

        # 1/28
        with uuid('0961d806-a14e-4bb0-9625-3f11bf6a28b5') as case:
            # session 2 : GIF Edit
            # case2.1.6 : GIF Edit > Video Speed
            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('loop.gif')

            # Enter Video Speed
            main_page.tap_TipsArea_Tools_menu('Video Speed')
            time.sleep(DELAY_TIME * 5)

            check_result = video_speed_page.Edit_VideoSpeedDesigner_EntireClip_SpeedMultiplier_SetValue(2.000)
            logger(check_result)
            time.sleep(DELAY_TIME * 5)

            video_speed_page.Edit_VideoSpeedDesigner_ClickOK()
            time.sleep(DELAY_TIME*3)

            # snapshot for preview window
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.6_Edit_Gif_By_Speed_Designer.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.6_Edit_Gif_By_Speed_Designer.png', preview_wnd, similarity=0.85)
            logger(compare_result)

            case.result = compare_result

        # 1/28
        with uuid('c02c316d-bef3-4951-8321-dff795d3aa55') as case:
            # session 2 : GIF Edit
            # case2.1.7 : GIF Edit > Video In Reverse
            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('loop.gif')
            time.sleep(DELAY_TIME)

            # Apply Video In Reverse
            tips_area_page.tools.select_Video_in_Reverse(skip=1)

            # seek animated GIF via preview window
            time.sleep(DELAY_TIME)
            set_timecode = main_page.set_timeline_timecode('00_00_00_15')
            logger(set_timecode)

            # snapshot for preview window
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.7_Edit_Gif_By_Video_In_Reverse.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.7_Edit_Gif_By_Video_In_Reverse.png', preview_wnd, similarity=0.85)
            logger(compare_result)

            case.result = compare_result



    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        #1/28
        with uuid('a7b44244-813c-424a-8210-971cda647e48') as case:
            # session 2 : GIF Edit
            # case2.1.8 : GIF Edit > Blending Mode
            time.sleep(DELAY_TIME * 5)
            main_page.set_project_aspect_ratio_1_1()
            main_page.select_library_icon_view_media('Food.jpg')
            main_page.insert_media('Food.jpg')
            time.sleep(DELAY_TIME*2)
            import_media = media_room_page.import_media_file(
                Test_Material_Folder + 'GIF_Import/loop.gif')
            logger(import_media)

            # Select track2
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # insert .gif to timeline
            time.sleep(DELAY_TIME * 5)
            main_page.select_library_icon_view_media('loop.gif')
            main_page.insert_media('loop.gif')

            # Select track2
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('loop.gif')

            # Enter Blending mode via tools
            blending_mode_diag = tips_area_page.tools.select_Blending_Mode()
            logger(blending_mode_diag)

            # set blending mode to "Overlay"
            blending_mode_1 = blending_mode_page.set_blending_mode('Overlay')
            logger(blending_mode_1)
            time.sleep(DELAY_TIME * 3)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.8_Edit_Gif_By_Blending_Mode.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.8_Edit_Gif_By_Blending_Mode.png',
                                                    preview_wnd, similarity=0.85)

            # click [OK] to apply and exit Blending mode dialogue
            blending_mode_page.click_ok()
            time.sleep(DELAY_TIME * 3)

            logger(compare_result)

            case.result = compare_result

        #1/28
        with uuid('32f6c712-cf4a-42c2-94a5-343c36077303') as case:
            # session 2 : GIF Edit
            # case2.1.9.2 : GIF Edit > Fix/Enhance > White Balance
            # Select track2
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('loop.gif')

            # enter fix/enhance
            tips_area_page.click_fix_enhance()
            time.sleep(DELAY_TIME*2)
            # Verify if in "Fix Enhance" page
            is_in_fix_enhance = fix_enhance_page.is_in_fix_enhance()
            logger(f"{is_in_fix_enhance= }")
            fix_enhance_page.fix.enable_white_balance()
            time.sleep(DELAY_TIME*2)
            fix_enhance_page.fix.white_balance.color_temperature.set_value(30)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.9.2_Edit_Gif_By_Fix_Enhnace_WB.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.9.2_Edit_Gif_By_Fix_Enhnace_WB.png',
                                                    preview_wnd, similarity=0.85)
            logger(f"{compare_result= }")

            case.result = compare_result

        #1/28
        with uuid('07b8134c-4ff9-4cd0-a3aa-d9fcc7bbdb89') as case:
            # session 2 : GIF Edit
            # case2.1.9.3 : GIF Edit > Fix/Enhance > Video Stabilizer
            # Select track2
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('loop.gif')

            # enter fix/enhance
            tips_area_page.click_fix_enhance()
            time.sleep(DELAY_TIME * 2)

            # Apply fix/enhance > Video Stabilizer
            fix_enhance_page.fix.enable_video_stabilizer()

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.9.3_Edit_Gif_By_Fix_Enhnace_Video_Stabilizer.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G2.1.9.3_Edit_Gif_By_Fix_Enhnace_Video_Stabilizer.png',
                                                    preview_wnd, similarity=0.85)
            logger(f"{compare_result= }")

            case.result = compare_result

        #1/28
        with uuid('bce74d53-1866-4e18-9ef8-9ff65a827b57') as case:
            # session 2 : GIF Edit
            # case2.1.9.4 : GIF Edit > Fix/Enhance > Lens Correction
            # Select track2
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('loop.gif')

            # enter fix/enhance
            tips_area_page.click_fix_enhance()
            time.sleep(DELAY_TIME * 2)

            # Apply fix/enhance > Lens Correction
            fix_enhance_page.fix.enable_lens_correction()
            time.sleep(DELAY_TIME*2)
            fix_enhance_page.fix.lens_correction.select_marker_type('GoPro')
            fix_enhance_page.fix.lens_correction.select_model_type(18)
            time.sleep(DELAY_TIME * 2)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.9.4_Edit_Gif_By_Fix_Enhnace_Lens_Correction.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.9.4_Edit_Gif_By_Fix_Enhnace_Lens_Correction.png',
                preview_wnd, similarity=0.85)
            logger(f"{compare_result= }")

            case.result = compare_result

        #1/28
        with uuid('484ff778-052d-4539-8f4e-4bea9d480b74') as case:
            # session 2 : GIF Edit
            # case2.1.9.5 : GIF Edit > Fix/Enhance > Color Adjustment
            # Select track2
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('loop.gif')

            # enter fix/enhance
            tips_area_page.click_fix_enhance()
            time.sleep(DELAY_TIME * 2)

            # Apply fix/enhance > Color Adjustment
            fix_enhance_page.enhance.switch_to_color_adjustment()
            time.sleep(DELAY_TIME * 2)
            fix_enhance_page.enhance.color_adjustment.exposure.set_value(70)
            time.sleep(DELAY_TIME * 2)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.9.5_Edit_Gif_By_Fix_Enhnace_Color_Adjustment.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.9.5_Edit_Gif_By_Fix_Enhnace_Color_Adjustment.png',
                preview_wnd, similarity=0.85)
            logger(f"{compare_result= }")

            case.result = compare_result

        #1/28
        with uuid('017143da-3839-4ce4-bf7a-9682a30956da') as case:
            # session 2 : GIF Edit
            # case2.1.10 : GIF Edit > Enable Fade-in and Fade-out
            # Select track2
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # select video on timeline
            main_page.select_timeline_media('loop.gif')

            # Edit gif via context menu
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Edit Video', 'Enable Fade-in and Fade-out')
            logger(context_menu)
            time.sleep(2)

            # seek to 00:00:01:00
            set_timecode = main_page.set_timeline_timecode('00_00_01_00')
            logger(set_timecode)

            # snapshot for preview window
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.10_Edit_Gif_By_Enable_Fade-in_and_out.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.10_Edit_Gif_By_Enable_Fade-in_and_out.png',
                preview_wnd, similarity=0.85)
            logger(compare_result)

            case.result = compare_result



    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        #1/28
        with uuid('56770d0f-3d04-4092-964b-0f4a3afff2f8') as case:
            # session 2 : GIF Edit
            # case2.1.11.1 : GIF Edit > Ripple Editing > Overwrite
            time.sleep(DELAY_TIME * 5)
            main_page.set_project_aspect_ratio_1_1()
            import_media = media_room_page.import_media_file(
                Test_Material_Folder + 'GIF_Import/loop.gif')
            logger(import_media)

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # insert .gif to timeline
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media('loop.gif')
            main_page.insert_media('loop.gif')

            # seek to 00:00:05:00
            set_timecode = main_page.set_timeline_timecode('00_00_05_00')
            logger(set_timecode)

            # Select track2
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.insert_media('Skateboard 01.mp4')

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # seek to 00:00:01:00
            set_timecode = main_page.set_timeline_timecode('00_00_01_00')
            logger(set_timecode)

            main_page.select_library_icon_view_media('Food.jpg')
            #main_page.insert_media('Food.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=0)
            time.sleep(DELAY_TIME*5)

            # snapshot for preview window
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.11.1_Edit_Gif_By_RippleEditing_Overwrite.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.11.1_Edit_Gif_By_RippleEditing_Overwrite.png',
            preview_wnd)
            logger(compare_result)

            case.result = compare_result

        #1/28
        with uuid('2fcd31c6-49b2-40a1-8ba2-9d6742957982') as case:
            # session 2 : GIF Edit
            # case2.1.11.4 : GIF Edit > Ripple Editing > Insert
            main_page.click_undo()
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media('Food.jpg')
            # main_page.insert_media('Food.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=1)
            time.sleep(DELAY_TIME * 5)

            # snapshot for preview window
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.11.4_Edit_Gif_By_RippleEditing_Insert.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.11.4_Edit_Gif_By_RippleEditing_Insert.png',
                preview_wnd)
            logger(compare_result)

            case.result = compare_result

        #1/28
        with uuid('cf2b1660-1e5b-4aad-9a8f-09d62759aa3d') as case:
            # session 2 : GIF Edit
            # case2.1.11.5 : GIF Edit > Ripple Editing > Insert and move all clips
            main_page.click_undo()
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media('Food.jpg')
            # main_page.insert_media('Food.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=2)
            time.sleep(DELAY_TIME * 5)

            # snapshot for preview window
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.11.5_Edit_Gif_By_RippleEditing_Insert&MoveAllClips.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.11.5_Edit_Gif_By_RippleEditing_Insert&MoveAllClips.png',
                preview_wnd)
            logger(compare_result)

            case.result = compare_result
        #'''
        #1/28
        with uuid('45cadb8c-4f90-44cf-954a-8ed1f547e428') as case:
            # session 2 : GIF Edit
            # case2.1.11.6 : GIF Edit > Ripple Editing > Crossfadae
            main_page.click_undo()
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media('Food.jpg')
            # main_page.insert_media('Food.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=3)
            time.sleep(DELAY_TIME * 5)

            # snapshot for preview window
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.11.6_Edit_Gif_By_RippleEditing_Crossfade.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.11.6_Edit_Gif_By_RippleEditing_Crossfade.png',
                preview_wnd, similarity=0.85)
            logger(compare_result)

            case.result = compare_result
        #'''
        #''' # Exception occurs when using "main_page.select_right_click_menu('Trim to Fit')"
        #2/9
        with uuid('92ff94b2-8891-495d-945b-3b27af86e776') as case:
            # session 2 : GIF Edit
            # case2.1.11.2 : GIF Edit > Ripple Editing > Trim to fit
            main_page.click_undo()
            time.sleep(DELAY_TIME * 2)

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # seek to 00:00:08:00
            set_timecode = main_page.set_timeline_timecode('00_00_08_00')
            logger(set_timecode)

            # insert clip from library to timeline
            main_page.select_library_icon_view_media('Food.jpg')
            main_page.insert_media('Food.jpg')
            time.sleep(DELAY_TIME * 2)

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # seek to 00:00:05:07
            set_timecode = main_page.set_timeline_timecode('00_00_05_07')
            logger(set_timecode)
            time.sleep(DELAY_TIME * 2)

            main_page.select_library_icon_view_media('loop.gif')
            main_page.tips_area_insert_media_to_selected_track(option=5) # will be marked once new page function is available
            time.sleep(DELAY_TIME * 2)
            '''
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Insert on Selected Track')
            logger(context_menu)
            time.sleep(DELAY_TIME * 5)
            context_menu1 = main_page.select_right_click_menu('Trim to Fit')
            logger(context_menu1)
            '''

            # seek to 00:00:02:02
            set_timecode = main_page.set_timeline_timecode('00_00_02_02')
            logger(set_timecode)
            time.sleep(DELAY_TIME * 2)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.11.2_Edit_Gif_By_RippleEditing_TrimToFit.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.11.2_Edit_Gif_By_RippleEditing_TrimToFit.png',
                preview_wnd)
            logger(compare_result)

            case.result = compare_result

        #2/9
        with uuid('209e9c7b-cf44-453f-9606-b820c69acc63') as case:
            # session 2 : GIF Edit
            # case2.1.11.3 : GIF Edit > Ripple Editing > Speed up to fit
            main_page.click_undo()
            time.sleep(DELAY_TIME * 2)

            # insert clip to timeline with "Speed up to fit"
            main_page.select_library_icon_view_media('loop.gif')
            main_page.tips_area_insert_media_to_selected_track(option=6) # will be marked once new page function is available
            time.sleep(DELAY_TIME * 2)
            '''
            main_page.right_click()
            context_menu = main_page.select_right_click_menu('Insert on Selected Track')
            logger(context_menu)
            # main_page.tips_area_insert_media_to_selected_track(option=1)
            time.sleep(DELAY_TIME * 2)
            context_menu1 = main_page.select_right_click_menu('Speed up to Fit')
            logger(context_menu1)
            time.sleep(DELAY_TIME * 2)
            '''

            # seek to 00:00:02:02
            set_timecode = main_page.set_timeline_timecode('00_00_02_02')
            logger(set_timecode)
            time.sleep(DELAY_TIME * 2)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.11.3_Edit_Gif_By_RippleEditing_SpeedUpToFit.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.11.3_Edit_Gif_By_RippleEditing_SpeedUpToFit.png',
                preview_wnd)
            logger(compare_result)

            case.result = compare_result
        #'''

        #2/9
        with uuid('57114446-d108-41ba-b6d0-05b44331922b') as case:
            # session 2 : GIF Edit
            # case2.1.11.7 : GIF Edit > Ripple Editing > Replace
            #main_page.click_undo()
            #time.sleep(DELAY_TIME * 2)

            # insert clip to timeline with "Speed up to fit"
            main_page.select_library_icon_view_media('loop.gif')
            main_page.tips_area_insert_media_to_selected_track(option=4)
            time.sleep(DELAY_TIME * 5)

            # seek to 00:00:05:05
            set_timecode = main_page.set_timeline_timecode('00_00_05_05')
            logger(set_timecode)
            time.sleep(DELAY_TIME * 2)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.11.7_Edit_Gif_By_RippleEditing_Replace.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.11.7_Edit_Gif_By_RippleEditing_Replace.png',
                preview_wnd)
            logger(compare_result)

            case.result = compare_result

        #2/9
        with uuid('7aef6fce-267f-4064-8b4f-2170c4e25347') as case:
            # session 2 : GIF Edit
            # case2.1.12 : GIF Edit > Render Preview

            # seek to 00:00:00:15
            set_timecode = main_page.set_timeline_timecode('00_00_00_15')
            logger(set_timecode)
            time.sleep(DELAY_TIME * 2)

            # click "Render Preview"
            timeline_operation_page.edit_timeline_render_preview()
            main_page.set_timeline_timecode('00_00_06_00')
            time.sleep(10)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G2.1.12_Edit_Gif_By_RenderPreview.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G2.1.12_Edit_Gif_By_RenderPreview.png',
                preview_wnd)
            logger(compare_result)

            case.result = compare_result

    # v20.6.4113 does NOT support project room, skip this case ( uuid)
    # v21.1.4806 (Media Room) > My project = project room
    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):

        download_folder_path = Test_Material_Folder + 'GIF_Import/download_project/01012022'
        if main_page.exist_file(download_folder_path):
            main_page.delete_folder(download_folder_path)

        #2/9
        with uuid('c6db9f1f-5dd3-44d2-a5e3-a692a85a7418') as case:
            # session 3 : Project
            # case3.1.1.1 : Insert nested project > w/ GIF edit photo
            time.sleep(DELAY_TIME * 5)
            main_page.set_project_aspect_ratio_1_1()
            import_media = media_room_page.import_media_file(
                Test_Material_Folder + 'GIF_Import/loop.gif')
            logger(import_media)

            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # insert .gif to timeline
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media('loop.gif')
            main_page.insert_media('loop.gif')

            # seek to 00:00:05:00
            set_timecode = main_page.set_timeline_timecode('00_00_05_00')
            logger(set_timecode)

            # Select track2
            select_track = main_page.timeline_select_track(2)
            logger(select_track)

            # insert new clip to timeline
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            main_page.insert_media('Skateboard 01.mp4')

            # save project
            check_result_1 = main_page.top_menu_bar_file_save_project_as()
            logger(check_result_1)
            save_proj = project_new_page.save_file.handle_save_file(
                'gif_nested_project', Test_Material_Folder + 'GIF_Import/')
            logger(save_proj)

            # new project
            check_result_2 = main_page.top_menu_bar_file_new_project()
            logger(check_result_2)
            media_room_page.find(L.media_room.library_listview.unit_collection_view_item, timeout=10)
            default_project_name = main_page.get_project_name()
            check_result_3 = False if not default_project_name == 'New Untitled Project' else True
            logger(check_result_3)

            # Enter project room
            project_room_page.enter_project_room()
            time.sleep(DELAY_TIME*2)
            #main_page.select_library_icon_view_media('Untitled') #('gif_nested_project')
            main_page.select_library_icon_view_media('gif_nested_project')  # ('gif_nested_project')
            time.sleep(DELAY_TIME*2)
            tips_area_page.click_TipsArea_btn_insert_project()
            time.sleep(DELAY_TIME*2)

            # switch to nested project tab
            nest_project_page.click_sub_project_tab(1)
            time.sleep(DELAY_TIME*2)

            # snapshot
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G3.1.1.1_Insert_nested_project.png')
            logger(preview_wnd)
            compare_result = tips_area_page.compare(
                Ground_Truth_Folder + 'G3.1.1.1_Insert_nested_project.png',
                preview_wnd)
            logger(compare_result)

            case.result = compare_result

        #2/9
        with uuid('7d05721e-def8-41fc-9cf2-2ed54b78bcaa') as case:
            # session 3 : Project
            # case3.1.1.2 : Insert nested project > Edit project
            # seek to 00:00:02:00
            time.sleep(DELAY_TIME * 2)
            set_timecode = main_page.set_timeline_timecode('00_00_02_00')
            logger(set_timecode)

            # split .gif
            tips_area_page.click_TipsArea_btn_split()

            # snapshot for timeline
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G3.1.1.2_Insert_nested_project_Split.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G3.1.1.2_Insert_nested_project_Split.png',
                                                    timeline_snap)
            logger(compare_result)

            # snapshot for preview screen
            preview_wnd = tips_area_page.snapshot(locator=L.playback_window.main,
                                                  file_name=Auto_Ground_Truth_Folder + 'G3.1.1.2_Insert_nested_project_Split_preview_window.png')
            logger(preview_wnd)
            compare_result1 = tips_area_page.compare(
                Ground_Truth_Folder + 'G3.1.1.2_Insert_nested_project_Split_preview_window.png',
                preview_wnd)
            logger(compare_result1)

            case.result = compare_result and compare_result1

        #2/9
        with uuid('3b97c81c-e7e1-44aa-86b3-0c43260eb361') as case:
            # session 3 : Project
            # case3.1.2.1 : Save & Open Project > w/ GIF Edit photo
            # Click [Stop] to reset timecode to 00:00:00:00
            playback_window_page.Edit_Timeline_PreviewOperation('Stop')
            # Select track1
            select_track = main_page.timeline_select_track(1)
            logger(select_track)

            # switch to media content
            media_room_page.enter_media_content()

            # insert .gif to timeline
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media('loop.gif')
            #main_page.insert_media('loop.gif')
            main_page.tips_area_insert_media_to_selected_track(option=1)

            # save project
            check_result_1 = main_page.top_menu_bar_file_save_project_as()
            logger(check_result_1)
            save_proj = project_new_page.save_file.handle_save_file(
                'new_project.pds', Test_Material_Folder + 'GIF_Import/')
            logger(save_proj)
            time.sleep(DELAY_TIME * 2)

            # new project
            check_result_2 = main_page.top_menu_bar_file_new_project()
            logger(check_result_2)
            media_room_page.find(L.media_room.library_listview.unit_collection_view_item, timeout=10)

            # open saved project
            project_new_page.tap_menu_bar_file_open_project()
            #project_new_page.open_project.select_project('new_project.pds', Test_Material_Folder + 'GIF_Import/')
            #project_new_page.open_project.select_project('Untitled.pds', Test_Material_Folder + 'GIF_Import/') #gif_nested_project
            project_new_page.open_project.select_project('new_project.pds', Test_Material_Folder + 'GIF_Import/')
            project_new_page.exist_click(L.main.open_file_dialog.btn_open)
            main_page.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='no')

            current_project_name = project_new_page.exist(L.main.top_project_name).AXValue
            #check_result = False if not current_project_name == 'new_project' else True
            check_result = False if not current_project_name == 'Untitled' else True

            # switch to nested project tab
            nest_project_page.click_sub_project_tab(1)
            time.sleep(DELAY_TIME * 2)

            # snapshot for timeline
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G3.1.2.1_Save & Open Project.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G3.1.2.1_Save & Open Project.png',
                                                    timeline_snap)
            logger(compare_result)

            case.result = check_result_1 and check_result_2 and compare_result

        #2/9
        with uuid('dcef6631-34e5-4915-ac19-858b2816d61a') as case:
            # session 3 : Project
            # case3.1.2.2 : Save & Open Project > w/ Nested Project included GIF Edit photo
            case.result = compare_result

        #2/10
        with uuid('ca23d882-897f-4711-898a-b25b901ebcf0') as case:
            # session 3 : Project
            # case3.1.3.1 : Pack & Open Project > w/ GIF Edit photo
            # switch back to nested project's main tab
            nest_project_page.click_nest_project_main_tab()
            time.sleep(DELAY_TIME)

            # pack project
            check_result_1 = project_new_page.menu_bar_file_pack_project_materials(
                'Untitled', Test_Material_Folder + 'GIF_Import/pack_project/')
            logger(check_result_1)

            current_project_name = main_page.get_project_name()
            check_result_2 = False if not current_project_name == 'New Untitled Project*' else True
            logger(check_result_2)
            time.sleep(DELAY_TIME * 5)

            # new project
            #check_result_3 = main_page.top_menu_bar_file_new_project()
            check_result_3 = main_page.tap_CreateNewProject_hotkey()
            logger(check_result_3)
            media_room_page.find(L.media_room.library_listview.unit_collection_view_item, timeout=10)

            # handle confirmation dialogue
            save_project_confirm_dialog = project_new_page.is_exist(L.base.confirm_dialog.main_window, timeout=5)
            check_result = False if not save_project_confirm_dialog else True
            logger(save_project_confirm_dialog)
            logger(check_result)
            project_new_page.click(L.base.confirm_dialog.btn_no)
            #main_page.press_enter_key()
            time.sleep(DELAY_TIME * 5)

            # open packed project
            check_result_1 = project_new_page.open_pdk_project(
                Test_Material_Folder + 'GIF_Import/pack_project/Untitled.pdk',
                Test_Material_Folder + 'GIF_Import/pack_project/1')
            logger(check_result_1)
            current_project_name = main_page.get_project_name()
            check_result_2 = False if not current_project_name == 'Untitled' else True
            logger(check_result_2)
            time.sleep(DELAY_TIME * 2)

            # switch to nested project tab
            nest_project_page.click_sub_project_tab(1)
            time.sleep(DELAY_TIME * 2)

            # snapshot for timeline
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G3.1.3.1_Open_Packed_Project.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G3.1.3.1_Open_Packed_Project.png',
                                                    timeline_snap)
            logger(compare_result)

            case.result = check_result and compare_result

        #2/10
        with uuid('3398d1ce-de14-40a0-aaa8-7f948aa377fe') as case:
            # session 3 : Project
            # case3.1.3.2 : Pack & Open Project > w/ Nested Project included GIF Edit photo
            case.result = compare_result

        #2/10
        with uuid('dcbdad63-3551-40a5-9f5f-4af1e2e3ba2e') as case:
            # session 3 : Project
            # case3.1.4.1 : Pack, Upload and Download Project > w/ GIF Edit photo
            # switch back to nested project's main tab
            nest_project_page.click_nest_project_main_tab()
            time.sleep(DELAY_TIME)

            # pack & upload project
            main_page.top_menu_bar_file_pack_project_and_upload_to_cyberlink_cloud()
            download_from_cl_dz_page.upload_project.set_project_name('01012022')
            download_from_cl_dz_page.pack_project_and_upload.click_ok()
            time.sleep(DELAY_TIME*3)

            # if pop up warning message 'The project already exists on CyberLink Cloud. Do you want to overwrite?
            project_exist_warning = main_page.exist(L.download_from_cl_dz.pack_project_and_upload.warning_msg.txt)
            if project_exist_warning:
                main_page.click(L.download_from_cl_dz.pack_project_and_upload.warning_msg.ok)
                time.sleep(DELAY_TIME)

            for x in range(15):
                upload_ok_btn = main_page.exist(L.download_from_cl_dz.pack_project_and_upload.ok)
                if upload_ok_btn:
                    main_page.click(L.download_from_cl_dz.pack_project_and_upload.ok)
                    logger('Success')
                    break
                else:
                    time.sleep(DELAY_TIME*2)

            # new project
            check_result_3 = main_page.tap_CreateNewProject_hotkey()
            logger(check_result_3)
            media_room_page.find(L.media_room.library_listview.unit_collection_view_item, timeout=10)

            # handle confirmation dialogue
            save_project_confirm_dialog = project_new_page.is_exist(L.base.confirm_dialog.main_window, timeout=5)
            check_result = False if not save_project_confirm_dialog else True
            logger(save_project_confirm_dialog)
            logger(check_result)
            project_new_page.click(L.base.confirm_dialog.btn_no)
            time.sleep(DELAY_TIME * 5)

            # download project from CLCloud
            main_page.top_menu_bar_file_download_project_from_cyberlink_cloud()
            time.sleep(DELAY_TIME * 3)
            download_from_cl_dz_page.download_project.select_project('01012022')

            # click [Download]
            download_from_cl_dz_page.tap_download()

            # download to the selected folder
            check_result = download_from_cl_dz_page.download_project.select_download_folder(
                Test_Material_Folder + 'GIF_Import/download_project/')
            logger(check_result)
            time.sleep(DELAY_TIME * 10)

            # open the downloaded project
            download_from_cl_dz_page.is_exist(L.download_from_cl_dz.download_project.downloaded.open, timeout=100)
            check_result_1 = download_from_cl_dz_page.download_project.downloaded.click_open()
            logger(check_result_1)

            main_page.handle_merge_media_to_current_library_dialog(option='no')

            # snapshot
            timeline_snap = tips_area_page.snapshot(locator=L.timeline_operation.workspace,
                                                    file_name=Auto_Ground_Truth_Folder + 'G3.1.4.1_Download_Uploaded_Project.png')
            logger(timeline_snap)
            compare_result = tips_area_page.compare(Ground_Truth_Folder + 'G3.1.4.1_Download_Uploaded_Project.png',
                                                    timeline_snap)
            logger(compare_result)

            # delete uploaded project
            time.sleep(DELAY_TIME * 5)
            main_page.enter_room(1)
            logger('1599')
            main_page.enter_room(0)
            logger('1601')
            main_page.top_menu_bar_file_download_project_from_cyberlink_cloud()
            logger('1603')
            time.sleep(DELAY_TIME * 2)
            download_from_cl_dz_page.download_project.select_project('01012022')
            check_result_2 = download_from_cl_dz_page.download_project.click_delete()
            logger(check_result_2)
            download_from_cl_dz_page.download_project.click_delete()
            download_from_cl_dz_page.download_project.handle_warning_msg(option='ok')
            time.sleep(DELAY_TIME * 3)
            case.result = compare_result

        # 2/10
        with uuid('a66b0e72-e345-42be-b6f0-ffb5698140b0') as case:
            # session 3 : Project
            # case3.1.4.2 : Pack, Upload and Download Project > w/ Nested Project included GIF Edit photo
            # close download project page
            download_from_cl_dz_page.press_esc_key()
            #download_from_cl_dz_page.pack_project_and_upload.click_cancel()
            case.result = compare_result

        # 2/10
        with uuid('3631098d-6ebc-45e2-9728-e284495d5109') as case:
            # session 3 : Project
            # case3.1.5.1 : Produce > H.264
            # Enter "Produce" page
            main_page.click_produce()
            produce_page.check_enter_produce_page()
            #time.sleep(DELAY_TIME * 3)

            # File extension > H264 (.MP4)
            produce_page.local.select_file_format(container='avc')

            # Adjust AVC 1080 x 1080/24p (12Mbps)
            select_profile = produce_page.local.select_profile_name(index=5)
            logger(f'{select_profile =}')
            time.sleep(DELAY_TIME * 2)
            check_profile = produce_page.local.get_profile_name()
            if check_profile != 'MPEG-4 1080 x 1080/24p (12 Mb...':
                logger('Check profile setting error')
                raise Exception
            else:
                logger('Check profile pass')
                pass
            time.sleep(DELAY_TIME)

            # set country format to ntsc
            produce_page.local.select_country_video_format('ntsc')

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
            #self.check_dont_show_again_dialog(tick=0)

            # Verify :  Video compare
            main_page.select_library_icon_view_media(explore_file)
            video_compare_result = main_page.compare_video(explore_full_path,
                                                           Test_Material_Folder + 'GIF_Import/Produce_Video.mp4')
            case.result = video_compare_result
            logger(video_compare_result)

            # Remove the produced file
            main_page.select_library_icon_view_media(explore_file)
            media_room_page.library_clip_context_menu_move_to_trash_can()

    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    258e8dd5-8160-4b7a-a919-b10579dfa40d
                    c86505d5-0f82-4bd3-85d7-56c2d6b13476
                ''') as case:
            case.result = None
            case.fail_log = "*SKIP by AT*"
            #