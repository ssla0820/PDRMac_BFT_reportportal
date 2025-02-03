
main_window = {'AXTitle': 'Preferences'}
#content_frame = {'AXIdentifier': '_NS:378'} # hardcode_0427: Not Fix (_NS:443), v2529: _NS:450 # v2922
content_frame = {'AXIdentifier': 'IDC_PREF_MAIN_TAB_VIEW'}  # v3004
btn_ok = [main_window, {'AXTitle': 'OK'}]
btn_cancel = [main_window, {'AXTitle': 'Cancel'}]
btn_close = [main_window, {'AXRoleDescription': 'close button'}]
tab_general = [main_window, {'AXTitle': 'General'}]
tab_editing = [main_window, {'AXTitle': 'Editing'}]
tab_file = [main_window, {'AXTitle': 'File'}]
tab_display = [main_window, {'AXTitle': 'Display'}]
tab_project = [main_window, {'AXTitle': 'Project'}]
tab_confirmation = [main_window, {'AXTitle': 'Confirmation'}]
tab_director_zone = [main_window, {'AXTitle': 'DirectorZone'}]
tab_cyberlink_cloud = [main_window, {'AXTitle': 'CyberLink Cloud'}]
arrow_up = {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP'} # for editbox, hardcode_0408: IDC_SPINEDIT_BTN_UP, v2529: _NS:9
arrow_down = {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN'} # for editbox, hardcode_0408: IDC_SPINEDIT_BTN_DOWN, v2529: _NS:72
editbox_unit = {'AXIdentifier': 'spinEditTextField'}

class confirm_dialog():
    main_window = {'AXRoleDescription': 'dialog', 'AXTitle': 'CyberLink PowerDirector'}
    btn_ok = [main_window, {'AXRoleDescription': 'button', 'AXTitle': 'OK'}]

class general():
    input_text_maximum_undo_levels = [main_window, {'AXIdentifier': 'spinEditTextField'}]
    btn_maximum_undo_levels_up = [main_window, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP'}] # hardcode_0408: IDC_SPINEDIT_BTN_UP, v2529: _NS:9
    btn_maximum_undo_levels_down = [main_window, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN'}] # hardcode_0408: IDC_SPINEDIT_BTN_DOWN, v2529: _NS:72

    class audio_channels():
        btn_combobox = {'AXIdentifier': 'IDC_PREF_COMBOBOX_AUDIOCHANNEL'} # hardcode_0408: IDC_PREF_COMBOBOX_AUDIOCHANNEL, v2529: _NS:96
        menu_item_stereo = {'AXValue': 'Stereo'}
        menu_item_51_surround = {'AXValue': '5.1 Surround'}

    class timeline_frame_rate():
        btn_combobox = {'AXIdentifier': 'IDC_PREF_COMBOBOX_FRAMERATE'} # harcode_0408: IDC_PREF_COMBOBOX_FRAMERATE, v2529: _NS:65
        menu_item_24_fps = {'AXValue': '24 FPS (FILM)'}
        menu_item_25_fps = {'AXValue': '25 FPS (PAL)'}
        menu_item_30_fps = {'AXValue': '30 FPS (NTSC)'}
        menu_item_50_fps = {'AXValue': '50 FPS (PAL)'}
        menu_item_60_fps = {'AXValue': '60 FPS (NTSC)'}

    class use_drop_frame_timecode():
        btn_combobox = [main_window, {'AXIdentifier': 'IDC_PREF_COMBOBOX_DROPFRAMEMODE'}]  # harcode_0408: IDC_PREF_COMBOBOX_DROPFRAMEMODE, v2529: _NS:111
        menu_item_yes = {'AXValue': 'Yes'}
        menu_item_no = {'AXValue': 'No'}

    chx_show_sound_waveform = [main_window, {'AXIdentifier': 'IDC_PREF_CHECKBOX_ENABLE_SHOWWAVEFORM'}] # hardcode_0408: IDC_PREF_CHECKBOX_ENABLE_SHOWWAVEFORM, v2529: _NS:129
    chx_play_audio_while_scrubbing = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_CHECKBOX_ENABLE_AUDIO_SCRUBBING'}] # hardcode_0408 (_NS:141): IDC_PREF_CHECKBOX_ENABLE_AUDIO_SCRUBBING, v2529: _NS:141
    chx_enable_continuous_thumbnail_on_video = [main_window, {'AXIdentifier': 'IDC_PREF_CHECKBOX_ENABLE_CONTINUE_THUMBNAIL'}] # hardcode_0408: IDC_PREF_CHECKBOX_ENABLE_CONTINUE_THUMBNAIL, v2529: _NS:150
    chx_enable_shadow_file = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_CHECKBOX_ENABLE_SHADOWEDIT'}] # hardcode_0408: IDC_PREF_CHECKBOX_ENABLE_SHADOWEDIT, v2529: _NS:159

    class shadow_file_resolution():
        btn_combobox = {'AXIdentifier': 'IDC_PREF_COMBOBOX_SHADOWEDIT'}  # hardcode_0408: IDC_PREF_COMBOBOX_SHADOWEDIT, v2529: _NS:180
        menu_item_720_480 = {'AXValue': '720 x 480'}
        menu_item_1280_720 = {'AXValue': '1280 x 720'}
        menu_item_1920_1080 = {'AXValue': '1920 x 1080'}

    chx_render_preview_in_uhd_preview_quality = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_CHECKBOX_ENABLE_AUTO_CACHE'}] # hardcode_0408: IDC_PREF_CHECKBOX_ENABLE_AUTO_CACHE, v2529: _NS:196
    chx_auto_delete_temporary_files = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_CHECKBOX_ENABLE_AUTO_DELETE'}] # hardcode_0408: IDC_PREF_CHECKBOX_ENABLE_AUTO_DELETE, v2529: _NS:203
    btn_manually_delete = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_BUTTON_MANUAL_DELETE'}]

    class auto_delete_temporary_files():
        input_days = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_EDIT_DELETE_DAYS'}, {'AXIdentifier': 'spinEditTextField'}] # hardcode_0408: IDC_PREF_EDIT_DELETE_DAYS, v2529: _NS:214
        btn_days_arrow_up = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_EDIT_DELETE_DAYS'}, {'AXIdentifier': 'IDC_SPINEDIT_BTN_UP'}] # hardcode_0408: IDC_PREF_EDIT_DELETE_DAYS, IDC_SPINEDIT_BTN_UP, v2529: _NS: 214, _NS:9
        btn_days_arrow_down = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_EDIT_DELETE_DAYS'}, {'AXIdentifier': 'IDC_SPINEDIT_BTN_DOWN'}] # hardcode_0408: IDC_PREF_EDIT_DELETE_DAYS, IDC_SPINEDIT_BTN_DOWN, v2529: _NS:214, _NS:72

    class language():
        chx_use_system_default = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_RADIO_SYSTEM_LANG'}] # hardcode_0408: IDC_PREF_RADIO_SYSTEM_LANG, v2529: _NS:284
        chx_user_defined = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_RADIO_USER_DEFINE'}] # hardcode_0408: IDC_PREF_RADIO_USER_DEFINE, v2529: _NS:296
        cbx_language = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_COMBO_LANGUAGE'}] # hardcode_0408: IDC_PREF_COMBO_LANGUAGE, v2529: _NS:309
        option_language_deu = {'AXRoleDescription': 'text', 'AXValue': 'Deutsch'}
        option_language_eng = {'AXRoleDescription': 'text', 'AXValue': 'English'}
        option_language_esp = {'AXRoleDescription': 'text', 'AXValue': 'español'}
        option_language_fra = {'AXRoleDescription': 'text', 'AXValue': 'français'}
        option_language_ita = {'AXRoleDescription': 'text', 'AXValue': 'italiano'}
        option_language_nld = {'AXRoleDescription': 'text', 'AXValue': 'Nederlands'}
        option_language_chs = {'AXRoleDescription': 'text', 'AXValue': '中文(简体)'}
        option_language_cht = {'AXRoleDescription': 'text', 'AXValue': '中文(繁體)'}
        option_language_jpn = {'AXRoleDescription': 'text', 'AXValue': '日本語'}
        option_language_kor = {'AXRoleDescription': 'text', 'AXValue': '한국어'}


class editing():
    class timeline():
        cbx_default_transition_behavior = [main_window, content_frame, {'AXIdentifier': 'IDC_TRANSITION_TYPE_COMBOBOX'}] # hardcode_0408: IDC_TRANSITION_TYPE_COMBOBOX, v2529: _NS:43
        option_overlap = {'AXRoleDescription': 'text', 'AXValue': 'Overlap'}
        option_cross = {'AXRoleDescription': 'text', 'AXValue': 'Cross'}
        chx_return_to_beginning_of_video_after_preview = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_CHECKBOX_ENABLE_RETURN_TO_BEGIN'}] # hardcode_0408: IDC_PREF_CHECKBOX_ENABLE_RETURN_TO_BEGIN, v2529: _NS:93
        chx_reverse_timeline_track_order = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_CHECKBOX_ENABLE_TIMELINE_REVERSE'}] # hardcode_0408: IDC_PREF_CHECKBOX_ENABLE_TIMELINE_REVERSE, v2529: _NS:129
        chx_add_transition_between_photos = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_CHECKBOX_ADDCROSSFADE'}] # hardcode_0427: IDC_PREF_CHECKBOX_ADDCROSSFADE, v2529: _NS:59
        option_cross_fade = {'AXRoleDescription': 'text', 'AXValue': 'Cross Fade'}
        option_my_favorite = {'AXRoleDescription': 'text', 'AXValue': 'My Favorite'}
        cbx_transition_type = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_COMBOBOX_TRANSITION'}] # hardcode_0427: IDC_PREF_COMBOBOX_TRANSITION, v2529: _NS:78
        cbx_insert_project_behavior = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_COMBOBOX_INSERTPROJECT'}]
        option_nested = {'AXRoleDescription': 'text', 'AXValue': 'As Nested Project'}
        option_expanded = {'AXRoleDescription': 'text', 'AXValue': 'As Expanded Project'}

    class duration():
        editbox_image_files_parent = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_EDIT_IMAGE_FILES'}] # hardcode_0408: IDC_PREF_EDIT_IMAGE_FILES, v2529: _NS:187
        editbox_transitions_parent = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_EDIT_TRANSITION'}] # hardcode_0408: IDC_PREF_EDIT_TRANSITION, v2529: _NS:212
        editbox_title_parent = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_EDIT_TITLE'}] # hardcode_0408: IDC_PREF_EDIT_TITLE, v2529: _NS:245
        editbox_effect_parent = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_EDIT_EFFECT'}] # hardcode_0408: IDC_PREF_EDIT_EFFECT, v2529: _NS:270
        editbox_subtitle_parent = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_EDIT_SUBTITLE'}] # hardcode_0408: IDC_PREF_EDIT_SUBTITLE, v2529: _NS:295


class file():
    class default_locations():
        editbox_import_folder = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_EDIT_IMPORT_DIR'}]  # hardcode_0408: IDC_PREF_EDIT_IMPORT_DIR, v2529: _NS:45
        editbox_export_folder = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_EDIT_EXPORT_DIR'}]  # hardcode_0408: IDC_PREF_EDIT_EXPORT_DIR, v2529: _NS:93
        btn_import_folder_browse = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_BUTTON_IMPORT_DIR'}]  # hardcode_0408: IDC_PREF_BUTTON_IMPORT_DIR, v2529: _NS:62
        btn_export_folder_browse = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_BUTTON_EXPORT_DIR'}]  # hardcode_0408: IDC_PREF_BUTTON_EXPORT_DIR, v2529: _NS:104

    class file_name():
        editbox_snapshot_filename = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_EDIT_SNAP_DEFAULT_NAME'}]  # hardcode_0408: IDC_PREF_EDIT_SNAP_DEFAULT_NAME, v2529: _NS:145
        cbx_snapshot_filename_extension = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_COMBOBOX_SNAPSHOT_NAME'}]  # hardcode_0408: IDC_PREF_COMBOBOX_SNAPSHOT_NAME, v2529: _NS:153
        cbx_snapshot_destination = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_COMBOBOX_SNAPSHOT_FORMAT'}]  # hardcode_0408: IDC_PREF_COMBOBOX_SNAPSHOT_FORMAT, v2529: _NS:188
        option_file_ext_bmp = {'AXRoleDescription': 'text', 'AXValue': '.bmp'}
        option_file_ext_jpg = {'AXRoleDescription': 'text', 'AXValue': '.jpg'}
        option_file_ext_gif = {'AXRoleDescription': 'text', 'AXValue': '.gif'}
        option_file_ext_png = {'AXRoleDescription': 'text', 'AXValue': '.png'}
        option_snapshot_destination_file = {'AXRoleDescription': 'text', 'AXValue': 'File'}
        option_snapshot_destination_clipboard = {'AXRoleDescription': 'text', 'AXValue': 'Clipboard'}


class display():
    cbx_timeline_preview_quality = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_COMBOBOX_PREVIEW_QUALITY'}]  # hardcode_0408: IDC_PREF_COMBOBOX_PREVIEW_QUALITY, v2529: _NS:38
    chx_snap_to_reference_lines = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_CHECKBOX_SNAP_TO_REFERENCE'}]  # hardcode_0408: IDC_PREF_CHECKBOX_SNAP_TO_REFERENCE, v2529: _NS:86
    cbx_grid_lines = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_COMBOBOX_GRID_LINES'}]  # hardcode_0408: IDC_PREF_COMBOBOX_GRID_LINES, v2529: _NS:105
    option_timeline_preview_quality_ultra_hd = {'AXRoleDescription': 'text', 'AXValue': 'Ultra HD Preview Resolution'}
    option_timeline_preview_quality_full_hd = {'AXRoleDescription': 'text', 'AXValue': 'Full HD Preview Resolution'}
    option_timeline_preview_quality_hd = {'AXRoleDescription': 'text', 'AXValue': 'HD Preview Resolution'}
    option_timeline_preview_quality_high = {'AXRoleDescription': 'text', 'AXValue': 'High Preview Resolution'}
    option_timeline_preview_quality_normal = {'AXRoleDescription': 'text', 'AXValue': 'Normal Preview Resolution'}
    option_timeline_preview_quality_low = {'AXRoleDescription': 'text', 'AXValue': 'Low Preview Resolution'}
    option_grid_lines_unit = {'AXRoleDescription': 'text', 'AXValue': ''}


class project():
    editbox_numbers_of_recently_used_projects_parent = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_EDIT_RECENT_FILE_SPIN'}] # hardcode_0408: IDC_PREF_EDIT_RECENT_FILE_SPIN, v2529: _NS:43
    chx_auto_load_the_last_project = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_CHECKBOX_AUTOLOAD'}]  # hardcode_0408: IDC_PREF_CHECKBOX_AUTOLOAD, v2529: _NS:52
    chx_auto_load_sample_clips = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_CHECKBOX_AUTOLOADSAMPLECLIPS'}]  # hardcode_0408: IDC_PREF_CHECKBOX_AUTOLOADSAMPLECLIPS, v2529: _NS:69


class confirmation():
    btn_reset = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_CONFIRM_RESET'}] # hardcode_0408: IDC_PREF_CONFIRM_RESET, v2529: _NS:9


class director_zone():
    editbox_email = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_DZ_EMAIL'}]  # hardcode_0408: IDC_PREF_DZ_EMAIL, v2529: _NS:86
    editbox_password = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_DZ_PASSWORD'}]  # hardcode_0408: IDC_PREF_DZ_PASSWORD, v2529: _NS:40
    btn_sign_in = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_BUTTON_LOG_IN', 'AXTitle': 'Sign in'}]  # hardcode_0408: IDC_PREF_BUTTON_LOG_IN, v2529: _NS:252
    btn_sign_out = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_BUTTON_LOG_IN', 'AXTitle': 'Sign out'}]  # hardcode_0408: IDC_PREF_BUTTON_LOG_IN, v2529: _NS:252
    chx_auto_sign_in = [main_window, content_frame, {'AXIdentifier': 'IDC_STATIC_DIRECTORZONE_SIGNIN'}]  # hardcode_0408: IDC_STATIC_DIRECTORZONE_SIGNIN, v2529: _NS:204
    lnk_template_upload_to_dz = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_STATIC_DZ_UPLOADED_LINK'}]  # hardcode_0408: IDC_PREF_STATIC_DZ_UPLOADED_LINK, v2529: _NS:128
    lnk_template_download_from_dz = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_STATIC_DZ_DOWNLOADED_LINK'}]  # hardcode_0408: IDC_PREF_STATIC_DZ_DOWNLOADED_LINK, v2529: _NS:135


class cyberlink_cloud:
    editbox_download_folder = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_CHOOSE_DOWNLOAD_FOLDER'}]  # hardcode_0408: IDC_PREF_CHOOSE_DOWNLOAD_FOLDER, v2529: _NS:53
    btn_browse = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_BTN_DOWNLOAD_DIR'}]  # hardcode_0408: IDC_PREF_BTN_DOWNLOAD_DIR, v2529: _NS:249
    lnk_account_info = [main_window, content_frame, {'AXIdentifier': 'IDC_PREF_STATIC_ACCOUNT_INFO'}]  # hardcode_0427: IDC_PREF_STATIC_ACCOUNT_INFO, v2529: _NS:223

class alert_dialog:
    main = {'AXIdentifier': 'IDD_CLALERT'}
    btn_yes = [main, {'AXIdentifier': 'IDC_CLALERT_BUTTON_0'}]