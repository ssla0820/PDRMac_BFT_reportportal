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
# Modify locator to hardcode_0408
#from pages.locator.hardcode_0408 import locator as L

#for update_report_info
from globals import *



# read PDR cap >>
app = SimpleNamespace(**PDR_cap)
# read PDR cap <<

# create driver & page >>
mac = DriverFactory().get_mac_driver_object('mac', app.app_name, app.app_bundleID, app.app_path)
main_page = PageFactory().get_page_object('main_page', mac)
#base_page = PageFactory().get_page_object('base_page', mac)
particle_room_page = PageFactory().get_page_object('particle_room_page',mac)
media_room_page = PageFactory().get_page_object('media_room_page',mac)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="Particle Room.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<



# For Ground Truth / Test Material folder
#======= (Mac Mini)
Ground_Truth_Folder = app.ground_truth_root + '/Particle_Room/' #'/Users/cl/Desktop/AT/PDR_SFT_fromSVN/SFT/GroundTruth/Particle_Room/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Particle_Room/' #'/Users/cl/Desktop/AT/PDR_SFT_fromSVN/SFT/ATGroundTruth/Particle_Room/'
Test_Material_Folder = app.testing_material #'/Users/cl/Desktop/AT/PDR_SFT_fromSVN/Material/'

#======= (iMac27")
#Ground_Truth_Folder = '/Users/qadf-imac27/Desktop/AT/SFT/GroundTruth/Particle_Room/'
#Auto_Ground_Truth_Folder = '/Users/qadf-imac27/Desktop/AT/SFT/ATGroundTruth/Particle_Room/'
#Test_Material_Folder = '/Users/qadf-imac27/Desktop/AT/Material/'

#=======
# Ernesto
#Ground_Truth_Folder = '/Users/clt/Desktop/Ernesto/SFT/GroundTruth/Media_Room/'
#Auto_Ground_Truth_Folder = '/Users/clt/Desktop/Ernesto/SFT/ATGroundTruth/Media_Room/'
#Test_Material_Folder = '/Users/clt/Desktop/Ernesto/Material/'


DELAY_TIME = 1



'''
@pytest.fixture(scope="module", autouse= True)
def init():
    yield
    report.export()
    report.show()
'''




class Test_Particle_Room():

    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        yield mac
        main_page.close_app()
        main_page.clear_cache()

    @classmethod
    def setup_class(cls):
        main_page.clear_cache()
        print('setup class - enter')
        # for update the correct module start time of report (2021/04/20)
        now = datetime.datetime.now()
        report.add_ovinfo('time', now.time().strftime("%H:%M:%S"))
        report.start_time = time.time()
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_init('Particle_Room')


    @classmethod
    def teardown_class(cls):

        #print('teardown_class - export report')
        #report.export()
        #print(
            #f"mask designer result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        #update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           #report.get_ovinfo('skip'),
                           #report.get_ovinfo('duration'))
        #report.show()
        logger('teardown_class - export report')
        report.export()
        logger(
            f"particle room result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           report.get_ovinfo('skip'),
                           report.get_ovinfo('duration'))
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number,
                                                     report.get_ovinfo('na'),
                                                     report.get_ovinfo('skip'),
                                                     report.get_ovinfo('duration'))
        report.show()


    @pytest.mark.skip
    @exception_screenshot
    def test1_1_a(self):
        with uuid("9fbc4bb9-8600-4cf5-8cdd-d4cb37bb8478") as case:
            media_room_page.media_filter_display_audio_only()
            time.sleep(2)
            result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame)
            logger(result)



    #@pytest.mark.skip
    @exception_screenshot
    def test1_1_1_1(self):

        with uuid("efa5601f-4366-453d-97f2-f5844c438222") as case:
            # case1.1.1 : Enter particle room by tap particle room btn
            # select and add one of sample video to timeline
            time.sleep(DELAY_TIME*2)
            main_page.insert_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME*3)
            preview_img_1 = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'preview_img_1.png')
            logger(f"{preview_img_1=}")
            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'preview_img_1.png', preview_img_1)
            logger(compare_result1)
            # select 'particle room' in library
            particle_room_page.enter_room(5)
            result_status = particle_room_page.check_in_particle_room()
            logger(result_status)
            case.result = result_status and compare_result1


        #4/1
        with uuid("f5f7de96-e5c1-45cd-b7c0-bde91250b147") as case:
            ## case2.2.3.1 : add new tag with new name
            # particle_room_page.enter_room(5)
            time.sleep(DELAY_TIME * 2)
            #result_status = media_room_page.add_new_tag('test_123')
            #logger(result_status)
            #media_room_page.add_new_tag('test_123')
            particle_room_page.add_particleroom_new_tag('test_123')
            time.sleep(DELAY_TIME*3)
            SetCheck_result = particle_room_page.find_specific_tag('test_123')
            logger(SetCheck_result)
            if not SetCheck_result:
                case.result = False
            else:
                case.result = True

        #4/1
        with uuid("46d32e39-dd34-41a7-8b25-e20afe6ad55d") as case:
            # case2.1.2 : Download More Particle Effects from CL Cloud
            # time.sleep(5)
            # particle_room_page.tap_ParticleRoom_hotkey()
            # Download two particle templates from CL Cloud (Jamie: can only download one particle at once)
            #result_status_1 = particle_room_page.download_content_from_CL('F')
            result_status_1 = particle_room_page.download_content_from_CL('01-ParticleEffect')
            time.sleep(DELAY_TIME * 2)
            logger(result_status_1)
            #result_status_2 = particle_room_page.download_content_from_CL('wqf')
            result_status_2 = particle_room_page.download_content_from_CL('02-ParticleEffect')
            time.sleep(DELAY_TIME * 2)
            logger(result_status_2)
            particle_room_2_1_2 = particle_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + 'G2.1.2_particle_room_DL_from_CLCloud.png')
            logger(f"{particle_room_2_1_2=}")
            compare_result1 = particle_room_page.compare(Ground_Truth_Folder + 'G2.1.2_particle_room_DL_from_CLCloud.png', particle_room_2_1_2)
            logger(compare_result1)
            case.result = result_status_1 and result_status_2 and compare_result1

        # 4/1
        with uuid("b12f9f24-21b7-4399-a2ba-28ad27fd3537") as case:
            ## case2.3.4.7 : add particle to custom tag
            # particle_room_page.enter_room(5)
            time.sleep(DELAY_TIME * 2)
            # Select one of particle template first
            #particle_room_page.hover_library_media('wqf')
            particle_room_page.hover_library_media('02-ParticleEffect')
            # Add target object to specific tag - test@_123
            result_status_1 = particle_room_page.select_RightClickMenu_Addto('test_123')
            logger(result_status_1)
            # select custom tag - test@_123
            result_status_2 = particle_room_page.select_specific_tag('test_123')
            logger(result_status_2)
            #find_object = media_room_page.select_media_content('wqf') #particle_room_page.hover_library_media('wqf')
            find_object = media_room_page.select_media_content('02-ParticleEffect')
            logger(find_object)
            if find_object == True:
                case.result = True
            else:
                case.result = False
            '''
            particle_room_custom_tag = particle_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + 'G2.3.4.7_particle_room_add_to_custom_tag.png')
            logger(f"{particle_room_custom_tag =}")
            compare_result1 = particle_room_page.compare(Ground_Truth_Folder + 'G2.3.4.7_particle_room_add_to_custom_tag.png', particle_room_custom_tag)
            logger(compare_result1)
            case.result = result_status_1 and compare_result1
            '''

        with uuid("37fd9dcd-265d-4b2d-853b-c7a786b06037") as case:
            # case2.1.8.4 : Thumbnails show as extra large icons
            # particle_room_page.enter_room(5)
            time.sleep(DELAY_TIME * 2)
            result_status = particle_room_page.select_LibraryMenu_ExtraLargeIcons()
            logger(result_status)
            particle_room_1_1 = particle_room_page.snapshot (locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + 'G2.1.8_4_particle_room_extra_large.png')
            logger(f"{particle_room_1_1 =}")
            compare_result1 = particle_room_page.compare(Ground_Truth_Folder + 'G2.1.8_4_particle_room_extra_large.png',particle_room_1_1)
            logger(compare_result1)
            case.result = result_status and compare_result1

        with uuid("6e961597-fe7e-43b6-afa6-fdafab73dbfd") as case:
            # case2.1.8.5 : Thumbnails show as large icons
            # particle_room_page.enter_room(5)
            time.sleep(DELAY_TIME * 2)
            result_status = particle_room_page.select_LibraryMenu_LargeIcons()
            logger(result_status)
            particle_room_1_2 = particle_room_page.snapshot (locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + 'G2.1.8_5_particle_room_large.png')
            logger(f"{particle_room_1_2 =}")
            compare_result1 = particle_room_page.compare(Ground_Truth_Folder + 'G2.1.8_5_particle_room_large.png',particle_room_1_2)
            logger(compare_result1)
            case.result = result_status and compare_result1

        with uuid("c5abf83a-0466-4363-82ac-54696cd99e32") as case:
            # case2.1.8.7 : Thumbnails show as small icons
            # particle_room_page.enter_room(5)
            time.sleep(DELAY_TIME * 2)
            result_status = particle_room_page.select_LibraryMenu_SmallIcons()
            logger(result_status)
            particle_room_1_3 = particle_room_page.snapshot (locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + 'G2.1.8_7_particle_room_small.png')
            logger(f"{particle_room_1_3 =}")
            compare_result1 = particle_room_page.compare(Ground_Truth_Folder + 'G2.1.8_7_particle_room_small.png',particle_room_1_3)
            logger(compare_result1)
            case.result = result_status and compare_result1

        with uuid("b401be23-0a44-40ea-93b4-02fe84a20a6c") as case:
            # case2.1.8.6 : Thumbnails show as medium icons
            # particle_room_page.enter_room(5)
            time.sleep(DELAY_TIME * 2)
            result_status = particle_room_page.select_LibraryMenu_MediumIcons()
            logger(result_status)
            particle_room_1_4 = particle_room_page.snapshot (locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + 'G2.1.8_6_particle_room_medium.png')
            logger(f"{particle_room_1_4 =}")
            compare_result1 = particle_room_page.compare(Ground_Truth_Folder + 'G2.1.8_6_particle_room_medium.png',particle_room_1_4)
            logger(compare_result1)
            case.result = result_status and compare_result1


        # 4/1
        with uuid("a79144a6-cbcf-4a15-ac4c-77775aa1c704") as case:
            ## case2.2.1.2 : Hide explore view
            # particle_room_page.enter_room(5)
            #time.sleep(DELAY_TIME * 2)
            result_status = particle_room_page.click_ExplorerView()
            logger(result_status)
            particle_room_hide_explore_view = particle_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + 'G2.2.1.2_particle_room_hide_explore_view.png')
            logger(f"{particle_room_hide_explore_view =}")
            compare_result1 = particle_room_page.compare(Ground_Truth_Folder + 'G2.2.1.2_particle_room_hide_explore_view.png', particle_room_hide_explore_view)
            logger(compare_result1)
            case.result = result_status and compare_result1


        # 4/7
        with uuid("673609ff-719e-4ea1-8762-33e1492f41cf") as case:
            ## case2.2.1.1 : Display explore view
            # particle_room_page.enter_room(5)
            #time.sleep(DELAY_TIME * 2)
            result_status = particle_room_page.click_ExplorerView()
            logger(result_status)
            particle_room_display_explore_view = particle_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + 'G2.2.1.1_particle_room_display_explore_view.png')
            logger(f"{particle_room_display_explore_view =}")
            compare_result1 = particle_room_page.compare(Ground_Truth_Folder + 'G2.2.1.1_particle_room_display_explore_view.png', particle_room_display_explore_view)
            logger(compare_result1)
            case.result = result_status and compare_result1


    #@pytest.mark.skip
    #@exception_screenshot
    #def test1_1_1_2(self):
        #4/7
        with uuid("ba036d39-e7b2-44df-8148-2718537910ee") as case:
            ## case2.2.3.2 : add new tag with existed name > pops up warning dialogue
            #time.sleep(DELAY_TIME * 5)
            #particle_room_page.enter_room(5)
            SetCheck_result = particle_room_page.add_particleroom_new_tag('test_123')
            time.sleep(DELAY_TIME*3)
            #SetCheck_result = L.particle_room.warning_dialog.msg1
            logger(SetCheck_result)
            if not SetCheck_result:
                case.result = True
            else:
                case.result = False
            '''
            if not particle_room_page.exist(locator=SetCheck_result):
                case.result = False
            else:
                case.result = True
            '''

        # 4/7
        with uuid("bcf452e0-32ef-4613-b64a-a69647f627e6") as case:
            ## case2.2.3.3 : add new tag with Unicode name
            time.sleep(DELAY_TIME * 3)
            particle_room_page.add_particleroom_new_tag('???')
            SetCheck_result = particle_room_page.find_specific_tag('???')

            if not SetCheck_result:
                case.result = False
            else:
                case.result = True


        # 4/7
        with uuid("60aeb406-2f14-49de-9444-cabcc416ded7") as case:
            ## Case2.2.4.1 Delete the selected tag > Default tag
            #time.sleep(DELAY_TIME * 3)
            particle_room_page.select_specific_tag('Custom')
            particle_room_page.right_click()

            image_full_path = Auto_Ground_Truth_Folder + 'particle_room_2_2_4_1.png'

            ground_truth = Ground_Truth_Folder + 'particle_room_2_2_4_1.png'
            current_preview = particle_room_page.snapshot(locator=L.particle_room.explore_view_region.table_all_content_tags,
                                                            file_name=image_full_path)

            check_result = particle_room_page.compare(ground_truth, current_preview)
            particle_room_page.select_specific_tag('General')
            case.result = check_result


        # 4/7
        with uuid("a9a6e1d6-e6c4-4a52-9fc5-39d2b656746f") as case:
            ## Case2.3.4.6 Delete template (only for Custom/Downloaded)
            #time.sleep(DELAY_TIME * 3)
            # select downloaded particle object in specific tag
            particle_room_page.select_specific_tag('test_123')
            #particle_room_page.hover_library_media('wqf')
            particle_room_page.hover_library_media('02-ParticleEffect')
            # delete template from this tag
            check_result = particle_room_page.select_RightClickMenu_Delete()

            case.result = check_result


        # 4/7
        with uuid("504c6da6-65dd-4e14-b5cf-75ec3cc4de0d") as case:
            ## Case2.2.4.2 Delete the selected tag > Custom tag
            #time.sleep(DELAY_TIME * 3)
            particle_room_page.delete_tag('test_123')
            check_result = particle_room_page.select_specific_tag('test_123')
            logger(check_result)
            logger('known bug: VDE212430-0088, VDE212430-0011')
            if not check_result:
                case.result = True
            else:
                case.result = False

        # 4/7
        with uuid("57ba3ace-4ef3-4d10-96df-ce38e625a08d") as case:
            ## Case2.2.2 Select tag
            #time.sleep(DELAY_TIME*3)
            SetCheck_result1 = particle_room_page.check_is_in_special_category('General', 'Maple')
            logger(SetCheck_result1)
            #SetCheck_result2 = particle_room_page.check_is_in_special_category('Downloaded', 'F')
            SetCheck_result2 = particle_room_page.check_is_in_special_category('Downloaded', '01-ParticleEffect')
            logger(SetCheck_result2)
            SetCheck_result_custom = particle_room_page.select_specific_tag('Custom')
            logger(SetCheck_result_custom)
            particle_room_library = particle_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + 'G2.2.2_particle_room_library_area.png')
            logger(f"{particle_room_library =}")
            compare_result1 = particle_room_page.compare(Ground_Truth_Folder + 'G2.2.2_particle_room_library_area.png', particle_room_library)
            logger(compare_result1)
            SetCheck_result3 = particle_room_page.check_is_in_special_category('All Content', 'Effect-A')
            logger(SetCheck_result3)
            #time.sleep(DELAY_TIME*2)
            case.result = SetCheck_result1 and SetCheck_result2 and SetCheck_result3 and compare_result1
            time.sleep(DELAY_TIME)


        # 4/7
        with uuid("5a01c4d4-5069-41cb-bbc4-6cbafaa3c192") as case:
            ## Case2.2.5.1 Right click on default tag and check context menu
            #time.sleep(DELAY_TIME * 3)
            # select 'downloaded' to check context menu
            particle_room_page.select_specific_tag('Downloaded')
            particle_room_page.right_click()
            image_full_path = Auto_Ground_Truth_Folder + 'particle_room_2_2_5_1_Downloaded.png'
            ground_truth = Ground_Truth_Folder + 'particle_room_2_2_5_1_Downloaded.png'
            current_preview = particle_room_page.snapshot(locator=L.particle_room.explore_view_region.table_all_content_tags,
                                                            file_name=image_full_path)
            check_result_1 = particle_room_page.compare(ground_truth, current_preview)
            logger(check_result_1)
            # select 'General' to check context menu
            particle_room_page.select_specific_tag('General')
            particle_room_page.right_click()
            image_full_path = Auto_Ground_Truth_Folder + 'particle_room_2_2_5_1_General.png'
            ground_truth = Ground_Truth_Folder + 'particle_room_2_2_5_1_General.png'
            current_preview_1 = particle_room_page.snapshot(locator=L.particle_room.explore_view_region.table_all_content_tags,
                file_name=image_full_path)
            check_result_2 = particle_room_page.compare(ground_truth, current_preview_1)
            logger(check_result_2)
            # select 'General' to check context menu
            particle_room_page.select_specific_tag('Custom')
            particle_room_page.right_click()
            image_full_path = Auto_Ground_Truth_Folder + 'particle_room_2_2_5_1_Custom.png'
            ground_truth = Ground_Truth_Folder + 'particle_room_2_2_5_1_Custom.png'
            current_preview_2 = particle_room_page.snapshot(locator=L.particle_room.explore_view_region.table_all_content_tags,
                file_name=image_full_path)
            check_result_3 = particle_room_page.compare(ground_truth, current_preview_2)
            logger(check_result_3)
            # check comparison result
            case.result = check_result_1 and check_result_2 and check_result_3


        # 4/7
        with uuid("13ee3edc-3337-4e4b-9905-f6236f3fa91c") as case:
            ## Case2.2.5.2 Rename custom tag
            #time.sleep(DELAY_TIME * 3)
            # select custom tag 'New Tag' to check context menu
            particle_room_page.select_tag_RightClickMenu_RenameTag('New Tag', 'abc')
            SetCheck_result = particle_room_page.select_specific_tag('abc')
            logger(SetCheck_result)
            if not SetCheck_result:
                case.result = False
            else:
                case.result = True

    #def test1_1_2_4(self):
        # 4/7
        with uuid("f24851ce-1624-42e5-b681-08e84a964f99") as case:
            ## Case2.2.5.3 Delete custom tag via context menu
            #time.sleep(DELAY_TIME * 3)
            # select another custom tag 'test_123' or '???'
            particle_room_page.select_specific_tag('???')
            #particle_room_page.select_specific_tag('abc')
            # select custom tag 'abc' and delete it via context menu
            particle_room_page.select_tag_RightClickMenu_DeleteTag('abc')
            time.sleep(DELAY_TIME * 2)
            SetCheck_result = particle_room_page.select_specific_tag('abc')
            logger(SetCheck_result)
            # delete all custom tag
            particle_room_page.select_tag_RightClickMenu_DeleteTag('???')
            # delete downloaded template
            particle_room_page.select_specific_tag('Downloaded')
            #particle_room_page.hover_library_media('F')
            particle_room_page.hover_library_media('01-ParticleEffect')
            particle_room_page.select_RightClickMenu_Delete()
            # select 'All Content'
            particle_room_page.select_specific_tag('All Content')
            main_page.save_project('test', Test_Material_Folder)
            if SetCheck_result:
                case.result = False
            else:
                case.result = True





    #@pytest.mark.skip
    @exception_screenshot
    def test1_1_2_1(self):

        with uuid("1cbe8b3f-3ffd-4e9a-9df9-68f3eafd257f") as case:
            # case1.1.2 : Enter particle room by hotkey
            time.sleep(3)
            # switch to 'particle room' by hotkey
            particle_room_page.tap_ParticleRoom_hotkey()
            result_status = particle_room_page.check_in_particle_room()
            logger(result_status)
            case.result = result_status


        with uuid("feb32aa1-af24-435f-af64-ec8692b4765d") as case:
            # case2.1.1 : Import particle template that downloaded from DZ
            #time.sleep(5)
            particle_room_page.tap_ParticleRoom_hotkey()
            result_status = particle_room_page.click_import_particle_objects(Test_Material_Folder + '/Particle_DZ_2.dzp/') #'/Users/qadf-imac27/Desktop/AT/Material/Particle_DZ_2.dzp')
            time.sleep(1)
            particle_room_page.click_OK_onEffectExtractor()
            time.sleep(2)
            logger(result_status)
            particle_room_2_1_1 = particle_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + 'G2.1.1_particle_room.png')
            logger(f"{particle_room_2_1_1=}")
            compare_result1 = particle_room_page.compare(Ground_Truth_Folder + 'G2.1.1_particle_room.png', particle_room_2_1_1)
            logger(compare_result1)
            case.result = result_status and compare_result1
            #case.result = result_status

        # 3/30
        with uuid("35ba4188-700e-4a07-bda6-4152013d6dcd") as case:
            # case2.1.6 : Switch to detail view
            #time.sleep(5)
            #particle_room_page.tap_ParticleRoom_hotkey()
            # click detail view button
            main_page.click_library_details_view()
            # snapshot detail view button to check enable status
            details_view_btn_status = particle_room_page.snapshot(locator=L.main.btn_library_details_view, file_name=Auto_Ground_Truth_Folder + 'G2.1.6_detail_view_btn.png')
            time.sleep(2)
            logger(details_view_btn_status)
            compare_result1 = particle_room_page.compare(Ground_Truth_Folder + 'G2.1.6_detail_view_btn.png', details_view_btn_status)
            logger(compare_result1)
            # snapshot list view
            particle_room_list = particle_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view, file_name=Auto_Ground_Truth_Folder + 'G2.1.6_particle_room_list.png')
            logger(f"{particle_room_list=}")
            compare_result2 = particle_room_page.compare(Ground_Truth_Folder + 'G2.1.6_particle_room_list.png', particle_room_list)
            logger(compare_result2)
            case.result = compare_result1 and compare_result2

        # 3/30
        with uuid("e8628cc4-c2de-4534-bd3b-75f8b13dc559") as case:
            # case2.1.10 : Search the library
            #time.sleep(DELAY_TIME*3)
            #particle_room_page.tap_ParticleRoom_hotkey()
            # switch to "All Content"
            media_room_page.select_specific_category('All Content')
            # input text in search bar
            particle_room_page.search_Particle_room_library('ra')
            #time.sleep(DELAY_TIME*2)
            # snapshot list view
            result_status1 = particle_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view, file_name=Auto_Ground_Truth_Folder + 'G2.1.10_particle_search_result.png')
            logger(result_status1)
            compare_result1 = particle_room_page.compare(Ground_Truth_Folder + 'G2.1.10_particle_search_result.png', result_status1)
            logger(compare_result1)
            # cancel search
            media_room_page.search_library_click_cancel()
            # snapshot list view after cancel search
            result_status2 = particle_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view, file_name=Auto_Ground_Truth_Folder + 'G2.1.10_particle_cancel_search.png')
            logger(result_status2)
            compare_result2 = particle_room_page.compare(Ground_Truth_Folder + 'G2.1.10_particle_cancel_search.png', result_status2)
            logger(compare_result2)
            # check test result
            case.result = compare_result1 and compare_result2

        # 3/30
        with uuid("2a60753b-9108-419b-9b54-303cb9ba3118") as case:
            # case2.1.7 : Switch to icon view
            #time.sleep(5)
            #particle_room_page.tap_ParticleRoom_hotkey()
            # click icon view button
            main_page.click_library_icon_view()
            # snapshot detail view button to check enable status
            icon_view_btn_status = particle_room_page.snapshot(locator=L.main.btn_library_icon_view, file_name=Auto_Ground_Truth_Folder + 'G2.1.7_icon_view_btn.png')
            time.sleep(2)
            logger(icon_view_btn_status)
            compare_result1 = particle_room_page.compare(Ground_Truth_Folder + 'G2.1.7_icon_view_btn.png', icon_view_btn_status)
            logger(compare_result1)
            # snapshot list view
            particle_room_thumb = particle_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + 'G2.1.7_particle_room_thumb.png')
            logger(f"{particle_room_thumb=}")
            compare_result2 = particle_room_page.compare(Ground_Truth_Folder + 'G2.1.7_particle_room_thumb.png', particle_room_thumb)
            logger(compare_result2)
            case.result = compare_result1 and compare_result2

        # 3/30
        with uuid("05261fc8-adb0-485b-8cfa-471276f1c656") as case:
            # case2.1.3 : Select different category
            #time.sleep(5)
            #particle_room_page.tap_ParticleRoom_hotkey()
            # switch to Downloaded
            media_room_page.select_specific_category('Downloaded')
            particle_room_status1 = particle_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + 'G2.1.3_particle_room_downloaded.png')
            logger(f"{particle_room_status1=}")
            compare_result1 = particle_room_page.compare(Ground_Truth_Folder + 'G2.1.3_particle_room_downloaded.png', particle_room_status1)
            logger(compare_result1)
            # switch to General
            media_room_page.select_specific_category('General')
            particle_room_status2 = particle_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + 'G2.1.3_particle_room_general.png')
            logger(f"{particle_room_status2=}")
            compare_result2 = particle_room_page.compare(Ground_Truth_Folder + 'G2.1.3_particle_room_general.png', particle_room_status2)
            logger(compare_result2)
            # switch to Custom
            media_room_page.select_specific_category('Custom')
            particle_room_status3 = particle_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + 'G2.1.3_particle_room_custom.png')
            logger(f"{particle_room_status3=}")
            compare_result3 = particle_room_page.compare(Ground_Truth_Folder + 'G2.1.3_particle_room_custom.png', particle_room_status3)
            logger(compare_result3)
            # switch to All content
            media_room_page.select_specific_category('All Content')
            particle_room_status4 = particle_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + 'G2.1.3_particle_room_all_content.png')
            logger(f"{particle_room_status4=}")
            compare_result4 = particle_room_page.compare(Ground_Truth_Folder + 'G2.1.3_particle_room_all_content.png', particle_room_status4)
            logger(compare_result4)
            case.result = compare_result1 and compare_result2 and compare_result3 and compare_result4


        #3/31
        with uuid("c4d0d565-51ff-42e2-9cdc-b63c4c344615") as case:
            # case2.1.8.2 : sort by category
            # particle_room_page.enter_room(5)
            time.sleep(DELAY_TIME * 2)
            result_status = particle_room_page.sort_by_category()
            logger(result_status)
            particle_room_sort_by_category = particle_room_page.snapshot (locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + 'G2.1.8_2_particle_room_sort_by_category.png')
            logger(f"{particle_room_sort_by_category =}")
            compare_result1 = particle_room_page.compare(Ground_Truth_Folder + 'G2.1.8_2_particle_room_sort_by_category.png', particle_room_sort_by_category )
            logger(compare_result1)
            case.result = result_status and compare_result1
            particle_room_page.sort_by_category()

        #3/31
        with uuid("22498757-b244-4125-8c4c-6273ca717211") as case:
            # case2.1.8.3 : sort by create date
            # particle_room_page.enter_room(5)
            time.sleep(DELAY_TIME * 2)
            result_status = particle_room_page.sort_by_createdate()
            logger(result_status)
            particle_room_sort_by_createdate = particle_room_page.snapshot (locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + 'G2.1.8_3_particle_room_sort_by_createdate.png')
            logger(f"{particle_room_sort_by_createdate =}")
            compare_result1 = particle_room_page.compare(Ground_Truth_Folder + 'G2.1.8_3_particle_room_sort_by_createdate.png', particle_room_sort_by_createdate )
            logger(compare_result1)
            case.result = result_status and compare_result1
            particle_room_page.sort_by_createdate()

        #3/31
        with uuid("d8a214e5-eb78-4beb-91e7-b32810a022d3") as case:
            # case2.1.8.1 : sort by name
            # particle_room_page.enter_room(5)
            time.sleep(DELAY_TIME * 2)
            result_status = particle_room_page.sort_by_name()
            logger(result_status)
            particle_room_sort_by_name = particle_room_page.snapshot (locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + 'G2.1.8_1_particle_room_sort_by_name.png')
            logger(f"{particle_room_sort_by_name =}")
            compare_result1 = particle_room_page.compare(Ground_Truth_Folder + 'G2.1.8_1_particle_room_sort_by_name.png', particle_room_sort_by_name )
            logger(compare_result1)
            case.result = result_status and compare_result1

    #def test1_1_2_5(self):
        #4/8
        with uuid("da843fbe-0d82-4ff5-9d0b-b92b13092457") as case:
            # case2.3.4.1 : Right click menu - add to timeline
            #time.sleep(DELAY_TIME)
            # select track#2
            main_page.timeline_select_track(2)
            # select particle object
            media_room_page.select_media_content('Maple')
            # insert to the selected track
            Setcheck_result = particle_room_page.select_RightClickMenu_AddToTimeline()
            logger(Setcheck_result)
            # set timecode to 00_00_05_00 and then snapshot the preview screen
            main_page.set_timeline_timecode('00_00_05_00')
            preview_img = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_img.png')
            logger(f"{preview_img=}")

            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'preview_img.png', preview_img)
            logger(compare_result1)

            # remove downloaded template
            #particle_room_page.select_specific_tag('Downloaded')
            #particle_room_page.hover_library_media('!Pa.20098-16:9')
            #particle_room_page.select_RightClickMenu_Delete()
            main_page.save_project('test', Test_Material_Folder)
            case.result = Setcheck_result and compare_result1


    #@pytest.mark.skip
    @exception_screenshot
    def test1_1_2_2(self):

        with uuid("97ddf81d-0009-4845-963d-eace3cf528bc") as case:
            # case2.3.2.1 : check 4:3 template's thumbnail
            time.sleep(DELAY_TIME*5)
            # switch project aspect ratio to 4:3
            main_page.set_project_aspect_ratio('4_3')
            # Enter particle room
            particle_room_page.tap_ParticleRoom_hotkey()
            result_status = particle_room_page.check_in_particle_room()
            logger(result_status)
            # snapshot for library area
            particle_library_area = particle_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                        file_name=Auto_Ground_Truth_Folder + 'G2.3.2.1_particle_room_thumb_4_3.png')
            logger(f"{particle_library_area =}")
            compare_result = particle_room_page.compare(Ground_Truth_Folder + 'G2.3.2.1_particle_room_thumb_4_3.png', particle_library_area)
            logger(compare_result)
            case.result = result_status and compare_result

        with uuid("8b7471b0-dff5-460f-83cd-9c8abfc29e2d") as case:
            # case2.3.2.2 : check preview screen after insert 4:3 template to timeline
            media_room_page.select_media_content('Effect-A')
            # insert to the selected track
            Setcheck_result = particle_room_page.select_RightClickMenu_AddToTimeline()
            logger(Setcheck_result)
            # set timecode to 00_00_05_00 and then snapshot the preview screen
            main_page.set_timeline_timecode('00_00_05_00')
            time.sleep(DELAY_TIME * 2)
            preview_img2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                   file_name=Auto_Ground_Truth_Folder + 'preview_img_4_3.png')
            logger(f"{preview_img2=}")
            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'preview_img_4_3.png', preview_img2)
            logger(compare_result1)
            # reset timecode to 00_00_00_00 by hotkey
            particle_room_page.tap_Stop_hotkey()
            #case.result = Setcheck_result and compare_result1
            case.result = compare_result1

        with uuid("5c117171-f493-4008-8c95-aa28af07d0a2") as case:
            # case2.3.2.7 : check 1:1 template's thumbnail
            #time.sleep(DELAY_TIME*2)
            # switch project aspect ratio to 1:1
            main_page.set_project_aspect_ratio('1_1')
            # Enter particle room
            #particle_room_page.tap_ParticleRoom_hotkey()
            #result_status = particle_room_page.check_in_particle_room()
            #logger(result_status)
            # snapshot for library area
            particle_library_area = particle_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                        file_name=Auto_Ground_Truth_Folder + 'G2.3.2.7_particle_room_thumb_1_1.png')
            logger(f"{particle_library_area =}")
            compare_result = particle_room_page.compare(Ground_Truth_Folder + 'G2.3.2.7_particle_room_thumb_1_1.png', particle_library_area)
            logger(compare_result)
            case.result = compare_result

        with uuid("6c2a0e98-62d4-457c-b934-dce2a5f7b770") as case:
            # case2.3.2.8 : check preview screen after insert 1:1 template to timeline
            media_room_page.select_media_content('Effect-A') #('Maple')
            # insert to the selected track
            #Setcheck_result = particle_room_page.select_RightClickMenu_AddToTimeline()
            Setcheck_result = main_page.tips_area_insert_media_to_selected_track(1)
            logger(Setcheck_result)
            # set timecode to 00_00_05_00 and then snapshot the preview screen
            main_page.set_timeline_timecode('00_00_05_00')
            preview_img2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                   file_name=Auto_Ground_Truth_Folder + 'preview_img_1_1.png')
            logger(f"{preview_img2=}")
            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'preview_img_1_1.png', preview_img2)
            logger(compare_result1)
            # reset timecode to 00_00_00_00 by hotkey
            particle_room_page.tap_Stop_hotkey()
            case.result = Setcheck_result and compare_result1


        with uuid("2ee46260-d49b-4abc-bf3d-5ba045f11b50") as case:
            # case2.3.2.5 : check 9:16 template's thumbnail
            #time.sleep(DELAY_TIME*2)
            # switch project aspect ratio to 9:16
            main_page.set_project_aspect_ratio('9_16')
            # Enter particle room
            #particle_room_page.tap_ParticleRoom_hotkey()
            #result_status = particle_room_page.check_in_particle_room()
            #logger(result_status)
            # snapshot for library area
            particle_library_area = particle_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                        file_name=Auto_Ground_Truth_Folder + 'G2.3.2.5_particle_room_thumb_9_16.png')
            logger(f"{particle_library_area =}")
            compare_result = particle_room_page.compare(Ground_Truth_Folder + 'G2.3.2.5_particle_room_thumb_9_16.png', particle_library_area)
            logger(compare_result)
            case.result = compare_result

        with uuid("4ef6b286-48c0-422b-907d-4523567ee516") as case:
            # case2.3.2.6 : check preview screen after insert 9:16 template to timeline
            media_room_page.select_media_content('Effect-A')
            # insert to the selected track
            #Setcheck_result = particle_room_page.select_RightClickMenu_AddToTimeline()
            Setcheck_result = main_page.tips_area_insert_media_to_selected_track(1)
            logger(Setcheck_result)
            # set timecode to 00_00_05_00 and then snapshot the preview screen
            main_page.set_timeline_timecode('00_00_05_00')
            preview_img2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                   file_name=Auto_Ground_Truth_Folder + 'preview_img_9_16.png')
            logger(f"{preview_img2=}")
            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'preview_img_9_16.png', preview_img2)
            logger(compare_result1)
            # reset timecode to 00_00_00_00 by hotkey
            particle_room_page.tap_Stop_hotkey()
            case.result = Setcheck_result and compare_result1


        with uuid("a2a63d34-1c51-4571-b313-71891b754eed") as case:
            # case2.3.2.3 : check 16:9 template's thumbnail
            #time.sleep(DELAY_TIME*2)
            # switch project aspect ratio to 16:9
            main_page.set_project_aspect_ratio('16_9')
            # Enter particle room
            #particle_room_page.tap_ParticleRoom_hotkey()
            #result_status = particle_room_page.check_in_particle_room()
            #logger(result_status)
            # snapshot for library area
            particle_library_area = particle_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                        file_name=Auto_Ground_Truth_Folder + 'G2.3.2.5_particle_room_thumb_16:9.png')
            logger(f"{particle_library_area =}")
            compare_result = particle_room_page.compare(Ground_Truth_Folder + 'G2.3.2.5_particle_room_thumb_16:9.png', particle_library_area)
            logger(compare_result)
            case.result = compare_result

        with uuid("c3f054a3-6e77-427a-8ccb-bfe931287e16") as case:
            # case2.3.2.4 : check preview screen after insert 16:9 template to timeline
            media_room_page.select_media_content('Effect-A')
            # insert to the selected track
            #Setcheck_result = particle_room_page.select_RightClickMenu_AddToTimeline()
            Setcheck_result = main_page.tips_area_insert_media_to_selected_track(1)
            logger(Setcheck_result)
            # set timecode to 00_00_05_00 and then snapshot the preview screen
            main_page.set_timeline_timecode('00_00_05_00')
            preview_img2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                   file_name=Auto_Ground_Truth_Folder + 'preview_img_16:9.png')
            logger(f"{preview_img2=}")
            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'preview_img_16:9.png', preview_img2)
            logger(compare_result1)
            # reset timecode to 00_00_00_00 by hotkey
            particle_room_page.tap_Stop_hotkey()
            main_page.save_project('test', Test_Material_Folder)
            case.result = Setcheck_result and compare_result1
            time.sleep(DELAY_TIME*3)

    #@pytest.mark.skip
    @exception_screenshot
    def test1_1_2_3(self):

        #4/13
        with uuid("ad7f50f0-185a-4727-8d9b-059dba5e0e63") as case:
            # case2.2.6.1 : save then open project
            # save current status to a new project
            # Enter particle room
            time.sleep(DELAY_TIME*5)
            particle_room_page.tap_ParticleRoom_hotkey()

            # Insert a particle object to timeline
            main_page.select_library_icon_view_media('Rain')
            main_page.tips_area_insert_media_to_selected_track()

            # save as a new project
            main_page.save_project('particle', Test_Material_Folder)

            #logger(path)
            
            # create new project
            main_page.top_menu_bar_file_new_project()
            # open saved project
            #path =
            #Setcheck_result = main_page.top_menu_bar_file_open_recent_projects(Test_Material_Folder + '/particle.pds')
            Setcheck_result = main_page.top_menu_bar_file_open_recent_projects(Test_Material_Folder+'particle.pds')
            main_page.handle_merge_media_to_current_library_dialog()
            case.result = Setcheck_result


            #main_page.save_project('test_particle.pds', Test_Material_Folder)  # save project fail
            main_page.close_and_restart_app()
            time.sleep(DELAY_TIME * 5)
            main_page.top_menu_bar_file_open_project()
            main_page.handle_open_project_dialog(Test_Material_Folder + '/particle.pds')
            main_page.enter_room(5)

            media_room_page.select_specific_category('All Content')
            check_result = media_room_page.select_media_content('Maple')
            if not check_result:
                case.result = False
            else:
                case.result = True
        #'''

        #4/13
        with uuid("14532e22-5dc3-4a80-8b40-38c2fe6a1c6a") as case:
            # case2.3.1 : Free Templates and link to DZ Particle download website
            # enter Particle room
            time.sleep(DELAY_TIME * 3)
            particle_room_page.tap_ParticleRoom_hotkey()
            # make sure PDR does enter particle room
            particle_room_page.check_in_particle_room()
            # click Free template
            #Set_check = particle_room_page.click_freeTemplate() # Fail by checking website's title?
            Set_check = particle_room_page.click_freeTemplate()
            logger(Set_check)
            if not Set_check:
                case.result = False
            else:
                case.result = True

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_3_1(self):

        with uuid('ad7f50f0-185a-4727-8d9b-059dba5e0e63') as case:
            # save project (need recheck)
            case.result = None
            case.fail_log = "*Skip by AT*"

        '''
        with uuid('c0e6f659-9c22-474c-997e-9916ccf0a1c1') as case:
            case.result = None

        with uuid('8b771169-1027-449c-aad8-e3b18d15b696') as case:
            case.result = None

        with uuid('6a9095f0-ff3d-421d-9d73-f6ee17794b3f') as case:
            case.result = None

        with uuid('bad34e79-35bb-4a99-a070-3f55cf9d0307') as case:
            case.result = None
            
        with uuid('') as case:
            case.result = None
        '''
