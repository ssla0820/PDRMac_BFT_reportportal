import time, datetime, os, copy

from .base_page import BasePage
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
from .locator import locator as L
from reportportal_client import step

OPERATION_DELAY = 1 # sec


def checkbox_set_check(obj, locator, is_check=1):
    try:
        el_chx = obj.exist(locator)
        status = bool(el_chx.AXValue)
        if status != is_check:
            obj.el_click(el_chx)
            time.sleep(OPERATION_DELAY)
            if bool(obj.exist(locator).AXValue) != is_check:
                logger(f'Fail to verify status - {is_check=}')
                raise Exception
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        raise Exception
    return True


def editbox_set_value(obj, locator, value, verify=1):
    try:
        logger(f'input {value=}')
        obj.exist(locator).AXValue = str(value)
        time.sleep(OPERATION_DELAY)
        # verify value
        if verify:
            if obj.exist(locator).AXValue != str(value):
                logger('Fail to verify after set value')
                raise Exception
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        raise Exception
    return True


def combobox_select_by_index(self, combobox_locator, index):
    try:
        logger(f'{index=}')
        self.exist_click(combobox_locator)
        time.sleep(OPERATION_DELAY)
        el_menu = self.exist(L.produce.combobox_menu.menu)
        els_menu_item = self.exist_elements(L.produce.combobox_menu.menu_item, el_menu)
        select_option_text = self.exist(L.produce.combobox_menu.menu_item_text, els_menu_item[index - 1]).AXValue
        logger(f'current select={select_option_text}')
        self.el_click(els_menu_item[index - 1])
        time.sleep(OPERATION_DELAY * 0.5)
        # verify the result
        if self.exist(combobox_locator).AXTitle.replace('...', '') not in select_option_text:
            logger(f'Fail to verify set profile name. {self.exist(combobox_locator).AXTitle}')
            raise Exception
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        raise Exception
    return True


def editbox_get_value(obj, locator):
    try:
        value = obj.exist(locator).AXValue
        logger(f'get {value=}')
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        raise Exception
    return value

class Produce(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.local = self.Local(*args, **kwargs)
        self.online = self.Online(*args, **kwargs)

    def compare_timecode(self, timecode_1, timecode_2):  # format: 00;00;01;23
        result = 0  # 1: larger, 0: equal, -1: less
        try:
            list_timecode_1 = timecode_1.split(';')
            list_timecode_2 = timecode_2.split(';')
            value_1 = list_timecode_1[0] * 60 * 60 + list_timecode_1[1] * 60 + list_timecode_1[2] + list_timecode_1[3]
            value_2 = list_timecode_2[0] * 60 * 60 + list_timecode_2[1] * 60 + list_timecode_2[2] + list_timecode_2[3]
            if value_1 == value_2:
                result = 0
            elif value_1 > value_2:
                result = 1
            else:
                result = -1
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return result

    def verify_preview(self,file_path, similarity=0.95):
        file_full_path = os.path.abspath(file_path)
        toolbar = self.exist(L.main.top_toolbar)
        slider = self.exist(L.produce.slider_preview_playback)
        x = slider.AXPosition[0] + 25
        w = slider.AXSize[0] - 50
        y = toolbar.AXPosition[1] + toolbar.AXSize[1] + 15
        h = slider.AXPosition[1] - y
        time.sleep(OPERATION_DELAY)
        current_snapshot = self.image.snapshot(x=x, y=y, h=h, w=w)
        logger(f'{current_snapshot=}')
        return self.compare(file_full_path, current_snapshot, similarity)

    def switch_mode(self, mode='local'): # mode: local, online
        try:
            self.exist_click(eval(f'L.produce.tab_mode_{mode}'))
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_cancel_rendering(self):
        try:
            self.exist_click(L.produce.btn_cancel_rendering)
            time.sleep(OPERATION_DELAY)
            if not self.exist(L.produce.confirm_dialog.btn_yes, 3):
                logger('Fail to cancel rendering')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_confirm_cancel_rendering_dialog_yes(self):
        try:
            self.exist_click(L.produce.confirm_dialog.btn_yes)
            if not self.is_not_exist(L.produce.btn_cancel_rendering, None, OPERATION_DELAY * 6):
                logger('Fail to click confirm dialog yes')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            return False
        return True

    def click_confirm_cancel_rendering_dialog_no(self):
        try:
            self.exist_click(L.produce.confirm_dialog.btn_no)
            if self.is_not_exist(L.produce.btn_cancel_rendering, None, OPERATION_DELAY * 6):
                logger('Fail to click confirm dialog no')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            return False
        return True

    @step('[Verify][Produce] Check [Produce] page show')
    def check_enter_produce_page(self):
        return self.is_exist(L.produce.tab_mode_local)

    @step('[Action][Produce] Click [Edit] button')
    def click_edit(self):
        try:
            self.exist_click(L.main.btn_edit)
            if not self.exist(L.main.room_entry.btn_media_room, 3):
                logger('Fail to click confirm dialog yes')
                raise Exception('Fail to click confirm dialog yes')
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
    @step('[Action][Produce] Get timecode')
    def get_preview_timecode(self):
        return self.exist(L.produce.edittext_preview_playback_timecode).AXValue.replace(';', '_')

    def click_cancel_upload_video(self, timeout=30):
        try:
            el_btn = self.exist(L.produce.btn_cancel_upload)
            time_start = time.time()
            is_complete = 0
            while time.time() - time_start < timeout:
                if el_btn.AXEnabled:
                    self.click(L.produce.btn_cancel_upload)
                    self.exist_click(L.produce.confirm_dialog.btn_yes)
                    is_complete = 1
                    break
            if not is_complete:
                logger('Fail to click cancel upload video')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def get_pie_chart_remaining_size(self):
        return self.exist(L.produce.txt_remaining_size).AXValue

    def get_pie_chart_produced_size(self):
        return self.exist(L.produce.txt_produced_size).AXValue

    def get_pie_chart_time_remaining(self):
        try:
            value_time = self.exist(L.produce.txt_time_remaining).AXValue
            list_time = value_time.split(':')
            value_sec = int(list_time[0])*60*60 + int(list_time[1])*60 + int(list_time[2])
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return value_sec

    def get_pie_chart_time_elapsed(self):
        try:
            value_time = self.exist(L.produce.txt_time_elapsed).AXValue
            list_time = value_time.split(':')
            value_sec = int(list_time[0])*60*60 + int(list_time[1])*60 + int(list_time[2])
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return value_sec


    class Local(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.profile_analyzer = self.ProfileAnalyzer(*args, **kwargs)
            self.quality_profile_setup = self.QualityProfileSetup(*args, **kwargs)

        @step('[Action][Produce][Local] Select file format')
        def select_file_format(self, container):
            try:
                locator = eval(f'L.produce.local.btn_file_format_{container}')
                self.exist_click(locator)
                time.sleep(OPERATION_DELAY)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][Produce][Local] Check [Upload Copy to CyberLink Cloud] is visible')
        def check_visible_upload_copy_to_cyberlink_cloud(self):
            return self.is_exist(L.produce.local.chx_upload_copy_to_cyberlink_cloud, 2)

        @step('[Action][Produce][Local] Enable/ Disable [Upload Copy to CyberLink Cloud]')
        def set_check_upload_copy_to_cyberlink_cloud(self, is_check=1):
            locator = L.produce.local.chx_upload_copy_to_cyberlink_cloud
            return checkbox_set_check(self, locator, is_check)

        @step('[Action][Produce][Local] Click [Yes]/ [No] button on [Convert CyberLink Cloud Copy to MP4] dialog')
        def click_option_convert_cyberlink_cloud_copy_to_mp4_dialog(self, option=1): # 1: yes, 0: no
            try:
                map_list = {0: 'no', 1: 'yes'}
                locator = eval(f'L.produce.confirm_dialog.btn_{map_list[option]}')
                self.exist_click(locator)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True
        
        @step('[Verify][Produce][Local] Check [Back] button show on [Produce] page after produce complete')
        def check_back_btn_shows_on_upload_to_cyberlink_cloud_in_secs(self, wait_time=40):
            for i in range(wait_time):
                if self.is_exist(L.produce.btn_back_to_edit_after_upload_cl):
                    return True
                time.sleep(1)
            return False
        
        @step('[Action][Produce][Local] Click [Back] button on [Produce] page after produce complete')
        def click_back_btn_on_produce_page_after_upload(self):
            return self.click(L.produce.btn_back_to_edit_after_upload_cl)
        
        def click_profile_analyzer(self):
            try:
                self.exist_click(L.produce.local.btn_profile_analyzer)
                if not self.is_exist(L.produce.local.profile_analyzer.main_window):
                    logger('Fail to click profile analyzer')
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def click_cancel_upload_video(self, timeout=30):
            try:
                el_btn = self.exist_click(L.produce.btn_cancel_upload)
                time_start = time.time()
                is_complete = 0
                while time.time() - time_start < timeout:
                    if el_btn.AXEnabled:
                        self.el_click(el_btn)
                        self.exist_click(L.produce.confirm_dialog.btn_yes)
                        is_complete = 1
                        break
                if not is_complete:
                    logger('Fail to click cancel upload video')
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        class ProfileAnalyzer(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            def click_detail(self):
                try:
                    self.exist_click(L.produce.local.profile_analyzer.btn_detail)
                    if not self.is_exist(L.media_room.svrt_window.title):
                        logger('Fail to click detail of profile analyzer')
                        raise Exception
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def click_cancel(self):
                try:
                    self.exist_click(L.produce.local.profile_analyzer.btn_cancel)
                    time.sleep(OPERATION_DELAY)
                    if self.exist(L.produce.local.profile_analyzer.btn_cancel, 3):
                        logger('Fail to close profile analyzer dialog')
                        raise Exception
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def click_ok(self):
                try:
                    self.exist_click(L.produce.local.profile_analyzer.btn_ok)
                    time.sleep(OPERATION_DELAY)
                    if self.exist(L.produce.local.profile_analyzer.btn_ok, 3):
                        logger('Fail to click ok of profile analyzer dialog')
                        raise Exception
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def click_close(self):
                try:
                    self.exist_click(L.produce.local.profile_analyzer.btn_close)
                    time.sleep(OPERATION_DELAY)
                    if self.exist(L.produce.local.profile_analyzer.btn_close, 3):
                        logger('Fail to close profile analyzer dialog')
                        raise Exception
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def get_profile_name(self, index): # index - 1-based
                try:
                    els_row = self.exist_elements(L.produce.local.profile_analyzer.unit_table_row)
                    els_row_item = self.exist_elements(L.produce.local.profile_analyzer.unit_row_item, els_row[index-1])
                    value = els_row_item[0].AXValue
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return value

        @step('[Action][Produce][Local] Select [File Extension]')
        def select_file_extension(self, value):
            try:
                logger(f'input {value=}')
                self.exist_click(L.produce.local.cbx_file_extension)
                time.sleep(OPERATION_DELAY * 0.5)
                self.exist_click(eval(f'L.produce.local.file_extension.option_{value}'))
                time.sleep(OPERATION_DELAY * 0.5)
                # verify the result
                if self.exist(L.produce.local.cbx_file_extension).AXTitle != \
                        eval(f"L.produce.local.file_extension.option_{value}['AXValue']"):
                    logger(
                        f'Fail to verify set file extension. {self.exist(L.produce.local.cbx_file_extension).AXTitle}')
                    raise Exception(f'Fail to verify set file extension to {value}. {self.exist(L.produce.local.cbx_file_extension).AXTitle}')
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True
        
        @step('[Action][Produce][Local] Get [File Extension] value')
        def get_file_extension(self):
            return self.exist(L.produce.local.cbx_file_extension).AXTitle

        def select_profile_type(self, value):
            try:
                logger(f'input {value=}')
                self.exist_click(L.produce.local.cbx_profile_type)
                time.sleep(OPERATION_DELAY * 0.5)
                self.exist_click(eval(f'L.produce.local.profile_type.option_{value}'))
                time.sleep(OPERATION_DELAY * 0.5)
                # verify the result
                if self.exist(L.produce.local.cbx_profile_type).AXTitle != \
                        eval(f"L.produce.local.profile_type.option_{value}['AXValue']"):
                    logger(
                        f'Fail to verify set profile type. {self.exist(L.produce.local.cbx_profile_type).AXTitle}')
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        @step('[Action][Produce][Local] Select [Profile Name] by index')
        def select_profile_name(self, index):
            try:
                logger(f'{index=}')
                self.exist_click(L.produce.local.cbx_profile_quality)
                time.sleep(OPERATION_DELAY)
                el_menu = self.exist(L.produce.combobox_menu.menu)
                els_menu_item = self.exist_elements(L.produce.combobox_menu.menu_item, el_menu)
                select_option_text = self.exist(L.produce.combobox_menu.menu_item_text, els_menu_item[index-1]).AXValue
                logger(f'current select={select_option_text}')
                self.el_click(els_menu_item[index-1])
                time.sleep(OPERATION_DELAY * 0.5)
                #verify the result
                if self.exist(L.produce.local.cbx_profile_quality).AXTitle.replace('...', '') not in select_option_text:
                    logger(f'Fail to verify set profile name. {self.exist(L.produce.local.cbx_profile_quality).AXTitle}')
                    raise Exception(f'Fail to verify set profile name. {self.exist(L.produce.local.cbx_profile_quality).AXTitle}')
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def select_country_video_format(self, format): # format: 'ntsc', 'pal'
            try:
                format_dict = {'ntsc': 'ntsc', 'pal': 'togo'}
                format_verify = {'ntsc': 'NTSC', 'pal': 'Togo (PAL)'}
                self.exist_click(L.produce.local.cbx_country_format)
                time.sleep(1)
                self.keyboard.send(format_dict[format])
                time.sleep(OPERATION_DELAY * 0.5)
                with self.keyboard.pressed(self.keyboard.key.enter): time.sleep(OPERATION_DELAY)
                time.sleep(OPERATION_DELAY)
                # verify
                if not self.exist(L.produce.local.cbx_country_format).AXTitle == format_verify[format]:
                    logger(f'Fail to set country format: {format}')
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def click_create_a_new_profile(self):
            try:
                self.exist_click(L.produce.local.btn_create_a_new_profile)
                if not self.is_exist(L.produce.local.quality_profile_setup_dialog.main_window):
                    logger('Fail to click create a new profile button')
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def click_edit_custom_profile(self):
            try:
                self.exist_click(L.produce.local.btn_edit_custom_profile)
                if not self.is_exist(L.produce.local.quality_profile_setup_dialog.main_window):
                    logger('Fail to click custom profile button')
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def click_delete_custom_profile(self):
            try:
                self.exist_click(L.produce.local.btn_delete_custom_profile)
                time.sleep(OPERATION_DELAY * 0.5)
                self.exist_click(L.produce.confirm_dialog.btn_yes)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def click_no_customized_profiles_available_ok(self):
            try:
                self.exist_click(L.produce.confirm_dialog.btn_yes)
                time.sleep(OPERATION_DELAY * 0.5)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        @step('[Action][Produce][Local] Get [Profile Name] value')
        def get_profile_name(self):
            return self.exist(L.produce.local.cbx_profile_quality).AXTitle

        def get_country_video_format(self):
            return self.exist(L.produce.local.cbx_country_format).AXTitle

        class QualityProfileSetup(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            def switch_to_video_tab(self):
                try:
                    self.exist_click(L.produce.local.quality_profile_setup_dialog.tab_video)
                    if not self.is_exist(L.produce.local.quality_profile_setup_dialog.video.cbx_resolution):
                        logger('Fail to switch to video tab')
                        raise Exception
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def switch_to_audio_tab(self):
                try:
                    self.exist_click(L.produce.local.quality_profile_setup_dialog.tab_audio)
                    if not self.is_exist(L.produce.local.quality_profile_setup_dialog.audio.cbx_compression):
                        logger('Fail to switch to audio tab')
                        raise Exception
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def apply_profile_name(self, profile_name, description):
                try:
                    self.exist(
                        L.produce.local.quality_profile_setup_dialog.profile_name.edittext_profile_name).AXValue = profile_name
                    time.sleep(OPERATION_DELAY * 0.5)
                    self.exist(
                        L.produce.local.quality_profile_setup_dialog.profile_name.edittext_description).AXValue = description
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def set_video_resolution(self, index):
                return combobox_select_by_index(self, L.produce.local.quality_profile_setup_dialog.video.cbx_resolution, index)

            def set_video_frame_rate(self, index):
                return combobox_select_by_index(self, L.produce.local.quality_profile_setup_dialog.video.cbx_frame_rate, index)

            def set_video_profile_type(self, index):
                return combobox_select_by_index(self, L.produce.local.quality_profile_setup_dialog.video.cbx_profile_type, index)

            def set_video_profile(self, index_resolution, index_frame_rate, index_profile_type=None):
                try:
                    self.set_video_resolution(index_resolution)
                    self.set_video_frame_rate(index_frame_rate)
                    if index_profile_type:
                        self.set_video_profile_type(index_profile_type)
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def set_video_entropy_coding(self, index):
                try:
                    coding_type = ['cabac', 'cavlc']
                    locator = eval(f'L.produce.local.quality_profile_setup_dialog.video.rdb_entropy_coding_{coding_type[index-1]}')
                    checkbox_set_check(self, locator, 1)
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def set_video_bitrate(self, value):
                try:
                    locator = L.produce.local.quality_profile_setup_dialog.video.edittext_bitrate
                    editbox_set_value(self, locator, value)
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def set_audio_compression(self, index):
                return combobox_select_by_index(self, L.produce.local.quality_profile_setup_dialog.audio.cbx_compression, index)

            def set_audio_channel(self, index):
                return combobox_select_by_index(self, L.produce.local.quality_profile_setup_dialog.audio.cbx_channel, index)

            def set_audio_compression_rate(self, index):
                return combobox_select_by_index(self, L.produce.local.quality_profile_setup_dialog.audio.cbx_compression_rate, index)

            def set_audio_profile(self, index_compression, index_channel, index_compression_rate):
                try:
                    self.set_audio_compression(index_compression)
                    self.set_audio_channel(index_channel)
                    self.set_audio_compression_rate(index_compression_rate)
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def click_close(self):
                try:
                    self.exist_click(L.produce.local.quality_profile_setup_dialog.btn_close)
                    time.sleep(OPERATION_DELAY)
                    if self.is_exist(L.produce.local.quality_profile_setup_dialog.btn_close, 2):
                        logger('Fail to click close button')
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def click_ok(self):
                try:
                    self.exist_click(L.produce.local.quality_profile_setup_dialog.btn_ok)
                    time.sleep(OPERATION_DELAY)
                    if self.is_exist(L.produce.local.quality_profile_setup_dialog.btn_ok, 2):
                        logger('Fail to click ok button')
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def click_cancel(self):
                try:
                    self.exist_click(L.produce.local.quality_profile_setup_dialog.btn_cancel)
                    time.sleep(OPERATION_DELAY)
                    if self.is_exist(L.produce.local.quality_profile_setup_dialog.btn_cancel, 2):
                        logger('Fail to click close button')
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

        def click_details(self):
            try:
                self.exist_click(L.produce.local.btn_detail)
                time.sleep(OPERATION_DELAY)
                if not self.is_exist(L.produce.local.details_dialog.main_window):
                    logger('Fail to click detail dialog')
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        @step('[Action][Produce][Local] Enable/ Disable [Fast Video Rendering]')
        def set_fast_video_rendering(self, is_checked=1):
            try:
                locator = L.produce.local.chx_fast_video_rendering
                checkbox_set_check(self, locator, is_checked)
                time.sleep(OPERATION_DELAY*0.5)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def set_fast_video_rendering_svrt(self):
            try:
                locator = L.produce.local.rdb_fast_video_rendering_svrt
                checkbox_set_check(self, locator, 1)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        @step('[Action][Produce][Local] Set [Fast Video Rendering] to (Hardware Encode)')
        def set_fast_video_rendering_hardware_encode(self):
            try:
                locator = L.produce.local.rdb_fast_video_rendering_hardware_encode
                checkbox_set_check(self, locator, 1)
                time.sleep(OPERATION_DELAY*0.5)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True
        
        @step('[Action][Produce][Local] Get [Fast Video Rendering - Hardware Encode] status')
        def get_fast_video_rendering_hardware_encode_status(self):
            return bool(self.exist(L.produce.local.rdb_fast_video_rendering_hardware_encode).AXValue)

        def get_fast_video_rendering_svrt_status(self):
            return bool(self.exist(L.produce.local.rdb_fast_video_rendering_svrt).AXValue)

        @step('[Action][Produce][Local] Enable/ Disable [Surround Sound]')
        def set_surround_sound(self, is_checked=1):
            try:
                locator = L.produce.local.chx_surround_sound
                checkbox_set_check(self, locator, is_checked)
                time.sleep(OPERATION_DELAY*0.5)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][Produce][Local] Set [Surround Sound] to (AAC 5.1)')
        def set_surround_sound_aac51(self):
            try:
                locator = L.produce.local.rdb_surround_sound_ac51
                checkbox_set_check(self, locator, 1)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def set_surround_sound_true_theater_option(self, option):
            try:
                locator = L.produce.local.rdb_surround_sound_true_theater
                checkbox_set_check(self, locator, 1)
                time.sleep(OPERATION_DELAY * 0.5)
                self.exist_click(L.produce.local.btn_surround_sound_true_theater_dialog)
                time.sleep(OPERATION_DELAY * 0.5)
                option_locator = eval(f'L.produce.local.true_theater_settings_dialog.rdb_{option}')
                checkbox_set_check(self, option_locator, 1)
                time.sleep(OPERATION_DELAY * 0.5)
                self.exist_click(L.produce.local.true_theater_settings_dialog.btn_ok)
                time.sleep(OPERATION_DELAY)
                if self.is_exist(option_locator, 2):
                    logger(f'Fail to apply {option}')
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def set_surround_sound_true_theater_option_living_room(self):
            option = 'living_room'
            return self.set_surround_sound_true_theater_option(option)

        @step('[Action][Produce][Local] Set [Surround Sound] to (Theater) option')
        def set_surround_sound_true_theater_option_theater(self):
            option = 'theater'
            return self.set_surround_sound_true_theater_option(option)

        def set_surround_sound_true_theater_option_stadium(self):
            option = 'stadium'
            return self.set_surround_sound_true_theater_option(option)
        
        @step('[Action][Produce][Local] Set timecode')
        def set_preview_timecode(self, str_timecode):
            return self._set_timecode(str_timecode, L.produce.edittext_preview_playback_timecode)

    def drag_slider_to_timecode(self, timecode, timeline_frame_rate=30, max_fix_step=30):
        try:
            slider_max_value = self.exist(L.produce.slider_preview_playback).AXMaxValue
            slider_size = self.exist(L.produce.slider_preview_playback).AXSize
            indicator_size = self.exist(L.produce.indicator_preview_playback).AXSize
            indicator_position = self.exist(L.produce.indicator_preview_playback).AXPosition
            unit_slider_x_pixel_per_value = slider_size[0]/slider_max_value
            if unit_slider_x_pixel_per_value < 1:
                unit_slider_x_pixel_per_value = 1 # min shift unit: 1 pixel
            # transfer from timecode to value
            list_timecode = timecode.split('_')
            value = (int(list_timecode[0])*60*60 + int(list_timecode[1])*60 + int(list_timecode[2]))*timeline_frame_rate + int(list_timecode[3])
            input_timecode = f'{list_timecode[0]};{list_timecode[1]};{list_timecode[2]};{list_timecode[3]}'
            # drag indicator to position
            start_pos = (indicator_position[0]+int(indicator_size[0]/2), indicator_position[1]+int(indicator_size[1]/2))
            end_pos = (indicator_position[0]+int(value*unit_slider_x_pixel_per_value), indicator_position[1]+int(indicator_size[1]/2))
            self.mouse.drag(start_pos, end_pos)
            curr_timecode = self.exist(L.produce.edittext_preview_playback_timecode).AXValue
            # adjust the indicator
            cnt_step = 1
            is_completed = 0
            unit_shift_step = int(unit_slider_x_pixel_per_value)
            if self.compare_timecode(curr_timecode, input_timecode) > 0:
                unit_shift_step = -int(unit_slider_x_pixel_per_value)
            while cnt_step < max_fix_step:
                if curr_timecode == f'{list_timecode[0]};{list_timecode[1]};{list_timecode[2]};{list_timecode[3]}':
                    logger(f'Match timecode > {curr_timecode}')
                    is_completed = 1
                    break
                start_pos = end_pos
                end_pos = (end_pos[0]+unit_shift_step, end_pos[1])
                self.mouse.drag(start_pos, end_pos)
                curr_timecode = self.exist(L.produce.edittext_preview_playback_timecode).AXValue
                cnt_step += 1
            if not is_completed:
                logger('Fail to drag indicator to timecode. Over the max fix step.')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_preview_operation(self, operation): # operation: play, pause, stop, next_frame, previous_frame
        try:
            locator = eval(f'L.produce.btn_preview_playback_{operation}')
            self.exist_click(locator)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Produce] Click [Select Output Folder] button and select output folder')
    def select_output_folder(self, file_path): # file_path: the full path of output file
        try:
            self.exist_click(L.produce.btn_select_output_folder)
            self.select_file(file_path)
            time.sleep(OPERATION_DELAY)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True
    
    @step('[Action][Produce] Get [Produced Filename]')
    def get_produced_filename(self):
        try:
            file_path = self.exist(L.produce.edittext_output_folder).AXValue
            filename = file_path.split('/')[-1]
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return filename

    @step('[Action][Produce] Click [Start] button to produce')
    def click_start(self):
        try:
            self.exist_click(L.produce.btn_start_produce)
            if not self.is_exist(L.produce.btn_pause_produce):
                logger('Fail to click start produce')
                raise Exception('Fail to click start produce')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_pause(self):
        return self.exist_click(L.produce.btn_pause_produce)

    def click_resume(self):
        return self.exist_click(L.produce.btn_resume_produce)

    def click_previous(self):
        try:
            self.exist_click(L.produce.btn_previous)
            if not self.is_exist(L.produce.local.btn_file_format_avc):
                logger('Fail to click previous button')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_back_to_edit(self, timeout=10):
        try:
            time.sleep(OPERATION_DELAY*3)
            self.click(L.produce.btn_back_to_edit_page)
            if not self.is_exist(L.media_room.btn_import_media, timeout):
                self.press_esc_key()
                logger('Press Esc key to close five star dialog')

                self.exist_click(L.produce.btn_back_to_edit_page)
                if not self.is_exist(L.media_room.btn_import_media, timeout):
                    logger('Fail to click back to edit button')
                    raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Verify][Produce] Check [Produce] is completed')
    def check_produce_complete(self, wait_time=60):
        try:
            result = False
            for _ in range(wait_time):
                if 'complete' in self.exist(L.produce.txt_producing_video_progress).AXValue:
                    logger('Produce is completed')
                    result = True
                    break
                time.sleep(1)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return result

    class Online(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.sign_in_to_youtube = self.SignIn_to_YouTube(*args, **kwargs)

        def select_profile_type(self, index):
            locator = L.produce.online.cbx_profile_type
            return combobox_select_by_index(self, locator, index)

        def select_online_site(self, name='youtube'):
            try:
                locator = eval(f'L.produce.online.btn_site_{name}')
                self.exist_click(locator)
                time.sleep(OPERATION_DELAY)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def get_profile_type(self):
            return self.exist(L.produce.online.cbx_profile_type).AXTitle

        def remove_title(self):
            locator = L.produce.online.edittext_title
            return editbox_set_value(self, locator, '')

        def set_title(self, value):
            locator = L.produce.online.edittext_title
            return editbox_set_value(self, locator, value)

        def remove_description(self):
            locator = L.produce.online.edittext_description
            return editbox_set_value(self, locator, '')

        def set_description(self, value):
            locator = L.produce.online.edittext_description
            return editbox_set_value(self, locator, value)

        def remove_tags(self):
            locator = L.produce.online.edittext_tags
            return editbox_set_value(self, locator, '')

        def set_tags(self, value):
            locator = L.produce.online.edittext_tags
            return editbox_set_value(self, locator, value)

        def select_youtube_video_category(self, index):
            locator = L.produce.online.cbx_video_categories
            return combobox_select_by_index(self, locator, index)

        def get_youtube_video_category(self):
            locator = L.produce.online.cbx_video_categories
            return self.exist(locator).AXTitle

        def set_public_sharing_enable(self):
            locator = L.produce.online.rdb_public_sharing
            return checkbox_set_check(self, locator)

        def set_private_sharing_enable(self):
            locator = L.produce.online.rdb_private_sharing
            return checkbox_set_check(self, locator)

        def set_hardware_video_encode(self, is_enable=1):
            locator = L.produce.online.chx_hardware_encode
            return checkbox_set_check(self, locator, is_enable)

        def get_hardware_video_encode_status(self):
            locator = L.produce.online.chx_hardware_encode
            return bool(self.exist(locator).AXValue)

        class SignIn_to_YouTube(BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            # def check_webpage_ready(self, locator, timeout=10):
            #     try:
            #         start_time = time.time()
            #         is_ready = 0
            #         while time.time() - start_time < timeout:
            #             try:
            #                 if self.exist(locator, None, 3):
            #                     logger('Webpage is ready.')
            #                     is_ready = 1
            #                     break
            #             except:
            #                 time.sleep(3)
            #         if not is_ready:
            #             logger('Fail to wait webpage ready')
            #             raise
            #     except Exception as e:
            #         logger(f'Exception occurs. log={e}')
            #         raise Exception
            #     return True
            #
            # def handle_sign_in_page(self, account, pw, timeout=10): # for using this, needs chrome driver to create page
            #     try:
            #         # if found translate dialog, close it
            #         el_translate_close = self.exist(L.produce.online.sign_in_to_youtube_dialog.chrome_sign_in_page.btn_translate_dialog_close, None, 3)
            #         if el_translate_close:
            #             self.el_click(el_translate_close)
            #         time.sleep(OPERATION_DELAY * 2)
            #         # select other account
            #         self.check_webpage_ready(L.produce.online.sign_in_to_youtube_dialog.chrome_sign_in_page.txt_use_other_account)
            #         self.exist_click(L.produce.online.sign_in_to_youtube_dialog.chrome_sign_in_page.txt_use_other_account)
            #         self.exist(L.produce.online.sign_in_to_youtube_dialog.chrome_sign_in_page.edittext_account, None, timeout)
            #         time.sleep(OPERATION_DELAY * 2)
            #         # enter account
            #         self.keyboard.send(account)
            #         time.sleep(OPERATION_DELAY * 0.5)
            #         self.exist(L.produce.online.sign_in_to_youtube_dialog.chrome_sign_in_page.btn_continue).press()
            #         # enter password
            #         self.exist(L.produce.online.sign_in_to_youtube_dialog.chrome_sign_in_page.edittext_password, None, timeout)
            #         time.sleep(OPERATION_DELAY * 2)
            #         self.keyboard.send(pw)
            #         time.sleep(OPERATION_DELAY * 0.5)
            #         self.exist(L.produce.online.sign_in_to_youtube_dialog.chrome_sign_in_page.btn_continue).press()
            #         # allow to access your google account
            #         self.check_webpage_ready(L.produce.online.sign_in_to_youtube_dialog.chrome_sign_in_page.txt_would_like_to_access_your_account)
            #         self.exist(L.produce.online.sign_in_to_youtube_dialog.chrome_sign_in_page.txt_would_like_to_access_your_account, None, timeout * 2)
            #         self.exist(L.produce.online.sign_in_to_youtube_dialog.chrome_sign_in_page.btn_allow_to_access).press()
            #         # get authorization code
            #         self.check_webpage_ready(L.produce.online.sign_in_to_youtube_dialog.chrome_sign_in_page.txt_authorization_code)
            #         el_authorization_code = self.exist(L.produce.online.sign_in_to_youtube_dialog.chrome_sign_in_page.txt_authorization_code, None, timeout * 2)
            #         authorization_code = el_authorization_code.AXValue
            #         print(f'{authorization_code=}')
            #         # close chrome app
            #         # self.close_app()
            #         # time.sleep(OPERATION_DELAY)
            #     except Exception as e:
            #         logger(f'Exception occurs. log={e}')
            #         raise Exception
            #     return authorization_code

            def click_sign_in(self):
                try:
                    self.exist_click(L.produce.online.sign_in_to_youtube_dialog.btn_sign_in)
                    time.sleep(OPERATION_DELAY * 2)
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def set_authorization_code(self, value):
                try:
                    self.exist(L.produce.online.sign_in_to_youtube_dialog.edittext_authorization_code).AXValue = value
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception
                return True

            def click_next(self):
                return self.exist_click(L.produce.online.sign_in_to_youtube_dialog.btn_next)

        def click_make_sure_fill_in_fields_ok(self):
            return self.exist_click(L.main.confirm_dialog.btn_ok)

        def check_produce_and_upload_complete(self, timeout=5):
            try:
                result = False
                if self.is_exist(L.produce.txt_produce_and_upload_complete, None, timeout):
                    logger('Produce and Upload is completed')
                    result = True
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return result
