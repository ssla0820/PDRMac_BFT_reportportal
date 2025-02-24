import time, datetime, os, copy

from .base_page import BasePage
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
from AppKit import NSScreen
from .locator import locator as L
from reportportal_client import step

DELAY_TIME = 1
def arrow(obj, button="up", times=1, locator=None):
    locator = locator[button.lower() == "up"]
    elem = obj.exist(locator)
    for _ in range(times):
        obj.mouse.click(*elem.center)
    return True


class VideoCollageDesigner(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.border = self.Border(*args, **kwargs)
        self.media = self.Media(*args, **kwargs)
        self.layout = self.Layout(*args, **kwargs)
        self.share_to = self.Share_to(*args, **kwargs)
        self.preview = self.Preview(*args, **kwargs)

    def verify_preview(self,file_path, similarity=0.95):
        file_full_path = os.path.abspath(file_path)
        splitter = self.exist(L.video_collage_designer.splitter)
        slider = self.exist(L.video_collage_designer.slider)
        settings = self.exist(L.video_collage_designer.border.frame)
        y1 = settings.AXPosition[1]
        h1 = settings.AXSize[1]
        x = splitter.AXPosition[0] + splitter.AXSize[0] + 2
        w = (slider.center[0] - x -1) * 2
        y = y1
        h = h1 - (y1+h1 - slider.center[1]) * 2
        current_snapshot = self.image.snapshot(x=x, y=y, h=h, w=w)
        logger(f'{current_snapshot=}')
        return self.compare(file_full_path, current_snapshot, similarity)

    @step('[Verify][VideoCollageDesigner] Check if [Video Collage Designer] window opened')
    def check_window_opened(self):
        return self.exist(L.video_collage_designer.main_window)
    
    @step('[Action][VideoCollageDesigner] Set Timecode')
    def set_timecode(self, timecode):
        return self._set_timecode(timecode,  L.video_collage_designer.time_code)
    
    @step('[Action][VideoCollageDesigner] Get Timecode')
    def get_timecode(self):
        return self.exist(L.video_collage_designer.time_code).AXValue

    @step('[Action][VideoCollageDesigner] Click [OK] button to leave [Video Collage Designer] window')
    def click_ok(self):
        return self.press(L.video_collage_designer.btn_ok)

    def click_save_as_ok(self, name):
        self.exist(L.video_collage_designer.save_as.input_name).AXValue = name
        self.press(L.video_collage_designer.save_as.btn_ok)
        time.sleep(DELAY_TIME*0.5)
        return True

    def click_cancel(self, option = 0):
        button = [None,
                  L.video_collage_designer.cancel.yes,
                  L.video_collage_designer.cancel.no,
                  L.video_collage_designer.cancel.cancel,][option]
        self.press(L.video_collage_designer.btn_cancel)
        if button: self.exist_click(button)
        return True
    
    @step('[Action][VideoCollageDesigner] Save As the custom layout with name')
    def click_save_as_with_name(self, name):
        self.press(L.video_collage_designer.btn_save_as)
        return self.click_save_as_ok(name)

    def click_save_as_with_name_slider(self, name, percentage = 0.5):
        self.press(L.video_collage_designer.btn_save_as)
        self.exist(L.video_collage_designer.save_as.slider).AXValue = percentage
        return self.click_save_as_ok(name)

    def click_save_as_then_cancel(self):
        self.press(L.video_collage_designer.btn_save_as)
        self.press(L.video_collage_designer.save_as.btn_cancel)
        return True

    def click_share(self):
        self.press(L.video_collage_designer.btn_share)
        return True

    def _share_to(self, name, option=0):
        self.click_share()
        self.share_to.set_name(name)
        self.share_to.press_ok()
        if self.share_to.press_auto_sign_in_checkbox():
            self.share_to.press_auto_sign_in_ok()
        self.share_to.press_category_menu()
        self.share_to.select_category_item(option)
        self.share_to.set_tag("AT_tag")
        self.exist(L.video_collage_designer.share.input_tag).AXValue = "AT_tag"
        self.share_to.set_collection("AT_collection")
        self.exist(L.video_collage_designer.share.input_collection).AXValue = "AT_collection"
        self.share_to.set_description("AT_description")
        self.exist_click(L.video_collage_designer.share.input_description)
        self.exist(L.video_collage_designer.share.input_description).AXValue = "AT_description"
        time.sleep(DELAY_TIME)
        self.share_to.press_next_button()
        if self.share_to.press_confirm_button():
            self.share_to.press_next_button()
        self.share_to.press_finish_button()
        return True

    def share_to_cloud_dz(self, name):
        return self._share_to(name, 0)

    def share_to_cloud(self, name):
        return self._share_to(name, 1)
    
    @step('[Action][VideoCollageDesigner] Share to DZ with name')
    def share_to_dz(self, name):
        return self._share_to(name, 2)

    def adjust_splitter(self, value):
        splitter = self.find(L.video_collage_designer.splitter)
        x,y = splitter.center
        self.drag_mouse((x,y), (x+value,y))
        return True

    @step('[Action][VideoCollageDesigner] Click preview operation -- play, pause, stop, previous frame, next frame, fast forward')
    def click_preview_operation(self, op):
        return bool(self.exist_press(getattr(L.video_collage_designer.preview, op.lower())))

    def click_snapshot(self, path):
        self.exist_press(L.video_collage_designer.preview.btn_snapshot)
        self.select_file(path, btn_confirm="Save")
        self.exist_press(L.video_collage_designer.preview.btn_replace, timeout=1, no_warning=True)
        return True

    def select_quality(self, name):
        target_name = f"{name} Preview Resolution"
        target_locator = copy.deepcopy(L.video_collage_designer.preview.menu_item_quality)
        target_locator[-1]["AXTitle"] = target_name
        logger(f"Select >>  {target_name} << menu item")
        self.exist_press(L.video_collage_designer.preview.menu_quality)
        time.sleep(DELAY_TIME)
        self.exist_click(target_locator)
        return True

    def set_volume(self, percentage):
        self.exist_click(L.video_collage_designer.preview.btn_volume)
        self.exist(L.video_collage_designer.preview.slider_volumn).AXValue = percentage
        self._close_menu()
        return True

    def adjust_playback_slider(self, percentage):
        slider = self.exist(L.video_collage_designer.preview.slider_playback)
        maxi = slider.AXMaxValue
        target = int(maxi * percentage)
        slider.AXValue = target
        return True

    class Border(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.advanced = self.Advanced(*args, **kwargs)

        @step('[Action][VideoCollageDesigner][Border] Scroll bar')
        def set_scroll_bar(self, value):
            try:
                self.exist(L.video_collage_designer.border.scroll_bar).AXValue = value
                return True
            except Exception as e:
                logger(f"[Warning] {e=}")
                raise Exception(f"[Warning] {e=}")

        def enable_border(self, is_enable=True):
            checkbox = self.exist(L.video_collage_designer.border.checkbox_enable)
            if bool(checkbox.AXValue) != is_enable:
                checkbox.press()
            return True

        @step('[Action][VideoCollageDesigner][Border] Get Value')
        def get_border_value(self):
            if self.exist(L.video_collage_designer.border.value_border):
                return self.exist(L.video_collage_designer.border.value_border).AXValue
            else:
                raise Exception("Border value not found")

        @step('[Action][VideoCollageDesigner][Border] Set Value by Slider')
        def set_border_slider(self, value):
            self.exist(L.video_collage_designer.border.slider_border).AXValue = value
            time.sleep(DELAY_TIME)
            return True

        def set_border_value(self, value):
            target = self.exist(L.video_collage_designer.border.value_border)
            self.mouse.click(*target.center)
            target.AXValue = str(value)
            self.keyboard.enter()
            return True

        def click_border_arrow(self, button="up", times = 1):
            locator = [L.video_collage_designer.border.arrow_down_border,
                       L.video_collage_designer.border.arrow_up_border]
            return arrow(self, button, times, locator)

        @step('[Verify][VideoCollageDesigner][Border] Check if Border Color as Expected')
        def is_border_color(self, color):
            self.exist_click(L.video_collage_designer.border.btn_color)
            self.color_picker_switch_category_to_RGB()
            ret = self.exist(L.video_collage_designer.border.text_hex).AXValue
            logger(f"current hex = {ret} / expect hex = {color.upper()}")
            self.click(L.base.colors.btn_close)
            return ret == color.upper()

        @step('[Action][VideoCollageDesigner][Border] Set Border Color')
        def set_border_color(self, color, _target=None):
            _target = _target or L.video_collage_designer.border.btn_color
            self.exist_click(_target)
            self.color_picker_switch_category_to_RGB()
            if color:
                self.exist(L.tips_area.button.change_color_hex).AXFocused = True
                self.click(L.tips_area.button.change_color_hex)
                time.sleep(DELAY_TIME*0.5)
                self.exist(L.tips_area.button.change_color_hex).AXValue = color
                time.sleep(DELAY_TIME*0.5)
                self.press_enter_key()
                self.click(L.base.colors.btn_close)
                time.sleep(DELAY_TIME*0.5)
            return True

        @step('[Action][VideoCollageDesigner][Border] Get Interclip Value')
        def get_interclip_value(self):
            if self.exist(L.video_collage_designer.border.value_interclip):
                return self.exist(L.video_collage_designer.border.value_interclip).AXValue
            else:
                raise Exception("Interclip value not found")

        @step('[Action][VideoCollageDesigner][Border] Set Interclip by Slider')
        def set_interclip_slider(self, value):
            self.exist(L.video_collage_designer.border.slider_interclip).AXValue = value
            time.sleep(DELAY_TIME)
            return True

        @step('[Action][VideoCollageDesigner][Border] Set Interclip Value by Input')
        def set_interclip_value(self, value):
            target = self.exist(L.video_collage_designer.border.value_interclip)
            self.mouse.click(*target.center)
            target.AXValue = str(value)
            self.keyboard.enter()
            time.sleep(DELAY_TIME)
            return True

        def click_interclip_arrow(self, button="up", times = 1):
            locator = [L.video_collage_designer.border.arrow_down_interclip,
                       L.video_collage_designer.border.arrow_up_interclip]
            return arrow(self, button, times, locator)

        @step('[Action][VideoCollageDesigner][Border] Set Fill Type')
        def set_fill_type(self, index):
            target = [ L.video_collage_designer.border.menu_item_uniform,
                       L.video_collage_designer.border.menu_item_interclip][index]
            self.exist_click(L.video_collage_designer.border.menu_fill_type)
            time.sleep(DELAY_TIME)
            self.exist_click(target)
            time.sleep(DELAY_TIME)
            return True

        @step('[Action][VideoCollageDesigner][Border] Set Uniform Color')
        def set_uniform_color(self, color):
            return self.set_border_color(color, L.video_collage_designer.border.btn_uniform_color)

        @step('[Action][VideoCollageDesigner][Border] Get Uniform Color')
        def get_uniform_color(self):
            self.exist_click(L.video_collage_designer.border.btn_uniform_color)
            self.color_picker_switch_category_to_RGB()
            ret = self.exist(L.video_collage_designer.border.text_hex).AXValue
            logger(f"current hex = {ret}")
            self.click(L.base.colors.btn_close)
            return ret

        @step('[Action][VideoCollageDesigner][Border] Select Interclip Texture by Path')
        def select_interclip_texture(self, path):
            self.select_file(path)
            return True

        @step('[Action][VideoCollageDesigner][Border] Set Frame Animation')
        def set_frame_animation(self, index):
            target = [L.video_collage_designer.border.menu_item_from_beginning,
                      L.video_collage_designer.border.menu_item_during_closing,
                      L.video_collage_designer.border.menu_item_off][index]
            self.exist_click(L.video_collage_designer.border.menu_frame_animation)
            time.sleep(DELAY_TIME)
            self.exist_click(target)
            time.sleep(DELAY_TIME)
            return True

        @step('[Action][VideoCollageDesigner][Border] Set Start Clip Playback by index')
        def set_start_playback(self, index):
            opt = [ L.video_collage_designer.border.radio_with_frame_animation,
                    L.video_collage_designer.border.radio_after_frame_animation][index]
            target = self.exist(opt)
            if not target.AXValue: target.press()
            return True

        def set_pause_playback(self, index):
            opt = [L.video_collage_designer.border.radio_pause_with_frame_animation,
                   L.video_collage_designer.border.radio_pause_after_frame_animation][index]
            target = self.exist(opt)
            if not target.AXValue: target.press()
            return True

        @step('[Action][VideoCollageDesigner][Border] Set [Before/ After Clip Playback] by index')
        def set_before_after_clip_playback(self, index):
            opt = [L.video_collage_designer.border.radio_freeze_the_video,
                   L.video_collage_designer.border.radio_display_color_board,
                   L.video_collage_designer.border.radio_restart_playback][index]
            target = self.exist(opt)
            if not target.AXValue: target.press()
            return True

        @step('[Action][VideoCollageDesigner][Border] Set [Before/ After Clip Playback -- Color Board] Color')
        def set_before_after_color_board(self, color):
            return self.set_border_color(color, L.video_collage_designer.border.btn_before_after_color_board)

        @step('[Action][VideoCollageDesigner][Border] Click [Advanced Setting] button')
        def click_advanced_setting(self):
            return bool(self.exist_press(L.video_collage_designer.border.btn_advanced_setting))

        def click_close(self):
            return bool(self.exist_press(L.video_collage_designer.border.btn_close))

        class Advanced(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            @step('[Action][VideoCollageDesigner][Border][Advanced] Set [Playback Timing] by index')
            def set_playback_timing(self, index):
                opt = [L.video_collage_designer.border.advanced.radio_all_at_once,
                       L.video_collage_designer.border.advanced.radio_delay,
                       L.video_collage_designer.border.advanced.radio_one_after_another][index]
                target = self.exist(opt)
                if not target.AXValue: target.press()
                return True

            @step('[Action][VideoCollageDesigner][Border][Advanced] Set [Playback Timing - Delay Time] by sec')
            def set_delay_sec(self, sec):
                target = self.exist(L.video_collage_designer.border.advanced.input_delay_sec)
                self.mouse.click(*target.center)
                target.AXValue = str(sec)
                self.keyboard.enter()
                return True

            @step('[Action][VideoCollageDesigner][Border][Advanced] Set match collage duration')
            def set_match_collage_duration_to(self,index):
                target = [L.video_collage_designer.border.advanced.menu_item_all_video,
                          L.video_collage_designer.border.advanced.menu_item_longest_clip,
                          L.video_collage_designer.border.advanced.menu_item_shortest_clip,
                          L.video_collage_designer.border.advanced.menu_item_clip1,
                          L.video_collage_designer.border.advanced.menu_item_clip2,
                          L.video_collage_designer.border.advanced.menu_item_clip3,
                          L.video_collage_designer.border.advanced.menu_item_clip4][index]
                self.exist_click(L.video_collage_designer.border.advanced.menu_collage_duration)
                time.sleep(DELAY_TIME)
                self.exist_click(target)
                return True

            def click_default(self):
                return bool(self.exist_press(L.video_collage_designer.border.advanced.btn_default))

            def click_cancel(self):
                return bool(self.exist_press(L.video_collage_designer.border.advanced.btn_cancel))

            @step('[Action][VideoCollageDesigner][Border][Advanced] Click [OK] button to leave Advanced Setting')
            def click_ok(self):
                return bool(self.exist_press(L.video_collage_designer.border.advanced.btn_ok))


    class Media(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def set_scroll_bar(self, value):
            try:
                self.exist(L.video_collage_designer.media.scroll_bar).AXValue = value
                return True
            except Exception as e:
                logger(f"[Warning] {e=}")
                return False
        
        @step('[Action][VideoCollageDesigner][Media] Import media')
        def import_media(self, file_path, option=0, timeout = 30):
            target = [
                L.video_collage_designer.media.btn_yes,
                L.video_collage_designer.media.btn_no,
                L.video_collage_designer.media.btn_yes_to_all,
                L.video_collage_designer.media.btn_no_to_all][option]
            timer = time.time()
            self.exist_press(L.video_collage_designer.media.btn_import)
            self.select_file(file_path, "Open")
            time.sleep(DELAY_TIME)
            while time.time()-timer < timeout:
                self.exist_press(target, timeout=0)
                dialogs = self.find({"AXSubrole":"AXDialog","recursive":False,"get_all":True})
                for dialog in dialogs:
                    if "Importing Media" in dialog.AXTitle:
                        logger("importing media, wait a sec")
                        time.sleep(DELAY_TIME)
                        continue
                logger("Importation completed")
                time.sleep(DELAY_TIME)
                return True
            else:
                return False
            
        @step('[Action][VideoCollageDesigner][Media] Select media category')
        def select_category(self, index):
            target = [
                L.video_collage_designer.media.menu_item_all_media,
                L.video_collage_designer.media.menu_item_video,
                L.video_collage_designer.media.menu_item_image,
                L.video_collage_designer.media.menu_item_color_board,][index]
            self.exist_click(L.video_collage_designer.media.menu_media)
            self.exist_click(target)
            time.sleep(DELAY_TIME)
            return True

        @step('[Action][VideoCollageDesigner][Media] Click [Auto Fill] button')
        def click_auto_fill(self):
            self.exist_click(L.video_collage_designer.media.btn_auto_fill)
            time.sleep(DELAY_TIME*0.5)
            return True
        
        @step('[Action][VideoCollageDesigner][Media] Select media by name')
        def select_media(self, name):
            target = copy.deepcopy(L.video_collage_designer.media.template)
            target["AXValue"] = name
            self.mouse.click(*self.exist(target).center)
            time.sleep(DELAY_TIME*0.5)

        def select_multiple_media(self, *args):
            self.activate()
            self.select_media(args[0])
            with self.keyboard.pressed(self.keyboard.key.cmd_l):
                for name in args[1:]:
                    self.select_media(name)
            return True


        def is_exist_media(self, name, timeout=5):
            target = copy.deepcopy(L.video_collage_designer.media.template)
            target["AXValue"] = name
            return self.is_exist(target, timeout=timeout)

    class Layout(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.library = self.Library(*args, **kwargs)

        def hover_layout(self, index):
            locator = copy.deepcopy(L.video_collage_designer.layout.templates)
            locator["AXIndex"] = index
            frame_layout = self.exist(L.video_collage_designer.layout.frame)
            x_min, _ = frame_layout.AXPosition
            w, _ = frame_layout.AXSize
            x_max = x_min + w
            retry = index
            logger(f"{x_min=}, {x_max=}")
            while not (target := self.exist(locator, timeout=0, no_warning=True)):
                self.exist_press(L.video_collage_designer.layout.arrow_right)
                time.sleep(DELAY_TIME)
                if not (retry := retry -1):
                    logger(f"Unable to find the layout. {index=}")
                    raise Exception(f"Unable to find the layout. {index=}")
            retry = 32
            while retry := retry - 1:
                logger(f"{target.AXPosition=}")
                if target.AXPosition[0] < x_min:
                    self.exist_press(L.video_collage_designer.layout.arrow_left)
                elif target.AXPosition[0] >= x_max:
                    self.exist_press(L.video_collage_designer.layout.arrow_right)
                else:
                    self.mouse.move(*target.center)
                    return target
                    # return True
                time.sleep(DELAY_TIME)  # wait animation stop
            else:
                logger("Unable to find the template")
                return False
        @step('[Action][VideoCollageDesigner][Layout] Select layout')
        def select_layout(self, index):
            self.hover_layout(index)
            self.mouse.click()
            time.sleep(DELAY_TIME)
            return True

        def remove_layout(self, index):
            self.hover_layout(index)
            self.mouse.click(btn="right")
            self.select_right_click_menu("Delete (only for Custom/Downloaded)")
            self.click_remove_yes()
            return True

        def select_category(self, index):
            target = [L.video_collage_designer.layout.menu_item_all,
                      L.video_collage_designer.layout.menu_item_custom,
                      L.video_collage_designer.layout.menu_item_downloaded][index]
            self.exist_click(L.video_collage_designer.layout.menu_category)
            self.exist_click(target)
            return True

        def open_layout_library(self):
            self.exist_press(L.video_collage_designer.layout.btn_layout_library)
            return True

        @step('[Action][VideoCollageDesigner][Layout] Remove layout with [Yes]')
        def click_remove_yes(self):
            return bool(self.exist_click(L.video_collage_designer.layout.btn_yes))

        def click_remove_no(self):
            return bool(self.exist_click(L.video_collage_designer.layout.btn_no))

        def click_scroll_right(self):
            return bool(self.exist_press(L.video_collage_designer.layout.arrow_right))

        def click_scroll_left(self):
            return bool(self.exist_press(L.video_collage_designer.layout.arrow_left))

        class Library(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            def set_scroll_bar(self, value):
                try:
                    self.exist(L.video_collage_designer.layout.library.scroll_bar).AXValue = value
                    return True
                except Exception as e:
                    logger(f"[Warning] {e=}")
                    return False

            def select_category(self, index):
                target = [L.video_collage_designer.layout.library.menu_item_all,
                          L.video_collage_designer.layout.library.menu_item_custom,
                          L.video_collage_designer.layout.library.menu_item_downloaded][index]
                self.exist_click(L.video_collage_designer.layout.library.menu_category)
                self.exist_click(target)
                return True

            def click_zoom(self):
                return bool(self.exist_click(L.video_collage_designer.layout.library.btn_zoom))

            def select_layout(self, index):
                templates = self.exist(L.video_collage_designer.layout.library.templates)
                self.mouse.click(*templates[index].center)
                return True

            def click_ok(self):
                return bool(self.exist_click(L.video_collage_designer.layout.library.btn_ok))

            def click_cancel(self):
                return bool(self.exist_click(L.video_collage_designer.layout.library.btn_cancel))

    class Share_to(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def set_name(self, name):
            self.exist(L.video_collage_designer.save_as.input_name).AXValue = name
            return True

        def press_ok(self):
            self.press(L.video_collage_designer.save_as.btn_ok)
            return True

        def press_auto_sign_in_checkbox(self):
            return bool(self.exist_press(L.video_collage_designer.share.checkbox_auto_sign_in, timeout=3))

        def press_auto_sign_in_ok(self):
            return bool(self.exist_press(L.video_collage_designer.share.btn_auto_sign_in_ok))

        def press_category_menu(self):
            self.exist_click(L.video_collage_designer.share.menu_upload_to, timeout=30)
            return True

        def select_category_item(self, option):
            target = [
                L.video_collage_designer.share.menu_item_cloud_and_dz,
                L.video_collage_designer.share.menu_item_cloud,
                L.video_collage_designer.share.menu_item_dz,
            ][option]
            self.exist_click(target)
            time.sleep(DELAY_TIME*2)

        def set_tag(self, value):
            self.exist_click(L.video_collage_designer.share.input_tag)
            self.exist(L.video_collage_designer.share.input_tag).AXValue = value

        def set_collection(self, value):
            self.exist_click(L.video_collage_designer.share.input_collection)
            self.exist(L.video_collage_designer.share.input_collection).AXValue = value

        def set_description(self, value):
            self.exist_click(L.video_collage_designer.share.input_description)
            self.exist(L.video_collage_designer.share.input_description).AXValue = value

        def press_next_button(self):
            self.exist_click(L.video_collage_designer.share.btn_next)

        def press_confirm_button(self):
            ret = bool(self.exist_click(L.video_collage_designer.share.btn_confirm))
            time.sleep(DELAY_TIME)
            return ret

        def press_finish_button(self):
            self.exist(L.video_collage_designer.share.btn_finish, timeout=60).press()
            return True

    class Preview(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def set_duration(self, timecode):
            '''
            :param timecode: "HH_MM_SS_mm" -> "1_00_59_99"
            '''
            self.activate()
            elem = self.find(L.video_collage_designer.preview.timecode_duration)
            w, h = elem.AXSize
            x, y = elem.AXPosition

            pos_click = tuple(map(int, (x + w * 0.1, y + h * 0.5)))
            self.mouse.click(*pos_click)
            time.sleep(DELAY_TIME)
            self.keyboard.send(timecode.replace("_", ""))
            self.keyboard.enter()
            return True

        def click_duration_ok(self):
            self.exist_click(L.video_collage_designer.preview.btn_ok)
            return True
        
        def _open_right_click_menu(self):
            elelm_menu = self.exist(L.video_collage_designer.border.menu_frame_animation)
            ori_pos = elelm_menu.AXPosition
            size_w, size_h = elelm_menu.AXSize
            target_slot_pos = (ori_pos[0] - size_w, ori_pos[1])
            self.mouse.move(target_slot_pos[0], target_slot_pos[1])
            self.right_click()
            time.sleep(DELAY_TIME)
            
        
        @step('[Action][VideoCollageDesigner][Preview] Enter [Dutation Settings] Window by Right Click Menu')
        def enter_duration_setting_by_right_click_menu(self):
            self._open_right_click_menu()
            self.select_right_click_menu('Set duration...')

        @step('[Action][VideoCollageDesigner][Preview] Remove Clip on Preview by Right Click Menu')
        def remove_clip_on_preview_by_right_click_menu(self):
            self._open_right_click_menu()
            return self.select_right_click_menu('Remove')
        
        @step('[Action][VideoCollageDesigner][Preview] Exchange Media by Drag Mouse on Preview')
        def exchange_media_by_drag_mouse_on_preview(self):
            elelm_menu = self.exist(L.video_collage_designer.border.menu_frame_animation)
            ori_pos = elelm_menu.AXPosition
            size_w, size_h = elelm_menu.AXSize
            target_slot_pos = (ori_pos[0] - size_w, ori_pos[1])
            upper_slot_pos = (ori_pos[0] - size_w, ori_pos[1] - size_h * 5)
            self.drag_mouse(upper_slot_pos, target_slot_pos)
            time.sleep(DELAY_TIME)
        
        @step('[Action][VideoCollageDesigner][Preview] Hover on slot with layout 10')
        def hover_on_slot_with_layout_10(self, times_of_size_w, times_of_size_h): # only enable to hover on slot 3 with layout 10 now
            # Mouse Hover Slot 3
            elelm_menu = self.exist(L.video_collage_designer.border.menu_frame_animation)
            ori_pos = elelm_menu.AXPosition
            size_w, size_h = elelm_menu.AXSize
            target_slot_pos = (ori_pos[0] - size_w * times_of_size_w, ori_pos[1]- size_h * times_of_size_h)
            self.mouse.move(target_slot_pos[0], target_slot_pos[1])
            if not self.exist(locator=L.video_collage_designer.preview.btn_mute):
                raise Exception("Mute button doesn't exist after hover on slot. Please check if icon not display or not hover on slot.")
        

        class Zoom(BasePage):
            @step('[Action][VideoCollageDesigner][Preview][Zoom] Zoom In by Arrow')
            def zoom_in_by_arrow(self, times):
                for _ in range(times):
                    self.exist_click(L.video_collage_designer.preview.btn_zoom_in)
                    time.sleep(DELAY_TIME*0.5)
                return True
            
            @step('[Action][VideoCollageDesigner][Preview][Zoom] Zoom Out by Arrow')
            def zoom_out_by_arrow(self, times):
                for _ in range(times):
                    self.exist_click(L.video_collage_designer.preview.btn_zoom_out)
                    time.sleep(DELAY_TIME*0.5)
                return True
            
            @step('[Action][VideoCollageDesigner][Preview][Zoom] Zoom by Slider')
            def zoom_by_slider(self, value):
                self.exist(L.video_collage_designer.preview.slider_zoom).AXValue = value
                return True
        
        class Trim(BasePage):
            @step('[Action][VideoCollageDesigner][Preview][Trim] Click [Trim] button and check opened Trim Window')
            def open_trim_window(self):
                try:
                    self.click(L.video_collage_designer.preview.btn_trim)
                    time.sleep(DELAY_TIME * 0.5)
                    if not self.exist(L.trim.main_window):
                        raise Exception("Not in Trim Window")
                    if self.exist(L.trim.main_window).AXTitle.startswith('Trim |'):
                        return True
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception(f'Exception occurs. log={e}')
