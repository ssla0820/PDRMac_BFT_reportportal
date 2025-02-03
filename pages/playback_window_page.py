import time, datetime, os, copy

from .base_page import BasePage
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
# from AppKit import NSScreen
from .locator import locator as L

OPERATION_DELAY = 1 # sec

def arrow(obj, button="up", times=1, locator=None):
    locator = locator[button.lower() == "up"]
    elem = obj.exist(locator)
    for _ in range(times):
        elem.press()
    return True




class Playback_window(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = self.ContextMenu(*args, **kwargs)
        self.floating_menu = self.FloatingMenu(*args, **kwargs)

    class ContextMenu(BasePage):
        def __init__(self,*args, **kwargs):
            super().__init__(*args, **kwargs)

        def _right_click_menu(self):
            self.exist_click(self.area.preview.main , btn="right")

        def click_play_pause(self):
            self._right_click_menu()
            return bool(self.exist_click(L.playback_window.context_menu.play))

        def click_stop(self):
            self._right_click_menu()
            return bool(self.exist_click(L.playback_window.context_menu.stop))

        def click_previous_frame(self):
            self._right_click_menu()
            return bool(self.exist_click(L.playback_window.context_menu.previous_frame))

        def click_next_frame(self):
            self._right_click_menu()
            return bool(self.exist_click(L.playback_window.context_menu.next_frame))

        def click_fastforward(self):
            self._right_click_menu()
            return bool(self.exist_click(L.playback_window.context_menu.fast_forward))

        def click_snapshot(self):
            self._right_click_menu()
            self.exist_click(L.playback_window.context_menu.snapshot)

        def _click_quality(self, operation):
            self._right_click_menu()
            return self.select_right_click_menu("Preview Quality", operation + " Preview Resolution")

        def click_quality_ultra_hd(self):
            return self._click_quality("Ultra HD")

        def click_quality_full_hd(self):
            return self._click_quality("Full HD")

        def click_quality_hd(self):
            return self._click_quality("HD")

        def click_quality_high(self):
            return self._click_quality("High")

        def click_quality_normal(self):
            return self._click_quality("Normal")

        def click_quality_low(self):
            return self._click_quality("Low")

        def click_previous_sec(self):
            self._right_click_menu()
            return self.select_right_click_menu("Go to", "Go to Previous Second")

        def click_next_sec(self):
            self._right_click_menu()
            return self.select_right_click_menu("Go to", "Go to Next Second")

        def _click_edit(self, operation):
            self._right_click_menu()
            return self.select_right_click_menu("Edit", operation)

        def click_edit_modify(self):
            return self._click_edit("Modify...")

        def click_edit_trim(self):
            return self._click_edit("Trim...")

        def click_edit_fix_enhance(self):
            return self._click_edit("Fix/Enhance")

        def click_edit_pan_and_zoom(self):
            return self._click_edit("Pan & Zoom")

        def click_dock_undock_preview_window(self):
            self._right_click_menu()
            return self.select_right_click_menu("Dock/Undock Preview Window")

        def _click_zoom(self, operation):
            self._right_click_menu()
            return self.select_right_click_menu("Zoom", operation)

        def click_zoom_fit(self):
            return self._click_zoom("Fit")

        def click_zoom_10(self):
            return self._click_zoom("10%")

        def click_zoom_25(self):
            return self._click_zoom("25%")

        def click_zoom_50(self):
            return self._click_zoom("50%")

        def click_zoom_75(self):
            return self._click_zoom("75%")

        def click_zoom_100(self):
            return self._click_zoom("100%")

        def click_zoom_200(self):
            return self._click_zoom("200%")

        def click_zoom_300(self):
            return self._click_zoom("300%")

        def click_zoom_400(self):
            return self._click_zoom("400%")

    def set_timeline_sliderbar(self, value):
        sliderbar = self.find(L.playback_window.slider)
        if 0 < value < 1:
            max , min = sliderbar.AXMaxValue, sliderbar.AXMinValue
            sliderbar.AXValue = int((max-min)*value)
        else:
            sliderbar.AXValue = int(value)
        return True

    def get_timeline_slidebar(self):
        return int(float(self.find(L.playback_window.slider).AXValue))

    def set_timecode_slidebar(self,timecode):
        elem = self.find(L.playback_window.timecode)
        w, h = elem.AXSize
        x, y = elem.AXPosition
        pos_click = tuple(map(int, (x + w * 0.1, y + h * 0.5)))
        self.mouse.click(*pos_click)
        time.sleep(1)
        self.keyboard.send(timecode.replace("_", ""))
        self.keyboard.enter()
        return True

    def get_timecode_slidebar(self):
        return self.find(L.playback_window.timecode).AXValue

    def Viewer_Zoom_dropdown_menu(self, value="Fit"):
        category = self.exist(L.playback_window.zoom)
        category._activate()
        self.mouse.click(*category.center)
        option_locator = L.playback_window.zoom_value.copy()
        option_locator.append({"AXValue": value})
        zoom_value = self.exist(option_locator)
        self.mouse.click(*zoom_value.center)
        return True

    def Edit_Timeline_PreviewOperation(self, operation):
        self.find(getattr(L.playback_window.operation, operation.lower())).press()
        return True

    def Edit_TimelinePreview_ClickTakeSnapshot(self):
        self.find(L.playback_window.take_snapshot).press()
        return True

    def Edit_SaveAsSanpshot_FileName(self, value):
        return self.select_file(value)

    def Edit_TimelinePreview_SetPreviewQuality(self, operation):
        self.find(L.playback_window.set_quality).press()
        time.sleep(1)
        self.select_right_click_menu("Preview Quality",operation + " Preview Resolution")
        return True

    def Edit_TimelinePreview_GetPreviewQuality(self):
        self.find(L.playback_window.set_quality).press()
        elem = self.select_right_click_menu("Preview Quality", return_elem=True)
        ret = elem.findAll(AXRole="AXMenu")[0].findAll(AXMenuItemMarkChar="✓")[0].AXTitle
        self.mouse.click(0,0)
        return ret

    def Edit_TimelinePreview_Click_SetPreviewQuality_btn(self):
        self.find(L.playback_window.set_quality).press()
        return True

    def Edit_Timeline_Grid_line_format(self, index=1):
        name = ["None", "None", "2 x 2", "3 x 3", "4 x 4", "5 x 5",
                "6 x 6", "7 x 7", "8 x 8", "9 x 9", "10 x 10"][index]
        self.find(L.playback_window.set_quality).press()
        self.select_right_click_menu("Grid Lines", name)
        return True

    def Edit_TimelinePreview_ClickDock(self):
        self.exist(L.playback_window.dock).press()
        return True

    def Edit_TimelinePreview_ClickUnDock(self):
        self.exist(L.playback_window.undock).press()
        return True

    def Edit_TimelinePreview_ClickMaximize_RestoreDown(self):
        self.press(L.playback_window.popup_window.max_restore)
        return True

    def Edit_TImelinePreview_ClickMinimize(self):
        self.press(L.playback_window.popup_window.minimize)
        return True

    def Edit_TimelinePreview_ClickShowTimelinePreview(self):
        self.exist_click(L.media_room.top_tool_bar.btn_show_minimized_library_window)
        self.exist_click(L.media_room.top_tool_bar.option_timeline_preview)
        return bool(self.exist(L.playback_window.popup_window.main))

    def Edit_TimelinePreview_DoubleClick_EnterFullScreen(self):
        self.activate()
        time.sleep(2)
        self.click(L.playback_window.popup_window.toolbar,times=2)
        return True

    def Edit_TImelinePreview_ClickViewFullScreen(self):
        self.click(L.playback_window.popup_window.full_screen)
        return True

    def adjust_timeline_preview_on_canvas_arrow_key_move_up(self, times=1):
        try:
            self.exist(L.playback_window.focus_canvas_object).activate()
            time.sleep(OPERATION_DELAY * 0.5)
            for x in range(times):
                self.keyboard.up()
                time.sleep(OPERATION_DELAY * 0.3)
        except Exception as e:
            logger(f'Exception occurs. error={e}')
            return False
        return True

    def adjust_timeline_preview_on_canvas_arrow_key_move_down(self, times=1):
        try:
            self.exist(L.playback_window.focus_canvas_object).activate()
            time.sleep(OPERATION_DELAY * 0.5)
            for x in range(times):
                self.keyboard.down()
                time.sleep(OPERATION_DELAY * 0.3)
        except Exception as e:
            logger(f'Exception occurs. error={e}')
            return False
        return True

    def adjust_timeline_preview_on_canvas_arrow_key_move_left(self, times=1):
        try:
            self.exist(L.playback_window.focus_canvas_object).activate()
            time.sleep(OPERATION_DELAY * 0.5)
            for x in range(times):
                self.keyboard.left()
                time.sleep(OPERATION_DELAY * 0.3)
        except Exception as e:
            logger(f'Exception occurs. error={e}')
            return False
        return True

    def adjust_timeline_preview_on_canvas_arrow_key_move_right(self, times=1):
        try:
            self.exist(L.playback_window.focus_canvas_object).activate()
            time.sleep(OPERATION_DELAY * 0.5)
            for x in range(times):
                self.keyboard.right()
                time.sleep(OPERATION_DELAY * 0.3)
        except Exception as e:
            logger(f'Exception occurs. error={e}')
            return False
        return True

    def adjust_timeline_preview_on_canvas_resize_to_small(self):
        try:
            el_canvas = self.exist(L.playback_window.focus_canvas_object)
            el_canvas.activate()
            pos_canvas = el_canvas.AXPosition
            size_canvas = el_canvas.AXSize
            time.sleep(OPERATION_DELAY * 0.5)
            top_right_x = pos_canvas[0] + size_canvas[0]
            top_right_y = pos_canvas[1]
            self.drag_mouse((top_right_x, top_right_y), (top_right_x-80, top_right_y+45))
            time.sleep(OPERATION_DELAY * 0.5)
        except Exception as e:
            logger(f'Exception occurs. error={e}')
            return False
        return True

    def adjust_timeline_preview_on_canvas_resize_to_large(self):
        try:
            el_canvas = self.exist(L.playback_window.focus_canvas_object)
            el_canvas.activate()
            pos_canvas = el_canvas.AXPosition
            size_canvas = el_canvas.AXSize
            time.sleep(OPERATION_DELAY * 0.5)
            top_right_x = pos_canvas[0] + size_canvas[0]
            top_right_y = pos_canvas[1]
            self.drag_mouse((top_right_x, top_right_y), (top_right_x+80, top_right_y-45))
            time.sleep(OPERATION_DELAY * 0.5)
        except Exception as e:
            logger(f'Exception occurs. error={e}')
            return False
        return True

    def adjust_timeline_preview_on_canvas_drag_move_to_left(self):
        try:
            el_canvas = self.exist(L.playback_window.focus_canvas_object)
            el_canvas.activate()
            pos_canvas = el_canvas.AXPosition
            size_canvas = el_canvas.AXSize
            time.sleep(OPERATION_DELAY * 0.5)
            center_x = pos_canvas[0] + int(size_canvas[0]/2)
            center_y = pos_canvas[1] + int(size_canvas[1]/2)
            self.drag_mouse((center_x, center_y), (center_x-80, center_y))
            time.sleep(OPERATION_DELAY * 0.5)
        except Exception as e:
            logger(f'Exception occurs. error={e}')
            return False
        return True

    def adjust_timeline_preview_on_canvas_drag_move_to_right(self):
        try:
            el_canvas = self.exist(L.playback_window.focus_canvas_object)
            el_canvas.activate()
            pos_canvas = el_canvas.AXPosition
            size_canvas = el_canvas.AXSize
            time.sleep(OPERATION_DELAY * 0.5)
            center_x = pos_canvas[0] + int(size_canvas[0]/2)
            center_y = pos_canvas[1] + int(size_canvas[1]/2)
            self.drag_mouse((center_x, center_y), (center_x+80, center_y))
            time.sleep(OPERATION_DELAY * 0.5)
        except Exception as e:
            logger(f'Exception occurs. error={e}')
            return False
        return True

    def adjust_timeline_preview_on_canvas_drag_rotate_clockwise(self, radius=26):
        try:
            el_canvas = self.exist(L.playback_window.focus_canvas_object)
            el_canvas.activate()
            pos_canvas = el_canvas.AXPosition
            size_canvas = el_canvas.AXSize

            time.sleep(OPERATION_DELAY * 0.5)
            center_x = pos_canvas[0] + int(size_canvas[0] / 2)
            center_y = pos_canvas[1] + int(size_canvas[1] / 2)
            #center_pos = (center_x, center_y)
            self.mouse.move(center_x+2, pos_canvas[1])
            time.sleep(OPERATION_DELAY * 2)
            self.mouse.move(center_x + 4, pos_canvas[1] - 4)
            time.sleep(OPERATION_DELAY * 2)

            # show double arrow icon
            time.sleep(OPERATION_DELAY * 2)
            self.mouse.move(center_x + 12, pos_canvas[1] - 4)
            center_x_right = pos_canvas[0] + int(size_canvas[0] / 2) + + int(size_canvas[0] / 4)
            # drag to new position
            self.drag_mouse((center_x + 12, pos_canvas[1] - 4), (center_x_right, center_y))
            time.sleep(OPERATION_DELAY * 0.5)

        except Exception as e:
            logger(f'Exception occurs. error={e}')
            return False
        return True

    def adjust_timeline_preview_on_canvas_drag_rotate_anticlockwise(self, radius=26):
        try:
            el_canvas = self.exist(L.playback_window.focus_canvas_object)
            el_canvas.activate()
            pos_canvas = el_canvas.AXPosition
            size_canvas = el_canvas.AXSize
            time.sleep(OPERATION_DELAY * 0.5)
            center_x = pos_canvas[0] + int(size_canvas[0]/2)
            center_y = pos_canvas[1] + int(size_canvas[1]/2)
            self.drag_mouse((center_x+radius, center_y), (center_x, center_y-radius))
            time.sleep(OPERATION_DELAY * 0.5)
        except Exception as e:
            logger(f'Exception occurs. error={e}')
            return False
        return True

    def adjust_timeline_preview_on_canvas_freeform(self):
        try:
            el_canvas = self.exist(L.playback_window.focus_canvas_object)
            el_canvas.activate()
            pos_canvas = el_canvas.AXPosition
            size_canvas = el_canvas.AXSize
            time.sleep(OPERATION_DELAY * 0.5)
            top_right_x = pos_canvas[0] + size_canvas[0] - 5
            top_right_y = pos_canvas[1] + 5
            self.drag_mouse((top_right_x, top_right_y), (top_right_x-280, top_right_y+50))
            time.sleep(OPERATION_DELAY * 0.5)
        except Exception as e:
            logger(f'Exception occurs. error={e}')
            return False
        return True

    def click_title_on_canvas(self):
        #self.exist(L.playback_window.focus_canvas_object).activate()
        self.exist_click(L.playback_window.focus_canvas_object)
        time.sleep(OPERATION_DELAY * 3)
        self.exist_click(L.playback_window.focus_canvas_object, times=2)

        return True

    def unselect_title_on_canvas(self):
        self.move_mouse_to_0_0()
        self.press_esc_key()
        return True


    def edit_title_on_canvas(self, str):
        self.keyboard.send(str)
        return True


    class FloatingMenu(BasePage):
        def __init__(self,*args, **kwargs):
            super().__init__(*args, **kwargs)

        def set_font_type(self, type='Helvetica'):
            el_menu = self.exist(L.playback_window.floating_menu.dialog)
            el_menu.activate()
            self.exist_click(L.playback_window.floating_menu.font_type_button)
            time.sleep(OPERATION_DELAY * 2)
            items = self.exist(L.playback_window.floating_menu.font_type_item)
            for item in items:
                if item.AXValue.strip() == type:
                    self.mouse.click(*item.center)
                    return True
            return False

        def get_font_type(self):
            self.exist_click(L.playback_window.focus_canvas_object)
            time.sleep(OPERATION_DELAY * 3)
            self.exist_click(L.playback_window.focus_canvas_object, times=2)
            return self.exist(L.playback_window.floating_menu.font_type_parent).AXValue

        def set_font_size(self,size):
            el_menu = self.exist(L.playback_window.floating_menu.dialog)
            el_menu.activate()
            self.exist_click(L.playback_window.floating_menu.font_size_button)
            time.sleep(OPERATION_DELAY * 2)
            items = self.exist(L.playback_window.floating_menu.font_size_item)
            for item in items:
                if item.AXValue.strip() == str(size):
                    self.mouse.click(*item.center)
                    return True
            return False

        def get_font_size(self):
            self.exist_click(L.playback_window.focus_canvas_object)
            time.sleep(OPERATION_DELAY * 3)
            self.exist_click(L.playback_window.focus_canvas_object, times=2)
            return self.exist(L.playback_window.floating_menu.font_size_parent).AXValue

        def set_font_color(self, hexcolor=222222):
            el_menu = self.exist(L.playback_window.floating_menu.dialog)
            el_menu.activate()
            self.exist_click(L.playback_window.floating_menu.font_color_button)
            time.sleep(OPERATION_DELAY * 2)
            self.exist_click(L.playback_window.floating_menu.font_color_color_sliders)
            time.sleep(OPERATION_DELAY * 2)
            self.exist_click(L.playback_window.floating_menu.font_color_color_sliders_menu)
            time.sleep(OPERATION_DELAY * 2)
            self.exist_click(L.playback_window.floating_menu.font_color_color_sliders_menu_rgb)
            time.sleep(OPERATION_DELAY * 2)
            self.exist_click(L.playback_window.floating_menu.font_color_color_sliders_menu_rgb_hex).AXValue = str(hexcolor)
            self.press_enter_key()
            time.sleep(OPERATION_DELAY)
            self.press_esc_key()
            time.sleep(OPERATION_DELAY)
            return True

        def get_font_color(self):
            el_menu = self.exist(L.playback_window.floating_menu.dialog)
            el_menu.activate()
            self.exist_click(L.playback_window.floating_menu.font_color_button)
            time.sleep(OPERATION_DELAY * 2)
            self.exist_click(L.playback_window.floating_menu.font_color_color_sliders)
            time.sleep(OPERATION_DELAY * 2)
            self.exist_click(L.playback_window.floating_menu.font_color_color_sliders_menu)
            time.sleep(OPERATION_DELAY * 2)
            self.exist_click(L.playback_window.floating_menu.font_color_color_sliders_menu_rgb)
            time.sleep(OPERATION_DELAY * 2)
            color = self.exist_click(L.playback_window.floating_menu.font_color_color_sliders_menu_rgb_hex).AXValue
            self.press_esc_key()
            time.sleep(OPERATION_DELAY)
            return color

        def get_border_color_status(self):
            el_menu = self.exist(L.playback_window.floating_menu.dialog)
            el_menu.activate()
            return self.exist(L.playback_window.floating_menu.border_color_button).AXEnabled


        def get_shadow_color_status(self):
            el_menu = self.exist(L.playback_window.floating_menu.dialog)
            el_menu.activate()
            return self.exist(L.playback_window.floating_menu.shadow_color_button).AXEnabled

        def click_bold_btn(self):
            self.exist_click(L.playback_window.floating_menu.bold_button)
            return True

        def click_italic_btn(self):
            self.exist_click(L.playback_window.floating_menu.italic_button)
            return True

        def get_bold_status(self):
            return self.exist(L.playback_window.floating_menu.bold_button).AXEnabled

        def get_italic_status(self):
            return self.exist(L.playback_window.floating_menu.italic_button).AXEnabled

    """
    def set_MaskDesigner_timecode(self, timecode):
        '''
        :param timecode: "HH_MM_SS_mm" -> "1_00_59_99"
        :return: True/False
        '''
        self.activate()
        elem = self.find(L.mask_designer.timecode)
        w, h = elem.AXSize
        x, y = elem.AXPosition

        pos_click = tuple(map(int, (x + w * 0.1, y + h * 0.5)))
        self.mouse.click(*pos_click)
        time.sleep(1)
        self.keyboard.send(timecode.replace("_", ""))
        self.keyboard.enter()

    def tap_MaskDesigner_Undo_btn(self):
        self.find(L.mask_designer.undo).press()

    def tap_MaskDesigner_Redo_btn(self):
        self.find(L.mask_designer.redo).press()

    def Edit_MaskDesigner_Only_Show_Selected_track_SetCheck(self, check_it=True):
        checkbox = self.find(L.mask_designer.only_show_selected_track_checkbox)
        if checkbox.AXValue != check_it:
            checkbox.press()
        return True

    def Edit_MaskDesigner_ClickOK(self):
        self.find(L.mask_designer.ok).press()
        return True

    def Edit_MaskDesigner_ClickSaveAs(self):
        self.exist(L.mask_designer.save_as).press()
        return True

    def Edit_MaskDesigner_ClickOK_CustomName(self, name):
        try:
            self.exist(L.mask_designer.save_as).press()
            self.exist(L.mask_designer.save_as_dlg.name).sendKeys(name)
            self.exist(L.mask_designer.save_as_dlg.ok).press()
            return True
        except:
            return False

    def MaskDesigner_SaveAs_SetSlider(self, value):
        try:
            self.exist(L.mask_designer.save_as_dlg.slider).AXValue = float(value)
            return True
        except:
            return False

    def Edit_MaskDesigner_ClickCancel(self, option):
        self.exist(L.mask_designer.cancel).press()
        if option is not None:
            self.exist([L.mask_designer.cancel_dlg.yes,
                        L.mask_designer.cancel_dlg.no,
                        L.mask_designer.cancel_dlg.cancel][option]).press()
        return True

    def Edit_MaskDesigner_ClickShare(self):
        self.exist(L.mask_designer.share).press()

    def drag_Mask_Settings_Scroll_Bar(self, value):
        self.exist(L.mask_designer.settings.scroll_bar).AXValue = float(value)

    def drag_Mask_Properties_Scroll_Bar(self, value):
        self.exist(L.mask_designer.mask_property.scroll_bar).AXValue = float(value)

    def MaskDesigner_Select_category(self, option=0):
        category = self.exist(L.mask_designer.mask_property.category)
        category._activate()
        self.mouse.click(*category.center)
        option_locator = L.mask_designer.mask_property.category_option.copy()
        option_locator[1]["index"] = option
        category_option = self.exist(option_locator)
        self.mouse.click(*category_option.center)
        return True

    def MaskDesigner_Apply_template(self, index):
        template_index = L.mask_designer.mask_property.template.copy()
        template_index["index"] = index
        self.mouse.click(*self.find(template_index).center)
        self.mouse.click(*self.find(template_index).center)  # performance issue? click again
        return True

    def Edit_MaskDesigner_CreateImageMask(self, full_path):
        self.exist(L.mask_designer.mask_property.create_mask).press()
        time.sleep(1)
        self.select_file(full_path)
        return True

    def MaskDesigner_Select_Mask_Alpha_Channel(self, option=1):
        opt = [L.mask_designer.mask_property.gif.use_alpha_channel,
               L.mask_designer.mask_property.gif.convert_grayscale][bool(option)]
        self.exist(opt).press()
        time.sleep(1)
        self.exist(L.mask_designer.mask_property.gif.ok).press()
        return True

    def Edit_MaskDesigner_Invert_mask_SetCheck(self, check=True):
        button = self.exist(L.mask_designer.mask_property.invert_mask)
        if button.AXValue != int(bool(check)): button.press()
        return True

    def Edit_MaskDesigner_Feather_radius_Slider(self, value):
        self.exist(L.mask_designer.mask_property.feather_slider).AXValue = int(value)
        return True

    def Edit_MaskDesigner_Feather_radius_InputValue(self, value):
        self.exist(L.mask_designer.mask_property.feather_slider).AXValue = int(value)
        return True

    def Edit_MaskDesigner_Feather_radius_ArrowButton(self, button="up", times=1):
        return arrow(self, button, times, [
            L.mask_designer.mask_property.feather_down,
            L.mask_designer.mask_property.feather_up,
        ])

    def Edit_MaskDesigner_PreviewOperation(self, operation):
        self.find(getattr(L.mask_designer.preview, operation.lower())).press()
        return True

    def Viewer_Zoom_dropdown_menu(self, value="Fit"):
        category = self.exist(L.mask_designer.zoom)
        category._activate()
        self.mouse.click(*category.center)
        option_locator = L.mask_designer.zoom_value.copy()
        option_locator.append({"AXValue": value})
        zome_value = self.exist(option_locator)
        self.mouse.click(*zome_value.center)
        return True

    def set_snap_ref_line(self, value=True):
        toggle = self.exist(L.mask_designer.toggle_grid_line)
        toggle.activate()
        toggle.press()
        snap_ref_line = self.exist(L.mask_designer.snap_ref_line)
        current = snap_ref_line.AXMenuItemMarkChar is not None
        if current == value:
            self.mouse.click()
        else:
            snap_ref_line.press()
        return True

    def set_grid_line(self, index):
        toggle = self.exist(L.mask_designer.toggle_grid_line)
        toggle.activate()
        toggle.press()
        grid_line = self.exist(L.mask_designer.grid_line)
        self.mouse.move(*grid_line.center)
        targer_locator = L.mask_designer.grid_list.copy()
        targer_locator[1]["index"] = index
        target = self.exist(targer_locator)
        self.mouse.click(*target.center)
        return True

    def Get_MaskDesigner_Feather_radius_CurrentValue(self):
        try:
            return self.find(L.mask_designer.mask_property.feather_slider).AXValue
        except:
            return None

    def Get_MaskDesigner_ObjectSetting_PositionX_Value(self):
        try:
            return self.find(L.mask_designer.settings.position_x_value).AXValue
        except:
            return None

    def Get_MaskDesigner_ObjectSetting_PositionY_Value(self):
        try:
            return self.find(L.mask_designer.settings.position_y_value).AXValue
        except:
            return None

    def Get_MaskDesigner_ObjectSetting_ScaleWidth_Value(self):
        try:
            return self.find(L.mask_designer.settings.scale_width_value).AXValue
        except:
            return None

    def Get_MaskDesigner_ObjectSetting_ScaleHigh_Value(self):
        try:
            return self.find(L.mask_designer.settings.scale_height_value).AXValue
        except:
            return None

    def Get_MaskDesigner_ObjectSetting_Opacity_Value(self):
        try:
            return self.find(L.mask_designer.settings.opacity_value).AXValue
        except:
            return None

    def Get_MaskDesigner_ObjectSetting_Rotation_Value(self):
        try:
            return self.find(L.mask_designer.settings.rotation_value).AXValue
        except:
            return None

    def Edit_MaskDesigner_CloseWindow(self):
        self.find(L.mask_designer.close).press()
        return True

    def Edit_MaskDesigner_ClickFullScreen(self):
        self.find(L.mask_designer.zoom_window).press()
        return True

    def Edit_MaskDesigner_ClickRestoreScreen(self):
        self.find(L.mask_designer.zoom_window).press()
        return True

    def Edit_MaskDesigner_RemoveCustomMask(self, index):
        template_index = L.mask_designer.mask_property.template.copy()
        template_index["index"] = index
        self.mouse.click(*self.find(template_index).center, btn="right")
        time.sleep(1)
        # self.select_right_click_menu("Remove Mask")
        x= self.find({"AXRole":"AXMenuItem","AXTitle":"Remove Mask"})
        print(f"{x.AXPosition=} / {x.AXSize=} / {x.AXIdentifier=}")
        self.mouse.click(*x.center)
        self.find(L.mask_designer.cancel_dlg.yes).press()
        return True

    def Edit_MaskDesigner_ClickZoomIn(self):
        self.find(L.mask_designer.zoom_in).press()
        return True

    def Edit_MaskDesigner_ClickZoomOut(self):
        self.find(L.mask_designer.zoom_out).press()
        return True

    def Get_MaskDesigner_ViewerZoomValue(self):
        try:
            return self.find(L.mask_designer.zoom).AXTitle
        except:
            return None

    """
