main_window = {"AXRole":"AXWindow","recursive": False}
full_screen = [{"AXRole":"AXWindow","recursive": False},{"AXSubrole":"AXFullScreenButton","recursive": False}]
minimize = [{"AXRole":"AXWindow","recursive": False},{"AXSubrole":"AXMinimizeButton","recursive": False}]

tag_list = [{'AXIdentifier': 'IDD_LIBRARY'}, {"AXIdentifier": "RoomTagTextField", "get_all": True}]
tag_list_2 = [{'AXIdentifier': 'IDD_LIBRARY'}, {"AXIdentifier": "RoomTagOutlineViewTextField", "get_all": True}]
category = {'AXIdentifier': '_NS:765'}
category_items = [category, {"AXRole": "AXStaticText", "get_all": True}]

timecode = [{"AXSubrole":"AXDialog","get_all":True},
            {"AXRole":"AXGroup"},
            {"AXIdentifier":"spinTimeEditTextField"}]
button_ok = {"AXRole":"AXButton", "AXTitle":"OK"}

class quit_dialog:
    main = {"AXTitle": "CyberLink PowerDirector", "AXIdentifier": "_NS:10"}
    yes = [main, {"AXRole": "AXButton", "index": 0}]
    no = [main, {"AXRole": "AXButton", "index": 1}]
    cancel = [main, {"AXRole": "AXButton", "index": 2}]


class finder_window:
    main = {'AXIdentifier': 'FinderWindow'}
    btn_close = [main, {'AXRoleDescription': 'close button'}]


download_window_title = [
    {"AXRole": "AXToolbar", "recursive": False},
    {"AXRole": "AXGroup", "recursive": False},
    {'AXIdentifier': '_NS:63', "recursive": False},
]


class file_picker:
    main = {"AXSubrole": "AXDialog", "AXMain": False, "AXRole": "AXWindow"}
    popup_button = {'AXRoleDescription': "pop up button"}
    view_options = {'AXIdentifier': 'View Options'}
    column_view = [view_options, {'AXIdentifier': 'cmdViewAsColumns:'}]
    show_more_options = [main, {'AXIdentifier': 'NS_OPEN_SAVE_DISCLOSURE_TRIANGLE'}]
    file_name = {'AXIdentifier': '_NS:111'}
