
display_panel = {'AXIdentifier': 'IDD_DISPLAYPANEL'}
timeline_preview_area = [display_panel, {'AXRole': 'AXScrollArea'}]

dock_preview_window = {'AXDescription': 'Custom View', 'AXRole': 'AXButton'}
library_preview_window_close = {'AXIdentifier': 'IDC_LIB_PREVIEW_BTN_CLOSE'}
undock_preview_window = {'AXIdentifier': 'IDC_LIB_PREVIEW_BTN_UNDOCK'}
toolbar = [{'AXIdentifier': '_NS:212', 'AXRole': 'AXWindow'}, {'AXRole': 'AXToolbar', 'AXRoleDescription': 'toolbar'}] #20v3310_Checked. v2922: _NS:198 (PDR Main window)

library_preview_window_maximize = {'AXSubrole': 'AXZoomButton', 'AXRoleDescription': 'zoom button'}
library_preview_window_restoredown = {'AXSubrole': 'AXZoomButton', 'AXRoleDescription': 'zoom button'}
library_preview_window_minimize = {'AXSubrole': 'AXMinimizeButton', 'AXRoleDescription': 'minimize button'}
show_minimized_window = [{'AXRole': 'AXToolbar'}, {'AXRole': 'AXButton', 'index': 2, 'AXSize': (41.0, 38.0)}]
toolbar_last_btn = [{'AXRole': 'AXToolbar'}, {'AXRole': 'AXButton', 'index': 7}]
restore_minimized_window = {'AXIdentifier': 'menuLibraryPreview'}

upper_project_name = {'AXIdentifier': 'IDC_UNDOCK_WINDOW_TITLE'} #20v3310_Checked. v2922: _NS:42
add_to_effect_track = {'AXIdentifier': 'IDC_TIPSAREA_BTN_ADDTOEFFECTTRACK'}
timeline_scrollbar = {'AXRole': 'AXValueIndicator', 'AXRoleDescription': 'value indicator'}

menu_bar_view_btn = {'AXIdentifier': 'IDM_MAIN_MENU_VIEW', 'AXRole': 'AXMenuBarItem'} #20v3310_Checked, v2922: _NS:278
menu_bar_view_show_library_preview_window = {'AXIdentifier': 'IDM_MENU_VIEW_LIBRARY_PREVIEW_WINDOW'}

upper_view_region = {'AXIdentifier': 'IDD_UPPERVIEW'}

class dock_window:
    dock_window_duration_section = [{'AXIdentifier': 'IDD_UPPERVIEW'}, {'AXIdentifier': 'spinTimeEditTextField', 'AXRole': 'AXStaticText'}]
    dock_window_play_btn = {'AXIdentifier': 'IDC_LIB_PREVIEW_BTN_PLAY', 'AXRole': 'AXButton'}
    dock_window_pause_btn = {'AXIdentifier': 'IDC_LIB_PREVIEW_BTN_PAUSE', 'AXRole': 'AXButton'}
    dock_window_stop_btn = {'AXIdentifier': 'IDC_LIB_PREVIEW_BTN_STOP', 'AXRole': 'AXButton'}
    dock_window_previous_frame_btn = {'AXIdentifier': 'IDC_LIB_PREVIEW_BTN_PREVIOUSFRAME', 'AXRole': 'AXButton'}
    dock_window_next_frame_btn = {'AXIdentifier': 'IDC_LIB_PREVIEW_BTN_NEXTFRAME', 'AXRole': 'AXButton'}
    dock_window_fast_forward_btn = {'AXIdentifier': 'IDC_LIB_PREVIEW_BTN_FASTFORWARD', 'AXRole': 'AXButton'}
    #dock_window_snapshot_btn = [{'AXIdentifier': 'IDD_UPPERVIEW', 'AXRole': 'AXSplitGroup'}, {'AXRole': 'AXButton', 'index': 38}]
    dock_window_snapshot_btn = {'AXIdentifier': 'IDC_LIB_PREVIEW_BTN_SNAPSHOT'}
    #undock_window_snapshot_btn = [{'AXIdentifier': 'PopupWindow', 'AXRoleDescription': 'standard window'}, {'AXRole': 'AXButton', 'index': 13}]
    undock_window_snapshot_btn = {'AXIdentifier': 'IDC_LIB_PREVIEW_BTN_SNAPSHOT'}
    dock_window_snapshot_save_btn = {'AXIdentifier': '_NS:314', 'AXRole': 'AXButton'} #20v3310_Checked

snapshot_filename_textfield = {'AXIdentifier': '_NS:111', 'AXRole': 'AXTextField'} #20v3310_Checked
snapshot_save_btn = {'AXIdentifier': '_NS:314'} #20v3310_Checked
snapshot_filename_existed_dialog = {'AXIdentifier': '_NS:58', 'AXRole': 'AXStaticText'} #20v3310_Checked; the 2nd text description
snapshot_save_replace_btn = {'AXIdentifier': '_NS:9', 'AXTitle': 'Replace'} #20v3310_Checked
#dock_window_volume_btn = [{'AXIdentifier': 'IDD_UPPERVIEW', 'AXRole': 'AXSplitGroup'}, {'AXRole': 'AXButton', 'index': 37}]
dock_window_volume_btn = {'AXIdentifier': 'IDC_LIB_PREVIEW_BTN_VOLUME', 'AXRole': 'AXButton'}
#undock_window_volume_btn = [{'AXIdentifier': 'PopupWindow', 'AXRoleDescription': 'standard window'}, {'AXRole': 'AXButton', 'index': 12}]
undock_window_volume_btn = {'AXIdentifier': 'IDC_LIB_PREVIEW_BTN_VOLUME', 'AXRole': 'AXButton'}

library_preview_window_slider = {'AXRole': 'AXValueIndicator', 'AXRoleDescription': 'value indicator'}
library_preview_window_volume_slider = {'AXIdentifier': 'IDC_VOLUME_POPOVER_SLIDER', 'AXRoleDescription': 'slider', 'AXOrientation': 'AXVerticalOrientation'}
library_preview_window_duration_section = {'AXIdentifier': 'spinTimeEditTextField', 'AXRole': 'AXStaticText'}

library_preview_window_markin = {'AXIdentifier': 'IDC_LIB_PREVIEW_BTN_MARKIN', 'AXRole': 'AXButton'}
library_preview_window_markout = {'AXIdentifier': 'IDC_LIB_PREVIEW_BTN_MARKOUT', 'AXRole': 'AXButton'}
library_preview_window_click_insert_on_selected_track = {'AXIdentifier': 'IDC_LIB_PREVIEW_BTN_INSERT', 'AXRole': 'AXButton'}
library_preview_window_click_overwrite_on_selected_track = {'AXIdentifier': 'IDC_LIB_PREVIEW_BTN_OVERWRITE', 'AXRole': 'AXButton'}
library_preview_window_add_clip_marker = {'AXIdentifier': 'IDC_LIB_PREVIEW_BTN_CLIPMARKER', 'AXRole': 'AXButton'}

library_preview_window_modify_marker = {'AXIdentifier': 'IDC_ADD_CLIP_MARKER_WINDOW', 'AXRole': 'AXWindow'}
library_preview_window_add_clip_marker_text_field = {'AXIdentifier': 'IDC_ADD_TIMELINE_MARKER_TEXTVIEW', 'AXRoleDescription': 'text entry area'}
library_preview_window_clip_marker_ok = {'AXIdentifier': 'IDC_ADD_TIMELINE_MARKER_BUTTON_OK'}

library_preview_window_play_btn = {'AXIdentifier': 'IDC_LIB_PREVIEW_BTN_PLAY', 'AXRole': 'AXButton'}
library_preview_window_pause_btn = {'AXIdentifier': 'IDC_LIB_PREVIEW_BTN_PAUSE', 'AXRole': 'AXButton'}
library_preview_window_stop_btn = {'AXIdentifier': 'IDC_LIB_PREVIEW_BTN_STOP', 'AXRole': 'AXButton'}
library_preview_window_previous_frame_btn = {'AXIdentifier': 'IDC_LIB_PREVIEW_BTN_PREVIOUSFRAME', 'AXRole': 'AXButton'}
library_preview_window_next_frame_btn = {'AXIdentifier': 'IDC_LIB_PREVIEW_BTN_NEXTFRAME', 'AXRole': 'AXButton'}
library_preview_window_fast_forward_btn = {'AXIdentifier': 'IDC_LIB_PREVIEW_BTN_FASTFORWARD', 'AXRole': 'AXButton'}
library_preview_window_timecode = {'AXIdentifier': 'spinTimeEditTextField', 'AXRole': 'AXStaticText'}
text_project_name = {'AXIdentifier': '_NS:251', 'AXRole': 'AXStaticText'} #20v3310_Checked. v2922: _NS:236

