import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from MacFramework.utils._report.report import MyReport

report = MyReport("MyReport",html_name="Video Collage.html")

uuid = report.uuid

class Test_mytest():
    def test_1_1(self):
        #jtw4fymh-impx-rxvu-s6xv-8tuno1mx4fls
        #m2pw5e07-puei-7jw8-08ax-vfndmr7us68e
        with uuid("jtw4fymh-impx-rxvu-s6xv-8tuno1mx4fls") as case:
            # start test case code


            # end test case code

            case.result = False # submit result


    def test_1_2(self):
        with uuid("at3jvd7f-hkdz-b7ge-6h9p-2ibo8t6mpd7c") as case:
            # fail case
            case.result = True

    def test_1_3(self):
        with uuid("qic6rmex-yslz-dfwy-2unl-ct6p3g9xjsdh") as case:
            # N/A case
            case.result = None


        print('test 1207')
        report.export()
        report.show()