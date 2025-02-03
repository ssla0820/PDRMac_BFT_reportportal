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
        main_page.start_app()
        time.sleep(DELAY_TIME * 3)
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
    def test_1_1_1(self):
        with uuid('3d2de55c-22e5-47a3-8118-b11bca4f87b5') as case:
            # 1. General
            # 1.1. Entry
            # 1.1.1. Import media > Download content from DZ/CL cloud > PiP Room
            # download pip objects window pops up
            main_page.enter_room(4)
            pip_room_page.exist_click(L.pip_room.btn_import_media)
            pip_room_page.exist_click(L.pip_room.btn_download_from_DZ_cloud)
            time.sleep(DELAY_TIME)

            check_result = download_from_cl_dz_page.has_window('PiP Objects')
            case.result = check_result

            main_page.press_esc_key()

        with uuid('2a5bdd26-6515-4546-be2f-687f9839b899') as case:
            # 1.1. Entry
            # 1.1.1. Import media > Download content from DZ/CL cloud > Particle Room
            # download particle objects window pops up
            main_page.enter_room(5)
            particle_room_page.exist_click(L.particle_room.btn_import_media)
            particle_room_page.exist_click(L.particle_room.btn_download_from_DZ_cloud)
            time.sleep(DELAY_TIME)

            check_result = download_from_cl_dz_page.has_window('Particle Objects')
            case.result = check_result

            main_page.press_esc_key()

        with uuid('01c637d4-d519-4f30-b0a0-78da0155ae25') as case:
            # 1.1. Entry
            # 1.1.1. Import media > Download content from DZ/CL cloud > Title Room
            # download title templates window pops up
            main_page.enter_room(1)
            title_room_page.exist_click(L.title_room.btn_import_media)
            title_room_page.exist_click(L.title_room.btn_download_from_DZ_cloud)
            time.sleep(DELAY_TIME)

            check_result = download_from_cl_dz_page.has_window('Title Templates')
            case.result = check_result

            main_page.press_esc_key()

        with uuid('3576e9ef-7b41-49ed-a088-d4f436aaab05') as case:
            # 1.1. Entry
            # 1.1.1. Import media > Download content from DZ/CL cloud > Transition Room
            # download transition templates window pops up
            main_page.enter_room(2)
            transition_room_page.exist_click(L.transition_room.btn_import_media)
            transition_room_page.exist_click(L.transition_room.btn_download_from_DZ_cloud)
            time.sleep(DELAY_TIME)

            check_result = download_from_cl_dz_page.has_window('Transition Templates')
            case.result = check_result

            main_page.press_esc_key()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid('22725be6-37fe-435e-ba80-f3b5f32cbd21') as case:
            # 2. PiP Room
            # 2.1. General Function
            # 2.1.1.Caption bar > Caption name
            # show "Download PiP Objects"
            main_page.enter_room(4)
            pip_room_page.exist_click(L.pip_room.btn_import_media)
            pip_room_page.exist_click(L.pip_room.btn_download_from_DZ_cloud)
            time.sleep(DELAY_TIME * 2)

            check_result = download_from_cl_dz_page.has_window('PiP Objects')
            case.result = check_result

            # waiting for CL cloud enable
            item = download_from_cl_dz_page.exist(L.download_from_cl_dz.cloud)
            # wait item [status: ready]
            for x in range(100):
                if item.AXEnabled:
                    logger('break')
                    break
                if x == 99:
                    logger('Tab cannot active [Time out]')
                    raise Exception
                time.sleep(DELAY_TIME)

        with uuid('e042b2df-9e1c-4088-84ae-6fc3f845bc9d') as case:
            # 2.2. My CyberLink Cloud
            # 2.2.1. Select all/Deselect all > Button icon > Select all
            # Default icon with "tick"
            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_2_1_1.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_2_1_1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=L.download_from_cl_dz.select_deselect_all, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('86579022-99e9-4525-82aa-42c19b3277e6') as case:
            # 2.2. My CyberLink Cloud
            # 2.2.1. Select all/Deselect all > Button icon > Deselect all
            # the icon with "X"
            download_from_cl_dz_page.tap_select_deselect_all()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_2_1_2.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_2_1_2.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=L.download_from_cl_dz.select_deselect_all, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('4646fe30-2e8e-4c9b-87c2-7f1939d604b8') as case:
            # 2.2. My CyberLink Cloud
            # 2.2.1. Select all/Deselect all
            # select/deselect all objects
            download_from_cl_dz_page.tap_select_deselect_all()
            time.sleep(DELAY_TIME)
            check_result_1 = download_from_cl_dz_page.is_selected_templates(4)

            download_from_cl_dz_page.tap_select_deselect_all()
            time.sleep(DELAY_TIME)
            check_result_2 = download_from_cl_dz_page.is_selected_templates(4)

            case.result = check_result_1 ^ check_result_2

            download_from_cl_dz_page.tap_select_deselect_all()

        with uuid('a5ba2577-4e32-457c-bb79-d2f5e5b64a8e') as case:
            # 2.2. My CyberLink Cloud
            # 2.2.3. Search > Search the library
            # search results match the search or display "no templates matched the search"
            download_from_cl_dz_page.set_search_text('zzz')

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_2_3_1.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_2_3_1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)
            check_result_1 = download_from_cl_dz_page.compare(ground_truth, current_preview)

            download_from_cl_dz_page.tap_clear_search_button()
            download_from_cl_dz_page.set_search_text('3')

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_2_3_2.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_2_3_2.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)
            check_result_2 = download_from_cl_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

            download_from_cl_dz_page.tap_clear_search_button()

        with uuid('93f0fd82-8877-4590-8501-8ae204802aa8') as case:
            # 2.2. My CyberLink Cloud
            # 2.2.4. Library menu > Sort By > Name
            # sort by name
            download_from_cl_dz_page.apply_sory_by_name()

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_2_4_1.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_2_4_1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('8b170dd0-d399-429c-bfb0-ba877728565a') as case:
            # 2.2. My CyberLink Cloud
            # 2.2.4. Library menu > Sort By > Upload Date (Default)
            # sort by upload date
            download_from_cl_dz_page.apply_sory_by_upload_date()

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_2_4_2.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_2_4_2.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('d3161545-1e44-41cc-9dda-d541d17646d3') as case:
            # 2.2. My CyberLink Cloud
            # 2.2.4. Library menu > Icons size > Extra Large Icons
            # show as extra large icons
            download_from_cl_dz_page.apply_show_extra_large_icons()

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_2_4_3.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_2_4_3.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('2c3d4d03-f18e-43b5-a762-eca27a4856f9') as case:
            # 2.2. My CyberLink Cloud
            # 2.2.4. Library menu > Icons size > Large Icons
            # show as large icons
            download_from_cl_dz_page.apply_show_large_icons()

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_2_4_4.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_2_4_4.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('63c6b595-2c6d-468f-b9a2-dfa159d6799b') as case:
            # 2.2. My CyberLink Cloud
            # 2.2.4. Library menu > icons size > Small Icons
            # show as small icons
            download_from_cl_dz_page.apply_show_small_icons()

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_2_4_6.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_2_4_6.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('5cdd6193-04ab-493e-bd32-7b4f00d2a8b2') as case:
            # 2.2. My CyberLink Cloud
            # 2.2.4. Library menu > Icons size > Details
            # show as details
            download_from_cl_dz_page.apply_show_details()

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_2_4_7.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_2_4_7.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.detail_view, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('3fe5fbc3-5b60-428a-a8e1-1b5904e25217') as case:
            # 2.2. My CyberLink Cloud
            # 2.2.4. Library menu > icons size > Medium Icons (Default)
            # show as medium icons
            download_from_cl_dz_page.apply_show_medium_icons()

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_2_4_5.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_2_4_5.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('f1cbd0ea-3250-4a25-b0ea-e96462a71a39') as case:
            # 2.2. My CyberLink Cloud
            # 2.2.5. Delete selected templates
            # 1. if no template is selected, the button is disabled
            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_2_5_1.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_2_5_1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=L.download_from_cl_dz.delete, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        # with uuid('f60a5db8-9e66-45a2-8caa-34c58033b003') as case:
            # 2.2. My CyberLink Cloud
            # 2.2.5. Delete selected templates
            # 2. "Are you sure..." warning msg pops up & delete correctly
            # download_from_cl_dz_page.select_template('pip')
            # download_from_cl_dz_page.tap_delete_button()
            #
            # image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_2_5_2.png'
            # ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_2_5_2.png'
            # current_preview = download_from_cl_dz_page.snapshot(
            #     locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)
            #
            # check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            # case.result = None

        with uuid('26f219d3-c675-4c86-8f9d-24c7e6d46304') as case:
            # 2.2. My CyberLink Cloud
            # 2.2.6. Download
            # 1. if no template is selected, the button is disabled
            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_2_6_1.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_2_6_1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=L.download_from_cl_dz.download, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('1e17c1af-7556-417b-afec-a1f448332a2e') as case:
            # 2.2. My CyberLink Cloud
            # 2.2.7. Information > # template(s) selected
            # the # should sync with the selected template(s)
            download_from_cl_dz_page.tap_select_deselect_all()
            time.sleep(DELAY_TIME)

            check_result = download_from_cl_dz_page.is_selected_templates(4)
            case.result = check_result

        with uuid('15e5a39e-01c7-488b-af33-c92d2f6a3d55') as case:
            # 2.2. My CyberLink Cloud
            # 2.2.8. Template > Aspect ratio
            # thumbnail show as 16:9 aspect ratio
            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_2_8_1.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_2_8_1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('c4495889-942f-460f-95b3-7c24f5cfcda7') as case:
            # 2.2. My CyberLink Cloud
            # 2.2.8. Template > Thumbnail
            # show a computer icon at the button right corner if the template is downloaded
            # download_from_cl_dz_page.select_template('01-PiPObject')
            download_from_cl_dz_page.tap_download()
            time.sleep(DELAY_TIME * 6)

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_2_8_2.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_2_8_2.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('9d53a62e-0dae-4225-9b00-f342766b9dd7') as case:
            # 2.3. My DirectorZone
            # 2.3.1. Log in dialog > Yes
            # show templates on DZ
            download_from_cl_dz_page.switch_tab('DZ')
            download_from_cl_dz_page.signin_dz()
            # if download_from_cl_dz_page.exist(L.pip_room.cyberlink_power_director.msg):
            #     download_from_cl_dz_page.exist_click(L.pip_room.cyberlink_power_director.yes)

            # switch to (My Director Zone) tab
            item = download_from_cl_dz_page.exist(L.download_from_cl_dz.dz)
            # wait item [status: ready]
            for x in range(100):
                if item.AXEnabled:
                    logger('break')
                    break
                if x == 99:
                    logger('Tab cannot active [Time out]')
                    raise Exception
                time.sleep(DELAY_TIME)
                check_result = item

            case.result = check_result

        with uuid('36bbd8fb-3c54-432c-8f19-6b11b7c48e8b') as case:
            # 2.3. My DirectorZone
            # 2.3.2. Select all/Deselect all > Button icon > Select all
            # default icon with "tick"
            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_3_2_1.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_3_2_1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=L.download_from_cl_dz.select_deselect_all, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('fcf4f558-dbd7-4ea2-a464-e22be1828e8f') as case:
            # 2.3. My DirectorZone
            # 2.3.2. Select all/Deselect all > Button icon > Deselect all
            # the icon with "X"
            download_from_cl_dz_page.tap_select_deselect_all()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_3_2_2.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_3_2_2.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=L.download_from_cl_dz.select_deselect_all, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('80bc52ed-64d1-455d-ad9e-2f357016269b') as case:
            # 2.3. My DirectorZone
            # 2.3.2. Select all/Deselect all
            # select/deselect all objects
            download_from_cl_dz_page.tap_select_deselect_all()
            time.sleep(DELAY_TIME)
            check_result_1 = download_from_cl_dz_page.is_selected_templates(4)

            download_from_cl_dz_page.tap_select_deselect_all()
            time.sleep(DELAY_TIME)
            check_result_2 = download_from_cl_dz_page.is_selected_templates(4)

            case.result = check_result_1 ^ check_result_2

            download_from_cl_dz_page.tap_select_deselect_all()

        with uuid('61aee676-e76e-4fe0-97b4-d503cdd99720') as case:
            # 2.3. My DirectorZone
            # 2.3.3. Category > My Uploads (Default)
            # show uploaded templates
            download_from_cl_dz_page.select_category(1)

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_3_3_1.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_3_3_1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('36cb08a4-383d-4e19-8542-9f75ff7c3f20') as case:
            # 2.3. My DirectorZone
            # 2.3.3. Category > Download History
            # show downloaded from DZ web page & My DZ history
            download_from_cl_dz_page.select_category(2)

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_3_3_2.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_3_3_2.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('b22850fb-2c2f-4824-8d76-fcabd8c15af7') as case:
            # 2.3. My DirectorZone
            # 2.3.3. Category > My Favorites
            # show templates added to My Favorite on the web page
            download_from_cl_dz_page.select_category(3)

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_3_3_3.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_3_3_3.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('8f5fe677-76b0-4733-b38c-47b4e203ef7c') as case:
            # 2.3. My DirectorZone
            # 2.3.5. Search > Search the library
            # search results match the search or display "No templates matched the search"
            download_from_cl_dz_page.set_search_text('zzz')

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_3_5_1.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_3_5_1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)
            check_result_1 = download_from_cl_dz_page.compare(ground_truth, current_preview)

            download_from_cl_dz_page.tap_clear_search_button()
            download_from_cl_dz_page.set_search_text('3')

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_3_5_2.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_3_5_2.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)
            check_result_2 = download_from_cl_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

            download_from_cl_dz_page.tap_clear_search_button()

        with uuid('bbd520f1-7077-4b48-966e-5a19407d9bb9') as case:
            # 2.3. My DirectorZone
            # 2.3.6. Library menu > Sort By > Name
            # sort by name
            download_from_cl_dz_page.apply_sory_by_name()

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_3_6_1.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_3_6_1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('a4814e87-52d3-49b6-bfcb-a084841ae89e') as case:
            # 2.3. My DirectorZone
            # 2.3.6. Library menu > Sort By > Upload Date (Default)
            # sort by upload date
            download_from_cl_dz_page.apply_sory_by_upload_date()

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_3_6_2.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_3_6_2.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('7e87344f-d96e-4fbb-bbe7-dee25cf603cb') as case:
            # 2.3. My DirectorZone
            # 2.3.6. Library menu > Icons size > Extra Large Icons
            # show as extra large icons
            download_from_cl_dz_page.apply_show_extra_large_icons()

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_3_6_3.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_3_6_3.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('6e9de6a8-14d0-47b5-9c8a-71d8dc7e85cd') as case:
            # 2.3. My DirectorZone
            # 2.3.6. Library menu > Icons size > Large Icons
            # show as large icons
            download_from_cl_dz_page.apply_show_large_icons()

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_3_6_4.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_3_6_4.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('40e12db1-f9ba-4271-9309-45a967d62082') as case:
            # 2.3. My DirectorZone
            # 2.3.6. Library menu > Icons size > Small Icons
            # show as small icons
            download_from_cl_dz_page.apply_show_small_icons()

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_3_6_6.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_3_6_6.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('fec61328-7aee-45cc-af03-9f6cf7406d4b') as case:
            # 2.3. My DirectorZone
            # 2.3.6. Library menu > Icons size > Details
            # show as details
            download_from_cl_dz_page.apply_show_details()

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_3_6_7.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_3_6_7.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.detail_view, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('3e3e35a5-051e-442a-9ecf-f4a1c37951dd') as case:
            # 2.3. My DirectorZone
            # 2.3.6. Library menu > Icons size > Medium Icons (Default)
            # show as medium icons
            download_from_cl_dz_page.apply_show_medium_icons()

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_3_6_5.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_3_6_5.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('ec639783-562b-4f29-b606-0c801267aa6c') as case:
            # 2.3. My DirectorZone
            # 2.3.7. Download
            # 1. if no template is selected, the button is disabled
            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_3_7_1.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_3_7_1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=L.download_from_cl_dz.download, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('2ba35b34-aa25-4e2d-8ee2-abdcaf65bb8d') as case:
            # 2.3. My DirectorZone
            # 2.3.8. Information > # template(s) selected
            # the # should sync with the selected template(s)
            download_from_cl_dz_page.tap_select_deselect_all()
            time.sleep(DELAY_TIME)

            check_result = download_from_cl_dz_page.is_selected_templates(7)
            case.result = check_result

        with uuid('1536d5f5-c150-45da-af0a-5c921eb6b5e3') as case:
            # 2.3. My DirectorZone
            # 2.3.9. Template > Aspect ratio
            # thumbnail show as 16:9 aspect ratio
            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_3_9_1.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_3_9_1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('64effb14-2b59-4fc5-af9b-ee2d7236c5fb') as case:
            # 2.3. My DirectorZone
            # 2.3.9. Template > Thumbnail
            # show a computer icon at the button right corner if the template is downloaded
            download_from_cl_dz_page.tap_select_deselect_all()
            time.sleep(DELAY_TIME)
            download_from_cl_dz_page.select_template('01-PiPObject')
            download_from_cl_dz_page.tap_download()
            time.sleep(DELAY_TIME * 3)

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_2_3_9_2.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_2_3_9_2.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('17d8ef77-709d-46d9-b547-01d4201c9380') as case:
            # 2.1. General Function
            # 2.1.1.Caption bar > X (Close)
            # close the window
            download_from_cl_dz_page.tap_close_button()
            download_from_cl_dz_page.click_OK_onEffectExtractor()
            time.sleep(DELAY_TIME)

            check_result = download_from_cl_dz_page.has_window('PiP Objects')
            if not check_result:
                case.result = True
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        with uuid('54dad148-53a7-4709-8773-d6af343bd6bc') as case:
            # 3. Particle Room
            # 3.1. General Function
            # 3.1.1. Caption bar > Caption name
            # show "Download Particle Objects"
            main_page.enter_room(5)
            particle_room_page.exist_click(L.particle_room.btn_import_media)
            particle_room_page.exist_click(L.particle_room.btn_download_from_DZ_cloud)
            time.sleep(DELAY_TIME)

            check_result = download_from_cl_dz_page.has_window('Particle Objects')
            case.result = check_result

            # waiting for CL cloud enable
            item = download_from_cl_dz_page.exist(L.download_from_cl_dz.cloud)
            # wait item [status: ready]
            for x in range(100):
                if item.AXEnabled:
                    logger('break')
                    break
                if x == 99:
                    logger('Tab cannot active [Time out]')
                    raise Exception
                time.sleep(DELAY_TIME)

        with uuid('e3e2416d-93fb-4370-8757-a71c4c87a24d') as case:
            # 3.2. My CyberLink Cloud
            # 3.2.1. Select all/Deselect all
            # select/deselect all objects
            download_from_cl_dz_page.tap_select_deselect_all()
            time.sleep(DELAY_TIME)
            check_result_1 = download_from_cl_dz_page.is_selected_templates(3)

            download_from_cl_dz_page.tap_select_deselect_all()
            time.sleep(DELAY_TIME)
            check_result_2 = download_from_cl_dz_page.is_selected_templates(3)

            case.result = check_result_1 ^ check_result_2

            download_from_cl_dz_page.tap_select_deselect_all()

        with uuid('22571313-6556-40c6-9447-b2b8849e406e') as case:
            # 3.2. My CyberLink Cloud
            # 3.2.3. Search > Search the library
            # search results match the search or display "No templates matched the search"
            download_from_cl_dz_page.set_search_text('zzz')

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_3_2_3_1.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_3_2_3_1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)
            check_result_1 = download_from_cl_dz_page.compare(ground_truth, current_preview)

            download_from_cl_dz_page.tap_clear_search_button()
            download_from_cl_dz_page.set_search_text('3')

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_3_2_3_2.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_3_2_3_2.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)
            check_result_2 = download_from_cl_dz_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

            download_from_cl_dz_page.tap_clear_search_button()

        with uuid('8899f3e7-932a-47b7-b33e-b6947a613b1c') as case:
            # 3.2. My CyberLink Cloud
            # 3.2.5. Delete selected templates
            # 1. if no template is selected, the button is disabled
            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_3_2_5_1.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_3_2_5_1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=L.download_from_cl_dz.delete, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        # with uuid('8e90af79-a327-41fa-857f-69d91211e736') as case:
            # 3.2. My CyberLink Cloud
            # 3.2.5. Delete selected templates
            # 2. "Are you sure..." warning msg pops up & delete correctly
            # download_from_cl_dz_page.select_template('pip')
            # download_from_cl_dz_page.tap_delete_button()
            #
            # image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_3_2_5_2.png'
            # ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_3_2_5_2.png'
            # current_preview = download_from_cl_dz_page.snapshot(
            #     locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)
            #
            # check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            # case.result = None

        with uuid('eb6072ae-dff1-4879-aca6-fc626be61652') as case:
            # 3.2. My CyberLink Cloud
            # 3.2.6. Download
            # 1. if no template is selected, the button is disabled
            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_3_2_6_1.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_3_2_6_1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=L.download_from_cl_dz.download, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('f85b6d3e-03a7-429d-ba4a-f380b5a9ad4a') as case:
            # 3.2. My CyberLink Cloud
            # 3.2.6. Download
            # 3. icon & location will change to "This computer" after the download is complete"
            download_from_cl_dz_page.select_template('01-ParticleEffect')
            download_from_cl_dz_page.tap_download()
            time.sleep(DELAY_TIME * 6)

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_3_2_6_2.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_3_2_6_2.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('cdd9a965-022c-46e0-aea0-319335336399') as case:
            # 3.3. My DirectorZone
            # 3.3.1. Log in dialog > Yes
            # show templates on DZ
            download_from_cl_dz_page.switch_tab('DZ')
            download_from_cl_dz_page.signin_dz()
            # if download_from_cl_dz_page.exist(L.pip_room.cyberlink_power_director.msg):
            #     download_from_cl_dz_page.exist_click(L.pip_room.cyberlink_power_director.yes)

            # switch to (My Director Zone) tab
            item = download_from_cl_dz_page.exist(L.download_from_cl_dz.dz)
            # wait item [status: ready]
            for x in range(100):
                if item.AXEnabled:
                    logger('break')
                    break
                if x == 99:
                    logger('Tab cannot active [Time out]')
                    raise Exception
                time.sleep(DELAY_TIME)
                check_result = item

            case.result = check_result

        with uuid('ff2f4105-140e-4649-863e-892c0c48e2f9') as case:
            # 3.3. My DirectorZone
            # 3.3.7. Download
            # 1. if no template is selected, the button is disabled
            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_3_3_7_1.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_3_3_7_1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=L.download_from_cl_dz.download, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('38d26207-c78e-4324-a565-03398f8a8de9') as case:
            # 3.3. My DirectorZone
            # 3.3.7. Download
            # 3. icon & location will change to "This computer" after the download is complete
            download_from_cl_dz_page.select_template('02-ParticleEffect')
            download_from_cl_dz_page.tap_download()
            time.sleep(DELAY_TIME * 3)
            main_page.move_mouse_to_0_0()

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_3_3_7_2.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_3_3_7_2.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('d6830975-c1bb-4f8e-bd64-bb045af5b944') as case:
            # 3.3. My DirectorZone
            # 3.3.8. Information > # template(s) selected
            # the # should sync with the selected template(s)
            download_from_cl_dz_page.tap_select_deselect_all()
            time.sleep(DELAY_TIME)

            check_result = download_from_cl_dz_page.is_selected_templates(3)
            case.result = check_result

        with uuid('41df3cd9-079b-45af-96ea-6110b0afcab0') as case:
            # 3.1. General Function
            # 3.1.1. Caption bar > X (Close)
            # close the window
            download_from_cl_dz_page.tap_close_button()
            time.sleep(DELAY_TIME)

            check_result = download_from_cl_dz_page.has_window('Particle Objects')
            if not check_result:
                case.result = True
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        with uuid('20332285-d3dd-47f1-9718-397640eac6ca') as case:
            # 4. Title Room
            # 4.1. General Function
            # 4.1.1. Caption bar > Caption name
            # show "Download Title templates"
            main_page.enter_room(1)
            title_room_page.exist_click(L.title_room.btn_import_media)
            title_room_page.exist_click(L.title_room.btn_download_from_DZ_cloud)
            time.sleep(DELAY_TIME)

            check_result = download_from_cl_dz_page.has_window('Title Templates')
            case.result = check_result

            # waiting for CL cloud enable
            item = download_from_cl_dz_page.exist(L.download_from_cl_dz.cloud)
            # wait item [status: ready]
            for x in range(100):
                if item.AXEnabled:
                    logger('break')
                    break
                if x == 99:
                    logger('Tab cannot active [Time out]')
                    raise Exception
                time.sleep(DELAY_TIME)

        with uuid('e1f3fe99-48d4-403e-9cda-7b06e898ffbb') as case:
            # 4.2. My CyberLink Cloud
            # 4.2.6. Download
            # 1. if no template is selected, the button is disabled
            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_4_2_6_1.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_4_2_6_1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=L.download_from_cl_dz.download, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('2d370207-d3f5-434f-ad5b-7f448a7b07af') as case:
            # 4.2. My CyberLink Cloud
            # 4.2.6. Download
            # 3. icon & location will change to "This Computer" after the download is complete
            download_from_cl_dz_page.select_template('01-MyTitle')
            download_from_cl_dz_page.tap_download()
            time.sleep(DELAY_TIME * 6)

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_4_2_6_2.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_4_2_6_2.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('cfae721f-e506-4c8b-8c2f-61823cadb5c4') as case:
            # 4.3. My DirectorZone
            # 4.3.1. Log in dialog > Yes
            # show templates on Dz
            download_from_cl_dz_page.switch_tab('DZ')
            download_from_cl_dz_page.signin_dz()
            # if download_from_cl_dz_page.exist(L.pip_room.cyberlink_power_director.msg):
            #     download_from_cl_dz_page.exist_click(L.pip_room.cyberlink_power_director.yes)

            # switch to (My Director Zone) tab
            item = download_from_cl_dz_page.exist(L.download_from_cl_dz.dz)
            # wait item [status: ready]
            for x in range(100):
                if item.AXEnabled:
                    logger('break')
                    break
                if x == 99:
                    logger('Tab cannot active [Time out]')
                    raise Exception
                time.sleep(DELAY_TIME)
                check_result = item

            case.result = check_result

        with uuid('aee194b9-e89c-4b84-9556-dc754d48a38c') as case:
            # 4.3. My DirectorZone
            # 4.3.7. Download
            # 1. if no template is selected, the button is disabled
            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_4_3_7_1.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_4_3_7_1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=L.download_from_cl_dz.download, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('223a375b-6dd7-45c8-961a-5e9b3dc6445d') as case:
            # 4.3. My DirectorZone
            # 4.3.7. Download
            # 3. icon & location will change to "This Computer" after the download is complete
            download_from_cl_dz_page.select_template('03-MyTitle')
            download_from_cl_dz_page.tap_download()
            time.sleep(DELAY_TIME * 6)

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_4_3_7_2.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_4_3_7_2.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('15fe531a-34c3-4492-8252-21985fbea98b') as case:
            # 4.3. My DirectorZone
            # 4.3.8. Information > # template(s) selected
            # the # should sync with the selected template(s)
            download_from_cl_dz_page.tap_select_deselect_all()
            time.sleep(DELAY_TIME)
            check_result = download_from_cl_dz_page.is_selected_templates(3)
            case.result = check_result

        with uuid('69adf255-bd38-4aad-a48d-9187433b7321') as case:
            # 4.1. General Function
            # 4.1.1. Caption bar > X (Close)
            # close the window
            download_from_cl_dz_page.tap_close_button()
            time.sleep(DELAY_TIME)

            check_result = download_from_cl_dz_page.has_window('Title Templates')
            if not check_result:
                case.result = True
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        with uuid('99ca1ad9-d428-47b8-ad86-a5e9c530ea59') as case:
            # 5. Transition Room
            # 5.1. General Function
            # 5.1.1. Caption bar > Caption name
            # show "Download Transition templates"
            main_page.enter_room(2)
            transition_room_page.exist_click(L.transition_room.btn_import_media)
            transition_room_page.exist_click(L.transition_room.btn_download_from_DZ_cloud)
            time.sleep(DELAY_TIME)

            check_result = download_from_cl_dz_page.has_window('Transition Templates')
            case.result = check_result

            # waiting for CL cloud enable
            item = download_from_cl_dz_page.exist(L.download_from_cl_dz.cloud)
            # wait item [status: ready]
            for x in range(100):
                if item.AXEnabled:
                    logger('break')
                    break
                if x == 99:
                    logger('Tab cannot active [Time out]')
                    raise Exception
                time.sleep(DELAY_TIME)

        with uuid('0823ab04-abf3-409b-9679-15f09c8360ed') as case:
            # 5.2. My CyberLink Cloud
            # 5.2.6. Download
            # 1. if no template is selected, the button is disabled
            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_5_2_6_1.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_5_2_6_1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=L.download_from_cl_dz.download, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('979e11be-6740-4df3-8525-8fc6499d5e19') as case:
            # 5.2. My CyberLink Cloud
            # 5.2.6. Download
            # 3. icon & location will change to "This Computer" after the download is complete
            download_from_cl_dz_page.select_template('Heart')
            download_from_cl_dz_page.tap_download()
            time.sleep(DELAY_TIME * 6)

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_5_2_6_2.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_5_2_6_2.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('39b5a86a-830d-46cb-9d52-2d576dd607b0') as case:
            # 5.3. My DirectorZone
            # 5.3.1. Log in dialog > Yes
            # show templates on Dz
            download_from_cl_dz_page.switch_tab('DZ')
            download_from_cl_dz_page.signin_dz()
            # if download_from_cl_dz_page.exist(L.pip_room.cyberlink_power_director.msg):
            #     download_from_cl_dz_page.exist_click(L.pip_room.cyberlink_power_director.yes)

            # switch to (My Director Zone) tab
            item = download_from_cl_dz_page.exist(L.download_from_cl_dz.dz)
            # wait item [status: ready]
            for x in range(100):
                if item.AXEnabled:
                    logger('break')
                    break
                if x == 99:
                    logger('Tab cannot active [Time out]')
                    raise Exception
                time.sleep(DELAY_TIME)
                check_result = item

            case.result = check_result

        with uuid('1a33baa3-49b3-437a-ab11-b8169927ba4d') as case:
            # 5.3. My DirectorZone
            # 5.3.7. Download
            # 1. if no template is selected, the button is disabled
            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_5_3_7_1.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_5_3_7_1.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=L.download_from_cl_dz.download, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('604a30ea-43e4-49ba-bebf-27ec0bf7844f') as case:
            # 5.3. My DirectorZone
            # 5.3.7. Download
            # 3. icon & location will change to "This Computer" after the download is complete
            download_from_cl_dz_page.select_template('Finish')
            download_from_cl_dz_page.tap_download()
            time.sleep(DELAY_TIME * 6)

            image_full_path = Auto_Ground_Truth_Folder + 'download_content_from_dzcl_5_3_7_2.png'
            ground_truth = Ground_Truth_Folder + 'download_content_from_dzcl_5_3_7_2.png'
            current_preview = download_from_cl_dz_page.snapshot(
                locator=download_from_cl_dz_page.area.download_from_cl_dz.content.library, file_name=image_full_path)

            check_result = download_from_cl_dz_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('6f100824-8715-459b-b285-1ea7cc466f33') as case:
            # 5.1. General Function
            # 5.1.1. Caption bar > X (Close)
            # close the window
            download_from_cl_dz_page.tap_close_button()
            time.sleep(DELAY_TIME)

            check_result = download_from_cl_dz_page.has_window('Transition Templates')
            if not check_result:
                case.result = True
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    ee2dd1c2-f88e-481c-aaf9-58c0c5b4c1a9
                    1160e20f-527a-4ae8-bd07-d8f48a6b8ecf
                    7e461349-9bb6-4a6a-ad96-31b45f5badf9
                    7f58b73f-fea5-4db2-bd08-07fa84aa7543
                    7d73320c-b875-465a-90fe-5919759f56d4
                    f60a5db8-9e66-45a2-8caa-34c58033b003
                    f980e6d6-cc90-4cc4-988c-45d0d2b785e1
                    da595e36-8ced-4d18-a81b-c38186583670
                    feb28a18-b2d0-4b7e-9db8-d2f46c43e879
                    6ef0fcca-0c39-467e-81c3-35e3556b2a83
                    ee232b6e-4302-4b61-89c2-15a0f568e3b9
                    ce377144-68f1-4fcb-8dfc-8da77e24b2c5
                    32c44be6-0cce-46fa-99f9-ec25bcc262fd
                    2d6388a6-2fc6-4df8-a1e4-6991b059ad50
                    c157aefa-aa71-46fd-8c09-dca48d1cb7ce
                    63c65634-c9c2-4237-9a52-6b5feca52681
                    250807cc-9ccb-44d5-b0bb-7268e40b567e
                    3a785975-0eb4-45a6-9fbf-949538dfa75a
                    75c46807-c000-4c06-a242-02f576ed7d7f
                    56c28272-20f5-4d37-a995-3ed53c0ca88d
                    c7fe9fa7-3f17-4fed-804b-6b469ab0c211
                    33635372-f28b-4adc-8ad9-b49253b1498a
                    08b63faf-20b3-4e84-8219-2fb76d472fc7
                    225365c3-941a-4ddd-ad2d-4dd169c03947
                    56e8c707-ace1-4e4a-a345-65d6f2540b20
                    b78cc6d2-a7ca-4f72-b298-ea69c99850da
                    4434ab87-d854-4def-bf08-320a5e839c2d
                    50fc9ee2-616b-40b1-be3e-329f4e8d5ea0
                    11d753c9-6a6f-49fc-a425-c26f5dd5e5ea
                    31961f1e-de1a-401f-84c6-f084c0e0f15b
                    8e90af79-a327-41fa-857f-69d91211e736
                    ee35b643-67f2-494d-a120-2bf010adb8e0
                    ca5a768e-643a-44db-845b-26a5e2721bd6
                    9a641189-143b-43af-9ff6-40af92aa41b5
                    0560db4e-cac6-499e-aece-8e458a48ba3e
                    e31655c1-0c3a-4770-8eaa-db1952a31911
                    8c37711e-4632-481b-b904-8dc52dc127e1
                    d8109985-485c-492f-a6ca-86c3dc5f9915
                    cb99f750-4fa8-44b0-a578-c40059cdc764
                    a3d5bd40-6ce9-44c6-803a-d6a7f952ad9a
                    43f94a10-96a2-4e5f-a55b-64abe2d09bf1
                    a616e331-cd4a-4c7d-9718-99cd3c8b26ed
                    823463d1-5c6e-48bc-88d5-bbeb3cd59293
                    2f9ea6a8-9dd0-4b68-9dcc-31458f09e7d1
                    5bad6559-b37d-481a-9196-ffead45d7703
                    633c93e4-a2bf-4083-8aa0-68804b5e7c1f
                    1079f0bb-4384-4dc7-a403-2d1ddd4ec892
                    5cb5abe7-9c6b-4256-9dc9-f3d1f13391ba
                    307f06c2-3f31-4b60-9574-a3f273088401
                    821b9397-dc65-4b01-9dbf-b14a08dd5b09
                    edde102c-e1e8-4f72-807d-93a43162e93c
                    cf780021-2e25-4f63-9310-a0c66ef6b517
                    0a2aef47-40fd-4773-8d67-f847955748a4
                    96eb40f2-1408-4c97-9a9f-435e5fd8bb11
                    1bd97552-b7fb-4a65-961e-dce4979400c4
                    185d9fd4-f8de-438d-ade5-a5422ce61a13
                    3f593f72-0a5a-421e-8fbc-17d0c52f1d1f
                    f9ab6beb-7f17-4ad1-9145-354428295571
                    34250aad-92fc-440e-8c04-322029fb1076
                    c360eab5-6aeb-4c13-ae79-0437138dffa6
                    3502b8ff-56b6-40e5-acdd-3d8a001236ef
                    dd3c6640-adb2-4e2d-aec9-5e6f4b3d4aba
                    d24ffcd8-25fd-473a-bf36-43c2312daa9d
                    a686209e-bc84-4ffa-9e81-acebc2774b4e
                    c52c3290-0d4b-4740-9585-4c0a55ad747d
                    0f8ffd94-bac6-4c4f-b13f-7b69b6ddd621
                    52d2c68d-0178-4e2c-b51e-1fdc90361675
                    2007b1d5-ce2d-4c9a-a3ad-04e9ab223af8
                    7fc7d720-600f-45b2-9d4f-c5026a4cc1eb
                    c6d9b89a-55c1-47ba-8a9f-082f59db98ba
                    bc32b307-94b8-4807-803e-1ba9cde8ad1e
                    b809f337-e512-4cd7-942c-5c9b4ec03fc7
                    9dde1826-f65f-4683-a8b8-21e5a1ff642b
                    0c2ea131-8677-4bb1-9c57-adff617618f0
                    d0894046-b519-45dc-ac28-cdbc332a1495
                    c967da9e-882c-4c97-8958-5a11fdf2ead2
                    b4076249-1426-4fae-8c58-2017a35013fe
                    fe534a8c-d59a-4c16-b9bc-520bb10ffe5a
                    38a07310-5554-4162-b783-7c8b3ade9936
                    e0ced9b2-e685-47a7-b658-3c3aad9dc95e
                    9e571fb1-179a-4c14-9b0f-60263d3a5f69
                    5c8aa945-cea2-4031-87b1-9ad10cf035f7
                    4965c535-ec69-4988-870a-0ea60864c787
                    8abdbcdb-9ab9-42c6-ba01-17b6a2e7d784
                    2bb9784e-75ab-4a1f-aa9b-60d10e205a58
                    9a8da369-1e0b-4534-9944-cc133f229544
                    84a44987-72be-4d83-ae72-38f416f05a87
                    19aea7a0-3831-4651-9e73-307be8344dcc
                    e2390380-189e-44b2-8f90-360fa1bf6cc2
                    1c2d2c2e-eb17-4ac2-a595-c2b0fb005829
                    ddd92b73-85b4-4a33-8670-9179885014c1
                    5e07a078-c94c-4dd0-b2b3-eec0537533e4
                    2f882370-ec03-4570-89b0-b36d35886bd3
                    d4f877a6-7fc8-4af8-979b-f94c7ada99ab
                    4b019419-d40e-40b1-99b8-0f7083b53d58
                    2a535550-2708-4d8f-84b8-cb1f0f619e7a
                    179bacf2-bf49-4bac-8903-0575385b8cd0
                    c399466b-5134-4da9-b91f-d80e4d0af06d
                    6addd687-2d4b-4105-94f4-8bc6145e052a
                    d2616317-9c71-4b17-9ca9-3ad383af1c50
                    1cb5ed30-728e-4929-9f39-8af4caad708d
                    5d8c89e8-740e-465f-8ebe-fbb41e282a8f
                    0b18164a-9bc7-4d9f-a5c6-3c207bd71618
                    9604e368-fd43-4a0f-97d1-8c2f1ae1dfd7
                    716b55b3-4a8b-4b4c-9a86-edd0ea590686
                    c59c2ae6-f2f6-4c67-a490-db965cc63c77
                    fc1f55c5-e200-4ad5-9a79-3517838f326d
                    53c254ed-f363-4592-812d-8bb9028a0087
                    01a65725-6a18-4e2d-9919-8a8d8a199c4f
                    56521b5d-3fac-4966-9908-25e632530132
                    a7738b98-e92e-4668-91e0-06c915753656
                    6cd7671b-2183-4fac-bb54-b486365cad99
                    a07624b2-646b-46b0-ba40-2cadf03dcf18
                    8397e796-4ccc-4048-a1dd-4bfe63c19fc1
                    41d4a14d-16bf-4721-8bbc-666a57abdae5
                    74fcb18e-d9b5-48f3-9fd5-ac80f9a6cbb9
                    3f7d0115-e8db-4cc7-8007-6f35bb2d95b0
                    81e53990-138d-44ec-bce5-224071ea4388
                    fe64b9fd-aa88-4181-8183-c38ff9d38523
                    8c842cf5-6497-4783-b269-a2d0f2d30863
                    6d4cad4b-f9a1-4d43-913f-409b14d6a590
                    775274a5-48d3-4c52-ab9f-686f9d1172d7
                    8d82e86a-868f-4f27-908c-7d13d90354b0
                    f889bddc-2dea-4462-9929-84083bcf94cc
                    da106641-7ad9-4c09-a9c0-0dd364f3fc62
                    ad94ce00-aaa6-48cb-ab10-55a9c79cab52
                    1490b3bd-11a4-443e-b464-e77b43c64beb
                    64d256a7-ec5a-4066-9386-6351d3721faf
                    c2c1c46c-3de0-403e-987b-969741836e6f
                    060f95c3-55ed-4714-9496-8c5d2a3c5148
                    f59e4580-bf79-44c2-8b69-23b5136c4042
                    aa5977de-9887-4c81-b094-221abfe8d4d3
                    366d428b-4f84-4b64-b6bc-9297ccf00f6d
                    99d74887-5eff-4da7-b88c-0fa754e29d2b
                    31d1fbef-0699-4086-ab7f-ade42e2e2dbd
                    36f38602-0547-4d9b-bf5b-51ac81f0a921
                    02dd96f6-c5e5-4262-8ae8-5a96dea882ed
                    bc3ce461-52dc-4210-9028-2009a8ae4ec3
                    d555e4dd-0ec6-48c0-a5b1-031f5e80c7e1
                    ca40f3c5-5126-4b62-ac93-9f521fdb41b0
                    956d00e9-bcff-4175-9c34-84811d745556
                    601fd8e2-75cc-4ff1-a61b-cc2b26665d90
                    b00dde68-b36b-4c2e-813c-f388228cc161
                    b02b9754-50cb-482a-a4ce-b6d18cf65d4c
                    637a4639-0f66-4b35-b723-bd48c095f2e3
                    14a02abf-df92-4ae3-bc92-e7d0b3028059
                    f142a60a-9ad2-46fd-9ab9-1b6a32addf24
                    ebdabdc7-4e3d-472f-9106-3250c1f52350
                    8fbdb4e9-cc5e-4c7a-910f-18ea75e08f1e
                    6e1d0892-501f-436f-8da4-c5819638b419
                    4d625ac8-fb7f-4197-a86e-13e577dce1c3
                    98191665-5469-4d06-9118-87f34e9f9211
                    3e6008e4-c67e-4983-a335-70560ba75693
                    60809f5e-f119-4ec2-b48b-dbe1a070327d
                    fb221d83-80fe-4ae6-86ec-94d3f633bb90
                    e8e376b6-0047-4223-803f-a401c7ee9a72
                    ''') as case:
            case.result = None
            case.fail_log = '*SKIP by AT*'



