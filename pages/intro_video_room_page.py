import time, datetime, os, copy

from .base_page import BasePage
from .main_page import Main_Page
from ATFramework.utils import logger
from .locator import locator as L
from reportportal_client import step

DELAY_TIME = 1 # sec

def _set_radio(self, _locator_radio_group, option=1, get_status=False):
    try:
        target = self.exist(_locator_radio_group[option-1])
        result = bool(int(target.AXValue))
        if get_status:
            return int(result)+1
        if not result:
            target.press()
            time.sleep(DELAY_TIME*1)
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        raise Exception(f'Exception occurs. log={e}')
    return True

def _set_option(self, _locator_cbx, _locator_group, option=1, get_status=False, path=None):
    try:
        target = self.exist(_locator_cbx)
        current_title = str(target.AXTitle)
        if get_status:
            return current_title
        else:
            self.click(_locator_cbx)
            time.sleep(DELAY_TIME*1)
            self.click(_locator_group[option-1])
            time.sleep(DELAY_TIME*1)
        if path is not None:
            time.sleep(DELAY_TIME * 1)
            self.select_file(path)
            time.sleep(DELAY_TIME * 1)
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        raise Exception(f'Exception occurs. log={e}')
    return True

def _set_color(self, HexColor):
    try:
        self.color_picker_switch_category_to_RGB()
        self.double_click(L.title_designer.colors.input_hex_color)
        time.sleep(DELAY_TIME)
        self.exist(L.title_designer.colors.input_hex_color).sendKeys(HexColor)
        time.sleep(DELAY_TIME)
        self.keyboard.enter()
        time.sleep(DELAY_TIME*2)
        self.click(L.title_designer.colors.btn_close)
        time.sleep(DELAY_TIME)
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        return False
    return True

def _get_color(self):
    try:
        self.color_picker_switch_category_to_RGB()
        time.sleep(DELAY_TIME)
        current_hex = self.exist(L.title_designer.colors.input_hex_color)
        time.sleep(DELAY_TIME)
        self.exist(L.title_designer.colors.btn_close).press()
        time.sleep(DELAY_TIME)
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        return False
    return current_hex.AXValue

def _set_edittext(self, _locator, value):
    try:
        target = self.exist(_locator)
        self.el_click(target)
        time.sleep(DELAY_TIME*1)
        target.AXValue = str(value)
        time.sleep(DELAY_TIME*1)
        self.keyboard.enter()
        time.sleep(DELAY_TIME*1)
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        return False
    return True

class Intro_Video_Room(Main_Page, BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.replace_media = self.Replace_Media(*args, **kwargs)
        self.crop_zoom_pan = self.CropZoomPan(*args, **kwargs)
        self.background_music = self.Background_Music(*args, **kwargs)
        self.general_title = self.General_Title(*args, **kwargs)
        self.color_filter = self.Color_Filter(*args, **kwargs)
        self.backdrop_settings = self.Backdrop_Settings(*args, **kwargs)
        self.motion_graphics = self.Motion_Graphics(*args, **kwargs)
        self.duration_setting = self.Duration_Setting(*args, **kwargs)
        self.image = self.Image(*args, **kwargs)
        self.my_profile = self.My_Profile(*args, **kwargs)
        self.share_temp = self.Share_Temp(*args, **kwargs)
        self.volume_settings = self.Volume_Settings(*args, **kwargs)

    @step('[Action][Intro Video Room] Enter Intro Video Room')
    def enter_intro_video_room(self):
        img_collection_view_before = self.snapshot(L.media_room.library_listview.main_frame)
        time.sleep(DELAY_TIME)
        self.exist_click(L.intro_video_room.room_entry.btn_intro_video_room)
        time.sleep(DELAY_TIME)
        img_collection_view_after = self.snapshot(L.media_room.library_listview.main_frame)
        # verify is collection view frame is changed by snapshot
        result_verify = self.compare(img_collection_view_before, img_collection_view_after)
        if result_verify:
            logger(f'Fail to enter Intro Video room')
            raise Exception(f'Fail to enter Intro Video room')

        time.sleep(DELAY_TIME)
        if self.is_exist(L.intro_video_room.dialog_quick_tutorial):
            logger('Pop up Quick Tutorial dialog - press Esc to close it.')
            self.press_esc_key()
        time.sleep(DELAY_TIME)

        return True

    @step('[Action][Intro Video Room] Enter [Season Theme] category')
    def enter_season_theme_category(self, strName):
        time.sleep(1)
        self.exist(L.intro_video_room.category_scroll_bar).AXValue = 0
        time.sleep(1)
        self.click_specific_tag(strName)
        time.sleep(DELAY_TIME)

        return True

    def click_Theme_specific_category(self, strName):
        el_option = ['', 'Beauty', 'Business', 'Design', 'Education', 'Event', 'Family', 'Fashion', 'Food',
                     'Gaming', 'Health', 'Holiday', 'Life', 'Love', 'Music', 'Nature', 'Pets', 'Repair', 'Retro',
                     'Season', 'Social Media', 'Sport', 'Technology', 'Travel']

        # if Theme category is fold, should unfold
        unfold_value = self.exist(L.intro_video_room.explore_view_region.triangle_theme).AXValue
        logger(unfold_value)

        if unfold_value == 0:
            self.click(L.intro_video_room.explore_view_region.triangle_theme)
            time.sleep(DELAY_TIME)

        keep_current_X = -1
        for x in range(25):
            if el_option[x] == strName:
                keep_current_X = x
                break

        if keep_current_X == -1:
            logger(f'Cannot Find {strName} category')
            raise Exception

        if keep_current_X > 14:
            self.exist(L.intro_video_room.category_scroll_bar).AXValue = 0.75
        else:
            self.exist(L.intro_video_room.category_scroll_bar).AXValue = 0.41

        items = self.exist(L.intro_video_room.explore_view_region.category_items)
        for item in items:
            if item.AXValue.startswith(f"{strName} ("):
                self.mouse.click(*item.center)
                return True

        logger('Cannot find the specific category under Theme')
        return False

    @step('[Action][Intro Video Room] Click specific category by name')
    def click_intro_specific_category(self, strName):
        el_option = ['', 'Beauty', 'Black & White', 'Business', 'Design', 'Education', 'Event', 'Family', 'Fashion',
                     'Food', 'Fun & Playful', 'Gaming', 'Handwritten', 'Health', 'Holiday', 'Life', 'Love',
                     'Minimalist', 'Modern', 'Music', 'Nature', 'Pets', 'Repair', 'Retro', 'Season', 'Social Media',
                     'Sport', 'Technology', 'Travel']

        keep_current_X = -1
        for x in range(29):
            if el_option[x] == strName:
                keep_current_X = x
                break

        if keep_current_X == -1:
            logger(f'Cannot Find {strName} category')
            raise Exception

        if keep_current_X > 11:
            self.exist(L.intro_video_room.category_scroll_bar).AXValue = 1
        else:
            self.exist(L.intro_video_room.category_scroll_bar).AXValue = 0.1

        items = self.exist(L.intro_video_room.explore_view_region.category_items)
        for item in items:
            if item.AXValue.startswith(f"{strName} ("):
                self.mouse.click(*item.center)
                return True

        logger('Cannot find the specific category under Theme')
        return False

    def click_Style_specific_category(self, strName):

        # if Theme category is unfold, should fold
        unfold_value = self.exist(L.intro_video_room.explore_view_region.triangle_theme).AXValue
        logger(unfold_value)

        if unfold_value:
            self.click(L.intro_video_room.explore_view_region.triangle_theme)
            time.sleep(DELAY_TIME)

        # if Style category is fold, should unfold
        unfold_status = self.exist(L.intro_video_room.explore_view_region.triangle_style).AXValue
        logger(unfold_status)

        if not unfold_status:
            self.click(L.intro_video_room.explore_view_region.triangle_style)
            time.sleep(DELAY_TIME)

        items = self.exist(L.intro_video_room.explore_view_region.category_items)
        for item in items:
            if item.AXValue.startswith(f"{strName} ("):
                self.mouse.click(*item.center)
                return True

        logger('Cannot find the specific category under Style')
        return False

    def get_Video_Intro_sub_category_string(self, index):
        # For 20.7.4219 : Merge "Cyberlink" and "Discover" to (Video Intro Template) category
        # index = 1, return Cyberlink
        # index = 2, return Family
        try:
            el_option = ['','Cyberlink', 'Beauty', 'Black & White', 'Business', 'Design', 'Education', 'Event', 'Family',
                         'Fashion', 'Food', 'Fun & Playful', 'Gaming', 'Handwritten', 'Health', 'Holiday', 'Life', 'Love',
                         'Minimalist', 'Modern', 'Music', 'Nature', 'Pets', 'Repair', 'Retro', 'Season', 'Social Media',
                          'Sport', 'Technology',  'Travel']
            result = -1
            result = el_option[index]

            if result == "":
                logger(f' Parameter: {index} is invalid')
                raise Exception

            # If access category > 16 (Life), should scroll down
            if index > 16:
                self.exist(L.intro_video_room.category_scroll_bar).AXValue = 1
                time.sleep(DELAY_TIME*2)
            elif index < 17:
                # If access category < 17 (Love), should scroll up
                self.exist(L.intro_video_room.category_scroll_bar).AXValue = 0
                time.sleep(DELAY_TIME*2)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return result

    def get_Discover_sub_category_string(self, index):
        # index = 1, return Travel
        # index = 2, return Family
        try:
            el_option = ['','Travel', 'Family', 'Social Media', 'Sport', 'Holiday', 'Season', 'Technology', 'Retro', 'Music',
                         'Nature', 'Food', 'Beauty', 'Fashion', 'Business', 'Pets', 'Education', 'Life', 'Health', 'Event',
                         'Love', 'Design', 'Fun & Playful', 'Modern', 'Minimalist', 'Black & White', 'Handwritten',
                         'Gaming', 'Repair']
            result = -1
            result = el_option[index]

            if result == "":
                logger(f' Parameter: {index} is invalid')
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return result

    def drag_scroll_bar_for_template(self, value):
        try:
            time.sleep(DELAY_TIME*3)
            self.exist(L.intro_video_room.scroll_bar).AXValue = float(value)
            time.sleep(DELAY_TIME)
            # Verify Step
            if float(value) == self.exist(L.intro_video_room.scroll_bar).AXValue:
                return True
            else:
                return False
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def select_intro_template(self, index):
        try:
            if index < 1:
                logger('Invalid index')
                return False
            self.activate()
            time.sleep(DELAY_TIME*2)
            value = index - 1
            logger(value)
            if index < 21:
                x, y = self.exist({"AXIdentifier": "LibraryCollectionViewItem", 'index': value}).center
                logger('111')
            else:
                check_step_1 = value % 10
                value = check_step_1 + 5
                x, y = self.exist({"AXIdentifier": "LibraryCollectionViewItem", 'index': value}).center
            '''    
            elif 20 < index < 31:
                value = value - 15
                x, y = self.exist({"AXIdentifier": "LibraryCollectionViewItem", 'index': value}).center
                logger('111')
            elif 30 < index < 41:
                value = value - 25
                x, y = self.exist({"AXIdentifier": "LibraryCollectionViewItem", 'index': value}).center
            else:
                x, y = self.exist({"AXIdentifier": "LibraryCollectionViewItem", 'index': value}, parent=L.intro_video_room.library_visible_area).center
                logger('114')
            '''
            logger(x)
            logger(y)
            self.mouse.move(x, y)
            self.left_click()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True
    
    @step('[Action][Intro Video Room] Select Intro Template with method 2')
    def select_intro_template_method_2(self, index):
        try:
            if index < 1:
                logger('Invalid index')
                return False
            time.sleep(DELAY_TIME*4)
            self.activate()
            value = index - 1
            logger(value)

            if index < 21:
                x, y = self.exist({"AXIdentifier": "LibraryCollectionViewItem", 'index': value}).center
                # logger('111')
            else:
                x, y = self.exist({"AXIdentifier": "LibraryCollectionViewItem", 'index': value}, parent=L.intro_video_room.library_visible_area).center
                # logger('114')
            '''    
            # For event (12x)
            elif index < 91:
                x, y = self.exist({"AXIdentifier": "LibraryCollectionViewItem", 'index': value}, parent=L.intro_video_room.library_visible_area).center
                logger('114')
            elif index < 101:
                value = value - 10
                x, y = self.exist({"AXIdentifier": "LibraryCollectionViewItem", 'index': value}, parent=L.intro_video_room.library_visible_area).center
                logger('280')
            else:
                value = value - 20
                x, y = self.exist({"AXIdentifier": "LibraryCollectionViewItem", 'index': value}, parent=L.intro_video_room.library_visible_area).center
                logger('279')
            '''
            #logger(x)
            #logger(y)
            self.mouse.move(x, y)
            self.left_click()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def scroll_down_to_template_visual_area(self, index):
        # if PDR re-launch then scroll down to show tempalte w/ index
        self.click({"AXIdentifier": "LibraryCollectionViewItem", 'index': 0})
        self.move_mouse_to_0_0()
        times = ((index - 1)/5) + 1
        loop_times = int(times)
        logger(loop_times)
        for x in range(loop_times):
            self.keyboard.press(self.keyboard.key.down)
            time.sleep(DELAY_TIME)

    def drag_intro_media_to_timeline_playhead_position(self, index, track_no=1): # track_no: 1, 2, 3
        try:
            # Select Intro template w/ index
            self.select_intro_template_method_2(index)
            start_pos = self.get_mouse_pos()
            logger(f'{start_pos=}')

            # get dest. y-axis by track_no
            els_row = self.exist_elements(L.main.timeline.track_unit)
            track_pos = els_row[(track_no - 1) * 2].center
            dest_y_axis = track_pos[1]
            logger(f'{dest_y_axis=}')
            # get dest x-axis by indicator position
            indicator_pos = self.exist(L.main.timeline.indicator).center
            dest_x_axis = indicator_pos[0]
            logger(f'{dest_x_axis=}')
            dest_pos = (dest_x_axis, dest_y_axis)
            # drag clip to destination
            self.drag_mouse(start_pos, dest_pos)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def find_the_template_count(self):
        try:
            time.sleep(DELAY_TIME * 3)
            if self.exist(L.intro_video_room.scroll_bar):
                # Long: Lots of templates
                self.drag_scroll_bar_for_template(0.2)
                time.sleep(DELAY_TIME*1)
                self.drag_scroll_bar_for_template(0.5)
                time.sleep(DELAY_TIME*1.5)
                self.drag_scroll_bar_for_template(0.89)
                time.sleep(DELAY_TIME*1.5)
                self.drag_scroll_bar_for_template(0.1)

            
            child_list = self.exist(L.intro_video_room.library_template)
            count = len(child_list)
            logger(count)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return count

    def find_Discover_the_template_count(self):
        try:
            time.sleep(DELAY_TIME * 3)

            # Find index
            round = 0
            for x in range(2):
                logger(x)
                img_before = self.snapshot(locator=L.base.Area.preview.main)
                time.sleep(DELAY_TIME*0.5)
                self.keyboard.press(self.keyboard.key.down)
                time.sleep(DELAY_TIME * 2)
                img_after = self.snapshot(locator=L.base.Area.preview.main)
                time.sleep(1)
                check_no_change = self.compare(img_before, img_after, similarity=0.98)
                logger(check_no_change)

                # library preview does not change, leave for loop
                if check_no_change == True:
                    break
                else:
                    round = round + 1

            logger(round)
            #child_list = self.exist(L.intro_video_room.library_collection_view).AXChildren
            #count = len(child_list)
            count = round * 5
            logger(count)
            time.sleep(DELAY_TIME*2)
            self.drag_scroll_bar_for_template(0)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return count

    def open_view_template(self):
        self.activate()
        self.right_click()
        self.select_right_click_menu('View Template')
        if self.find(L.intro_video_room.view_template_dialog.main_window, timeout=25):
            time.sleep(DELAY_TIME*3)
            return True
        else:
            logger('Time out and cannot enter View Template dialog')
            return False

    def select_then_enter_designer(self, index):
        try:
            if index < 1:
                logger('Invalid index')
                return False
            self.activate()
            time.sleep(DELAY_TIME)
            value = index - 1
            #x, y = self.exist({"AXIdentifier": "LibraryCollectionViewItem", 'index': value}).center

            if index < 21:
                x, y = self.exist({"AXIdentifier": "LibraryCollectionViewItem", 'index': value}).center
                logger('111')
            else:
                x, y = self.exist({"AXIdentifier": "LibraryCollectionViewItem", 'index': value}, parent=L.intro_video_room.library_visible_area).center
                logger('114')

            self.mouse.move(x, y)
            self.mouse.click()
            time.sleep(DELAY_TIME)
            self.mouse.move(x, y-2)
            self.right_click()
            time.sleep(DELAY_TIME*2)
            # If occur error, output log
            intro_item = self.exist({"AXRole": "AXMenuItem", "AXTitle": 'Edit in Video Intro Designer'})
            outro_item = self.exist({"AXRole": "AXMenuItem", "AXTitle": 'Edit in Video Outro Designer'})
            if intro_item:
                self.select_right_click_menu('Edit in Video Intro Designer')
                time.sleep(DELAY_TIME * 15)
            elif outro_item:
                self.select_right_click_menu('Edit in Video Outro Designer')
                time.sleep(DELAY_TIME * 15)
            else:
                logger('cannot find the menu - Edit in Video Intro/Outro Designer')

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_specific_tag(self, name):
        tags = self.exist({'AXIdentifier': 'RoomTagOutlineViewTextField', 'AXRole': 'AXStaticText', "get_all": True})
        for tag in tags:
            if tag.AXValue.startswith(f"{name}"):
                self.mouse.click(*tag.center)
                return True
        return False

    def enter_downloaded_category(self):
        self.click_specific_tag('Downloads')
        time.sleep(DELAY_TIME)

    @step('[Action][Intro Video Room] Enter Saved Category')
    def enter_saved_category(self):
        if self.exist(L.intro_video_room.category_scroll_bar):
            self.exist(L.intro_video_room.category_scroll_bar).AXValue = 0
        time.sleep(DELAY_TIME)
        if not self.click_specific_tag('Saved Templates'):
            return False
        time.sleep(DELAY_TIME)
        return True

    @step('[Action][Intro Video Room] Enter My Favorites')
    def enter_my_favorites(self):
        if not self.click(L.intro_video_room.explore_view_region.category_my_favorites):
            return False
        time.sleep(DELAY_TIME)
        return True

    @step('[Action][Intro Video Room] Enter My Profile')
    def enter_my_profile(self):
        self.click(L.intro_video_room.explore_view_region.category_my_profile)
        time.sleep(DELAY_TIME*10)
        if self.exist(L.intro_video_room.my_profile.main_window, timeout=7):
            return True
        else:
            return False

    # ---------------------------------------------------------------------------------------------
    #                         For Video Intro Designer page function
    # ---------------------------------------------------------------------------------------------
    def check_in_intro_designer(self):
        if self.find(L.intro_video_room.intro_video_designer.main_window, timeout=35):
            logger('Enter Intro Video Designer now.')
            return True
        else:
            logger('Time out and Cannot open Intro Video Room.')
            return False

    @step('[Action][Intro Video Room] Click Add to Timeline Button')
    def click_btn_add_to_timeline(self):
        if not self.check_in_intro_designer():
            return False
        time.sleep(DELAY_TIME)
        self.click(L.intro_video_room.intro_video_designer.btn_add_to_timeline)
        return True

    @step('[Action][Intro Video Room] Set Timecode')
    def set_designer_timecode(self, timecode):
        self.activate()
        elem = self.find(L.intro_video_room.intro_video_designer.timecode, timeout=15)
        w, h = elem.AXSize
        x, y = elem.AXPosition

        pos_click = tuple(map(int, (x+w*0.3, y + h * 0.5)))
        self.mouse.click(*pos_click)

        #self.mouse.click(x+w*0.3, y+h*0.4)
        #self.mouse.click()
        time.sleep(1)
        self.keyboard.send(timecode.replace("_", ""))
        self.keyboard.enter()
        time.sleep(DELAY_TIME)

    @step('[Action][Intro Video Room] Set preview Timecode')
    def get_designer_timecode(self):
        try:
            if not self.check_in_intro_designer():
                raise Exception
            timecode = self.exist(L.intro_video_room.intro_video_designer.timecode).AXValue
            return timecode
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception

    def get_designer_timecode_only_sec(self):
        try:
            if not self.check_in_intro_designer():
                raise Exception
            time.sleep(DELAY_TIME*8)
            timecode = self.exist(L.intro_video_room.intro_video_designer.timecode).AXValue

            return timecode[0:2]
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception

    @step('[Action][Intro Video Room] Click [Close] button')
    def click_btn_close(self):
        try:
            if not self.check_in_intro_designer():
                return False
            self.click(L.intro_video_room.intro_video_designer.btn_close)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        
    @step('[Action][Intro Video Room] Click Save As Button and Save')
    def click_btn_save_as(self, custom_name, option=1): # 1: yes, 0: no
        try:
            if not self.check_in_intro_designer():
                return False
            time.sleep(DELAY_TIME)
            self.click(L.intro_video_room.intro_video_designer.btn_save_as)

            time.sleep(DELAY_TIME)
            if not self.find(L.intro_video_room.intro_video_designer.save_template_window.txt_field):
                logger('Cannot find the Save as window')
                return False
            self.keyboard.send(custom_name)
            time.sleep(DELAY_TIME)
            self.click(L.intro_video_room.intro_video_designer.save_template_window.btn_OK)
            time.sleep(DELAY_TIME)

            # Verify Step:
            if self.exist(L.intro_video_room.intro_video_designer.save_template_window.txt_field, timeout=5):
                return False # Window is not automatically closed after click OK button

            # If option = 1 : Click [Close] to Leave Intro designer
            if option:
                self.click(L.intro_video_room.intro_video_designer.btn_close)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        
        return True

    @step('[Action][Intro Video Room] Click Share template button and share')
    def click_btn_share_template(self, custom_name):
        try:
            if not self.check_in_intro_designer():
                return False
            time.sleep(DELAY_TIME)
            self.click(L.intro_video_room.intro_video_designer.btn_share_template)

            time.sleep(DELAY_TIME)
            if not self.find(L.intro_video_room.intro_video_designer.save_template_window.txt_field):
                logger('Cannot find the Save as window')
                return False
            self.keyboard.send(custom_name)
            time.sleep(DELAY_TIME)
            self.click(L.intro_video_room.intro_video_designer.save_template_window.btn_OK)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def get_designer_title(self):
        try:
            if not self.exist(L.intro_video_room.intro_video_designer.main_window):
                logger("No Video Intro designer window show up")
                raise Exception
            title = self.exist(L.intro_video_room.intro_video_designer.main_window).AXTitle
            return title
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception

    def click_menu_bar_help(self):
        time.sleep(DELAY_TIME * 3)
        result = self.top_menu_bar_help_help()
        time.sleep(DELAY_TIME * 3)
        # Verify : Chrome page - title
        logger(result)
        if result.startswith("help"):
            return True
        else:
            return False

    def click_undo_button(self):
        try:
            if not self.exist(L.intro_video_room.intro_video_designer.main_window):
                logger("No Video Intro designer window show up")
                raise Exception
            self.click(L.intro_video_room.intro_video_designer.btn_undo)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_redo_button(self):
        try:
            if not self.exist(L.intro_video_room.intro_video_designer.main_window):
                logger("No Video Intro designer window show up")
                raise Exception
            self.click(L.intro_video_room.intro_video_designer.btn_redo)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_max_restore_btn(self):
        try:
            if not self.exist(L.intro_video_room.intro_video_designer.main_window):
                logger("No Video Intro designer window show up")
                raise Exception
            self.click(L.intro_video_room.intro_video_designer.btn_zoom)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_upper_close_btn(self):
        try:
            if not self.exist(L.intro_video_room.intro_video_designer.main_window):
                logger("No Video Intro designer window show up")
                raise Exception
            self.click(L.intro_video_room.intro_video_designer.btn_x)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Intro Video Room] Handle [Save Change Warning] dialog before leaving')
    def handle_warning_save_change_before_leaving(self, option):
        try:
            if option == 'Yes':
                selected = L.main.confirm_dialog.btn_yes
            elif option == 'No':
                selected = L.main.confirm_dialog.btn_no
            elif option == 'Cancel':
                selected = L.main.confirm_dialog.btn_cancel

            if not self.exist(L.main.confirm_dialog.main_window):
                logger("No Warning dialog show up")
                raise Exception("No Warning dialog show up")

            warning_message = self.exist(L.main.confirm_dialog.alter_msg)
            if warning_message.AXValue.startswith("Do you want to save your changes before leaving"):
                self.click(selected)
            else:
                raise Exception("Incorrect Warning message")

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_DZ_btn(self):
        try:
            if not self.exist(L.intro_video_room.intro_video_designer.main_window):
                logger("No Video Intro designer window show up")
                raise Exception
            self.click(L.intro_video_room.intro_video_designer.btn_DZ)
            time.sleep(DELAY_TIME*3)
            result = self.check_chrome_page()

            time.sleep(DELAY_TIME)
            self.tap_close_chrome_tab_hotkey()
            # Verify : Open Chrome page
            if result:
                return True
            else:
                return False

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception

    @step('[Action][Intro Video Room] Click Preview Operation for Play/Pause/Stop')
    def click_preview_operation(self, operation):
        try:
            if not self.exist(L.intro_video_room.intro_video_designer.main_window):
                logger("No Video Intro designer window show up")
                raise Exception("No Video Intro designer window show up")
            if operation == 'Play':
                self.exist_click(L.intro_video_room.intro_video_designer.operation.btn_play)
            elif operation == 'Pause':
                self.exist_click(L.intro_video_room.intro_video_designer.operation.btn_pause)
            elif operation == 'Stop':
                self.exist_click(L.intro_video_room.intro_video_designer.operation.btn_stop)
            else:
                logger(f'Invalid operation: {operation}')
                raise Exception(f'Invalid operation: {operation}, please input (Play, Pause, Stop)')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Intro Video Room] Hover at Center of Preview Area')
    def hover_preview_center(self, y_threshold=0.4):
        try:
            preview_elem = self.exist(L.intro_video_room.intro_video_designer.preview_area)
            ori_pos = preview_elem.AXPosition
            size_w, size_h = preview_elem.AXSize
            new_pos = (ori_pos[0] + size_w * (0.5), ori_pos[1] + size_h * y_threshold)
            self.mouse.move(new_pos[0], new_pos[1])
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
    
    @step('[Action][Intro Video Room] Click Preview Center')
    def click_preview_center(self):
        try:
            preview_elem = self.exist(L.intro_video_room.intro_video_designer.preview_area)
            ori_pos = preview_elem.AXPosition
            size_w, size_h = preview_elem.AXSize
            new_pos = (ori_pos[0] + size_w * (0.5), ori_pos[1] + size_h * (0.5))
            self.mouse.move(new_pos[0], new_pos[1])
            self.mouse.click()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_preview_left_upper(self):
        try:
            preview_elem = self.exist(L.intro_video_room.intro_video_designer.preview_area)
            ori_pos = preview_elem.AXPosition
            size_w, size_h = preview_elem.AXSize
            new_pos = (ori_pos[0] + size_w * (0.1), ori_pos[1] + 1)
            self.mouse.move(new_pos[0], new_pos[1])
            self.mouse.click()
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def move_preview_object_to_right_upper(self, y_threshold=0.1):
        # move object which is in preview center
        # Direction: Move Right then move upper
        # if set y_threshold value, then (upper offset) will use argument value
        # e.g. move Right Upper: y_threshold = 0.1
        # e.g. move Right center: y_threshold = 0.3
        # e.g. move Right down: y_threshold = 0.6
        try:
            preview_elem = self.exist(L.intro_video_room.intro_video_designer.preview_area)
            ori_pos = preview_elem.AXPosition
            size_w, size_h = preview_elem.AXSize
            star_pos = (ori_pos[0]+ size_w * (0.3), ori_pos[1] + size_w * (0.3))
            new_pos = (ori_pos[0] + size_w * (0.6), ori_pos[1] + size_w * y_threshold)
            self.drag_mouse(star_pos, new_pos)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Intro Video Room] Move Preview Object to Left Upper')
    def move_preview_object_to_left_upper(self, x_threshold=0.3, y_threshold=0.1):
        # move object which is in preview center
        # Direction: Move left then move upper
        # if set y_threshold value, then (upper offset) will use argument value
        # e.g. move Right Upper: y_threshold = 0.1
        # e.g. move Right center: y_threshold = 0.3
        # e.g. move Right down: y_threshold = 0.6
        try:
            preview_elem = self.exist(L.intro_video_room.intro_video_designer.preview_area)
            ori_pos = preview_elem.AXPosition
            size_w, size_h = preview_elem.AXSize
            star_pos = (ori_pos[0]+ size_w * x_threshold, ori_pos[1] + size_w * (0.3))
            new_pos = (ori_pos[0] + size_w * (0.1), ori_pos[1] + size_w * y_threshold)
            self.drag_mouse(star_pos, new_pos)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Intro Video Room] Move Preview Object to Down')
    def move_preview_object_to_down(self, y_threshold=0.6):
        # move object which is in preview center
        # Direction: Move down
        # if set y_threshold value, then (down offset) will use argument value
        # e.g. move Down: y_threshold = 0.6
        # e.g. move Upper: y_threshold = 0.1
        try:
            preview_elem = self.exist(L.intro_video_room.intro_video_designer.preview_area)
            ori_pos = preview_elem.AXPosition
            size_w, size_h = preview_elem.AXSize
            star_pos = (ori_pos[0]+ size_w * (0.3), ori_pos[1] + size_w * (0.3))
            new_pos = (ori_pos[0] + size_w * (0.3), ori_pos[1] + size_w * y_threshold)
            self.drag_mouse(star_pos, new_pos)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Intro Video Room] Click Duration button')
    def click_duration_btn(self):
        if self.click(L.intro_video_room.intro_video_designer.btn_duration):
            time.sleep(DELAY_TIME * 0.5)
            return True
        return False

    @step('[Action][Intro Video Room] Click [Flip] button and choose option')
    def click_flip(self, option=0):
        # option = 0 >> Only click [Flip] button
        # option = 1 >> Click [Flip] > Select Flip horizontally
        # option = 2 >> Click [Flip] > Select Flip vertically
        try:
            if option > 2:
                logger(f' Parameter: {option} is invalid')
                raise Exception

            el_option = ['','Flip horizontally', 'Flip vertically']
            result = -1
            result = el_option[option]

            self.click(L.intro_video_room.intro_video_designer.btn_flip)
            time.sleep(DELAY_TIME*0.5)
            self.select_right_click_menu(result)
            time.sleep(DELAY_TIME * 3)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True
    @step('[Action][Intro Video Room] Click Replace Media and choose option')
    def click_replace_media(self, option):
        # option = 1 >> Import from Hard Disk
        # option = 2 >> Download media form SS and GI
        # option = 3 >> Use a Color Board
        try:
            el_option = ['','Import a Media File...', 'Download Media from Getty Images...', 'Use a Color Board']
            result = -1
            result = el_option[option]

            if result == "":
                logger(f'Parameter: {option} is invalid')
                raise Exception(f'Parameter: {option} is invalid')

            if not self.click(L.intro_video_room.intro_video_designer.btn_change_media): 
                raise Exception(f'Unable to click Replace Media button')
            time.sleep(DELAY_TIME*0.5)
            if not self.select_right_click_menu(result):
                raise Exception(f'Unable to select {result} option')
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')

    @step('[Action][Intro Video Room] Click Crop button')
    def click_trim_btn(self):
        try:
            if not self.exist(L.intro_video_room.intro_video_designer.main_window):
                logger("No Video Intro designer window show up")
                raise Exception("No Video Intro designer window show up")
            self.click(L.intro_video_room.intro_video_designer.btn_trim)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Intro Video Room] Click Crop button')
    def click_crop_btn(self):
        try:
            if not self.exist(L.intro_video_room.intro_video_designer.main_window):
                logger("No Video Intro designer window show up")
                raise Exception("No Video Intro designer window show up")
            self.click(L.intro_video_room.intro_video_designer.btn_crop)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Intro Video Room] Click LUT button')
    def click_LUT_btn(self):
        try:
            if not self.exist(L.intro_video_room.intro_video_designer.main_window):
                logger("No Video Intro designer window show up")
                raise Exception("No Video Intro designer window show up")
            self.click(L.intro_video_room.intro_video_designer.btn_LUT)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
    
    @step('[Action][Intro Video Room] Click Add Text button and choose option')
    def click_add_text(self, option):
        # option = 1 >> General text
        # option = 2 >> Motion Graphics Title
        try:
            el_option = ['','Add Text', 'Add Motion Graphics Title']
            result = -1
            result = el_option[option]

            if result == "":
                logger(f'Parameter: {option} is invalid')
                raise Exception(f'Parameter: {option} is invalid')

            self.click(L.intro_video_room.intro_video_designer.btn_add_title)
            time.sleep(DELAY_TIME*0.5)
            self.select_right_click_menu(result)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Intro Video Room] Click Add Image button and choose option')
    def click_add_image(self, option):
        # option = 1 >> Import a Media File...
        # option = 2 >> Download Media from Shutterstock and Getty Images...
        try:
            el_option = ['','Import a Media File...', 'Download Media from Shutterstock and Getty Images...']
            result = -1
            result = el_option[option]

            if result == "":
                logger(f' Parameter: {option} is invalid')
                raise Exception

            self.click(L.intro_video_room.intro_video_designer.btn_add_image)
            time.sleep(DELAY_TIME*0.5)
            self.select_right_click_menu(result)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Intro Video Room] Click Add PIP Object Button')
    def click_add_pip_object(self):
        try:
            if not self.exist(L.intro_video_room.intro_video_designer.main_window):
                logger("No Video Intro designer window show up")
                raise Exception("No Video Intro designer window show up")
            self.click(L.intro_video_room.intro_video_designer.btn_add_pip)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_replace_BGM(self):
        try:
            if not self.exist(L.intro_video_room.intro_video_designer.main_window):
                logger("No Video Intro designer window show up")
                raise Exception
            self.click(L.intro_video_room.intro_video_designer.btn_replace_BGM)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_volume_settings_btn(self):
        try:
            if not self.exist(L.intro_video_room.intro_video_designer.main_window):
                logger("No Video Intro designer window show up")
                raise Exception
            self.click(L.intro_video_room.intro_video_designer.btn_volume_settings)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Intro Video Room] Cancel Selection')
    def cancel_selection_button(self):
        try:
            if not self.exist(L.intro_video_room.intro_video_designer.btn_cancel_selection):
                logger("Cannot find the button")
                raise Exception("Cannot find the button")
            self.click(L.intro_video_room.intro_video_designer.btn_cancel_selection)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
    
    @step('[Action][Intro Video Room] Select and Insert PIP Template')
    def select_pip_template(self, index, category=None):
        # Pop up (Video Overlay Room) then call this page function to select / insert pip
        try:
            if category is not None:
                elem = L.intro_video_room.intro_video_designer.video_overlay_room.combobox_category
                current_setting = self.exist(elem).AXTitle
                if current_setting != category:
                    self.click(elem)
                    time.sleep(DELAY_TIME*1.5)
                    self.click({"AXRole": "AXStaticText", "AXValue": category})

            index = index - 1
            # Select then download
            self.exist_click({'AXIdentifier': 'EntityCollectionViewItem', 'index': index}, timeout=10)
            for x in range(30):
                ok_elem = self.exist(L.intro_video_room.intro_video_designer.video_overlay_room.btn_OK).AXEnabled
                if ok_elem:
                    time.sleep(DELAY_TIME)
                    break
                else:
                    time.sleep(DELAY_TIME)
            self.click(L.intro_video_room.intro_video_designer.video_overlay_room.btn_OK)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Intro Video Room] Click Layer Order and choose option to modify order')
    def click_layer_order(self, option):
        # option = 1 >> Bring to Front
        # option = 2 >> Bring Forward
        # option = 3 >> Send Backward
        # option = 4 >> Send to Back
        try:
            el_option = ['','Bring to Front', 'Bring Forward', 'Send Backward', 'Send to Back']
            result = -1
            result = el_option[option]

            if result == "":
                logger(f'Parameter: {option} is invalid')
                raise Exception(f'Parameter: {option} is invalid')

            self.click(L.intro_video_room.intro_video_designer.btn_layer_order)
            time.sleep(DELAY_TIME*0.5)
            self.select_right_click_menu(result)
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_change_color(self, HexColor):
        try:
            if not self.exist(L.intro_video_room.intro_video_designer.btn_cancel_selection):
                logger("No object be selected")
                raise Exception
            self.click(L.intro_video_room.intro_video_designer.btn_change_color)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return _set_color(self, HexColor)

    class Duration_Setting(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        @step('[Action][Intro Video Room] Get Original Duration Time')
        def get_org_duration(self):
            try:
                if self.exist(L.intro_video_room.intro_video_designer.duration.txt_org_duration, timeout=7):
                    target = self.exist(L.intro_video_room.intro_video_designer.duration.txt_org_duration)
                    return target.AXValue

                else:
                    logger("Cannot find the button")
                    raise Exception("Cannot find the button")
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')

        @step('[Action][Intro Video Room] Set Duration Time to target value')
        def set_new_duration(self, value):
            target = L.intro_video_room.intro_video_designer.duration.editbox_new_duration
            return _set_edittext(self, target, value)

        @step('[Action][Intro Video Room] Get New Duration Time')
        def get_new_duration(self):
            elem = L.intro_video_room.intro_video_designer.duration.editbox_new_duration
            target = self.exist(elem)
            return target.AXValue

        @step('[Action][Intro Video Room] Click OK to confirm the duration setting')
        def click_OK(self):
            try:
                if not self.exist(L.intro_video_room.intro_video_designer.duration.btn_ok):
                    logger("Cannot find the button")
                    raise Exception("Cannot find the button")
                self.click(L.intro_video_room.intro_video_designer.duration.btn_ok)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

    class Color_Filter(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        @step('[Action][Intro Video Room] Close LUT window')
        def close_x(self):
            self.click(L.intro_video_room.intro_video_designer.color_filter_window.btn_x)
            time.sleep(DELAY_TIME*1.5)
            if not self.exist(L.intro_video_room.intro_video_designer.color_filter_window.main_window):
                return True
            else:
                return False
        @step('[Action][Intro Video Room] Select LUT template')
        def select_LUT_template(self, index, category=None):
            # Pop up (Color Filter) then call this page function to select LUT template
            try:
                if category is not None:
                    elem = L.intro_video_room.intro_video_designer.color_filter_window.combobox_category
                    current_setting = self.exist(elem).AXTitle
                    if current_setting != category:
                        self.click(elem)
                        time.sleep(DELAY_TIME * 1.5)
                        self.click({"AXRole": "AXStaticText", "AXValue": category})

                index = index - 1
                self.exist_click({'AXIdentifier': 'EntityCollectionViewItem', 'index': index}, timeout=10)
                time.sleep(DELAY_TIME * 6)

                # self.click(L.intro_video_room.intro_video_designer.video_overlay_room.btn_OK)
                self.double_click()
                time.sleep(DELAY_TIME)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def set_strength_value(self, value):
            target = L.intro_video_room.intro_video_designer.color_filter_window.strength.editbox_value
            _set_edittext(self, target, value)

    class Backdrop_Settings(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def get_backdrop_checkbox(self):
            current_result = self.exist(L.intro_video_room.intro_video_designer.general_title.backdrop_settings.cbx_enable_backdrop).AXValue
            return current_result
        @step('[Action][Intro Video Room] Enable Backdrop')
        def enable_backdrop(self, value=1):
            try:
                if not self.exist(L.intro_video_room.intro_video_designer.general_title.backdrop_settings.main_window):
                    logger("Cannot find Backdrop Setting window")
                    raise Exception("Cannot find Backdrop Setting window")

                current_result = self.exist(L.intro_video_room.intro_video_designer.general_title.backdrop_settings.cbx_enable_backdrop).AXValue
                if current_result != value:
                    self.click(L.intro_video_room.intro_video_designer.general_title.backdrop_settings.cbx_enable_backdrop)
                time.sleep(DELAY_TIME)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][Intro Video Room] Set Backdrop Type')
        def set_type(self, index, fit_type=None):
            target_radio = L.intro_video_room.intro_video_designer.general_title.backdrop_settings.radio_group
            target_option = L.intro_video_room.intro_video_designer.general_title.backdrop_settings.fit_with_title_group
            if not _set_radio(self, target_radio, option=index): return False

            # Select (Fit with title) to other setting
            time.sleep(DELAY_TIME)
            if index > 1 and fit_type is not None:
                #self.click(L.intro_video_room.intro_video_designer.general_title.backdrop_settings.cbx_fit_with_title)
                if not _set_option(self, L.intro_video_room.intro_video_designer.general_title.backdrop_settings.cbx_fit_with_title, target_option, fit_type):
                    return False
            return True

        def get_type(self):
            target_radio = L.intro_video_room.intro_video_designer.general_title.backdrop_settings.radio_group
            return _set_radio(self, target_radio, option=2, get_status=True)

        def get_fit_backdrop_status(self):
            current_title = self.exist(L.intro_video_room.intro_video_designer.general_title.backdrop_settings.cbx_fit_with_title)
            return current_title.AXTitle

        def set_uniform_color(self, HexColor):
            self.click(L.intro_video_room.intro_video_designer.general_title.backdrop_settings.btn_uniform_color)
            return _set_color(self, HexColor)

        def get_uniform_color(self):
            self.click(L.intro_video_room.intro_video_designer.general_title.backdrop_settings.btn_uniform_color)
            return _get_color(self)

        def click_close_btn(self):
            if not self.exist(L.intro_video_room.intro_video_designer.general_title.backdrop_settings.btn_close):
                return False
            self.click(L.intro_video_room.intro_video_designer.general_title.backdrop_settings.btn_close)
            time.sleep(DELAY_TIME)
            if not self.exist(L.intro_video_room.intro_video_designer.general_title.backdrop_settings.main_window):
                return True

    class Background_Music(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def import_BGM_from_SS(self):
            try:
                if not self.exist(L.intro_video_room.intro_video_designer.bgm_setting.main_window, timeout=10):
                    logger("Cannot find (Add Background Music) dialog")
                    raise Exception
                self.click(L.intro_video_room.intro_video_designer.bgm_setting.btn_download_BGM)
                time.sleep(DELAY_TIME)
                # 2023/05/03 v21.6.5303 build: Remove SS(music)
                #self.select_right_click_menu('Download Music from Shutterstock...')
                time.sleep(DELAY_TIME)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def click_ok(self):
            try:
                if not self.exist(L.intro_video_room.intro_video_designer.bgm_setting.main_window):
                    logger("Cannot find (Add Background Music) dialog")
                    raise Exception
                self.click(L.intro_video_room.intro_video_designer.bgm_setting.btn_ok)
                time.sleep(DELAY_TIME)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

    class General_Title(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.in_animation = self.In_Animation(*args, *kwargs)
            self.out_animation = self.Out_Animation(*args, *kwargs)

        @step('[Action][Intro Video Room] Click Backdrop Button')
        def click_backdrop_button(self):
            try:
                if not self.exist(L.intro_video_room.intro_video_designer.general_title.btn_backdrop):
                    logger("Cannot find the button")
                    raise Exception("Cannot find the button")
                self.click(L.intro_video_room.intro_video_designer.general_title.btn_backdrop)
                time.sleep(DELAY_TIME)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def click_animation_button(self):
            try:
                if not self.exist(L.intro_video_room.intro_video_designer.general_title.btn_animation):
                    logger("Cannot find the button")
                    raise Exception
                self.click(L.intro_video_room.intro_video_designer.general_title.btn_animation)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True
        @step('[Action][Intro Video Room] Click Remove Button in Preview Center')
        def click_remove_button(self):
            try:
                if not self.exist(L.intro_video_room.intro_video_designer.general_title.btn_remove):
                    logger("Cannot find the button")
                    raise Exception("Cannot find the button")
                self.click(L.intro_video_room.intro_video_designer.general_title.btn_remove)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def close_animation_window(self):
            try:
                if not self.exist(L.intro_video_room.intro_video_designer.general_title.animation_setting.btn_close):
                    logger("Cannot find the close button")
                    raise Exception
                self.click(L.intro_video_room.intro_video_designer.general_title.animation_setting.btn_close)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        class In_Animation(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            def select_specific_effect_combobox(self, effect_type):
                target_option = L.intro_video_room.intro_video_designer.general_title.animation_setting.fit_with_animation_group
                _set_option(self, L.intro_video_room.intro_video_designer.general_title.animation_setting.cbx_in_animation_with_title,
                            target_option, effect_type)

            def get_effect_dropdownmenu(self):
                current_title = self.exist(
                    L.intro_video_room.intro_video_designer.general_title.animation_setting.cbx_in_animation_with_title)
                return current_title.AXTitle

            @step('[Action][Intro Video Room][In Animation] Unfold Setting')
            def unfold_setting(self, option):
                # option = 1 - Unfold
                # option = 0 - Fold
                try:
                    if not self.exist(L.intro_video_room.intro_video_designer.main_window):
                        logger("No Intro Video designer window show up")
                        raise Exception("No Intro Video designer window show up")

                    result = self.exist(L.intro_video_room.intro_video_designer.general_title.animation_setting.btn_in_animation).AXValue
                    if result != option:
                        self.exist_click(L.intro_video_room.intro_video_designer.general_title.animation_setting.btn_in_animation)

                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception(f'Exception occurs. log={e}')
                return True

            def get_unfold_setting(self):
                result = self.exist(L.intro_video_room.intro_video_designer.general_title.animation_setting.btn_in_animation)

                return result.AXValue
            
            @step('[Action][Intro Video Room][In Animation] Select Template and Apply')
            def select_template(self, index):
                index = index -1
                try:
                    self.exist_click({'AXIdentifier': 'TitleEffectCollectionViewItem', 'index': index})
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception(f'Exception occurs. log={e}')
                return True

        class Out_Animation(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            def select_specific_effect_combobox(self, effect_type):
                target_option = L.intro_video_room.intro_video_designer.general_title.animation_setting.fit_with_animation_group
                _set_option(self, L.intro_video_room.intro_video_designer.general_title.animation_setting.cbx_out_animation_with_title,
                            target_option, effect_type)

            def get_effect_dropdownmenu(self):
                current_title = self.exist(
                    L.intro_video_room.intro_video_designer.general_title.animation_setting.cbx_out_animation_with_title)
                return current_title.AXTitle

            def unfold_setting(self, option):
                # option = 1 - Unfold
                # option = 0 - Fold
                try:
                    if not self.exist(L.intro_video_room.intro_video_designer.main_window):
                        logger("No Intro Video designer window show up")
                        raise Exception

                    result = self.exist(L.intro_video_room.intro_video_designer.general_title.animation_setting.btn_out_animation).AXValue
                    if result != option:
                        self.exist_click(L.intro_video_room.intro_video_designer.general_title.animation_setting.btn_out_animation)

                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def get_unfold_setting(self):
                result = self.exist(L.intro_video_room.intro_video_designer.general_title.animation_setting.btn_out_animation)

                return result.AXValue

            def select_template(self, index):
                index = index -1
                try:

                    # Fold (IN animation)
                    result = self.exist(
                        L.intro_video_room.intro_video_designer.general_title.animation_setting.btn_in_animation).AXValue
                    if result != 0:
                        self.exist_click(
                            L.intro_video_room.intro_video_designer.general_title.animation_setting.btn_in_animation)
                        time.sleep(DELAY_TIME*2)

                    self.exist_click({'AXIdentifier': 'TitleEffectCollectionViewItem', 'index': index})
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

    class Motion_Graphics(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        @step('[Action][Intro Video Room] Select Template and Import in Motion Graphics')
        def select_template(self, index, category=None):
            try:
                if category is not None:
                    target_option = L.intro_video_room.intro_video_designer.motion_graphics.title_room.fit_with_category_group
                    _set_option(self, L.intro_video_room.intro_video_designer.motion_graphics.title_room.cbx_category,
                                target_option, category)
                    time.sleep(DELAY_TIME*1.5)

                index = index - 1
                self.exist_click({'AXIdentifier': 'EntityCollectionViewItem', 'index': index})
                time.sleep(DELAY_TIME*3)
                self.click(L.intro_video_room.intro_video_designer.motion_graphics.title_room.btn_import)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def click_settings_button(self):
            try:
                self.click(L.intro_video_room.intro_video_designer.motion_graphics.btn_settings)
                time.sleep(DELAY_TIME)

                # Verify Step:
                if not self.exist(L.intro_video_room.intro_video_designer.motion_graphics.mgt_settings.main_window):
                    return False

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        @step('[Action][Intro Video Room][Motion Graphics] Click [Remove] button')
        def click_remove_button(self):
            try:
                self.click(L.intro_video_room.intro_video_designer.motion_graphics.btn_remove)
                time.sleep(DELAY_TIME)

                # Verify Step:
                if self.exist(L.intro_video_room.intro_video_designer.motion_graphics.btn_remove):
                    return False

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def set_title_text(self, strTitle):
            try:
                target = self.exist(L.intro_video_room.intro_video_designer.motion_graphics.mgt_settings.txt_title)
                self.el_click(target)
                self.mouse.click(times=3)
                time.sleep(DELAY_TIME * 1)
                target.AXValue = str(strTitle)
                time.sleep(DELAY_TIME * 1)

                ori_pos = target.AXPosition
                new_pos = (ori_pos[0], ori_pos[1] - 3)
                self.mouse.move(new_pos[0], new_pos[1])
                self.mouse.click()
                time.sleep(DELAY_TIME * 1)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                return False
            return True

        def get_title_text(self):
            try:
                if not self.exist(L.intro_video_room.intro_video_designer.motion_graphics.mgt_settings.txt_title):
                    raise Exception
                current_title = self.exist(L.intro_video_room.intro_video_designer.motion_graphics.mgt_settings.txt_title)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return current_title.AXValue

        def set_font_color(self, HexColor):
            self.click(L.intro_video_room.intro_video_designer.motion_graphics.mgt_settings.title_font_color)
            return _set_color(self, HexColor)

        def get_font_color(self):
            self.click(L.intro_video_room.intro_video_designer.motion_graphics.mgt_settings.title_font_color)
            return _get_color(self)

        def select_title_category(self, value):
            # value = Add Title Here, PowerDirector, FHD
            target = {'AXRole': 'AXStaticText', 'AXValue': value}
            current = L.intro_video_room.intro_video_designer.motion_graphics.mgt_settings.cbx_title_txt_category
            if self.exist(current).AXTitle != value:
                self.click(current)
            time.sleep(DELAY_TIME)
            self.click(target)


        def click_close_btn(self):
            try:
                if not self.exist(L.intro_video_room.intro_video_designer.motion_graphics.mgt_settings.btn_close):
                    logger("Cannot find the close button")
                    raise Exception
                self.click(L.intro_video_room.intro_video_designer.motion_graphics.mgt_settings.btn_close)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

    class Image(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.object_settings = self.Object_Settings(*args, *kwargs)
            self.in_animation = self.In_Animation(*args, *kwargs)
            self.out_animation = self.Out_Animation(*args, *kwargs)

        def click_object_settings_btn(self):
            try:
                self.click(L.intro_video_room.intro_video_designer.image.btn_obj_setting)
                time.sleep(DELAY_TIME)

                # Verify Step:
                if not self.exist(L.intro_video_room.intro_video_designer.image.object_settings.main_window):
                    return False

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        @step('[Action][Intro Video Room] Click Animation Button')
        def click_animation_btn(self):
            try:
                self.click(L.intro_video_room.intro_video_designer.image.btn_animation)
                time.sleep(DELAY_TIME)

                # Verify Step:
                if not self.exist(L.intro_video_room.intro_video_designer.image.animation.main_window):
                    return False

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def click_replace_btn(self):
            try:
                self.click(L.intro_video_room.intro_video_designer.image.btn_change_media)
                time.sleep(DELAY_TIME)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def click_remove_button(self):
            try:
                self.click(L.intro_video_room.intro_video_designer.image.btn_remove)
                time.sleep(DELAY_TIME)

                # Verify Step:
                if self.exist(L.intro_video_room.intro_video_designer.image.btn_remove):
                    return False

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def close_animation_window(self):
            try:
                if not self.exist(L.intro_video_room.intro_video_designer.image.animation.btn_close):
                    logger("Cannot find the close button")
                    raise Exception
                self.click(L.intro_video_room.intro_video_designer.image.animation.btn_close)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        class In_Animation(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            def unfold_setting(self, option):
                # option = 1 - Unfold
                # option = 0 - Fold
                try:
                    if not self.exist(L.intro_video_room.intro_video_designer.image.animation.main_window):
                        logger("No Animation window show up")
                        raise Exception

                    result = self.exist(L.intro_video_room.intro_video_designer.image.animation.btn_tri_in_animation).AXValue
                    if result != option:
                        self.exist_click(L.intro_video_room.intro_video_designer.image.animation.btn_tri_in_animation)

                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def select_template(self, option):
                # option = 'Basic Shape 01', 'Brush Transition 04', ...
                try:
                    self.click({'AXRole': 'AXStaticText', 'AXValue': option})
                    time.sleep(DELAY_TIME*0.5)

                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

        class Out_Animation(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            def unfold_setting(self, option):
                # option = 1 - Unfold
                # option = 0 - Fold
                try:
                    if not self.exist(L.intro_video_room.intro_video_designer.image.animation.main_window):
                        logger("No Animation window show up")
                        raise Exception

                    result = self.exist(L.intro_video_room.intro_video_designer.image.animation.btn_tri_out_animation).AXValue
                    if result != option:
                        self.exist_click(L.intro_video_room.intro_video_designer.image.animation.btn_tri_out_animation)

                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def select_template(self, option):
                # option = 'Basic Shape 01', 'Brush Transition 04', ...
                try:
                    self.click({'AXRole': 'AXStaticText', 'AXValue': option})
                    time.sleep(DELAY_TIME*0.5)

                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

        class Object_Settings(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            def unfold_border(self, option):
                # option = 1 - Unfold
                # option = 0 - Fold
                try:
                    if not self.exist(L.intro_video_room.intro_video_designer.main_window):
                        logger("No Intro Video designer window show up")
                        raise Exception

                    result = self.exist(L.intro_video_room.intro_video_designer.image.object_settings.btn_tri_border).AXValue
                    if result != option:
                        self.exist_click(L.intro_video_room.intro_video_designer.image.object_settings.btn_tri_border)

                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def get_border_unfold_setting(self):
                result = self.exist(L.intro_video_room.intro_video_designer.image.object_settings.btn_tri_border)

                return result.AXValue


            def get_border_status(self):
                current_result = self.exist(L.intro_video_room.intro_video_designer.image.object_settings.cbx_border).AXValue
                return current_result

            def enable_border(self, value=1):
                try:
                    if not self.exist(L.intro_video_room.intro_video_designer.image.object_settings.main_window):
                        logger("Cannot find Object Settings window")
                        raise Exception

                    current_result = self.exist(L.intro_video_room.intro_video_designer.image.object_settings.cbx_border).AXValue
                    if current_result != value:
                        self.click(L.intro_video_room.intro_video_designer.image.object_settings.cbx_border)

                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def set_border_size(self, value):
                target = L.intro_video_room.intro_video_designer.image.object_settings.editbox_border_size
                _set_edittext(self, target, value)

            def get_border_size(self):
                elem = L.intro_video_room.intro_video_designer.image.object_settings.editbox_border_size
                target = self.exist(elem)
                return target.AXValue

            def click_close_btn(self):
                try:
                    if not self.exist(L.intro_video_room.intro_video_designer.image.object_settings.btn_close):
                        logger("Cannot find the close button")
                        raise Exception
                    self.click(L.intro_video_room.intro_video_designer.image.object_settings.btn_close)
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

    class CropZoomPan(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        @step('[Action][Intro Video Room][Crop] Resize to small by dragging left-upper node')
        def resize_to_small(self):
            # Drag left - upper node
            try:
                time.sleep(2)
                if not self.exist(L.intro_video_room.intro_video_designer.crop_window.obj_edit_canvas, timeout=6):
                    raise Exception('Cannot find Crop window')

                target = self.exist(L.intro_video_room.intro_video_designer.crop_window.obj_edit_canvas)
                ori_pos = target.AXPosition
                size_w, size_h = target.AXSize
                des_pos = (ori_pos[0] + (size_w * 0.3), ori_pos[1] + (size_h * 0.3))
                self.drag_mouse(ori_pos, des_pos)
                time.sleep(DELAY_TIME*2)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        # 20.7.4205 does NOT work : option 'Yes'
        def click_cancel(self, option=None):
            if option == 'Yes':
                selected = L.main.confirm_dialog.btn_yes
            elif option == 'No':
                selected = L.main.confirm_dialog.btn_no
            elif option == 'Cancel':
                selected = L.main.confirm_dialog.btn_cancel

            self.click(L.intro_video_room.intro_video_designer.crop_window.btn_cancel)
            time.sleep(DELAY_TIME)
            if option:
                self.click(selected)

        # 20.7.4205 does NOT work : option 'Yes'
        @step('[Action][Intro Video Room][Crop] Click option on Crop window')
        def leave_crop(self, option=None):
            if option == 'Yes':
                selected = L.main.confirm_dialog.btn_yes
            elif option == 'No':
                selected = L.main.confirm_dialog.btn_no
            elif option == 'Cancel':
                selected = L.main.confirm_dialog.btn_cancel

            self.click(L.intro_video_room.intro_video_designer.crop_window.btn_x)
            time.sleep(DELAY_TIME)

            if option:
                self.click(selected)
            return True

    class Replace_Media(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def select_media_clip(self, index):
            # index : 1 = select 1st clip
            # index : 2 = select 2nd clip
            try:
                current = index - 1
                if not self.exist(L.intro_video_room.intro_video_designer.media_library.main_window):
                    raise Exception
                self.click({'AXIdentifier': 'EntityCollectionViewItem', 'index': current})
                self.click(L.intro_video_room.intro_video_designer.media_library.btn_OK)
                time.sleep(DELAY_TIME)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

    class My_Profile(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def handle_delete_post_msg(self):
            if self.exist(L.intro_video_room.my_profile.delete_warning_msg):
                self.click(L.intro_video_room.my_profile.btn_delete)
                return True
            else:
                return False
            
        @step('[Action][Intro Video Room] Delete 1st Template')
        def delete_1st_template(self):
            post_elem = self.exist(L.intro_video_room.my_profile.txt_view)
            #logger(post_elem.AXPosition)

            # Move mouse to 1st template
            high = post_elem.AXSize[1]
            new_x = post_elem.AXPosition[0]
            new_y = post_elem.AXPosition[1] + (high * 5)

            self.mouse.move(new_x, new_y)
            time.sleep(DELAY_TIME)
            self.right_click()
            self.select_right_click_menu('Delete')
            time.sleep(DELAY_TIME)
            result = self.handle_delete_post_msg()

            return result

    class Share_Temp(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        @step('[Action][Intro Video Room] Confirm Copyright for sharing Tempalte')
        def click_confirm(self):
            if self.exist(L.intro_video_room.share_template.btn_copyright_confirm, timeout=7):
                self.click(L.intro_video_room.share_template.btn_copyright_confirm)
                return True
            else:
                return False

        @step('[Action][Intro Video Room] Click Share button to Share Template')
        def click_share(self, input_description='Have a nice day'):
            if not self.exist(L.intro_video_room.share_template.edit_box_description, timeout=35):
                logger('Cannot find Description locator')
                return False
            target = L.intro_video_room.share_template.edit_box_description
            _set_edittext(self, target, input_description)
            self.click(L.intro_video_room.share_template.btn_share)

            complete_flag = 0
            for x in range(90):
                if self.exist(L.intro_video_room.share_template.btn_done):
                    self.click(L.intro_video_room.share_template.btn_done)
                    complete_flag = 1
                    break
                else:
                    time.sleep(DELAY_TIME*1.5)

            if complete_flag:
                return True
            else:
                return False

    class Volume_Settings(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def get_cbx_mute_status(self):
            if self.exist(L.intro_video_room.intro_video_designer.volume_setting_dialog.main_window):
                cbx_value = self.exist(L.intro_video_room.intro_video_designer.volume_setting_dialog.cbx_always_mute_video_s_audio)
                return cbx_value.AXValue
            else:
                return None

        def set_cbx_mute(self, applied=1):
            if not self.exist(L.intro_video_room.intro_video_designer.volume_setting_dialog.main_window):
                raise Exception

            current_cbx_value = self.get_cbx_mute_status()
            if current_cbx_value != applied:
                self.click(L.intro_video_room.intro_video_designer.volume_setting_dialog.cbx_always_mute_video_s_audio)
                time.sleep(DELAY_TIME)

        def click_ok(self):
            if self.exist(L.intro_video_room.intro_video_designer.volume_setting_dialog.main_window):
                self.click(L.intro_video_room.intro_video_designer.volume_setting_dialog.btn_ok)
                return True
            else:
                return False

