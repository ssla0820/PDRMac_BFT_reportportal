import time, datetime, os, copy

from .base_page import BasePage
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
# from AppKit import NSScreen
from .locator import locator as L
from reportportal_client import step

DELAY_TIME = 1 # sec
build_in_loop_time = 5

def _adjust_slider_to_handle_continue_dialog(self, _locator):
    self.click(_locator)
    self.exist_click(locator=L.base.confirm_dialog.btn_ok, timeout=3)
    return True

def _adjust_slider(self, _locator, value):
    self.exist(_locator).AXValue = value
    return True

def _adjust_slider_in_loop(self, _locator, min_value, max_value, loop_times):
    for x in range(loop_times):
        _adjust_slider(self, _locator, min_value)
        time.sleep(0.5)
        _adjust_slider(self, _locator, max_value)
        time.sleep(0.5)

    if self.exist(_locator).AXValue == max_value:
        return True
    else:
        return False

def _set_color(self, _locator, HexColor):
    try:
        if not self.exist(_locator):
            logger('Cannot find Color button now')
            return False
        else:
            self.click(_locator)

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
        except:
            logger("First round, force click it")
            if _get_status_only: target.press()
            target.press()
            time.sleep(1)
    else:
        return False
    return True

# Handle dropdown menu
def _set_option(self, _locator_cbx, target_menu, get_status=False):
    try:
        option_custom = {'AXRole': 'AXStaticText', 'AXValue': f'{target_menu}'}
        target = self.exist(_locator_cbx)
        current_title = str(target.AXTitle)
        if get_status:
            return current_title
        else:
            self.click(_locator_cbx)
            time.sleep(DELAY_TIME*1)
            self.click(option_custom)
            time.sleep(DELAY_TIME*1)

    except Exception as e:
        logger(f'Exception occurs. log={e}')
        raise Exception
    return True

class Effect_Settings(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Support Effect Room > Style Effect(75) --->>
        self.aberration = self.Aberration(*args, **kwargs)
        self.back_light = self.Back_Light(*args, **kwargs)
        self.band_noise = self.Band_Noise(*args, **kwargs)
        self.beating = self.Beating(*args, **kwargs)
        self.black_white = self.Black_White(*args, **kwargs)
        self.blackout = self.Blackout(*args, **kwargs)
        self.bloom = self.Bloom(*args, **kwargs)
        self.blur_bar = self.Blur_Bar(*args, **kwargs)
        self.broken_glass = self.Broken_Glass(*args, **kwargs)
        self.bump_map = self.Bump_Map(*args, **kwargs)

        self.chinese_paint = self.Chinese_Paint(*args, **kwargs)
        self.chinese_paint_2 = self.Chinese_Paint_2(*args, **kwargs)
        self.color_balance = self.Color_Balance(*args, **kwargs)
        self.color_crayon = self.Color_Crayon(*args, **kwargs)
        self.color_painting = self.Color_Painting(*args, **kwargs)
        self.continuous_shooting = self.Continuous_Shooting(*args, **kwargs)
        self.delay = self.Delay(*args, **kwargs)
        self.disturbance = self.Disturbance(*args, **kwargs)
        self.disturbance_2 = self.Disturbance_2(*args, **kwargs)
        self.double_fisheye = self.Double_FishEye(*args, **kwargs)

        self.drain = self.Drain(*args, **kwargs)
        self.dreamy = self.Dreamy(*args, **kwargs)
        self.emboss = self.Emboss(*args, **kwargs)
        self.filter_color = self.Filter_Color(*args, **kwargs)
        self.fine_noise = self.Fine_Noise(*args, **kwargs)
        self.fish_eye = self.Fish_Eye(*args, **kwargs)
        self.gamma_correction = self.Gamma_Correction(*args, **kwargs)
        self.gaussian_blur = self.Gaussian_Blur(*args, **kwargs)
        self.glass = self.Glass(*args, **kwargs)
        self.glass_tile = self.Glass_Tile(*args, **kwargs)

        self.glow = self.Glow(*args, **kwargs)
        self.grid = self.Grid(*args, **kwargs)
        self.halftone = self.Halftone(*args, **kwargs)
        self.halftone_color = self.Halftone_Color(*args, **kwargs)
        self.horizontal_stretch = self.Horizontal_Stretch(*args, **kwargs)
        self.jitter = self.Jitter(*args, **kwargs)
        self.kaleidoscope = self.Kaleidoscope(*args, **kwargs)
        self.laser = self.Laser(*args, **kwargs)
        self.light_ray = self.Light_Ray(*args, **kwargs)
        self.line_noise = self.Line_Noise(*args, **kwargs)

        self.mirror = self.Mirror(*args, **kwargs)
        self.moon_light = self.Moon_Light(*args, **kwargs)
        self.mosaic = self.Mosaic(*args, **kwargs)
        self.neutral_filter = self.Neutral_Filter(*args, **kwargs)
        self.noise_2 = self.Noise_2(*args, **kwargs)
        self.old_movie = self.Old_Movie(*args, **kwargs)
        self.pen_ink = self.Pen_Ink(*args, **kwargs)
        self.pop_art = self.Pop_Art(*args, **kwargs)
        self.pop_art_wall = self.Pop_Art_Wall(*args, **kwargs)
        self.posterize = self.Posterize(*args, **kwargs)

        self.quake = self.Quake(*args, **kwargs)
        self.radial_blur = self.Radial_Blur(*args, **kwargs)
        self.ripple = self.Ripple(*args, **kwargs)
        self.rocking = self.Rocking(*args, **kwargs)
        self.scratch_noise = self.Scratch_Noise(*args, **kwargs)
        self.sepia = self.Sepia(*args, **kwargs)
        self.skip = self.Skip(*args, **kwargs)
        self.solarize = self.Solarize(*args, **kwargs)
        self.spotlight = self.Spotlight(*args, **kwargs)
        self.square = self.Square(*args, **kwargs)

        self.squeeze = self.Squeeze(*args, **kwargs)
        self.swing = self.Swing(*args, **kwargs)
        self.threshold = self.Threshold(*args, **kwargs)
        self.tiles = self.Tiles(*args, **kwargs)
        self.triangle_stretch = self.Triangle_Stretch(*args, **kwargs)
        self.tv_wall = self.TV_Wall(*args, **kwargs)
        self.vertical_stretch = self.Vertical_Stretch(*args, **kwargs)
        self.vignette = self.Vignette(*args, **kwargs)
        self.water_reflection = self.Water_Reflection(*args, **kwargs)
        self.wave = self.Wave(*args, **kwargs)
        self.wave_noise = self.Wave_Noise(*args, **kwargs)
        self.woodcut = self.Woodcut(*args, **kwargs)
        self.zoom_in = self.Zoom_In(*args, **kwargs)
        self.zoom_out = self.Zoom_Out(*args, **kwargs)
        # Support Effect Room > Style Effect(75) ---<<

        # Support Effect Room > Style Effect(78) --->>
        self.magnifier = self.Magnifier(*args, **kwargs)
        self.pencil_sketch = self.Pencil_Sketch(*args, **kwargs)
        self.edge = self.Edge(*args, **kwargs)
        # Support Effect Room > Style Effect(78) ---<<

        self.body_effect = self.Body_Effect(*args, **kwargs)

    def click_reset_btn(self):
        if not self.exist(L.effect_settings.btn_reset):
            logger('Can NOT find [Reset] button')
            raise Exception

        self.click(L.effect_settings.btn_reset)

    def click_remove_btn(self):
        if not self.exist(L.effect_settings.btn_remove_effect):
            logger('Can NOT find [Reset] button')
            raise Exception

        self.click(L.effect_settings.btn_remove_effect)
        time.sleep(DELAY_TIME*2)

    @step('[Action][Effect Settings] Click [Close] button to leave [Effect Settings]')
    def close_window(self):
        try:
            if not self.exist(L.tips_area.button.btn_effect_close):
                logger('Can NOT find [Close] button')
                raise Exception('Can NOT find [Close] button')
            self.click(L.tips_area.button.btn_effect_close)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')


    class Aberration(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_frequency_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 200, build_in_loop_time)

        def adjust_strength_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 170, build_in_loop_time)

    class Back_Light(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_strength_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 50, build_in_loop_time)

        def adjust_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 15, build_in_loop_time)

        def adjust_light_color(self, hexColor):
            return _set_color(self, L.effect_settings.btn_color_2, hexColor)

    class Band_Noise(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_frequency_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 200, build_in_loop_time)

        def adjust_strength_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 200, build_in_loop_time)

    class Beating(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_frequency_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 5, 40, build_in_loop_time)

        def adjust_strength_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 110, 150, build_in_loop_time)

    class Black_White(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 175, build_in_loop_time)

        def adjust_gradient_depth_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 200, build_in_loop_time)

        def enable_invert_masked_area(self, value=True):
            return only_set_checkbox(self, L.effect_settings.cbx_invert_masked_area, value)

        def set_mask_type(self, custom_type='Circle'):
            return _set_option(self, L.effect_settings.cbx_mask_type, custom_type)

    class Blackout(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_frequency_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 200, build_in_loop_time)

    class Bloom(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_sample_number_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 1, 20, build_in_loop_time)

        def adjust_light_number_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 1, 3, build_in_loop_time)

        def adjust_sample_weight_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_3, 0, 200, build_in_loop_time)

        def adjust_angle_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_4, 0, 200, build_in_loop_time)

        def adjust_sample_space_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_5, 0, 200, build_in_loop_time)

    class Blur_Bar(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_frequency_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 200, build_in_loop_time)

        def adjust_range_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 200, build_in_loop_time)

        def adjust_shift_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_3, 0, 200, build_in_loop_time)

    class Broken_Glass(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
        @step('[Action][Effect Settings][Broken Glass] Adjust Degree slider')
        def adjust_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 200, build_in_loop_time)

    class Bump_Map(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 200, build_in_loop_time)

    class Chinese_Paint(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_blur_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 1, 5, build_in_loop_time)

    class Chinese_Paint_2(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_brush_size_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 1, 10, build_in_loop_time)

        def adjust_gray_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 255, build_in_loop_time)

    class Color_Balance(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_red_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, -255, 255, build_in_loop_time)

        def adjust_blue_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, -255, 255, build_in_loop_time)

        def adjust_green_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_3, -255, 255, build_in_loop_time)

        def adjust_gradient_depth_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_4, 0, 200, build_in_loop_time)

        def set_mask_type(self, custom_type='Circle'):
            return _set_option(self, L.effect_settings.cbx_mask_type, custom_type)

        def enable_grayscale_area(self, value=True):
            return only_set_checkbox(self, L.effect_settings.cbx_grayscale, value)

        def enable_invert_masked_area(self, value=True):
            return only_set_checkbox(self, L.effect_settings.cbx_invert_masked_area, value)

    class Color_Crayon(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def set_BG_texture(self, custom_type='Texture 3'):
            return _set_option(self, L.effect_settings.cbx_bg_texture, custom_type)

    class Color_Painting(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_edge_thickness_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 200, build_in_loop_time)

        def adjust_color_lightness_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 200, build_in_loop_time)

    class Continuous_Shooting(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_segment_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 2, 5, build_in_loop_time)

    class Delay(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_regularity_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 16, build_in_loop_time)

    class Disturbance(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_frequency_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 109, build_in_loop_time)

        def adjust_strength_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 200, build_in_loop_time)

    class Disturbance_2(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_frequency_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 159, build_in_loop_time)

        def adjust_shift_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 56, build_in_loop_time)

        def adjust_strength_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_3, 0, 200, build_in_loop_time)

        def adjust_range_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_4, 0, 200, build_in_loop_time)

    class Double_FishEye(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 200, build_in_loop_time)

        def adjust_size_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 200, build_in_loop_time)

        def enable_inverse(self, value=True):
            return only_set_checkbox(self, L.effect_settings.cbx_inverse, value)

    class Drain(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 200, 0, build_in_loop_time)

        def adjust_size_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 200, build_in_loop_time)

        def enable_inverse(self, value=True):
            return only_set_checkbox(self, L.effect_settings.cbx_inverse, value)

    class Dreamy(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 40, build_in_loop_time)

        def set_mask_type(self, custom_type='Circle'):
            return _set_option(self, L.effect_settings.cbx_mask_type, custom_type)

        def adjust_gradient_depth_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 200, build_in_loop_time)

        def enable_invert_masked_area(self, value=True):
            return only_set_checkbox(self, L.effect_settings.cbx_invert_masked_area, value)

    class Emboss(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_gradient_depth_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 200, 66, build_in_loop_time)

        def set_mask_type(self, custom_type='Circle'):
            return _set_option(self, L.effect_settings.cbx_mask_type, custom_type)

        def set_direction(self, custom_type='Down'):
            return _set_option(self, L.effect_settings.cbx_direction, custom_type)

        def enable_invert_masked_area(self, value=True):
            return only_set_checkbox(self, L.effect_settings.cbx_invert_masked_area, value)

    class Filter_Color(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_color_range_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 180, build_in_loop_time)

        def adjust_focus_color(self, hexColor):
            return _set_color(self, L.effect_settings.btn_color_1, hexColor)

    class Fine_Noise(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_noise_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 255, build_in_loop_time)

    class Fish_Eye(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 200, build_in_loop_time)

        def adjust_size_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 200, build_in_loop_time)

        def enable_inverse(self, value=True):
            return only_set_checkbox(self, L.effect_settings.cbx_inverse, value)

    class Gamma_Correction(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_gamma_level_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 3, 30, build_in_loop_time)

    class Gaussian_Blur(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 40, build_in_loop_time)

        def set_mask_type(self, custom_type='Circle'):
            return _set_option(self, L.effect_settings.cbx_mask_type, custom_type)

        def adjust_gradient_depth_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 200, build_in_loop_time)

        def enable_invert_masked_area(self, value=True):
            return only_set_checkbox(self, L.effect_settings.cbx_invert_masked_area, value)

    class Glass(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 3, 20, build_in_loop_time)

    class Glass_Tile(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 200, build_in_loop_time)

    class Glow(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_blur_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 174, build_in_loop_time)

        def adjust_glow_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 200, 79, build_in_loop_time)

    class Grid(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_width_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 2, 320, build_in_loop_time)

        def adjust_line_width_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 1, 31, build_in_loop_time)

        def adjust_height_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_3, 2, 240, build_in_loop_time)

        def adjust_BG_color(self, hexColor):
            return _set_color(self, L.effect_settings.btn_color_1, hexColor)

    class Halftone(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_sport_size_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 200, build_in_loop_time)

        def adjust_intensity_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 200, build_in_loop_time)

        def adjust_FG_color(self, hexColor):
            return _set_color(self, L.effect_settings.btn_color_1, hexColor)

        def adjust_BG_color(self, hexColor):
            return _set_color(self, L.effect_settings.btn_color_2, hexColor)

    class Halftone_Color(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_sport_size_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 200, build_in_loop_time)

        def adjust_intensity_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 200, build_in_loop_time)

    class Horizontal_Stretch(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 200, build_in_loop_time)

        def adjust_x_offset_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 200, build_in_loop_time)

        def adjust_size_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_3, 200, 11, build_in_loop_time)

        def enable_inverse(self, value=True):
            return only_set_checkbox(self, L.effect_settings.cbx_inverse, value)

    class Jitter(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_frequency_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 145, build_in_loop_time)

    class Kaleidoscope(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_angle_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 22, 200, build_in_loop_time)

        def adjust_x_offset_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 200, 13, build_in_loop_time)

        def adjust_segment_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_3, 10, 3, build_in_loop_time)

        def adjust_y_offset_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_4, 31, 187, build_in_loop_time)

    class Laser(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_percentage_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 21, 131, build_in_loop_time)

    class Light_Ray(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 30, build_in_loop_time)

    class Line_Noise(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_frequency_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 200, 91, build_in_loop_time)

        def adjust_strength_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 200, build_in_loop_time)

    class Mirror(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_x_offset_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 156, 54, build_in_loop_time)

        def enable_inverse(self, value=True):
            return only_set_checkbox(self, L.effect_settings.cbx_inverse, value)

    class Moon_Light(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 1, 30, build_in_loop_time)

        def set_mask_type(self, custom_type='Circle'):
            return _set_option(self, L.effect_settings.cbx_mask_type, custom_type)

        def adjust_gradient_depth_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 200, build_in_loop_time)

        def enable_invert_masked_area(self, value=True):
            return only_set_checkbox(self, L.effect_settings.cbx_invert_masked_area, value)

    class Mosaic(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_width_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 32, build_in_loop_time)

        def adjust_height_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 24, 5, build_in_loop_time)

        def set_mask_type(self, custom_type='Circle'):
            return _set_option(self, L.effect_settings.cbx_mask_type, custom_type)

    class Neutral_Filter(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_start_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 200, build_in_loop_time)

        def adjust_alpha_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 210, build_in_loop_time)

        def adjust_end_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_3, 0, 200, build_in_loop_time)

        def adjust_replace_color(self, hexColor):
            return _set_color(self, L.effect_settings.btn_color_1, hexColor)

    class Noise_2(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_frequency_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 200, build_in_loop_time)

        def adjust_strength_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 200, build_in_loop_time)

    class Old_Movie(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_artifact_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 10, build_in_loop_time)

        def adjust_scratch_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 16, build_in_loop_time)

        def adjust_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_3, 0, 198, build_in_loop_time)

        def adjust_noise_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_4, 0, 255, build_in_loop_time)

        def adjust_jitter_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_5, 0, 16, build_in_loop_time)

        def adjust_flicker_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_6, 0, 32, build_in_loop_time)

        def adjust_front_color(self, hexColor):
            return _set_color(self, L.effect_settings.btn_color_1, hexColor)

        def adjust_BG_color(self, hexColor):
            return _set_color(self, L.effect_settings.btn_color_2, hexColor)

    class Pen_Ink(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_blackness_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 200, build_in_loop_time)

    class Pop_Art(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 255, build_in_loop_time)

    class Pop_Art_Wall(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_pattern_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 1, 16, build_in_loop_time)

        def adjust_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 255, build_in_loop_time)

    class Posterize(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_levels_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 63, build_in_loop_time)

    class Quake(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_quake_level_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 200, build_in_loop_time)

        def adjust_starting_angle_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 11, build_in_loop_time)

        def adjust_frequency_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_3, 5, 1, build_in_loop_time)

        def adjust_stepping_angle_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_4, 0, 200, build_in_loop_time)

        def adjust_BG_color(self, hexColor):
            return _set_color(self, L.effect_settings.btn_color_1, hexColor)

    class Radial_Blur(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 50, build_in_loop_time)

    class Ripple(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_wavelets_slider(self):
            # Handle warning message (This operation resets all the keyframe ...Do you want to continue?) Click [OK]
            _adjust_slider_to_handle_continue_dialog(self, L.effect_settings.slider_1)
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 1, 16, build_in_loop_time)

        def adjust_progress_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 200, build_in_loop_time)

        def adjust_speed_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_3, 1, 9, build_in_loop_time)

    class Rocking(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_frequency_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 5, 40, build_in_loop_time)

        def adjust_strength_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 110, 150, build_in_loop_time)

    class Scratch_Noise(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_frequency_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 200, build_in_loop_time)

        def adjust_strength_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 200, build_in_loop_time)

    class Sepia(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 255, build_in_loop_time)

        def adjust_front_color(self, hexColor):
            return _set_color(self, L.effect_settings.btn_color_1, hexColor)

    class Skip(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_frequency_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 50, build_in_loop_time)

    class Solarize(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_threshold_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 255, 0, build_in_loop_time)

    class Spotlight(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_width_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 320, build_in_loop_time)

        def adjust_gradient_depth_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 100, 4, build_in_loop_time)

        def adjust_height_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_3, 240, 53, build_in_loop_time)

        def adjust_brightness_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_4, 75, 220, build_in_loop_time)

        def adjust_mean_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_5, 255, 9, build_in_loop_time)

        def adjust_BG_color(self, hexColor):
            return _set_color(self, L.effect_settings.btn_color_2, hexColor)

    class Square(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 200, build_in_loop_time)

    class Squeeze(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 200, build_in_loop_time)

        def adjust_size_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 200, 0, build_in_loop_time)

        def enable_inverse(self, value=True):
            return only_set_checkbox(self, L.effect_settings.cbx_inverse, value)

    class Swing(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_angle_slider(self):
            _adjust_slider_to_handle_continue_dialog(self, L.effect_settings.slider_1)
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 173, build_in_loop_time)

        def adjust_BG_color(self, hexColor):
            return _set_color(self, L.effect_settings.btn_color_1, hexColor)

        def set_type(self, custom_type='Left'):
            return _set_option(self, L.effect_settings.cbx_type, custom_type)

    class Threshold(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 193, build_in_loop_time)

        def adjust_BG_color(self, hexColor):
            return _set_color(self, L.effect_settings.btn_color_1, hexColor)

    class Tiles(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_count_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 2, 15, build_in_loop_time)

        def adjust_BG_color(self, hexColor):
            return _set_color(self, L.effect_settings.btn_color_1, hexColor)

    class Triangle_Stretch(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 200, build_in_loop_time)

        def adjust_size_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 200, build_in_loop_time)

        def enable_inverse(self, value=True):
            return only_set_checkbox(self, L.effect_settings.cbx_inverse, value)

    class TV_Wall(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        @step('[Action][Effect Settings Page][TV_Wall] Adjust Horizontal Slider')
        def adjust_horizontal_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 200, build_in_loop_time)

        @step('[Action][Effect Settings Page][TV_Wall] Adjust Vertical Slider')
        def adjust_vertical_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 190, 18, build_in_loop_time)

    class Vertical_Stretch(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 200, build_in_loop_time)

        def adjust_y_offset_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 200, build_in_loop_time)

        def adjust_size_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_3, 0, 200, build_in_loop_time)

        def enable_inverse(self, value=True):
            return only_set_checkbox(self, L.effect_settings.cbx_inverse, value)

    class Vignette(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_width_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 220, 54, build_in_loop_time)

        def adjust_gradient_depth_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 1, 10, build_in_loop_time)

        def adjust_height_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_3, 180, 18, build_in_loop_time)

        def adjust_alpha_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_4, 0, 178, build_in_loop_time)

        def adjust_BG_color(self, hexColor):
            return _set_color(self, L.effect_settings.btn_color_2, hexColor)

    class Water_Reflection(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_vertical_mirror_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 200, 0, build_in_loop_time)

        def adjust_wave_interval_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 1, 10, build_in_loop_time)

        def adjust_wavelet_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_3, 1, 40, build_in_loop_time)

        def adjust_brightness_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_4, -10, 10, build_in_loop_time)

        def adjust_speed_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_5, 0, 200, build_in_loop_time)

        def enable_inverse(self, value=True):
            return only_set_checkbox(self, L.effect_settings.cbx_inverse, value)

    class Wave(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_period_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 200, 58, build_in_loop_time)

        def adjust_amplitude_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 200, build_in_loop_time)

    class Wave_Noise(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_frequency_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 200, build_in_loop_time)

        def adjust_strength_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 0, 200, build_in_loop_time)

    class Woodcut(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_brush_size_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 200, build_in_loop_time)

    class Zoom_In(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_width_slider(self):
            _adjust_slider_to_handle_continue_dialog(self, L.effect_settings.slider_1)
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 200, 12, build_in_loop_time)

        def adjust_height_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 194, 62, build_in_loop_time)

    class Zoom_Out(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_width_slider(self):
            _adjust_slider_to_handle_continue_dialog(self, L.effect_settings.slider_1)
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 0, 200, build_in_loop_time)

        def adjust_height_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 180, 25, build_in_loop_time)

        def adjust_BG_color(self, hexColor):
            return _set_color(self, L.effect_settings.btn_color_1, hexColor)

    class Magnifier(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_magnify_rate_slider(self):
            _adjust_slider_to_handle_continue_dialog(self, L.effect_settings.slider_1)
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 200, 32, build_in_loop_time)

        def adjust_frame_width_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 5, 100, build_in_loop_time)

        def adjust_magnify_size_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_3, 98, 64, build_in_loop_time)

        def adjust_aspect_ratio_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_4, 18, 182, build_in_loop_time)

        def adjust_frame_feather_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_5, 0, 100, build_in_loop_time)

        def set_magnify_type(self, custom_type='Circle'):
            return _set_option(self, L.effect_settings.cbx_magnify_type, custom_type)

        def adjust_frame_color(self, hexColor):
            return _set_color(self, L.effect_settings.btn_color_3, hexColor)

    class Pencil_Sketch(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_degree_slider(self):
            _adjust_slider_to_handle_continue_dialog(self, L.effect_settings.slider_1)
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 5, 40, build_in_loop_time)

        def adjust_edge_intensity_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_2, 20, 100, build_in_loop_time)

        def adjust_edge_degree_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_3, 230, 1, build_in_loop_time)

        def adjust_gradient_depth_slider(self):
            return _adjust_slider_in_loop(self, L.effect_settings.slider_4, 7, 200, build_in_loop_time)

        def set_mask_type(self, custom_type='Circle'):
            return _set_option(self, L.effect_settings.cbx_mask_type, custom_type)

        def enable_grayscale(self, value=True):
            return only_set_checkbox(self, L.effect_settings.cbx_grayscale, value)

        def enable_invert_masked_area(self, value=True):
            return only_set_checkbox(self, L.effect_settings.cbx_invert_masked_area, value)

        def enable_random_stroke(self, value=True):
            return only_set_checkbox(self, L.effect_settings.cbx_random_stroke, value)

    class Edge(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_degree_slider(self):
            _adjust_slider_to_handle_continue_dialog(self, L.effect_settings.slider_1)
            return _adjust_slider_in_loop(self, L.effect_settings.slider_1, 1, 255, build_in_loop_time)

        def adjust_BG_color(self, hexColor):
            return _set_color(self, L.effect_settings.btn_color_1, hexColor)

        def adjust_FG_color(self, hexColor):
            return _set_color(self, L.effect_settings.btn_color_2, hexColor)

    class Body_Effect(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def adjust_1st_slider(self, value_1, value_2, option=1, custom_loop_time=None):
            if option == 1:
                option_locator = L.effect_settings.slider_1
            elif option == 2:
                option_locator = L.effect_settings.slider_2
            elif option == 3:
                option_locator = L.effect_settings.slider_3
            elif option == 4:
                option_locator = L.effect_settings.slider_4
            elif option == 5:
                option_locator = L.effect_settings.slider_5
            elif option == 6:
                option_locator = L.effect_settings.slider_6
            elif option == 7:
                option_locator = L.effect_settings.slider_7
            else:
                logger(f'Invalid option {option}')
                return False

            if custom_loop_time:
                build_in_loop_time = custom_loop_time
            else:
                build_in_loop_time=5

            return _adjust_slider_in_loop(self, option_locator, value_1, value_2, build_in_loop_time)

        def adjust_BG_color(self, hexColor, option=1):
            if option == 1:
                option_locator = L.effect_settings.btn_color_1
            elif option == 2:
                option_locator = L.effect_settings.btn_color_2
            elif option == 3:
                option_locator = L.effect_settings.btn_color_3
            else:
                option_locator = option
            return _set_color(self, option_locator, hexColor)

        def set_dropdown_menu(self, custom_type, custom_locator):
            return _set_option(self, custom_locator, custom_type)

        def get_direction_control_pos(self):
            return self.backdoor.get_direction_control_pos()