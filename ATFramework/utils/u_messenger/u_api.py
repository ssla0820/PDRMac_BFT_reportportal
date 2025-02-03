
import requests


"""
=== Send message to U by API ===
Please contact the ECL to get the UID and ECLToken.

"""


def send_u_message_by_api(u_params_dict):
    try:
        url = 'https://ecl.cyberlink.com/UService/Service/SendMsgByUIDToken?'
        response = requests.post(url, params=u_params_dict)
        if response.status_code != 200:
            print(f'response={response.text}')
            return False
        print(f'Message is sent to "{u_params_dict["Group"]}" group successfully.')
    except Exception as e:
        print(f'Exception occurs. error={e}')
        return False
    return True

        
if __name__ == "__main__":
    # params = {'UID': 'qaat_viruscan', 'ECLToken': 'a65022ed-8a46-48bb-9cf5-fe1a1b5d705c', 'Message': 'Test', 'Group': 'VIRUS_SCAN_AT_Report'}
    params_dict = {'UID': 'qaat_viruscan',
                   'ECLToken': 'a65022ed-8a46-48bb-9cf5-fe1a1b5d705c',
                   'Message': 'Test',
                   'Group': 'VIRUS_SCAN_AT_Report'
                   }
    send_u_message_by_api(params_dict)
