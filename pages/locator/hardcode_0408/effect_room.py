style_effect_tag = {'AXIdentifier': 'RoomTagOutlineViewTextField', 'AXValue': 'Style Effect (85)'}
clut_effect_tag = {'AXIdentifier': 'RoomTagOutlineViewTextField', 'AXNumberOfCharacters': 13}

class library_menu:
    library_menu = {'AXIdentifier': 'IDC_LIBRARY_BTN_MENU'}
    sort_by = {'AXIdentifier': '_NS:50', 'AXRoleDescription': 'menu item'}
    sort_by_name = {'AXIdentifier': 'sortByName', 'AXRoleDescription': 'menu item'}
    sort_by_type = {'AXIdentifier': 'sortByType', 'AXRoleDescription': 'menu item'}

    extra_large_icons = {'AXIdentifier': 'extraLargeIcon', 'AXRoleDescription': 'menu item'}
    large_icons = {'AXIdentifier': 'largeIcon', 'AXRoleDescription': 'menu item'}
    medium_icons = {'AXIdentifier': 'mediumIcon', 'AXRoleDescription': 'menu item'}
    small_icons = {'AXIdentifier': 'smallIcon', 'AXRoleDescription': 'menu item'}

class import_media:
    import_media = {'AXIdentifier': 'IDC_LIBRARY_BTN_IMPORT_MEDIA'}
    import_media_clut = {'AXIdentifier': 'importFiles', 'AXTitle': 'Import color presets & CLUTs'}
    import_from_desktop = {'AXRole': 'AXStaticText', 'AXValue': 'Desktop'}
    import_from_pdr_folder = {'AXRole': 'AXTextField', 'AXValue': 'PDR'}
    import_from_test_material_folder = {'AXRole': 'AXTextField', 'AXValue': 'Test Material'}
    import_from_test_material_folder = {'AXRole': 'AXTextField', 'AXValue': '05 CLUT'}
    import_from_untitled_folder = {'AXRole': 'AXTextField', 'AXValue': 'untitled folder'}
    import_clut_media = {'AXRole': 'AXTextField', 'AXValue': 'Jap_style.3dl'}
    import_open = {'AXIdentifier': '_NS:314'}
    import_cancel = {'AXIdentifier': '_NS:304'}


btn_hide_explorer = {'AXIdentifier': '_NS:256', 'AXRole': 'AXButton'}
btn_display_explorer = {'AXIdentifier': '_NS:256', 'AXRole': 'AXButton'}

class search:
    search_field = {'AXIdentifier': '_NS:1202', "AXRole": 'AXTextField'}
    search_cancel = {'AXDescription': 'cancel', 'AXRole': 'AXButton', 'AXRoleDescription': 'button'}

class tag:
    add_tag = {'AXIdentifier': '_NS:12', 'AXRole': 'AXButton'}
    tag_name = {'AXIdentifier': 'RoomTagOutlineViewTextField', 'AXRole': 'AXTextField'}
    duplicate_tag_msg = {'AXIdentifier': '_NS:34', 'AXRole': 'AXStaticText'}
    duplicate_tag_msg_ok = {'AXRole': 'AXButton', 'AXTitle': 'OK'}
    class delete_tag:
        select_deleted_tag = {'AXIdentifier': 'RoomTagOutlineViewTextField', 'AXValue': 'New Tag (1)'}
        delete_tag = {'AXIdentifier': '_NS:33'}
        delete_tag_msg = {'AXIdentifier': '_NS:34', 'AXRoleDescription': 'text'}
        delete_tag_ok = {'AXRole': 'AXButton', 'AXTitle': 'OK'}
        delete_tag_cancel= {'AXRole': 'AXButton', 'AXTitle': 'Cancel'}

class Apply_EffectRoom_Effect_to_VideoTrack:
    click_effect_blackout = {'AXIdentifier': 'CollectionViewItemTextField', 'AXValue': 'Blackout'}

class Apply_EffectRoom_Effect_to_EffectTrack:
    click_effect_aberration = {'AXIdentifier': 'CollectionViewItemTextField', 'AXValue': 'Aberration'}

class scroll_bar:
    scroll_bar = {'AXRole': 'AXValueIndicator', 'AXRoleDescription': 'value indicator'}


class effect_room_add_to:
    click_effect_blackout = {'AXIdentifier': 'CollectionViewItemTextField', 'AXValue': 'Blackout'}
    add_to_timeline = {'AXIdentifier': '_NS:32', 'AXRole': 'AXMenuItem'}
    add_to_my_favorite = {'AXIdentifier': 'onAddToTag:', 'AXTitle': 'My Favorites'}
    add_to_new_tag = {'AXIdentifier': 'onAddToTag:', 'AXTitle': 'New Tag'}

current_tag_amount = {'AXIdentifier': '_NS:241'}
effect_room_tag_list  = [ {'AXIdentifier': '_NS:241'}, {'AXIdentifier': "RoomTagOutlineViewTextField","get_all":True}]

class effect_room_remove_from_favorite:
    my_favorite = {'AXIdentifier': 'RoomTagOutlineViewTextField', 'AXNumberOfCharacters': 16}
    target_effect = {'AXIdentifier': 'CollectionViewItemTextField', 'AXValue': 'Band Noise'}
    remove_from_favorites = {'AXRole': 'AXMenuItem', 'AXTitle': 'Remove from My Favorites'}

class effect_room_rightclick_delete_clut:
    color_clut = {'AXIdentifier': 'RoomTagOutlineViewTextField', 'AXNumberOfCharacters': 13}
    click_clut = {'AXRole': 'AXStaticText', 'AXValue': 'Jap_style'}
    delete = {'AXIdentifier': '_NS:38'}
    delete_yes = {'AXRole': 'AXButton', 'AXTitle': 'Yes'}
    delete_no = {'AXRole': 'AXButton', 'AXTitle': 'No'}

add_to_effect_track = {'AXIdentifier': 'IDC_TIPSAREA_BTN_ADDTOEFFECTTRACK'}
timeline_scrollbar = {'AXRole': 'AXValueIndicator', 'AXSize': (15.0, 138.0)}
effect_track_content = {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup'}

selected_video_track = {'AXIdentifier': 'IDC_TIMELINE_LABEL_TRACKID', 'AXRole': 'AXStaticText'}
selected_video_clip = {'AXIdentifier': 'VideoCellItem'}
effect_overwrite = {'AXIdentifier': '_NS:12'}


