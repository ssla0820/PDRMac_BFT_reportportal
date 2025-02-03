# Main window
effect_setting_main = {'AXIdentifier': 'IDD_LIBRARY', 'AXRole': 'group'}

# Button
btn_reset = [effect_setting_main, {'AXIdentifier': 'IDC_EFFECT_SETTING_PANEL_BTN_RESET'}]
btn_remove_effect = [effect_setting_main, {'AXIdentifier': 'IDC_EFFECT_SETTING_PANEL_BTN_REMOVE_EFFECT'}]

parent_split_group = [effect_setting_main, {'AXRole': 'AXSplitGroup'}]
# (Left side) Applied effect area
scroll_area_left = [parent_split_group, {'AXRole': 'AXScrollArea', "index": 0}]
# (Right side) Parameter area
scroll_area_right = [parent_split_group, {'AXIdentifier': 'IDC_EFFECTSETTING_SCROLLVIEW_FLIPPEDVIEW'}]

# group for slider / editbox
group_slider_edit_1 = [scroll_area_right,  {'AXIdentifier': 'textSliderEdit', "index": 0}]
group_slider_edit_2 = [scroll_area_right,  {'AXIdentifier': 'textSliderEdit', "index": 1}]
group_slider_edit_3 = [scroll_area_right,  {'AXIdentifier': 'textSliderEdit', "index": 2}]
group_slider_edit_4 = [scroll_area_right,  {'AXIdentifier': 'textSliderEdit', "index": 3}]
group_slider_edit_5 = [scroll_area_right,  {'AXIdentifier': 'textSliderEdit', "index": 4}]
group_slider_edit_6 = [scroll_area_right,  {'AXIdentifier': 'textSliderEdit', "index": 5}]
group_slider_edit_7 = [scroll_area_right,  {'AXIdentifier': 'textSliderEdit', "index": 6}]
slider_1 = [group_slider_edit_1, {'AXIdentifier': 'IDC_SLIDER_TEXTSLIDEREDIT'}]
slider_2 = [group_slider_edit_2, {'AXIdentifier': 'IDC_SLIDER_TEXTSLIDEREDIT'}]
slider_3 = [group_slider_edit_3, {'AXIdentifier': 'IDC_SLIDER_TEXTSLIDEREDIT'}]
slider_4 = [group_slider_edit_4, {'AXIdentifier': 'IDC_SLIDER_TEXTSLIDEREDIT'}]
slider_5 = [group_slider_edit_5, {'AXIdentifier': 'IDC_SLIDER_TEXTSLIDEREDIT'}]
slider_6 = [group_slider_edit_6, {'AXIdentifier': 'IDC_SLIDER_TEXTSLIDEREDIT'}]
slider_7 = [group_slider_edit_7, {'AXIdentifier': 'IDC_SLIDER_TEXTSLIDEREDIT'}]

# Inverse checkbox
cbx_inverse = [scroll_area_right, {'AXTitle': 'Inverse', 'AXRole': 'AXCheckBox'}]
cbx_grayscale = [scroll_area_right, {'AXTitle': 'Grayscale', 'AXRole': 'AXCheckBox'}]
cbx_invert_masked_area = [scroll_area_right, {'AXTitle': 'Invert masked area', 'AXRole': 'AXCheckBox'}]
cbx_random_stroke = [scroll_area_right, {'AXTitle': 'Random Stroke', 'AXRole': 'AXCheckBox'}]

# Black and White
cbx_invert_masked_area = [scroll_area_right, {'AXIdentifier': 'IDS_Vi_Param_InverseEffectArea_Name', 'AXTitle': 'Invert masked area'}]
cbx_mask_type = [scroll_area_right, {'AXIdentifier': 'IDS_Vi_Param_MaskType_Name;box;circle'}]

# Color Balance
cbx_grayscale = [scroll_area_right, {'AXIdentifier': 'IDS_Vi_Param_GreyScale_Name'}]

# Color Crayon
cbx_bg_texture = [scroll_area_right, {'AXIdentifier': 'IDS_Vi_Param_TextureBackground_Name;Tex1;Tex2;Tex3;Tex4'}]

# Emboss
cbx_direction = [scroll_area_right, {'AXIdentifier': 'IDS_Vi_Param_Direction_Name;None;UL;U;UR;R;LR;D;LL;L'}]

# Swing
cbx_type = [scroll_area_right, {'AXIdentifier': 'IDS_Vi_Param_EffectType_Name;Up;Dn;L;R'}]

# Color
btn_color_1 = [scroll_area_right,  {'AXRole': 'AXButton', "index": 0}]
btn_color_2 = [scroll_area_right,  {'AXRole': 'AXButton', "index": 1}]
btn_color_3 = [scroll_area_right,  {'AXRole': 'AXButton', "index": 2}]

# Magnify Dropdown menu
cbx_magnify_type = [scroll_area_right, {'AXIdentifier': 'IDS_Vi_Param_MagnifyType_Name;Circle;Box'}]

# Body Effect : Aura1 (v21.6.5206)
cbx_preset = [effect_setting_main, {'AXTitle': 'Default'}]
btn_glow_color = [scroll_area_right, {'AXIdentifier': 'IDS_Vi_Param_GlowColor_Name'}]
btn_polygon_color = [scroll_area_right, {'AXIdentifier': 'IDS_Vi_Param_PolygonColor_Name'}]
btn_clone_color = [scroll_area_right, {'AXIdentifier': 'IDS_Vi_Param_CloneColor_Name'}]