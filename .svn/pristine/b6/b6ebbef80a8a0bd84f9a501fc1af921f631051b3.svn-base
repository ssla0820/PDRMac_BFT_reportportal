class keyframe():
    tab = {'AXIdentifier': '_NS:179', 'AXValue': 'Keyframe Settings'}
    close = {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_LEAVE'}

class fix_enhance():
    tab = {'AXIdentifier': '_NS:170', 'AXValue': 'Fix / Enhance'}
    close = {'AXIdentifier': 'IDC_FIX_ENHANCE_BTN_LEAVE'}

class audio_editor():
    main = {'AXIdentifier': '_NS:12', 'AXRole': 'AXWindow'}
    tab = [main, {"AXRole": "AXButton", "AXTitle": "Effects"}]
    close = {"AXRoleDescription":"close button"}

class pan_zoom():
    tab = {"AXRole": "AXStaticText", "AXValue": 'Pan & Zoom'}
    close = {'AXIdentifier': '_NS:131', 'AXRole': 'AXButton'}

# TipsArea button
class button():
    btn_Import_media = {'AXIdentifier': 'IDC_TIPSAREA_BTN_LOAD_MEDIA'}
    btn_Apply_my_Favorite_transition = {'AXIdentifier': 'IDC_TIPSAREA_BTN_ADDTRANSITION_FAVORITE'}
    btn_Apply_fading_transition = {'AXIdentifier': 'IDC_TIPSAREA_BTN_ADDTRANSITION_FADE'}
    btn_Copy = {'AXIdentifier': 'IDC_TIPSAREA_BTN_COPY'}
    btn_Paste = {'AXIdentifier': 'IDC_TIPSAREA_BTN_PASTE'}
    btn_Cut = {'AXIdentifier': 'IDC_TIPSAREA_BTN_CUT'}
    btn_Remove = {'AXIdentifier': 'IDC_TIPSAREA_BTN_REMOVE'}
    btn_Produce_Range = {'AXIdentifier': 'IDC_TIPSAREA_BTN_PRODUCE_RANGE'}
    btn_Lock_Range = {'AXIdentifier': 'IDC_TIPSAREA_BTN_LOCK_RANGE'}
    btn_Tools = {'AXIdentifier': 'IDC_TIPSAREA_BTN_TOOLS'}
    btn_Fix_Enhance = {'AXIdentifier': 'IDC_TIPSAREA_BTN_FIX_ENHANCE'}
    btn_Keyframe = {'AXIdentifier': 'IDC_TIPSAREA_BTN_KEYFRAME'}
    class more_features():
        main = {'AXIdentifier': 'IDC_TIPSAREA_BTN_MORE_FEATURE'}
        menu = [main,{"AXRole":"AXMenu","recursive":"False"}]
        btn_Remove = {'AXIdentifier': 'removeItem'}
        btn_SelectAll = {'AXIdentifier': 'selectAll'}
        btn_link_unlink = {'AXIdentifier': 'linkUnlinkVideoAndAudio'}
        btn_group_ungroup = {'AXIdentifier': 'groupUngroupObjects'}
        btn_split = {'AXIdentifier': 'clickSplit'}

        menu_edit_video = {"AXRole": "AXMenuItem", "AXTitle": "Edit Video"}
        menu_edit_image = {"AXRole": "AXMenuItem", "AXTitle": "Edit Image"}
        menu_edit_audio = {"AXRole": "AXMenuItem", "AXTitle": "Edit Audio"}
        menu_edit_clip_keyframe = {"AXRole": "AXMenuItem", "AXTitle": "Edit Clip Keyframe"}
        menu_set_clip_attrubutes = {"AXRole": "AXMenuItem", "AXTitle": "Set Clip Attributes"}
        menu_edit_clip_alias = {"AXRole": "AXMenuItem", "AXTitle": "Edit Clip Alias"}


        # For (Edit Image) sub-menu
        btn_edit_img = {'AXTitle': 'Edit Image', 'AXRole': 'AXMenuItem'}
        btn_crop_image = {'AXIdentifier': 'onCropImage'}
        btn_pan_zoom = {'AXIdentifier': 'onPanZoom'}
        btn_image_fix_enhance = [btn_edit_img, {'AXIdentifier': 'openFixEnhance'}]
        btn_image_fade_in_out = [btn_edit_img, {'AXIdentifier': 'enableFadeInOut'}]

        class image_stretch_mode:
            aspect_ratio = {'AXIdentifier': '_NS:9'}
            option_0 = {"AXValue": "Stretch clip to 16:9 aspect ratio"}
            option_1 = {"AXValue": "Use CLPV to stretch clip to 16:9 aspect ratio"}
            ok = {'AXIdentifier': '_NS:66'}

        class clip_aspect_ratio:
            detect_and_suggest = {'AXIdentifier': '_NS:84'}
            detect_aspect_ratio = {'AXIdentifier': '_NS:198'}
            ok = {'AXIdentifier': '_NS:149'}

        class set_alias:
            alias = {'AXIdentifier': '_NS:48'}
            ok = {'AXIdentifier': '_NS:64'}
            cancel = {'AXIdentifier': '_NS:54'}

        class properties:
            close = {'AXIdentifier': '_NS:9'}
            main = {"AXTitle":"Properties", "recursive":False}

    # for image
    btn_Crop_the_selected_image = {'AXIdentifier': 'IDC_TIPSAREA_BTN_CROP'}
    btn_Set_the_length_of_the_selected_clip = {'AXIdentifier': 'IDC_TIPSAREA_BTN_DURATION'}
    btn_trim = {'AXIdentifier': 'IDC_TIPSAREA_BTN_TRIM'}
    btn_transition_modify = {'AXIdentifier': 'IDC_TIPSAREA_BTN_TRANSITION'}
    btn_transition_close = {'AXIdentifier': 'IDC_TRANSITIONSETTING_BTN_CLOSE'}
    btn_effect_modify = {'AXIdentifier': 'IDC_TIPSAREA_BTN_EFFECT'}
    btn_effect_close = {'AXIdentifier': 'IDC_EFFECTSETTING_BTN_CLOSE'}
    btn_designer_close = {'AXIdentifier': 'IDC_TITLE_DESIGNER_BTN_CANCEL'}
    btn_designer = {'AXIdentifier': 'IDC_TIPSAREA_BTN_TITLE_DESIGNER'}
    btn_change_color = {'AXIdentifier': 'IDC_TIPSAREA_BTN_CHANGE_COLOR'}
    change_color_hex = {'AXIdentifier': 'hex'}
    btn_video_collage = {'AXIdentifier': 'IDC_TIPSAREA_BTN_TITLE_DESIGNER'}
    btn_duration_ok = {'AXIdentifier': 'IDC_DURATION_BTN_OK'}

class window():
    main = {'AXIdentifier': '_NS:10', 'AXRole': 'AXWindow'}

    crop_image = [main,{'AXValue': 'Crop Image'}]
    duration_settings = [main,{'AXValue': 'Duration Settings'}]
    blending_mode = [main,{'AXValue': 'Blending Mode'}]
    crop_zoom_pan = [main,{'AXValue': 'Crop/Zoom/Pan'}]

    audio_speed = [main,{'AXValue': 'Audio Speed'}]


class warning_dialog():
    main = {'AXIdentifier': '_NS:10'}
    msg1 = [main, {"AXIdentifier": "_NS:34", "AXValue": 'In the Crop/Zoom/Pan window, all applied effects are ignored.11'}]
    msg2 = [main, {"AXIdentifier": "_NS:34", "AXRole" : "AXStaticText"}]
    msg3 = [main, {"AXIdentifier": "_NS:34", "AXValue" : 'The selected clip contains alpha transparency, which is not supported by this function.'}]
    ok = [main, {"AXRole": "AXButton", "AXTitle": "OK"}]