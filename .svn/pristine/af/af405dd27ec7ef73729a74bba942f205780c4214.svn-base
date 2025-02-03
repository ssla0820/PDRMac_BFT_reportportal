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
effect_room_page = PageFactory().get_page_object('effect_room_page', mac)
media_room_page = PageFactory().get_page_object('media_room_page',mac)
pip_room_page = PageFactory().get_page_object('pip_room_page',mac)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="Color LUT.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<



# For Ground Truth / Test Material folder
#======= (Mac Mini)
Ground_Truth_Folder = app.ground_truth_root + '/Color_LUT/' #'/Users/cl/Desktop/AT/PDR_SFT_fromSVN/SFT/GroundTruth/Color_LUT/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Color_LUT/' #'/Users/cl/Desktop/AT/PDR_SFT_fromSVN/SFT/ATGroundTruth/Color_LUT/'
Test_Material_Folder = app.testing_material #'/Users/cl/Desktop/AT/PDR_SFT_fromSVN/Material/'

#======= (iMac27")
#Ground_Truth_Folder = '/Users/qadf-imac27/Desktop/AT/SFT/GroundTruth/Color_LUT/'
#Auto_Ground_Truth_Folder = '/Users/qadf-imac27/Desktop/AT/SFT/ATGroundTruth/Color_LUT/'
#Test_Material_Folder = '/Users/qadf-imac27/Desktop/AT/Material/'

#======= (Ernesto)
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




class Test_Color_LUT():

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
            google_sheet_execution_log_init('Color_LUT')


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
            f"Color LUT result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
        #4/15
        with uuid("feec677d-3eda-4bc9-bda8-a5bb2a8b5974") as case:
            # case1.1.1.1 : Enter effect room to check LUT count
            # select Color LUT after entering effect room
            time.sleep(5)
            main_page.enter_room(3)
            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)
            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)
            # snapshot for Color LUT library
            effect_room_LUT = effect_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                file_name=Auto_Ground_Truth_Folder + 'G1.1.1.1_effect_room_LUT.png')
            logger(f"{effect_room_LUT =}")
            compare_result1 = effect_room_page.compare(
                Ground_Truth_Folder + 'G1.1.1.1_effect_room_LUT.png', effect_room_LUT)
            logger(compare_result1)
            case.result = result_status and result_status_1 and compare_result1


        #4/15
        with uuid("a49dc5f3-0038-4c5a-b2b3-d985d47314b1") as case:
            # case2.1.1 : Import color presets & CLUTs
            #main_page.enter_room(3)
            # check if PDR does enter effect room normally
            #result_status = effect_room_page.check_effect_room()
            #logger(result_status)
            # import LUT
            #result_status_1 = effect_room_page.import_CLUTs('/Users/qadf-imac27/Desktop/AT/Material/LUT/vf/[AE-Buddy] Hazy.vf')
            result_status_1 = effect_room_page.import_CLUTs('/Users/cl/Desktop/MacPDR_SVN_Run/Material/LUT/vf/[AE-Buddy] Hazy.vf')
            logger(result_status_1)
            # snapshot for Color LUT library
            effect_room_LUT = effect_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.1.1_effect_room_import_LUT.png')
            logger(f"{effect_room_LUT =}")
            compare_result1 = effect_room_page.compare(
                Ground_Truth_Folder + 'G2.1.1_effect_room_import_LUT.png', effect_room_LUT)
            logger(compare_result1)
            case.result = result_status and compare_result1 #and result_status_1

        #4/15
        with uuid("66ae1135-64dc-4acc-8ca4-fedfc01c4a6a") as case:
            # case2.2.1.1 : check if *.3dl is supported or not
            #main_page.enter_room(3)
            # check if PDR does enter effect room normally
            #result_status = effect_room_page.check_effect_room()
            #logger(result_status)
            # import LUT
            #result_status_1 = effect_room_page.import_CLUTs('/Users/qadf-imac27/Desktop/AT/Material/LUT/3dl/[AE-QL] Dream-Look.3dl')
            #result_status_1 = effect_room_page.import_CLUTs('/Users/qadf-imac27/Desktop/AT/Material/LUT/3dl/AE-QL_Dream-Look.3dl')
            result_status_1 = effect_room_page.import_CLUTs(
                '/Users/cl/Desktop/MacPDR_SVN_Run/Material/LUT/3dl/AE-QL_Dream-Look.3dl')

            logger(result_status_1)
            # snapshot for Color LUT library
            effect_room_LUT = effect_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.2.1.1_effect_room_import_3dl_LUT.png')
            logger(f"{effect_room_LUT =}")
            compare_result1 = effect_room_page.compare(
                Ground_Truth_Folder + 'G2.2.1.1_effect_room_import_3dl_LUT.png', effect_room_LUT)
            logger(compare_result1)
            case.result = result_status and compare_result1


        #4/15
        with uuid("b08e5b0e-717d-4fce-a477-184051b86d1f") as case:
            # case2.2.1.2 : check if *.mga is supported or not
            #main_page.enter_room(3)
            # check if PDR does enter effect room normally
            #result_status = effect_room_page.check_effect_room()
            #logger(result_status)
            # import LUT
            #result_status_1 = effect_room_page.import_CLUTs('/Users/qadf-imac27/Desktop/AT/Material/LUT/mga/[Ground Control Color] Carbon_Saber-709.mga')
            #result_status_1 = effect_room_page.import_CLUTs('/Users/qadf-imac27/Desktop/AT/Material/LUT/mga/Carbon_Saber-709.mga')
            result_status_1 = effect_room_page.import_CLUTs('/Users/cl/Desktop/MacPDR_SVN_Run/Material/LUT/mga/Carbon_Saber-709.mga')
            logger(result_status_1)
            # snapshot for Color LUT library
            effect_room_LUT = effect_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.2.1.2_effect_room_import_mga_LUT.png')
            logger(f"{effect_room_LUT =}")
            compare_result1 = effect_room_page.compare(
                Ground_Truth_Folder + 'G2.2.1.2_effect_room_import_mga_LUT.png', effect_room_LUT)
            logger(compare_result1)
            case.result = result_status and compare_result1


        #4/15
        with uuid("2401b0b0-2bb0-4e3a-9c5e-e552d012111d") as case:
            # case2.2.1.3 : check if *.m3d is supported or not
            #main_page.enter_room(3)
            # check if PDR does enter effect room normally
            #result_status = effect_room_page.check_effect_room()
            #logger(result_status)
            # import LUT
            #result_status_1 = effect_room_page.import_CLUTs('/Users/qadf-imac27/Desktop/AT/Material/LUT/m3d/[AE] red gamma.m3d')
            #result_status_1 = effect_room_page.import_CLUTs('/Users/qadf-imac27/Desktop/AT/Material/LUT/m3d/AE_red_gamma.m3d')
            result_status_1 = effect_room_page.import_CLUTs('/Users/cl/Desktop/MacPDR_SVN_Run/Material/LUT/m3d/AE_red_gamma.m3d')
            logger(result_status_1)
            # snapshot for Color LUT library
            effect_room_LUT = effect_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.2.1.3_effect_room_import_m3d_LUT.png')
            logger(f"{effect_room_LUT =}")
            compare_result1 = effect_room_page.compare(
                Ground_Truth_Folder + 'G2.2.1.3_effect_room_import_m3d_LUT.png', effect_room_LUT)
            logger(compare_result1)
            case.result = result_status and compare_result1


        # 4/15
        with uuid("24cc61cf-cc33-403b-bd04-ccc4cf0c37bd") as case:
            # case2.2.1.4 : check if *.cube is supported or not
            # main_page.enter_room(3)
            # check if PDR does enter effect room normally
            # result_status = effect_room_page.check_effect_room()
            # logger(result_status)
            # import LUT
            #result_status_1 = effect_room_page.import_CLUTs('/Users/qadf-imac27/Desktop/AT/Material/LUT/cube/[Color Grading Central] OSIRIS_M31 - Rec.709.cube')
            #result_status_1 = effect_room_page.import_CLUTs('/Users/qadf-imac27/Desktop/AT/Material/LUT/cube/C_G_C_OS_M-R.cube')
            result_status_1 = effect_room_page.import_CLUTs(
                '/Users/cl/Desktop/MacPDR_SVN_Run/Material/LUT/cube/C_G_C_OS_M-R.cube')
            logger(result_status_1)
            # snapshot for Color LUT library
            effect_room_LUT = effect_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.2.1.4_effect_room_import_cube_LUT.png')
            logger(f"{effect_room_LUT =}")
            compare_result1 = effect_room_page.compare(
                Ground_Truth_Folder + 'G2.2.1.4_effect_room_import_cube_LUT.png', effect_room_LUT)
            logger(compare_result1)
            case.result = result_status and compare_result1


        # 4/15
        with uuid("6dfb302d-b537-407a-9e00-fdda4456beff") as case:
            # case2.2.1.5 : check if *.csp is supported or not
            # main_page.enter_room(3)
            # check if PDR does enter effect room normally
            # result_status = effect_room_page.check_effect_room()
            # logger(result_status)
            # import LUT
            #result_status_1 = effect_room_page.import_CLUTs('/Users/qadf-imac27/Desktop/AT/Material/LUT/csp/LUT_Cinespace.csp')
            result_status_1 = effect_room_page.import_CLUTs('/Users/cl/Desktop/MacPDR_SVN_Run/Material/LUT/csp/LUT_Cinespace.csp')
            logger(result_status_1)
            # snapshot for Color LUT library
            effect_room_LUT = effect_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.2.1.5_effect_room_import_csp_LUT.png')
            logger(f"{effect_room_LUT =}")
            compare_result1 = effect_room_page.compare(
                Ground_Truth_Folder + 'G2.2.1.5_effect_room_import_csp_LUT.png', effect_room_LUT)
            logger(compare_result1)
            case.result = result_status and compare_result1

        # 4/15
        with uuid("5b3ad19f-c257-430d-9d74-97c871c0cdca") as case:
            # case2.2.1.6 : check if *.cms is supported or not
            # main_page.enter_room(3)
            # check if PDR does enter effect room normally
            # result_status = effect_room_page.check_effect_room()
            # logger(result_status)
            # import LUT
            #result_status_1 = effect_room_page.import_CLUTs('/Users/qadf-imac27/Desktop/AT/Material/LUT/cms/[AE-Buddy] Grunge.cms')
            #result_status_1 = effect_room_page.import_CLUTs('/Users/qadf-imac27/Desktop/AT/Material/LUT/cms/AE-Buddy_Grunge.cms')
            result_status_1 = effect_room_page.import_CLUTs(
                '/Users/cl/Desktop/MacPDR_SVN_Run/Material/LUT/cms/AE-Buddy_Grunge.cms')
            logger(result_status_1)
            # snapshot for Color LUT library
            effect_room_LUT = effect_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.2.1.6_effect_room_import_cms_LUT.png')
            logger(f"{effect_room_LUT =}")
            compare_result1 = effect_room_page.compare(
                Ground_Truth_Folder + 'G2.2.1.6_effect_room_import_cms_LUT.png', effect_room_LUT)
            logger(compare_result1)
            case.result = result_status and compare_result1


        # 4/15
        with uuid("63eda3fd-a53a-4ca6-a1e3-455ff9bbd463") as case:
            # case2.2.1.7 : check if *.rv3dlut is supported or not
            # main_page.enter_room(3)
            # check if PDR does enter effect room normally
            # result_status = effect_room_page.check_effect_room()
            # logger(result_status)
            # import LUT
            #result_status_1 = effect_room_page.import_CLUTs('/Users/qadf-imac27/Desktop/AT/Material/LUT/rv3dlut/[AE-QL] Dream-Look.rv3dlut')
            #result_status_1 = effect_room_page.import_CLUTs('/Users/qadf-imac27/Desktop/AT/Material/LUT/rv3dlut/AE-QL_DL_rv.rv3dlut')
            result_status_1 = effect_room_page.import_CLUTs(
                '/Users/cl/Desktop/MacPDR_SVN_Run/Material/LUT/rv3dlut/AE-QL_DL_rv.rv3dlut')
            logger(result_status_1)
            # snapshot for Color LUT library
            effect_room_LUT = effect_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.2.1.7_effect_room_import_rv3dlut_LUT.png')
            logger(f"{effect_room_LUT =}")
            compare_result1 = effect_room_page.compare(
                Ground_Truth_Folder + 'G2.2.1.7_effect_room_import_rv3dlut_LUT.png', effect_room_LUT)
            logger(compare_result1)
            case.result = result_status and compare_result1


        #4/15
        with uuid("762e0748-9021-4c23-af3d-639e84697f48") as case:
            # case2.2.1.8 : check if *.vf is supported or not
            #main_page.enter_room(3)
            # check if PDR does enter effect room normally
            #result_status = effect_room_page.check_effect_room()
            #logger(result_status)
            # import LUT
            #result_status_1 = effect_room_page.import_CLUTs('/Users/qadf-imac27/Desktop/AT/Material/LUT/vf/LUT_Nuke Vectorfield.vf')
            #result_status_1 = effect_room_page.import_CLUTs('/Users/qadf-imac27/Desktop/AT/Material/LUT/vf/Demo_N_V.vf')
            result_status_1 = effect_room_page.import_CLUTs(
                '/Users/cl/Desktop/MacPDR_SVN_Run/Material/LUT/vf/Demo_N_V.vf')
            logger(result_status_1)
            # snapshot for Color LUT library
            effect_room_LUT = effect_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.2.1.8_effect_room_import_vf_LUT.png')
            logger(f"{effect_room_LUT =}")
            compare_result1 = effect_room_page.compare(
                Ground_Truth_Folder + 'G2.2.1.8_effect_room_import_vf_LUT.png', effect_room_LUT)
            logger(compare_result1)
            case.result = result_status and compare_result1


        # 4/15
        with uuid("01060bf2-4910-45f3-b1be-2447ca66d866") as case:
            # case2.2.1.9 : check if *.clfr is supported or not
            # main_page.enter_room(3)
            # check if PDR does enter effect room normally
            # result_status = effect_room_page.check_effect_room()
            # logger(result_status)
            # import LUT
            #result_status_1 = effect_room_page.import_CLUTs('/Users/qadf-imac27/Desktop/AT/Material/LUT/CLLUT/CLFR/portrait_aesthetic.clfr')
            result_status_1 = effect_room_page.import_CLUTs('/Users/cl/Desktop/MacPDR_SVN_Run/Material/LUT/CLLUT/CLFR/portrait_aesthetic.clfr')
            logger(result_status_1)
            # snapshot for Color LUT library
            effect_room_LUT = effect_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.2.1.9_effect_room_import_clfr_LUT.png')
            logger(f"{effect_room_LUT =}")
            compare_result1 = effect_room_page.compare(
                Ground_Truth_Folder + 'G2.2.1.9_effect_room_import_clfr_LUT.png', effect_room_LUT)
            logger(compare_result1)
            case.result = result_status and compare_result1





    #@pytest.mark.skip
    #@exception_screenshot
    #def test1_1_1_3(self):
        #4/23
        with uuid("284dd266-4567-4f17-9e36-18d7c3887577") as case:
            # case2.5.1.1 : Apply *.3dl LUT to image file
            # Switch to media room and add one of sample image to timeline
            main_page.enter_room(0)
            time.sleep(DELAY_TIME*2)
            main_page.insert_media('Food.jpg')
            time.sleep(DELAY_TIME*3)
            preview_img_1 = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'preview_img_1.png')
            logger(f"{preview_img_1=}")
            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'preview_img_1.png', preview_img_1)
            logger(compare_result1)
            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)
            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)
            # select one of LUT
            #main_page.select_library_icon_view_media('[AE-QL]_D-L.3dl')
            # Drag selected LUT to image on timeline
            #self.drag_mouse(147, 741)
            #main_page.drag_media_to_timeline_playhead_position('[AE-QL]_D-L',1) # page function doesn't work if include of '[]'
            main_page.drag_media_to_timeline_playhead_position('AE-QL_Dream-Look', 1)
            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_img_apply_3dl.png')
            logger(f"{preview_img_2=}")
            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_img_apply_3dl.png', preview_img_2)
            logger(compare_result2)
            # undo the change
            main_page.click_undo()
            '''
            main_page.tap_Undo_hotkey()
            preview_img_3 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_img_3.png')
            logger(f"{preview_img_3=}")
            # compare with ground truth
            compare_result3 = media_room_page.compare(Ground_Truth_Folder + 'preview_img_3.png', preview_img_3)
            logger(compare_result3)
            '''
            case.result = compare_result1 and compare_result2 and result_status and result_status_1 #and compare_result3


        #4/23
        with uuid("66b613c6-7647-4740-8f16-a20398606f29") as case:
            # case2.5.1.2 : Apply *.mga LUT to image file
            # Switch to media room and add one of sample image to timeline
            '''
            #main_page.enter_room(0)
            time.sleep(DELAY_TIME*2)
            main_page.insert_media('Food.jpg')
            time.sleep(DELAY_TIME*3)
            preview_img_1 = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'preview_img_1.png')
            logger(f"{preview_img_1=}")
            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'preview_img_1.png', preview_img_1)
            logger(compare_result1)
            
            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)
            '''
            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)
            # select one of LUT
            #main_page.select_library_icon_view_media('[Ground_Control_Color]_Carbon_Saber-709')
            # Drag selected LUT to image on timeline
            #self.drag_mouse(147, 741)
            main_page.drag_media_to_timeline_playhead_position('Carbon_Saber-709',1)
            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_img_apply_mga.png')
            logger(f"{preview_img_2=}")
            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_img_apply_mga.png', preview_img_2)
            logger(compare_result2)
            # undo the change
            result_status_2 = main_page.click_undo()
            logger(result_status_2)

            # summary case result
            case.result = compare_result2 and result_status and result_status_1 and result_status_2


        # 4/23
        with uuid("385d38a5-16d7-4a4f-b253-9ab298bfb41f") as case:
            # case2.5.1.3 : Apply *.m3d LUT to image file
            # Switch to media room and add one of sample image to timeline
            '''
            #main_page.enter_room(0)
            time.sleep(DELAY_TIME*2)
            main_page.insert_media('Food.jpg')
            time.sleep(DELAY_TIME*3)
            preview_img_1 = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'preview_img_1.png')
            logger(f"{preview_img_1=}")
            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'preview_img_1.png', preview_img_1)
            logger(compare_result1)

            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)
            '''
            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)
            # Drag selected LUT to image on timeline
            main_page.drag_media_to_timeline_playhead_position('AE_red_gamma', 1)
            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_img_apply_m3d.png')
            logger(f"{preview_img_2=}")
            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_img_apply_m3d.png', preview_img_2)
            logger(compare_result2)
            # undo the change
            result_status_2 = main_page.click_undo()
            logger(result_status_2)

            # summary case result
            case.result = compare_result2 and result_status and result_status_1 and result_status_2


        # 4/23
        with uuid("e4eea197-f112-415f-a1b5-09123293c8d9") as case:
            # case2.5.1.4 : Apply *.cube LUT to image file
            # Switch to media room and add one of sample image to timeline
            '''
            #main_page.enter_room(0)
            time.sleep(DELAY_TIME*2)
            main_page.insert_media('Food.jpg')
            time.sleep(DELAY_TIME*3)
            preview_img_1 = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'preview_img_1.png')
            logger(f"{preview_img_1=}")
            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'preview_img_1.png', preview_img_1)
            logger(compare_result1)

            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)
            '''
            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)
            # Drag selected LUT to image on timeline
            main_page.drag_media_to_timeline_playhead_position('C_G_C_OS_M-R', 1)
            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_img_apply_cube.png')
            logger(f"{preview_img_2=}")
            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_img_apply_cube.png', preview_img_2)
            logger(compare_result2)
            # undo the change
            result_status_2 = main_page.click_undo()
            logger(result_status_2)

            # summary case result
            case.result = compare_result2 and result_status and result_status_1 and result_status_2


       # 4/23
        with uuid("c21fef79-68f5-4035-b236-fad2de92e1a2") as case:
            # case2.5.1.5 : Apply *.csp LUT to image file
            # Switch to media room and add one of sample image to timeline
            '''
            #main_page.enter_room(0)
            time.sleep(DELAY_TIME*2)
            main_page.insert_media('Food.jpg')
            time.sleep(DELAY_TIME*3)
            preview_img_1 = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'preview_img_1.png')
            logger(f"{preview_img_1=}")
            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'preview_img_1.png', preview_img_1)
            logger(compare_result1)

            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)
            '''
            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)
            # Drag selected LUT to image on timeline
            main_page.drag_media_to_timeline_playhead_position('LUT_Cinespace', 1)
            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_img_apply_csp.png')
            logger(f"{preview_img_2=}")
            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_img_apply_csp.png', preview_img_2)
            logger(compare_result2)
            # undo the change
            result_status_2 = main_page.click_undo()
            logger(result_status_2)

            # summary case result
            case.result = compare_result2 and result_status and result_status_1 and result_status_2


      # 4/23
        with uuid("5df2b4f2-d17c-4e49-bcc3-74709e08fff7") as case:
            # case2.5.1.6 : Apply *.cms LUT to image file
            # Switch to media room and add one of sample image to timeline
            '''
            #main_page.enter_room(0)
            time.sleep(DELAY_TIME*2)
            main_page.insert_media('Food.jpg')
            time.sleep(DELAY_TIME*3)
            preview_img_1 = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'preview_img_1.png')
            logger(f"{preview_img_1=}")
            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'preview_img_1.png', preview_img_1)
            logger(compare_result1)

            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)
            '''
            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)
            # Drag selected LUT to image on timeline
            main_page.drag_media_to_timeline_playhead_position('AE-Buddy_Grunge', 1)
            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_img_apply_cms.png')
            logger(f"{preview_img_2=}")
            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_img_apply_cms.png', preview_img_2)
            logger(compare_result2)
            # undo the change
            result_status_2 = main_page.click_undo()
            logger(result_status_2)

            # summary case result
            case.result = compare_result2 and result_status and result_status_1 and result_status_2


      # 4/23
        with uuid("5046e02b-fb64-4176-a73a-a4e345f38b54") as case:
            # case2.5.1.7 : Apply *.rv3dlut LUT to image file
            # Switch to media room and add one of sample image to timeline
            '''
            #main_page.enter_room(0)
            time.sleep(DELAY_TIME*2)
            main_page.insert_media('Food.jpg')
            time.sleep(DELAY_TIME*3)
            preview_img_1 = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'preview_img_1.png')
            logger(f"{preview_img_1=}")
            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'preview_img_1.png', preview_img_1)
            logger(compare_result1)

            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)
            '''
            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)
            # Drag selected LUT to image on timeline
            main_page.drag_media_to_timeline_playhead_position('AE-QL_DL_rv', 1)
            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_img_apply_rv3dlut.png')
            logger(f"{preview_img_2=}")
            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_img_apply_rv3dlut.png', preview_img_2)
            logger(compare_result2)
            # undo the change
            result_status_2 = main_page.click_undo()
            logger(result_status_2)

            # summary case result
            case.result = compare_result2 and result_status and result_status_1 and result_status_2

      # 4/23
        with uuid("78bf0a4b-2c41-411e-9d55-e74093c7437c") as case:
            # case2.5.1.8 : Apply *.vf LUT to image file
            # Switch to media room and add one of sample image to timeline
            '''
            #main_page.enter_room(0)
            time.sleep(DELAY_TIME*2)
            main_page.insert_media('Food.jpg')
            time.sleep(DELAY_TIME*3)
            preview_img_1 = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'preview_img_1.png')
            logger(f"{preview_img_1=}")
            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'preview_img_1.png', preview_img_1)
            logger(compare_result1)

            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)
            '''
            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)
            # Drag selected LUT to image on timeline
            main_page.drag_media_to_timeline_playhead_position('Demo_N_V', 1)
            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_img_apply_vf.png')
            logger(f"{preview_img_2=}")
            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_img_apply_vf.png', preview_img_2)
            logger(compare_result2)
            # undo the change
            result_status_2 = main_page.click_undo()
            logger(result_status_2)

            # summary case result
            case.result = compare_result2 and result_status and result_status_1 and result_status_2


      # 4/23
        with uuid("59a39823-f8ad-4d32-b873-57e1069635e5") as case:
            # case2.5.1.9 : Apply *.clfr LUT to image file
            # Switch to media room and add one of sample image to timeline
            '''
            #main_page.enter_room(0)
            time.sleep(DELAY_TIME*2)
            main_page.insert_media('Food.jpg') ('Skateboard 03.mp4')
            time.sleep(DELAY_TIME*3)
            preview_img_1 = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'preview_img_1.png')
            logger(f"{preview_img_1=}")
            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'preview_img_1.png', preview_img_1)
            logger(compare_result1)

            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)
            '''
            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)
            # Drag selected LUT to image on timeline
            main_page.drag_media_to_timeline_playhead_position('portrait_aesthetic', 1)
            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_img_apply_clfr.png')
            logger(f"{preview_img_2=}")
            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_img_apply_clfr.png', preview_img_2)
            logger(compare_result2)
            # undo the change
            result_status_2 = main_page.click_undo()
            logger(result_status_2)

            # select and remove timeline clip
            main_page.select_timeline_media('Food.jpg',0)
            media_room_page.tap_Remove_hotkey()


            # summary case result
            case.result = compare_result2 and result_status and result_status_1 and result_status_2

        #########
        # 4/29
        with uuid("d6f6dba1-6040-418c-9e3d-33394a009a6b") as case:
            # case2.5.2.1 : Apply *.3dl LUT to video file
            # Switch to media room and add one of sample video to timeline
            time.sleep(DELAY_TIME * 2)
            main_page.enter_room(0)
            time.sleep(DELAY_TIME * 2)
            main_page.insert_media('Skateboard 03.mp4')
            time.sleep(DELAY_TIME * 3)
            preview_img_1 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_video_1.png')
            logger(f"{preview_img_1=}")

            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'preview_video_1.png', preview_img_1)
            logger(compare_result1)

            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)

            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)

            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)

            # select one of LUT
            # main_page.drag_media_to_timeline_playhead_position('[AE-QL]_D-L',1) # page function doesn't work if include of '[]'
            main_page.drag_media_to_timeline_playhead_position('AE-QL_Dream-Look', 1)

            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_video_apply_3dl.png')
            logger(f"{preview_img_2=}")

            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_video_apply_3dl.png', preview_img_2)
            logger(compare_result2)

            # undo the change
            main_page.click_undo()

            # summary case result
            case.result = compare_result1 and compare_result2 and result_status and result_status_1  # and compare_result3


        # 4/29
        with uuid("538d4db0-c23e-4ecf-b250-37ff82813cc6") as case:
            # case2.5.2.2 : Apply *.mga LUT to video file
            '''
            # Switch to media room and add one of sample video to timeline
            main_page.enter_room(0)
            time.sleep(DELAY_TIME * 2)
            main_page.insert_media(''Skateboard 03.mp4)
            time.sleep(DELAY_TIME * 3)
            preview_img_1 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_video_1.png')
            logger(f"{preview_img_1=}")

            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'preview_video_1.png', preview_img_1)
            logger(compare_result1)
            
            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            '''

            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)

            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)

            # select one of LUT
            # main_page.drag_media_to_timeline_playhead_position('[AE-QL]_D-L',1) # page function doesn't work if include of '[]'
            main_page.drag_media_to_timeline_playhead_position('Carbon_Saber-709',1)

            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_video_apply_mga.png')
            logger(f"{preview_img_2=}")

            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_video_apply_mga.png', preview_img_2)
            logger(compare_result2)

            # undo the change
            main_page.click_undo()

            # summary case result
            case.result = compare_result2 and result_status and result_status_1  # and compare_result3


        # 4/29
        with uuid("6098b4d9-9719-4376-9ef0-1798da40bd34") as case:
            # case2.5.2.3 : Apply *.m3d LUT to video file
            '''
            # Switch to media room and add one of sample video to timeline
            main_page.enter_room(0)
            time.sleep(DELAY_TIME * 2)
            main_page.insert_media(''Skateboard 03.mp4)
            time.sleep(DELAY_TIME * 3)
            preview_img_1 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_video_1.png')
            logger(f"{preview_img_1=}")

            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'preview_video_1.png', preview_img_1)
            logger(compare_result1)
            
            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            '''
            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)

            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)

            # select one of LUT
            # main_page.drag_media_to_timeline_playhead_position('[AE-QL]_D-L',1) # page function doesn't work if include of '[]'
            main_page.drag_media_to_timeline_playhead_position('AE_red_gamma', 1)

            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_video_apply_m3d.png')
            logger(f"{preview_img_2=}")

            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_video_apply_m3d.png',
                                                      preview_img_2)
            logger(compare_result2)

            # undo the change
            main_page.click_undo()

            # summary case result
            case.result = compare_result2 and result_status and result_status_1  # and compare_result3

        # 4/29
        with uuid("b395ba46-c43e-4689-b9a6-abf71065a494") as case:
            # case2.5.2.4 : Apply *.cube LUT to video file
            '''
            # Switch to media room and add one of sample video to timeline
            main_page.enter_room(0)
            time.sleep(DELAY_TIME * 2)
            main_page.insert_media(''Skateboard 03.mp4)
            time.sleep(DELAY_TIME * 3)
            preview_img_1 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_video_1.png')
            logger(f"{preview_img_1=}")

            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'preview_video_1.png', preview_img_1)
            logger(compare_result1)
            
            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            '''
            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)

            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)

            # select one of LUT
            # main_page.drag_media_to_timeline_playhead_position('[AE-QL]_D-L',1) # page function doesn't work if include of '[]'
            main_page.drag_media_to_timeline_playhead_position('C_G_C_OS_M-R', 1)

            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_video_apply_cube.png')
            logger(f"{preview_img_2=}")

            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_video_apply_cube.png',
                                                      preview_img_2)
            logger(compare_result2)

            # undo the change
            main_page.click_undo()

            # summary case result
            case.result = compare_result2 and result_status and result_status_1  # and compare_result3


        # 4/29
        with uuid("a0b3d44d-3c06-47c0-a873-ac78c754af82") as case:
            # case2.5.2.5 : Apply *.csp LUT to video file
            '''
            # Switch to media room and add one of sample video to timeline
            main_page.enter_room(0)
            time.sleep(DELAY_TIME * 2)
            main_page.insert_media(''Skateboard 03.mp4)
            time.sleep(DELAY_TIME * 3)
            preview_img_1 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_video_1.png')
            logger(f"{preview_img_1=}")

            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'preview_video_1.png', preview_img_1)
            logger(compare_result1)
            
            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            '''
            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)

            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)

            # select one of LUT
            # main_page.drag_media_to_timeline_playhead_position('[AE-QL]_D-L',1) # page function doesn't work if include of '[]'
            main_page.drag_media_to_timeline_playhead_position('LUT_Cinespace', 1)

            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_video_apply_csp.png')
            logger(f"{preview_img_2=}")

            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_video_apply_csp.png',
                                                      preview_img_2)
            logger(compare_result2)

            # undo the change
            main_page.click_undo()

            # summary case result
            case.result = compare_result2 and result_status and result_status_1  # and compare_result3


        # 4/29
        with uuid("44a7454c-e2fd-43a0-b2dc-05c4eee59b01") as case:
            # case2.5.2.6 : Apply *.cms LUT to video file
            '''
            # Switch to media room and add one of sample video to timeline
            main_page.enter_room(0)
            time.sleep(DELAY_TIME * 2)
            main_page.insert_media(''Skateboard 03.mp4)
            time.sleep(DELAY_TIME * 3)
            preview_img_1 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_video_1.png')
            logger(f"{preview_img_1=}")

            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'preview_video_1.png', preview_img_1)
            logger(compare_result1)
            
            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            '''
            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)

            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)

            # select one of LUT
            # main_page.drag_media_to_timeline_playhead_position('[AE-QL]_D-L',1) # page function doesn't work if include of '[]'
            main_page.drag_media_to_timeline_playhead_position('AE-Buddy_Grunge', 1)

            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_video_apply_cms.png')
            logger(f"{preview_img_2=}")

            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_video_apply_cms.png',
                                                      preview_img_2)
            logger(compare_result2)

            # undo the change
            main_page.click_undo()

            # summary case result
            case.result = compare_result2 and result_status and result_status_1  # and compare_result3


        # 4/29
        with uuid("226679e8-b079-4db9-b903-3e160e3c4266") as case:
            # case2.5.2.7 : Apply *.rv3dlut LUT to video file
            '''
            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            '''
            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)

            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)

            # select one of LUT
            # main_page.drag_media_to_timeline_playhead_position('[AE-QL]_D-L',1) # page function doesn't work if include of '[]'
            main_page.drag_media_to_timeline_playhead_position('AE-QL_DL_rv', 1)

            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_video_apply_rv3dlut.png')
            logger(f"{preview_img_2=}")

            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_video_apply_rv3dlut.png',
                                                      preview_img_2)
            logger(compare_result2)

            # undo the change
            main_page.click_undo()

            # summary case result
            case.result = compare_result2 and result_status and result_status_1  # and compare_result3


        # 4/29
        with uuid("e3797811-aa02-459d-a8a7-16b2fde483f3") as case:
            # case2.5.2.8 : Apply *.vf LUT to video file
            '''
            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            '''
            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)

            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)

            # select one of LUT
            # main_page.drag_media_to_timeline_playhead_position('[AE-QL]_D-L',1) # page function doesn't work if include of '[]'
            main_page.drag_media_to_timeline_playhead_position('Demo_N_V', 1)

            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_video_apply_vf.png')
            logger(f"{preview_img_2=}")

            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_video_apply_vf.png',
                                                      preview_img_2)
            logger(compare_result2)

            # undo the change
            main_page.click_undo()

            # summary case result
            case.result = compare_result2 and result_status and result_status_1  # and compare_result3


        # 4/29
        with uuid("e446c155-0b40-4372-b164-4962c5e9cdcf") as case:
            # case2.5.2.9 : Apply *.clfr LUT to video file
            '''
            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            '''
            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)

            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)

            # select one of LUT
            # main_page.drag_media_to_timeline_playhead_position('[AE-QL]_D-L',1) # page function doesn't work if include of '[]'
            main_page.drag_media_to_timeline_playhead_position('portrait_aesthetic', 1)

            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_video_apply_clfr.png')
            logger(f"{preview_img_2=}")

            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_video_apply_clfr.png',
                                                      preview_img_2)
            logger(compare_result2)

            # undo the change
            #main_page.click_undo() #marked this item in order to proceed next case

            # summary case result
            case.result = compare_result2 and result_status and result_status_1  # and compare_result3

        # 4/29
        with uuid("7f68b16e-053b-4bac-a179-ca43f46df76a") as case:
            # case2.5.3.1 : Only one LUT could be applied
            '''
            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            '''
            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)

            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)

            # select one of LUT
            # main_page.drag_media_to_timeline_playhead_position('[AE-QL]_D-L',1) # page function doesn't work if include of '[]'
            main_page.drag_media_to_timeline_playhead_position('Demo_N_V', 1)

            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_video_apply_vf_1.png')
            logger(f"{preview_img_2=}")

            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_video_apply_vf_1.png',
                                                      preview_img_2)
            logger(compare_result2)

            # undo the change
            main_page.click_undo()

            # summary case result
            case.result = compare_result2 and result_status and result_status_1  # and compare_result3




        # 4/29
        with uuid("7072c73e-e48a-4d8a-a818-538ed73097b7") as case:
            # case1.1.1.2 : show Imported tag and count
            '''
            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            '''
            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)

            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)
            # select "Imported" tag
            result_status_2 = effect_room_page.select_specific_tag('Imported')
            logger(result_status_2)

            # take snapshot for timeline preview
            preview_img_1 = media_room_page.snapshot(locator=L.effect_room.current_tag_amount,
                                                     file_name=Auto_Ground_Truth_Folder + 'Color_LUT_Imported.png')
            logger(f"{preview_img_1=}")
            # locator=L.particle_room.explore_view_region.table_all_content_tags,
            # compare with ground truth
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'Color_LUT_Imported.png', preview_img_1)
            logger(compare_result)

            # summary case result
            case.result = compare_result and preview_img_1 and result_status and result_status_1 and result_status_2  # and compare_result3

        # 4/29
        with uuid("6d795c1a-6634-4108-8f1d-60a51c40634a") as case:
            # case2.1.2 : Contents match the selected category.

            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)

            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)

            # snapshot for Color LUT library1
            effect_room_Color_LUT = effect_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                              file_name=Auto_Ground_Truth_Folder + 'G2.1.2_effect_room_Color_LUT_List.png')
            logger(f"{effect_room_Color_LUT =}")
            compare_result1 = effect_room_page.compare(
                Ground_Truth_Folder + 'G2.1.2_effect_room_Color_LUT_List.png', effect_room_Color_LUT)
            logger(compare_result1)

            # select "Imported" tag
            result_status_2 = effect_room_page.select_specific_tag('Imported')
            logger(result_status_2)

            # snapshot for Color LUT library2
            effect_room_Color_LUT1 = effect_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                               file_name=Auto_Ground_Truth_Folder + 'G2.1.2_effect_room_Color_LUT_Imported.png')
            logger(f"{effect_room_Color_LUT1 =}")
            compare_result2 = effect_room_page.compare(
                Ground_Truth_Folder + 'G2.1.2_effect_room_Color_LUT_Imported.png', effect_room_Color_LUT1)
            logger(compare_result2)

            # summary case result
            case.result = compare_result1 and compare_result2

        #########
        # 5/5
        with uuid("d3a7e18d-33bd-4a89-a9b1-24e592bd0ffa") as case:
            # case2.5.2.1 : Apply *.3dl LUT to pip object
            # select and remove timeline clip
            main_page.select_timeline_media('Skateboard 03.mp4', 0)
            media_room_page.tap_Remove_hotkey()
            # Switch to PiP room and add one of sample pip to timeline
            main_page.enter_room(4)
            # time.sleep(DELAY_TIME * 2)
            pip_room_page.hover_library_media('Dialog_06')
            pip_room_page.select_RightClickMenu_AddToTimeline()
            time.sleep(DELAY_TIME * 3)
            preview_img_1 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_pip_1.png')
            logger(f"{preview_img_1=}")

            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'preview_pip_1.png', preview_img_1)
            logger(compare_result1)

            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)

            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)

            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)

            # select one of LUT
            main_page.drag_media_to_timeline_playhead_position('AE-QL_Dream-Look', 1)

            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_pip_apply_3dl.png')
            logger(f"{preview_img_2=}")

            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_pip_apply_3dl.png', preview_img_2)
            logger(compare_result2)

            # undo the change
            #main_page.click_undo()

            # summary case result
            case.result = compare_result1 and compare_result2 and result_status and result_status_1

        # 5/5
        with uuid("ed427270-8c94-418c-b64b-f3e5a690589f") as case:
            # case2.5.2.2 : Apply *.mga LUT to pip object
            '''
            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            '''

            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)

            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)

            # select one of LUT
            # main_page.drag_media_to_timeline_playhead_position('[AE-QL]_D-L',1) # page function doesn't work if include of '[]'
            main_page.drag_media_to_timeline_playhead_position('Carbon_Saber-709', 1)

            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_pip_apply_mga.png')
            logger(f"{preview_img_2=}")

            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_pip_apply_mga.png',
                                                      preview_img_2)
            logger(compare_result2)

            # undo the change
            time.sleep(DELAY_TIME*2)
            #main_page.click_undo()

            # summary case result
            case.result = compare_result2 and result_status and result_status_1

        # 5/5
        with uuid("be7a65a2-70e1-4471-a52f-c4c72d8dfa7b") as case:
            # case2.5.2.3 : Apply *.m3d LUT to pip object
            '''
            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            '''
            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)

            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)

            # select one of LUT
            # main_page.drag_media_to_timeline_playhead_position('[AE-QL]_D-L',1) # page function doesn't work if include of '[]'
            main_page.drag_media_to_timeline_playhead_position('AE_red_gamma', 1)

            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_pip_apply_m3d.png')
            logger(f"{preview_img_2=}")

            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_pip_apply_m3d.png',
                                                      preview_img_2)
            logger(compare_result2)

            # undo the change
            #main_page.click_undo()

            # summary case result
            case.result = compare_result2 and result_status and result_status_1

        # 5/5
        with uuid("96340701-ba1a-42f6-aaa8-6ab8649cf8f9") as case:
            # case2.5.2.4 : Apply *.cube LUT to pip object
            '''
            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            '''
            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)

            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)

            # select one of LUT
            # main_page.drag_media_to_timeline_playhead_position('[AE-QL]_D-L',1) # page function doesn't work if include of '[]'
            main_page.drag_media_to_timeline_playhead_position('C_G_C_OS_M-R', 1)

            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_pip_apply_cube.png')
            logger(f"{preview_img_2=}")

            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_pip_apply_cube.png',
                                                      preview_img_2)
            logger(compare_result2)

            # undo the change
            #main_page.click_undo()

            # summary case result
            case.result = compare_result2 and result_status and result_status_1

        # 5/5
        with uuid("d7e6a3d2-8b1c-492e-8e11-644c8ef28ce0") as case:
            # case2.5.2.5 : Apply *.csp LUT to pip object
            '''
            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            '''
            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)

            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)

            # select one of LUT
            # main_page.drag_media_to_timeline_playhead_position('[AE-QL]_D-L',1) # page function doesn't work if include of '[]'
            main_page.drag_media_to_timeline_playhead_position('LUT_Cinespace', 1)

            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_pip_apply_csp.png')
            logger(f"{preview_img_2=}")

            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_pip_apply_csp.png',
                                                      preview_img_2)
            logger(compare_result2)

            # undo the change
            #main_page.click_undo()

            # summary case result
            case.result = compare_result2 and result_status and result_status_1

        # 5/5
        with uuid("28f8fed2-cff4-4e19-9057-32490f484a8d") as case:
            # case2.5.2.6 : Apply *.cms LUT to pip object
            '''
            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            '''
            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)

            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)

            # select one of LUT
            # main_page.drag_media_to_timeline_playhead_position('[AE-QL]_D-L',1) # page function doesn't work if include of '[]'
            main_page.drag_media_to_timeline_playhead_position('AE-Buddy_Grunge', 1)

            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_pip_apply_cms.png')
            logger(f"{preview_img_2=}")

            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_pip_apply_cms.png',
                                                      preview_img_2)
            logger(compare_result2)

            # undo the change
            #main_page.click_undo()

            # summary case result
            case.result = compare_result2 and result_status and result_status_1

        # 5/5
        with uuid("79641225-91cc-475f-aa8e-c8a67bcbb2b0") as case:
            # case2.5.2.7 : Apply *.rv3dlut LUT to video file
            '''
            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            '''
            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)

            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)

            # select one of LUT
            # main_page.drag_media_to_timeline_playhead_position('[AE-QL]_D-L',1) # page function doesn't work if include of '[]'
            main_page.drag_media_to_timeline_playhead_position('AE-QL_DL_rv', 1)

            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_pip_apply_rv3dlut.png')
            logger(f"{preview_img_2=}")

            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_pip_apply_rv3dlut.png',
                                                      preview_img_2)
            logger(compare_result2)

            # undo the change
            #main_page.click_undo()

            # summary case result
            case.result = compare_result2 and result_status and result_status_1

        # 5/5
        with uuid("c4ea0df8-125e-4a9b-be46-554d153b46e9") as case:
            # case2.5.2.8 : Apply *.vf LUT to pip object
            '''
            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            '''
            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)

            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)

            # select one of LUT
            # main_page.drag_media_to_timeline_playhead_position('[AE-QL]_D-L',1) # page function doesn't work if include of '[]'
            main_page.drag_media_to_timeline_playhead_position('Demo_N_V', 1)

            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_pip_apply_vf.png')
            logger(f"{preview_img_2=}")

            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_pip_apply_vf.png',
                                                      preview_img_2)
            logger(compare_result2)

            # undo the change
            #main_page.click_undo()

            # summary case result
            case.result = compare_result2 and result_status and result_status_1

        # 5/5
        with uuid("9d273592-5fea-4e9e-a00a-fc02522e7b33") as case:
            # case2.5.2.9 : Apply *.clfr LUT to pip object
            '''
            # select 'effect room' & Color LUT in library
            main_page.enter_room(3)
            '''
            # check if PDR does enter effect room normally
            result_status = effect_room_page.check_effect_room()
            logger(result_status)

            # check if Color LUT category is selected
            result_status_1 = effect_room_page.select_specific_tag('Color LUT')
            logger(result_status_1)

            # select one of LUT
            # main_page.drag_media_to_timeline_playhead_position('[AE-QL]_D-L',1) # page function doesn't work if include of '[]'
            main_page.drag_media_to_timeline_playhead_position('portrait_aesthetic', 1)

            # take snapshot for timeline preview
            preview_img_2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                     file_name=Auto_Ground_Truth_Folder + 'preview_pip_apply_clfr.png')
            logger(f"{preview_img_2=}")

            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'preview_pip_apply_clfr.png',
                                                      preview_img_2)
            logger(compare_result2)

            # undo the change
            # main_page.click_undo() #marked this item in order to proceed next case

            # summary case result
            case.result = compare_result2 and result_status and result_status_1

        # @pytest.mark.skip
        # @exception_screenshot
        # def test1_1_1_3(self):
        # 4/16
        with uuid("fede8567-e266-4bcc-99e9-183bd4855a6f") as case:
            # case2.3.2.1 : Add imported LUT to My Favorites
            # time.sleep(5)
            # main_page.enter_room(3)
            effect_room_page.select_LibraryRoom_category('Color LUT')
            # main_page.select_library_icon_view_media('[AE] red gamma')
            main_page.select_library_icon_view_media('LUT_Cinespace')
            effect_room_page.right_click_addto('My Favorites')
            time.sleep(DELAY_TIME)

            effect_room_page.select_LibraryRoom_category('My Favorites')
            check_result = main_page.select_library_icon_view_media('LUT_Cinespace')
            case.result = check_result

        # 4/16
        with uuid("53d1ca7e-8241-4d40-98b7-3dd3775e220b") as case:
            # case2.3.2.3 : create custom tag and add imported LUT to custom tag
            # create new tag
            set_check = effect_room_page.add_effectroom_new_tag('123')
            logger(set_check)
            # switch to Color LUT to add imported LUT to custom tag
            effect_room_page.select_LibraryRoom_category('Color LUT')
            main_page.select_library_icon_view_media('LUT_Cinespace')
            effect_room_page.right_click_addto('123')
            time.sleep(DELAY_TIME)

            effect_room_page.select_LibraryRoom_category('123')
            check_result = main_page.select_library_icon_view_media('LUT_Cinespace')
            case.result = check_result

        # 4/16
        with uuid("a4b8fa50-17fa-4166-b0a1-f7b039c6cbcc") as case:
            # case2.3.4 : remove LUT from custom tag
            # select custom tag
            # effect_room_page.select_LibraryRoom_category('Color LUT')
            effect_room_page.select_LibraryRoom_category('123')
            main_page.select_library_icon_view_media('LUT_Cinespace')
            check_result = effect_room_page.remove_from_custom_tag(4,
                                                                   'LUT_Cinespace')  # The tag_index of 'My Favorite' is 0
            logger(check_result)
            # check_result = main_page.select_library_icon_view_media('LUT_Cinespace')
            # logger(check_result)
            # if not main_page.select_library_icon_view_media('LUT_Cinespace'):
            # return True
            # else:
            # return False
            # effect_room_1_1 = effect_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + 'G2.3.4_effect_room_remove_object.png')
            effect_room_1_1 = effect_room_page.snapshot(locator=L.effect_room.current_tag_amount,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.3.4_effect_room_remove_object.png')
            logger(f"{effect_room_1_1 =}")
            compare_result = effect_room_page.compare(Ground_Truth_Folder + 'G2.3.4_effect_room_remove_object.png',
                                                      effect_room_1_1)
            # compare_result = effect_room_page.image.search(Ground_Truth_Folder + 'G2.3.4_effect_room_remove_object.png', effect_room_1_1)
            logger(compare_result)
            # case.result = check_result and compare_result

        # 5/5
        with uuid("f9e30f35-e676-4b07-927a-99d971e3229a") as case:
            # case2.3.3.1 : Remove LUT from My Favorites
            # time.sleep(5)
            # main_page.enter_room(3)
            effect_room_page.select_LibraryRoom_category('Color LUT')
            # main_page.select_library_icon_view_media('[AE] red gamma')
            main_page.select_library_icon_view_media('LUT_Cinespace')
            effect_room_page.remove_from_favorites()
            time.sleep(DELAY_TIME)

            effect_room_page.select_LibraryRoom_category('My Favorites')
            # take snapshot for removed LUT list
            effect_room_1_1 = effect_room_page.snapshot(locator=L.effect_room.current_tag_amount,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.3.3.1_effect_room_remove_from_MyFavorite.png')
            logger(f"{effect_room_1_1 =}")
            compare_result = effect_room_page.compare(
                Ground_Truth_Folder + 'G2.3.3.1_effect_room_remove_from_MyFavorite.png',
                effect_room_1_1)
            logger(compare_result)
            case.result = compare_result

        # 5/5
        with uuid("9a53f6b1-465d-4c76-8a25-69f8c7c5e23e") as case:
            # case2.3.5 : A warning dialog pops up when deleting LUT
            # time.sleep(5)
            # main_page.enter_room(3)
            # select "Imported" and go to delete specific LUT file
            effect_room_page.select_LibraryRoom_category('Imported')
            main_page.select_library_icon_view_media('LUT_Cinespace')
            check_result = effect_room_page.right_click_remove_clut()
            logger(check_result)

            # take snapshot after removing one of LUT
            effect_room_1_1 = effect_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                        file_name=Auto_Ground_Truth_Folder + 'G2.3.5_effect_room_delete_LUT.png')
            logger(f"{effect_room_1_1 =}")
            compare_result = effect_room_page.compare(Ground_Truth_Folder + 'G2.3.5_effect_room_delete_LUT.png',
                                                      effect_room_1_1)
            logger(compare_result)
            case.result = compare_result and check_result

    @exception_screenshot
    def test_1_3_1(self):
        with uuid('c013a31c-f5d0-48e2-8011-923ab31beb14') as case:
            # Show "Color LUT(*Template Name*)" by tooltips
            case.result = None
            case.fail_log = "*Skip by AT*"