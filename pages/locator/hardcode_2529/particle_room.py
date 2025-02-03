btn_import_media = {'AXIdentifier': 'IDC_LIBRARY_BTN_IMPORT_MEDIA', "index": 0}
btn_add_new_tag = {'AXIdentifier': '_NS:12'}
btn_delete_tag = {'AXIdentifier': '_NS:33'}
btn_import_particle_objects = {'AXTitle': 'Import Particle Objects'}
btn_download_from_DZ_cloud = {'AXTitle': 'Download Content from DirectorZone/CyberLink Cloud'}
btn_explore_view = {'AXIdentifier': '_NS:256'}

input_search = {'AXIdentifier': '_NS:1202', 'AXRole': 'AXTextField'}
btn_search_cancel = {'AXDescription': 'cancel'}

library_free_template = {'AXIdentifier': 'LibraryCollectionViewItem', 'AXRole': 'AXGroup', "index": 0}

class explore_view_region():
    table_all_content_tags = {'AXIdentifier': '_NS:210'}
    General_category = [table_all_content_tags, {'AXIdentifier': 'RoomTagTextField', 'AXRole': 'AXStaticText', "index": 2}]

class warning_dialog():
    main = {'AXIdentifier': '_NS:10'}
    msg1 = [main, {"AXIdentifier": "_NS:34", "AXValue": 'A folder with the same name already exists. Enter another folder name.'}]
    msg2 = [main, {"AXIdentifier": "_NS:34", "AXValue": 'Are you sure you want to delete this tag?'}]
    msg3 = [main, {"AXIdentifier": "_NS:34", "AXValue": 'Are you sure you want to delete the selected item(s)?'}]
    msg4 = [main, {"AXIdentifier": "_NS:34", "AXValue": 'The templates were successfully downloaded and are now available in the library.'}]
    ok = [main, {"AXRole": "AXButton", "AXTitle": "OK"}]
    yes = [main, {"AXRole": "AXButton", "AXTitle": "Yes"}]

class download_dialog():
    main = {'AXIdentifier': '_NS:48'}
    str_Title = {'AXIdentifier': '_NS:63', 'AXValue': 'Download Particle Objects'}
    cloud_tab = [main, {'AXIdentifier': '_NS:263', 'AXRole': 'AXButton'}]
    btn_download = [main, {'AXIdentifier': '_NS:100', 'AXTitle': 'Download', 'AXRole': 'AXButton'}]
    btn_close = [main, {'AXRoleDescription': 'close button'}]