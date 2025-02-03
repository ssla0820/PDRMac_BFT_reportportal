class room_entry():
    btn_intro_video_room = {'AXIdentifier': 'IDC_LIBRARY_BTN_VIDEO_INTRO_ROOM'}

dialog_quick_tutorial = {'AXRoleDescription': 'dialog', 'AXTitle': 'Video Intro Designer Tutorial', 'AXRole': 'AXWindow'}

class explore_view_region():
    triangle_theme = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRole': 'AXDisclosureTriangle', 'index': 0}
    triangle_style = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRole': 'AXDisclosureTriangle', 'index': 1}
    category_theme = {'AXIdentifier': 'RoomTagOutlineViewTextField', 'AXRole': 'AXStaticText', 'AXValue': 'Theme'}
    category_style = {'AXIdentifier': 'RoomTagOutlineViewTextField', 'AXRole': 'AXStaticText', 'AXValue': 'Style'}
    category_scroll_view = {'AXIdentifier': 'IDC_LIBRARY_ROOM_TAG_OUTLINEVIEW'}
    category_items = [category_scroll_view, {"AXRole": "AXStaticText", "get_all": True}]

    category_downloaded = {'AXIdentifier': 'RoomTagOutlineViewTextField', 'AXRole': 'AXStaticText', 'AXValue': 'Downloaded'}
    category_save_templates = {'AXIdentifier': 'RoomTagOutlineViewTextField', 'AXRole': 'AXStaticText', 'AXValue': 'Saved Templates'}
    category_my_profile = {'AXTitle': 'My Profile', 'AXRole': 'AXCheckBox'}
    category_my_favorites = {'AXIdentifier': 'RoomTagTextField', 'AXRole': 'AXStaticText'}

# For template scroll bar
#scroll_bar = {'AXRole': 'AXValueIndicator', 'AXRoleDescription': 'value indicator'}
scroll_bar = {'AXIdentifier': 'IDC_LIBRARY_SCROLLBAR_COLLECTIONVIEW_Y', 'AXRoleDescription': 'scroll bar'}

# For Video Intro category scroll bar
category_scroll_bar = [{'AXIdentifier': 'IDC_LIBRARY_ROOM_TAG_SCROLLVIEW'}, {'AXRole': 'AXScrollBar'}]

# Check all template count
library_template = {'AXIdentifier': 'LibraryCollectionViewItem', 'AXRole': 'AXGroup', "get_all": True}
library_collection_view = {'AXRoleDescription': 'section', 'AXRole': 'AXList', 'AXSubrole': 'AXSectionList'}
library_visible_area = {'AXIdentifier': 'IDD_LIBRARY'}

# Back to Intro Room (Library) after input search keyword
btn_library = {'AXTitle': 'Library', 'AXRole': 'AXButton'}

class my_profile():
    main_window = {'AXTitle': 'My Profile & Creations', 'AXRole': 'AXWindow'}
    btn_delete = {'AXTitle': 'Delete', 'AXRole': 'AXButton'}
    delete_warning_msg = {'AXValue': 'Are you sure you want delete this post?', 'AXRole': 'AXStaticText'}
    txt_view = [main_window, {'AXValue': 'Views', 'AXRole': 'AXStaticText'}]
    btn_dz = {'AXDescription': 'Click to view user\'s profile on DirectorZone', 'AXRole': 'AXLink'}

class share_template():
    main_window = {'AXTitle': 'Share Template', 'AXRole': 'AXWindow'}
    btn_copyright_confirm = [main_window, {'AXIdentifier': 'IDC_UPLOADTEMPLATE_EULA_NEXT'}]
    btn_share = [main_window, {'AXTitle': 'Share', 'AXRole': 'AXButton'}]
    btn_done = [main_window, {'AXTitle': 'Done', 'AXRole': 'AXButton'}]
    btn_add_to_timeline = [main_window, {'AXTitle': 'Add to Timeline', 'AXRole': 'AXButton'}]
    edit_box_description = [main_window, {'AXRoleDescription': 'text entry area', 'AXRole': 'AXTextArea'}]


class view_template_dialog():
    main_window = {'AXTitle': 'View Template', 'AXRole': 'AXWindow'}
    btn_edit_in_Intro_Desinger = [main_window, {'AXTitle': 'Customize the template', 'AXRole': 'AXButton'}]

class too_many_object_decteced_dialog():
    main_window = {'AXTitle': 'CyberLink PowerDirector'}
    description = [main_window, {'AXIdentifier': 'IDC_CLALERT_MESSAGE', 'AXValue': 'Too many objects were added. Remove some objects and then try again.'}] # hardcode_0427: IDC_CLALERT_MESSAGE, v2529: _NS:34
    btn_ok = [main_window, {'AXTitle': 'OK'}]

class intro_video_designer():
    # First version: Only Intro Designer
    #main_window = {'AXTitle': 'Video Intro Designer', 'AXRole': 'AXWindow'}

    # v21.1.4802: Intro / Outro Designer
    main_window = {'AXIdentifier': '_NS:8', 'AXRole': 'AXWindow'} #

    timecode = [{'AXIdentifier': 'IDC_INTRO_DESIGNER_SPINTIMEEDIT_TIMECODE'}, {'AXIdentifier': 'spinTimeEditTextField', 'AXRoleDescription': 'text'}]
    # down
    btn_add_to_timeline = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_ADV_EDITING'}
    btn_save_as = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_SAVE_AS'}
    btn_close = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_CANCEL'}
    btn_share_template = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_SHARE'}

    # upper
    btn_undo = {'AXIdentifier': 'IDC_INTRO_DESGINER_BTN_UNDO'}
    btn_redo = {'AXIdentifier': 'IDC_INTRO_DESGINER_BTN_REDO'}
    btn_zoom = {'AXRoleDescription': 'zoom button', 'AXRole': 'AXButton'}
    btn_x = {'AXRoleDescription': 'close button', 'AXRole': 'AXButton'}
    btn_DZ = {'AXIdentifier': 'IDC_INTRO_DESGINER_BTN_DZ', 'AXRole': 'AXButton'}

    # preview
    preview_area = {'AXIdentifier': 'IDC_INTRO_DESIGNER_PREVIEW_MTKVIEW', 'AXRole': 'Preview'}

    # designer function check
    btn_duration = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_TEMPLATE_DURATION_SETTING'}
    btn_change_media = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_CHANGE_MEDIA'}
    btn_trim = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_TRIM'}
    btn_crop = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_CROP'}
    btn_flip = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_FLIP'}
    btn_LUT = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_ADD_EFFECT'}
    btn_add_title = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_ADD_TITLE'}
    btn_add_image = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_ADD_Image'}
    btn_add_pip = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_ADD_PIP'}
    btn_replace_BGM = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_BGM'}
    btn_volume_settings = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_SETTINGS'}
    btn_cancel_selection = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_UNSELECT'}

    # layer order
    btn_layer_order = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_LAYER_ORDER'}
    btn_change_color = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_CHANGE_COLOR'}

    class save_template_window:
        main_window = {'AXIdentifier': 'IDC_SAVE_TEMPLATE_WINDOW', 'AXTitle': 'Save as Template'}
        txt_field = [main_window, {'AXIdentifier': 'IDC_SAVE_TEMPLATE_EDIT_TEMPLATE_NAME'}]
        btn_OK = [main_window, {'AXIdentifier': 'IDC_SAVE_TEMPLATE_BTN_OK'}]

    class operation:
        btn_play = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_PLAY', 'AXRole': 'AXButton'}
        btn_pause = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_PAUSE', 'AXRole': 'AXButton'}
        btn_stop = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_STOP', 'AXRole': 'AXButton'}

    class duration:
        main_window = {'AXTitle': 'Template Duration Setting', 'AXRole': 'AXWindow'}
        txt_org_duration = [main_window, {'AXIdentifier': 'IDS_INTRO_TEMPLATE_DURAITON_DLG_ORIGINAL_DURATION', 'AXRole': 'AXStaticText'}]
        new_duration = {'AXIdentifier': 'IDC_TEMPLATE_DURATION_SETTING_SPINEDIT_NEW_DURATION', 'AXRole': 'AXGroup'}
        editbox_new_duration = [new_duration, {'AXIdentifier': 'spinEditTextField', 'AXRole': 'AXTextField'}]
        btn_ok = {'AXIdentifier': 'IDC_INTRO_TEMPLATE_DURATION_SETTING_BTN_OK', 'AXRole': 'AXButton'}

    class media_library:
        main_window = {'AXTitle': 'Media Library', 'AXRole': 'AXWindow'}
        btn_OK = {'AXIdentifier': 'IDC_TITLE_IMPORT_PARTICLE_BTN_OK'}

    class video_overlay_room:
        main_window = {'AXTitle': 'Video Overlay Room', 'AXRole': 'AXWindow'}
        combobox_category = {'AXIdentifier': 'IDC_TITLE_IMPORT_PARTICLE_COMBOBOX_CATEGORY'}
        btn_OK = {'AXIdentifier': 'IDC_TITLE_IMPORT_PARTICLE_BTN_OK'}

    class image:
        btn_obj_setting = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_OBJECT_SETTING'}
        btn_animation = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_ANIMATION'}
        btn_change_media = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_CHANGE_PIP'}
        btn_remove = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_DELETE'}

        class object_settings:
            main_window = {'AXTitle': 'Object Settings', 'AXRole': 'AXWindow'}
            btn_tri_border = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRole': 'AXDisclosureTriangle', 'index': 1}
            cbx_border = {'AXIdentifier': 'IDC_PIP_DESIGNER_CHECKBOX_APPLY_PROPERTY'}
            border_size = {'AXIdentifier': 'IDC_PIP_DESIGNER_SPINEDIT_BORDER_SIZE', 'AXRole': 'AXGroup'}
            editbox_border_size = [border_size, {'AXIdentifier': 'spinEditTextField', 'AXRole': 'AXTextField'}]
            btn_close = [main_window, {'AXRoleDescription': 'close button', 'AXRole': 'AXButton'}]

        class animation:
            main_window = {'AXTitle': 'Animation', 'AXRole': 'AXWindow'}
            btn_tri_in_animation = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRole': 'AXDisclosureTriangle',
                              'index': 0}
            btn_tri_out_animation = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRole': 'AXDisclosureTriangle',
                              'index': 1}
            btn_close = [main_window, {'AXRoleDescription': 'close button', 'AXRole': 'AXButton'}]

    class motion_graphics:
        class title_room:
            main_window = {'AXTitle': 'Title Room', 'AXRole': 'AXWindow'}
            btn_close = [main_window, {'AXRoleDescription': 'close button', 'AXRole': 'AXButton'}]
            btn_import = {'AXIdentifier': 'IDC_TITLE_IMPORT_PARTICLE_BTN_OK'}
            cbx_category = {'AXIdentifier': 'IDC_TITLE_IMPORT_PARTICLE_COMBOBOX_CATEGORY'}
            option_all_content = {'AXRole': 'AXStaticText', 'AXValue': 'All Content'}
            option_motion_graphics = {'AXRole': 'AXStaticText', 'AXValue': 'Motion Graphics'}
            option_popular = {'AXRole': 'AXStaticText', 'AXValue': 'Popular'}
            option_lower_third = {'AXRole': 'AXStaticText', 'AXValue': 'Lower Third'}
            option_speech_bubble = {'AXRole': 'AXStaticText', 'AXValue': 'Speech Bubble Titles'}
            fit_with_category_group = [option_all_content, option_motion_graphics, option_popular,
                                    option_lower_third, option_speech_bubble]

        btn_settings = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_MGTITLE'}
        btn_remove = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_DELETE'}

        class mgt_settings:
            main_window = {'AXTitle': 'Motion Graphics Settings', 'AXRole': 'AXWindow'}
            txt_title = {'AXIdentifier': 'IDC_ELEGANT_TITLE_DESIGNER_EDIT_TITLE'}
            title_font_color = {'AXIdentifier': 'IDC_ELEGANT_TITLE_DESIGNER_BTN_FONT_COLOR'}
            btn_close = [main_window, {'AXRoleDescription': 'close button', 'AXRole': 'AXButton'}]
            cbx_title_txt_category = {'AXIdentifier': 'IDC_ELEGANT_TITLE_DESIGNER_COMBOBOX_SELECTED_OBJECT'}

    class crop_window:
        main_window = {'AXTitle': 'Crop / Rotate', 'AXRole': 'AXWindow'}
        obj_edit_canvas = [main_window, {'AXIdentifier': 'dashBorderedView'}]
        btn_OK = [main_window, {'AXIdentifier': 'IDC_MAGICMOTION_DESIGNER_OK_BUTTON'}]
        btn_cancel = [main_window, {'AXIdentifier': 'IDC_MAGICMOTION_DESIGNER_CANCEL_BUTTON'}]
        btn_x = [main_window, {'AXRoleDescription': 'close button', 'AXRole': 'AXButton'}]

    class color_filter_window:
        main_window = {'AXIdentifier': '_NS:8', 'AXTitle': 'Color Filter', 'AXRole': 'AXWindow'}
        btn_x = [main_window, {'AXRoleDescription': 'close button', 'AXRole': 'AXButton'}]
        combobox_category = [main_window, {'AXIdentifier': 'IDC_INTRO_COLORLUT_PAGE_COMBOBOX_FILTER'}]
        class strength:
            value = {'AXIdentifier': 'IDC_INTRO_COLORLUT_PAGE_SPINEDIT_STRENGTH', 'AXRole': 'AXGroup'}
            editbox_value = [value, {'AXIdentifier': 'spinEditTextField', 'AXRole': 'AXTextField'}]
            slider = {'AXIdentifier': 'IDC_INTRO_COLORLUT_PAGE_SLIDER_STRENGTH'}

    class general_title:
        btn_backdrop = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_BACKDROP'}
        btn_animation = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_ANIMATION'}
        btn_remove = {'AXIdentifier': 'IDC_INTRO_DESIGNER_BTN_DELETE'}

        class backdrop_settings:
            main_window = {'AXTitle': 'Backdrop Settings', 'AXRole': 'AXWindow'}
            cbx_enable_backdrop = {'AXIdentifier': 'IDC_INTRO_BACKDROP_ENABLE'}
            radio_solid_background_bar = {'AXIdentifier': 'IDC_INTRO_BACKDROP_SOLID_BACKGROUND',
                                          'AXTitle': 'Solid background bar'}
            radio_fit_with_title = {'AXIdentifier': 'IDC_INTRO_BACKDROP_FIT_WITH_TITLE', 'AXTitle': 'Fit with title'}
            radio_group = [radio_solid_background_bar, radio_fit_with_title]

            cbx_fit_with_title = {'AXIdentifier': 'IDC_INTRO_BACKDROP_SHAPE_TYPE', 'AXRole': 'AXButton'}
            option_ellipse = {'AXRole': 'AXStaticText', 'AXValue': 'Ellipse'}
            option_rectangle = {'AXRole': 'AXStaticText', 'AXValue': 'Rectangle'}
            option_curve_edged_rectangle = {'AXRole': 'AXStaticText', 'AXValue': 'Curve-edged Rectangle'}
            option_rounded_rectangle = {'AXRole': 'AXStaticText', 'AXValue': 'Rounded Rectangle'}
            fit_with_title_group = [option_ellipse, option_rectangle, option_curve_edged_rectangle,
                                    option_rounded_rectangle]

            btn_uniform_color = {'AXIdentifier': 'IDC_INTRO_BACKDROP_ONE_COLORPICKER'}
            btn_close = [main_window, {'AXRoleDescription': 'close button', 'AXRole': 'AXButton'}]

        class animation_setting:
            main_window = {'AXTitle': 'Animation', 'AXRole': 'AXWindow'}

            cbx_in_animation_with_title = {'AXIdentifier': 'IDC_INTRO_DESIGNER_COMBOBOX_INANIMATION', 'AXRole': 'AXButton'}
            option_all_effects = {'AXRole': 'AXStaticText', 'AXValue': 'All Effects'}
            option_fly = {'AXRole': 'AXStaticText', 'AXValue': 'Fly'}
            option_no_effect = {'AXRole': 'AXStaticText', 'AXValue': 'No Effect'}
            option_popup = {'AXRole': 'AXStaticText', 'AXValue': 'Popup'}
            option_roll_and_crawl = {'AXRole': 'AXStaticText', 'AXValue': 'Roll and Crawl'}
            option_slide = {'AXRole': 'AXStaticText', 'AXValue': 'Slide'}
            option_special = {'AXRole': 'AXStaticText', 'AXValue': 'Special'}
            option_video_and_rotation = {'AXRole': 'AXStaticText', 'AXValue': 'Video Rotation'}
            option_wipe = {'AXRole': 'AXStaticText', 'AXValue': 'Wipe'}
            fit_with_animation_group = [option_all_effects, option_fly, option_no_effect,option_popup,
                                    option_roll_and_crawl, option_slide, option_special, option_video_and_rotation,
                                    option_wipe]

            cbx_out_animation_with_title = {'AXIdentifier': 'IDC_INTRO_DESIGNER_COMBOBOX_OUTANIMATION', 'AXRole': 'AXButton'}
            btn_in_animation = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRole': 'AXDisclosureTriangle'}
            btn_out_animation = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRole': 'AXDisclosureTriangle', 'index': 1}
            btn_close = [main_window, {'AXRoleDescription': 'close button', 'AXRole': 'AXButton'}]

    class bgm_setting:
        main_window = {'AXIdentifier': 'IDC_DOWNLOADBGMDLG_WINDOW', 'AXRole': 'AXWindow'}
        btn_download_BGM = {'AXIdentifier': 'IDC_DOWNLOADBGMDLG_DOWNLOAD_BTN', 'AXRole': 'AXButton'}
        btn_ok = {'AXIdentifier': 'IDC_DOWNLOADBGMDLG_OK_BTN', 'AXRole': 'AXButton'}
        txt_bgm_timecode = {'AXIdentifier': 'IDC_DOWNLOADBGMDLG_FRAME_LABEL', 'AXRole': 'AXStaticText'}

    class volume_setting_dialog:
        main_window = {'AXTitle': 'Volume', 'AXIdentifier': 'IDC_INTRO_VOLUMESETTING_DLG'}
        cbx_always_mute_video_s_audio = {'AXIdentifier': 'IDC_EXPRESS_VIDEO_CHECKBOX_MUTE_VIDEO', 'AXRole': 'AXCheckBox'}
        btn_ok = [main_window, {'AXIdentifier': 'IDC_EXPRESS_VIDEO_BUTTON_OK', 'AXRole': 'AXButton'}]