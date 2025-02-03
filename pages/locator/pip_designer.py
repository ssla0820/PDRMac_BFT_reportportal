properties = {'AXIdentifier': 'IDC_PIP_DESIGNER_SCROLLVIEW_CONTAINER', 'AXRoleDescription': 'scroll area'}
properties_title = {'AXIdentifier': 'IDC_PIP_DESIGNER_BUTTON_PROPERTIES', 'AXTitle': 'Properties'}
preview = {'AXIdentifier': 'dashBorderedView', 'AXRoleDescription': 'group'}
timecode = {'AXIdentifier': 'spinTimeEditTextField', 'AXRoleDescription': 'text'}
designer_window = {'AXIdentifier': 'PIP_DESIGNER_DLG', 'AXRoleDescription': 'dialog'}
simple_track = [{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW'}, {'AXRole': 'AXRow', 'index': 0}] # hardcode_20v3303: _NS:195 > IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW

timecode = {'AXIdentifier': 'spinTimeEditTextField', 'AXRoleDescription': 'text'}
show_the_selected_track = {'AXIdentifier': 'IDC_PIP_DESIGNER_BUTTON_SHOWSELTRACK', 'AXTitle': 'Only show the selected track'}

menu_bar_help = {'AXIdentifier': 'IDM_PIP_DESIGNER_MAIN_MENU_HELP', 'AXRoleDescription': 'menu bar item'} # hardcode_20v3303: _NS:71 > IDM_PIP_DESIGNER_MAIN_MENU_HELP
menu_help = {'AXIdentifier': 'IDM_PIP_DESIGNER_MAIN_MENU_HELP_ITEM_HELP', 'AXRoleDescription': 'menu item'} # hardcode_20v3303: _NS:15 > IDM_PIP_DESIGNER_MAIN_MENU_HELP_ITEM_HELP

undo_btn = {'AXIdentifier': 'IDC_PIP_DESIGNER_BUTTON_UNDO', 'AXRoleDescription': 'button'}
redo_btn = {'AXIdentifier': 'IDC_PIP_DESIGNER_BUTTON_REDO', 'AXRoleDescription': 'button'}

# outline_row = [{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW', 'AXRoleDescription': 'outline'},
#                {'AXRole': 'AXRow', 'AXRoleDescription': 'outline row', 'index': 0},
#                {'AXIdentifier': '_NS:9', 'AXRole': 'AXButton'}] # hardcode_20v3303: _NS:195 > IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW # *unused*

class object_setting:
    object_setting = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRoleDescription': 'disclosure triangle'}
    scroll_bar = [{'AXIdentifier': 'IDC_PIP_DESIGNER_SCROLLBAR_Y'}, {'AXRole': 'AXValueIndicator', 'AXRoleDescription': 'value indicator'}]
    position = {'AXIdentifier': 'IDC_PIP_DESIGNER_OBJECT_SETTING_POSITION_TITLE', 'AXRoleDescription': 'text'} # hardcode_20v3303: _NS:15 > IDC_PIP_DESIGNER_OBJECT_SETTING_POSITION_TITLE
    position_add_remove_keyframe = {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_ADDREMOVE_KEYFRAME', 'AXRoleDescription': 'button'}
    position_reset_keyframe = {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_RESET_PARAM_KEYFRAME', 'AXRoleDescription': 'button'}
    reset_dialog = {'AXIdentifier': 'IDC_CLALERT_MESSAGE', 'AXValue': 'This operation will reset all the keyframes for this property.\nDo you want to continue?'}
    btn_yes_reset_dialog = {'AXIdentifier': 'IDC_CLALERT_BUTTON_0'}
    position_previous_keyframe = {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_PREVIOUS_KEYFRAME', 'AXRoleDescription': 'button'}
    position_next_keyframe = {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_NEXT_KEYFRAME', 'AXRoleDescription': 'button'}
    x_position = {'AXIdentifier': 'IDC_PIP_DESIGNER_SPINEDIT_POSITION_X', 'AXRole': 'AXGroup'}
    x_position_value = [x_position, {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field'}]
    x_position_up = [x_position, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP', 'AXRoleDescription': 'button'}]
    x_position_down = [x_position, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN', 'AXRoleDescription': 'button'}]
    y_position = {'AXIdentifier': 'IDC_PIP_DESIGNER_SPINEDIT_POSITION_Y', 'AXRole': 'AXGroup'}
    y_position_value = [y_position, {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field'}]
    y_position_up = [y_position, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP', 'AXRoleDescription': 'button'}]
    y_position_down = [y_position, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN', 'AXRoleDescription': 'button'}]
    ease_in_checkbox = {'AXIdentifier': 'IDC_EASE_CTRL_CHECKBOX_EASE_IN', 'AXRoleDescription': 'toggle button'}
    ease_in_value_box = {'AXIdentifier': 'IDC_EASE_CTRL_SPINEDIT_EASE_IN', 'AXRole': 'AXGroup'}
    ease_in_value = [ease_in_value_box, {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field'}]
    ease_in_value_up = [ease_in_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP', 'AXRoleDescription': 'button'}]
    ease_in_value_down = [ease_in_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN', 'AXRoleDescription': 'button'}]
    ease_in_slider = {'AXIdentifier': 'IDC_EASE_CTRL_SLIDER_EASE_IN', 'AXRoleDescription': 'slider'}
    ease_out_checkbox = {'AXIdentifier': 'IDC_EASE_CTRL_CHECKBOX_EASE_OUT', 'AXRoleDescription': 'toggle button'}
    ease_out_value_box = [{'AXIdentifier': 'IDC_PIP_DESIGNER_EASE_POSITION'}, {'AXIdentifier': 'IDC_EASE_CTRL_SPINEDIT_EASE_OUT'}]
    ease_out_value = [ease_out_value_box, {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field'}]
    ease_out_value_up = [ease_out_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP', 'AXRoleDescription': 'button'}]
    ease_out_value_down = [ease_out_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN', 'AXRoleDescription': 'button'}]
    ease_out_slider = {'AXIdentifier': 'IDC_EASE_CTRL_SLIDER_EASE_OUT', 'AXRoleDescription': 'slider'}
    class scale:
        scale = {'AXIdentifier': 'IDC_PIP_DESIGNER_OBJECT_SETTING_SCALE_TITLE', 'AXRoleDescription': 'text'} # hardcode_20v3303: _NS:79 > IDC_PIP_DESIGNER_OBJECT_SETTING_SCALE_TITLE
        add_remove_current_keyframe = {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_ADDREMOVE_KEYFRAME', 'AXRoleDescription': 'button', 'index': 1}
        reset_keyframe = {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_RESET_PARAM_KEYFRAME', 'AXRoleDescription': 'button', 'index': 1}
        previous_keyframe = {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_PREVIOUS_KEYFRAME', 'AXRoleDescription': 'button', 'index': 1}
        next_keyframe = {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_NEXT_KEYFRAME', 'AXRoleDescription': 'button', 'index': 1}
        width_value_box = {'AXIdentifier': 'IDC_PIP_DESIGNER_SPINEDIT_SCALE_WIDTH', 'AXRoleDescription': 'group'}
        width_value = [width_value_box, {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field'}]
        width_value_up = [width_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP', 'AXRoleDescription': 'button'}]
        width_value_down = [width_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN', 'AXRoleDescription': 'button'}]
        width_slider = {'AXIdentifier': 'IDC_PIP_DESIGNER_SLIDER_SCALE_WIDTH', 'AXRoleDescription': 'slider'}
        height_value_box = {'AXIdentifier': 'IDC_PIP_DESIGNER_SPINEDIT_SCALE_HEIGHT', 'AXRoleDescription': 'group'}
        height_value = [height_value_box, {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field'}]
        height_value_up = [height_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP', 'AXRoleDescription': 'button'}]
        height_value_down = [height_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN', 'AXRoleDescription': 'button'}]
        height_slider = {'AXIdentifier': 'IDC_PIP_DESIGNER_SLIDER_SCALE_HEIGHT', 'AXRoleDescription': 'slider'}
        maintain_aspect_ratio = {'AXIdentifier': 'IDC_PIP_DESIGNER_OB_CHECKBOX_KEEPRATIO', 'AXRoleDescription': 'toggle button'}
        ease_in_checkbox = {'AXIdentifier': 'IDC_EASE_CTRL_CHECKBOX_EASE_IN', 'AXRoleDescription': 'toggle button', 'index': 1}
        ease_in_value_box = [{'AXIdentifier': 'IDC_PIP_DESIGNER_EASE_SCALE'}, {'AXIdentifier': 'IDC_EASE_CTRL_SPINEDIT_EASE_IN'}]
        ease_in_value = [ease_in_value_box, {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field'}]
        ease_in_value_up = [ease_in_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP', 'AXRoleDescription': 'button'}]
        ease_in_value_down = [ease_in_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN', 'AXRoleDescription': 'button'}]
        ease_in_slider = {'AXIdentifier': 'IDC_EASE_CTRL_SLIDER_EASE_IN', 'AXRoleDescription': 'slider', 'index': 1}
        ease_out_checkbox = {'AXIdentifier': 'IDC_EASE_CTRL_CHECKBOX_EASE_OUT', 'AXRoleDescription': 'toggle button', 'index': 1}
        ease_out_value_box = [{'AXIdentifier': 'IDC_PIP_DESIGNER_EASE_SCALE'}, {'AXIdentifier': 'IDC_EASE_CTRL_SPINEDIT_EASE_OUT'}]
        ease_out_value = [ease_out_value_box, {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field'}]
        ease_out_value_up = [ease_out_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP', 'AXRoleDescription': 'button'}]
        ease_out_value_down = [ease_out_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN', 'AXRoleDescription': 'button'}]
        ease_out_slider = {'AXIdentifier': 'IDC_EASE_CTRL_SLIDER_EASE_OUT', 'AXRoleDescription': 'slider', 'index': 1}
    class opacity:
        opacity = {'AXIdentifier': 'IDC_PIP_DESIGNER_OBJECT_SETTING_OPACITY_TITLE', 'AXRoleDescription': 'text'} # hardcode_20v3303: _NS:152 > IDC_PIP_DESIGNER_OBJECT_SETTING_OPACITY_TITLE
        add_remove_current_keyframe = {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_ADDREMOVE_KEYFRAME', 'AXRoleDescription': 'button', 'index': 2}
        reset_keyframe = {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_RESET_PARAM_KEYFRAME', 'AXRoleDescription': 'button', 'index': 2}
        previous_keyframe = {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_PREVIOUS_KEYFRAME', 'AXRoleDescription': 'button', 'index': 2}
        next_keyframe = {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_NEXT_KEYFRAME', 'AXRoleDescription': 'button', 'index': 2}
        opacity_value_box = {'AXIdentifier': 'IDC_PIP_DESIGNER_SPINEDIT_OPACITY', 'AXRoleDescription': 'group'}
        opacity_value = [opacity_value_box, {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field'}]
        opacity_value_up = [opacity_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP', 'AXRoleDescription': 'button'}]
        opacity_value_down = [opacity_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN', 'AXRoleDescription': 'button'}]
        opacity_slider = {'AXIdentifier': 'IDC_PIP_DESIGNER_SLIDER_OPACITY', 'AXRoleDescription': 'slider'}
        blending_mode = {'AXIdentifier': 'IDC_PIP_DESIGNER_COMBOBOX_BLENDING_MODE', 'AXRoleDescription': 'button'}
        blending_mode_normal = {'AXValue': 'Normal', 'AXRole': 'AXStaticText'}
        blending_mode_overlay = {'AXValue': 'Overlay', 'AXRole': 'AXStaticText'}
        blending_mode_multiply = {'AXValue': 'Multiply', 'AXRole': 'AXStaticText'}
        blending_mode_screen = {'AXValue': 'Screen', 'AXRole': 'AXStaticText'}
        blending_mode_lighten = {'AXValue': 'Lighten', 'AXRole': 'AXStaticText'}
        blending_mode_darken = {'AXValue': 'Darken', 'AXRole': 'AXStaticText'}
        blending_mode_difference = {'AXValue': 'Difference', 'AXRole': 'AXStaticText'}
        blending_mode_hue = {'AXValue': 'Hue', 'AXRole': 'AXStaticText'}
    class rotation:
        rotation = {'AXIdentifier': 'IDC_PIP_DESIGNER_OBJECT_SETTING_ROTATION_TITLE', 'AXValue': 'Rotation', 'AXRoleDescription': 'text'} # hardcode_20v3303: _NS:193 > IDC_PIP_DESIGNER_OBJECT_SETTING_ROTATION_TITLE
        add_remove_current_keyframe = {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_ADDREMOVE_KEYFRAME','AXRoleDescription': 'button', 'index': 3}
        reset_keyframe = {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_RESET_PARAM_KEYFRAME', 'AXRoleDescription': 'button', 'index': 3}
        previous_keyframe = {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_PREVIOUS_KEYFRAME', 'AXRoleDescription': 'button', 'index': 3}
        next_keyframe = {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_NEXT_KEYFRAME', 'AXRoleDescription': 'button', 'index': 3}
        degree_value_box = {'AXIdentifier': 'IDC_PIP_DESIGNER_SPINEDIT_ROTATION', 'AXRoleDescription': 'group'}
        degree_value = [degree_value_box, {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field'}]
        degree_value_up = [degree_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP', 'AXRoleDescription': 'button'}]
        degree_value_down = [degree_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN', 'AXRoleDescription': 'button'}]
        ease_in_checkbox = {'AXIdentifier': 'IDC_EASE_CTRL_CHECKBOX_EASE_IN', 'AXRoleDescription': 'toggle button', 'index': 2}
        ease_in_value_box = [{'AXIdentifier': 'IDC_PIP_DESIGNER_EASE_ROTATION'}, {'AXIdentifier': 'IDC_EASE_CTRL_SPINEDIT_EASE_IN'}]
        ease_in_value = [ease_in_value_box, {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field'}]
        ease_in_value_up = [ease_in_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP', 'AXRoleDescription': 'button'}]
        ease_in_value_down = [ease_in_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN', 'AXRoleDescription': 'button'}]
        ease_in_slider = {'AXIdentifier': 'IDC_EASE_CTRL_SLIDER_EASE_IN', 'AXRoleDescription': 'slider', 'index': 2}
        ease_out_checkbox = {'AXIdentifier': 'IDC_EASE_CTRL_CHECKBOX_EASE_OUT', 'AXRoleDescription': 'toggle button', 'index': 2}
        ease_out_value_box = [{'AXIdentifier': 'IDC_PIP_DESIGNER_EASE_ROTATION'}, {'AXIdentifier': 'IDC_EASE_CTRL_SPINEDIT_EASE_OUT'}]
        ease_out_value = [ease_out_value_box, {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field'}]
        ease_out_value_up = [ease_out_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP', 'AXRoleDescription': 'button'}]
        ease_out_value_down = [ease_out_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN', 'AXRoleDescription': 'button'}]
        ease_out_slider = {'AXIdentifier': 'IDC_EASE_CTRL_SLIDER_EASE_OUT', 'AXRoleDescription': 'slider', 'index': 2}
class chromakey:
    chroma_key = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRoleDescription': 'disclosure triangle', 'index': 1}
    chromakey_checkbox = {'AXIdentifier': 'IDC_PIP_DESIGNER_CHECKBOX_APPLY_PROPERTY', 'AXRoleDescription': 'toggle button'}
    cutout_button = {'AXIdentifier': 'IDC_PIP_DESIGNER_BTN_AUTO_CUTOUT', 'AXRole': 'AXCheckBox'}
    bubble_cutout = {'AXRoleDescription': 'popover', 'AXRole': 'AXPopover'}
    chromakey_title = {'AXIdentifier': 'IDC_DESIGNER_TEXT_PROPERTY', 'AXValue': 'Cutout'}
    add_new_key = {'AXIdentifier': 'IDC_PIP_DESIGNER_BTN_CHROMAKEY_ADD', 'AXTitle': 'Add New Key'} # v20_3303: IDC_PIP_DESIGNER_CHROMAKEY_BTN_ADDKEY
    color_range_box = {'AXIdentifier': 'IDC_CHROMAKEY_SPINEDIT_COLOR_RANGE', 'AXRoleDescription': 'group'}
    color_range_value = [color_range_box, {'AXIdentifier': 'spinEditTextField'}]
    denoise_box = {'AXIdentifier': 'IDC_CHROMAKEY_SPINEDIT_DENOISE', 'AXRoleDescription': 'group'}
    denoise_value = [denoise_box, {'AXIdentifier': 'spinEditTextField'}]
    btn_dropper = {'AXIdentifier': 'IDC_CHROMAKEY_BTN_COLOR', 'AXRoleDescription': 'button'}
    btn_remove = {'AXIdentifier': 'IDC_CHROMAKEY_BTN_REMOVE', 'AXRoleDescription': 'button'}
class border:
    border = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRoleDescription': 'disclosure triangle',
                  'index': 2}
    border_checkbox = {'AXIdentifier': 'IDC_PIP_DESIGNER_CHECKBOX_APPLY_PROPERTY', 'AXRoleDescription': 'toggle button', 'index': 1}
    size_slider = {'AXIdentifier': 'IDC_PIP_DESIGNER_BORDER_SLIDER_SIZE', 'AXRoleDescription': 'slider'}
    size_value_box = {'AXIdentifier': 'IDC_PIP_DESIGNER_SPINEDIT_BORDER_SIZE', 'AXRoleDescription': 'group'}
    size_value = [size_value_box, {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field'}]
    size_title = {'AXIdentifier': 'IDC_PIP_DESIGNER_BORDER_SIZE_TITLE', 'AXValue': 'Size'} # hardcode_20v3303: _NS:15 > IDC_PIP_DESIGNER_BORDER_SIZE_TITLE
    size_value_up = [size_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP', 'AXRoleDescription': 'button'}]
    size_value_down = [size_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN', 'AXRoleDescription': 'button'}]
    blur_slider = {'AXIdentifier': 'IDC_PIP_DESIGNER_BORDER_SLIDER_BLUR', 'AXRoleDescription': 'slider'}
    blur_value_box = {'AXIdentifier': 'IDC_PIP_DESIGNER_SPINEDIT_BORDER_BLUR', 'AXRoleDescription': 'group'}
    blur_value = [blur_value_box, {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field'}]
    blur_title = {'AXIdentifier': 'IDC_PIP_DESIGNER_BORDER_BLUR_TITLE', 'AXValue': 'Blur'} # hardcode_20v3303: _NS:60 > IDC_PIP_DESIGNER_BORDER_BLUR_TITLE
    blur_value_up = [blur_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP', 'AXRoleDescription': 'button'}]
    blur_value_down = [blur_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN', 'AXRoleDescription': 'button'}]
    opacity_slider = {'AXIdentifier': 'IDC_PIP_DESIGNER_BORDER_SLIDER_OPACITY', 'AXRoleDescription': 'slider'}
    opacity_value_box = {'AXIdentifier': 'IDC_PIP_DESIGNER_SPINEDIT_BORDER_OPACITY', 'AXRoleDescription': 'group'}
    opacity_value = [opacity_value_box, {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field'}]
    opacity_title = {'AXIdentifier': 'IDC_PIP_DESIGNER_BORDER_OPACITY_TITLE', 'AXValue': 'Opacity'} # hardcode_20v3303: _NS:83 > IDC_PIP_DESIGNER_BORDER_OPACITY_TITLE
    opacity_value_up = [opacity_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP', 'AXRoleDescription': 'button'}]
    opacity_value_down = [opacity_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN', 'AXRoleDescription': 'button'}]
    fill_type = {'AXIdentifier': 'IDC_PIP_DESIGNER_BORDER_BTN_FILLTYPE', 'AXRoleDescription': 'button'}
    fill_type_uniform_color = {'AXRole': 'AXStaticText', 'AXValue': 'Solid Color'}
    uniform_color = {'AXIdentifier': 'IDC_PIP_DESIGNER_BORDER_BTN_UNICOLOR', 'AXRoleDescription': 'button'}
    uniform_color_close_button = {'AXRoleDescription': 'close button', 'AXSubrole': 'AXCloseButton'}
    red = {'AXIdentifier': 'red', 'AXRoleDescription': 'text field'}
    green = {'AXIdentifier': 'green', 'AXRoleDescription': 'text field'}
    blue = {'AXIdentifier': 'blue', 'AXRoleDescription': 'text field'}
    fill_type_2_color_gradient = {'AXRole': 'AXStaticText', 'AXValue': '2 Color Gradient'}
    begin_with = {'AXIdentifier': 'IDC_PIP_DESIGNER_BORDER_TWO_BTN_BEGINCOLOR', 'AXRoleDescription': 'button'}
    end_with = {'AXIdentifier': 'IDC_PIP_DESIGNER_BORDER_TWO_BTN_ENDCOLOR', 'AXRoleDescription': 'button'}
    fill_type_4_color_gradient = {'AXRole': 'AXStaticText', 'AXValue': '4 Color Gradient'}
    four_color_gradient = {'AXIdentifier': 'fourColorGradient', 'AXRoleDescription': 'group'}
class shadow:
    shadow = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRoleDescription': 'disclosure triangle',
              'index': 3}
    shadow_checkbox = {'AXIdentifier': 'IDC_PIP_DESIGNER_CHECKBOX_APPLY_PROPERTY', 'AXRoleDescription': 'toggle button', 'index': 2}
    apply_shadow_to = {'AXIdentifier': 'IDC_PIP_DESIGNER_COMBOBOX_SHADOW_TYPE', 'AXRoleDescription': 'button'}
    apply_shadow_to_object_and_border = {'AXRole': 'AXStaticText', 'AXValue': 'Object and Border'}
    apply_shadow_to_object_only = {'AXRole': 'AXStaticText', 'AXValue': 'Object Only'}
    apply_shadow_to_border_only = {'AXRole': 'AXStaticText', 'AXValue': 'Border Only'}
    distance_slider = {'AXIdentifier': 'IDC_PIP_DESIGNER_SHADOW_SLIDER_DISTANCE', 'AXRoleDescription': 'slider'}
    distance_value_box = {'AXIdentifier': 'IDC_PIP_DESIGNER_SHADOW_SLIDER_DISTANCE', 'AXRoleDescription': 'group'}
    distance_value = [distance_value_box, {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field'}]
    distance_value_up = [distance_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP', 'AXRoleDescription': 'button'}]
    distance_value_down = [distance_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN', 'AXRoleDescription': 'button'}]
    distance_title = {'AXIdentifier': 'IDC_PIP_DESIGNER_SHADOW_DISTANCE_TITLE', 'AXValue': 'Distance'} # hardcode_20v3303: _NS:170 > IDC_PIP_DESIGNER_SHADOW_DISTANCE_TITLE
    blur_slider = {'AXIdentifier': 'IDC_PIP_DESIGNER_SHADOW_SLIDER_BLUR', 'AXRoleDescription': 'slider'}
    blur_value_box = {'AXIdentifier': 'IDC_PIP_DESIGNER_SPINEDIT_SHADOW_BLUR', 'AXRoleDescription': 'group'}
    blur_value = [blur_value_box, {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field'}]
    blur_value_up = [blur_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP', 'AXRoleDescription': 'button'}]
    blur_value_down = [blur_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN', 'AXRoleDescription': 'button'}]
    blur_title = {'AXIdentifier': 'IDC_PIP_DESIGNER_SHADOW_BLUR_TITLE', 'AXValue': 'Blur'} # hardcode_20v3303: _NS:177 > IDC_PIP_DESIGNER_SHADOW_BLUR_TITLE
    opacity_slider = {'AXIdentifier': 'IDC_PIP_DESIGNER_SHADOW_SLIDER_OPACITY', 'AXRoleDescription': 'slider'}
    opacity_value_box = {'AXIdentifier': 'IDC_PIP_DESIGNER_SPINEDIT_SHADOW_OPACITY', 'AXRoleDescription': 'group'}
    opacity_value = [opacity_value_box, {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field'}]
    opacity_value_up = [opacity_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP', 'AXRoleDescription': 'button'}]
    opacity_value_down = [opacity_value_box, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN', 'AXRoleDescription': 'button'}]
    opacity_title = {'AXIdentifier': 'IDC_PIP_DESIGNER_SHADOW_OPACITY_TITLE', 'AXValue': 'Opacity'} # hardcode_20v3303: _NS:184 > IDC_PIP_DESIGNER_SHADOW_OPACITY_TITLE
    select_color = {'AXIdentifier': 'IDC_PIP_DESIGNER_SHADOW_BTN_SHADOWCOLOR', 'AXRoleDescription': 'button'}
    red = {'AXIdentifier': 'red', 'AXRoleDescription': 'text field'}
    green = {'AXIdentifier': 'green', 'AXRoleDescription': 'text field'}
    blue = {'AXIdentifier': 'blue', 'AXRoleDescription': 'text field'}
    select_color_close = {'AXRole': 'AXButton', 'AXRoleDescription': 'close button'}
class flip:
    flip = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRoleDescription': 'disclosure triangle',
              'index': 4}
    flip_title = {'AXIdentifier': 'IDC_DESIGNER_TEXT_PROPERTY', 'AXValue': 'Flip'}
    flip_checkbox = {'AXIdentifier': 'IDC_PIP_DESIGNER_CHECKBOX_APPLY_PROPERTY', 'AXRoleDescription': 'toggle button', 'index': 3}
    upside_down = {'AXIdentifier': 'IDC_PIP_DESIGNER_FLIP_BTN_VERTICAL', 'AXTitle': 'Upside down'}
    left_to_right = {'AXIdentifier': 'IDC_PIP_DESIGNER_FLIP_BTN_HORIZONAL', 'AXTitle': 'Left to right'}
class fades:
    fades = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRoleDescription': 'disclosure triangle',
            'index': 4}
    fades_express = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRoleDescription': 'disclosure triangle',
            'index': 4}
    fades_checkbox = {'AXIdentifier': 'IDC_PIP_DESIGNER_CHECKBOX_APPLY_PROPERTY', 'AXRoleDescription': 'toggle button', 'index': 3}
    fades_express_checkbox = {'AXIdentifier': 'IDC_PIP_DESIGNER_CHECKBOX_APPLY_PROPERTY', 'AXRoleDescription': 'toggle button', 'index': 3}
    enable_fade_in = {'AXIdentifier': 'IDC_PIP_DESIGNER_FADE_BTN_IN', 'AXTitle': 'Enable fade-in'}
    enable_fade_out = {'AXIdentifier': 'IDC_PIP_DESIGNER_BTN_FADE_OUT', 'AXTitle': 'Enable fade-out'}

viewer_ratio = {'AXIdentifier': 'IDC_PIP_DESIGNER_COMBOBOX_ZOOM_LEVEL', 'AXRoleDescription': 'button'}
preview_play = {'AXIdentifier': 'IDC_PIP_DESIGNER_BUTTON_PLAY', 'AXRoleDescription': 'button'}
preview_pause = {'AXIdentifier': 'IDC_PIP_DESIGNER_BUTTON_PAUSE', 'AXRoleDescription': 'button'}
preview_stop = {'AXIdentifier': 'IDC_PIP_DESIGNER_BUTTON_STOP', 'AXRoleDescription': 'button'}
preview_previous_frame = {'AXIdentifier': 'IDC_PIP_DESIGNER_BUTTON_PREVFRAME', 'AXRoleDescription': 'button'}
preview_next_frame = {'AXIdentifier': 'IDC_PIP_DESIGNER_BUTTON_NEXTFRAME', 'AXRoleDescription': 'button'}
preview_fast_forward = {'AXIdentifier': 'IDC_PIP_DESIGNER_BUTTON_FASTFORWARD', 'AXRoleDescription': 'button'}
toggle_grid_line_on_off = {'AXIdentifier': 'IDC_PIP_DESIGNER_BUTTON_GRID_LINE_MENU', 'AXRoleDescription': 'button'}
snap_to_reference_line = {'AXIdentifier': 'IDM_PIP_DESIGNER_GRID_LINE_MENU_SNAP_REFERENCE_LINE', 'AXTitle': 'Snap to Reference Lines'} # hardcode_20v3303: _NS:9 > IDM_PIP_DESIGNER_GRID_LINE_MENU_SNAP_REFERENCE_LINE
grid_lines = {'AXIdentifier': 'IDM_PIP_DESIGNER_GRID_LINE_MENU_GRID_LINES', 'AXTitle': 'Grid Lines'} # hardcode_20v3303: _NS:27 > IDM_PIP_DESIGNER_GRID_LINE_MENU_GRID_LINES
clip_timecode = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_CLIP_TIMECODE', 'AXRoleDescription': 'button'}
video_timecode = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_MOVIE_TIMECODE', 'AXRoleDescription': 'button'}
display_timeline_mode = {'AXIdentifier': 'IDC_PIP_DESIGNER_BUTTON_SHOW_TIMELINE', 'AXRoleDescription': 'button'}
hide_timeline_mode = {'AXIdentifier': 'IDC_PIP_DESIGNER_BUTTON_HIDE_TIMELINE', 'AXRoleDescription': 'button'}
keyframe_scrollbar = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_VERTICAL_SCROLLVIEW_SCROLLBAR', 'AXRoleDescription': 'scroll bar'} # hardcode_20v3033: _NS:115 > IDC_SIMPLE_TIMELINE_TRACK_VERTICAL_SCROLLVIEW_SCROLLBAR

scroller_removed_scroll_view = {'AXIdentifier': 'IDC_RULER_SCROLLAREA', 'AXRole': 'AXScrollArea'}

class simple_position_track:
    add_remove_current_keyframe = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_ADD_REMOVE_KEYFRAME'}
    previous_keyframe = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_PREV_KEYFRAME'}
    next_keyframe = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_NEXT_KEYFRAME'}
class simple_scale_track:
    add_remove_current_keyframe = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_ADD_REMOVE_KEYFRAME', 'index': 1}
    previous_keyframe = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_PREV_KEYFRAME', 'index': 1}
    next_keyframe = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_NEXT_KEYFRAME', 'index': 1}
class simple_opacity_track:
    add_remove_current_keyframe = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_ADD_REMOVE_KEYFRAME', 'index': 2}
    previous_keyframe = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_PREV_KEYFRAME', 'index': 2}
    next_keyframe = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_NEXT_KEYFRAME', 'index': 2}
class simple_rotation_track:
    add_remove_current_keyframe = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_ADD_REMOVE_KEYFRAME', 'index': 3}
    previous_keyframe = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_PREV_KEYFRAME', 'index': 3}
    next_keyframe = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_NEXT_KEYFRAME', 'index': 3}
class simple_freeform_track:
    add_remove_current_keyframe = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_ADD_REMOVE_KEYFRAME', 'index': 4}
    previous_keyframe = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_PREV_KEYFRAME', 'index': 4}
    next_keyframe = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_NEXT_KEYFRAME', 'index': 4}

ok_button = {'AXIdentifier': 'IDC_PIP_DESIGNER_BUTTON_OK', 'AXTitle': 'OK'}
save_as_button = {'AXIdentifier': 'IDC_PIP_DESIGNER_BUTTON_SAVE', 'AXTitle': 'Save As'}
save_as_template_dialog = {'AXIdentifier': 'IDC_SAVE_TEMPLATE_WINDOW', 'AXTitle': 'Save as Template'}
save_as_textfield = {'AXIdentifier': 'IDC_SAVE_TEMPLATE_EDIT_TEMPLATE_NAME'}
save_as_ok = {'AXIdentifier': 'IDC_SAVE_TEMPLATE_BTN_OK'}
save_as_cancel_btn = {'AXIdentifier': 'IDC_SAVE_TEMPLATE_BTN_CANCEL', 'AXRole': 'AXButton'}
cancel_button = {'AXIdentifier': 'IDC_PIP_DESIGNER_BUTTON_CANCEL'}
cancel_dialog = {'AXIdentifier': 'IDD_CLALERT', 'AXTitle': 'CyberLink PowerDirector', 'AXRoleDescription': 'dialog'}
cancel_dialog_cancel = {'AXIdentifier': 'IDC_CLALERT_BUTTON_2'}
cancel_dialog_no = {'AXIdentifier': 'IDC_CLALERT_BUTTON_1'}
cancel_dialog_yes = {'AXIdentifier': 'IDC_CLALERT_BUTTON_0'}
save_as_slider = {'AXIdentifier': 'IDC_SAVE_TEMPLATE_SLIDER_MARK_FRAME', 'AXRoleDescription': 'slider'}
share_button = {'AXIdentifier': 'IDC_PIP_DESIGNER_BUTTON_SHARE', 'AXTitle': 'Share'}
auto_sign_in_to_DZ = {'AXIdentifier': 'IDC_STATIC_DIRECTORZONE_AUTOLOGIN', 'AXTitle': 'Auto sign in to DirectorZone'}
log_in_no = {'AXIdentifier': 'IDC_SSO_BUTTON_NO', 'AXTitle': 'No'}
log_in_yes = {'AXIdentifier': 'IDC_SSO_BUTTON_YES', 'AXTitle': 'Yes'}
remove_dialog = [cancel_dialog,  {'AXIdentifier': 'IDC_CLALERT_MESSAGE', 'AXValue': 'Are you sure you want to delete the selected item?'}]
remove_dialog_ok = [cancel_dialog, {'AXIdentifier': 'IDC_CLALERT_BUTTON_0'}]

class upload:
    upload_to_box = {'AXIdentifier': 'IDC_UPLOADTEMPLATE_HOWLOADTO', 'AXRoleDescription': 'button'}
    cloud_and_dz = {'AXValue': 'CyberLink Cloud and DirectorZone', 'AXRole': 'AXStaticText'}
    cloud = {'AXValue': 'CyberLink Cloud', 'AXRole': 'AXStaticText'}
    dz = {'AXValue': 'DirectorZone', 'AXRole': 'AXStaticText'}
    style = {'AXIdentifier': 'IDC_UPLOADTEMPLATE_STYLE', 'AXRoleDescription': 'button'}
    type = {'AXIdentifier': 'IDC_UPLOADTEMPLATE_TITLE', 'AXRoleDescription': 'button'}
    tags = {'AXIdentifier': 'IDC_UPLOADTEMPLATE_TAGS', 'AXRoleDescription': 'text field'}
    collection = {'AXIdentifier': 'IDC_UPLOADTEMPLATE_COLLECTION', 'AXRoleDescription': 'text field'}
    description = {'AXIdentifier': 'IDC_UPLOADTEMPLATE_DESCRIPTION', 'AXRoleDescription': 'text field'}
    next_btn = {'AXIdentifier': 'IDC_UPLOADTEMPLATE_NEXT', 'AXTitle': 'Next'}
    confirm_disclaimer = {'AXIdentifier': 'IDC_UPLOADTEMPLATE_CONFIRM', 'AXRoleDescription': 'toggle button'}
    finish = {'AXIdentifier': 'IDC_UPLOADTEMPLATE_FINISH', 'AXTitle': 'Finish'}
express = {'AXIdentifier': 'IDC_PIP_DESIGNER_BUTTON_BASIC_MODE', 'AXTitle': 'Express'}
advanced = {'AXIdentifier': 'IDC_PIP_DESIGNER_BUTTON_ADVANCED_MODE', 'AXTitle': 'Advanced'}
maximize_btn = [{'AXIdentifier': 'PIP_DESIGNER_DLG'}, {'AXRoleDescription': 'zoom button', 'AXRole': 'AXButton', 'index': 0}]
close_btn = [{'AXIdentifier': 'PIP_DESIGNER_DLG'}, {'AXRoleDescription': 'close button', 'AXRole': 'AXButton', 'index': 0}]
btn_zoom_in = {'AXIdentifier': 'IDC_PIP_DESIGNER_BUTTON_ZOOM_IN', 'AXRole': 'AXButton'}
btn_zoom_out = {'AXIdentifier': 'IDC_PIP_DESIGNER_BUTTON_ZOOM_OUT', 'AXRole': 'AXButton'}
btn_flip = {'AXIdentifier': 'IDC_PIP_DESIGNER_BUTTON_FLIP', 'AXRole': 'AXButton'}
btn_timeline_zoom_in = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_ZOOM_IN', 'AXRole': 'AXButton'}
btn_timeline_zoom_out = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_ZOOM_OUT', 'AXRole': 'AXButton'}
# btn_timeline_indicator = {'AXIdentifier': '_NS:240', 'AXRole': 'AXImage'} # unused
timeline_scrollarea = {'AXIdentifier': 'IDC_RULER_SCROLLAREA', 'AXRole': 'AXScrollArea'}
class express_mode:
    btn_object_setting = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRole': 'AXDisclosureTriangle'}
    edittext_hex = {'AXIdentifier': 'hex', 'AXRole': 'AXTextField'}
class timeline_context_menu:
    remove_keyframe = {'AXIdentifier': 'onAddRemoveKeyframe:', 'AXRole': 'AXMenuItem'}
    remove_all_keyframe = {'AXIdentifier': 'onRemoveAllKeyframe:', 'AXRole': 'AXMenuItem'}
    duplicate_previous_keyframe = {'AXIdentifier': 'onDuplicatePrevKeyframe:', 'AXRole': 'AXMenuItem'}
    duplicate_next_keyframe = {'AXIdentifier': 'onDuplicateNextKeyframe:', 'AXRole': 'AXMenuItem'}
    ease_in = {'AXIdentifier': 'onEaseIn:', 'AXRole': 'AXMenuItem'}
    ease_out = {'AXIdentifier': 'onEaseOut:', 'AXRole': 'AXMenuItem'}

# motion tab
tab_motion = {'AXIdentifier': 'IDC_PIP_DESIGNER_BUTTON_MOTION', 'AXRole': 'AXButton'}

# animation tab
tab_animation = {'AXIdentifier': 'IDC_PIP_DESIGNER_BUTTON_EFFECT', 'AXRole': 'AXButton'}

# properties tab
tab_properties = {'AXIdentifier': 'IDC_PIP_DESIGNER_BUTTON_PROPERTIES', 'AXRole': 'AXButton'}

class path:
    # triangle button
    btn_path = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRoleDescription': 'disclosure triangle',
                 'index': 0}
    path_title = {'AXIdentifier': 'IDC_DESIGNER_TEXT_PROPERTY', 'AXValue': 'Path'}

    # path dropdown menu (combobox)
    cbx_path_menu = {'AXIdentifier': 'IDC_PIP_DESIGNER_MOTIONPATH_COMBOBOX_FILTER', 'AXRole': 'AXButton'}
    option_all = {'AXRole': 'AXStaticText', 'AXValue': 'All Paths'}
    option_default = {'AXRole': 'AXStaticText', 'AXValue': 'Default Paths'}
    option_custom = {'AXRole': 'AXStaticText', 'AXValue': 'Custom Paths'}

    # Default path template
    path_template = {'AXIdentifier': 'motionPathThumbCVI', 'AXRole': 'AXGroup', 'get_all': True}

    # Save custom path button
    btn_custom_path = {'AXIdentifier': 'IDC_PIP_DESIGNER_MOTIONPATH_BTN_SAVE_MOTION_SCRIPT', 'AXRole': 'AXButton'}

    # Outline Row (for snapshot)
    area_path_outline_row = {'AXRoleDescription': 'outline row', 'AXRole': 'AXRow', 'index': 1}

class in_animation:
    # triangle button
    btn_in_animation = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRoleDescription': 'disclosure triangle',
                 'index': 0}

    animation_title = {'AXIdentifier': 'IDC_DESIGNER_TEXT_PROPERTY', 'AXValue': 'In Animation'}

    # in animation > Effect dropdown menu (combobox)
    cbx_effect_menu = {'AXIdentifier': 'IDC_PIP_DESIGNER_IN_EFFECT_FILTER', 'AXRole': 'AXButton'}

    # Default Animation template
    animation_template = {'AXIdentifier': 'PipEffectCollectionViewItem', 'AXRole': 'AXGroup', 'get_all': True}

class out_animation:
    # triangle button
    btn_out_animation = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRoleDescription': 'disclosure triangle',
                 'index': 1}

    animation_title = {'AXIdentifier': 'IDC_DESIGNER_TEXT_PROPERTY', 'AXValue': 'Out Animation'}

class loop_animation:
    # triangle button
    btn_loop_animation = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRoleDescription': 'disclosure triangle',
                 'index': 2}

    animation_title = {'AXIdentifier': 'IDC_DESIGNER_TEXT_PROPERTY', 'AXValue': 'Loop Animation'}

class motion_blur:
    # triangle button
    btn_motion_blur = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRoleDescription': 'disclosure triangle',
                 'index': 1}

    # checkbox
    checkbox = {'AXIdentifier': 'IDC_PIP_DESIGNER_CHECKBOX_APPLY_PROPERTY', 'AXRole': 'AXCheckBox', 'AXRoleDescription': 'toggle button'}

    # length
    editbox_parent = {'AXIdentifier': 'IDC_PIP_DESIGNER_MOTIONBLUR_SPINEDIT_STRENGTH', 'AXRole': 'AXGroup'}
    text_field_length = [editbox_parent, {'AXIdentifier': 'spinEditTextField', 'AXRole': 'AXTextField'}]
    arrow_up_btn_length = [editbox_parent, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP'}]
    arrow_down_btn_length = [editbox_parent, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN'}]
    slider_length = {'AXIdentifier': 'IDC_PIP_DESIGNER_MOTIONBLUR_SLIDER_STRENGTH', 'AXRole': 'AXSlider'}
    indicator_length = [slider_length, {'AXRole': 'AXValueIndicator'}]

    # density
    editbox_parent_density = {'AXIdentifier': 'IDC_PIP_DESIGNER_MOTIONBLUR_SPINEDIT_FRAME_SAMPLES', 'AXRole': 'AXGroup'}
    text_field_density = [editbox_parent_density, {'AXIdentifier': 'spinEditTextField', 'AXRole': 'AXTextField'}]
    arrow_up_btn_density = [editbox_parent_density, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP'}]
    arrow_down_btn_density = [editbox_parent_density, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN'}]
    slider_density = {'AXIdentifier': 'IDC_PIP_DESIGNER_MOTIONBLUR_SLIDER_FRAME_SAMPLES', 'AXRole': 'AXSlider'}
    indicator_density = [slider_density, {'AXRole': 'AXValueIndicator'}]

# Simple track > Right Click Menu
# Linear
option_linear = {'AXIdentifier': 'Linear', 'AXRole': 'AXMenuItem'}
# Hold
option_hold = {'AXIdentifier': 'Hold', 'AXRole': 'AXMenuItem'}
# Ease In
option_ease_in = {'AXIdentifier': 'onEaseIn:', 'AXRole': 'AXMenuItem'}
# Ease Out
option_ease_out = {'AXIdentifier': 'onEaseOut:', 'AXRole': 'AXMenuItem'}

# Image track title
image_track = {'AXIdentifier': 'IDC_SIMPLETIMELINE_TRACKOBJECT_TEXTFIELD_TITLE', 'AXRole': 'AXStaticText'}

# Image track > Right Click Menu
# Loop Playback
option_loop = {'AXIdentifier': 'onAnimationLoop', 'AXRole': 'AXMenuItem'}
# Freeze on Last Frame
option_last = {'AXIdentifier': 'onAnimationLastFrame', 'AXRole': 'AXMenuItem'}
# Freeze on First Frame
option_first = {'AXIdentifier': 'onAnimationFirstFrame', 'AXRole': 'AXMenuItem'}
# Stop Playback
option_stop = {'AXIdentifier': 'onAnimationStop', 'AXRole': 'AXMenuItem'}