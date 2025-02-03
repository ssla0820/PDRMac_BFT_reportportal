what_is_stock_media_dialog = {'AXIdentifier': 'IDD_CLALERT'}
what_is_stock_media_dialog_ok = {'AXIdentifier': 'IDC_CLALERT_BUTTON_0'}
gettyimage_tab = {'AXIdentifier': 'IDC_SHUTTERSTOCK_BTN_GETTYIMAGES'} #3630: _NS:407
shutterstock_tab = {'AXIdentifier': 'IDC_SHUTTERSTOCK_BTN_SHUTTERSTOCK'} #3630: _NS:399
btn_favorite = {'AXIdentifier': 'IDC_SHUTTERSTOCK_BTN_MY_FAVORITES'} #3630: _NS:365
btn_purchased = {'AXIdentifier': 'IDC_SHUTTERSTOCK_BTN_PURCHASED'} #3630: _NS:374
btn_download = {'AXIdentifier': 'IDC_SHUTTERSTOCK_BTN_DOWNLOADED'} #3630: _NS:383
no_favorite_msg = {'AXIdentifier': 'IDC_SHUTTERSTOCK_HINT_NO_FAVORITES'} #3630: _NS:747
btn_filter = {'AXIdentifier': 'IDC_SHUTTERSTOCK_BTN_FILTER'} #3630: _NS:754
btn_filter_explorer_view = {'AXIdentifier': 'IDC_SHUTTERSTOCK_BTN_FOLDER_BAR'} #3630: _NS:75
btn_clear_all = {'AXIdentifier': 'IDC_SHUTTERSTOCK_BTN_CLEAR_ALL'} #3630: _NS:17
btn_add_to_cart = {'AXTitle': 'Add to Cart', 'AXIdentifier': 'IDC_SHUTTERSTOCK_BTN_DOWNLOAD'}
bubble_proceed_to_checkout = {'AXIdentifier': 'IDC_ADD_TO_CART_BTN_CHECKOUT'} #3630: _NS:407
btn_next_checkout_dialog = {'AXIdentifier': 'IDC_CLALERT_BUTTON_0'}
btn_cancel_checkout_dialog = {'AXIdentifier': 'IDC_CLALERT_BUTTON_1'}
bubble_cart = {'AXIdentifier': 'IDC_ADD_TO_CART_BTN_OPEN_CART'} #3630: _NS:43
cart_window = {'AXIdentifier': 'IDD_STOCK_MEDIA_SHOPPING_CART'} #3630: _NS:10
btn_cart = {'AXIdentifier': 'IDC_SHUTTERSTOCK_BTN_SHOPPING_CART'}
btn_proceed_to_checkout = {'AXIdentifier': 'IDC_STOCK_MEDIA_SHOPPING_CART_CHECKOUT'} #3630: _NS:12
trash_can_button = {'AXIdentifier': 'IDC_STOCK_MEDIA_SHOPPING_CART_DELETE'} #3630: _NS:9
subtotal_text = {'AXIdentifier': 'IDC_STOCK_MEDIA_SHOPPING_CART_COUNT_LABEL'} #3630: _NS:195
subtotal_total = {'AXIdentifier': 'IDC_STOCK_MEDIA_SHOPPING_CART_PRICE_LABEL'} #3630: _NS:202
heart_icon = {'AXIdentifier': 'IDC_SHUTTERSTOCK_ITEM_FAVORITE'} #3630: _NS:9
no_match_dialog = {'AXIdentifier': 'IDD_CLALERT'}
no_match_dialog_ok = {'AXIdentifier': 'IDC_CLALERT_BUTTON_0'}

# for select/unselect video/photo clip
window = {"AXIdentifier": "IDC_DOWNLOAD_FROM_SHUTTERSTOCK_DLG"}
scroll_media = [window, {"AXRole":"AXValueIndicator"}]
frame_section = {"AXSubrole":"AXSectionList"}
frame_scroll_view = {"AXIdentifier": "IDC_SHUTTERSTOCK_COLLECTION_VIEW"} # 3615:_NS:194, 3310:_NS:434      2922: _NS:445
frame_clip = {"AXIdentifier": "ShutterstockCollectionViewItem"}
frame_clips = {"AXIdentifier": "ShutterstockCollectionViewItem", "get_all":True}
image_clip = {"AXIdentifier": "ShutterstockCollectionViewItem"} # _NS:47

class collection:
    # [For Video]
    all = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_ALL'} #3630: _NS:38
    subscription = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_SUBSCRIBED'} #3630: _NS:55
    premium = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_PAY'} #3630: _NS:62
    # [For Photo]
    all_photo = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_PHOTO_ALL'}
    subscription_photo = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_PHOTO_SUBSCRIBED'}
    premium_photo = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_PHOTO_PAY'}

class sort_by:
    # [For Video]
    best_matched = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_BEST_MATCH'} #3630: _NS:106
    newest = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_NEWEST'} #3630: _NS:117
    random = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_RANDOM'} #3630: _NS:124
    popular = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_MOST_POPULAR'} #3630: _NS:131
    # [For Photo]
    best_matched_photo = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_PHOTO_BEST_MATCH'}
    newest_photo = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_PHOTO_NEWEST'}
    random_photo = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_PHOTO_RANDOM'}
    popular_photo = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_PHOTO_MOST_POPULAR'}
class video:
    scroll_bar_filter = {'AXIdentifier': 'IDC_GETTYIMAGES_VIDEO_FILTER_SCROLLER'} #3630: _NS:808

    class duration:
        all = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_DURATION_ALL'} #3630: _NS:155
        _30s = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_DURATION_30S_LESS'} #3630: _NS:163
        _1min = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_DURATION_60S_LESS'} #3630: _NS:170
        _2min = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_DURATION_60S_LONGER'} #3630: _NS:177

    class resolution:
        all = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_RESOLUTION_ALL'} #3630: _NS:201
        _4k = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_RESOLUTION_4K'} #3630: _NS:207
        hd = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_RESOLUTION_HD'} #3630: _NS:214
        sd = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_RESOLUTION_SD'} #3630: _NS:221

    class composition:
        close_up = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_CLOSE_UP'} #3630: _NS:245
        looking = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_LOOKING_AT_CAMERA'} #3630: _NS:252
        candid = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_CANDID'} #3630: _NS:259

    class viewpoint:
        lockdown = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_LOCKDOWN'} #3630: _NS:283
        panning = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_PANNING'} #3630: _NS:290
        tracking_shot = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_TRACKING_SHOT'} #3630: _NS:297
        aerial_view = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_AERIAL_VIEW'} #3630: _NS:306
        high_angle = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_HIGH_ANGLE_VIEW'} #3630: _NS:313
        low_angle = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_LOW_ANGLE_VIEW'} #3630: _NS:320
        tilt = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_TILT'} #3630: _NS:327
        point_view = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_POINT_OF_VIEW'} #3630: _NS:334

    class image_technique:
        real_time = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_REAL_TIME'} #3630: _NS:358
        time_lapse = {'AXIdentifier' : 'IDC_GETTYIMAGES_BTN_VIDEO_TIME_LAPSE'} #3630: _NS:365
        slow_motion = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_SLOW_MOTION'} #3630: _NS:372
        color = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_COLOR'} #3630: _NS:379
        black_white = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_BLACK_AND_WHITE'} #3630: _NS:386
        animation = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_ANIMATION'} #3630: _NS:393
        selective_focus = {'AXIdentifier': 'IDC_GETTYIMAGES_BTN_VIDEO_SELECTIVE_FOCUS'} #3630: _NS:400

    class thumbnail_icon:
        img_premium = [{'AXIdentifier': 'IDC_SHUTTERSTOCK_ITEM_DOLLAR', 'AXDescription': 'ic badge', 'AXRole': 'AXImage'}]

class photo:
    scroll_bar_filter = {'AXIdentifier': 'IDC_GETTYIMAGES_PHOTO_FILTER_SCROLLER'}
    class orientation:
        vertical_chx = {'AXTitle': 'Vertical', "AXSubrole": "AXToggle"}
        horizontal_chx = {'AXTitle': 'Horizontal', "AXSubrole": "AXToggle"}
        square_chx = {'AXTitle': 'Square', "AXSubrole": "AXToggle"}
        panoramic_chx = {'AXTitle': 'Panoramic Horizontal', "AXSubrole": "AXToggle"}

    class image_style:
        abstract_chx = {'AXTitle': 'Abstract', "AXSubrole": "AXToggle"}
        portrait_chx = {'AXTitle': 'Portrait', "AXSubrole": "AXToggle"}
        close_up_chx = {'AXTitle': 'Close-up', "AXSubrole": "AXToggle"}
        sparse_chx = {'AXTitle': 'Sparse', "AXSubrole": "AXToggle"}
        cut_out_chx = {'AXTitle': 'Cut out', "AXSubrole": "AXToggle"}
        full_frame_chx = {'AXTitle': 'Full frame', "AXSubrole": "AXToggle"}
        copy_space_chx = {'AXTitle': 'Copy space', "AXSubrole": "AXToggle"}
        macro_chx = {'AXTitle': 'Macro', "AXSubrole": "AXToggle"}
        still_life_chx = {'AXTitle': 'Still life', "AXSubrole": "AXToggle"}

    class number_people:
        no_people_chx = {'AXTitle': 'No people', "AXSubrole": "AXToggle"}
        one_person_chx = {'AXTitle': 'One person', "AXSubrole": "AXToggle"}
        two_people_chx = {'AXTitle': 'Two people', "AXSubrole": "AXToggle"}
        group_people_chx = {'AXTitle': 'Group of people', "AXSubrole": "AXToggle"}

