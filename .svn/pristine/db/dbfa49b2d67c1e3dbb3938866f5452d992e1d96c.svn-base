
main_window = {'AXTitle': 'Preferences'}
content_frame = {'AXIdentifier': '_NS:450'} # hardcode_0427: Not Fix (_NS:443)
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
arrow_up = {'AXIdentifier': '_NS:9'} # for editbox, hardcode_0408: IDC_SPINEDIT_BTN_UP
arrow_down = {'AXIdentifier': '_NS:72'} # for editbox, hardcode_0408: IDC_SPINEDIT_BTN_DOWN
editbox_unit = {'AXIdentifier': 'spinEditTextField'}

class confirm_dialog():
    main_window = {'AXRoleDescription': 'dialog', 'AXTitle': 'CyberLink PowerDirector'}
    btn_ok = [main_window, {'AXRoleDescription': 'button', 'AXTitle': 'OK'}]

class general():
    input_text_maximum_undo_levels = [main_window, {'AXIdentifier': 'spinEditTextField'}]
    btn_maximum_undo_levels_up = [main_window, {'AXIdentifier': '_NS:9'}] # hardcode_0408: IDC_SPINEDIT_BTN_UP
    btn_maximum_undo_levels_down = [main_window, {'AXIdentifier': '_NS:72'}] # hardcode_0408: IDC_SPINEDIT_BTN_DOWN

    class audio_channels():
        btn_combobox = {'AXIdentifier': '_NS:96'} # hardcode_0408: IDC_PREF_COMBOBOX_AUDIOCHANNEL
        menu_item_stereo = {'AXValue': 'Stereo'}
        menu_item_51_surround = {'AXValue': '5.1 Surround'}

    class timeline_frame_rate():
        btn_combobox = {'AXIdentifier': '_NS:65'} # harcode_0408: IDC_PREF_COMBOBOX_FRAMERATE
        menu_item_24_fps = {'AXValue': '24 FPS (FILM)'}
        menu_item_25_fps = {'AXValue': '25 FPS (PAL)'}
        menu_item_30_fps = {'AXValue': '30 FPS (NTSC)'}
        menu_item_50_fps = {'AXValue': '50 FPS (PAL)'}
        menu_item_60_fps = {'AXValue': '60 FPS (NTSC)'}

    class use_drop_frame_timecode():
        btn_combobox = [main_window, {'AXIdentifier': '_NS:111'}]  # harcode_0408: IDC_PREF_COMBOBOX_DROPFRAMEMODE
        menu_item_yes = {'AXValue': 'Yes'}
        menu_item_no = {'AXValue': 'No'}

    chx_show_sound_waveform = [main_window, {'AXIdentifier': '_NS:129'}] # hardcode_0408: IDC_PREF_CHECKBOX_ENABLE_SHOWWAVEFORM
    chx_play_audio_while_scrubbing = [main_window, content_frame, {'AXIdentifier': '_NS:141'}] # hardcode_0408 (_NS:141): IDC_PREF_CHECKBOX_ENABLE_AUDIO_SCRUBBING
    chx_enable_continuous_thumbnail_on_video = [main_window, {'AXIdentifier': '_NS:150'}] # hardcode_0408: IDC_PREF_CHECKBOX_ENABLE_CONTINUE_THUMBNAIL
    chx_enable_shadow_file = [main_window, content_frame, {'AXIdentifier': '_NS:159'}] # hardcode_0408: IDC_PREF_CHECKBOX_ENABLE_SHADOWEDIT

    class shadow_file_resolution():
        btn_combobox = {'AXIdentifier': '_NS:180'}  # hardcode_0408: IDC_PREF_COMBOBOX_SHADOWEDIT
        menu_item_720_480 = {'AXValue': '720 x 480'}
        menu_item_1280_720 = {'AXValue': '1280 x 720'}
        menu_item_1920_1080 = {'AXValue': '1920 x 1080'}

    chx_render_preview_in_uhd_preview_quality = [main_window, content_frame, {'AXIdentifier': '_NS:196'}] # hardcode_0408: IDC_PREF_CHECKBOX_ENABLE_AUTO_CACHE
    chx_auto_delete_temporary_files = [main_window, content_frame, {'AXIdentifier': '_NS:203'}] # hardcode_0408: IDC_PREF_CHECKBOX_ENABLE_AUTO_DELETE

    class auto_delete_temporary_files():
        input_days = [main_window, content_frame, {'AXIdentifier': '_NS:214'}, {'AXIdentifier': 'spinEditTextField'}] # hardcode_0408: IDC_PREF_EDIT_DELETE_DAYS
        btn_days_arrow_up = [main_window, content_frame, {'AXIdentifier': '_NS:214'}, {'AXIdentifier': '_NS:9'}] # hardcode_0408: IDC_SPINEDIT_BTN_UP
        btn_days_arrow_down = [main_window, content_frame, {'AXIdentifier': '_NS:214'}, {'AXIdentifier': '_NS:72'}] # hardcode_0408: IDC_SPINEDIT_BTN_DOWN

    class language():
        chx_use_system_default = [main_window, content_frame, {'AXIdentifier': '_NS:284'}] # hardcode_0408: IDC_PREF_RADIO_SYSTEM_LANG
        chx_user_defined = [main_window, content_frame, {'AXIdentifier': '_NS:296'}] # hardcode_0408: IDC_PREF_RADIO_USER_DEFINE
        cbx_language = [main_window, content_frame, {'AXIdentifier': '_NS:309'}] # hardcode_0408: IDC_PREF_COMBO_LANGUAGE
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
        cbx_default_transition_behavior = [main_window, content_frame, {'AXIdentifier': '_NS:43'}] # hardcode_0408: IDC_TRANSITION_TYPE_COMBOBOX
        option_overlap = {'AXRoleDescription': 'text', 'AXValue': 'Overlap'}
        option_cross = {'AXRoleDescription': 'text', 'AXValue': 'Cross'}
        chx_return_to_beginning_of_video_after_preview = [main_window, content_frame, {'AXIdentifier': '_NS:93'}] # hardcode_0408: IDC_PREF_CHECKBOX_ENABLE_RETURN_TO_BEGIN
        chx_reverse_timeline_track_order = [main_window, content_frame, {'AXIdentifier': '_NS:129'}] # hardcode_0408: IDC_PREF_CHECKBOX_ENABLE_TIMELINE_REVERSE
        chx_add_transition_between_photos = [main_window, content_frame, {'AXIdentifier': '_NS:59'}] # hardcode_0427: IDC_PREF_CHECKBOX_ADDCROSSFADE
        option_cross_fade = {'AXRoleDescription': 'text', 'AXValue': 'Cross Fade'}
        option_my_favorite = {'AXRoleDescription': 'text', 'AXValue': 'My Favorite'}
        cbx_transition_type = [main_window, content_frame, {'AXIdentifier': '_NS:78'}] # hardcode_0427: IDC_PREF_COMBOBOX_TRANSITION

    class duration():
        editbox_image_files_parent = [main_window, content_frame, {'AXIdentifier': '_NS:187'}] # hardcode_0408: IDC_PREF_EDIT_IMAGE_FILES
        editbox_transitions_parent = [main_window, content_frame, {'AXIdentifier': '_NS:212'}] # hardcode_0408: IDC_PREF_EDIT_TRANSITION
        editbox_title_parent = [main_window, content_frame, {'AXIdentifier': '_NS:245'}] # hardcode_0408: IDC_PREF_EDIT_TITLE
        editbox_effect_parent = [main_window, content_frame, {'AXIdentifier': '_NS:270'}] # hardcode_0408: IDC_PREF_EDIT_EFFECT
        editbox_subtitle_parent = [main_window, content_frame, {'AXIdentifier': '_NS:295'}] # hardcode_0408: IDC_PREF_EDIT_SUBTITLE


class file():
    class default_locations():
        editbox_import_folder = [main_window, content_frame, {'AXIdentifier': '_NS:45'}]  # hardcode_0408: IDC_PREF_EDIT_IMPORT_DIR
        editbox_export_folder = [main_window, content_frame, {'AXIdentifier': '_NS:93'}]  # hardcode_0408: IDC_PREF_EDIT_EXPORT_DIR
        btn_import_folder_browse = [main_window, content_frame, {'AXIdentifier': '_NS:62'}]  # hardcode_0408: IDC_PREF_BUTTON_IMPORT_DIR
        btn_export_folder_browse = [main_window, content_frame, {'AXIdentifier': '_NS:104'}]  # hardcode_0408: IDC_PREF_BUTTON_EXPORT_DIR

    class file_name():
        editbox_snapshot_filename = [main_window, content_frame, {'AXIdentifier': '_NS:145'}]  # hardcode_0408: IDC_PREF_EDIT_SNAP_DEFAULT_NAME
        cbx_snapshot_filename_extension = [main_window, content_frame, {'AXIdentifier': '_NS:153'}]  # hardcode_0408: IDC_PREF_COMBOBOX_SNAPSHOT_NAME
        cbx_snapshot_destination = [main_window, content_frame, {'AXIdentifier': '_NS:188'}]  # hardcode_0408: IDC_PREF_COMBOBOX_SNAPSHOT_FORMAT
        option_file_ext_bmp = {'AXRoleDescription': 'text', 'AXValue': '.bmp'}
        option_file_ext_jpg = {'AXRoleDescription': 'text', 'AXValue': '.jpg'}
        option_file_ext_gif = {'AXRoleDescription': 'text', 'AXValue': '.gif'}
        option_file_ext_png = {'AXRoleDescription': 'text', 'AXValue': '.png'}
        option_snapshot_destination_file = {'AXRoleDescription': 'text', 'AXValue': 'File'}
        option_snapshot_destination_clipboard = {'AXRoleDescription': 'text', 'AXValue': 'Clipboard'}


class display():
    cbx_timeline_preview_quality = [main_window, content_frame, {'AXIdentifier': '_NS:38'}]  # hardcode_0408: IDC_PREF_COMBOBOX_PREVIEW_QUALITY
    chx_snap_to_reference_lines = [main_window, content_frame, {'AXIdentifier': '_NS:86'}]  # hardcode_0408: IDC_PREF_CHECKBOX_SNAP_TO_REFERENCE
    cbx_grid_lines = [main_window, content_frame, {'AXIdentifier': '_NS:105'}]  # hardcode_0408: IDC_PREF_COMBOBOX_GRID_LINES
    option_timeline_preview_quality_ultra_hd = {'AXRoleDescription': 'text', 'AXValue': 'Ultra HD Preview Resolution'}
    option_timeline_preview_quality_full_hd = {'AXRoleDescription': 'text', 'AXValue': 'Full HD Preview Resolution'}
    option_timeline_preview_quality_hd = {'AXRoleDescription': 'text', 'AXValue': 'HD Preview Resolution'}
    option_timeline_preview_quality_high = {'AXRoleDescription': 'text', 'AXValue': 'High Preview Resolution'}
    option_timeline_preview_quality_normal = {'AXRoleDescription': 'text', 'AXValue': 'Normal Preview Resolution'}
    option_timeline_preview_quality_low = {'AXRoleDescription': 'text', 'AXValue': 'Low Preview Resolution'}
    option_grid_lines_unit = {'AXRoleDescription': 'text', 'AXValue': ''}


class project():
    editbox_numbers_of_recently_used_projects_parent = [main_window, content_frame, {'AXIdentifier': '_NS:43'}] # hardcode_0408: IDC_PREF_EDIT_RECENT_FILE_SPIN
    chx_auto_load_the_last_project = [main_window, content_frame, {'AXIdentifier': '_NS:52'}]  # hardcode_0408: IDC_PREF_CHECKBOX_AUTOLOAD
    chx_auto_load_sample_clips = [main_window, content_frame, {'AXIdentifier': '_NS:69'}]  # hardcode_0408: IDC_PREF_CHECKBOX_AUTOLOADSAMPLECLIPS


class confirmation():
    btn_reset = [main_window, content_frame, {'AXIdentifier': '_NS:9'}] # hardcode_0408: IDC_PREF_CONFIRM_RESET


class director_zone():
    editbox_email = [main_window, content_frame, {'AXIdentifier': '_NS:86'}]  # hardcode_0408: IDC_PREF_DZ_EMAIL
    editbox_password = [main_window, content_frame, {'AXIdentifier': '_NS:40'}]  # hardcode_0408: IDC_PREF_DZ_PASSWORD
    btn_sign_in = [main_window, content_frame, {'AXIdentifier': '_NS:252', 'AXTitle': 'Sign in'}]  # hardcode_0408: IDC_PREF_BUTTON_LOG_IN
    btn_sign_out = [main_window, content_frame, {'AXIdentifier': '_NS:252', 'AXTitle': 'Sign out'}]  # hardcode_0408: IDC_PREF_BUTTON_LOG_IN
    chx_auto_sign_in = [main_window, content_frame, {'AXIdentifier': '_NS:204'}]  # hardcode_0408: IDC_STATIC_DIRECTORZONE_SIGNIN
    lnk_template_upload_to_dz = [main_window, content_frame, {'AXIdentifier': '_NS:128'}]  # hardcode_0408: IDC_PREF_STATIC_DZ_UPLOADED_LINK
    lnk_template_download_from_dz = [main_window, content_frame, {'AXIdentifier': '_NS:135'}]  # hardcode_0408: IDC_PREF_STATIC_DZ_DOWNLOADED_LINK


class cyberlink_cloud:
    editbox_download_folder = [main_window, content_frame, {'AXIdentifier': '_NS:53'}]  # hardcode_0408: IDC_PREF_CHOOSE_DOWNLOAD_FOLDER
    btn_browse = [main_window, content_frame, {'AXIdentifier': '_NS:249'}]  # hardcode_0408: IDC_PREF_BTN_DOWNLOAD_DIR
    lnk_account_info = [main_window, content_frame, {'AXIdentifier': '_NS:223'}]  # hardcode_0427: IDC_PREF_STATIC_ACCOUNT_INFO