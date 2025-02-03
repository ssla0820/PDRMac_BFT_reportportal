cloud = {'AXIdentifier': '_NS:263'}
dz = {'AXIdentifier': '_NS:186'}

close = {'AXSubrole':"AXCloseButton"}

select_deselect_all = {'AXIdentifier': '_NS:156'}
download = {'AXIdentifier': '_NS:100'}
search = {'AXIdentifier': '_NS:280'}
reset_search = [search, {"AXDescription":"cancel"}]
library_menu = {'AXIdentifier': '_NS:308'}

template = [{'AXIdentifier': 'CloudTemplateCollectionViewItem', "get_all": True},{"AXRole":"AXStaticText"}]
delete = {'AXIdentifier': '_NS:622'}

template_selected = {'AXIdentifier': '_NS:316'}

class signin:
    auto_signin = {'AXIdentifier': '_NS:24'}
    no = {'AXIdentifier': '_NS:80'}
    yes = {'AXIdentifier': '_NS:89'}

class delete_dialog:
    main = {"AXSubrole":"AXDialog"}
    ok = [main, {"AXTitle":"OK"}]


class category:
    button = [{"AXSubrole": "AXDialog"}, {"AXRole": "AXButton", "AXIdentifier": "_NS:9"}]
    my_upload = [button,{"AXRole":"AXStaticText", "AXValue":"My Uploads"}]
    download_history = [button, {"AXRole": "AXStaticText", "AXValue":"Download History"}]
    my_favorites = [button, {"AXRole": "AXStaticText", "AXValue":"My Favorites"}]