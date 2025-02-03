from ATFramework.pages.base_page import BasePage
from ATFramework.utils.log import logger
from ATFramework.utils.ocr import OCR
from ATFramework.utils.Image_Search import CompareImage
# from AppKit import NSScreen
try:
    from PIL import ImageGrab, Image
except Exception as e:
    logger(f"[Warning] {e}")
import time, datetime, os, copy
import inspect

class Main_Page(BasePage):
    """
    Author: Terence
    Date: 2020/08/04
    """
    # ******** Includes locators at Main_Page ***********
    # Note:
    # 1. Try to use general locator to avoid MUI problem
    # 2. If can't find via inspector, use (.page_source) to get actually source
    # ***************************************************
    # ============================ Locators ============================

    # Activate DLG
    btn_activate_this_computer = {'AXTitle': 'Activate this Computer', 'AXRole': 'AXButton'}

    # tab
    #old tab_main_edit = {'AXIdentifier': 'IDC_BTN_EDIT'}
    tab_main_edit = {'AXHelp': 'Create and edit your video', 'AXRole': 'AXButton'}
    #old tab_main_product = {'AXIdentifier': 'IDC_BTN_PRODUCE'}
    tab_main_produce = {'AXHelp': 'Output your video to a file, device, or upload it to a social media web site'}
    # button
    #old: btn_display_all_media = {'AXIdentifier': 'IDC_LIBRARY_BUTTON_FILTER_ALL'}
    btn_display_all_media = {'AXIdentifier': 'IDC_LIBRARY_BTN_FILTER_ALL'}
    #old: btn_display_videos_only = {'AXIdentifier': 'IDC_LIBRARY_BUTTON_FILTER_VIDEO'}
    btn_display_videos_only = {'AXIdentifier': 'IDC_LIBRARY_BTN_FILTER_VIDEO'}
    #old: btn_display_images_only = {'AXIdentifier': 'IDC_LIBRARY_BUTTON_FILTER_IMAGE'}
    btn_display_images_only = {'AXIdentifier': 'IDC_LIBRARY_BTN_FILTER_IMAGE'}
    #old: btn_display_audio_only = {'AXIdentifier': 'IDC_LIBRARY_BUTTON_FILTER_AUDIO'}
    btn_display_audio_only = {'AXIdentifier': 'IDC_LIBRARY_BTN_FILTER_AUDIO'}
    #old: btn_icon_view = {'AXIdentifier': '_NS:33'}
    btn_icon_view = {'AXIdentifier': 'IDC_LIBRARY_BTN_ICON_VIEW'}
    #old: btn_details_view = {'AXIdentifier': '_NS:12'}
    btn_details_view = {'AXIdentifier': 'IDC_LIBRARY_BTN_DETAILS_VIEW'}
    #old; btn_library_menu = {'AXIdentifier': '_NS:790'}
    btn_library_menu = {'AXIdentifier': 'IDC_LIBRARY_BTN_MENU'}

    # main top-btn
    #old btn_import_media = {'AXHelp': 'Import media', 'AXRole': 'AXButton'}
    btn_import_media = {'AXIdentifier': 'IDC_LIBRARY_BTN_IMPORT_MEDIA', 'AXRole': 'AXButton'}
    # main left-btn
    #old btn_media_room = {'AXIdentifier': 'IDC_LIBRARY_BUTTON_MEDIAROOM', 'AXRole': 'AXButton'}
    btn_media_room = {'AXIdentifier': 'IDC_LIBRARY_BTN_MEDIAROOM', 'AXRole': 'AXButton'}
    #old btn_effect_room = {'AXIdentifier': 'IDC_LIBRARY_BUTTON_EFFECTROOM', 'AXRole': 'AXButton'}
    btn_effect_room = {'AXIdentifier': 'IDC_LIBRARY_BTN_EFFECTROOM', 'AXRole': 'AXButton'}
    #old btn_pip_room = {'AXIdentifier': 'IDC_LIBRARY_BUTTON_PIPROOM', 'AXRole': 'AXButton'}
    btn_pip_room = {'AXIdentifier': 'IDC_LIBRARY_BTN_PIPROOM', 'AXRole': 'AXButton'}
    #old btn_particle_room = {'AXIdentifier': 'IDC_LIBRARY_BUTTON_PARTICLEROOM', 'AXRole': 'AXButton'}
    btn_particle_room = {'AXIdentifier': 'IDC_LIBRARY_BTN_PARTICLEROOM', 'AXRole': 'AXButton'}
    #old btn_title_room = {'AXIdentifier': 'IDC_LIBRARY_BUTTON_TITLEROOM', 'AXRole': 'AXButton'}
    btn_title_room = {'AXIdentifier': 'IDC_LIBRARY_BTN_TITLEROOM', 'AXRole': 'AXButton'}
    #old btn_transition_room = {'AXIdentifier': 'IDC_LIBRARY_BUTTON_TRANSITIONROOM', 'AXRole': 'AXButton'}
    btn_transition_room = {'AXIdentifier': 'IDC_LIBRARY_BTN_TRANSITIONROOM', 'AXRole': 'AXButton'}
    #old btn_audiomixing_room = {'AXIdentifier': 'IDC_LIBRARY_BUTTON_AUDIOMIXINGROOM', 'AXRole': 'AXButton'}
    btn_audiomixing_room = {'AXIdentifier': 'IDC_LIBRARY_BTN_AUDIOMIXINGROOM', 'AXRole': 'AXButton'}
    #old btn_recording_room = {'AXIdentifier': 'IDC_LIBRARY_BUTTON_VOICEOVER', 'AXRole': 'AXButton'}
    btn_recording_room = {'AXIdentifier': 'menuVoiceOver', 'AXRole': 'AXMenuItem'}
    #old btn_subtitle_room = {'AXIdentifier': 'IDC_LIBRARY_BUTTON_SUBTITLEROOM', 'AXRole': 'AXButton'}
    btn_subtitle_room = {'AXIdentifier': 'menuSubtitle', 'AXRole': 'AXMenuItem'}
    btn_room_express = {'AXIdentifier': '_NS:886', 'AXRole': 'AXButton'}

    # effect page
    el_effect_setting = {'AXIdentifier': 'IDC_EFFECTSETTING_SCROLLVIEW_FLIPPEDVIEW', 'AXRole': 'AXScrollArea'}

    # tip area(mid-area)
    btn_insert_on_selected_track = {'AXIdentifier': 'IDC_TIPSAREA_BTN_ADDTOVIDEOTRACK', 'AXRole': 'AXButton'}
    btn_add_to_effect_track = {'AXIdentifier': 'IDC_TIPSAREA_BTN_ADDTOEFFECTTRACK'}
    btn_tipsarea_modify = {'AXIdentifier': 'IDC_TIPSAREA_BTN_TRANSITION', 'AXRole': 'AXCheckBox'}
    btn_tipsarea_tool = {'AXIdentifier': 'IDC_TIPSAREA_BTN_TOOLS', 'AXRole': 'AXButton'}
    btn_tipsarea_video_collage = {'AXIdentifier': 'IDC_TIPSAREA_BTN_TITLE_DESIGNER', 'AXRole': 'AXButton'}

    # [Jamie add] >> 09/21 Build
    context_menu_Insert = {'AXIdentifier': '_NS:41', 'AXRole': 'AXMenuItem'}
    btn_tipsarea_Trim = {'AXIdentifier': 'IDC_TIPSAREA_BTN_TRIM', 'AXHelp': 'Trim unwanted portions from the selected clip (⌥⌘T)'}
    btn_crop_image = {'AXIdentifier': 'IDC_TIPSAREA_BTN_CROP', 'AXHelp': 'Crop the selected image'}

    # For 09/19 Build
    btn_tipsarea_Trim = {'AXIdentifier': 'IDC_TIPSAREA_BTN_TRIM'}
    btn_crop_image = {'AXIdentifier': 'IDC_TIPSAREA_BTN_CROP'}
    # [Jamie add] <<

    # timeline
    # v2219
    el_timeline_left_cell_table = {'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACKHEAD', 'AXRole': 'AXTable'}
    # v2219
    el_timeline_right_cell_table = {'AXIdentifier': 'IDC_TIMELINE_TABLEVIEW_TRACK', 'AXRole': 'AXTable'}
    #old btn_transition_timeline = {'AXIdentifier': '_NS:113'}
    btn_transition_timeline = {'AXIdentifier': '_NS:115'}
    btn_transition_timeline_01 = {'AXIdentifier': '_NS:153', 'AXRole': 'AXButton'}
    split_group_timeline_timecode = [['standard window', 'type'], ['group', 'type'], ['split group', 'type'],
                                     ['scroll area', 'type', -8],
                                     ['collection', 'type'], ['section', 'type']]
    split_group_el = [['standard window', 'type'], ['group', 'type'], ['split group', 'type']]
    split_group_timeline_area = [['standard window', 'type'], ['group', 'type'], ['split group', 'type'],
                                 ['split group', 'type', 6]]

    # [Jamie add] >> 09/21 Build
    image_timeline_range_r = {'AXIdentifier': 'IDC_TIMELINE_IMAGE_RSINDICATOR_RIGHT'}
    # [Jamie add] <<

    # area
    area_contents = {'AXRole': 'AXList', 'AXIdentifier': '_NS:348'}
    # old: area_room_frame = {'AXIdentifier': '_NS:135', 'AXRole': 'AXSplitGroup'}
    area_room_frame = {'AXIdentifier': 'IDD_UPPERVIEW', 'AXRole': 'AXSplitGroup'}
    area_timeline_frame = {'AXIdentifier': '_NS:9', 'AXRole': 'AXSplitGroup'}
    area_cell_frame = {'AXIdentifier': '_NS:9', 'AXRole': 'AXTable'}

    # column
    column_search_text_field = {'AXHelp': 'Search the library'}
    column_new_tag = {'AXIdentifier': 'RoomTagTextField', 'AXValue': 'New Tag'}
    column_effectroom_new_tag = {'AXIdentifier': 'RoomTagOutlineViewTextField', 'AXValue': 'New Tag'}
    column_piproom_new_tag = {'AXIdentifier': 'RoomTagTextField', 'AXRole': 'AXTextField'}

    # spliter(line)
    spliter_between_mediaroom_and_preview = {'AXOrientation': 'AXVerticalOrientation', 'AXRole': 'AXSplitter'}

    # group
    #old group_edit_page_top = {'AXIdentifier': '_NS:135', 'AXRole': 'AXSplitGroup'}
    group_edit_page_top = {'AXIdentifier': 'IDD_UPPERVIEW', 'AXRole': 'AXSplitGroup'}

    # slider
    #old slider_main_playback = {'AXIdentifier': '_NS:364', 'AXOrientation': 'AXHorizontalOrientation', 'AXRole': 'AXSlider'}
    slider_main_playback = {'AXIdentifier': 'IDC_DISPLAY_SLIDER_PLAYBACK', 'AXOrientation': 'AXHorizontalOrientation', 'AXRole': 'AXSlider'}

    # drop-down menu
    #old drop_down_menu_effect_room_category = {'AXIdentifier': '_NS:936', 'AXRole': 'AXButton'}
    drop_down_menu_effect_room_category = {'AXIdentifier': '_NS:765', 'AXRole': 'AXButton'}

    # icon
    icon_x = {'AXDescription': 'cancel', 'AXRole': 'AXButton'}
    #old icon_x_setting_frame = {'AXIdentifier': '_NS:68', 'AXRole': 'AXButton'}
    icon_x_setting_frame = {'AXIdentifier': 'IDC_KEYFRAMEROOM_BTN_LEAVE', 'AXRole': 'AXButton'}
    #old icon_display_hide_explorer_view = {'AXHelp': 'Display/Hide explorer view', 'AXRole': 'AXButton'}
    icon_display_hide_explorer_view = {'AXIdentifier': '_NS:256', 'AXRole': 'AXButton'}
    #old icon_add_a_new_tag = {'AXHelp': 'Add a new tag', 'AXRole': 'AXButton'}
    icon_add_a_new_tag = {'AXIdentifier': '_NS:12', 'AXRole': 'AXButton'}
    #old icon_delete_the_selected_tag = {'AXHelp': 'Delete the selected tag', 'AXRole': 'AXButton'}
    icon_delete_the_selected_tag = {'AXIdentifier': '_NS:33', 'AXRole': 'AXButton'}
    #old icon_play = {'AXIdentifier': 'IDC_DISPLAY_BUTTONPLAY', 'AXRole': 'AXButton'}
    icon_play = {'AXIdentifier': 'IDC_DISPLAY_BTN_PLAY', 'AXRole': 'AXButton'}
    #old icon_pause = {'AXHelp': 'Pause (Space)', 'AXRole': 'AXButton'}
    icon_pause = {'AXIdentifier': 'IDC_DISPLAY_BTN_PAUSE', 'AXRole': 'AXButton'}
    #old icon_stop = {'AXHelp': 'Stop (⌘/)', 'AXRole': 'AXButton'}
    icon_stop = {'AXIdentifier': '_NS:152', 'AXRole': 'AXButton'}

    # Alert
    img_critical_alert = {'AXDescription': 'PowerDirector critical alert'}
    img_usernotificationcenter_alert = {'AXDescription': 'UserNotificationCenter alert'}
    img_pdr_alert = {'AXDescription': 'PowerDirector alert'}
    btn_no = {'AXTitle': 'No', 'AXRole': 'AXButton'}
    btn_ok = {'AXTitle': 'OK', 'AXRole': 'AXButton'}
    btn_apply = {'AXTitle': 'Apply', 'AXRole': 'AXButton'}
    btn_yes = {'AXTitle': 'Yes', 'AXRole': 'AXButton'}
    btn_cancel = {'AXTitle': 'Cancel', 'AXRole': 'AXButton'}
    btn_dontallow = {'AXTitle': 'Don’t Allow', 'AXRole': 'AXButton'}
    btn_saveas = {'AXTitle': 'Save As', 'AXRole': 'AXButton'}

    # Jamie debug for v2401
    #You have not saved the changes you made to current project.
    img_critical_alert = {'AXIdentifier': '_NS:11', 'AXRole': 'AXImage'}
    dialog_PDR_alert = {'AXIdentifier': '_NS:10', 'AXRole': 'AXWindow'}

    # string
    str_media_content = {'AXIdentifier': 'RoomTagTextField', 'AXValue': 'Media Content'}
    str_color_boards = {'AXIdentifier': 'RoomTagTextField', 'AXValue': 'Color Boards'}
    str_background_music = {'AXIdentifier': 'RoomTagTextField', 'AXValue': 'Background Music'}
    str_sound_clips = {'AXIdentifier': 'RoomTagTextField', 'AXValue': 'Sound Clips'}

    # for verification
    str_timecode_none = {'AXValue': '--:--:--:--'}
    str_aberration = {'AXValue': 'Aberration'}
    str_ballon = {'AXValue': 'ballon.jpg'}
    str_food = {'AXValue': 'Food.jpg'}
    str_free_templates = {'AXValue': 'Free Templates'}
    str_effect_a = {'AXValue': 'Effect-A'}
    str_clover_01 = {'AXValue': 'Clover_01'}
    str_audio1 = {'AXValue': 'Audio 1', 'AXRole': 'AXStaticText'}
    str_mute_all_tracks_when_recording = {'AXTitle': 'Mute all tracks when recording'}
    btn_subtitle_info = {'AXIdentifier': '_NS:169', 'AXRole': 'AXButton'}
    img_effecticon = {'AXDescription': 'list icon effect'}
    img_pipicon = {'AXDescription': 'list icon pip'}
    img_particleicon = {'AXDescription': 'list icon particle'}
    img_titleicon = {'AXDescription': 'list icon title'}
    img_transitionicon = {'AXDescription': 'list icon transition'}

    # menubar
    '''
    #old
    menubar_pdr = {'AXIdentifier': '_NS:158', 'AXTitle': 'PowerDirector', 'AXRole': 'AXMenuBarItem'}
    menubar_file = {'AXIdentifier': '_NS:209', 'AXTitle': 'File', 'AXRole': 'AXMenuBarItem'}
    menubar_file_save_as = {'AXIdentifier': '_NS:106', 'AXTitle': 'Save Project As...'}
    menubar_file_open_project = {'AXIdentifier': '_NS:96', 'AXTitle': 'Open Project...'}
    menubar_plugins = {'AXIdentifier': '_NS:215', 'AXTitle': 'Plugins', 'AXRole': 'AXMenuBarItem'}
    menubar_plugins_video_collage_designer = {'AXIdentifier': 'IDM_MENU_PLUGINS_OPEN_VIDEO_COLLAGE', 'AXRole': 'AXMenuItem'}
    '''
    menubar_pdr = {'AXTitle': 'PowerDirector', 'AXRole': 'AXMenuBarItem'}
    menubar_file = {'AXTitle': 'File', 'AXRole': 'AXMenuBarItem'}
    menubar_file_save_as = {'AXIdentifier': 'IDM_MENU_FILE_SAVE_PROJECT_AS', 'AXTitle': 'Save Project As...'}
    menubar_file_open_project = {'AXIdentifier': 'IDM_MENU_FILE_OPEN_PROJECT', 'AXTitle': 'Open Project...'}
    menubar_plugins = {'AXTitle': 'Plugins', 'AXRole': 'AXMenuBarItem'}
    menubar_plugins_video_collage_designer = {'AXIdentifier': 'IDM_MENU_PLUGINS_OPEN_VIDEO_COLLAGE',
                                              'AXRole': 'AXMenuItem'}

    # save DLG
    icon_disclosure_triangle = {'AXIdentifier': 'NS_OPEN_SAVE_DISCLOSURE_TRIANGLE', 'AXRole': 'AXDisclosureTriangle'}
    dlg_save_file = {'AXRole': 'AXWindow', 'AXSubrole': 'AXDialog', 'AXTitle': 'Save file'}
    column_save_as_name = {'AXIdentifier': '_NS:111', 'AXRole': 'AXTextField'}
    btn_dlg_save = {'AXTitle': 'Save', 'AXRole': 'AXButton'}
    #old btn_dlg_ignore = {'AXIdentifier': '_NS:60', 'AXTitle': 'Ignore All'}
    btn_dlg_ignore = {'AXRole': 'AXButton', 'AXTitle': 'Ignore All'}
    btn_dlg_replace = {'AXTitle': 'Replace', 'AXRole': 'AXButton'}
    column_where_projects = {'AXTitle': 'Where:', 'AXValue': 'Projects', 'AXRole': 'AXPopUpButton'}
    column_where_downloads = {'AXTitle': 'Where:', 'AXValue': 'Downloads', 'AXRole': 'AXPopUpButton'}

    # load DLG
    dlg_open = {'AXDescription': 'open', 'AXRole': 'AXSheet'}

    # effect settings(frame)
    str_effect_settings = {'AXValue': 'Effect Settings', 'AXRole': 'AXStaticText'}
    btn_keyframe = {'AXTitle': 'Keyframe', 'AXRole': 'AXButton'}



    # transition settings(frame)
    str_transition_settings = {'AXValue': 'Transition Settings', 'AXRole': 'AXStaticText'}

    # Pip room
    btn_create_a_new_pip = {'AXIdentifier': 'IDC_LIBRARY_BTN_NEWTEMPLATE', 'AXRole': 'AXButton'}
    btn_modify_the_selected = {'AXIdentifier': 'IDC_LIBRARY_BTN_MODIFYTEMPLATE', 'AXRole': 'AXButton'}

    # pip designer dlg
    str_pipdesigner_default = {'AXValue': 'PiP Designer  |  Default', 'AXRole': 'AXStaticText'}
    #old column_pipname = {'AXIdentifier': '_NS:49', 'AXRole': 'AXTextField'}
    # v2219
    el_save_as_template_dlg = {'AXTitle': 'Save as Template', 'AXRole': 'AXWindow'}
    section_pipdesigner_timeline = {'AXOrientation': 'AXHorizontalOrientation', 'AXRole': 'AXList', 'AXSubrole': 'AXSectionList'}
    #old outline_pipdesigner = {'AXIdentifier': '_NS:147', 'AXRole': 'AXOutline'}
    outline_pipdesigner = {'AXIdentifier': '_NS:195', 'AXRole': 'AXOutline'}
    #old area_pipdesigner_right_frame = {'AXIdentifier': '_NS:157', 'AXRole': 'AXSplitGroup'}
    area_pipdesigner_right_frame = {'AXIdentifier': '_NS:138', 'AXRole': 'AXSplitGroup'}
    #old outline_pipdesigner_left = {'AXIdentifier': '_NS:41', 'AXRole': 'AXOutline'}
    outline_pipdesigner_left = {'AXIdentifier': 'IDC_PIP_DESIGNER_OUTLINEVIEW_CONTAINER', 'AXRole': 'AXOutline'}
    checkbox_ease_in = {'AXTitle': 'Ease in', 'AXRole': 'AXCheckBox'}
    checkbox_ease_out = {'AXTitle': 'Ease out', 'AXRole': 'AXCheckBox'}
    #old scroll_bar_pipdesigner_right = {'AXIdentifier': '_NS:9', 'AXOrientation': 'AXVerticalOrientation', 'AXRole': 'AXScrollBar'}
    scroll_bar_pipdesigner_right = {'AXIdentifier': '_NS:115', 'AXOrientation': 'AXVerticalOrientation',
                                    'AXRole': 'AXScrollBar'}
    #old scroll_bar_pipdesigner_left = {'AXIdentifier': '_NS:26', 'AXOrientation': 'AXVerticalOrientation', 'AXRole': 'AXScrollBar'}
    scroll_bar_pipdesigner_left = {'AXIdentifier': 'IDC_PIP_DESIGNER_SCROLLBAR_Y', 'AXOrientation': 'AXVerticalOrientation',
                                   'AXRole': 'AXScrollBar'}
    #old scroll_bar_pipdesigner_preview_bottom = {'AXIdentifier': '_NS:196', 'AXRole': 'AXScrollBar', 'AXOrientation': 'AXHorizontalOrientation'}
    scroll_bar_pipdesigner_preview_bottom = {'AXIdentifier': '_NS:182', 'AXRole': 'AXScrollBar',
                                             'AXOrientation': 'AXHorizontalOrientation'}
    #old scroll_bar_pipdesigner_preview_right = {'AXIdentifier': '_NS:120', 'AXRole': 'AXScrollBar', 'AXOrientation': 'AXVerticalOrientation'}
    scroll_bar_pipdesigner_preview_right = {'AXIdentifier': '_NS:206', 'AXRole': 'AXScrollBar',
                                            'AXOrientation': 'AXVerticalOrientation'}
    #old dropper_pipdesigner_chroma_key = {'AXIdentifier': '_NS:83', 'AXRole': 'AXButton'}
    dropper_pipdesigner_chroma_key = {'AXIdentifier': 'IDC_PIP_DESIGNER_CHROMAKEY_BTN_DROPER', 'AXRole': 'AXButton'}
    btn_pipdesigner_chroma_key_delete = {'AXIdentifier': '_NS:129', 'AXRole': 'AXButton'}
    #old slider_pipdesigner_chroma_key_color_range = {'AXIdentifier': '_NS:9', 'AXRole': 'AXSlider'}
    slider_pipdesigner_chroma_key_color_range = {'AXIdentifier': 'IDC_PIP_DESIGNER_CHROMAKEY_SLIDER_COLORRANGE', 'AXRole': 'AXSlider'}
    #old slider_pipdesigner_chroma_key_denoise = {'AXIdentifier': '_NS:60', 'AXRole': 'AXSlider'}
    slider_pipdesigner_chroma_key_denoise = {'AXIdentifier': 'IDC_PIP_DESIGNER_CHROMAKEY_SLIDER_DENOISE', 'AXRole': 'AXSlider'}
    #old btn_pipdesigner_chroma_key_add_new_key = {'AXIdentifier': '_NS:15', 'AXRole': 'AXButton'}
    btn_pipdesigner_chroma_key_add_new_key = {'AXIdentifier': 'IDC_PIP_DESIGNER_CHROMAKEY_BTN_ADDKEY', 'AXRole': 'AXButton'}
    #old slider_pipdesigner_border_size = {'AXIdentifier': '_NS:42', 'AXRole': 'AXSlider'}
    slider_pipdesigner_border_size = {'AXIdentifier': 'IDC_PIP_DESIGNER_BORDER_SLIDER_SIZE', 'AXRole': 'AXSlider'}
    #old slider_pipdesigner_border_blur = {'AXIdentifier': '_NS:70', 'AXRole': 'AXSlider'}
    slider_pipdesigner_border_blur = {'AXIdentifier': 'IDC_PIP_DESIGNER_BORDER_SLIDER_BLUR', 'AXRole': 'AXSlider'}
    #old slider_pipdesigner_border_opacity = {'AXIdentifier': '_NS:95', 'AXRole': 'AXSlider'}
    slider_pipdesigner_border_opacity = {'AXIdentifier': 'IDC_PIP_DESIGNER_BORDER_SLIDER_OPACITY', 'AXRole': 'AXSlider'}
    #old drop_down_menu_pipdesigner_border_fill_type = {'AXIdentifier': '_NS:120', 'AXRole': 'AXButton'}
    drop_down_menu_pipdesigner_border_fill_type = {'AXIdentifier': 'IDC_PIP_DESIGNER_BORDER_BTN_FILLTYPE', 'AXRole': 'AXButton'}
    #old slider_pipdesigner_shadow_distance = {'AXIdentifier': '_NS:115', 'AXRole': 'AXSlider'}
    slider_pipdesigner_shadow_distance = {'AXIdentifier': 'IDC_PIP_DESIGNER_SHADOW_SLIDER_DISTANCE', 'AXRole': 'AXSlider'}
    #old slider_pipdesigner_shadow_blur = {'AXIdentifier': '_NS:142', 'AXRole': 'AXSlider'}
    slider_pipdesigner_shadow_blur = {'AXIdentifier': 'IDC_PIP_DESIGNER_SHADOW_SLIDER_BLUR', 'AXRole': 'AXSlider'}
    #old slider_pipdesigner_shadow_opacity = {'AXIdentifier': '_NS:35', 'AXRole': 'AXSlider'}
    slider_pipdesigner_shadow_opacity = {'AXIdentifier': 'IDC_PIP_DESIGNER_SHADOW_SLIDER_OPACITY', 'AXRole': 'AXSlider'}
    #old checkbox_pipdesigner_flip_upside_down = {'AXIdentifier': '_NS:85', 'AXRole': 'AXCheckBox'}
    checkbox_pipdesigner_flip_upside_down = {'AXIdentifier': 'IDC_PIP_DESIGNER_FLIP_BTN_VERTICAL', 'AXRole': 'AXCheckBox'}
    #old checkbox_pipdesigner_flip_left_to_right = {'AXIdentifier': '_NS:9', 'AXRole': 'AXCheckBox'}
    checkbox_pipdesigner_flip_left_to_right = {'AXIdentifier': 'IDC_PIP_DESIGNER_FLIP_BTN_HORIZONAL', 'AXRole': 'AXCheckBox'}
    #old checkbox_pipdesigner_fade_in = {'AXIdentifier': '_NS:83', 'AXRole': 'AXCheckBox'}
    checkbox_pipdesigner_fade_in = {'AXIdentifier': 'IDC_PIP_DESIGNER_FADE_BTN_IN', 'AXRole': 'AXCheckBox'}
    checkbox_pipdesigner_fade_out = {'AXIdentifier': '_NS:9', 'AXRole': 'AXCheckBox'}

    # title designer dlg
    str_titledesigner_default = {'AXValue': 'Title Designer | Default', 'AXRole': 'AXStaticText'}
    #old btn_titledesigner_add_title = {'AXIdentifier': '_NS:147', 'AXRole': 'AXButton'}
    btn_titledesigner_add_title = {'AXIdentifier': '_NS:181', 'AXRole': 'AXButton'}
    btn_titledesigner_add_particle = {'AXIdentifier': '_NS:155', 'AXRole': 'AXButton'}
    btn_titledesigner_add_pip = {'AXIdentifier': '_NS:171', 'AXRole': 'AXButton'}
    btn_titledesigner_add_background = {'AXIdentifier': '_NS:179', 'AXRole': 'AXButton'}
    btn_titledesigner_del_background = {'AXIdentifier': '_NS:187', 'AXRole': 'AXButton'}
    #old btn_titledesigner_undo = {'AXIdentifier': '_NS:12', 'AXRole': 'AXButton'}
    btn_titledesigner_undo = {'AXIdentifier': '_NS:71', 'AXRole': 'AXButton'}
    #old btn_titledesigner_redo = {'AXIdentifier': '_NS:33', 'AXRole': 'AXButton'}
    btn_titledesigner_redo = {'AXIdentifier': '_NS:79', 'AXRole': 'AXButton'}
    #old btn_titledesigner_basic = {'AXIdentifier': '_NS:124', 'AXRole': 'AXButton'}
    btn_titledesigner_basic = {'AXIdentifier': '_NS:153', 'AXRole': 'AXButton'}
    #old btn_titledesigner_advanced = {'AXIdentifier': '_NS:132', 'AXRole': 'AXButton'}
    btn_titledesigner_advanced = {'AXIdentifier': '_NS:164', 'AXRole': 'AXButton'}
    #old tab_titledesigner_object = {'AXIdentifier': '_NS:12', 'AXRole': 'AXButton', 'AXTitle': 'Object'}
    tab_titledesigner_object = {'AXIdentifier': '_NS:80', 'AXRole': 'AXButton', 'AXTitle': 'Object'}
    #old tab_titledesigner_effect = {'AXIdentifier': '_NS:32', 'AXRole': 'AXButton', 'AXTitle': 'Effect'}
    tab_titledesigner_animation = {'AXIdentifier': '_NS:96', 'AXRole': 'AXButton', 'AXTitle': 'Animation'}
    outline_titledesigner_object = [['dialog', 'type'], ['split group', 'type'], ['scroll area', 'type'],
                                    ['outline', 'type']]
    scroll_bar_titledesigner_object = [['dialog', 'type'], ['split group', 'type'], ['scroll area', 'type'],
                                       ['scroll bar', 'type']]
    scroll_bar_titledesigner_timeline = {'AXIdentifier': '_NS:115', 'AXRole': 'AXScrollBar'}
    #old outline_titledesigner_cell = [['dialog', 'type'], ['split group', 'type'], ['split group', 'type'], ['scroll area', 'type', 29], ['outline', 'type']]
    outline_titledesigner_cell = {'AXIdentifier': '_NS:195', 'AXRole': 'AXOutline'}
    collection_titledesigner_timecode = [['dialog', 'type'], ['split group', 'type'], ['split group', 'type'],
                                         ['scroll area', 'type', 30], ['collection', 'type']]
    #old outline_titledesigner_timeline = [['dialog', 'type'], ['split group', 'type'], ['split group', 'type'], ['scroll area', 'type', 31], ['outline', 'type']]
    outline_titledesigner_timeline = {'AXIdentifier': '_NS:255', 'AXRole': 'AXOutline'}
    #old area_titledesigner_preview = {'AXIdentifier': '_NS:555', 'AXRole': 'AXScrollArea'}
    area_titledesigner_preview = {'AXIdentifier': '_NS:278', 'AXRole': 'AXScrollArea'}
    dlg_titledesigner_color_dlg = {'AXIdentifier': '_NS:12', 'AXRole': 'AXSplitGroup'}
    #old icon_titledesigner_play = {'AXIdentifier': '_NS:54', 'AXRole': 'AXButton'}
    icon_titledesigner_play = {'AXIdentifier': '_NS:94', 'AXRole': 'AXButton'}
    #old icon_titledesigner_stop = {'AXIdentifier': '_NS:76', 'AXRole': 'AXButton'}
    icon_titledesigner_stop = {'AXIdentifier': '_NS:103', 'AXRole': 'AXButton'}
    #old icon_titledesigner_pause = {'AXIdentifier': '_NS:62', 'AXRole': 'AXButton'}
    icon_titledesigner_pause = {'AXIdentifier': '_NS:94', 'AXRole': 'AXButton'}

    # mask designer
    dlg_maskdesigner = {'AXIdentifier': '_NS:10', 'AXRole': 'AXWindow'}
    #old icon_maskdesigner_play = {'AXIdentifier': '_NS:12', 'AXRole': 'AXButton'}
    icon_maskdesigner_play = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_PLAY', 'AXRole': 'AXButton'}
    #old icon_maskdesigner_stop = {'AXIdentifier': '_NS:41', 'AXRole': 'AXButton'}
    icon_maskdesigner_stop = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_STOP', 'AXRole': 'AXButton'}
    #old icon_maskdesigner_pause = {'AXIdentifier': '_NS:33', 'AXRole': 'AXButton'}
    # need new pause btn..
    icon_maskdesigner_pause = {'AXIdentifier': 'IDC_MASK_DESIGNER_BTN_PLAY', 'AXRole': 'AXButton'}

    # duration setting dlg
    dlg_duration_settings = {'AXTitle': 'Duration Settings', 'AXRole': 'AXWindow'}

    # audiomixing dlg
    #old
    '''
    area_audiomixing_group = [['standard window', 'type'], ['group', 'type'], ['split group', 'type'],
                              ['split group', 'type', 0], ['scroll area', 'type'], ['collection', 'type'],
                              ['section', 'type']]
    area_audiomixing_group1 = [['standard window', 'type'], ['group', 'type'], ['split group', 'type'],
                               ['split group', 'type', 0], ['scroll area', 'type', 9], ['collection', 'type'],
                               ['section', 'type']]
    '''
    area_audiomixing_group = [['standard window', 'type'], ['group', 'type'], ['split group', 'type'],
                              ['split group', 'type', 0], ['group', 'type', 0], ['scroll area', 'type'], ['collection', 'type'],
                              ['section', 'type']]
    area_audiomixing_group1 = [['standard window', 'type'], ['group', 'type'], ['split group', 'type'],
                               ['split group', 'type', 0], ['group', 'type', 0], ['scroll area', 'type', 9], ['collection', 'type'],
                               ['section', 'type']]
    #old btn_audiomixing_fade_in = {'AXIdentifier': '_NS:234', 'AXRole': 'AXButton'}
    #old btn_audiomixing_fade_out = {'AXIdentifier': '_NS:239', 'AXRole': 'AXButton'}
    btn_audiomixing_fade_in = {'AXIdentifier': '_NS:257', 'AXRole': 'AXButton'}
    btn_audiomixing_fade_out = {'AXIdentifier': '_NS:262', 'AXRole': 'AXButton'}


    # recording room
    btn_recording_preferences = {'AXTitle': 'Preferences', 'AXRole': 'AXButton'}
    str_caption_recording_preferences = {'AXValue': 'Recording Preferences', 'AXRole': 'AXStaticText'}
    checkbox_recording_time_limit = {'AXTitle': 'Time limit', 'AXRole': 'AXCheckBox'}
    checkbox_recodingg_3second_delay = {'AXTitle': 'Add a 3 second delay before recording', 'AXRole': 'AXCheckBox'}
    checkbox_recording_fade_in = {'AXTitle': 'Auto fade-in at beginning of recording', 'AXRole': 'AXCheckBox'}
    checkbox_recording_fade_out = {'AXTitle': 'Auto fade-out at end of recording', 'AXRole': 'AXCheckBox'}
    #old btn_recording_record = {'AXIdentifier': '_NS:163', 'AXRole': 'AXButton'}
    btn_recording_record = {'AXIdentifier': '_NS:101', 'AXRole': 'AXButton'}
    #old btn_recording_stop = {'AXIdentifier': '_NS:171', 'AXRole': 'AXButton'}
    btn_recording_stop = {'AXIdentifier': '_NS:139', 'AXRole': 'AXButton'}
    drop_down_menu_recording_seconds = {'AXIdentifier': '_NS:123', 'AXRole': 'AXButton'}
    #old str_recording_value = {'AXIdentifier': '_NS:114', 'AXRole': 'AXStaticText'}
    str_recording_value = {'AXIdentifier': '_NS:286', 'AXRole': 'AXStaticText'}
    checkbox_recording_mute = {'AXTitle': 'Mute all tracks when recording', 'AXRole': 'AXCheckBox'}
    slider_recording = {'AXRole': 'AXSlider'}

    # subtitle room
    #old table_subtitle = {'AXIdentifier': '_NS:177', 'AXRole': 'AXTable'}
    table_subtitle = {'AXIdentifier': '_NS:196', 'AXRole': 'AXTable'}
    #old btn_subtitle_add = {'AXIdentifier': '_NS:149', 'AXRole': 'AXButton'}
    btn_subtitle_add = {'AXIdentifier': '_NS:116', 'AXRole': 'AXButton'}
    #old btn_subtitle_font = {'AXIdentifier': '_NS:154', 'AXRole': 'AXButton'}
    btn_subtitle_font = {'AXIdentifier': '_NS:178', 'AXRole': 'AXButton'}

    # subtitle font dlg
    #old checkbox_subtitle_shadow = {'AXIdentifier': '_NS:182', 'AXRole': 'AXCheckBox'}
    checkbox_subtitle_shadow = {'AXIdentifier': '_NS:148', 'AXRole': 'AXCheckBox'}

    # trim dlg
    dlg_videocollagedesigner_trim = {'AXIdentifier': '_NS:10', 'AXRole': 'AXWindow'}

    # video collage frame
    #old dlg_video_collage_designer = {'AXIdentifier': '_NS:10', 'AXRole': 'AXWindow', 'AXSubrole': 'AXDialog'}
    dlg_video_collage_designer = {'AXTitle': 'Video Collage Designer', 'AXRole': 'AXWindow', 'AXSubrole': 'AXDialog'}
    frame_video_collage = {'AXIdentifier': '_NS:89', 'AXRole': 'AXSplitGroup'}
    #old drop_down_menu_video_collage_designer_media = {'AXIdentifier': '_NS:34', 'AXRole': 'AXButton'}
    drop_down_menu_video_collage_designer_media = {'AXIdentifier': '_NS:37', 'AXRole': 'AXButton'}
    btn_video_collage_designer_auto_fill = {'AXIdentifier': 'IDC_VIDEO_COLLAGE_BUTTON_AUTO_FILL', 'AXRole': 'AXButton'}
    icon_video_collage_designer_play_btn = {'AXIdentifier': 'IDC_VIDEO_COLLAGE_BUTTON_PLAY', 'AXRole': 'AXButton'}
    #old icon_video_collage_designer_pause_btn = {'AXIdentifier': '_NS:15', 'AXHelp': 'Pause (Space)', 'AXRole': 'AXButton'}
    icon_video_collage_designer_pause_btn = {'AXIdentifier': '_NS:15', 'AXRole': 'AXButton'}
    #old icon_video_collage_designer_stop_btn = {'AXIdentifier': '_NS:54', 'AXHelp': 'Stop (⌘/)', 'AXRole': 'AXButton'}
    icon_video_collage_designer_stop_btn = {'AXIdentifier': '_NS:54', 'AXRole': 'AXButton'}

    # video collage -> advanced settings dlg
    dlg_advanced_settings = {'AXTitle': 'Advanced Settings', 'AXRole': 'AXWindow'}

    # video speed dialogue
    tab_video_speed_entire_clip = {'AXRole': 'AXButton', 'AXIdentifier': 'IDC_VIDEO_SPEED_BTN_ENTIRE'}
    tab_video_speed_selected_range = {'AXRole': 'AXButton', 'AXIdentifier': 'IDC_VIDEO_SPEED_BTN_PARTIAL'}
    btn_video_speed_reset = {'AXTitle': 'Reset', 'AXRole': 'AXButton'}
    #old icon_video_speed_settings = {'AXHelp': 'Settings', 'AXRole': 'AXButton'}
    icon_video_speed_settings = {'AXIdentifier': '_NS:9', 'AXRole': 'AXButton'}
    #old icon_video_speed_play = {'AXHelp': 'Play (Space)', 'AXRole': 'AXButton'}
    icon_video_speed_play = {'AXIdentifier': 'IDC_VIDEO_SPEED_BTN_PLAY', 'AXRole': 'AXButton'}
    #old icon_video_speed_stop = {'AXHelp': 'Stop (⌘/)', 'AXRole': 'AXButton'}
    icon_video_speed_stop = {'AXIdentifier': '_NS:121', 'AXRole': 'AXButton'}
    #old icon_video_speed_pause = {'AXHelp': 'Pause (Space)', 'AXRole': 'AXButton'}
    icon_video_speed_pause = {'AXIdentifier': 'IDC_VIDEO_SPEED_BTN_PLAY', 'AXRole': 'AXButton'}

    # video speed -> setting dlg
    dlg_video_speed_settings = {'AXTitle': 'Setting', 'AXRole': 'AXWindow'}


    # PRODUCE PAGE( need to create another page if having time)
    group_produce_page = [['standard window', 'type'], ['group', 'type']]
    tab_produce_page_standard2d = {'AXTitle': 'Standard 2D', 'AXRole': 'AXCheckBox'}
    tab_produce_page_online = {'AXTitle': 'Online', 'AXRole': 'AXCheckBox'}
    str_produce_standard2d = {'AXTitle': 'Standard 2D', 'AXRole': 'AXCheckBox'}
    youtube_category_el = {'AXIdentifier': 'IDC_PRODUCE_ONLINE_BTN_VIDEOCATEGORIES', 'AXRole': 'AXButton'}

    # YouTube Authorization dlg
    dlg_youtube_frame = {'AXTitle': 'YouTube authorization', 'AXRole': 'AXWindow'}

    # Vimeo Authorization dlg
    dlg_vimeo_frame = {'AXTitle': 'Vimeo authorization', 'AXRole': 'AXWindow'}

    # [Fix/Enhance]
    btn_tipsarea_fix_enhance = {'AXIdentifier': 'IDC_TIPSAREA_BTN_FIX_ENHANCE', 'AXRole': 'AXButton'}
    btn_reset = {'AXTitle': 'Reset', 'AXRole': 'AXButton'}
    btn_keyframe = {'AXTitle': 'Keyframe', 'AXRole': 'AXButton'}
    btn_applytoall = {'AXTitle': 'Apply to All', 'AXRole': 'AXButton'}
    str_main_enhance_white_balance = {'AXTitle': 'White Balance', 'AXRole': 'AXButton'}
    str_main_enhance_lens_correction = {'AXTitle': 'Lens Correction', 'AXRole': 'AXButton'}
    str_main_enahnce_audio_denoise = {'AXTitle': 'Audio Denoise', 'AXRole': 'AXButton'}
    str_main_enhance_color_adjustment = {'AXTitle': 'Color Adjustment', 'AXRole': 'AXButton'}
    checkbox_main_enhance_compareinsplitpreview = {'AXTitle': 'Compare in split preview' , 'AXRole': 'AXCheckBox'}

    # [Keyframe] main page
    str_keyframe_settings = {'AXValue': 'Keyframe Settings', 'AXRole': 'AXStaticText'}

    # Main-page-preview icon
    icon_main_preview_dock = {'AXIdentifier': '_NS:117', 'AXRole': 'AXButton'}
    icon_main_preview_undock = {'AXDescription': 'Custom View', 'AXRole': 'AXButton'}

    # [Jamie add] >> 09/21 Build
    # Media Room
    Video_SkateBoard_01 = {'AXIdentifier': 'CollectionViewItemTextField', 'AXValue': 'Skateboard 01.mp4', 'AXRole': 'AXStaticText'}
    Video_SkateBoard_02 = {'AXIdentifier': 'CollectionViewItemTextField', 'AXValue': 'Skateboard 02.mp4', 'AXRole': 'AXStaticText'}
    Image_Food = {'AXIdentifier': 'CollectionViewItemTextField', 'AXValue': 'Food.jpg', 'AXRole': 'AXStaticText'}

    # Preview Window
    preview_window_slider = {'AXRoleDescription': 'value indicator', 'AXValue': '151', 'AXRole': 'AXValueIndicator'}

    # blending mode
    dlg_blending_mode = {'AXTitle': 'Blending Mode', 'AXRole': 'AXWindow'}

    # Magic Motion Designer
    dlg_Magic_Motion_Designer = {'AXTitle': 'Magic Motion Designer', 'AXRole': 'AXWindow'}

    # Fix / Enhance
    btn_fix_enhance = {'AXIdentifier': 'IDC_TIPSAREA_BTN_FIX_ENHANCE'}
    # [Jamie add] <<

    def open_app(self, timeout=15, for_activate=0):
        if for_activate == 0:
            if self.launch_app(timeout) is not None:
                time.sleep(5)
                self.tap_activate_this_computer_btn()
                time.sleep(5)
                self.tap_cancel_btn()
                logger('Done')
                return True
            else:
                logger('launch_app fail')
        elif for_activate == 1:
            # for activate(email/account) dialogue
            if self.launch_app(3, get_main_wnd=0) is True:
                # verify if activate window pops up
                if self.search_text_position('Sign') is not False:
                    time.sleep(1)
                    self.tap_cancel_btn()
                    logger('Done')
                    return True
                else:
                    logger('verify fail')
            else:
                logger('launch_app fail')
        else:
            logger('incorrect arg.')
        return False

    def tap_permission_ok_btn(self, ground_truth_folder):
        pos = self.search_pos_from_image('alert_ok.png', ground_truth_folder)
        if pos is False:
            logger('get pos fail')
            return False
        if self.tap_pos(pos):
            logger('Done')
            return True
        else:
            logger('tap pos fail')
        return False

    def tap_activate_this_computer_btn(self):
        if self.tap_locator(self.btn_activate_this_computer):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    # activate dialogue
    def input_email_password_in_activate_dlg(self, email, password):
        # search email text position
        email_pos = self.search_text_position('E-mail')
        time.sleep(5)
        if email_pos is False:
            logger("get text pos fail")
            return False
        # adjust email_pos
        email_pos = (int(email_pos[0] + 40), email_pos[1])
        # click the column
        if self.click_mouse(email_pos):
            # start to input
            if self.input_text(email):
                # tap {tab} switch to password column
                if self.input_keyboard('tab'):
                    if self.input_text(password):
                        logger('Done')
                        return True
                    else:
                        logger('input password fail')
                else:
                    logger('tap tab fail')
            else:
                logger('input email fail')
        else:
            logger('click mouse fail')
        return False

    def tap_forgot_hyperlink_in_activate_dlg(self):
        # search 1st hyperlink
        str_forgot_your_password_pos = self.search_text_position('Forgot')
        if str_forgot_your_password_pos is False:
            logger("get text pos fail")
            return False
        if self.click_mouse(str_forgot_your_password_pos):
            logger('Done')
            return True
        else:
            logger('click mouse fial')
        return False

    def tap_signup_hyperlink_in_activate_dlg(self):
        # search 1st hyperlink
        str_sign_up_pos = self.search_text_position('up')
        if str_sign_up_pos is False:
            logger("get text pos fail")
            return False
        if self.click_mouse(str_sign_up_pos):
            logger('Done')
            return True
        else:
            logger('click mouse fial')
        return False

    def tap_activate_btn(self):
        pos = self.search_text_position('activate', order='2/2')
        if pos is False:
            logger('get pos fail')
            return False
        if self.tap_pos(pos):
            logger('Done')
            return True
        else:
            logger('tap pos fail')
        return False

    def tap_cancel_btn(self, ocr_mode=0):
        if ocr_mode == 0:
            if self.tap_locator(self.btn_cancel):
                logger('Done')
                return True
            else:
                logger('tap locator fail')
        elif ocr_mode == 1:
            cancel_pos = self.search_text_position('Cancel')
            if cancel_pos is False:
                logger('get text pos fail')
                return False
            if self.click_mouse(cancel_pos):
                logger('Done')
                return True
            else:
                logger('click mouse fail')
        else:
            logger('incorrect parameter')
        return False

    def tap_signin_btn(self):
        # old : signin_pos = self.search_text_position('Sign', order='2/2')
        # Jamie debug for v2219
        #signin_pos = self.search_text_position('Sign', order='3/3')

        # Jamie debug for 2401
        signin_pos = self.search_text_position('Sign', order='2/2')
        if signin_pos is False:
            logger('get text pos fail')
            return False
        if self.click_mouse(signin_pos):
            time.sleep(3)
            self.tap_activate_this_computer_btn()
            logger('Done')
            return True
        else:
            logger('click mouse fail')
        return False

    def check_if_ap_exist(self):
        time.sleep(5)
        if self.is_app_exist():
            logger('Done')
            return True
        else:
            logger('app does not exist')
        return False

    def activate_pdr(self):
        """
        only press pdr icon to let AP on top
        :return:
        """
        self.launch_app(get_main_wnd=0, skip_exist=1)
        logger('Done')

    def is_in_Edit_tab(self):
        # el = self.search_el(self.tab_main_produce) ## v2219
        ## Jamie maintain for v2401
        el = self.search_el(self.Video_SkateBoard_01)
        if el is None:
            logger('get el fail')
            return False
        logger('Done')
        return True
        '''
        (previous version)
        status = self.get_axvalue(el)
        if status == 0:
            logger('not in Edit tab')
            return False
        elif status == 1:
            logger('in Edit tab')
            return True
        else:
            logger(f'get incorrect status. ({status})')
        return False
        '''

    def is_content_exists(self, filename):
        """
        for media room content
        8/20: add position checking(filter out the position of timeline), only check media room page
        :param filename:
        :return:
        """
        locator_unselect = {'AXRole': 'AXStaticText', 'AXValue': f'{filename}'}
        locator_select = {'AXRole': 'AXTextField', 'AXValue': f'{filename}'}
        el_check = self.search_el(locator_unselect)
        if el_check is not None:
            # verify if in room area
            room_area_pos = self.get_locator_pos(self.area_room_frame)
            if room_area_pos is False:
                logger('get room area pos fail(1)')
                return False
            el_pos = self.get_pos(el_check)
            if el_pos is False:
                logger('get el_pos fail(1)')
                return False
            # check if in room area
            if el_pos[1] < room_area_pos[1] + room_area_pos[3]:
                logger('Done')
                return True
            else:
                logger('find but out of room area(1)')
                return False
        else:
            el_check = self.search_el(locator_select)
            if el_check is not None:
                # verify if in room area
                room_area_pos = self.get_locator_pos(self.area_room_frame)
                if room_area_pos is False:
                    logger('get room area pos fail(2)')
                    return False
                el_pos = self.get_pos(el_check)
                if el_pos is False:
                    logger('get el_pos fail(2)')
                    return False
                # check if in room area
                if el_pos[1] < room_area_pos[1] + room_area_pos[3]:
                    logger('Done')
                    return True
                else:
                    logger('find but out of room area(2)')
                    return False
            else:
                logger('search el fail')
        return False

    def is_pip_exists(self, filename):
        return self.is_content_exists(filename)

    def is_title_exists(self, filename):
        return self.is_content_exists(filename)

    def is_transition_exists(self, filename):
        return self.is_content_exists(filename)

    def is_content_selected(self, filename):
        locator_select = {'AXRole': 'AXTextField', 'AXValue': f'{filename}'}
        el_check = self.search_el(locator_select)
        if el_check is not None:
            logger('Done')
            return True
        else:
            logger('search el fail')
        return False

    def check_frame_exists(self, target_name, ground_truth_folder):
        if self.search_pos_from_image(target_name, ground_truth_folder) is not False:
            logger('Done')
            return True
        else:
            logger('img not exists')
        return False

    def tap_displayallmedia_btn(self):
        if self.tap_locator(self.btn_display_all_media):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def tap_displayvideosonly_btn(self):
        if self.tap_locator(self.btn_display_videos_only):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def tap_displayimagesonly_btn(self):
        if self.tap_locator(self.btn_display_images_only):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def tap_displayaudioonly_btn(self):
        if self.tap_locator(self.btn_display_audio_only):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def tap_detailview_btn(self):
        if self.tap_locator(self.btn_details_view):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def tap_iconview_btn(self):
        if self.tap_locator(self.btn_icon_view):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def is_in_detail_view(self, which_room=None):
        """
        :param which_room: None: in media room, others: use its text
        :return:
        """
        if which_room is None:
            if self.search_el(self.str_timecode_none) is not None:
                logger('in detail view')
                return True
            else:
                logger('not in detail view')
                return False
        elif which_room == 'Effect Room':
            if self.search_el(self.img_effecticon) is not None:
                logger('in detail view')
                return True
            else:
                logger('not in detail view')
                return False
        elif which_room == 'PiP Room':
            if self.search_el(self.img_pipicon) is not None:
                logger('in detail view')
                return True
            else:
                logger('not in detail view')
                return False
        elif which_room == 'Particle Room':
            if self.search_el(self.img_particleicon) is not None:
                logger('in detail view')
                return True
            else:
                logger('not in detail view')
                return False
        elif which_room == 'Title Room':
            if self.search_el(self.img_titleicon) is not None:
                logger('in detail view')
                return True
            else:
                logger('not in detail view')
                return False
        elif which_room == 'Transition Room':
            if self.search_el(self.img_transitionicon) is not None:
                logger('in detail view')
                return True
            else:
                logger('not in detail view')
                return False
        else:
            logger('Incorrect parameter')
        return False

    def tap_librarymenu_btn(self, menu_item1=None, menu_item2=None, menu1_index=0, menu2_index=0):
        """
        if assign menu_item, select them
        :param menu_item1:
        :param menu_item2:
        :menu_index: in order to assign which index if has 2 same menu items
        :return:
        """
        if self.tap_locator(self.btn_library_menu):
            if menu_item1 is None:
                logger('Done')
                return True
            else:
                # wait 1sec. to express menu
                time.sleep(1)
                menu_item1_locator = {'AXRole': 'AXMenuItem', 'AXTitle': f'{menu_item1}'}
                if self.tap_locator(menu_item1_locator):
                    if menu_item2 is None:
                        logger('Done')
                        return True
                    else:
                        # wait 1sec. to express menu
                        time.sleep(1)
                        menu_item2_locator = {'AXRole': 'AXMenuItem', 'AXTitle': f'{menu_item2}'}
                        el_list = self.search_all_el(menu_item2_locator)
                        # avoid 2 result ==> get the last one(ex: has 2 'Prefix Transition' elements)
                        if self.tap_element(el_list[menu2_index]):
                            logger('Done')
                            return True
                        else:
                            logger('tap menu item2 fail')
                else:
                    logger('tap menu item1 fail')
        else:
            logger('tap locator fail')
        return False

    def get_content_section(self):
        """
        reason: for new UI, find the content name
        Structure: split group -> split group -> group[0] -> group -> scroll area -> collection
                    -> section(this function)
        :return:
        """
        logger('aaa')
        top_split_el = self.get_pdr_mian_window_top_split_group()
        if top_split_el is False:
            logger('get top_split_el fail')
            return False
        group_1_list = self.search_child_el_by_role(top_split_el, 'group')
        if group_1_list is False:
            logger('get group_1_list fail')
            return False
        group_2_list = self.search_child_el_by_role(group_1_list[0], 'AXGroup')
        if group_2_list is False:
            logger('get group_1_list fail')
            return False
        scroll_area = self.search_child_el_by_role(group_2_list, 'AXScrollArea')
        if scroll_area is False:
            logger('get scroll_area fail')
            return False
        collection_el = self.search_child_el_by_role(scroll_area, 'AXList')
        if collection_el is False:
            logger('get collection_el fail')
            return False
        section_el = self.search_child_el_by_role(collection_el, 'AXList')
        if section_el is False:
            logger('get section_el fail')
            return False
        logger('Done')
        return section_el

    def get_content_name(self, index=2):
        """
        index: 0, 1, 2, 3, ...
        old: index (from 2nd), ex: index=2 => means 2nd clip (haven't handle 1st clip case)
        :param index:
        :return:
        """
        # new(structure: section -> groups -> img/textfield
        section_el = self.get_content_section()
        if section_el is False:
            logger('get section_el fail')
            return False
        group_list = self.search_child_el_by_role(section_el, 'AXGroup')
        if group_list is False:
            logger('get group_list fail')
            return False
        # get content name
        try:
            child_text_el = self.search_child_el_by_role(group_list[index], 'AXTextField')
            if child_text_el is False:
                logger('get child_text_el fail(1)')
                child_text_el = self.search_child_el_by_role(group_list[index], 'AXStaticText')
                if child_text_el is False:
                    logger('get child_text_el fail(2)')
                    return False
            name = self.get_axvalue(child_text_el)
            if name is not False:
                logger(f'Done. ({name})')
                return name
            else:
                logger('get name fail')
                return False
        except:
            logger('Exception')
            return False
        '''
        # old
        locator = [['standard window', 'type'], ['group', 'type'], ['split group', 'type'], ['split group', 'type', 0],
                   ['group', 'type', 25], ['scroll area', 'type'], ['collection', 'type'], ['section', 'type'],
                   ['group', 'type', index - 1], ['text', 'type']]
        el = self.search_el(locator)
        if el is None:
            logger('get el fail')
            return False
        return self.get_axvalue(el)
        '''

    def get_effect_name(self, index=2):
        """
        index: 0, 1, 2, 3, ...
        old: index (from 2nd), ex: index=2 => means 2nd clip (haven't handle 1st clip case)
        :param index:
        :return:
        """
        logger('interface of get_effect_name')
        return self.get_content_name(index)
        '''
        locator = [['standard window', 'type'], ['group', 'type'], ['split group', 'type'], ['split group', 'type', 0],
                   ['group', 'type', 20], ['scroll area', 'type'], ['collection', 'type'], ['section', 'type'],
                   ['group', 'type', index - 1], ['text', 'type']]
        el = self.search_el(locator)
        if el is None:
            logger('get el fail')
            return False
        return self.get_axvalue(el)
        '''

    def get_pip_name(self, index=0):
        logger('interface get_pip_name')
        return self.get_content_name(index)
        """
        #old
        locator = [['standard window', 'type'], ['group', 'type'], ['split group', 'type'], ['split group', 'type', 0],
                   ['group', 'type', 22], ['scroll area', 'type'], ['collection', 'type'], ['section', 'type'],
                   ['group', 'type', index], ['text', 'type']]
        # index0 is 'Free Templates' , -1 is the last one
        el = self.search_el(locator)
        if el is None:
            logger('get el fail')
            return False
        res = self.get_axvalue(el)
        if res is not False:
            logger(f'Done, ({res})')
            return res
        else:
            logger('get axvalue fail')
        return False
        """

    def get_particle_name(self, index=0):
        logger('interface get_pip_name')
        return self.get_content_name(index)
        """
        #old
        locator = [['standard window', 'type'], ['group', 'type'], ['split group', 'type'], ['split group', 'type', 0],
                   ['group', 'type', 20], ['scroll area', 'type'], ['collection', 'type'], ['section', 'type'],
                   ['group', 'type', index], ['text', 'type']]
        # index0 is 'Free Templates' , -1 is the last one
        el = self.search_el(locator)
        if el is None:
            logger('get el fail')
            return False
        res = self.get_axvalue(el)
        if res is not False:
            logger(f'Done, ({res})')
            return res
        else:
            logger('get axvalue fail')
        return False
        """

    def get_title_name(self, index=0):
        logger('interface get_title_name')
        return self.get_content_name(index)
        """
        #old
        locator = [['standard window', 'type'], ['group', 'type'], ['split group', 'type'], ['split group', 'type', 0],
                   ['group', 'type', 22], ['scroll area', 'type'], ['collection', 'type'], ['section', 'type'],
                   ['group', 'type', index], ['text', 'type']]
        # index0 is 'Free Templates' , -1 is the last one
        el = self.search_el(locator)
        if el is None:
            logger('get el fail')
            return False
        res = self.get_axvalue(el)
        if res is not False:
            logger(f'Done, ({res})')
            return res
        else:
            logger('get axvalue fail')
        return False
        """

    def get_transition_name(self, index=0):
        logger('interface get_transition_name')
        return self.get_content_name(index)
        """
        #old
        locator = [['standard window', 'type'], ['group', 'type'], ['split group', 'type'], ['split group', 'type', 0],
                   ['group', 'type', 20], ['scroll area', 'type'], ['collection', 'type'], ['section', 'type'],
                   ['group', 'type', index], ['text', 'type']]
        # index0 is 'Free Templates' , -1 is the last one
        el = self.search_el(locator)
        if el is None:
            logger('get el fail')
            return False
        res = self.get_axvalue(el)
        if res is not False:
            logger(f'Done, ({res})')
            return res
        else:
            logger('get axvalue fail')
        return False
        """

    def click_content_empty_area(self):
        """
        for unselect all contents
        :return:
        """
        '''
        el = self.search_el(self.area_contents)
        if el is None:
            logger('search el fail')
            return False
        '''
        section_el = self.get_content_section()
        if section_el is False:
            logger('get section_el fail')
            return False
        parent_el = self.get_parent_wnd(section_el)
        if parent_el is False:
            logger('get parent_el fail')
            return False
        pos = self.get_axposition(parent_el)
        if pos is False:
            logger('get pos fail')
            return False
        if self.click_mouse((pos[0] + 3, pos[1] + 3)):
            logger('Done')
            return True
        else:
            logger('click mouse fail')
        return False

    def change_icon_size(self, size):
        """
        size: Extra Large Icons, Large Icons, Medium Icons, Small Icons
        :param size:
        :return:
        """
        # new(structure: section -> groups -> img/textfield
        section_el = self.get_content_section()
        if section_el is False:
            logger('get section_el fail')
            return False
        group_list = self.search_child_el_by_role(section_el, 'AXGroup')
        if group_list is False:
            logger('get group_list fail')
            return False
        # get 1st content img el
        child_img_el = self.search_child_el_by_role(group_list[0], 'AXImage')
        if child_img_el is False:
            logger('get child_img_el fail')
            return False
        '''
        # old
        # get org icon size 1st
        locator = [['standard window', 'type'], ['group', 'type'], ['split group', 'type'], ['split group', 'type', 0],
                     ['group', 'type', 25], ['scroll area', 'type'], ['collection', 'type'], ['section', 'type'],
                     ['group', 'type', 0], ['image', 'type']]
        el = self.search_el(locator)
        if el is None:
            logger('get el fail')
            return False
        '''
        org_size = self.get_axsize(child_img_el)
        if org_size is False:
            logger('get size fail(1)')
            return False
        # start to change size
        if not self.tap_librarymenu_btn(size):
            logger('tap library menu btn fail')
            return False
        # get changed_size
        changed_size = self.get_axsize(child_img_el)
        if changed_size is False:
            logger('get size fail(2)')
            return False
        # start to compare
        logger(f'org size: {org_size}, changed size: {changed_size}')
        if org_size != changed_size:
            logger('Done')
            return True
        else:
            logger('size is the same')
        return False

    def change_effect_icon_size(self, size):
        # new(structure: section -> groups -> img/textfield
        section_el = self.get_content_section()
        if section_el is False:
            logger('get section_el fail')
            return False
        group_list = self.search_child_el_by_role(section_el, 'AXGroup')
        if group_list is False:
            logger('get group_list fail')
            return False
        # get 1st content img el
        child_img_el = self.search_child_el_by_role(group_list[0], 'AXImage')
        if child_img_el is False:
            logger('get child_img_el fail')
            return False
        '''
        locator = [['standard window', 'type'], ['group', 'type'], ['split group', 'type'], ['split group', 'type', 0],
                   ['group', 'type', 20], ['scroll area', 'type'], ['collection', 'type'], ['section', 'type'],
                   ['group', 'type', 0], ['image', 'type']]
        el = self.search_el(locator)
        if el is None:
            logger('get el fail(1)')
            return False
        '''
        org_size = self.get_axsize(child_img_el)
        if org_size is False:
            logger('get size fail(1)')
            return False
        # start to change size
        if not self.tap_librarymenu_btn(size):
            logger('tap library menu btn fail')
            return False
        # get 1st content img el(need to get again for effect page)
        child_img_el = self.search_child_el_by_role(group_list[0], 'AXImage')
        if child_img_el is False:
            logger('get child_img_el fail')
            return False
        # get changed_size
        changed_size = self.get_axsize(child_img_el)
        if changed_size is False:
            logger('get size fail(2)')
            return False
        # start to compare
        logger(f'org size: {org_size}, changed size: {changed_size}')
        if org_size != changed_size:
            logger('Done')
            return True
        else:
            logger('size is the same')
        return False

    def change_pip_icon_size(self, size):
        # new(structure: section -> groups -> img/textfield
        section_el = self.get_content_section()
        if section_el is False:
            logger('get section_el fail')
            return False
        group_list = self.search_child_el_by_role(section_el, 'AXGroup')
        if group_list is False:
            logger('get group_list fail')
            return False
        # get 1st content img el
        child_img_el = self.search_child_el_by_role(group_list[0], 'AXImage')
        if child_img_el is False:
            logger('get child_img_el fail')
            return False
        """
        # old
        locator = [['standard window', 'type'], ['group', 'type'], ['split group', 'type'], ['split group', 'type', 0],
                   ['group', 'type', 22], ['scroll area', 'type'], ['collection', 'type'], ['section', 'type'],
                   ['group', 'type', 0], ['image', 'type']]
        el = self.search_el(locator)
        if el is None:
            logger('get el fail(1)')
            return False
        """
        org_size = self.get_axsize(child_img_el)
        if org_size is False:
            logger('get size fail(1)')
            return False
        # start to change size
        if not self.tap_librarymenu_btn(size):
            logger('tap library menu btn fail')
            return False
        # get 1st content img el(need to get again for effect page)
        child_img_el = self.search_child_el_by_role(group_list[0], 'AXImage')
        if child_img_el is False:
            logger('get child_img_el fail')
            return False
        # get changed_size
        changed_size = self.get_axsize(child_img_el)
        if changed_size is False:
            logger('get size fail(2)')
            return False
        # start to compare
        logger(f'org size: {org_size}, changed size: {changed_size}')
        if org_size != changed_size:
            logger('Done')
            return True
        else:
            logger('size is the same')
        return False


    def change_particle_icon_size(self, size):
        # new(structure: section -> groups -> img/textfield
        section_el = self.get_content_section()
        if section_el is False:
            logger('get section_el fail')
            return False
        group_list = self.search_child_el_by_role(section_el, 'AXGroup')
        if group_list is False:
            logger('get group_list fail')
            return False
        # get 1st content img el
        child_img_el = self.search_child_el_by_role(group_list[0], 'AXImage')
        if child_img_el is False:
            logger('get child_img_el fail')
            return False
        """
        #old
        locator = [['standard window', 'type'], ['group', 'type'], ['split group', 'type'], ['split group', 'type', 0],
                   ['group', 'type', 20], ['scroll area', 'type'], ['collection', 'type'], ['section', 'type'],
                   ['group', 'type', 0], ['text', 'type']]
        el = self.search_el(locator)
        if el is None:
            logger('get el fail(1)')
            return False
        """
        org_size = self.get_axsize(child_img_el)
        if org_size is False:
            logger('get size fail(1)')
            return False
        # start to change size
        if not self.tap_librarymenu_btn(size):
            logger('tap library menu btn fail')
            return False
        # get 1st content img el(need to get again for effect page)
        child_img_el = self.search_child_el_by_role(group_list[0], 'AXImage')
        if child_img_el is False:
            logger('get child_img_el fail')
            return False
        # get changed_size
        changed_size = self.get_axsize(child_img_el)
        if changed_size is False:
            logger('get size fail(2)')
            return False
        # start to compare
        logger(f'org size: {org_size}, changed size: {changed_size}')
        if org_size != changed_size:
            logger('Done')
            return True
        else:
            logger('size is the same')
        return False

    def change_title_icon_size(self, size):
        # new(structure: section -> groups -> img/textfield
        section_el = self.get_content_section()
        if section_el is False:
            logger('get section_el fail')
            return False
        group_list = self.search_child_el_by_role(section_el, 'AXGroup')
        if group_list is False:
            logger('get group_list fail')
            return False
        # get 1st content img el
        child_img_el = self.search_child_el_by_role(group_list[0], 'AXImage')
        if child_img_el is False:
            logger('get child_img_el fail')
            return False
        """
        #old
        locator = [['standard window', 'type'], ['group', 'type'], ['split group', 'type'], ['split group', 'type', 0],
                   ['group', 'type', 22], ['scroll area', 'type'], ['collection', 'type'], ['section', 'type'],
                   ['group', 'type', 0], ['image', 'type']]
        el = self.search_el(locator)
        if el is None:
            logger('get el fail(1)')
            return False
        """
        org_size = self.get_axsize(child_img_el)
        if org_size is False:
            logger('get size fail(1)')
            return False
        # start to change size
        if not self.tap_librarymenu_btn(size):
            logger('tap library menu btn fail')
            return False
        # get 1st content img el(need to get again for effect page)
        child_img_el = self.search_child_el_by_role(group_list[0], 'AXImage')
        if child_img_el is False:
            logger('get child_img_el fail')
            return False
        # get changed_size
        changed_size = self.get_axsize(child_img_el)
        if changed_size is False:
            logger('get size fail(2)')
            return False
        # start to compare
        logger(f'org size: {org_size}, changed size: {changed_size}')
        if org_size != changed_size:
            logger('Done')
            return True
        else:
            logger('size is the same')
        return False

    def change_transition_icon_size(self, size):
        # new(structure: section -> groups -> img/textfield
        section_el = self.get_content_section()
        if section_el is False:
            logger('get section_el fail')
            return False
        group_list = self.search_child_el_by_role(section_el, 'AXGroup')
        if group_list is False:
            logger('get group_list fail')
            return False
        # get 1st content img el
        child_img_el = self.search_child_el_by_role(group_list[0], 'AXImage')
        if child_img_el is False:
            logger('get child_img_el fail')
            return False
        """
        #old
        locator = [['standard window', 'type'], ['group', 'type'], ['split group', 'type'], ['split group', 'type', 0],
                   ['group', 'type', 20], ['scroll area', 'type'], ['collection', 'type'], ['section', 'type'],
                   ['group', 'type', 0], ['image', 'type']]
        el = self.search_el(locator)
        if el is None:
            logger('get el fail(1)')
            return False
        """
        org_size = self.get_axsize(child_img_el)
        if org_size is False:
            logger('get size fail(1)')
            return False
        # start to change size
        if not self.tap_librarymenu_btn(size):
            logger('tap library menu btn fail')
            return False
        # get 1st content img el(need to get again for effect page)
        child_img_el = self.search_child_el_by_role(group_list[0], 'AXImage')
        if child_img_el is False:
            logger('get child_img_el fail')
            return False
        # get changed_size
        changed_size = self.get_axsize(child_img_el)
        if changed_size is False:
            logger('get size fail(2)')
            return False
        # start to compare
        logger(f'org size: {org_size}, changed size: {changed_size}')
        if org_size != changed_size:
            logger('Done')
            return True
        else:
            logger('size is the same')
        return False

    def tap_insertonselectedtrack_btn(self):
        if self.tap_locator(self.btn_insert_on_selected_track):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def tap_addtoeffecttrack_btn(self):
        if self.tap_locator(self.btn_add_to_effect_track):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def get_transition_number_timeline(self):
        """
        only return how many transition in timeline
        :return:
        """
        try:
            el_list = self.search_all_el(self.btn_transition_timeline)
            el_list2 = self.search_all_el(self.btn_transition_timeline_01)
            if el_list is not None and \
                    el_list2 is not None:
                logger(f'has {len(el_list) + len(el_list2)} transition(s) in timeline')
                return len(el_list) + len(el_list2)
            else:
                logger('get el_list fail')
            return False
        except Exception as e:
            logger(f'Exception. ({e})')
            return False

    def select_transition_in_timeline(self, index=0):
        """
        select transition in timeline
        :param index:
        :return:
        """
        try:
            el_list = self.search_all_el(self.btn_transition_timeline)
            el_list2 = self.search_all_el(self.btn_transition_timeline_01)
            if el_list is not None and \
                    el_list2 is not None:
                el_list_all = el_list + el_list2
                logger(el_list_all)
                if self.tap_element(el_list_all[index]):
                    # verify if modify btn shows
                    if self.search_el(self.btn_tipsarea_modify) is not None:
                        logger('Done')
                        return True
                    else:
                        logger('verify fail')
                else:
                    logger('tap element fail')
            else:
                logger('get el_list fail')
            return False
        except Exception as e:
            logger(f'Exception. ({e})')
            return False

    def undo(self):
        if self.input_combo_keyboard('cmd_l', 'z'):
            logger('Done')
            return True
        else:
            logger('input combo keyboard fail')
        return False

    def redo(self):
        if self.input_combo_keyboard('cmd_l', 'z', 'shift_l'):
            logger('Done')
            return True
        else:
            logger('input combo keyboard fail')
        return False

    def tap_titledesigner_undo_btn(self):
        if self.tap_locator(self.btn_titledesigner_undo):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def tap_titledesigner_redo_btn(self):
        if self.tap_locator(self.btn_titledesigner_redo):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def is_in_timeline(self, filename):
        if self.is_in_timeline_method1(filename):
            logger('Done')
            return True
        else:
            if self.is_in_timeline_method2(filename):
                logger('Done')
                return True
            else:
                logger("Can't find in timeline")
        return False

    def is_in_timeline_method1(self, filename):
        """
        get timeline cell => find its child => verify filename
        :param filename:  (ex: Food) , doesn't have => .jpg
        :return:
        """
        timelinecell_locator = {'AXIdentifier': 'VideoCellItem', 'AXRole': 'AXGroup'}
        timelinecell_el = self.search_el(timelinecell_locator)
        if timelinecell_el is None:
            logger('search el fail')
            return False
        # find its child
        child_el_list = self.get_child_wnd(timelinecell_el)
        for x in range(len(child_el_list)):
            if self.get_axvalue(child_el_list[x]) == filename:
                logger('Done')
                return True
        logger("Can't find in timeline")
        return False

    def is_in_timeline_method2(self, filename):
        """
        another method : find the bottom area position, find all elements that match the bottom area
        :param filename:
        :return:
        """
        target = {'AXValue': f'{filename.split(".")[0]}', 'AXRole': 'AXStaticText'}
        # get frame position
        frame_pos = self.get_locator_pos(self.area_timeline_frame)
        if frame_pos is False:
            logger('get frame pos fail')
            return False
        # get all target as list
        target_list = self.search_all_el(target)
        if target_list is None:
            logger('get target list fail')
            return False
        for x in range(len(target_list)):
            target_pos = self.get_pos(target_list[x])
            if target_pos is False:
                logger(f'get target pos fail {x} times')
                return False
            if target_pos[1] > frame_pos[1]:
                logger('Done')
                return True
        logger('not in timeline2')
        return False

    def get_timeline_timecode_list(self):
        """
        Structure: collection -> section -> groups(this function)
        :return:
        """
        section_el = self.search_el(self.split_group_timeline_timecode)
        if section_el is False:
            logger('get collection_el fail')
            return False
        logger(section_el)
        # get child list
        timecode_list = self.get_child_wnd(section_el)
        if timecode_list is False:
            logger('get timecode_list fail')
            return False
        logger('Done')
        return timecode_list

    def get_timeline_timecode_area(self):
        el = self.get_pdr_mian_window_bottom_split_group()
        if el is False:
            logger('get el fail')
            return False
        logger(self.get_child_wnd(el))
        scrollarea_list = self.search_child_el_by_role(el, 'AXScrollArea')
        if scrollarea_list is False:
            logger('get scrollarea_list fail')
            return False
        try:
            target_scrollarea = scrollarea_list[2]
        except:
            logger('assign index fail')
            return False
        pos = self.get_pos(target_scrollarea)
        if pos is not False:
            logger(f'Done. {pos}')
            return pos
        else:
            logger('get pos fail')
        return False

    def get_timeline_timecode_pos(self, timecode):
        timecode_list = self.get_timeline_timecode_list()
        if timecode_list is False:
            logger('get timecode_list fail')
            return False
        target = ''
        for x in range(len(timecode_list)):
            try:
                text = self.search_child_el_by_role(timecode_list[x], 'AXStaticText')
                if text == timecode:
                    target = x
                    break
            except:
                continue
        if target == '':
            logger('get target fail')
            return False
        pos = self.get_pos(self.search_child_el_by_role(timecode_list[target], 'AXStaticText'))
        if pos is not False:
            logger(f'Done. {pos}')
            return pos
        else:
            logger('get pos fail')
        return False

    def tap_timeline_timecode(self, timecode):
        """
        tap left-top pos
        :param timecode:
        :return:
        """
        pos = self.get_timeline_timecode_pos(timecode)
        if pos is False:
            logger('get pos fail')
            return False
        target_pos = (pos[0] + 1, pos[1] + pos[3] / 2)
        if self.tap_pos(target_pos):
            logger('Done')
            return True
        else:
            logger('tap pos fail')
        return False

    def get_timeline_el(self, filename, index):
        """
        get el in timeline
        :param filename:
        :param index:
        :return:
        """
        try:
            target = {'AXValue': f'{filename}', 'AXRole': 'AXStaticText'}
            # get frame position
            frame_pos = self.get_locator_pos(self.area_timeline_frame)
            if frame_pos is False:
                logger('get frame pos fail')
                return False
            # get all target as list
            target_list = self.search_all_el(target)
            if target_list is None:
                logger('get target list fail')
                return False
            logger(f'target list: {target_list}')
            new_target_list = []
            for x in range(len(target_list)):
                target_pos = self.get_pos(target_list[x])
                if target_pos is False:
                    logger(f'get target pos fail {x} times')
                    return False
                if target_pos[1] > frame_pos[1]:
                    new_target_list.append(target_list[x])
            logger(f'new target_list: {new_target_list}')
            logger('Done')
            return new_target_list[index]
        except Exception as e:
            logger(f'Exception. ({e})')
            return False

    def get_timeline_block_pos(self, filename, index):
        """
        index(0, 1, 2)
        return pos(x, y, w, h)
        :return:
        """
        el = self.get_timeline_el(filename, index)
        if el is False:
            logger('get el fail')
            return False
        parent_el = self.get_parent_wnd(el)
        if parent_el is False:
            logger('get parent fail')
            return False
        pos = self.get_pos(parent_el)
        if pos is not False:
            logger(f'Done. {pos}')
            return pos
        else:
            logger('get pos fail')
        return False

    def tap_timeline_block(self, filename, index, click=1):
        """
        click content(text)
        :param filename:
        :param index:
        :param click: 1 or double click(2)
        :return:
        """
        pos = self.get_timeline_block_pos(filename, index)
        if pos is False:
            logger('get pos fail')
            return False
        target_pos = (pos[0] + pos[2] / 2, pos[1] + pos[3] / 2)
        if self.click_mouse(target_pos, 'left', click):
            logger('Done')
            return True
        else:
            logger('click mouse fail')
        return False

    def tap_main_keyframe_btn(self):
        """
        in effect settings
        :return:
        """
        if self.tap_locator(self.btn_keyframe):
            # verify
            time.sleep(1)
            if self.search_el(self.str_keyframe_settings) is not None:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap locator fail')
        return False

    # new
    def get_timeline_left_cell_table_el(self):
        """
        left cell table element
        :return:
        """
        table_el = self.search_el(self.el_timeline_left_cell_table)
        if table_el is False:
            logger('get table_el fail')
            return False
        logger('Done')
        return table_el

    def get_timeline_left_cell_table_row_list(self):
        """
        structure: scroll area -> table -> table row(list) (this function)
        """
        table_el = self.get_timeline_left_cell_table_el()
        if table_el is False:
            logger('get table_el fail')
            return False
        tablerow_list = self.get_child_wnd(table_el)
        if tablerow_list is False:
            logger('get tablerow_list fail')
            return False
        logger('Done')
        return tablerow_list

    def get_timeline_right_table(self):
        """
        Structure: Table(this function) -> table row (s) -> cell -> scroll area -> collection -> section -> group ->
                    => scroll area &  -> collection -> section -> group ->
                    => text(AXStaticText)
        :return:
        """
        right_table_el = self.search_el(self.el_timeline_right_cell_table)
        if right_table_el is False:
            logger('get right_table_el fail')
            return False
        logger('Done')
        return right_table_el

    def get_timeline_right_table_row_list(self):
        table_el = self.get_timeline_right_table()
        if table_el is False:
            logger('get table_el fail')
            return False
        tablerow_list = self.search_child_el_by_role(table_el, 'AXRow')
        if tablerow_list is False:
            logger('get tablerow_list fail')
            return False
        logger('Done')
        return tablerow_list

    def get_timeline_left_cell(self, option):
        """
        Table View
        option: 'fx', 'pip', 'video track 1', 'video track 2'
        :return:
        """
        cell_table_row_list = self.get_timeline_left_cell_table_row_list()
        if cell_table_row_list is False:
            logger('get cell_table_row_list fail')
            return False
        # to find its' child to match option
        # structure: Table -> table row -> cell -> text/button/button/text field(target), (ex: axvalue)
        target_dict = {'fx': 'Effect Track',
                       'pip': 'Video Track 1',
                       'video track 1': 'Video Track 1'}
        try:
            target = target_dict[option]
        except:
            logger('incorrect parameter')
            return False
        # check if has index
        index_checkflag = ''
        try:
            if int(target.split(' ')[-1]) in [1, 2, 3, 4]:
                index_checkflag = int(target.split(' ')[-1])
                target = target[:-2]
        except:
            logger("doesn't have index order, next")
        target_flag = ''
        for x in range(len(cell_table_row_list)):
            try:
                cell_el = self.get_child_wnd(cell_table_row_list[x])[0]
                if cell_el is False:
                    continue
                text_field_el = self.search_child_el_by_role(cell_el, 'AXTextField')
                if text_field_el is False:
                    continue
                value = self.get_axvalue(text_field_el)
                if value == target:
                    if index_checkflag in [1, 2, 3, 4]:
                        # need to search index
                        index_el = self.search_child_el_by_role(cell_el, 'AXStaticText')
                        if index_el is False:
                            continue
                        index_value = self.get_axvalue(index_el)
                        if int(index_value) == index_checkflag:
                            target_flag = x
                            break
                        else:
                            continue
                    else:
                        target_flag = x
                        break
                else:
                    continue
            except:
                continue
        if target_flag == '':
            logger('get target fail')
            return False
        logger('Done')
        return cell_table_row_list[target_flag]

    def get_timeline_cell(self, option):
        """
        NEW:
        in order to get cell, 'fx', 'pip', 'video track 1', 'video track 2'
        :param option:
        :return:  Cell element
        """
        # 1: get left cell and its posistion(in order to match y-axis)
        # 2: get right(timeline) cell
        # 3: match the y axis

        # 1:
        left_cell_table_row = self.get_timeline_left_cell(option)
        if left_cell_table_row is False:
            logger('get left_cell_table_row fail')
            return False
        left_pos = self.get_pos(left_cell_table_row, int_rule=0)
        if left_pos is False:
            logger('get left_pos fail')
            return False

        # 2:
        right_cell_table_row_list = self.get_timeline_right_table_row_list()
        if right_cell_table_row_list is False:
            logger('get right_cell_table_row_list fail')
            return False

        # 3: match the y axis
        target_flag = ''
        for x in range(len(right_cell_table_row_list)):
            right_pos = self.get_pos(right_cell_table_row_list[x], int_rule=0)
            if right_pos is False:
                logger('get right_pos fail')
                return False
            if right_pos[1] == left_pos[1]:
                target_flag = x
                break
        if target_flag == '':
            logger('get target fail')
            return False
        # get cell(child)
        cell_el = self.search_child_el_by_role(right_cell_table_row_list[target_flag], 'AXCell')
        if cell_el is False:
            logger('get cell_el fail')
            return False
        logger('Done')
        return cell_el

    '''
#old
    def get_timeline_cell(self, option):
        """
        in order to get cell, 'fx', 'pip', 'video track 1', 'video track 2'
        :param option:
        :return:  Cell element
        """
        if option == 'fx':
            # (1)find timeline table
            # NEW
            table_el = self.get_timeline_cell_table_el()
            if table_el is False:
                logger('get table_el fail')
                return False
            timeline_table_locator = {'AXIdentifier': '_NS:17', 'AXRole': 'AXTable'}
            timeline_table_el = self.search_el(timeline_table_locator)
            if timeline_table_el is None:
                logger('search el fail')
                return False
            # find its child
            child_layer1_list = self.get_child_wnd(timeline_table_el)

            # (2)get effect track -> its parent -> y position
            effect_track_locator = {'AXValue': 'Effect Track', 'AXIdentifier': '_NS:123'}
            effect_track_el = self.search_el(effect_track_locator)
            if effect_track_el is None:
                logger('search effect track el fail')
                return False
            # get parent
            parent_effect_track_el = self.get_parent_wnd(effect_track_el)
            # get parent's pos
            parent_effect_track_pos = self.get_pos(parent_effect_track_el, int_rule=0)
            if parent_effect_track_pos is False:
                logger('get parent effect track pos fail')
                return False

            # (3) match the y position to get fx timeline cell
            index_flag = ''
            for x in range(len(child_layer1_list)):
                try:
                    if self.get_pos(child_layer1_list[x], int_rule=0)[1] == parent_effect_track_pos[1]:
                        index_flag = x
                        break
                except:
                    logger('Exception(1)')
                    return False
            if index_flag == '':
                logger("can't find track")
                return False
            effect_track_cell_el = child_layer1_list[index_flag]
            logger(f'index cell is:{index_flag}')
            logger('Done')
            return effect_track_cell_el
        elif option == 'pip':
            # (1)find timeline table
            timeline_table_locator = {'AXIdentifier': '_NS:17', 'AXRole': 'AXTable'}
            timeline_table_el = self.search_el(timeline_table_locator)
            if timeline_table_el is None:
                logger('search el fail')
                return False
            # find its child
            child_layer1_list = self.get_child_wnd(timeline_table_el)
            logger(child_layer1_list)
            # (2)get pip track it belongs to [0] for video track
            parent_pip_track_el = child_layer1_list[0]

            # get parent's pos
            parent_pip_track_pos = self.get_pos(parent_pip_track_el, int_rule=0)
            if parent_pip_track_pos is False:
                logger('get parent pip track pos fail')
                return False

            # (3) match the y position to get pip timeline cell
            index_flag = ''
            for x in range(len(child_layer1_list)):
                try:
                    if self.get_pos(child_layer1_list[x], int_rule=0)[1] == parent_pip_track_pos[1]:
                        index_flag = x
                        break
                except:
                    logger('Exception(1)')
                    return False
            if index_flag == '':
                logger("can't find track")
                return False
            effect_track_cell_el = child_layer1_list[index_flag]
            logger(f'index cell is:{index_flag}')
            logger('Done')
            return effect_track_cell_el
        elif option == 'video track 1':
            # (1)find timeline table
            timeline_table_locator = {'AXIdentifier': '_NS:17', 'AXRole': 'AXTable'}
            timeline_table_el = self.search_el(timeline_table_locator)
            if timeline_table_el is None:
                logger('search el fail')
                return False
            # find its child
            child_layer1_list = self.get_child_wnd(timeline_table_el)
            logger(child_layer1_list)
            # (2)get pip track it belongs to [0] for video track
            parent_pip_track_el = child_layer1_list[0]

            # get parent's pos
            parent_pip_track_pos = self.get_pos(parent_pip_track_el, int_rule=0)
            if parent_pip_track_pos is False:
                logger('get parent pip track pos fail')
                return False

            # (3) match the y position to get pip timeline cell
            index_flag = ''
            for x in range(len(child_layer1_list)):
                try:
                    if self.get_pos(child_layer1_list[x], int_rule=0)[1] == parent_pip_track_pos[1]:
                        index_flag = x
                        break
                except:
                    logger('Exception(1)')
                    return False
            if index_flag == '':
                logger("can't find track")
                return False
            effect_track_cell_el = child_layer1_list[index_flag]
            logger(f'index cell is:{index_flag}')
            logger('Done')
            return effect_track_cell_el
        elif option == 'video track 2':
            # (1)find timeline table
            timeline_table_locator = {'AXIdentifier': '_NS:17', 'AXRole': 'AXTable'}
            timeline_table_el = self.search_el(timeline_table_locator)
            if timeline_table_el is None:
                logger('search el fail')
                return False
            # find its child
            child_layer1_list = self.get_child_wnd(timeline_table_el)
            logger(child_layer1_list)
            # (2)get video track it belongs to [2] for video track 2
            parent_video_track_el = child_layer1_list[2]

            # get parent's pos
            parent_video_track_pos = self.get_pos(parent_video_track_el, int_rule=0)
            if parent_video_track_pos is False:
                logger('get parent video track pos fail')
                return False

            # (3) match the y position to get pip timeline cell
            index_flag = ''
            for x in range(len(child_layer1_list)):
                try:
                    if self.get_pos(child_layer1_list[x], int_rule=0)[1] == parent_video_track_pos[1]:
                        index_flag = x
                        break
                except:
                    logger('Exception(1)')
                    return False
            if index_flag == '':
                logger("can't find track")
                return False
            effect_track_cell_el = child_layer1_list[index_flag]
            logger(f'index cell is:{index_flag}')
            logger('Done')
            return effect_track_cell_el
        else:
            logger('incorrect parameter')
        return False
    '''

    def tap_cell(self, cell=1, target='video'):
        """
        cell: 1, 2, 3, 4
        target: video/audio
        :param cell:
        Note: tap left-top avoid tapping the icon
        """
        pos = self.get_cell_pos(cell, target)
        if pos is False:
            logger('get cell pos fail')
            return False
        if self.tap_pos((pos[0] + 5, pos[1] + 5)):
            logger('Done')
            return True
        else:
            logger('tap pos fail')
        return False

    def is_media_in_timeline(self, medianame):
        return self.is_pip_in_timeline(medianame)

    def is_effect_in_timeline(self, effectname):
        """
        get timeline cell => find its child => verify filename
        :param filename:
        :return:
        """
        effect_track_cell_el = self.get_timeline_cell('fx')
        if effect_track_cell_el is False:
            logger('get timeline cell fail')
            return False

        # (4) get its child -> child
        try:
            child_child_scrollarea_effect_track_cell_el = self.search_child_el_by_role(effect_track_cell_el, 'AXScrollArea')
            child_child_collection_effect_track_cell_el = self.search_child_el_by_role(child_child_scrollarea_effect_track_cell_el, 'AXList')
            child_child_section_effect_track_cell_el = self.search_child_el_by_role(child_child_collection_effect_track_cell_el, 'AXList')
        except:
            logger('Exception(2)')
            return False

        # (5) try to check if effect name in section's child
        group_el_list = self.get_child_wnd(child_child_section_effect_track_cell_el)
        if group_el_list is False:
            logger('get group_el_list fail')
            return False
        for x in range(len(group_el_list)):
            if self.get_axvalue(self.get_child_wnd(group_el_list[x])[1]) == effectname:
                logger('Done')
                return True
        logger("doens't exist in timeline")
        return False

    def is_pip_in_timeline(self, pipname):
        """
        get timeline cell => find its child => verify filename
        :param filename:
        :return:
        """
        effect_track_cell_el = self.get_timeline_cell('pip')
        if effect_track_cell_el is False:
            logger('get timeline cell fail')
            return False

        # (4) get its child -> child
        try:
            child_child_scrollarea_effect_track_cell_el = self.search_child_el_by_role(effect_track_cell_el, 'AXScrollArea')
            child_child_collection_effect_track_cell_el = self.search_child_el_by_role(child_child_scrollarea_effect_track_cell_el, 'AXList')
            child_child_section_effect_track_cell_el = self.search_child_el_by_role(child_child_collection_effect_track_cell_el, 'AXList')
            '''
            # old
            child_pip_track_cell_el = self.get_child_wnd(effect_track_cell_el)
            child_child_pip_track_cell_el = self.get_child_wnd(child_pip_track_cell_el[0])
            child_child_collection_pip_track_cell_el = self.get_child_wnd(child_child_pip_track_cell_el[0])
            child_child_section_pip_track_cell_el = self.get_child_wnd(child_child_collection_pip_track_cell_el[0])
            '''
        except:
            logger('Exception(2)')
            return False

        # (5) try to check if pip name in section's child
        group_el_list = self.get_child_wnd(child_child_section_effect_track_cell_el)
        if group_el_list is False:
            logger('get group_el_list fail')
            return False

        for x in range(len(group_el_list)):
            if self.get_axvalue(self.get_child_wnd(group_el_list[x])[1]) == pipname:
                logger('Done')
                return True
        logger("doens't exist in timeline")
        return False

    def is_particle_in_timeline(self, particlename):
        return self.is_pip_in_timeline(particlename)

    def is_title_in_timeline(self):
        """
        only check if has 'Title Here' text
        :param particlename:
        :return:
        """
        return self.is_pip_in_timeline('Title Here')

    def get_effect_name_pos(self, effectname):
        """
        name in timeline
        :param effectname:
        :return:
        """
        effect_track_cell_el = self.get_timeline_cell('fx')
        if effect_track_cell_el is False:
            logger('get timeline cell fail')
            return False

        # (4) get its child -> child
        try:
            child_child_scrollarea_effect_track_cell_el = self.search_child_el_by_role(effect_track_cell_el, 'AXScrollArea')
            child_child_collection_effect_track_cell_el = self.search_child_el_by_role(child_child_scrollarea_effect_track_cell_el, 'AXList')
            child_child_section_effect_track_cell_el = self.search_child_el_by_role(child_child_collection_effect_track_cell_el, 'AXList')
            '''
            #old
            child_effect_track_cell_el = self.get_child_wnd(effect_track_cell_el)
            child_child_effect_track_cell_el = self.get_child_wnd(child_effect_track_cell_el[0])
            child_child_collection_effect_track_cell_el = self.get_child_wnd(child_child_effect_track_cell_el[0])
            child_child_section_effect_track_cell_el = self.get_child_wnd(
                child_child_collection_effect_track_cell_el[0])
            '''
        except:
            logger('Exception(2)')
            return False

        # (5) try to check if effect name in section's child
        try:
            child_section_el_list = self.get_child_wnd(child_child_section_effect_track_cell_el)
        except:
            logger('Exception(3)')
            return False
        for x in range(len(child_section_el_list)):
            text_el = self.get_child_wnd(child_section_el_list[x])[1]
            if self.get_axvalue(text_el) == effectname:
                logger('Done')
                return self.get_mid_pos(text_el)
        logger("doens't exist in timeline")
        return False


    def get_transition_name_pos(self, transitionname):
        """
        name in timeline
        :param effectname:
        :return:
        """
        effect_track_cell_el = self.get_timeline_cell('video track 1')
        if effect_track_cell_el is False:
            logger('get timeline cell fail')
            return False

        # (4) get its child -> child
        try:
            child_effect_track_cell_el = self.get_child_wnd(effect_track_cell_el)
            child_child_effect_track_cell_el = self.get_child_wnd(child_effect_track_cell_el[0])
            child_child_collection_effect_track_cell_el = self.get_child_wnd(child_child_effect_track_cell_el[0])
            child_child_section_effect_track_cell_el = self.get_child_wnd(
                child_child_collection_effect_track_cell_el[0])
        except:
            logger('Exception(2)')
            return False

        # (5) try to check if effect name in section's child
        try:
            child_section_el_list = self.get_child_wnd(child_child_section_effect_track_cell_el[0])
        except:
            logger('Exception(3)')
            return False
        for x in range(len(child_section_el_list)):
            text_el = self.get_child_wnd(child_section_el_list[x])[1]
            if self.get_axvalue(text_el) == transitionname:
                logger('Done')
                return self.get_mid_pos(text_el)
        logger("doens't exist in timeline")
        return False

    def open_effect_setting(self, effectname):
        """
        double click effect -> verify if effect setting shows
        :param effectname:
        :return:
        """
        pos = self.get_effect_name_pos(effectname)
        if pos is False:
            logger('get pos fail')
            return False
        if self.click_mouse(pos, times=2):
            # verify
            if self.search_el(self.str_effect_settings) is not None:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('click mouse fail')
        return False

    def get_effect_setting_el(self):
        """
        structure: AXScrollArea(this function) -> group(s) -> slider
        :return:
        """
        el = self.search_el(self.el_effect_setting)
        if el is False:
            logger('get el fail')
            return False
        logger('Done')
        return el

    def adjust_effect_value(self, order, value):
        """
        NEW:
        :param order: 1(freqency)(0-200), 2(Strength)(0-200)
        :param value:
        :return:
        """
        index = order - 1
        scrollarea_el = self.get_effect_setting_el()
        if scrollarea_el is False:
            logger('get scrollarea_el fail')
            return False
        group_list = self.get_child_wnd(scrollarea_el)
        if group_list is False:
            logger('get group_list fail')
            return False
        slider = self.search_child_el_by_role(group_list[index], 'AXSlider')
        if slider is False:
            logger('get slider fail')
            return False
        tolerance = [value - 3, value + 3]
        if self.adjust_element_slider(slider, value, 0, 200, edge=12, tolerance=tolerance):
            logger('Done')
            return True
        else:
            logger('adjust fail')
        return False

    '''
#old
    def change_effect_value(self, ground_truth_folder):
        """
        hardcode, no element can be found
        :return:
        """
        org_img_name = 'change_effect_value_org.png'
        after_img_name = 'change_effect_value_after.png'
        # get org value
        pos = self.search_text_position('0.40')
        if pos is False:
            logger('get text pos fail')
            return False
        pos_crop = (pos[0] - 20, pos[1] - 20, 40, 40)
        org_img = self.snapshot(org_img_name, pos_crop)
        # crop to compare
        pos_indicator = self.search_pos_from_image('effect_indicator.png', ground_truth_folder=ground_truth_folder, order=1)
        if pos_indicator is False:
            self.remove_snapshot(org_img_name)
            logger('get indicator pos fail')
            return False
        # start to adjust
        if self.drag_mouse(pos_indicator, (pos_indicator[0] + 5, pos_indicator[1])):
            # verify
            after_img = self.snapshot(after_img_name, pos_crop)
            if self.compare(org_img_name, after_img_name) is False:
                self.remove_snapshot(org_img_name)
                self.remove_snapshot(after_img_name)
                logger('Done')
                return True
            else:
                # self.remove_snapshot(org_img_name)
                # self.remove_snapshot(after_img_name)
                logger('verify fail')
        else:
            self.remove_snapshot(org_img_name)
            logger('drag mouse fail')
        return False
    '''

    def drag_effect_to_timeline(self, effect_name, align_which=None, has_same_file=0):
        """
        :param align_which: if None, align most left, if has other effect, align the effect
        :param effect_name:
        :param has_same_file: if == 1, do not check exists in timeline
        :return:
        """
        # get fx cell
        fx_cell_el = self.get_timeline_cell('fx')
        if fx_cell_el is False:
            logger('get cell fail')
            return False
        # check if has effect in timeline
        try:
            child_effect_track_cell_el = self.get_child_wnd(fx_cell_el)
            child_child_effect_track_cell_el = self.get_child_wnd(child_effect_track_cell_el[0])
            child_child_collection_effect_track_cell_el = self.get_child_wnd(child_child_effect_track_cell_el[0])
            child_child_section_effect_track_cell_el = self.get_child_wnd(child_child_collection_effect_track_cell_el[0])
        except:
            logger('Exception(2)')
            return False
        align_which_flag = ''
        if align_which is None:
            if len(child_child_section_effect_track_cell_el) == 0:
                logger('Note: no effect in timeline')
                # destination is section_el's left
                destination_pos = self.get_pos(child_child_collection_effect_track_cell_el[0])
                if destination_pos is False:
                    logger('get destination pos fail')
                    return False
                # magic number adjustment
                destination_pos = (destination_pos[0] + 2, destination_pos[1] + 2)
                align_which_flag = 1
            else:
                # find out most right effect
                child_child_group_effect_track_cell_el = self.get_child_wnd(child_child_section_effect_track_cell_el[0])
                if child_child_group_effect_track_cell_el is False:
                    logger('get group el fail')
                    return False
                destination_pos = self.get_pos(child_child_group_effect_track_cell_el[0])
                if destination_pos is False:
                    logger('get destination pos fail')
                    return False
                # magic number adjustment
                destination_pos = (destination_pos[0] + destination_pos[2] + 2, destination_pos[1] + 2)
                align_which_flag = 1
        else:
            # TODO: need to fix
            # check if the align_which name exists
            if has_same_file == 1:
                pass
            else:
                if not self.is_effect_in_timeline(align_which):
                    logger(f'{align_which} effect not exists')
                    return False
            # destination is section_el's right
            effect_flag = ''
            logger(child_child_collection_effect_track_cell_el)
            logger(self.get_pos(child_child_collection_effect_track_cell_el[0]))
            logger(self.get_axrole(child_child_collection_effect_track_cell_el))
            child_child_section_effect_track_cell_el = self.get_child_wnd(child_child_collection_effect_track_cell_el[0])
            logger(child_child_section_effect_track_cell_el)
            logger(self.get_child_wnd(child_child_section_effect_track_cell_el))

            '''
            for x in range(len(child_child_section_effect_track_cell_el)):
                if self.get_axvalue(self.get_child_wnd(child_child_section_effect_track_cell_el[x])[1]) == align_which:
                    effect_flag = x
                    break
            '''
            if effect_flag == '':
                logger(f"can't find {align_which}")
                return False
            child_child_group_effect_track_cell_el = self.get_child_wnd(child_child_section_effect_track_cell_el[effect_flag])
            if child_child_group_effect_track_cell_el is False:
                logger('get group el fail')
                return False
            destination_pos = self.get_pos(child_child_group_effect_track_cell_el[1])
            if destination_pos is False:
                logger('get destination pos fail')
                return False
            # magic number adjustment
            destination_pos = (destination_pos[0] + destination_pos[2] + 2, destination_pos[1] + 2)
            align_which_flag = 1

        if align_which_flag != 1:
            logger('check align which flag fail')
            return False

        # select element and get current position
        if not self.select_effect(effect_name):
            logger('select effect fail')
            return False
        start_pos = self.get_mouse_pos()
        if start_pos is False:
            logger('get start position fail')
            return False

        # drag section
        if self.drag_mouse(start_pos, destination_pos):
            check_flag = 1
        else:
            logger('drag mouse fail')
            return False

        # verification part
        if check_flag == 1:
            if self.is_effect_in_timeline(effect_name):
                logger('Done')
                return True
            else:
                logger('verify fail')
                return False
        else:
            logger('verification part fail')
        return False

    def get_cell_pos(self, cell=1, target='video'):
        """
        cell: 1, 2, 3, 4
        target: video/audio
        :param cell:
        :param target:
        :return: (x, y, w, h)
        """
        if target == 'video':
            target = 'Video Track'
        elif target == 'audio':
            target = 'Audio Track'
        else:
            logger('incorrect parameter')
            return False
        # get cell table el
        #old table_el = self.search_el(self.area_cell_frame)
        table_el = self.get_timeline_left_cell_table_el()
        if table_el is None:
            logger('search el fail')
            return False
        # get it's child
        table_el_child_list = self.get_child_wnd(table_el)
        table_row_list = []
        # filter out others(keep table row)
        for x in range(len(table_el_child_list)):
            if self.get_axrole(table_el_child_list[x]) == 'AXRow':
                table_row_list.append(table_el_child_list[x])
        logger(f'table_row_list: {table_row_list}')
        # search target index
        cell_el_child_list = []
        for y in range(len(table_row_list)):
            cell_el_list = self.get_child_wnd(table_row_list[y])
            if cell_el_list is False:
                continue
            text_layer_list = self.get_child_wnd(cell_el_list[0])
            if text_layer_list is False:
                continue
            # 1st one is text(ex: 1, 2, 3)
            if self.get_axvalue(text_layer_list[0]) == str(cell):
                cell_el_child_list.append(cell_el_list[0])
        logger(f'cell_el_child_list: {cell_el_child_list}')
        # search video or audio track
        for z in range(len(cell_el_child_list)):
            text_layer_list = self.get_child_wnd(cell_el_child_list[z])
            if text_layer_list is False:
                continue
            # 4th one is text field
            if self.get_axvalue(text_layer_list[3]) == target:
                # get pos
                pos = self.get_pos(cell_el_child_list[z])
                if pos is False:
                    logger(f'get pos fail. {z}times')
                    continue
                logger(f'Done. {pos}')
                return pos
        logger("can't find target")
        return False

    def drag_media_to_timeline(self, medianame, cell=1, target='video'):
        """
        drag aside the cell (cell: 1, 2, 3, target: video or audio cell)
        :param medianame:
        :param align_which:
        :param has_same_file:
        :return:
        """
        # get cell pos
        pos = self.get_cell_pos(cell, target)
        if pos is False:
            logger('get pos fail')
            return False
        destination_pos = (int(pos[0] + pos[2] + 2), int(pos[1] + pos[3] / 2))
        # select media
        if not self.select_media(medianame):
            logger('select media fail')
            return False
        start_pos = self.get_mouse_pos()
        if start_pos is False:
            logger('get start pos fail')
            return False
        if self.drag_mouse(start_pos, destination_pos):
            # verify
            if self.is_in_timeline(medianame):
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('drag mouse fail')
        return False

    def drag_transition_to_timeline(self, transition_name, align_which=None, has_same_file=0, verify_transition_num=1):
        """
        :param align_which: if None, align most left, if has other effect, align the effect
        :param effect_name:
        :param has_same_file: if == 1, do not check exists in timeline
        verify_transition number: how many transition in timeline
        :return:
        """
        # get fx cell
        fx_cell_el = self.get_timeline_cell('video track 1')
        if fx_cell_el is False:
            logger('get cell fail')
            return False
        # check if has effect in timeline
        logger('Jamie check 2731')
        try:
            child_effect_track_cell_el = self.get_child_wnd(fx_cell_el)
            child_child_effect_track_cell_el = self.get_child_wnd(child_effect_track_cell_el[0])
            child_child_collection_effect_track_cell_el = self.get_child_wnd(child_child_effect_track_cell_el[0])
            child_child_section_effect_track_cell_el = self.get_child_wnd(child_child_collection_effect_track_cell_el[0])
            logger('Jamie check 2737')
        except:
            logger('Exception(2)')
            return False
        align_which_flag = ''
        if align_which is None:
            logger('Jamie check 2743')
            if len(child_child_section_effect_track_cell_el) == 0:
                logger('Note: no effect in timeline')
                # destination is section_el's right
                destination_pos = self.get_pos(child_child_collection_effect_track_cell_el[0])
                if destination_pos is False:
                    logger('get destination pos fail')
                    return False
                # magic number adjustment
                destination_pos = (destination_pos[0] + 2, destination_pos[1] + 2)
                align_which_flag = 1
            else:
                # find out most right effect
                logger('Jamie check 2756')
                child_child_group_effect_track_cell_el = self.get_child_wnd(child_child_section_effect_track_cell_el[0])
                if child_child_group_effect_track_cell_el is False:
                    logger('get group el fail')
                    return False
                destination_pos = self.get_pos(child_child_group_effect_track_cell_el[0])
                if destination_pos is False:
                    logger('get destination pos fail')
                    return False
                # magic number adjustment
                destination_pos = (destination_pos[0] + destination_pos[2] - 5, destination_pos[1] + 2)
                align_which_flag = 1
        else:
            logger('Jamie check 2769')
            # TODO: need to fix
            # check if the align_which name exists
            if has_same_file == 1:
                pass
            else:
                if not self.is_effect_in_timeline(align_which):
                    logger(f'{align_which} effect not exists')
                    return False
            # destination is section_el's right
            effect_flag = ''
            logger(child_child_collection_effect_track_cell_el)
            logger(self.get_pos(child_child_collection_effect_track_cell_el[0]))
            logger(self.get_axrole(child_child_collection_effect_track_cell_el))
            child_child_section_effect_track_cell_el = self.get_child_wnd(child_child_collection_effect_track_cell_el[0])
            logger(child_child_section_effect_track_cell_el)
            logger(self.get_child_wnd(child_child_section_effect_track_cell_el))

            '''
            for x in range(len(child_child_section_effect_track_cell_el)):
                if self.get_axvalue(self.get_child_wnd(child_child_section_effect_track_cell_el[x])[1]) == align_which:
                    effect_flag = x
                    break
            '''
            if effect_flag == '':
                logger(f"can't find {align_which}")
                return False
            child_child_group_effect_track_cell_el = self.get_child_wnd(child_child_section_effect_track_cell_el[effect_flag])
            if child_child_group_effect_track_cell_el is False:
                logger('get group el fail')
                return False
            destination_pos = self.get_pos(child_child_group_effect_track_cell_el[1])
            if destination_pos is False:
                logger('get destination pos fail')
                return False
            # magic number adjustment
            destination_pos = (destination_pos[0] + destination_pos[2] + 2, destination_pos[1] + 2)
            align_which_flag = 1

        if align_which_flag != 1:
            logger('check align which flag fail')
            return False

        # select element and get current position
        if not self.select_transition(transition_name):
            logger('select effect fail')
            return False
        start_pos = self.get_mouse_pos()
        if start_pos is False:
            logger('get start position fail')
            return False

        # drag section
        if self.drag_mouse(start_pos, destination_pos):
            check_flag = 1
        else:
            logger('drag mouse fail')
            return False

        # verification part
        if check_flag == 1:
            if self.get_transition_number_timeline() == verify_transition_num:
                logger('Done')
                return True
            else:
                x = self.get_transition_number_timeline()
                print('verify fail, x = ', x)
                return False
        else:
            logger('verification part fail')
        return False

    def select_media(self, filename):
        """
        2 Role mode for material
        :param filename:
        :return:
        """
        locator_unselect = {'AXRole': 'AXStaticText', 'AXValue': f'{filename}'}
        locator_select = {'AXRole': 'AXTextField', 'AXValue': f'{filename}'}
        el_check = self.search_el(locator_unselect)
        if el_check is None:
            logger('search el fail')
            el_check = self.search_el(locator_select)
            if el_check is None:
                logger('search el fail')
                return False
        el_parent = self.get_parent_wnd(el_check)
        if el_parent is False:
            logger('get parent wnd fail')
            return False
        pos = self.get_mid_pos(el_parent)
        if pos is False:
            logger('get pos fail')
            return False
        if self.click_mouse(pos):
            logger('Done')
            return True
        else:
            logger('click mouse fail')
        return False

    def get_media_img_pos(self, filename):
        # new (for verify 4-1 mark icon)
        locator_unselect = {'AXRole': 'AXStaticText', 'AXValue': f'{filename}'}
        locator_select = {'AXRole': 'AXTextField', 'AXValue': f'{filename}'}
        el_check = self.search_el(locator_unselect)
        if el_check is None:
            logger('search el fail')
            el_check = self.search_el(locator_select)
            if el_check is None:
                logger('search el fail')
                return False
        el_parent = self.get_parent_wnd(el_check)
        if el_parent is False:
            logger('get parent wnd fail')
            return False
        img_el = self.search_child_el_by_role(el_parent, 'AXImage')
        if img_el is False:
            logger('get img_el fail')
            return False
        pos = self.get_pos(img_el)
        if pos is False:
            logger('get pos fail')
            return False
        logger(f'Done. ({pos})')
        return pos

    def tap_no_btn(self):
        if self.tap_locator(self.btn_no):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def reset_project(self, save=0, has_alert=1):
        """
        reset project
        save: 0: w/o saving
        has_alert: 1 (need close alert)
        :param save:
        :return:
        """
        if self.input_combo_keyboard('cmd_l', 'n'):
            time.sleep(2)
            # check if alert pops up
            if has_alert == 1:
                if self.search_el(self.img_critical_alert) is not None:
                    # tap no(w/o save)
                    if self.tap_no_btn():
                        logger('Done')
                        return True
                    else:
                        logger('tap no btn fail')
                else:
                    logger("alert doesn't pops up")
            elif has_alert == 0:
                logger('Done')
                return True
            else:
                logger('incorrect parameter')
        else:
            logger('input combo keyboard fail')
        return False

    def search_library(self, text):
        if self.tap_locator(self.column_search_text_field):
            # input text
            if self.input_text(text):
                logger('Done')
                return True
            else:
                logger('input text fail')
        else:
            logger('tap locator fail')
        return False

    def tap_x_icon(self):
        if self.tap_locator(self.icon_x):
            logger('Done')
            return True
        else:
            # handle another kind x icon
            if self.tap_locator(self.icon_x_setting_frame):
                logger('Done')
                return True
            else:
                logger('tap locator fail')
        return True

    def display_explorer_view(self):
        # check current status
        if self.search_el(self.str_media_content) is not None:
            logger('explorer view already express')
            return False
        else:
            if self.tap_locator(self.icon_display_hide_explorer_view):
                # verify if expressed
                if self.search_el(self.str_media_content) is not None:
                    logger('Done')
                    return True
                else:
                    logger('search el fail')
            else:
                logger('tap locator fail')
        return False

    def hide_explorer_view(self):
        # check current status
        if self.search_el(self.str_media_content) is None:
            logger('explorer view already fold')
            return False
        else:
            if self.tap_locator(self.icon_display_hide_explorer_view):
                # verify if expressed
                if self.search_el(self.str_media_content) is None:
                    logger('Done')
                    return True
                else:
                    logger('search el fail')
            else:
                logger('tap locator fail')
        return False

    def check_aa(self):
        logger(self.search_el(self.icon_add_a_new_tag))

    def hide_effectroom_explorer_view(self):
        """
        new: use pos to verify
        :return:
        """
        # check current status
        if self.search_el(self.icon_add_a_new_tag) is None:
            logger('explorer view already fold')
            return False
        else:
            org_pos = self.get_locator_pos(self.icon_display_hide_explorer_view)
            if org_pos is False:
                logger('get org_pos fail')
                return False
            if self.tap_locator(self.icon_display_hide_explorer_view):
                time.sleep(1)
                # verify if expressed
                changed_pos = self.get_locator_pos(self.icon_display_hide_explorer_view)
                if changed_pos is False:
                    logger('get changed_pos fail')
                    return False
                if org_pos != changed_pos:
                    logger(f'Done. {org_pos}, {changed_pos}')
                    return True
                else:
                    logger(f'verify fail{org_pos}, {changed_pos}')
                '''
                #old
                if self.search_el(self.icon_add_a_new_tag) is None:
                    logger('Done')
                    return True
                else:
                    logger('search el fail')
                '''
            else:
                logger('tap locator fail')
        return False

    def hide_piproom_explorer_view(self):
        return self.hide_effectroom_explorer_view()

    def hide_titleroom_explorer_view(self):
        return self.hide_effectroom_explorer_view()

    def display_piproom_explorer_view(self):
        return self.display_effectroom_explorer_view()

    def display_particleroom_explorer_view(self):
        return self.display_effectroom_explorer_view()

    def display_titleroom_explorer_view(self):
        return self.display_effectroom_explorer_view()

    def display_effectroom_explorer_view(self):
        """
        NEW: use pos to verify
        :return:
        """
        '''
        # check current status (old: not work)
        if self.search_el(self.icon_add_a_new_tag) is not None:
            logger('explorer view already express')
            return False
        '''
        org_pos = self.get_locator_pos(self.icon_display_hide_explorer_view)
        if org_pos is False:
            logger('get org_pos fail')
            return False
        if self.tap_locator(self.icon_display_hide_explorer_view):
            # verify if expressed
            time.sleep(1)
            changed_pos = self.get_locator_pos(self.icon_display_hide_explorer_view)
            if changed_pos is False:
                logger('get changed_pos fail')
                return False
            if org_pos != changed_pos:
                logger(f'Done. {org_pos}, {changed_pos}')
                return True
            else:
                logger('verify fail')
            """
            if self.search_el(self.icon_add_a_new_tag) is not None:
                logger('Done')
                return True
            else:
                logger('search el fail')
            """
        else:
            logger('tap locator fail')
        return False

    def add_new_tag(self, tag_name):
        if self.tap_locator(self.icon_add_a_new_tag):
            # verify if new tag shows
            if self.search_el(self.column_new_tag) is not None:
                # start to assign text
                if self.input_text(tag_name) and \
                        self.input_keyboard('enter'):
                    # verify if input name is exists
                    verify_locator = {'AXIdentifier': 'RoomTagTextField', 'AXValue': f'{tag_name} (0)'}
                    if self.search_el(verify_locator) is not None:
                        logger('Done')
                        return True
                    else:
                        logger('verification fail')
                else:
                    logger('input text fail')
            else:
                logger('search el fail')
        else:
            logger('tap locator fail')
        return False

    def add_effectroom_new_tag(self, tag_name):
        if self.tap_locator(self.icon_add_a_new_tag):
            # verify if new tag shows
            if self.search_el(self.column_effectroom_new_tag) is not None:
                # start to assign text
                if self.input_text(tag_name) and \
                        self.input_keyboard('enter'):
                    # verify if input name is exists
                    verify_locator = {'AXIdentifier': 'RoomTagOutlineViewTextField', 'AXValue': f'{tag_name} (0)'}
                    if self.search_el(verify_locator) is not None:
                        logger('Done')
                        return True
                    else:
                        logger('verification fail')
                else:
                    logger('input text fail')
            else:
                logger('search el fail')
        else:
            logger('tap locator fail')
        return False

    def add_piproom_new_tag(self, tag_name):
        if self.tap_locator(self.icon_add_a_new_tag):
            if self.search_el(self.column_piproom_new_tag) is not None:
                # start to assign text
                if self.input_text(tag_name) and \
                        self.input_keyboard('enter'):
                    # verify if input name is exists
                    verify_locator = {'AXIdentifier': 'RoomTagTextField', 'AXValue': f'{tag_name} (0)'}
                    if self.search_el(verify_locator) is not None:
                        logger('Done')
                        return True
                    else:
                        # TODO: sometimes would fail for inputing(need rename manually)
                        new_tag_locator = {'AXValue': 'New Tag (0)', 'AXIdentifier': 'RoomTagTextField'}
                        tag_pos = self.get_locator_mid_pos(new_tag_locator)
                        if tag_pos is False:
                            logger('get pos fail')
                            return False
                        if not self.click_mouse(tag_pos, 'right'):
                            logger('click mouse fail')
                            return False
                        if self.tap_menu_item('Rename Tag'):
                            # start to assign text
                            if self.input_text(tag_name) and \
                                    self.input_keyboard('enter'):
                                # verify if input name is exists
                                verify_locator = {'AXIdentifier': 'RoomTagTextField', 'AXValue': f'{tag_name} (0)'}
                                if self.search_el(verify_locator) is not None:
                                    logger('Done')
                                    return True
                                else:
                                    logger('verification fail')
                            else:
                                logger('input text fail(1)')
                        else:
                            logger('tap menu item fail')
                else:
                    logger('input text fail(2)')
            else:
                logger('search el fail')
        else:
            logger('tap locator fail')
        return False

    def add_titleroom_new_tag(self, tag_name):
        return self.add_piproom_new_tag(tag_name)

    def add_transitionroom_new_tag(self, tag_name):
        return self.add_piproom_new_tag(tag_name)

    def select_tag(self, tag_name, count=0):
        """
        auto add count( ex: AT_Test_Tag (0) )
        :param tag_name:
        :return:
        """
        locator = {'AXIdentifier': 'RoomTagTextField', 'AXValue': f'{tag_name} ({count})'}
        if self.tap_locator(locator):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def select_effectroom_tag(self, tag_name, count=0):
        """
        auto add count( ex: AT_Test_Tag (0) )
        :param tag_name:
        :return:
        """
        locator = {'AXIdentifier': 'RoomTagOutlineViewTextField', 'AXValue': f'{tag_name} ({count})'}
        if self.tap_locator(locator):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def select_piproom_tag(self, tag_name, count=0):
        """
        auto add count( ex: AT_Test_Tag (0) )
        :param tag_name:
        :return:
        """
        locator = {'AXIdentifier': 'RoomTagTextField', 'AXValue': f'{tag_name} ({count})'}
        if self.tap_locator(locator):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def alert_handle(self, option):
        """
        option: cancel, no, ok, yes, not allow
        :param option:
        :return:
        """
        locator = ''
        if option == 'ok':
            locator = self.btn_ok
        elif option == 'no':
            logger('line 3245 option = no')
            locator = self.btn_no
        elif option == 'yes':
            locator = self.btn_yes
        # check if alert pops up
        # PDR critical Alert
        if self.search_el(self.img_critical_alert) is not None:
            if self.tap_locator(locator):
                logger('Done')
                return True
            else:
                logger('tap locator fail1')
        # System Alert
        elif self.search_el(self.img_usernotificationcenter_alert) is not None:
            if self.tap_locator(locator):
                logger('Done')
                return True
            else:
                logger('tap locator fail2')
        # pdr Alert
        elif self.search_el(self.img_pdr_alert) is not None:
            if self.tap_locator(locator):
                logger('Done')
                return True
            else:
                logger('tap locator fail3')
        elif self.search_el(self.dialog_PDR_alert) is not None:
            if self.tap_locator(locator):
                logger('Done')
                return True
            else:
                logger('tap locator fail4')
        else:
            logger("can't find alert img5")
        return False

    def tap_ok_btn(self):
        if self.tap_locator(self.btn_ok):
            logger('Done')
            return True
        else:
            logger('tap fail')
        return False

    def tap_ok_btn_enable_ocr(self):
        ok_pos = self.search_text_position('OK')
        if ok_pos is False:
            logger('get text pos fail')
            return False
        if self.click_mouse(ok_pos):
            logger('Done')
            return True
        else:
            logger('click mouse fail')

    def tap_yes_btn(self):
        if self.tap_locator(self.btn_yes):
            logger('Done')
            return True
        else:
            logger('tap fail')
        return False

    def tap_apply_btn(self):
        if self.tap_locator(self.btn_apply):
            logger('Done')
            return True
        else:
            logger('tap fail')
        return False

    def delete_tag(self, tag_name, count=0):
        """
        auto add count( ex: AT_Test_Tag (0) )
        :param tag_name:
        :param count:
        :return:
        """
        if self.select_tag(tag_name, count):
            if self.tap_locator(self.icon_delete_the_selected_tag):
                # handle alert
                time.sleep(1)
                #if not self.alert_handle('ok'): ##v2219
                if not self.tap_locator(self.btn_ok):
                    logger('handle alert fail')
                    return False
                # verification
                verify_locator = {'AXIdentifier': 'RoomTagTextField', 'AXValue': f'{tag_name} ({count})'}
                if self.search_el(verify_locator) is None:
                    logger('Done')
                    return True
                else:
                    logger('verify fail')
            else:
                logger('tap locator fail')
        else:
            logger('select tag fail')
        return False

    def delete_effectroom_tag(self, tag_name, count=0):
        """
        auto add count( ex: AT_Test_Tag (0) )
        :param tag_name:
        :param count:
        :return:
        """
        if self.select_effectroom_tag(tag_name, count):
            if self.tap_locator(self.icon_delete_the_selected_tag):
                # handle alert
                time.sleep(1)
                if not self.alert_handle('ok'):
                    logger('handle alert fail')
                    return False
                # verification
                verify_locator = {'AXIdentifier': 'RoomTagOutlineViewTextField', 'AXValue': f'{tag_name} ({count})'}
                if self.search_el(verify_locator) is None:
                    logger('Done')
                    return True
                else:
                    logger('verify fail')
            else:
                logger('tap locator fail')
        else:
            logger('select tag fail')
        return False


    def delete_piproom_tag(self, tag_name, count=0):
        """
        auto add count( ex: AT_Test_Tag (0) )
        :param tag_name:
        :param count:
        :return:
        """
        if self.select_piproom_tag(tag_name, count):
            if self.tap_locator(self.icon_delete_the_selected_tag):
                # handle alert
                time.sleep(1)
                if not self.alert_handle('ok'):
                    logger('handle alert fail')
                    return False
                # verification
                verify_locator = {'AXIdentifier': 'RoomTagTextField', 'AXValue': f'{tag_name} ({count})'}
                if self.search_el(verify_locator) is None:
                    logger('Done')
                    return True
                else:
                    logger('verify fail')
            else:
                logger('tap locator fail')
        else:
            logger('select tag fail')
        return False



    def delete_particleroom_tag(self, tag_name, count=0):
        """
        auto add count( ex: AT_Test_Tag (0) )
        :param tag_name:
        :param count:
        :return:
        """
        if self.select_piproom_tag(tag_name, count):
            if self.tap_locator(self.icon_delete_the_selected_tag):
                # handle alert
                time.sleep(1)
                if not self.alert_handle('ok'):
                    logger('handle alert fail')
                    return False
                # verification
                verify_locator = {'AXIdentifier': 'RoomTagTextField', 'AXValue': f'{tag_name} ({count})'}
                if self.search_el(verify_locator) is None:
                    logger('Done')
                    return True
                else:
                    logger('verify fail')
            else:
                logger('tap locator fail')
        else:
            logger('select tag fail')
        return False

    def delete_titleroom_tag(self, tag_name, count=0):
        return self.delete_particleroom_tag(tag_name, count)

    def delete_transitionroom_tag(self, tag_name, count=0):
        return self.delete_particleroom_tag(tag_name, count)

    def select_mediaroom_option(self, option):
        """
        option: 'Media Content', 'Color Boards', 'Background Music', 'Sound Clips'
        :param option:
        :return:
        """
        # select option
        locator = ''
        wait_time = 0
        if option == 'Media Content':
            locator = self.str_media_content
        elif option == 'Color Boards':
            locator = self.str_color_boards
        elif option == 'Background Music':
            locator = self.str_background_music
            # need time for initial
            wait_time = 3
        elif option == 'Sound Clips':
            locator = self.str_sound_clips
            # need time for initial
            wait_time = 3
        else:
            logger('incorrect parameter')
            return False
        # tap locator
        time.sleep(wait_time)
        if self.tap_locator(locator):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def select_mediaroom_colorboard(self, option):
        """
        option: ex: 0,0,0   , 0,120,255
        :param option:
        :return:
        """
        locator = {'AXValue': option}
        if self.tap_locator(locator):
            # verify if selected ( if selected, the role would become AXTextField, org is AXStaticText)
            if self.get_axrole(self.search_el(locator)) == 'AXTextField':
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap locator fail')
        return False

    def tap_play_icon(self):
        if self.tap_locator(self.icon_play):
            time.sleep(3) # for download audio
            # verify
            if self.search_el(self.icon_pause) is not None:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap locator fail')
        return False

    def tap_pause_icon(self):
        if self.tap_locator(self.icon_pause):
            # verify
            if self.search_el(self.icon_play) is not None:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap locator fail')
        return False

    def tap_stop_icon(self):
        if self.tap_locator(self.icon_stop):
            # verify
            if self.search_el(self.icon_play) is not None:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap locator fail')
        return False

    def verify_playback(self, verify_short_content=0):
        """
        for case, only playback & stop
        if verify short content = 1, doesn't check pause case
        :return:
        """
        if self.tap_play_icon():
            if self.tap_stop_icon():
                logger('Done')
                return True
            else:
                logger('tap stop fail')
        else:
            if verify_short_content == 1:
                if self.tap_stop_icon():
                    logger('Done')
                    return True
                else:
                    logger('tap stop fail')
            else:
                logger('tap play fail')
        return False

    def background_music_table_list(self):
        """
        return list of all music(element) with list
        :return:
        """
        try:
            # in order to avoid download timing
            table_el_list = []
            for x in range(5):
                try:
                    music_el_list = []
                    #old music_table_locator = {'AXIdentifier': '_NS:394', 'AXRole': 'AXTable'}
                    music_table_locator = {'AXIdentifier': 'IDC_LIBRARY_TABLEVIEW_DETAILED', 'AXRole': 'AXTable'}
                    music_table_el = self.search_el(music_table_locator)
                    table_el_list = self.get_child_wnd(music_table_el)
                    # the last one of table_el_list is 'caption' (ex: name. type, duration...)
                    test = len(table_el_list)
                    break
                except:
                    time.sleep(1)
                    continue

            for x in range(len(table_el_list) - 1):
                res = self.get_child_wnd(table_el_list[x])
                try:
                    if len(res) == 6:
                        music_el_list.append(res)
                except:
                    continue
            return music_el_list
        except Exception as e:
            logger(f'Exception. ({e})')
            return False

    def search_background_music(self, music_name):
        """
        return list [[name_pos, category_pos, duration_pos, size_pos, date_pos, download_pos],
                        [name_el, category_el, duration_el, size_el, date_el, download_el]
                        ]
        :param music_name:
        :return:
        """
        try:
            music_el_list = self.background_music_table_list()
            if music_el_list is False:
                logger('get music_el_list fail')
                return False
            # start to search
            for x in range(len(music_el_list)):
                res = ''
                name_el_parent = self.get_child_wnd(music_el_list[x][0])
                name_el = name_el_parent[1]
                if self.get_axvalue(name_el) == music_name:
                    res = x
                    break
            if res == '':
                logger("can't find music")
                return False
            result = []
            result_pos = []
            result_el = [self.get_child_wnd(music_el_list[res][0])[1],
                         self.get_child_wnd(music_el_list[res][1])[0],
                         self.get_child_wnd(music_el_list[res][2])[0],
                         self.get_child_wnd(music_el_list[res][3])[0],
                         self.get_child_wnd(music_el_list[res][4])[0],
                         self.get_child_wnd(music_el_list[res][5])[0]
                         ]
            for y in range(len(result_el)):
                try:
                    result_pos.append(self.get_mid_pos(result_el[y]))
                except Exception as e:
                    logger(f'Exception. ({e})')
                    return False
            result = [result_pos, result_el]
            return result
        except Exception as e:
            logger(f'Exception. ({e})')
            return False

    def select_background_music(self, music_name):
        try:
            time.sleep(3)
            # wait 3sec. avoid loading
            target_pos = ()
            for x in range(3):
                time.sleep(1)
                target_pos = self.search_background_music(music_name)[0][0]
                if target_pos is not False:
                    break
                else:
                    continue
            if target_pos is False:
                logger('Get pos fail')
                return False
            if self.tap_pos(target_pos):
                logger('Done')
                return True
            else:
                logger('tap el fail')
            return False
        except Exception as e:
            logger(f'Exception. ({e})')
            return False

    def download_background_music(self, music_name):
        try:
            download_el = self.search_background_music(music_name)[1][5]
            if self.tap_element(download_el):
                # wait till cancel is disappear
                for x in range(10):
                    time.sleep(1)
                    if self.search_el(self.btn_cancel) is None:
                        # verify
                        if self.get_axlabel(self.search_background_music(music_name)[1][5]) == 'Icon DownloadOK':
                            logger('Done')
                            return True
            else:
                logger('tap el fail')
            return False
        except Exception as e:
            logger(f'Exception ({e})')
            return False

    def tap_menu_item(self, menu_item1, menu_item2=None, menu_item3=None, ocr_mode=0, order=1):
        """
        if ocr_mode == 1, use ocr mode
        :param menu_item1:
        :param menu_item2:
        :param menu_item3:
        :param ocr_mode:
        :return:
        """
        if ocr_mode == 0:
            menu_item1_locator = {'AXRole': 'AXMenuItem', 'AXTitle': f'{menu_item1}'}
            menu_item2_locator = {'AXRole': 'AXMenuItem', 'AXTitle': f'{menu_item2}'}
            menu_item3_locator = {'AXRole': 'AXMenuItem', 'AXTitle': f'{menu_item3}'}
            if self.tap_locator(menu_item1_locator):
                if menu_item2 is None:
                    logger('Done')
                    return True
                else:
                    if self.tap_locator(menu_item2_locator):
                        if menu_item3 is None:
                            logger('Done')
                            return True
                        else:
                            if self.tap_locator(menu_item3_locator):
                                logger('Done')
                                return True
                            else:
                                logger('tap locator fail(3)')
                    else:
                        logger('tap locator fail(2)')
            else:
                logger('tap locator fail(1)')
            # NEW: try another Role
            menu_item1_locator = {'AXRole': 'AXStaticText', 'AXValue': f'{menu_item1}'}
            menu_item2_locator = {'AXRole': 'AXStaticText', 'AXValue': f'{menu_item2}'}
            menu_item3_locator = {'AXRole': 'AXStaticText', 'AXValue': f'{menu_item3}'}
            if self.tap_locator(menu_item1_locator):
                if menu_item2 is None:
                    logger('Done')
                    return True
                else:
                    if self.tap_locator(menu_item2_locator):
                        if menu_item3 is None:
                            logger('Done')
                            return True
                        else:
                            if self.tap_locator(menu_item3_locator):
                                logger('Done')
                                return True
                            else:
                                logger('tap locator fail(3-1)')
                    else:
                        logger('tap locator fail(2-1)')
            else:
                logger('tap locator fail(1-1)')
            return False
        elif ocr_mode == 1:
            # TODO: only handle menu_item1, need to expand
            menu_item1_pos = self.search_text_position(menu_item1, mouse_move=0, order=order)
            if menu_item1_pos is not False:
                if self.click_mouse(menu_item1_pos):
                    logger('Done')
                    return True
                else:
                    logger('click mouse fail')
            else:
                logger('get pos fail')
        else:
            logger('Incorrect parameter')
        return False

    def delete_background_music(self, music_name):
        if self.click_mouse(self.search_background_music(music_name)[0][0], 'right'):
            if self.tap_menu_item('Delete from Disk'):
                # check if alert pops up
                if self.alert_handle('yes'):
                    # verify if become to download icon
                    logger('Done')
                    return True
                    # TODO: work arround(can't get AXLabel, PDR Mac should support this), ignore this for now
                    if self.get_axlabel(self.search_background_music(music_name)[1][5]) == 'Icon DownloadOK':
                        logger('Done')
                        return True
                    else:
                        logger('get axlabel fail')
                else:
                    logger('handle alert fail')
            else:
                logger('tap menu item fail')
        else:
            logger('click mouse fail')
        return False

    def get_preview_area(self):
        """
        in order to snapshot area for comparison
        :return: (x, y, w, h)
        """
        # need to transfer to tuple before return
        preview_area_pos = [0, 0, 0, 0]
        # get the gap between media room & preview area
        spliter_pos = self.get_locator_pos(self.spliter_between_mediaroom_and_preview)
        if spliter_pos is False:
            logger('get pos fail(1)')
            return False
        preview_area_pos[0] = spliter_pos[0] + spliter_pos[2]
        preview_area_pos[1] = spliter_pos[1]
        # get top group area
        top_group_pos = self.get_locator_pos(self.group_edit_page_top)
        if top_group_pos is False:
            logger('get pos fail(2)')
            return False
        preview_area_pos[2] = top_group_pos[0] + top_group_pos[2] - spliter_pos[0]
        # get playback slider area
        playback_slider_pos = self.get_locator_pos(self.slider_main_playback)
        if playback_slider_pos is False:
            logger('get pos fail(3)')
            return False
        preview_area_pos[3] = playback_slider_pos[1] - top_group_pos[1]
        logger(f'get area is : {tuple(preview_area_pos)}')
        return tuple(preview_area_pos)

    def select_room(self, option):
        """
        option: "Media Room", "Effect Room", "PiP Room", "Particle Room", "Title Room", "Transition Room",
                "Audiomixing Room", "Recording Room", "Subtitle Room"
        :param option:
        :return:
        """
        locator = ''
        verify_flag = ''
        if option == 'Media Room':
            locator = self.btn_media_room
            verify_flag = 1
        elif option == 'Effect Room':
            locator = self.btn_effect_room
            verify_flag = 2
        elif option == 'PiP Room':
            locator = self.btn_pip_room
            verify_flag = 3
        elif option == 'Particle Room':
            locator = self.btn_particle_room
            verify_flag = 4
        elif option == 'Title Room':
            locator = self.btn_title_room
            verify_flag = 5
        elif option == 'Transition Room':
            locator = self.btn_transition_room
            verify_flag = 6
        elif option == 'Audiomixing Room':
            locator = self.btn_audiomixing_room
            verify_flag = 7
        elif option == 'Recording Room':
            locator = self.btn_recording_room
            #new express [...]
            if not self.tap_locator(self.btn_room_express):
                logger('tap express fail(1)')
                return False
            verify_flag = 8
        elif option == 'Subtitle Room':
            locator = self.btn_subtitle_room
            # new express [...]
            if not self.tap_locator(self.btn_room_express):
                logger('tap express fail(1)')
                return False
            verify_flag = 9
        else:
            logger('Incorrect parameter')
            return False
        # start to tag
        if self.tap_locator(locator):
            # verification
            if verify_flag == 1:
                #v2219
                if self.search_el(self.str_food) is not None:
                    logger('Done')
                    return True
                else:
                    logger('verify fail')
            elif verify_flag == 2:
                if self.search_el(self.str_aberration) is not None:
                    logger('Done')
                    return True
                else:
                    logger('verify fail')
            elif verify_flag == 3:
                if self.is_content_exists('Dialog_03'):
                    logger('Done')
                    return True
                else:
                    logger('verify fail')
                """
                #old
                if self.search_el(self.str_free_templates) is not None:
                    logger('Done')
                    return True
                else:
                    logger('verify fail')
                """
            elif verify_flag == 4:
                if self.search_el(self.str_effect_a) is not None:
                    logger('Done')
                    return True
                else:
                    logger('verify fail')
            elif verify_flag == 5:
                if self.search_el(self.str_clover_01) is not None:
                    logger('Done')
                    return True
                else:
                    logger('verify fail')
            elif verify_flag == 6:
                if self.search_el(self.str_aberration) is not None:
                    logger('Done')
                    return True
                else:
                    logger('verify fail')
            elif verify_flag == 7:
                if self.search_el(self.str_audio1) is not None:
                    logger('Done')
                    return True
                else:
                    logger('verify fail')
            elif verify_flag == 8:
                self.activate_pdr()
                if self.search_el(self.str_mute_all_tracks_when_recording) is not None:
                    logger('Done')
                    return True
                else:
                    logger('verify fail')
            elif verify_flag == 9:
                self.activate_pdr()
                if self.search_el(self.btn_subtitle_add) is not None:
                    logger('Done')
                    return True
                else:
                    logger('verify fail')
            else:
                logger('incorrect flag')
        else:
            logger('tap locator fail')
        return False

    def tap_room_express_btn(self):
        if self.tap_locator(self.btn_room_express):
            logger('Done')
            return True
        else:
            logger('tap express fail')
        return False

    def select_effect(self, filename):
        return self.select_media(filename)

    def select_pip(self, filename):
        return self.select_media(filename)

    def select_particle(self, filename):
        return self.select_media(filename)

    def select_title(self, filename):
        return self.select_media(filename)

    def select_transition(self, filename):
        return self.select_media(filename)

    def tap_import_media_btn(self):
        if self.tap_locator(self.btn_import_media):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def import_media(self, filename, wait_menubar=1):
        """
        choose local all, and search and then press [OK] to import
        :param filename:
        :return:
        wait_menubar=1, need to wait menu bar
        """
        # go projects folder
        filename_new = os.path.abspath(os.path.sep.join([f"{os.getcwd()}", "..", "Material",filename]))
        if os.path.isfile(filename_new):
            path = filename_new.split(os.path.sep)[2:]
            self.tap_locator({'AXValue': path.pop(0), 'AXRole': 'AXStaticText'})
            for folder_name in path:
                if not self.tap_locator({'AXValue': folder_name, 'AXRole': 'AXTextField'}):
                    logger(f"select ({folder_name}) fail")
                    return False
            self.tap_locator({"AXTitle":"Open", "AXRole": "AXButton"})
            extractor = copy.deepcopy(self.driver)
            extractor.app_bundleID = "com.cyberlink.EffectExtractor"
            extractor.tap_locator({"AXTitle":"OK", "AXRole": "AXButton"})
            del extractor
            return True

        else:
            locator = {'AXValue': 'Project_PDR_Mac_AT', 'AXRole': 'AXStaticText'}
            if not self.tap_locator(locator):
                logger('select tab fail')
                return False
            if self.select_dlg_file('BFT') and \
                    self.select_dlg_file('Material') and \
                    self.select_dlg_file('TestContent'):
                pass
            else:
                logger('go projects folder fail')
                return False
        # select project
        if self.select_dlg_file(filename):
            if wait_menubar == 1:
                if self.till_pdr_menubar_shows():
                    logger('Done')
                    return True
                else:
                    logger('till pdr menubar fail')
            else:
                logger('Done')
                return True
        else:
            logger('select project fail')
        return False

    def till_pdr_menubar_shows(self):
        """
        Design for waiting importing..process dialogue
        :return:
        """
        locator = self.menubar_pdr
        wait_sec = 1
        for x in range(30):
            if self.search_el(locator) is not None:
                logger('Done')
                return True
            time.sleep(wait_sec)
            wait_sec += 0.5
        logger('still can not find after 30sec.')
        return False

    def tap_modifypip_btn(self):
        # tap modify btn
        if self.tap_locator(self.btn_modify_the_selected):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def tap_modifytitle_btn(self):
        return self.tap_modifypip_btn()

    def tap_create_a_new_title_btn(self):
        # tap create new btn
        if self.tap_locator(self.btn_create_a_new_pip):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return True

    def create_new_pip(self, filename):
        """
        choose local all, and search and then press [OK] to import
        :param filename:
        :return:
        """
        # tap create new btn
        if not self.tap_locator(self.btn_create_a_new_pip):
            logger('tap locator fail')
            return False

        # go projects folder
        time.sleep(1)
        locator = {'AXValue': 'Project_PDR_Mac_AT', 'AXRole': 'AXStaticText'}
        if not self.tap_locator(locator):
            logger('select tab fail')
            return False
        if self.select_dlg_file('BFT') and \
                self.select_dlg_file('Material') and \
                self.select_dlg_file('TestContent'):
            pass
        else:
            logger('go projects folder fail')
            return False
        # select file
        if self.select_dlg_file(filename):
            logger('Done')
            return True
        else:
            logger('select file fail')
        return False

    def input_custompipname(self, text):
        """
        NEW
        :param text:
        :return:
        """
        dlg_el = self.search_el(self.el_save_as_template_dlg)
        if dlg_el is False:
            logger('get dlg_el fail')
            return False
        text_column = self.search_child_el_by_role(dlg_el, 'AXTextField')
        if text_column is False:
            logger('get text_column fail')
            return False
        if self.tap_element(text_column):
            if self.input_text(text):
                logger('Done')
                return True
            else:
                logger('input text fail')
        else:
            logger('tap locator fail')
        return False

    def is_pipdesigner_popup(self, pip_name='Default'):
        """
        if has pip_name, need to change search locator
        :param pip_name:
        :return:
        """
        # str_pipdesigner_default = {'AXValue': 'PiP Designer  |  Default', 'AXRole': 'AXStaticText'}
        if pip_name == 'Default':
            locator = self.str_pipdesigner_default
        else:
            locator = {'AXValue': f'PiP Designer  |  {pip_name}', 'AXRole': 'AXStaticText'}
        if self.search_el(locator) is not None:
            logger('Done')
            return True
        else:
            logger('pip designer does not pop up')
        return False

    def is_maskdesigner_popup(self, pip_name='Default'):
        """
        if has pip_name, need to change search locator
        :param pip_name:
        :return:
        """
        # str_pipdesigner_default = {'AXValue': 'PiP Designer  |  Default', 'AXRole': 'AXStaticText'}
        if pip_name == 'Default':
            locator = self.str_pipdesigner_default
        else:
            locator = {'AXValue': f'Mask Designer  |  {pip_name}', 'AXRole': 'AXStaticText'}
        if self.search_el(locator) is not None:
            logger('Done')
            return True
        else:
            logger('mask designer does not pop up')
        return False

    def is_titledesigner_popup(self, title_name='Default'):
        """
        if has title name, need to change search locator
        :param title_name:
        :return:
        """
        # str_pipdesigner_default = {'AXValue': 'PiP Designer  |  Default', 'AXRole': 'AXStaticText'}
        if title_name == 'Default':
            locator = self.str_titledesigner_default
        else:
            locator = {'AXValue': f'Title Designer | {title_name}', 'AXRole': 'AXStaticText'}
        if self.search_el(locator) is not None:
            logger('Done')
            return True
        else:
            logger('title designer does not pop up')
        return False

    def is_has_lut(self):
        check_locator = {'AXValue': 'Color LUT (1)', 'AXRole': 'AXStaticText'}
        if self.search_el(check_locator) is not None:
            logger('Done')
            return True
        else:
            logger('search el fail')
        return False

    def select_effectroom_category(self, option):
        """
        option: 'All Content' ...etc
        :param option:
        :return:
        """
        # open drop down menu
        if self.select_drop_down_list(self.drop_down_menu_effect_room_category, f'{option}'):
            # verification
            if self.get_axtitle(self.search_el(self.drop_down_menu_effect_room_category)) == option:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('drop down list handle fail')
        return False
        '''
        # open drop down menu(old)
        if self.tap_locator(self.drop_down_menu_effect_room_category):
            if self.tap_menu_item(f'{option}'):
                # verification
                if self.get_axtitle(self.search_el(self.drop_down_menu_effect_room_category)) == option:
                    logger('Done')
                    return True
                else:
                    logger('verify fail')
            else:
                logger('tap menu item fail')
        else:
            logger('tap locator fail')
        return False
        '''

    def select_drop_down_list(self, drop_down_locator, target_menu_item, arrow_locator=None, element_mode=0, need_verify=1):
        """
        :param drop_down_locator: locator of drop-down item
        :param target_menu_item: target option
        :param need_verify=1, 0(for those open menu only, ex: open mask designer dlg)
        :return:
        arrow_locator: None(no need to tap arrow), element/locator(need to tap arrow)
        """
        if arrow_locator is None:
            if element_mode == 0:
                # open drop down menu
                if not self.tap_locator(drop_down_locator):
                    logger('tap locator fail')
                    return False
            elif element_mode == 1:
                if not self.tap_element(drop_down_locator):
                    logger('tap element fail')
                    return False
            else:
                logger('incorrect parameter')
                return False
            if self.tap_menu_item(f'{target_menu_item}'):
                if need_verify == 0:
                    logger('Done')
                    return True
                # verification
                if element_mode == 0:
                    if self.get_axtitle(self.search_el(drop_down_locator)) == target_menu_item:
                        logger('Done')
                        return True
                    else:
                        logger('verify fail')
                elif element_mode == 1:
                    if self.get_axtitle(drop_down_locator) == target_menu_item:
                        logger('Done')
                        return True
                    else:
                        logger('verify fail')
                else:
                    logger('incorrect parameter')
            else:
                logger('tap menu item fail')
            return False
        else:
            if element_mode == 0:
                # open drop down menu
                if not self.tap_locator(arrow_locator):
                    logger('tap locator fail')
                    return False
            elif element_mode == 1:
                if not self.tap_element(arrow_locator):
                    logger('tap element fail')
                    return False
            else:
                logger('incorrect parameter')
                return False
            if self.tap_menu_item(f'{target_menu_item}'):
                # verification
                if element_mode == 0:
                    if self.get_axtitle(self.search_el(drop_down_locator)) == target_menu_item:
                        logger('Done')
                        return True
                    else:
                        logger('verify fail')
                elif element_mode == 1:
                    if self.get_axtitle(drop_down_locator) == target_menu_item:
                        logger('Done')
                        return True
                    else:
                        logger('verify fail')
                else:
                    logger('incorrect parameter')
            else:
                logger('tap menu item fail')
            return False


    def select_piproom_category(self, option):
        return self.select_effectroom_category(option)

    def select_titleroom_category(self, option):
        return self.select_effectroom_category(option)

    def tap_menubar_file(self):
        # tap menubar
        if self.tap_locator(self.menubar_file):
            if self.tap_locator(self.menubar_file_save_as):
                # check if dlg pops up(wait 2sec.)
                for x in range(3):
                    if self.search_el(self.dlg_save_file) is not None:
                        logger('Done')
                        return True
                    else:
                        time.sleep(1)
                        if x == 2:
                            logger('save file dlg does not pop up')
                            return False
            else:
                logger('tap menu item fail(1)')
                return False
        else:
            logger('tap menu item fail(2)')
            return False

    def tap_menubar_plugins(self):
        # tap menubar
        if self.tap_locator(self.menubar_plugins):
            if self.tap_locator(self.menubar_plugins_video_collage_designer):
                # check if dlg pops up (wait 2sec.)
                for x in range(3):
                    if self.search_el(self.dlg_video_collage_designer) is not None:
                        logger('Done')
                        return True
                    else:
                        time.sleep(1)
                        if x == 2:
                            logger('video collage designer dlg does not pop up')
                            return False
            else:
                logger('tap menu item fail(1)')
        else:
            logger('tap menu item fail(2)')
        return False

    def express_dlg_disclosure_triangle_icon(self, option):
        el = self.search_el(self.icon_disclosure_triangle)
        if el is False:
            logger('get el fail')
            return False
        if self.checkbox_handle(el, option, element_mode=1, verify=0):
            logger('Done')
            return True
        else:
            logger('checkbox handle fail')
        return False

    def save_project(self, project_name):
        """
        save project at \\BFT\\Material\\Projects\\
        :param name:
        :return:
        """
        # tap menubar
        for x in range(5):
            if self.tap_menubar_file():
                break
            time.sleep(2)
            if x == 4:
                logger('tap menubar fail')
                return False

        # if got project list, choose directly
        if not self.express_dlg_disclosure_triangle_icon('on'):
            logger('express dlg fail')
            return False
        if self.search_el(self.column_where_projects) is None:
            # go projects folder
            locator = {'AXValue': 'Project_PDR_Mac_AT', 'AXRole': 'AXStaticText'}
            if not self.tap_locator(locator):
                logger('select tab fail')
                return False
            if self.select_dlg_file('BFT') and \
                    self.select_dlg_file('Material') and \
                    self.select_dlg_file('Projects'):
                pass
            else:
                logger('go projects folder fail')
                return False
        else:
            pass
        # assign project name
        column_pos = self.get_locator_mid_pos(self.column_save_as_name)
        if column_pos is False:
            logger('get column pos fail')
            return False
        if self.click_mouse(column_pos, times=2):
            # input prject name
            if self.input_text(project_name):
                # click save
                if self.tap_locator(self.btn_dlg_save):
                    # click save btn
                    if self.tap_locator(self.btn_dlg_save):
                        time.sleep(1)
                        # close replace if any
                        self.tap_locator(self.btn_dlg_replace)
                        logger('Done')
                        time.sleep(1)
                        return True
                    else:
                        logger('tap save btn fail')
                else:
                    logger('tap btn save fail')
            else:
                logger('input text fail')
        else:
            logger('click mouse fail')
        return False

    def load_project(self, project_name):
        """
        load project at \\BFT\\Material\\Projects\\
        :param project_name:
        :return:
        """
        # tap menubar (wait 3sec. to show menubar)
        check_flag = ''
        for x in range(3):
            if self.tap_locator(self.menubar_file):
                check_flag = 1
                break
            else:
                if x == 2:
                    logger('timeout')
                    logger('tap menu item fail(2)')
                    return False
                time.sleep(1)

        if check_flag == '':
            logger('tap menu item fail(3)')
            return False

        if self.tap_locator(self.menubar_file_open_project):
            # check if dlg pops up(wait 2sec.)
            for x in range(3):
                if self.search_el(self.dlg_open) is not None:
                    break
                else:
                    time.sleep(1)
                    if x == 2:
                        logger('save file dlg does not pop up')
                        return False
        else:
            logger('tap menu item fail(1)')
            return False
        '''
        if not self.express_dlg_disclosure_triangle_icon('on'):
            logger('express dlg fail')
            return False
        '''

        if self.search_el(self.column_where_projects) is None:
            # go projects folder
            locator = {'AXValue': 'Project_PDR_Mac_AT', 'AXRole': 'AXStaticText'}
            if not self.tap_locator(locator):
                logger('select tab fail')
                return False
            if self.select_dlg_file('BFT') and \
                    self.select_dlg_file('Material') and \
                    self.select_dlg_file('Projects'):
                pass
            else:
                logger('go projects folder fail')
                return False
        else:
            logger('find projects column')
            pass
        # select project
        if self.select_dlg_file(f'{project_name}.pds'):
            # handle alert('no merge')
            if self.alert_handle('no'):
                # handle file missing case if any
                time.sleep(1)
                self.tap_locator(self.btn_dlg_ignore)
                logger('Done')
                return True
            else:
                logger('handle alert fail')
        else:
            logger('select project fail')
        return False

    def select_dlg_file(self, value, click=2):
        """
        select item in dialogue(list mode)
        :param value:
        :return:
        """
        # file name should not have [ ] symbol
        locator = {'AXValue': f'{value}', 'AXRole': 'AXTextField'}
        pos = self.get_locator_mid_pos(locator)
        if pos is False:
            logger(self.search_el(locator))
            logger('get pos fail')
            return False
        if type(click) is int:
            if self.click_mouse(pos, times=click):
                logger('Done')
                return True
            else:
                logger('click mouse fail')
        else:
            logger('incorrect parameter')
        return False

    def tap_tipsarea_modify(self):
        if self.tap_locator(self.btn_tipsarea_modify):
            # verify if enter modify page
            if self.search_el(self.str_transition_settings) is not None:
                logger('Done')
                return True
            else:
                logger('search el fail')
        else:
            logger('tap locator fail')
        return False

    def get_audio_track_number(self):
        locator = {'AXIdentifier': '_NS:123', 'AXRole': 'AXTextField', 'AXValue': 'Audio Track'}
        el_list = self.search_all_el(locator)
        if el_list is None:
            logger('search all el fail')
            return False
        try:
            audio_track_num = len(el_list)
            return audio_track_num
        except Exception as e:
            logger(f'Exception. ({e})')
            return False

    def get_audiomixing_track_number(self):
        try:
            # search section el
            el = self.search_el(self.area_audiomixing_group)
            if el is None:
                el = self.search_el(self.area_audiomixing_group1)
                if el is None:
                    logger('search el fail')
                    return False
            # get how many group('Audio mixing group')
            child_list = self.get_child_wnd(el)
            if child_list is False:
                logger('get child list fail')
                return False
            res = len(child_list)
            logger(f'Done. ({res})')
            return res
        except Exception as e:
            logger(f'Exception. ({e})')
            return False

    def get_audiomixing_el(self, index=0):
        """
        in order to get audiomixing group, index = 0 means 'audio 1'
        :param index:
        :return:
        """
        try:
            # search section el
            el = self.search_el(self.area_audiomixing_group)
            if el is None:
                el = self.search_el(self.area_audiomixing_group1)
                if el is None:
                    logger('search el fail')
                    return False
            # get how many group('Audio mixing group')
            child_list = self.get_child_wnd(el)
            if child_list is False:
                logger('get child list fail')
                return False
            if len(child_list) == 0:
                logger('get none audio mixing group')
                return False
            return child_list[index]
        except Exception as e:
            logger(f'Exception. ({e})')
            return False

    def get_audiomixing_frame(self, index):
        # get el
        el = self.get_audiomixing_el(index)
        if el is False:
            logger('Get el fail')
            return False
        pos = self.get_pos(el)
        if pos is False:
            logger('get pos fail')
            return False
        return pos

    def adjust_audiomixing_volume_slider(self, value, index=0):
        """
        index0 means 'audio 1'
        :param index:
        :return:
        """
        el = self.get_audiomixing_el(index)
        if el is False:
            logger('get audiomixing el fail')
            return False
        child_list = self.get_child_wnd(el)
        if child_list is False:
            logger('get child list fail')
            return False
        volume_slider_el = child_list[1]
        return self.adjust_element_slider(volume_slider_el, value)

    def tap_audiomixing_fade_in_btn(self, index):
        """
        tap audio mixing fade in btn
        index0 means: 'audio 1'
        :param index:
        :return:
        """
        try:
            # search all btn
            btn_list = self.search_all_el(self.btn_audiomixing_fade_in)
            if btn_list is None:
                logger('search all el fail')
                return False
            if self.tap_element(btn_list[index]):
                logger('Done')
                return True
            else:
                logger('tap element fail')
            return False
        except Exception as e:
            logger(f'Exception ({e})')
            return False

    def tap_audiomixing_fade_out_btn(self, index):
        """
        tap audio mixing fade in btn
        index0 means: 'audio 1'
        :param index:
        :return:
        """
        try:
            # search all btn
            btn_list = self.search_all_el(self.btn_audiomixing_fade_out)
            if btn_list is None:
                logger('search all el fail')
                return False
            if self.tap_element(btn_list[index]):
                logger('Done')
                return True
            else:
                logger('tap element fail')
            return False
        except Exception as e:
            logger(f'Exception ({e})')
            return False

    def tap_recording_preferences_btn(self):
        if self.tap_locator(self.btn_recording_preferences):
            # verify
            if self.search_el(self.str_caption_recording_preferences) is not None:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap locator fail')
        return False

    def checkbox_handle(self, locator, option, element_mode=0, verify=1):
        """
        option: 'on', 'off'
        element_mode: 0:use locator, 1: use element
        :param option:
        :return:
        Note: only for UI can return correct value element (1 or 0)
        """
        if option not in ['on', 'off']:
            logger('incorrect parameter')
            return False
        if element_mode == 0:
            el = self.search_el(locator)
            if el is None:
                logger('search el fail')
                return False
        elif element_mode == 1:
            el = locator
        else:
            logger('incorrect parameter')
            return False
        # start to check option
        if option == 'on':
            status = self.get_axvalue(el)
            if status == 1:
                logger('Done(1)')
                return True
            elif status == 0:
                if verify == 0:
                    logger('Done(a)')
                    return True
                else:
                    if self.tap_element(el):
                        # verify
                        time.sleep(1)
                        status = self.get_axvalue(el)
                        if status == 1:
                            logger('Done(2)')
                            return True
                        else:
                            logger(f'verify fail(1), status: ({status})')
                            return False
                    else:
                        logger('tap el fail(1)')
                        return False
            else:
                logger(f'get incorrect status(1): ({status})')
                return False
        elif option == 'off':
            status = self.get_axvalue(el)
            if status == 0:
                logger('Done(3)')
                return True
            elif status == 1:
                if verify == 0:
                    logger('Done(b)')
                    return True
                else:
                    if self.tap_element(el):
                        # verify
                        time.sleep(1)
                        status = self.get_axvalue(el)
                        if status == 0:
                            logger('Done(4)')
                            return True
                        else:
                            logger(f'verify fail(2), status: ({status})')
                            return False
                    else:
                        logger('tap el fail(2)')
            else:
                logger(f'get incorrect status(2): ({status})')
                return False
        else:
            logger('unexpected error')
        return False

    def tap_recording_start_btn(self):
        if self.tap_locator(self.btn_recording_record):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def tap_recording_stop_btn(self):
        if self.tap_locator(self.btn_recording_stop):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def get_timeline_recording_audio_el(self, audioname):
        locator = {'AXValue': f'{audioname}', 'AXRole': 'AXStaticText'}
        el = self.search_el(locator)
        if el is not None:
            logger('Done')
            return el
        else:
            logger('search el fail')
        return False

    def get_timeline_recording_audio_pos(self, audioname):
        el = self.get_timeline_recording_audio_el(audioname)
        if el is False:
            logger('get timeline recording audio el fail')
            return False
        # get its parent to get length
        parent_el = self.get_parent_wnd(el)
        if parent_el is False:
            logger('get parent fail')
            return False
        pos = self.get_pos(parent_el, int_rule=0)
        if pos is not False:
            logger(f'Done. {pos}')
            return pos
        else:
            logger('get pos fail')
        return False

    def get_timeline_timecode_el(self, timecode):
        """
        ex: timecode: '00;00;00'
        :param timecode:
        :return:
        """
        locator = {'AXValue': f'{timecode}', 'AXRole': 'AXStaticText'}
        el = self.search_el(locator)
        if el is not None:
            logger('Done')
            return el
        else:
            logger('search el fail')
        return False

    def get_timeline_timecode_pos(self, timecode):
        """
        in order to count the length
        ex: timecode: '00;00;00'
        :param timecode:
        :return:
        """
        el = self.get_timeline_timecode_el(timecode)
        if el is False:
            logger('get timeline timecode el fail')
            return False
        # get its parent
        parent_el = self.get_parent_wnd(el)
        if parent_el is False:
            logger('get parent fail')
            return False
        pos = self.get_pos(parent_el, int_rule=0)
        if pos is not False:
            logger(f'Done. {pos}')
            return pos
        else:
            logger('get pos fail')
        return False

    def select_recording_seconds(self, option):
        """
        drop-down menu
        :param option: '1', '2', '3',...
        :return:
        """
        if self.tap_locator(self.drop_down_menu_recording_seconds):
            if self.tap_menu_item(option):
                # verify
                el = self.search_el(self.drop_down_menu_recording_seconds)
                if el is None:
                    logger('search el fail')
                    return False
                title = self.get_axtitle(el)
                if title == option:
                    logger('Done')
                    return True
                else:
                    logger(f'verify fail. title: ({title})')
                    return False
            else:
                logger('tap menu item fail')
        else:
            logger('tap locator fail')
        return False

    def get_recording_value(self):
        """
        :return: int
        """
        el = self.search_el(self.str_recording_value)
        if el is None:
            logger('search el fail')
            return False
        value = self.get_axvalue(el)
        if value is False:
            logger('get ax value fail')
            return False
        logger(f'Done. ({int(value)})')
        return int(value)

    def adjust_recording_volume_slider(self, value):
        """
        :param value: int
        :return:
        """
        #x=150 y=156 w=19 h=158
        locator = {'AXPosition': (150.0, 156.0), 'AXSize': (19.0, 158.0), 'AXRole': 'AXSlider'}
        self.locator_generator(locator)
        """
        self.search_el(self.slider_recording)
        self.search_all_el(self.slider_recording)
        # search el
        if self.adjust_locator_slider(self.slider_recording, value):
            # verify
            if self.get_recording_value() == value:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('adjust locator slider fail')
        return False
        """

    def get_subtitle_table_el(self):
        """
        :return: table el/False
        Note: structure: Table -> "table row(subtitle row)/group(caption text)"
        """
        el = self.search_el(self.table_subtitle)
        if el is not None:
            logger('Done')
            return el
        else:
            logger('search el fail')
        return False

    def get_subtitle_number(self):
        """
        return how many number of subtitle
        :return:
        """
        table_el = self.get_subtitle_table_el()
        if table_el is False:
            logger('get table el fail')
            return False
        table_el_child_list = self.get_child_wnd(table_el)
        if table_el_child_list is False:
            logger('get table el child list fail')
            return False
        number = 0
        for x in range(len(table_el_child_list)):
            try:
                if self.get_axrole(table_el_child_list[x]) == 'AXRow':
                    number += 1
            except:
                continue
        logger(f'Done. ({number})')
        return number

    def get_subtitle_tablerow_el(self, index):
        """
        index: 1 means 1 in UI
        :return:
        Note: structure: Table -> "table row(subtitle row)/group(caption text)"
                table row, includs "index", "start time", "end time", "text"
        """
        table_el = self.get_subtitle_table_el()
        if table_el is False:
            logger('get table el fail')
            return False
        table_el_child_list = self.get_child_wnd(table_el)
        if table_el_child_list is False:
            logger('get table el child list fail')
            return False
        axrow_list = []
        for x in range(len(table_el_child_list)):
            try:
                if self.get_axrole(table_el_child_list[x]) == 'AXRow':
                    axrow_list.append(table_el_child_list[x])
            except:
                continue
        logger(f'Done. list is:({axrow_list})')
        return axrow_list[index - 1]

    def select_subtitle_index(self, index):
        """
        index: 1 means 1 in UI
        :return:
        Note: structure: Table -> "table row(subtitle row)/group(caption text)"
                table row, includs "index", "start time", "end time", "text"
                table row => cell => group => text
        """
        table_row_el = self.get_subtitle_tablerow_el(index)
        if table_row_el is False:
            logger('get subtitle tablerow el fail')
            return False
        child_el_list = self.get_child_wnd(table_row_el)
        if child_el_list is False:
            logger('get child_el_list fail')
            return False
        if self.tap_element(child_el_list[0]):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def get_subtitle_start_time(self, index):
        """
        index: 1 means 1 in UI
        :return:
        Note: structure: Table -> "table row(subtitle row)/group(caption text)"
                table row, includs "index", "start time", "end time", "text"
                table row => cell => group => text
        """
        table_row_el = self.get_subtitle_tablerow_el(index)
        if table_row_el is False:
            logger('get subtitle tablerow el fail')
            return False
        table_row_el_child_list = self.get_child_wnd(table_row_el)
        if table_row_el_child_list is False:
            logger('get table_row_el_child_list fail')
            return False
        start_time_cell_el = table_row_el_child_list[1]
        group_el_list = self.get_child_wnd(start_time_cell_el)
        if group_el_list is False:
            logger('get group_el_list fail')
            return False
        group_el_child_list = self.get_child_wnd(group_el_list[0])
        if group_el_child_list is False:
            logger('get group_el_child_list fail')
            return False
        start_time = self.get_axvalue(group_el_child_list[0])
        if start_time is False:
            logger('get start_time fail')
            return False
        logger(f'Done. ({start_time})')
        return start_time

    def get_subtitle_end_time(self, index):
        """
        index: 1 means 1 in UI
        :return:
        Note: structure: Table -> "table row(subtitle row)/group(caption text)"
                table row, includs "index", "start time", "end time", "text"
                table row => cell => group => text
        """
        table_row_el = self.get_subtitle_tablerow_el(index)
        if table_row_el is False:
            logger('get subtitle tablerow el fail')
            return False
        table_row_el_child_list = self.get_child_wnd(table_row_el)
        if table_row_el_child_list is False:
            logger('get table_row_el_child_list fail')
            return False
        end_time_cell_el = table_row_el_child_list[2]
        group_el_list = self.get_child_wnd(end_time_cell_el)
        if group_el_list is False:
            logger('get group_el_list fail')
            return False
        group_el_child_list = self.get_child_wnd(group_el_list[0])
        if group_el_child_list is False:
            logger('get group_el_child_list fail')
            return False
        end_time = self.get_axvalue(group_el_child_list[0])
        if end_time is False:
            logger('get start_time fail')
            return False
        logger(f'Done. ({end_time})')
        return end_time

    def get_subtitle_text(self, index):
        """
        index: 1 means 1 in UI
        :return:
        Note: structure: Table -> "table row(subtitle row)/group(caption text)"
                table row, includs "index", "start time", "end time", "text"
                table row => cell => group => text
        """
        table_row_el = self.get_subtitle_tablerow_el(index)
        if table_row_el is False:
            logger('get subtitle tablerow el fail')
            return False
        table_row_el_child_list = self.get_child_wnd(table_row_el)
        if table_row_el_child_list is False:
            logger('get table_row_el_child_list fail')
            return False
        text_cell_el = table_row_el_child_list[3]
        group_el_list = self.get_child_wnd(text_cell_el)
        if group_el_list is False:
            logger('get group_el_list fail')
            return False
        text = self.get_axvalue(group_el_list[0])
        if text is False:
            logger('get start_time fail')
            return False
        logger(f'Done. ({text})')
        return text

    def input_subtitle_text(self, index, text):
        """
        input text for subtitle,
        ex: index(1), text(AT Test)
        :param index:
        :param text:
        :return:
        """
        table_row_el = self.get_subtitle_tablerow_el(index)
        if table_row_el is False:
            logger('get subtitle tablerow el fail')
            return False
        table_row_el_child_list = self.get_child_wnd(table_row_el)
        if table_row_el_child_list is False:
            logger('get table_row_el_child_list fail')
            return False
        text_cell_el = table_row_el_child_list[3]
        group_el_list = self.get_child_wnd(text_cell_el)
        if group_el_list is False:
            logger('get group_el_list fail')
            return False
        text_el = group_el_list[0]
        # double click the element
        pos = self.get_pos(text_el)
        if pos is False:
            logger('get pos fail')
            return False
        if self.click_mouse((pos[0] + 5, pos[1] + 5), 'left'):
            time.sleep(1)
            if self.click_mouse((pos[0] + 5, pos[1] + 5), 'left'):
                pass
            else:
                logger('click mouse fail(1)')
                return False
        else:
            logger('click mouse fail(2)')
            return False
        # select all
        """ not support cmd + a
        if not self.input_combo_keyboard('cmd_l', 'a'):
            logger('input combo keyboard fail')
            return False
        """
        if not self.drag_mouse((pos[0] + pos[2] - 5, pos[1] + pos[3] - 5), (pos[0] + 5, pos[1] + 5)):
            logger('delete org text fail')
            return False
        # input
        if not self.input_text(text):
            logger('input combo keyboard fail')
            return False
        # enter(v2219, no need to press enter)
        '''
        if not self.input_keyboard('enter'):
            logger('input keyboard fail')
            return False
        '''
        # verify
        if self.get_subtitle_text(index) == text:
            logger('Done')
            return True
        else:
            logger('verify fail')
        return False

    def tap_subtitle_add_btn(self):
        if self.tap_locator(self.btn_subtitle_add):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def tap_subtitle_font_btn(self):
        if self.tap_locator(self.btn_subtitle_font):
            # verify
            if self.search_el(self.checkbox_subtitle_shadow) is not None:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap locator fail')
        return False

    def get_pipdesigner_timeline_el(self):
        res = self.search_el(self.section_pipdesigner_timeline)
        if res is not None:
            logger('Done')
            return res
        else:
            logger('search el fail')
        return False

    def get_pipdesigner_timeline_timecode_pos(self, timecode):
        """
        structure: section => group(s) => text
        :param timecode:
        :return:
        """
        section_el = self.get_pipdesigner_timeline_el()
        if section_el is False:
            logger('get section_el fail')
            return False
        # search timecode
        section_child_list = self.get_child_wnd(section_el)
        if section_child_list is False:
            logger('get section_child_list fail')
            return False
        check_flag = ''
        for x in range(len(section_child_list)):
            try:
                group_child = self.get_child_wnd(section_child_list[x])
                if group_child is False:
                    continue
                if self.get_axvalue(group_child[0]) == timecode:
                    check_flag = x
                    break
            except:
                continue
        if type(check_flag) is int:
            pos = self.get_pos(group_child[0])
            if pos is not False:
                logger(f'Done. {pos}')
                return pos
            else:
                logger('get pos fail')
        else:
            logger('check_flag fail')
        return False

    def tap_pipdesigner_timecode(self, timecode):
        """
        New: v2219(sometimes would fail) , AP's structure problem, use OCR to workarround
        :param timecode:
        :return:
        """
        try:
            pos = self.get_pipdesigner_timeline_timecode_pos(timecode)
            if pos is False:
                logger('get pip designer timeline timecode pos fail')
                return False
            if self.tap_pos((pos[0], pos[1] + pos[3] / 2)):
                logger('Done')
                return True
            else:
                logger('tap pos fail')
            return False
        except Exception as e:
            logger(f'structure problem. {e}')
            return False

    def get_pipdesigner_outline_el(self):
        """
        structure: outline => outline row(s) => cell => text/button/button/button
        :return:
        """
        outline_el = self.search_el(self.outline_pipdesigner)
        if outline_el is not None:
            logger('Done')
            return outline_el
        else:
            logger('search el fail')
        return False

    def get_pipdesigner_position_cell_el(self):
        outline_el = self.get_pipdesigner_outline_el()
        if outline_el is False:
            logger('get get_pipdesigner_outline_el fail')
            return False
        outline_el_child_list = self.get_child_wnd(outline_el)
        if outline_el_child_list is False:
            logger('get outline_el_child_list fail')
            return False
        # list[0] is index -> 1:position, 2:Scale, 3:opacity
        position_cell_list = self.get_child_wnd(outline_el_child_list[1])
        if position_cell_list is False:
            logger('get position_cell_list fail')
            return False
        logger('Done')
        return position_cell_list[0]

    def get_pipdesigner_scale_cell_el(self):
        outline_el = self.get_pipdesigner_outline_el()
        if outline_el is False:
            logger('get get_pipdesigner_outline_el fail')
            return False
        outline_el_child_list = self.get_child_wnd(outline_el)
        if outline_el_child_list is False:
            logger('get outline_el_child_list fail')
            return False
        # list[0] is index -> 1:position, 2:Scale, 3:opacity
        position_cell_list = self.get_child_wnd(outline_el_child_list[2])
        if position_cell_list is False:
            logger('get position_cell_list fail')
            return False
        logger('Done')
        return position_cell_list[0]

    def get_pipdesigner_opacity_cell_el(self):
        outline_el = self.get_pipdesigner_outline_el()
        if outline_el is False:
            logger('get get_pipdesigner_outline_el fail')
            return False
        outline_el_child_list = self.get_child_wnd(outline_el)
        if outline_el_child_list is False:
            logger('get outline_el_child_list fail')
            return False
        # list[0] is index -> 1:position, 2:Scale, 3:opacity
        position_cell_list = self.get_child_wnd(outline_el_child_list[3])
        if position_cell_list is False:
            logger('get position_cell_list fail')
            return False
        logger('Done')
        return position_cell_list[0]

    def get_pipdesigner_rotation_cell_el(self):
        outline_el = self.get_pipdesigner_outline_el()
        if outline_el is False:
            logger('get get_pipdesigner_outline_el fail')
            return False
        outline_el_child_list = self.get_child_wnd(outline_el)
        if outline_el_child_list is False:
            logger('get outline_el_child_list fail')
            return False
        # list[0] is index -> 1:position, 2:Scale, 3:opacity 4: rotation
        position_cell_list = self.get_child_wnd(outline_el_child_list[4])
        if position_cell_list is False:
            logger('get position_cell_list fail')
            return False
        logger('Done')
        return position_cell_list[0]

    def tap_pipdesigner_keyframe_btn(self, category, btn):
        """
        category: position/scale/opacity
        btn: left/keyframe/right
        :param category:
        :param btn:
        :return:
        """
        cell_el = eval(f'self.get_pipdesigner_{category}_cell_el()')
        if cell_el is False:
            logger('get cell el fail')
            return False
        # btn: 0~3, text/left/keyframe/right
        control_list = self.get_child_wnd(cell_el)
        if control_list is False:
            logger('get control_list fail')
            return False
        if btn == 'left':
            target_el = control_list[1]
        elif btn == 'keyframe':
            target_el = control_list[2]
        elif btn == 'right':
            target_el = control_list[3]
        else:
            logger('incorrect parameter')
            return False
        # start to tap
        if self.tap_element(target_el):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def get_pipdesigner_control_area(self):
        group_el = self.search_el(self.area_pipdesigner_right_frame)
        if group_el is None:
            logger('get group_el fail')
            return False
        spliter_el = self.search_child_el_by_role(group_el, 'AXSplitter')
        # get pos
        group_pos = self.get_pos(group_el)
        if group_pos is False:
            logger('get group_pos fail')
            return False
        spliter_pos = self.get_pos(spliter_el)
        if spliter_pos is False:
            logger('get spliter_pos fail')
            return False
        area_pos = (int(spliter_pos[0]), int(spliter_pos[1]), int(group_pos[2]), int(group_pos[1] + group_pos[3] - spliter_pos[1]))
        logger(f'Done. {area_pos}')
        return area_pos

    def get_pipdesigner_preview_area(self):
        preview_bottom_el = self.search_el(self.scroll_bar_pipdesigner_preview_bottom)
        if preview_bottom_el is None:
            logger('get preview_bottom_el fail')
            return False
        preview_right_el = self.search_el(self.scroll_bar_pipdesigner_preview_right)
        if preview_right_el is None:
            logger('get preview_right_el fail')
            return False
        # get pos
        preview_bottom_pos = self.get_pos(preview_bottom_el)
        if preview_bottom_pos is False:
            logger('get preview_bottom_pos fail')
            return False
        preview_right_pos = self.get_pos(preview_right_el)
        if preview_right_pos is False:
            logger('get preview_right_pos fail')
            return False
        area_pos = (int(preview_bottom_pos[0]), int(preview_right_pos[1]), int(preview_bottom_pos[2]), int(preview_right_pos[3]))
        logger(f'Done. {area_pos}')
        return area_pos

    def get_pipdesigner_outline_left_el(self):
        """
        structure: outline => outline row(s) => cell => text/triangle
        :return:
        """
        outline_el = self.search_el(self.outline_pipdesigner_left)
        if outline_el is not None:
            logger('Done')
            return outline_el
        else:
            logger('search el fail')
        return False

    def get_pipdesigner_objectsettings_cell_el(self):
        outline_el = self.get_pipdesigner_outline_left_el()
        if outline_el is False:
            logger('get get_pipdesigner_outline_el fail')
            return False
        outline_el_child_list = self.get_child_wnd(outline_el)
        if outline_el_child_list is False:
            logger('get outline_el_child_list fail')
            return False
        # list[0] is object -> 1:chroma key, 2:border, 3:shadow, 4:flip, 5:fade
        position_cell_list = self.get_child_wnd(outline_el_child_list[0])
        if position_cell_list is False:
            logger('get position_cell_list fail')
            return False
        logger('Done')
        return position_cell_list[0]

    def get_pipdesigner_chromakey_cell_el(self):
        outline_el = self.get_pipdesigner_outline_left_el()
        if outline_el is False:
            logger('get get_pipdesigner_outline_el fail')
            return False
        outline_el_child_list = self.get_child_wnd(outline_el)
        if outline_el_child_list is False:
            logger('get outline_el_child_list fail')
            return False
        # list[0] is objectsettings -> 1:chromakey, 2:border, 3:shadow, 4:flip, 5:fade
        position_cell_list = self.get_child_wnd(outline_el_child_list[1])
        if position_cell_list is False:
            logger('get position_cell_list fail')
            return False
        logger('Done')
        return position_cell_list[0]

    def get_pipdesigner_border_cell_el(self):
        outline_el = self.get_pipdesigner_outline_left_el()
        if outline_el is False:
            logger('get get_pipdesigner_outline_el fail')
            return False
        outline_el_child_list = self.get_child_wnd(outline_el)
        if outline_el_child_list is False:
            logger('get outline_el_child_list fail')
            return False
        # list[0] is objectsettings -> 1:chromakey, 2:border, 3:shadow, 4:flip, 5:fade
        position_cell_list = self.get_child_wnd(outline_el_child_list[2])
        if position_cell_list is False:
            logger('get position_cell_list fail')
            return False
        logger('Done')
        return position_cell_list[0]

    def get_pipdesigner_shadow_cell_el(self):
        outline_el = self.get_pipdesigner_outline_left_el()
        if outline_el is False:
            logger('get get_pipdesigner_outline_el fail')
            return False
        outline_el_child_list = self.get_child_wnd(outline_el)
        if outline_el_child_list is False:
            logger('get outline_el_child_list fail')
            return False
        # list[0] is objectsettings -> 1:chromakey, 2:border, 3:shadow, 4:flip, 5:fade
        position_cell_list = self.get_child_wnd(outline_el_child_list[3])
        if position_cell_list is False:
            logger('get position_cell_list fail')
            return False
        logger('Done')
        return position_cell_list[0]

    def get_pipdesigner_flip_cell_el(self):
        outline_el = self.get_pipdesigner_outline_left_el()
        if outline_el is False:
            logger('get get_pipdesigner_outline_el fail')
            return False
        outline_el_child_list = self.get_child_wnd(outline_el)
        if outline_el_child_list is False:
            logger('get outline_el_child_list fail')
            return False
        # list[0] is objectsettings -> 1:chromakey, 2:border, 3:shadow, 4:flip, 5:fade
        position_cell_list = self.get_child_wnd(outline_el_child_list[4])
        if position_cell_list is False:
            logger('get position_cell_list fail')
            return False
        logger('Done')
        return position_cell_list[0]

    def get_pipdesigner_fade_cell_el(self):
        outline_el = self.get_pipdesigner_outline_left_el()
        if outline_el is False:
            logger('get get_pipdesigner_outline_el fail')
            return False
        outline_el_child_list = self.get_child_wnd(outline_el)
        if outline_el_child_list is False:
            logger('get outline_el_child_list fail')
            return False
        # list[0] is objectsettings -> 1:chromakey, 2:border, 3:shadow, 4:flip, 5:fade
        position_cell_list = self.get_child_wnd(outline_el_child_list[5])
        if position_cell_list is False:
            logger('get position_cell_list fail')
            return False
        logger('Done')
        return position_cell_list[0]

    def get_pipdesigner_checkbox_el(self, option):
        """
        option : chromakey, border, shadow, flip, fade
        :param option:
        :return:
        """
        cell_el = eval(f'self.get_pipdesigner_{option}_cell_el()')
        if cell_el is False:
            logger('get cell el fail')
            return False
        checkbox_el = self.search_child_el_by_role(cell_el, 'AXCheckBox')
        if checkbox_el is not False:
            logger('Done')
            return checkbox_el
        else:
            logger('search_child_el_by_role fail')
        return False

    def express_fold_pipdesigner_option(self, category):
        """
        category: # list[0] is objectsettings -> 1:chromakey, 2:border, 3:shadow, 4:flip, 5:fade
        :param category:
        :return:
        """
        cell_el = eval(f'self.get_pipdesigner_{category}_cell_el()')
        if cell_el is False:
            logger('get cell el fail')
            return False
        # index 1 is triangle icon
        triangle_el = self.search_child_el_by_role(cell_el, 'AXDisclosureTriangle')
        if triangle_el is False:
            triangle_el = self.get_child_wnd(cell_el)[2]
            if triangle_el is False:
                logger('get triangle_el fail')
                return False
        if self.tap_element(triangle_el):
            time.sleep(1)
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def get_pipdesigner_ease_in_el(self, order):
        res = self.search_all_el(self.checkbox_ease_in, order)
        if res is not None:
            logger('Done')
            return res
        else:
            logger('search all el fail')
            return False

    def get_pipdesigner_ease_out_el(self, order):
        res = self.search_all_el(self.checkbox_ease_out, order)
        if res is not None:
            logger('Done')
            return res
        else:
            logger('search all el fail')
            return False

    def scroll_pipdesigner_right(self, option):
        """
        :param option: up/down
        :return:
        """
        pos = self.get_locator_pos(self.scroll_bar_pipdesigner_right)
        if pos is False:
            logger('get pos fail')
            return False
        if option not in ['up', 'down']:
            logger('incorrect parameter')
            return False
        mid_pos = (int(pos[0] + pos[2] / 2), int(pos[1] + pos[3] / 2))
        up_pos = (int(pos[0] + pos[2] / 2), int(pos[1] + pos[3] / 4))
        down_pos = (int(pos[0] + pos[2] / 2), int(pos[1] + pos[3] * 3 / 4))
        # start to drag
        if option == 'up':
            if self.drag_mouse(mid_pos, up_pos):
                logger('Done')
                return True
            else:
                logger('drag mouse fial(1)')
                return False
        else:
            if self.drag_mouse(mid_pos, down_pos):
                logger('Done')
                return True
            else:
                logger('drag mouse fial(2)')
                return False

    def scroll_pipdesigner_left(self, option):
        """
        :param option: up/down
        :return:
        """
        pos = self.get_locator_pos(self.scroll_bar_pipdesigner_left)
        if pos is False:
            logger('get pos fail')
            return False
        if option not in ['up', 'down']:
            logger('incorrect parameter')
            return False
        mid_pos = (int(pos[0] + pos[2] / 2), int(pos[1] + pos[3] / 2))
        up_pos = (int(pos[0] + pos[2] / 2), int(pos[1] + pos[3] / 4))
        down_pos = (int(pos[0] + pos[2] / 2), int(pos[1] + pos[3] * 3 / 4))
        # start to drag
        if option == 'up':
            if self.drag_mouse(mid_pos, up_pos):
                logger('Done')
                return True
            else:
                logger('drag mouse fial(1)')
                return False
        else:
            if self.drag_mouse(mid_pos, down_pos):
                logger('Done')
                return True
            else:
                logger('drag mouse fial(2)')
                return False

# common function for scroll
    def scroll_scrollbar(self, locator, option, element_mode=0, top_bottom_ratio=4):
        """
        :param locator:
        :param option: 'up'/ 'down'  (TBD extend: left/right)
        :param element_mode:
        :return:
        top_bottom_ratio: the ratio of y-axis
        """
        pos = ''
        if element_mode == 0:
            pos = self.get_locator_pos(locator)
            if pos is False:
                logger('get pos fail(1)')
                return False
        elif element_mode == 1:
            pos = self.get_pos(locator)
            if pos is False:
                logger('get pos fail(2)')
                return False
        if option not in ['up', 'down']:
            logger('incorrect parameter')
            return False
        mid_pos = (int(pos[0] + pos[2] / 2), int(pos[1] + pos[3] / 2))
        up_pos = (int(pos[0] + pos[2] / 2), int(pos[1] + pos[3] / top_bottom_ratio))
        down_pos = (int(pos[0] + pos[2] / 2), int(pos[1] + pos[3] * 3 / top_bottom_ratio))
        # start to drag
        if option == 'up':
            if self.drag_mouse(mid_pos, up_pos):
                logger('Done')
                return True
            else:
                logger('drag mouse fial(1)')
                return False
        elif option == 'down':
            if self.drag_mouse(mid_pos, down_pos):
                logger('Done')
                return True
            else:
                logger('drag mouse fial(2)')
                return False
        else:
            logger('incorrect parameter')
        return False

    def tap_pipdesigner_chormakey_dropper(self, index=0):
        dropper_el = self.search_all_el(self.dropper_pipdesigner_chroma_key)
        if dropper_el is None:
            logger('search all el fail')
            return False
        if self.tap_element(dropper_el[index]):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def tap_pipdesigner_chromakey_delete(self, index=0):
        delete_el = self.search_all_el(self.btn_pipdesigner_chroma_key_delete)
        if delete_el is None:
            logger('search all el fail(1)')
            return False
        org_delete_num = len(delete_el)
        if self.tap_element(delete_el[index]):
            # verify
            delete_el = self.search_all_el(self.btn_pipdesigner_chroma_key_delete)
            if delete_el is None:
                logger('search all el fail(2)')
                return False
            delete_num = len(delete_el)
            if org_delete_num == delete_num + 1:
                logger('Done')
                return True
            else:
                logger(f'verify fail. org:{org_delete_num}, after:{delete_num}')
                return False
        else:
            logger('tap locator fail')
        return False

    def get_pipdesigner_chormakey_color_area(self):
        dropper_pos = self.get_locator_pos(self.dropper_pipdesigner_chroma_key)
        if dropper_pos is False:
            logger('get dropper_pos fail(1)')
            return False
        delete_pos = self.get_locator_pos(self.btn_pipdesigner_chroma_key_delete)
        if delete_pos is False:
            logger('get dropper_pos fail(2)')
            return False
        area_pos = (int(dropper_pos[0] + dropper_pos[2]), int(dropper_pos[1]), int(delete_pos[0] - (dropper_pos[0] + dropper_pos[2])), int(dropper_pos[3]))
        logger(f'Done. {area_pos}')
        return area_pos

    def adjust_pipdesigner_chormakey_color_range(self, value):
        el = self.search_el(self.slider_pipdesigner_chroma_key_color_range)
        if el is False:
            logger('search el fail')
            return False
        return self.adjust_element_slider(el, value, min=0, max=60)

    def adjust_pipdesigner_chormakey_denoise(self, value):
        el = self.search_el(self.slider_pipdesigner_chroma_key_denoise)
        if el is False:
            logger('search el fail')
            return False
        return self.adjust_element_slider(el, value)

    def adjust_pipdesigner_border_size(self, value):
        el = self.search_el(self.slider_pipdesigner_border_size)
        if el is False:
            logger('search el fail')
            return False
        return self.adjust_element_slider(el, value, min=0, max=10)

    def adjust_pipdesigner_border_blur(self, value):
        el = self.search_el(self.slider_pipdesigner_border_blur)
        if el is False:
            logger('search el fail')
            return False
        return self.adjust_element_slider(el, value, min=0, max=20)

    def adjust_pipdesigner_border_opacity(self, value):
        el = self.search_el(self.slider_pipdesigner_border_opacity)
        if el is False:
            logger('search el fail')
            return False
        return self.adjust_element_slider(el, value)

    def tap_pipdesigner_chromakey_add_new_key_btn(self):
        # count current dropper
        org_dropper_num_list = self.search_all_el(self.dropper_pipdesigner_chroma_key)
        if org_dropper_num_list is None:
            logger('search all el fail(1)')
            return False
        if self.tap_locator(self.btn_pipdesigner_chroma_key_add_new_key):
            dropper_num_list = self.search_all_el(self.dropper_pipdesigner_chroma_key)
            if dropper_num_list is None:
                logger('search all el fail(2)')
                return False
        else:
            logger('tap locator fail')
            return False
        if len(org_dropper_num_list) == len(dropper_num_list) - 1:
            logger('Done')
            return True
        else:
            logger(f'get wrong num. before:{len(org_dropper_num_list)}, after:{len(dropper_num_list)}')
            return False

    def select_pipdesigner_border_fill_type(self, option):
        if self.select_drop_down_list(self.drop_down_menu_pipdesigner_border_fill_type, option):
            logger('Done')
            return True
        else:
            logger('select drop down list fail')
        return False

    def adjust_pipdesigner_shadow_distance(self, value, tolerance):
        el = self.search_el(self.slider_pipdesigner_shadow_distance)
        if el is False:
            logger('search el fail')
            return False
        return self.adjust_element_slider(el, value, tolerance=tolerance)

    def adjust_pipdesigner_shadow_blur(self, value):
        el = self.search_el(self.slider_pipdesigner_shadow_blur)
        if el is False:
            logger('search el fail')
            return False
        return self.adjust_element_slider(el, value, min=0, max=20)

    def adjust_pipdesigner_shadow_opacity(self, value):
        el = self.search_el(self.slider_pipdesigner_shadow_opacity)
        if el is False:
            logger('search el fail')
            return False
        return self.adjust_element_slider(el, value)

    def tap_pipdesigner_direction(self, direction, ground_truth_folder):
        """
        direction = 'up, right, down, left'
        search up icon
        """
        if direction not in ['up', 'right', 'down', 'left']:
            logger('incorrect parameter')
            return False
        target_img = f'direction_{direction}.png'
        pos = self.search_pos_from_image(target_img, ground_truth_folder=ground_truth_folder)
        if pos is False:
            logger('search pos from image fail')
            return False
        if self.tap_pos(pos):
            logger('Done')
            return True
        else:
            logger('tap pos fail')
        return False

    def tap_pipdesigner_flip_upside_down_checkbox(self):
        if self.checkbox_handle(self.checkbox_pipdesigner_flip_upside_down, 'on'):
            logger('Done')
            return True
        else:
            logger('checkbox handle fail')
        return False

    def tap_pipdesigner_flip_left_to_right_checkbox(self):
        if self.checkbox_handle(self.checkbox_pipdesigner_flip_left_to_right, 'on'):
            logger('Done')
            return True
        else:
            logger('checkbox handle fail')
        return False

    def tap_pipdesigner_fade_out_checkbox(self, option):
        if self.checkbox_handle(self.checkbox_pipdesigner_fade_out, option):
            logger('Done')
            return True
        else:
            logger('checkbox handle fail')
        return False

    def tap_pipdesigner_fade_in_checkbox(self, option):
        if self.checkbox_handle(self.checkbox_pipdesigner_fade_in, option):
            logger('Done')
            return True
        else:
            logger('checkbox handle fail')
        return False

    def adjust_pipdesigner_position(self, ground_truth_folder):
        """
        search mid icon
        """
        pos = self.search_pos_from_image('pipdesigner_move.png', ground_truth_folder=ground_truth_folder)
        if pos is False:
            logger('search pos from image fail')
            return False
        if self.drag_mouse(pos, (pos[0] + 5, pos[1] + 5)):
            logger('Done')
            return True
        else:
            logger('drag pos fail')
        return False

    def adjust_pipdesigner_rotate(self, ground_truth_folder):
        """
        search mid icon
        """
        pos = self.search_pos_from_image('pipdesigner_rotate.png', ground_truth_folder=ground_truth_folder)
        if pos is False:
            logger('search pos from image fail')
            return False
        if self.drag_mouse(pos, (pos[0] + 5, pos[1] + 5)):
            logger('Done')
            return True
        else:
            logger('drag pos fail')
        return False

    def adjust_pipdesigner_resize(self, ground_truth_folder):
        """
        search mid icon
        """
        pos = self.search_pos_from_image('pipdesigner_resize.png', ground_truth_folder=ground_truth_folder)
        if pos is False:
            logger('search pos from image fail')
            return False
        if self.drag_mouse(pos, (pos[0] - 20, pos[1])):
            logger('Done')
            return True
        else:
            logger('drag pos fail')
        return False

    def tap_save_as_btn(self):
        if self.tap_locator(self.btn_saveas):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def get_titledesigner_cell_el(self):
        el = self.search_el(self.outline_titledesigner_cell)
        if el is not None:
            logger('Done')
            return el
        else:
            logger('search el fail')
        return False

    def get_titledesigner_cell_pos(self):
        el = self.get_titledesigner_cell_el()
        if el is False:
            logger('get_titledesigner_cell_el fail')
            return False
        pos = self.get_pos(el)
        if pos is not False:
            logger('Done')
            return pos
        else:
            logger('get pos fail')
        return False

    def get_titledesigner_cell_list(self):
        el = self.get_titledesigner_cell_el()
        if el is None:
            logger('get_titledesigner_cell_el fail')
            return False
        child_list = self.search_child_el_by_role(el, 'AXRow')
        if child_list is False:
            logger('child_list fail')
            return False
        logger('Done')
        return child_list

    def count_titledesigner_cell_num(self):
        list = self.get_titledesigner_cell_list()
        if list is not False:
            num = len(list)
            logger(f'Done.(num)')
            return num
        else:
            logger('get list fail')
        return False

    def get_titledesigner_cell_index_pos(self, index):
        """
        index: 1, 2, 3
        :param index:
        :return:
        """
        cell_list = self.get_titledesigner_cell_list()
        if cell_list is False:
            logger('get_titledesigner_cell_list fail')
            return False
        try:
            pos = self.get_pos(cell_list[index - 1])
            if pos is False:
                logger('get pos fail')
                return False
            logger(f'Done. {pos}')
            return pos
        except Exception as e:
            logger(f'Exception. {e}')
            return False

    def tap_titledesigner_cell_index(self, index):
        pos = self.get_titledesigner_cell_index_pos(index)
        if pos is False:
            logger('get pos fail')
            return False
        target_pos = (pos[0] + pos[2] * 3 / 4, pos[1] + pos[3] / 2)
        if self.tap_pos(target_pos):
            logger('Done')
            return True
        else:
            logger('tap pos fail')
        return False

    def express_fold_titledesigner_cell(self, index, verify=1):
        """
        index: 1, 2, 3
        :param index:
        :return:
        """
        try:
            cell_list = self.get_titledesigner_cell_list()
            if cell_list is False:
                logger('get cell list fail')
                return False
            target_cell_el = cell_list[index - 1]
            target_cell_child_list = self.get_child_wnd(target_cell_el)
            if target_cell_child_list is False:
                logger('get target_cell_child_list fail')
                return False
            cell_triangle_el = self.search_child_el_by_role(target_cell_child_list[0], 'AXDisclosureTriangle')
            if cell_triangle_el is False:
                logger('get cell_triangle_el fail')
                return False
            # verify
            org_status = self.get_axvalue(cell_triangle_el)
            if self.tap_element(cell_triangle_el):
                # verify
                time.sleep(1.5)
                if verify == 0:
                    logger('Done')
                    return True
                cell_triangle_el = self.search_child_el_by_role(target_cell_child_list[0], 'AXDisclosureTriangle')
                if cell_triangle_el is False:
                    cell_triangle_el = self.get_child_wnd(target_cell_child_list[0])[2]
                    if cell_triangle_el is False:
                        logger('get cell_triangle_el fail')
                        return False
                after_status = self.get_axvalue(cell_triangle_el)
                if after_status is False:
                    logger('get after_status fail')
                    return False
                if org_status != after_status:
                    logger('Done')
                    return True
                else:
                    logger('verify fail')
                    return False
            else:
                logger('tap element fail')
            return False
        except Exception as e:
            logger(f'Exception. ({e})')
            return False

    def get_titledesigner_preview_area(self):
        pos = self.get_locator_pos(self.area_titledesigner_preview)
        if pos is not False:
            logger(f'Done. {pos}')
            return pos
        else:
            logger('get pos fail')
        return False

    def get_titledesigner_timeline_area(self):
        pos = self.get_locator_pos(self.outline_titledesigner_timeline)
        if pos is not False:
            logger(f'Done. {pos}')
            return pos
        else:
            logger('get pos fail')
        return False

    def get_titledesigner_timeline_el(self):
        el = self.search_el(self.outline_titledesigner_timeline)
        if el is False:
            logger('search el fail')
            return False
        logger('Done')
        return el

    def get_titledesigner_timeline_list(self):
        scroll_area_el = self.get_titledesigner_timeline_el()
        if scroll_area_el is False:
            logger('get scroll_area_el fail')
            return False
        #search row layer
        row_list = self.search_child_el_by_role(scroll_area_el, 'AXRow')
        if row_list is False:
            logger('get row list fail')
            return False
        logger('Done')
        return row_list

    def get_titledesigner_timeline_index_el(self, index):
        """
        index: 1, 2, 3
        :param index:
        :return:
        """
        parent_el_list = self.get_titledesigner_timeline_list()
        if parent_el_list is False:
            logger('get parent_el_list fail')
            return False
        parent_el = parent_el_list[index - 1]
        cell_el = self.get_child_wnd(parent_el)
        if cell_el is False:
            logger('get cell el fail')
            return False
        logger('Done')
        return cell_el[0]

    def get_titledesinger_timeline_index_pos(self, index):
        """
        index: 1, 2, 3
        :param index:
        :return:
        """
        el = self.get_titledesigner_timeline_index_el(index)
        if el is False:
            logger('get_titledesigner_timeline_index_el fail')
            return False
        pos = self.get_pos(el)
        if pos is False:
            logger('get pos fail')
            return False
        logger(f'Done {pos}')
        return pos

    def get_titledesigner_timeline_text(self, index):
        """
        index: 1, 2, 3
        :param index:
        :return:
        """
        el = self.get_titledesigner_timeline_index_el(index)
        if el is False:
            logger('get_titledesigner_timeline_index_el fail')
            return False
        child = self.get_child_wnd(el)
        if child is False:
            logger('get_child_wnd fail')
            return False
        scroll_el = child[0]
        text_el = self.search_child_el_by_role(scroll_el, 'AXStaticText')
        if text_el is False:
            logger('search_child_el_by_role fail')
            return False
        text = self.get_axvalue(text_el)
        if text is not False:
            logger(f'Done. ({text})')
            return text
        else:
            logger('get text fail')
        return False

    #new
    def tap_titledesinger_timeline_text(self, index):
        """
        index: 1, 2, 3
        :param index:
        :return:
        """
        el = self.get_titledesigner_timeline_index_el(index)
        if el is False:
            logger('get_titledesigner_timeline_index_el fail')
            return False
        child = self.get_child_wnd(el)
        if child is False:
            logger('get_child_wnd fail')
            return False
        scroll_el = child[0]
        text_el = self.search_child_el_by_role(scroll_el, 'AXStaticText')
        if text_el is False:
            logger('search_child_el_by_role fail')
            return False
        if self.tap_element(text_el):
            logger('Done')
            return True
        else:
            logger('tap text fail')
        return False


    def tap_titledesigner_add_title_btn(self):
        if self.tap_locator(self.btn_titledesigner_add_title):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def tap_titledesigner_preview_left_top(self):
        """
        in order to confirm 'add text'
        :return:
        """
        pos = self.get_titledesigner_preview_area()
        if pos is False:
            logger('get pos fail')
            return False
        target_pos = (pos[0] + 5, pos[1] + 5)
        if self.tap_pos(target_pos):
            logger('Done')
            return True
        else:
            logger('tap pos fail')
        return False

    def add_titledesigner_text(self, text):
        """
        need to verify in test case
        :param text:
        :return:
        """
        if self.tap_titledesigner_add_title_btn():
            if self.input_text(text):
                if self.tap_titledesigner_preview_left_top():
                    logger('Done')
                    return True
                else:
                    logger('tap left top fail')
            else:
                logger('input text fail')
        else:
            logger('tap add title btn fail')
        return False

    def get_titledesigner_object_el(self):
        el = self.search_el(self.outline_titledesigner_object)
        if el is None:
            logger('get el fail')
            return False
        logger('Done')
        return el

    def get_titledesigner_object_scrollbar_el(self):
        el = self.search_el(self.scroll_bar_titledesigner_object)
        if el is None:
            logger('get el fail')
            return False
        logger('Done')
        return el

    def scroll_titledesigner_object_scrollbar(self, option):
        """
        :param option: 'up'/'down'
        :return:
        """
        scrollbar_el = self.get_titledesigner_object_scrollbar_el()
        if scrollbar_el is False:
            logger('get scrollbar el fail')
            return False
        if self.scroll_scrollbar(scrollbar_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('scroll scrollbar fail')
        return False

    def scroll_titledesigner_timeline_scrollbar(self, option):
        """
        :param option: 'up'/'down'
        :return:
        """
        scrollbar_el = self.search_el(self.scroll_bar_titledesigner_timeline)
        if scrollbar_el is False:
            logger('get scrollbar el fail')
            return False
        if self.scroll_scrollbar(scrollbar_el, option, element_mode=1, top_bottom_ratio=8):
            logger('Done')
            return True
        else:
            logger('scroll scrollbar fail')
        return False

    def get_titledesigner_object_list(self):
        outline_el = self.get_titledesigner_object_el()
        if outline_el is False:
            logger('get outline_el fail')
            return False
        row_list = self.search_child_el_by_role(outline_el, 'AXRow')
        if row_list is False:
            logger('get row_list fail')
            return False
        logger('Done')
        return row_list

    def get_titledesigner_object_cell_el(self, option):
        """
        option: Object: "Character Presets", "Font/Paragraph", "Font Face", "Border", "Object Settings", "Shadow",
                Effect: "Starting Effect", "Ending Effect"
                express: "Character types:", "icon font", "Blur:", "Size:", "Apply shadow to:", "Position", "Effect:"
        New option:
                Animation: "In Animation", "Out Animation"
        :param option:
        :return:
        """
        para_list = ["Character Presets", "Font/Paragraph", "Font Face", "Object Settings", "Shadow", "Border",
                     "Starting Effect", "Ending Effect",
                     "Character types:", "icon font", "Blur:", "Size:", "Apply shadow to:", "Position", "Effect:",
                     "In Animation", "Out Animation"]
        if option not in para_list:
            logger('incorrect parameter')
            return False
        row_list = self.get_titledesigner_object_list()
        if row_list is False:
            logger('get row_list fail')
            return False
        target = ''
        for x in range(len(row_list)):
            cell_el = self.get_child_wnd(row_list[x])
            if cell_el is False:
                logger(f'get cell el fail.({x})')
                return False
            text_el = self.search_child_el_by_role(cell_el[0], 'AXStaticText')
            if text_el is not False:
                # for has AXStaticText case
                text = self.get_axvalue(text_el)
                if text is False:
                    text = self.get_axvalue(text_el[0])
                    if text is False:
                        logger(f'get text fail. ({x})')
                        continue
                if text == option:
                    target = x
                    break
            else:
                # for has AXImage case
                img_el_list = self.search_child_el_by_role(cell_el[0], 'AXImage')
                if img_el_list is False:
                    logger(f'get img_el_list fail. ({x})')
                    continue
                img_label = self.get_axlabel(img_el_list[0])
                if img_label is False:
                    logger(f'get img_label fail. ({x})')
                    continue
                if img_label == option:
                    target = x
                    break
        if target != '':
            target_cell_el = self.get_child_wnd(row_list[target])
            if target_cell_el is False:
                logger('need to check(unexpected error)')
                return False
            logger('Done')
            return target_cell_el[0]
        else:
            logger("can't find")
        return False

    def express_fold_titledesigner_object(self, option):
        # get target cell
        cell_el = self.get_titledesigner_object_cell_el(option)
        if cell_el is False:
            logger('get cell_el fail(1)')
            return False
        triangle_el = self.search_child_el_by_role(cell_el, 'AXDisclosureTriangle')
        if triangle_el is False:
            logger('get triangle_el fail(1)')
            return False
        org_status = self.get_axvalue(triangle_el)
        if self.tap_element(triangle_el):
            # verify
            time.sleep(1.5)
            cell_el = self.get_titledesigner_object_cell_el(option)
            if cell_el is False:
                logger('get cell_el fail(2)')
                return False
            triangle_el = self.search_child_el_by_role(cell_el, 'AXDisclosureTriangle')
            if triangle_el is False:
                logger('get triangle_el fail(2)')
                return False
            after_status = self.get_axvalue(triangle_el)
            if org_status != after_status:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap element fail')
        return False

    def tick_titledesigner_object_checkbox(self, checkbox, option):
        # get target cell
        cell_el = self.get_titledesigner_object_cell_el(checkbox)
        if cell_el is False:
            logger('get cell_el fail')
            return False
        checkbox_el = self.search_child_el_by_role(cell_el, 'AXCheckBox')
        if checkbox_el is False:
            logger('get checkbox_el fail')
            return False
        if self.checkbox_handle(checkbox_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('checkbox handle fail')
        return False

    def get_titledesigner_object_scroll_area_el(self, option):
        """
        structure -> outline -> axrow -> cell -> "scroll area"(this function) -> collection/scroll bar
        :param option:
        :return:
        """
        cell_el = self.get_titledesigner_object_cell_el(option)
        if cell_el is False:
            logger('get cell_el fail')
            return False
        scroll_area_el = self.search_child_el_by_role(cell_el, 'AXScrollArea')
        if scroll_area_el is False:
            logger('get scroll_area_el fail')
            return False
        logger('Done')
        return scroll_area_el

    def get_titledesigner_character_preset_list(self):
        """
        collection -> section -> groups(this function, return list)
        :param option:
        :return:
        """
        scroll_area_el = self.get_titledesigner_object_scroll_area_el('Character types:')
        if scroll_area_el is False:
            logger('get scroll_area_el fail')
            return False
        collection_el = self.search_child_el_by_role(scroll_area_el, 'AXList')
        if collection_el is False:
            logger('get collection_el fail')
            return False
        section_el = self.search_child_el_by_role(collection_el, 'AXList')
        if section_el is False:
            logger('get section_el fail')
            return False
        preset_list = self.get_child_wnd(section_el)
        if preset_list is False:
            logger('get preset_list fail')
            return False
        logger('Done')
        return preset_list

    def select_titledesigner_character_preset(self, option):
        """
        option: 1, 2, 3, 4
        :param option:
        :return:
        Note: verify in test case
        """
        preset_list = self.get_titledesigner_character_preset_list()
        if preset_list is False:
            logger('get preset_list fail')
            return False
        if self.tap_element(preset_list[option - 1]):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def get_titledesigner_fontparagraph_list(self):
        """
        cell el -> control list(this function)
        :param option:
        :return:
        """
        cell_el = self.get_titledesigner_object_cell_el('icon font')
        if cell_el is False:
            logger('get cell_el fail')
            return False
        control_list = self.get_child_wnd(cell_el)
        if control_list is False:
            logger('get control_list fail')
            return False
        logger('Done')
        return control_list

    def get_titledesigner_fontparagraph_checkbox_list(self):
        """
        structure cell -> group -> checkbox(this function)
        :return:
        """
        cell_el = self.get_titledesigner_object_cell_el('icon font')
        if cell_el is False:
            logger('get cell_el fail')
            return False
        checkbox_list = []
        group_list = self.search_child_el_by_role(cell_el, 'AXGroup')
        if group_list is False:
            logger('get group_list fail')
            return False
        for x in range(len(group_list)):
            checkbox_el = self.search_child_el_by_role(group_list[x], 'AXComboBox')
            if checkbox_el is False:
                logger(f'get checkbox_el fail. {x}')
                continue
            checkbox_list.append(checkbox_el)
        logger('Done')
        return checkbox_list

    def get_titledesigner_fontparagraph_arrow_list(self):
        """
        structure cell -> group -> checkbox(this function)
        :return:
        """
        cell_el = self.get_titledesigner_object_cell_el('icon font')
        if cell_el is False:
            logger('get cell_el fail')
            return False
        arrow_list = []
        group_list = self.search_child_el_by_role(cell_el, 'AXGroup')
        if group_list is False:
            logger('get group_list fail')
            return False
        for x in range(len(group_list)):
            arrow_el = self.search_child_el_by_role(group_list[x], 'AXButton')
            if arrow_el is False:
                logger(f'get checkbox_el fail. {x}')
                continue
            arrow_list.append(arrow_el)
        logger('Done')
        return arrow_list

    def get_titledesigner_fontparagraph_font_type_arrow(self):
        arrow_list = self.get_titledesigner_fontparagraph_arrow_list()
        if arrow_list is False:
            logger('get arrow_list fail')
            return False
        # 1st is font type
        logger('Done')
        return arrow_list[0]

    def get_titledesigner_fontparagraph_font_size_arrow(self):
        arrow_list = self.get_titledesigner_fontparagraph_arrow_list()
        if arrow_list is False:
            logger('get arrow_list fail')
            return False
        # 2nd is font size
        logger('Done')
        return arrow_list[1]

    def get_titledesigner_fontparagraph_line_spacing_arrow(self):
        arrow_list = self.get_titledesigner_fontparagraph_arrow_list()
        if arrow_list is False:
            logger('get arrow_list fail')
            return False
        # 3rd is line spacing
        logger('Done')
        return arrow_list[2]

    def get_titledesigner_fontparagraph_text_spacing_arrow(self):
        arrow_list = self.get_titledesigner_fontparagraph_arrow_list()
        if arrow_list is False:
            logger('get arrow_list fail')
            return False
        # 4th is text spacing
        logger('Done')
        return arrow_list[3]

    def select_titldesigner_fontparagraph_font_type(self, option):
        arrow = self.get_titledesigner_fontparagraph_font_type_arrow()
        if arrow is False:
            logger('get arrow fail')
            return False
        checkbox = self.get_titledesigner_fontparagraph_checkbox_list()
        if checkbox is False:
            logger('get checkbox fail')
            return False
        # select menu
        if self.tap_element(arrow):
            text_pos = self.search_text_position(option)
            if text_pos is False:
                logger('get text_pos fail')
                return False
            if self.tap_pos(text_pos):
                time.sleep(1)
                # verify
                res = self.get_axvalue(checkbox[0])
                res_split = res.split(' ')
                if option in res_split:
                    logger(f'Done. ({res_split})')
                    return True
                else:
                    logger(f'verify fail. ({res})')
            else:
                logger('tap pos fail')
        else:
            logger('select drop down list fail')
        return False

    def select_titldesigner_fontparagraph_font_size(self, option):
        arrow = self.get_titledesigner_fontparagraph_font_size_arrow()
        if arrow is False:
            logger('get arrow fail')
            return False
        checkbox = self.get_titledesigner_fontparagraph_checkbox_list()
        if checkbox is False:
            logger('get checkbox fail')
            return False
        # select menu
        if self.tap_element(arrow):
            text_pos = self.search_text_position(option)
            if text_pos is False:
                logger('get text_pos fail')
                return False
            if self.tap_pos(text_pos):
                time.sleep(1)
                # verify
                res = self.get_axvalue(checkbox[1])
                if res == option or res == int(option):
                    logger(f'Done. ({res})')
                    return True
                else:
                    logger(f'verify fail. ({res})')
            else:
                logger('tap pos fail')
        else:
            logger('select drop down list fail')
        return False

    def select_titldesigner_fontparagraph_line_spacing(self, option):
        arrow = self.get_titledesigner_fontparagraph_line_spacing_arrow()
        if arrow is False:
            logger('get arrow fail')
            return False
        checkbox = self.get_titledesigner_fontparagraph_checkbox_list()
        if checkbox is False:
            logger('get checkbox fail')
            return False
        # select menu
        if self.tap_element(arrow):
            #hardcode press arrow down
            if self.input_keyboard('down') and \
                    self.input_keyboard('enter'):
                # verify
                res = self.get_axvalue(checkbox[2])
                if res == '5' or res == 5:
                    logger(f'Done. ({res})')
                    return True
                else:
                    logger(f'verify fail. ({res})')
            else:
                logger('verify fail')
        else:
            logger('tap element fail')
        return False

        """
        #old
            text_pos = self.search_text_position(option)
            if text_pos is False:
                logger('get text_pos fail')
                return False
            if self.tap_pos(text_pos):
                time.sleep(1)
                # verify
                res = self.get_axvalue(checkbox[2])
                if res == option or res == int(option):
                    logger(f'Done. ({res})')
                    return True
                else:
                    logger(f'verify fail. ({res})')
            else:
                logger('tap pos fail')
        else:
            logger('select drop down list fail')
        return False
        """

    def select_titldesigner_fontparagraph_text_spacing(self, option):
        arrow = self.get_titledesigner_fontparagraph_text_spacing_arrow()
        if arrow is False:
            logger('get arrow fail')
            return False
        checkbox = self.get_titledesigner_fontparagraph_checkbox_list()
        if checkbox is False:
            logger('get checkbox fail')
            return False
        # select menu
        if self.tap_element(arrow):
            text_pos = self.search_text_position(option)
            if text_pos is False:
                logger('get text_pos fail')
                return False
            if self.tap_pos(text_pos):
                # verify
                time.sleep(1)
                res = self.get_axvalue(checkbox[3])
                if res == option or res == int(option):
                    logger(f'Done.({res})')
                    return True
                else:
                    logger(f'verify fail. ({res})')
            else:
                logger('tap pos fail')
        else:
            logger('select drop down list fail')
        return False

    def get_titledesigner_fontparagraph_kerning_el(self):
        """
        structure cell -> kerning(this function)
        :return:
        """
        cell_el = self.get_titledesigner_object_cell_el('icon font')
        if cell_el is False:
            logger('get cell_el fail')
            return False
        kerning_el = self.search_child_el_by_role(cell_el, 'AXCheckBox')
        if kerning_el is False:
            logger('get kerning el fail')
            return False
        logger('Done')
        return kerning_el

    def get_titledesigner_fontparagraph_btn_list(self):
        """
        structure cell -> button lists(color/bold/italic/align left/mid/right)
        :return:
        """
        cell_el = self.get_titledesigner_object_cell_el('icon font')
        if cell_el is False:
            logger('get cell_el fail')
            return False
        btn_list = self.search_child_el_by_role(cell_el, 'AXButton')
        if btn_list is False:
            logger('get btn_list fail')
            return False
        logger('Done')
        return btn_list

    def tap_titledesinger_fontparagraph_bold_btn(self):
        btn_list = self.get_titledesigner_fontparagraph_btn_list()
        if btn_list is False:
            logger('get btn_list fail')
            return False
        if self.tap_element(btn_list[1]):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def tap_titledesinger_fontparagraph_italic_btn(self):
        btn_list = self.get_titledesigner_fontparagraph_btn_list()
        if btn_list is False:
            logger('get btn_list fail')
            return False
        if self.tap_element(btn_list[2]):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def tap_titledesinger_fontparagraph_alignment_btn(self, option):
        """
        :param option: "left/middle/right"
        :return:
        """
        if option not in ['left', 'middle', 'right']:
            logger('incorrect parameter')
            return False
        btn_list = self.get_titledesigner_fontparagraph_btn_list()
        if btn_list is False:
            logger('get btn_list fail')
            return False
        target_el = ''
        if option == 'left':
            target_el == btn_list[3]
        elif option == 'middle':
            target_el == btn_list[4]
        elif option == 'right':
            target_el == btn_list[5]
        if self.tap_element(target_el):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def get_titledesigner_fontface_list(self):
        """
        cell el -> control list(this function)
        :param option:
        :return:
        """
        cell_el = self.get_titledesigner_object_cell_el('Blur:')
        if cell_el is False:
            logger('get cell_el fail')
            return False
        control_list = self.get_child_wnd(cell_el)
        if control_list is False:
            logger('get control_list fail')
            return False
        logger('Done')
        return control_list

    def adjust_titledesigner_fontface_blur_slider(self, value):
        control_list = self.get_titledesigner_fontface_list()
        if control_list is False:
            logger('get control_list fail')
            return False
        slider_el = control_list[1]
        if self.adjust_element_slider(slider_el, value, min=0, max=20):
            logger('Done')
            return True
        else:
            logger('adjust slider fail')
        return False

    def adjust_titledesigner_fontface_opacity_slider(self, value):
        control_list = self.get_titledesigner_fontface_list()
        if control_list is False:
            logger('get control_list fail')
            return False
        slider_el = control_list[4]
        if self.adjust_element_slider(slider_el, value):
            logger('Done')
            return True
        else:
            logger('adjust slider fail')
        return False

    def tap_titledesigner_fontface_opacity_uniformcolor_btn(self):
        control_list = self.get_titledesigner_fontface_list()
        if control_list is False:
            logger('get control_list fail')
            return False
        btn_el = control_list[-4]
        if self.tap_element(btn_el):
            # verify
            time.sleep(1)
            if self.get_titledesigner_color_dialogue_el() is not False:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('adjust btn fail')
        return False

    def get_titledesigner_color_dialogue_el(self):
        el = self.search_el(self.dlg_titledesigner_color_dlg)
        if el is not None:
            logger('Done')
            return el
        else:
            logger('search el fail')
        return False

    def get_titledesigner_color_dialogue_input_column_list(self):
        group_el = self.get_titledesigner_color_dialogue_el()
        if group_el is False:
            logger('get group_el fail')
            return False
        child_list = self.search_child_el_by_role(group_el, 'AXTextField')
        if child_list is False:
            logger('get child list fail')
            return False
        logger('Done')
        return child_list

    def change_titledesigner_color_dialogue_color(self, option, value):
        """
        :param option: red/green/blue  (TBD: able to add HEX)
        :param value: 0~255
        :return:
        """
        if option not in ['red', 'green', 'blue']:
            logger('incorrect parameter. option')
            return False
        if not 0 <= value <= 255:
            logger('incorrect parameter. value')
            return False
        textfield_list = self.get_titledesigner_color_dialogue_input_column_list()
        if textfield_list is False:
            logger('get textfield_list fail')
            return False
        target_columne_el = ''
        if option == 'red':
            target_columne_el = textfield_list[0]
        elif option == 'green':
            target_columne_el = textfield_list[1]
        elif option == 'blue':
            target_columne_el = textfield_list[2]
        # tap column
        if self.set_text_on_element(target_columne_el, value, double_click=1):
            logger('Done')
            return True
        else:
            logger('set text fail')
        return False

    def get_dialogue_child_list(self, axtitle):
        """
        for getting all the AXWindow Role via title name(AXTitle)
        :return:
        """
        locator = {'AXRole': 'AXWindow', 'AXTitle': f'{axtitle}'}
        dlg_el = self.search_all_el(locator)
        if dlg_el is not None and len(dlg_el) != 0:
            # determine if element or list
            if type(dlg_el) is list:
                dlg_el = dlg_el[0]
            # start to get child list
            child_list = self.get_child_wnd(dlg_el)
            if child_list is not False:
                logger('Done')
                return child_list
            else:
                logger('get child_list fail')
        else:
            logger('search all el fail')
        return False

    def tap_dlg_close_icon(self, axtitle):
        """
        search axtitle and tap close icon
        :param axtitle:
        :return:
        """
        control_list = self.get_dialogue_child_list(axtitle)
        if control_list is False:
            logger('get control list fail')
            return False
        # search close icon el
        target = ''
        for x in range(len(control_list)):
            if self.get_axtype(control_list[x]) == 'close button':
                target = x
                break
        if target == '':
            logger("can't find close button")
            return False
        if self.tap_element(control_list[target]):
            time.sleep(1)
            # verify if dlg closed
            if self.get_dialogue_child_list(axtitle) is False:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap element fail')
        return False
# title designer - border

    def get_titledesigner_border_list(self):
        """
        cell el -> control list(this function)
        :param option:
        :return:
        """
        cell_el = self.get_titledesigner_object_cell_el('Size:')
        if cell_el is False:
            logger('get cell_el fail')
            return False
        control_list = self.get_child_wnd(cell_el)
        if control_list is False:
            logger('get control_list fail')
            return False
        logger('Done')
        return control_list

    def adjust_titledesigner_border_size_slider(self, value):
        # get slider el
        control_list = self.get_titledesigner_border_list()
        if control_list is False:
            logger('get control_list fail')
            return False
        slider_size_el = control_list[1]
        if self.adjust_element_slider(slider_size_el, value, min=0, max=10):
            logger('Done')
            return True
        else:
            logger('adjust slider fail')
        return False

    def adjust_titledesigner_border_blur_slider(self, value):
        # get slider el
        control_list = self.get_titledesigner_border_list()
        if control_list is False:
            logger('get control_list fail')
            return False
        slider_size_el = control_list[4]
        if self.adjust_element_slider(slider_size_el, value, min=0, max=20):
            logger('Done')
            return True
        else:
            logger('adjust slider fail')
        return False

    def adjust_titledesigner_border_opacity_slider(self, value):
        # get slider el
        control_list = self.get_titledesigner_border_list()
        if control_list is False:
            logger('get control_list fail')
            return False
        slider_size_el = control_list[7]
        if self.adjust_element_slider(slider_size_el, value):
            logger('Done')
            return True
        else:
            logger('adjust slider fail')
        return False

    def get_color_dialogue_el(self):
        logger('interface: get_color_dialogue_el')
        return self.get_titledesigner_color_dialogue_el()

    def change_color_dialogue_color(self, option, value):
        logger('interface: change_color_dialogue_color')
        return self.change_titledesigner_color_dialogue_color(option, value)

    def close_color_dialogue(self):
        el = self.get_color_dialogue_el()
        if el is False:
            logger('get el fail')
            return False
        parent = self.get_parent_wnd(el)
        if parent is False:
            logger('get parent fail')
            return False
        close_btn = self.search_child_el_by_type(parent, 'close button')
        if close_btn is False:
            logger('get close_btn fail')
            return False
        if self.tap_element(close_btn):
            time.sleep(0.5)
            # verify
            if self.get_color_dialogue_el() is False:
                logger('Done')
                return True
            else:
                logger('verify fail')
                return False
        else:
            logger('tap element fail')
        return False

    def tap_titledesigner_border_uniformcolor_beginwith_btn(self):
        control_list = self.get_titledesigner_border_list()
        if control_list is False:
            logger('get control_list fail')
            return False
        btn_el = control_list[-4]
        if self.tap_element(btn_el):
            # verify
            time.sleep(1)
            if self.get_color_dialogue_el() is not False:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('adjust btn fail')
        return False

# Titledesigner - Shadow
    def get_titledesigner_shadow_list(self):
        """
        cell el -> control list(this function)
        :param option:
        :return:
        """
        cell_el = self.get_titledesigner_object_cell_el('Apply shadow to:')
        if cell_el is False:
            logger('get cell_el fail')
            return False
        control_list = self.get_child_wnd(cell_el)
        if control_list is False:
            logger('get control_list fail')
            return False
        logger('Done')
        return control_list

    def select_titledesigner_shadow_applyshadowto_drop_down_menu(self, option):
        # get element
        control_list = self.get_titledesigner_shadow_list()
        if control_list is False:
            logger('get control_list fail')
            return False
        drop_down_menu_el = control_list[1]
        if self.select_drop_down_list(drop_down_menu_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('select drop down list fail')
        return False

    def adjust_titledesigner_shadow_distance_slider(self, value, tolerance):
        """
        need tolerance bcz the value would be (ex: 5.303501...)
        :param value:
        :param tolerance:
        :return:
        """
        # get slider el
        control_list = self.get_titledesigner_shadow_list()
        if control_list is False:
            logger('get control_list fail')
            return False
        slider_distance_el = control_list[3]
        if self.adjust_element_slider(slider_distance_el, value, tolerance=tolerance):
            logger('Done')
            return True
        else:
            logger('adjust slider fail')
        return False

    def adjust_titledesigner_shadow_blur_slider(self, value):
        """
        :param value:
        :param tolerance:
        :return:
        """
        # get slider el
        control_list = self.get_titledesigner_shadow_list()
        if control_list is False:
            logger('get control_list fail')
            return False
        slider_blur_el = control_list[6]
        if self.adjust_element_slider(slider_blur_el, value, min=0, max=20):
            logger('Done')
            return True
        else:
            logger('adjust slider fail')
        return False


    def adjust_titledesigner_shadow_opacity_slider(self, value):
        """
        :param value:
        :param tolerance:
        :return:
        """
        # get slider el
        control_list = self.get_titledesigner_shadow_list()
        if control_list is False:
            logger('get control_list fail')
            return False
        slider_opacity_el = control_list[9]
        if self.adjust_element_slider(slider_opacity_el, value):
            logger('Done')
            return True
        else:
            logger('adjust slider fail')
        return False

    def tap_titledesigner_shadow_fillshadow_checkbox(self, option):
        """
        :param option:  'on', 'off'
        :return:
        """
        # get slider el
        control_list = self.get_titledesigner_shadow_list()
        if control_list is False:
            logger('get control_list fail')
            return False
        checkbox_el = control_list[-3]
        if self.checkbox_handle(checkbox_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('checkbox handle fail')
        return False

    def tap_titledesigner_shadow_direction(self, direction, ground_truth_folder):
        logger('Interface: tap_titledesigner_shadow_direction')
        return self.tap_pipdesigner_direction(direction, ground_truth_folder)

    def tap_titledesigner_basic_btn(self):
        if self.tap_locator(self.btn_titledesigner_basic):
            # verify
            if self.get_titledesigner_cell_el() is False:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap locator fail')
        return False

    def tap_titledesigner_advanced_btn(self):
        if self.tap_locator(self.btn_titledesigner_advanced):
            # verify
            if self.get_titledesigner_cell_el():
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap locator fail')
        return False

# titledesigner-object settings
    def get_titledesigner_objectsettings_list(self):
        cell_el = self.get_titledesigner_object_cell_el('Position')
        if cell_el is False:
            logger('get cell_el fail')
            return False
        control_list = self.get_child_wnd(cell_el)
        if control_list is False:
            logger('get control_list fail')
            return False
        logger('Done')
        return control_list

    def tap_titledesigner_objectsettings_position_addkeyframe_icon(self):
        control_list = self.get_titledesigner_objectsettings_list()
        if control_list is False:
            logger('get control_list fail')
            return False
        position_addkeyframe_el = control_list[3]
        if self.tap_element(position_addkeyframe_el):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def tap_titledesigner_objectsettings_scale_addkeyframe_icon(self):
        control_list = self.get_titledesigner_objectsettings_list()
        if control_list is False:
            logger('get control_list fail')
            return False
        scale_addkeyframe_el = control_list[19]
        if self.tap_element(scale_addkeyframe_el):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def tap_titledesigner_objectsettings_opacity_addkeyframe_icon(self):
        control_list = self.get_titledesigner_objectsettings_list()
        if control_list is False:
            logger('get control_list fail')
            return False
        opacity_addkeyframe_el = control_list[-10]
        if self.tap_element(opacity_addkeyframe_el):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def tap_titledesigner_objectsettings_rotation_addkeyframe_icon(self):
        control_list = self.get_titledesigner_objectsettings_subcontrol_list("Rotation")
        if control_list is False:
            logger('get control_list fail')
            return False
        rotation_addkeyframe_el = control_list[3]
        if self.tap_element(rotation_addkeyframe_el):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def tap_titledesigner_objectsettings_position_movekeyframe_icon(self, option):
        """
        :param option: "left/right"
        :return:
        """
        control_list = self.get_titledesigner_objectsettings_list()
        if control_list is False:
            logger('get control_list fail')
            return False
        position_movekeyframe_el = ''
        if option == 'left':
            position_movekeyframe_el = control_list[2]
        elif option == 'right':
            position_movekeyframe_el = control_list[4]
        else:
            logger('incorrect parameter')
            return False
        if self.tap_element(position_movekeyframe_el):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def tap_titledesigner_objectsettings_scale_movekeyframe_icon(self, option):
        """
        :param option: "left/right"
        :return:
        """
        control_list = self.get_titledesigner_objectsettings_list()
        if control_list is False:
            logger('get control_list fail')
            return False
        scale_movekeyframe_el = ''
        if option == 'left':
            scale_movekeyframe_el = control_list[18]
        elif option == 'right':
            scale_movekeyframe_el = control_list[20]
        else:
            logger('incorrect parameter')
            return False
        if self.tap_element(scale_movekeyframe_el):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def tap_titledesigner_objectsettings_rotation_movekeyframe_icon(self, option):
        """
        :param option: "left/right"
        :return:
        """
        control_list = self.get_titledesigner_objectsettings_subcontrol_list("Rotation")
        if control_list is False:
            logger('get control_list fail')
            return False
        scale_movekeyframe_el = ''
        if option == 'left':
            scale_movekeyframe_el = control_list[2]
        elif option == 'right':
            scale_movekeyframe_el = control_list[4]
        else:
            logger('incorrect parameter')
            return False
        if self.tap_element(scale_movekeyframe_el):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def get_titledesigner_objectsettings_subcontrol_list(self, subcontrol):
        """
        :param subcontrol: "Position", "Scale", "Opacity", "Rotation"
        :return: after the subcontrol list
        """
        if subcontrol not in ["Position", "Scale", "Opacity", "Rotation"]:
            logger('incorrect parameter')
            return False
        control_list = self.get_titledesigner_objectsettings_list()
        if control_list is False:
            logger('get control_list fail')
            return False
        start_index = ''
        for x in range(len(control_list)):
            try:
                if self.get_axvalue(control_list[x]) == subcontrol:
                    start_index = x
                    break
            except:
                continue
        if start_index == '':
            logger('get start index fail')
            return False
        logger('Done')
        return control_list[start_index:]

    def tap_titledesigner_timecode(self, timecode):
        """
        ex: 00;00;00, 00;01;20, 00;03;10, 00;05;00
        :param timecode:
        :return:
        """
        logger('interface:tap_titledesigner_timecode')
        return self.tap_pipdesigner_timecode(timecode)

    def tick_titledesigner_objectsettings_position_easein_checkbox(self, option):
        control_list = self.get_titledesigner_objectsettings_list()
        if control_list is False:
            logger('get control_list fail')
            return False
        position_easein_el = control_list[9]
        if self.checkbox_handle(position_easein_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('checkbox handle fail')
        return False

    def tick_titledesigner_objectsettings_position_easeout_checkbox(self, option):
        control_list = self.get_titledesigner_objectsettings_list()
        if control_list is False:
            logger('get control_list fail')
            return False
        position_easeout_el = control_list[12]
        if self.checkbox_handle(position_easeout_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('checkbox handle fail')
        return False

    def tick_titledesigner_objectsettings_scale_easein_checkbox(self, option):
        control_list = self.get_titledesigner_objectsettings_list()
        if control_list is False:
            logger('get control_list fail')
            return False
        scale_easein_el = control_list[28]
        if self.checkbox_handle(scale_easein_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('checkbox handle fail')
        return False

    def tick_titledesigner_objectsettings_scale_easeout_checkbox(self, option):
        control_list = self.get_titledesigner_objectsettings_list()
        if control_list is False:
            logger('get control_list fail')
            return False
        scale_easeout_el = control_list[31]
        if self.checkbox_handle(scale_easeout_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('checkbox handle fail')
        return False

    def tick_titledesigner_objectsettings_rotation_easein_checkbox(self, option):
        control_list = self.get_titledesigner_objectsettings_subcontrol_list("Rotation")
        if control_list is False:
            logger('get control_list fail')
            return False
        rotation_easein_el = control_list[6]
        if self.checkbox_handle(rotation_easein_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('checkbox handle fail')
        return False

    def tick_titledesigner_objectsettings_rotation_easeout_checkbox(self, option):
        control_list = self.get_titledesigner_objectsettings_subcontrol_list("Rotation")
        if control_list is False:
            logger('get control_list fail')
            return False
        rotation_easeout_el = control_list[9]
        if self.checkbox_handle(rotation_easeout_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('checkbox handle fail')
        return False

# titledesinger tab
    #old
    '''
    def tap_titledesigner_effect_tab(self):
        if self.tap_locator(self.tab_titledesigner_effect):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False
    '''
    #new
    def tap_titledesigner_animation_tab(self):
        if self.tap_locator(self.tab_titledesigner_animation):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def tap_titledesigner_object_tab(self):
        if self.tap_locator(self.tab_titledesigner_object):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

# titledesigner starting effect
    def get_titledesigner_startingeffect_preset_list(self):
        """
        collection -> section -> groups(this function, return list)
        :param option:
        :return:
        """
        scroll_area_el = self.get_titledesigner_object_scroll_area_el('Effect:')
        if scroll_area_el is False:
            logger('get scroll_area_el fail')
            return False
        collection_el = self.search_child_el_by_role(scroll_area_el, 'AXList')
        if collection_el is False:
            logger('get collection_el fail')
            return False
        section_el = self.search_child_el_by_role(collection_el, 'AXList')
        if section_el is False:
            logger('get section_el fail')
            return False
        preset_list = self.get_child_wnd(section_el)
        if preset_list is False:
            logger('get preset_list fail')
            return False
        logger('Done')
        return preset_list

    def select_titledesigner_startingeffect_preset(self, option):
        """
        option: 1, 2, 3, 4
        :param option:
        :return:
        Note: verify in test case
        """
        preset_list = self.get_titledesigner_startingeffect_preset_list()
        if preset_list is False:
            logger('get preset_list fail')
            return False
        if self.tap_element(preset_list[option - 1]):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def select_titledesigner_endingeffect_preset(self, option):
        logger('Interface: select_titledesigner_endingeffect_preset')
        return self.select_titledesigner_startingeffect_preset(option)

    def tap_titledesigner_cell_keyframe_control(self, option, icon):
        """
        :param option: Position/Scale...
        :param icon: 'left/keyframe/right'
        :return:
        """
        outline_list = self.get_titledesigner_cell_list()
        if outline_list is False:
            logger('get cell_list fail')
            return False
        # search correct cell
        target = ''
        for x in range(len(outline_list)):
            try:
                cell_list = self.get_child_wnd(outline_list[x])
                if cell_list is False:
                    continue
                cell_child_list = self.get_child_wnd(cell_list[0])
                if cell_child_list is False:
                    continue
                if self.get_axvalue(cell_child_list[0]) == option:
                    target = x
                    break
            except:
                continue
        if target == '':
            logger('get target fail')
            return False
        target_control_list = self.get_child_wnd(self.get_child_wnd(outline_list[target])[0])
        if target_control_list is False:
            logger('get target_control_list fail')
            return False
        # start to control
        if icon not in ['left', 'keyframe', 'right']:
            logger('incorrect parameter')
            return False
        if icon == 'left':
            if self.tap_element(target_control_list[1]):
                logger('Done')
                return True
            else:
                logger('tap element fail(1)')
        elif icon == 'keyframe':
            if self.tap_element(target_control_list[2]):
                logger('Done')
                return True
            else:
                logger('tap element fail(2)')
        elif icon == 'right':
            if self.tap_element(target_control_list[3]):
                logger('Done')
                return True
            else:
                logger('tap element fail(3)')
        else:
            logger('unexpected error')
        return False

    def tap_titledesigner_play_icon(self):
        if self.tap_locator(self.icon_titledesigner_play):
            time.sleep(3)  # for download audio
            # verify
            if self.search_el(self.icon_titledesigner_pause) is not None:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap locator fail')
        return False

    def tap_titledesigner_pause_icon(self):
        if self.tap_locator(self.icon_titledesigner_pause):
            # verify
            if self.search_el(self.icon_titledesigner_play) is not None:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap locator fail')
        return False

    def tap_titledesigner_stop_icon(self):
        if self.tap_locator(self.icon_titledesigner_stop):
            # verify
            if self.search_el(self.icon_titledesigner_play) is not None:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap locator fail')
        return False

    def verify_titledesigner_playback(self, verify_short_content=0):
        """
        for case, only playback & stop
        if verify short content = 1, doesn't check pause case
        :return:
        """
        if self.tap_titledesigner_play_icon():
            if self.tap_titledesigner_stop_icon():
                logger('Done')
                return True
            else:
                logger('tap stop fail')
        else:
            if verify_short_content == 1:
                if self.tap_titledesigner_stop_icon():
                    logger('Done')
                    return True
                else:
                    logger('tap stop fail')
            else:
                logger('tap play fail')
        return False

    def adjust_titledesigner_resize(self, ground_truth_folder):
        """
        search left-top icon
        """
        pos = self.search_pos_from_image('titledesigner_resize.png', ground_truth_folder=ground_truth_folder)
        if pos is False:
            logger('search pos from image fail')
            return False
        if self.drag_mouse(pos, (pos[0], pos[1] - 20)):
            logger('Done')
            return True
        else:
            logger('drag pos fail')
        return False

    def adjust_titledesigner_move(self, ground_truth_folder):
        """
        search left-top icon
        """
        pos = self.search_pos_from_image('titledesigner_move.png', ground_truth_folder=ground_truth_folder)
        if pos is False:
            logger('search pos from image fail')
            return False
        if self.drag_mouse(pos, (pos[0] - 10, pos[1] - 10)):
            logger('Done')
            return True
        else:
            logger('drag pos fail')
        return False

    def adjust_titledesigner_rotate(self, ground_truth_folder):
        """
        search left-top icon
        """
        pos = self.search_pos_from_image('titledesigner_rotate.png', ground_truth_folder=ground_truth_folder)
        if pos is False:
            logger('search pos from image fail')
            return False
        if self.drag_mouse(pos, (pos[0] - 10, pos[1])):
            logger('Done')
            return True
        else:
            logger('drag pos fail')
        return False
# tip area(mid control edit area)
    def tap_tipsarea_tool_btn(self, option):
        """
        :param option: "Mask Designer"
        :return:
        """
        if self.select_drop_down_list(self.btn_tipsarea_tool, option, need_verify=0):
            logger('Done')
            return True
        else:
            logger('select drop down list fail')
        return False

    def tap_tipsarea_video_collage_btn(self):
        if self.tap_locator(self.btn_tipsarea_video_collage):
            time.sleep(1)
            # verify
            if self.get_videocollagedesigner_frame_el() is not False:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap locator fail')
        return False


# mask designer
    def is_maskdesigner_popup(self, mask_name='Default'):
        """
        if has pip_name, need to change search locator
        :param pip_name:
        :return:
        """
        # str_pipdesigner_default = {'AXValue': 'PiP Designer  |  Default', 'AXRole': 'AXStaticText'}
        if mask_name == 'Default':
            locator = self.str_pipdesigner_default
        else:
            locator = {'AXValue': f'Mask Designer  |  {mask_name}', 'AXRole': 'AXStaticText'}
        if self.search_el(locator) is not None:
            logger('Done')
            return True
        else:
            logger('pip designer does not pop up')
        return False

    def get_maskdesigner_control_list(self):
        """
        Structure: dialogue -> control list(this function) -> split group/button/text...etc
        :return:
        """
        el = self.search_el(self.dlg_maskdesigner)
        if el is False:
            logger('get el fail')
            return False
        control_list = self.get_child_wnd(el)
        if control_list is False:
            logger('get control_list fail')
            return False
        logger('Done')
        return control_list

    def get_maskdesigner_leftgroup_control_list(self):
        """
        structure: control_list -(index 0)-> split group -> leftgroup('AXGroup') -> scroll area -> control list(this function)
        left group control lislt: 0: outline, 1:scroll bar
        :return:
        """
        control_list = self.get_maskdesigner_control_list()
        if control_list is False:
            logger('get control list fail')
            return False
        split_group = self.search_child_el_by_role(control_list[0], 'AXGroup')
        if split_group is False:
            logger('get split_group fail')
            return False
        scroll_area_el = self.search_child_el_by_role(split_group, 'AXScrollArea')
        if scroll_area_el is False:
            logger('get scroll_area_el fail')
            return False
        left_control_list = self.get_child_wnd(scroll_area_el)
        if left_control_list is False:
            logger('get left_control_list fail')
            return False
        logger('Done')
        return left_control_list

    def get_maskdesigner_leftgroup_outlinerow_list(self):
        """
        structure: scrollarea -> outline -> outline row(this function)
        :return:
        """
        outline_el = self.get_maskdesigner_leftgroup_control_list()[0]
        if outline_el is False:
            logger('get outline_el fail')
            return False
        outlinerow_list = self.get_child_wnd(outline_el)
        if outlinerow_list is False:
            logger('get outlinerow_list fail')
            return False
        logger('Done')
        return outlinerow_list

    def get_maskdesigner_leftgroup_scroll_el(self):
        """
        structure: scrollarea -> scrollbar(this function)
        :return:
        """
        scrollbar_el = self.get_maskdesigner_leftgroup_control_list()[1]
        if scrollbar_el is False:
            logger('get scrollbar_el fail')
            return False
        logger('Done')
        return scrollbar_el

    def scroll_maskdesigner_leftgroup_scrollbar(self, option):
        scrollbar_el = self.get_maskdesigner_leftgroup_scroll_el()
        if scrollbar_el is False:
            logger('get scrollbar_el fail')
            return False
        if self.scroll_scrollbar(scrollbar_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('scroll fail')
        return False


    def get_maskdesigner_rightgroup_control_list(self):
        """
        structure: control_list -(index 0)-> split group -> righttgroup('AXSplitGroup') -> control list(this function)
        left group control lislt: 0: outline, 1:scroll bar
        :return:
        """
        control_list = self.get_maskdesigner_control_list()
        if control_list is False:
            logger('get control list fail')
            return False
        split_group = self.search_child_el_by_role(control_list[0], 'AXSplitGroup')
        if split_group is False:
            logger('get split_group fail')
            return False
        right_control_list = self.get_child_wnd(split_group)
        if right_control_list is False:
            logger('get right_control_list fail')
            return False
        logger('Done')
        return right_control_list

    def get_maskdesigner_left_cell(self, option):
        """
        Structure: outlinerow -> cell -> text/triangle
        :param option: "Mask Properties", "Object Settings",  contents: 'All Masks", "Default Masks", "Custom Masks", "Position"
        :return:
        """
        if option not in ["Mask Properties", "Object Settings", "All Masks","Default Masks", "Custom Masks", "Position"]:
            logger('incorrect parameter')
            return False
        outline_list = self.get_maskdesigner_leftgroup_outlinerow_list()
        if outline_list is False:
            logger('get outline_list fail')
            return False
        target = ''
        for x in range(len(outline_list)):
            cell = self.get_child_wnd(outline_list[x])
            if cell is False:
                continue
            cell_child_list = self.get_child_wnd(cell[0])
            if cell_child_list is False:
                continue
            if self.get_axvalue(cell_child_list[0]) == option:
                target = x
                break
            if self.get_axtitle(cell_child_list[0]) == option:
                target = x
                break
        if target == '':
            logger('get target fail')
            return False
        logger('Done')
        return self.get_child_wnd(outline_list[target])[0]

    def express_fold_maskdesigner_option(self, category, option):
        """
        :param category:
        :return:
        """
        cell_el = self.get_maskdesigner_left_cell(category)
        if cell_el is False:
            logger('get cell el fail')
            return False
        # index 1 is triangle icon
        triangle_el = self.search_child_el_by_role(cell_el, 'AXDisclosureTriangle')
        if triangle_el is False:
            logger('get triangle_el fail')
            return False
        if self.checkbox_handle(triangle_el, option, element_mode=1):
            time.sleep(1)
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def select_maskdesigner_maskproperties_drop_down_menu(self, option):
        # get drop-down el
        cell_el = self.get_maskdesigner_left_cell('All Masks')
        if cell_el is False:
            cell_el = self.get_maskdesigner_left_cell('Default Masks')
            if cell_el is False:
                cell_el = self.get_maskdesigner_left_cell('Custom Masks')
                if cell_el is False:
                    logger('get cell_el fail')
                    return False
        drop_down_el = self.get_child_wnd(cell_el)
        if drop_down_el is False:
            logger('get drop_down_el fail')
            return False
        drop_down_el = drop_down_el[0]
        if self.select_drop_down_list(drop_down_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('drop down menu fail')
        return False

    def get_maskdesigner_preview_area(self):
        right_group_control_list = self.get_maskdesigner_rightgroup_control_list()
        if right_group_control_list is False:
            logger('get right_group_control_list fail')
            return False
        area_el = right_group_control_list[1]
        pos = self.get_pos(area_el)
        if pos is False:
            logger('get pos fail')
            return False
        logger(f'Done. {pos}')
        return pos

    def select_maskdesigner_maskproperties_mask(self, option):
        """
        :param option: index 1, 2, 3, 4
        :return:
        """
        option -= 1
        cell_el = self.get_maskdesigner_left_cell('All Masks')
        if cell_el is False:
            cell_el = self.get_maskdesigner_left_cell('Default Masks')
            if cell_el is False:
                cell_el = self.get_maskdesigner_left_cell('Custom Masks')
                if cell_el is False:
                    logger('get cell_el fail')
                    return False
        scroll_area = self.search_child_el_by_role(cell_el, 'AXScrollArea')
        if scroll_area is False:
            logger('get scroll_area fail')
            return False
        collection_el = self.search_child_el_by_role(scroll_area, 'AXList')
        if collection_el is False:
            logger('get collection_el fail')
            return False
        section_el = self.search_child_el_by_role(collection_el, 'AXList')
        if section_el is False:
            logger('get section_el fail')
            return False
        option_list = self.get_child_wnd(section_el)
        if option_list is False:
            logger('get option_list fail')
            return False
        # select option
        if self.tap_element(option_list[option]):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def tap_maskdesigner_maskproperties_importimage_btn(self, filename):
        cell_el = self.get_maskdesigner_left_cell('All Masks')
        if cell_el is False:
            cell_el = self.get_maskdesigner_left_cell('Default Masks')
            if cell_el is False:
                cell_el = self.get_maskdesigner_left_cell('Custom Masks')
                if cell_el is False:
                    logger('get cell_el fail')
                    return False
        control_list = self.get_child_wnd(cell_el)
        if control_list is False:
            logger('get control list fail')
            return False
        import_btn_el = control_list[2]
        if self.tap_element(import_btn_el):
            if self.import_media(filename, wait_menubar=0):
                logger('Done')
                return True
            else:
                logger('import fail')
        else:
            logger('tap element fail')
        return False

    def tap_maskdesigner_maskproperties_invertmask_checkbox(self, option):
        cell_el = self.get_maskdesigner_left_cell('All Masks')
        if cell_el is False:
            cell_el = self.get_maskdesigner_left_cell('Default Masks')
            if cell_el is False:
                cell_el = self.get_maskdesigner_left_cell('Custom Masks')
                if cell_el is False:
                    logger('get cell_el fail')
                    return False
        control_list = self.get_child_wnd(cell_el)
        if control_list is False:
            logger('get control list fail')
            return False
        invert_el = control_list[3]
        if self.checkbox_handle(invert_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('checkbox handle fail')
        return False

    def adjust_maskdesigner_maskproperties_featherradius_slider(self, value):
        cell_el = self.get_maskdesigner_left_cell('All Masks')
        if cell_el is False:
            cell_el = self.get_maskdesigner_left_cell('Default Masks')
            if cell_el is False:
                cell_el = self.get_maskdesigner_left_cell('Custom Masks')
                if cell_el is False:
                    logger('get cell_el fail')
                    return False
        slider_el = self.search_child_el_by_role(cell_el, 'AXSlider')
        if slider_el is False:
            logger('get control list fail')
            return False
        if self.adjust_element_slider(slider_el, value, min=0, max=10):
            logger('Done')
            return True
        else:
            logger('adjust slider fail')
        return False

    def input_maskdesigner_objectsettings_position_x(self, value):
        cell_el = self.get_maskdesigner_left_cell('Position')
        if cell_el is False:
            logger('get cell_el fail')
            return False
        control_list = self.get_child_wnd(cell_el)
        if control_list is False:
            logger('get control_list fail')
            return False
        x_text_column_group = control_list[2]
        x_text_column_el = self.search_child_el_by_role(x_text_column_group, 'AXTextField')
        if self.set_text_on_element(x_text_column_el, value, double_click=1):
            logger('Done')
            return True
        else:
            logger('set text fail')
        return False

    def adjust_maskdesigner_objectsettings_scalewidth_slider(self, value):
        cell_el = self.get_maskdesigner_left_cell('Position')
        if cell_el is False:
            logger('get cell_el fail')
            return False
        slider_list = self.search_child_el_by_role(cell_el, 'AXSlider')
        if slider_list is False:
            logger('get slider list fail')
            return False
        scalewidth_el = slider_list[0]
        tolerance = [value - 0.1, value + 0.1]
        if self.adjust_element_slider(scalewidth_el, value, min=0.001, max=4.500, tolerance=tolerance):
            logger('Done')
            return True
        else:
            logger('adjust element slider fail')
        return False

    def adjust_maskdesigner_objectsettings_scaleheight_slider(self, value):
        cell_el = self.get_maskdesigner_left_cell('Position')
        if cell_el is False:
            logger('get cell_el fail')
            return False
        slider_list = self.search_child_el_by_role(cell_el, 'AXSlider')
        if slider_list is False:
            logger('get slider list fail')
            return False
        scalewidth_el = slider_list[1]
        tolerance = [value - 0.1, value + 0.1]
        if self.adjust_element_slider(scalewidth_el, value, min=0.001, max=6.000, tolerance=tolerance):
            logger('Done')
            return True
        else:
            logger('adjust element slider fail')
        return False

    def adjust_maskdesigner_objectsettings_opacity_slider(self, value):
        cell_el = self.get_maskdesigner_left_cell('Position')
        if cell_el is False:
            logger('get cell_el fail')
            return False
        slider_list = self.search_child_el_by_role(cell_el, 'AXSlider')
        if slider_list is False:
            logger('get slider list fail')
            return False
        scalewidth_el = slider_list[2]
        tolerance = [value - 1, value + 1]
        if self.adjust_element_slider(scalewidth_el, value, min=0, max=100, tolerance=tolerance):
            logger('Done')
            return True
        else:
            logger('adjust element slider fail')
        return False

    def input_maskdesigner_objectsettings_rotation_x(self, value):
        cell_el = self.get_maskdesigner_left_cell('Position')
        if cell_el is False:
            logger('get cell_el fail')
            return False
        control_list = self.get_child_wnd(cell_el)
        if control_list is False:
            logger('get control_list fail')
            return False
        rotation_column_group = control_list[-4]
        rotation_column_el = self.search_child_el_by_role(rotation_column_group, 'AXTextField')
        if self.set_text_on_element(rotation_column_el, value, double_click=1):
            logger('Done')
            return True
        else:
            logger('set text fail')
        return False

    def adjust_maskdesigner_resize(self, ground_truth_folder):
        """
        search mid icon
        """
        pos = self.search_pos_from_image('maskdesigner_resize.png', ground_truth_folder=ground_truth_folder)
        if pos is False:
            logger('search pos from image fail')
            return False
        if self.drag_mouse(pos, (pos[0] + 20, pos[1] - 20)):
            logger('Done')
            return True
        else:
            logger('drag pos fail')
        return False

    def adjust_maskdesigner_rotate(self, ground_truth_folder):
        """
        search mid icon
        """
        pos = self.search_pos_from_image('maskdesigner_rotate.png', ground_truth_folder=ground_truth_folder)
        if pos is False:
            logger('search pos from image fail')
            return False
        if self.drag_mouse((pos[0], pos[1]), (pos[0] + 10, pos[1] + 20)):
            logger('Done')
            return True
        else:
            logger('drag pos fail')
        return False


    def adjust_maskdesigner_move(self, ground_truth_folder):
        """
        search mid icon
        """
        pos = self.search_pos_from_image('maskdesigner_move.png', ground_truth_folder=ground_truth_folder)
        if pos is False:
            logger('search pos from image fail')
            return False
        if self.drag_mouse(pos, (pos[0] - 10, pos[1])):
            logger('Done')
            return True
        else:
            logger('drag pos fail')
        return False

    def tap_maskdesigner_play_icon(self):
        # axidentifier is the same as mask tab, so search 2nd
        el = self.search_el(self.icon_maskdesigner_play)
        if el is None:
            logger('search all el fail')
            return False
        if self.tap_element(el):
            time.sleep(3)  # for download audio
            # verify
            if self.search_el(self.icon_maskdesigner_pause) is not None:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap locator fail')
        return False

    def tap_maskdesigner_stop_icon(self):
        if self.tap_locator(self.icon_maskdesigner_stop):
            # verify
            if self.search_el(self.icon_maskdesigner_play) is not None:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap locator fail')
        return False

    def verify_maskdesigner_playback(self, verify_short_content=0):
        """
        for case, only playback & stop
        if verify short content = 1, doesn't check pause case
        :return:
        """
        if self.tap_maskdesigner_play_icon():
            if self.tap_maskdesigner_stop_icon():
                logger('Done')
                return True
            else:
                logger('tap stop fail')
        else:
            if verify_short_content == 1:
                if self.tap_maskdesigner_stop_icon():
                    logger('Done')
                    return True
                else:
                    logger('tap stop fail')
            else:
                logger('tap play fail')
        return False

# video collage designer
    def get_videocollagedesinger_dlg_el(self):
        """
        Top element
        :return:
        """
        el = self.search_el(self.dlg_video_collage_designer)
        if el is not None:
            logger('Done')
            return el
        else:
            logger('search el fail')
        return False

    def get_videocollagedesigner_frame_el(self):
        """
        split group(this function)
        :return:
        """
        el = self.get_videocollagedesinger_dlg_el()
        if el is False:
            logger('search el fail')
            return False
        split_group_el = self.search_child_el_by_role(el, 'AXSplitGroup')
        if split_group_el is False:
            logger('search split_group_el fail')
            return False
        logger('Done')
        return split_group_el

    def is_open_dlg_popup(self):
        locator = {'AXTitle': 'Open', 'AXRole': 'AXWindow'}
        if self.search_el(locator) is not None:
            logger('Done')
            return True
        else:
            logger('search el fail')
        return False

    def is_saveas_dlg_popup(self):
        locator = {'AXTitle': 'Save As', 'AXRole': 'AXWindow'}
        if self.search_el(locator) is not None:
            logger('Done')
            return True
        else:
            logger('search el fail')
        return False

    def tap_videocollagedesigner_importmedia_btn(self):
        frame_el = self.get_videocollagedesigner_frame_el()
        if frame_el is False:
            logger('get frame el fail')
            return False
        importmedia_btn = self.search_child_el_by_title(frame_el, 'Import Media')
        if importmedia_btn is False:
            logger('get importmedia_btn fail')
            return False
        if self.tap_element(importmedia_btn):
            # verify
            time.sleep(1)
            if self.is_open_dlg_popup():
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap element fail')
        return False

    def select_videocollagedesigner_media_drop_down_menu(self, option):
        drop_down_el = self.search_el(self.drop_down_menu_video_collage_designer_media)
        if drop_down_el is False:
            logger('get drop_down_el fail')
            return False
        logger(drop_down_el)
        if self.select_drop_down_list(drop_down_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('select drop down menu fail')
        return False

    def get_videocollagedesigner_leftscroll_area_el(self):
        frame_el = self.get_videocollagedesigner_frame_el()
        if frame_el is False:
            logger('get frame el fail')
            return False
        scrollarea_list = self.search_child_el_by_role(frame_el, 'AXScrollArea')
        # left/top/right
        if scrollarea_list is not False:
            logger('Done')
            return scrollarea_list[0]
        else:
            logger('get scrollarea list fail')
        return False

    def get_videocollagedesigner_topscroll_area_el(self):
        frame_el = self.get_videocollagedesigner_frame_el()
        if frame_el is False:
            logger('get frame el fail')
            return False
        scrollarea_list = self.search_child_el_by_role(frame_el, 'AXScrollArea')
        # left/top/right
        if scrollarea_list is not False:
            logger('Done')
            return scrollarea_list[1]
        else:
            logger('get scrollarea list fail')
        return False

    def get_videocollagedesigner_rightscroll_area_el(self):
        frame_el = self.get_videocollagedesigner_frame_el()
        if frame_el is False:
            logger('get frame el fail')
            return False
        scrollarea_list = self.search_child_el_by_role(frame_el, 'AXScrollArea')
        # left/top/right
        if scrollarea_list is not False:
            logger('Done')
            return scrollarea_list[2]
        else:
            logger('get scrollarea list fail')
        return False

    def select_videocollagedesigner_left_content(self, option):
        """
        option: 1, 2, 3, 4...
        structure: scrollarea -> collection -> section -> groups(this function)
        :param option:
        :return:
        """
        scroll_area = self.get_videocollagedesigner_leftscroll_area_el()
        if scroll_area is False:
            logger('get scroll_area fail')
            return False
        collection_el = self.search_child_el_by_role(scroll_area, 'AXList')
        if collection_el is False:
            logger('get collection_el fail')
            return False
        section_el = self.search_child_el_by_role(collection_el, 'AXList')
        if section_el is False:
            logger('get section_el fail')
            return False
        group_list = self.get_child_wnd(section_el)
        if group_list is False:
            logger('get group_list fail')
            return False
        if self.tap_element(group_list[option - 1]):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def tap_videocollagedesigner_autofill_btn(self):
        if self.tap_locator(self.btn_video_collage_designer_auto_fill):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def get_videocollagedesigner_playback_slider_pos(self):
        frame_el = self.get_videocollagedesigner_frame_el()
        if frame_el is False:
            logger('get frame el fail')
            return False
        slider_el = self.search_child_el_by_role(frame_el, 'AXSlider')
        if slider_el is False:
            logger('get slider_el fail')
            return False
        if type(slider_el) is list:
            slider_el = slider_el[-1]
        pos = self.get_pos(slider_el)
        if pos is not False:
            logger(f'Done. {pos}')
            return pos
        else:
            logger('get pos fail')
        return False

    def get_videocollagedesigner_spliter_pos(self):
        frame_el = self.get_videocollagedesigner_frame_el()
        if frame_el is False:
            logger('get frame el fail')
            return False
        slider_el = self.search_child_el_by_role(frame_el, 'AXSplitter')
        if slider_el is False:
            logger('get slider_el fail')
            return False
        pos = self.get_pos(slider_el)
        if pos is not False:
            logger(f'Done. {pos}')
            return pos
        else:
            logger('get pos fail')
        return False

    def get_videocollagedesigner_rightscroll_area_pos(self):
        area_el = self.get_videocollagedesigner_rightscroll_area_el()
        if area_el is False:
            logger('get area_el fail')
            return False
        pos = self.get_pos(area_el)
        if pos is not False:
            logger(f'Done. {pos}')
            return pos
        else:
            logger('get pos fail')
        return False

    def get_videocollagedesigner_preview_area(self):
        """
        get spliter pos, playback slider pos, right group pos
        :return:
        """
        spliter_pos = self.get_videocollagedesigner_spliter_pos()
        if spliter_pos is False:
            logger('get spliter_pos fail')
            return False
        slider_pos = self.get_videocollagedesigner_playback_slider_pos()
        if slider_pos is False:
            logger('get slider_pos fail')
            return False
        rightgroup_pos = self.get_videocollagedesigner_rightscroll_area_pos()
        if rightgroup_pos is False:
            logger('get rightgroup_pos fail')
            return False
        x = spliter_pos[0] + spliter_pos[2] + 2
        y = rightgroup_pos[1]
        dx = rightgroup_pos[0] - (spliter_pos[0] + spliter_pos[2])
        dy = slider_pos[1] - rightgroup_pos[1]
        pos = (x, y, dx, dy)
        logger(f'Done. {pos}')
        return pos

    def select_videocollagedesigner_top_layout(self, option):
        """
        option: 1(DZ), 2, 3, 4...
        structure: scrollarea -> collection -> section -> groups(this function)
        :param option:
        :return:
        """
        scroll_area = self.get_videocollagedesigner_topscroll_area_el()
        if scroll_area is False:
            logger('get scroll_area fail')
            return False
        collection_el = self.search_child_el_by_role(scroll_area, 'AXList')
        if collection_el is False:
            logger('get collection_el fail')
            return False
        section_el = self.search_child_el_by_role(collection_el, 'AXList')
        if section_el is False:
            logger('get section_el fail')
            return False
        group_list = self.get_child_wnd(section_el)
        if group_list is False:
            logger('get group_list fail')
            return False
        if self.tap_element(group_list[option - 1]):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def get_videocollagedesigner_content_name(self, index=1):
        """
        index: 1, 2, 3, 4...
        structure: scrollarea -> collection -> section -> groups -> AXStaticText(this function)
        :param index:
        :return:
        """
        scroll_area = self.get_videocollagedesigner_leftscroll_area_el()
        if scroll_area is False:
            logger('get scroll_area fail')
            return False
        collection_el = self.search_child_el_by_role(scroll_area, 'AXList')
        if collection_el is False:
            logger('get collection_el fail')
            return False
        section_el = self.search_child_el_by_role(collection_el, 'AXList')
        if section_el is False:
            logger('get section_el fail')
            return False
        group_list = self.get_child_wnd(section_el)
        if group_list is False:
            logger('get group_list fail')
            return False
        target_group = group_list[index - 1]
        # get axstatictext
        text_el = self.search_child_el_by_role(target_group, 'AXStaticText')
        if text_el is False:
            logger('get text_el fail')
            return False
        # get value
        text = self.get_axvalue(text_el)
        if text is not False:
            logger(f'Done. ({text})')
            return text
        else:
            logger('get axvalue fail')
        return False

    def get_videocollagedesigner_content_pos(self, index=1):
        """
        index: 1, 2, 3, 4...
        get mid pos (x, y)
        structure: scrollarea -> collection -> section -> groups (get its pos)
        :param index:
        :return:
        """
        scroll_area = self.get_videocollagedesigner_leftscroll_area_el()
        if scroll_area is False:
            logger('get scroll_area fail')
            return False
        collection_el = self.search_child_el_by_role(scroll_area, 'AXList')
        if collection_el is False:
            logger('get collection_el fail')
            return False
        section_el = self.search_child_el_by_role(collection_el, 'AXList')
        if section_el is False:
            logger('get section_el fail')
            return False
        group_list = self.get_child_wnd(section_el)
        if group_list is False:
            logger('get group_list fail')
            return False
        target_group = group_list[index - 1]
        # get pos
        pos = self.get_mid_pos(target_group)
        if pos is False:
            logger('get pos fail')
            return False
        logger(f'Done. {pos}')
        return pos

    def drag_videocollagedesigner_to_layout(self, index, pos=None):
        """
        :param index: 1, 2, 3, 4, ...
        :param pos: None(hardcode, or pos)
        :return:
        """
        # get preview area pos
        preview_area = self.get_videocollagedesigner_preview_area()
        if preview_area is False:
            logger('get preview_area fail')
            return False
        # get content pos
        content_pos = self.get_videocollagedesigner_content_pos(index)
        if content_pos is False:
            logger('get content_pos fail')
            return False
        destination = (preview_area[0] + preview_area[2] / 3, preview_area[1] + preview_area[3] / 3)
        if pos is not None:
            destination = pos
        # start to drag
        if self.drag_mouse(content_pos, destination):
            logger('Done')
            return True
        else:
            logger('drag mouse fail')
        return False

    def del_videocollagedesigner_from_layout(self, pos=None):
        """
        :param
        pos: None(hardcode, or pos)
        :return:
        """
        # get preview area pos
        preview_area = self.get_videocollagedesigner_preview_area()
        if preview_area is False:
            logger('get preview_area fail')
            return False
        start_pos = (int(preview_area[0] + preview_area[2] / 3), int(preview_area[1] + preview_area[3] / 3))
        destination = (int(preview_area[0] + preview_area[2] / 2), int(preview_area[1] + preview_area[3] / 8))
        if pos is not None:
            start_pos = pos
        # start to drag
        if self.drag_mouse(start_pos, destination):
            logger('Done')
            return True
        else:
            logger('drag mouse fail')
        return False

    def hover_videocollagedesigner_mouse_on_layout(self, pos=None):
        target_pos = ''
        preview_area = self.get_videocollagedesigner_preview_area()
        if preview_area is False:
            logger('get preview_area fail')
            return False
        target_pos = (int(preview_area[0] + preview_area[2] / 3), int(preview_area[1] + preview_area[3] / 3))
        if pos is not None:
            target_pos = pos
        logger(target_pos)
        if self.move_mouse(target_pos) and \
                self.click():
            logger('Done')
            return True
        else:
            logger('move mouse fail')
        return False

    def move_videocollagedesigner_reposition(self, search_text, pos=None, destination=None):
        """
        move layout video, search_text: search time code position (ex: '00:00:07:00')
        :param pos: if None, search timecode to move
        :param destination:
        :return:
        """
        start_pos = ''
        destination_pos = ''
        if pos is None:
            pos = self.search_text_position(search_text, mouse_move=0)
            if pos is False:
                logger('get pos fail')
                return False
        start_pos = pos
        destination_pos = (pos[0], pos[1] + 10)
        if pos is not None:
            start_pos = pos
        if destination is not None:
            destination_pos = destination
        # start to move
        if self.drag_mouse(start_pos, destination_pos):
            logger('Done')
            return True
        else:
            logger('drag fail')
        return False

    def adjust_videocollagedesigner_zoom(self, ground_truth_folder):
        pos = self.search_pos_from_image('videocollagedesigner_zoom.png', ground_truth_folder=ground_truth_folder, mouse_move=0)
        if pos is False:
            logger('search pos from image fail')
            return False
        if self.drag_mouse(pos, (pos[0] + 10, pos[1])):
            logger('Done')
            return True
        else:
            logger('drag pos fail')
        return False

    def click_videocollagedesigner_empty_position(self, pos=None):
        target_pos = ''
        preview_area = self.get_videocollagedesigner_preview_area()
        if preview_area is False:
            logger('get preview_area fail')
            return False
        target_pos = (int(preview_area[0] + preview_area[2] / 2), int(preview_area[1] + preview_area[3] / 8))
        if pos is not None:
            target_pos = pos
        if self.click_mouse(target_pos):
            logger('Done')
            return True
        else:
            logger('click mouse fail')
        return False

# duration settings dialogue
    def get_durationsettings_dlg_el(self):
        el = self.search_el(self.dlg_duration_settings)
        if el is not None:
            logger('Done')
            return el
        else:
            logger('get el fail')
        return False

    def get_durationsettings_dlg_control_list(self):
        """
        structure: dialogue -> group -> controlist(this function)
        :return:
        """
        dlg_el = self.get_durationsettings_dlg_el()
        if dlg_el is False:
            logger('get dlg_el fail')
            return False
        group_el = self.search_child_el_by_role(dlg_el, 'AXGroup')
        if group_el is False:
            logger('get group_el fail')
            return False
        control_list = self.get_child_wnd(group_el)
        if control_list is False:
            logger('get control_list fail')
            return False
        logger('Done')
        return control_list

    def get_durationsettings_dlg_timecode(self):
        control_list = self.get_durationsettings_dlg_control_list()
        if control_list is False:
            logger('get control_list fail')
            return False
        timecode = self.get_axvalue(control_list[0])
        if timecode is not False:
            logger(f'Done. ({timecode})')
            return timecode
        else:
            logger('get timecode fail')
        return False

    def tap_durationsettings_dlg_arrow_icon(self, option):
        control_list = self.get_durationsettings_dlg_control_list()
        if control_list is False:
            logger('get control_list fail')
            return False
        if option == 'up':
            if self.tap_element(control_list[1]):
                logger('Done')
                return True
            else:
                logger('tap element fail(1)')
        elif option == 'down':
            if self.tap_element(control_list[2]):
                logger('Done')
                return True
            else:
                logger('tap element fail(2)')
        else:
            logger('Incorrect parameter')
        return False

    def tap_videocollagedesigner_durationsettings_icon(self, ground_truth_folder):
        pos = self.search_pos_from_image('videocollagedesigner_durationsettings.png', ground_truth_folder=ground_truth_folder, mouse_move=0)
        if pos is False:
            logger('search pos from image fail')
            return False
        if self.click_mouse(pos):
            time.sleep(1)
            # verify
            if self.get_durationsettings_dlg_el() is not False:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap pos fail')
        return False

    def open_videocollagedesigner_trim_dlg(self, pos=None):
        """
        via double clicking to open
        :param pos:
        :return:
        """
        target_pos = ''
        preview_area = self.get_videocollagedesigner_preview_area()
        if preview_area is False:
            logger('get preview_area fail')
            return False
        target_pos = (int(preview_area[0] + preview_area[2] / 2), int(preview_area[1] + preview_area[3] * 4 / 6))
        if pos is not None:
            target_pos = pos
        if self.click_mouse(target_pos, times=2):
            # verify
            time.sleep(1)
            if self.get_trim_dlg_el() is not False:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('click mouse fail')
        return False

# Trim dialogue
    def get_trim_dlg_el(self):
        el = self.search_el(self.dlg_videocollagedesigner_trim)
        if el is not None:
            logger('Done')
            return el
        else:
            logger('search el fail')
        return False

    def get_trim_dlg_group_list(self):
        """
        Group: Slider, Timecode, Duration, In Position, Out Position
        :return:
        """
        el = self.get_trim_dlg_el()
        if el is False:
            logger('get el fail')
            return False
        group_list = self.search_child_el_by_role(el, 'AXGroup')
        if group_list is False:
            logger('get group_list fail')
            return False
        logger('Done')
        return group_list

    def get_trim_dlg_lefttrim_el(self):
        """
        Structure: Group -> unknown -> slider/slider/multitrim(left)/multitrim(right)
        :return:
        """
        group_list = self.get_trim_dlg_group_list()
        if group_list is False:
            logger('get group_list fail')
            return False
        group = group_list[0]
        unknown_el = self.search_child_el_by_role(group, 'AXUnknown')
        if unknown_el is False:
            logger('get unknown_el fail')
            return False
        child_list = self.get_child_wnd(unknown_el)
        if child_list is False:
            logger('get child_list fail')
            return False
        logger('Done')
        return child_list[2]

    def get_trim_dlg_righttrim_el(self):
        """
        Structure: Group -> unknown -> slider/slider/multitrim(left)/multitrim(right)
        :return:
        """
        group_list = self.get_trim_dlg_group_list()
        if group_list is False:
            logger('get group_list fail')
            return False
        group = group_list[0]
        unknown_el = self.search_child_el_by_role(group, 'AXUnknown')
        if unknown_el is False:
            logger('get unknown_el fail')
            return False
        child_list = self.get_child_wnd(unknown_el)
        if child_list is False:
            logger('get child_list fail')
            return False
        logger('Done')
        return child_list[3]

    def adjust_trim_dlg_multitrim_icon(self, option, move=30):
        """
        option: left or right
        :param move: ex: 10 or -10
        :return:
        """
        if option == 'left':
            el = self.get_trim_dlg_lefttrim_el()
            if el is False:
                logger('get el fail(1)')
                return False
            pos = self.get_mid_pos(el)
            if pos is False:
                logger('get pos fail(1)')
                return False
            start_pos = (pos[0], pos[1] - 5)
            destination = (pos[0] + move, pos[1])
            if self.drag_mouse(start_pos, destination):
                logger('Done')
                return True
            else:
                logger('drag mouse fail(1)')
                return False
        elif option == 'right':
            el = self.get_trim_dlg_righttrim_el()
            if el is False:
                logger('get el fail(2)')
                return False
            pos = self.get_mid_pos(el)
            if pos is False:
                logger('get pos fail(2)')
                return False
            start_pos = pos
            destination = (pos[0] + move, pos[1])
            if self.drag_mouse(start_pos, destination):
                logger('Done')
                return True
            else:
                logger('drag mouse fail(2)')
                return False
        else:
            logger('incorrect parameter')
        return False

    def tap_trim_dlg_left_icon(self, ground_truth_folder):
        pos = self.search_pos_from_image('trim_left.png', ground_truth_folder=ground_truth_folder)
        if pos is False:
            logger('search pos from image fail')
            return False
        if self.click_mouse(pos):
            logger('Done')
            return True
        else:
            logger('tap pos fail')
        return False

    def tap_trim_dlg_right_icon(self, ground_truth_folder):
        pos = self.search_pos_from_image('trim_right.png', ground_truth_folder=ground_truth_folder)
        if pos is False:
            logger('search pos from image fail')
            return False
        if self.click_mouse(pos):
            logger('Done')
            return True
        else:
            logger('tap pos fail')
        return False

    def get_trim_dlg_duration_timecode(self):
        group_list = self.get_trim_dlg_group_list()
        if group_list is False:
            logger('get group_list fail')
            return False
        group = group_list[2]
        text_el = self.search_child_el_by_role(group, 'AXStaticText')
        if text_el is False:
            logger('get text_el fail')
            return False
        # get timecode
        text = self.get_axvalue(text_el)
        if text is False:
            logger('get text fail')
            return False
        logger(f'Done. ({text})')
        return text

    def get_trim_dlg_inposition_timecode(self):
        group_list = self.get_trim_dlg_group_list()
        if group_list is False:
            logger('get group_list fail')
            return False
        group = group_list[3]
        text_el = self.search_child_el_by_role(group, 'AXStaticText')
        if text_el is False:
            logger('get text_el fail')
            return False
        # get timecode
        text = self.get_axvalue(text_el)
        if text is False:
            logger('get text fail')
            return False
        logger(f'Done. ({text})')
        return text

    def get_trim_dlg_outposition_timecode(self):
        group_list = self.get_trim_dlg_group_list()
        if group_list is False:
            logger('get group_list fail')
            return False
        group = group_list[3]
        text_el = self.search_child_el_by_role(group, 'AXStaticText')
        if text_el is False:
            logger('get text_el fail')
            return False
        # get timecode
        text = self.get_axvalue(text_el)
        if text is False:
            logger('get text fail')
            return False
        logger(f'Done. ({text})')
        return text

    def tap_videocollagedesigner_mute_icon(self, ground_truth_folder):
        pos = self.search_pos_from_image('videocollagedesigner_mute.png', ground_truth_folder=ground_truth_folder, mouse_move=0)
        if pos is False:
            logger('search pos from image fail')
            return False
        if self.click_mouse(pos):
            # verify
            if self.move_mouse((pos[0] + 40, pos[1])):
                unmute_pos = self.search_pos_from_image('videocollagedesigner_unmute.png',
                                                 ground_truth_folder=ground_truth_folder, mouse_move=0)
                if unmute_pos is not False:
                    logger('Done')
                    return True
                else:
                    logger('verify fail')
            else:
                logger('move mouse fail')
        else:
            logger('tap pos fail')
        return False

    def drag_videocollagedesigner_spliter(self):
        preview_area = self.get_videocollagedesigner_preview_area()
        if preview_area is False:
            logger('get preview_area fail')
            return False

        #old
        '''
        pos_top = self.search_pos_from_image('videocollagedesigner_spliter_top.png', ground_truth_folder=ground_truth_folder)
        if pos_top is False:
            logger('search pos_top from image fail')
            return False
        self.move_mouse(pos_top)
        time.sleep(1)
        pos_bottom = self.search_pos_from_image('videocollagedesigner_spliter_bottom.png', ground_truth_folder=ground_truth_folder)
        if pos_bottom is False:
            logger('search pos_bottom from image fail')
            return False
        self.move_mouse(pos_bottom)
        time.sleep(1)
        '''
        start_pos = (preview_area[0] + preview_area[2] / 2, preview_area[1] - 7 + preview_area[3] / 2)
        destination = (start_pos[0], start_pos[1] - 20)
        if self.click_mouse(start_pos) and \
                self.drag_mouse(start_pos, destination):
            logger('Done')
            return True
        else:
            logger('tap pos fail')
        return False

    def get_videocollagedesigner_rightscroll_slider_list(self):
        """
        index: size/interclipsize
        :return:
        """
        el = self.get_videocollagedesigner_rightscroll_area_el()
        if el is False:
            logger('get el fail')
            return False
        slider_list = self.search_child_el_by_role(el, 'AXSlider')
        if slider_list is False:
            logger('get slider_list fail')
            return False
        logger('Done')
        return slider_list

    def get_videocollagedesigner_rightscroll_button_list(self):
        """
        index: Color/Uniform Color(drop-down-menu)/Uniform Color/From Beginning(drop-down-menu)/
                Color(display color board)/advanced settings
        index(if have img): Color/Uniform Color(drop-down-menu)/From Beginning(drop-down-menu)/
                Color(display color board)/advanced settings
        :return:
        """
        el = self.get_videocollagedesigner_rightscroll_area_el()
        if el is False:
            logger('get el fail')
            return False
        button_list = self.search_child_el_by_role(el, 'AXButton')
        if button_list is False:
            logger('get button_list fail')
            return False
        logger('Done')
        return button_list

    def scroll_videocollagedesigner_rightscroll_scrollbar(self, option):
        if option not in ['up', 'down']:
            logger('incorrect parameter')
            return False
        # get scroll el
        el = self.get_videocollagedesigner_rightscroll_area_el()
        if el is False:
            logger('get el fail')
            return False
        scrollbar_el = self.search_child_el_by_role(el, 'AXScrollBar')
        if scrollbar_el is False:
            logger('get scrollbar fail')
            return False
        if self.scroll_scrollbar(scrollbar_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('scroll scrollbar fail')
        return False

    def adjust_videocollagedesigner_size(self, value):
        """
        need tolerance bcz return value is ex:9.34243
        :param value:
        :return:
        """
        slider_list = self.get_videocollagedesigner_rightscroll_slider_list()
        if slider_list is False:
            logger('get slider_list fail')
            return False
        size_slider = slider_list[0]
        tolerance = [value - 0.8, value + 0.8]
        if self.adjust_element_slider(size_slider, value, edge=8, min=0, max=100, tolerance=tolerance):
            logger('Done')
            return True
        else:
            logger('adjust slider fail')
        return False

    def adjust_videocollagedesigner_interclipsize(self, value):
        """
        need tolerance bcz the return value is ex: 10.2342
        :param value:
        :return:
        """
        slider_list = self.get_videocollagedesigner_rightscroll_slider_list()
        if slider_list is False:
            logger('get slider_list fail')
            return False
        size_slider = slider_list[1]
        tolerance = [value - 0.8, value + 0.8]
        if self.adjust_element_slider(size_slider, value, edge=8, min=0, max=100, tolerance=tolerance):
            logger('Done')
            return True
        else:
            logger('adjust slider fail')
        return False

    def tap_videocollagedesigner_color_icon(self):
        # get icon
        btn_list = self.get_videocollagedesigner_rightscroll_button_list()
        if btn_list is False:
            logger('get btn_list fail')
            return False
        color_el = btn_list[0]
        if self.tap_element(color_el):
            time.sleep(1)
            # verify
            if self.get_color_dialogue_el() is not False:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap element fail')
        return False

    def tap_videocollagedesigner_uniformcolor_icon(self):
        # get icon
        btn_list = self.get_videocollagedesigner_rightscroll_button_list()
        if btn_list is False:
            logger('get btn_list fail')
            return False
        color_el = btn_list[2]
        if self.tap_element(color_el):
            time.sleep(1)
            # verify
            if self.get_color_dialogue_el() is not False:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap element fail')
        return False

    def select_videocollagedesigner_filltype_drop_down_menu(self, option):
        btn_list = self.get_videocollagedesigner_rightscroll_button_list()
        if btn_list is False:
            logger('get btn_list fail')
            return False
        drop_down_el = btn_list[1]
        if self.select_drop_down_list(drop_down_el, option, element_mode=1, need_verify=0):
            time.sleep(1)
            # verify
            if self.is_open_dlg_popup():
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('select drop down list fail')
        return False

    def get_videocollagedesigner_rightscroll_checkbox_list(self):
        """
        index: Border/from beginning(2 options)/before after clip playback(3 options)
        :return:
        """
        el = self.get_videocollagedesigner_rightscroll_area_el()
        if el is False:
            logger('get el fail')
            return False
        checkbox_list = self.search_child_el_by_role(el, 'AXCheckBox')
        if checkbox_list is False:
            logger('get checkbox list fail')
            return False
        logger('Done')
        return checkbox_list

    def tick_videocollagedesigner_rightscroll_startclipplayback_checkbox(self, index, option):
        """
        :param index: 1st or 2nd one (use 1/2)
        :param option: on/off
        :return:
        """
        checkbox_list = self.get_videocollagedesigner_rightscroll_checkbox_list()
        if checkbox_list is False:
            logger('get checkbox_list fail')
            return False
        # 1, 2
        target = index
        checkbox = checkbox_list[target]
        if self.checkbox_handle(checkbox, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('handle checkbox fail')
        return False

    def tick_videocollagedesigner_rightscroll_beforeafterclipplayback_checkbox(self, index, option):
        """
        :param index: 1st or 2nd or 3rd one (use 1/2/3)
        :param option: on/off
        :return:
        """
        checkbox_list = self.get_videocollagedesigner_rightscroll_checkbox_list()
        if checkbox_list is False:
            logger('get checkbox_list fail')
            return False
        # 3, 4, 5
        target = index + 2
        checkbox = checkbox_list[target]
        if self.checkbox_handle(checkbox, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('handle checkbox fail')
        return False

    def select_videocollagedesigner_frameanimation_drop_down_menu(self, option, index=3):
        """
        :param option:
        :param index: if fill type is not img, index=3(default), if has img, need use 2
        :return:
        """
        btn_list = self.get_videocollagedesigner_rightscroll_button_list()
        if btn_list is False:
            logger('get btn_list fail')
            return False
        drop_down_el = btn_list[index]
        if self.select_drop_down_list(drop_down_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('select drop down list fail')
        return False

    def tap_videocollagedesigner_advancedsettings_btn(self):
        # get btn
        btn_list = self.get_videocollagedesigner_rightscroll_button_list()
        if btn_list is False:
            logger('get btn_list fail')
            return False
        advsettings_el = btn_list[-1]
        if self.tap_element(advsettings_el):
            time.sleep(1)
            # verify is dlg pops up
            if self.get_videocollagedesigner_advancedsettings_el():
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap element fail')
        return False

    def get_videocollagedesigner_advancedsettings_el(self):
        el = self.search_el(self.dlg_advanced_settings)
        if el is not None:
            logger('Done')
            return el
        else:
            logger('search el fail')
        return False

    def get_videocollagedesigner_advancedsettings_checkbox_list(self):
        """
        index: all at once/delay/one after another
        :return:
        """
        el = self.get_videocollagedesigner_advancedsettings_el()
        if el is False:
            logger('get el fail')
            return False
        checkbox_list = self.search_child_el_by_role(el, 'AXCheckBox')
        if checkbox_list is False:
            logger('get checkbox_list fail')
            return False
        logger('Done')
        return checkbox_list

    def tick_videocollagedesigner_advancedsettings_checkbox(self, index, option):
        """
        :param index: 1, 2, 3
        :param option: on/off(off not work for radio btn)
        :return:
        """
        checkbox_list = self.get_videocollagedesigner_advancedsettings_checkbox_list()
        if checkbox_list is False:
            logger('get checkbox_list fail')
            return False
        target_el = checkbox_list[index - 1]
        if self.checkbox_handle(target_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('checkbox handle fail')
        return False

    def tap_videocollagedesigner_play_icon(self):
        if self.tap_locator(self.icon_video_collage_designer_play_btn):
            # verify
            if self.search_el(self.icon_video_collage_designer_pause_btn) is not None:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap locator fail')
        return False

    def tap_videocollagedesigner_pause_icon(self):
        if self.tap_locator(self.icon_video_collage_designer_pause_btn):
            time.sleep(0.5)
            # verify
            if self.search_el(self.icon_video_collage_designer_play_btn) is not None:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap locator fail')
        return False

    def tap_videocollagedesigner_stop_icon(self):
        #v2219
        el_list = self.search_all_el(self.icon_video_collage_designer_stop_btn)
        if el_list is False:
            logger('get el_list fail')
            return False
        if self.tap_element(el_list[1]):
            # verify
            if self.search_el(self.icon_video_collage_designer_play_btn) is not None:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap locator fail')
        return False

    def get_videocollagedesigner_advancedsettings_button_list(self):
        """
        index: drop-down-menu/default/cancel/ok
        :return:
        """
        el = self.get_videocollagedesigner_advancedsettings_el()
        if el is False:
            logger('get el fail')
            return False
        button_list = self.search_child_el_by_role(el, 'AXButton')
        if button_list is False:
            logger('get checkbox_list fail')
            return False
        logger('Done')
        return button_list

    def select_videocollagedesigner_advancedsettings_drop_down_menu(self, option):
        el = self.get_videocollagedesigner_advancedsettings_button_list()
        if el is False:
            logger('get el fail')
            return False
        dropdown_el = el[0]
        if self.select_drop_down_list(dropdown_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('select drop down list fail')
        return False

    def get_group_list(self):
        """
        index: main/tipsarea/timeline
        :return:
        """
        group_parent = self.search_el(self.split_group_el)
        if group_parent is False:
            logger('get group_parent fail')
            return False
        group_list = self.search_child_el_by_role(group_parent, 'AXSplitGroup')
        if group_list is False:
            logger('get group_list fail')
            return False
        logger('Done')
        return group_list

    def get_timeline_group_area(self):
        return self.get_timeline_area()
        #old
        '''
        group_parent = self.get_group_list()
        if group_parent is False:
            logger('get group_parent fail')
            return False
        timeline_el = group_parent[-1]
        pos = self.get_pos(timeline_el)
        if pos is False:
            logger('get pos fail')
            return False
        logger(f'Done. {pos}')
        return pos
        '''


    def get_timeline_area(self):
        #old el = self.search_el(self.split_group_timeline_area)
        el = self.get_pdr_mian_window_bottom_split_group()
        if el is False:
            logger('get el fail')
            return False
        spliter_group = self.search_child_el_by_role(el, 'AXSplitGroup')
        if spliter_group is False:
            logger('get spliter_group fail')
            return False
        logger(spliter_group)
        pos = self.get_pos(spliter_group)
        if pos is not False:
            logger(f'Done. {pos}')
            return pos
        else:
            logger('get pos fail')
        return False

# video speed dlg
    def is_videospeed_dlg_popup(self):
        if self.search_el(self.tab_video_speed_entire_clip) is not None:
            logger('Done')
            return True
        else:
            logger('dlg does not pop up')
        return False

    def tap_media_in_timeline(self, filename, index):
        pos = self.get_timeline_block_pos(filename, index)
        if pos is False:
            logger('get pos fail')
            return False
        target_pos = (pos[0] + pos[2] / 2, pos[1] + pos[3] / 2)
        if self.tap_pos(target_pos):
            logger('Done')
            return True
        else:
            logger('tap pos fail')
        return False

    def tap_videospeed_dlg_entireclip_btn(self):
        if self.tap_locator(self.tab_video_speed_entire_clip):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def tap_videospeed_dlg_selectedrange_btn(self):
        if self.tap_locator(self.tab_video_speed_selected_range):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def get_videospeed_dlg_frame(self):
        """
        find the frame via [Reset] -> parent
        :return:
        """
        reset_el = self.search_el(self.btn_video_speed_reset)
        if reset_el is None:
            logger('get reset_el fail')
            return False
        frame_el = self.get_parent_wnd(reset_el)
        if frame_el is False:
            logger('get reset_el fail')
            return False
        logger('Done')
        return frame_el

    def get_videospeed_dlg_group_list(self):
        """
        index(entire clip): timecode/original video length/new video duration/speed multiplier
        index(selected range): timecode/duration/speed multiplier
        :return:
        """
        frame_el = self.get_videospeed_dlg_frame()
        if frame_el is False:
            logger('get frame_el fail')
            return False
        group_list = self.search_child_el_by_role(frame_el, 'AXGroup')
        if group_list is False:
            logger('get group_list fail')
            return False
        logger('Done')
        return group_list

    def get_videospeed_dlg_btn_list(self):
        """
        index: -7(remove btn)
        :return:
        """
        frame_el = self.get_videospeed_dlg_frame()
        if frame_el is False:
            logger('get frame_el fail')
            return False
        btn_list = self.search_child_el_by_role(frame_el, 'AXButton')
        if btn_list is False:
            logger('get btn_list fail')
            return False
        logger('Done')
        return btn_list

    def get_videospeed_dlg_originalvideolength_timecode(self):
        """
        :return:  ex: 00;00;15;28
        """
        group_list = self.get_videospeed_dlg_group_list()
        if group_list is False:
            logger('get group_list fail')
            return False
        timecode_el = group_list[1]
        text_el = self.search_child_el_by_role(timecode_el, 'AXStaticText')
        if text_el is False:
            logger('get text_el fail')
            return False
        text = self.get_axvalue(text_el)
        if text is not False:
            logger(f'Done. ({text})')
            return text
        else:
            logger('get text fail')
        return False

    def get_videospeed_dlg_newvideoduration_timecode(self):
        """
        :return:  ex: 00;00;15;28
        """
        group_list = self.get_videospeed_dlg_group_list()
        if group_list is False:
            logger('get group_list fail')
            return False
        timecode_el = group_list[2]
        text_el = self.search_child_el_by_role(timecode_el, 'AXStaticText')
        if text_el is False:
            logger('get text_el fail')
            return False
        text = self.get_axvalue(text_el)
        if text is not False:
            logger(f'Done. ({text})')
            return text
        else:
            logger('get text fail')
        return False

    def adjust_videospeed_dlg_newvideoduration_timecode(self, option):
        """
        :param option: 'up'/'down'
        :return:
        """
        org_value = self.get_videospeed_dlg_newvideoduration_timecode()
        if org_value is False:
            logger('get org_value fail')
            return False
        if option not in ['up', 'down']:
            logger('incorrect parameter')
            return False
        group_list = self.get_videospeed_dlg_group_list()
        if group_list is False:
            logger('get group_list fail')
            return False
        timecode_el = group_list[2]
        btn_list = self.search_child_el_by_role(timecode_el, 'AXButton')
        if btn_list is False:
            logger('get btn_list fail')
            return False
        if option == 'up':
            target_el = btn_list[0]
        elif option == 'down':
            target_el = btn_list[1]
        if self.tap_element(target_el):
            # verify
            after_value = self.get_videospeed_dlg_newvideoduration_timecode()
            if after_value is False:
                logger('get after_value fail')
                return False
            if after_value != org_value:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap element fail')
        return False

    def adjust_videospeed_dlg_speedmultiplier_slider(self, value):
        """
        :param value: default(50)
        :return:
        """
        # get slider el
        frame_el = self.get_videospeed_dlg_frame()
        if frame_el is False:
            logger('get frame_el fail')
            return False
        slider_list = self.search_child_el_by_role(frame_el, 'AXSlider')
        # index: playback/speedmultiplier/preview size slider
        if slider_list is False:
            logger('get slider_list fail')
            return False
        slider_el = slider_list[1]
        tolerance_range = [value - 1, value + 1]
        if self.adjust_element_slider(slider_el, value, min=0, max=98.7, tolerance=tolerance_range):
            logger('Done')
            return True
        else:
            logger('adjust slider fail')
        return False

    def tap_videospeed_dlg_reset_btn(self):
        if self.tap_locator(self.btn_video_speed_reset):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def get_videospeed_dlg_timeline_area(self):
        frame_el = self.get_videospeed_dlg_frame()
        if frame_el is False:
            logger('get frame_el fail')
            return False
        scrollarea_list = self.search_child_el_by_role(frame_el, 'AXScrollArea')
        if scrollarea_list is False:
            logger('get scrollarea_list fail')
            return False
        timeline_area = scrollarea_list[0]
        pos = self.get_pos(timeline_area)
        if pos is False:
            logger('get pos fail')
            return False
        logger('Done')
        return pos

    #new special handle
    def tap_videospeed_dlg_timeshift_block_top(self, group=0):
        """
        group: 0, 1, 2,
        Structure: scrollarea -> collection/AXList -> section/AXList(this function)
        :return:
        """
        frame_el = self.get_videospeed_dlg_frame()
        if frame_el is False:
            logger('get frame_el fail')
            return False
        scrollarea_list = self.search_child_el_by_role(frame_el, 'AXScrollArea')
        if scrollarea_list is False:
            logger('get scrollarea_list fail')
            return False
        collection_el = self.search_child_el_by_role(scrollarea_list[0], 'AXList')
        if collection_el is False:
            logger('get collection_el fail')
            return False
        section_el = self.search_child_el_by_role(collection_el, 'AXList')
        if section_el is False:
            logger('get section_el fail')
            return False
        group_list = self.search_child_el_by_role(section_el, 'AXGroup')
        if group_list is False:
            logger('get group_list fail')
            return False
        target_el = group_list[group]
        # tap top-mid
        pos = self.get_pos(target_el)
        if pos is False:
            logger('get pos fail')
            return False
        target_pos = (pos[0] + pos[2] / 2, pos[1] - 2)
        if self.tap_pos(target_pos):
            logger('Done')
            return True
        else:
            logger('tap pos fail')
        return False

    def adjust_videospeed_dlg_timeshift_block_size(self, group=0):
        """
        group: 0, 1, 2,
        Structure: scrollarea -> collection/AXList -> section/AXList(this function)
        :return:
        """
        frame_el = self.get_videospeed_dlg_frame()
        if frame_el is False:
            logger('get frame_el fail')
            return False
        scrollarea_list = self.search_child_el_by_role(frame_el, 'AXScrollArea')
        if scrollarea_list is False:
            logger('get scrollarea_list fail')
            return False
        collection_el = self.search_child_el_by_role(scrollarea_list[0], 'AXList')
        if collection_el is False:
            logger('get collection_el fail')
            return False
        section_el = self.search_child_el_by_role(collection_el, 'AXList')
        if section_el is False:
            logger('get section_el fail')
            return False
        group_list = self.search_child_el_by_role(section_el, 'AXGroup')
        if group_list is False:
            logger('get group_list fail')
            return False
        target_el = group_list[group]
        # tap top-mid
        pos = self.get_pos(target_el)
        if pos is False:
            logger('get pos fail')
            return False
        start_pos = (pos[0] + pos[2] - 2, pos[1] + pos[3] / 2)
        end_pos = (pos[0] + pos[2] + 100, pos[1] + pos[3] / 2)
        if self.drag_mouse(start_pos, end_pos):
            logger('Done')
            return True
        else:
            logger('tap pos fail')
        return False

    def tap_videospeed_dlg_createtimeshift_btn(self):
        frame_el = self.get_videospeed_dlg_frame()
        if frame_el is False:
            logger('get frame_el fail')
            return False
        btn_list = self.search_child_el_by_title(frame_el, 'Create time shift')
        btn_el = btn_list[0]
        if btn_el is False:
            logger('get btn_el fail')
            return False
        if self.tap_element(btn_el):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def tap_videospeed_dlg_delete_btn(self):
        btn_list = self.get_videospeed_dlg_btn_list()
        if btn_list is False:
            logger('get btn_list fail')
            return False
        delete_btn = btn_list[-7]
        if self.tap_element(delete_btn):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def get_videospeed_dlg_duration_timecode(self):
        group_list = self.get_videospeed_dlg_group_list()
        if group_list is False:
            logger('get group_list fail')
            return False
        timecode_el = group_list[1]
        text_el = self.search_child_el_by_role(timecode_el, 'AXStaticText')
        if text_el is False:
            logger('get text_el fail')
            return False
        text = self.get_axvalue(text_el)
        if text is not False:
            logger(f'Done. ({text})')
            return text
        else:
            logger('get text fail')
        return False

    def adjust_videospeed_dlg_duration_timecode(self, option):
        """
        :param option: 'up'/'down'
        :return:
        """
        org_value = self.get_videospeed_dlg_duration_timecode()
        if org_value is False:
            logger('get org_value fail')
            return False
        if option not in ['up', 'down']:
            logger('incorrect parameter')
            return False
        group_list = self.get_videospeed_dlg_group_list()
        if group_list is False:
            logger('get group_list fail')
            return False
        timecode_el = group_list[1]
        btn_list = self.search_child_el_by_role(timecode_el, 'AXButton')
        if btn_list is False:
            logger('get btn_list fail')
            return False
        if option == 'up':
            target_el = btn_list[0]
        elif option == 'down':
            target_el = btn_list[1]
        if self.tap_element(target_el):
            # verify
            after_value = self.get_videospeed_dlg_duration_timecode()
            if after_value is False:
                logger('get after_value fail')
                return False
            if after_value != org_value:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap element fail')
        return False

    def tick_videospeed_dlg_easein_checkbox(self, option):
        frame_el = self.get_videospeed_dlg_frame()
        if frame_el is False:
            logger('get frame_el fail')
            return False
        easein_checkbox = self.search_child_el_by_title(frame_el, 'Ease in')
        if easein_checkbox is False:
            logger('get easein_checkbox fail')
            return False
        if self.checkbox_handle(easein_checkbox, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('check box handle fail')
        return False

    def tick_videospeed_dlg_easeout_checkbox(self, option):
        frame_el = self.get_videospeed_dlg_frame()
        if frame_el is False:
            logger('get frame_el fail')
            return False
        easeout_checkbox = self.search_child_el_by_title(frame_el, 'Ease out')
        if easeout_checkbox is False:
            logger('get easeout_checkbox fail')
            return False
        if self.checkbox_handle(easeout_checkbox, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('check box handle fail')
        return False

    def get_videospeed_dlg_settings_dlg_el(self):
        dlg_el = self.search_el(self.dlg_video_speed_settings)
        if dlg_el is not None:
            logger('Done')
            return dlg_el
        else:
            logger('get dlg_el fail')
        return False

    def get_videospeed_dlg_settings_dlg_checkbox_list(self):
        """
        index: remove audio/keep audio/Keep audio pitch (0.5X to 2X only)
        :return:
        """
        dlg_el = self.get_videospeed_dlg_settings_dlg_el()
        if dlg_el is False:
            logger('get dlg_el fail')
            return False
        checkbox_list = self.search_child_el_by_role(dlg_el, 'AXCheckBox')
        if checkbox_list is False:
            logger('get checkbox_list fail')
            return False
        logger('Done')
        return checkbox_list

    def tap_videospeed_dlg_settings(self):
        #new 2nd el
        el_list = self.search_all_el(self.icon_video_speed_settings)
        if el_list is False:
            logger('get el_list fail')
            return False
        if self.tap_element(el_list[1]):
            time.sleep(1)
            # verify
            if self.get_videospeed_dlg_settings_dlg_el() is not False:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap locator fail')
        return False

    def tick_videospeed_dlg_settings_removeaudio_checkbox(self, option):
        checkbox_list = self.get_videospeed_dlg_settings_dlg_checkbox_list()
        if checkbox_list is False:
            logger('get checkbox_list fail')
            return False
        removeaudio_el = checkbox_list[0]
        if self.checkbox_handle(removeaudio_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('handle checkbox fail')
        return False

    def tick_videospeed_dlg_settings_keepaudio_checkbox(self, option):
        checkbox_list = self.get_videospeed_dlg_settings_dlg_checkbox_list()
        if checkbox_list is False:
            logger('get checkbox_list fail')
            return False
        keepaudio_el = checkbox_list[1]
        if self.checkbox_handle(keepaudio_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('handle checkbox fail')
        return False

    def tick_videospeed_dlg_settings_keepaudiopitch_checkbox(self, option):
        checkbox_list = self.get_videospeed_dlg_settings_dlg_checkbox_list()
        if checkbox_list is False:
            logger('get checkbox_list fail')
            return False
        keepaudiopitch_el = checkbox_list[2]
        if self.checkbox_handle(keepaudiopitch_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('handle checkbox fail')
        return False


    def tap_videospeed_play_icon(self):
        if self.tap_locator(self.icon_video_speed_play):
            time.sleep(3) # for download audio
            # verify
            if self.search_el(self.icon_video_speed_pause) is not None:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap locator fail')
        return False

    def tap_videospeed_pause_icon(self):
        if self.tap_locator(self.icon_video_speed_pause):
            # verify
            if self.search_el(self.icon_video_speed_play) is not None:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap locator fail')
        return False

    def tap_videospeed_stop_icon(self):
        if self.tap_locator(self.icon_video_speed_stop):
            # verify
            if self.search_el(self.icon_video_speed_play) is not None:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap locator fail')
        return False

    def verify_videospeed_playback(self, verify_short_content=0):
        """
        for case, only playback & stop
        if verify short content = 1, doesn't check pause case
        :return:
        """
        if self.tap_videospeed_play_icon():
            if self.tap_videospeed_stop_icon():
                logger('Done')
                return True
            else:
                logger('tap stop fail')
        else:
            if verify_short_content == 1:
                if self.tap_videospeed_stop_icon():
                    logger('Done')
                    return True
                else:
                    logger('tap stop fail')
            else:
                logger('tap play fail')
        return False

# Product functions
    def get_produce_page_group(self):
        """
        Structures: groups(this function, whole page) -> tab view/buttons/buttons/groups
        :return:
        """
        produce_group = self.search_el(self.group_produce_page)
        if produce_group is False:
            logger('get group_produce_page fail')
            return False
        logger('Done')
        return produce_group

    def get_produce_page_left_group(self):
        """
        has standard 2D & online
        standard 2D:
        :return:
        """
        produce_group = self.get_produce_page_group()
        if produce_group is False:
            logger('get produce_group fail')
            return False
        left_group_list = self.search_child_el_by_role(produce_group, 'AXGroup')
        if left_group_list is False:
            logger('get left_group_list fail')
            return False
        logger('Done')
        return left_group_list[0]

    def get_produce_page_left_group_button_list(self):
        """
        standard 2d index: profile analyze/XAVC S/h264 AVC/h265 HEVC
        online index: YouTube/Viemo
        :return:
        """
        left_group = self.get_produce_page_left_group()
        if left_group is False:
            logger('get left_group fail')
            return False
        btn_list = self.search_child_el_by_role(left_group, 'AXButton')
        if btn_list is False:
            logger('get btn_list fail')
            return False
        logger('Done')
        return btn_list

    def tap_produce_page_standard2d_xavc_btn(self):
        btn_list = self.get_produce_page_left_group_button_list()
        if btn_list is False:
            logger('get btn_list fail')
            return False
        xavc_btn = btn_list[3]
        if self.tap_element(xavc_btn):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def tap_produce_page_standard2d_h264_btn(self):
        btn_list = self.get_produce_page_left_group_button_list()
        if btn_list is False:
            logger('get btn_list fail')
            return False
        h264_btn = btn_list[1]
        if self.tap_element(h264_btn):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def tap_produce_page_standard2d_h265_btn(self):
        btn_list = self.get_produce_page_left_group_button_list()
        if btn_list is False:
            logger('get btn_list fail')
            return False
        h265_btn = btn_list[2]
        if self.tap_element(h265_btn):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def tap_produce_page_profileanalyzer_btn(self):
        btn_list = self.get_produce_page_left_group_button_list()
        if btn_list is False:
            logger('get btn_list fail')
            return False
        profileanalyzer_btn = btn_list[0]
        if self.tap_element(profileanalyzer_btn):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def tap_produce_page_online_youtube_btn(self):
        btn_list = self.get_produce_page_left_group_button_list()
        if btn_list is False:
            logger('get btn_list fail')
            return False
        youtube_btn = btn_list[0]
        if self.tap_element(youtube_btn):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def tap_produce_page_online_vimeo_btn(self):
        btn_list = self.get_produce_page_left_group_button_list()
        if btn_list is False:
            logger('get btn_list fail')
            return False
        vimeo_btn = btn_list[1]
        if self.tap_element(vimeo_btn):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def tap_produce_tab(self):
        if self.tap_locator(self.tab_main_produce):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def tap_edit_tab(self):
        if self.tap_locator(self.tab_main_edit):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False


    def is_in_produce_page(self):
        if self.search_el(self.str_produce_standard2d) is not None:
            logger('Done')
            return True
        else:
            logger('not in produce page')
        return False

    def get_produce_page_leftbottom_group(self):
        """
        Structure: group(this function) -> drop down list...etc
        :return:
        """
        left_group = self.get_produce_page_left_group()
        if left_group is False:
            logger('get left_group fail')
            return False
        group = self.search_child_el_by_role(left_group, 'AXGroup')
        if group is False:
            logger('get group fail')
            return False
        logger('Done')
        return group

    def get_produce_page_drop_down_el(self, textname, mode='h264'):
        """
        for 264 265 only
        find the text and next is button el
        name: "Profile type:", "Profile name/Quality:", "Country/video format of disk:", "File extension:",
                "Video categories:"(YouTube)
        mode: h264(h265), xavc, youtube, vimeo
        """
        #new
        add_num = 0
        if mode == 'h264' or mode == 'h265':
            if textname == "Profile type:":
                add_num = 2
            elif textname == "Profile name/Quality:":
                add_num = 1
            elif textname == "Country/video format of disk:":
                add_num = -5
            elif textname == "File extension:":
                add_num = 2
        elif mode == 'xavc':
            if textname == "Profile type:":
                add_num = 1
            elif textname == "Profile name/Quality:":
                add_num = 1
            elif textname == "Country/video format of disk:":
                add_num = -5
        elif mode == 'youtube' or mode == 'vimeo':
            if textname == "Profile type:":
                add_num = 1

        group = self.get_produce_page_leftbottom_group()
        if group is False:
            logger('get group fail')
            return False
        child_list = self.get_child_wnd(group)
        if child_list is False:
            logger('get child_list fail')
            return False
        # search profile type text
        target_index = ''
        logger(child_list)
        for x in range(len(child_list)):
            if self.get_axvalue(child_list[x]) == textname:
                target_index = x
                break
        if target_index == '':
            logger('search order fail')
            return False
        # find next drop-down element
        target_index = target_index + add_num
        if self.get_axrole(child_list[target_index]) != 'AXButton':
            logger('need to maintain function')
            return False
        logger('Done')
        logger(target_index)
        logger(child_list)
        return child_list[target_index]

    def select_produce_page_profiletype_drop_down_menu(self, option, mode='h264'):
        target_el = self.get_produce_page_drop_down_el('Profile type:', mode)
        if target_el is False:
            logger('get target_el fail')
            return False
        if self.select_drop_down_list(target_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('select drop down list fail')
        return False

    def select_produce_page_profilenamequality_drop_down_menu(self, option, mode='h264'):
        target_el = self.get_produce_page_drop_down_el('Profile name/Quality:', mode)
        if target_el is False:
            logger('get target_el fail')
            return False
        if self.select_drop_down_list(target_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('select drop down list fail')
        return False

    def select_produce_page_countryvideoformatofdisk_drop_down_menu(self, option, mode='h264'):
        target_el = self.get_produce_page_drop_down_el('Country/video format of disk:', mode)
        if target_el is False:
            logger('get target_el fail')
            return False
        if self.select_drop_down_list(target_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('select drop down list fail')
        return False

    def select_produce_page_fileextension_drop_down_menu(self, option, mode='h264'):
        target_el = self.get_produce_page_drop_down_el('File extension:', mode)
        if target_el is False:
            logger('get target_el fail')
            return False
        if self.select_drop_down_list(target_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('select drop down list fail')
        return False

    def get_produce_page_leftbottom_checkbox_list(self):
        """
        index:
            => standard 2d: Fast vedio renderin.../SVRT/Hardware video enco.../Surround sound/AAC 5.1/
                            TrueTheater Surroun.../Upload a copy to Cy...
            => online: Public: Share your .../ Share timeline info.../Private: Only viewa.../Hardware video enco...
        :return:
        """
        group = self.get_produce_page_leftbottom_group()
        if group is False:
            logger('get group fail')
            return False
        # get checkbox list
        checkbox_list = self.search_child_el_by_role(group, 'AXCheckBox')
        if checkbox_list is False:
            logger('get child_list fail')
            return False
        logger('Done')
        return checkbox_list

    def tick_produce_page_fastvideorendering_checkbox(self, option):
        # get el
        checkbox_list = self.get_produce_page_leftbottom_checkbox_list()
        if checkbox_list is False:
            logger('get child_list fail')
            return False
        target_el = checkbox_list[0]
        if self.checkbox_handle(target_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('handle checkbox fail')
        return False

    def tick_produce_page_svrt_checkbox(self, option):
        # get el
        checkbox_list = self.get_produce_page_leftbottom_checkbox_list()
        if checkbox_list is False:
            logger('get child_list fail')
            return False
        target_el = checkbox_list[1]
        if self.checkbox_handle(target_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('handle checkbox fail')
        return False

    def tick_produce_page_hardwarevideoencoder_checkbox(self, option):
        # get el
        checkbox_list = self.get_produce_page_leftbottom_checkbox_list()
        if checkbox_list is False:
            logger('get child_list fail')
            return False
        logger(checkbox_list)
        # Index: public/privacy/HW  (youtube/vimeo)
        # check in standard 2d or online
        index = ''
        standard2d_el = self.search_el(self.tab_produce_page_standard2d)
        if standard2d_el is None:
            logger('get standard2d_el fail')
            return False
        online_el = self.search_el(self.tab_produce_page_online)
        if online_el is None:
            logger('get online_el fail')
            return False
        if self.get_axvalue(standard2d_el) == 1:
            logger('standard 2d')
            index = 2
        elif self.get_axvalue(online_el) == 1:
            logger('online')
            index = 2
        else:
            logger('get axvalue fail')
            return False
        target_el = checkbox_list[index]
        if self.checkbox_handle(target_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('handle checkbox fail')
        return False

    def tick_produce_page_surroundsound_checkbox(self, option):
        # get el
        checkbox_list = self.get_produce_page_leftbottom_checkbox_list()
        if checkbox_list is False:
            logger('get child_list fail')
            return False
        target_el = checkbox_list[3]
        if self.checkbox_handle(target_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('handle checkbox fail')
        return False

    def tick_produce_page_aac_checkbox(self, option):
        # get el
        checkbox_list = self.get_produce_page_leftbottom_checkbox_list()
        if checkbox_list is False:
            logger('get child_list fail')
            return False
        target_el = checkbox_list[4]
        # make sure its aac(M2TS doesn't have aac)
        if self.get_axtitle(target_el) != 'AAC 5.1':
            logger('no AAC for this profile')
            return False
        if self.checkbox_handle(target_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('handle checkbox fail')
        return False

    def tick_produce_page_tts_checkbox(self, option):
        # get el
        checkbox_list = self.get_produce_page_leftbottom_checkbox_list()
        if checkbox_list is False:
            logger('get child_list fail')
            return False
        target_el = checkbox_list[5]
        # make sure its aac(M2TS doesn't have aac)
        if self.get_axtitle(target_el) != 'TrueTheater Surround':
            target_el = checkbox_list[4]
        if self.checkbox_handle(target_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('handle checkbox fail')
        return False

    def tick_produce_page_uploadacopy_checkbox(self, option):
        # get el
        checkbox_list = self.get_produce_page_leftbottom_checkbox_list()
        if checkbox_list is False:
            logger('get child_list fail')
            return False
        try:
            target_el = checkbox_list[5]
            # make sure its aac(M2TS doesn't have aac)
            if self.get_axtitle(target_el) != 'Upload a copy to Cyberlink Cloud':
                if self.get_axtitle(target_el) != 'Upload a copy to CyberLink Cloud':
                    target_el = checkbox_list[6]
        except Exception:
            logger('list out of range')
            logger(f'checkbox_list: {checkbox_list}')
            return False
        if self.checkbox_handle(target_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('handle checkbox fail')
        return False

    def get_produce_page_button_list(self):
        """
        last one is 'file path'
        :return:
        """
        group = self.get_produce_page_group()
        if group is False:
            logger('get group fail')
            return False
        btn_list = self.search_child_el_by_role(group, 'AXButton')
        if btn_list is False:
            logger('get btn_list fail')
            return False
        logger('Done')
        return btn_list

    def tap_produce_page_outputpath_btn(self):
        btn_list = self.get_produce_page_button_list()
        if btn_list is False:
            logger('get btn_list fail')
            return False
        outputpath_btn = btn_list[-1]
        if self.tap_element(outputpath_btn):
            # verify
            time.sleep(1)
            if self.is_saveas_dlg_popup():
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap element fail')
        return False

    def assign_produce_page_outputpath(self, outputname):
        """
        save file at \\Downloads
        :param name:
        :return:
        """
        # if got project list, choose directly
        if self.search_el(self.column_where_downloads) is None:
            # go projects folder
            locator = {'AXValue': 'Downloads', 'AXRole': 'AXStaticText'}
            if not self.tap_locator(locator):
                logger('select tab fail')
                return False
        else:
            pass
        # assign project name
        column_pos = self.get_locator_mid_pos(self.column_save_as_name)
        if column_pos is False:
            logger('get column pos fail')
            return False
        if self.click_mouse(column_pos, times=2):
            time.sleep(1)
            # input prject name
            if self.input_text(outputname):
                # click save
                if self.tap_locator(self.btn_dlg_save):
                    # click save btn
                    if self.tap_locator(self.btn_dlg_save):
                        # close replace if any
                        self.tap_locator(self.btn_dlg_replace)
                        logger('Done')
                        return True
                    else:
                        logger('tap save btn fail')
                else:
                    logger('tap btn save fail')
            else:
                logger('input text fail')
        else:
            logger('click mouse fail')
        return False

    def tap_produce_page_start_btn(self, convert_to_mp4='no'):
        group = self.get_produce_page_group()
        if group is False:
            logger('get group fail')
            return False
        start_btn = self.search_child_el_by_title(group, 'Start')
        if start_btn is False:
            logger('get start_btn fail')
            return False
        if self.tap_element(start_btn):
            time.sleep(1)
            # close 'convert to mp4' 1st dlg
            if convert_to_mp4 == 'no':
                if not self.tap_no_btn():
                    logger('tap no btn fail')
                    return False
            elif convert_to_mp4 == 'yes':
                if not self.tap_yes_btn():
                    logger('tap yes btn fail')
                    return False
            elif convert_to_mp4 is None:
                # for youtube/vimeo case
                pass
            # press 'yes' to overwirte existed file if any
            time.sleep(1)
            self.tap_yes_btn()
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def get_produce_page_process(self):
        """
        :return: AXValue (ex: Produce progress... 7%)
        group 1st type:text
        """
        group = self.get_produce_page_group()
        if group is False:
            logger('get group fail')
            return False
        text_list = self.search_child_el_by_role(group, 'AXStaticText')
        if text_list is False:
            logger('get text_list fail')
            return False
        text_el = text_list[0]
        text = self.get_axvalue(text_el)
        if text is False:
            logger('get text fail')
            return False
        res = text.split(' ')[-1]
        logger(f'Done. ({res})')
        return res

    def check_produce_page_process_till_complete(self, timeout=200):
        """
        # Jamie modified default value to 200
        :param timeout: default: 60sec.
        :return:
        """
        for x in range(timeout):
            # check process every 5sec.
            if int(str(x / 5).split('.')[-1]) == 0:
                res = self.get_produce_page_process()
                # Jamie modified
                if res == 'complete.':
                    logger('Done')
                    return True
            time.sleep(1)
        logger(f"complete text doesn't show after {timeout}sec.")
        return False

    def tap_produce_page_openfilelocation_btn(self):
        locator = {'AXTitle': 'Open file location', 'AXButton': 'AXButton'}
        if self.tap_locator(locator):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def tap_produce_page_standard2d_tab(self):
        # bcz it's axcheckbox, use checkbox handle function to check
        if self.checkbox_handle(self.tab_produce_page_standard2d, 'on'):
            logger('Done')
            return True
        else:
            logger('checkbox handle fail')
        return False

    def tap_produce_page_online_tab(self):
        # bcz it's axcheckbox, use checkbox handle function to check
        if self.checkbox_handle(self.tab_produce_page_online, 'on'):
            logger('Done')
            return True
        else:
            logger('checkbox handle fail')
        return False

    def tick_produce_page_public_checkbox(self, option):
        checkbox_list = self.get_produce_page_leftbottom_checkbox_list()
        if checkbox_list is False:
            logger('get checkbox_list fail')
            return False
        target_checkbox = checkbox_list[0]
        if self.checkbox_handle(target_checkbox, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('handle checkbox fail')
        return False

    def tick_produce_page_sharetimelineinfo_checkbox(self, option):
        checkbox_list = self.get_produce_page_leftbottom_checkbox_list()
        if checkbox_list is False:
            logger('get checkbox_list fail')
            return False
        target_checkbox = checkbox_list[1]
        if self.checkbox_handle(target_checkbox, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('handle checkbox fail')
        return False

    def tick_produce_page_privacy_checkbox(self, option):
        checkbox_list = self.get_produce_page_leftbottom_checkbox_list()
        if checkbox_list is False:
            logger('get checkbox_list fail')
            return False
        target_checkbox = checkbox_list[2]
        if self.checkbox_handle(target_checkbox, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('handle checkbox fail')
        return False

# YouTube authorization dlg
    def get_youtube_authorization_dlg_el(self):
        el = self.search_el(self.dlg_youtube_frame)
        if el is None:
            logger('search el fail')
            return False
        logger('Done')
        return el

    def is_youtube_authorization_dlg_pop_up(self):
        if self.get_youtube_authorization_dlg_el() is False:
            logger("can't find youtube authorization dlg")
            return False
        else:
            logger('Done')
            return True

    def tap_authorize_btn(self):
        locator = {'AXTitle': 'Authorize', 'AXRole': 'AXButton'}
        if self.tap_locator(locator):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def input_youtube_account(self, account, ground_truth_folder):
        """
        use image folder
        :param account:
        :param ground_truth_folder:
        :return:
        """
        pos = self.search_pos_from_image('youtube_column.png', ground_truth_folder)
        if pos is False:
            logger('get pos fail')
            return False
        if not self.tap_pos(pos):
            logger('tap pos fail')
            return False
        if self.input_text(account):
            logger('Done')
            return True
        else:
            logger('input text fail')
        return False

    def input_youtube_password(self, password, ground_truth_folder):
        """
        use image folder
        :param account:
        :param ground_truth_folder:
        :return:
        """
        pos = self.search_pos_from_image('youtube_column.png', ground_truth_folder)
        if pos is False:
            logger('get pos fail')
            return False
        if not self.tap_pos(pos):
            logger('tap pos fail')
            return False
        if self.input_text(password):
            logger('Done')
            return True
        else:
            logger('input text fail')
        return False

    def tap_youtube_next_btn(self, ground_truth_folder):
        pos = self.search_pos_from_image('youtube_next.png', ground_truth_folder)
        if pos is False:
            logger('get pos fail')
            return False
        if self.tap_pos(pos):
            logger('Done')
            return True
        else:
            logger('tap pos fail')
        return False

    def check_youtube_process_till_complete(self, timeout=120):
        """
        :param timeout: default: 60sec.
        :return:
        """
        locator = {'AXValue': 'Movie producing and uploading complete.', 'AXRole': 'AXStaticText'}
        for x in range(timeout):
            # check process every 5sec.
            if int(str(x / 5).split('.')[-1]) == 0:
                if self.search_el(locator) is not None:
                    logger('Done')
                    return True
            time.sleep(1)
        logger(f"complete text doesn't show after {timeout}sec.")
        return False

# Vimeo authorization dlg
    def get_vimeo_authorization_dlg_el(self):
        el = self.search_el(self.dlg_vimeo_frame)
        if el is None:
            logger('search el fail')
            return False
        logger('Done')
        return el

    def is_vimeo_authorization_dlg_pop_up(self):
        if self.get_vimeo_authorization_dlg_el() is False:
            logger("can't find youtube authorization dlg")
            return False
        else:
            logger('Done')
            return True

    def input_vimeo_account(self, account):
        """
        use ocr bcz BG would change
        :param account:
        :param ground_truth_folder:
        :return:
        """
        pos = self.search_text_position('address')
        if pos is False:
            logger('get pos fail')
            return False
        if not self.tap_pos(pos):
            logger('tap pos fail')
            return False
        if self.input_text(account):
            logger('Done')
            return True
        else:
            logger('input text fail')
        return False

    def input_vimeo_password(self, account):
        """
        use ocr bcz BG would change
        :param account:
        :param ground_truth_folder:
        :return:
        """
        pos = self.search_text_position('Password')
        if pos is False:
            logger('get pos fail')
            return False
        if not self.tap_pos(pos):
            logger('tap pos fail')
            return False
        if self.input_text(account):
            logger('Done')
            return True
        else:
            logger('input text fail')
        return False

    def tap_vimeo_loginwithemail_btn(self, ground_truth_folder):
        pos = self.search_pos_from_image('vimeo_next.png', ground_truth_folder)
        if pos is False:
            logger('get pos fail')
            return False
        if self.tap_pos(pos):
            logger('Done')
            return True
        else:
            logger('tap pos fail')
        return False

    def is_vimeo_login_success(self, ground_truth_folder):
        """
        check via 'showcases' img
        :return:
        """
        pos = self.search_pos_from_image('vimeo_showcases.png', ground_truth_folder)
        if pos is False:
            logger('get pos fail')
            return False
        else:
            logger('Done')
            return True

    def close_vimeo_authorization_dlg(self):
        el = self.get_vimeo_authorization_dlg_el()
        if el is False:
            logger('get el fail')
            return False
        close_btn = self.search_child_el_by_type(el, 'close button')
        if close_btn is False:
            logger('get close_btn fail')
            return False
        if self.tap_element(close_btn):
            # verify
            if self.is_vimeo_authorization_dlg_pop_up() is False:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap element fail')
        return False

    def tap_vimeo_allow_btn(self):
        """
        use ocr
        :return:
        """
        # has allow & don't allow
        pos = self.search_text_position('Allow', '1/2')
        if pos is False:
            logger('get pos fail')
            return False
        if self.tap_pos(pos):
            logger('Done')
            return True
        else:
            logger('tap pos fail')
        return False

    def check_vimeo_process_till_complete(self):
        logger('interface of check_vimeo_process_till_complete')
        return self.check_youtube_process_till_complete()

# [Main WINDOW HANDLE]
    pdr_main_ui = {'AXTitle': 'PowerDirector', 'AXRole': 'AXWindow'}
    def get_pdr_main_window_el(self):
        """
        structure: main -> group -> split group -> split group(top)...splitgroup(bottom)
        :return:
        """
        main_el = self.search_el(self.pdr_main_ui)
        if main_el is False:
            logger('get main_el fail')
            return False
        logger('Done')
        return main_el

    def get_pdr_mian_window_group(self):
        main_el = self.get_pdr_main_window_el()
        if main_el is False:
            logger('get main_el fail')
            return False
        group_el = self.search_child_el_by_role(main_el, 'AXGroup')
        if group_el is False:
            logger('get group_el fail')
            return False
        logger('Done')
        return group_el

    def get_pdr_mian_window_split_group(self):
        group_el = self.get_pdr_mian_window_group()
        if group_el is False:
            logger('get group_el fail')
            return False
        split_group_el = self.search_child_el_by_role(group_el, 'AXSplitGroup')
        if split_group_el is False:
            logger('get split_group_el fail')
            return False
        logger('Done')
        return split_group_el

    def get_pdr_mian_window_top_split_group(self):
        split_group_el = self.get_pdr_mian_window_split_group()
        if split_group_el is False:
            logger('get split_group_el fail')
            return False
        split_group_top_el = self.search_child_el_by_role(split_group_el, 'AXSplitGroup')
        if split_group_top_el is False:
            logger('get split_group_top_el fail')
            return False
        logger('Done')
        try:
            return split_group_top_el[0]
        except:
            return split_group_top_el

    def get_pdr_mian_window_bottom_split_group(self):
        split_group_el = self.get_pdr_mian_window_split_group()
        if split_group_el is False:
            logger('get split_group_el fail')
            return False
        split_group_bottom_el = self.search_child_el_by_role(split_group_el, 'group')
        if split_group_bottom_el is False:
            logger('get split_group_top_el fail')
            return False
        logger('Done')
        try:
            return split_group_bottom_el[1]
        except:
            return split_group_bottom_el


    def is_in_fixenhance_page(self):
        split_group_top_el = self.get_pdr_mian_window_top_split_group()
        if split_group_top_el is False:
            logger('get split_group_top_el fail')
            return False
        child_list = self.get_child_wnd(split_group_top_el)
        if child_list is False:
            logger('get child_list fail')
            return False
        if self.get_axvalue(child_list[0]) == 'Fix / Enhance':
            logger('Done')
            return True
        else:
            logger('get axvalue fail')
        return False

    def tap_fixenahnce_tipsarea_btn(self):
        if self.tap_locator(self.btn_tipsarea_fix_enhance):
            time.sleep(1)
            # verify
            if self.is_in_fixenhance_page():
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap locator fail')
        return False

    def get_fixenhance_scrollarea_list(self):
        """
        index: left checkbox, control area
        :return:
        """
        split_group_top_el = self.get_pdr_mian_window_top_split_group()
        if split_group_top_el is False:
            logger('get split_group_top_el fail')
            return False
        scrollarea_list = self.search_child_el_by_role(split_group_top_el, 'AXScrollArea')
        if scrollarea_list is False:
            logger('get scrollarea_list fail')
            return False
        logger('Done')
        return scrollarea_list

    def get_fixenhance_left_scrollarea(self):
        scrollarea_list = self.get_fixenhance_scrollarea_list()
        if scrollarea_list is False:
            logger('get scrollarea_list fail')
            return False
        try:
            target = scrollarea_list[0]
            logger('Done')
            return target
        except:
            logger('Exception')
            return False

    def get_fixenhance_right_scrollarea(self):
        scrollarea_list = self.get_fixenhance_scrollarea_list()
        if scrollarea_list is False:
            logger('get scrollarea_list fail')
            return False
        try:
            target = scrollarea_list[1]
            logger('Done')
            return target
        except:
            logger('Exception')
            return False

    def get_fixenhance_left_checkbox_list(self):
        left_srollarea = self.get_fixenhance_left_scrollarea()
        if left_srollarea is False:
            logger('get left_srollarea fail')
            return False
        group_list = self.search_child_el_by_role(left_srollarea, 'AXGroup')
        if group_list is False:
            logger('get group_list fail')
            return False
        logger('Done')
        return group_list

    def tick_fixenahnce_left_checkbox(self, target):
        """
        :param target:  ex: 'Lens Correction'
        :return:
        """
        # search the target el
        group_list = self.get_fixenhance_left_checkbox_list()
        if group_list is False:
            logger('get group_list fail')
            return False
        # the 2nd one has name
        check_flag = ''
        for x in range(len(group_list)):
            child_wnd = self.get_child_wnd(group_list[x])
            if child_wnd is False:
                logger(f'get child_wnd fail. {x}')
                return False
            if self.get_axtitle(child_wnd[1]) == target:
                check_flag = x
                break
        if check_flag == '':
            logger('get target fail')
            return False
        # start to tag
        child_wnd = self.get_child_wnd(group_list[check_flag])
        if child_wnd is False:
            logger('get child_wnd fail')
            return False
        if self.tap_element(child_wnd[1]):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def tick_fixenhance_compareinsplitpreview(self, option):
        '''
        #old
        top_splitgroup = self.get_pdr_mian_window_top_split_group()
        if top_splitgroup is False:
            logger('get top_splitgroup fail')
            return False
        target = self.search_child_el_by_title(top_splitgroup, 'Compare in split preview')
        if target is False:
            logger('get target fail')
            return False
        '''
        target = self.search_el(self.checkbox_main_enhance_compareinsplitpreview)
        if target is None:
            logger('get target fail')
            return False
        # checkbox handel
        if self.checkbox_handle(target, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('checkbox handle fail')
        return False

    def tap_reset_btn(self):
        if self.tap_locator(self.btn_reset):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def tap_applytoall_btn(self):
        if self.tap_locator(self.btn_applytoall):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

# Key Frame Room
    def tap_keyframe_btn(self):
        if self.tap_locator(self.btn_keyframe):
            # verify
            if self.is_in_keyframe_page():
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap locator fail')
        return False

    def is_in_keyframe_page(self):
        if self.search_el(self.str_keyframe_settings) is not None:
            logger('Done')
            return True
        else:
            logger('search el fail')
        return False

        '''
        #old
        split_group_top_el = self.get_pdr_mian_window_top_split_group()
        if split_group_top_el is False:
            logger('get split_group_top_el fail')
            return False
        child_list = self.get_child_wnd(split_group_top_el)
        if child_list is False:
            logger('get child_list fail')
            return False
        if self.get_axvalue(child_list[0]) == 'Keyframe Settings':
            logger('Done')
            return True
        else:
            logger('get axvalue fail')
        return False
        '''

# main page preview area
    def tap_main_preview_dock_icon(self):
        if self.tap_locator(self.icon_main_preview_dock):
            #verify
            if self.is_in_dock_mode():
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap locator fail')
        return False

    def tap_main_preview_undock_icon(self):
        if self.tap_locator(self.icon_main_preview_undock):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False


    def is_in_dock_mode(self):
        if self.search_el(self.icon_main_preview_undock) is not None:
            logger('Done')
            return True
        else:
            logger('search el fail')
        return False


    # [Jamie add] >> 09/21 Build
    def timeline_split_in_0s(self):
        timeline_0s = {'AXIdentifier': '_NS:18', 'AXValue': '00;00;00'}

        #self.tap_locator(self.icon_Movie_Mode)
        self.tap_locator(self.icon_stop)

        timeline_0s_pos = self.get_locator_pos(timeline_0s)
        range_r_pos = self.get_locator_pos(self.image_timeline_range_r)
        print('timeline_0s_pos',timeline_0s_pos[0],' range_r_pos', range_r_pos[0])
        if timeline_0s_pos[0] == range_r_pos[0]:
            logger('timeline split is in 0s')
            return True
        else:
            logger('timeline split is not in 0s')
            return False

    def check_CropImage_preview(self, ground_truth_folder):
        """
        search mid icon
        """
        pos = self.search_pos_from_image('crop_4_3_4_result check.jpg', ground_truth_folder=ground_truth_folder)
        if pos is False:
            logger('search pos from image fail')
            return False
        if self.drag_mouse(pos, (pos[0] + 5, pos[1] + 5)):
            logger('Done')
            return True
        else:
            logger('drag pos fail')
        return False

    def adjust_CropZoomPan_scalewidth_slider(self, value):
        C_Z_P_dialog = {'AXIdentifier': '_NS:10', 'AXRole': 'AXWindow'}
        C_Z_P_dialog_el = self.search_el(C_Z_P_dialog)
        if C_Z_P_dialog_el is None:
            logger('Not found CropZoomPan element')
            return False

        slider_Width = {'AXIdentifier': '_NS:251', 'AXRole': 'AXSlider'}

        slider_Width_el = self.search_el(slider_Width)
        if slider_Width_el is None:
            logger('Not found slider_Width_el')
            return False

        slider_icon = self.search_child_el_by_role(slider_Width_el, 'AXValueIndicator')
        if slider_icon is False:
            print('get slider_pos fail')
            return False
        else:
            pos_init = self.get_pos(slider_icon)
            print('get slider_pos pass')

        tolerance = [value - 0.1, value + 0.1]
        if self.adjust_element_slider(slider_Width_el, value, min=0.001, max=6.000, tolerance=tolerance):
            logger('Adjust Done')
        else:
            logger('adjust element slider fail')
            return False

        pos_later = self.get_pos(slider_icon)
        if (value > 1) and (pos_init[0] < pos_later[0]):
            logger('verify Pass')
            return True
        elif (value < 1) and (pos_init[0] > pos_later[0]):
            logger('verify Pass')
            return True
        else:
            logger('verify Fail')
            return False

    def select_2_clip(self, pos1):
        if self.multi_select(pos1):
            logger('done')
            return True
        else:
            logger('multi select fail')
            return False

    def Double_click_then_input_value(self, pos, value):
        if not self.click_mouse(pos, times=2):
            logger('Double click pos Fail')
            return False
        time.sleep(1)
        if not self.input_keyboard('backspace'):
            return False
        time.sleep(1)
        if not self.input_text(value):
            return False
        time.sleep(1)
        if not self.input_keyboard('enter'):
            return False
        logger('Input value Done')
        return True

    def adjust_VideoSpeed_SpeedMultiplier(self, value):
        VideoSpeed_dialog = {'AXIdentifier': '_NS:10', 'AXRole': 'AXWindow'}
        V_S_dialog_el = self.search_el(VideoSpeed_dialog)
        if V_S_dialog_el is None:
            logger('Not found VideoSpeed element')
            return False

        #SpeedMultiplier_slider = {'AXIdentifier': '_NS:109', 'AXRole': 'AXSlider'} # 0921 R8 Build
        SpeedMultiplier_slider = {'AXIdentifier': '_NS:67', 'AXRole': 'AXSlider'}   # v2219 Build

        SpeedMultiplier_slider_el = self.search_el(SpeedMultiplier_slider)
        if SpeedMultiplier_slider_el is None:
            logger('Not found SpeedMultiplier_slider_el')
            return False

        slider_icon = self.search_child_el_by_role(SpeedMultiplier_slider_el, 'AXValueIndicator')
        if slider_icon is False:
            print('get slider_pos fail')
            return False
        else:
            pos_init = self.get_pos(slider_icon)
            print('get slider_pos pass')

        Slider_Edit_Field = {'AXIdentifier': 'spinEditTextField', 'AXRole': 'AXTextField', 'AXValue': '1.000'}
        Slider_Edit_Field_pos = self.get_locator_pos(Slider_Edit_Field)
        if not self.click_mouse(Slider_Edit_Field_pos, times=2):
            logger('Double click Slider Edit Text Field Fail')
            return False
        time.sleep(1)
        if not self.input_keyboard('backspace'):
            return False
        time.sleep(1)
        if not self.input_text(value):
            return False
        time.sleep(1)
        if not self.input_keyboard('enter'):
            return False
        return True

    def get_FixEnhance_Left_group_list(self):
        """
        Group: Slider, Timecode, Duration, In Position, Out Position
        :return:
        """

        Fix_Enhance_Left_Group_Area = {'AXIdentifier': '_NS:205'}

        el = self.search_el(Fix_Enhance_Left_Group_Area)
        if el is False:
            logger('get el fail')
            return False

        group_list = self.search_child_el_by_role(el, 'AXGroup')
        if group_list is False:
            logger('get group_list fail')
            return False
        logger('Done')
        return group_list


    def get_FixEnhance_Adjustment_el(self, value):
        """
        Structure: Value = 0 for White Balance
                   Value = 1 for Lens Correction
                   Value = 2 for Audio Denoise
                   Value = 3 for Color Adjustment
        :return:
        """
        group_list = self.get_FixEnhance_Left_group_list()
        if group_list is False:
            logger('get group_list fail')
            return False

        group = group_list[value]

        AXButton_el = self.search_child_el_by_role(group, 'AXButton')
        if AXButton_el is False:
            logger('get unknown_el fail')
            return False

        # Due to group has two children for AXButton
        # Child 0 for checkbox
        # Child 1 for string (e.g. White Balance / Lens Correction / Audio Denoise)
        item_el = AXButton_el[1]

        return item_el

    def get_WhiteBalance_ColorTemperature_TextField_el(self):
        """
        Description: <case 1> Get White Balance > Color Temperature TextField (First TextField)
                     <case 2> Get Lens Correction > FishEye distortion TextField (First TextField)
        :return:
        """

        Fix_Enahcne_Library = {'AXIdentifier': 'IDD_LIBRARY'}

        Fix_Enahcne_Library_el = self.search_el(Fix_Enahcne_Library)
        if Fix_Enahcne_Library_el is None:
            logger('get Fix_Enahcne_Library_el fail')
            return False

        ScrollArea_list = self.search_child_el_by_role(Fix_Enahcne_Library_el, 'AXScrollArea')
        if ScrollArea_list is False:
            logger('get ScrollArea_list fail')
            return False
        try:
            ScrollArea_Right = ScrollArea_list[1]
            print('get ScrollArea_Right pass')
        except Exception as e:
            logger(f'Exception {e}')
            return False

        # self.MWC.get_child_wnd(ScrollArea_Right)

        WhiteBalance_group = self.search_child_el_by_role(ScrollArea_Right, 'AXGroup')
        if WhiteBalance_group is False:
            logger('get ScrollArea_list fail')
            return False
        else:
            print('get WhiteBalance_group pass')

        Inner_group = self.search_child_el_by_role(WhiteBalance_group, 'AXGroup')
        if Inner_group is False:
            logger('get Inner_group fail')
            return False

        ColorTemperature_TextField_group = Inner_group[0] # 0 = lst child, for ColorTemperature
                                                          # 1 = 2nd child, for Tint

        TextField_el = self.search_child_el_by_role(ColorTemperature_TextField_group, 'AXTextField')
        if TextField_el is False:
            logger('get TextField_el fail')
            return False
        else:
            return TextField_el

# main fix/enhance
    def tap_main_fixenhance_whitebalance_btn(self):
        if self.tap_locator(self.str_main_enhance_white_balance):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def tap_main_fixenhance_lenscorrection_btn(self):
        if self.tap_locator(self.str_main_enhance_lens_correction):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def tap_main_fixenhance_audiodenoise_btn(self):
        if self.tap_locator(self.str_main_enahnce_audio_denoise):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def tap_main_fixenhance_coloradjustment_btn(self):
        if self.tap_locator(self.str_main_enhance_color_adjustment):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def get_main_fixenhance_control_group_el(self):
        """
        Structure: upper split group -> split group -> group -> scroll area -> control group(this function)
        :return:
        """
        top_el = self.get_pdr_mian_window_top_split_group()
        if top_el is False:
            logger('get top_el fail')
            return False
        group_list = self.search_child_el_by_role(top_el, 'group')
        if group_list is False:
            logger('get group_list fail')
            return False
        try:
            target_group = group_list[0]
        except:
            logger('assign group fail')
            return False
        scrollarea_list = self.search_child_el_by_role(target_group, 'AXScrollArea')
        if scrollarea_list is False:
            logger('get scrollarea_list fail')
            return False
        try:
            target_scrollarea = scrollarea_list[1]
        except:
            logger('assign scroll area fail')
            return False
        control_group = self.search_child_el_by_role(target_scrollarea, 'AXGroup')
        if control_group is False:
            logger('get control_group fail')
            return False
        logger('Done')
        return control_group

    def get_main_fixenhance_whitebalance_slider_list(self):
        control_group = self.get_main_fixenhance_control_group_el()
        if control_group is False:
            logger('get control_group fail')
            return False
        slider_list = self.search_child_el_by_role(control_group, 'AXSlider')
        if slider_list is False:
            logger('get slider_list fail')
            return False
        logger('Done')
        return slider_list

    def adjust_main_fixenhance_whiteblance_colortemperature_slider(self, value):
        slider_list = self.get_main_fixenhance_whitebalance_slider_list()
        if slider_list is False:
            logger('get slider_list fail')
            return False
        try:
            target_slider = slider_list[0]
        except:
            logger('assign slider index fail')
            return False
        tolerance = [value - 1, value + 1]
        if self.adjust_element_slider(target_slider, value, min=1, max=100, tolerance=tolerance):
            logger('Done')
            return True
        else:
            logger('adjust slider fail')
        return False

    def get_main_fixenhance_lenscorrection_slider_list(self):
        control_group = self.get_main_fixenhance_control_group_el()
        if control_group is False:
            logger('get control_group fail')
            return False
        slider_list = self.search_child_el_by_role(control_group, 'AXSlider')
        if slider_list is False:
            logger('get slider_list fail')
            return False
        logger('Done')
        return slider_list

    def adjust_main_fixenhance_lenscorrection_fisheye_slider(self, value):
        slider_list = self.get_main_fixenhance_whitebalance_slider_list()
        if slider_list is False:
            logger('get slider_list fail')
            return False
        try:
            target_slider = slider_list[0]
        except:
            logger('assign slider index fail')
            return False
        tolerance = [value - 4, value + 4]
        if self.adjust_element_slider(target_slider, value, min=-100, max=100, tolerance=tolerance):
            logger('Done')
            return True
        else:
            logger('adjust slider fail')
        return False

    def get_main_fixenhance_coloradjustment_slider_list(self):
        """
        the structure is not the same as others, group -> group(s) -> AXUnknown -> slider
        :return:
        """
        control_group = self.get_main_fixenhance_control_group_el()
        if control_group is False:
            logger('get control_group fail')
            return False
        sub_group_list = self.search_child_el_by_role(control_group, 'AXGroup')
        if sub_group_list is False:
            logger('get sub_group_list fail')
            return False
        slider_list = []
        for x in range(len(sub_group_list)):
            child_wnd = self.search_child_el_by_role(sub_group_list[x], 'AXUnknown')
            if child_wnd is False:
                continue
            slider_el = self.search_child_el_by_role(child_wnd, 'AXSlider')
            if slider_el is False:
                continue
            slider_list.append(slider_el)
        logger('Done')
        return slider_list


    def adjust_main_fixenhance_coloradjustment_exposure_slider(self, value):
        slider_list = self.get_main_fixenhance_coloradjustment_slider_list()
        if slider_list is False:
            logger('get slider_list fail')
            return False
        try:
            target_slider = slider_list[0]
        except:
            logger('assign slider index fail')
            return False
        tolerance = [value - 4, value + 4]
        if self.adjust_element_slider(target_slider, value, min=0, max=200, tolerance=tolerance):
            logger('Done')
            return True
        else:
            logger('adjust slider fail')
        return False

# keyframe - main page
    def tap_main_keyframe_btn(self):
        """
        in effect settings
        :return:
        """
        if self.tap_locator(self.btn_keyframe):
            # verify
            time.sleep(1)
            if self.search_el(self.str_keyframe_settings) is not None:
                logger('Done')
                return True
            else:
                logger('verify fail')
        else:
            logger('tap locator fail')
        return False


    # keyframe structure: top -> group(0)(this function) -> scrollarea(1)(left part) / scrollarea(0)(timeline)
                                            #scrollarea(2)(library)
    # left scroll area structure: scrollarea -> outlinerow(0) fix/enahnce
                                            #-> outlinerow(1) clip attribute
    #                                   => Cell(0) => fix/ enhance button(0),disclosure triangle
    def get_main_keyframe_el(self):
        top_el = self.get_pdr_mian_window_top_split_group()
        if top_el is False:
            logger('get top_el fail')
            return False
        group_list = self.search_child_el_by_role(top_el, 'group')
        if group_list is False:
            logger('get group_list fail')
            return False
        try:
            target_el = group_list[0]
        except:
            logger('assign index fail')
            return False
        logger('Done')
        return target_el

    def get_main_keyframe_left_scroll_area_el(self):
        group_el = self.get_main_keyframe_el()
        if group_el is False:
            logger('get group_el fail')
            return False
        scrollarea_list = self.search_child_el_by_role(group_el, 'AXScrollArea')
        if scrollarea_list is False:
            logger('get scrollarea_list fail')
            return False
        try:
            target_el = scrollarea_list[1]
        except:
            logger('assign index fail')
            return False
        logger('Done')
        return target_el

    def get_main_keyframe_left_outline_el(self):
        scrollarea_el = self.get_main_keyframe_left_scroll_area_el()
        if scrollarea_el is False:
            logger('get scrollarea_el fail')
            return False
        outline_el = self.search_child_el_by_role(scrollarea_el, 'AXOutline')
        if outline_el is False:
            logger('get outline_el fail')
            return False
        logger('Done')
        return outline_el

    def get_main_keyframe_left_outlinerow_list(self):
        outline = self.get_main_keyframe_left_outline_el()
        if outline is False:
            logger('get outline fail')
            return False
        outlinerow_list = self.search_child_el_by_role(outline, 'AXRow')
        if outlinerow_list is False:
            logger('get outlinerow_list fail')
            return False
        logger('Done')
        return outlinerow_list

    def get_main_keyframe_left_triangle(self, option):
        """
        :param option:
        :return:
        """
        # outline row -> cell
        outlinerow_list = self.get_main_keyframe_left_outlinerow_list()
        if outlinerow_list is False:
            logger('get outlinerow_list fail')
            return False
        target_flag = ''
        for x in range(len(outlinerow_list)):
            # get cell
            cell = self.search_child_el_by_role(outlinerow_list[x], 'AXCell')
            if cell is False:
                continue
            text_el = self.search_child_el_by_role(cell, 'AXButton')
            if text_el is False:
                continue
            if self.get_axtitle(text_el) == option:
                target_flag = x
                break
        if target_flag == '':
            logger('get target_flag fail')
            return False
        target_triangle_el = self.search_child_el_by_role(self.search_child_el_by_role(outlinerow_list[target_flag], 'AXCell'), 'AXDisclosureTriangle')
        if target_triangle_el is False:
            logger('get target_triangle_el fail')
            return False
        logger('Done')
        return target_triangle_el

    def get_main_keyframe_left_control_cell(self, name):
        # outline row -> cell
        outlinerow_list = self.get_main_keyframe_left_outlinerow_list()
        if outlinerow_list is False:
            logger('get outlinerow_list fail')
            return False
        target_flag = ''
        for x in range(len(outlinerow_list)):
            # get cell
            cell = self.search_child_el_by_role(outlinerow_list[x], 'AXCell')
            if cell is False:
                continue
            text_el = self.search_child_el_by_role(cell, 'AXStaticText')
            if text_el is False:
                continue
            if self.get_axvalue(text_el) == name:
                target_flag = x
                break
            try:
                if self.get_axvalue(text_el[0]) == name:
                    target_flag = x
                    break
            except:
                continue
        if target_flag == '':
            logger('get target_flag fail')
            return False
        target_cell_el = self.search_child_el_by_role(outlinerow_list[target_flag], 'AXCell')
        if target_cell_el is False:
            logger('get target_cell_el fail')
            return False
        logger('Done')
        return target_cell_el

    def add_main_keyframe_left_coloradjustment_keyframe(self, name):
        """
        the btn is -2
        :param name:
        :return:
        """
        target_cell_el = self.get_main_keyframe_left_control_cell(name)
        if target_cell_el is False:
            logger('get target_cell_el fail')
            return False
        btn_list = self.search_child_el_by_role(target_cell_el, 'AXButton')
        try:
            target_btn = btn_list[-2]
        except:
            logger('assign index fail')
            return False
        if self.tap_element(target_btn):
            logger('Done')
            return True
        else:
            logger('tap el fail')
        return False

    def add_main_keyframe_left_clipattributes_scale_keyframe(self, name):
        """
        the btn is -2
        :param name:
        :return:
        """
        target_cell_el = self.get_main_keyframe_left_control_cell(name)
        if target_cell_el is False:
            logger('get target_cell_el fail')
            return False
        btn_list = self.search_child_el_by_role(target_cell_el, 'AXButton')
        try:
            target_btn = btn_list[2]
        except:
            logger('assign index fail')
            return False
        if self.tap_element(target_btn):
            logger('Done')
            return True
        else:
            logger('tap el fail')
        return False

    def adjust_main_keyframe_left_coloradjustment_slider(self, name, value, min=1, max=100):
        cell_el = self.get_main_keyframe_left_control_cell(name)
        if cell_el is False:
            logger('get cell_el fail')
            return False
        slider = self.search_child_el_by_role(cell_el, 'AXSlider')
        if slider is False:
            logger('get slider fail')
            return False
        tolerance = [value - 5, value + 5]
        if self.adjust_element_slider(slider, value, min=min, max=max, tolerance=tolerance):
            logger('Done')
            return True
        else:
            logger('adjust slider fail')
        return False

    def add_main_keyframe_left_clipattributes_position_keyframe(self, name):
        """
        the btn is -2
        :param name:
        :return:
        """
        target_cell_el = self.get_main_keyframe_left_control_cell(name)
        if target_cell_el is False:
            logger('get target_cell_el fail')
            return False
        btn_list = self.search_child_el_by_role(target_cell_el, 'AXButton')
        try:
            target_btn = btn_list[2]
        except:
            logger('assign index fail')
            return False
        if self.tap_element(target_btn):
            logger('Done')
            return True
        else:
            logger('tap el fail')
        return False

    def add_main_keyframe_left_clipattributes_rotation_keyframe(self):
        """
        the btn is -2
        :param name:
        :return:
        """
        target_cell_el = self.get_main_keyframe_left_control_cell('Rotation')
        if target_cell_el is False:
            logger('get target_cell_el fail')
            return False
        btn_list = self.search_child_el_by_role(target_cell_el, 'AXButton')
        try:
            target_btn = btn_list[2]
        except:
            logger('assign index fail')
            return False
        if self.tap_element(target_btn):
            logger('Done')
            return True
        else:
            logger('tap el fail')
        return False

    def add_main_keyframe_left_clipattributes_freeform_keyframe(self):
        """
        the btn is -2
        :param name:
        :return:
        """
        target_cell_el = self.get_main_keyframe_left_control_cell('Freeform top-left position')
        if target_cell_el is False:
            logger('get target_cell_el fail')
            return False
        btn_list = self.search_child_el_by_role(target_cell_el, 'AXButton')
        try:
            target_btn = btn_list[2]
        except:
            logger('assign index fail')
            return False
        if self.tap_element(target_btn):
            logger('Done')
            return True
        else:
            logger('tap el fail')
        return False

    def tap_main_keyframe_left_clipattributes_freeform_up(self, option):
        cell_el = self.get_main_keyframe_left_control_cell('Freeform top-left position')
        if cell_el is False:
            logger('get cell_el fail')
            return False
        group_list = self.search_child_el_by_role(cell_el, 'AXGroup')
        if group_list is False:
            logger('get group_list fail')
            return False
        target_slider = group_list[0]
        btn_list = self.search_child_el_by_role(target_slider, 'AXButton')
        if btn_list is False:
            logger('get btn_list fail')
            return False
        if option == 'up':
            target_btn = btn_list[0]
        elif option == 'down':
            target_btn = btn_list[1]
        if self.tap_element(target_btn):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False


    def tap_main_keyframe_left_clipattributes_rotation_up(self, option):
        cell_el = self.get_main_keyframe_left_control_cell('Rotation')
        if cell_el is False:
            logger('get cell_el fail')
            return False
        group_list = self.search_child_el_by_role(cell_el, 'AXGroup')
        if group_list is False:
            logger('get group_list fail')
            return False
        target_slider = group_list[0]
        btn_list = self.search_child_el_by_role(target_slider, 'AXButton')
        if btn_list is False:
            logger('get btn_list fail')
            return False
        if option == 'up':
            target_btn = btn_list[0]
        elif option == 'down':
            target_btn = btn_list[1]
        if self.tap_element(target_btn):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def add_main_keyframe_left_clipattributes_opacity_keyframe(self):
        """
        the btn is -2
        :param name:
        :return:
        """
        target_cell_el = self.get_main_keyframe_left_control_cell('Opacity')
        if target_cell_el is False:
            logger('get target_cell_el fail')
            return False
        btn_list = self.search_child_el_by_role(target_cell_el, 'AXButton')
        try:
            target_btn = btn_list[2]
        except:
            logger('assign index fail')
            return False
        if self.tap_element(target_btn):
            logger('Done')
            return True
        else:
            logger('tap el fail')
        return False

    def adjust_main_keyframe_left_clipattributes_slider(self, value, min=0, max=100):
        cell_el = self.get_main_keyframe_left_control_cell('Opacity')
        if cell_el is False:
            logger('get cell_el fail')
            return False
        slider = self.search_child_el_by_role(cell_el, 'AXSlider')
        if slider is False:
            logger('get slider fail')
            return False
        tolerance = [value - 5, value + 5]
        if self.adjust_element_slider(slider, value, min=min, max=max, tolerance=tolerance):
            logger('Done')
            return True
        else:
            logger('adjust slider fail')
        return False


    def tap_main_keyframe_left_clipattributes_position_up(self, option):
        cell_el = self.get_main_keyframe_left_control_cell('X')
        if cell_el is False:
            logger('get cell_el fail')
            return False
        group_list = self.search_child_el_by_role(cell_el, 'AXGroup')
        if group_list is False:
            logger('get group_list fail')
            return False
        target_slider = group_list[0]
        btn_list = self.search_child_el_by_role(target_slider, 'AXButton')
        if btn_list is False:
            logger('get btn_list fail')
            return False
        if option == 'up':
            target_btn = btn_list[0]
        elif option == 'down':
            target_btn = btn_list[1]
        if self.tap_element(target_btn):
            logger('Done')
            return True
        else:
            logger('tap element fail')
        return False

    def adjust_main_keyframe_left_whitebalance_slider(self, name, value, min=1, max=100):
        cell_el = self.get_main_keyframe_left_control_cell(name)
        if cell_el is False:
            logger('get cell_el fail')
            return False
        slider_list = self.search_child_el_by_role(cell_el, 'AXSlider')
        if slider_list is False:
            logger('get slider fail')
            return False
        target_slider = slider_list[0]
        tolerance = [value - 5, value + 5]
        if self.adjust_element_slider(target_slider, value, min=min, max=max, tolerance=tolerance):
            logger('Done')
            return True
        else:
            logger('adjust slider fail')
        return False

    def adjust_main_keyframe_left_clipattributes_scale_slider(self, name, value, min=1, max=100):
        cell_el = self.get_main_keyframe_left_control_cell(name)
        if cell_el is False:
            logger('get cell_el fail')
            return False
        slider_list = self.search_child_el_by_role(cell_el, 'AXSlider')
        if slider_list is False:
            logger('get slider fail')
            return False
        target_slider = slider_list[0]
        tolerance = [value - 1, value + 1]
        if self.adjust_element_slider(target_slider, value, min=min, max=max, tolerance=tolerance):
            logger('Done')
            return True
        else:
            logger('adjust slider fail')
        return False

    def add_main_keyframe_left_whitebalance_keyframe(self, name):
        """
        the btn is -2
        :param name:
        :return:
        """
        target_cell_el = self.get_main_keyframe_left_control_cell(name)
        if target_cell_el is False:
            logger('get target_cell_el fail')
            return False
        btn_list = self.search_child_el_by_role(target_cell_el, 'AXButton')
        try:
            target_btn = btn_list[-3]
        except:
            logger('assign index fail')
            return False
        if self.tap_element(target_btn):
            logger('Done')
            return True
        else:
            logger('tap el fail')
        return False

    def express_fold_main_keyframe_left_option(self, option, value):
        target_el = self.get_main_keyframe_left_triangle(option)
        if target_el is False:
            logger('get target_el fail')
            return False
        if self.checkbox_handle(target_el, value, element_mode=1):
            logger('Done')
            return True
        else:
            logger('checkbox handle fail')
        return False

    def get_main_keyframe_left_scroll_bar(self):
        scrollarea_el = self.get_main_keyframe_left_scroll_area_el()
        if scrollarea_el is False:
            logger('get scrollarea_el fail')
            return False
        target_scrollbar = self.search_child_el_by_role(scrollarea_el, 'AXScrollBar')
        if target_scrollbar is False:
            logger('get target_scrollbar fail')
            return False
        logger('Done')
        return target_scrollbar

    def scroll_main_keyframe_left_scroll_bar(self, option):
        """
        :param option: up/down
        :return:
        """
        scroll_bar = self.get_main_keyframe_left_scroll_bar()
        if scroll_bar is False:
            logger('get scroll_bar fail')
            return False
        pos = self.get_pos(scroll_bar)
        if pos is False:
            logger('get pos fail')
            return False
        if option not in ['up', 'down']:
            logger('incorrect parameter')
            return False
        mid_pos = (int(pos[0] + pos[2] / 2), int(pos[1] + pos[3] / 2))
        up_pos = (int(pos[0] + pos[2] / 2), int(pos[1] + pos[3] / 4))
        down_pos = (int(pos[0] + pos[2] / 2), int(pos[1] + pos[3] * 3 / 4))
        # start to drag
        if option == 'up':
            if self.drag_mouse(mid_pos, up_pos):
                logger('Done')
                return True
            else:
                logger('drag mouse fial(1)')
                return False
        else:
            if self.drag_mouse(mid_pos, down_pos):
                logger('Done')
                return True
            else:
                logger('drag mouse fial(2)')
                return False

# timeline operater
    icon_timeline_range_right = {'AXIdentifier': 'IDC_TIMELINE_IMAGE_RSINDICATOR_RIGHT', 'AXRole': 'AXImage'}
    btn_timeline_tipsarea_copy = {'AXIdentifier': 'IDC_TIPSAREA_BTN_COPY', 'AXRole': 'AXButton'}
    btn_timeline_tipsarea_paste = {'AXIdentifier': 'IDC_TIPSAREA_BTN_PASTE', 'AXRole': 'AXButton'}
    btn_timeline_tipsarea_cut = {'AXIdentifier': 'IDC_TIPSAREA_BTN_CUT', 'AXRole': 'AXButton'}
    btn_timeline_tipsarea_remove = {'AXIdentifier': 'IDC_TIPSAREA_BTN_REMOVE', 'AXRole': 'AXButton'}
    btn_timeline_tipsarea_produce_range = {'AXIdentifier': 'IDC_TIPSAREA_BTN_PRODUCE_RANGE', 'AXRole': 'AXButton'}
    btn_timeline_tipsarea_render_preview = {'AXIdentifier': 'IDC_TIPSAREA_BTN_RENDER_PREVIEW', 'AXRole': 'AXButton'}
    btn_timeline_tipsarea_lock_range = {'AXIdentifier': 'IDC_TIPSAREA_BTN_LOCK_RANGE', 'AXRole': 'AXButton'}


    def drag_main_timeline_range_right(self):
        el = self.search_el(self.icon_timeline_range_right)
        if el is None:
            logger('get el fail')
            return False
        org_pos = self.get_pos(el)
        if org_pos is None:
            logger('get org_pos fail')
            return False
        start_pos = (org_pos[0] + org_pos[2] * 2 / 3, org_pos[1] + org_pos[3] / 2)
        end_pos = (org_pos[0] + org_pos[2] + 50, org_pos[1] + org_pos[3] / 2)
        if self.drag_mouse(start_pos, end_pos):
            logger('Done')
            return True
        else:
            logger('drag mouse fail')
        return False

    def tap_main_timeline_range_control_copy(self):
        if self.tap_locator(self.btn_timeline_tipsarea_copy):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False


    def tap_main_timeline_range_control_paste(self):
        if self.tap_locator(self.btn_timeline_tipsarea_paste):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False


    def tap_main_timeline_range_control_cut(self):
        if self.tap_locator(self.btn_timeline_tipsarea_cut):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False


    def tap_main_timeline_range_control_remove(self):
        if self.tap_locator(self.btn_timeline_tipsarea_remove):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def tap_main_timeline_range_control_producerange(self):
        if self.tap_locator(self.btn_timeline_tipsarea_produce_range):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def tap_main_timeline_range_control_renderpreview(self):
        if self.tap_locator(self.btn_timeline_tipsarea_render_preview):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def tap_main_timeline_range_control_lockrange(self):
        if self.tap_locator(self.btn_timeline_tipsarea_lock_range):
            logger('Done')
            return True
        else:
            logger('tap locator fail')
        return False

    def select_youtube_category_drop_down_menu(self, option):
        target_el = self.search_el(self.youtube_category_el)
        if target_el is None:
            logger('search el fail')
            return False
        if self.select_drop_down_list(target_el, option, element_mode=1):
            logger('Done')
            return True
        else:
            logger('select drop down list fail')
        return False

    def check_preview_animation(self):
        # get preview area
        preview_area = self.get_preview_area()
        if not preview_area:
            return False

        # check animation
        folder_path = "tmp"
        if not os.path.isfile(folder_path): os.makedirs(folder_path,exist_ok=True)
        img1 = os.path.abspath(folder_path + '/preview_before.png')
        img2 = os.path.abspath(folder_path + '/preview_after.png')
        if self.snapshot(img1, crop=preview_area):
            time.sleep(1)
            if self.snapshot(img2, crop=preview_area) and \
                    not self.compare(img1, img2):
                logger('check_preview_animation - pass')
                return True
            else:
                logger('check_preview_animation - fail')
                return False
        else:
            return False

    def check(self):
        res = self.search_all_el(self.btn_ok)
        logger(res)
