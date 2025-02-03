btn_create_new_2d_title = {'AXIdentifier': 'IDC_LIBRARY_BTN_NEWTEMPLATE'}
btn_modify_selected_title_template = {'AXIdentifier': 'IDC_LIBRARY_BTN_MODIFYTEMPLATE'}
btn_add_new_tag = {'AXIdentifier': '_NS:12'}
btn_delete_tag = {'AXIdentifier': '_NS:33'}
btn_import_media = {'AXIdentifier': 'IDC_LIBRARY_BTN_IMPORT_MEDIA', "index": 0}
btn_upload_to_DZ_cloud = {'AXIdentifier': 'IDC_LIBRARY_BTN_IMPORT_MEDIA', "index": 1}
btn_import_title_templates = {'AXTitle': 'Import Title Templates'}
btn_download_from_DZ_cloud = {'AXTitle': 'Download Content from DirectorZone/CyberLink Cloud'}

btn_explore_view = {'AXIdentifier': '_NS:256'}

main_window = {"AXIdentifier": "_NS:10"}

input_search = {'AXIdentifier': '_NS:1202', 'AXRole': 'AXTextField'}
btn_search_cancel = {'AXDescription': 'cancel'}

library_free_template = {'AXIdentifier': 'LibraryCollectionViewItem', 'AXRole': 'AXGroup', "index": 0}

class scroll_bar():
    main = {'AXIdentifier': 'IDC_LIBRARY_SCROLLBAR_COLLECTIONVIEW_Y', 'AXRole': 'AXScrollBar'}
    scroll_elem = [main, {"index": 0}]

# Custom, Download, Motion Graphics, ..., Custom tag
class explore_view_region():
    table_all_content_tags = {'AXIdentifier': '_NS:210'}
    Motion_Graphics_category = [table_all_content_tags, {'AXIdentifier': 'RoomTagTextField', 'AXRole': 'AXStaticText', "index": 2}]

class warning_dialog():
    main = {'AXIdentifier': '_NS:10'}
    msg1 = [main, {"AXIdentifier": "_NS:34", "AXValue": 'A folder with the same name already exists. Enter another folder name.'}]
    msg2 = [main, {"AXIdentifier": "_NS:34", "AXValue": 'Are you sure you want to delete this tag?'}]
    msg3 = [main, {"AXIdentifier": "_NS:34", "AXValue": 'Are you sure you want to delete the selected item(s)?'}]
    msg4 = [main, {"AXIdentifier": "_NS:34", "AXValue": 'The templates were successfully downloaded and are now available in the library.'}]
    ok = [main, {"AXRole": "AXButton", "AXTitle": "OK"}]
    yes = [main, {"AXRole": "AXButton", "AXTitle": "Yes"}]

class cyberlink_power_director():
    main = {'AXIdentifier': '_NS:10', 'AXTitle': 'CyberLink PowerDirector'}
    msg = [main, {"AXIdentifier": "_NS:97", "AXValue": 'Do you want to log in to DirectorZone with the following account?'}]
    yes = [main, {"AXIdentifier": "_NS:89", "AXTitle": "Yes"}]
    no = [main, {"AXIdentifier": "_NS:80", "AXTitle": "No"}]

class download_dialog():
    main = {'AXIdentifier': '_NS:48'}
    str_Title = {'AXIdentifier': '_NS:63', 'AXValue': 'Download Title Templates'}
    cloud_tab = [main, {'AXIdentifier': '_NS:263', 'AXRole': 'AXButton'}]
    btn_download = [main, {'AXIdentifier': '_NS:100', 'AXTitle': 'Download', 'AXRole': 'AXButton'}]
    btn_close = [main, {'AXRoleDescription': 'close button'}]

class upload_dialog():
    main = {'AXIdentifier': '_NS:10', 'AXTitle': 'Upload'}
    step1 = [main, {'AXIdentifier': '_NS:317', 'AXValue': 'Step 1. Describe this title template'}]
    btn_close = [main, {'AXRoleDescription': 'close button'}]

class right_click_menu:
    rename_Tag = {'AXIdentifier': '_NS:12', 'AXTitle': 'Rename Tag', 'AXRole': 'AXMenuItem'}