
btn_import_media = {'AXIdentifier': 'IDC_LIBRARY_BTN_IMPORT_MEDIA'}
btn_create_new_color_board = {'AXIdentifier': '_NS:914'} # hardcoard_0427: IDC_LIBRARY_BTN_NEWCOLORBOARD
tag_media_content = {'AXValue': 'Media Content'}
tag_color_boards = {'AXValue': 'Color Boards'}
tag_background_music = {'AXValue': 'Background Music'}
tag_sound_clips = {'AXValue': 'Sound Clips'}
tag_downloaded = {'AXValue': 'Downloaded'}
unit_tag_room_text_field = {'AXIdentifier': 'RoomTagTextField'} # the general identifier of tag_room e.g. Media Content
btn_add_new_tag = {'AXIdentifier': '_NS:12'} # hardcode_0427: IDC_LIBRARY_BTN_ADD_TAG
input_new_tag = {'AXIdentifier': 'RoomTagTextField', 'AXFocused': True}
btn_delete_tag = {'AXIdentifier': '_NS:33'} # hardcode_0427: IDC_LIBRARY_BTN_DELETE_TAG
tag_scroll_view_frame = {'AXIdentifier': '_NS:206'} # hardcode_0427: IDC_LIBRARY_ROOM_TAG_TABLEVIEW, the custom tag scrll view frame
tag_main_frame = {'AXIdentifier': '_NS:63'} # hardcode_0427: IDC_LIBRARY_DEFAULT_TAG_TABLEVIEW, parent frame of default tag (e.g. Media Content, Color Boards)
unit_main_tag_text_field = [tag_main_frame, unit_tag_room_text_field]
unit_custom_tag_text_field = [tag_scroll_view_frame, unit_tag_room_text_field]
btn_media_filter_all = {'AXIdentifier': 'IDC_LIBRARY_BTN_FILTER_ALL'}
btn_media_filter_display_video_only = {'AXIdentifier': 'IDC_LIBRARY_BTN_FILTER_VIDEO'}
btn_media_filter_display_image_only = {'AXIdentifier': 'IDC_LIBRARY_BTN_FILTER_IMAGE'}
btn_media_filter_display_audio_only = {'AXIdentifier': 'IDC_LIBRARY_BTN_FILTER_AUDIO'}
input_search = {'AXRoleDescription': 'search text field'}
btn_search_cancel = {'AXDescription': 'cancel'}
splitter_library_to_preview_window = [{'AXIdentifier': 'IDD_UPPERVIEW'}, {'AXRole': 'AXSplitter'}] # the vertical splitter between library and preview
library_frame = {'AXIdentifier': 'IDD_LIBRARY'}

class top_tool_bar():
    main_window = {'AXRole': 'AXToolbar'}
    btn_show_minimized_library_window = [main_window, {'AXRole': 'AXButton', 'index': 3}]
    option_media_library = {'AXIdentifier': 'menuMediaLibrary'} # the context menu after clicked btn_show_minimize_library_window
    option_timeline_preview = {'AXIdentifier': 'menuTimelinePreview'} # the timeline window option after clicked minimize button

class undock_library_window():
    main_window = {'AXIdentifier': 'PopupWindow'}
    btn_minimize = [main_window, {'AXRoleDescription': 'minimize button'}]

class import_media():
    option_import_media_file = {'AXIdentifier': 'importFiles'}
    option_import_media_folder = {'AXIdentifier': 'importFolders'}
    option_download_media_from_cyberlink_cloud = {'AXIdentifier': 'downloadMVPWithSender:'}


class library_menu():
    btn_menu = {'AXIdentifier': 'IDC_LIBRARY_BTN_MENU'}
    option_sort_by = {'AXTitle': 'Sort By'}
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
    option_new_color_board = {'AXTitle': 'New Color Board'}
    option_restore_to_defaults = {'AXTitle': 'Restore to Defaults'}
    option_download_from = {'AXTitle': 'Download from'}
    option_download_from_cyberlink_cloud = {'AXIdentifier': 'downloadFromCloud'}
    option_dock_undock_library_window = {'AXTitle': 'Dock/Undock Library Window'}
    option_reset_all_undocked_windows = {'AXTitle': 'Reset All Undocked Windows'}
    option_import_media_files = {'AXIdentifier': 'IDC_LIBRARY_BUTTON_IMPORT_MEDIA_FILES'}
    option_import_a_media_folder = {'AXIdentifier': 'importFolders'}

class library_listview():
    main_frame = {'AXIdentifier': 'IDC_LIBRARY_SCROLLVIEW_COLLECTIONVIEW'}
    collection_list = {'AXSubrole': 'AXCollectionList'}
    unit_collection_view_item = {'AXIdentifier': 'LibraryCollectionViewItem'}
    unit_collection_view_item_image = {'AXRole': 'AXImage'}
    unit_collection_view_item_text = {'AXIdentifier': 'CollectionViewItemTextField'}
    btn_display_hide_explore_view = {'AXIdentifier': '_NS:256'} # hardcode_0427: IDC_LIBRARY_BTN_OPEN_CLOSE_EXPLORERVIEW
    table_view = {'AXIdentifier': 'IDC_LIBRARY_TABLEVIEW_DETAILED'}

class colors():
    main_window = {'AXTitle': 'Colors'}
    input_hex_color = {'AXIdentifier': 'hex'}
    btn_close = [main_window, {'AXRoleDescription': 'close button'}]

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
    table_view_text_field_name = [library_table_view, {'AXIdentifier': 'DetailedViewItemTextField'}] # should be found under table row unit
    table_view_text_field_category = {'AXIdentifier': '_NS:13'} # hardcode_0427: DetailedViewItemTextField, should be found under table row unit
    table_view_text_field_duration = {'AXIdentifier': '_NS:13', 'index': 1}  # hardcode_0427: DetailedViewItemTextField, should be found under table row unit
    table_view_text_field_size = {'AXIdentifier': '_NS:13', 'index': 2}  # hardcode_0427: DetailedViewItemTextField, hardcode_0427: DetailedViewItemTextField, should be found under table row unit
    table_view_text_field_date = {'AXIdentifier': '_NS:13', 'index': 3}  # hardcode_0427: DetailedViewItemTextField, should be found under table row unit
    table_view_text_field_download = {'AXIdentifier': '_NS:13', 'index': 4}  # hardcode_0427: DetailedViewItemImageView, should be found under table row unit
    table_view_text_field_download_ok = {'AXIdentifier': '_NS:13', 'AXDescription': 'Icon DownloadOK'} # hardcode_0427: DetailedViewItemImageView
    table_view_text_field_download_button = {'AXIdentifier': '_NS:13', 'AXDescription': 'Btn Download N'} # hardcode_0427: DetailedViewItemImageView
    table_view_scroll_bar_unit = [library_table_view, {'AXRole': 'AXValueIndicator'}]
    sound_clips_scroll_bar_horizontal = [library_table_view, {'AXIdentifier': '_NS:514', 'recursive': False}, {'AXRole': 'AXValueIndicator'}] # hardcode_0427: IDC_LIBRARY_SCROLLBAR_TABLEVIEW_X
    sound_clips_scroll_bar_vertical = [library_table_view, {'AXIdentifier': 'IDC_LIBRARY_SCROLLBAR_TABLEVIEW_Y', 'recursive': False}, {'AXRole': 'AXValueIndicator'}]

class confirm_dialog():
    main = {'AXIdentifier': '_NS:10'} # hardcode_0427: IDD_CLALERT
    txt_description = [main, {'AXIdentifier': '_NS:34'}] # hardcode_0427: IDC_CLALERT_MESSAGE
    btn_ok = {'AXRoleDescription': 'button', 'AXTitle': 'OK'}
    btn_yes = {'AXRoleDescription': 'button', 'AXTitle': 'Yes'}
    btn_no = {'AXRoleDescription': 'button', 'AXTitle': 'No'}
    chx_do_not_show_again = {'AXRole': 'AXCheckBox', 'AXTitle': 'Don\'t show again'}

class download_media_dialog():
    main_window = {'AXIdentifier': '_NS:48'} # hardcode_0427: IDC_DOWNLOAD_FROM_CYBERLINKCLOUD_DLG
    btn_close = [main_window, {'AXRoleDescription': 'close button'}]

class library_media_find_in_timeline_confirm_dialog(): # pops up after clicked find media in timeline
    static_text_file_name = {'AXIdentifier': '_NS:82'} # hardcode_0427: IDC_SEARCHMEDIASTATIC_FILENAME
    btn_close = [{'AXTitle': 'Find'}, {'AXRoleDescription': 'close button'}]

class properties_dialog():
    main_window = {'AXTitle': 'Properties'}
    btn_close = [main_window, {'AXTitle': 'Close'}]

class svrt_window:
    title = {'AXIdentifier': '_NS:260'} # hardcode_0427: Not fix