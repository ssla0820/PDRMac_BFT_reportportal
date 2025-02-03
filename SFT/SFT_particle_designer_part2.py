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
timeline_page = PageFactory().get_page_object('timeline_operation_page', mwc)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mwc)
playback_window_page = PageFactory().get_page_object('playback_window_page',mwc)
particle_room_page = PageFactory().get_page_object('particle_room_page',mwc)
particle_designer_page = PageFactory().get_page_object('particle_designer_page',mwc)

# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Particle Designer_part2.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder - Setup for Overall Project
Ground_Truth_Folder = app.ground_truth_root + '/Particle_Designer/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Particle_Designer/'
Test_Material_Folder = app.testing_material

# For Ground Truth / Test Material folder - Setup for Duncan personal testing
# Ground_Truth_Folder = '/Users/cl/Desktop/Duncan/SFT/GroundTruth/Title_Room/'
# Auto_Ground_Truth_Folder = '/Users/cl/Desktop/Duncan/SFT/ATGroundTruth/Title_Room/'
# Test_Material_Folder = '/Users/cl/Desktop/Duncan/Material/'

DELAY_TIME = 1

class Test_Particle_Designer_part2():
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
            google_sheet_execution_log_init('Particle_Designer_part2')

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



    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_11(self):
        with uuid("a50178ee-493f-4fff-a6b3-6c8ee31de75a") as case:
            # Zoom in Preview

            time.sleep(1)
            main_page.enter_room(5)
            media_room_page.select_media_content('Effect-A')
            # Click "Modify Particle Template"
            particle_room_page.click_ModifySelectedParticle_btn()

            time.sleep(1)
            # Drag Size slider to Max + Snapshot Preview of Particle Designer
            particle_designer_page.express_mode.drag_Size_slider(value=200000)

            time.sleep(1)
            particle_designer_page.click_zoom_in(times=2)

            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L260_ParticleDesigner(ZoomIn_Preview).png'
            ground_truth = Ground_Truth_Folder + 'L260_ParticleDesigner(ZoomIn_Preview).png'
            current_preview = particle_designer_page.snapshot(
                locator=L.particle_designer.preview_area, file_name=image_full_path)
            case.result = particle_designer_page.compare(ground_truth, current_preview)


        with uuid("0fadb02a-8304-4861-afc9-df27555b3c45") as case:
            # Zoom out Preview
            time.sleep(1)
            particle_designer_page.click_zoom_out(times=4)

            time.sleep(3)
            image_full_path = Auto_Ground_Truth_Folder + 'L261_ParticleDesigner(ZoomOut_Preview).png'
            ground_truth = Ground_Truth_Folder + 'L261_ParticleDesigner(ZoomOut_Preview).png'
            current_preview = particle_designer_page.snapshot(
                locator=L.particle_designer.preview_area, file_name=image_full_path)
            case.result = particle_designer_page.compare(ground_truth, current_preview)


        with uuid("530daa7a-f503-4c5b-b937-dd51f16906d5") as case:
            # Fit Preview

            time.sleep(1)
            particle_designer_page.click_viewer_zoom_menu(value='Fit')
            current_value = particle_designer_page.get_viewer_setting()

            # Verify Zoom = Fit
            if current_value == 'Fit':
                default_value = True
                logger(default_value)
            else:
                default_value = False
                logger(default_value)

            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L262_ParticleDesigner(Fit_Preview).png'
            ground_truth = Ground_Truth_Folder + 'L262_ParticleDesigner(Fit_Preview).png'
            current_preview = particle_designer_page.snapshot(
                locator=L.particle_designer.preview_area, file_name=image_full_path)
            case.result = particle_designer_page.compare(ground_truth, current_preview)


        with uuid("78608ba2-8923-4339-81ed-1ad956fa83e6") as case:
            # Zoom 10% Preview

            time.sleep(1)
            # Get Viewer value
            particle_designer_page.click_viewer_zoom_menu(value='10%')
            current_value = particle_designer_page.get_viewer_setting()

            # Verify Zoom = 10%
            if current_value == '10%':
                default_value = True
                logger(default_value)
            else:
                default_value = False
                logger(default_value)

            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L263_ParticleDesigner(Zoom10%_Preview).png'
            ground_truth = Ground_Truth_Folder + 'L263_ParticleDesigner(Zoom10%_Preview).png'
            current_preview = particle_designer_page.snapshot(
                locator=L.particle_designer.preview_area, file_name=image_full_path)
            case.result = particle_designer_page.compare(ground_truth, current_preview) and default_value


        with uuid("761ad4f0-6aa2-42cc-a36c-f10ff14ea294") as case:
            # Zoom 25% Preview
            time.sleep(1)
            particle_designer_page.click_viewer_zoom_menu(value='25%')
            current_value = particle_designer_page.get_viewer_setting()

            # Verify Zoom = 25%
            if current_value == '25%':
                default_value = True
                logger(default_value)
            else:
                default_value = False
                logger(default_value)

            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L264_ParticleDesigner(Zoom25%_Preview).png'
            ground_truth = Ground_Truth_Folder + 'L264_ParticleDesigner(Zoom25%_Preview).png'
            current_preview = particle_designer_page.snapshot(
                locator=L.particle_designer.preview_area, file_name=image_full_path)
            case.result = particle_designer_page.compare(ground_truth, current_preview) and default_value


        with uuid("3fce28e9-db76-493c-b4c4-f3001fbd0851") as case:
            # Zoom 50% Preview
            time.sleep(1)
            particle_designer_page.click_viewer_zoom_menu(value='50%')
            current_value = particle_designer_page.get_viewer_setting()

            # Verify Zoom = 50%
            if current_value == '50%':
                default_value = True
                logger(default_value)
            else:
                default_value = False
                logger(default_value)

            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L265_ParticleDesigner(Zoom50%_Preview).png'
            ground_truth = Ground_Truth_Folder + 'L265_ParticleDesigner(Zoom50%_Preview).png'
            current_preview = particle_designer_page.snapshot(
                locator=L.particle_designer.preview_area, file_name=image_full_path)
            case.result = particle_designer_page.compare(ground_truth, current_preview) and default_value


        with uuid("4aee2008-dbaf-4da8-b33b-77136d259076") as case:
            # Zoom 75% Preview
            time.sleep(1)
            particle_designer_page.click_viewer_zoom_menu(value='75%')
            current_value = particle_designer_page.get_viewer_setting()

            # Verify Zoom = 75%
            if current_value == '75%':
                default_value = True
                logger(default_value)
            else:
                default_value = False
                logger(default_value)

            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L266_ParticleDesigner(Zoom75%_Preview).png'
            ground_truth = Ground_Truth_Folder + 'L266_ParticleDesigner(Zoom75%_Preview).png'
            current_preview = particle_designer_page.snapshot(
                locator=L.particle_designer.preview_area, file_name=image_full_path)
            case.result = particle_designer_page.compare(ground_truth, current_preview) and default_value


        with uuid("fc5903d5-71fd-43ea-97bd-c8b14c3c50c8") as case:
            # Zoom 100% Preview
            time.sleep(1)
            particle_designer_page.click_viewer_zoom_menu(value='100%')
            current_value = particle_designer_page.get_viewer_setting()

            # Verify Zoom = 100%
            if current_value == '100%':
                default_value = True
                logger(default_value)
            else:
                default_value = False
                logger(default_value)

            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L267_ParticleDesigner(Zoom100%_Preview).png'
            ground_truth = Ground_Truth_Folder + 'L267_ParticleDesigner(Zoom100%_Preview).png'
            current_preview = particle_designer_page.snapshot(
                locator=L.particle_designer.preview_area, file_name=image_full_path)
            case.result = particle_designer_page.compare(ground_truth, current_preview) and default_value


        with uuid("88708f3f-68f0-4635-9349-ee3be23bf1ff") as case:
            # Zoom 200% Preview
            time.sleep(1)
            particle_designer_page.click_viewer_zoom_menu(value='200%')
            current_value = particle_designer_page.get_viewer_setting()

            # Verify Zoom = 200%
            if current_value == '200%':
                default_value = True
                logger(default_value)
            else:
                default_value = False
                logger(default_value)

            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L268_ParticleDesigner(Zoom200%_Preview).png'
            ground_truth = Ground_Truth_Folder + 'L268_ParticleDesigner(Zoom200%_Preview).png'
            current_preview = particle_designer_page.snapshot(
                locator=L.particle_designer.preview_area, file_name=image_full_path)
            case.result = particle_designer_page.compare(ground_truth, current_preview) and default_value


        with uuid("0317a3f9-1449-41ce-b25e-d076d6f9d5cb") as case:
            # Zoom 300% Preview
            time.sleep(1)
            particle_designer_page.click_viewer_zoom_menu(value='300%')
            current_value = particle_designer_page.get_viewer_setting()

            # Verify Zoom = 300%
            if current_value == '300%':
                default_value = True
                logger(default_value)
            else:
                default_value = False
                logger(default_value)

            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L269_ParticleDesigner(Zoom300%_Preview).png'
            ground_truth = Ground_Truth_Folder + 'L269_ParticleDesigner(Zoom300%_Preview).png'
            current_preview = particle_designer_page.snapshot(
                locator=L.particle_designer.preview_area, file_name=image_full_path)
            case.result = particle_designer_page.compare(ground_truth, current_preview) and default_value


        with uuid("44a32375-3b2b-4217-a836-9364c32d0c1f") as case:
            # Zoom 400% Preview
            time.sleep(1)
            particle_designer_page.click_viewer_zoom_menu(value='400%')
            current_value = particle_designer_page.get_viewer_setting()

            # Verify Zoom = 400%
            if current_value == '400%':
                default_value = True
                logger(default_value)
            else:
                default_value = False
                logger(default_value)

            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L270_ParticleDesigner(Zoom400%_Preview).png'
            ground_truth = Ground_Truth_Folder + 'L270_ParticleDesigner(Zoom400%_Preview).png'
            current_preview = particle_designer_page.snapshot(
                locator=L.particle_designer.preview_area, file_name=image_full_path)
            case.result = particle_designer_page.compare(ground_truth, current_preview) and default_value


    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_12(self):
        with uuid("97190a0a-8c3c-4cc7-aa99-1ef1ba0a2644") as case:
            # Check Playback: Play + Pause...

            time.sleep(1)
            main_page.enter_room(5)
            media_room_page.select_media_content('Effect-A')
            # Click "Modify Particle Template"
            particle_room_page.click_ModifySelectedParticle_btn()

            time.sleep(1)
            particle_designer_page.click_preview_operation('Play')

            time.sleep(1)
            check_preview = particle_designer_page.Check_PreviewWindow_is_different(area=L.particle_designer.preview_area,sec=2)

            time.sleep(1)
            particle_designer_page.click_preview_operation('Pause')

            current_timecode = particle_designer_page.get_timecode()

            # Verify Timecode != 00_00_00_00
            if current_timecode != '00_00_00_00':
                default_value = True
                logger(default_value)
            else:
                default_value = False
                logger(default_value)

            case.result = check_preview and current_timecode

        with uuid("97e38d19-54b1-4203-b8d0-787a0b566a09") as case:
            # Check Playback: Play + Stop...

            time.sleep(1)
            particle_designer_page.click_preview_operation('Play')

            time.sleep(1)
            particle_designer_page.click_preview_operation('Stop')

            current_timecode = particle_designer_page.get_timecode()

            # Verify Timecode == 00_00_00_00
            if current_timecode == '00_00_00_00':
                default_value = True
                logger(default_value)
            else:
                default_value = False
                logger(default_value)

            case.result = current_timecode

        with uuid("0f07d3d6-c128-4c32-834d-4bfb5425f78f") as case:
            # Check Playback: Next frame...

            time.sleep(1)
            particle_designer_page.click_preview_operation('Next_Frame')

            current_timecode = particle_designer_page.get_timecode()

            # Verify Timecode == 00_00_00_01
            if current_timecode == '00_00_00_01':
                default_value = True
                logger(default_value)
            else:
                default_value = False
                logger(default_value)

            case.result = current_timecode

        with uuid("d243a8c4-b11b-4efa-af95-b94b340de578") as case:
            # Check Playback: Previous frame...

            time.sleep(1)
            particle_designer_page.click_preview_operation('Previous_Frame')

            current_timecode = particle_designer_page.get_timecode()

            # Verify Timecode == 00_00_00_00
            if current_timecode == '00_00_00_00':
                default_value = True
                logger(default_value)
            else:
                default_value = False
                logger(default_value)

            case.result = current_timecode

        with uuid("d911d9eb-1d9c-41ce-8120-97c9e28474b0") as case:
            # Check Playback: Fast Forward...

            time.sleep(1)
            particle_designer_page.click_preview_operation('Fast_Forward')

            current_timecode = particle_designer_page.get_timecode()

            # Verify Timecode != 00_00_00_00
            if current_timecode != '00_00_00_00':
                default_value = True
                logger(default_value)
            else:
                default_value = False
                logger(default_value)

            case.result = current_timecode

        with uuid("1ece6799-8673-476b-9575-01982e1acf17") as case:
            # Check Playback: Input Timecode...

            time.sleep(1)
            particle_designer_page.click_preview_operation('Stop')
            # Set Timecode

            preview1 = particle_designer_page.set_timecode('00_00_03_00')
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L288_ParticleRoom_InputTimecode.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L288_ParticleRoom_InputTimecode.png', current_image)
            case.result = compare_result


        with uuid("4e6d469c-db97-4f3e-9ae1-aafd905fbf53") as case:
            # Check Playback: Display Timecode...

            current_timecode = particle_designer_page.get_timecode()
            # Verify Timecode != 00_00_03_00
            if current_timecode != '00_00_03_00':
                default_value = True
                logger(default_value)
            else:
                default_value = False
                logger(default_value)

            case.result = current_timecode