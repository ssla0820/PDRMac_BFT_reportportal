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
report = MyReport("MyReport", driver=mwc, html_name="Particle Designer.html")
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

class Test_Particle_Designer():
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
            google_sheet_execution_log_init('Particle_Designer')

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
        with uuid("abe40abf-1ddd-4a1a-9a1c-7636157701f3") as case:
            # Enter Particle Designer by "Modify Template" button from Particle Room...
            # Entry Particle Room
            time.sleep(1)
            main_page.enter_room(5)
            time.sleep(2)
            main_page.select_LibraryRoom_category('General')
            time.sleep(1)
            media_room_page.select_media_content('Effect-A')
            # Click "Modify Particle Template"
            particle_room_page.click_ModifySelectedParticle_btn()
            time.sleep(1)

            entry_check = particle_designer_page.check_in_particle_designer()
            case.result = entry_check

            particle_designer_page.press_esc_key()


        with uuid("7d99746a-183a-4320-ac05-cbad20cc9441") as case:
            # Enter Particle Designer by "Modify Template" context menu from Particle Room...
            time.sleep(1)
            media_room_page.select_media_content('Effect-A')
            # Right Click to select "Modify Template"
            time.sleep(1)
            particle_room_page.right_click()
            time.sleep(1)
            particle_room_page.select_right_click_menu('Modify Template...')
            particle_room_page.keyboard.enter()
            time.sleep(1)

            entry_check = particle_designer_page.check_in_particle_designer()
            case.result = entry_check

            particle_designer_page.press_esc_key()


        with uuid("0249e40e-45d0-480e-8f13-58442f5acf86") as case:
            # Enter Particle Designer by Double Click from Particle Room...
            time.sleep(1)
            media_room_page.select_media_content('Effect-A')
            # Right Click to select "Modify Template"
            time.sleep(1)
            particle_room_page.double_click()
            time.sleep(1)

            entry_check = particle_designer_page.check_in_particle_designer()
            case.result = entry_check

            particle_designer_page.press_esc_key()


        with uuid("996098ee-3577-4f96-a5d8-21aa464359ca") as case:
            # Enter Particle Designer by "Designer" button from Tip Area...
            time.sleep(1)
            media_room_page.select_media_content('Effect-A')
            # Right Click to select "Modify Template"
            time.sleep(1)
            particle_room_page.right_click()
            time.sleep(1)
            particle_room_page.select_right_click_menu('Add to Timeline')
            # Select Timeline Clip
            timeline_page.select_timeline_media(track_index=0, clip_index=0)
            # Enter Tip Area > "Designer"
            tips_area_page.click_TipsArea_btn_Designer('particle')
            time.sleep(1)

            entry_check = particle_designer_page.check_in_particle_designer()
            case.result = entry_check

            particle_designer_page.press_esc_key()


        with uuid("603c042a-4451-4c07-918f-2a1bedbf5836") as case:
            # Enter Particle Designer by "More Features" button from Tip Area...

            # Restart PDR
            main_page.close_and_restart_app()
            time.sleep(1)

            main_page.enter_room(5)
            # Click "Modify Particle Template"
            main_page.select_LibraryRoom_category('General')
            time.sleep(1)
            media_room_page.select_media_content('Effect-A')
            # Right Click to select "Modify Template"
            time.sleep(1)
            particle_room_page.right_click()
            time.sleep(1)
            particle_room_page.select_right_click_menu('Add to Timeline')
            time.sleep(1)
            # Select Timeline Clip
            timeline_page.select_timeline_media(track_index=0, clip_index=0)
            # Enter Tip Area > "More Features"
            tips_area_page.more_features.click_btn()
            tips_area_page.select_right_click_menu('Edit in Particle Designer...')
            time.sleep(1)

            entry_check = particle_designer_page.check_in_particle_designer()
            case.result = entry_check

            particle_designer_page.press_esc_key()


        with uuid("d7e5be44-3d11-4980-9409-d5bc197f6a27") as case:
            # Enter Particle Designer by "Designer" button from Tip Area...

            # Restart PDR
            main_page.close_and_restart_app()
            time.sleep(1)
            main_page.enter_room(5)
            # Click "Modify Particle Template"

            main_page.select_LibraryRoom_category('General')
            time.sleep(1)
            media_room_page.select_media_content('Effect-A')
            # Right Click to select "Modify Template"
            time.sleep(1)
            particle_room_page.right_click()
            time.sleep(1)
            particle_room_page.select_right_click_menu('Add to Timeline')
            time.sleep(1)
            timeline_page.select_timeline_media(track_index=0, clip_index=0)
            timeline_operation_page.right_click()
            timeline_operation_page.select_right_click_menu('Edit in Particle Designer...')
            time.sleep(1)

            entry_check = particle_designer_page.check_in_particle_designer()
            case.result = entry_check

            particle_designer_page.press_esc_key()


        with uuid("1a6d56e7-9c4b-4e0a-afee-24d399006f19") as case:
            # Enter Particle Designer by "Designer" button from Tip Area...

            # Restart PDR
            main_page.close_and_restart_app()
            time.sleep(1)
            main_page.enter_room(5)
            # Click "Modify Particle Template"

            main_page.select_LibraryRoom_category('General')
            time.sleep(1)
            media_room_page.select_media_content('Effect-A')
            # Right Click to select "Modify Template"
            time.sleep(1)
            particle_room_page.right_click()
            time.sleep(1)

            particle_room_page.select_right_click_menu('Add to Timeline')
            time.sleep(1)
            timeline_page.select_timeline_media(track_index=0, clip_index=0)
            timeline_operation_page.double_click()
            time.sleep(1)

            entry_check = particle_designer_page.check_in_particle_designer()
            case.result = entry_check

            particle_designer_page.press_esc_key()


    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid("9813f801-ee6f-41e6-98cf-2b13ec0ec500") as case:
            # Enter Particle Designer by "Fn" + "F2" hotkey of Timeline
            # Entry Particle Room
            time.sleep(2)
            main_page.enter_room(5)
            time.sleep(2)
            main_page.select_LibraryRoom_category('General')
            time.sleep(1)
            media_room_page.select_media_content('Effect-A')
            # Right Click to select "Modify Template"
            time.sleep(1)
            particle_room_page.right_click()
            time.sleep(1)
            particle_room_page.select_right_click_menu('Add to Timeline')
            timeline_page.select_timeline_media(track_index=0, clip_index=0)
            # Hold "f2" hotkey
            particle_designer_page.press_hotkey_enter_designer()
            time.sleep(1)

            entry_check = particle_designer_page.check_in_particle_designer()
            case.result = entry_check

        with uuid("68551de3-99ec-44db-9549-edc577075f59") as case:
            # Check Left Panel page of Particle Designer...
            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L91_ParticleDesigner(DisplayLeftPanel).png'
            ground_truth = Ground_Truth_Folder + 'L91_ParticleDesigner(DisplayLeftPanel).png'
            current_preview = particle_designer_page.snapshot(locator=L.particle_designer.properties_panel,
                                                                file_name=image_full_path)
            check_result = particle_designer_page.compare(ground_truth, current_preview)
            case.result = check_result


        with uuid("1ad872cb-8bb1-42d2-8d47-934c693d1323") as case:
            # Check Viewer display of Particle Designer...
            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L92_ParticleDesigner(Viewer).png'
            ground_truth = Ground_Truth_Folder + 'L92_ParticleDesigner(Viewer).png'
            current_preview = particle_designer_page.snapshot(locator=L.particle_designer.preview_area,
                                                                file_name=image_full_path)
            check_result = particle_designer_page.compare(ground_truth, current_preview)
            case.result = check_result


    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        with uuid("c6962392-7c20-4825-9ee9-de558645053b") as case:
            # Check Express Mode > modify Parameters > Emit Rate > Default ...
            # Entry Particle Room
            time.sleep(1)
            main_page.enter_room(5)
            main_page.select_LibraryRoom_category('General')
            time.sleep(1)
            media_room_page.select_media_content('Effect-A')
            # Click "Modify Particle Template"
            particle_room_page.click_ModifySelectedParticle_btn()
            time.sleep(1)

            # Get Emit Rate value
            current_value = particle_designer_page.express_mode.get_Emit_value()
            logger(current_value)

            # Verify Emit Rate = Default (100000)
            if current_value == 100000:
                default_value = True
                logger(default_value)
            else:
                default_value = False
                logger(default_value)
            case.result = default_value


        with uuid("7f8e08ce-c95f-4435-95e0-048ac355dd2d") as case:
            # Check Express Mode > modify Parameters > Emit Rate > [+] ...

            # Emit Rate > Click [+] button x 5 times
            particle_designer_page.express_mode.click_Emit_plus_btn(times=5)

            # Get Emit Rate value
            current_value = particle_designer_page.express_mode.get_Emit_value()
            logger(current_value)

            # Verify Emit Rate > click [+] button x 5 times
            if current_value == 105000:
                custom_value = True
                logger(default_value)
            else:
                custom_value = False
                logger(default_value)
            case.result = custom_value


        with uuid("c7b388d0-6868-4126-a820-10525d60a021") as case:
            # Check Express Mode > modify Parameters > Emit Rate > [-] ...
            time.sleep(1)
            # Emit Rate > Click [-] button x 5 times
            particle_designer_page.express_mode.click_Emit_minus_btn(times=5)
            time.sleep(1)

            # Get Emit Rate value
            current_value = particle_designer_page.express_mode.get_Emit_value()
            logger(current_value)

            # Verify Emit Rate value
            if current_value == 100000:
                custom_value = True
            else:
                custom_value = False
            case.result = custom_value


        with uuid("d971dead-c7a3-4e8f-97e4-abcee738ea14") as case:
            # Check Express Mode > modify Parameters > Emit Rate > Min value...

            # Drag Emit Rate slider to Min
            particle_designer_page.express_mode.drag_Emit_slider(value=0)
            time.sleep(1)

            # Get Emit Rate value
            current_value = particle_designer_page.express_mode.get_Emit_value()
            logger(current_value)

            # Verify Emit Rate value
            if current_value == 0:
                min_value = True
            else:
                min_value = False

            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L96_ParticleDesigner(EmitRate_Min).png'
            ground_truth = Ground_Truth_Folder + 'L96_ParticleDesigner(EmitRate_Min).png'
            current_preview = particle_designer_page.snapshot(locator=L.particle_designer.preview_area,
                                                                file_name=image_full_path)
            check_result = particle_designer_page.compare(ground_truth, current_preview)
            case.result = check_result and min_value


        with uuid("288641e8-ad70-444a-9ec4-76e45e989c6f") as case:
            # Check Express Mode > modify Parameters > Emit Rate > Max value...

            time.sleep(1)
            # Drag Emit Rate slider to Max
            particle_designer_page.express_mode.drag_Emit_slider(value=200000)
            time.sleep(1)

            # Get Emit Rate value
            current_value = particle_designer_page.express_mode.get_Emit_value()
            logger(current_value)

            # Verify Emit Rate value
            if current_value == 200000:
                max_value = True
            else:
                max_value = False
            case.result = max_value

        with uuid("f6248af1-b30d-4ef4-8239-e3f740cc8ca5") as case:
            # Verify Emit Rate = Max value from Preview ...

            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L98_ParticleDesigner(EmitRate_Slider_Max).png'
            ground_truth = Ground_Truth_Folder + 'L98_ParticleDesigner(EmitRate_Slider_Max).png'
            current_preview = particle_designer_page.snapshot(locator=L.particle_designer.preview_area,
                                                                file_name=image_full_path)
            check_result = particle_designer_page.compare(ground_truth, current_preview)
            case.result = check_result


    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        with uuid("9cd0abb9-3eda-4760-ae0c-b1da09b0a14d") as case:
            # Undo ...
            # Undo to restore Emit Rate = Default
            time.sleep(1)
            main_page.enter_room(5)
            main_page.select_LibraryRoom_category('General')
            time.sleep(1)
            media_room_page.select_media_content('Effect-A')
            # Click "Modify Particle Template"
            particle_room_page.click_ModifySelectedParticle_btn()

            time.sleep(1)
            # Snapshot Video clip icon from Library
            before_image1 = particle_designer_page.snapshot(locator=L.particle_designer.designer_window,

                                                                file_name=Auto_Ground_Truth_Folder + 'L33_ParticleDesigner(EmitRate_Slider_BeforeUndo_Default_Window_Check).png')
            time.sleep(1)
            # Drag Emit Rate slider to Max
            particle_designer_page.express_mode.drag_Emit_slider(value=200000)
            time.sleep(1)
            before_image2 = particle_designer_page.snapshot(locator=L.particle_designer.designer_window,
                                                                file_name=Auto_Ground_Truth_Folder + 'L35_ParticleDesigner(EmitRate_Slider_BeforeRedo_Max_Window_Check).png')

            time.sleep(1)
            # Undo
            particle_designer_page.click_undo()
            time.sleep(1)
            after_image1 = particle_designer_page.snapshot(locator=L.particle_designer.designer_window,
                                                                file_name=Auto_Ground_Truth_Folder + 'L33_ParticleDesigner(EmitRate_Slider_Undo_Default_Window_Check).png')

            case.result = before_image1 and after_image1

        with uuid("b811cda8-312d-4cac-a9c2-3aee2e9ddb31") as case:
            # Redo...

            # Redo to Emit Rate slider to Max
            particle_designer_page.click_redo()

            time.sleep(1)
            # Snapshot Video clip icon from Library
            after_image2 = particle_designer_page.snapshot(locator=L.particle_designer.designer_window,
                                                                file_name=Auto_Ground_Truth_Folder + 'L35_ParticleDesigner(EmitRate_Slider_Redo_Max_Window_Check).png')
            case.result = before_image2 and after_image2


        with uuid("23e80f47-6401-4021-94c2-1c3a248dde2a") as case:
            # Undo Hotkey...

            time.sleep(1)
            # Snapshot Video clip icon from Library
            before_image1 = particle_designer_page.snapshot(locator=L.particle_designer.preview_area,
                                                                file_name=Auto_Ground_Truth_Folder + 'L34_ParticleDesigner(EmitRate_Slider_BeforeUndo_Default).png')
            # Drag Emit Rate slider to Max
            time.sleep(1)
            particle_designer_page.express_mode.drag_Emit_slider(value=200000)
            before_image2 = particle_designer_page.snapshot(locator=L.particle_designer.preview_area,
                                                                file_name=Auto_Ground_Truth_Folder + 'L36_ParticleDesigner(EmitRate_Slider_BeforeRedo_Max).png')

            # Undo
            time.sleep(1)
            particle_designer_page.tap_Undo_hotkey()
            after_image1 = particle_designer_page.snapshot(locator=L.particle_designer.preview_area,
                                                                file_name=Auto_Ground_Truth_Folder + 'L34_ParticleDesigner(EmitRate_Slider_Undo_Hotkey_Default).png')

            case.result = before_image1 and after_image1

        with uuid("25bcbdca-48ff-4778-96da-ee2bf3456bbc") as case:
            # Redo Hotkey...

            # Redo to Emit Rate slider to Max
            particle_designer_page.tap_Redo_hotkey()

            time.sleep(1)
            # Snapshot Video clip icon from Library
            after_image2 = particle_designer_page.snapshot(locator=L.particle_designer.preview_area,
                                                                file_name=Auto_Ground_Truth_Folder + 'L36_ParticleDesigner(EmitRate_Slider_Redo_Hotkey_Max).png')
            case.result = before_image2 and after_image2

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        with uuid("c0e5f990-f781-48dc-a517-16aa6f472912") as case:
            # Check Express Mode > modify Parameters > Max count > Default ...
            # Entry Particle Room
            time.sleep(1)
            main_page.enter_room(5)
            main_page.select_LibraryRoom_category('General')
            time.sleep(1)
            media_room_page.select_media_content('Effect-A')
            # Click "Modify Particle Template"
            time.sleep(1)
            particle_room_page.click_ModifySelectedParticle_btn()
            time.sleep(1)

            # Get Max count value
            current_value = particle_designer_page.express_mode.get_Max_value()
            logger(current_value)

            # Verify Max count = Default (100000)
            if current_value == 100000:
                default_value = True
                logger(default_value)
            else:
                default_value = False
                logger(default_value)
            case.result = default_value


        with uuid("72277c25-93f9-4f63-980a-264d682ffe59") as case:
            # Check Express Mode > modify Parameters > Max count > [+] ...

            # Max count  > Click [+] button x 5 times
            particle_designer_page.express_mode.click_Max_plus_btn(times=5)

            # Get Max count value
            current_value = particle_designer_page.express_mode.get_Max_value()
            logger(current_value)

            # Verify Max count > click [+] button x 5 times
            if current_value == 105000:
                custom_value = True
                logger(default_value)
            else:
                custom_value = False
                logger(default_value)
            case.result = custom_value



        with uuid("f0f6f663-8168-45b6-9aee-4e787bfc4358") as case:
            # Check Express Mode > modify Parameters > Max count > [-] ...
            time.sleep(1)
            # Min count  > Click [-] button x 5 times
            particle_designer_page.express_mode.click_Max_minus_btn(times=5)
            time.sleep(1)

            # Get Min count value
            current_value = particle_designer_page.express_mode.get_Max_value()
            logger(current_value)

            # Verify Max count > click [-] button x 5 times
            if current_value == 100000:
                custom_value = True
                logger(default_value)
            else:
                custom_value = False
                logger(default_value)
            case.result = custom_value


        with uuid("4d953e54-26ed-4fd3-b30a-b2487d019dfd") as case:
            # Check Express Mode > modify Parameters > Max count > Min value...

            # Drag "Max count" slider to Min
            particle_designer_page.express_mode.drag_Max_slider(value=0)
            time.sleep(1)

            # Get Max count value
            current_value = particle_designer_page.express_mode.get_Max_value()
            logger(current_value)

            # Verify Max count value
            if current_value == 0:
                min_value = True
            else:
                min_value = False

            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L102_ParticleDesigner(MacCount_Min).png'
            ground_truth = Ground_Truth_Folder + 'L102_ParticleDesigner(MacCount_Min).png'
            current_preview = particle_designer_page.snapshot(locator=L.particle_designer.preview_area,
                                                                file_name=image_full_path)
            check_result = particle_designer_page.compare(ground_truth, current_preview)
            case.result = check_result and min_value


        with uuid("dfd3be39-abc0-4afd-80ed-aff6b940aa9d") as case:
            # Check Express Mode > modify Parameters > Max count > Max value ...

            time.sleep(1)
            # Drag "Max count" slider to Max
            particle_designer_page.express_mode.drag_Max_slider(value=200000)
            time.sleep(1)

            # Get Max count value
            current_value = particle_designer_page.express_mode.get_Max_value()
            logger(current_value)

            # Verify Max count
            if current_value == 200000:
                custom_value = True
                logger(default_value)
            else:
                custom_value = False
                logger(default_value)

            case.result = custom_value

        with uuid("56171e76-16a3-428a-b93d-186866baf4a4") as case:
            # Max Max count + Verify
            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L104_ParticleDesigner(MacCount_Slider_Max).png'
            ground_truth = Ground_Truth_Folder + 'L104_ParticleDesigner(MacCount_Slider_Max).png'
            current_preview = particle_designer_page.snapshot(locator=L.particle_designer.preview_area,
                                                                file_name=image_full_path)
            check_result = particle_designer_page.compare(ground_truth, current_preview)
            case.result = check_result




    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):
        with uuid("d142cc71-d7cc-4e68-86d1-ddf9e3fcacdc") as case:
            # Check Express Mode > modify Parameters > Life > Default ...
            # Entry Particle Room
            time.sleep(1)
            main_page.enter_room(5)
            main_page.select_LibraryRoom_category('General')
            time.sleep(1)
            media_room_page.select_media_content('Effect-A')
            # Click "Modify Particle Template"
            time.sleep(1)
            particle_room_page.click_ModifySelectedParticle_btn()
            time.sleep(1)

            # Get Life value
            current_value = particle_designer_page.express_mode.get_Life_value()
            logger(current_value)

            # Verify Life = Default (100000)
            if current_value == 100000:
                default_value = True
                logger(default_value)
            else:
                default_value = False
                logger(default_value)
            case.result = default_value


        with uuid("28199b88-5c18-48a4-bb71-7671b043af76") as case:
            # Check Express Mode > modify Parameters > Life > [+] ...

            # Life > Click [+] button x 5 times
            particle_designer_page.express_mode.click_Life_plus_btn(times=5)

            # Get Life value
            current_value = particle_designer_page.express_mode.get_Life_value()
            logger(current_value)

            # Verify Life > click [+] button x 5 times
            if current_value == 105000:
                custom_value = True
                logger(default_value)
            else:
                custom_value = False
                logger(default_value)
            case.result = custom_value



        with uuid("3acbf9f0-8500-43ae-a178-cfdce24b83c3") as case:
            # Check Express Mode > modify Parameters > Life > [-] ...

            # Life  > Click [-] button x 5 times
            particle_designer_page.express_mode.click_Life_minus_btn(times=5)

            # Get Life value
            current_value = particle_designer_page.express_mode.get_Life_value()
            logger(current_value)

            # Verify Life > click [-] button x 5 times
            if current_value == 100000:
                custom_value = True
                logger(default_value)
            else:
                custom_value = False
                logger(default_value)
            case.result = custom_value


        with uuid("26b721d2-e747-479d-b8cc-73bb72d36267") as case:
            # Check Express Mode > modify Parameters > Life > Min value...

            # Drag "Life" slider to Min
            particle_designer_page.express_mode.drag_Life_slider(value=0)

            # Get Life value
            current_value = particle_designer_page.express_mode.get_Life_value()
            logger(current_value)

            # Verify Life value
            if current_value == 0:
                min_value = True
            else:
                min_value = False

            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L108_ParticleDesigner(Life_Min).png'
            ground_truth = Ground_Truth_Folder + 'L108_ParticleDesigner(Life_Min).png'
            current_preview = particle_designer_page.snapshot(locator=L.particle_designer.preview_area,
                                                                file_name=image_full_path)
            check_result = particle_designer_page.compare(ground_truth, current_preview)
            case.result = check_result and min_value



        with uuid("e49e1579-401f-4380-9c2e-7ae8eb1673b7") as case:
            # Check Express Mode > modify Parameters > Life > Max value ...


            # Drag "Life" slider to Max
            particle_designer_page.express_mode.drag_Life_slider(value=200000)

            # Get Life value
            current_value = particle_designer_page.express_mode.get_Life_value()
            logger(current_value)

            # Verify Life count
            if current_value == 200000:
                custom_value = True
                logger(default_value)
            else:
                custom_value = False
                logger(default_value)

            case.result = custom_value

        with uuid("1656b4a9-725c-4a41-bef0-0f25dd475d92") as case:
            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L110_ParticleDesigner(Life_Slider_Max).png'
            ground_truth = Ground_Truth_Folder + 'L110_ParticleDesigner(Life_Slider_Max).png'
            current_preview = particle_designer_page.snapshot(locator=L.particle_designer.preview_area,
                                                                file_name=image_full_path)
            check_result = particle_designer_page.compare(ground_truth, current_preview)
            case.result = check_result



    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_7(self):
        with uuid("286ed516-9061-480f-b8b2-d89857c9ac20") as case:
            # Check Express Mode > modify Parameters > Size > Default ...
            # Entry Particle Room
            time.sleep(1)
            main_page.enter_room(5)
            main_page.select_LibraryRoom_category('General')
            time.sleep(1)
            media_room_page.select_media_content('Effect-A')
            # Click "Modify Particle Template"
            time.sleep(1)
            particle_room_page.click_ModifySelectedParticle_btn()
            time.sleep(1)

            # Get Size value
            current_value = particle_designer_page.express_mode.get_Size_value()
            logger(current_value)

            # Verify Size = Default (100000)
            if current_value == 100000:
                default_value = True
                logger(default_value)
            else:
                default_value = False
                logger(default_value)
            case.result = default_value


        with uuid("ebd8e61d-2daa-447f-a047-c0947139bf34") as case:
            # Check Express Mode > modify Parameters > Size > [+] ...

            # Life > Click [+] button x 5 times
            particle_designer_page.express_mode.click_Size_plus_btn(times=5)

            # Get Size value
            current_value = particle_designer_page.express_mode.get_Size_value()
            logger(current_value)

            # Verify Size > click [+] button x 5 times
            if current_value == 105000:
                custom_value = True
                logger(default_value)
            else:
                custom_value = False
                logger(default_value)
            case.result = custom_value



        with uuid("e2767d8c-30a6-487d-84c0-2fe3a8261c0e") as case:
            # Check Express Mode > modify Parameters > Size > [-] ...

            # Life  > Click [-] button x 5 times
            particle_designer_page.express_mode.click_Size_minus_btn(times=5)

            # Get Size value
            current_value = particle_designer_page.express_mode.get_Size_value()
            logger(current_value)

            # Verify Size > click [-] button x 5 times
            if current_value == 100000:
                custom_value = True
                logger(default_value)
            else:
                custom_value = False
                logger(default_value)
            case.result = custom_value

        with uuid("ffbea19f-c772-416e-98c5-defed9b8aa94") as case:
            # Check Express Mode > modify Parameters > Size > Min value...

            # Drag "Size" slider to Min
            particle_designer_page.express_mode.drag_Size_slider(value=0)

            # Get Size value
            current_value = particle_designer_page.express_mode.get_Size_value()
            logger(current_value)

            # Verify Size value
            if current_value == 0:
                min_value = True
            else:
                min_value = False

            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L114_ParticleDesigner(Size_Min).png'
            ground_truth = Ground_Truth_Folder + 'L114_ParticleDesigner(Size_Min).png'
            current_preview = particle_designer_page.snapshot(locator=L.particle_designer.preview_area,
                                                                file_name=image_full_path)
            check_result = particle_designer_page.compare(ground_truth, current_preview)
            case.result = check_result and min_value


        with uuid("e157a7f6-de8e-4526-a208-e084d8dacd7f") as case:
            # Check Express Mode > modify Parameters > Size > Max value ...


            # Drag "Size" slider to Max
            particle_designer_page.express_mode.drag_Size_slider(value=200000)

            # Get Size value
            current_value = particle_designer_page.express_mode.get_Size_value()
            logger(current_value)

            # Verify Size count
            if current_value == 200000:
                custom_value = True
                logger(default_value)
            else:
                custom_value = False
                logger(default_value)

            case.result = custom_value

        with uuid("4711faa8-e16c-414f-a42d-08ecd0d2a206") as case:
            # Max Size count + Verify
            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L116_ParticleDesigner(Size_Slider_Max).png'
            ground_truth = Ground_Truth_Folder + 'L116_ParticleDesigner(Size_Slider_Max).png'
            current_preview = particle_designer_page.snapshot(locator=L.particle_designer.preview_area,
                                                                file_name=image_full_path)
            check_result = particle_designer_page.compare(ground_truth, current_preview)
            case.result = check_result


    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_8(self):
        with uuid("bfcf944b-8fac-4d77-bf6b-5c762c777fc4") as case:
            # Check Express Mode > modify Parameters > Speed > Default ...
            # Entry Particle Room
            time.sleep(1)
            main_page.enter_room(5)
            main_page.select_LibraryRoom_category('General')
            time.sleep(1)
            media_room_page.select_media_content('Effect-A')
            # Click "Modify Particle Template"
            time.sleep(1)
            particle_room_page.click_ModifySelectedParticle_btn()
            time.sleep(1)

            # Get Speed value
            current_value = particle_designer_page.express_mode.get_Speed_value()
            logger(current_value)

            # Verify Speed = Default (100000)
            if current_value == 100000:
                default_value = True
                logger(default_value)
            else:
                default_value = False
                logger(default_value)
            case.result = default_value

        with uuid("d69bcd55-c613-4b00-a029-040e09c7bc0c") as case:
            # Check Express Mode > modify Parameters > Speed > [+] ...

            time.sleep(1)
            # Speed > Click [+] button x 5 times
            particle_designer_page.express_mode.click_Speed_plus_btn(times=5)
            time.sleep(1)

            # Get Speed value
            current_value = particle_designer_page.express_mode.get_Speed_value()
            logger(current_value)

            # Verify Speed > click [+] button x 5 times
            if current_value == 105000:
                custom_value = True
                logger(default_value)
            else:
                custom_value = False
                logger(default_value)
            case.result = custom_value

        with uuid("320edc53-20e1-497f-87d5-8f29502549c2") as case:
            # Check Express Mode > modify Parameters > Speed > [-] ...

            time.sleep(1)
            # Speed  > Click [-] button x 5 times
            particle_designer_page.express_mode.click_Speed_minus_btn(times=5)
            time.sleep(1)

            # Get Speed value
            current_value = particle_designer_page.express_mode.get_Speed_value()
            logger(current_value)

            # Verify Speed > click [-] button x 5 times
            if current_value == 100000:
                custom_value = True
                logger(default_value)
            else:
                custom_value = False
                logger(default_value)
            case.result = custom_value

        with uuid("84b2888b-e66f-47c1-b15e-ef4b0b1cf680") as case:
            # Check Express Mode > modify Parameters > Speed > Min value...

            time.sleep(1)
            # Drag "Speed" slider to Min
            particle_designer_page.express_mode.drag_Speed_slider(value=0)
            time.sleep(1)

            # Get Speed value
            current_value = particle_designer_page.express_mode.get_Speed_value()
            logger(current_value)

            # Verify Speed value
            if current_value == 0:
                min_value = True
            else:
                min_value = False

            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L120_ParticleDesigner(Speed_Min).png'
            ground_truth = Ground_Truth_Folder + 'L120_ParticleDesigner(Speed_Min).png'
            current_preview = particle_designer_page.snapshot(locator=L.particle_designer.preview_area,
                                                                file_name=image_full_path)
            check_result = particle_designer_page.compare(ground_truth, current_preview)
            case.result = check_result and min_value

        with uuid("9af62455-3601-4a53-a5d7-f9b7e0cbfcd5") as case:
            # Check Express Mode > modify Parameters > Speed > Max value ...

            time.sleep(1)
            # Drag "Speed" slider to Max
            particle_designer_page.express_mode.drag_Speed_slider(value=200000)
            time.sleep(1)

            # Get Speed value
            current_value = particle_designer_page.express_mode.get_Speed_value()
            logger(current_value)

            # Verify Speed count
            if current_value == 200000:
                custom_value = True
                logger(default_value)
            else:
                custom_value = False
                logger(default_value)

            case.result = custom_value


        with uuid("19301dfe-a370-445d-8a23-210a91940932") as case:
            # Max Speed count + Verify
            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L22_ParticleDesigner(Speed_Slider_Max).png'
            ground_truth = Ground_Truth_Folder + 'L22_ParticleDesigner(Speed_Slider_Max).png'
            current_preview = particle_designer_page.snapshot(locator=L.particle_designer.preview_area,
                                                                file_name=image_full_path)
            check_result = particle_designer_page.compare(ground_truth, current_preview)
            case.result = check_result



    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_9(self):
        with uuid("dd1b51f1-27c9-4390-81b3-402031356256") as case:
            # Check Express Mode > modify Parameters > Opacity > Default ...
            # Entry Particle Room
            time.sleep(1)
            main_page.enter_room(5)
            # Import Particle Template
            particle_room_page.click_import_particle_objects(Test_Material_Folder + 'Particle_Designer/1.dzp')
            time.sleep(3)
            particle_designer_page.click_OK_onEffectExtractor()
            time.sleep(1)
            media_room_page.select_media_content('T')
            # Click "Modify Particle Template"
            time.sleep(1)
            particle_room_page.click_ModifySelectedParticle_btn()
            time.sleep(1)

            # Maximize Particle Designer window
            particle_designer_page.click_zoom_btn()

            # Get Opacity value
            current_value = particle_designer_page.express_mode.get_Opacity_value()
            logger(current_value)

            # Verify Opacity = Default (100000)
            if current_value == 100000:
                default_value = True
                logger(default_value)
            else:
                default_value = False
                logger(default_value)
            case.result = default_value


        with uuid("543dc7ba-367f-4ecb-bdfa-ae8162adc4e0") as case:
            # Check Express Mode > modify Parameters > Opacity > [+] ...

            time.sleep(1)
            # Opacity > Click [+] button x 5 times
            particle_designer_page.express_mode.click_Opacity_plus_btn(times=5)
            time.sleep(1)

            # Get Opacity value
            current_value = particle_designer_page.express_mode.get_Opacity_value()
            logger(current_value)

            # Verify Opacity > click [+] button x 5 times
            if current_value == 105000:
                custom_value = True
                logger(default_value)
            else:
                custom_value = False
                logger(default_value)
            case.result = custom_value


        with uuid("4d1b742c-7866-4fe9-af10-72e5ee17eb9b") as case:
            # Check Express Mode > modify Parameters > Opacity > [-] ...

            time.sleep(1)
            # Speed  > Click [-] button x 5 times
            particle_designer_page.express_mode.click_Opacity_minus_btn(times=5)
            time.sleep(1)

            # Get Opacity value
            current_value = particle_designer_page.express_mode.get_Opacity_value()
            logger(current_value)

            # Verify Opacity > click [-] button x 5 times
            if current_value == 100000:
                custom_value = True
                logger(default_value)
            else:
                custom_value = False
                logger(default_value)
            case.result = custom_value


        with uuid("92647e8d-71d5-4cb8-b879-e38c55f576cc") as case:
            # Check Express Mode > modify Parameters > Opacity > Min value...

            time.sleep(1)
            # Drag "Opacity" slider to Min
            particle_designer_page.express_mode.drag_Opacity_slider(value=0)
            time.sleep(1)

            # Get Opacity value
            current_value = particle_designer_page.express_mode.get_Opacity_value()
            logger(current_value)

            # Verify Opacity value
            if current_value == 0:
                min_value = True
            else:
                min_value = False

            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L126_ParticleDesigner(Opacity_Min).png'
            ground_truth = Ground_Truth_Folder + 'L126_ParticleDesigner(Opacity_Min).png'
            current_preview = particle_designer_page.snapshot(locator=L.particle_designer.preview_area,
                                                                file_name=image_full_path)
            check_result = particle_designer_page.compare(ground_truth, current_preview)
            case.result = check_result and min_value


        with uuid("21b18a09-3f7f-4632-bdb0-df6eb5b86f24") as case:
            # Check Express Mode > modify Parameters > Opacity > Max value ...


            # Drag "Opacity" slider to Max
            particle_designer_page.express_mode.drag_Opacity_slider(value=200000)

            # Get Opacity value
            current_value = particle_designer_page.express_mode.get_Opacity_value()
            logger(current_value)

            # Verify Opacity count
            if current_value == 200000:
                custom_value = True
                logger(default_value)
            else:
                custom_value = False
                logger(default_value)

            case.result = custom_value


        with uuid("29244b49-873f-44dc-84e6-73ae68ea884c") as case:
            # Max Opacity count + Verify
            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L128_ParticleDesigner(Opacity_Slider_Max).png'
            ground_truth = Ground_Truth_Folder + 'L128_ParticleDesigner(Opacity_Slider_Max).png'
            current_preview = particle_designer_page.snapshot(locator=L.particle_designer.preview_area,
                                                                file_name=image_full_path)
            check_result = particle_designer_page.compare(ground_truth, current_preview)
            case.result = check_result



    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_10(self):
        with uuid("8bc9f1be-9664-46bb-86b0-683ecd3d78da") as case:
            # Undo ...
            # Undo to restore Size = Default
            time.sleep(2)
            main_page.enter_room(5)
            main_page.select_LibraryRoom_category('General')
            time.sleep(1)
            media_room_page.select_media_content('Effect-A')
            # Click "Modify Particle Template"
            time.sleep(1)
            particle_room_page.click_ModifySelectedParticle_btn()

            time.sleep(1)
            # Snapshot Preview of Particle Designer
            before_image1 = particle_designer_page.snapshot(locator=L.particle_designer.preview_area,
                                                                file_name=Auto_Ground_Truth_Folder + 'L255_ParticleDesigner(Size_Slider_BeforeUndo_Default_PreviewCheck).png')
            # Drag Size slider to Max + Snapshot Preview of Particle Designer
            particle_designer_page.express_mode.drag_Size_slider(value=200000)
            time.sleep(1)
            before_image2 = particle_designer_page.snapshot(locator=L.particle_designer.preview_area,
                                                                file_name=Auto_Ground_Truth_Folder + 'L256_ParticleDesigner(Size_Slider_BeforeRedo_Max_PreviewCheck).png')

            # Undo + Snapshot Preview of Particle Designer
            particle_designer_page.click_undo()
            time.sleep(1)
            after_image1 = particle_designer_page.snapshot(locator=L.particle_designer.preview_area,
                                                                file_name=Auto_Ground_Truth_Folder + 'L255_ParticleDesigner(Size_Slider_Undo_Default_PreviewCheck).png')

            case.result = before_image1 and after_image1

        with uuid("2d9088e6-d00e-4f73-bbd6-53ea121be1df") as case:
            # Redo...

            # Redo to Size slider to Max
            particle_designer_page.click_redo()
            time.sleep(1)
            # Snapshot Preview of Particle Designer
            after_image2 = particle_designer_page.snapshot(locator=L.particle_designer.preview_area,
                                                                file_name=Auto_Ground_Truth_Folder + 'L256_ParticleDesigner(Size_Slider_Redo_Max_PreviewCheck).png')
            case.result = before_image2 and after_image2