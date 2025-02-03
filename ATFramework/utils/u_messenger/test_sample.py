from u_lib import U


message_package = {'account': '',
                   'password': '',
                   'contact_name': '',
                   'message': '',
                   'is_prod': True}


def send_message(message_package):
    try:
        sender = U(email=message_package['account'], pwd=message_package['password'], is_prod=message_package['is_prod'])
        sender.clear_data()
        sender.update_ini()
        sender.launch_u()
        sender.send_message_to_contact(message_package['contact_name'], message_package['message'])
        sender.close()
    except Exception as e:
        print(f'Exception occurs. error={e}')
        return False
    return True