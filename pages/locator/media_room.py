
btn_import_media = {'AXIdentifier': 'IDC_LIBRARY_BTN_IMPORT_MEDIA'}
btn_create_new_color_board = {'AXIdentifier': 'IDC_LIBRARY_BTN_NEWCOLORBOARD'} # hardcoard_0427: IDC_LIBRARY_BTN_NEWCOLORBOARD, v2529: _NS:914
string_use_sample_media = {'AXValue': 'use sample media.'}
string_on_boarding_blue_bubble_media = {'AXValue': 'Browse all the titles, transitions, effects, PiP, and particles, and easily drag and drop to apply to your clips.', "AXRole": "AXStaticText"}
string_on_boarding_blue_bubble_tooltip = {'AXValue': 'Customize your clips with advanced tools, and solve white balance, color match, and other quality problems.', "AXRole": "AXStaticText"}

color_board_window = {'AXTitle': 'Colors'}
btn_color_sliders = {'AXDescription': 'Color Sliders'}
btn_color_palettes = {'AXDescription': 'Color Palettes'}
slider_category = {'AXIdentifier': '_NS:156'}
slider_category_items = [slider_category, {"AXRole": "AXMenuItem", "get_all": True}]
input_color_palettes_search = {'AXIdentifier': '_NS:104'}
color_palettes_category = {'AXIdentifier': '_NS:180'}
color_palettes_category_items = [color_palettes_category, {"AXRole": "AXMenuItem", "get_all": True}]
color_palettes_scroll_area = {'AXIdentifier': '_NS:9'}
color_palettes_scroll_area_items = [color_palettes_scroll_area, {"AXRole": "AXTextField", "get_all": True}]

tag_media_content = {'AXValue': 'Media Content'}
tag_color_boards = {'AXValue': 'Color Boards'}
tag_background_music_CL = {'AXValue': 'Background Music'}
tag_background_music = {'AXValue': 'Background Music (Meta)'}
tag_background_music_soundstripe = {'AXValue': 'Background Music (Soundstripe)'}
tag_sound_clips = {'AXValue': 'Sound Effects'}
tag_downloaded = {'AXValue': 'Downloads'}
btn_add_new_tag = {'AXIdentifier': 'IDC_LIBRARY_BTN_ADD_TAG'} # hardcode_0427: IDC_LIBRARY_BTN_ADD_TAG, v2529: _NS:12
input_new_tag = {'AXIdentifier': 'RoomTagTextField', 'AXFocused': True}
btn_delete_tag = {'AXIdentifier': 'IDC_LIBRARY_BTN_DELETE_TAG'} # hardcode_0427: IDC_LIBRARY_BTN_DELETE_TAG, v2529: _NS:33
tag_scroll_view_frame = {'AXIdentifier': 'IDC_LIBRARY_ROOM_TAG_TABLEVIEW'} # hardcode_0427: IDC_LIBRARY_ROOM_TAG_TABLEVIEW, the custom tag scrll view frame, v2529: _NS:206
tag_main_frame = {'AXIdentifier': 'IDC_LIBRARY_DEFAULT_TAG_TABLEVIEW'} # hardcode_0427: IDC_LIBRARY_DEFAULT_TAG_TABLEVIEW, parent frame of default tag (e.g. Media Content, Color Boards), v2529: _NS:63 (default tag parent frame)
unit_tag_room_text_field = {'AXIdentifier': 'RoomTagTextField'} # the general identifier of tag_room e.g. Media Content
unit_tag_room_bgm_text_field = [tag_scroll_view_frame, {'AXIdentifier': 'RoomTagTextField'}] # the general identifier of tag_room if enter BGM/ Sound Clips
unit_main_tag_text_field = [tag_main_frame, unit_tag_room_text_field]
unit_custom_tag_text_field = [tag_scroll_view_frame, unit_tag_room_text_field]
btn_media_filter_all = {'AXIdentifier': 'IDC_LIBRARY_BTN_FILTER_ALL'}
btn_media_filter_display_video_only = {'AXIdentifier': 'IDC_LIBRARY_BTN_FILTER_VIDEO'}
btn_media_filter_display_image_only = {'AXIdentifier': 'IDC_LIBRARY_BTN_FILTER_IMAGE'}
btn_media_filter_display_audio_only = {'AXIdentifier': 'IDC_LIBRARY_BTN_FILTER_AUDIO'}
input_search = {'AXIdentifier': 'IDC_LIBRARY_SEARCHFIELD'}
btn_search_cancel = {'AXDescription': 'cancel'}
txt_no_search_result = {'AXIdentifier': 'IDC_STATIC_NO_SEARCH_RESULT'}
txt_no_results_for_dot = {'AXValue': 'No results for "."', 'AXRole': 'AXStaticText'}
txt_no_results_for_backslash = {'AXValue': 'No results for "\\"', 'AXRole': 'AXStaticText'}
txt_no_results_for_special_character = {'AXValue': 'No results for "&^$%"', 'AXRole': 'AXStaticText'}
splitter_library_to_preview_window = [{'AXIdentifier': 'IDD_UPPERVIEW'}, {'AXRole': 'AXSplitter'}] # the vertical splitter between library and preview
library_frame = {'AXIdentifier': 'IDD_LIBRARY'}

# for GI entry
btn_stock_media = {'AXTitle': 'Stock Media'}

# For New On boarding flow 2
bb_new_on_boarding_1 = {'AXRoleDescription': 'popover', 'AXRole': 'AXPopover', 'index': 0}
bb_new_on_boarding_2 = {'AXRoleDescription': 'popover', 'AXRole': 'AXPopover', 'index': 1}
txt_new_on_boarding_2_string = [bb_new_on_boarding_2, {'AXRole': 'AXStaticText'}]

# for Background Music (Soundstripe)
btn_upgrade_now = {'AXTitle': 'Upgrade Now', 'AXRole': 'AXButton'}
btn_no_thanks = {'AXTitle': 'No, thanks.', 'AXRole': 'AXButton'}

class top_tool_bar():
    main_window = {'AXRole': 'AXToolbar'}
    btn_show_minimized_library_window = [main_window, {'AXRole': 'AXButton', 'index': 3}]
    option_media_library = {'AXIdentifier': 'menuMediaLibrary'} # the context menu after clicked btn_show_minimize_library_window
    option_timeline_preview = {'AXIdentifier': 'menuTimelinePreview'} # the timeline window option after clicked minimize button

class undock_library_window():
    main_window = {'AXIdentifier': 'PopupWindow'}
    btn_minimize = [main_window, {'AXRoleDescription': 'minimize button'}]

class import_media():
    option_import_media_file = {'AXIdentifier': 'IDM_MEDIALIB_IMPORT_FILE'} # v2529: 'importFiles'
    option_import_media_folder = {'AXIdentifier': 'IDM_MEDIALIB_IMPORT_FOLDER'} # v2529: 'importFolders'
    option_download_media_from_cyberlink_cloud = {'AXIdentifier': 'IDM_MENU_FILE_DOWNLOAD_MVP_FROM_LIVE'} # v2529: 'downloadMVPWithSender:'
    option_download_media_from_shutterstock = {'AXIdentifier': 'IDM_MEDIALIB_DOWNLOAD_FROM_SHUTTERSTOCK'}

class library_menu():
    btn_menu = {'AXIdentifier': 'IDC_LIBRARY_BTN_MENU'}
    option_sort_by = {'AXTitle': 'Sort by'}
    option_display_as = {'AXTitle': 'Display As'}
    option_sort_by_name = {'AXTitle': 'Name'}
    option_sort_by_duration = {'AXTitle': 'Duration'}
    option_sort_by_file_size = {'AXTitle': 'File Size'}
    option_sort_by_created_date = {'AXTitle': 'Created Date'}
    option_sort_by_modified_date = {'AXTitle': 'Modified Date'}
    option_sort_by_type = {'AXTitle': 'Type'}
    option_sort_by_r = {'AXTitle': 'R'}
    option_sort_by_g = {'AXTitle': 'G'}
    option_sort_by_b = {'AXTitle': 'B'}
    option_sort_by_date = {'AXTitle': 'Date'}
    option_sort_by_category = {'AXTitle': 'Category'}
    option_sort_by_download = {'AXTitle': 'Download'}
    option_select_all = {'AXTitle': 'Select All'}
    option_extra_large_icons = {'AXTitle': 'Extra Large Icons'}
    option_large_icons = {'AXTitle': 'Large Icons'}
    option_medium_icons = {'AXTitle': 'Medium Icons'}
    option_small_icons = {'AXTitle': 'Small Icons'}
    option_empty_the_library = {'AXTitle': 'Empty the Library'}
    option_remove_all_unused_content_from_library = {'AXTitle': 'Remove All Unused Content from Library'}
    option_new_color_board = {'AXTitle': 'Solid Color Board'}
    option_new_gradient_color = {'AXIdentifier': 'IDM_COLORBOARD_ADD_GRADIENT'}
    option_restore_to_defaults = {'AXTitle': 'Restore to Defaults'}
    option_download_from = {'AXTitle': 'Download from'}
    option_download_from_cyberlink_cloud = {'AXIdentifier': 'IDM_MENU_FILE_DOWNLOAD_MVP_FROM_LIVE'} #v2529: downloadFromCloud
    option_dock_undock_library_window = {'AXTitle': 'Dock/Undock Library Window'}
    option_reset_all_undocked_windows = {'AXTitle': 'Reset All Undocked Windows'}
    option_import_media_files = {'AXIdentifier': 'IDM_MEDIALIB_IMPORT_FILE'} #v2529: IDC_LIBRARY_BUTTON_IMPORT_MEDIA_FILES
    option_import_a_media_folder = {'AXIdentifier': 'IDM_MEDIALIB_IMPORT_FOLDER'} #v2529: importFolders

class library_listview():
    main_frame = {'AXIdentifier': 'IDC_LIBRARY_SCROLLVIEW_COLLECTIONVIEW'}
    collection_list = {'AXSubrole': 'AXCollectionList'}
    unit_collection_view_item = {'AXIdentifier': 'LibraryCollectionViewItem'}
    unit_collection_view_item_second = {'AXIdentifier': 'LibraryCollectionViewItem', 'index': 1} # For select 2nd color board template
    unit_collection_view_item_image = {'AXRole': 'AXImage'}
    unit_collection_view_item_text = {'AXIdentifier': 'CollectionViewItemTextField'}
    btn_display_hide_explore_view = {'AXIdentifier': 'IDC_LIBRARY_BTN_OPEN_CLOSE_EXPLORERVIEW'} # hardcode_0427: IDC_LIBRARY_BTN_OPEN_CLOSE_EXPLORERVIEW, v2529: _NS:256
    table_view = {'AXIdentifier': 'IDC_LIBRARY_TABLEVIEW_DETAILED'}

class colors():
    main_window = {'AXTitle': 'Colors'}
    input_hex_color = {'AXIdentifier': 'hex', 'AXRole': 'AXTextField'}
    btn_close = [main_window, {'AXRoleDescription': 'close button'}]
    btn_color_sliders = [main_window, {'AXHelp': 'Color Sliders'}]
    category = [main_window, {'AXIdentifier': '_NS:140'}]
    category_items = [category, {"AXRole": "AXMenuItem", "get_all": True}]

class scroll_area(): # the top title button of list view under background music and sound clips
    btn_sort_by_name = [{'AXIdentifier': 'IDC_LIBRARY_TABLEVIEW_DETAILED'}, {'AXRole': 'AXGroup', 'recursive': False}, {'AXTitle': 'Name'}]
    btn_sort_by_category = [{'AXIdentifier': 'IDC_LIBRARY_TABLEVIEW_DETAILED'}, {'AXRole': 'AXGroup', 'recursive': False}, {'AXTitle': 'Category'}]
    btn_sort_by_duration = [{'AXIdentifier': 'IDC_LIBRARY_TABLEVIEW_DETAILED'}, {'AXRole': 'AXGroup', 'recursive': False}, {'AXTitle': 'Duration'}]
    btn_sort_by_size = [{'AXIdentifier': 'IDC_LIBRARY_TABLEVIEW_DETAILED'}, {'AXRole': 'AXGroup', 'recursive': False}, {'AXTitle': 'Size'}]
    btn_sort_by_date = [{'AXIdentifier': 'IDC_LIBRARY_TABLEVIEW_DETAILED'}, {'AXRole': 'AXGroup', 'recursive': False}, {'AXTitle': 'Date'}]
    btn_sort_by_download = [{'AXIdentifier': 'IDC_LIBRARY_TABLEVIEW_DETAILED'}, {'AXRole': 'AXGroup', 'recursive': False},
                        {'AXTitle': 'Download'}]
    list_icon_music = {'AXDescription': 'list icon music'}
    library_table_view = [{'AXIdentifier': 'IDD_LIBRARY'}, {'AXIdentifier': 'IDC_LIBRARY_SCROLLVIEW_DETAILEDTABLEVIEW'}]  # the frame of table view
    library_table_view_detailed = {'AXIdentifier': 'IDC_LIBRARY_TABLEVIEW_DETAILED'} # table view content list
    table_view_row_unit = [library_table_view, {'AXRoleDescription': 'table row'}]
    table_view_text_field_name = {'AXIdentifier': 'DetailedViewItemTextField'}
    table_view_text_field_category = {'AXIdentifier': 'DetailedViewItemTextField'} # hardcode_0427: DetailedViewItemTextField, should be found under table row unit, v2529: _NS:13
    table_view_text_field_duration = {'AXIdentifier': 'DetailedViewItemTextField', 'index': 1}  # hardcode_0427: DetailedViewItemTextField, should be found under table row unit, v2529: _NS:13
    table_view_text_field_size = {'AXIdentifier': 'DetailedViewItemTextField', 'index': 2}  # hardcode_0427: DetailedViewItemTextField, hardcode_0427: DetailedViewItemTextField, should be found under table row unit, v2529: _NS:13
    table_view_text_field_date = {'AXIdentifier': 'DetailedViewItemTextField', 'index': 3}  # hardcode_0427: DetailedViewItemTextField, should be found under table row unit, v2529: _NS:13
    table_view_text_field_download = {'AXIdentifier': 'DetailedViewItemImageView', 'index': 4}  # hardcode_0427: DetailedViewItemImageView, should be found under table row unit, v2529: _NS:13
    table_view_text_field_download_ok = {'AXIdentifier': 'DetailedViewItemImageView', 'AXDescription': 'Icon DownloadOK'} # hardcode_0427: DetailedViewItemImageView, v2529: _NS:13
    table_view_text_field_download_button = {'AXIdentifier': 'DetailedViewItemImageView', 'AXDescription': 'Btn Download N'} # hardcode_0427: DetailedViewItemImageView, v2529: _NS:13
    table_view_scroll_bar_unit = [library_table_view, {'AXRole': 'AXValueIndicator'}]
    sound_clips_scroll_bar_horizontal = [library_table_view, {'AXIdentifier': 'IDC_LIBRARY_SCROLLBAR_TABLEVIEW_X', 'recursive': False}, {'AXRole': 'AXValueIndicator'}] # hardcode_0427: IDC_LIBRARY_SCROLLBAR_TABLEVIEW_X, v2529: _NS:514
    sound_clips_scroll_bar_vertical = [library_table_view, {'AXIdentifier': 'IDC_LIBRARY_SCROLLBAR_TABLEVIEW_Y', 'recursive': False}, {'AXRole': 'AXValueIndicator'}]

class confirm_dialog():
    main = {'AXIdentifier': 'IDD_CLALERT'} # hardcode_0427: IDD_CLALERT, v2529: _NS:10
    txt_description = [main, {'AXIdentifier': 'IDC_CLALERT_MESSAGE'}] # hardcode_0427: IDC_CLALERT_MESSAGE, v2529: _NS:34
    btn_ok = {'AXRoleDescription': 'button', 'AXTitle': 'OK'}
    btn_yes = {'AXRoleDescription': 'button', 'AXTitle': 'Yes'}
    btn_no = {'AXRoleDescription': 'button', 'AXTitle': 'No'}
    chx_do_not_show_again = {'AXRole': 'AXCheckBox', 'AXTitle': 'Don\'t show again'}

class download_media_dialog(): # btn_import_media > download media from Cyberlink Cloud
    main_window = {'AXIdentifier': 'IDC_DOWNLOAD_FROM_CYBERLINKCLOUD_DLG'} # hardcode_0427: IDC_DOWNLOAD_FROM_CYBERLINKCLOUD_DLG, v2529: _NS:48
    btn_close = [main_window, {'AXRoleDescription': 'close button'}]

class download_media_from_shutterstock_dialog(): # btn_import_media > download media from Cyberlink Cloud
    main_window = {'AXIdentifier': 'IDC_DOWNLOAD_FROM_SHUTTERSTOCK_DLG'}
    btn_close = [main_window, {'AXRoleDescription': 'close button'}]

class library_media_find_in_timeline_confirm_dialog(): # pops up after clicked find media in timeline
    static_text_file_name = {'AXIdentifier': 'IDC_SEARCHMEDIASTATIC_FILENAME'} # hardcode_0427: IDC_SEARCHMEDIASTATIC_FILENAME, v2529: _NS:82
    btn_close = [{'AXTitle': 'Find'}, {'AXRoleDescription': 'close button'}]

class properties_dialog():
    main_window = {'AXTitle': 'Properties'}
    btn_close = [main_window, {'AXIdentifier': 'IDC_PROPERTIES_DIALOG_BTN_CLOSE'}]
    video_info = [main_window, {'AXRole': 'AXStaticText', 'index': 3}]

class svrt_window():
    title = {'AXIdentifier': 'IDC_SVRT_DETAIL_TITLE'} # hardcode_0427: _NS:260 (fix in 20.0.3303)
    btn_refresh = {'AXIdentifier': 'IDC_LIB_SVRT_PROFILEDETAIL_BTN_REFRESH'}
    btn_close = {'AXIdentifier': 'IDC_LIB_SVRT_PROFILEDETAIL_BTN_CLOSE'}
    btn_help = {'AXIdentifier': 'IDC_LIB_SVRT_PROFILEDETAIL_BTN_HELP'}
    unit_table = {'AXIdentifier': 'IDC_LIB_SVRT_PROFILEDETAIL_TABLEVIEW'} # v3310: _NS:127 (has feedback)
    unit_table_row = [unit_table, {'AXSubrole': 'AXTableRow'}]
    field_work_reduced = [unit_table_row, {'AXIdentifier': 'IDC_LIB_SVRT_PROFILEDETAIL_TEXTFIELD_WORKLOADREDUCED', 'index': 5}] # v3310: _NS:11 (has feedback)


class cmyk_sliders():
    cyan = {'AXIdentifier': 'cyan', 'AXRole': 'AXSlider'}
    magenta = {'AXIdentifier': 'magenta', 'AXRole': 'AXSlider'}
    yellow = {'AXIdentifier': 'yellow', 'AXRole': 'AXSlider'}
    black = {'AXIdentifier': 'black', 'AXRole': 'AXSlider'}

class hsb_sliders():
    hue = {'AXIdentifier': 'hue', 'AXRole': 'AXSlider'}
    saturation = {'AXIdentifier': 'saturation', 'AXRole': 'AXSlider'}
    brightness = {'AXIdentifier': 'brightness', 'AXRole': 'AXSlider'}

class meta_music():
    icon_meta = {'AXIdentifier': '_NS:1241', 'AXRole': 'AXButton'}