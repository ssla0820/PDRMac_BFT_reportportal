
top_toolbar = {'AXRole': 'AXToolbar'}
top_project_name = [top_toolbar, {'AXRole': 'AXStaticText'}]
btn_produce = [top_toolbar, {'AXRole': 'AXButton', 'index': 0}]
btn_edit = [top_toolbar, {'AXRole': 'AXButton', 'index': 0}]
btn_undo = [top_toolbar, {'AXRole': 'AXButton', 'index': 1}]
btn_redo = [top_toolbar, {'AXRole': 'AXButton', 'index': 2}]
btn_set_user_preferences = [top_toolbar, {'AXRole': 'AXButton', 'index': 5}]
btn_library_icon_view = {'AXIdentifier': 'IDC_LIBRARY_BTN_ICON_VIEW'}
btn_library_details_view = {'AXIdentifier': 'IDC_LIBRARY_BTN_DETAILS_VIEW'}
btn_project_aspect_ratio = {'AXIdentifier': 'IDC_DISPLAY_BTN_ASPECTRATIO'}

class top_menu_bar():
    btn_file = {'AXRoleDescription': 'menu bar item', 'AXTitle': 'File'}
    btn_plugins = {'AXRoleDescription': 'menu bar item', 'AXTitle': 'Plugins'}
    btn_view = {'AXRoleDescription': 'menu bar item', 'AXTitle': 'View'}
    option_open_project = 'Open Project...'
    option_import_media_files = eval("'Import', 'Media Files...'")
    option_import_media_folder = eval("'Import', 'Media Folder...'")
    option_new_project = 'New Project'
    option_save_project_as = 'Save Project As...'
    option_open_recent_projects = 'Open Recent Projects'
    option_import_media_from_cyberlink_cloud = eval("'Import', 'Download Media from CyberLink Cloud...'")
    option_video_collage_designer = 'Video Collage Designer'
    option_show_library_preview_window = 'Show Library Preview Window'
    option_show_timeline_preview_volume_meter = 'Show Timeline Preview Volume Meter'
    option_pack_project_materials = 'Pack Project Materials...'

class room_entry():
    btn_media_room = {'AXIdentifier': 'IDC_LIBRARY_BTN_MEDIAROOM'}
    btn_title_room = {'AXIdentifier': 'IDC_LIBRARY_BTN_TITLEROOM'}
    btn_transition_room = {'AXIdentifier': 'IDC_LIBRARY_BTN_TRANSITIONROOM'}
    btn_effect_room = {'AXIdentifier': 'IDC_LIBRARY_BTN_EFFECTROOM'}
    btn_pip_room = {'AXIdentifier': 'IDC_LIBRARY_BTN_PIPROOM'}
    btn_particle_room = {'AXIdentifier': 'IDC_LIBRARY_BTN_PARTICLEROOM'}
    btn_audio_mixing_room = {'AXIdentifier': 'IDC_LIBRARY_BTN_AUDIOMIXINGROOM'}
    btn_more = {'AXIdentifier': 'IDC_LIBRARY_BTN_MORE'} #v2529: _NS:886
    btn_voice_over_room = {'AXIdentifier': 'menuVoiceOver'}
    btn_subtitle_room = {'AXIdentifier': 'menuSubtitle'}

class activate_dialog():
    btn_activate = {'AXIdentifier': '_NS:78'} # skip hardcode, normal run will have a specific account

class tips_area():
    btn_insert_to_selected_track = {'AXIdentifier': 'IDC_TIPSAREA_BTN_ADDTOVIDEOTRACK'}
    btn_tools = {'AXIdentifier': 'IDC_TIPSAREA_BTN_TOOLS'}
    menu_pip_designer = {'AXIdentifier': 'IDM_TIPSAREA_PIP_DESIGNER'}
    btn_designer = {'AXIdentifier': 'IDC_TIPSAREA_BTN_TITLE_DESIGNER'}
    btn_fix_enhance = {'AXIdentifier': 'IDC_TIPSAREA_BTN_FIX_ENHANCE'}
    btn_key_frame = {'AXIdentifier': 'IDC_TIPSAREA_BTN_KEYFRAME'}
    btn_more_feature = {'AXIdentifier': 'IDC_TIPSAREA_BTN_MORE_FEATURE'}
    btn_split = {'AXIdentifier': 'IDC_TIPSAREA_BTN_SPLIT'}
    btn_set_length_of_selected_clip = {'AXIdentifier': 'IDC_TIPSAREA_BTN_DURATION'}
    btn_video_collage = {'AXTitle': 'Video Collage'}
    btn_add_to_effect_track = {'AXIdentifier': 'IDC_TIPSAREA_BTN_ADDTOEFFECTTRACK'}

class timeline():
    table_view = {'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK'}
    track_unit = [table_view, {'AXRoleDescription': 'table row'}]
    indicator = {'AXDescription': 'timeline indicator n'}
    clip_name_unit = {'AXIdentifier': '_NS:66'} # Not Fix

class duration_setting_dialog():
    txt_duration = {'AXIdentifier': 'spinTimeEditTextField'}
    btn_ok = {'AXIdentifier': 'IDC_DURATION_BTN_OK'}

class library_preview_window():
    slider = {'AXRole': 'AXSlider', 'AXIdentifier': 'IDC_SELECTSLIDER_SLIDER'} #v2529: _NS:12
    txt_time_code = {'AXIdentifier': 'spinTimeEditTextField', 'index': 0}

class save_file_dialog():
    main_window = {'AXTitle': 'Save file'}
    input_save_as = [main_window, {'AXRole': 'AXTextField', 'index': 0}]
    btn_pop_up = [main_window, {'AXRole': 'AXPopUpButton'}]
    btn_save = [main_window, {'AXRoleDescription': 'button', 'AXTitle': 'Save'}]
    btn_replace = {'AXTitle': 'Replace'}
    btn_show_more_options = [main_window, {'AXIdentifier': 'NS_OPEN_SAVE_DISCLOSURE_TRIANGLE'}]
    input_search = [{'AXTitle': 'Save file'}, {'AXRoleDescription': 'search text field'}]

class save_as_file_dialog():
    main_window = {'AXTitle': 'Save As'}
    input_save_as = [main_window, {'AXRoleDescription': 'text field', 'index': 0}]
    btn_pop_up = [main_window, {'AXRole': 'AXPopUpButton'}]
    btn_save = [main_window, {'AXRoleDescription': 'button', 'AXTitle': 'Save'}]
    btn_replace = {'AXTitle': 'Replace'}
    btn_show_more_options = [main_window, {'AXIdentifier': 'NS_OPEN_SAVE_DISCLOSURE_TRIANGLE'}]
    input_search = [main_window, {'AXRoleDescription': 'search text field'}]

class open_file_dialog():
    main_window = {'AXRoleDescription': 'sheet', 'AXDescription': 'open'}
    btn_open = [main_window, {'AXTitle': 'Open'}]
    column_view_frame = [main_window, {'AXIdentifier': 'ColumnView'}]
    btn_change_items_grouping = [main_window, {'AXRoleDescription': 'menu button'}]

class merge_media_to_library_dialog():
    btn_yes = {'AXTitle': 'Yes'}
    btn_no = {'AXTitle': 'No'}
    btn_cancel = {'AXTitle': 'Cancel'}
    chx_do_not_show_again = {'AXTitle': 'Don\'t show again'}

class download_media_dialog():
    title = {'AXValue': 'Download Media'}

class serious_frame_drop_decteced_dialog():
    main_window = {'AXTitle': 'CyberLink PowerDirector'}
    description = [main_window, {'AXIdentifier': '_NS:34'}] # Not Fix
    btn_yes = [main_window, {'AXTitle': 'Yes'}]