import time, datetime, os, copy

from .base_page import BasePage
from .locator import locator as L
from ATFramework.utils import logger
from reportportal_client import step

DELAY_TIME = 1
def arrow(obj, button="up", times=1, locator=None):
    locator = locator[button.lower() == "up"]
    elem = obj.exist(locator)
    for _ in range(times):
        elem.press()
    return True


class My_element(BasePage):
    def __init__(self, *arg, locator):
        super().__init__(*arg)
        self.locator = locator

    def is_enabled(self):
        return self.find(self.locator).AXEnabled


class Video_speed_page(BasePage):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.select_range = self.Select_range(*arg, **kwarg)

    class Select_range(BasePage):
        def __init__(self, *arg, **kwarg):
            super().__init__(*arg,  **kwarg)
            self.upper_create_time_shift = My_element(*arg, locator=L.video_speed.time_shift_1)
            self.lower_create_time_shift = My_element(*arg, locator=L.video_speed.time_shift_2)
            self.reset = My_element(*arg, locator=L.video_speed.reset)

    def check_VideoSpeedDesigner_preveiw(self, file_path, similarity=0.95):
        file_full_path = os.path.abspath(file_path)
        # if not os.path.exists(file_full_path): raise Exception("File is not exist")
        select = self.exist(L.video_speed.tab.selected_range)
        slider = self.exist(L.video_speed.video_slider)
        x, y1 = slider.AXPosition
        w, _ = slider.AXSize
        _, y = select.AXPosition
        h = y1 - y
        current_snapshot = self.image.snapshot(x=x, y=y, h=h, w=w)
        logger(f'{current_snapshot=}')
        return self.compare(file_full_path, current_snapshot, similarity)

    @step('[Action][Video Speed] Set [Timecode] in [Video Speed Designer]')
    def set_VideoSpeedDesigner_timecode(self, timecode):
        '''
        :param timecode: "HH_MM_SS_mm" -> "1_00_59_99"
        '''
        self.activate()
        elem = self.find(L.video_speed.navigation.time_code)
        w, h = elem.AXSize
        x, y = elem.AXPosition

        pos_click = tuple(map(int, (x + w * 0.1, y + h * 0.5)))
        self.mouse.click(*pos_click)
        time.sleep(DELAY_TIME)
        self.keyboard.send(timecode.replace("_", ""))
        self.keyboard.enter()
        return True

    @step('[Action][Video Speed] Select Tab in [Video Speed Designer]')
    def Edit_VideoSpeedDesigner_SelectTab(self, tab):
        target = [L.video_speed.tab.entire_clip,
                  L.video_speed.tab.selected_range][tab.lower() == "selected range"]
        self.find(target).press()
        return True

    def Edit_Question_dlg_ClickButton(self, btn):
        target = [
            L.video_speed.cancel_dialog.ok,
            L.video_speed.cancel_dialog.yes,
            L.video_speed.cancel_dialog.cancel,
            L.video_speed.cancel_dialog.no,
        ][["ok", "yes", "cancel", "no"].index(btn.lower())]
        self.find(target).press()
        return True

    def Edit_VideoSpeedDesigner_EntireClip_NewVideoDuration_SetValue(self, timecode, _locator=None, _clear=False):
        '''
        :param timecode: "HH_MM_SS_mm" -> "1_00_59_99"
        '''
        self.activate()
        elem = self.find(_locator or L.video_speed.new_video.time_code)
        w, h = elem.AXSize
        x, y = elem.AXPosition
        pos_click = tuple(map(int, (x + w * 0.1, y + h * 0.5)))
        self.mouse.click(*pos_click)
        time.sleep(DELAY_TIME)
        if _clear:
            with self.keyboard.pressed(self.keyboard.key.cmd, "a"): time.sleep(0.3)
        self.keyboard.send(timecode.replace("_", ""))
        self.keyboard.enter()
        return True

    def Edit_VideoSpeedDesigner_EntireClip_NewVideoDuration_ArrowButton(self, direction, _locator=None):
        target = (_locator or [
            L.video_speed.new_video.up,
            L.video_speed.new_video.down,
        ])[direction.lower() == "down"]
        elem = self.find(target)
        self.mouse.click(*elem.center)
        return True

    @step('[Action][Video Speed] Set [Sppeed Multiplier] value')
    def Edit_VideoSpeedDesigner_EntireClip_SpeedMultiplier_SetValue(self, multiplier):
        return self.Edit_VideoSpeedDesigner_EntireClip_NewVideoDuration_SetValue(
            str(multiplier),
            L.video_speed.multiplier.value,
            True
        )

    @step('[Action][Video Speed] Set [Speed Multiplier] for [Entire Clip] by dragging the slider')
    def Edit_VideoSpeedDesigner_EntireClip_SpeedMultiplier_DragSlider(self, percentage):
        elem = self.find(L.video_speed.multiplier.slider)
        elem.AXValue = float(percentage)
        return True

    @step('[Action][Video Speed] Set [Speed Multiplier] for [Entire Clip] by clicking the arrow button')
    def Edit_VideoSpeedDesigner_EntireClip_SpeedMultiplier_ArrowButton(self, direction):
        return self.Edit_VideoSpeedDesigner_EntireClip_NewVideoDuration_ArrowButton(
            direction,
            [
                L.video_speed.multiplier.up,
                L.video_speed.multiplier.down
            ])

    def Edit_VideoSpeedDesigner_SelectRange_Click_i_Button(self):
        self.exist(L.video_speed.i_button).press()
        time.sleep(DELAY_TIME)
        return self.is_exist(L.video_speed.i_dialog)

    @step('[Action][Video Speed] Click [Create Time Shift] button to upper')
    def VideoSpeedDesigner_SelectRange_Click_Upper_CreateTimeShift_btn(self):
        self.exist(L.video_speed.time_shift_1).press()
        return True
    @step('[Action][Video Speed] Click [Create Time Shift] button to lower')
    def VideoSpeedDesigner_SelectRange_Click_lower_CreateTimeShift_btn(self):
        self.exist(L.video_speed.time_shift_2).press()
        return True

    def Edit_VideoSpeedDesigner_SelectRange_Duration_SetValue(self, timecode):
        return self.Edit_VideoSpeedDesigner_EntireClip_NewVideoDuration_SetValue(
            timecode,
            L.video_speed.duration.time_code
        )

    def Edit_VideoSpeedDesigner_SelectRange_Duration_ArrowButton(self, direction):
        return self.Edit_VideoSpeedDesigner_EntireClip_NewVideoDuration_ArrowButton(
            direction,
            [L.video_speed.duration.up,
             L.video_speed.duration.down]
        )

    @step('[Action][Video Speed] Set [Speed Multiplier] value for [Selected Range]')
    def Edit_VideoSpeedDesigner_SelectRange_SpeedMultiplier_SetValue(self, multiplier):
        return self.Edit_VideoSpeedDesigner_EntireClip_NewVideoDuration_SetValue(
            str(multiplier),
            L.video_speed.multiplier_partial.value,
            True
        )

    def Edit_VideoSpeedDesigner_SelectRange_SpeedMultiplier_DragSlider(self, percentage):
        elem = self.find(L.video_speed.multiplier_partial.slider)
        elem.AXValue = float(percentage)
        return True

    def Edit_VideoSpeedDesigner_SelectRange_SpeedMultiplier_ArrowButton(self, direction):
        return self.Edit_VideoSpeedDesigner_EntireClip_NewVideoDuration_ArrowButton(
            direction,
            [L.video_speed.multiplier_partial.up,
             L.video_speed.multiplier_partial.down]
        )

    def Edit_VideoSpeedDesigner_SelectRange_EaseIn_SetCheck(self, bCheck=1, _locator=None):
        _locator = _locator or L.video_speed.multiplier_partial.ease_in
        elem = self.find(_locator)
        if elem.AXValue != [0,1][bool(bCheck)]:
            if not elem.AXEnabled: raise Exception("check box is not enabled")
            elem.press()
        return True

    def Edit_VideoSpeedDesigner_SelectRange_EaseOut_SetCheck(self, bCheck=1):
        return self.Edit_VideoSpeedDesigner_SelectRange_EaseIn_SetCheck(
            bCheck,
            L.video_speed.multiplier_partial.ease_out,
        )

    def Edit_VideoSpeedDesigner_SelectRange_EaseIn_IsEnabled(self,_locator=None):
        _locator = _locator or L.video_speed.multiplier_partial.ease_in
        elem = self.find(_locator)
        return elem.AXEnabled

    def Edit_VideoSpeedDesigner_SelectRange_EaseOut_IsEnabled(self,_locator=None):
        return self.Edit_VideoSpeedDesigner_SelectRange_EaseIn_IsEnabled(L.video_speed.multiplier_partial.ease_out)

    def VideoSpeedDesigner_PreviewOperation(self, operation):
        self.find(getattr(L.video_speed.preview, operation.lower())).press()
        return True

    def Edit_VideoSpeedDesigner_Click_Remove_btn(self):
        self.find(L.video_speed.remove).press()
        return True

    def Edit_VideoSpeedDesigner_Click_ViewEntireMovie(self):
        self.find(L.video_speed.view_entir_movie).press()
        return True

    @step('[Action][Video Speed] Click [Reset] button in [Video Speed Designer]')
    def Edit_VideoSpeedDesigner_ClickReset(self):
        self.find(L.video_speed.reset).press()
        time.sleep(DELAY_TIME*2)
        return True

    def Edit_VideoSpeedDesigner_ClickCancel(self):
        self.find(L.video_speed.cancel).press()
        return True

    @step('[Action][Video Speed] Click [OK] button')
    def Edit_VideoSpeedDesigner_ClickOK(self):
        self.find(L.video_speed.ok).press()
        return True

    def Edit_VideoSpeedDesigner_Click_ZoomOut_btn(self):
        self.find(L.video_speed.zoom_out).press()
        return True

    def Edit_VideoSpeedDesigner_Click_ZoomIn_btn(self):
        self.find(L.video_speed.zoom_in).press()
        return True

    # video speed
    @step('[Action][Video Speed] Set [New Video Duration] value for [Entire Clip]')
    def Edit_VideoSpeed_EntireClip_NewVideoDuration_SetValue(self, timecode):
        return self.Edit_VideoSpeedDesigner_EntireClip_NewVideoDuration_SetValue(
            timecode,
            L.video_speed.video_speed.time_code
        )

    def Edit_VideoSpeed_EntireClip_NewVideoDuration_ArrowButton(self, direction):
        return self.Edit_VideoSpeedDesigner_EntireClip_NewVideoDuration_ArrowButton(
            direction,
            [L.video_speed.video_speed.up,
             L.video_speed.video_speed.down]
        )

    def Edit_VideoSpeed_EntireClip_SpeedMultiplier_SetValue(self, multiplier):
        return self.Edit_VideoSpeedDesigner_EntireClip_NewVideoDuration_SetValue(
            str(multiplier),
            L.video_speed.video_speed.multiplier.value,
            True
        )

    def Edit_VideoSpeed_EntireClip_SpeedMultiplier_DragSlider(self, percentage):
        elem = self.find(L.video_speed.video_speed.multiplier.slider)
        elem.AXValue = float(percentage)
        return True

    def Edit_VideoSpeed_ClickReset(self):
        self.find(L.video_speed.video_speed.reset).press()
        return True

    def Edit_VideoSpeed_ClickCancel(self):
        self.find(L.video_speed.video_speed.cancel).press()
        return True

    def Edit_VideoSpeed_ClickOK(self):
        self.find(L.video_speed.video_speed.ok).press()
        return True

    def Edit_VideoSpeedDesigner_Click_Maximize_btn(self):
        self.find(L.video_speed.max_and_restore).press()
        return True

    def Edit_VideoSpeedDesigner_Click_Restore_btn(self):
        self.find(L.video_speed.max_and_restore).press()
        return True

    def Edit_VideoSpeedDesigner_Click_Close_btn(self):
        self.find(L.video_speed.close).press()
        return True

    def Edit_VideoSpeedDesigner_EntireClip_OriginalVideoLength(self):
        return self.find(L.video_speed.original_video.timecode).AXValue

    @step('[Action][Video Speed] Get [Speed Multiplier] value for [Entire Clip]')
    def Edit_VideoSpeedDesigner_EntireClip_SpeedMultiplier_GetValue(self):
        return self.find(L.video_speed.multiplier.value).AXValue
    
    @step('[Action][Video Speed] Get [Speed Multiplier] value for [Selected Range]')
    def Edit_VideoSpeedDesigner_SelectRange_SpeedMultiplier_GetValue(self):
        return self.find(L.video_speed.multiplier_partial.value).AXValue

    def Edit_VideoSpeed_EntireClip_SpeedMultiplier_GetValue(self):
        return self.find(L.video_speed.video_speed.multiplier.value).AXValue
    
    @step('[Action][Video Speed] Get [New Video Duration] value for [Entire Clip]')
    def Edit_VideoSpeed_EntireClip_NewVideoDuration_GetValue(self):
        return self.find(L.video_speed.video_speed.time_code).AXValue

    def Edit_VideoSpeed_Reset_GetStatus(self):
        return self.find(L.video_speed.video_speed.reset).AXEnabled

    def Edit_VideoSpeedDesigner_SelectRange_i_Click_Close_btn(self):
        self.find(L.video_speed.i_close).press()
        return True

    @step('[Action][Video Speed] Get [New Video Length] value')
    def Edit_VideoSpeedDesigner_EntireClip_NewVideoLength_GetValue(self):
        return self.find(L.video_speed.new_video.time_code).AXValue

    @step('[Action][Video Speed] Get [Video Length] value for [Select Range]')
    def Edit_VideoSpeedDesigner_SelectRange_VideoLength_GetValue(self):
        return self.find(L.video_speed.duration.time_code).AXValue


