main_window = {'AXRole': 'AXWindow', 'AXIdentifier': 'IDC_VIDEO_TRIM_DIALOG_WINDOW'}
btn_OK = [main_window, {'AXIdentifier': 'IDC_MULCUTBUTTON_OK'}]

class alert_dialog:
    main = {'AXIdentifier': 'IDD_CLALERT'}
    warning_msg = [main, {'AXValue': 'In the Video Trim window, all applied effects are ignored. In order to perform a trim, CyberLink PowerDirector must remove the applied reverse from this clip. Are you sure you want to continue?'}]
    btn_Yes = [main, {'AXIdentifier': 'IDC_CLALERT_BUTTON_0'}]
    btn_No = [main, {'AXIdentifier': 'IDC_CLALERT_BUTTON_1'}]