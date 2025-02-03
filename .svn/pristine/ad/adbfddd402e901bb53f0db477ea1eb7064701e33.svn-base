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
from pages.locator import locator as L, media_room

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
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="Media Room.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<



# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Media_Room/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Media_Room/'
Test_Material_Folder = app.testing_material

#Ground_Truth_Folder = '/Users/clt/Desktop/Ernesto_MacAT/SFT/GroundTruth/Media_Room/'
#Auto_Ground_Truth_Folder = '/Users/clt/Desktop/Ernesto_MacAT/SFT/ATGroundTruth/Media_Room/'
#Test_Material_Folder = '/Users/clt/Desktop/Ernesto_MacAT/Material/'

DELAY_TIME = 1



'''
@pytest.fixture(scope="module", autouse= True)
def init():
    yield
    report.export()
    report.show()
'''




class Test_Media_Room():

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
            google_sheet_execution_log_init('Media_Room')

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
            f"media room result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
    def test1_1_2_1(self):

        # switch to color board

        with uuid("9fbc4bb9-8600-4cf5-8cdd-d4cb37bb8478") as case:
            # select 'color board' in media room
            time.sleep(DELAY_TIME * 2)
            media_room_page.enter_color_boards()
            time.sleep(DELAY_TIME * 2)
            # select the 2nd object '0,120,255' and insert to timeline
            media_room_page.hover_library_media('0,120,255')
            #media_room_page.right_click()
            #media_room_page.select_right_click_menu('Insert on Selected Track')
            # snapshot for current list view
            color_board_status = media_room_page.snapshot(locator=L.media_room.tag_color_boards, file_name=Auto_Ground_Truth_Folder + 'G1_1_2_2-1.png', )
            logger(f"{color_board_status=}")
            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'G1_1_2_2-1.png', color_board_status)
            logger(compare_result1)
            # snapshot for current media library list view
            #preview_img_cb = media_room_page.snapshot(locator=media_room_page.area.preview.main)
            #logger(f"{preview_img_cb=}")
            list_view_cb = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + 'G1_1_2_2-2.png')
            logger(f"{list_view_cb=}")
            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'G1_1_2_2-2.png', list_view_cb)
            logger(compare_result2)
            # remove inserted color board from timeline by tap del key / new workspace by hotkey
            time.sleep(DELAY_TIME * 2)
            #media_room_page.tap_Remove_hotkey()
            media_room_page.tap_NewWorkspace_hotkey()
            time.sleep(DELAY_TIME * 2)
            case.result = compare_result1 and compare_result2


            # switch to Sound Clips
        with uuid("3032810e-0e6a-41de-9eb1-f99e498d1813") as case:
            # select 'sound clips' in media room
            media_room_page.enter_sound_clips()
            # snapshot for current list view of each room
            SFX_status = media_room_page.snapshot(locator=L.media_room.tag_sound_clips, file_name=Auto_Ground_Truth_Folder + 'G1_1_2_4-1.png')
            logger(f"{SFX_status=}")
            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'G1_1_2_4-1.png', SFX_status)
            logger(compare_result1)
            #current_library_list_view_sfx = media_room_page.snapshot(locator=L.media_room.library_listview.unit_collection_view_item_image) #unit_collection_view_item_image --> not suitable
            list_icon_sfx = media_room_page.snapshot(locator=L.media_room.scroll_area.list_icon_music, file_name=Auto_Ground_Truth_Folder + 'G1_1_2_4-2.png')
            logger(f"{list_icon_sfx=}")
            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'G1_1_2_4-2.png',list_icon_sfx)
            logger(compare_result2)
            case.result = compare_result1 and compare_result2

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_2_2(self):
        # switch to Background Music
        with uuid("89ee141b-b702-4975-b875-1daa0021802e") as case:
            # select 'BGM' in media room
            media_room_page.enter_background_music()
            # snapshot for current list view of each room
            time.sleep(DELAY_TIME*3)
            # download one of BGM
            BGM_status = media_room_page.snapshot(locator=L.media_room.tag_background_music, file_name=Auto_Ground_Truth_Folder + 'G1_1_2_3-1.png')
            logger(f"{BGM_status=}")
            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'G1_1_2_3-1.png', BGM_status)
            logger(compare_result1)
            # snapshot for current media library list icon
            list_icon_bgm = media_room_page.snapshot(locator=L.media_room.scroll_area.list_icon_music, file_name=Auto_Ground_Truth_Folder + 'G1_1_2_3-2.png')
            logger(f"{list_icon_bgm=}")
            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'G1_1_2_3-2.png', list_icon_bgm)
            logger(compare_result2)
            case.result = compare_result1 and compare_result2

        # switch to media content
        with uuid("fcd27665-138d-4f03-93f7-cdb602e6ab35") as case:
            # select 'media content' in media room
            media_room_page.enter_media_content()
            # snapshot for current list view of each room
            media_content_status = media_room_page.snapshot(locator=L.media_room.tag_media_content, file_name=Auto_Ground_Truth_Folder + 'G1_1_2_1-1.png')
            logger(f"{media_content_status=}")
            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'G1_1_2_1-1.png', media_content_status)
            logger(compare_result1)
            # Insert selected clip to timeline (via context menu)
            media_room_page.hover_library_media('Food.jpg')
            media_room_page.right_click()
            media_room_page.select_right_click_menu('Insert on Selected Track')
            time.sleep(DELAY_TIME*1.5)
            preview_img_mc = media_room_page.snapshot(locator=media_room_page.area.preview.main, file_name=Auto_Ground_Truth_Folder + 'G1_1_2_1-2.png')
            logger(f"{preview_img_mc=}")
            # compare with ground truth
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'G1_1_2_1-2.png', preview_img_mc)
            logger(compare_result2)
            case.result = compare_result1 and compare_result2

        # switch to display video only
        with uuid("24b2de54-45fe-4285-8cd5-f411c85ce4c9") as case:
            # select 'media content' in media room
            media_room_page.enter_media_content()
            # select "display video only" to filter out other materials
            time.sleep(DELAY_TIME)
            media_room_page.media_filter_display_video_only()
            media_filter_video = media_room_page.snapshot(locator=L.media_room.btn_media_filter_display_video_only, file_name=Auto_Ground_Truth_Folder + 'G2.2.1_Media_Filter_Video_Only.png')
            logger(f"{media_filter_video=}")
            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'G2.2.1_Media_Filter_Video_Only.png', media_filter_video)
            logger(compare_result1)
            media_filter_video_1 = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + 'G2.2.1_Media_Filter_Video_Only_1.png')
            logger(f"{media_filter_video_1=}")
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'G2.2.1_Media_Filter_Video_Only_1.png',media_filter_video_1)
            logger(compare_result2)
            case.result = compare_result1 and compare_result2
            time.sleep(DELAY_TIME)

        with uuid("0ee100dc-aeaf-484b-be30-3bf2e745fdae") as case:
            # select 'media content' in media room
            time.sleep(DELAY_TIME)
            #media_room_page.enter_media_content()
            # select "display image only" to filter out other materials
            media_room_page.media_filter_display_image_only()
            media_filter_image = media_room_page.snapshot(locator=L.media_room.btn_media_filter_display_image_only, file_name=Auto_Ground_Truth_Folder + 'G2.2.2_Media_Filter_Image_Only.png')
            logger(f"{media_filter_image=}")
            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'G2.2.2_Media_Filter_Image_Only.png', media_filter_image)
            logger(compare_result1)
            media_filter_image_1 = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + 'G2.2.2_Media_Filter_Image_Only_1.png')
            logger(f"{media_filter_image_1=}")
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'G2.2.2_Media_Filter_Image_Only_1.png',media_filter_image_1)
            logger(compare_result2)
            case.result = compare_result1 and compare_result2

        with uuid("ffa5d1c8-e601-4c0d-a660-fdaeb2fbfd5a") as case:
            # select 'media content' in media room
            time.sleep(DELAY_TIME * 2)
            #media_room_page.enter_media_content()
            # select "display audio only" to filter out other materials
            media_room_page.media_filter_display_audio_only()
            time.sleep(DELAY_TIME * 2)
            media_filter_audio = media_room_page.snapshot(locator=L.media_room.btn_media_filter_display_audio_only, file_name=Auto_Ground_Truth_Folder + 'G2.2.3_Media_Filter_Audio_Only.png')
            logger(f"{media_filter_audio=}")
            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'G2.2.3_Media_Filter_Audio_Only.png', media_filter_audio)
            logger(compare_result1)
            media_filter_audio_1 = media_room_page.snapshot(locator=media_room_page.area.library_detail_view, file_name=Auto_Ground_Truth_Folder + 'G2.2.3_Media_Filter_Audio_Only_1.png')
            logger(f"{media_filter_audio_1=}")
            #list_icon_audio = media_room_page.snapshot(locator=L.media_room.scroll_area.list_icon_music)
            #logger(f"{list_icon_audio=}")
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'G2.2.3_Media_Filter_Audio_Only_1.png', media_filter_audio_1)
            #compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'G2.2.3_Media_Filter_Audio_Only_1.png', list_icon_audio)
            logger(compare_result2)
            case.result = compare_result1 and compare_result2

        with uuid("01254730-617d-4ba7-9dd1-16d62ec7244b") as case:
            # select 'media content' in media room
            time.sleep(DELAY_TIME * 2)
            #media_room_page.enter_media_content()
            # select "display all media" to filter out other materials
            media_room_page.media_filter_display_all()
            media_filter_all = media_room_page.snapshot(locator=L.media_room.btn_media_filter_all, file_name=Auto_Ground_Truth_Folder + 'G2.2.0_Media_Filter_All.png')
            logger(f"{media_filter_all=}")
            # compare with ground truth
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'G2.2.0_Media_Filter_All.png', media_filter_all)
            logger(compare_result1)
            media_filter_all_1 = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + 'G2.2.0_Media_Filter_All_1.png')
            logger(f"{media_filter_all_1=}")
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'G2.2.0_Media_Filter_All_1.png',media_filter_all_1)
            logger(compare_result2)
            case.result = compare_result1 and compare_result2


    #@pytest.mark.skip
    @exception_screenshot
    def test1_1_2_3(self):
        # library menu sort by type
        with uuid("8b774821-ecaa-448b-95eb-a399c82f711e") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.library_menu_sort_by_type()
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + 'G2.3.0_LibraryMenu_SortByType.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.3.0_LibraryMenu_SortByType.png', library_result)
            case.result = current_result and compare_result

        # library menu sort by Modified Date
        with uuid("ad0ac59e-3862-47de-8298-4b293c4cc1f9") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.library_menu_sort_by_modified_date()
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.3.1_LibraryMenu_SortByModifiedDate.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.3.1_LibraryMenu_SortByModifiedDate.png',
                                                     library_result)
            case.result = current_result and compare_result
            media_room_page.library_menu_sort_by_modified_date()
        # library menu sort by Created Date
        with uuid("f2b9a62b-cf02-4b0a-bc61-0e4570002448") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.library_menu_sort_by_created_date()
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.3.2_LibraryMenu_SortByCreatedDate.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.3.2_LibraryMenu_SortByCreatedDate.png',
                                                     library_result)
            case.result = current_result and compare_result
            media_room_page.library_menu_sort_by_created_date()

        # library menu sort by File Size
        with uuid("b578675d-6224-482b-8d22-b9147e594224") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.library_menu_sort_by_file_size()
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.3.3_LibraryMenu_SortByFileSize.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.3.3_LibraryMenu_SortByFileSize.png',
                                                     library_result)
            case.result = current_result and compare_result

        # library menu sort by Duration
        with uuid("205a9a74-8b0b-4fe1-ab78-5a411c9a8587") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.library_menu_sort_by_duration()
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.3.4_LibraryMenu_SortByDuration.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.3.4_LibraryMenu_SortByDuration.png',
                                                     library_result)
            case.result = current_result and compare_result

        # library menu sort by Name
        with uuid("e3281a29-a1ee-4486-8762-ec2bf0e1f6f7v") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.library_menu_sort_by_name()
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.3.5_LibraryMenu_SortByName.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.3.5_LibraryMenu_SortByName.png',
                                                     library_result)
            case.result = current_result and compare_result


    #@pytest.mark.skip
    @exception_screenshot
    def test1_1_2_4(self):
        # details view
        with uuid("0d60dc50-7f2c-44e7-8e19-92f52cd4c969") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = main_page.click_library_details_view()
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.4.0_DetailsView.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.4.0_DetailsView.png',
                                                     library_result)
            case.result = current_result and compare_result

        # icon view
        with uuid("23d587d0-c777-4575-85c7-d9a4f730bceb") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = main_page.click_library_icon_view()
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.4.1_IconView.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.4.1_IconView.png',
                                                     library_result)
            case.result = current_result and compare_result


    #@pytest.mark.skip
    @exception_screenshot
    def test1_1_2_5(self):
        # library menu select all
        with uuid("fea53bb4-8cd7-4a8e-a5c0-4018054b72fc") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.library_menu_select_all()
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.5.0_LibraryMenu_SelectAll.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.5.0_LibraryMenu_SelectAll.png',
                                                     library_result)
            case.result = current_result and compare_result

        # library menu extra large icon
        with uuid("96a2787d-9a1d-4b5d-b19c-08a82b2880d0") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.library_menu_extra_large_icons()
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.5.1_LibraryMenu_ExtraLargeIcons.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.5.1_LibraryMenu_ExtraLargeIcons.png',
                                                     library_result)
            case.result = current_result and compare_result

        # library menu large icon
        with uuid("aff76bb1-cf74-4a46-93fa-86ae0f6d0e1d") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.library_menu_large_icons()
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.5.2_LibraryMenu_LargeIcons.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.5.2_LibraryMenu_ExtraLargeIcons.png',
                                                     library_result)
            case.result = current_result and compare_result

        # library menu small icon
        with uuid("3cf4759e-b661-4a94-a724-0aa13900e544") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.library_menu_small_icons()
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.5.3_LibraryMenu_SmallIcons.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.5.3_LibraryMenu_SmallIcons.png',
                                                     library_result)
            case.result = current_result and compare_result

        # library menu medium icon
        with uuid("03ab1863-d47f-4eb2-92b4-456048a143c6") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.library_menu_medium_icons()
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.5.4_LibraryMenu_MediumIcons.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.5.4_LibraryMenu_MediumIcons.png',
                                                     library_result)
            case.result = current_result and compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test1_1_2_6(self):
        # library menu remove all unused
        with uuid("918605d7-7d45-4d20-96b1-cc30bc848afa") as case:
            time.sleep(DELAY_TIME * 2)
            main_page.insert_media("Food.jpg")
            time.sleep(DELAY_TIME * 4)

            current_result = media_room_page.library_menu_remove_all_unused_content_from_library()
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.6.0_LibraryMenu_RemoveAllUnused.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.6.0_LibraryMenu_RemoveAllUnused.png',
                                                     library_result)
            case.result = current_result and compare_result

        # empty the library
        with uuid("1dfec1a8-b9cb-40e1-b6c1-ba7daf69ff6b") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.library_menu_empty_the_library()
            time.sleep(DELAY_TIME * 2)

            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.6.1_LibraryMenu_EmptyTheLibrary.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.6.1_LibraryMenu_EmptyTheLibrary.png',
                                                     library_result)
            case.result = current_result and compare_result



    #@pytest.mark.skip
    @exception_screenshot
    def test1_1_2_7(self):
        # search media library
        with uuid("964ae170-8c57-4119-8214-a4ec8ad2139d") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.search_library('Foo')
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.7.0_SearchLibrary.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.7.0_SearchLibrary.png',
                                                     library_result)
            case.result = current_result and compare_result

        # cancel search
        with uuid("a7bb49a3-c9e2-4923-b8c4-0dc0417558ea") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.search_library_click_cancel()
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.7.1_CancelSearch.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.7.1_CancelSearch.png',
                                                     library_result)
            case.result = current_result and compare_result


        # library_resultqqq = media_room_page.snapshot(locator=L.media_room.tag_scroll_view_frame,
        #                                                       file_name=Auto_Ground_Truth_Folder + '111.png')


    #@pytest.mark.skip
    @exception_screenshot
    def test1_1_2_8(self):
        # Hide explorer view
        with uuid("3e7d5fee-c602-40ce-ba25-cb3b52c04aed") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.click_display_hide_explore_view()
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.8.0_HideExplorerView.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.8.0_HideExplorerView.png',
                                                     library_result)
            case.result = current_result and compare_result

        # Display explorer view
        with uuid("d4e4025b-1b25-496e-a378-31d8678a6979") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.click_display_hide_explore_view()
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.8.1_DisplayExplorerView.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.8.1_DisplayExplorerView.png',
                                                     library_result)
            case.result = current_result and compare_result

        # add new tag
        with uuid("c2d95d57-2848-4848-a5ee-8d4526174f17") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.add_new_tag('abc')
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.media_room.tag_scroll_view_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.8.2_AddNewTag.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.8.2_AddNewTag.png',
                                                     library_result)
            case.result = current_result and compare_result

        # add new tag with exist name
        with uuid("8c7eaf7e-9405-42ee-80f1-6cc6ca9c0944") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.add_new_tag('abc')
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.tag_scroll_view_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.8.3_AddNewTagWithExistName.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.8.3_AddNewTagWithExistName.png',
                                                     library_result)
            case.result = (not current_result) and compare_result


        # delete default tag (gray out)
        with uuid("244a4e45-dac2-4f3c-a15e-c1f23b7e3cd2") as case:
            time.sleep(DELAY_TIME * 2)

            library_result = media_room_page.snapshot(locator=L.media_room.btn_delete_tag,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.8.4_DeleteDefaultTag.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.8.4_DeleteDefaultTag.png',
                                                     library_result)
            case.result = compare_result

        # delete tag
        with uuid("59bf780e-f675-4902-a518-891b07a74829") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.delete_tag('abc')
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.tag_scroll_view_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.8.5_DeleteTag.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.8.5_DeleteTag.png',
                                                     library_result)
            case.result = current_result and compare_result

        # mouse hovor media content to show tool tip
        with uuid("a69a2dba-5bf9-4a91-be15-a475edcf9a12") as case:
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.hover_library_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.8.6_HovorOnClip.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.8.6_HovorOnClip.png',
                                                     library_result)
            case.result = compare_result

        # right click to insert to selected track
        with uuid("4410585d-96ef-4658-a4e0-56f338eb745e") as case:
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.library_clip_context_menu_insert_on_selected_track()
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=media_room_page.area.timeline,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.8.7_RightClickInsertVideoToTimeline.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.8.7_RightClickInsertVideoToTimeline.png',
                                                     library_result)
            case.result = compare_result and current_result


        # right click remove from library
        with uuid("e070cee1-109f-4ce7-ab49-478334c143da") as case:
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media('Skateboard 02.mp4')
            time.sleep(DELAY_TIME)
            current_result = media_room_page.library_clip_context_menu_remove_from_library()
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.8.8_RightClickRemoveFromLibrary.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.8.8_RightClickRemoveFromLibrary.png',
                                                     library_result)
            case.result = compare_result and current_result

        # add to new tag
        with uuid("f0588371-9d28-4481-ab5c-d6945e2c5904") as case:
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media('Skateboard 03.mp4')
            time.sleep(DELAY_TIME)
            current_result = media_room_page.library_clip_context_menu_add_to('New Tag')
            time.sleep(DELAY_TIME * 2)
            media_room_page.select_specific_category('New Tag')
            library_result1 = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.8.9_RightClickAddTo1.png')
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'G2.8.9_RightClickAddTo1.png',
                                                     library_result1)
            library_result2 = media_room_page.snapshot(locator=L.media_room.tag_scroll_view_frame,
                                                       file_name=Auto_Ground_Truth_Folder + 'G2.8.9_RightClickAddTo2.png')
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'G2.8.9_RightClickAddTo2.png',
                                                      library_result2)

            case.result = compare_result1 and compare_result2 and current_result


        # right click change alias
        with uuid("0d6ae109-90e8-4ce4-aea7-e8f7314a681d") as case:
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media('Skateboard 03.mp4')
            time.sleep(DELAY_TIME)
            current_result = media_room_page.library_clip_context_menu_change_alias('aaa')
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.8.10_RightClickChangeAlias.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.8.10_RightClickChangeAlias.png',
                                                     library_result)
            case.result = compare_result and current_result

        # right click reset alias
        with uuid("f570bc0f-19f7-4c21-9502-106f60be1e3d") as case:
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media('aaa')
            time.sleep(DELAY_TIME)
            current_result = media_room_page.library_clip_context_menu_reset_alias('Skateboard 03.mp4')
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.8.11_RightClickResetAlias.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.8.11_RightClickResetAlias.png',
                                                     library_result)
            case.result = compare_result and current_result

        # right click find in timeline
        with uuid("f1ed742d-2ede-4bdb-91db-707e6cc1821d") as case:
            time.sleep(DELAY_TIME * 2)
            media_room_page.enter_media_content()
            time.sleep(DELAY_TIME)
            main_page.select_library_icon_view_media('Skateboard 01.mp4')
            time.sleep(DELAY_TIME)
            current_result = media_room_page.library_clip_context_menu_find_in_timeline('Skateboard 01.mp4')
            time.sleep(DELAY_TIME)
            media_room_page.close_library_clip_find_in_timeline_confirm_dialog()
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.8.12_RightClickFindInTimeline.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.8.12_RightClickFindInTimeline.png',
                                                     library_result)
            case.result = compare_result and current_result


    #@pytest.mark.skip
    @exception_screenshot
    def test1_1_2_9(self):
        # right click insert image to timeline
        with uuid("a070f4f5-a970-4d00-a7f5-24df5fd361b6") as case:
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media('Food.jpg')
            time.sleep(DELAY_TIME)
            current_result = media_room_page.library_clip_context_menu_insert_on_selected_track()
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=media_room_page.area.timeline,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.9.0_RightClickInsertImageToTimeline.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.9.0_RightClickInsertImageToTimeline.png',
                                                     library_result)
            case.result = compare_result and current_result

        # right click remove from library
        with uuid("14b9a6a9-278e-474b-a5b1-83d7bbe3f492") as case:
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media('Landscape 01.jpg')
            time.sleep(DELAY_TIME)
            current_result = media_room_page.library_clip_context_menu_remove_from_library()
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.9.1_RightClickRemoveFromLibrary.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.9.1_RightClickRemoveFromLibrary.png',
                                                     library_result)
            case.result = compare_result and current_result


        # right click add to
        with uuid("94dd4a2a-693f-48fe-941d-c98cfeb2c394") as case:
            time.sleep(DELAY_TIME * 2)
            media_room_page.add_new_tag('abc')
            time.sleep(DELAY_TIME)
            main_page.select_library_icon_view_media('Landscape 02.jpg')
            time.sleep(DELAY_TIME)
            current_result = media_room_page.library_clip_context_menu_add_to('abc')
            time.sleep(DELAY_TIME)
            media_room_page.select_specific_category('abc')
            library_result1 = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                       file_name=Auto_Ground_Truth_Folder + 'G2.9.2_RightClickAddTo1.png')
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'G2.9.2_RightClickAddTo1.png',
                                                      library_result1)
            library_result2 = media_room_page.snapshot(locator=L.media_room.tag_scroll_view_frame,
                                                       file_name=Auto_Ground_Truth_Folder + 'G2.9.2_RightClickAddTo2.png')
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'G2.9.2_RightClickAddTo2.png',
                                                      library_result2)
            case.result = compare_result1 and compare_result2 and current_result

        # right click change alias
        with uuid("b520668a-26d5-4dcd-9f42-21d88e663a33") as case:
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media('Landscape 02.jpg')
            time.sleep(DELAY_TIME)
            current_result = media_room_page.library_clip_context_menu_change_alias('aaa')
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.9.3_RightClickChangeAlias.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.9.3_RightClickChangeAlias.png',
                                                     library_result)
            case.result = compare_result and current_result

        # right click reset alias
        with uuid("8527c524-42d8-4779-927d-743044272c9b") as case:
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media('aaa')
            time.sleep(DELAY_TIME)
            current_result = media_room_page.library_clip_context_menu_reset_alias('Landscape 02.jpg')
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.9.4_RightClickResetAlias.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.9.4_RightClickResetAlias.png',
                                                     library_result)
            case.result = compare_result and current_result

        # right click rotate right
        with uuid("550a728e-c4e1-4266-b6ee-3e09dbb57a12") as case:
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media('Landscape 02.jpg')
            time.sleep(DELAY_TIME)
            current_result = media_room_page.library_clip_context_menu_rotate_right()
            time.sleep(DELAY_TIME)
            library_result1 = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.9.5_RightClickRotateRight1.png')
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'G2.9.5_RightClickRotateRight1.png',
                                                     library_result1)
            library_result2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                       file_name=Auto_Ground_Truth_Folder + 'G2.9.5_RightClickRotateRight2.png')
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'G2.9.5_RightClickRotateRight2.png',
                                                      library_result2)
            case.result = compare_result1 and compare_result2 and current_result

        # right click rotate left
        with uuid("43a1d452-b034-4073-bc12-e2c47cd1c27f") as case:
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media('Landscape 02.jpg')
            time.sleep(DELAY_TIME)
            current_result = media_room_page.library_clip_context_menu_rotate_left()
            time.sleep(DELAY_TIME)
            library_result1 = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.9.6_RightClickRotateLeft1.png')
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'G2.9.6_RightClickRotateLeft1.png',
                                                     library_result1)
            library_result2 = media_room_page.snapshot(locator=media_room_page.area.preview.main,
                                                       file_name=Auto_Ground_Truth_Folder + 'G2.9.6_RightClickRotateLeft2.png')
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'G2.9.6_RightClickRotateLeft2.png',
                                                      library_result2)
            case.result = compare_result1 and compare_result2 and current_result

        # right click move to trash can
        with uuid("8c5f4e45-3f6b-46e0-b946-259b926d9e7c") as case:
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media('Landscape 02(0).jpg')
            time.sleep(DELAY_TIME)
            media_room_page.library_clip_context_menu_move_to_trash_can()
            time.sleep(DELAY_TIME * 2)
            main_page.select_library_icon_view_media('Landscape 02(1).jpg')
            time.sleep(DELAY_TIME)
            media_room_page.library_clip_context_menu_move_to_trash_can()
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                       file_name=Auto_Ground_Truth_Folder + 'G2.9.7_RightClickMoveToTrashCan.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.9.7_RightClickMoveToTrashCan.png',
                                                      library_result)
            case.result = compare_result

        # right click find in timeline
        with uuid("1a784820-0f84-459a-9f12-a59c9456cbd7") as case:
            time.sleep(DELAY_TIME * 2)
            media_room_page.enter_media_content()
            time.sleep(DELAY_TIME)
            main_page.select_library_icon_view_media('Food.jpg')
            time.sleep(DELAY_TIME)
            current_result = media_room_page.library_clip_context_menu_find_in_timeline('Food.jpg')
            time.sleep(DELAY_TIME)
            media_room_page.close_library_clip_find_in_timeline_confirm_dialog()
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.9.8_RightClickFindInTimeline.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.9.8_RightClickFindInTimeline.png',
                                                     library_result)
            case.result = compare_result and current_result



    #@pytest.mark.skip
    @exception_screenshot
    def test1_1_2_10(self):
        # right click insert audio to timeline
        with uuid("6960ebfa-b473-4c7f-be3f-9609bc281e5f") as case:
            main_page.select_library_icon_view_media('Mahoroba.mp3')
            current_result = media_room_page.library_clip_context_menu_insert_on_selected_track()
            library_result = media_room_page.snapshot(locator=media_room_page.area.timeline,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.10.0_RightClickInsertAudioToTimeline.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.10.0_RightClickInsertAudioToTimeline.png',
                                                     library_result)
            case.result = compare_result and current_result

        # right click remove from library
        with uuid("094e5256-0acd-461d-a064-78d7fee8748e") as case:
            main_page.select_library_icon_view_media('Speaking Out.mp3')
            current_result = media_room_page.library_clip_context_menu_remove_from_library()
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.10.1_RightClickRemoveFromLibrary.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.10.1_RightClickRemoveFromLibrary.png',
                                                     library_result)
            case.result = compare_result and current_result

        # right click add to
        with uuid("8b5632de-6a63-4cd6-9b80-33c06e9305dd") as case:
            media_room_page.add_new_tag('ccc')
            main_page.select_library_icon_view_media('Mahoroba.mp3')
            current_result = media_room_page.library_clip_context_menu_add_to('ccc')
            media_room_page.select_specific_category('ccc')
            library_result1 = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                       file_name=Auto_Ground_Truth_Folder + 'G2.10.2_RightClickAddTo1.png')
            compare_result1 = media_room_page.compare(Ground_Truth_Folder + 'G2.10.2_RightClickAddTo1.png',
                                                      library_result1)
            library_result2 = media_room_page.snapshot(locator=L.media_room.tag_scroll_view_frame,
                                                       file_name=Auto_Ground_Truth_Folder + 'G2.10.2_RightClickAddTo2.png')
            compare_result2 = media_room_page.compare(Ground_Truth_Folder + 'G2.10.2_RightClickAddTo2.png',
                                                      library_result2)
            case.result = compare_result1 and compare_result2 and current_result

        # right click change alias
        with uuid("7f2dc96e-95bd-4a8b-bf45-df8f7cfad45a") as case:
            main_page.select_library_icon_view_media('Mahoroba.mp3')
            current_result = media_room_page.library_clip_context_menu_change_alias('aaa')
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.10.3_RightClickChangeAlias.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.10.3_RightClickChangeAlias.png',
                                                     library_result)
            case.result = compare_result and current_result

        # right click reset alias
        with uuid("d258dfa5-120f-4c82-a235-3dfc4b09f36d") as case:
            main_page.select_library_icon_view_media('aaa')
            current_result = media_room_page.library_clip_context_menu_reset_alias('Mahoroba.mp3')
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.10.4_RightClickResetAlias.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.10.4_RightClickResetAlias.png',
                                                     library_result)
            case.result = compare_result and current_result

        # right click find in timeline
        with uuid("eb59f8bc-08e2-4c5f-bec3-5bcbaf5f2024") as case:
            media_room_page.enter_media_content()
            main_page.select_library_icon_view_media('Mahoroba.mp3')
            current_result = media_room_page.library_clip_context_menu_find_in_timeline('Mahoroba.mp3')
            media_room_page.close_library_clip_find_in_timeline_confirm_dialog()
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.10.5_RightClickFindInTimeline.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.10.5_RightClickFindInTimeline.png',
                                                     library_result)
            case.result = compare_result and current_result



    #@pytest.mark.skip
    @exception_screenshot
    def test1_1_2_11(self):
        # import media file
        with uuid("9a369994-c552-4b56-bd61-16260f17f474") as case:
            time.sleep(DELAY_TIME*2)
            current_result = media_room_page.import_media_file(Test_Material_Folder + '001.jpg')
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.11.0_ImportMediaFile.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.11.0_ImportMediaFile.png',
                                                     library_result)
            case.result = compare_result and current_result

        # import media folder
        with uuid("9c388210-c035-4f43-95be-5dedce609b39") as case:
            current_result = media_room_page.import_media_folder(Test_Material_Folder + 'import folder')
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.11.1_ImportMediaFolder.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.11.1_ImportMediaFolder.png',
                                                     library_result)
            case.result = compare_result and current_result


    #@pytest.mark.skip
    @exception_screenshot
    def test1_1_2_12(self):
        # right click import media file
        with uuid("bc203099-4305-4af9-aa8a-becd972fd11b") as case:
            time.sleep(DELAY_TIME*2)
            current_result = media_room_page.collection_view_right_click_import_media_files(Test_Material_Folder + '001.jpg')
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.12.0_RightClickImportMediaFile.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.12.0_RightClickImportMediaFile.png',
                                                     library_result)
            case.result = compare_result and current_result

        # right click import media folder
        with uuid("21427ecc-d454-4aa4-a72b-1f477467f19d") as case:
            time.sleep(DELAY_TIME*2)
            current_result = media_room_page.collection_view_right_click_import_a_media_folder(Test_Material_Folder + 'import folder')
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.12.1_RightClickImportMediaFolder.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.12.1_RightClickImportMediaFolder.png',
                                                     library_result)
            case.result = compare_result and current_result

        # right click select all
        with uuid("d2d6dbcd-54e6-4d29-b786-cc58f82d320b") as case:
            current_result = media_room_page.collection_view_right_click_select_all()
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.12.2_RightClickSelectAll.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.12.2_RightClickSelectAll.png',
                                                     library_result)
            case.result = compare_result and current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_2_13(self):
        # right click remove unused
        with uuid("442afa47-3859-4412-aca4-7d719fb31208") as case:
            time.sleep(DELAY_TIME*2)
            main_page.select_library_icon_view_media('Food.jpg')
            media_room_page.library_clip_context_menu_insert_on_selected_track()
            current_result = media_room_page.collection_view_right_click_remove_all_unused_content_from_library()
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.13.0_RightClickRemoveUnused.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.13.0_RightClickRemoveUnused.png',
                                                     library_result)
            case.result = compare_result and current_result

        # right click empty library
        with uuid("b7ec5b54-cb31-4bf0-8e0f-333f4a26c2b2") as case:
            current_result = media_room_page.collection_view_right_click_empty_library()
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.13.1_RightClickEmptyLibrary.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.13.1_RightClickEmptyLibrary.png',
                                                     library_result)
            case.result = compare_result and current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_2_14(self):
        # right click sort by type
        with uuid("05a2fab1-f7e9-4b1f-8205-4ea7f8df8537") as case:
            time.sleep(DELAY_TIME*2)
            current_result = media_room_page.collection_view_right_click_sort_by_type()
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.14.0_RightClickSortByType.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.14.0_RightClickSortByType.png',
                                                     library_result)
            case.result = compare_result and current_result

        # right click sort by modified date
        with uuid("d4612def-36b3-4d9a-a687-6b5ff85f5a17") as case:
            current_result = media_room_page.collection_view_right_click_sort_by_modified_date()
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.14.1_RightClickSortByModifiedDate.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.14.1_RightClickSortByModifiedDate.png',
                                                     library_result)
            case.result = compare_result and current_result
            media_room_page.collection_view_right_click_sort_by_modified_date()

        # right click sort by created date
        with uuid("e3994e41-8c2c-41d8-a280-c70a0804ec79") as case:
            current_result = media_room_page.collection_view_right_click_sort_by_created_date()
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.14.2_RightClickSortByCreatedDate.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.14.2_RightClickSortByCreatedDate.png',
                                                     library_result)
            case.result = compare_result and current_result
            media_room_page.collection_view_right_click_sort_by_created_date()

        # right click sort by file size
        with uuid("cc3b7b0a-1722-40e9-84f6-42f2ef57f766") as case:
            current_result = media_room_page.collection_view_right_click_sort_by_file_size()
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.14.3_RightClickSortByFileSize.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.14.3_RightClickSortByFileSize.png',
                                                     library_result)
            case.result = compare_result and current_result

        # right click sort by duration
        with uuid("b664de09-f040-42d1-97f4-993bfc4cedd6") as case:
            current_result = media_room_page.collection_view_right_click_sort_by_duration()
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.14.4_RightClickSortByDuration.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.14.4_RightClickSortByDuration.png',
                                                     library_result)
            case.result = compare_result and current_result

        # right click sort by name
        with uuid("a530558f-0062-4e3c-9202-d0f367af6eb3") as case:
            current_result = media_room_page.collection_view_right_click_sort_by_name()
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.14.5_RightClickSortByName.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.14.5_RightClickSortByName.png',
                                                     library_result)
            case.result = compare_result and current_result



    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_2_15(self):
        # color board create from color selector
        with uuid("444692ff-9959-4a70-b772-18f709c4b6f3") as case:
            time.sleep(DELAY_TIME * 2)
            media_room_page.enter_color_boards()
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.color_board_create_new_color_board('C0E351')
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.15.0_CreateColorBoardFromSelector.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.15.0_CreateColorBoardFromSelector.png',
                                                     library_result)

            case.result = compare_result and current_result

        # color board details view
        with uuid("7b32435f-a64a-473f-8707-673e1b026671") as case:
            current_result = main_page.click_library_details_view()
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.15.1_ColorBoardDetailsView.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.15.1_ColorBoardDetailsView.png',
                                                     library_result)
            case.result = compare_result and current_result

        # color board icon view
        with uuid("b978a14f-d525-4365-aa0c-8ddeabb781b9") as case:
            current_result = main_page.click_library_icon_view()
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.15.2_ColorBoardIconView.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.15.2_ColorBoardIconView.png',
                                                     library_result)
            case.result = compare_result and current_result

        # color board library menu create from color selector
        with uuid("7330feb1-7c7a-4cc2-8076-e7bd6a67762e") as case:
            current_result = media_room_page.library_menu_new_color_board('1A2EB5')
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.15.3_LibraryMenuCreateColorBoardFromSelector.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.15.3_LibraryMenuCreateColorBoardFromSelector.png',
                                                     library_result)

            case.result = compare_result and current_result

        # color board library menu restore to default
        with uuid("55e7b701-3dd8-4d14-91cf-cb5292919730") as case:
            current_result = media_room_page.library_menu_restore_to_defaults()
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.15.4_LibraryMenuRestoreToDefault.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.15.4_LibraryMenuRestoreToDefault.png',
                                                     library_result)

            case.result = compare_result and current_result

        # color board library menu sort by date
        with uuid("ff420f15-7ac0-4edb-8c1f-465717224d7f") as case:
            current_result = media_room_page.library_menu_sort_by_date()
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.15.5_LibraryMenuSortByDate.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.15.5_LibraryMenuSortByDate.png',
                                                     library_result)

            case.result = compare_result and current_result

        # color board library menu sort by B
        with uuid("effe331a-fc0d-4609-875f-7436fbe2be10") as case:
            current_result = media_room_page.library_menu_sort_by_b()
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.15.6_LibraryMenuSortByB.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.15.6_LibraryMenuSortByB.png',
                                                     library_result)

            case.result = compare_result and current_result

        # color board library menu sort by G
        with uuid("d04d43b1-71a6-4c41-8095-cec9b1647e8c") as case:
            current_result = media_room_page.library_menu_sort_by_g()
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.15.7_LibraryMenuSortByG.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.15.7_LibraryMenuSortByG.png',
                                                     library_result)

            case.result = compare_result and current_result

        # color board library menu sort by R
        with uuid("98539a5f-7334-4dc7-9bbc-30c060a12220") as case:
            current_result = media_room_page.library_menu_sort_by_r()
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.15.8_LibraryMenuSortByR.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.15.8_LibraryMenuSortByR.png',
                                                     library_result)

            case.result = compare_result and current_result

        # color board library menu sort by name
        with uuid("625b5d70-de8e-42c5-8632-b76981058d92") as case:
            current_result = media_room_page.library_menu_sort_by_name()
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.15.9_LibraryMenuSortByName.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.15.9_LibraryMenuSortByName.png',
                                                     library_result)

            case.result = compare_result and current_result



    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_2_16(self):
        # color board extra large icons
        with uuid("e42587f1-7a2b-4af7-9999-b33da369c592") as case:
            time.sleep(DELAY_TIME * 2)
            media_room_page.enter_color_boards()
            current_result = media_room_page.library_menu_display_as_extra_large_icons()
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.16.0_ColorBoardExtraLargeIcons.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.16.0_ColorBoardExtraLargeIcons.png',
                                                     library_result)

            case.result = compare_result and current_result

        # color board large icons
        with uuid("5487bfaf-2294-4084-9ca9-f71f4d86290b") as case:
            current_result = media_room_page.library_menu_display_as_large_icons()
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.16.1_ColorBoardLargeIcons.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.16.1_ColorBoardLargeIcons.png',
                                                     library_result)

            case.result = compare_result and current_result

        # color board small icons
        with uuid("79f54e91-5b85-445c-9f64-058b58ecfbb1") as case:
            current_result = media_room_page.library_menu_display_as_small_icons()
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.16.2_ColorBoardSmallIcons.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.16.2_ColorBoardSmallIcons.png',
                                                     library_result)

            case.result = compare_result and current_result

        # color board medium icons
        with uuid("590dcabd-19cc-465c-bad9-dd8acd046d57") as case:
            current_result = media_room_page.library_menu_display_as_medium_icons()
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.16.3_ColorBoardMediumIcons.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.16.3_ColorBoardMediumIcons.png',
                                                     library_result)

            case.result = compare_result and current_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_2_17(self):
        # color board search library
        with uuid("79da5b7b-6a4b-46bb-a71b-54d887dbd105") as case:
            time.sleep(DELAY_TIME * 2)
            media_room_page.enter_color_boards()
            time.sleep(DELAY_TIME * 2)
            current_result = media_room_page.search_library('31')
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.17.0_ColorBoardSearch.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.17.0_ColorBoardSearch.png',
                                                     library_result)
            case.result = compare_result and current_result

        # color board cancel search
        with uuid("4202a121-3b3a-4c6c-b4b8-f71c696b3a40") as case:
            current_result = media_room_page.search_library_click_cancel()
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.17.1_ColorBoardCancelSearch.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.17.1_ColorBoardCancelSearch.png',
                                                     library_result)
            case.result = compare_result and current_result

        # color board insert on selected track
        with uuid("394956d9-614d-4012-a331-e220d07120fb") as case:
            main_page.select_library_icon_view_media('0,120,255')
            current_result = media_room_page.library_clip_context_menu_insert_on_selected_track()
            library_result = media_room_page.snapshot(locator=media_room_page.area.timeline,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.17.2_ColorBoardInsertOnSelectedTrack.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.17.2_ColorBoardInsertOnSelectedTrack.png',
                                                     library_result)
            case.result = compare_result and current_result


        # color board change alias
        with uuid("14e30bc4-ed4b-4979-b41b-2d69be33bed5") as case:
            main_page.select_library_icon_view_media('51,53,128')
            current_result = media_room_page.color_board_context_menu_change_alias('asd')
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.17.3_ColorBoardChangeAlias.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.17.3_ColorBoardChangeAlias.png',
                                                    library_result)
            case.result = compare_result and current_result


        # color board reset alias
        with uuid("1c56e57e-82f6-4d41-a40b-5d54105a47fe") as case:
            main_page.select_library_icon_view_media('asd')
            current_result = media_room_page.color_board_context_menu_reset_alias('51,53,128')
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.17.4_ColorBoardResetAlias.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.17.4_ColorBoardResetAlias.png',
                                                    library_result)
            case.result = compare_result and current_result


        # color board remove from library
        with uuid("254c8c17-e2df-4530-a84e-aa81d9858e9b") as case:
            main_page.select_library_icon_view_media('51,53,128')
            current_result = media_room_page.color_board_context_menu_remove_from_media_library()
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.17.5_ColorBoardRemoveFromLibrary.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.17.5_ColorBoardRemoveFromLibrary.png',
                                                    library_result)
            case.result = compare_result and current_result
            media_room_page.library_menu_restore_to_defaults()
            time.sleep(DELAY_TIME)

        # color board set aspect ratio to 4:3
        with uuid("d099bc90-0275-47ec-ac80-92408217ee07") as case:
            current_result = main_page.set_project_aspect_ratio_4_3()

            library_result = media_room_page.snapshot(locator = media_room_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.17.6_ColorBoardAspectRatio43.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.17.6_ColorBoardAspectRatio43.png',
                                                    library_result)
            case.result = compare_result and current_result


        # color board set aspect ratio to 9:16
        with uuid("541e1510-c2bc-4050-a7b3-dc1b6c24726b") as case:
            current_result = main_page.set_project_aspect_ratio_9_16()

            library_result = media_room_page.snapshot(locator = media_room_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.17.7_ColorBoardAspectRatio916.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.17.7_ColorBoardAspectRatio916.png',
                                                    library_result)
            case.result = compare_result and current_result

        # color board set aspect ratio to 1:1
        with uuid("cec14694-e885-4d0c-bb46-6ad5f7e70d46") as case:
            current_result = main_page.set_project_aspect_ratio_1_1()

            library_result = media_room_page.snapshot(locator = media_room_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.17.8_ColorBoardAspectRatio11.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.17.8_ColorBoardAspectRatio11.png',
                                                    library_result)
            case.result = compare_result and current_result

        # color board set aspect ratio to 16:9
        with uuid("edf81745-ed53-4722-b49c-6006a688f1a0") as case:
            current_result = main_page.set_project_aspect_ratio_16_9()

            library_result = media_room_page.snapshot(locator = media_room_page.area.preview.main,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.17.9_ColorBoardAspectRatio169.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.17.9_ColorBoardAspectRatio169.png',
                                                    library_result)
            case.result = compare_result and current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_2_18(self):
        # BGM sort by download
        with uuid("215a019a-20fe-452d-8b9a-c8c46561ab50") as case:
            media_room_page.enter_background_music()
            time.sleep(DELAY_TIME)
            current_result = media_room_page.library_menu_sort_by_download()
            library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.18.0_BGMSortByDownload.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.18.0_BGMSortByDownload.png',
                                                     library_result)
            case.result = compare_result and current_result

        # BGM sort by date
        with uuid("c5a26bf0-c38d-42f3-818b-05fc9aa7d5d9") as case:

            current_result = media_room_page.library_menu_sort_by_date()
            library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.18.1_BGMSortByDate.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.18.1_BGMSortByDate.png',
                                                     library_result)
            case.result = compare_result and current_result

        # BGM sort by file size
        with uuid("9c7ddde9-fcd8-486d-ad21-e70ffe9d1887") as case:

            current_result = media_room_page.library_menu_sort_by_file_size()
            library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.18.2_BGMSortByFileSize.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.18.2_BGMSortByFileSize.png',
                                                     library_result)
            case.result = compare_result and current_result

        # BGM sort by duration
        with uuid("fc769248-e6db-456d-9fd1-e22f70e09d77") as case:

            current_result = media_room_page.library_menu_sort_by_duration()
            library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.18.3_BGMSortByDuration.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.18.3_BGMSortByDuration.png',
                                                     library_result)
            case.result = compare_result and current_result

        # BGM sort by category
        with uuid("5f7eb588-f3f7-4382-a0b0-dd7de5f556e5") as case:

            current_result = media_room_page.library_menu_sort_by_category()
            library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.18.4_BGMSortByCategory.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.18.4_BGMSortByCategory.png',
                                                     library_result)
            case.result = compare_result and current_result

        # BGM sort by name
        with uuid("87fd1034-9eb9-40b7-bd02-22522ae41ca7") as case:

            current_result = media_room_page.library_menu_sort_by_name()
            library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.18.5_BGMSortByName.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.18.5_BGMSortByName.png',
                                                     library_result)
            case.result = compare_result and current_result

        # BGM select all
        with uuid("2b2d7e70-8eff-46b8-8d47-e7465df41710") as case:

            current_result = media_room_page.library_menu_select_all()
            library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.18.6_BGMSelectAll.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.18.6_BGMSelectAll.png',
                                                     library_result)
            case.result = compare_result and current_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_2_19(self):
        # BGM search
        with uuid("11c3b5fd-a533-4257-942a-a987756f59c2") as case:
            media_room_page.enter_background_music()
            current_result = media_room_page.search_library('1983')
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.19.0_BGMSearch.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.19.0_BGMSearch.png',
                                                     library_result)
            case.result = compare_result and current_result

            # BGM cancel search
        with uuid("e7b72b81-32c5-465f-b18b-2a84a8eb252f") as case:
            current_result = media_room_page.search_library_click_cancel()
            library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.19.1_BGMCancelSearch.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.19.1_BGMCancelSearch.png',
                                                     library_result)
            case.result = compare_result and current_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_2_20(self):
        # BGM download
        with uuid("30117fbf-0103-4052-8aa0-dc3f1d172601") as case:
            with uuid("ad31527b-1d41-4294-9331-224fd85233bb") as case:
                media_room_page.enter_background_music()
                current_result = media_room_page.background_music_clip_context_menu_download('1983')
                library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                          file_name=Auto_Ground_Truth_Folder + 'G2.20.0_BGMDownload.png')
                compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.20.0_BGMDownload.png',
                                                         library_result)
                case.result = compare_result and current_result
            case.result = compare_result and current_result

        # play BGM
        with uuid("b6fadfb0-f22f-4282-8c64-04231b7f2778") as case:
            current_result = media_room_page.press_space_key()
            time.sleep(DELAY_TIME)
            case.result = True
            time.sleep(DELAY_TIME)
            media_room_page.tap_Stop_hotkey()

        # delete from disk
        with uuid("fddf0b12-facd-4355-8bb0-f007966d8024") as case:
            current_result = media_room_page.background_music_clip_context_menu_delete_from_disk('1983')
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.20.2_BGMDelete.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.20.2_BGMDelete.png',
                                                     library_result)
            case.result = compare_result and current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_2_21(self):
        # BGM undock library window
        with uuid("30117fbf-0103-4052-8aa0-dc3f1d172601") as case:
            media_room_page.enter_background_music()
            time.sleep(DELAY_TIME*2)
            current_result = media_room_page.background_music_context_menu_dock_undock_library_window()

            case.result = current_result

        # BGM reset undock window
        with uuid("c17457c1-0e37-43e2-b0df-0bf19bcf30ab") as case:
            current_result = media_room_page.background_music_context_menu_reset_all_undocked_windows()
            library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.21.1_BGMResetUndockWindow.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.21.1_BGMResetUndockWindow.png',
                                                     library_result)
            case.result = compare_result and current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_2_22(self):
        # BGM explorer view
        with uuid("3bf09177-c401-45b3-922f-f377da1a123f") as case:
            media_room_page.enter_background_music()
            library_result = media_room_page.snapshot(locator=L.media_room.tag_scroll_view_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.22.0_BGMExplorerView.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.22.0_BGMExplorerView.png',
                                                     library_result)
            case.result = compare_result

        # BGM insert to selected track
        with uuid("8bf0fa33-e26f-4b0a-bde4-75bec984be01") as case:
            media_room_page.background_music_clip_context_menu_download('1983')
            time.sleep(DELAY_TIME * 2)
            current_result = main_page.tips_area_insert_media_to_selected_track()
            library_result = media_room_page.snapshot(locator=media_room_page.area.timeline,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.22.1_BGMInsertOnSelectedTrack.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.22.1_BGMInsertOnSelectedTrack.png',
                                                    library_result)
            case.result = compare_result and current_result

        # play BGM
        with uuid("39f8aa5f-a2d9-4954-b09b-8fc0702e5b14") as case:
            current_result = media_room_page.press_space_key()
            time.sleep(DELAY_TIME)
            case.result = True
            time.sleep(DELAY_TIME)
            media_room_page.tap_Stop_hotkey()
            media_room_page.background_music_clip_context_menu_delete_from_disk('1983')


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_2_23(self):
        # Sound clip sort by download
        with uuid("ca81515d-559b-4426-ab7a-0883765e15e7") as case:
            media_room_page.enter_sound_clips()
            current_result = media_room_page.library_menu_sort_by_download()
            library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.23.0_SoundClipSortByDownload.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.23.0_SoundClipSortByDownload.png',
                                                     library_result)
            case.result = compare_result and current_result

        # Sound clip sort by date
        with uuid("8b65c792-3760-4020-8937-1e3ecea3128d") as case:
            current_result = media_room_page.library_menu_sort_by_date()
            library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.23.1_SoundClipSortByDate.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.23.1_SoundClipSortByDate.png',
                                                     library_result)
            case.result = compare_result and current_result

        # Sound clip sort by file size
        with uuid("75d07d03-3c35-41b2-a9eb-c50d38839cdd") as case:
            current_result = media_room_page.library_menu_sort_by_file_size()
            library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.23.2_SoundClipSortByFileSize.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.23.2_SoundClipSortByFileSize.png',
                                                     library_result)
            case.result = compare_result and current_result

        # Sound clip sort by duration
        with uuid("2d12cf02-824f-4899-a9dd-654c737246d2") as case:
            current_result = media_room_page.library_menu_sort_by_duration()
            library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.23.3_SoundClipSortByDuration.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.23.3_SoundClipSortByDuration.png',
                                                     library_result)
            case.result = compare_result and current_result

        # Sound clip sort by category
        with uuid("5c54354d-bbf5-460b-86ff-996b8f9188d9") as case:
            current_result = media_room_page.library_menu_sort_by_category()
            library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.23.4_SoundClipSortByCategory.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.23.4_SoundClipSortByCategory.png',
                                                     library_result)
            case.result = compare_result and current_result

        # Sound clip sort by name
        with uuid("74dbf399-45cc-4eaf-acbe-41acf0e821c7") as case:
            current_result = media_room_page.library_menu_sort_by_name()
            library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.23.5_SoundClipSortByName.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.23.5_SoundClipSortByName.png',
                                                     library_result)
            case.result = compare_result and current_result

        # Sound clip select all
        with uuid("785e7ad3-71a4-4450-a68b-eb6e7ee4ff50") as case:
            current_result = media_room_page.library_menu_select_all()
            library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.23.6_SoundClipSelectAll.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.23.6_SoundClipSelectAll.png',
                                                     library_result)
            case.result = compare_result and current_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_2_24(self):
        # Sound clip search
        with uuid("53d9f4db-f645-4da5-b60d-96b4ba271198") as case:
            media_room_page.enter_sound_clips()
            current_result = media_room_page.search_library('Airplane')
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.24.0_SoundClipSearch.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.24.0_SoundClipSearch.png',
                                                     library_result)
            case.result = compare_result and current_result

        # sound clip cancel search
        with uuid("8fa50c31-9f1e-4f87-a7c1-2d7381b8f489") as case:
            current_result = media_room_page.search_library_click_cancel()
            library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.24.1_SoundClipCancelSearch.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.24.1_SoundClipCancelSearch.png',
                                                     library_result)
            case.result = compare_result and current_result

        # sound clip mouse hovor clip
        with uuid("57c4da4e-7e7a-42a5-97b6-f63dfec6cf61") as case:
            current_result = media_room_page.sound_clips_hover_library_clip('Airplane')
            library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.24.2_SoundClipMouseHovorClip.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.24.2_SoundClipMouseHovorClip.png',
                                                     library_result)
            case.result = compare_result and current_result


    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_2_25(self):
        # Sound clip click duration button
        with uuid("be211ad0-c15e-47f4-b592-80940d583b8c") as case:
            media_room_page.enter_sound_clips()
            current_result = media_room_page.sound_clips_sort_button_click_duration()
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.25.0_SoundClipClickDuration.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.25.0_SoundClipClickDuration.png',
                                                     library_result)
            case.result = compare_result and current_result

        # Sound clip click date button
        with uuid("f77d0f68-bd2e-4783-8118-4be089c915b9") as case:
            current_result = media_room_page.sound_clips_sort_button_click_date()
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.25.1_SoundClipClickDate.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.25.1_SoundClipClickDate.png',
                                                     library_result)
            case.result = compare_result and current_result

        # Sound clip click download button
        with uuid("58be6022-e35d-45e3-9a4e-0fb26320dc52") as case:
            current_result = media_room_page.sound_clips_sort_button_click_download()
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.25.2_SoundClipClickDownload.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.25.2_SoundClipClickDownload.png',
                                                     library_result)
            case.result = compare_result and current_result

        # Sound clip click size button
        with uuid("5ea55607-c0a0-478c-91a0-9197d0e8f5e8") as case:
            current_result = media_room_page.sound_clips_sort_button_click_size()
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.25.3_SoundClipClickSize.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.25.3_SoundClipClickSize.png',
                                                     library_result)
            case.result = compare_result and current_result

        # Sound clip click category button
        with uuid("8a86a50c-a71a-4da1-8a06-198ec4e9fcb5") as case:
            current_result = media_room_page.sound_clips_sort_button_click_category()
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.25.4_SoundClipClickCategory.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.25.4_SoundClipClickCategory.png',
                                                     library_result)
            case.result = compare_result and current_result

        # Sound clip click name button
        with uuid("259935e6-defa-4c14-a435-5f962c96c0f6") as case:
            current_result = media_room_page.sound_clips_sort_button_click_name()
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.25.5_SoundClipClickName.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.25.5_SoundClipClickName.png',
                                                     library_result)
            case.result = compare_result and current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_2_26(self):
        # Sound clip download
        with uuid("f1ba96bd-2276-46a4-ad86-8b34be81e8b9") as case:
            with uuid("49fa0772-0ba2-48ac-9f97-bbd0274c4a0c") as case:
                media_room_page.enter_sound_clips()
                current_result = media_room_page.sound_clips_clip_context_menu_download('Airplane')
                library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                          file_name=Auto_Ground_Truth_Folder + 'G2.26.0_SoundClipDownload.png')
                compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.26.0_SoundClipDownload.png',
                                                         library_result)
                case.result = compare_result and current_result
            case.result = compare_result and current_result

        # play Sound clip
        with uuid("500369c0-07b4-4829-be42-a6336f0404fe") as case:
            current_result = media_room_page.press_space_key()
            time.sleep(DELAY_TIME)
            case.result = True
            time.sleep(DELAY_TIME)
            media_room_page.tap_Stop_hotkey()

        # Sound clip insert to selected track
        with uuid("4ae8f41f-703b-42f9-98b0-e130b2071637") as case:

            current_result = main_page.tips_area_insert_media_to_selected_track()
            library_result = media_room_page.snapshot(locator=media_room_page.area.timeline,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.26.2_SoundClipInsertOnSelectedTrack.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.26.2_SoundClipInsertOnSelectedTrack.png',
                                                    library_result)
            case.result = compare_result and current_result

        # play Sound clip
        with uuid("a02f81f0-afc7-499b-bdae-ec3dd6d3679e") as case:
            current_result = media_room_page.press_space_key()
            time.sleep(DELAY_TIME)
            case.result = True
            time.sleep(DELAY_TIME)
            media_room_page.tap_Stop_hotkey()

        # delete from disk
        with uuid("913cf333-e6cf-4aa3-b9d2-f7240f6ac767") as case:
            current_result = media_room_page.sound_clips_clip_context_menu_delete_from_disk('Airplane')
            library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.26.4_SoundClipDelete.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.26.4_SoundClipDelete.png',
                                                     library_result)
            case.result = compare_result and current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_2_27(self):
        # Sound clip explorer view
        with uuid("ec16aa4c-d8b9-4590-9b30-36c4676948f7") as case:
            media_room_page.enter_sound_clips()
            library_result = media_room_page.snapshot(locator=L.media_room.tag_scroll_view_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.27.0_SoundClipExplorerView.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.27.0_SoundClipExplorerView.png',
                                                     library_result)
            case.result = compare_result

        # Sound clip undock library window
        with uuid("c1d207ea-2391-442d-ba25-5bdeca7dff5f") as case:

            current_result = media_room_page.sound_clips_context_menu_dock_undock_library_window()

            case.result = current_result

        # Sound clip reset undock window
        with uuid("67d7418d-8969-404c-8189-356e28f7cfbb") as case:
            current_result = media_room_page.sound_clips_context_menu_reset_all_undocked_windows()
            library_result = media_room_page.snapshot(locator=L.media_room.scroll_area.library_table_view,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.27.2_SoundClipResetUndockWindow.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.27.2_SoundClipResetUndockWindow.png',
                                                     library_result)
            case.result = compare_result and current_result



    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_2_28(self):
        # enter media room
        with uuid("5a8d7efb-9eb7-4938-835e-3132b3ee1f38") as case:
            time.sleep(DELAY_TIME*2)
            main_page.enter_room(1)
            current_result = main_page.enter_room(0)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.28.0_EnterMediaRoom.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.28.0_EnterMediaRoom.png',
                                                     library_result)
            case.result = current_result and compare_result

        # enter media room
        with uuid("c13691e0-8a71-4559-9467-37fba30b1767") as case:
            media_room_page.tap_EffectRoom_hotkey()
            time.sleep(DELAY_TIME)
            media_room_page.tap_MediaRoom_hotkey()
            time.sleep(DELAY_TIME)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.28.1_EnterMediaRoomByHotkey.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.28.1_EnterMediaRoomByHotkey.png',
                                                     library_result)
            case.result = compare_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_2_29(self):
        # rename tag
        with uuid("943e5b18-59fd-4ac7-aa8b-3def957ff57a") as case:
            time.sleep(DELAY_TIME * 2)
            media_room_page.add_new_tag('abcd')
            current_result = media_room_page.right_click_rename_tag('abcd', '1234')
            library_result = media_room_page.snapshot(locator=L.media_room.tag_scroll_view_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.29.0_RenameTag.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.29.0_RenameTag.png',
                                                     library_result)
            case.result = current_result and compare_result

        # delete tag
        with uuid("6fca9a30-2e78-463e-9af5-a8627cd0d934") as case:
            current_result = media_room_page.right_click_delete_tag('1234')
            library_result = media_room_page.snapshot(locator=L.media_room.tag_scroll_view_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.29.1_DeleteTag.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.29.1_DeleteTag.png',
                                                     library_result)
            case.result = current_result and compare_result







    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_2_Testaaa(self):
        # color board create from color selector
        with uuid("444692ff-9959-4a70-b772-18f709c4b6f3") as case:
            time.sleep(DELAY_TIME * 5)
            media_room_page.enter_color_boards()
            current_result = media_room_page.color_board_create_new_color_board('C0E351')
            time.sleep(DELAY_TIME * 2)
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.15.0_CreateColorBoardFromSelector.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.15.0_CreateColorBoardFromSelector.png',
                                                     library_result)

            case.result = compare_result and current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test1_1_2_Testaa(self):
        # color board create from color selector
        with uuid("444692ff-9959-4a70-b772-18f709c4b6f3") as case:
            time.sleep(DELAY_TIME * 5)
            media_room_page.enter_color_boards()
            media_room_page.color_board_create_new_color_board_button()
            media_room_page.click_color_board_color_sliders()
            media_room_page.select_color_slider_category('HSB Sliders')
            media_room_page.drag_color_board_color_sliders_hsb_sliders(0.3,0.4,0.5)
            time.sleep(DELAY_TIME * 2)
            media_room_page.click_color_board_close()
            library_result = media_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                      file_name=Auto_Ground_Truth_Folder + 'G2.15.0_CreateColorBoardFromSelector.png')
            compare_result = media_room_page.compare(Ground_Truth_Folder + 'G2.15.0_CreateColorBoardFromSelector.png',
                                                     library_result)

            case.result = compare_result and current_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    b624a865-a7e8-4df2-9465-9bb4864c0d92
                    233a981b-49a1-49a0-b104-1e7b014cb5a1
                    d4dba1ef-91a4-4970-bcef-849391c62a64
                    86a6c22e-7174-49f1-8180-c1fb4f3427d5
                    db5a5903-a11c-40f3-b980-b9897e6cccff
                    f0196b4c-8861-4219-8a96-bc32559d8c7d
                    6f49fa69-f1fe-45c8-ae6a-f158bf256d01
                    6ab9cbb6-1c7f-468f-ad6c-d18606ffc82b
                    26eaf645-55d4-43b6-b698-264a14966cfd
                    78299011-ed2c-4b04-bc73-1f4dfbdcf84d
                    2100bc13-8b9a-4b6c-af13-bec365f4431c
                    f6dadea2-4b03-449f-bd60-376aba68e5da
                    b8e615e2-0991-4e48-85df-10e2a2cfbc7b
                    c8974f1f-7345-4e2c-9f8f-5e6362a07d5d
                    e222d9af-6ff9-4806-b0e6-66afde9a12be
                    aea4c4a9-90f8-49f7-817c-88672698a359
                    34e1ac2b-3c63-4b54-b068-51baf49a956b
                    7440f231-c7e9-40b8-b186-9f9879ad6278
                    20abe3f9-f2da-4fb2-bfe0-cc7c58ae765c
                    a6b98f07-4761-4022-809d-7bfb8a092bce
                    cef151d3-f9ef-4401-8642-882f9f92eaf6
                    
                ''') as case:
            case.result = None
            case.fail_log = "*SKIP by AT*"

















