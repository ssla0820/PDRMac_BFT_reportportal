
# main locator
main_window = {'AXIdentifier': 'IDD_LIBRARY'}
btn_close = [main_window, {'AXRoleDescription': 'button', 'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_LEAVE'}]
frame_setting_panel = [main_window, {'AXRoleDescription': 'outline', 'AXIdentifier': 'IDC_SETTINGPANEL_KEYFRAMEROOM'}]
frame_setting_panel_scroll_area =  {'AXIdentifier': 'IDC_KEYFRAME_SETTING_PANEL_GROUP_CONTAINER_SCROLLVIEW'} # hardcode in 3033
frame_keyframe_panel = {'AXIdentifier': 'IDC_KEYFRAME_SETTING_PANEL_KEYFRAME_CONTAINER_OUTLINEVIEW'} # hardcode in 3033
image_thumbnail = {'AXIdentifier': 'IDC_KEYFRAME_SETTING_PANEL_THUMBNAIL'} # hardcode in 3033
scrollbar_vertical = [frame_setting_panel_scroll_area, {'AXRole': 'AXScrollBar'}]
txt_top_left_duration = [main_window, {'AXRole': 'AXStaticText', 'recursive': False}]

# === left attribute setting panel ===
# unit of category: Fix/ Enhance, Clip Attributes, Volume
unit_setting_category = [frame_setting_panel, {'AXRoleDescription': 'outline row'}] # the unit of 3 categories
disclosure_triangle = {'AXRoleDescription': 'disclosure triangle'} # child of unit_setting_category, value=0 (close), 1(open)
# category: Fix/ Enhance
btn_category_fix_enhance = {'AXRoleDescription': 'button', 'AXTitle': 'Fix / Enhance'} # child of unit_setting_category
btn_category_clip_attributes = {'AXRoleDescription': 'button', 'AXTitle': 'Clip Attributes'} # child of unit_setting_category
btn_category_volume = {'AXRoleDescription': 'button', 'AXTitle': 'Volume'} # child of unit_setting_category
unit_attribute_name = {'AXRole': 'AXStaticText'} # attribute name in outline row
unit_category_name = {'AXRoleDescription': 'button', 'AXTitle': ''}
unit_attribute_name_checkbox = {'AXRole': 'AXCheckBox'} # attribute name of using checkbox > for 20.0 Extreme backlighting
# unit sub-item of category
unit_item_of_category = unit_setting_category
# keyframe operation
btn_add_remove_keyframe = {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_ADDREMOVE_KEYFRAME'} # check AXEnabled: True/ False
btn_next_keyframe = {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_NEXT_KEYFRAME'}
btn_previous_keyframe = {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_PREVIOUS_KEYFRAME'}
btn_reset_keyframe = {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_RESET_PARAM_KEYFRAME'}
# attribute setting
unit_slider = {'AXIdentifier': 'IDC_KEYFRAMEROOM_SLIDER_SELECTSLIDER'}
unit_edittext_slider_value = {'AXIdentifier': 'spinEditTextField'}
btn_stepper_up = {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP'}
btn_stepper_down = {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN'}
edittext_attribute_value = {'AXIdentifier': 'spinEditTextField'}
# btn_combobox = {'AXIdentifier': '_NS:9'} # 3018: _NS:9 (already feedback hardcode)
btn_noise_type_combobox = {'AXIdentifier': 'IDC_COMBOBOX_PARAM_CTRL_BTN'} # fix_enhance > audio denoise > noise type
btn_blending_mode_combobox = {'AXIdentifier': 'IDC_OPACITY_PARAM_CTRL_BTN'} # clip attributes > opacity > blending mode

#Fix/ Enhance
# >> White Balance
rdb_color_temperature = {'AXIdentifier': 'IDC_KEYFRAMEROOM_RADIO_COLORTEMPERATURE'}
rdb_white_calibration = {'AXIdentifier': 'IDC_KEYFRAMEROOM_RADIO_WHITECALIBRATE'}
group_edittext_stepper_color_temperature = {'AXIdentifier': 'IDC_WHITE_BALANCE_PARAM_CTRL_SPINEDIT_COLOR_TEMPERATURE'} # hardcode in 3033
group_edittext_stepper_tint = {'AXIdentifier': 'IDC_WHITE_BALANCE_PARAM_CTRL_SPINEDIT_TINT'} # hardcode in 3033
btn_white_calibration = {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_WHITECALIBRATION'}


class white_calibration_dialog:
    main_window = {'AXRoleDescription': 'dialog', 'AXTitle': 'White Calibration'}
    btn_close = [main_window, {'AXRoleDescription': 'close button'}]
    btn_information = {'AXIdentifier': 'IDC_WHITE_BALANCE_DIALOG_BTN_CALIBRATED'} # hardcode in 3033

class what_is_white_calibration_dialog:
    main_window = {'AXRoleDescription': 'dialog', 'AXTitle': 'What is White Calibration?'}
    btn_close = [main_window, {'AXRoleDescription': 'close button'}]

# === right keyframe panel ===
unit_keyframe_outline_row = [frame_keyframe_panel, {'AXRoleDescription': 'outline row'}]
unit_keyframe_node = {'AXDescription': 'keyframe seek*'}

# > Clip Attribute
# >> Position
group_edittext_stepper_xy = {'AXIdentifier': 'IDC_KEYFRAMEROOM_SPINEDIT_POSITION'}
group_edittext_stepper_ease_in_out = {'AXIdentifier': 'IDC_EASE_CTRL_SPINEDIT_EASE_IN'}
group_edittext_stepper_ease_out = {'AXIdentifier': 'IDC_EASE_CTRL_SPINEDIT_EASE_OUT'}
chx_ease_in = {'AXIdentifier': 'IDC_EASE_CTRL_CHECKBOX_EASE_IN'}
slider_ease_in = {'AXIdentifier': 'IDC_EASE_CTRL_SLIDER_EASE_IN'}
chx_ease_out = {'AXIdentifier': 'IDC_EASE_CTRL_CHECKBOX_EASE_OUT'}
slider_ease_out = {'AXIdentifier': 'IDC_EASE_CTRL_SLIDER_EASE_OUT'}
btn_tutorial = {'AXIdentifier': 'IDC_EASE_CTRL_BTN_TUTORIAL'}

# >> Scale
group_edittext_stepper_width = {'AXIdentifier': 'IDC_SIZE_PARAM_CTRL_SPINEDIT_WIDTH'} # hardcode in 3033
group_edittext_stepper_height = {'AXIdentifier': 'IDC_SIZE_PARAM_CTRL_SPINEDIT_HEIGHT'} # hardcode in 3033
chx_maintain_aspect_ratio = {'AXIdentifier': 'IDC_KEYFRAMEROOM_CHECKBOX'}