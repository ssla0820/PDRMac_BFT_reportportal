import time, datetime, os, copy

from .base_page import BasePage
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
# from AppKit import NSScreen
from .locator import locator as L
from reportportal_client import step

OPERATION_DELAY = 1 # sec

def arrow(obj, button="up", times=1, locator=None):
    locator = locator[button.lower() == "up"]
    elem = obj.exist(locator)
    for _ in range(times):
        elem.press()
    return True


class DownloadFromCLDZ(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.download_project = self.Download_project(*args, **kwargs)
        self.upload_project = self.Upload_project(*args, **kwargs)
        self.pack_project_and_upload = self.Pack_project_and_upload(*args, **kwargs)

    def has_window(self, partial_title):
        # consider about performance, do not find dialog title directly
        win_list = self.find({"AXRole":"AXWindow", "recursive":False, "get_all":True})
        for win in win_list:
            print(f"{win=}")
            try:
                if partial_title in self.exist(L.base.download_window_title, timeout=0).AXValue: return True
            except:
                pass
        return False

    def switch_tab(self, name, timeout=60):
        locator = [L.download_from_cl_dz.cloud,
                   L.download_from_cl_dz.dz][name.lower() == "dz"]
        btn = self.exist(locator)
        btn.press()
        time.sleep(1)
        timer=time.time()
        display_sec = 0
        while (sec := time.time()-timer) < timeout:
            if btn.AXEnabled: return True
            time.sleep(0.4)
            if display_sec != sec: logger(f"wait for loading - {display_sec} sec")
        else:
            logger("[Warning] Timeout!")
        return True

    def tap_close_button(self):
        self.exist(L.download_from_cl_dz.close).press()
        return True

    def tap_select_deselect_all(self):
        self.exist(L.download_from_cl_dz.select_deselect_all).press()
        return True

    def tap_download(self):
        self.exist(L.download_from_cl_dz.download).press()
        self.is_exist({"AXTitle": "Cancel", "AXRole": "AXButton"}, timeout=3)
        self.is_not_exist({"AXTitle":"Cancel","AXRole":"AXButton"},timeout=3)
        return True

    def set_search_text(self, text):
        elem = self.exist(L.download_from_cl_dz.search)
        self.mouse.click(*elem.center)
        elem.AXValue = text
        return True

    def tap_clear_search_button(self):
        self.exist(L.download_from_cl_dz.reset_search).press()
        return True

    def hover_sort_by(self):
        self.mouse.click(*self.exist(L.download_from_cl_dz.library_menu).center)
        self.select_right_click_menu("Sort by")

    def apply_sory_by_name(self):
        self.mouse.click(*self.exist(L.download_from_cl_dz.library_menu).center)
        self.select_right_click_menu("Sort by", "Name")
        return True

    def apply_sory_by_upload_date(self):
        self.mouse.click(*self.exist(L.download_from_cl_dz.library_menu).center)
        self.select_right_click_menu("Sort by", "Upload Date")
        return True

    def apply_show_extra_large_icons(self):
        self.mouse.click(*self.exist(L.download_from_cl_dz.library_menu).center)
        self.select_right_click_menu("Extra Large Icons")
        return True

    def apply_show_large_icons(self):
        self.mouse.click(*self.exist(L.download_from_cl_dz.library_menu).center)
        self.select_right_click_menu("Large Icons")
        return True

    def apply_show_medium_icons(self):
        self.mouse.click(*self.exist(L.download_from_cl_dz.library_menu).center)
        self.select_right_click_menu("Medium Icons")
        return True

    def apply_show_small_icons(self):
        self.mouse.click(*self.exist(L.download_from_cl_dz.library_menu).center)
        self.select_right_click_menu("Small Icons")
        return True

    def apply_show_details(self):
        self.mouse.click(*self.exist(L.download_from_cl_dz.library_menu).center)
        self.select_right_click_menu("Details")
        return True


    def signin_dz(self, auto_signin=True):
        btn_auto_signin = self.exist(L.download_from_cl_dz.signin.auto_signin)
        if btn_auto_signin.AXValue != int(auto_signin): btn_auto_signin.press()
        self.exist(L.download_from_cl_dz.signin.yes).press()
        return True

    @step('[Action][DownloadFromCLDZ] Select template')
    def select_template(self, name):
        locator = copy.deepcopy(L.download_from_cl_dz.template)
        locator[-1]["AXValue"] = name
        time.sleep(3)
        self.mouse.click(*self.exist(locator).center)
        time.sleep(OPERATION_DELAY)
        return True
    
    @step('[Action][DownloadFromCLDZ] Delete template')
    def tap_delete_button(self):
        self.exist_click(L.download_from_cl_dz.delete)
        time.sleep(OPERATION_DELAY*2)
        self.click(L.download_from_cl_dz.delete_dialog.ok)
        time.sleep(OPERATION_DELAY*2)
        return True

    def is_selected_templates(self, number):
        text = self.exist(L.download_from_cl_dz.template_selected).AXValue
        value = int(text.replace(" template(s) selected",""))
        return number == value

    def select_category(self, index):
        locator = [
            None,
            L.download_from_cl_dz.category.my_upload,
            L.download_from_cl_dz.category.download_history,
            L.download_from_cl_dz.category.my_favorites,][index]
        self.exist_click(L.download_from_cl_dz.category.button)
        self.exist_click(locator)
        return True

    class Download_project(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.process_dialog = self.Process_dialog(*args, **kwargs)
            self.downloaded = self.Downloaded(*args, **kwargs)

        def click_close(self):
            self.exist_click(L.download_from_cl_dz.download_project.close)
            return self.is_not_exist({"AXTitle": "Cancel", "AXRole": "AXButton"}, timeout=3)


        def caption_name(self):
            try:
                return self.exist(L.download_from_cl_dz.download_project.caption).AXValue
            except:
                return None

        def sort_by_name(self, increase=True):
            self.exist_click(L.download_from_cl_dz.sort.name)
            item = self.exist(L.download_from_cl_dz.sort.name).AXSortDirection
            if item == 'AXAscendingSortDirection':
                token = True
            else:
                token = False
            if increase != token:
                self.exist_click(L.download_from_cl_dz.sort.name)
            return True

        def sort_by_date(self, increase=True):
            self.exist_click(L.download_from_cl_dz.sort.date)
            item = self.exist(L.download_from_cl_dz.sort.date).AXSortDirection
            if item == 'AXAscendingSortDirection':
                token = True
            else:
                token = False
            if increase != token:
                self.exist_click(L.download_from_cl_dz.sort.date)
            return True

        def sort_by_size(self, increase=True):
            self.exist_click(L.download_from_cl_dz.sort.size)
            item = self.exist(L.download_from_cl_dz.sort.size).AXSortDirection
            if item == 'AXAscendingSortDirection':
                token = True
            else:
                token = False
            if increase != token:
                self.exist_click(L.download_from_cl_dz.sort.size)
            return True

        def sort_by_type(self, increase=True):
            self.exist_click(L.download_from_cl_dz.sort.type)
            item = self.exist(L.download_from_cl_dz.sort.type).AXSortDirection
            if item == 'AXAscendingSortDirection':
                token = True
            else:
                token = False
            if increase != token:
                self.exist_click(L.download_from_cl_dz.sort.type)
            return True

        def select_project(self, name):
            items = self.exist(L.download_from_cl_dz.download_project.project_list_item, timeout=15)
            for item in items:
                if item.AXValue.strip() == name:
                    self.mouse.click(*item.center)
                    return True
            return False

        def find_project(self, name):
            items = self.exist(L.download_from_cl_dz.download_project.project_list_item)
            for item in items:
                if item.AXValue.strip() == name:
                    return True
            return False

        def get_del_status(self):
            return self.exist(L.download_from_cl_dz.download_project.delete).AXEnabled

        def click_delete(self):
            if self.get_del_status():
                self.exist_click(L.download_from_cl_dz.download_project.delete)
                return True
            else:
                logger('Delete is not enabled')
                return False

        def handle_warning_msg(self, option='ok'):
            if option == 'ok':
                self.exist_click(L.download_from_cl_dz.download_project.warning_msg.ok)
                return True
            elif option == 'cancel':
                self.exist_click(L.download_from_cl_dz.download_project.warning_msg.cancel)
                return True
            else:
                logger('wrong input')
                return False

        def click_download(self):
            self.exist_click(L.download_from_cl_dz.download_project.download)
            time.sleep(OPERATION_DELAY)
            return True

        def click_cancel(self):
            self.exist_click(L.download_from_cl_dz.download_project.cancel)
            return self.is_not_exist({"AXTitle": "Cancel", "AXRole": "AXButton"}, timeout=3)

        def select_download_folder(self, full_path):
            try:
                self.select_file(full_path)
                time.sleep(OPERATION_DELAY * 3)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True




        class Process_dialog(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            def click_cancel(self):
                self.exist_click(L.download_from_cl_dz.download_project.process_dialog.cancel)
                return self.is_not_exist({'AXIdentifier': 'IDC_CLOUDPROGRESS_PROGRESS_BTN_CANCEL'}, timeout=3)

            def check_main_window(self):
                return self.is_exist({'AXIdentifier': 'IDC_CLOUDPROGRESS_PROGRESS_BTN_CANCEL'}, timeout=3)

            def check_remain_time(self):
                return self.exist(L.download_from_cl_dz.download_project.process_dialog.remain_time).AXValue




        class Downloaded(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            def click_open(self):
                self.exist_click(L.download_from_cl_dz.download_project.downloaded.open)
                return True

            def click_ok(self):
                self.exist_click(L.download_from_cl_dz.download_project.downloaded.ok)
                return True

            def check_main_window(self):
                return self.is_exist({'AXIdentifier': 'IDC_DOWNLOAD_PROJECT_RESULT_DLG'}, timeout=3)


    class Upload_project(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.uploaded = self.Uploaded(*args, **kwargs)

        def get_project_name(self):
            return self.exist(L.download_from_cl_dz.upload_project.project_name).AXValue

        def set_project_name(self, name):
            self.exist(L.download_from_cl_dz.upload_project.project_name).AXValue = name
            return True

        def click_close(self):
            self.exist_click(L.download_from_cl_dz.upload_project.close)
            return self.is_not_exist({'AXIdentifier': 'IDC_UPLOAD_PROJECT_CANCEL'}, timeout=3)

        def click_cancel(self):
            self.exist_click(L.download_from_cl_dz.upload_project.cancel)
            return self.is_not_exist({'AXIdentifier': 'IDC_UPLOAD_PROJECT_CANCEL'}, timeout=3)

        def click_ok(self):
            self.exist_click(L.download_from_cl_dz.upload_project.ok)
            time.sleep(OPERATION_DELAY * 3)
            return True

        def handle_warning_msg(self, option='ok'):
            if option == 'ok':
                self.exist_click(L.download_from_cl_dz.upload_project.warning_msg.ok)
                return True
            elif option == 'cancel':
                self.exist_click(L.download_from_cl_dz.upload_project.warning_msg.cancel)
                return True
            else:
                logger('wrong input')
                return False

        class Uploaded(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            def click_link(self):
                self.exist_click(L.download_from_cl_dz.upload_project.uploaded.link)
                time.sleep(OPERATION_DELAY * 2)
                self.activate()
                return True

            def click_ok(self):
                self.exist_click(L.download_from_cl_dz.upload_project.uploaded.ok)
                return self.is_not_exist({'AXIdentifier': 'IDC_UPLOAD_PROJECT_OK'}, timeout=3)

    class Pack_project_and_upload(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.uploaded = self.Uploaded(*args, **kwargs)

        def get_project_name(self):
            return self.exist(L.download_from_cl_dz.pack_project_and_upload.project_name).AXValue

        def set_project_name(self, name):
            self.exist(L.download_from_cl_dz.pack_project_and_upload.project_name).AXValue = name
            return True

        def click_close(self):
            self.exist_click(L.download_from_cl_dz.pack_project_and_upload.close)
            return self.is_not_exist({'AXIdentifier': 'IDC_UPLOAD_PROJECT_DLG'}, timeout=3)

        def click_cancel(self):
            self.exist_click(L.download_from_cl_dz.pack_project_and_upload.cancel)
            return self.is_not_exist({'AXIdentifier': 'IDC_UPLOAD_PROJECT_DLG'}, timeout=3)

        def click_ok(self):
            self.exist_click(L.download_from_cl_dz.pack_project_and_upload.ok)
            time.sleep(OPERATION_DELAY * 5)
            return True

        def handle_warning_msg(self, option='ok'):
            if option == 'ok':
                self.exist_click(L.download_from_cl_dz.pack_project_and_upload.warning_msg.ok)
                return True
            elif option == 'cancel':
                self.exist_click(L.download_from_cl_dz.pack_project_and_upload.warning_msg.cancel)
                return True
            else:
                logger('wrong input')
                return False

        class Uploaded(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            def check_main_window(self):
                return self.is_exist(L.download_from_cl_dz.upload_project.uploaded.ok, timeout=100)

            def click_link(self):
                self.exist_click(L.download_from_cl_dz.upload_project.uploaded.link)
                time.sleep(OPERATION_DELAY * 2)
                self.activate()
                return True

            def click_ok(self):
                self.exist_click(L.download_from_cl_dz.upload_project.uploaded.ok)
                return self.is_not_exist({'AXIdentifier': 'IDC_UPLOAD_PROJECT_OK'}, timeout=3)


"""
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
        self.find(L.playback_window.save_as.file_name).AXValue = value
        self.find(L.playback_window.save_as.ok).press()
        return True

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
        name = ["None", "None", "2 x 2", "3 x 3", "4 x 4", "5 x 5"
                          "6 x 6", "7 x 7", "8 x 8", "9 x 9"][index]
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

