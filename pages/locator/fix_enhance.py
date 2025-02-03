btn_close = {"AXIdentifier": "IDC_FIX_ENHANCE_BTN_LEAVE"}
btn_reset = {"AXIdentifier": "IDC_FIX_ENHANCE_BTN_RESET"}
btn_keyframe = {"AXIdentifier": "IDC_FIX_ENHANCE_BTN_KEYFRAME"}
btn_apply_to_all = {"AXIdentifier": "IDC_FIX_ENHANCE_BTN_APPLY_ALL"}

checkbox_compare_in_split_preview = {"AXIdentifier": "IDC_FIX_ENHANCE_BTN_CHECK_COMPARE_SPLIT"}


class AdjustSet:
    def __init__(self, frame, **kwargs):
        self.slider = [frame, {"AXIdentifier": "IDC_SLIDER"}]
        self.value = [frame, {"AXIdentifier": "spinEditTextField"}]
        self.arrow_up = [frame, {"AXIdentifier": "IDC_SPINEDIT_BTN_UP"}]
        self.arrow_down = [frame, {"AXIdentifier": "IDC_SPINEDIT_BTN_DOWN"}]
        self.btn_plus = [frame, {"AXIdentifier": "IDC_BUTTON_SLIDER_PARAM_CTRL_BTN_INCREASE"}]
        self.btn_minus = [frame, {"AXIdentifier": "IDC_BUTTON_SLIDER_PARAM_CTRL_BTN_DECREASE"}]
        for k, v in kwargs.items():
            self.__setattr__(k, [frame, v])
        self.group = [self.slider, self.value, self.arrow_up, self.arrow_down, self.btn_plus, self.btn_minus]


class fix:
    frame_lighting_adjustment = {"AXIdentifier": "autolight"}
    frame_white_balance = {"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_WHITEBALANCE"}
    frame_video_stabilizer = {"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_VIDEO_STABILIZER"}
    frame_lens_correction = {"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_LENS_CORRECTION"}
    frame_video_denoise = {"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_VIDEO_DENOISE"}
    frame_audio_denoise = {"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_AUDIO_DENOISE"}
    frame_wind_removal = {"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_WIND_REMOVAL"}

    checkbox_lighting_adjustment = [frame_lighting_adjustment, {"AXIdentifier": "IDC_BTN_CHECKBTN"}]
    checkbox_white_balance = [frame_white_balance, {"AXIdentifier": "IDC_BTN_CHECKBTN"}]
    checkbox_video_stabilizer = [frame_video_stabilizer, {"AXIdentifier": "IDC_BTN_CHECKBTN"}]
    checkbox_lens_correction = [frame_lens_correction, {"AXIdentifier": "IDC_BTN_CHECKBTN"}]
    checkbox_video_denoise = [frame_video_denoise, {"AXIdentifier": "IDC_BTN_CHECKBTN"}]
    checkbox_audio_denoise = [frame_audio_denoise, {"AXIdentifier": "IDC_BTN_CHECKBTN"}]

    tab_white_balance = [frame_white_balance, {"AXIdentifier": "IDC_CHECKBUTTON_RIGHT_BTN"}]
    tab_video_stabilizer = [frame_video_stabilizer, {"AXIdentifier": "IDC_CHECKBUTTON_RIGHT_BTN"}]
    tab_lens_correction = [frame_lens_correction, {"AXIdentifier": "IDC_CHECKBUTTON_RIGHT_BTN"}]
    tab_audio_denoise = [frame_audio_denoise, {"AXIdentifier": "IDC_CHECKBUTTON_RIGHT_BTN"}]
    tab_lighting_adjustment = [frame_lighting_adjustment, {"AXIdentifier": "IDC_CHECKBUTTON_RIGHT_BTN"}]
    tab_video_denoise = [frame_video_denoise, {"AXIdentifier": "IDC_CHECKBUTTON_RIGHT_BTN"}]
    tab_wind_removal = [frame_wind_removal, {"AXIdentifier": "IDC_CHECKBUTTON_RIGHT_BTN"}]

    class lighting_adjustment:
        extreme_backlight = AdjustSet({"AXIdentifier": "strength"})
        extreme_backlight.slider[-1]["AXIdentifier"] = "IDC_FIX_ENHANCE_SLIDER_PARAMCTRL"  # it is different from others
        btn_extreme_backlight = {"AXIdentifier": "extremeMode"}

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
            btn_i = [frame, {"AXIdentifier": "IDC_WHITE_BALANCE_DIALOG_BTN_CALIBRATED"}]
            btn_close = [frame, {"AXRole": "AXButton", "AXRoleDescription": "close button"}]
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
        btn_plus_vignette_amount = [frame_vignette_amount,
                                    {"AXIdentifier": "IDC_BUTTON_SLIDER_PARAM_CTRL_BTN_INCREASE"}]
        btn_minus_vignette_amount = [frame_vignette_amount,
                                     {"AXIdentifier": "IDC_BUTTON_SLIDER_PARAM_CTRL_BTN_DECREASE"}]
        group_vignette_amount = [slider_vignette_amount, value_vignette_amount, arrow_up_vignette_amount,
                                 arrow_down_vignette_amount,
                                 btn_plus_vignette_amount, btn_minus_vignette_amount]

        frame_vignette_midpoint = {"AXIdentifier": "IDS_Vi_Param_MidPoint_Name"}
        slider_vignette_midpoint = [frame_vignette_midpoint, {"AXIdentifier": "IDC_FIX_ENHANCE_SLIDER_PARAMCTRL"}]
        value_vignette_midpoint = [frame_vignette_midpoint, {"AXIdentifier": "spinEditTextField"}]
        arrow_up_vignette_midpoint = [frame_vignette_midpoint, {"AXIdentifier": "IDC_SPINEDIT_BTN_UP"}]
        arrow_down_vignette_midpoint = [frame_vignette_midpoint, {"AXIdentifier": "IDC_SPINEDIT_BTN_DOWN"}]
        btn_plus_vignette_midpoint = [frame_vignette_midpoint,
                                      {"AXIdentifier": "IDC_BUTTON_SLIDER_PARAM_CTRL_BTN_INCREASE"}]
        btn_minus_vignette_midpoint = [frame_vignette_midpoint,
                                       {"AXIdentifier": "IDC_BUTTON_SLIDER_PARAM_CTRL_BTN_DECREASE"}]
        group_vignette_midpoint = [slider_vignette_midpoint, value_vignette_midpoint, arrow_up_vignette_midpoint,
                                   arrow_down_vignette_midpoint,
                                   btn_plus_vignette_midpoint, btn_minus_vignette_midpoint]

    class video_stabilizer:
        correction_level = AdjustSet({"AXIdentifier": "cutLevel"})
        correction_level.slider[-1]["AXIdentifier"] = "IDC_FIX_ENHANCE_SLIDER_PARAMCTRL"
        bb_text = {'AXValue': 'Find the feature in Fix / Enhance to correct shaking videos.',
                   'AXRole': "AXStaticText"}

    class video_denoise:
        degree = AdjustSet({"AXIdentifier": "strength"})
        degree.slider[-1]["AXIdentifier"] = "IDC_FIX_ENHANCE_SLIDER_PARAMCTRL"
        bb_text = {'AXValue': 'Find the feature in Fix / Enhance to remove signal noise from the video clip.', 'AXRole': "AXStaticText"}

    class audio_denoise:
        menu_noise_type = {"AXIdentifier": "Preset"}
        menu_item_noise_type = [menu_noise_type, {"AXRole": "AXStaticText"}]
        degree = AdjustSet({"AXIdentifier": "Strength"})
        degree.slider[-1]["AXIdentifier"] = "IDC_FIX_ENHANCE_SLIDER_PARAMCTRL"
        bb_text = {'AXValue': 'Find the feature in Fix / Enhance to enhance your audio quality.',
                   'AXRole': "AXStaticText"}

    class wind_removal:
        # On fix/enhance > wind removal page
        btn_wind_removal = {"AXIdentifier": "IDC_MCLP_BUTTON_WIND_REMOVAL"}
        # On Wind Removal window
        main_window = {"AXIdentifier": "IDD_WIND_REMOVAL"}
        btn_apply = {"AXIdentifier": "IDC_BUTTON_OK", 'AXTitle': 'Apply'}
        bb_text_1 = {'AXValue': 'Preview and compare the effects before and after applying AI Wind Removal.',
                   'AXRole': "AXStaticText"}
        bb_text_2 = {'AXValue': 'Find the feature in Fix / Enhance to remove wind noise.',
                   'AXRole': "AXStaticText"}

class PickColor:
    main_window = {"AXTitle": "Color", "AXRole": "AXWindow"}
    hue = AdjustSet([main_window, {"AXIdentifier": "IDC_COLOR_SCENE_EDIT_HUE", "index": 0}])
    saturation = AdjustSet([main_window, {"AXIdentifier": "IDC_COLOR_SCENE_EDIT_SATURATION", "index": 0}])
    btn_ok = [main_window, {"AXRole": "AXButton", "AXTitle": "OK"}]


class enhance:
    frame_color_adjustment = {"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_COLORAJUSTMENT"}
    frame_split_toning = {"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_SPLITTONE"}
    frame_hdr_effect = {"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_HDR"}
    frame_color_match = {"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_COLORMATCH"}
    frame_color_enhancement = {"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_TTColor"}
    frame_speech_enhancement = {"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_SPEECH_ENHANCE"}

    checkbox_color_adjustment = [frame_color_adjustment, {"AXIdentifier": "IDC_BTN_CHECKBTN"}]
    checkbox_split_toning = [frame_split_toning, {"AXIdentifier": "IDC_BTN_CHECKBTN"}]
    checkbox_hdr_effect = [frame_hdr_effect, {"AXIdentifier": "IDC_BTN_CHECKBTN"}]
    checkbox_color_match = [frame_color_match, {"AXIdentifier": "IDC_BTN_CHECKBTN"}]
    checkbox_color_enhancement = [frame_color_enhancement, {"AXIdentifier": "IDC_BTN_CHECKBTN"}]
    bb_color_adjustment = {'AXValue': 'Manually adjust the color attributes (exposure, brightness, contrast, hue, etc.)', 'AXRole': "AXStaticText"}
    bb_color_enhancement = {'AXValue': 'Find the feature in Fix / Enhance to make the colors in the video more vivid.', 'AXRole': "AXStaticText"}

    tab_color_adjustment = [frame_color_adjustment, {"AXIdentifier": "IDC_CHECKBUTTON_RIGHT_BTN"}]
    tab_split_toning = [frame_split_toning, {"AXIdentifier": "IDC_CHECKBUTTON_RIGHT_BTN"}]
    tab_hdr_effect = [frame_hdr_effect, {"AXIdentifier": "IDC_CHECKBUTTON_RIGHT_BTN"}]
    tab_color_match = [frame_color_match, {"AXIdentifier": "IDC_CHECKBUTTON_RIGHT_BTN"}]
    tab_color_enhancement = [frame_color_enhancement, {"AXIdentifier": "IDC_CHECKBUTTON_RIGHT_BTN"}]
    tab_speech_enhancement = [frame_speech_enhancement, {"AXIdentifier": "IDC_CHECKBUTTON_RIGHT_BTN"}]

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

    class split_toning:
        class ModuleSet:
            pick_color = PickColor()

            def __init__(self, index=0):
                hue = AdjustSet({"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_HUE", "index": index})
                saturation = AdjustSet({"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_SATURATION", "index": index})
                btn_pick_color = [{"AXIdentifier": "IDD_LIBRARY"},
                                  {"AXRole": "AXScrollArea", "index": 1, "recursive": False},
                                  {"AXRole": "AXGroup"},
                                  {"AXRole": "AXButton", "index": [1, 0][index], "recursive": False}]  # strange index
                self.groups = [{"hue": hue}, {"saturation": saturation}, btn_pick_color]

        balance = AdjustSet({"AXIdentifier": "IDC_FIX_ENHANCE_GROUP_BALANCE"})
        highlights = ModuleSet(0)
        shadow = ModuleSet(1)

    class hdr_effect:
        frame = [{'AXIdentifier': 'IDD_LIBRARY'}, {'AXRole': 'AXScrollArea', 'index': 1, 'recursive': False}]
        scroll_bar = [frame, {"AXRole": "AXScrollBar"}]

        class grow:
            strength = AdjustSet({"AXIdentifier": "IDS_Co_Param_GlowStrength_Name"},
                                 slider={"AXIdentifier": "IDC_FIX_ENHANCE_SLIDER_PARAMCTRL"})
            radius = AdjustSet({"AXIdentifier": "IDS_Co_Param_GlowRadius_Name"},
                               slider={"AXIdentifier": "IDC_FIX_ENHANCE_SLIDER_PARAMCTRL"})
            balance = AdjustSet({"AXIdentifier": "IDS_Co_Param_GlowBalance_Name"},
                                slider={"AXIdentifier": "IDC_FIX_ENHANCE_SLIDER_PARAMCTRL"})
            groups = [{"strength": strength}, {"radius": radius}, {"balance": balance}]

        class edge:
            strength = AdjustSet({"AXIdentifier": "IDS_Co_Param_EdgeStrength_Name"},
                                 slider={"AXIdentifier": "IDC_FIX_ENHANCE_SLIDER_PARAMCTRL"})
            radius = AdjustSet({"AXIdentifier": "IDS_Co_Param_EdgeRadius_Name"},
                               slider={"AXIdentifier": "IDC_FIX_ENHANCE_SLIDER_PARAMCTRL"})
            balance = AdjustSet({"AXIdentifier": "IDS_Co_Param_EdgeBalance_Name"},
                                slider={"AXIdentifier": "IDC_FIX_ENHANCE_SLIDER_PARAMCTRL"})
            groups = [{"strength": strength}, {"radius": radius}, {"balance": balance}]

    class color_match:
        # stay fix/enhance page
        btn_color_match = {"AXIdentifier": "IDC_FIX_ENHANCE_BTN_COLOR_MATCH", "AXRole": "AXButton", "AXTitle": "Color Match"}

        # enter (Color match) page
        btn_match_color = {"AXIdentifier": "IDC_COLOR_MATCH_BTN_MATCH_COLOR", "AXTitle": "Match Color"}
        setting_scroll_view = {"AXIdentifier": "IDC_COLOR_MATCH_SCROLLVIEW", "AXRole": "AXScrollArea"}

        # close button
        btn_close = {"AXIdentifier": "IDC_LIB_PREVIEW_BTN_CLOSE", "AXRole": "AXButton"}

    class color_enhancement:
        degree = AdjustSet({"AXIdentifier": "strength"})
        degree.slider[-1]["AXIdentifier"] = "IDC_FIX_ENHANCE_SLIDER_PARAMCTRL"

    class speech_enhancement:
        # On fix/enhance > speech enhancement page
        btn_speech_enhancement = {"AXIdentifier": "IDC_MCLP_BUTTON_SPEECH_ENHANCE"}
        # On Wind Removal window
        main_window = {"AXIdentifier": "IDD_SPEECH_ENHANCE"}
        btn_apply = {"AXIdentifier": "IDC_BUTTON_OK", 'AXTitle': 'Apply'}
        compensation = AdjustSet({"AXIdentifier": "IDC_EDITOR_COMPENSATION"}, slider={"AXIdentifier": "IDC_SLIDER_COMPENSATION"})
        bb_text_1 = {'AXValue': 'Preview and compare the effects before and after applying Speech Enhancement.', 'AXRole': "AXStaticText"}
        bb_text_2 = {'AXValue': 'Find feature in Fix / Enhance to enhance to sound like recorded in a professional studio.',
                     'AXRole': "AXStaticText"}