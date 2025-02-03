cloud = {'AXIdentifier': 'IDC_TB_BTN_CLOUD'}
dz = {'AXIdentifier': 'IDC_TB_BTN_DZ'}

close = {'AXSubrole':"AXCloseButton"}

class download_project:
    window = {'AXIdentifier': 'IDC_DOWNLOAD_PROJECT_DLG'}
    caption = [window, [{'AXRole' : 'AXToolbar'}, {"AXRole": "AXStaticText"}]]
    project_list = {'AXIdentifier': 'IDC_DOWNLOAD_PROJECT_TABLEVIEW'}
    project_list_item = [project_list, {'AXIdentifier': '_NS:9', "get_all": True}]
    delete = {'AXIdentifier': 'IDC_DOWNLOAD_PROJECT_DELETE'}
    delete_window = {'AXIdentifier': 'IDD_CLALERT'}
    download = {'AXIdentifier': 'IDC_DOWNLOAD_PROJECT_DOWNLOAD'}
    cancel = {'AXIdentifier': 'IDC_DOWNLOAD_PROJECT_CANCEL'}
    close = [window, {'AXSubrole': "AXCloseButton"}]
    used_space = {'AXIdentifier': 'IDC_DOWNLOAD_PROJECT_USED_SPACE'}
    sort_header = {'AXIdentifier': 'IDC_DOWNLOAD_PROJECT_TABLE_HEADER_VIEW', 'AXRole': 'AXGroup'} #81#3904:_NS:34
    class warning_msg:
        ok = {'AXIdentifier': 'IDC_CLALERT_BUTTON_0'}
        cancel = {'AXIdentifier': 'IDC_CLALERT_BUTTON_1'}
    class open_file_dialog:
        open = {'AXIdentifier': '_NS:264'}
    class downloaded:
        ok = {'AXIdentifier': 'IDC_DOWNLOAD_PROJECT_RESULT_OK'}
        open = {'AXIdentifier': 'IDC_DOWNLOAD_PROJECT_RESULT_OPEN'}
    class process_dialog:
        cancel = {'AXIdentifier': 'IDC_CLOUDPROGRESS_PROGRESS_BTN_CANCEL'}
        remain_time = {'AXIdentifier': 'IDC_CLOUDPROGRESS_TEXT_REMAINING_TIME'} #3904: _NS:17     #3823:_NS:107     #3630: _NS:17    #3310: _NS:130

class upload_project:
    window = {'AXIdentifier': 'IDC_UPLOAD_PROJECT_DLG'}
    project_name = {'AXIdentifier': 'IDC_UPLOAD_PROJECT_PROJECTNAME'}
    close = {'AXSubrole':"AXCloseButton"}
    cancel = {'AXIdentifier': 'IDC_UPLOAD_PROJECT_CANCEL'}
    ok = {'AXIdentifier': 'IDC_UPLOAD_PROJECT_OK'}
    class warning_msg:
        cancel = {'AXIdentifier': 'IDC_CLALERT_BUTTON_1'}
        ok = {'AXIdentifier': 'IDC_CLALERT_BUTTON_0'}
    class uploaded:
        link = {'AXIdentifier': 'IDC_UPLOAD_PROJECT_PREVIEW'}
        ok = {'AXIdentifier': 'IDC_UPLOAD_PROJECT_OK'}

class pack_project_and_upload:
    window = {'AXIdentifier': 'IDC_UPLOAD_PROJECT_DLG'}
    project_name = {'AXIdentifier': 'IDC_UPLOAD_PROJECT_PROJECTNAME'}
    close = {'AXSubrole': "AXCloseButton"}
    cancel = {'AXIdentifier': 'IDC_UPLOAD_PROJECT_CANCEL'}
    ok = {'AXIdentifier': 'IDC_UPLOAD_PROJECT_OK'}
    class warning_msg:
        txt = {'AXIdentifier': 'IDC_CLALERT_MESSAGE'}
        cancel = {'AXIdentifier': 'IDC_CLALERT_BUTTON_1'}
        ok = {'AXIdentifier': 'IDC_CLALERT_BUTTON_0'}
    class uploaded:
        link = {'AXIdentifier': 'IDC_UPLOAD_PROJECT_PREVIEW'}
        ok = {'AXIdentifier': 'IDC_UPLOAD_PROJECT_OK'}

select_deselect_all = {'AXIdentifier': 'IDC_TB_BTN_SELECTALL'}
download = {"AXTitle":"Download","AXRole":"AXButton"} #{'AXIdentifier': 'IDC_MVPB_BTN_DOWNLOAD'}
search = {'AXIdentifier': 'IDS_LIBRARY_SEARCH_DEFAULT'}
reset_search = [search, {"AXDescription":"cancel"}]
library_menu = {'AXIdentifier': 'IDC_TB_BTN_POPUPMENU'}

# template = [{'AXIdentifier': 'CloudTemplateCollectionViewItem', "get_all": True},{"AXRole":"AXStaticText"}]
template = [{"AXSubrole":"AXCollectionList"},{"AXRole":"AXStaticText"}] # workaround for 2922
delete = {'AXIdentifier': 'IDC_TB_BTN_REMOVE_FILE'}

template_selected = {'AXIdentifier': 'IDC_DOWNLOAD_TEMPLATE_LABEL_SELECTED_TEMPLATES'} # 2922: _NS:385

class signin:
    auto_signin = {'AXIdentifier': 'IDC_STATIC_DIRECTORZONE_AUTOLOGIN'}
    no = {'AXIdentifier': 'IDC_SSO_BUTTON_NO'}
    yes = {'AXIdentifier': 'IDC_SSO_BUTTON_YES'}

class delete_dialog:
    main = {"AXSubrole":"AXDialog"}
    ok = [main, {"AXTitle":"OK"}]


class category: #
    button = [{"AXSubrole":"AXDialog","recursive":False},{"AXIdentifier":"IDC_TB_BTN_DZMAINTAG"}]
    my_upload = [button,{"AXRole":"AXStaticText", "AXValue":"My Uploads"}]
    download_history = [button, {"AXRole": "AXStaticText", "AXValue":"Download History"}]
    my_favorites = [button, {"AXRole": "AXStaticText", "AXValue":"My Favorites"}]

class sort:
    name = {"AXTitle":"Name"}
    date = {"AXTitle":"Date"}
    size = {"AXTitle":"Size"}
    type = {"AXTitle":"Type"}