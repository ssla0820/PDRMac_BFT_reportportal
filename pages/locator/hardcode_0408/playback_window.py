main = {'AXIdentifier': 'IDD_DISPLAYPANEL'}
slider = {'AXIdentifier': 'IDC_DISPLAY_SLIDER_PLAYBACK'}
timecode = [main, {'AXIdentifier': 'spinTimeEditTextField'}]
zoom = [main, {'AXIdentifier': '_NS:60'}]
zoom_value = [zoom]

class operation:
    play = {'AXIdentifier': 'IDC_DISPLAY_BTN_PLAY'}
    stop = {'AXIdentifier': '_NS:152'}
    previous_frame = {'AXIdentifier': 'IDC_DISPLAY_BTN_PREVIOUSFRAME'}
    next_frame = {'AXIdentifier': 'IDC_DISPLAY_BTN_NEXTFRAME'}
    fast_forward = {'AXIdentifier': 'IDC_DISPLAY_BTN_FULLSCREEN'}


render_preview = {'AXIdentifier': 'IDC_DISPLAY_BTN_RENDERPREVIEW'}
take_snapshot = {'AXIdentifier': 'IDC_DISPLAY_BTN_SNAPSHOT'}

class save_as:
    main = {'AXIdentifier': 'save-panel'}
    file_name = {'AXIdentifier': 'saveAsNameTextField'}
    ok = {'AXIdentifier': 'OKButton'}


set_quality = {'AXIdentifier': 'IDC_DISPLAY_BTN_DISPLAY_OPTIONS'}
dock = {'AXIdentifier': '_NS:164'}
undock = {"AXDescription":"Custom View", "AXRole":"AXButton"}

class popup_window:
    main = {'AXIdentifier': 'PopupWindow'}
    max_restore = [main, {"AXSubrole":"AXZoomButton"}]
    minimize = [main,{"AXSubrole":"AXMinimizeButton"}]
    toolbar = [main,{"AXRole":"AXToolbar"}]
    full_screen = [main,{'AXIdentifier': 'IDC_DISPLAY_BTN_FULLSCREEN'}]

class context_menu:
    main = {'AXIdentifier': '_NS:10'}
    play = {'AXRole': 'AXMenuItem', "AXIdentifier":"_NS:139"}
    stop = {'AXRole': 'AXMenuItem', "AXIdentifier":"_NS:144"}
    previous_frame = {'AXRole': 'AXMenuItem', "AXIdentifier":"_NS:149"}
    next_frame = {'AXRole': 'AXMenuItem', "AXIdentifier":"_NS:154"}
    fast_forward = {'AXRole': 'AXMenuItem', "AXIdentifier":"_NS:65"}
    snapshot = {'AXRole': 'AXMenuItem', "AXIdentifier": "_NS:159"}