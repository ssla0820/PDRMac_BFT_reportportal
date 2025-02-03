# Library menu if subtitle room is empty
class library_menu():
    btn_speech_to_text = {'AXIdentifier': 'IDC_SUBTITLE_ROOM_BTN_SPEECH_TO_TEXT', 'AXRole': 'AXButton'}
    btn_create_manually = {'AXIdentifier': 'IDC_SUBTITLE_ROOM_BTN_CREATE_SUBTITLE_MANUALLY', 'AXRole': 'AXButton'}
    btn_import_file = {'AXIdentifier': 'IDC_SUBTITLE_ROOM_BTN_IMPORT_SUBTITLE_FROM_FILE', 'AXRole': 'AXButton'}
    bb_first_time = {'AXValue': 'Automatically detects voices and transcribes into subtitles.', 'AXRole': "AXStaticText"}

    # STT button is next on (Change subtitle text format
    uppper_btn_STT = {'AXIdentifier': 'IDC_BUTTON_STT', 'AXTitle': 'Speech to Text', 'AXRole': "AXButton"}

# Auto Transcirbe Subtitles window
class speech_to_text_window():
    main_window = {'AXTitle': 'Speech to Text', 'AXIdentifier': 'IDC_SPEECHTOTEXTDLG', 'AXRole': 'AXWindow'}
    btn_location = [main_window, {'AXIdentifier': 'IDC_SPEECHTOTEXTDLG_COMBOBOX_AUDIOTRACK', 'AXRole': 'AXButton'}]
    btn_language = [main_window, {'AXIdentifier': 'IDC_SPEECHTOTEXTDLG_COMBOBOX_LANGUAGE', 'AXRole': 'AXButton'}]
    option_enu = {'AXRole': 'AXMenuItem', 'AXTitle': 'English (United States)'}
    option_jpn = {'AXRole': 'AXMenuItem', 'AXTitle': 'Japanese'}
    option_cht = {'AXRole': 'AXMenuItem', 'AXTitle': 'Mandarin Chinese (Taiwan)'}
    lan_with_title_group = [option_enu, option_jpn, option_cht]
    checkbox_selected_range = [main_window, {'AXTitle': 'Transcribe selected range only', 'AXIdentifier': 'IDC_SPEECHTOTEXTDLG_CHKBTN_SELECTED_RANGE_ONLY', 'AXRole': 'AXCheckBox'}]
    btn_cancel = [main_window, {'AXIdentifier': 'IDC_SPEECHTOTEXTDLG_BTN_CANCEL', 'AXRole': 'AXButton'}]
    btn_create = [main_window, {'AXIdentifier': 'IDC_SPEECHTOTEXTDLG_BTN_CREATE', 'AXRole': 'AXButton'}]
    btn_close = [main_window, {'AXSubrole': 'AXCloseButton', 'AXRole': 'AXButton'}]

class handle_progress_dialog:
    frame = {"AXIdentifier": "IDC_PROGRESS_DIALOG"}
    title = [frame, {"AXRole": "AXStaticText"}]
    btn_cancel = [frame, {"AXIdentifier": "IDC_PROGRESS_BTN_CANCEL"}]

# Click i button to open (Subtitle editing tips)
class subtitle_editing_tips():
    main_window = {'AXTitle': 'Subtitle editing tips', 'AXIdentifier': 'IDC_EDITINGTIPSDLG', 'AXRole': 'AXWindow'}
    btn_close = [main_window, {'AXIdentifier': 'IDC_EDITINGTIPSDLG_BTN_CLOSE', 'AXRole': 'AXButton'}]
    txt_title = [main_window, {'AXValue': 'How to edit in subtitle room?', 'AXIdentifier': 'IDC_EDITINGTIPSDLG_TEXTFIELD_HOWTOEDIT', 'AXRole': 'AXStaticText'}]

class position():
    main_window= {'AXTitle': 'Position', 'AXIdentifier': 'IDC_OFFSETDLG', 'AXRole': 'AXWindow'}
    x_slider = [main_window, {'AXIdentifier': 'IDC_OFFSETDLG_SLIDER_POSX', 'AXRole': 'AXSlider'}]
    x_value = [main_window, {'AXIdentifier': 'IDC_OFFSETDLG_SPINEDIT_POSX', 'AXRole': 'AXGroup'}]
    editbox_x_field = [x_value, {'AXIdentifier': 'spinEditTextField', 'AXRole': 'AXTextField'}]
    y_slider = [main_window, {'AXIdentifier': 'IDC_OFFSETDLG_SLIDER_POSY', 'AXRole': 'AXSlider'}]
    y_value = [main_window, {'AXIdentifier': 'IDC_OFFSETDLG_SPINEDIT_POSY', 'AXRole': 'AXGroup'}]
    editbox_y_field = [y_value, {'AXIdentifier': 'spinEditTextField', 'AXRole': 'AXTextField'}]
    btn_apply_to_all = [main_window, {'AXIdentifier': 'IDC_OFFSETDLG_BTN_APPLYALL', 'AXRole': 'AXButton'}]
    btn_reset = [main_window, {'AXIdentifier': 'IDC_OFFSETDLG_BTN_RESET', 'AXRole': 'AXButton'}]
    btn_close = [main_window, {'AXSubrole': 'AXCloseButton', 'AXRole': 'AXButton'}]

class character():
    main_window = {'AXTitle': 'Character', 'AXIdentifier': 'IDC_FONTDLG', 'AXRole': 'AXWindow'}
    cbx_font = [main_window, {'AXIdentifier': 'IDC_COMBOBOX_CELL', 'AXRole': 'AXComboBox'}]
    cbx_font_pop_up_cell = [main_window, {'AXIdentifier': 'IDC_COMBOBOX_POPUP_BTN_CELL', 'AXRole': 'AXButton'}]

    cbx_style = [main_window, {'AXIdentifier': 'IDC_FONTDLG_COMBOBOX_STYLE', 'AXRole': 'AXButton'}]
    option_bold_italic = {'AXRole': 'AXStaticText', 'AXValue': 'Bold Italic'}

    cbx_size = [main_window, {'AXIdentifier': 'IDC_FONTDLG_COMBOBOX_SIZE', 'AXRole': 'AXButton'}]

    cbx_alignment = [main_window, {'AXIdentifier': 'IDC_FONTDLG_COMBOBOX_ALLIGNMENT', 'AXRole': 'AXButton'}]
    option_align_center = {'AXRole': 'AXStaticText', 'AXValue': 'Align Multiple Text Center'}
    option_align_right = {'AXRole': 'AXStaticText', 'AXValue': 'Align Multiple Text Right'}

    checkbox_text = [main_window, {'AXIdentifier': 'IDC_FONTDLG_CHKBTN_TEXT', 'AXTitle': 'Text', 'AXRole': 'AXCheckBox'}]
    checkbox_shadow = [main_window, {'AXIdentifier': 'IDC_FONTDLG_CHKBTN_SHADOW', 'AXTitle': 'Shadow', 'AXRole': 'AXCheckBox'}]
    checkbox_border = [main_window, {'AXIdentifier': 'IDC_FONTDLG_CHKBTN_BORDER', 'AXTitle': 'Border', 'AXRole': 'AXCheckBox'}]

    colorpicker_text = [main_window, {'AXIdentifier': 'IDC_FONTDLG_COLORPICKER_TEXT', 'AXRole': 'AXButton'}]
    colorpicker_shadow = [main_window, {'AXIdentifier': 'IDC_FONTDLG_COLORPICKER_SHADOW', 'AXRole': 'AXButton'}]
    colorpicker_border = [main_window, {'AXIdentifier': 'IDC_FONTDLG_COLORPICKER_BORDER', 'AXRole': 'AXButton'}]

    btn_ok = [main_window, {'AXIdentifier': 'IDC_FONTDLG_BTN_OK', 'AXRole': 'AXButton'}]
    btn_apply_all = [main_window, {'AXIdentifier': 'IDC_FONTDLG_BTN_APPLYALL', 'AXRole': 'AXButton'}]

# Upper button
btn_add_subtitle = {'AXIdentifier': 'IDC_SUBTITLE_ROOM_BTN_ADD_MARKER', 'AXRole': 'AXButton'}
btn_del_subtitle = {'AXIdentifier': 'IDC_SUBTITLE_ROOM_BTN_DELETE_MARKER', 'AXRole': 'AXButton'}
btn_split = {'AXIdentifier': 'IDC_SUBTITLE_ROOM_BTN_SPLIT', 'AXRole': 'AXButton'}
btn_merge = {'AXIdentifier': 'IDC_SUBTITLE_ROOM_BTN_MERGE', 'AXRole': 'AXButton'}
btn_adjust_pos = {'AXIdentifier': 'IDC_SUBTITLE_ROOM_BTN_OFFSET', 'AXRole': 'AXButton'}
btn_change_format = {'AXIdentifier': 'IDC_SUBTITLE_ROOM_BTN_FONT', 'AXRole': 'AXButton'}
btn_more = {'AXIdentifier': 'IDC_SUBTITLE_ROOM_BTN_MORE', 'AXRole': 'AXButton'}
btn_i = {'AXIdentifier': 'IDC_SUBTITLE_ROOM_BTN_INFO', 'AXRole': 'AXButton'}

# scroll bar
scroll_bar = {'AXIdentifier': 'IDC_SUBTITLE_ROOM_VERTICAL_SCROLLBAR', 'AXRole': 'AXScrollBar'}

# search field
search_field = {'AXIdentifier': 'IDC_SUBTITLE_ROOM_SEARCHFIELD', 'AXRole': 'AXTextField'}
replace_txt_field = {'AXIdentifier': 'IDC_SUBTITLE_ROOM_REPLACE_TEXTFIELD', 'AXRole': 'AXTextField'}
cancel_button = [search_field, {'AXDescription': 'cancel', 'AXRole': 'AXButton'}]
btn_replace = {'AXIdentifier': 'IDC_SUBTITLE_ROOM_BTN_REPLACE', 'AXRole': 'AXButton'}
btn_replace_single = {'AXIdentifier': 'IDC_SUBTITLE_ROOM_BTN_REPLACE_SINGLE', 'AXRole': 'AXButton'}
btn_replace_all = {'AXIdentifier': 'IDC_SUBTITLE_ROOM_BTN_REPLACE_ALL', 'AXRole': 'AXButton'}
btn_next = {'AXIdentifier': 'IDC_SUBTITLE_ROOM_BTN_NEXT', 'AXRole': 'AXButton'}

# subtitle content (no. / Start Time / End Time / Subtitle Text)
class subtitle_region():
    main_content = [{'AXIdentifier': 'IDD_LIBRARY', 'AXRole': 'group'}, {'AXIdentifier': 'IDC_SUBTITLE_ROOM_SCROLLVIEW', 'AXRole': 'AXScrollArea', 'AXRoleDescription': 'scroll area'}]
    scroll_view = [main_content, {'AXIdentifier': 'IDC_SUBTITLE_ROOM_TABLEVIEW', 'AXRole': 'AXTable'}]
    rows_clip = [scroll_view, {"AXSubrole": "AXTableRow", "get_all": True, "recursive": False}]

# Subtitle Room button
btn_subtitle_room = {'AXIdentifier': 'IDC_LIBRARY_BTN_SUBTITLEROOM', 'AXRole': 'AXButton'}