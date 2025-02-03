btn_create_new_PiP_object = {'AXIdentifier': 'IDC_LIBRARY_BTN_NEWTEMPLATE'}
btn_modify_PiP_Attributes = {'AXIdentifier': 'IDM_PIPROOM_MODIFYTEMPLATES'}
btn_add_new_tag = {'AXIdentifier': 'IDC_LIBRARY_BTN_ADD_TAG'}
btn_delete_tag = {'AXIdentifier': 'IDC_LIBRARY_BTN_DELETE_TAG'}
btn_modify_Mask_Attributes = {'AXIdentifier': 'IDM_PIPROOM_MODIFYTEMPLATES_MASKDESIGNER'}
btn_modify_selected_PiP_object = {'AXIdentifier': 'IDC_LIBRARY_BTN_MODIFYTEMPLATE'}
btn_import_media = {'AXIdentifier': 'IDC_LIBRARY_BTN_IMPORT_MEDIA', "index": 0}
btn_upload_to_DZ_cloud = {'AXIdentifier': 'IDC_LIBRARY_BTN_IMPORT_MEDIA', "index": 1}
btn_import_PiP_object = {'AXTitle': 'Import PiP Objects'}
btn_download_from_DZ_cloud = {'AXTitle': 'Download Content from DirectorZone/CyberLink Cloud'}
btn_explore_view = {'AXIdentifier': 'IDC_LIBRARY_BTN_OPEN_CLOSE_EXPLORERVIEW'}

input_search = {'AXIdentifier': 'IDC_LIBRARY_SEARCHFIELD', 'AXRole': 'AXTextField'}
btn_search_cancel = {'AXDescription': 'cancel'}

# Custom, Downloaded, General, Romance ..., Custom tag
class explore_view_region():
    table_all_content_tags = {'AXIdentifier': 'IDC_LIBRARY_ROOM_TAG_TABLEVIEW'}
    Romance_category = [table_all_content_tags, {'AXIdentifier': 'RoomTagTextField', 'AXRole': 'AXStaticText', "index": 3}]

class warning_dialog():
    main = {'AXIdentifier': 'IDD_CLALERT'}
    msg1 = [main, {"AXIdentifier": "_NS:34", "AXValue": 'A folder with the same name already exists. Enter another folder name.'}]
    msg2 = [main, {"AXIdentifier": "_NS:34", "AXValue": 'Are you sure you want to delete this tag?'}]
    msg3 = [main, {"AXIdentifier": "_NS:34", "AXValue": 'Are you sure you want to delete the selected item(s)?'}]
    ok = [main, {"AXRole": "AXButton", "AXTitle": "OK"}]
    yes = [main, {"AXRole": "AXButton", "AXTitle": "Yes"}]

class pip_designer():
    main_window = {'AXIdentifier': '_NS:10', 'AXRole': 'AXWindow'}
    properties_tab = [main_window, {'AXIdentifier': '_NS:12', 'AXTitle': 'Properties'}]

class cyberlink_power_director():
    main = {'AXIdentifier': '_NS:10', 'AXTitle': 'CyberLink PowerDirector'}
    msg = [main, {"AXIdentifier": "_NS:97", "AXValue": 'Do you want to log in to DirectorZone with the following account?'}]
    yes = [main, {"AXIdentifier": "_NS:89", "AXTitle": "Yes"}]
    no = [main, {"AXIdentifier": "_NS:80", "AXTitle": "No"}]

class upload_dialog():
    main = {'AXIdentifier': '_NS:10', 'AXTitle': 'Upload'}
    step1 = [main, {'AXIdentifier': '_NS:317', 'AXValue': 'Step 1. Describe this PiP template'}]
    btn_close = [main, {'AXRoleDescription': 'close button'}]

class download_dialog():
    main = {'AXIdentifier': '_NS:48'}
    str_Title = {'AXIdentifier': '_NS:63', 'AXValue': 'Download PiP Objects'}
    cloud_tab = [main, {'AXIdentifier': '_NS:220', 'AXRole': 'AXButton'}]
    director_zone_tab = [main, {'AXIdentifier': '_NS:186', 'AXRole': 'AXButton'}]
    busy_icon = [main, {'AXIdentifier': '_NS:627', 'AXRole': 'AXImage'}]
    btn_download = [main, {'AXIdentifier': '_NS:100', 'AXTitle': 'Download', 'AXRole': 'AXButton'}]
    btn_close = [main, {'AXRoleDescription': 'close button'}]

class right_click_menu:
    rename_Tag = {'AXIdentifier': 'IDM_LIBRARYMGR_ALIAS', 'AXTitle': 'Rename Tag', 'AXRole': 'AXMenuItem'}
    delete_Tag = {'AXIdentifier': 'IDM_LIBRARYMGR_REMOVE', 'AXTitle': 'Delete Tag', 'AXRole': 'AXMenuItem'}