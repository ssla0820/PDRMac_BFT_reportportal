# from configs import driver_config
import subprocess
import pytest
from ATFramework import logger

class Test_Init():

    def setup_class(cls):
        print('Skip setup class')
        pass

    # def test00_report_init(self):
    #     print('Init report in test case')
    #     pass

    # @pytest.mark.skip
    @pytest.mark.order(1)
    def test_usage_log_init(self):
        from conftest import GOOGLE_API_INSTANCE
        # from conftest import BUILD_TYPE
        from conftest import SCRIPT_VERSION
        from conftest import SCRIPT_NAME
        from globals import get_sr_number, get_tr_number, get_build_number, get_prod_version, get_os_version
        import datetime

        # for 2021 new header
        now = datetime.datetime.now()
        new_record = {'Date': now.date().strftime("%Y-%m-%d"),
                      'Time': now.time().strftime("%H:%M:%S"),
                      'Script_Name': SCRIPT_NAME,
                      'Script_Ver': SCRIPT_VERSION,
                      'SR_No': get_sr_number(),
                      'TR_No': get_tr_number(),
                      'Build_No': get_build_number(),
                      'Prod_Ver': get_prod_version(),
                      # 'Prod_Ver_Type': BUILD_TYPE,
                      'OS': 'MacOS',
                      'OS_Ver': get_os_version(),
                      # 'Device_ID': self.report.get_ovinfo('device'),
                      # 'Server': self.report.get_ovinfo('server'),
                      }
        GOOGLE_API_INSTANCE.add_new_record(new_record)
        logger(f'Usage Log Init - Start')
        logger(f'Usage Log Init - add new record to row: {GOOGLE_API_INSTANCE.row_prev_record}')
        # logger(f"Date={new_record['Date']}, Time={new_record['Time']=}, Script_Name={new_record['Script_Name']=}, \
        #     Script_Ver={new_record['Script_Ver']=}, SR_No={new_record['SR_No']=}, TR_No={new_record['TR_No']=}, Build_No={new_record['Build_No']=}, \
        #     OS={new_record['OS']=}, OS_Ver={new_record['OS_Ver']=}")