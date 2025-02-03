mask_designer_window = {"AXIdentifier": "IDC_MASK_DESIGNER_WINDOW"}
close = [mask_designer_window, {"AXSubrole": "AXCloseButton"}]
zoom_window = [mask_designer_window, {"AXSubrole": "AXZoomButton"}]

preview_window = {"AXIdentifier": "IDC_MASK_DESIGNER_SCROLLVIEW_PREVIEW", "AXRoleDescription": "scroll area"}
timecode = {"AXRole": "AXStaticText", "AXIdentifier": "spinTimeEditTextField"}
# toolbar = {"AXRole": "AXToolbar"}
# undo = [toolbar, {"AXRole": "AXButton", "index": 1}]
# redo = [toolbar, {"AXRole": "AXButton", "index": 2}]
# split_group = {"AXRole": "AXSplitGroup", "AXIdentifier": "_NS:75"}
# undo = [split_group, {"AXRole": "AXButton", "index": 3}]
# redo = [split_group, {"AXRole": "AXButton", "index": 4}]
undo = {"AXIdentifier": "IDC_MASK_DESIGNER_BTN_UNDO"}
redo = {"AXIdentifier": "IDC_MASK_DESIGNER_BTN_REDO"}
only_show_selected_track_checkbox = {"AXIdentifier": "IDC_MASK_DESIGNER_CHECKBOX_SHOW_SELECTED_TRACK"}

ok = {"AXIdentifier": "IDC_MASK_DESIGNER_BTN_OK"}
save_as = {"AXIdentifier": "IDC_MASK_DESIGNER_BTN_SAVE_AS"}
cancel = {"AXIdentifier": "IDC_MASK_DESIGNER_BTN_CANCEL"}
share = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_SHARE'}

mask_frame = [mask_designer_window, {"AXIdentifier": "dashBorderedView", "index": 1}]

btn_hide_timeline_mode = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_HIDE_TIMELINE'}
btn_display_timeline_mode = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_SHOW_TIMELINE'}

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


# if need update ground truth images (e.g. Run test case to another platform)
# Set take_preview_pic = 1
take_preview_pic = 0


class save_as_dlg():
    slider = {"AXIdentifier": "IDC_SAVE_TEMPLATE_SLIDER_MARK_FRAME"}
    ok = {"AXIdentifier": "IDC_SAVE_TEMPLATE_BTN_OK", "AXRoleDescription": "button"}
    cancel = {"AXIdentifier": "IDC_SAVE_TEMPLATE_BTN_CANCEL"}
    name = {"AXIdentifier": "IDC_SAVE_TEMPLATE_EDIT_TEMPLATE_NAME"}


class cancel_dlg:
    main = {"AXIdentifier": "IDD_CLALERT", "AXMain": False}
    yes = [main, {"AXIdentifier": "IDC_CLALERT_BUTTON_0"}]
    no = [main, {"AXIdentifier": "IDC_CLALERT_BUTTON_1"}]
    cancel = [main, {"AXIdentifier": "IDC_CLALERT_BUTTON_2"}]


class tab:
    mask = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_MASK_TAB'}
    motion = {'AXTitle': 'Motion', "AXRole": "AXButton"}

class motion_tab:
    path_text = {'AXIdentifier': 'IDC_DESIGNER_TEXT_PROPERTY', "AXValue": "Path"}
    path_tag = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', "index": 0}
    path_category = {'AXIdentifier': 'IDC_MASK_DESIGNER_MOTIONPATH_COMBOBOX_FILTER'}
    path_category_item = {"AXRoleDescription": "text", "AXRole": "AXStaticText", "get_all": True}
    path_template_item = {"AXRoleDescription": "group", 'AXIdentifier': 'motionPathThumbCVI', "get_all": True}
    save_path_btn = {'AXIdentifier': 'IDC_MASK_DESIGNER_MOTIONPATH_BTN_SAVE_MOTION_SCRIPT'}
    remove_menu_item = {'AXIdentifier': 'onRemovePathWithSender:'}
    confirm_remove_window = {"AXIdentifier": "IDD_CLALERT", "AXMain": False}
    confirm_remove_ok = [confirm_remove_window, {"AXIdentifier": "IDC_CLALERT_BUTTON_0"}]


tab_content = {'AXIdentifier': 'IDC_PIP_DESIGNER_SCROLLVIEW_CONTAINER'}
tab_scroll = {'AXIdentifier': 'IDC_PIP_DESIGNER_SCROLLBAR_Y'}
property_captions = {'AXIdentifier': 'IDC_DESIGNER_TEXT_PROPERTY', "get_all": True}
property_frame = {'AXIdentifier': 'IDC_PIP_DESIGNER_OUTLINEVIEW_CONTAINER'}


class mask_property:
    caption = [tab_content, {"AXRoleDescription": "outline row", "index": 0}]
    content = [tab_content, {"AXRoleDescription": "outline row", "index": 1}]
    scroll_bar = [content, {"AXRoleDescription": "value indicator"}]
    category = [content, {"AXIdentifier": "IDC_MASK_DESIGNER_BTN_MASK_LIST"}]
    category_option = [category, {"AXRoleDescription": "text"}]
    template = {'AXIdentifier': 'maskThumbCVI'}
    create_mask = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_CREATE_CUSTOM_MASK'}
    create_text_mask = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_TITLE_MASK'}
    create_brush_mask = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_SELECTION_MASK', "index": 0}
    mask_property_text = {'AXIdentifier': 'IDC_DESIGNER_TEXT_PROPERTY', "AXValue": "Mask Properties"}
    create_selection_mask = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_SELECTION_MASK', "index": 1}

    class mask_composer:
        window = {'AXIdentifier': 'TITLE_DESIGNER_DLG', "AXTitle": "Mask Composer"}

    class brush_mask_designer:
        window = {'AXIdentifier': 'IDC_BRUSHMASK_DESIGNER_WINDOW'}
        undo = {'AXIdentifier': 'IDC_BRUSH_MASK_DESIGNER_BTN_UNDO'}
        redo = {'AXIdentifier': 'IDC_BRUSH_MASK_DESIGNER_BTN_REDO'}
        reset = {'AXIdentifier': 'IDC_BRUSH_MASK_DESIGNER_BTN_RESET'}
        maximize = [window, {"AXSubrole": "AXZoomButton"}]
        close = [window, {"AXSubrole": "AXCloseButton"}]
        auto_object_select_tool = {'AXIdentifier': 'IDC_BRUSH_MASK_DESIGNER_BTN_AUTO_SELECTION'}
        preview_area = [window, {'AXIdentifier': 'IDC_MASK_DESIGNER_SCROLLVIEW_PREVIEW'}]
        brush_preview = {'AXIdentifier': '_NS:129', "AXRole": "AXImage"}
        width_value_parent = {'AXIdentifier': 'IDC_BRUSH_MASK_DESIGNER_SPINEDIT_TRANSPARENCY', "index": 1}
        width_value = [width_value_parent, {'AXIdentifier': 'spinEditTextField'}]
        width_slider = {'AXIdentifier': 'IDC_BRUSH_MASK_DESIGNER_SLIDER_WIDTH'}
        width_arrow_up = [width_value_parent, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP'}]
        width_arrow_down = [width_value_parent, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN'}]
        transparency_value_parent = {'AXIdentifier': 'IDC_BRUSH_MASK_DESIGNER_SPINEDIT_TRANSPARENCY', "index": 0}
        transparency_value = [transparency_value_parent, {'AXIdentifier': 'spinEditTextField'}]
        transparency_slider = {'AXIdentifier': 'IDC_BRUSH_MASK_DESIGNER_SLIDER_TRANSPARENCY'}
        transparency_arrow_up = [transparency_value_parent, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP'}]
        transparency_arrow_down = [transparency_value_parent, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN'}]

        class smart_brush:
            ceate_new_selection = {'AXIdentifier': 'IDC_BRUSH_MASK_DESIGNER_BTN_NEW_SELECTION'}
            add_to_selection = {'AXIdentifier': 'IDC_BRUSH_MASK_DESIGNER_BTN_ADD_SELECTION'}
            subtract_from_selection = {'AXIdentifier': 'IDC_BRUSH_MASK_DESIGNER_BTN_SUBTRACT_SELECTION'}


        zoom_out = {'AXIdentifier': 'IDC_BRUSH_MASK_DESIGNER_BTN_ZOOM_OUT'}
        zoom_in = {'AXIdentifier': 'IDC_BRUSH_MASK_DESIGNER_BTN_ZOOM_IN'}
        zoom_menu = {'AXIdentifier': 'IDC_BRUSH_MASK_DESIGNER_BTN_ZOOM_LEVEL'}
        zoom_menu_item = {"AXRoleDescription": "text", "AXRole": "AXStaticText", "get_all": True}
        previous_frame = {'AXIdentifier': 'IDC_BURSH_MASK_DESIGNER_BTN_PREV_FRAME'}
        next_frame = {'AXIdentifier': 'IDC_BURSH_MASK_DESIGNER_BTN_NEXT_FRAME'}
        timecode_parent = {'AXIdentifier': '_NS:29'}
        timecode = [timecode_parent, {'AXIdentifier': 'spinTimeEditTextField'}]

        ok = [window, {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_OK'}]
        cancel = [window, {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_CANCEL'}]

        class reset_dialog:
            window = {'AXIdentifier': 'IDD_CLALERT'}
            ok = {'AXIdentifier': 'IDC_CLALERT_BUTTON_0'}
            cancel = {'AXIdentifier': 'IDC_CLALERT_BUTTON_1'}

        class close_dialog:
            window = {'AXIdentifier': 'IDD_CLALERT'}
            cancel = {'AXIdentifier': 'IDC_CLALERT_BUTTON_2'}
            no = {'AXIdentifier': 'IDC_CLALERT_BUTTON_1'}
            yes = {'AXIdentifier': 'IDC_CLALERT_BUTTON_0'}

        class tools:
            round = {'AXIdentifier': 'IDC_BRUSH_MASK_DESIGNER_BTN_ROUND'}
            flat = {'AXIdentifier': 'IDC_BRUSH_MASK_DESIGNER_BTN_FLAT'}
            smart_brush = {'AXIdentifier': 'IDC_BRUSH_MASK_DESIGNER_BTN_ADD_SELECTION'}
            eraser = {'AXIdentifier': 'IDC_BRUSH_MASK_DESIGNER_BTN_ERASER'}

    class gif:
        use_alpha_channel = {"AXIdentifier": "IDC_MASK_DESIGNER_BTN_USE_ALPHA_CHANNEL", "AXRole": "AXCheckBox"}
        convert_grayscale = {"AXIdentifier": "IDC_MASK_DESIGNER_BTN_USE_GREY_SCALE", "AXRole": "AXCheckBox"}
        ok = {"AXIdentifier": 'IDC_MASK_DESIGNER_MODE_SELECTION_BTN_OK', "AXTitle": "OK"}
        cancel = {"AXIdentifier": 'IDC_MASK_DESIGNER_MODE_SELECTION_BTN_CANCEL', "AXTitle": "Cancel"}

    invert_mask = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_INVERT_MASK'}
    feather_slider = {'AXIdentifier': 'IDC_MASK_DESIGNER_SLIDER_FEATHER'}
    feather_group = {'AXIdentifier': 'IDC_MASK_DESIGNER_SPINEDIT_FEATHER'}
    feather_up = [feather_group, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP'}]
    feather_down = [feather_group, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN'}]
    selection_mask_list = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_SELECTION_MASK_LIST'}


class settings:
    scroll_bar = {'AXIdentifier': 'IDC_PIP_DESIGNER_SCROLLBAR_Y'}
    caption = [tab.mask, {"AXRoleDescription": "outline row", "index": 2}]
    content = [tab.mask, {"AXRoleDescription": "outline row", "index": 3}]

    position_x = {'AXIdentifier': 'IDC_MASK_DESIGNER_OB_SPINEDIT_POSITION_X'}
    position_x_value = [position_x, {"AXIdentifier": "spinEditTextField"}]
    position_x_up = [position_x, {"AXIdentifier": "IDC_SPINEDIT_BTN_UP"}]
    position_x_down = [position_x, {"AXIdentifier": "IDC_SPINEDIT_BTN_DOWN"}]

    position_y = {'AXIdentifier': 'IDC_MASK_DESIGNER_OB_SPINEDIT_POSITION_Y'}
    position_y_value = [position_y, {"AXIdentifier": "spinEditTextField"}]
    position_y_up = [position_y, {"AXIdentifier": "IDC_SPINEDIT_BTN_UP"}]
    position_y_down = [position_y, {"AXIdentifier": "IDC_SPINEDIT_BTN_DOWN"}]

    class ControlSet:
        def __init__(self, keyframe, ease):
            self.previous_keyframe = [keyframe, {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_PREVIOUS_KEYFRAME'}]
            self.add_remove_keyframe = [keyframe, {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_ADDREMOVE_KEYFRAME'}]
            self.next_keyframe = [keyframe, {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_NEXT_KEYFRAME'}]
            self.reset_keyframe = [keyframe, {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_RESET_PARAM_KEYFRAME'}]
            self.group_ease = EaseSet(ease)

    position_ease = {'AXIdentifier': 'IDC_MASK_DESIGNER_EASE_CTRL_POSITION'}
    position_keyframe = {"AXIdentifier": "IDC_MASK_DESIGNER_KEYFRAME_CTRL_POSITION"}
    position = ControlSet(position_keyframe, position_ease)
    scale_ease = {'AXIdentifier': 'IDC_MASK_DESIGNER_EASE_CTRL_SCALE'}
    scale_keyframe = {"AXIdentifier": "IDC_MASK_DESIGNER_KEYFRAME_CTRL_SCALE"}
    scale = ControlSet(scale_keyframe, scale_ease)
    opacity_ease = {'AXIdentifier': 'IDC_MASK_DESIGNER_EASE_CTRL_OPACITY'}
    opacity_keyframe = {"AXIdentifier": "IDC_MASK_DESIGNER_KEYFRAME_CTRL_OPACITY"}
    opacity = ControlSet(opacity_keyframe, opacity_ease)
    rotation_ease = {'AXIdentifier': 'IDC_MASK_DESIGNER_EASE_CTRL_ROTATION'}
    rotation_keyframe = {"AXIdentifier": "IDC_MASK_DESIGNER_KEYFRAME_CTRL_ROTATION"}
    rotation = ControlSet(rotation_keyframe, rotation_ease)

    scale_width_slider = {'AXIdentifier': 'IDC_MASK_DESIGNER_OB_SLIDER_WIDTH'}
    scale_width = {'AXIdentifier': 'IDC_MASK_DESIGNER_SPINEDIT_WIDTH'}
    scale_width_value = [scale_width, {"AXIdentifier": "spinEditTextField"}]
    scale_width_up = [scale_width, {"AXIdentifier": "IDC_SPINEDIT_BTN_UP"}]
    scale_width_down = [scale_width, {"AXIdentifier": "IDC_SPINEDIT_BTN_DOWN"}]

    scale_height_slider = {'AXIdentifier': 'IDC_MASK_DESIGNER_OB_SLIDER_HEIGHT'}
    scale_height = {'AXIdentifier': 'IDC_MASK_DESIGNER_SPINEDIT_HEIGHT'}
    scale_height_value = [scale_height, {"AXIdentifier": "spinEditTextField"}]
    scale_height_up = [scale_height, {"AXIdentifier": "IDC_SPINEDIT_BTN_UP"}]
    scale_height_down = [scale_height, {"AXIdentifier": "IDC_SPINEDIT_BTN_DOWN"}]
    scale_ratio = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_MAINTAIN_ASPECT_RATIO'}

    opacity_slider = {'AXIdentifier': 'IDC_MASK_DESIGNER_OB_SLIDER_OPACITY'}
    opacity_set = {'AXIdentifier': 'IDC_MASK_DESIGNER_SPINEDIT_OPACITY'}
    opacity_value = [opacity_set, {"AXIdentifier": "spinEditTextField"}]
    opacity_up = [opacity_set, {"AXIdentifier": "IDC_SPINEDIT_BTN_UP"}]
    opacity_down = [opacity_set, {"AXIdentifier": "IDC_SPINEDIT_BTN_DOWN"}]

    rotation_set = {'AXIdentifier': 'IDC_MASK_DESIGNER_OB_SPINEDIT_ROTATION'}
    rotation_value = [rotation_set, {"AXIdentifier": "spinEditTextField"}]
    rotation_up = [rotation_set, {"AXIdentifier": "IDC_SPINEDIT_BTN_UP"}]
    rotation_down = [rotation_set, {"AXIdentifier": "IDC_SPINEDIT_BTN_DOWN"}]


class preview:
    play = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_PLAY'}
    stop = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_STOP'}
    previous_frame = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_PREV_FRAME'}
    next_frame = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_NEXT_FRAME', "AXRole": "AXButton"}
    fast_forward = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_FAST_FORWARD'}

    mask_object = {"AXIdentifier": "dashBorderedView", "index": 1}
    video_frame = {"AXIdentifier": "dashBorderedView", "index": 0}


zoom = {"AXIdentifier": "IDC_MASK_DESIGNER_BTN_ZOOM_LEVEL"}
zoom_value = [zoom]
zoom_in = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_ZOOM_IN'}
zoom_out = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_ZOOM_OUT'}

toggle_grid_line = {"AXIdentifier": 'IDC_MASK_DESIGNER_BTN_GRID_LINE_MENU'}
snap_ref_line = [toggle_grid_line, {'AXRole': "AXMenuItem", "index": 0}]
grid_line = [toggle_grid_line, {'AXRole': "AXMenuItem", "index": 1}]
grid_list = [grid_line, {"AXRole": "AXMenuItem"}]

class simple_track:
    unit_keyframe_outline_row = [{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW'}, {'AXRole': 'AXRow'}]
    unit_keyframe_attribute_outline_row = [mask_designer_window, {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW'}, {'AXRoleDescription': 'outline row'}]
    unit_attribute_name = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_KEYFRAME_HEADER_CELL_TITLE'}
    track_header_outline_view = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW'}
    btn_next_keyframe = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_NEXT_KEYFRAME'}
    btn_add_remove_keyframe = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_ADD_REMOVE_KEYFRAME'}
    btn_previous_keyframe = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_PREV_KEYFRAME'}