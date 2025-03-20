import time, datetime, os, copy
import os.path
from os.path import expanduser
from reportportal_client import step

from .base_page import BasePage
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
from .locator import locator as L

OPERATION_DELAY = 1 # sec


def select_combobox_item(obj, locator_combobox, locator_option):
    try:
        locator = locator_option
        el_cbx = obj.exist(locator_combobox)
        if el_cbx.AXTitle != locator['AXValue']:
            obj.el_click(el_cbx)
            time.sleep(OPERATION_DELAY * 0.5)
            obj.exist_click(locator)
            time.sleep(OPERATION_DELAY * 0.5)
            # verify if apply correctly
            if obj.exist(locator_combobox).AXTitle != locator['AXValue']:
                logger(f'Fail to verify apply combobox setting.')
                raise Exception
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        raise Exception
    return True

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

@step('[Action][Preferences_Page] Set editbox value')
def editbox_set_value(obj, locator, value, verify=1):
    try:
        logger(f'input {value=}')
        obj.exist(locator).AXValue = str(value)
        time.sleep(OPERATION_DELAY)
        # verify value
        if verify:
            if obj.exist(locator).AXValue != str(value):
                logger('Fail to verify after set value')
                raise Exception('Fail to verify after set value')
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        raise Exception(f'Exception occurs. log={e}')
    return True


def editbox_get_value(obj, locator):
    try:
        value = obj.exist(locator).AXValue
        logger(f'get {value=}')
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        raise Exception
    return value


def set_arrow_button(obj, locator_parent, direction='up', times=1):
    try:
        locator = locator_parent.copy()
        locator.append(eval(f'L.preferences.arrow_{direction.lower()}'))
        el_arrow = obj.exist(locator)
        for unit in range(times):
            obj.el_click(el_arrow)
            time.sleep(OPERATION_DELAY * 0.5)
        time.sleep(OPERATION_DELAY)
    except Exception as e:
        logger(f'Exception occurs. log={e}')
        return False
    return True


class Preferences_Page(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.general = self.General(*args, **kwargs)
        self.editing = self.Editing(*args, **kwargs)
        self.file = self.File(*args, **kwargs)
        self.display = self.Display(*args, **kwargs)
        self.project = self.Project(*args, **kwargs)
        self.confirmation = self.Confirmation(*args, **kwargs)
        self.director_zone = self.DirectorZone(*args, **kwargs)
        self.cyberlink_cloud = self.CyberlinkCloud(*args, **kwargs)

    @step('[Action][Preferences_Page] Click [OK] button to leave [Preferences page]')
    def click_ok(self):
        try:
            img_before = self.screenshot()
            self.exist_click(L.preferences.btn_ok)
            time.sleep(OPERATION_DELAY)
            self.exist_click(L.preferences.confirm_dialog.btn_ok, 3)
            self.wait_for_image_changes(img_before, similarity=0.97)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_cancel(self):
        try:
            self.exist_click(L.preferences.btn_cancel)
            start_time = time.time()
            is_complete = 0
            while time.time() - start_time < 10:
                if self.is_exist(L.preferences.btn_cancel, 2):
                    time.sleep(OPERATION_DELAY)
                    continue
                is_complete = 1
                break
            if not is_complete:
                logger('Fail to click cancel')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_close(self):
        try:
            img_before = self.screenshot()
            self.exist_click(L.preferences.btn_close)
            self.wait_for_image_changes(img_before)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def switch_to_general(self):
        try:
            if not self.exist_click(L.preferences.tab_general):
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Preferences_Page] Switch to [Editing] tab')
    def switch_to_editing(self):
        try:
            if not self.exist_click(L.preferences.tab_editing):
                raise Exception('Fail to click [Editing] tab')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def switch_to_file(self):
        try:
            if not self.exist_click(L.preferences.tab_file):
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def switch_to_display(self):
        try:
            if not self.exist_click(L.preferences.tab_display):
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Preferences_Page] Switch to [Project] tab')
    def switch_to_project(self):
        try:
            if not self.exist_click(L.preferences.tab_project):
                raise Exception('There is no [Project] tab')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def switch_to_confirmation(self):
        try:
            if not self.exist_click(L.preferences.tab_confirmation):
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def switch_to_director_zone(self):
        try:
            if not self.exist_click(L.preferences.tab_director_zone):
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def switch_to_cyberlink_cloud(self):
        try:
            if not self.exist_click(L.preferences.tab_cyberlink_cloud):
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def get_exist_render_file_amount(self):
        root = expanduser("~")
        render_file_path = root + '/Library/Group Containers/FPY8L862BK.com.cyberlink.powerdirector/Library/Caches/Preview Cache Files'
        #logger(render_file_path
        files = os.listdir(render_file_path)

        # Note: if [Preview Cache Files] is empty, the query number len(files) is 1
        current_file_num = len(files) - 1
        return current_file_num

    class General(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def maximum_undo_levels_set_value(self, value):
            try:
                logger(f'input {value=}')
                self.exist(L.preferences.general.input_text_maximum_undo_levels).AXValue = value
                time.sleep(OPERATION_DELAY)
                # verify value
                if self.exist(L.preferences.general.input_text_maximum_undo_levels).AXValue != value:
                    logger('Fail to set the maximum undo level')
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def maximum_undo_levels_set_arrow_button(self, direction='up', times=1):
            try:
                value_before = self.exist(L.preferences.general.input_text_maximum_undo_levels).AXValue
                locator = eval(f'L.preferences.general.btn_maximum_undo_levels_{direction}')
                el_arrow = self.exist(locator)
                for unit in range(times):
                    self.el_click(el_arrow)
                    time.sleep(OPERATION_DELAY * 0.5)
                time.sleep(OPERATION_DELAY)
                value_after = self.exist(L.preferences.general.input_text_maximum_undo_levels).AXValue
                if abs(int(value_after) - int(value_before)) != times:
                    logger(f'Fail to verify value. {value_after=}')
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                return False
            return True

        @step('[Action][Preferences_Page][General] Set [Audio Channels] to (Stereo)')
        def audio_channels_set_stereo(self):
            try:
                self.exist_click(L.preferences.general.audio_channels.btn_combobox)
                time.sleep(OPERATION_DELAY * 0.5)
                self.exist_click(L.preferences.general.audio_channels.menu_item_stereo)
                time.sleep(OPERATION_DELAY * 0.5)
                # verify the result
                if self.exist(L.preferences.general.audio_channels.btn_combobox).AXTitle != L.preferences.general.audio_channels.menu_item_stereo['AXValue']:
                    logger('Fail to verify set stereo')
                    raise Exception('Fail to verify set stereo')
                time.sleep(OPERATION_DELAY)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][Preferences_Page][General] Set [Audio Channels] to (5.1 Surround)')
        def audio_channels_set_51_surround(self):
            try:
                self.exist_click(L.preferences.general.audio_channels.btn_combobox)
                time.sleep(OPERATION_DELAY * 0.5)
                self.exist_click(L.preferences.general.audio_channels.menu_item_51_surround)
                time.sleep(OPERATION_DELAY * 0.5)
                # verify the result
                if self.exist(L.preferences.general.audio_channels.btn_combobox).AXTitle != L.preferences.general.audio_channels.menu_item_51_surround['AXValue']:
                    logger('Fail to verify set stereo')
                    raise Exception('Fail to verify set stereo')
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def timeline_frame_rate_set_value(self, value): # value: 24, 25, 30, 50, 60
            try:
                logger(f'input {value=}')
                self.exist_click(L.preferences.general.timeline_frame_rate.btn_combobox)
                time.sleep(OPERATION_DELAY * 0.5)
                self.exist_click(eval(f'L.preferences.general.timeline_frame_rate.menu_item_{value}_fps'))
                time.sleep(OPERATION_DELAY * 0.5)
                # verify the result
                if self.exist(L.preferences.general.timeline_frame_rate.btn_combobox).AXTitle != \
                        eval(f"L.preferences.general.timeline_frame_rate.menu_item_{value}_fps['AXValue']"):
                    logger(f'Fail to verify set timeline frame rate. {self.exist(L.preferences.general.timeline_frame_rate.btn_combobox).AXTitle}')
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def timeline_frame_rate_set_24_fps(self):
            return self.timeline_frame_rate_set_value(24)

        def timeline_frame_rate_set_25_fps(self):
            return self.timeline_frame_rate_set_value(25)

        def timeline_frame_rate_set_30_fps(self):
            return self.timeline_frame_rate_set_value(30)

        def timeline_frame_rate_set_50_fps(self):
            return self.timeline_frame_rate_set_value(50)

        def timeline_frame_rate_set_60_fps(self):
            return self.timeline_frame_rate_set_value(60)

        def use_drop_frame_timecode_set_option(self, value): # option: 'yes', 'no'
            try:
                logger(f'input {value=}')
                self.exist_click(L.preferences.general.use_drop_frame_timecode.btn_combobox)
                time.sleep(OPERATION_DELAY * 0.5)
                self.exist_click(eval(f'L.preferences.general.use_drop_frame_timecode.menu_item_{value}'))
                time.sleep(OPERATION_DELAY * 0.5)
                # verify the result
                if self.exist(L.preferences.general.use_drop_frame_timecode.btn_combobox).AXTitle != \
                        eval(f"L.preferences.general.use_drop_frame_timecode.menu_item_{value}['AXValue']"):
                    logger(
                        f'Fail to verify set use drop frame timecode. {self.exist(L.preferences.general.use_drop_frame_timecode.btn_combobox).AXTitle}')
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def use_drop_frame_timecode_set_yes(self):
            return self.use_drop_frame_timecode_set_option('yes')

        def use_drop_frame_timecode_set_no(self):
            return self.use_drop_frame_timecode_set_option('no')

        def combobox_set_check(self, locator, is_check=1): # is_check: 1-check (default), 0-uncheck
            try:
                el_chx = self.exist(locator)
                if el_chx.AXValue != is_check:
                    self.el_click(el_chx)
                    time.sleep(OPERATION_DELAY * 0.5)
                    # verify status
                    if self.exist(locator).AXValue != is_check:
                        logger('Fail to verify status after set check')
                        raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def show_sound_waveform_set_check(self, is_check=1):
            locator = L.preferences.general.chx_show_sound_waveform
            return self.combobox_set_check(locator, is_check)

        def play_audio_while_scrubbing_set_check(self, is_check=1):
            locator = L.preferences.general.chx_play_audio_while_scrubbing
            return self.combobox_set_check(locator, is_check)

        def enable_continuous_thumbnail_on_video_set_check(self, is_check=1):
            locator = L.preferences.general.chx_enable_continuous_thumbnail_on_video
            return self.combobox_set_check(locator, is_check)

        def enable_shadow_file_set_check(self, is_check=1):
            locator = L.preferences.general.chx_enable_shadow_file
            return self.combobox_set_check(locator, is_check)

        def shadow_file_apply_resolution(self, value): # value: 1, 2, 3
            try:
                resolution = ['', '720_480', '1280_720', '1920_1080']
                logger(f'input {value=}')
                if value < 1 or value > 3:
                    logger('Incorrect input. It should be 1, 2, 3.')
                    raise Exception
                self.exist_click(L.preferences.general.shadow_file_resolution.btn_combobox)
                time.sleep(OPERATION_DELAY * 0.5)
                self.exist_click(eval(f'L.preferences.general.shadow_file_resolution.menu_item_{resolution[value]}'))
                time.sleep(OPERATION_DELAY * 0.5)
                # verify the result
                if self.exist(L.preferences.general.shadow_file_resolution.btn_combobox).AXTitle != \
                        eval(f"L.preferences.general.shadow_file_resolution.menu_item_{resolution[value]}['AXValue']"):
                    logger(f'Fail to verify set shadow file resolution. {self.exist(L.preferences.general.shadow_file_resolution.btn_combobox).AXTitle}')
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def render_preview_in_uhd_preview_quality_is_enabled(self):
            try:
                value = bool(self.exist(L.preferences.general.chx_render_preview_in_uhd_preview_quality).AXValue)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return value

        def render_preview_in_uhd_preview_quality_set_check(self, is_check=1):
            try:
                status = self.render_preview_in_uhd_preview_quality_is_enabled()
                if status != is_check:
                    self.exist_click(L.preferences.general.chx_render_preview_in_uhd_preview_quality)
                    time.sleep(OPERATION_DELAY)
                    if self.render_preview_in_uhd_preview_quality_is_enabled() != is_check:
                        logger(f'Fail to verify status - {is_check=}')
                        raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def auto_delete_temporary_files_set_check(self, is_check=1):
            try:
                el_chx = self.exist(L.preferences.general.chx_auto_delete_temporary_files)
                status = bool(el_chx.AXValue)
                if status != is_check:
                    self.el_click(el_chx)
                    time.sleep(OPERATION_DELAY)
                    if bool(self.exist(L.preferences.general.chx_auto_delete_temporary_files).AXValue) != is_check:
                        logger(f'Fail to verify status - {is_check=}')
                        raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def auto_delete_temporary_files_days_input_value(self, value):
            try:
                self.exist(L.preferences.general.auto_delete_temporary_files.input_days).AXValue = str(value)
                time.sleep(OPERATION_DELAY)
                value_after = self.exist(L.preferences.general.auto_delete_temporary_files.input_days).AXValue
                if value != value_after:
                    logger(f'Fail to verify {value_after=}')
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def auto_delete_temporary_files_days_click_arrow_button(self, direction='up', times=1):
            try:
                value_before = self.exist(L.preferences.general.auto_delete_temporary_files.input_days).AXValue
                el_arrow = self.exist(eval(f'L.preferences.general.auto_delete_temporary_files.btn_days_arrow_{direction}'))
                for op in range(times):
                    self.el_click(el_arrow)
                    time.sleep(OPERATION_DELAY * 0.5)
                value_after = self.exist(L.preferences.general.auto_delete_temporary_files.input_days).AXValue
                if abs(int(value_after) - int(value_before)) != times:
                    logger(f'Fail to verify {value_after=}')
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def click_manually_delete(self):
            try:
                # click [manually delete]
                if not self.exist_click(L.preferences.general.btn_manually_delete):
                    raise Exception

                if self.exist(L.preferences.alert_dialog.main, timeout=6):
                    self.exist_click(L.preferences.alert_dialog.btn_yes)

                # verify step:
                if self.exist(L.preferences.alert_dialog.main):
                    raise Exception

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def language_use_system_default_set_apply(self):
            try:
                el_chx = self.exist(L.preferences.general.language.chx_use_system_default)
                if not el_chx.AXValue:
                    self.el_click(el_chx)
                    time.sleep(OPERATION_DELAY * 0.5)
                # verify if checked
                if not self.exist(L.preferences.general.language.chx_use_system_default).AXValue:
                    logger('Fail to verify apply setting')
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def language_use_uer_defined_set_apply(self, lang='eng'):
            try:
                el_chx = self.exist(L.preferences.general.language.chx_user_defined)
                if not el_chx.AXValue:
                    self.el_click(el_chx)
                    time.sleep(OPERATION_DELAY * 0.5)
                # select language option
                locator = eval(f'L.preferences.general.language.option_language_{lang}')
                if self.exist(L.preferences.general.language.cbx_language).AXTitle == locator['AXValue']:
                    logger('Language match. SKIP it.')
                    return True
                self.exist_click(L.preferences.general.language.cbx_language)
                time.sleep(OPERATION_DELAY * 0.5)
                self.exist_click(locator)
                time.sleep(OPERATION_DELAY * 0.5)
                # verify if apply correctly
                if self.exist(L.preferences.general.language.cbx_language).AXTitle != locator['AXValue']:
                    logger(f'Fail to verify apply setting. {lang=}')
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def language_use_uer_defined_apply_deu(self):
            return self.language_use_uer_defined_set_apply('deu')

        def language_use_uer_defined_apply_eng(self):
            return self.language_use_uer_defined_set_apply('eng')

        def language_use_uer_defined_apply_esp(self):
            return self.language_use_uer_defined_set_apply('esp')

        def language_use_uer_defined_apply_fra(self):
            return self.language_use_uer_defined_set_apply('fra')

        def language_use_uer_defined_apply_ita(self):
            return self.language_use_uer_defined_set_apply('ita')

        def language_use_uer_defined_apply_nld(self):
            return self.language_use_uer_defined_set_apply('nld')

        def language_use_uer_defined_apply_chs(self):
            return self.language_use_uer_defined_set_apply('chs')

        def language_use_uer_defined_apply_cht(self):
            return self.language_use_uer_defined_set_apply('cht')

        def language_use_uer_defined_apply_jpn(self):
            return self.language_use_uer_defined_set_apply('jpn')

        def language_use_uer_defined_apply_kor(self):
            return self.language_use_uer_defined_set_apply('kor')

    class Editing(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def set_default_transition_behavior_apply_overlap(self):
            locator_combobox = L.preferences.editing.timeline.cbx_default_transition_behavior
            locator_option = L.preferences.editing.timeline.option_overlap
            return select_combobox_item(self, locator_combobox, locator_option)

        def set_default_transition_behavior_apply_cross(self):
            locator_combobox = L.preferences.editing.timeline.cbx_default_transition_behavior
            locator_option = L.preferences.editing.timeline.option_cross
            return select_combobox_item(self, locator_combobox, locator_option)

        def get_default_transition_behavior(self):
            locator_combobox = L.preferences.editing.timeline.cbx_default_transition_behavior
            return self.exist(locator_combobox).AXTitle

        def return_to_beginnings_of_video_after_preview_set_check(self, is_check=1):
            locator = L.preferences.editing.timeline.chx_return_to_beginning_of_video_after_preview
            return checkbox_set_check(self, locator, is_check)

        def reverse_timeline_track_order_set_check(self, is_check=1):
            locator = L.preferences.editing.timeline.chx_reverse_timeline_track_order
            return checkbox_set_check(self, locator, is_check)

        def durations_image_files_set_arrow_button(self, direction='up', times=1):
            locator = L.preferences.editing.duration.editbox_image_files_parent
            return set_arrow_button(self, locator, direction, times)

        def durations_image_files_get_value(self):
            locator_parent = L.preferences.editing.duration.editbox_image_files_parent
            locator = locator_parent.copy()
            locator.append(L.preferences.editbox_unit)
            return editbox_get_value(self, locator)

        def durations_image_files_set_value(self, value):
            locator_parent = L.preferences.editing.duration.editbox_image_files_parent
            locator = locator_parent.copy()
            locator.append(L.preferences.editbox_unit)
            return editbox_set_value(self, locator, value)

        def durations_transitions_set_arrow_button(self, direction='up', times=1):
            locator = L.preferences.editing.duration.editbox_transitions_parent
            return set_arrow_button(self, locator, direction, times)

        def durations_transitions_get_value(self):
            locator_parent = L.preferences.editing.duration.editbox_transitions_parent
            locator = locator_parent.copy()
            locator.append(L.preferences.editbox_unit)
            return editbox_get_value(self, locator)

        def durations_transitions_set_value(self, value):
            locator_parent = L.preferences.editing.duration.editbox_transitions_parent
            locator = locator_parent.copy()
            locator.append(L.preferences.editbox_unit)
            return editbox_set_value(self, locator, value)

        def durations_title_set_arrow_button(self, direction='up', times=1):
            locator = L.preferences.editing.duration.editbox_title_parent
            return set_arrow_button(self, locator, direction, times)

        def durations_title_get_value(self):
            locator_parent = L.preferences.editing.duration.editbox_title_parent
            locator = locator_parent.copy()
            locator.append(L.preferences.editbox_unit)
            return editbox_get_value(self, locator)

        @step('[Action][Preferences_Page] Set Title default Duration')
        def durations_title_set_value(self, value):
            locator_parent = L.preferences.editing.duration.editbox_title_parent
            locator = locator_parent.copy()
            locator.append(L.preferences.editbox_unit)
            return editbox_set_value(self, locator, value)

        def durations_effect_set_arrow_button(self, direction='up', times=1):
            locator = L.preferences.editing.duration.editbox_effect_parent
            return set_arrow_button(self, locator, direction, times)

        def durations_effect_get_value(self):
            locator_parent = L.preferences.editing.duration.editbox_effect_parent
            locator = locator_parent.copy()
            locator.append(L.preferences.editbox_unit)
            return editbox_get_value(self, locator)

        def durations_effect_set_value(self, value):
            locator_parent = L.preferences.editing.duration.editbox_effect_parent
            locator = locator_parent.copy()
            locator.append(L.preferences.editbox_unit)
            return editbox_set_value(self, locator, value)

        def durations_subtitle_set_arrow_button(self, direction='up', times=1):
            locator = L.preferences.editing.duration.editbox_subtitle_parent
            return set_arrow_button(self, locator, direction, times)

        def durations_subtitle_get_value(self):
            locator_parent = L.preferences.editing.duration.editbox_subtitle_parent
            locator = locator_parent.copy()
            locator.append(L.preferences.editbox_unit)
            return editbox_get_value(self, locator)

        @step('[Action][Preferences_Page] Set [Subtitle] default Duration to (value)')
        def durations_subtitle_set_value(self, value):
            locator_parent = L.preferences.editing.duration.editbox_subtitle_parent
            locator = locator_parent.copy()
            locator.append(L.preferences.editbox_unit)
            return editbox_set_value(self, locator, value)

        def transition_between_photos_get_checkbox_status(self):
            locator_checkbox = L.preferences.editing.timeline.chx_add_transition_between_photos
            return self.exist(locator_checkbox).AXValue

        def transition_between_photos_set_type(self, transition_type=None): # transition_type: None, cross_fade, my_favorite
            locator_checkbox = L.preferences.editing.timeline.chx_add_transition_between_photos
            el_chx = self.exist(locator_checkbox)
            if not transition_type:
                if el_chx.AXValue:
                    self.el_click(el_chx)
                return True
            if not el_chx.AXValue:
                self.el_click(el_chx)
            time.sleep(OPERATION_DELAY)
            locator_combobox = L.preferences.editing.timeline.cbx_transition_type
            locator_option = eval(f'L.preferences.editing.timeline.option_{transition_type}')
            return select_combobox_item(self, locator_combobox, locator_option)

        def set_default_insert_project_behavior_status(self, project_type): # project_type: nested, expanded
            if project_type == 'nested' or project_type == 'expanded':
                locator_combobox = L.preferences.editing.timeline.cbx_insert_project_behavior
                locator_option = eval(f'L.preferences.editing.timeline.option_{project_type}')
                return select_combobox_item(self, locator_combobox, locator_option)
            else:
                logger('Invalid parameter')
                return False

        def get_default_insert_project_behavior_status(self):
            locator_combobox = L.preferences.editing.timeline.cbx_insert_project_behavior
            return self.exist(locator_combobox).AXTitle

    class File(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def default_locations_import_folder_get_path(self):
            try:
                value = self.exist(L.preferences.file.default_locations.editbox_import_folder).AXValue
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return value

        def default_locations_import_folder_click_browse(self):
            try:
                # img_before = self.screenshot()
                self.exist_click(L.preferences.file.default_locations.btn_import_folder_browse)
                # self.wait_for_image_changes(img_before)
                time.sleep(OPERATION_DELAY)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def default_locations_import_folder_set_path(self, full_path):
            try:
                self.select_file(full_path)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def default_locations_export_folder_get_path(self):
            try:
                value = self.exist(L.preferences.file.default_locations.editbox_export_folder).AXValue
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return value

        def default_locations_export_folder_click_browse(self):
            try:
                # img_before = self.screenshot()
                self.exist_click(L.preferences.file.default_locations.btn_export_folder_browse)
                # self.wait_for_image_changes(img_before)
                time.sleep(OPERATION_DELAY)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def default_locations_export_folder_set_path(self, full_path, is_exist=1):
            try:
                if not is_exist and os.path.exists(full_path): # for new folder case, remove target folder first if exists
                    logger('remove exist folder first')
                    import shutil
                    shutil.rmtree(full_path)
                self.select_file(full_path)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def filename_snapshot_set_file_name(self, name):
            locator = L.preferences.file.file_name.editbox_snapshot_filename
            return editbox_set_value(self, locator, name)

        def filename_snapshot_get_file_name(self):
            try:
                value = self.exist(L.preferences.file.file_name.editbox_snapshot_filename).AXValue
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return value

        def filename_snapshot_set_file_format(self, file_ext='jpg'):
            locator_combobox = L.preferences.file.file_name.cbx_snapshot_filename_extension
            locator_option = eval(f'L.preferences.file.file_name.option_file_ext_{file_ext}')
            return select_combobox_item(self, locator_combobox, locator_option)

        def filename_snapshot_get_file_format(self):
            try:
                value = self.exist(L.preferences.file.file_name.cbx_snapshot_filename_extension).AXTitle
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return value

        def filename_snapshot_set_file_destination(self, dest='file'):
            locator_combobox = L.preferences.file.file_name.cbx_snapshot_destination
            locator_option = eval(f'L.preferences.file.file_name.option_snapshot_destination_{dest}')
            return select_combobox_item(self, locator_combobox, locator_option)

        def filename_snapshot_get_file_destination(self):
            try:
                value = self.exist(L.preferences.file.file_name.cbx_snapshot_destination).AXTitle
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return value


    class Display(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def timeline_preview_quality_set_value(self, quality): # quality: ultra_hd, full_hd, hd, high, normal, low
            locator_combobox = L.preferences.display.cbx_timeline_preview_quality
            locator_option = eval(f'L.preferences.display.option_timeline_preview_quality_{quality}')
            return select_combobox_item(self, locator_combobox, locator_option)

        def snap_to_reference_lines_set_check(self, is_check=1):
            try:
                el_chx = self.exist(L.preferences.display.chx_snap_to_reference_lines)
                if el_chx.AXValue != is_check:
                    self.el_click(el_chx)
                    time.sleep(OPERATION_DELAY * 0.5)
                    if is_check != self.exist(L.preferences.display.chx_snap_to_reference_lines).AXValue:
                        logger('Fail to verify after set check')
                        raise Exception
            except Exception:
                raise Exception
            return True

        def snap_to_reference_lines_checkbox_get_status(self):
            try:
                value = self.exist(L.preferences.display.chx_snap_to_reference_lines).AXValue
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return value

        def grid_lines_set_value(self, lines=0):
            try:
                if lines == 1:
                    logger('No match grid lines of 1x1')
                    raise Exception
                if lines == 0:
                    lines = 'None'
                else:
                    lines = f'{lines} x {lines}'
                locator_option = L.preferences.display.option_grid_lines_unit.copy()
                locator_option['AXValue'] = lines
                locator_combobox = L.preferences.display.cbx_grid_lines
                select_combobox_item(self, locator_combobox, locator_option)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def grid_lines_get_value(self):
            try:
                value = self.exist(L.preferences.display.cbx_grid_lines).AXTitle
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return value


    class Project(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        @step('[Action][Preferences_Page][Project] Set [Numbers of Recently Used Projects] to value')
        def numbers_of_recently_used_project_set_value(self, value):
            locator_parent = L.preferences.project.editbox_numbers_of_recently_used_projects_parent
            locator = locator_parent.copy()
            locator.append(L.preferences.editbox_unit)
            return editbox_set_value(self, locator, value)

        @step('[Action][Preferences_Page][Project] Get [Numbers of Recently Used Projects] value')
        def numbers_of_recently_used_project_get_value(self):
            locator_parent = L.preferences.project.editbox_numbers_of_recently_used_projects_parent
            locator = locator_parent.copy()
            locator.append(L.preferences.editbox_unit)
            return editbox_get_value(self, locator)

        def auto_load_the_last_project_set_check(self, is_check=1):
            try:
                el_chx = self.exist(L.preferences.project.chx_auto_load_the_last_project)
                if el_chx.AXValue != is_check:
                    self.el_click(el_chx)
                    time.sleep(OPERATION_DELAY * 0.5)
                    if is_check != self.exist(L.preferences.project.chx_auto_load_the_last_project).AXValue:
                        logger('Fail to verify after set check')
                        raise Exception
            except Exception:
                raise Exception
            return True

        def auto_load_the_last_project_checkbox_get_status(self):
            try:
                value = self.exist(L.preferences.project.chx_auto_load_the_last_project).AXValue
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return value

        def auto_load_sample_clips_set_check(self, is_check=1):
            try:
                el_chx = self.exist(L.preferences.project.chx_auto_load_sample_clips)
                if el_chx.AXValue != is_check:
                    self.el_click(el_chx)
                    time.sleep(OPERATION_DELAY * 0.5)
                    if is_check != self.exist(L.preferences.project.chx_auto_load_sample_clips).AXValue:
                        logger('Fail to verify after set check')
                        raise Exception
            except Exception:
                raise Exception
            return True

        def auto_load_sample_clips_checkbox_get_status(self):
            try:
                value = self.exist(L.preferences.project.chx_auto_load_sample_clips).AXValue
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return value


    class Confirmation(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def click_reset(self):
            try:
                self.exist_click(L.preferences.confirmation.btn_reset)
                time.sleep(OPERATION_DELAY * 0.5)
                self.exist_click(L.preferences.confirm_dialog.btn_ok)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True


    class DirectorZone(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def input_email(self, value):
            locator = L.preferences.director_zone.editbox_email
            return editbox_set_value(self, locator, value)

        def input_password(self, value):
            locator = L.preferences.director_zone.editbox_password
            return editbox_set_value(self, locator, value, 0)

        def get_email(self):
            locator = L.preferences.director_zone.editbox_email
            return editbox_get_value(self, locator)

        def get_password(self):
            locator = L.preferences.director_zone.editbox_password
            return editbox_get_value(self, locator)

        def auto_sign_in_set_check(self, is_check=1):
            try:
                el_chx = self.exist(L.preferences.director_zone.chx_auto_sign_in)
                if el_chx.AXValue != is_check:
                    self.el_click(el_chx)
                    time.sleep(OPERATION_DELAY * 0.5)
                    if is_check != self.exist(L.preferences.director_zone.chx_auto_sign_in).AXValue:
                        logger('Fail to verify after set check')
                        raise Exception
            except Exception:
                raise Exception
            return True

        def auto_sign_in_checkbox_get_status(self):
            try:
                value = self.exist(L.preferences.director_zone.chx_auto_sign_in).AXValue
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return value

        def click_sign_in(self, timeout=10):
            try:
                self.exist_click(L.preferences.director_zone.btn_sign_in)
                if not self.exist(L.preferences.director_zone.btn_sign_out, timeout):
                    logger('Fail to click sign in')
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def click_sign_out(self, timeout=10):
            try:
                self.exist_click(L.preferences.director_zone.btn_sign_out)
                if not self.exist(L.preferences.director_zone.btn_sign_in, timeout):
                    logger('Fail to click sign in')
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def click_upload_link(self):
            try:
                self.exist_click(L.preferences.director_zone.lnk_template_upload_to_dz)
                start_time = time.time()
                is_complete = 0
                while time.time() - start_time < 30:
                    title = self.check_chrome_page()
                    if 'DirectorZone' in title:
                        is_complete = 1
                        break
                if not is_complete:
                    logger('Fail to navigate to upload link')
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                return False
            return True

        def click_download_link(self):
            try:
                self.exist_click(L.preferences.director_zone.lnk_template_download_from_dz)
                start_time = time.time()
                is_complete = 0
                while time.time() - start_time < 30:
                    title = self.check_chrome_page()
                    if 'DirectorZone' in title:
                        is_complete = 1
                        break
                if not is_complete:
                    logger('Fail to navigate to upload link')
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                return False
            return True

    class CyberlinkCloud(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def click_browse(self):
            try:
                # img_before = self.screenshot()
                self.exist_click(L.preferences.cyberlink_cloud.btn_browse)
                # self.wait_for_image_changes(img_before, simularity=0.98)
                time.sleep(OPERATION_DELAY)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def download_folder_set_path(self, path):
            try:
                self.exist(L.preferences.cyberlink_cloud.editbox_download_folder).AXValue = path
                time.sleep(OPERATION_DELAY)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def download_folder_get_path(self):
            try:
                value = self.exist(L.preferences.cyberlink_cloud.editbox_download_folder).AXValue
                time.sleep(OPERATION_DELAY)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return value

        def download_folder_select_folder_by_browse(self, full_path):
            try:
                self.click_browse()
                time.sleep(OPERATION_DELAY * 0.5)
                self.select_file(full_path)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def click_account_info_link(self):
            try:
                self.exist_click(L.preferences.cyberlink_cloud.lnk_account_info)
                start_time = time.time()
                is_complete = 0
                while time.time() - start_time < 30:
                    title = self.check_chrome_page()
                    if 'CyberLink Cloud' in title:
                        is_complete = 1
                        break
                if not is_complete:
                    logger('Fail to navigate to upload link')
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                return False
            return True