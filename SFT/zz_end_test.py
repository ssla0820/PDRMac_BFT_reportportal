
import pytest
from ATFramework import logger

class Test_End():

    # @pytest.mark.skip
    def test_usage_log_end(self):
        from conftest import GOOGLE_API_INSTANCE
        from globals import get_report_info
        data = {'Pass': get_report_info('pass'), 'Fail': get_report_info('fail'), 'Skip': get_report_info('skip'),
                'N/A': get_report_info('na'), 'Total time': get_report_info('duration')}
        GOOGLE_API_INSTANCE.update_columns(data)
        logger(f'Usage Log End - Start')
        logger(f'Update record to row: {GOOGLE_API_INSTANCE.row_prev_record}')
        # logger(f"Pass={data['Pass']}, Fail={data['Fail']}, Skip={data['Skip']}, N/A={data['N/A']}, Total time={data['Total time']}")
