mask_designer_window = {"AXIdentifier": "_NS:10"}
close = [mask_designer_window, {"AXSubrole": "AXCloseButton"}]
zoom_window = [mask_designer_window, {"AXSubrole": "AXZoomButton"}]

preview_window = {"AXIdentifier": "_NS:87", "AXRoleDescription": "scroll area"}
timecode = {"AXRole": "AXStaticText", "AXIdentifier": "spinTimeEditTextField"}
# toolbar = {"AXRole": "AXToolbar"}
# undo = [toolbar, {"AXRole": "AXButton", "index": 1}]
# redo = [toolbar, {"AXRole": "AXButton", "index": 2}]
split_group = {"AXRole": "AXSplitGroup", "AXIdentifier": "_NS:75"}
undo = [split_group, {"AXRole": "AXButton", "index": 3}]
redo = [split_group, {"AXRole": "AXButton", "index": 4}]
only_show_selected_track_checkbox = {"AXIdentifier": "_NS:136"}

ok = {"AXIdentifier": "IDC_MASK_DESIGNER_BTN_OK"}
save_as = {"AXIdentifier": "_NS:102", "index": 1}
cancel = {"AXIdentifier": "IDC_MASK_DESIGNER_BTN_CANCEL"}
share = {'AXIdentifier': '_NS:184', "AXRoleDescription": "button"}

# if need update ground truth images (e.g. Run test case to another platform)
# Set take_preview_pic = 1
take_preview_pic = 0

class save_as_dlg():
    slider = {"AXIdentifier": "_NS:63"}
    ok = {"AXIdentifier": "_NS:72", "AXRoleDescription": "button"}
    cancel = {"AXIdentifier": "_NS:86"}
    name = {"AXIdentifier": "_NS:9"}


class cancel_dlg:
    main = {"AXIdentifier": "_NS:10", "AXMain": False}
    yes = [main, {"AXRole": "AXButton", "index": 0}]
    no = [main, {"AXRole": "AXButton", "index": 1}]
    cancel = [main, {"AXRole": "AXButton", "index": 2}]


class tab:
    mask = {'AXIdentifier': 'IDC_PIP_DESIGNER_OUTLINEVIEW_CONTAINER', "index": 0}


class mask_property:
    scroll_bar = [{"AXIdentifier": "_NS:81", "AXRoleDescription": "scroll bar"},
                  {"AXRoleDescription": "value indicator"}]
    caption = [tab.mask, {"AXRoleDescription": "outline row", "index": 0}]
    content = [tab.mask, {"AXRoleDescription": "outline row", "index": 1}]
    category = [content, {"AXIdentifier": "_NS:9", "index": 0}]
    category_option = [category, {"AXRoleDescription": "text"}]
    template = {'AXIdentifier': 'maskThumbCVI'}
    create_mask = {'AXIdentifier': '_NS:108'}

    class gif:
        use_alpha_channel = {"AXIdentifier": "_NS:66", "AXRole": "AXCheckBox"}
        convert_grayscale = {"AXIdentifier": "_NS:122", "AXRole": "AXCheckBox"}
        ok = {"AXIdentifier": '_NS:129', "AXTitle": "OK"}
        cancel = {"AXIdentifier": '_NS:9', "AXTitle": "Cancel"}

    invert_mask = {'AXIdentifier': '_NS:137'}
    feather_slider = {'AXIdentifier': '_NS:124'}
    feather_group = {'AXIdentifier': '_NS:94', "AXRole": "AXGroup"}
    feather_up = [feather_group, {'AXIdentifier': '_NS:9'}]
    feather_down = [feather_group, {'AXIdentifier': '_NS:72'}]


class settings:
    scroll_bar = {'AXIdentifier': 'IDC_PIP_DESIGNER_SCROLLBAR_Y'}
    caption = [tab.mask, {"AXRoleDescription": "outline row", "index": 2}]
    content = [tab.mask, {"AXRoleDescription": "outline row", "index": 3}]

    position_x = {'AXIdentifier': 'IDC_MASK_DESIGNER_OB_SPINEDIT_POSITION_X'}
    position_x_value = [position_x, {"AXIdentifier": "spinEditTextField"}]
    position_x_up = [position_x, {"AXIdentifier": "_NS:9"}]
    position_x_down = [position_x, {"AXIdentifier": "_NS:72"}]

    position_y = {'AXIdentifier': 'IDC_MASK_DESIGNER_OB_SPINEDIT_POSITION_Y'}
    position_y_value = [position_y, {"AXIdentifier": "spinEditTextField"}]
    position_y_up = [position_y, {"AXIdentifier": "_NS:9"}]
    position_y_down = [position_y, {"AXIdentifier": "_NS:72"}]

    scale_width_slider = {'AXIdentifier': 'IDC_MASK_DESIGNER_OB_SLIDER_WIDTH'}
    scale_width = [content, {'AXIdentifier': '_NS:102'}]
    scale_width_value = [scale_width, {"AXIdentifier": "spinEditTextField"}]
    scale_width_up = [scale_width, {"AXIdentifier": "_NS:9"}]
    scale_width_down = [scale_width, {"AXIdentifier": "_NS:72"}]

    scale_height_slider = {'AXIdentifier': 'IDC_MASK_DESIGNER_OB_SLIDER_HEIGHT'}
    scale_height = [content, {'AXIdentifier': '_NS:119'}]
    scale_height_value = [scale_height, {"AXIdentifier": "spinEditTextField"}]
    scale_height_up = [scale_height, {"AXIdentifier": "_NS:9"}]
    scale_height_down = [scale_height, {"AXIdentifier": "_NS:72"}]
    scale_ratio = {'AXIdentifier': '_NS:122'}

    opacity_slider = {'AXIdentifier': 'IDC_MASK_DESIGNER_OB_SLIDER_OPACITY'}
    opacity = {'AXIdentifier': '_NS:168'}
    opacity_value = [opacity, {"AXIdentifier": "spinEditTextField"}]
    opacity_up = [opacity, {"AXIdentifier": "_NS:9"}]
    opacity_down = [opacity, {"AXIdentifier": "_NS:72"}]

    rotation = {'AXIdentifier': 'IDC_MASK_DESIGNER_OB_SPINEDIT_ROTATION'}
    rotation_value = [rotation, {"AXIdentifier": "spinEditTextField"}]
    rotation_up = [rotation, {"AXIdentifier": "_NS:9"}]
    rotation_down = [rotation, {"AXIdentifier": "_NS:72"}]


class preview:
    play = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_PLAY'}
    pause = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_PAUSE'}
    stop = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_STOP'}
    previous_frame = {'AXIdentifier': '_NS:41'}
    next_frame = {'AXIdentifier': '_NS:50', "AXRole": "AXButton"}
    fast_forward = {'AXIdentifier': '_NS:59'}


zoom = [split_group, {"AXIdentifier": "_NS:102"}]
zoom_value = [split_group]
zoom_in = {'AXIdentifier': '_NS:211', "AXRole": "AXButton"}
zoom_out = {'AXIdentifier': '_NS:206', "AXRole": "AXButton"}

toggle_grid_line = {'AXIdentifier': '_NS:226'}
snap_ref_line = {'AXRole': "AXMenuItem", "AXIdentifier": "_NS:80"}
grid_line = {'AXIdentifier': '_NS:91'}
grid_list = [grid_line, {"AXRole": "AXMenuItem"}]
