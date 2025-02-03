
main_window = {'AXRole': 'AXWindow', 'AXIdentifier': 'IDC_VIDEO_TRIM_DIALOG_WINDOW'} #2922: _NS:10
btn_restore = [main_window, {'AXRole': 'AXButton', 'AXRoleDescription': 'zoom button'}]
btn_cancel = [main_window, {'AXIdentifier': 'IDC_MULCUTBUTTON_CANCEL', 'AXTitle': 'Cancel'}]
btn_close = [main_window, {'AXRole': 'AXButton', 'AXRoleDescription': 'close button'}]
btn_ok = [main_window, {'AXIdentifier': 'IDC_MULCUTBUTTON_OK'}]
btn_no = [main_window, {'AXTitle': 'No'}]
close_dialog_cancel = {'AXIdentifier': 'IDC_CLALERT_BUTTON_2'}
close_dialog_yes = {'AXIdentifier': 'IDC_CLALERT_BUTTON_0'}
close_dialog_no = {'AXIdentifier': 'IDC_CLALERT_BUTTON_1'}

precut_window_current_time = [{'AXIdentifier': 'IDC_MULCUT_SPINTIMEEDIT', 'AXRole': 'AXGroup'}, {'AXIdentifier': 'spinTimeEditTextField', 'AXRoleDescription': 'text'}]
single_trim = {'AXIdentifier': 'IDC_CUTBUTTON_SINGLE_CUT', 'AXRole': 'AXCheckBox'}
single_trim_in_position_thumbnail = {'AXIdentifier': 'IDC_VIDEO_TRIM_DIALOG_SINGLE_TRIM_IN_THUMBNAIL', 'AXRole': 'AXImage'} # 2922: 770
single_trim_out_position_thumbnail = {'AXIdentifier': 'IDC_VIDEO_TRIM_DIALOG_SINGLE_TRIM_OUT_THUMBNAIL', 'AXRole': 'AXImage'} # 2922: _NS:750
multi_trim = {'AXIdentifier': 'IDC_CUTBUTTON_MULTI_CUT', 'AXRole': 'AXCheckBox'}
multi_trim_not_been_applied = {'AXIdentifier': 'IDC_CLALERT_MESSAGE', 'AXValue': 'The trims you made in the Multi Trim window have not yet been applied. Only the first trimmed segment will be available in the Single Trim window. Do you want to continue?'}
multi_trim_not_been_applied_ok = {'AXTitle': 'OK', 'AXIdentifier': 'IDC_CLALERT_BUTTON_0'}
multi_trim_thumbnail_slider = {'AXOrientation': 'AXHorizontalOrientation', 'AXRole': 'AXList', 'AXRoleDescription': 'section'}
multi_trim_selected_segment = {'AXIdentifier': 'IDC_VIDEO_TRIM_DIALOG_MULTI_TRIM_SELECTED_SEGMENTS', 'AXRoleDescription': 'collection'} # 2922: _NS:820

save_before_leaving_cancel = {'AXRole': 'AXButton', 'AXTitle': 'Cancel'}
save_before_leaving_no = {'AXRole': 'AXButton', 'AXTitle': 'No'}
save_before_leaving_yes = {'AXRole': 'AXButton', 'AXTitle': 'Yes'}

single_trim_drag_slider = {'AXRole': 'AXValueIndicator', 'AXRoleDescription': 'value indicator'}
yellow_left_slider = {'AXRole': 'AXImage', 'AXDescription': 'multiTrim EditFilm Slider Y l'}
yellow_right_slider = {'AXRole': 'AXImage', 'AXDescription': 'multiTrim EditFilm Slider Y r'}

single_trim_mark_in = {'AXIdentifier': 'IDC_SINMULCUTBUTTON_MARKIN', 'AXRole': 'AXButton'}
single_trim_mark_out = {'AXIdentifier': 'IDC_SINMULCUTBUTTON_MARKOUT', 'AXRole': 'AXButton'}
single_trim_lock_duration = {'AXIdentifier': 'IDC_SINMULCUTBUTTON_LOCKABLE', 'AXRole': 'AXButton'}

single_trim_precut_duration = {'AXIdentifier': 'spinTimeEditTextField', 'AXHelp': 'Duration'}
single_trim_precut_duration_up = [{'AXIdentifier': 'IDC_VIDEOTRIM_SPINTIMEEDITDURATION', 'AXRole': 'AXGroup'}, {'AXIdentifier': 'IDC_SPINTIMEEDIT_BTN_UP', 'AXRoleDescription': 'button'}]
single_trim_precut_duration_down = [{'AXIdentifier': 'IDC_VIDEOTRIM_SPINTIMEEDITDURATION', 'AXRole': 'AXGroup'}, {'AXIdentifier': 'IDC_SPINTIMEEDIT_BTN_DOWN', 'AXRoleDescription': 'button'}]

single_trim_precut_in_position = {'AXIdentifier': 'spinTimeEditTextField', 'AXHelp': 'In position'}
single_trim_precut_in_position_up = [{'AXIdentifier': 'IDC_VIDEOTRIM_SPINTIMEEDITMARKIN', 'AXHelp': 'In position'}, {'AXIdentifier': 'IDC_SPINTIMEEDIT_BTN_UP', 'AXRoleDescription': 'button'}]
single_trim_precut_in_position_down = [{'AXIdentifier': 'IDC_VIDEOTRIM_SPINTIMEEDITMARKIN', 'AXHelp': 'In position'}, {'AXIdentifier': 'IDC_SPINTIMEEDIT_BTN_DOWN', 'AXRoleDescription': 'button'}]

single_trim_precut_out_position = {'AXIdentifier': 'spinTimeEditTextField', 'AXHelp': 'Out position'}
single_trim_precut_out_position_up = [{'AXIdentifier': 'IDC_VIDEOTRIM_SPINTIMEEDITMARKOUT', 'AXHelp': 'Out position'}, {'AXIdentifier': 'IDC_SPINTIMEEDIT_BTN_UP', 'AXRoleDescription': 'button'}]
single_trim_precut_out_position_down = [{'AXIdentifier': 'IDC_VIDEOTRIM_SPINTIMEEDITMARKOUT', 'AXHelp': 'Out position'}, {'AXIdentifier': 'IDC_SPINTIMEEDIT_BTN_DOWN', 'AXRoleDescription': 'button'}]

multi_trim_mark_in = {'AXIdentifier': 'IDC_MULCUTBUTTON_MARKIN', 'AXRole': 'AXButton'}
multi_trim_mark_out = {'AXIdentifier': 'IDC_MULCUTBUTTON_MARKOUT', 'AXRole': 'AXButton'}
multi_trim_slider = {'AXIdentifier': 'selectSlider', 'AXRoleDescription': 'group'}
multi_trim_drag_slider = {'AXRole': 'AXValueIndicator', 'AXRoleDescription': 'value indicator'}
multi_trim_invert_trim = {'AXIdentifier': 'IDC_MULCUTBUTTON_REVERSE', 'AXRole': 'AXButton'}
multi_trim_remove = {'AXIdentifier': 'IDC_MULCUTBUTTON_REMOVE', 'AXRole': 'AXButton'}
multi_trim_remove_segment = {'AXIdentifier': 'removeSegment:', 'AXTitle': 'Remove Selected'}
multi_trim_invert_selection = {'AXIdentifier': 'onMultiTrimInvertClicked:', 'AXTitle': 'Invert Selection'}

precut_play = {'AXIdentifier': 'IDC_MULCUTBUTTON_PLAY', 'AXRole': 'AXButton'}
precut_pause = {'AXIdentifier': 'IDC_MULCUTBUTTON_PAUSE', 'AXRole': 'AXButton'}
precut_stop = {'AXIdentifier': 'IDC_MULCUTBUTTON_STOP', 'AXRole': 'AXButton'}
precut_previous_frame = {'AXIdentifier': 'IDC_MULCUTBUTTON_PREVFRAME', 'AXRole': 'AXButton'}
precut_next_frame = {'AXIdentifier': 'IDC_MULCUTBUTTON_NEXTFRAME', 'AXRole': 'AXButton'}

multi_trim_original = {'AXIdentifier': 'IDC_MULCUTBUTTON_ORIGINAL', 'AXTitle': 'Original'}
multi_trim_output = {'AXIdentifier': 'IDC_MULCUTBUTTON_OUTPUT', 'AXTitle': 'Output'}

single_trim_slider = {'AXIdentifier': '_NS:12', 'AXRole': 'AXSlider'}
