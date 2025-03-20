import time, datetime, os, copy

from .base_page import BasePage
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
# from AppKit import NSScreen
from .locator import locator as L
#from .locator.hardcode_0408 import locator as L
from .main_page import Main_Page
from reportportal_client import step

DELAY_TIME = 1 # sec

class Audio_Mixing_Room(Main_Page, BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_audio_volume(self, audio_no, value):
        try:
            if self.exist([{'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': audio_no}, {'AXIdentifier': 'IDC_AUDIOMIXINGROOM_SLIDER_VOLUMN'}]).AXEnabled == False:
                logger("target audio track can't set the volume")
                raise Exception
            self.exist([{'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': audio_no}, {'AXRole': 'AXValueIndicator', 'AXRoleDescription': 'value indicator'}]).AXValue = int(value)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def hover_audio_gain(self, audio_no):
        try:
            if self.exist([{'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': audio_no}, {'AXIdentifier': 'IDC_AUDIOMIXINGROOM_SLIDER_VOLUMN'}]).AXEnabled == False:
                logger("target audio track can't set the volume")
                raise Exception
            audio_gain = self.find([{'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': audio_no},{'AXIdentifier': 'IDC_AUDIOMIXER_SLIDER_GAINVIDEO', 'AXRoleDescription': 'slider'},
                                     {'AXRole': 'AXValueIndicator', 'AXRoleDescription': 'value indicator'}])
            self.mouse.move(*audio_gain.center)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Audio_Mixing_Room] Set [Audio Gain] value on (audio_no) to (value)')
    def set_audio_gain(self, audio_no, value):
        try:
            audio_no = audio_no - 1
            if self.exist([{'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': audio_no}, {'AXIdentifier': 'IDC_AUDIOMIXINGROOM_SLIDER_VOLUMN'}]).AXEnabled == False:
                logger("target audio track can't set the volume")
                raise Exception("target audio track can't set the volume")
            self.exist([{'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': audio_no},{'AXIdentifier': 'IDC_AUDIOMIXER_SLIDER_GAINVIDEO', 'AXRoleDescription': 'slider'},{'AXRole': 'AXValueIndicator', 'AXRoleDescription': 'value indicator'}]).AXValue = int(value)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Audio_Mixing_Room] Get [Audio Gain] value on (audio_no)')
    def get_audio_gain(self, audio_no):
        try:
            audio_no = audio_no - 1
            if self.exist([{'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': audio_no}, {'AXIdentifier': 'IDC_AUDIOMIXINGROOM_SLIDER_VOLUMN'}]).AXEnabled == False:
                logger("target audio track : Gray out now")
                raise Exception("target audio track : Gray out now")
            current_gain_value = self.exist([{'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': audio_no},{'AXIdentifier': 'IDC_AUDIOMIXER_SLIDER_GAINVIDEO', 'AXRoleDescription': 'slider'},{'AXRole': 'AXValueIndicator', 'AXRoleDescription': 'value indicator'}]).AXValue

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return current_gain_value

    @step('[Action][Audio_Mixing_Room] Click [Keyframe Control] on track (audio_no)')
    def click_keyframe_control(self, audio_no):
        try:
            audio_no = audio_no - 1
            if self.exist([{'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': audio_no},
                           {'AXIdentifier': 'IDC_AUDIOMIXINGROOM_SLIDER_VOLUMN'}]).AXEnabled == False:
                logger("target audio track can't set the volume")
                raise Exception("target audio track can't set the volume")
            self.exist_click([{'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': audio_no}, {'AXIdentifier': 'IDC_AUDIOMIXER_ADDREMOVE_VOLUMEKEYFRAME', 'AXRole': 'AXButton'}])
            time.sleep(DELAY_TIME)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Audio_Mixing_Room] Click [Previous Keyframe] on track (audio_no)')
    def click_previous_keyframe(self, audio_no):
        try:
            audio_no = audio_no - 1
            if self.exist([{'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': audio_no},
                           {'AXIdentifier': 'IDC_AUDIOMIXINGROOM_SLIDER_VOLUMN'}]).AXEnabled == False:
                logger("target audio track can't set the volume")
                raise Exception("target audio track can't set the volume")
            self.exist_click([{'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': audio_no}, {'AXIdentifier': 'IDC_AUDIOMIXER_PRE_VOLUMEKEYFRAME', 'AXRole': 'AXButton'}])

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Audio_Mixing_Room] Click [Next Keyframe] on track (audio_no)')
    def click_next_keyframe(self, audio_no):
        try:
            audio_no = audio_no - 1
            if self.exist([{'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': audio_no},
                           {'AXIdentifier': 'IDC_AUDIOMIXINGROOM_SLIDER_VOLUMN'}]).AXEnabled == False:
                logger("target audio track can't set the volume")
                raise Exception("target audio track can't set the volume")
            self.exist_click([{'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': audio_no}, {'AXIdentifier': 'IDC_AUDIOMIXER_NEXT_VOLUMEKEYFRAME', 'AXRole': 'AXButton'}])

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    @step('[Action][Audio_Mixing_Room] Click [Fade In] on (audio_no)')
    def click_fade_in(self, audio_no):
        try:
            audio_no = audio_no - 1
            if self.exist([{'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': audio_no},
                           {'AXIdentifier': 'IDC_AUDIOMIXINGROOM_SLIDER_VOLUMN'}]).AXEnabled == False:
                logger("target audio track can't set the volume")
                raise Exception("target audio track can't set the volume")
            self.exist_click([{'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': audio_no}, {'AXIdentifier': 'IDC_AUDIOMIXER_BUTTONVIDEOFADIN', 'AXRole': 'AXButton'}])

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_fade_out(self, audio_no):
        try:
            audio_no = audio_no - 1
            if self.exist([{'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': audio_no},
                           {'AXIdentifier': 'IDC_AUDIOMIXINGROOM_SLIDER_VOLUMN'}]).AXEnabled == False:
                logger("target audio track can't set the volume")
                raise Exception
            self.exist_click([{'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': audio_no}, {'AXIdentifier': 'IDC_AUDIOMIXER_BUTTONVIDEOFADOUT', 'AXRole': 'AXButton'}])

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Audio_Mixing_Room] Click [Normalize] on track (audio_no)')
    def click_normalize(self, audio_no):
        try:
            audio_no = audio_no - 1
            if self.exist([{'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': audio_no},
                           {'AXIdentifier': 'IDC_AUDIOMIXINGROOM_SLIDER_VOLUMN'}]).AXEnabled == False:
                logger("target audio track can't set the volume")
                raise Exception("target audio track can't set the volume")
            self.click([{'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': audio_no},
                              {'AXIdentifier': 'IDC_AUDIOMIXER_BUTTONNORMALIZE', 'AXRole': 'AXButton'}])

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def get_volume_db_value(self, audio_no):
        try:
            if self.exist([{'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': audio_no},
                           {'AXIdentifier': 'IDC_AUDIOMIXINGROOM_SLIDER_VOLUMN'}]).AXEnabled == False:
                logger("target audio track can't set the volume")
                raise Exception
            value = self.exist([{'AXIdentifier': 'AudioMixingCollectionViewItem', 'index': audio_no},
                                {'AXIdentifier': 'IDC_AUDIOMIXER_EDIT_VIDEO', 'AXRole': 'AXTextField'}]).AXValue
            return value

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True


