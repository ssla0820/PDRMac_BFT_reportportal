import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time, inspect, datetime, pytest, re, configparser
os.chdir(os.path.dirname(__file__))
from types import SimpleNamespace

from ATFramework import MyReport, logger
from ATFramework.drivers.driver_factory import DriverFactory
from pages.page_factory import PageFactory
from configs.app_config import *
# import pages.media_room_page
from pages.locator import locator as L

#for update_report_info
from globals import *



# read PDR cap >>
app = SimpleNamespace(**PDR_cap)
# read PDR cap <<

# create driver & page >>
mac = DriverFactory().get_mac_driver_object('mac', app.app_name, app.app_bundleID, app.app_path)
main_page = PageFactory().get_page_object('main_page', mac)
#base_page = PageFactory().get_page_object('base_page', mac)
media_room_page = PageFactory().get_page_object('media_room_page',mac)
library_preview_page = PageFactory().get_page_object('library_preview_page',mac)
mask_designer_page = PageFactory().get_page_object('mask_designer_page', mac)
effect_room_page = PageFactory().get_page_object('effect_room_page', mac)
pip_room_page = PageFactory().get_page_object('pip_room_page', mac)
particle_room_page = PageFactory().get_page_object('particle_room_page',mac)
title_room_page = PageFactory().get_page_object('title_room_page',mac)
transition_room_page = PageFactory().get_page_object('transition_room_page',mac)
# create driver & page <<Ernesto_MacAT_Trunk

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="Library Tags.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<


# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Library_Tags/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Library_Tags/'
Test_Material_Folder = app.testing_material

#Ground_Truth_Folder = '/Users/clt/Desktop/Ernesto_MacAT/SFT/GroundTruth/Library_Tags/'
#Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Library_Tags/'
#Test_Material_Folder = '/Users/clt/Desktop/Ernesto_MacAT/Material/'

DELAY_TIME = 1


class Test_Library_Tags():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
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
            google_sheet_execution_log_init('Library_Tags')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"mask designer result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
    def test1_1_4_1(self):
        # add new tag input characters
        with uuid("9275d26e-4ef8-4323-992a-2822696f0f56") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = media_room_page.add_new_tag('abcd')
            time.sleep(DELAY_TIME * 4)
            library_result = media_room_page.snapshot(locator=L.media_room.tag_scroll_view_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G4.1.0_AddNewTag.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.1.0_AddNewTag.png',
                                                     library_result)
            case.result = compare_result and current_result

        # delete tag then OK
        with uuid("84a317ce-596f-48d9-bb82-aa550c846e92") as case:
            with uuid("ec458539-e2a8-48b0-a406-2072e0974172") as case:
                time.sleep(DELAY_TIME * 4)
                current_result = media_room_page.delete_tag('abcd')
                time.sleep(DELAY_TIME * 4)
                library_result = media_room_page.snapshot(locator=L.media_room.tag_scroll_view_frame,
                                                          file_name=Auto_Ground_Truth_Folder + 'G4.1.1_DeleteTag.png')
                compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.1.1_DeleteTag.png',
                                                         library_result)
                case.result = compare_result and current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_4_2(self):
        # add new tag relaunch PDR
        with uuid("54ea4f63-d3b0-4fe0-8c96-9b466b3ca69b") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = media_room_page.add_new_tag('abcd')
            main_page.close_app()
            time.sleep(DELAY_TIME * 4)
            main_page.start_app()
            time.sleep(DELAY_TIME * 10)
            library_result = media_room_page.snapshot(locator=L.media_room.tag_scroll_view_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G4.2.0_AddNewTagRelaunchPDR.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.2.0_AddNewTagRelaunchPDR.png',
                                                     library_result)
            case.result = compare_result and current_result

        # open saved project
        with uuid("b8a6bb58-1dc1-40d6-b1c3-91713a734bb6") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.top_menu_bar_file_open_project()
            time.sleep(DELAY_TIME * 4)
            main_page.handle_open_project_dialog(Test_Material_Folder + 'save.pds')
            time.sleep(DELAY_TIME * 4)
            main_page.handle_merge_media_to_current_library_dialog('no')
            time.sleep(DELAY_TIME * 4)
            library_result = media_room_page.snapshot(locator=L.media_room.tag_scroll_view_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G4.2.1_OpenProject.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.2.1_OpenProject.png',
                                                     library_result)
            case.result = compare_result and current_result



    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_4_3(self):
        # effect room default
        with uuid("95741f84-694a-4273-9848-0a1d9b652051") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(3)
            time.sleep(DELAY_TIME * 4)
            library_result = media_room_page.snapshot(locator=L.effect_room.current_tag_amount,
                                                      file_name=Auto_Ground_Truth_Folder + 'G4.3.0_EffectRoomDefault.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.3.0_EffectRoomDefault.png',
                                                     library_result)
            case.result = compare_result

        # effect room right click gray out
        with uuid("ea135ed2-89f3-46b8-aa50-87f37e80df3d") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = media_room_page.right_click_rename_tag('My Favorites', 'abc')
            case.result = not current_result

        # effect room default delete tag gray
        with uuid("82179f69-b473-47b9-9d35-28df505b5830") as case:
            time.sleep(DELAY_TIME * 4)
            library_result = media_room_page.snapshot(locator=L.effect_room.tag.delete_tag.delete_tag,
                                                      file_name=Auto_Ground_Truth_Folder + 'G4.3.2_EffectRoomDefaultDeleteTag.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.3.2_EffectRoomDefaultDeleteTag.png',
                                                     library_result)
            case.result = compare_result

        # effect room add new tag
        with uuid("ecfa57a8-d838-4ea9-9c57-ce6c801c2ed3") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = effect_room_page.add_effectroom_new_tag('stuv')
            time.sleep(DELAY_TIME * 4)
            library_result = media_room_page.snapshot(locator=L.effect_room.current_tag_amount,
                                                      file_name=Auto_Ground_Truth_Folder + 'G4.3.3_EffectRoomAddNewTag.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.3.3_EffectRoomAddNewTag.png',
                                                     library_result)
            case.result = compare_result and current_result

        # effect room relaunch PDR
        with uuid("46cc6286-1014-48c0-ab70-7613ac18a713") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.close_app()
            main_page.start_app()
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(3)
            time.sleep(DELAY_TIME * 4)
            library_result = media_room_page.snapshot(locator=L.effect_room.current_tag_amount,
                                                      file_name=Auto_Ground_Truth_Folder + 'G4.3.4_EffectRoomRelaunchPDR.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.3.4_EffectRoomRelaunchPDR.png',
                                                     library_result)
            case.result = compare_result

        # effect room delete tag
        with uuid("aa28a203-4b5f-4208-a2bd-903eae7bedba") as case:
            with uuid("873daa44-fafa-48bf-8f74-86c4a20841e1") as case:
                time.sleep(DELAY_TIME * 4)
                current_result = effect_room_page.delete_tag('stuv')
                time.sleep(DELAY_TIME * 4)
                library_result = media_room_page.snapshot(locator=L.effect_room.current_tag_amount,
                                                          file_name=Auto_Ground_Truth_Folder + 'G4.3.5_EffectRoomDeleteTag.png')
                compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.3.5_EffectRoomDeleteTag.png',
                                                         library_result)
                case.result = compare_result and current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_4_4(self):
        # PiP room default
        with uuid("58c7aba9-34b0-4992-87cf-61516c63a1ef") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 4)
            library_result = media_room_page.snapshot(locator=L.pip_room.explore_view_region.table_all_content_tags,
                                                      file_name=Auto_Ground_Truth_Folder + 'G4.4.0_PiPRoomDefaultTag.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.4.0_PiPRoomDefaultTag.png',
                                                     library_result)
            case.result = compare_result

        # PiP room custom tag delete tag disable
        with uuid("2b458a84-5578-4440-b486-548879a09268") as case:
            media_room_page.select_specific_category('Custom')
            time.sleep(DELAY_TIME * 4)
            current_result = pip_room_page.get_status_DeleteSelectedTag()
            case.result = not current_result

        # PiP room right click gray out
        with uuid("fa267b57-4a23-4683-ab56-487ca90d754f") as case:
            time.sleep(DELAY_TIME * 4)
            media_room_page.select_specific_category('Downloaded')
            time.sleep(DELAY_TIME * 4)
            main_page.right_click()
            time.sleep(DELAY_TIME * 4)
            current_result = pip_room_page.get_status_rightclickmenu_RenameTag()
            time.sleep(DELAY_TIME * 4)
            case.result = not current_result


        # PiP room Downloaded tag delete tag disable
        with uuid("12e820e8-e8e5-4139-a081-77342682c321") as case:
            time.sleep(DELAY_TIME * 4)
            current_result = pip_room_page.get_status_DeleteSelectedTag()
            case.result = not current_result


        # PiP room right click gray out
        with uuid("1b0d7a0d-c428-47c0-b9d0-3a97290482f0") as case:
            time.sleep(DELAY_TIME * 4)
            media_room_page.select_specific_category('Romance')
            time.sleep(DELAY_TIME * 4)
            main_page.right_click()
            time.sleep(DELAY_TIME * 4)
            current_result = pip_room_page.get_status_rightclickmenu_RenameTag()
            case.result = not current_result
            time.sleep(DELAY_TIME * 4)
            main_page.right_click()


        # PiP room add tag
        with uuid("c543769e-fd57-4f7d-8be8-8bffa805d773") as case:
            with uuid("c7c6310d-550b-4dc3-8bfe-9fb577cf4887") as case:
                time.sleep(DELAY_TIME * 4)
                current_result = pip_room_page.add_new_tag('123abc')
                time.sleep(DELAY_TIME * 4)
                library_result = media_room_page.snapshot(locator=L.pip_room.explore_view_region.table_all_content_tags,
                                                          file_name=Auto_Ground_Truth_Folder + 'G4.4.6_PiPRoomAddNewTag.png')
                compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.4.6_PiPRoomAddNewTag.png',
                                                         library_result)
                case.result = compare_result and current_result

        # PiP room rename tag
        with uuid("2906e8f0-a3af-4467-9b46-59a952f25316") as case:
            current_result = pip_room_page.select_tag_RightClickMenu_RenameTag('123abc','654cba')
            time.sleep(DELAY_TIME * 4)
            library_result = media_room_page.snapshot(locator=L.pip_room.explore_view_region.table_all_content_tags,
                                                      file_name=Auto_Ground_Truth_Folder + 'G4.4.7_PiPRoomRenameTag.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.4.7_PiPRoomRenameTag.png',
                                                     library_result)
            case.result = compare_result and current_result

        # PiP room relaunch PDR
        with uuid("59c68245-f4c5-46b7-a77e-ad72773f4acd") as case:
            main_page.close_app()
            main_page.start_app()
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(4)
            time.sleep(DELAY_TIME * 4)
            library_result = media_room_page.snapshot(locator=L.pip_room.explore_view_region.table_all_content_tags,
                                                      file_name=Auto_Ground_Truth_Folder + 'G4.4.8_PiPRoomRelaunchPDR.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.4.8_PiPRoomRelaunchPDR.png',
                                                     library_result)
            case.result = compare_result

        # PiP room delete tag
        with uuid("a0a615aa-c265-437a-854f-9f470953fc80") as case:
            with uuid("acfbd9d0-1f61-4e46-83f2-3521d9cfab42") as case:
                time.sleep(DELAY_TIME * 4)
                current_result = pip_room_page.delete_tag('654cba')
                time.sleep(DELAY_TIME * 4)
                library_result = media_room_page.snapshot(locator=L.pip_room.explore_view_region.table_all_content_tags,
                                                          file_name=Auto_Ground_Truth_Folder + 'G4.4.9_PiPRoomDeleteTag.png')
                compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.4.9_PiPRoomDeleteTag.png',
                                                         library_result)
                case.result = compare_result and current_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_4_5(self):
        # Particle room default
        with uuid("21f09faa-b4ce-4942-b1ab-9454b2da2ad7") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(5)
            time.sleep(DELAY_TIME * 4)
            library_result = particle_room_page.snapshot(locator=L.particle_room.explore_view_region.table_all_content_tags,
                                                      file_name=Auto_Ground_Truth_Folder + 'G4.5.0_ParticleRoomDefaultTag.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.5.0_ParticleRoomDefaultTag.png',
                                                     library_result)
            case.result = compare_result

        # Particle room downloaded tag delete tag disable
        with uuid("3d2f5cea-48fb-4ceb-9fc5-1b08c229844c") as case:
            time.sleep(DELAY_TIME * 4)
            media_room_page.select_specific_category('Downloaded')
            time.sleep(DELAY_TIME * 4)
            library_result = particle_room_page.snapshot(locator=L.particle_room.btn_delete_tag,
                                                        file_name=Auto_Ground_Truth_Folder + 'G4.5.1_ParticleRoomDownloadedDeleteTag.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.5.1_ParticleRoomDownloadedDeleteTag.png',
                                                     library_result)
            case.result = compare_result

        # Particle room general tag delete tag disable
        with uuid("f65c6ab0-fee3-4fa0-a0cb-b35ade7ec102") as case:
            time.sleep(DELAY_TIME * 4)
            media_room_page.select_specific_category('General')
            time.sleep(DELAY_TIME * 4)
            library_result = particle_room_page.snapshot(locator=L.particle_room.btn_delete_tag,
                                                        file_name=Auto_Ground_Truth_Folder + 'G4.5.2_ParticleRoomGeneralDeleteTag.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.5.2_ParticleRoomGeneralDeleteTag.png',
                                                     library_result)
            case.result = compare_result

        # Particle room add new tag and default is 0
        with uuid("f65c6ab0-fee3-4fa0-a0cb-b35ade7ec102") as case:
            with uuid("897c6510-4a28-4393-83f7-c5803d966c59") as case:
                time.sleep(DELAY_TIME * 4)
                particle_room_page.add_particleroom_new_tag('xyz')
                time.sleep(DELAY_TIME * 4)
                library_result = particle_room_page.snapshot(locator=L.particle_room.explore_view_region.table_all_content_tags,
                                                            file_name=Auto_Ground_Truth_Folder + 'G4.5.3_ParticleRoomAddNewTag.png')
                compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.5.3_ParticleRoomAddNewTag.png',
                                                         library_result)
                case.result = compare_result

        # Particle room relaunch PDR
        with uuid("ac646b15-6176-4854-84fa-424a8fecc4e4") as case:
            time.sleep(DELAY_TIME * 4)
            main_page.close_app()
            main_page.start_app()
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(5)
            time.sleep(DELAY_TIME * 4)
            library_result = media_room_page.snapshot(locator=L.particle_room.explore_view_region.table_all_content_tags,
                                                      file_name=Auto_Ground_Truth_Folder + 'G4.5.4_ParticleRoomRelaunchPDR.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.5.4_ParticleRoomRelaunchPDR.png',
                                                     library_result)
            case.result = compare_result

        # particle room delete tag
        with uuid("edea1973-cfa5-46b6-9d26-53d10fca9d17") as case:
            with uuid("807daeba-8f45-415b-acba-be834eb0b567") as case:
                time.sleep(DELAY_TIME * 4)
                media_room_page.select_specific_category('xyz')
                time.sleep(DELAY_TIME * 4)
                particle_room_page.delete_tag('xyz')
                time.sleep(DELAY_TIME * 4)
                library_result = media_room_page.snapshot(locator=L.particle_room.explore_view_region.table_all_content_tags,
                                                          file_name=Auto_Ground_Truth_Folder + 'G4.5.5_ParticleRoomDeleteTag.png')
                compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.5.5_ParticleRoomDeleteTag.png',
                                                         library_result)
                case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_4_6(self):
        # title room default
        with uuid("804e9824-5c12-4321-a093-e15f95c68e91") as case:
            with uuid("cb7292ed-7bc4-4b18-99f9-0b1a8d5997fd") as case:
                with uuid("846c0f80-62bc-4a95-9122-e5089967e634") as case:
                    time.sleep(DELAY_TIME * 4)
                    main_page.enter_room(1)
                    time.sleep(DELAY_TIME * 4)
                    library_result = particle_room_page.snapshot(locator=L.title_room.explore_view_region.table_all_content_tags,
                                                              file_name=Auto_Ground_Truth_Folder + 'G4.6.0_TitleRoomDefaultTag.png')
                    compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.6.0_TitleRoomDefaultTag.png',
                                                             library_result)
                    case.result = compare_result

        # title room custom tag delete tag disable
        with uuid("d2208ac1-ffb7-4357-b72b-dab416644180") as case:
            time.sleep(DELAY_TIME * 4)
            media_room_page.select_specific_category('Custom')
            time.sleep(DELAY_TIME * 4)
            library_result = particle_room_page.snapshot(locator=L.title_room.btn_delete_tag,
                                                        file_name=Auto_Ground_Truth_Folder + 'G4.6.1_TitleRoomCustomDeleteTag.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.6.1_TitleRoomCustomDeleteTag.png',
                                                     library_result)
            case.result = compare_result

        # title room downloaded tag delete tag disable
        with uuid("853be06f-307a-46b2-af87-e4aeec543874") as case:
            time.sleep(DELAY_TIME * 4)
            media_room_page.select_specific_category('Downloaded')
            time.sleep(DELAY_TIME * 4)
            library_result = particle_room_page.snapshot(locator=L.title_room.btn_delete_tag,
                                                        file_name=Auto_Ground_Truth_Folder + 'G4.6.2_TitleRoomDownloadedDeleteTag.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.6.2_TitleRoomDownloadedDeleteTag.png',
                                                     library_result)
            case.result = compare_result

        # title room general tag rename tag disable
        with uuid("118d9481-60c3-4d0e-a2ed-0d976853f2c8") as case:
            time.sleep(DELAY_TIME * 4)
            media_room_page.select_specific_category('General')
            time.sleep(DELAY_TIME * 4)
            main_page.right_click()
            time.sleep(DELAY_TIME * 4)
            current_result = title_room_page.get_status_rightclickmenu_RenameTag()
            case.result = not current_result
            time.sleep(DELAY_TIME * 4)
            main_page.right_click()

        # title room add new tag
        with uuid("0de5b4d2-9e4e-4484-a536-c46b880f9424") as case:
            with uuid("a7439b3c-53a1-4d80-b453-e3a20fff31f8") as case:
                time.sleep(DELAY_TIME * 4)
                title_room_page.add_titleroom_new_tag('gif')
                time.sleep(DELAY_TIME * 4)
                library_result = particle_room_page.snapshot(locator=L.title_room.explore_view_region.table_all_content_tags,
                                                             file_name=Auto_Ground_Truth_Folder + 'G4.6.4_TitleRoomAddNewTag.png')
                compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.6.4_TitleRoomAddNewTag.png',
                                                        library_result)
                case.result = compare_result

        # title room relaunch PDR
        with uuid("77b384ef-8a2d-41ec-84e2-974ef9971b05") as case:
            main_page.close_app()
            main_page.start_app()
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(1)
            time.sleep(DELAY_TIME * 4)
            library_result = media_room_page.snapshot(locator=L.title_room.explore_view_region.table_all_content_tags,
                                                      file_name=Auto_Ground_Truth_Folder + 'G4.6.5_TitleRoomRelaunchPDR.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.6.5_TitleRoomRelaunchPDR.png',
                                                     library_result)
            case.result = compare_result

        # title room delete tag
        with uuid("da14262e-1bbe-466d-934a-8c903ec3dd32") as case:
            with uuid("c75b76fb-23c7-47fc-a4b3-6f37f521794b") as case:
                time.sleep(DELAY_TIME * 4)
                title_room_page.delete_tag('gif')
                time.sleep(DELAY_TIME * 4)
                library_result = particle_room_page.snapshot(locator=L.title_room.explore_view_region.table_all_content_tags,
                                                            file_name=Auto_Ground_Truth_Folder + 'G4.6.6_TitleRoomDeleteTag.png')
                compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.6.6_TitleRoomDeleteTag.png',
                                                         library_result)
                case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_4_7(self):
        # transition room default
        with uuid("64c3b27a-f9df-4db9-8b14-40eec9977d1f") as case:
            with uuid("fced6e92-bea8-431a-9446-e6be54c3501f") as case:
                with uuid("68441eed-9adb-4dd8-998a-48bf64e49fe8") as case:
                    time.sleep(DELAY_TIME * 4)
                    main_page.enter_room(2)
                    time.sleep(DELAY_TIME * 4)
                    library_result = particle_room_page.snapshot(locator=L.transition_room.explore_view_region.table_all_content_tags,
                                                              file_name=Auto_Ground_Truth_Folder + 'G4.7.0_TransitionRoomDefaultTag.png')
                    compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.7.0_TransitionRoomDefaultTag.png',
                                                             library_result)
                    case.result = compare_result

        # transition room general tag rename tag disable
        with uuid("54cfb2ac-67b9-4345-a614-56536ac95301") as case:
            time.sleep(DELAY_TIME * 4)
            media_room_page.select_specific_category('General')
            time.sleep(DELAY_TIME * 4)
            main_page.right_click()
            time.sleep(DELAY_TIME * 4)
            current_result = pip_room_page.get_status_rightclickmenu_RenameTag()
            case.result = not current_result
            time.sleep(DELAY_TIME * 4)
            main_page.right_click()
            time.sleep(DELAY_TIME)

        # transition room general tag delete tag disable
        with uuid("8005d35e-a85a-48fd-ade0-67a4546e7d3b") as case:
            time.sleep(DELAY_TIME * 4)
            media_room_page.select_specific_category('General')
            time.sleep(DELAY_TIME * 4)
            library_result = particle_room_page.snapshot(locator=L.transition_room.btn_delete_tag,
                                                        file_name=Auto_Ground_Truth_Folder + 'G4.7.4_TransitionRoomGeneralDeleteTag.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.7.4_TransitionRoomGeneralDeleteTag.png',
                                                     library_result)
            case.result = compare_result

        # title room add new tag
        with uuid("f0fb5871-5d03-4b27-b516-9097921712ec") as case:
            with uuid("c71eb042-805a-48c2-84a9-453898059679") as case:
                time.sleep(DELAY_TIME * 4)
                transition_room_page.add_transitionroom_new_tag('abc')
                time.sleep(DELAY_TIME * 4)
                library_result = particle_room_page.snapshot(locator=L.transition_room.explore_view_region.table_all_content_tags,
                                                            file_name=Auto_Ground_Truth_Folder + 'G4.7.5_TransitionRoomAddNewTag.png')
                compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.7.5_TransitionRoomAddNewTag.png',
                                                         library_result)
                case.result = compare_result

        # transition room relaunch PDR
        with uuid("5a642c78-7417-4405-ad87-6e1dd253b6b6") as case:
            main_page.close_app()
            main_page.start_app()
            time.sleep(DELAY_TIME * 4)
            main_page.enter_room(2)
            time.sleep(DELAY_TIME * 4)
            library_result = media_room_page.snapshot(locator=L.transition_room.explore_view_region.table_all_content_tags,
                                                      file_name=Auto_Ground_Truth_Folder + 'G4.7.6_TransitionRoomRelaunchPDR.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.7.6_TransitionRoomRelaunchPDR.png',
                                                     library_result)
            case.result = compare_result

        # transition room delete tag
        with uuid("dcb48ede-5e1a-4271-ac37-b9d80858c292") as case:
            with uuid("1d68b219-4187-413a-94dd-058e6d04476a") as case:
                time.sleep(DELAY_TIME * 4)
                transition_room_page.delete_tag('abc')
                time.sleep(DELAY_TIME * 4)
                library_result = particle_room_page.snapshot(locator=L.transition_room.explore_view_region.table_all_content_tags,
                                                            file_name=Auto_Ground_Truth_Folder + 'G4.7.7_TransitionRoomDeleteTag.png')
                compare_result = media_room_page.compare(Ground_Truth_Folder + 'G4.7.7_TransitionRoomDeleteTag.png',
                                                         library_result)
                case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid("59fbe579-6ffb-4a49-a22a-d7f9387f0de8") as case:
            # Skip w/ v20.0.3223
            # My Favorite remove right click menu  > 6.1.2 My Favorites Tag > rename tag disable
            case.result = None
            case.fail_log = '*SKIP by v3223'

        with uuid("6ea1082b-895e-4dbc-801d-de37721b83aa") as case:
            # Skip w/ v20.0.3223
            # My Favorite remove right click menu  > 6.1.2 My Favorites Tag > delete tag disable
            case.result = None
            case.fail_log = '*SKIP by v3223'












