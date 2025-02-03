from ..mask_designer import *
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

# if need update ground truth images (e.g. Run test case to another platform)
# Set take_preview_pic = 1
take_preview_pic = 0

class save_as_dlg():
    slider = {"AXIdentifier": "_NS:63"}
    ok = {"AXIdentifier": "_NS:72", "AXRoleDescription": "button"}
    cancel = {"AXIdentifier": "_NS:86"}
    name = {"AXIdentifier": "_NS:9"}


class cancel_dlg:
    main = {"AXIdentifier": "IDD_CLALERT", "AXMain": False}
    yes = [main, {"AXIdentifier": "IDC_CLALERT_BUTTON_2"}]
    no = [main, {"AXIdentifier": "IDC_CLALERT_BUTTON_2"}]
    cancel = [main, {"AXIdentifier": "IDC_CLALERT_BUTTON_2"}]


class tab:
    mask = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_MASK_TAB'}

tab_content = {'AXIdentifier': 'IDC_PIP_DESIGNER_SCROLLVIEW_CONTAINER'}
tab_scroll = {'AXIdentifier': 'IDC_PIP_DESIGNER_SCROLLBAR_Y'}
class mask_property:
    caption = [tab_content, {"AXRoleDescription": "outline row", "index": 0}]
    content = [tab_content, {"AXRoleDescription": "outline row", "index": 1}]
    scroll_bar = [content, {"AXRoleDescription": "value indicator"}]
    category = [content, {"AXIdentifier": "IDC_MASK_DESIGNER_BTN_MASK_LIST"}]
    category_option = [category, {"AXRoleDescription": "text"}]
    template = {'AXIdentifier': 'maskThumbCVI'}
    create_mask = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_CREATE_CUSTOM_MASK'}

    class gif:
        use_alpha_channel = {"AXIdentifier": "_NS:66", "AXRole": "AXCheckBox"}
        convert_grayscale = {"AXIdentifier": "_NS:122", "AXRole": "AXCheckBox"}
        ok = {"AXIdentifier": '_NS:129', "AXTitle": "OK"}
        cancel = {"AXIdentifier": '_NS:9', "AXTitle": "Cancel"}

    invert_mask = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_INVERT_MASK'}
    feather_slider = {'AXIdentifier': 'IDC_MASK_DESIGNER_SLIDER_FEATHER'}
    feather_group = {'AXIdentifier': 'IDC_MASK_DESIGNER_SPINEDIT_FEATHER'}
    feather_up = [feather_group, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP'}]
    feather_down = [feather_group, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN'}]


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

    scale_width_slider = {'AXIdentifier': 'IDC_MASK_DESIGNER_OB_SLIDER_WIDTH'}
    scale_width = [content, {'AXIdentifier': 'IDC_MASK_DESIGNER_SPINEDIT_WIDTH'}]
    scale_width_value = [scale_width, {"AXIdentifier": "spinEditTextField"}]
    scale_width_up = [scale_width, {"AXIdentifier": "IDC_SPINEDIT_BTN_UP"}]
    scale_width_down = [scale_width, {"AXIdentifier": "IDC_SPINEDIT_BTN_DOWN"}]

    scale_height_slider = {'AXIdentifier': 'IDC_MASK_DESIGNER_OB_SLIDER_HEIGHT'}
    scale_height = [content, {'AXIdentifier': 'IDC_MASK_DESIGNER_SPINEDIT_HEIGHT'}]
    scale_height_value = [scale_height, {"AXIdentifier": "spinEditTextField"}]
    scale_height_up = [scale_height, {"AXIdentifier": "IDC_SPINEDIT_BTN_UP"}]
    scale_height_down = [scale_height, {"AXIdentifier": "IDC_SPINEDIT_BTN_DOWN"}]
    scale_ratio = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_MAINTAIN_ASPECT_RATIO'}

    opacity_slider = {'AXIdentifier': 'IDC_MASK_DESIGNER_OB_SLIDER_OPACITY'}
    opacity = {'AXIdentifier': 'IDC_MASK_DESIGNER_SPINEDIT_OPACITY'}
    opacity_value = [opacity, {"AXIdentifier": "spinEditTextField"}]
    opacity_up = [opacity, {"AXIdentifier": "IDC_SPINEDIT_BTN_UP"}]
    opacity_down = [opacity, {"AXIdentifier": "IDC_SPINEDIT_BTN_DOWN"}]

    rotation = {'AXIdentifier': 'IDC_MASK_DESIGNER_OB_SPINEDIT_ROTATION'}
    rotation_value = [rotation, {"AXIdentifier": "spinEditTextField"}]
    rotation_up = [rotation, {"AXIdentifier": "IDC_SPINEDIT_BTN_UP"}]
    rotation_down = [rotation, {"AXIdentifier": "IDC_SPINEDIT_BTN_DOWN"}]


class preview:
    play = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_PLAY'}
    stop = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_STOP'}
    previous_frame = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_PREV_FRAME'}
    next_frame = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_NEXT_FRAME', "AXRole": "AXButton"}
    fast_forward = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_FAST_FORWARD'}


zoom = {"AXIdentifier": "IDC_MASK_DESIGNER_BTN_ZOOM_LEVEL"}
zoom_value = [zoom]
zoom_in = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_ZOOM_IN'}
zoom_out = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_ZOOM_OUT'}

toggle_grid_line = {"AXIdentifier":'IDC_MASK_DESIGNER_BTN_GRID_LINE_MENU'}
snap_ref_line = [toggle_grid_line, {'AXRole': "AXMenuItem", "index": 0}]
grid_line = [toggle_grid_line, {'AXRole': "AXMenuItem", "index": 1}]
grid_list = [grid_line, {"AXRole": "AXMenuItem"}]
