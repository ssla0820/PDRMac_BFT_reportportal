from .mask_designer import mask_designer_window
class Area:
    full = None
    timeline = {'AXIdentifier': 'IDC_TIMELINE_SPLITVIEW', "AXRole": "AXSplitGroup"}
    library = {'AXIdentifier': 'IDC_LIBRARY_COLLECTIONVIEW'}
    library_icon_view = {'AXIdentifier': 'IDC_LIBRARY_COLLECTIONVIEW'}
    library_detail_view = {'AXIdentifier': 'IDC_LIBRARY_SCROLLVIEW_DETAILEDTABLEVIEW'}

    class preview:
        main = {'AXIdentifier': 'IDD_DISPLAYPANEL'}
        only_mtk_view = {'AXIdentifier': 'IDC_DISPLAY_PANEL_MTKVIEW'}
        pip_designer = [{'AXIdentifier': '_NS:138'}, {'AXIdentifier': 'dashBorderedView'}] # 3303: _NS:138
        mask_designer = [mask_designer_window, {'AXIdentifier': 'dashBorderedView'}]
        video_speed = []

    class download_from_cl_dz:
        class content:
            library = {'AXIdentifier': 'IDC_TB_COLLECTIONVIEW'}
            detail_view = {'AXIdentifier': 'IDC_DOWNLOAD_TEMPLATE_DIALOG_DETAILS_SCROLLVIEW'}
        class media:
            library = {'AXIdentifier': 'IDC_MVPB_BTN_COLLECTIONVIEW'}

main_window = {"AXRole":"AXWindow","recursive": False}
main_caption = {'AXIdentifier': 'IDC_MAIN_CAPTION'}
full_screen = [{"AXRole":"AXWindow","recursive": False},{"AXSubrole":"AXFullScreenButton","recursive": False}]
minimize = [{"AXRole":"AXWindow","recursive": False},{"AXSubrole":"AXMinimizeButton","recursive": False}]

tag_list = [{'AXIdentifier': 'IDD_LIBRARY'}, {"AXIdentifier": "RoomTagTextField", "get_all": True}]
tag_list_2 = [{'AXIdentifier': 'IDD_LIBRARY'}, {"AXIdentifier": "RoomTagOutlineViewTextField", "get_all": True}]
# >>----- For Scan IAD category
tag_outline_area = {'AXIdentifier': 'IDC_LIBRARY_ROOM_TAG_OUTLINEVIEW'}
uni_outline_row = [tag_outline_area, {'AXRole': 'AXRow', "AXSubrole": "AXOutlineRow"}]
disclosure_triangle = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRole': 'AXDisclosureTriangle', "get_all": True}
# <<-----

category = {'AXIdentifier': 'IDC_LIBRARY_COMBOBOX_FILTER'}
category_items = [category, {"AXRole": "AXStaticText", "get_all": True}]

timecode = [{"AXSubrole":"AXDialog","get_all":True},
            {"AXRole":"AXGroup"},
            {"AXIdentifier":"spinTimeEditTextField"}]
button_ok = {"AXRole":"AXButton", "AXTitle":"OK"}

#for v20.1.3425 /v20.1.3428
ceip_dialog = {"AXIdentifier": "IDC_CEIP_DIALOG", "AXTitle": "CyberLink Product Improvement Program"}
button_close_on_ceip = [ceip_dialog,{"AXRole": "AXButton", "AXTitle":"Close"}]
radio_button_no_on_ceip = [ceip_dialog,{"AXRole": "AXCheckBox", "AXTitle": "No, thank you"}]

class quit_dialog:
    main = {"AXTitle": "CyberLink PowerDirector", "AXIdentifier": "IDD_CLALERT"}
    yes = [main, {"AXRole": "AXButton", "index": 0}]
    no = [main, {"AXRole": "AXButton", "index": 1}]
    cancel = [main, {"AXRole": "AXButton", "index": 2}]


class finder_window:
    main = {'AXIdentifier': 'FinderWindow'}
    btn_close = [main, {'AXRoleDescription': 'close button'}]

class gdpr_dialog:
    main = {'AXIdentifier': 'GDPR_DLG'}
    btn_accept_continue = [main, {'AXTitle': 'Accept and Continue', "AXRole": "AXButton"}]

class launcher_window:
    main = {'AXIdentifier': 'IDC_LAUNCHER_MAIN_WINDOW'}
    btn_new_project = [main, {'AXIdentifier': 'IDC_LAUNCHER_NEW_PROJECT'}]
    image_WOW = [main, {'AXRoleDescription': 'HTML content', 'AXRole': 'AXWebArea'}]
    btn_try_on_first = [image_WOW, {'AXTitle': 'Try Now', 'AXRole': 'AXLink', 'index': 0}]
    btn_try_on_second = [image_WOW, {'AXTitle': 'Try Now', 'AXRole': 'AXLink', 'index': 1}]
    chx_show_launcher = [main, {'AXTitle': 'Show launcher after closing program', 'AXRole': 'AXCheckBox'}]

    # Showcase Banner
    banner_7_dots_list = [main, {'AXRoleDescription': 'scroll area', 'AXRole': 'AXScrollArea', 'index': 0}]
    show_case_title = [main, {'AXIdentifier': 'IDC_STATIC_LAUNCHER_SHOWCASE_TITLE', 'AXRole': 'AXStaticText'}]
    show_case_description = [main, {'AXIdentifier': 'IDC_STATIC_LAUNCHER_SHOWCASE_DESCRIPTION', 'AXRole': 'AXStaticText'}]
    show_case_video_area = [main, {'AXIdentifier': 'IDC_BUTTON_LAUNCHER_BANNER', 'AXRole': 'AXButton'}]

    # If click banner, pop up import dialog
    import_dialog = {'AXIdentifier': 'IDC_LAUNCHER_IMPORT_DLG_WIN', 'AXRole': 'AXWindow'}
    txt_try_sample_clip = [import_dialog, {'AXValue': 'Try with sample clip', 'AXRole': 'AXStaticText'}]

    # Recent Project
    img_recently_icon = [main, {'AXDescription': 'img projects gradient', 'AXRole': 'AXImage', 'index': 0}]
    launcher_scroll_area_list = [main, {'AXRoleDescription': 'scroll area', 'AXRole': 'AXScrollArea', "get_all": True}]
    txt_no_recent_project = [main, {'AXValue': 'No Recent Projects', 'AXRole': 'AXStaticText'}]


    btn_open_project = [main, {'AXTitle': 'Open Project', 'AXRole': 'AXButton'}]

    btn_aspect_ratio_16_9 = [main, {'AXTitle': '16:9', 'AXRole': 'AXButton'}]
    aspect_ratio_menu = {'AXIdentifier':"IDC_STATUS_POPUP_BUTTON_MENU"}
    aspect_ratio_list = [aspect_ratio_menu, {'AXRole': "AXStaticText", "get_all": True}]

    # Tool area
    btn_ai_body_effect = [main, {'AXIdentifier': 'LauncherToolCollectionViewItem', 'AXRole': 'AXGroup', 'index': 0}]
    btn_video_stabilizer = [main, {'AXIdentifier': 'LauncherToolCollectionViewItem', 'AXRole': 'AXGroup', 'index': 1}]
    btn_video_denoise = [main, {'AXIdentifier': 'LauncherToolCollectionViewItem', 'AXRole': 'AXGroup', 'index': 2}]
    btn_greener_grass = [main, {'AXIdentifier': 'LauncherToolCollectionViewItem', 'AXRole': 'AXGroup', 'index': 3}]
    btn_ai_bg_remover = [main, {'AXIdentifier': 'LauncherToolCollectionViewItem', 'AXRole': 'AXGroup', 'index': 4}]
    btn_audio_denoise = [main, {'AXIdentifier': 'LauncherToolCollectionViewItem', 'AXRole': 'AXGroup', 'index': 5}]
    btn_wind_removal = [main, {'AXIdentifier': 'LauncherToolCollectionViewItem', 'AXRole': 'AXGroup', 'index': 6}]
    btn_trim_video = [main, {'AXIdentifier': 'LauncherToolCollectionViewItem', 'AXRole': 'AXGroup', 'index': 7}]
    btn_crop_rotate = [main, {'AXIdentifier': 'LauncherToolCollectionViewItem', 'AXRole': 'AXGroup', 'index': 8}]
    btn_video_speed = [main, {'AXIdentifier': 'LauncherToolCollectionViewItem', 'AXRole': 'AXGroup', 'index': 9}]
    btn_color_adjustment = [main, {'AXIdentifier': 'LauncherToolCollectionViewItem', 'AXRole': 'AXGroup', 'index': 10}]
    btn_speech_enhancement = [main, {'AXIdentifier': 'LauncherToolCollectionViewItem', 'AXRole': 'AXGroup', 'index': 11}]
    btn_STT = [main, {'AXIdentifier': 'LauncherToolCollectionViewItem', 'AXRole': 'AXGroup', 'index': 12}]

class seasonal_bb_window:
    main = {'AXIdentifier': '_NS:8'}

download_window_title = [
    {"AXIdentifier":"IDC_DOWNLOAD_TEMPLATE_FROM_CYBERLINKCLOUD_AND_DZ_DLG"},
    {"AXRole": "AXToolbar", "recursive": False},
    {"AXRole": "AXGroup", "recursive": False},
    {'AXIdentifier': 'IDC_DOWNLOAD_TEMPLATE_WINDOW_TITLE'}
]


class file_picker:
    # main = {"AXSubrole": "AXDialog", "AXMain": False, "AXRole": "AXWindow"}
    main = {"AXSubrole": "AXDialog", "AXRole": "AXWindow"}
    popup_button = {'AXRoleDescription': "pop up button"}
    view_options = {'AXIdentifier': 'View Options'}
    column_view = [view_options, {'AXIdentifier': 'cmdViewAsColumns:'}]
    show_more_options = [main, {'AXIdentifier': 'NS_OPEN_SAVE_DISCLOSURE_TRIANGLE'}]
    file_name = {'AXIdentifier': 'saveAsNameTextField'}  # Monterey
    file_name_big_sur = {'AXIdentifier': 'saveAsNameTextField'}
    tags_editbox = [main, {'AXRole': 'AXTextField', 'AXDescription': 'tag editor'}]
    tag_item = [tags_editbox, {'AXSubrole': 'AXTextAttachment'}]  # Catalina
    unit_menu_option_tag = [tags_editbox, {'AXRole': 'AXStaticText'}]
    btn_back = [main, {'AXRole': 'AXButton', 'AXDescription': 'back'}]
    btn_forward = [main, {'AXRole': 'AXButton', 'AXDescription': 'forward'}]
    btn_change_item_grouping = [main, {'AXRole': 'AXMenuButton', 'AXRoleDescription': 'menu button'}]
    btn_top_new_folder = [main, {'AXRole': 'AXButton', 'AXDescription': 'new folder'}]
    btn_bottom_new_folder = [main, {'AXRole': 'AXButton', 'AXTitle': 'New Folder'}]
    btn_cancel = [main, {'AXRole': 'AXButton', 'AXTitle': 'Cancel'}]
    btn_save = [main, {'AXRole': 'AXButton', 'AXTitle': 'Save'}]
    btn_open = [main, {'AXRole': 'AXButton', 'AXTitle': 'Open'}]
    btn_replace_exist_file = [main, {'AXRole': 'AXButton', 'AXTitle': 'Replace'}]
    sidebar = [main, {'AXDescription': 'sidebar'}]
    unit_sidebar_item = [sidebar, {'AXRole': 'AXStaticText', 'AXValue': ''}]

    class new_folder:
        main = [{"AXSubrole": "AXDialog", "AXMain": False, "AXRole": "AXWindow"}, {'AXRole': 'AXSheet', 'AXRoleDescription': 'sheet'}]
        str_new_folder = [main, {'AXRole': 'AXStaticText', 'AXValue': 'New Folder'}]
        btn_cancel = [main, {'AXRole': 'AXButton', 'AXTitle': 'Cancel'}]
        btn_create = [main, {'AXRole': 'AXButton', 'AXTitle': 'Create'}]
        editbox_folder_name = [main, {'AXRole': 'AXTextField', 'AXRoleDescription': 'text field'}]

class confirm_dialog():
    main_window = {'AXIdentifier': 'IDD_CLALERT'}
    btn_yes = [main_window, {'AXIdentifier': 'IDC_CLALERT_BUTTON_0'}]
    btn_ok = [main_window, {'AXIdentifier': 'IDC_CLALERT_BUTTON_0'}]
    btn_no = [main_window, {'AXIdentifier': 'IDC_CLALERT_BUTTON_1'}]
    btn_cancel = [main_window, {'AXIdentifier': 'IDC_CLALERT_BUTTON_1'}]

class colors(): # color picker
    main_window = {'AXTitle': 'Colors'}
    input_hex_color = {'AXIdentifier': 'hex'}
    btn_close = [main_window, {'AXRoleDescription': 'close button'}]
    btn_color_sliders = [main_window, {'AXHelp': 'Color Sliders'}]
    category = [main_window, {'AXRole': 'AXPopUpButton'}]
    category_items = [category, {"AXRole": "AXMenuItem", "get_all": True}]

# Create Color Gradient / Change Color Gradient
class create_color_gradient():
    main_window = {'AXTitle': 'Create Color Gradient'}
    input_hex_color = {'AXIdentifier': 'IDC_COLORGRADIENTCTRL_COLORPICKER'}
    btn_close = {'AXRoleDescription': 'close button'}
    btn_ok = {'AXIdentifier': 'IDC_COLORGRADIENTDLG_BTN_OK'}

class try_for_free_dialog:
    main = {'AXTitle': 'CyberLink PowerDirector', 'AXIdentifier': '_NS:8'}
    btn_try_for_free = {'AXTitle': 'Try for Free', 'AXRole': 'AXButton'}
    btn_unlock_all = {'AXTitle': 'Unlock All', 'AXRole': 'AXButton'}
    chx_do_not_show_again = {'AXRole': 'AXCheckBox', 'AXTitle': 'Don\'t show again'}
    icon_premium = {'AXDescription': 'icon premium2', 'AXRole': 'AXImage'}
    btn_try_once = {'AXTitle': 'Try Once', 'AXRole': 'AXButton'}

class pou_dialog:
    # if click STT again, should pop up POU
    btn_get_premium = {'AXTitle': 'GET PREMIUM', 'AXRole': 'AXLink'}

    # if insert premium content then click [Export], pop up POU dialog
    # You're using the following premium content.\nUpgrade your plan to export your video or remove all to continue
    btn_not_now = {'AXTitle': 'Not Now', 'AXIdentifier': 'IDC_BTN_CANCEL', 'AXRole': 'AXButton'}
    btn_remove_all = {'AXTitle': 'Remove All', 'AXIdentifier': 'IDC_SC_BUTTON_REMOVEALL', 'AXRole': 'AXButton'}

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


class EaseSet:
    def __init__(self, frame):
        class ControlSet:
            def __init__(self, ctrlframe):
                for items in zip(("arrow_up", "arrow_down", "value"), (
                        {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP'},
                        {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN'},
                        {'AXIdentifier': 'spinEditTextField'},
                )):
                    (locator := ctrlframe.copy()).append(items[1])
                    setattr(self, items[0], locator)

        ease_in = ControlSet([frame, {'AXIdentifier': 'IDC_EASE_CTRL_SPINEDIT_EASE_IN'}])
        ease_in_button = [frame, {'AXIdentifier': 'IDC_EASE_CTRL_CHECKBOX_EASE_IN'}]
        ease_in_slider = [frame, {'AXIdentifier': 'IDC_EASE_CTRL_SLIDER_EASE_IN'}]
        ease_out = ControlSet([frame, {'AXIdentifier': 'IDC_EASE_CTRL_SPINEDIT_EASE_OUT'}])
        ease_out_button = [frame, {'AXIdentifier': 'IDC_EASE_CTRL_CHECKBOX_EASE_OUT'}]
        ease_out_slider = [frame, {'AXIdentifier': 'IDC_EASE_CTRL_SLIDER_EASE_OUT'}]
        self.group_in = [ease_in_slider, ease_in.value, ease_in.arrow_up, ease_in.arrow_down, ease_in_button]
        self.group_out = [ease_out_slider, ease_out.value, ease_out.arrow_up, ease_out.arrow_down, ease_out_button]


class KeyframeSet:
    def __init__(self, frame):
        keyframe_reset = [frame, {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_RESET_PARAM_KEYFRAME'}]
        keyframe_previous = [frame, {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_PREVIOUS_KEYFRAME'}]
        keyframe_add_remove = [frame, {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_ADDREMOVE_KEYFRAME'}]
        keyframe_next = [frame, {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_NEXT_KEYFRAME'}]
        btn_reset_yes = [{'AXIdentifier': 'IDD_CLALERT'}, {'AXIdentifier': 'IDC_CLALERT_BUTTON_0'}]
        self.group = [keyframe_reset, keyframe_previous, keyframe_add_remove, keyframe_next, btn_reset_yes]


class KEComboSet:
    def __init__(self, keyframe_frame, ease_frame):
        self.group_keyframe = KeyframeSet(keyframe_frame)
        self.group_ease = EaseSet(ease_frame)
