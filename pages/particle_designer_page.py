import time, datetime, os, copy

from .base_page import BasePage
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
from AppKit import NSScreen
from .locator import locator as L
from .main_page import Main_Page
from reportportal_client import step

DELAY_TIME = 1 # sec

class Particle_Designer(Main_Page, BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.express_mode = self.Express_Mode(*args, **kwargs)

    def check_in_particle_designer(self):
        if not self.exist(L.particle_designer.designer_window):
            logger('not enter Particle Designer now')
            return False

        # Verify Step:
        if not self.exist(L.particle_designer.designer_window).AXTitle.startswith('Particle Designer |'):
            logger('Not enter Particle Designer now')
            return False
        else:
            return True

    def click_zoom_btn(self):
        try:
            if not self.exist_click(L.particle_designer.btn_zoom):
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_close_btn(self):
        try:
            if not self.exist_click(L.particle_designer.btn_close):
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_undo(self):
        try:
            if not self.exist_click(L.particle_designer.btn_undo):
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_redo(self):
        try:
            if not self.exist_click(L.particle_designer.btn_redo):
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_zoom_in(self, times=1):
        try:
            if not self.exist(L.particle_designer.btn_zoom_in):
                raise Exception
            for x in range(times):
                self.exist_click(L.particle_designer.btn_zoom_in)
                time.sleep(DELAY_TIME*0.5)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_zoom_out(self, times=1):
        try:
            if not self.exist(L.particle_designer.btn_zoom_out):
                raise Exception
            for x in range(times):
                self.exist_click(L.particle_designer.btn_zoom_out)
                time.sleep(DELAY_TIME*0.5)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_viewer_zoom_menu(self, value='Fit'):
        '''
        :param value: Fit, 10%, 25%, 50%, 75%, 100%, ...
        '''
        try:
            if not self.check_in_particle_designer():
                raise Exception
            self.exist_click(L.particle_designer.cbx_viewer_zoom)
            self.exist_click({'AXRole': 'AXStaticText', 'AXValue': value})
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def get_viewer_setting(self):
        try:
            if not self.exist(L.particle_designer.cbx_viewer_zoom):
                raise Exception
            else:
                return self.exist(L.particle_designer.cbx_viewer_zoom).AXTitle
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
    @step('[Action][Particle Designer] Get Particle Designer title')
    def get_particle_designer_title(self):
        try:
            if not self.exist(L.particle_designer.designer_window):
                logger('Not enter Particle Designer now')
                raise Exception('Not enter Particle Designer now')

            title = self.exist(L.particle_designer.designer_window).AXTitle
            return title[20:]
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
    
    @step('[Action][Particle Designer] Set Timecode')
    def set_timecode(self, timecode):
        self.activate()
        elem = self.find(L.particle_designer.timecode)
        w, h = elem.AXSize
        x, y = elem.AXPosition

        pos_click = tuple(map(int, (x + w * 0.1, y + h * 0.5)))
        self.mouse.click(*pos_click)
        time.sleep(1)
        self.keyboard.send(timecode.replace("_", ""))
        self.keyboard.enter()

    @step('[Action][Particle Designer] Get Timecode')
    def get_timecode(self):
        try:
            if not self.exist(L.particle_designer.designer_window):
                logger("No particle designer window show up")
                raise Exception("No particle designer window show up")
            timecode = self.exist(L.particle_designer.timecode).AXValue
            return timecode
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_preview_operation(self, strOperation):
        try:
            if not self.exist(L.particle_designer.designer_window):
                logger("No particle designer window show up")
                raise Exception
            if strOperation == 'Play':
                self.exist_click(L.particle_designer.preview_play)
            elif strOperation == 'Stop':
                self.exist_click(L.particle_designer.preview_stop)
            elif strOperation == 'Pause':
                self.exist_click(L.particle_designer.preview_pause)
            elif strOperation == 'Previous_Frame':
                self.exist_click(L.particle_designer.preview_previous_frame)
            elif strOperation == 'Next_Frame':
                self.exist_click(L.particle_designer.preview_next_frame)
            elif strOperation == 'Fast_Forward':
                self.exist_click(L.particle_designer.preview_fast_forward)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def drag_properties_scroll_bar(self, value):
        try:
            if not self.exist(L.particle_designer.designer_window):
                logger("No particle designer window show up")
                raise Exception
            self.exist(L.particle_designer.scroll_bar).AXValue = float(value)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Particle Designer] Click [OK] button to close Particle Designer window')
    def click_OK(self):
        try:
            if not self.exist(L.particle_designer.designer_window):
                logger("No particle designer window show up")
                raise Exception("No particle designer window show up")
            self.exist_click(L.particle_designer.btn_OK)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_Cancel(self):
        try:
            if not self.exist(L.particle_designer.designer_window):
                logger("No particle designer window show up")
                raise Exception
            self.exist_click(L.particle_designer.btn_Cancel)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_Share(self):
        try:
            if not self.exist(L.particle_designer.designer_window):
                logger("No particle designer window show up")
                raise Exception
            if not self.exist_click(L.particle_designer.btn_Share):
                logger('Cannot find Share button')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def share_to_cloud(self, name, tags, collection, description, verify_dz_link=0, only_dz=0):
        try:
            self.click_Share()
            self.input_template_name_and_click_ok(name)
            time.sleep(DELAY_TIME*2)
            if self.exist(L.pip_designer.auto_sign_in_to_DZ):
                self.exist_click(L.pip_designer.log_in_yes)
                time.sleep(DELAY_TIME * 2)

            self.exist_click(L.pip_designer.upload.upload_to_box)
            self.exist_click(L.pip_designer.upload.cloud_and_dz)
            if only_dz:
                self.exist_click(L.pip_designer.upload.dz)
            else:
                self.exist_click(L.pip_designer.upload.cloud_and_dz)
            time.sleep(DELAY_TIME * 2)
            self.click(L.pip_designer.upload.tags)
            self.keyboard.send(tags)
            time.sleep(DELAY_TIME * 2)
            self.exist_click(L.pip_designer.upload.collection)
            self.keyboard.send(collection)
            time.sleep(DELAY_TIME * 2)
            self.exist_click(L.pip_designer.upload.description)
            self.keyboard.send(description)
            self.exist_click(L.pip_designer.upload.next_btn)

            if self.exist(L.pip_designer.upload.confirm_disclaimer, timeout=6):
                self.exist_click(L.pip_designer.upload.confirm_disclaimer)
                self.exist_click(L.pip_designer.upload.next_btn)

            for x in range(200):
                if not self.exist(L.pip_designer.upload.finish):
                    time.sleep(DELAY_TIME)
                elif self.exist(L.pip_designer.upload.finish).AXEnabled == False:
                    time.sleep(DELAY_TIME)
                else:
                    time.sleep(DELAY_TIME)
                    if verify_dz_link:
                        logger('run 248')
                        self.click(L.upload_cloud_dz.upload_view_DZ)
                        time.sleep(DELAY_TIME*3)
                        self.activate()
                        time.sleep(DELAY_TIME*6)
                    break
            self.click(L.pip_designer.upload.finish)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_cancel_yes(self):
        try:
            if not self.exist(L.particle_designer.designer_window):
                logger("No particle designer window show up")
                raise Exception
            self.exist_click(L.particle_designer.btn_Cancel)

            if not self.exist(L.particle_designer.alert_dialog.message):
                raise Exception
            self.exist_click(L.particle_designer.alert_dialog.btn_Yes)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_cancel_no(self):
        try:
            if not self.exist(L.particle_designer.designer_window):
                logger("No particle designer window show up")
                raise Exception
            self.exist_click(L.particle_designer.btn_Cancel)

            if not self.exist(L.particle_designer.alert_dialog.message):
                raise Exception
            self.exist_click(L.particle_designer.alert_dialog.btn_No)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_cancel_cancel(self):
        try:
            if not self.exist(L.particle_designer.designer_window):
                logger("No particle designer window show up")
                raise Exception
            self.exist_click(L.particle_designer.btn_Cancel)

            if not self.exist(L.particle_designer.alert_dialog.message):
                raise Exception
            self.exist_click(L.particle_designer.alert_dialog.btn_Cancel)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def input_template_name_and_click_ok(self, strName):
        try:
            if not self.exist(L.particle_designer.designer_window):
                logger("No particle designer window show up")
                raise Exception
            if not self.exist(L.particle_designer.save_as_template_dialog.main):
                logger("No Save as dialog show up")
                raise Exception

            self.exist_click(L.particle_designer.save_as_template_dialog.save_as_textfield)
            self.keyboard.send(strName)
            self.exist_click(L.particle_designer.save_as_template_dialog.btn_OK)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True
    
    @step('[Action][Particle Designer] Save as template')
    def save_as_name(self, name):
        # Click (Save as) button > Input custom name w/ name
        try:
            if not self.exist(L.particle_designer.designer_window):
                logger("No particle designer window show up")
                raise Exception("No particle designer window show up")
            self.exist_click(L.particle_designer.btn_SaveAs)
            if not self.exist(L.particle_designer.save_as_template_dialog.main):
                logger("No Save as dialog show up")
                raise Exception("No Save as dialog show up")

            self.exist_click(L.particle_designer.save_as_template_dialog.save_as_textfield)
            self.keyboard.send(name)
            time.sleep(DELAY_TIME)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def save_as_get_custom_name(self):
        try:
            if not self.exist(L.particle_designer.save_as_template_dialog.save_as_textfield):
                logger('Not find custom name textfield')
                raise Exception
            custom_name = self.exist(L.particle_designer.save_as_template_dialog.save_as_textfield).AXValue
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return custom_name

    def save_as_set_slider(self, value):
        try:
            if not self.exist(L.particle_designer.save_as_template_dialog.slider):
                logger('Not find Save As slider')
                raise Exception
            self.exist(L.particle_designer.save_as_template_dialog.slider).AXValue = value
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def save_as_get_slider_value(self):
        try:
            if not self.exist(L.particle_designer.save_as_template_dialog.slider):
                logger('Not find Save As slider')
                raise Exception
            current_value = self.exist(L.particle_designer.save_as_template_dialog.slider).AXValue
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return current_value

    def save_as_cancel(self):
        try:
            if not self.exist_click(L.particle_designer.save_as_template_dialog.btn_Cancel):
                logger('Not find Save As Cancel')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Particle Designer] Save as OK')
    def save_as_ok(self):
        try:
            if not self.exist_click(L.particle_designer.save_as_template_dialog.btn_OK):
                logger('Not find Save As OK')
                raise Exception('Not find Save As OK')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def press_hotkey_enter_designer(self):
        # Step0: Clip is in timeline > Click [More Features] buttonPress
        # Step1: Press hotkey F2 to enter designer
        try:
            time.sleep(DELAY_TIME)
            with self.keyboard.pressed(self.keyboard.key.f2):
                pass
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    class Express_Mode(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        @step('[Action][Express Mode][Particle Designer] Click [Emit] slider')
        def drag_Emit_slider(self, value):
            try:
                if value < 0:
                    logger('Detect Invalid parameter !!!')
                    raise Exception(f'Detect Invalid parameter {value}!!! Should be greater than 0')
                elif value > 200000:
                    logger('Detect Invalid parameter !!!')
                    raise Exception(f'Detect Invalid parameter {value}!!! Should be less than 200000')

                if not self.exist(L.particle_designer.designer_window):
                    logger("No particle designer window show up")
                    raise Exception("No particle designer window show up")
                if self.exist(L.particle_designer.modify_parameters).AXValue == 0:
                    self.exist_click(L.particle_designer.modify_parameters)
                self.exist(L.particle_designer.emit_rate.slider).AXValue = float(value)
                time.sleep(DELAY_TIME)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True
        
        @step('[Action][Express Mode][Particle Designer] Get [Emit] value')
        def get_Emit_value(self):
            try:
                if not self.exist(L.particle_designer.designer_window):
                    logger("No particle designer window show up")
                    raise Exception("No particle designer window show up")

                if not self.exist(L.particle_designer.emit_rate.slider):
                    raise Exception("No [Emit] slider show up")
                value = self.exist(L.particle_designer.emit_rate.slider).AXValue
                return value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')

        @step('[Action][Express Mode][Particle Designer] Click [Emit] plus button')
        def click_Emit_plus_btn(self, times=1):
            try:
                if not self.exist(L.particle_designer.designer_window):
                    logger("No particle designer window show up")
                    raise Exception("No particle designer window show up")
                if not self.exist(L.particle_designer.emit_rate.btn_plus):
                    raise Exception("No [Emit] plus button show up")
                new_x, new_y = self.exist(L.particle_designer.emit_rate.btn_plus).AXPosition
                new_x = new_x + 30
                new_y = new_y + 20

                for x in range(times):
                    self.exist_click(L.particle_designer.emit_rate.btn_plus)
                    self.mouse.move(new_x, new_y)
                    time.sleep(DELAY_TIME*0.5)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')

        @step('[Action][Express Mode][Particle Designer] Click [Emit] minus button')
        def click_Emit_minus_btn(self, times=1):
            try:
                if not self.exist(L.particle_designer.designer_window):
                    logger("No particle designer window show up")
                    raise Exception("No particle designer window show up")
                if not self.exist(L.particle_designer.emit_rate.btn_minus):
                    raise Exception("No [Emit] minus button show up")
                new_x, new_y = self.exist(L.particle_designer.emit_rate.btn_minus).AXPosition
                new_x = new_x + 30
                new_y = new_y + 20

                for x in range(times):
                    self.exist_click(L.particle_designer.emit_rate.btn_minus)
                    self.mouse.move(new_x, new_y)
                    time.sleep(DELAY_TIME*0.5)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')

        @step('[Action][Express Mode][Particle Designer] Drag [Max] slider')
        def drag_Max_slider(self, value):
            try:
                if value < 0:
                    logger('Detect Invalid parameter !!!')
                    raise Exception(f'Detect Invalid parameter {value}!!! Should be greater than 0')
                elif value > 200000:
                    logger('Detect Invalid parameter !!!')
                    raise Exception(f'Detect Invalid parameter {value}!!! Should be less than 200000')

                if not self.exist(L.particle_designer.designer_window):
                    logger("No particle designer window show up")
                    raise Exception(f'Exception occurs. log={e}')
                # if Express Mode : (Modify Parameters) tab status = fold, auto unfold
                if self.exist(L.particle_designer.modify_parameters).AXValue == 0:
                    self.exist_click(L.particle_designer.modify_parameters)

                self.exist(L.particle_designer.max_count.slider).AXValue = float(value)
                time.sleep(DELAY_TIME)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][Express Mode][Particle Designer] Get [Max] value')
        def get_Max_value(self):
            try:
                if not self.exist(L.particle_designer.designer_window):
                    logger("No particle designer window show up")
                    raise Exception("No particle designer window show up")

                if not self.exist(L.particle_designer.max_count.slider):
                    raise Exception("No [Max] slider show up")
                value = self.exist(L.particle_designer.max_count.slider).AXValue
                return value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')

        @step('[Action][Express Mode][Particle Designer] Click [Max] plus button')
        def click_Max_plus_btn(self, times=1):
            try:
                if not self.exist(L.particle_designer.designer_window):
                    logger("No particle designer window show up")
                    raise Exception("No particle designer window show up")
                if not self.exist(L.particle_designer.max_count.btn_plus):
                    raise Exception("No [Max] plus button show up")
                new_x, new_y = self.exist(L.particle_designer.max_count.btn_plus).AXPosition
                new_x = new_x + 30
                new_y = new_y + 20

                for x in range(times):
                    self.exist_click(L.particle_designer.max_count.btn_plus)
                    self.mouse.move(new_x, new_y)
                    time.sleep(DELAY_TIME*0.5)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')

        @step('[Action][Express Mode][Particle Designer] Click [Max] minus button')
        def click_Max_minus_btn(self, times=1):
            try:
                if not self.exist(L.particle_designer.designer_window):
                    logger("No particle designer window show up")
                    raise Exception("No particle designer window show up")
                if not self.exist(L.particle_designer.max_count.btn_minus):
                    raise Exception("No [Max] minus button show up")
                new_x, new_y = self.exist(L.particle_designer.max_count.btn_minus).AXPosition
                new_x = new_x + 30
                new_y = new_y + 20

                for x in range(times):
                    self.exist_click(L.particle_designer.max_count.btn_minus)
                    self.mouse.move(new_x, new_y)
                    time.sleep(DELAY_TIME*0.5)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')

        @step('[Action][Express Mode][Particle Designer] Drag [Life] slider')
        def drag_Life_slider(self, value):
            try:
                if value < 0:
                    logger('Detect Invalid parameter !!!')
                    raise Exception(f'Detect Invalid parameter {value}!!! Should be greater than 0')
                elif value > 200000:
                    logger('Detect Invalid parameter !!!')
                    raise Exception(f'Detect Invalid parameter {value}!!! Should be less than 200000')

                if not self.exist(L.particle_designer.designer_window):
                    logger("No particle designer window show up")
                    raise Exception("No particle designer window show up")
                # if Express Mode : (Modify Parameters) tab status = fold, auto unfold
                if self.exist(L.particle_designer.modify_parameters).AXValue == 0:
                    self.exist_click(L.particle_designer.modify_parameters)

                self.exist(L.particle_designer.life.slider).AXValue = float(value)
                time.sleep(DELAY_TIME)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][Express Mode][Particle Designer] Get [Life] value')
        def get_Life_value(self):
            try:
                if not self.exist(L.particle_designer.designer_window):
                    logger("No particle designer window show up")
                    raise Exception("No particle designer window show up")

                if not self.exist(L.particle_designer.life.slider):
                    raise Exception("No [Life] slider show up")
                value = self.exist(L.particle_designer.life.slider).AXValue
                return value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')

        @step('[Action][Express Mode][Particle Designer] Click [Life] plus button')
        def click_Life_plus_btn(self, times=1):
            try:
                if not self.exist(L.particle_designer.designer_window):
                    logger("No particle designer window show up")
                    raise Exception("No particle designer window show up")
                if not self.exist(L.particle_designer.life.btn_plus):
                    raise Exception("No [Life] plus button show up")
                new_x, new_y = self.exist(L.particle_designer.life.btn_plus).AXPosition
                new_x = new_x + 30
                new_y = new_y + 20

                for x in range(times):
                    self.exist_click(L.particle_designer.life.btn_plus)
                    self.mouse.move(new_x, new_y)
                    time.sleep(DELAY_TIME*0.5)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')

        @step('[Action][Express Mode][Particle Designer] Click [Life] minus button')
        def click_Life_minus_btn(self, times=1):
            try:
                if not self.exist(L.particle_designer.designer_window):
                    logger("No particle designer window show up")
                    raise Exception("No particle designer window show up")
                if not self.exist(L.particle_designer.life.btn_minus):
                    raise Exception("No [Life] minus button show up")
                new_x, new_y = self.exist(L.particle_designer.life.btn_minus).AXPosition
                new_x = new_x + 30
                new_y = new_y + 20

                for x in range(times):
                    self.exist_click(L.particle_designer.life.btn_minus)
                    self.mouse.move(new_x, new_y)
                    time.sleep(DELAY_TIME*0.5)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')

        @step('[Action][Express Mode][Particle Designer] Drag [Speed] slider')
        def drag_Size_slider(self, value):
            try:
                if value < 0:
                    logger('Detect Invalid parameter !!!')
                    raise Exception(f'Detect Invalid parameter {value}!!! Should be greater than 0')
                elif value > 200000:
                    logger('Detect Invalid parameter !!!')
                    raise Exception(f'Detect Invalid parameter {value}!!! Should be less than 200000')

                if not self.exist(L.particle_designer.designer_window):
                    logger("No particle designer window show up")
                    raise Exception("No particle designer window show up")
                # if Express Mode : (Modify Parameters) tab status = fold, auto unfold
                if self.exist(L.particle_designer.modify_parameters).AXValue == 0:
                    self.exist_click(L.particle_designer.modify_parameters)

                self.exist(L.particle_designer.size.slider).AXValue = float(value)
                time.sleep(DELAY_TIME)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][Express Mode][Particle Designer] Get [Size] value')
        def get_Size_value(self):
            try:
                if not self.exist(L.particle_designer.designer_window):
                    logger("No particle designer window show up")
                    raise Exception("No particle designer window show up")

                if not self.exist(L.particle_designer.size.slider):
                    raise Exception("No [Size] slider show up")
                value = self.exist(L.particle_designer.size.slider).AXValue
                return value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')

        @step('[Action][Express Mode][Particle Designer] Click [Size] plus button')
        def click_Size_plus_btn(self, times=1):
            try:
                if not self.exist(L.particle_designer.designer_window):
                    logger("No particle designer window show up")
                    raise Exception("No particle designer window show up")
                if not self.exist(L.particle_designer.size.btn_plus):
                    raise Exception("No [Size] plus button show up")
                new_x, new_y = self.exist(L.particle_designer.size.btn_plus).AXPosition
                new_x = new_x + 30
                new_y = new_y + 20

                for x in range(times):
                    self.exist_click(L.particle_designer.size.btn_plus)
                    self.mouse.move(new_x, new_y)
                    time.sleep(DELAY_TIME*0.5)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')

        @step('[Action][Express Mode][Particle Designer] Click [Size] minus button')
        def click_Size_minus_btn(self, times=1):
            try:
                if not self.exist(L.particle_designer.designer_window):
                    logger("No particle designer window show up")
                    raise Exception("No particle designer window show up")
                if not self.exist(L.particle_designer.size.btn_minus):
                    raise Exception("No [Size] minus button show up")
                new_x, new_y = self.exist(L.particle_designer.size.btn_minus).AXPosition
                new_x = new_x + 30
                new_y = new_y + 20

                for x in range(times):
                    self.exist_click(L.particle_designer.size.btn_minus)
                    self.mouse.move(new_x, new_y)
                    time.sleep(DELAY_TIME*0.5)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')

        @step('[Action][Express Mode][Particle Designer] Drag [Speed] slider')
        def drag_Speed_slider(self, value):
            try:
                if value < 0:
                    logger('Detect Invalid parameter !!!')
                    raise Exception(f'Detect Invalid parameter {value}!!! Should be greater than 0')
                elif value > 200000:
                    logger('Detect Invalid parameter !!!')
                    raise Exception(f'Detect Invalid parameter {value}!!! Should be less than 200000')

                if not self.exist(L.particle_designer.designer_window):
                    logger("No particle designer window show up")
                    raise Exception("No particle designer window show up")
                # if Express Mode : (Modify Parameters) tab status = fold, auto unfold
                if self.exist(L.particle_designer.modify_parameters).AXValue == 0:
                    self.exist_click(L.particle_designer.modify_parameters)

                self.exist(L.particle_designer.speed.slider).AXValue = float(value)
                time.sleep(DELAY_TIME)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][Express Mode][Particle Designer] Get [Speed] value')
        def get_Speed_value(self):
            try:
                if not self.exist(L.particle_designer.designer_window):
                    logger("No particle designer window show up")
                    raise Exception("No particle designer window show up")

                if not self.exist(L.particle_designer.speed.slider):
                    raise Exception("No [Speed] slider show up")
                value = self.exist(L.particle_designer.speed.slider).AXValue
                return value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')

        @step('[Action][Express Mode][Particle Designer] Click [Speed] plus button')
        def click_Speed_plus_btn(self, times=1):
            try:
                if not self.exist(L.particle_designer.designer_window):
                    logger("No particle designer window show up")
                    raise Exception("No particle designer window show up")
                if not self.exist(L.particle_designer.speed.btn_plus):
                    raise Exception("No [Speed] plus button show up")
                new_x, new_y = self.exist(L.particle_designer.speed.btn_plus).AXPosition
                new_x = new_x + 30
                new_y = new_y + 20

                for x in range(times):
                    self.exist_click(L.particle_designer.speed.btn_plus)
                    self.mouse.move(new_x, new_y)
                    time.sleep(DELAY_TIME*0.5)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')

        @step('[Action][Express Mode][Particle Designer] Click [Speed] minus button')
        def click_Speed_minus_btn(self, times=1):
            try:
                if not self.exist(L.particle_designer.designer_window):
                    logger("No particle designer window show up")
                    raise Exception("No particle designer window show up")
                if not self.exist(L.particle_designer.speed.btn_minus):
                    raise Exception("No [Speed] minus button show up")
                new_x, new_y = self.exist(L.particle_designer.speed.btn_minus).AXPosition
                new_x = new_x + 30
                new_y = new_y + 20

                for x in range(times):
                    self.exist_click(L.particle_designer.speed.btn_minus)
                    self.mouse.move(new_x, new_y)
                    time.sleep(DELAY_TIME*0.5)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')

        @step('[Action][Express Mode][Particle Designer] Drag [Gravity] slider')
        def drag_Opacity_slider(self, value):
            try:
                if value < 0:
                    logger('Detect Invalid parameter !!!')
                    raise Exception(f'Detect Invalid parameter {value}!!! Should be greater than 0')
                elif value > 200000:
                    logger('Detect Invalid parameter !!!')
                    raise Exception(f'Detect Invalid parameter {value}!!! Should be less than 200000')

                if not self.exist(L.particle_designer.designer_window):
                    logger("No particle designer window show up")
                    raise Exception("No particle designer window show up")
                # if Express Mode : (Modify Parameters) tab status = fold, auto unfold
                if self.exist(L.particle_designer.modify_parameters).AXValue == 0:
                    self.exist_click(L.particle_designer.modify_parameters)

                self.exist(L.particle_designer.opacity.slider).AXValue = float(value)
                time.sleep(DELAY_TIME)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        @step('[Action][Express Mode][Particle Designer] Get [Opacity] value')
        def get_Opacity_value(self):
            try:
                if not self.exist(L.particle_designer.designer_window):
                    logger("No particle designer window show up")
                    raise Exception("No particle designer window show up")

                if not self.exist(L.particle_designer.opacity.slider):
                    raise Exception("No [Opacity] slider show up")
                value = self.exist(L.particle_designer.opacity.slider).AXValue
                return value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')

        @step('[Action][Express Mode][Particle Designer] Click [Opacity] plus button')
        def click_Opacity_plus_btn(self, times=1):
            try:
                if not self.exist(L.particle_designer.designer_window):
                    logger("No particle designer window show up")
                    raise Exception("No particle designer window show up")
                if not self.exist(L.particle_designer.opacity.btn_plus):
                    raise Exception("No [Opacity] plus button show up")
                new_x, new_y = self.exist(L.particle_designer.opacity.btn_plus).AXPosition
                new_x = new_x + 30
                new_y = new_y + 20

                for x in range(times):
                    self.exist_click(L.particle_designer.opacity.btn_plus)
                    self.mouse.move(new_x, new_y)
                    time.sleep(DELAY_TIME*0.5)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')

        @step('[Action][Express Mode][Particle Designer] Click [Opacity] minus button')
        def click_Opacity_minus_btn(self, times=1):
            try:
                if not self.exist(L.particle_designer.designer_window):
                    logger("No particle designer window show up")
                    raise Exception("No particle designer window show up")
                if not self.exist(L.particle_designer.opacity.btn_minus):
                    raise Exception("No [Opacity] minus button show up")
                new_x, new_y = self.exist(L.particle_designer.opacity.btn_minus).AXPosition
                new_x = new_x + 30
                new_y = new_y + 20

                for x in range(times):
                    self.exist_click(L.particle_designer.opacity.btn_minus)
                    self.mouse.move(new_x, new_y)
                    time.sleep(DELAY_TIME*0.5)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
