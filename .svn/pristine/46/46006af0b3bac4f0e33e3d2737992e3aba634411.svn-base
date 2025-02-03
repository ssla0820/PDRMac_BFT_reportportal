window = {"AXIdentifier": "IDC_DOWNLOAD_FROM_SHUTTERSTOCK_DLG"}
ss_title_txt = [window, {"AXRole": "AXStaticText", "AXIdentifier": "_NS:72"}]
waiting_cursor = [window,{"AXIdentifier": "_NS:278", "recursive": False}] # 3303:_NS:304    2922: _NS:278

btn_close = [window, {"AXSubrole": "AXCloseButton"}]
btn_zoom = [window, {"AXSubrole": "AXZoomButton"}]

btn_i = {"AXIdentifier": "IDC_SHUTTERSTOCK_BTN_INFO"}     # 3615:_NS:577, 3310:_NS:329     2922: _NS:150
text_i = {"AXValue": "Shutterstock Terms of Use"}
btn_i_close = {"AXIdentifier": "IDC_SHUTTERSTOCK_TERMS_OF_USE_BTN_OK", "AXTitle": "OK"}    # 3615:_NS:37, 3310:_NS:9      2922: _NS:9

btn_download = {"AXIdentifier": "IDC_SHUTTERSTOCK_BTN_DOWNLOAD"}  # 3615:_NS:615, 3310:_NS:87    2922: _NS:332
btn_next_page = {"AXIdentifier": "IDC_SHUTTERSTOCK_BTN_NEXT_PAGE"}  # 3615:_NS:781, 3310:_NS:189      2922: _NS:130
btn_previous_page = {"AXIdentifier": "IDC_SHUTTERSTOCK_BTN_PREV_PAGE"}  # 3615:_NS:759, 3310:_NS:342      2922: _NS:168
# Download Music for Meta window
btn_ok = {"AXTitle": "OK", "AXIdentifier": 'IDC_DOWNLOADCLBGM_BTN_CLOSE'}

scroll_media = [window, {"AXRole":"AXValueIndicator"}]

frame_section = {"AXSubrole":"AXSectionList"}
frame_scroll_view = {"AXIdentifier": "IDC_SHUTTERSTOCK_COLLECTION_VIEW"} # 3615:_NS:194, 3310:_NS:434      2922: _NS:445

frame_clip = {"AXIdentifier": "ShutterstockCollectionViewItem"}
frame_clips = {"AXIdentifier": "ShutterstockCollectionViewItem", "get_all":True}
checkbox_select = [frame_clip, {"AXRole":"AXButton"}] # bug in 2922, hierarchy issue

text_page_number = {"AXIdentifier": "IDC_SHUTTERSTOCK_TEXT_INPUT_PAGE"} # 3615:_NS:777, 3310:_NS:362         2922: _NS:171
text_total_page_number = {"AXIdentifier": "IDC_SHUTTERSTOCK_TEXT_TOTAL_PAGE"}    # 3615:_NS:796, 3310:_NS:372       2922: _NS:374

btn_library = {"AXIdentifier": "IDC_SHUTTERSTOCK_BTN_LIBRARY"} # 3615:_NS:397, 3310:_NS:169        2922: _NS:9
menu_item_library_icons = [btn_library, {"AXRole":"AXMenuItem", "get_all":True}]

text_selected_amount = {"AXIdentifier": "IDC_SHUTTERSTOCK_TEXT_SELECTED_CLIPS"}  # 3615:_NS:757, 3310: _NS:340     2922: _NS:345
image_clip = {"AXIdentifier": "ShutterstockCollectionViewItem"} # _NS:47

btn_video_tab = {"AXTitle": "Video", "AXRole": "AXButton"}
btn_photo_tab = {"AXTitle": "Photo", "AXRole": "AXButton"}
btn_music_tab = {"AXTitle": "Music", "AXRole": "AXButton"}

img_waiting_cursor = {"AXRoleDescription":"p 05"}

#20.7.4210 add
class max_preview:
    main_window = {"AXIdentifier": "_NS:8", "AXRole": 'AXWindow', "AXTitle": "Window"}
    btn_close = [main_window, {"AXRoleDescription": "close button"}]

class music:
    btn_play = {"AXIdentifier": "IDC_SHUTTERSTOCK_BTN_PLAY_PAUSE"}
    btn_pause = {"AXIdentifier": "IDC_SHUTTERSTOCK_BTN_PLAY_PAUSE"}
    btn_stop = {"AXIdentifier": "IDC_SHUTTERSTOCK_BTN_STOP"}  # 3615:  _NS:648    2922: _NS:419
    btn_mute = {"AXIdentifier": "IDC_SHUTTERSTOCK_BTN_MUTE_ON_OFF"}   # 3615:_NS:551, 3310:  _NS:210   2922: _NS:46
    btn_volumn = {"AXIdentifier": "IDC_SHUTTERSTOCK_SLIDER_VOLUME"}    # 3615:_NS:823 , 3310: _NS:416   2922: _NS:423

    btn_sort = btn_library
    menu_table_header_view = {"AXIdentifier": "IDC_SHUTTERSTOCK_TABLE_HEADER_VIEW", "AXRole": 'AXGroup'} # 3904: _NS:329,  3630: _NS: 201, 3615: _NS:259, 3310:_NS:487
    menu_item_sort = [btn_sort, {"AXRole":"AXMenuItem"},{"AXRole":"AXMenuItem","get_all":True}]

    table_clip = {"AXIdentifier": "IDC_LIBRARY_TABLEVIEW_DETAILED"}    # 3615:_NS:255, 3310: _NS:483     2922: _NS:494
    rows_clip = [table_clip, {"AXSubrole":"AXTableRow","get_all": True,"recursive": False}]

    frame_scroll_view = {"AXIdentifier": "IDC_DOWNLOADCLBGM_SCROLLVIEW_DETAILEDTABLEVIEW"} # 3615:_NS:251, 3310: _NS:479    2922: _NS:490
    scroll_media = [{"AXRole":"AXScrollArea"},{"AXRole":"AXScrollBar","recursive":False}]


class download:
    frame = {"AXIdentifier": "IDC_PROGRESS_DIALOG"}  # 3303: _NS:10   2922: _NS:10
    progress_dl = {"AXRole": "AXProgressIndicator"}
    text_dl = {"AXIdentifier": "IDC_PROGRESS_TEXT_FIRST_PART"}    # 3303: _NS:54      2922: _NS:54 IDC_PROGRESS_TEXT_FIRST_PART
    btn_cancel = {"AXIdentifier": "IDC_PROGRESS_BTN_CANCEL"} #  2922: _NS:11
    btn_complete_ok = [{"AXIdentifier": "IDD_CLALERT"}, {"AXIdentifier": "IDC_CLALERT_BUTTON_0", "AXTitle": 'OK'}]
    txt_complete_msg = {'AXIdentifier': 'IDC_CLALERT_MESSAGE'}

    class hd_video:
        checkbox_dont_show_again = {"AXIdentifier": "IDC_CLALERT_SUPPRESSION_BUTTON"}
        btn_yes = {"AXIdentifier": "IDC_CLALERT_BUTTON_0"}
        btn_no = {"AXIdentifier": "IDC_CLALERT_BUTTON_1"}


class search_not_found:
    btn_ok = {"AXIdentifier": "IDC_CLALERT_BUTTON_0"}

class search:
    input_search = {"AXSubrole":"AXSearchField"}
    btn_clear = {"AXDescription":"cancel"}
    btn_not_found_ok = {"AXIdentifier": "IDC_CLALERT_BUTTON_0"}
'''
class AdjustSet:
    def __init__(self, frame):
        self.slider = [frame, {"AXIdentifier": "IDC_SLIDER"}]
        self.value = [frame, {"AXIdentifier": "spinEditTextField"}]
        self.arrow_up = [frame, {"AXIdentifier": "IDC_SPINEDIT_BTN_UP"}]
        self.arrow_down = [frame, {"AXIdentifier": "IDC_SPINEDIT_BTN_DOWN"}]
        self.btn_plus = [frame, {"AXIdentifier": "IDC_BUTTON_SLIDER_PARAM_CTRL_BTN_INCREASE"}]
        self.btn_minus = [frame, {"AXIdentifier": "IDC_BUTTON_SLIDER_PARAM_CTRL_BTN_DECREASE"}]
        self.group = [self.slider, self.value, self.arrow_up, self.arrow_down, self.btn_plus, self.btn_minus]


class fix:
    frame_white_balance = {"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_WHITEBALANCE"}
    frame_video_stabilizer = {"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_VIDEO_STABILIZER"}
    frame_lens_correction = {"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_LENS_CORRECTION"}
    frame_audio_denoise = {"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_AUDIO_DENOISE"}

    checkbox_white_balance = [frame_white_balance, {"AXIdentifier": "IDC_BTN_CHECKBTN"}]
    checkbox_video_stabilizer = [frame_video_stabilizer, {"AXIdentifier": "IDC_BTN_CHECKBTN"}]
    checkbox_lens_correction = [frame_lens_correction, {"AXIdentifier": "IDC_BTN_CHECKBTN"}]
    checkbox_audio_denoise = [frame_audio_denoise, {"AXIdentifier": "IDC_BTN_CHECKBTN"}]

    tab_white_balance = [frame_white_balance, {"AXIdentifier": "IDC_CHECKBUTTON_RIGHT_BTN"}]
    tab_video_stabilizer = [frame_video_stabilizer, {"AXIdentifier": "IDC_CHECKBUTTON_RIGHT_BTN"}]
    tab_lens_correction = [frame_lens_correction, {"AXIdentifier": "IDC_CHECKBUTTON_RIGHT_BTN"}]
    tab_audio_denoise = [frame_audio_denoise, {"AXIdentifier": "IDC_CHECKBUTTON_RIGHT_BTN"}]

    class white_balance:
        radio_color_temperature = {"AXIdentifier": "IDC_FIX_ENHANCE_BTN_COLORTEMPERATURE"}
        radio_white_calibration = {"AXIdentifier": "IDC_FIX_ENHANCE_BTN_WHITECALIBRAT"}

        frame_color_temperature = {"AXIdentifier": "IDS_Co_Param_Temperature_Name"}
        slider_color_temperature = [frame_color_temperature, {"AXIdentifier": "IDC_SLIDER"}]
        value_color_temperature = [frame_color_temperature, {"AXIdentifier": "spinEditTextField"}]
        arrow_up_color_temperature = [frame_color_temperature, {"AXIdentifier": "IDC_SPINEDIT_BTN_UP"}]
        arrow_down_color_temperature = [frame_color_temperature, {"AXIdentifier": "IDC_SPINEDIT_BTN_DOWN"}]
        group_color_temperature = [slider_color_temperature, value_color_temperature, arrow_up_color_temperature,
                                   arrow_down_color_temperature]

        frame_tint = {"AXIdentifier": "IDS_Co_Param_Tint_Name"}
        slider_tint = [frame_tint, {"AXIdentifier": "IDC_SLIDER"}]
        value_tint = [frame_tint, {"AXIdentifier": "spinEditTextField"}]
        arrow_up_tint = [frame_tint, {"AXIdentifier": "IDC_SPINEDIT_BTN_UP"}]
        arrow_down_tint = [frame_tint, {"AXIdentifier": "IDC_SPINEDIT_BTN_DOWN"}]
        group_tint = [slider_tint, value_tint, arrow_up_tint, arrow_down_tint]

        btn_white_calibrate = {"AXIdentifier": "IDS_Vi_Param_ReferencePoint_Name"}

        class white_calibration:
            frame = {"AXSubrole": "AXDialog", "AXTitle": "White Calibration"}
            btn_i = [frame, {"AXRole": "AXButton", "AXTitle": ""}]
            btn_close = [frame, {"AXRole": "AXButton", "AXTitle": "Close"}]
            slider = [frame, {"AXRole": "AXSlider"}]
            btn_cancel = [frame, {"AXRole": "AXButton", "AXTitle": "Cancel"}]
            btn_ok = [frame, {"AXRole": "AXButton", "AXTitle": "OK"}]


    class lens_correction:
        menu_maker = {"AXIdentifier": "IDS_Vi_Param_MakerType_Name"}
        menu_item_maker = [menu_maker, {"AXRole": "AXMenuItem", "get_all": True}, {"AXRole": "AXStaticText"}]
        btn_import_marker = {"AXIdentifier": "IDS_FIX_ENHANCE_BTN_IMPORT_LENS_PROFILE"}
        btn_download = {"AXIdentifier": "IDS_FIX_ENHANCE_BTN_DOWNLOAD_LENS_PROFILE"}

        menu_model = {"AXIdentifier": "IDS_Vi_Param_ProfileType_Name"}
        menu_item_model = [menu_model, {"AXRole": "AXMenuItem"}]

        frame_fisheye = {"AXIdentifier": "IDS_Vi_Param_Distortion_Name"}
        slider_fisheye = [frame_fisheye, {"AXIdentifier": "IDC_FIX_ENHANCE_SLIDER_PARAMCTRL"}]
        value_fisheye = [frame_fisheye, {"AXIdentifier": "spinEditTextField"}]
        arrow_up_fisheye = [frame_fisheye, {"AXIdentifier": "IDC_SPINEDIT_BTN_UP"}]
        arrow_down_fisheye = [frame_fisheye, {"AXIdentifier": "IDC_SPINEDIT_BTN_DOWN"}]
        btn_plus_fisheye = [frame_fisheye, {"AXIdentifier": "IDC_BUTTON_SLIDER_PARAM_CTRL_BTN_INCREASE"}]
        btn_minus_fisheye = [frame_fisheye, {"AXIdentifier": "IDC_BUTTON_SLIDER_PARAM_CTRL_BTN_DECREASE"}]
        group_fisheye = [slider_fisheye, value_fisheye, arrow_up_fisheye, arrow_down_fisheye,
                         btn_plus_fisheye, btn_minus_fisheye]

        frame_vignette_amount = {"AXIdentifier": "IDS_Vi_Param_VignetteRemovalAmounts_Name"}
        slider_vignette_amount = [frame_vignette_amount, {"AXIdentifier": "IDC_FIX_ENHANCE_SLIDER_PARAMCTRL"}]
        value_vignette_amount = [frame_vignette_amount, {"AXIdentifier": "spinEditTextField"}]
        arrow_up_vignette_amount = [frame_vignette_amount, {"AXIdentifier": "IDC_SPINEDIT_BTN_UP"}]
        arrow_down_vignette_amount = [frame_vignette_amount, {"AXIdentifier": "IDC_SPINEDIT_BTN_DOWN"}]
        btn_plus_vignette_amount = [frame_vignette_amount, {"AXIdentifier": "IDC_BUTTON_SLIDER_PARAM_CTRL_BTN_INCREASE"}]
        btn_minus_vignette_amount = [frame_vignette_amount, {"AXIdentifier": "IDC_BUTTON_SLIDER_PARAM_CTRL_BTN_DECREASE"}]
        group_vignette_amount = [slider_vignette_amount, value_vignette_amount, arrow_up_vignette_amount, arrow_down_vignette_amount,
                         btn_plus_vignette_amount, btn_minus_vignette_amount]

        frame_vignette_midpoint = {"AXIdentifier": "IDS_Vi_Param_MidPoint_Name"}
        slider_vignette_midpoint = [frame_vignette_midpoint, {"AXIdentifier": "IDC_FIX_ENHANCE_SLIDER_PARAMCTRL"}]
        value_vignette_midpoint = [frame_vignette_midpoint, {"AXIdentifier": "spinEditTextField"}]
        arrow_up_vignette_midpoint = [frame_vignette_midpoint, {"AXIdentifier": "IDC_SPINEDIT_BTN_UP"}]
        arrow_down_vignette_midpoint = [frame_vignette_midpoint, {"AXIdentifier": "IDC_SPINEDIT_BTN_DOWN"}]
        btn_plus_vignette_midpoint = [frame_vignette_midpoint, {"AXIdentifier": "IDC_BUTTON_SLIDER_PARAM_CTRL_BTN_INCREASE"}]
        btn_minus_vignette_midpoint = [frame_vignette_midpoint, {"AXIdentifier": "IDC_BUTTON_SLIDER_PARAM_CTRL_BTN_DECREASE"}]
        group_vignette_midpoint = [slider_vignette_midpoint, value_vignette_midpoint, arrow_up_vignette_midpoint, arrow_down_vignette_midpoint,
                         btn_plus_vignette_midpoint, btn_minus_vignette_midpoint]


    class video_stabilizer:
        correction_level = AdjustSet({"AXIdentifier": "cutLevel"})
        correction_level.slider[-1]["AXIdentifier"] = "IDC_FIX_ENHANCE_SLIDER_PARAMCTRL"

    class audio_denoise:
        menu_noise_type = {"AXIdentifier": "Preset"}
        menu_item_noise_type = [menu_noise_type, {"AXRole":"AXStaticText"}]
        degree = AdjustSet({"AXIdentifier":"Strength"})
        degree.slider[-1]["AXIdentifier"] = "IDC_FIX_ENHANCE_SLIDER_PARAMCTRL"

class enhance:
    frame_color_adjustment = {"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_COLORAJUSTMENT"}

    checkbox_color_adjustment = [frame_color_adjustment, {"AXIdentifier": "IDC_BTN_CHECKBTN"}]

    tab_color_adjustment = [frame_color_adjustment, {"AXIdentifier": "IDC_CHECKBUTTON_RIGHT_BTN"}]

    class color_adjustment:
        exposure = AdjustSet({"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_EXPOSURE"})
        brightness = AdjustSet({"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_BRIGHTNESS"})
        contrast = AdjustSet({"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_CONTRAST"})
        hue = AdjustSet({"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_HUE"})
        saturation = AdjustSet({"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_SATURATION"})
        vibrancy = AdjustSet({"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_VIBRANCY"})
        highlight_healing = AdjustSet({"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_HIGHLIGHT"})
        shadow = AdjustSet({"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_SHADOW"})
        sharpness = AdjustSet({"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_SHARPNESS"})


'''
