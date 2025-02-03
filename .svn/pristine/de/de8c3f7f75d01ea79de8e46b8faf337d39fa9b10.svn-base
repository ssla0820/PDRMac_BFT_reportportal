import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time, inspect, datetime, pytest, re, configparser
os.chdir(os.path.dirname(__file__))
from types import SimpleNamespace

from ATFramework import MyReport, logger, qa_log
from ATFramework.drivers.driver_factory import DriverFactory
from pages.page_factory import PageFactory
from configs.app_config import *



# read PDR cap >>
app = SimpleNamespace(**PDR_cap)
# read PDR cap <<

# create driver & page >>
mwc = DriverFactory().get_mac_driver_object('mac', app.app_name, app.app_bundleID, app.app_path)
main_page = PageFactory().get_page_object('main_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Particle Room.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

@pytest.fixture(scope="module", autouse= True)
def init():
    yield
    report.export()
    report.show()

class Test_sce_1_1():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        # main_page.open_app()
        yield mwc
        # tear down
        # main_page.close_app(forcemode=1)

    # @pytest.mark.skip
    @qa_log()
    @exception_screenshot
    def test_case1(self):
        with uuid(  "395b2563-8c85-4689-aa18-14bd4a2a9d0e",
                    "91780072-9706-464e-8442-4fe844a2cc67",
                    "33b96c79-5075-4ce6-ad4d-2cb475b4ec82",
                    "ce4f3342-9790-4637-8f39-5ec6f42fabdc",
                    "00eaaaba-95db-4641-b6b7-02b0e83f78b1",
                    "8fb9b948-5e33-45b0-8590-183df1ddc6bc",
                    "94870d27-ed8d-4dfd-b8e6-17a09a587bf8",
                    "c7b5d56e-e725-43b9-91d2-40101ebcd1ec",
                    "d3110465-5b6d-42b6-804a-7e5a4c191813",
                    "c6831526-acfe-4f37-8beb-dccd35ccf185",
                    "ac58b904-fa8c-4d92-ad3d-d396e00aecc7",
                    "806932c0-45ab-4840-bbed-12491047ecc0",
                    "1395dd40-84b9-4b4b-ad81-b69715724061",
                    "a2771c2b-5647-46c9-a2aa-4cd1b0ad9dd1",
                    "cbafedaa-ad25-40e4-b109-d105419fe6d9",
                    "f9317131-c9c2-461d-bd6f-5362d0848beb",
                    "f5afc837-7a99-403c-a4cf-492bc282ce21",
                    "ff29cb85-3c9a-4343-bc19-ee74b9da4490",
                    "33ddd1de-dd3a-4d91-b007-af2bb6bc92ef",
                    "97e67db6-4edc-4db0-a8b9-9bc0aefbb6d8",
                    "09741064-04b1-456c-a2ee-db8aa0fab89a",
                    "49b278a1-46dc-41a4-8aa3-f23c8c411217",
                    "5f5726a1-a7e3-4397-9a32-eee0ed9567b5",
                    "91e7c6ad-0ebb-45cb-8898-26f481ee7019",
                    "324f4f40-c308-40d5-870d-b6e6b154a6a8",
                    "6d6161cf-6a47-4338-ba3c-95af2eed64ab",
                    "1d4f1d30-023e-4fbf-9404-27a7682cdddd",
                    "93d94423-1da5-40b6-a4f9-c41638f40805",
                    "a379699a-e039-4124-ba86-e894d8ad0272",
                    "8080ea26-8e56-4445-9876-52600c6d7614",
                    "687b1ce4-dd64-4b39-ad93-7fbeb4ba578f",
                    "ec63aeaf-c16a-4d52-83e3-9ca8b8b03a15",
                    "8d6dac40-fd22-4317-9f5f-07573a1b6caf",
                    "191984f5-1a94-4d94-999e-b1df0cf7ca90",
                    "d52bbb8a-c588-469b-b3b4-7259d8790a38",
                    "3df32b92-79e1-43c9-a0d8-1a1abe629a01",
                    "3d64f981-d4fd-45a2-8617-c46a0b090889",
                    "f459d701-5d49-4819-a362-46129011100a",
                    "b517bc73-147d-4bfd-860d-61a0272b7945",
                    "6b1e6054-ad7b-4ca2-89da-338d5eed2f65",
                    "971f93bc-75bc-4217-a68b-30a764f19ad5",
                    "094e4d01-a0b2-49c5-be24-276f39c62594",
                    "3970b5e0-96a4-482c-9bbb-54f0bf8975e7",
                    "0b355948-df65-4765-bd4c-05e4b819f945",
                    "33ce865e-cb68-4c27-9155-70f83ef8f0b1",
                    "7638da91-d60b-41c7-835a-dec6b9a56bde",
                    "a6b689c7-09f8-46f0-9b72-4437e4c0be4c",
                    "7a291cbb-2112-4af8-b108-e9f80221d14c",
                    "35bb7809-382a-4d41-acb2-acd83d712f5c",
                    "1ba4730c-30cd-4b12-a5cf-474fc02aa738",
                    "4c6db2b8-af74-4ecd-b89c-26890dedef78",
                    "d3a1dad4-15f1-4fe5-a8b0-931b6e2f9438",
                    "a82bc239-868a-4b47-bc22-97890feeae56",
                    "0d5d3ab1-a864-418c-be1d-16aed4dba785",
                    "08ab6019-3e88-401b-9154-b3396940283c",
                    "f7f41489-256e-404e-b70a-2a96f25c77a7",
                    "74e605e8-7a3d-4580-a04b-a2e56d83acfe",
                    "6a21536a-6a28-4c8d-81c2-151d8b230b06",
                    "cc070dc0-9608-4e81-b763-4ba84f8a4bcf",
                    "e4aa6cb6-98f1-4dff-a374-6009d523bc25",
                    "cc3ee7d1-e4f3-409f-9d78-918ba8144e94",
                    "687f60a6-d65a-4c05-9db9-c3cad72a206f",
                    "aec47cc8-3708-440b-9cf9-b56427a41f9d",
                    "d6a79533-6547-45cf-acae-8ea3d0d8c181",
                    "45163421-e879-4e62-87bf-180104d6237d",
                    "654aa4f8-382b-4559-af46-027f92315e9c",
                    "11758802-33af-4709-ab60-61523b851b4f",
                    "6418566d-6129-48f9-938c-6be49ace69ba",
                    "bab76f4b-c296-4593-84c8-3c8ae7dada3e",
                    "b788725d-3bba-4e84-bc32-d64a9067f041",
                    "ccdac930-2de9-444d-91db-3b7f94fdaf9c",
                    "b6013297-f249-40ff-8728-0dad0235c571",
                    "583f6a84-65d2-49df-b20a-ef846b87f2d9",
                    "b3fc4c66-ddf6-4097-a632-14a4bc18c46f",
                    "2c78b81d-83cc-4c5a-8e5a-fae901861441",
                    "cd22dbf6-d1a8-458e-bc7f-73a95bcc7717",
                    "b307b62d-b7c4-4e4b-acbc-6dfcfca3bba6",
                    "7c2dfdf5-596f-44c6-b70f-1578ec8b80ff",
                    "83933435-cc1a-4ba4-b0be-ab1237868c40",
                    "0990c9f8-e29a-432d-a910-9c82deb08a16",
                    "3cbb9827-0a51-4989-8a09-5e7e960fe148",
                    "f5858c64-8a13-49bf-9ef0-31a0ab3fc5b3",
                    "bf82e1e6-4225-44fd-834a-62d01630cf1e",
                    "78195876-a681-445c-be9d-0a33a23915c0",
                    "2598575e-7a5e-486f-8467-14b9987cb3db",
                    "bf3e2aa9-a599-4230-8642-97e84638517f",
                    "20eb41f2-a813-4165-acf2-1fc13b7f947d",
                    "534bf701-e281-4c62-850f-b10d304fe2fb",
                    "9071e6ff-28de-4aa7-b4a6-4aaf92dbc297",
                    "2806fc53-1d70-4668-b336-406366da3663",
                    "cc24bc72-c4e0-4126-8c04-bdfbaec9a644",
                    "437e140a-b3a8-40de-ab6e-2a92e8f2652b",
                    "7040b5a1-4750-4612-b9c8-d339c0c8274e",
                    "0e5e4f9f-8bd1-4cc5-aa70-e780cf6f969c",
                    "3a8c27c7-4ac5-42bc-9d7b-119b555a4fc6",
                    "ca4b54b1-3c2a-4d68-9b7f-0792383f0045",
                    "7b48a894-e331-4987-8d57-b038515d75f5",
                    "923363d6-cb3c-47ac-90ca-4c8c2e5b5b29",
                    "2610755f-10bf-4a72-b2ba-79ea5fda3d14",
                    "6a25aad7-18db-4637-a41b-756d91706de7",
                    "9e1b45d1-ebee-48cb-8465-5e0fdace9e46",
                    "4e17ec66-a6ac-4df7-86fe-4b3789f281c5",
                    "28c38e3d-1841-474b-a997-0253c6feb627",
                    "6b172f2a-657a-4b7a-8f1f-3d0c3d1fb5e5",
                    "ffb87e60-ce78-4d77-b50c-66e6ae87d8e0",
                    "c378f060-d461-4f10-9c13-b4cf83532282",
                    "856718bb-f486-4385-8c44-3c368b719923",
                    "a3f18b5d-8e98-413e-9497-2a2b7700265b",
                    "587dba90-7995-4517-8456-c328ea53c641",
                    "9f87e740-2804-4564-a454-8ec0711496c8",
                    "5b4a40f3-e740-46de-809b-0d69180e11ea",
                    "07d7efac-f547-454d-a8e3-c8456bda69d8",
                    "ecc5e255-a144-4161-8407-c1b494583515",
                    "1f57a35d-ca46-4c8b-884e-dd212820d6ea",
                    "61168835-44e9-409e-a35f-8aba73f42029",
                    "41dc1a04-60e3-4263-ae93-c456af09c13d",
                    "79b85a32-5fe1-4a41-8bb4-a73a3f87069b",
                    "57674817-a50b-494c-9836-5bfafcca6113",
                    "d56a7b26-1e34-4e3c-9205-e6acd554003b",
                    "b3127ee8-2e5f-4868-9af9-7126066b4d0e",
                    "a815369d-c625-4095-9ebc-386cb0795876",
                    "84226664-1cbb-4c1a-b944-bc893ef929cb",
                    "181f37d2-cf5e-40d3-a82f-6cfa950514b3",
                    "f1e24c40-f4df-4a0c-b7f6-49e4de45612a",
                    "599d516a-173c-4c2b-9d4f-6db259dd62b4",
                    "363f0055-6020-4b10-8d50-a55289339b99",
                    "f991c925-26c9-41e5-9e1a-539a2a8cec99",
                    "261839b6-e925-4c3e-8dd0-30145029e015",
                    "ff70b162-d283-4859-b985-27b403334468",
                    "b8f1f119-672e-4887-93c1-c0f21aafa371",
                    "cfa52ea6-401a-4dff-96e0-93344b01fb1c",
                    "2f4bb3e3-a057-4979-a79d-45d3ea50418e",
                    "967b0bff-e2ba-4c2a-a731-834a7b488b05",
                    "cf4b22cc-125b-4bc9-bc26-0250e9f9d6d5",
                    "dff99275-ab6b-4fa4-9bf6-b4cc211d019f",
                    "123b8e4f-28a0-43bb-b303-f3b1031939b4"
                  ) as case:
            # start test case code

            case.result = True
            # end test case code

    # @pytest.mark.skip
    @exception_screenshot
    def test_case2(self):
        with uuid("15373155-ba15-4bc3-a7ad-2ec10a51ff11") as case:
            case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_case3(self):
        with uuid("""efa5601f-4366-453d-97f2-f5844c438222
1cbe8b3f-3ffd-4e9a-9df9-68f3eafd257f



feb32aa1-af24-435f-af64-ec8692b4765d
46d32e39-dd34-41a7-8b25-e20afe6ad55d
c0482c6e-6c2d-4161-916f-f0a7977d5673
05261fc8-adb0-485b-8cfa-471276f1c656


35ba4188-700e-4a07-bda6-4152013d6dcd
2a60753b-9108-419b-9b54-303cb9ba3118
d8a214e5-eb78-4beb-91e7-b32810a022d3
c4d0d565-51ff-42e2-9cdc-b63c4c344615
22498757-b244-4125-8c4c-6273ca717211
37fd9dcd-265d-4b2d-853b-c7a786b06037
6e961597-fe7e-43b6-afa6-fdafab73dbfd
b401be23-0a44-40ea-93b4-02fe84a20a6c
c5abf83a-0466-4363-82ac-54696cd99e32
e8628cc4-c2de-4534-bd3b-75f8b13dc559


673609ff-719e-4ea1-8762-33e1492f41cf
a79144a6-cbcf-4a15-ac4c-77775aa1c704
57ba3ace-4ef3-4d10-96df-ce38e625a08d
f5f7de96-e5c1-45cd-b7c0-bde91250b147
ba036d39-e7b2-44df-8148-2718537910ee
bcf452e0-32ef-4613-b64a-a69647f627e6
60aeb406-2f14-49de-9444-cabcc416ded7
504c6da6-65dd-4e14-b5cf-75ec3cc4de0d
5a01c4d4-5069-41cb-bbc4-6cbafaa3c192
13ee3edc-3337-4e4b-9905-f6236f3fa91c
f24851ce-1624-42e5-b681-08e84a964f99
ad7f50f0-185a-4727-8d9b-059dba5e0e63



14532e22-5dc3-4a80-8b40-38c2fe6a1c6a
97ddf81d-0009-4845-963d-eace3cf528bc
8b7471b0-dff5-460f-83cd-9c8abfc29e2d
a2a63d34-1c51-4571-b313-71891b754eed
c3f054a3-6e77-427a-8ccb-bfe931287e16
2ee46260-d49b-4abc-bf3d-5ba045f11b50
4ef6b286-48c0-422b-907d-4523567ee516
5c117171-f493-4008-8c95-aa28af07d0a2
6c2a0e98-62d4-457c-b934-dce2a5f7b770




da843fbe-0d82-4ff5-9d0b-b92b13092457
c0e6f659-9c22-474c-997e-9916ccf0a1c1
8b771169-1027-449c-aad8-e3b18d15b696
6a9095f0-ff3d-421d-9d73-f6ee17794b3f
bad34e79-35bb-4a99-a070-3f55cf9d0307
a9a6e1d6-e6c4-4a52-9fc5-39d2b656746f
b12f9f24-21b7-4399-a2ba-28ad27fd3537""") as case:
            case.result = None
            case.fail_log = "*SKIP by AT*"

    # @pytest.mark.skip
    @exception_screenshot
    def test_case4(self):
        with uuid("a57a5054-4820-4083-8295-a466ec8b7d89") as case:
            raise Exception("fail case")
            case.result = True

