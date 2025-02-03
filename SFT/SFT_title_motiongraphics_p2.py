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
mask_designer_page = PageFactory().get_page_object('title_designer_page', mwc)
media_room_page = PageFactory().get_page_object('media_room_page', mwc)
title_room_page = PageFactory().get_page_object('title_room_page', mwc)
title_designer_page = PageFactory().get_page_object('title_designer_page', mwc)
timeline_page = PageFactory().get_page_object('timeline_operation_page', mwc)
tips_area_page = PageFactory().get_page_object('tips_area_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Motion Graphics Title_ARLON_M3.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Motion_Graphics_Title/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Motion_Graphics_Title/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Motion_Graphics_Title_p2():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
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
            google_sheet_execution_log_init('Motion_Graphics_Title_ARLON_M3')

    @classmethod
    def teardown_class(cls):

        logger('teardown_class - export report')
        report.export()
        logger(
            f"Motion Graphics Title result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
    def test_1_1_6(self):
        # click undo button
        with uuid("e160e697-867e-4c29-af99-56fdc903f9b7") as case:
            time.sleep(4)
            main_page.enter_room(1)
            title_room_page.select_specific_tag('Motion Graphics')
            media_room_page.select_media_content('Motion Graphics 002')
            title_room_page.select_RightClickMenu_ModifyTemplate()
            title_designer_page.mgt.handle_warning_msg(1)
            title_designer_page.mgt.click_warning_msg_ok()
            title_designer_page.click_maximize_btn()
            title_designer_page.mgt.unfold_object_setting_tab()
            title_designer_page.mgt.set_rotation_value('45')
            title_designer_page.mgt.click_undo_btn()
            time.sleep(2)
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + 'ClickUndo_button.png')
            logger(image_result)
            compare_result = title_designer_page.compare(Ground_Truth_Folder + 'ClickUndo_button.png',
                                                         image_result)
            case.result = compare_result

        with uuid("cd3e4059-d054-46b4-be8f-d570f9d9a30a") as case:
            # click redo button
            time.sleep(1)
            title_designer_page.mgt.click_redo_btn()
            time.sleep(2)
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + 'ClickRedo_button.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + 'ClickRedo_button.png',
                                                         image_result)
            case.result = compare_result

        with uuid("c8c31dfc-ccb9-41d7-a228-474fabdf465d") as case:
            # click  zoom in
            time.sleep(1)
            title_designer_page.mgt.click_zoom_in()
            title_designer_page.mgt.click_zoom_in()
            title_designer_page.mgt.click_zoom_in()
            time.sleep(2)
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + 'Zoomin.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + 'Zoomin.png',
                                                         image_result)
            case.result = compare_result

        with uuid("70d2009d-fc14-4ea3-a9f3-3ff890484126") as case:
            # select fit from menu
            time.sleep(1)
            title_designer_page.mgt.click_viewer_zoom_menu('Fit')
            time.sleep(2)
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + 'Fit.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + 'Fit.png',
                                                         image_result)
            case.result = compare_result

        with uuid("da142049-c35f-4cae-94db-3dc03f317f20") as case:
            # click zoom out
            time.sleep(1)
            title_designer_page.mgt.click_zoom_out_btn()
            title_designer_page.mgt.click_zoom_out_btn()
            time.sleep(2)
            image_result = title_designer_page.snapshot(locator=L.title_designer.area.frame_preview,
                                                        file_name=Auto_Ground_Truth_Folder + 'ZoomOut.png')
            compare_result = title_designer_page.compare(Ground_Truth_Folder + 'ZoomOut.png',
                                                         image_result)
            case.result = compare_result




    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_21(self):
        with uuid("""d123305c-297a-4c27-8ca3-c5a210414734
bf323ef4-0fc7-455f-880d-1f1e170e2459
8f5f61b8-5113-43c9-8a86-f42ba7ef5db6
975f2012-f58d-4856-93a3-8d662573029c
5669edea-2e7e-46ab-9ffb-bb5f40be49fc
278eb33e-348c-40ef-b7fc-ca07c8387703
67b1ae49-a292-418d-b1a4-dc52b336acea
bd1bbed8-8d38-43c0-a63b-32312484decc
362dab7a-2a45-4575-8eff-a3126300f890
ebb3f6df-ec29-4206-aa00-3a2015d622bc
5b6dce0c-bc6c-4f46-80d2-faf158f82385
65bb20fb-967e-4409-b3b1-570113f68ddf
3943bf43-d1f0-45da-8be7-767372386dc0
5cc0780f-08e3-4287-91d7-c5e9bf8d501d
95cdd00b-58e5-4ae1-8c90-e255210ea350
2b79fdac-ee86-4469-ac45-a5a58a99126b
cb5cdabe-ee93-4114-8722-2e134c8d79af
8dd0b798-0a69-42c2-afeb-49c942ca07ac
75ca0614-655f-4374-9681-11298855430a
2359a7e6-94a6-4d89-87c4-fae7ed2e0ff2
3e6ac88a-fc6e-4e72-bdd3-476366855615
84217281-2b15-4f7f-8263-dfa44297532b
29ca3003-dd08-4684-a2d1-8c367e80801f
9c5929c4-0e13-4e38-89bf-5089a0f46c2f
234fe143-1663-4f24-b6e3-e676b68007d5
531d0668-5015-41e4-a8cb-7ddc0a258d94
72e950df-588c-4b3f-94b4-cc0d801bbc84
61b422c7-70a9-4c78-8657-46e75ac36e0c
9bfe114d-08f0-4bca-b83d-dc3731add235
8631e135-ff6e-4733-9672-6b941c380856
01726d8e-a199-4588-8298-b6cae1b43a4b
d7952f75-677e-42ab-8974-a0c374f22c30
db32a353-30b6-45dd-be59-95ed4ab362b0
24099712-2cbd-4df5-b0e4-ed6beecdc370
0249110d-ca27-4db6-b0ae-85aefe673483
a8866c40-7f73-4c0c-a7c0-956608649d12
fbed6d3a-cfbb-4641-906f-930c4ce67dab
c06c1043-f3d3-4298-9689-2dab01f2d0a1
58ff77c7-523c-4ab0-9b6a-7b8edfbe1de5
1f9276d4-3b0a-40a3-ac3e-4a4e01818009
dc4f80fc-1ce5-4c27-93b9-f494946e23e1
a2e0c688-7ad9-43b4-bc1d-8bd0beffa025
e5bd8605-85c1-4d04-a298-84a7bb84ba11
65b65055-3be8-48a4-b12d-97990196fca9
d0ea5cc6-f4d2-40d7-b68f-1b49d5276616
deb813e3-97dc-4b70-91ec-cafb25741fb3
01a9e60a-947b-48d2-adf2-c4c6045e97a3
a7dccf5e-afdf-4260-b842-c3a3dca9458a
35733491-0e75-4eba-9bbd-6d46a021f14b
658a4865-b4e9-44c0-8dc9-3d01d32a931b
ec3f696b-20f7-4e5b-99ce-d40a2ecd31f8
8b7e4a95-e53a-4a51-9b96-b099531b8e66
4dc05475-1fdc-4e8a-add8-cd11654d0241
61e8394d-c886-4cc4-9436-d591adcc542d
13bf2d51-65c4-4d0b-a44c-0dd4aabf740c
093a1861-c22d-46b9-a3b0-173e00357d17
66fe1237-1e68-489d-bcdf-c599997b8bda
701c17ef-4de5-4ab7-8474-405de362fdd0
63c3796f-660a-445c-98fe-145dd35000d5
c3899941-0321-4e80-8a6a-5e48d93d3783
e806ec34-4b20-4814-84d3-615ea5166bc5
caa26d13-0d7a-4b56-b1f5-0511288be608
fae0ee13-af7c-4d23-b4eb-e8dea2bf1ad9
c9150327-e789-424d-90e0-ce8288068dd6
c65d28eb-10fe-4d3c-83d8-98b2a974321d
c540c40b-135d-43e3-adcd-25b972565a9e
1eb31f65-7a9d-4ed0-9e9e-801c2e91efbd
27b78552-87b3-462f-a6e7-7e111be86471
08ebdf05-af06-45d0-965e-d7096dcd541a
bf959a23-e03f-45c0-92a8-624c48cf9fb8
6142a6d7-1e93-45b2-a87b-dc6e9d47c443
29a93025-65d5-4636-a6b6-724484f2c827
ef59e0e5-933d-459d-a2c8-5e362847f517
6c3a4308-bcb9-4e41-8804-6f36373ff061
e160e697-867e-4c29-af99-56fdc903f9b7
cd3e4059-d054-46b4-be8f-d570f9d9a30a
c8c31dfc-ccb9-41d7-a228-474fabdf465d
da142049-c35f-4cae-94db-3dc03f317f20
70d2009d-fc14-4ea3-a9f3-3ff890484126""") as case:
            case.result = None
            case.fail_log = "*SKIP by AT*"