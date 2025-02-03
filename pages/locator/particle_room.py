btn_import_media = {'AXIdentifier': 'IDC_LIBRARY_BTN_IMPORT_MEDIA', "index": 0}
btn_add_new_tag = {'AXIdentifier': 'IDC_LIBRARY_BTN_ADD_TAG'}
btn_delete_tag = {'AXIdentifier': 'IDC_LIBRARY_BTN_DELETE_TAG'}
btn_import_particle_objects = {'AXTitle': 'Import Particle Objects'}
btn_download_from_DZ_cloud = {'AXTitle': 'Download Content from CyberLink Cloud/DirectorZone'}
btn_explore_view = {'AXIdentifier': 'IDC_LIBRARY_BTN_OPEN_CLOSE_EXPLORERVIEW'}
btn_modify_template = {'AXIdentifier': 'IDC_LIBRARY_BTN_MODIFYTEMPLATE'}

input_search = {'AXIdentifier': 'IDC_LIBRARY_SEARCHFIELD', 'AXRole': 'AXTextField'}
btn_search_cancel = {'AXDescription': 'cancel'}

library_free_template = {'AXIdentifier': 'LibraryCollectionViewItem', 'AXRole': 'AXGroup', "index": 0}

class explore_view_region():
    table_all_content_tags = {'AXIdentifier': 'IDC_LIBRARY_ROOM_TAG_TABLEVIEW'}
    General_category = [table_all_content_tags, {'AXIdentifier': 'RoomTagTextField', 'AXRole': 'AXStaticText', "index": 2}]

class warning_dialog():
    main = {'AXIdentifier': 'IDD_CLALERT'}
    msg1 = [main, {"AXIdentifier": "IDC_CLALERT_MESSAGE", "AXValue": 'A folder with the same name already exists. Enter another folder name.'}]
    msg2 = [main, {"AXIdentifier": "IDC_CLALERT_MESSAGE", "AXValue": 'Are you sure you want to delete this tag?'}]
    msg3 = [main, {"AXIdentifier": "IDC_CLALERT_MESSAGE", "AXValue": 'Are you sure you want to delete the selected item(s)?'}]
    msg4 = [main, {"AXIdentifier": "IDC_CLALERT_MESSAGE", "AXValue": 'The templates were successfully downloaded and are now available in the library.'}]
    ok = [main, {"AXRole": "AXButton", "AXTitle": "OK"}]
    yes = [main, {"AXRole": "AXButton", "AXTitle": "Yes"}]

class download_dialog():
    main = {'AXIdentifier': 'IDC_DOWNLOAD_TEMPLATE_FROM_CYBERLINKCLOUD_AND_DZ_DLG'}
    str_Title = {'AXValue': 'Download Particle Objects'}
    cloud_tab = [main, {'AXIdentifier': 'IDC_TB_BTN_CLOUD', 'AXRole': 'AXButton'}]
    btn_download = [main, {'AXIdentifier': 'IDC_TB_BTN_DETAIL', 'AXTitle': 'Download', 'AXRole': 'AXButton'}]
    btn_close = [main, {'AXRoleDescription': 'close button'}]