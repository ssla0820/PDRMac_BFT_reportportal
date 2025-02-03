class tab:
    entire_clip = {'AXIdentifier': 'IDC_VIDEO_SPEED_BTN_ENTIRE'}
    selected_range = {'AXIdentifier': 'IDC_VIDEO_SPEED_BTN_PARTIAL'}

video_slider = {'AXIdentifier': 'IDC_VIDEO_SPEED_SLIDER_SELECTSLIDER'}
i_button = {'AXIdentifier': 'IDC_VIDEO_SPEED_BTN_ADD_MARKER_HINT'}
i_dialog = {'AXIdentifier': 'IDD_TIME_SHIFT_HINT_DLG'}
i_close = {'AXIdentifier': 'IDC_TIME_SHIFT_HINT_CLOSE'}
time_shift_1 = {'AXIdentifier': 'IDC_VIDEO_SPEED_BTN_ADD_MARKER'}
time_shift_2 = {'AXIdentifier': 'IDC_FILMCTRL_ADD_MARK_IN_OUT'}

class navigation:
    main = {'AXIdentifier': 'IDC_VIDEO_SPEED_SPINTIMEEDIT_TIMECODE'}
    time_code = [main,{'AXIdentifier': 'spinTimeEditTextField'}]

class cancel_dialog:
    main = {'AXIdentifier': 'IDD_CLALERT'}
    ok = [main, {"AXRole": "AXButton", "AXTitle": "OK"}]
    cancel = [main, {"AXRole": "AXButton", "AXTitle": "Cancel"}]
    yes = [main, {"AXRole": "AXButton", "AXTitle": "Yes"}]
    no = [main, {"AXRole": "AXButton", "AXTitle": "No"}]

class new_video:
    main = {'AXIdentifier': 'IDC_VIDEO_SPEED_SPINEDIT_ENTIRE_NEW_DURATION'}
    time_code = [main,{'AXIdentifier': 'spinTimeEditTextField'}]
    up = [main, {'AXIdentifier': '_NS:12'}]
    down = [main, {'AXIdentifier': '_NS:32'}]


class multiplier:
    main = {'AXIdentifier': 'IDC_VIDEO_SPEED_SPINEDIT_ENTIRE_SPEED'}
    slider = {'AXIdentifier': 'IDC_VIDEO_SPEED_SLIDER_ENTIRE_SPEED'}
    value = [main,{'AXIdentifier': 'spinEditTextField'}]
    up = [main, {'AXIdentifier': '_IDC_SPINEDIT_BTN_UP'}]
    down = [main, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN'}]

class duration:
    main = {'AXIdentifier': 'IDC_VIDEO_SPEED_SPINEDIT_PARTIAL_NEW_DURATION'}
    time_code = [main, {'AXIdentifier': 'spinTimeEditTextField'}]
    up = [main, {'AXIdentifier': '_NS:12'}]
    down = [main, {'AXIdentifier': '_NS:32'}]

class multiplier_partial:
    main = {'AXIdentifier': 'IDC_VIDEO_SPEED_SPINEDIT_PARTIAL'}
    slider = {'AXIdentifier': '_NS:48',"AXRole":"AXSlider"}
    value = [main,{'AXIdentifier': 'spinEditTextField'}]
    up = [main, {'AXIdentifier': '_NS:9'}]
    down = [main, {'AXIdentifier': '_NS:72'}]
    ease_in = {'AXIdentifier': 'IDC_VIDEO_SPEED_CHECKBOX_EASE_IN'}
    ease_out = {'AXIdentifier': 'IDC_VIDEO_SPEED_CHECKBOX_EASE_OUT'}

class preview:
    play = {'AXIdentifier': 'IDC_VIDEO_SPEED_BTN_PLAY'}
    stop = {'AXIdentifier': 'IDC_VIDEO_SPEED_BTN_STOP'}
    previous_frame = {'AXIdentifier': 'IDC_VIDEO_SPEED_BTN_PREVFRAME'}
    next_frame = {'AXIdentifier': 'IDC_VIDEO_SPEED_BTN_NEXTFRAME'}
    fast_forward = {'AXIdentifier': 'IDC_VIDEO_SPEED_BTN_FASTFORWARD'}

remove = {'AXIdentifier': '_NS:IDC_FILMCTRL_DELETE_MARKER'}
view_entir_movie = {'AXIdentifier': 'IDC_FILMCTRL_FIT_FILM'}
reset = {'AXIdentifier': 'IDC_VIDEO_SPEED_BTN_RESET'}
cancel = {'AXIdentifier': 'IDC_VIDEO_SPEED_BTN_CANCEL'}
ok = {'AXIdentifier': 'IDC_VIDEO_SPEED_BTN_OK'}
zoom_out = {'AXIdentifier': 'IDC_FILMCTRL_ZOOM_OUT'}
zoom_in = {'AXIdentifier': 'IDC_FILMCTRL_ZOOM_IN'}



class video_speed:
    main = {'AXIdentifier': '_NS:10'}
    time_code = [main,{'AXIdentifier': 'spinTimeEditTextField'}]
    up = [main, {'AXIdentifier': '_NS:12'}]
    down = [main, {'AXIdentifier': '_NS:32'}]

    class multiplier:
        slider = {'AXIdentifier': '_NS: 133'}
        _group = {'AXIdentifier': '_NS:151', "AXRole":"AXGroup"}
        value = [_group, {'AXIdentifier': 'spinEditTextField'}]
        up = [_group, {'AXIdentifier': 'NS:9'}]
        down = [_group, {'AXIdentifier': 'NS:72'}]
        setting = {'AXIdentifier': '_NS:90'}

    reset = {'AXIdentifier': '_NS:67'}
    cancel = [{'AXIdentifier': '_NS:10'},{'AXIdentifier': '_NS:129'}]
    ok = [{'AXIdentifier': '_NS:10'},{'AXIdentifier': '_NS:9', "AXTitle": "OK"}]


max_and_restore = {"AXRoleDescription":"zoom button"}
close = {"AXRoleDescription":"close button"}

class original_video:
    main = {'AXIdentifier': '_NS:51'}
    timecode = [main, {"AXIdentifier":"spinTimeEditTextField"}]