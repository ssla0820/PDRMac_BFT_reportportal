import time, datetime, os, copy

from .base_page import BasePage
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
from AppKit import NSScreen
from .locator import locator as L
from reportportal_client import step


def arrow(obj, button="up", times=1, locator=None):
    locator = locator[button.lower() == "up"]
    elem = obj.exist(locator)
    for _ in range(times):
        obj.mouse.click(*elem.center)
    return True


class AdjustSet:
    def __init__(self, driver, locators):
        self.driver = driver
        self.locators = locators

    def adjust_slider(self, value):
        self.driver.exist(self.locators[0]).AXValue = value
        return True

    def set_value(self, value):
        target = self.driver.exist(self.locators[1])
        self.driver.mouse.click(*target.center)
        target.AXValue = str(value)
        self.driver.keyboard.enter()
        return True

    def get_value(self):
        return self.driver.exist(self.locators[1]).AXValue

    def click_up(self, times=1):
        return arrow(self.driver, button="up", times=times, locator=self.locators[3:1:-1])

    def click_down(self, times=1):
        return arrow(self.driver, button="down", times=times, locator=self.locators[3:1:-1])

    def click_arrow(self, opt="up", times=1):
        index = opt if isinstance(opt, int) else opt.lower() == "down"
        option = ["up", "down"][index]
        return self.__getattribute__(f"click_{option}")(times)

    def click_plus(self, times=1, _btn=True, _get_status=False):
        try:
            locator = self.locators[5:3:-1][bool(_btn)]
        except:
            logger("[Error] locator was not defined")
            return False
        target = self.driver.exist(locator)
        if _get_status:
            return target.AXEnabled
        else:
            self.driver.mouse.click(*target.center, times=times)
            return True

    def click_minus(self, times=1):
        return self.click_plus(times, False)

    def is_plus_enabled(self, btn=True):
        return self.click_plus(_get_status=True)

    def is_minus_enabled(self):
        return self.click_plus(_btn=False, _get_status=True)


def get_checkbox_status(self, _locator):
    check_status = self.exist(_locator).AXValue
    return check_status

def only_set_checkbox(self, _locator, value=True):
    try:
        current_value = self.exist(_locator)
        if current_value != value:
            self.click(_locator)
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        raise Exception
    return True

def _set_checkbox(self, _locator, value=True, _get_status_only=False):
    target = self.exist(_locator)
    timer = time.time()
    while time.time() - timer < 5:
        try:
            current_value = bool(int(target.AXValue))
            if _get_status_only: return current_value
            if current_value == value:
                break
            else:
                target.press()
                time.sleep(1)
                break
        except:
            logger("First round, force click it")
            if _get_status_only: target.press()
            target.press()
            time.sleep(1)
    else:
        return False
    return True


class FixEnhance(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fix = self.Fix(*args, **kwargs)
        self.enhance = self.Enhance(*args, **kwargs)

    def is_in_fix_enhance(self):
        return self.is_exist(L.fix_enhance.btn_close)

    def click_close(self):
        return bool(self.exist_press(L.fix_enhance.btn_close))

    def click_reset(self):
        return bool(self.exist_press(L.fix_enhance.btn_reset))

    def click_keyframe(self):
        return bool(self.exist_press(L.fix_enhance.btn_keyframe))

    def click_apply_to_all(self):
        return bool(self.exist_press(L.fix_enhance.btn_apply_to_all))

    def set_check_compare_in_split_preview(self, value):
        target = self.exist(L.fix_enhance.checkbox_compare_in_split_preview)
        if bool(target.AXValue) != value: target.press()
        return True

    class Fix(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.lighting_adjustment = LightingAdjusement(*args, **kwargs)
            self.white_balance = WhiteBalance(*args, **kwargs)
            self.video_stabilizer = VideoStabilizer(*args, **kwargs)
            self.lens_correction = LensCorrection(*args, **kwargs)
            self.video_denoise = VideoDenoise(*args, **kwargs)
            self.audio_denoise = AudioDenoise(*args, **kwargs)

        def switch_to_white_balance(self):
            return bool(self.exist_press(L.fix_enhance.fix.tab_white_balance))

        def switch_to_video_stabilizer(self):
            return bool(self.exist_press(L.fix_enhance.fix.tab_video_stabilizer))

        def switch_to_lens_correction(self):
            return bool(self.exist_press(L.fix_enhance.fix.tab_lens_correction))

        def switch_to_audio_denoise(self):
            return bool(self.exist_press(L.fix_enhance.fix.tab_audio_denoise))

        def switch_to_lighting_adjustment(self):
            self.exist_press(L.fix_enhance.fix.tab_lighting_adjustment)
            return self.is_exist(L.fix_enhance.fix.lighting_adjustment.btn_extreme_backlight)

        def switch_to_video_denoise(self):
            self.exist_press(L.fix_enhance.fix.tab_video_denoise)
            return self.is_exist(L.fix_enhance.fix.video_denoise.degree.slider)

        def switch_to_wind_removal(self):
            self.exist_press(L.fix_enhance.fix.tab_wind_removal)
            return self.is_exist(L.fix_enhance.fix.wind_removal.btn_wind_removal)

        def enable_white_balance(self, value=True):
            return _set_checkbox(self, L.fix_enhance.fix.checkbox_white_balance, value)

        def enable_video_stabilizer(self, value=True):
            return _set_checkbox(self, L.fix_enhance.fix.checkbox_video_stabilizer, value)

        def enable_lens_correction(self, value=True):
            return _set_checkbox(self, L.fix_enhance.fix.checkbox_lens_correction, value)

        def enable_audio_denoise(self, value=True):
            return _set_checkbox(self, L.fix_enhance.fix.checkbox_audio_denoise, value)

        def enable_lighting_adjustment(self, value=True):
            return _set_checkbox(self, L.fix_enhance.fix.checkbox_lighting_adjustment, value)

        def enable_video_denoise(self, value=True):
            return _set_checkbox(self, L.fix_enhance.fix.checkbox_video_denoise, value)

        def get_white_balance(self):
            return _set_checkbox(self, L.fix_enhance.fix.checkbox_white_balance, _get_status_only=True)

        def get_video_stabilizer(self):
            return _set_checkbox(self, L.fix_enhance.fix.checkbox_video_stabilizer, _get_status_only=True)

        def get_lens_correction(self):
            return _set_checkbox(self, L.fix_enhance.fix.checkbox_lens_correction, _get_status_only=True)

        def get_audio_denoise(self):
            return _set_checkbox(self, L.fix_enhance.fix.checkbox_audio_denoise, _get_status_only=True)

        def get_lighting_adjustment(self):
            return _set_checkbox(self, L.fix_enhance.fix.checkbox_lighting_adjustment, _get_status_only=True)

        def get_video_denoise(self):
            return _set_checkbox(self, L.fix_enhance.fix.checkbox_video_denoise, _get_status_only=True)

        def click_wind_removal(self):
            self.click(L.fix_enhance.fix.wind_removal.btn_wind_removal)

        @step('[Action][Fix Enhance][Fix] Click [Apply] Button in [Wind Removal] Window')
        def click_wind_removal_apply(self, delay_time=10):
            if not self.exist(L.fix_enhance.fix.wind_removal.main_window):
                logger('Not enter Wind Removal window, return False')
                return False

            self.click(L.fix_enhance.fix.wind_removal.btn_apply)
            processing_render_audio = False
            for x in range(delay_time):
                if self.is_not_exist(L.fix_enhance.enhance.tab_color_adjustment, timeout=0.5):
                    processing_render_audio = True
                    break
                else:
                    time.sleep(1)
            return processing_render_audio

    class Enhance(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.color_adjustment = ColorAdjustment(*args, **kwargs)
            self.split_toning = SplitToning(*args, **kwargs)
            self.hdr_effect = HDREffect(*args, **kwargs)
            self.color_match = ColorMatch(*args, **kwargs)
            self.color_enhancement = ColorEnhancement(*args, **kwargs)
            self.speech_enhancement = SpeechEnhancement(*args, **kwargs)

        def switch_to_color_adjustment(self):
            return bool(self.exist_press(L.fix_enhance.enhance.tab_color_adjustment))

        def switch_to_split_toning(self):
            return bool(self.exist_press(L.fix_enhance.enhance.tab_split_toning))

        def switch_to_hdr_effect(self):
            return bool(self.exist_press(L.fix_enhance.enhance.tab_hdr_effect))

        def switch_to_color_match(self):
            return bool(self.exist_press(L.fix_enhance.enhance.tab_color_match))

        def switch_to_color_enhancement(self):
            return bool(self.exist_press(L.fix_enhance.enhance.tab_color_enhancement))

        def switch_to_speech_enhancement(self):
            self.exist_press(L.fix_enhance.enhance.tab_speech_enhancement)
            return self.is_exist(L.fix_enhance.enhance.speech_enhancement.btn_speech_enhancement)

        def enable_color_adjustment(self, value=True):
            return only_set_checkbox(self, L.fix_enhance.enhance.checkbox_color_adjustment, value)

        def enable_split_toning(self, value=True):
            return _set_checkbox(self, L.fix_enhance.enhance.checkbox_split_toning, value)

        def enable_hdr_effect(self, value=True):
            return _set_checkbox(self, L.fix_enhance.enhance.checkbox_hdr_effect, value)

        def enable_color_match(self, value=True):
            return _set_checkbox(self, L.fix_enhance.enhance.checkbox_color_match, value)

        def enable_color_enhancement(self, value=True):
            return _set_checkbox(self, L.fix_enhance.enhance.checkbox_color_enhancement, value)

        @step('[Action][Fix Enhance][Enhance] Get [Color Adjustment] Checkbox Status')
        def get_color_adjustment(self):
            return _set_checkbox(self, L.fix_enhance.enhance.checkbox_color_adjustment, _get_status_only=True)

        @step('[Action][Fix Enhance][Enhance] Get [Color Enhancement] Checkbox Status')
        def get_color_enhancement(self):
            return _set_checkbox(self, L.fix_enhance.enhance.checkbox_color_enhancement, _get_status_only=True)

        def get_split_toning(self):
            return _set_checkbox(self, L.fix_enhance.enhance.checkbox_split_toning, _get_status_only=True)

        def get_hdr_effect(self):
            return _set_checkbox(self, L.fix_enhance.enhance.checkbox_hdr_effect, _get_status_only=True)

        def get_color_match(self):
            return _set_checkbox(self, L.fix_enhance.enhance.checkbox_color_match, _get_status_only=True)

        def click_speech_enhancement(self):
            self.click(L.fix_enhance.enhance.speech_enhancement.btn_speech_enhancement)

class LightingAdjusement(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extreme_backlight = AdjustSet(self, L.fix_enhance.fix.lighting_adjustment.extreme_backlight.group)

    def enable_extreme_backlight(self, value):
        return _set_checkbox(self, L.fix_enhance.fix.lighting_adjustment.btn_extreme_backlight, value)

    def get_extreme_backlight(self):
        return _set_checkbox(self, L.fix_enhance.fix.lighting_adjustment.btn_extreme_backlight, _get_status_only=True)


class WhiteBalance(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color_temperature = AdjustSet(self, L.fix_enhance.fix.white_balance.group_color_temperature)
        self.tint = AdjustSet(self, L.fix_enhance.fix.white_balance.group_tint)
        self.white_calibration = self.WhiteCalibration(*args, **kwargs)

    def set_radio_button(self, option=0, _get_status=False):
        locator = [L.fix_enhance.fix.white_balance.radio_color_temperature,
                   L.fix_enhance.fix.white_balance.radio_white_calibration][option]
        target = self.exist(locator)
        result = bool(int(target.AXValue))
        logger(f"{result=}")
        if _get_status: return int(result)
        if not result:
            target.press()
        return True

    def get_radio_button(self):
        return self.set_radio_button(option=1, _get_status=True)

    def set_color_temperature_value(self, value):
        return self.color_temperature.set_value(value)

    def get_color_temperature_value(self):
        return self.color_temperature.get_value()

    def set_color_temperature_slider(self, value):
        return self.color_temperature.adjust_slider(value)

    def click_color_temperature_arrow(self, option="up"):
        return self.color_temperature.click_arrow(option)

    def set_tint_value(self, value):
        return self.tint.set_value(value)

    def get_tint_value(self):
        return self.tint.get_value()

    def set_tint_slider(self, value):
        return self.tint.adjust_slider(value)

    def click_tint_arrow(self, option="up"):
        return self.tint.click_arrow(option)

    def click_white_calibrate_button(self):
        return bool(self.exist_press(L.fix_enhance.fix.white_balance.btn_white_calibrate))

    class WhiteCalibration(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def click_i_button(self):
            return bool(self.exist_press(L.fix_enhance.fix.white_balance.white_calibration.btn_i))

        def click_close(self):
            return bool(self.exist_press(L.fix_enhance.fix.white_balance.white_calibration.btn_close))

        def click_cancel(self):
            return bool(self.exist_press(L.fix_enhance.fix.white_balance.white_calibration.btn_cancel))

        def click_ok(self):
            return bool(self.exist_press(L.fix_enhance.fix.white_balance.white_calibration.btn_ok))

        def adjust_slider(self, percent):
            if not 0.0 < percent <= 1.0: raise Exception("Value({percent}) is incorrect")
            target = self.exist(L.fix_enhance.fix.white_balance.white_calibration.slider)
            max, min = target.AXMaxValue, target.AXMinValue
            value = int((max - min) * percent + min)
            logger(f"{min=} / {max=}/ {value=}")
            self.exist(L.fix_enhance.fix.white_balance.white_calibration.slider).AXValue = value
            return True


class VideoStabilizer(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.correction_level = AdjustSet(self, L.fix_enhance.fix.video_stabilizer.correction_level.group)


class LensCorrection(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fisheye_distortion = AdjustSet(self, L.fix_enhance.fix.lens_correction.group_fisheye)
        self.vignette_amount = AdjustSet(self, L.fix_enhance.fix.lens_correction.group_vignette_amount)
        self.vignette_midpoint = AdjustSet(self, L.fix_enhance.fix.lens_correction.group_vignette_midpoint)

    def select_marker_type(self, type):
        target = copy.deepcopy(L.fix_enhance.fix.lens_correction.menu_item_maker)
        target[-1]["AXValue"] = type
        self.exist_click(L.fix_enhance.fix.lens_correction.menu_maker)
        self.exist_click(target)
        time.sleep(1)
        return True

    def get_marker_type(self):
        return self.exist(L.fix_enhance.fix.lens_correction.menu_maker).AXTitle

    def import_lens_profile(self, full_path):
        self.exist_press(L.fix_enhance.fix.lens_correction.btn_import_marker)
        self.select_file(full_path)
        self.click_OK_onEffectExtractor()
        return True

    def download_lens_profile(self):
        bid = "com.google.Chrome"
        app = self.driver.getRunningAppRefsByBundleId(bid)
        if app: self.get_top().terminateAppByBundleId("com.google.Chrome")
        self.exist_click(L.fix_enhance.fix.lens_correction.btn_download)
        timer = time.time()
        while time.time() - timer < 5:
            try:
                app = self.driver.getRunningAppRefsByBundleId(bid)[0]
                if "cyberlink.com/pdr" in app.findAllR(AXHelp="⌘L")[0].AXValue:
                    app.terminateAppByBundleId("com.google.Chrome")
                    break
            except:
                pass
        else:
            self.activate()
            return False
        self.activate()
        return True

    def select_model_type(self, index):
        target = copy.deepcopy(L.fix_enhance.fix.lens_correction.menu_item_model)
        target[-1]["index"] = index
        self.exist_click(L.fix_enhance.fix.lens_correction.menu_model)
        self.exist_click(target)
        return True

    def get_model_type(self):
        return self.exist(L.fix_enhance.fix.lens_correction.menu_model).AXTitle


class VideoDenoise(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.degree = AdjustSet(self, L.fix_enhance.fix.video_denoise.degree.group)


class AudioDenoise(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.degree = AdjustSet(self, L.fix_enhance.fix.audio_denoise.degree.group)

    def set_noise_type(self, index):
        target = copy.deepcopy(L.fix_enhance.fix.audio_denoise.menu_item_noise_type)
        target[-1]["AXValue"] = ["Stationary noise", "Wind noise"][index]
        self.exist_click(L.fix_enhance.fix.audio_denoise.menu_noise_type)
        self.exist_click(target)
        return True

    def get_noise_type(self):
        return self.exist(L.fix_enhance.fix.audio_denoise.menu_noise_type).AXTitle


class ColorAdjustment(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exposure = AdjustSet(self, L.fix_enhance.enhance.color_adjustment.exposure.group)
        self.brightness = AdjustSet(self, L.fix_enhance.enhance.color_adjustment.brightness.group)
        self.contrast = AdjustSet(self, L.fix_enhance.enhance.color_adjustment.contrast.group)
        self.hue = AdjustSet(self, L.fix_enhance.enhance.color_adjustment.hue.group)
        self.saturation = AdjustSet(self, L.fix_enhance.enhance.color_adjustment.saturation.group)
        self.vibrancy = AdjustSet(self, L.fix_enhance.enhance.color_adjustment.vibrancy.group)
        self.highlight_healing = AdjustSet(self, L.fix_enhance.enhance.color_adjustment.highlight_healing.group)
        self.shadow = AdjustSet(self, L.fix_enhance.enhance.color_adjustment.shadow.group)
        self.sharpness = AdjustSet(self, L.fix_enhance.enhance.color_adjustment.sharpness.group)

class ColorEnhancement(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.degree = AdjustSet(self, L.fix_enhance.enhance.color_enhancement.degree.group)

class SpeechEnhancement(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.compensation = AdjustSet(self, L.fix_enhance.enhance.speech_enhancement.compensation.group)

    def click_apply(self, delay_time=10):
        if not self.exist(L.fix_enhance.enhance.speech_enhancement.main_window):
            logger('Not enter Speech Enhancement window, return False')
            return False

        self.click(L.fix_enhance.enhance.speech_enhancement.btn_apply)
        time.sleep(delay_time)
        return True

class ModuleSet:
    def __init__(self, *args, **kwargs):
        self.args = []
        self.args.append(args[0])
        for arg in args[1]:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self.__setattr__(k, AdjustSet(self.args[0], v.group))
            else:
                self.args.append(arg)

    def set_color(self, hue, saturation):
        logger(f"{self.args[1]=}")
        self.args[0].click(self.args[1])
        self.args[0].find(L.fix_enhance.enhance.split_toning.highlights.pick_color.hue.value).AXValue = str(hue)
        self.args[0].find(L.fix_enhance.enhance.split_toning.highlights.pick_color.saturation.value).AXValue = str(
            saturation)
        self.args[0].click(L.fix_enhance.enhance.split_toning.highlights.pick_color.btn_ok)
        return True


class SplitToning(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.highlights = ModuleSet(self, L.fix_enhance.enhance.split_toning.highlights.groups)
        self.balance = AdjustSet(self, L.fix_enhance.enhance.split_toning.balance.group)
        self.shadow = ModuleSet(self, L.fix_enhance.enhance.split_toning.shadow.groups)


class HDREffect(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.glow = ModuleSet(self, L.fix_enhance.enhance.hdr_effect.grow.groups)
        self.edge = ModuleSet(self, L.fix_enhance.enhance.hdr_effect.edge.groups)

    def drag_scroll_bar(self, value):
        el = self.find(L.fix_enhance.enhance.hdr_effect.scroll_bar)
        el.AXValue = value
        timer = time.time()
        while time.time() - timer < 3:
            if el.AXValue == value: return True
        else:
            return False

class ColorMatch(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def exist_color_match_button(self):
        return bool(self.exist(L.fix_enhance.enhance.color_match.btn_color_match))

    def click_color_match_button(self):
        if not self.exist_color_match_button():
            logger('Cannot find  Color Match button')
            raise Exception
        self.click(L.fix_enhance.enhance.color_match.btn_color_match)

        # Verify Step:
        # Can find the parameter setting of (Color match)
        if self.exist(L.fix_enhance.enhance.color_match.setting_scroll_view):
            return True
        else:
            logger('Does NOT enter Color match setting, raise Exception')
            raise Exception

    def get_match_color_status(self):
        btn_elem = self.exist(L.fix_enhance.enhance.color_match.btn_match_color)
        if not btn_elem:
            return None
        else:
            return btn_elem.AXEnabled

    def click_match_color(self):
        if self.get_match_color_status():
            self.click(L.fix_enhance.enhance.color_match.btn_match_color)
            time.sleep(3)
            return True
        else:
            logger('Button is disabled or not found now.')
            raise Exception

    def click_close(self, option=None):
        btn_elem = self.exist(L.fix_enhance.enhance.color_match.btn_close)
        if not btn_elem:
            logger('Cannot find the close button')
            raise Exception
        self.click(L.fix_enhance.enhance.color_match.btn_close)

        # not set aug1 (option = None)
        if not option:
            return True

        # Handle question dialog to click certain button with aug1
        if option == 'Yes':
            option_btn = L.base.quit_dialog.yes
        elif option == 'No':
            option_btn = L.base.quit_dialog.no
        elif option == 'Cancel':
            option_btn = L.base.quit_dialog.cancel
        else:
            logger(f'Invalid parameter - {option}')
            return False

        self.click(option_btn)
        return True

