from .base import AdjustSet, KEComboSet

designer_window = {'AXIdentifier': 'IDC_IDC_SHAPE_DESIGNER_WINDOW', 'AXRoleDescription': 'dialog', 'AXRole': 'AXWindow'}
btn_zoom = [designer_window, {'AXRoleDescription': 'zoom button'}]
btn_close = [designer_window, {'AXRoleDescription': 'close button'}]
btn_undo = [designer_window, {'AXIdentifier': 'IDC_IDC_SHAPE_DESIGNER_UNDO_BTN'}]
btn_redo = [designer_window, {'AXIdentifier': 'IDC_IDC_SHAPE_DESIGNER_REDO_BTN'}]
btn_zoom_in = [designer_window, {'AXIdentifier': 'IDC_IDC_SHAPE_DESIGNER_ZOOM_IN_BTN'}]
btn_zoom_out = [designer_window, {'AXIdentifier': 'IDC_IDC_SHAPE_DESIGNER_ZOOM_OUT_BTN'}]
cbx_viewer_zoom = [designer_window, {'AXIdentifier': 'IDC_IDC_SHAPE_DESIGNER_ZOOM_LEVEL_BTN', 'AXRole': 'AXButton'}]
timecode = [designer_window, {'AXIdentifier': 'spinTimeEditTextField', 'AXRoleDescription': 'text'}]

# For Left panel setting
properties_tab = [designer_window, {'AXTitle': 'Properties', 'AXRole': 'AXButton'}]
keyframe_tab = [designer_window, {'AXTitle': 'Keyframe', 'AXRole': 'AXButton'}]
left_panel_scroll_bar = [{'AXIdentifier': 'IDC_PIP_DESIGNER_SCROLLBAR_Y'}, {'AXRole': 'AXValueIndicator', 'AXRoleDescription': 'value indicator'}]

outline_row = [designer_window, {'AXRole': 'AXRow', 'AXRoleDescription': 'outline row'}]
preset_collection_item = {'AXIdentifier': 'TitleCharPresetCollectionViewItem', 'AXRole': 'AXGroup'}
# Left Panel region (Properties + Keyframe) (Height value > designer window's height)
left_panel_simple_container_outline_view = {'AXIdentifier': 'IDC_PIP_DESIGNER_OUTLINEVIEW_CONTAINER', 'AXRole': 'AXOutline'}

# Left Panel region (Properties + Keyframe), only for snapshot (Height value = 671)
left_panel_scroll_view = {'AXIdentifier': 'IDC_PIP_DESIGNER_SCROLLVIEW_CONTAINER', 'AXRole': 'AXScrollArea'}

# Left Panel > Properties > Outline view for unfold the parameter setting case
left_panel_outline_view_parameter_setting = [left_panel_simple_container_outline_view, {'AXRole': 'AXRow', 'AXAlternateUIVisible': False, "recursive": True}]

# Save / Cancel / OK
btn_save_as = [designer_window, {'AXIdentifier': 'IDC_SHAPE_DESIGNER_BUTTON_SAVE'}]
btn_cancel = [designer_window, {'AXIdentifier': 'IDC_IDC_SHAPE_DESIGNER_BUTTON_CANCEL'}]
btn_ok = [designer_window, {'AXIdentifier': 'IDC_SHAPE_DESIGNER_BUTTON_OK'}]

# Checkbox (Only show the selected track)
show_the_selected_track = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_BUTTON_SHOWSELTRACK', 'AXTitle': 'Only show the selected track'}

class save_template_dialog:
    main = {'AXIdentifier': 'IDC_SAVE_TEMPLATE_WINDOW', 'AXTitle': 'Save as Template'}
    edittext_template_name = {'AXIdentifier': 'IDC_SAVE_TEMPLATE_EDIT_TEMPLATE_NAME'}
    slider_mark_frame = {'AXIdentifier': 'IDC_SAVE_TEMPLATE_SLIDER_MARK_FRAME'}
    btn_cancel = {'AXIdentifier': 'IDC_SAVE_TEMPLATE_BTN_CANCEL', 'AXTitle': 'Cancel'}
    btn_ok = {'AXIdentifier': 'IDC_SAVE_TEMPLATE_BTN_OK', 'AXTitle': 'OK'}

class shape_type:
    # triangle button
    btn_shape_type = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRoleDescription': 'disclosure triangle'}
    #scroll_bar = [designer_window, {'AXIdentifier': '_NS:23', 'AXRole': 'AXScrollArea'}, {'AXRole': 'AXScrollBar', 'AXRoleDescription': 'scroll bar'}]
    scroll_bar = [designer_window, {'AXIdentifier': 'IDC_SHAPE_DESIGNER_SHAPE_TYPE_V_SCROLLER', 'AXRole': 'AXScrollBar'}]
    shape_type_collection_view = [designer_window, {'AXIdentifier': 'IDC_SHAPE_DESIGNER_SHAPE_TYPE_COLLECTIONVIEW', 'AXRole': 'AXList'}]
    preset_collection_item = [shape_type_collection_view, {'AXIdentifier': 'TitleCharPresetCollectionViewItem', 'AXRole': 'AXGroup'}]

class shape_preset:
    # triangle button
    btn_shape_preset = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRoleDescription': 'disclosure triangle', 'index': 1}

    # (outline row)  for menu
    setting_outline_view_menu = [left_panel_simple_container_outline_view, {'AXRole': 'AXRow', 'AXAlternateUIVisible': True, 'index': 1, "recursive": False}]
    preset_collection_item = [left_panel_outline_view_parameter_setting,{'AXIdentifier': 'TitleCharPresetCollectionViewItem', 'AXRole': 'AXGroup', "recursive": True}]

class shape_fill:
    # triangle button
    btn_shape_fill = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRoleDescription': 'disclosure triangle', 'index': 2}

    # (outline row)  for menu
    setting_outline_view_menu = [left_panel_simple_container_outline_view, {'AXRole': 'AXRow', 'AXAlternateUIVisible': True, 'index': 2, "recursive": False}]
    checkbox = [setting_outline_view_menu, {'AXIdentifier': 'IDC_PIP_DESIGNER_CHECKBOX_APPLY_PROPERTY', 'AXRole': 'AXCheckBox'}]

    # for blur
    text_field_blur = {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field', 'AXRole': 'AXTextField'}
    slider_blur = {'AXHelp': 'Set the blur level'}
    arrow_up_btn_blur = {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP'}
    arrow_down_btn_blur = {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN'}

    # for opacity
    text_field_opacity = {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field', 'AXRole': 'AXTextField', 'index': 1}
    slider_opacity = {'AXHelp': 'Set the opacity level'}
    arrow_up_btn_opacity = {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP', 'index': 1}
    arrow_down_btn_opacity = {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN', 'index': 1}

    fill_type_dropdown_menu = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_BORDER_BTN_FILLTYPE', 'AXRole': 'AXButton'}
    fill_type_Uniform = {'AXValue': 'Uniform Color', 'AXRole': 'AXStaticText'}
    fill_type_Gradient = {'AXValue': '2 Color Gradient', 'AXRole': 'AXStaticText'}
    fill_type_uniform_color = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_BORDER_BTN_UNICOLOR', 'AXRole': 'AXButton'}
    fill_type_gradient_begin_color = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_BORDER_TWO_BTN_BEGINCOLOR', 'AXRole': 'AXButton'}
    fill_type_gradient_end_color = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_BORDER_TWO_BTN_ENDCOLOR', 'AXRole': 'AXButton'}

class shape_outline:
    # triangle button
    btn_shape_outline = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRoleDescription': 'disclosure triangle',
                         'index': 3}

    # (outline row)  for menu
    setting_outline_view_menu = [left_panel_simple_container_outline_view, {'AXRole': 'AXRow', 'AXAlternateUIVisible': True, 'index': 3, "recursive": False}]

    checkbox = [setting_outline_view_menu, {'AXIdentifier': 'IDC_PIP_DESIGNER_CHECKBOX_APPLY_PROPERTY', 'AXRole': 'AXCheckBox'}]

    # Line type
    line_type_1 = [left_panel_outline_view_parameter_setting, {'AXIdentifier': 'IDC_SHAPE_DESIGNER_LINE_TYPE_BTN_1'}]
    line_type_2 = [left_panel_outline_view_parameter_setting, {'AXIdentifier': 'IDC_SHAPE_DESIGNER_LINE_TYPE_BTN_2'}]
    line_type_3 = [left_panel_outline_view_parameter_setting, {'AXIdentifier': 'IDC_SHAPE_DESIGNER_LINE_TYPE_BTN_3'}]

    # Cap & join type
    join_type_menu = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_CAP_JOIN_TYPE_COMBOBOX', 'AXRole': 'AXButton'} # v20.3.3630: _NS: 87
    join_type_round = {'AXValue': 'Round', 'AXRole': 'AXStaticText'}
    join_type_flat = {'AXValue': 'Flat', 'AXRole': 'AXStaticText'}

    # Begin arrow type / Begin arrow size / End arrow type / End arrow size
    # Only index value are different
    arrow_begin_type = [left_panel_outline_view_parameter_setting, {'AXIdentifier': 'IDC_PIP_DESIGNER_CHROMAKEY_BTN_ADDKEY', 'get_all': True}]

    # Size
    text_field_size = {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field', 'AXRole': 'AXTextField', 'index': 0}
    slider_size = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_OUTLINE_SIZE_SLIDER', 'AXRole': 'AXSlider'} # v20.3.3630: _NS: 424
    arrow_up_btn_size = {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP'}
    arrow_down_btn_size = {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN'}

    # Blur
    text_field_blur = {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field', 'AXRole': 'AXTextField', 'index': 1}
    slider_blur = {'AXHelp': 'Set the blur level'}
    arrow_up_btn_blur = {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP', 'index': 1}
    arrow_down_btn_blur = {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN', 'index': 1}

    # Opacity
    text_field_opacity = {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field', 'AXRole': 'AXTextField', 'index': 2}
    slider_opacity = {'AXHelp': 'Set the opacity level'}
    arrow_up_btn_opacity = {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP', 'index': 2}
    arrow_down_btn_opacity = {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN', 'index': 2}

    # Fill type
    fill_type_dropdown_menu = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_OUTLINE_BTN_FILLTYPE', 'AXRole': 'AXButton'}
    fill_type_Uniform = {'AXValue': 'Uniform Color', 'AXRole': 'AXStaticText'}
    fill_type_Gradient = {'AXValue': '2 Color Gradient', 'AXRole': 'AXStaticText'}
    fill_type_uniform_color = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_OUTLINE_BTN_UNICOLOR', 'AXRole': 'AXButton'}
    fill_type_gradient_begin_color = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_OUTLINE_TWO_BTN_BEGINCOLOR', 'AXRole': 'AXButton'}
    fill_type_gradient_end_color = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_OUTLINE_TWO_BTN_ENDCOLOR', 'AXRole': 'AXButton'}
class shadow:
    # triangle button
    btn_shadow = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRoleDescription': 'disclosure triangle',
                  'index': 4}

    # (outline row)  for menu
    setting_outline_view_menu = [left_panel_simple_container_outline_view, {'AXRole': 'AXRow', 'AXAlternateUIVisible': True, 'index': 4, "recursive": False}]

    checkbox = [setting_outline_view_menu, {'AXIdentifier': 'IDC_PIP_DESIGNER_CHECKBOX_APPLY_PROPERTY', 'AXRole': 'AXCheckBox'}]

    # Apply shadow to
    apply_shadow_dropdown_menu = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_SHADOW_BTN_APPLYTO', 'AXRole': 'AXButton'} # v20.3.3630:_NS:135
    shadow_type_both = {'AXValue': 'Object and Outline', 'AXRole': 'AXStaticText'}
    shadow_type_outline = {'AXValue': 'Outline Only', 'AXRole': 'AXStaticText'}
    shadow_type_object = {'AXValue': 'Object Only', 'AXRole': 'AXStaticText'}

    # Distance
    text_field_distance = {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field', 'AXRole': 'AXTextField', 'index': 0}
    slider_distance = {'AXHelp': 'Set the shadow distance'}
    arrow_up_btn_distance = {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP'}
    arrow_down_btn_distance = {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN'}

    # Blur
    text_field_blur = {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field', 'AXRole': 'AXTextField', 'index': 1}
    slider_blur = {'AXHelp': 'Set the blur level of the shadow'}
    arrow_up_btn_blur = {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP', 'index': 1}
    arrow_down_btn_blur = {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN', 'index': 1}

    # Opacity
    text_field_opacity = {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field', 'AXRole': 'AXTextField', 'index': 2}
    slider_opacity = {'AXHelp': 'Set the opacity level of the shadow'}
    arrow_up_btn_opacity = {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP', 'index': 2}
    arrow_down_btn_opacity = {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN', 'index': 2}

    # Fill shadow
    checkbox_fill_shadow = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_FILL_SHADOW_CHECKBOX', 'AXRole': 'AXCheckBox'} # v20.3.3630:_NS:31
    fill_shadow_custom_color = {'AXIdentifier': 'IDC_PIP_DESIGNER_SHADOW_BTN_SHADOWCOLOR', 'AXRole': 'AXButton'}

    # Shadow direction
    text_field_shadow_direction = {'AXIdentifier': 'spinEditTextField', 'AXRoleDescription': 'text field', 'AXRole': 'AXTextField', 'index': 3}
    arrow_up_btn_shadow_direction = {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP', 'index': 3}
    arrow_down_btn_shadow_direction = {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN', 'index': 3}

class title:
    # triangle button
    btn_title = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey', 'AXRoleDescription': 'disclosure triangle',
                 'index': 5}

    # title text field
    txt_field = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_TITLE_TEXTFIELD', 'AXRole': 'AXTextField'} # v20.3.3630:_NS:328

    # title font cbx menu
    font_cbx_menu = {'AXIdentifier': 'IDC_COMBOBOX_CELL', 'AXRole': 'AXComboBox'}  # v20.3.3630:_NS:65
    font_type_triangle_button = [font_cbx_menu, {'AXRole': 'AXButton'}]

    # title font size
    size_cbx_menu = {'AXIdentifier': 'IDC_COMBOBOX_CELL', 'AXRole': 'AXComboBox', 'index': 1}  # v20.3.3630:_NS:65
    size_triangle_button = [size_cbx_menu, {'AXRole': 'AXButton'}]

    # title color
    title_color = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_BTN_COLORPICKER_FONT', 'AXRole': 'AXButton'} # v20.3.3630:_NS:72

    # Bold
    btn_bold = [designer_window, {'AXIdentifier': 'IDC_SHAPE_DESIGNER_BTN_FONT_BOLD'}] # v20.3.3630:'_NS:12', 'index': 1

    # Italic
    btn_italic = [designer_window, {'AXIdentifier': 'IDC_SHAPE_DESIGNER_BTN_FONT_ITALIC'}] # v20.3.3630:_NS:32

    # Align
    btn_align_left = [designer_window, {'AXIdentifier': 'IDC_SHAPE_DESIGNER_BTN_ALIGN_LEFT'}] # v20.3.3630:_NS:108
    btn_align_center = [designer_window, {'AXIdentifier': 'IDC_SHAPE_DESIGNER_BTN_ALIGN_CENTER'}] # v20.3.3630:_NS:116
    btn_align_right = [designer_window, {'AXIdentifier': 'IDC_SHAPE_DESIGNER_BTN_ALIGN_RIGHT'}] # v20.3.3630:_NS:24

    # Shrink text on overflow
    checkbox_shrink = [designer_window, {'AXTitle': 'Shrink text on overflow', 'AXRole': 'AXCheckBox'}]

class alert_dialog:
    main = {'AXIdentifier': 'IDD_CLALERT', 'AXTitle': 'CyberLink PowerDirector'}
    shape_outline_warning_message = [main, {'AXIdentifier': 'IDC_CLALERT_MESSAGE',
                                            'AXValue': 'Shape outline must remain enabled for this shape.'}]
    btn_OK = [main, {'AXIdentifier': 'IDC_CLALERT_BUTTON_0', 'AXTitle': 'OK'}]
    btn_cancel = [main, {'AXIdentifier': 'IDC_CLALERT_BUTTON_2', 'AXTitle': 'Cancel'}]
    btn_no = [main, {'AXIdentifier': 'IDC_CLALERT_BUTTON_1', 'AXTitle': 'No'}]
    btn_yes = [main, {'AXIdentifier': 'IDC_CLALERT_BUTTON_0', 'AXTitle': 'Yes'}]

# keyframe session
class keyframe:
    class object_settings:
        disclosure_triangle = {'AXIdentifier': 'NSOutlineViewDisclosureButtonKey'}

        class position:
            keyframe = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_KEYFRAME_POSITION'} # v20.3.3630:_NS:39
            ease = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_EASE_POSITION'} # v20.3.3630:_NS:72
            ke_combo = KEComboSet(keyframe, ease)
            x = AdjustSet({'AXIdentifier': 'IDC_SHAPE_DESIGNER_SPINEDIT_POSITION_X'}) # v20.3.3630:_NS:50
            y = AdjustSet({'AXIdentifier': 'IDC_SHAPE_DESIGNER_SPINEDIT_POSITION_Y'}) # v20.3.3630:_NS:60

        class scale:
            keyframe = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_KEYFRAME_SCALE'} # v20.3.3630:_NS:95
            ease = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_EASE_SCALE'} # v20.3.3630:_NS:156
            ke_combo = KEComboSet(keyframe, ease)
            slider_width = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_SLIDER_SCALE_WIDTH'} # v20.3.3630:_NS:106
            width = AdjustSet({'AXIdentifier': 'IDC_SHAPE_DESIGNER_SPINEDIT_SCALE_WIDTH'}) # v20.3.3630:_NS:114
            width.group[0] = slider_width
            slider_height = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_SLIDER_SCALE_HEIGHT'} # v20.3.3630:_NS:125
            height = AdjustSet({'AXIdentifier': 'IDC_SHAPE_DESIGNER_SPINEDIT_SCALE_HEIGHT'}) # v20.3.3630:_NS:132
            height.group[0] = slider_height
            maintain_aspect_ratio = {'AXIdentifier': 'IDC_PIP_DESIGNER_OB_CHECKBOX_KEEPRATIO'}

        class opacity:
            keyframe = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_KEYFRAME_OPACITY'} # v20.3.3630:_NS:177
            ease = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_EASE_OPACITY'} # v20.3.3630:_NS:196
            ke_combo = KEComboSet(keyframe, ease)
            value = AdjustSet({'AXIdentifier': 'IDC_SHAPE_DESIGNER_SPINEDIT_OPACITY'}) # v20.3.3630:_NS:187
            slider = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_SLIDER_OPACITY'}
            value.group[0] = slider

        class rotation:
            keyframe = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_KEYFRAME_ROTATION'} # v20.3.3630:_NS:217
            ease = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_EASE_ROTATION'} # v20.3.3630:_NS:229
            ke_combo = KEComboSet(keyframe, ease)
            value = AdjustSet({'AXIdentifier': 'IDC_SHAPE_DESIGNER_SPINEDIT_ROTATION'}) # v20.3.3630:_NS:220

class simple_track:
    btn_zoom_in = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_ZOOM_IN'}
    btn_zoom_out = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_ZOOM_OUT'}
    slider_zoom = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_SLIDER_ZOOM'}
    indicator_zoom = [slider_zoom, {'AXRole': 'AXValueIndicator'}]
    scroll_bar_in_vertical = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_VERTICAL_SCROLLVIEW_SCROLLBAR', 'AXRole': 'AXScrollBar'}
    indicator_vertical = [scroll_bar_in_vertical, {'AXRoleDescription': 'value indicator'}]
    btn_movie_mode = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_MOVIE_TIMECODE'}
    btn_clip_mode = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_CLIP_TIMECODE'}
    keyframe_header_outline_row = [designer_window, {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_HEADER_OUTLINEVIEW'}, {'AXRoleDescription': 'outline row'}]
    keyframe_header_name = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_KEYFRAME_HEADER_CELL_TITLE'}
    keyframe_track_outlineview = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW'}
    keyframe_track_outline_row = [{'AXIdentifier': 'IDC_SIMPLE_TIMELINE_TRACK_OUTLINEVIEW'}, {'AXRole': 'AXRow'}]
    keyframe_node_group = {'AXIdentifier': 'SimpleTimelineKeyframeCollectionViewItem'}

    class right_click_menu:
        remove_keyframe = {'AXIdentifier': 'onAddRemoveKeyframe:'}
        remove_all_keyframe = {'AXIdentifier': 'onRemoveAllKeyframe:'}
        duplicate_prev_keyframe = {'AXIdentifier': 'onDuplicatePrevKeyframe:'}
        duplicate_next_keyframe = {'AXIdentifier': 'onDuplicateNextKeyframe:'}
        ease_in = {'AXIdentifier': 'onEaseIn:'}
        ease_out = {'AXIdentifier': 'onEaseOut:'}

class simple_position_track:
    add_remove_current_keyframe = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_ADD_REMOVE_KEYFRAME'}
    previous_keyframe = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_PREV_KEYFRAME'}
    next_keyframe = {'AXIdentifier': 'IDC_SIMPLE_TIMELINE_BTN_NEXT_KEYFRAME'}

btn_hide_timeline_mode = {'AXIdentifier': '_NS:375', 'AXRole': 'AXButton'}
btn_show_timeline_mode = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_BUTTON_SHOW_HIDE_TIMELINE', 'AXRole': 'AXButton'} # v20.3.3630:_NS:383

preview_play = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_BUTTON_PLAY', 'AXRoleDescription': 'button'}
preview_stop = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_BUTTON_STOP', 'AXRoleDescription': 'button'}
preview_previous_frame = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_BUTTON_PREVIOUS_FRAME', 'AXRoleDescription': 'button'} # v20.3.3630:_NS:41
preview_next_frame = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_BUTTON_NEXT_FRAME', 'AXRoleDescription': 'button'} # v20.3.3630:_NS:50
preview_fast_forward = {'AXIdentifier': 'IDC_SHAPE_DESIGNER_BUTTON_FAST_FORWARD', 'AXRoleDescription': 'button'} # v20.3.3630:_NS:59

toggle_grid_line_on_off = {'AXIdentifier': '_NS:165', 'AXRoleDescription': 'button'}
snap_to_reference_line = {'AXIdentifier': '_NS:70', 'AXTitle': 'Snap to Reference Lines'}
grid_lines = {'AXIdentifier': '_NS:74', 'AXTitle': 'Grid Lines'}
menu_item_none = {'AXIdentifier': '_NS:15', 'AXTitle': 'None'}
menu_item_2 = {'AXIdentifier': '_NS:27', 'AXTitle': '2 x 2'}
menu_item_3 = {'AXIdentifier': '_NS:31', 'AXTitle': '3 x 3'}
menu_item_4 = {'AXIdentifier': '_NS:35', 'AXTitle': '4 x 4'}
menu_item_5 = {'AXIdentifier': '_NS:39', 'AXTitle': '5 x 5'}
menu_item_6 = {'AXIdentifier': '_NS:43', 'AXTitle': '6 x 6'}
menu_item_7 = {'AXIdentifier': '_NS:47', 'AXTitle': '7 x 7'}
menu_item_8 = {'AXIdentifier': '_NS:51', 'AXTitle': '8 x 8'}
menu_item_9 = {'AXIdentifier': '_NS:55', 'AXTitle': '9 x 9'}
menu_item_10 = {'AXIdentifier': '_NS:59', 'AXTitle': '10 x 10'}

# for canvas shape (general)
canvas_object_shape = {'AXIdentifier': 'dashBorderedView', 'AXRole': 'AXGroup'}
canvas_split_view = [designer_window, {'AXIdentifier': 'IDC_IDC_SHAPE_DESIGNER_PREVIEW_SCROLL_VIEW', 'AXRole': 'AXScrollArea'}]
