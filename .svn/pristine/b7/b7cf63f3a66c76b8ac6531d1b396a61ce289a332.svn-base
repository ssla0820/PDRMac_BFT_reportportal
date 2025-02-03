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
download_from_cl_dz_page = PageFactory().get_page_object('download_from_cl_dz_page', mwc)
pip_room_page = PageFactory().get_page_object('pip_room_page', mwc)
particle_room_page = PageFactory().get_page_object('particle_room_page', mwc)
title_room_page = PageFactory().get_page_object('title_room_page', mwc)
transition_room_page = PageFactory().get_page_object('transition_room_page', mwc)
title_designer_page = PageFactory().get_page_object('title_designer_page', mwc)
crop_zoom_pan_page = PageFactory().get_page_object('crop_zoom_pan_page', mwc)
pan_zoom_page = PageFactory().get_page_object('pan_zoom_page', mwc)
playback_window_page = PageFactory().get_page_object('playback_window_page', mwc)
tips_area_page = PageFactory().get_page_object('tips_area_page', mwc)
mask_designer_page = PageFactory().get_page_object('mask_designer_page', mwc)
gettyimage_page = PageFactory().get_page_object('gettyimage_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Download Content from DZ CL Cloud.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Download_Content_From_DZ_CL_Cloud/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Download_Content_From_DZ_CL_Cloud/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Download_Content_From_DZ_CL_Cloud():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        #main_page.start_app()
        #time.sleep(DELAY_TIME * 3)
        yield mwc
        #main_page.close_app()

    @classmethod
    def setup_class(cls):
        main_page.clear_cache()
        # for update the correct module start time of report (2021/04/20)
        now = datetime.datetime.now()
        report.add_ovinfo('time', now.time().strftime("%H:%M:%S"))
        report.start_time = time.time()
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_init('Download_Content_From_DZ_CL_Cloud')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"download content from dz cl cloud result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
    def test_close(self):
        download_from_cl_dz_page.download_project.click_close()
        return True

    # @pytest.mark.skip
    @exception_screenshot
    def test_caption(self):
        name = download_from_cl_dz_page.download_project.caption_name()
        print(name)
        return True

    # @pytest.mark.skip
    @exception_screenshot
    def test_sort_by_name(self):
        download_from_cl_dz_page.download_project.sort_by_name()
        return True

    # @pytest.mark.skip
    @exception_screenshot
    def test_select_project(self):
        download_from_cl_dz_page.download_project.select_project('biyr')
        return True

    # @pytest.mark.skip
    @exception_screenshot
    def test_find_project(self):
        return download_from_cl_dz_page.download_project.find_project('ojhg')


    # @pytest.mark.skip
    @exception_screenshot
    def test_delete_cancel(self):
        download_from_cl_dz_page.download_project.click_delete()
        download_from_cl_dz_page.download_project.handle_warning_msg('cancel')
        return True

    # @pytest.mark.skip
    @exception_screenshot
    def test_download(self):
        download_from_cl_dz_page.download_project.click_download()
        return True

    # @pytest.mark.skip
    @exception_screenshot
    def test_cancel(self):
        download_from_cl_dz_page.download_project.click_cancel()
        return True

    # @pytest.mark.skip
    @exception_screenshot
    def test_process_dialog_cancel(self):
        download_from_cl_dz_page.download_project.process_dialog.click_cancel()
        return True

    # @pytest.mark.skip
    @exception_screenshot
    def test_process_dialog_cancel(self):
        download_from_cl_dz_page.download_project.select_download_folder('/Users/cl/Desktop/ooo')
        return True

    # @pytest.mark.skip
    @exception_screenshot
    def test_upload_project_set_project_name(self):
        download_from_cl_dz_page.upload_project.set_project_name('alibuda')
        return True

    # @pytest.mark.skip
    @exception_screenshot
    def test_upload_project_click_cancel(self):
        download_from_cl_dz_page.upload_project.click_cancel()
        return True

    # @pytest.mark.skip
    @exception_screenshot
    def test_upload_project_uploaded_click_link(self):
        download_from_cl_dz_page.upload_project.uploaded.click_link()
        return True

    # @pytest.mark.skip
    @exception_screenshot
    def test_crop_zoom_pan_close(self):
        crop_zoom_pan_page.close_window()
        return True

    # @pytest.mark.skip
    @exception_screenshot
    def test_crop_zoom_pan_maximize(self):
        crop_zoom_pan_page.click_maximize_btn()
        return True

    # @pytest.mark.skip
    @exception_screenshot
    def test_crop_zoom_pan_set_timecode(self):
        crop_zoom_pan_page.set_timecode('00_00_03_21')
        return True

    # @pytest.mark.skip
    @exception_screenshot
    def test_crop_zoom_pan_aspect_ratio_4_3(self):
        crop_zoom_pan_page.set_AspectRatio_4_3()
        return True

    # @pytest.mark.skip
    @exception_screenshot
    def test_crop_zoom_pan_set_gridline(self):
        crop_zoom_pan_page.select_grid_lines_format(10)
        return True

    # @pytest.mark.skip
    @exception_screenshot
    def test_crop_zoom_pan_set_viewer_zoom(self):
        crop_zoom_pan_page.click_viewer_zoom_menu('50%')
        return True

    # @pytest.mark.skip
    @exception_screenshot
    def test_crop_zoom_pan_set_positionX(self):
        crop_zoom_pan_page.set_position_x(0.55)
        return True

    # @pytest.mark.skip
    @exception_screenshot
    def test_crop_zoom_pan_set_positionX_by_arrow(self):
        crop_zoom_pan_page.click_position_y_arrow('up')
        crop_zoom_pan_page.click_position_y_arrow('up')
        crop_zoom_pan_page.click_position_y_arrow('up')
        crop_zoom_pan_page.click_position_y_arrow('down')
        return True

    # @pytest.mark.skip
    @exception_screenshot
    def test_crop_zoom_pan_set_scale_width(self):
        crop_zoom_pan_page.set_scale_width("0.33")
        return True

    # @pytest.mark.skip
    @exception_screenshot
    def test_crop_zoom_pan_set_scale_width_slider(self):
        crop_zoom_pan_page.set_scale_width_slider(3.54)
        return True

    # @pytest.mark.skip
    @exception_screenshot
    def test_crop_zoom_pan_set_rotation(self):
        crop_zoom_pan_page.set_rotation('160')
        return True

    # @pytest.mark.skip
    @exception_screenshot
    def test_crop_zoom_pan_set_maintain_aspect_ratio_check(self):
        crop_zoom_pan_page.set_maintain_aspect_ratio(1)
        return True

    # @pytest.mark.skip
    @exception_screenshot
    def test_crop_zoom_pan_snap_ref_line(self):
        crop_zoom_pan_page.apply_snap_ref_line(1)
        return True

    # @pytest.mark.skip
    @exception_screenshot
    def test_crop_zoom_pan_rotation_arrow(self):
        crop_zoom_pan_page.click_rotation_arrow('up')
        crop_zoom_pan_page.click_rotation_arrow('up')
        crop_zoom_pan_page.click_rotation_arrow('up')
        crop_zoom_pan_page.click_rotation_arrow('down')
        return True

    @exception_screenshot
    def test_crop_zoom_pan_preview_slider(self):
        crop_zoom_pan_page.set_preview_slider(0)
        return True

    @exception_screenshot
    def test_crop_zoom_pan_add_keyframe(self):
        crop_zoom_pan_page.keyframe.add()
        return True

    @exception_screenshot
    def test_crop_zoom_pan_duplicate_prevoius_keyframe(self):
        crop_zoom_pan_page.keyframe.duplicate_previous()
        return True

    @exception_screenshot
    def test_playback_window_floating_menu_set_font(self):
        playback_window_page.floating_menu.set_font_type('Gill Sans')
        return True


    @exception_screenshot
    def test_2233444(self):
        pan_zoom_page.magic_motion_designer.scale_width.set_slider(0.3)
        return True

    @exception_screenshot
    def test_playback_window_click_title(self):
        playback_window_page.click_title_on_canvas()
        playback_window_page.edit_title_on_canvas('5566FFG')
        playback_window_page.unselect_title_on_canvas()
        return True

    @exception_screenshot
    def test_playback_window_floating_menu_set_font_size(self):
        playback_window_page.floating_menu.set_font_size(24)
        return True

    @exception_screenshot
    def test_playback_window_floating_menu_set_font_color(self):
        playback_window_page.floating_menu.set_font_color('283F2A')
        return True

    @exception_screenshot
    def test_tips_area_enter_shape_designer_from_tools(self):
        tips_area_page.more_features.edit_Shape_Designer()
        return True


    @exception_screenshot
    def test_tips_area_enter_color_match(self):
        tips_area_page.click_color_match_button()
        return True

    @exception_screenshot
    def test_tips_mask_designer_enter_brush_mask_designer(self):
        mask_designer_page.click_create_brush_mask_btn()
        return True

    @exception_screenshot
    def test_tips_mask_designer_brush_mask_auto_object(self):
        mask_designer_page.brush_mask.enable_auto_object_selection('No')
        return True

    @exception_screenshot
    def test_tips_mask_designer_brush_mask_drew_canvas(self):
        mask_designer_page.brush_mask.click_mouse_on_canvas_center()
        return True

    @exception_screenshot
    def test_tips_mask_designer_brush_mask_width_value(self):
        mask_designer_page.brush_mask.width.set_arrow(1,3)
        return True

    @exception_screenshot
    def test_tips_mask_designer_brush_mask_zoom(self):
        mask_designer_page.brush_mask.click_viewer_zoom_menu("25%")
        return True

    @exception_screenshot
    def test_tips_mask_designer_brush_mask_timecode(self):
        mask_designer_page.brush_mask.set_timecode("00_00_03_11")
        return True

    @exception_screenshot
    def test_tips_mask_designer_motion_open_path(self):
        mask_designer_page.motion.open_path_tag()
        return True


    @exception_screenshot
    def test_tips_mask_designer_motion_select_category(self):
        mask_designer_page.motion.select_category('all')
        return True

    @exception_screenshot
    def test_tips_mask_designer_motion_select_path(self):
        mask_designer_page.motion.select_path_template(4)
        return True

    @exception_screenshot
    def test_tips_mask_designer_resize(self):
        mask_designer_page.adjust_object_on_canvas_resize()
        return True


    @exception_screenshot
    def test_tips_mask_designer_remove_path_template(self):
        mask_designer_page.motion.remove_custom_template(2)
        return True

    @exception_screenshot
    def test_gettyimage_filter_set_check_vertical(self):
        gettyimage_page.filter.photo.image_style.set_portrait(1)
        return True











































































































