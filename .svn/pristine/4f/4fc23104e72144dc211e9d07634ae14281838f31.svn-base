class keyframe():
    tab = {'AXIdentifier': 'IDC_KEYFRAMEROOM_LABEL', 'AXValue': 'Keyframe Settings'}  # v2922, _NS179 in v3303
    close = {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_LEAVE'}

class fix_enhance():
    tab = {'AXIdentifier': 'IDC_FIX_ENHANCE_TITLE', 'AXValue': 'Fix / Enhance'}
    close = {'AXIdentifier': 'IDC_FIX_ENHANCE_BTN_LEAVE'}

class audio_editor():
    main = {'AXIdentifier': '_NS:12', 'AXRole': 'AXWindow'}  # v2922, _NS12 in v3303
    tab = [main, {"AXRole": "AXButton", "AXTitle": "Effects"}]
    close = {"AXRoleDescription": "close button"}

class pan_zoom():
    tab = {"AXRole": "AXStaticText", "AXValue": 'Pan / Zoom'}
    close = {'AXIdentifier': 'IDC_MAGIC_MOTION_PAGE_CLOSE_BUTTON', 'AXRole': 'AXButton'}

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
    btn_color_match = {'AXIdentifier': 'IDC_TIPSAREA_BTN_COLOR_MATCH'}
    btn_sync_by_audio = {'AXIdentifier': 'IDC_TIPSAREA_BTN_SYNC_BY_AUDIO'}

    class tools():
        btn_VideoInReverse = {"AXRole": "AXMenuItem", "AXTitle": "Video in Reverse"}
        btn_AudioInReverse = {"AXRole": "AXMenuItem", "AXTitle": "Audio in Reverse"}
        bb_auto_cutout = {'AXValue': 'Find the feature in PiP Designer > Cutout to remove the video background.', 'AXRole': "AXStaticText"}
        bb_video_speed = {'AXValue': 'Find the feature in Tools > Video Speed to adjust the speed of your video clip.',
                          'AXRole': "AXStaticText"}

    class more_features():
        main = {'AXIdentifier': 'IDC_TIPSAREA_BTN_MORE_FEATURE'}
        menu = [main,{"AXRole":"AXMenu","recursive":"False"}]
        btn_Remove = {'AXIdentifier': 'IDM_TIMELINE_REMOVE_OBJECT'}
        btn_SelectAll = {'AXIdentifier': 'IDM_TIMELINE_SELECT_ALL'}
        btn_link_unlink = {'AXIdentifier': 'IDM_TIMELINE_LINK_UNLINK_OBJECTS'}
        btn_group_ungroup = {'AXIdentifier': 'IDM_TIMELINE_GROUP_UNGROUP_OBJECTS'}
        btn_split = {'AXIdentifier': 'IDM_TIMELINE_SPLIT'}
        btn_shape_designer = {'AXIdentifier': 'IDM_TIMELINE_EDIT_SHAPE'}

        menu_edit_video = {"AXRole": "AXMenuItem", "AXTitle": "Edit Video"}
        menu_edit_image = {"AXRole": "AXMenuItem", "AXTitle": "Edit Image"}
        menu_edit_audio = {"AXRole": "AXMenuItem", "AXTitle": "Edit Audio"}
        menu_edit_clip_keyframe = {"AXRole": "AXMenuItem", "AXTitle": "Edit Clip Keyframe"}
        menu_set_clip_attrubutes = {"AXRole": "AXMenuItem", "AXTitle": "Set Clip Attributes"}
        menu_edit_clip_alias = {"AXRole": "AXMenuItem", "AXTitle": "Edit Clip Alias"}


        # For (Edit Image) sub-menu
        btn_edit_img = {'AXTitle': 'Edit Image', 'AXRole': 'AXMenuItem'}
        btn_crop_image = {'AXIdentifier': 'IDM_TIMELINE_CROPPICTURE'}
        btn_pan_zoom = {'AXIdentifier': 'IDM_TAT_PAN_AND_ZOOM'}
        btn_image_fix_enhance = [btn_edit_img, {'AXIdentifier': 'IDM_TIMELINE_EDIT_FIX_ENHANCE'}]
        btn_image_fade_in_out = [btn_edit_img, {'AXIdentifier': 'IDM_TIMELINE_FADE_IN_FADE_OUT'}]

        class image_stretch_mode:
            main_window = {'AXTitle': 'Image Stretch Mode Settings'}
            aspect_ratio = {'AXIdentifier': 'IDC_IMAGE_STRETCH_MODE_DIALOG_BTN_ASPECT_RATIO'}
            option_0 = {"AXValue": "Stretch clip to 16:9 aspect ratio"}
            option_1 = {"AXValue": "Use CLPV to stretch clip to 16:9 aspect ratio"}
            ok = {'AXIdentifier': 'IDC_IMAGE_STRETCH_MODE_DIALOG_BTN_OK'}

        class clip_aspect_ratio:
            detect_and_suggest = {'AXIdentifier': 'IDC_CLIP_ASPECT_RATIO_DIALOG_BTN_DETECT_AND_SUGGEST'}
            detect_aspect_ratio = {'AXIdentifier': 'IDC_CLIP_ASPECT_RATIO_DIALOG_LABEL_PROJECT_ASPECT_RATIO'}
            ok = {'AXIdentifier': '_NS:149'}    # v2922, _NS42 in v3303

        class set_alias:
            alias = {'AXIdentifier': 'IDC_EDIT_TIMELINE_ALIAS_NEW'}
            ok = {'AXIdentifier': 'IDC_SC_BUTTON_OK'}
            cancel = {'AXIdentifier': 'IDC_SC_BUTTON_CANCEL'}

        class properties:
            close = {'AXIdentifier': 'IDC_PROPERTIES_DIALOG_BTN_CLOSE'}
            main = {"AXTitle":"Properties", "recursive":False}

    # for image
    btn_Crop_the_selected_image = {'AXIdentifier': 'IDC_TIPSAREA_BTN_CROP'}
    btn_Set_the_length_of_the_selected_clip = {'AXIdentifier': 'IDC_TIPSAREA_BTN_DURATION'}
    bb_crop = {'AXValue': 'Crop out the edges of your frame, customize the aspect ratio, and adjust orientation.', 'AXRole': "AXStaticText"}

    # for video
    btn_trim = {'AXIdentifier': 'IDC_TIPSAREA_BTN_TRIM'}
    bb_trim = {'AXValue': 'Quickly edit length of video and audio clips', 'AXRole': "AXStaticText"}

    # for transition
    btn_transition_modify = {'AXIdentifier': 'IDC_TIPSAREA_BTN_TRANSITION'}
    btn_transition_close = {'AXIdentifier': 'IDC_TRANSITIONSETTING_BTN_CLOSE'}

    # for effect
    btn_effect_modify = {'AXIdentifier': 'IDC_TIPSAREA_BTN_EFFECT'}
    btn_effect_close = {'AXIdentifier': 'IDC_EFFECTSETTING_BTN_CLOSE'}

    btn_designer_close = {'AXIdentifier': 'IDC_TITLE_DESIGNER_BTN_CANCEL'}
    btn_designer = {'AXIdentifier': 'IDC_TIPSAREA_BTN_TITLE_DESIGNER'}
    btn_change_color = {'AXIdentifier': 'IDC_TIPSAREA_BTN_CHANGE_COLOR'}
    change_color_hex = {'AXIdentifier': 'hex'}
    btn_video_collage = {'AXIdentifier': 'IDC_TIPSAREA_BTN_TITLE_DESIGNER'}
    btn_duration_ok = {'AXIdentifier': 'IDC_DURATION_BTN_OK'}

class window():
    crop_image = {'AXIdentifier': 'IDC_MAGIC_MOTION_DESIGNER_WINDOW', 'AXTitle': 'Crop / Rotate'}
    duration_settings = {'AXIdentifier': 'IDC_DURATION_SETTING_WINDOW', 'AXTitle': 'Duration Settings'}
    duration_timecode = [duration_settings, {'AXIdentifier': 'spinTimeEditTextField'}]
    blending_mode = {'AXIdentifier': 'IDC_BLENDING_MODE_DIALOG_WINDOW', 'AXTitle': 'Blending Mode'}
    crop_zoom_pan = {'AXIdentifier': 'IDC_MAGIC_MOTION_DESIGNER_WINDOW', 'AXTitle': 'Crop/Zoom/Pan'}
    audio_speed = {'AXIdentifier': 'IDC_AUDIO_SPEED_DIALOG_WINDOW', 'AXTitle': 'Audio Speed'}


class warning_dialog():
    main = {'AXIdentifier': 'IDD_CLALERT'}
    msg1 = [main, {"AXIdentifier": "IDC_CLALERT_MESSAGE", "AXValue": 'In the Crop/Zoom/Pan window, all applied effects are ignored.'}]

    # message2: The current keyframe settings will be replaced with the pasted attributes. Do you want to continue?
    msg2 = [main, {"AXIdentifier": "IDC_CLALERT_MESSAGE", "AXRole": "AXStaticText"}]

    msg3 = [main, {"AXIdentifier": "IDC_CLALERT_MESSAGE", "AXValue" : 'The selected clip contains alpha transparency, which is not supported by this function.'}]
    ok = [main, {"AXRole": "AXButton", "AXTitle": "OK"}]
