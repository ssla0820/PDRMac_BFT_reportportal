main_window = {'AXRoleDescription': 'dialog', 'AXTitle': 'Video Collage Designer'}
splitter = [main_window, {"AXRole": "AXSplitter"}]

slider = [main_window, {'AXIdentifier': 'IDC_VIDEO_COLLAGE_EDITORPANEL_SLIDER_PLAYBACK', "AXRole": "AXSlider"}]
time_code = [main_window, {'AXIdentifier': 'IDC_VIDEO_COLLAGE_TIME_EDIT'}, {"AXIdentifier": "spinTimeEditTextField"}]

btn_ok = {"AXIdentifier": "IDC_VIDEO_COLLAGE_BUTTON_OK"}
btn_cancel = {"AXIdentifier": "IDC_VIDEO_COLLAGE_BUTTON_CANCEL"}
btn_save_as = {"AXIdentifier": "IDC_VIDEO_COLLAGE_BUTTON_SAVEAS"}
btn_share = {"AXIdentifier": "IDC_VIDEO_COLLAGE_BUTTON_SHARE"}

media_library = {"AXIdentifier": "IDC_VIDEO_COLLAGE_LIBRARY_COLLECTIONVIEW"}


class border:
    frame = [main_window, {"AXIdentifier": "IDS_VIDEO_COLLAGE_SETTING_PANEL_SCROLLVIEW"}] # 3303: _NS:285 2922: _NS:255
    scroll_bar = {"AXIdentifier": "IDS_VIDEO_COLLAGE_SETTING_PANEL_VERTIVAL_SCROLLBAR"} # 3303: _NS:442  2922: _NS:252
    checkbox_enable = {"AXIdentifier": "IDC_VIDEO_COLLAGE_SETTINGPANEL_CHECKBOX_APPLY_BORDER"}

    slider_border = {"AXIdentifier": "IDC_VIDEO_COLLAGE_SETTINGPANEL_SLIDER_SIZE"}
    frame_border = {"AXIdentifier": "IDC_VIDEO_COLLAGE_SETTINGPANEL_SPINEDIT_SIZE"}
    value_border = [frame_border, {"AXIdentifier": "spinEditTextField"}]
    arrow_up_border = [frame_border, {"AXIdentifier": "IDC_SPINEDIT_BTN_UP"}]
    arrow_down_border = [frame_border, {"AXIdentifier": "IDC_SPINEDIT_BTN_DOWN"}]

    slider_interclip = {"AXIdentifier": "IDC_VIDEO_COLLAGE_SETTINGPANEL_SLIDER_INTERCLIP_SIZE"}
    frame_interclip = {"AXIdentifier": "IDC_VIDEO_COLLAGE_SETTINGPANEL_SPINEDIT_INTERCLIP_SIZE"}
    value_interclip = [frame_interclip, {"AXIdentifier": "spinEditTextField"}]
    arrow_up_interclip = [frame_interclip, {"AXIdentifier": "IDC_SPINEDIT_BTN_UP"}]
    arrow_down_interclip = [frame_interclip, {"AXIdentifier": "IDC_SPINEDIT_BTN_DOWN"}]

    menu_fill_type = {"AXIdentifier": "IDC_VIDEO_COLLAGE_SETTINGPANEL_COMBOBOX_FILL_TYPE"}
    menu_item_uniform = [menu_fill_type, {"AXValue":"Uniform color"}]
    menu_item_interclip = [menu_fill_type, {"AXValue":"Interclip texture"}]

    btn_color = {"AXIdentifier": "IDC_VIDEO_COLLAGE_SETTINGPANEL_BUTTON_COLOR"}
    btn_uniform_color = {"AXIdentifier": "IDC_VIDEO_COLLAGE_SETTINGPANEL_BUTTON_UNIFORM_COLOR"}
    text_hex = {"AXIdentifier": "hex"}

    menu_frame_animation = {"AXIdentifier": "IDC_VIDEO_COLLAGE_SETTINGPANEL_COMBOBOX_FRAME_ANIMATION"}
    menu_item_begining = [menu_frame_animation, {"AXValue":"From Beginning"}]
    menu_item_from_beginning = [menu_frame_animation, {"AXValue": "From Beginning"}]
    menu_item_during_closing = [menu_frame_animation, {"AXValue": "During Closing"}]
    menu_item_off = [menu_frame_animation, {"AXValue": "Off"}]

    radio_with_frame_animation = {"AXIdentifier": "IDC_VIDEO_COLLAGE_SETTINGPANEL_RADIOBUTTON_START_WITH_ANIMATION"}
    radio_after_frame_animation = {"AXIdentifier": "IDC_VIDEO_COLLAGE_SETTINGPANEL_RADIOBUTTON_START_AFTER_ANIMATION"}
    radio_pause_with_frame_animation = {"AXIdentifier": "IDC_VIDEO_COLLAGE_SETTINGPANEL_RADIOBUTTON_PAUSE_AFTER_ANIMATION"}
    radio_pause_after_frame_animation = {"AXIdentifier": "IDC_VIDEO_COLLAGE_SETTINGPANEL_RADIOBUTTON_PAUUSE_WITH_ANIMATION"}
    radio_freeze_the_video = {"AXIdentifier": "IDC_VIDEO_COLLAGE_SETTINGPANEL_RADIOBUTTON_FREEZE"}
    radio_display_color_board = {"AXIdentifier": "IDC_VIDEO_COLLAGE_SETTINGPANEL_RADIOBUTTON_COLORBOARD"}
    radio_restart_playback = {"AXIdentifier": "IDC_VIDEO_COLLAGE_SETTINGPANEL_RADIOBUTTON_RESTART"}
    btn_before_after_color_board = {"AXIdentifier": "IDC_VIDEO_COLLAGE_SETTINGPANEL_BUTTON_COLORBOARD"}
    btn_advanced_setting = {"AXIdentifier": "IDC_VIDEO_COLLAGE_SETTINGPANEL_BUTTON_ADVANCE_SETTING"}

    btn_close = [{"AXSubrole": "AXFloatingWindow"}, {"AXSubrole": "AXCloseButton"}]

    class advanced:
        radio_all_at_once = {"AXIdentifier": "IDC_VIDEO_COLLAGE_ADVSETTINGDLG_RADIOBUTTON_ALL_AT_ONCE"}
        radio_delay = {"AXIdentifier": "IDC_VIDEO_COLLAGE_ADVSETTINGDLG_RADIOBUTTON_DELAY"}
        radio_one_after_another = {"AXIdentifier": "IDC_VIDEO_COLLAGE_ADVSETTINGDLG_RADIOBUTTON_ONE_AFTER_ANOTHER"}

        frame_delay_sec = {"AXIdentifier": "IDC_VIDEO_COLLAGE_ADVSETTINGDLG_SPINEDIT_DELAY"}
        input_delay_sec = [frame_delay_sec, {"AXRole": "AXTextField"}]

        menu_collage_duration = {"AXIdentifier": "IDC_VIDEO_COLLAGE_ADVSETTINGDLG_COMBOBOX_MATCH_DURATION"}
        menu_item_all_video = [menu_collage_duration, {"AXValue": "All Videos"}]
        menu_item_longest_clip = [menu_collage_duration, {"AXValue": "Longest Clip"}]
        menu_item_shortest_clip = [menu_collage_duration, {"AXValue": "Shortest Clip"}]
        menu_item_clip1 = [menu_collage_duration, {"AXValue": "Clip 1"}]
        menu_item_clip2 = [menu_collage_duration, {"AXValue": "Clip 2"}]
        menu_item_clip3 = [menu_collage_duration, {"AXValue": "Clip 3"}]
        menu_item_clip4 = [menu_collage_duration, {"AXValue": "Clip 4"}]

        btn_default = {"AXIdentifier": "IDC_VIDEO_COLLAGE_ADVSETTINGDLG_BUTTON_DEFAULT"}
        btn_cancel = {"AXIdentifier": "IDC_VIDEO_COLLAGE_ADVSETTINGDLG_BUTTON_CANCEL"}
        btn_ok = {"AXIdentifier": "IDC_VIDEO_COLLAGE_ADVSETTINGDLG_BUTTON_OK"}


class media:
    scroll_bar = {"AXIdentifier": "_NS:129"} # 3303: _NS:118  2922: _NS:129
    btn_import = {"AXIdentifier": "IDC_THEME_BUTTON_IMPORT_MEDIA"}
    menu_media = {"AXIdentifier": "IDC_VIDEO_COLLAGE_LIBRARY_COMBOBOX"}
    menu_item_all_media = [menu_media, {"AXRole": "AXStaticText", "AXValue": "All Media"}]
    menu_item_video = [menu_media, {"AXRole":"AXStaticText", "AXValue":"Videos"}]
    menu_item_image = [menu_media, {"AXRole":"AXStaticText", "AXValue":"Images"}]
    menu_item_color_board = [menu_media, {"AXRole": "AXStaticText", "AXValue": "Color Boards"}]
    btn_auto_fill = {"AXIdentifier": "IDC_VIDEO_COLLAGE_BUTTON_AUTO_FILL"}
    template = {"AXIdentifier": "IDS_VIDOE_COLLAGE_ENTITY_NAME"} # 3303: _NS:32    2922: _NS:32
    btn_yes = [{"AXSubrole":"AXDialog"} ,{"AXTitle": "Yes", "recursive":False}]
    btn_no = [{"AXSubrole":"AXDialog"} ,{"AXTitle": "No", "recursive":False}]
    btn_yes_to_all = [{"AXSubrole":"AXDialog"} ,{"AXTitle": "Yes to All", "recursive":False}]
    btn_no_to_all = [{"AXSubrole":"AXDialog"} ,{"AXTitle": "No to All", "recursive":False}]

class layout:
    frame = {"AXIdentifier":"IDC_VIDEO_COLLAGE_TEMPLATEPANEL_SCROLLVIEW"}
    templates = {"AXIdentifier":"TemplateCollectionViewItem"}
    arrow_right = {"AXIdentifier":"IDC_VIDEO_COLLAGE_TEMPLATE_BUTTON_NEXT"}
    arrow_left = {"AXIdentifier":"IDC_VIDEO_COLLAGE_TEMPLATE_BUTTON_PREVIOUS"}
    menu_category = {"AXIdentifier":"IDC_VIDEO_COLLAGE_TEMPLATE_COMBOBOX"}
    menu_item_all = [menu_category, {"AXValue":"All"}]
    menu_item_custom = [menu_category, {"AXValue":"Custom"}]
    menu_item_downloaded = [menu_category, {"AXValue":"Downloaded"}]

    btn_layout_library = {"AXIdentifier": "IDC_VIDEO_COLLAGE_TEMPLATE_BUTTON_POPUP_TEMPLATE_DLG"}
    btn_yes = {"AXIdentifier":"IDC_CLALERT_BUTTON_0"}
    btn_no = {"AXIdentifier":"IDC_CLALERT_BUTTON_1"}

    class library:
        frame = {"AXIdentifier":"IDS_VIDEO_COLLAGE_TEMPLATE_DLG_WINDOW"} # 3303: _NS:10   2922: _NS:10
        scroll_bar = {"AXIdentifier": "IDS_VIDEO_COLLAGE_TEMPLATE_DLG_VERTICAL_SCROLLBAR"} # 3303: _NS:90    2922: _NS:116
        menu_category = {"AXIdentifier":"IDC_VIDEO_COLLAGE_TEMPLATEDLG_COMBOBOX_FILTER"}
        menu_item_all = [menu_category, {"AXValue":"All"}]
        menu_item_custom = [menu_category, {"AXValue":"Custom"}]
        menu_item_downloaded = [menu_category, {"AXValue":"Downloaded"}]
        btn_zoom = [frame, {"AXRoleDescription":"zoom button"}]
        btn_close = [frame, {"AXRoleDescription":"close button"}]
        templates = [frame, {"AXIdentifier":"TemplateCollectionViewItem", "get_all":True}]
        btn_ok = {"AXIdentifier": "IDC_VIDEO_COLLAGE_TEMPLATEDLG_BUTTON_OK"}
        btn_cancel = {"AXIdentifier": "IDC_VIDEO_COLLAGE_TEMPLATEDLG_BUTTON_CANCEL"}


class save_as:
    input_name = {"AXIdentifier": "IDC_SAVE_TEMPLATE_EDIT_TEMPLATE_NAME"}
    slider = {"AXIdentifier": "IDC_SAVE_TEMPLATE_SLIDER_MARK_FRAME"}
    btn_ok = {"AXIdentifier": "IDC_SAVE_TEMPLATE_BTN_OK"}
    btn_cancel = {"AXIdentifier": "IDC_SAVE_TEMPLATE_BTN_CANCEL"}


class cancel:
    yes = {"AXIdentifier": "IDC_CLALERT_BUTTON_0"}
    no = {"AXIdentifier": "IDC_CLALERT_BUTTON_1"}
    cancel = {"AXIdentifier": "IDC_CLALERT_BUTTON_2"}


class share:
    checkbox_auto_sign_in = {"AXIdentifier": "IDC_STATIC_DIRECTORZONE_AUTOLOGIN"}
    btn_auto_sign_in_ok = {"AXIdentifier": "IDC_SSO_BUTTON_YES"}
    menu_upload_to = {"AXIdentifier": "IDC_UPLOADTEMPLATE_HOWLOADTO"}
    menu_item_cloud_and_dz = {"AXValue": "CyberLink Cloud and DirectorZone"}
    menu_item_cloud = {"AXValue": "CyberLink Cloud"}
    menu_item_dz = {"AXValue": "DirectorZone"}
    input_title = {"AXIdentifier": "_NS:96"} # 3303: _NS:96    2922: _NS:96
    input_tag = {"AXIdentifier": "IDC_UPLOADTEMPLATE_TAGS"}
    input_collection = {"AXIdentifier": "IDC_UPLOADTEMPLATE_COLLECTION"}
    input_description = {"AXIdentifier": "IDC_UPLOADTEMPLATE_DESCRIPTION"}
    btn_next = {"AXIdentifier": "IDC_UPLOADTEMPLATE_NEXT"}
    btn_confirm = {"AXIdentifier": "IDC_UPLOADTEMPLATE_CONFIRM"}
    btn_finish = {"AXIdentifier": "IDC_UPLOADTEMPLATE_FINISH"}


class preview:
    play = {"AXIdentifier": "IDC_VIDEO_COLLAGE_BUTTON_PLAY"}
    pause = {"AXIdentifier": "IDC_VIDEO_COLLAGE_BUTTON_PAUSE"}
    stop = {"AXIdentifier": "IDC_VIDEO_COLLAGE_BUTTON_STOP"}
    previous_frame = {"AXIdentifier": "IDC_VIDEO_COLLAGE_BUTTON_PREVIOUS_FRAME"}
    next_frame = {"AXIdentifier": "IDC_VIDEO_COLLAGE_BUTTON_NEXT_FRAME"}

    btn_snapshot = {"AXIdentifier": "IDC_VIDEO_COLLAGE_BUTTON_SNAPSHOT"}
    btn_replace = {"AXTitle": "Replace", "AXRole": "AXButton"}
    menu_quality = {"AXIdentifier": "IDC_VIDEO_COLLAGE_BUTTON_PREVIEW_QUALITY"}
    menu_item_quality = [main_window, {"AXRole": "AXMenuItem"}]
    btn_volume = {"AXIdentifier": "IDC_VIDEO_COLLAGE_BUTTON_VOLUME"}
    slider_volumn = {"AXIdentifier": "IDC_VOLUME_POPOVER_SLIDER"}
    slider_playback = {"AXIdentifier": "IDC_VIDEO_COLLAGE_EDITORPANEL_SLIDER_PLAYBACK"}

    btn_set_duration = {"AXIdentifier": "IDS_VIDEO_COLLAGE_BTN_DURATION"} # 3303: _NS:48    2922: _NS:46
    btn_zoom_in = {"AXIdentifier": "IDS_VIDEO_COLLAGE_BTN_ZOOM_IN"} # 3303: _NS: 46   2922: _NS:46
    btn_zoom_out = {"AXIdentifier": "IDS_VIDEO_COLLAGE_BTN_ZOOM_OUT"} # 3303: _NS:9   2922: _NS:9
    slider_zoom = {"AXIdentifier": "IDS_VIDEO_COLLAGE_SLIDER_ZOOM", "AXRole":"AXSlider"} # 3303: _NS: 67   2922: _NS:67
    btn_trim = {"AXIdentifier": "IDS_VIDEO_COLLAGE_BTN_TRIM"} # 3303: _NS:9    2922: _NS:9
    btn_mute = {"AXIdentifier": "IDS_VIDEO_COLLAGE_BTN_MUTE", "AXRole":"AXCheckBox"} # 3303: _NS:67    2922: _NS:64

    timecode_duration = [{"AXIdentifier": "IDC_VIDEO_COLLAGE_TIME_EDIT", "AXRole":"AXGroup"}, {"AXIdentifier": "spinTimeEditTextField"}] # 3303: _NS:69    2922: _NS:11
    btn_ok = {"AXIdentifier": "IDC_DURATION_BTN_OK"}