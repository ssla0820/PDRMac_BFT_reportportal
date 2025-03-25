import time, datetime, os, copy

from .base_page import BasePage
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
from .locator import locator as L
from .main_page import Main_Page
from reportportal_client import step

DELAY_TIME = 1  # sec


class Tips_area(Main_Page, BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tools = self.Tools(*args, **kwargs)
        self.more_features = self.MoreFeatures(*args, **kwargs)

    class Tools(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def click_btn(self):
            # Click TipsArea [Tools] button
            try:
                if not self.exist_click(L.tips_area.button.btn_Tools):
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        @step('[Action][Tip Areas][Tools] Select [Pip Designer] from [Tools]')
        def select_PiP_Designer(self):
            # Description : Click TipsArea [Tools] button > Select (PiP Designer)
            try:
                # Click TipsArea [Tools] button
                if not self.exist_click(L.tips_area.button.btn_Tools):
                    raise Exception('Fail to click [Tools] button')

                self.select_right_click_menu('PiP Designer')

                # Verify Step
                if not self.exist(L.pip_room.pip_designer.properties_tab):
                    logger('Not enter Pip Designer, verify Fail')
                    return False
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')
            return True

        def select_Mask_Designer(self):
            # Description : Click TipsArea [Tools] button > Select (Mask Designer)
            try:
                # Click TipsArea [Tools] button
                if not self.exist_click(L.tips_area.button.btn_Tools):
                    raise Exception

                # Select (Mask Designer)
                self.select_right_click_menu('Mask Designer')

                # Verify Step
                if not self.exist(L.mask_designer.tab.mask):
                    logger('Not enter Mask Designer, verify Fail')
                    return False
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def select_Shape_Designer(self):
            # Description : Click TipsArea [Tools] button > Select (Shape Designer)
            try:
                # Click TipsArea [Tools] button
                if not self.exist_click(L.tips_area.button.btn_Tools):
                    raise Exception

                # Select (Mask Designer)
                self.select_right_click_menu('Shape Designer')

                # Verify Step
                if not self.exist(L.pip_designer.cancel_button):
                    logger('Not enter Shape Designer, verify Fail')
                    return False
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def select_Blending_Mode(self):
            # Description : Click TipsArea [Tools] button > Select (Blending Mode)
            try:
                # Click TipsArea [Tools] button
                if not self.exist_click(L.tips_area.button.btn_Tools):
                    raise Exception

                # Select (Blending Mode)
                self.select_right_click_menu('Blending Mode')

                # Verify Step
                if not self.exist(L.tips_area.window.blending_mode):
                    logger('Not enter Blending Mode, verify Fail')
                    return False
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def select_Pan_Zoom(self, close_win=False):
            # Description : Click TipsArea [Tools] button > Select (Pan & Zoom)
            try:
                # Click TipsArea [Tools] button
                if not self.exist_click(L.tips_area.button.btn_Tools):
                    raise Exception

                # Select (Pan & Zoom)
                self.select_right_click_menu('Pan / Zoom')

                # Verify Step
                if not self.exist(L.tips_area.pan_zoom.tab):
                    logger('Not enter Pan / Zoom, verify Fail')
                    return False

                if close_win:
                    self.exist_click(L.tips_area.pan_zoom.close)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def select_CropZoomPan(self):
            # Description : Click TipsArea [Tools] button > Select (Crop/Zoom/Pan)
            try:
                # Click TipsArea [Tools] button
                if not self.exist_click(L.tips_area.button.btn_Tools):
                    raise Exception

                # Select (Crop/Zoom/Pan)
                self.select_right_click_menu('Crop / Rotate')

                if self.exist(L.tips_area.warning_dialog.msg1):
                    self.exist_click(L.tips_area.warning_dialog.ok)

                # Verify Step
                if not self.exist(L.tips_area.window.crop_zoom_pan):
                    logger('Not enter Crop/Zoom/Pan, verify Fail')
                    return False
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def select_VideoSpeed(self):
            # Description : Click TipsArea [Tools] button > Select (Video Speed)
            try:
                # Click TipsArea [Tools] button
                if not self.exist_click(L.tips_area.button.btn_Tools):
                    raise Exception

                # Select (Video Speed)
                self.select_right_click_menu('Video Speed')

                # Verify Step
                if not self.exist(L.video_speed.tab.entire_clip):
                    logger('Not enter Video Speed, verify Fail')
                    return False
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def select_smart_fit_duration(self):
            # Description : Click TipsArea [Tools] button > Select (Smart Fit for Duration)
            try:
                # Click TipsArea [Tools] button
                if not self.exist_click(L.tips_area.button.btn_Tools):
                    raise Exception

                # Select (Video Speed)
                self.select_right_click_menu('Smart Fit for Duration')

                # Verify Step
                if not self.exist(L.audio_editing.smart_fit.main_window):
                    logger('Not enter Smart Fit, verify Fail')
                    return False
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def select_Video_in_Reverse(self, skip=0):
            # Description : Click TipsArea [Tools] button > Select (Video in Reverse)
            try:
                img_before = self.snapshot(L.main.timeline.table_view)

                # Click TipsArea [Tools] button
                if not self.exist_click(L.tips_area.button.btn_Tools):
                    raise Exception

                # Select (Video in Reverse)
                self.select_right_click_menu('Video in Reverse')

                time.sleep(DELAY_TIME)

                if skip:
                    # Skip verify
                    pass
                else:
                    # Verify Step
                    img_after = self.snapshot(L.main.timeline.table_view)
                    # result = self.image.search(img_before, img_after)
                    # logger(result)
                    result_verify = self.compare(img_before, img_after, similarity=0.99)
                    if result_verify:
                        logger(f'Fail to verify timeline table_view')
                        raise Exception

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def get_select_Video_in_Reverse_status(self):
            # Click TipsArea [Tools] button > Return True/False about [Video in Reverse] status
            try:
                # Click TipsArea [Tools] button
                if not self.exist_click(L.tips_area.button.btn_Tools):
                    raise Exception

                if not self.exist(L.tips_area.button.tools.btn_VideoInReverse):
                    logger('cannot find btn_VideoInReverse')
                    raise Exception

                if self.exist(L.tips_area.button.tools.btn_VideoInReverse).AXMenuItemMarkChar == '✓':
                    result = True
                else:
                    result = False

                self.right_click()
                time.sleep(DELAY_TIME)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return result

        def select_Audio_Editor(self, close_win=False):
            # Description : Click TipsArea [Tools] button > Select (Audio Editor)
            try:
                img_before = self.snapshot(L.main.timeline.table_view)

                # Click TipsArea [Tools] button
                if not self.exist_click(L.tips_area.button.btn_Tools):
                    raise Exception

                # Select (Audio Editor)
                self.select_right_click_menu('Audio Editor')

                time.sleep(DELAY_TIME)

                # Verify Step
                if not self.exist(L.tips_area.audio_editor.tab):
                    logger('Not enter Audio Editor, verify Fail')
                    return False

                if close_win:
                    self.exist_click(L.tips_area.audio_editor.close)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def select_Audio_Speed(self):
            # Description : Click TipsArea [Tools] button > Select (Audio Speed)
            try:
                img_before = self.snapshot(L.main.timeline.table_view)

                # Click TipsArea [Tools] button
                if not self.exist_click(L.tips_area.button.btn_Tools):
                    raise Exception

                # Select (Audio Speed)
                self.select_right_click_menu('Audio Speed')

                time.sleep(DELAY_TIME)

                # Verify Step
                if not self.exist(L.tips_area.window.audio_speed):
                    logger('Not enter Audio Speed, verify Fail')
                    return False

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def select_Audio_in_Reverse(self):
            # Description : Click TipsArea [Tools] button > Select (Audio in Reverse)
            try:
                img_before = self.snapshot(L.main.timeline.table_view)

                # Click TipsArea [Tools] button
                if not self.exist_click(L.tips_area.button.btn_Tools):
                    raise Exception

                # Select (Audio in Reverse)
                self.select_right_click_menu('Audio in Reverse')

                time.sleep(DELAY_TIME)

                # Verify Step
                img_after = self.snapshot(L.main.timeline.table_view)
                # result = self.image.search(img_before, img_after)
                # logger(result)
                result_verify = self.compare(img_before, img_after, similarity=0.99)
                if result_verify:
                    logger(f'Fail to verify timeline table_view')
                    raise Exception

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def get_select_Audio_in_Reverse_status(self):
            # Click TipsArea [Tools] button > Return True/False about [Audio in Reverse] status
            try:
                # Click TipsArea [Tools] button
                if not self.exist_click(L.tips_area.button.btn_Tools):
                    raise Exception

                if not self.exist(L.tips_area.button.tools.btn_AudioInReverse):
                    logger('cannot find btn_AudioInReverse')
                    raise Exception

                if self.exist(L.tips_area.button.tools.btn_AudioInReverse).AXMenuItemMarkChar == '✓':
                    result = True
                else:
                    result = False

                self.right_click()
                time.sleep(DELAY_TIME)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return result

    class MoreFeatures(BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def click_btn(self, verify=False):
            # [Parameter] verify = True, False
            # When verify is True, execute (Verify Step) : After clicking the [More Functions] button, the context menu will be displayed
            # When verify is False, skip (Verify Step)

            # Click TipsArea [More Features] button
            try:
                # if not self.exist_click(L.tips_area.button.more_features.main):
                #     raise Exception
                # << modify by Miti. Using mouse click to prevent pop-up menu out of screen>>
                self.mouse.click(*self.find(L.tips_area.button.more_features.main).center)

                # Verify Step:
                if not self.check_ContextMenu_status() and verify:
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def check_ContextMenu_status(self):
            # case1: TipsArea doesn't exist [More Features] button
            # Return "None"
            if not self.exist(L.tips_area.button.more_features.main):
                logger("cannot find the [More Features] button")
                return None
            # case2: TipsArea exists [More Features] button
            # if exist [More Features] button and (Context Menu), return True
            # if exist [More Features] button and no display (Context Menu), return False
            if self.exist(L.tips_area.button.more_features.main).AXChildren:
                return True
            else:
                return False

        def first_level(self, index, sequence=1):
            try:
                self.click_btn(verify=True)
                el_list = ['Cut', 'Copy', 'Paste', 'Remove', 'Image']
                current = el_list[index]
                logger(f' Select Content Menu [{current}] by OCR')

                self.select_right_click_menu(f'{current}')
                # Select (Context Menu) by OCR
                #menu_item1_pos = self.search_text_position(f'{current}', mouse_move=0, order=sequence)
                #print(f'{menu_item1_pos=}')
                #if menu_item1_pos is not False:
                #    self.mouse.click(*menu_item1_pos)
                #else:
                #    logger('Fail to get the position of target')
                #    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def cut(self, option=-1):
            # option = -1 : Click [More Features] button > click [Cut]
            # option = 1 : Click [More Features] button > [Cut] > select [Cut and Leave Gap]
            # option = 2 : Click [More Features] button > [Cut] > select [Cut and Fill Gap]
            # option = 3 : Click [More Features] button > [Cut] > select [Cut,  Fill Gap and Move All Clips]

            # Click TipsArea [More Features] button > Click [Cut]
            try:
                self.click_btn(verify=True)
                if option == -1:
                    self.select_right_click_menu('Cut')
                elif option == 1:
                    self.select_right_click_menu('Cut', 'Cut and Leave Gap')
                elif option == 2:
                    self.select_right_click_menu('Cut', 'Cut and Fill Gap')
                elif option == 3:
                    self.select_right_click_menu('Cut', 'Cut, Fill Gap, and Move All Clips')
                else:
                    logger(f'Input parameter ({option}) is invalid.')
                    raise Exception

                # Verify Step:
                if self.check_ContextMenu_status() is None:
                    logger('click cut [done]')
                    pass
                else:
                    raise Exception

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def copy(self):
            # Click TipsArea [More Features] button > Click [Copy]
            try:
                self.click_btn(verify=True)
                self.select_right_click_menu('Copy')

                # Verify Step:
                if self.check_ContextMenu_status() is False:
                    logger('click copy [done]')
                    pass
                else:
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def copy_keyframe_attributes(self):
            # Click TipsArea [More Features] button > Click [Copy Keyframe Attributes]
            try:
                self.click_btn(verify=True)
                self.select_right_click_menu('Copy Keyframe Attributes')

                # Verify Step:
                if self.check_ContextMenu_status() is False:
                    logger('click copy_keyframe_attributes [done]')
                    pass
                else:
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def check_paste_second_level_option(self, option):
            try:
                el_option = ['Overwrite', 'Trim', 'Speed', 'Insert', 'MoveAll', 'Crossfade']
                el_result = ['Paste and Overwrite                             	  ⌃+Drop',
                             'Paste and Trim to Fit',
                             'Paste and Speed up to Fit',
                             'Paste and Insert',
                             'Paste, Insert, and Move All Clips        	  ⇧+Drop',
                             'Crossfade                                              	  ⌥+Drop']
                result = -1
                for x in range(6):
                    if option == f'{el_option[x]}':
                        result = f'{el_result[x]}'
                if result == -1:
                    logger(f' Parameter - {option} is invalid')
                    raise Exception

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return result

        def paste(self, option=-1):
            # option = -1 : Click [More Features] button > click [Paste]
            # option = Overwrite : Click [More Features] button > [Paste] > select [Paste and Overwrite]
            # option = Trim : Click [More Features] button > [Paste] > select [Paste and Trim to Fit]
            # option = Speed : Click [More Features] button > [Paste] > select [Paste and Speed up to Fit]
            # option = Insert : Click [More Features] button > [Paste] > select [Paste and Insert]
            # option = MoveAll : Click [More Features] button > [Paste] > select [Paste, Insert, and Move All Clips]
            # option = Crossfade : Click [More Features] button > [Paste] > select [Crossfade]
            try:

                # Click [More Features] button
                self.click_btn(verify=True)

                # select context menu / submenu
                if option == -1:
                    self.select_right_click_menu('Paste')
                elif option == 'Overwrite':
                    self.select_right_click_menu('Paste', 'Paste and Overwrite                             	  ⌃+Drop')
                elif option == 'Trim':
                    self.select_right_click_menu('Paste', 'Paste and Trim to Fit')
                elif option == 'Speed':
                    self.select_right_click_menu('Paste', 'Paste and Speed up to Fit')
                elif option == 'Insert':
                    self.select_right_click_menu('Paste', 'Paste and Insert')
                elif option == 'MoveAll':
                    self.select_right_click_menu('Paste', 'Paste, Insert, and Move All Clips        	  ⇧+Drop')
                elif option == 'Crossfade':
                    self.select_right_click_menu('Paste', 'Crossfade                                              	  ⌥+Drop')
                else:
                    logger(f'Input parameter ({option}) is invalid.')
                    raise Exception

                # Verify Step:
                if self.check_ContextMenu_status() is False:
                    logger('click ContextMenu [done]')
                    pass
                else:
                    logger('Verify [FAIL]')
                    return False

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def paste_keyframe_attributes(self):
            # Click TipsArea [More Features] button > Click [Paste Keyframe Attributes]
            try:
                # Click [More Features] button
                self.click_btn(verify=True)
                self.select_right_click_menu('Paste Keyframe Attributes')

                # Verify Step:
                warning_status = self.exist(L.tips_area.warning_dialog.msg2).AXValue.startswith(
                    'The current keyframe settings will be')
                if not warning_status:
                    logger('Verify : No warning message pop up [FAIL]')
                    raise Exception
                else:
                    self.exist_click(L.tips_area.warning_dialog.ok)

                if self.check_ContextMenu_status() is False:
                    logger('click paste_keyframe_attributes [done]')
                    pass
                else:
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def remove(self, index=0):
            # index = 0 : Click [More Features] button > click [Remove]
            # index = 1 : Click [More Features] button > [Remove] > select [Remove and Leave Gap]
            # index = 2 : Click [More Features] button > [Remove] > select [Remove and Fill Gap]
            # index = 3 : Click [More Features] button > [Remove] > select [Remove, Fill Gap, and Move All Clips]

            try:
                el_result = ['', 'Remove and Leave Gap',
                             'Remove and Fill Gap',
                             'Remove, Fill Gap, and Move All Clips']

                # Click [More Features] button > select [Remove]
                self.click_btn(verify=True)
                if index == 0:
                    self.exist_click(L.tips_area.button.more_features.btn_Remove)
                else:
                    current = f'{el_result[index]}'
                    # Click second level (Context Menu)
                    self.select_right_click_menu('Remove', current)

                # Verify Step:
                if self.check_ContextMenu_status() is None:
                    logger('click ContextMenu [done]')
                    pass
                else:
                    logger('Verify [FAIL]')
                    return False

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def select_all(self):
            # Click TipsArea [More Features] button > Click [Select All]
            try:
                self.click_btn(verify=True)
                time.sleep(DELAY_TIME)
                self.exist_click(L.tips_area.button.more_features.btn_SelectAll)

                # Verify Step:
                if self.check_ContextMenu_status() is False:
                    logger('click select_all [done]')
                    pass
                else:
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def get_link_unlink_status(self):
            # Click TipsArea [More Features] button > Return True/False about [Link/Unlink Video and Audio] status
            try:
                self.click_btn(verify=True)

                if not self.exist(L.tips_area.button.more_features.btn_link_unlink):
                    logger('cannot find btn_link_unlink')
                    raise Exception
                result = self.exist(L.tips_area.button.more_features.btn_link_unlink).AXEnabled
                self.right_click()
                time.sleep(DELAY_TIME)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return result

        def get_group_ungroup_status(self):
            # Click TipsArea [More Features] button > Return True/False about [Group/Ungroup Objects] status
            try:
                self.click_btn(verify=True)

                if not self.exist(L.tips_area.button.more_features.btn_group_ungroup):
                    logger('cannot find btn_group_ungroup')
                    raise Exception
                result = self.exist(L.tips_area.button.more_features.btn_group_ungroup).AXEnabled
                self.right_click()
                time.sleep(DELAY_TIME)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return result

        def get_split_status(self):
            # Click TipsArea [More Features] button > Return True/False about [Split] status
            try:
                self.click_btn(verify=True)

                if not self.exist(L.tips_area.button.more_features.btn_split):
                    logger('cannot find btn_split')
                    raise Exception
                result = self.exist(L.tips_area.button.more_features.btn_split).AXEnabled
                self.right_click()
                time.sleep(DELAY_TIME)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return result

        def edit_Shape_Designer(self):
            # Description : Click TipsArea [More Features] button > Select (Shape Designer)
            try:
                # Click TipsArea [More Features] button
                self.click_btn(verify=True)
                if not self.exist_click(L.tips_area.button.more_features.btn_shape_designer):
                    raise Exception


                # Verify Step
                if not self.exist(L.pip_designer.cancel_button):
                    logger('Not enter Shape Designer, verify Fail')
                    return False
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True













        def link_unlink_video_audio(self):
            # Click TipsArea [More Features] button > Click [Link/Unlink Video and Audio]
            try:
                self.click_btn(verify=True)
                time.sleep(DELAY_TIME)
                self.exist_click(L.tips_area.button.more_features.btn_link_unlink)

                # Verify Step:
                if self.check_ContextMenu_status() is False:
                    logger('click link_unlink_video_audio [done]')
                    pass
                else:
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def group_ungroup_obj(self):
            # Click TipsArea [More Features] button > Click [Group/Ungroup Objects]
            try:
                self.click_btn(verify=True)
                time.sleep(DELAY_TIME)
                self.exist_click(L.tips_area.button.more_features.btn_group_ungroup)

                # Verify Step:
                if self.check_ContextMenu_status() is False:
                    logger('click group_ungroup_obj [done]')
                    pass
                else:
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def split(self):
            # Click TipsArea [More Features] button > Click [Split]
            try:
                self.click_btn(verify=True)
                time.sleep(DELAY_TIME)
                self.exist_click(L.tips_area.button.more_features.btn_split)

                # Verify Step:
                if self.check_ContextMenu_status() is False:
                    logger('click split [done]')
                    pass
                else:
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def edit_image(self):
            # Click [More Features] button > click [Edit Image]
            try:
                self.click_btn(verify=True)
                self.select_right_click_menu('Edit Image')

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def get_edit_image_status(self):
            try:
                self.click_btn(verify=True)

                if not self.exist(L.tips_area.button.more_features.btn_edit_img):
                    logger('cannot find btn_edit_img')
                    raise Exception
                result = self.exist(L.tips_area.button.more_features.btn_edit_img).AXEnabled
                self.right_click()
                time.sleep(DELAY_TIME)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return result

        def edit_image_CropImage(self):
            # Click [More Features] button > [Edit Image] > select [Crop Image]
            try:
                # Click [More Features] button > click [Edit Image]
                self.click_btn(verify=True)
                self.select_right_click_menu('Edit Image')

                # Click [Crop Image]
                self.exist_click(L.tips_area.button.more_features.btn_crop_image)

                # Verify Step: Check to open (Crop Image) window
                if not self.is_exist(L.tips_area.window.crop_image, None, DELAY_TIME * 10):
                    logger('Click More Feature > Edit Image > Crop Image, cannot enter Crop Image window')
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def edit_image_PanZoom(self, close_win=False):
            # Click [More Features] button > [Edit Image] > select [Pan & Zoom]
            try:
                # Click [More Features] button > click [Edit Image]
                self.click_btn(verify=True)
                self.select_right_click_menu('Edit Image')

                # Click [Pan & Zoom]
                self.exist_click(L.tips_area.button.more_features.btn_pan_zoom)

                # Verify Step: Check to enter (Pan & Zoom)
                if not self.exist(L.tips_area.pan_zoom.tab):
                    logger('Not enter Pan & Zoom, verify Fail')
                    return False

                if close_win:
                    self.exist_click(L.tips_area.pan_zoom.close)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def edit_image_FixEnhance(self, close_win=False):
            # Click [More Features] button > [Edit Image] > select [Fix/Enhance]
            try:
                # Click [More Features] button > click [Edit Image]
                self.click_btn(verify=True)
                self.exist_click(L.tips_area.button.more_features.btn_edit_img)

                # Select [Fix/Enhance]
                self.exist_click(L.tips_area.button.more_features.btn_image_fix_enhance)

                # Verify Step: Check to enter (Fix/Enhance)
                if not self.exist(L.tips_area.fix_enhance.tab):
                    logger('Not enter Fix/Enhance, verify Fail')
                    return False

                if close_win:
                    self.exist_click(L.tips_area.fix_enhance.close)
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def edit_image_enable_fade_feature(self, tick=1):
            # Click [More Features] button > [Edit Image]
            # if tick = 1 (Default), Enable [Enable Fade-in and Fade-out]
            # if tick = 0, Disable [Enable Fade-in and Fade-out]
            try:
                if tick < 0 or tick > 1:
                    logger('Parameter is invalid')
                    raise Exception
                # Click [More Features] button > click [Edit Image]
                self.click_btn(verify=True)
                self.exist_click(L.tips_area.button.more_features.btn_edit_img)

                # Check status about [Enable Fade-in and Fade-out]
                current_status = self.get_image_enable_Fade_feature_status()
                logger(current_status)

                if tick != current_status:
                    self.exist_click(L.tips_area.button.more_features.btn_image_fade_in_out)

                    # Verify Step:
                    if self.check_ContextMenu_status() is False:
                        pass
                    else:
                        raise Exception
                else:
                    self.click_btn(verify=False)

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def get_image_enable_Fade_feature_status(self):
            # Check [Edit Image] > [Enable Fade-in and Fade-out] status
            # Return 1 if tick
            # Return 0 if un-tick
            try:
                # Check status about [Enable Fade-in and Fade-out]
                if not self.is_exist(L.tips_area.button.more_features.btn_image_fade_in_out):
                    raise Exception
                if self.exist(L.tips_area.button.more_features.btn_image_fade_in_out).AXMenuItemMarkChar == '✓':
                    result = 1
                else:
                    result = 0
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return result

        def get_image_fade_tick_status(self):
            # Click [More Features] button > click [Edit Image]
            self.click_btn(verify=True)
            self.exist_click(L.tips_area.button.more_features.btn_edit_img)

            result = self.get_image_enable_Fade_feature_status()
            if result == 1:
                result = True
            else:
                result = False
            self.click_btn(verify=False)
            return result

        def edit_image_restore_opacity(self):
            # Click [More Features] button > [Edit Image] > select [Restore to Original Opacity Level]
            try:

                # Click [More Features] button > click [Edit Image]
                self.click_btn(verify=True)

                #  [Edit Image] > select [Restore to Original Opacity Level]
                result = self.select_right_click_menu('Edit Image', 'Restore to Original Opacity Level')
                if result is False:
                    logger('[Restore to Original Opacity Level] is gray now')
                    raise Exception

            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return result

        def get_image_restore_opacity_status(self):
            # The page function will return result (True/False/None) after checked [Restore to Original Opacity Level]

            # Step1: Click [More Features] button
            self.click_btn(verify=True)

            # Step2: Click [Edit Image] > Check [Restore to Original Opacity Level]
            # Return True if enable / Return False if gray out / Return None if not found
            result = self.is_right_click_menu_enabled('Edit Image', 'Restore to Original Opacity Level')

            return result

        def edit_video(self):
            self.click_btn(verify=True)
            self.select_right_click_menu("Edit Video")

        def _get_status(self, item):
            self.click_btn(verify=True)
            return self.select_right_click_menu(item, click_it=False)

        def get_edit_video_status(self):
            return self._get_status("Edit Video")

        def _is_exist_dialog(self, name):
            title_list = [x.AXValue for x in self.find([{"AXSubrole": "AXDialog", "recursive": False},
                                                        {"AXRole": "AXStaticText", "recursive": False,
                                                         "get_all": True}])]
            for title in title_list:
                if name in title: return True
            return False

        def edit_video_trim(self):
            self.click_btn(verify=True)
            self.select_right_click_menu("Edit Video", "Trim...")
            return self._is_exist_dialog("Trim | ")

        def edit_video_FixEnhance(self):
            self.click_btn(verify=True)
            self.select_right_click_menu("Edit Video", "Fix / Enhance")
            return self.is_exist({"AXValue": "Fix / Enhance"})

        def edit_video_enable_fade_feature(self, tick=True):
            self.click_btn(verify=True)
            elem = self.select_right_click_menu("Edit Video", "Enable Fade-in and Fade-out", return_elem=True)
            if bool(elem.AXMenuItemMarkChar) != tick:
                self.mouse.click(*elem.center)
            else:
                self._close_menu()
            return True

        def get_video_fade_tick_status(self):
            self.click_btn(verify=True)
            return self.select_right_click_menu("Edit Video", "Enable Fade-in and Fade-out", return_is_selected=True)

        def edit_video_restore_opacity(self):
            self.click_btn(verify=True)
            ret = self.select_right_click_menu("Edit Video", "Restore to Original Opacity Level")
            if ret:
                return True
            else:
                raise Exception("ERROR: [Restore to Original Opacity Level] is gray out")

        def get_video_restore_opacity_status(self):
            self.click_btn(verify=True)
            return self.select_right_click_menu("Edit Video", "Restore to Original Opacity Level", click_it=False)

        def edit_in_video_collage_designer(self):
            self.click_btn(verify=True)
            return self.select_right_click_menu("Edit Video", "Edit in Video Collage Designer...")

        def get_edit_in_video_collage_status(self):
            self.click_btn(verify=True)
            return self.select_right_click_menu("Edit Video", "Edit in Video Collage Designer...", click_it=False)

        def click_clip_attributes_duration(self):
            self.click_btn(verify=True)
            return self.select_right_click_menu("Set Clip Attributes", "Set Duration...")

        def click_clip_attributes_stretch_mode(self):
            self.click_btn(verify=True)
            self.select_right_click_menu("Set Clip Attributes", "Set Image Stretch Mode...")
            return self.is_exist({"AXTitle": "Image Stretch Mode Settings"})

        def set_image_stretch_settings(self, option):
            locator = eval(f'L.tips_area.button.more_features.image_stretch_mode.option_{option}')
            text = ["Stretch clip to 16:9 aspect ratio", "Use CLPV to stretch clip to 16:9 a..."][option]
            self.activate()
            self.exist_click(L.tips_area.button.more_features.image_stretch_mode.aspect_ratio)
            self.exist_click(locator)
            if self.is_exist({"AXTitle": text}):
                self.exist_click(L.tips_area.button.more_features.image_stretch_mode.ok)
                return True
            else:
                return False

        def set_attributes_aspect_ratio(self):
            self.click_btn(verify=True)
            self.select_right_click_menu("Set Clip Attributes", "Set Aspect Ratio...")
            return self._is_exist_dialog("Clip Aspect Ratio Settings")

        def edit_clip_aspect_ratio_settings(self):
            self.exist(L.tips_area.button.more_features.clip_aspect_ratio.detect_and_suggest).press()
            elem = self.exist(L.tips_area.button.more_features.clip_aspect_ratio.detect_aspect_ratio)
            timer = time.time()
            while time.time() - timer < 5:
                if not elem.AXValue:
                    self.exist_click(L.tips_area.button.more_features.clip_aspect_ratio.ok)
                    return True
            raise Exception("Click detect aspect ratio fail")

        def set_attributes_blending_mode(self, index):
            text = ["Normal", "Darken", "Multiply", "Lighten", "Screen", "Overlay", "Difference", "Hue"][index]
            self.click_btn(verify=True)
            return self.select_right_click_menu("Set Clip Attributes", "Set Blending Mode", text)

        def click_change_alias(self):
            self.click_btn(verify=True)
            self.select_right_click_menu("Edit Clip Alias", "Change Alias...")
            return self.is_exist({"AXValue", "Set Alias"})

        def set_alias(self, alias):
            self.exist(L.tips_area.button.more_features.set_alias.alias).AXValue = alias
            return bool(self.exist_click(L.tips_area.button.more_features.set_alias.ok))

        def get_alias(self):
            self.click_btn(verify=True)
            self.select_right_click_menu("Edit Clip Alias", "Change Alias...")
            ret = self.exist(L.tips_area.button.more_features.set_alias.alias).AXValue
            self.exist_click(L.tips_area.button.more_features.set_alias.cancel)
            return ret

        def click_reset_alias(self):
            self.click_btn(verify=True)
            return self.select_right_click_menu("Edit Clip Alias", "Reset Alias")

        def view_properties(self, close_win=True):
            self.click_btn(verify=True)
            self.select_right_click_menu("View Properties")
            ret = self.is_exist({"AXValue": "Properties"})
            if close_win: self.exist_click(L.tips_area.button.more_features.properties.close)
            return ret

        def dock_undock_timeline_window(self, undock=True):
            if self.is_exist([{"AXIdentifier": "PopupWindow", "recursive": False},
                              {"AXRole": "AXToolbar", "recursive": False},
                              {"AXRole": "AXGroup", "recursive": False},
                              {"AXValue": "Timeline Window", "recursive": False}], timeout=0) != undock:
                self.click_btn(verify=True)
                self.select_right_click_menu("Dock/Undock Timeline Window")
            return True

        def reset_all_undock_windows(self):
            self.click_btn(verify=True)
            return self.select_right_click_menu("Reset All Undocked Windows")

        def get_reset_all_undock_windows_status(self):
            self.click_btn(verify=True)
            return self.select_right_click_menu("Reset All Undocked Windows", click_it=False)

        def get_menu_status(self, *args):
            try:
                return self.select_right_click_menu(*args, click_it=False)
            except:
                return None

        def mute_clip(self):
            self.click_btn(verify=True)
            return bool(self.select_right_click_menu("Mute Clip"))

        def get_mute_clip_tick_status(self):
            self.click_btn(verify=True)
            return self.select_right_click_menu("Mute Clip", return_is_selected=True)

        def restore_original_volume(self):
            self.click_btn(verify=True)
            return self.select_right_click_menu("Restore to Original Volume Level")

        def get_restore_original_volume_status(self):
            self.click_btn(verify=True)
            return self.select_right_click_menu("Restore to Original Volume Level", click_it=False)

        def remove_all_clip_markers(self):
            self.click_btn(verify=True)
            return self.select_right_click_menu("Remove All Clip Markers For Selected Clip")

        def get_remove_all_clip_markers_status(self):
            self.click_btn(verify=True)
            return self.select_right_click_menu("Remove All Clip Markers For Selected Clip", click_it=False)

        def normalize_audio(self):
            self.click_btn(verify=True)
            return self.select_right_click_menu("Normalize Audio")

        def get_normalize_audio_status(self):
            self.click_btn(verify=True)
            return self.select_right_click_menu("Normalize Audio", click_it=False)

        def edit_effect(self, close_win=True):
            self.click_btn(verify=True)
            self.select_right_click_menu("Edit Effect")
            timer = time.time()
            while time.time() - timer < 3:
                try:
                    elem_close = self.exist(L.tips_area.button.btn_effect_close, timeout=0)
                    if elem_close:
                        if close_win: elem_close.press()
                        return True
                    raise Exception(f"{type} Window is not found")
                except:
                    pass
            else:
                return False

        def edit_title(self):
            self.click_btn(verify=True)
            return self.select_right_click_menu("Edit Title...")

        def modifiy_transition(self, close_win=True):
            self.click_btn(verify=True)
            self.select_right_click_menu("Modify Transition")
            timer = time.time()
            while time.time() - timer < 3:
                try:
                    elem_close = self.exist(L.tips_area.button.btn_transition_close, timeout=0)
                    if elem_close:
                        if close_win: elem_close.press()
                        return True
                    raise Exception(f"Transition Window is not found")
                except:
                    pass
            else:
                return False

        def click_set_duration(self, close_win=True):
            self.click_btn(verify=True)
            self.select_right_click_menu("Set Duration...")
            timer = time.time()
            while time.time() - timer < 3:
                try:
                    elem_close = self.exist(L.tips_area.button.btn_duration_ok, timeout=0, no_warning=True)
                    if elem_close:
                        if close_win: elem_close.press()
                        return True
                    raise Exception(f"Duration Window is not found")
                except:
                    pass
            else:
                return False

        def get_edit_video_trim_status(self):
            self.click_btn(verify=True)
            return self.select_right_click_menu("Edit Video", "Trim...", click_it=False)

        def get_edit_video_fixenhance_status(self):
            self.click_btn(verify=True)
            return self.select_right_click_menu("Edit Video", "Fix / Enhance", click_it=False)

    def click_TipsArea_btn_import_media(self, full_path):
        # full_path: /Users/qadf_at/Desktop/01.png
        try:
            if not self.exist_click(L.tips_area.button.btn_Import_media):
                logger('Cannot find btn_tips_area_Import_media')
                raise Exception
            time.sleep(DELAY_TIME * 2)
            logger('line23')
            if not self.select_file(full_path):
                raise Exception('Cannot select file w/ full_path')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_TipsArea_btn_insert(self, option=-1):
        # option: -1-None, 0-Overwrite, 1-Insert,
        #          2-insert_and_move_all_clips, 3-CrossFade, 4-Replace
        return self.tips_area_insert_media_to_selected_track(option)

    @step('[Action][TipsArea] Click [Insert to Selected Track] button')
    def click_TipsArea_btn_insert_project(self):
        self.click(L.main.tips_area.btn_insert_to_selected_track_project)
        time.sleep(DELAY_TIME * 3)
        return True

    @step('[Action][TipsArea] Click [Effect] button on [Tips Area]')
    def click_TipsArea_btn_effect(self):
        self.click(L.tips_area.button.btn_effect_modify)
        time.sleep(DELAY_TIME * 2)
        return True

    def click_sync_by_audio(self):
        self.click(L.tips_area.button.btn_sync_by_audio)
        time.sleep(DELAY_TIME * 5)
        return True

    def click_TipsArea_btn_add_to_effect_track(self, option=-1):
        # option = -1(No pop up menu), 0(Overwrite), 1(Insert), 2(Insert and Move All Clips)
        return self.tips_area_click_add_effect_to_track(option)

    def click_TipsArea_btn_apply_favorite_transition(self, option):
        # option = 0(Prefix Transition), 1(Postfix Transition), 2(Cross Transition), 3(Overlap Transition)
        try:
            el_option = ['Prefix', 'Postfix', 'Cross', 'Overlap']
            self.exist_click(L.tips_area.button.btn_Apply_my_Favorite_transition)
            time.sleep(DELAY_TIME * 2)
            if not option == -1:
                # click by OCR
                menu_item1_pos = self.search_text_position(el_option[option], mouse_move=0, order=1)
                print(f'{menu_item1_pos=}')
                if menu_item1_pos is not False:
                    self.mouse.click(*menu_item1_pos)
                else:
                    logger('Fail to get the position of target')
                    raise Exception
            if self.is_exist(L.tips_area.button.btn_Apply_my_Favorite_transition, None, 2):
                logger('Fail to apply my Favorite transition to all video')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_TipsArea_btn_apply_fading_transition(self, option):
        # option = 0(Prefix Transition), 1(Postfix Transition), 2(Cross Transition), 3(Overlap Transition)
        try:
            el_option = ['Prefix', 'Postfix', 'Cross', 'Overlap']
            self.exist_click(L.tips_area.button.btn_Apply_fading_transition)
            time.sleep(DELAY_TIME * 2)
            if not option == -1:
                # click by OCR
                menu_item1_pos = self.search_text_position(el_option[option], mouse_move=0, order=1)
                print(f'{menu_item1_pos=}')
                if menu_item1_pos is not False:
                    self.mouse.click(*menu_item1_pos)
                else:
                    logger('Fail to get the position of target')
                    raise Exception
            if self.is_exist(L.tips_area.button.btn_Apply_fading_transition, None, 2):
                logger('Fail to apply fading transition to all video')
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_TipsArea_btn_insert_audio(self, option):
        # option = -1 (No handle pop up menu)
        # option = 0 (Overwrite)
        # option = 1 (Trim to Fit)
        # option = 2 (Speed up to Fit)
        # option = 3 (Insert)
        # option = 4 (Insert and Move All Clips)
        try:
            el_option = ['Overwrite', 'Trim', 'Speed', 'Insert', 'Move']
            self.exist_click(L.main.tips_area.btn_insert_to_selected_track)
            time.sleep(DELAY_TIME * 2)
            if not option == -1:
                # click by OCR
                menu_item1_pos = self.search_text_position(el_option[option], mouse_move=0, order=1)
                print(f'{menu_item1_pos=}')
                if menu_item1_pos is not False:
                    self.mouse.click(*menu_item1_pos)
                else:
                    logger('Fail to get the position of target')
                    raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_TipsArea_btn_split(self):
        return self.tips_area_click_split()

    def get_btn_split_status(self):
        try:
            if not self.find(L.main.tips_area.btn_split):
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return self.exist(L.main.tips_area.btn_split).AXEnabled

    def click_TipsArea_btn_Copy(self):
        try:
            if not self.exist_click(L.tips_area.button.btn_Copy):
                logger('Cannot find btn_Copy')
                raise Exception
            time.sleep(DELAY_TIME)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_TipsArea_btn_Paste(self):
        try:
            img_before = self.snapshot(L.main.timeline.table_view)
            if not self.exist_click(L.tips_area.button.btn_Paste):
                logger('Cannot find btn_Paste')
                raise Exception
            time.sleep(DELAY_TIME)
            self.wait_for_image_changes(img_before, L.main.timeline.table_view, DELAY_TIME * 5)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_TipsArea_btn_Cut(self):
        try:
            img_before = self.snapshot(L.main.timeline.table_view)
            if not self.exist_click(L.tips_area.button.btn_Cut):
                logger('Cannot find btn_Cut')
                raise Exception
            time.sleep(DELAY_TIME)
            self.wait_for_image_changes(img_before, L.main.timeline.table_view, DELAY_TIME * 5, similarity=0.985)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_TipsArea_btn_Remove(self):
        try:
            img_before = self.snapshot(L.main.timeline.table_view)
            if not self.exist_click(L.tips_area.button.btn_Remove):
                logger('Cannot find btn_Remove')
                raise Exception
            time.sleep(DELAY_TIME)
            self.wait_for_image_changes(img_before, L.main.timeline.table_view, DELAY_TIME * 5)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_TipsArea_btn_Produce_Range(self):
        try:
            if not self.exist_click(L.tips_area.button.btn_Produce_Range):
                logger('Cannot find btn_Produce_Range')
                raise Exception

            # Verify Step: Check enter Produce Page
            if not self.is_exist(L.produce.btn_start_produce, None, DELAY_TIME * 10):
                logger('Fail to enter produce page')
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_TipsArea_btn_Lock_Range(self):
        try:
            img_collection_view_before = self.snapshot(L.tips_area.button.btn_Lock_Range)

            if not self.exist_click(L.tips_area.button.btn_Lock_Range):
                logger('Cannot find btn_Lock_Range')
                raise Exception
            el_position = self.find(L.tips_area.button.btn_Lock_Range).AXPosition
            x_axis = el_position[0]
            y_axis = el_position[1] - 25
            self.mouse.move(x_axis, y_axis)

            img_collection_view_after = self.snapshot(L.tips_area.button.btn_Lock_Range)

            # Verify Step: Check before/after is changed by snapshot
            result_verify = self.compare(img_collection_view_before, img_collection_view_after)

            if result_verify:
                logger(f'Fail to click [Lock Range]] button')
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_TipsArea_btn_Lock_Range(self):
        try:
            img_collection_view_before = self.snapshot(L.tips_area.button.btn_Lock_Range)

            if not self.exist_click(L.tips_area.button.btn_Lock_Range):
                logger('Cannot find btn_Lock_Range')
                raise Exception
            el_position = self.find(L.tips_area.button.btn_Lock_Range).AXPosition
            x_axis = el_position[0]
            y_axis = el_position[1] - 25
            self.mouse.move(x_axis, y_axis)

            img_collection_view_after = self.snapshot(L.tips_area.button.btn_Lock_Range)

            # Verify Step: Check before/after is changed by snapshot
            result_verify = self.compare(img_collection_view_before, img_collection_view_after)

            if result_verify:
                logger(f'Fail to click [Lock Range]] button')
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_TipsArea_btn_Crop_Image(self):
        try:
            if not self.exist_click(L.tips_area.button.btn_Crop_the_selected_image):
                logger('Cannot find btn_Crop_the_selected_image')
                raise Exception

            # Verify Step: Check to open (Crop Image) window
            if not self.is_exist(L.tips_area.window.crop_image, None, DELAY_TIME * 10):
                logger('Fail to click Crop')
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_TipsArea_btn_Duration(self):
        try:
            if not self.exist_click(L.tips_area.button.btn_Set_the_length_of_the_selected_clip):
                logger('Cannot find btn_Set_the_length_of_the_selected_clip')
                raise Exception

            # Verify Step: Check to open (Duration Settings) window
            if not self.is_exist(L.tips_area.window.duration_settings, None, DELAY_TIME * 10):
                logger('Fail to click Duration')
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def apply_duration_settings(self, duration):
        # duration: in format 'HH_MM_SS_mm'
        #                 e.g. 00_00_20_00 (00:00:20:00)
        #                 e.g. 01_00_05_00 (01:00:05:00)
        # Initial status : Open Duration Settings window
        try:
            img_before = self.snapshot(L.main.timeline.table_view)
            # Step 1 : Set time code
            el_locator = self.exist(L.main.duration_setting_dialog.txt_duration)
            self.set_time_code(el_locator, duration)

            # Step 2 : Click [OK] button
            self.exist_click(L.main.duration_setting_dialog.btn_ok)

            # Step 3 : Verify
            self.wait_for_image_changes(img_before, L.main.timeline.table_view, DELAY_TIME * 5, 0.99)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_fix_enhance(self, close_win=False):
        try:
            if not self.exist_click(L.tips_area.button.btn_Fix_Enhance):
                logger('Cannot find btn_Fix_Enhance')
                raise Exception

            # Verify Step: Check to enter (Fix/Enhance)
            if not self.exist(L.tips_area.fix_enhance.tab, timeout= 10):
                logger('Not enter Fix/Enhance, verify Fail')
                return False

            # if selected clip contains alpha transparency and enter (White Balance), will pop up warning msg
            if self.exist(L.tips_area.warning_dialog.msg3):
                self.click(L.tips_area.warning_dialog.ok)

            if close_win:
                self.exist_click(L.tips_area.fix_enhance.close)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_keyframe(self, close_win=False):
        try:
            if not self.exist_click(L.tips_area.button.btn_Keyframe):
                logger('Cannot find btn_Keyframe')
                raise Exception

            # Verify Step: Check to enter (Keyframe)
            if not self.exist(L.tips_area.keyframe.tab):
                logger('Not enter Fix/Enhance, verify Fail')
                return False

            if close_win:
                self.exist_click(L.tips_area.keyframe.close)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][TipsArea] Click [Trim] button in [Tips Area]')
    def click_TipsArea_btn_Trim(self, type):
        self.exist_click(L.tips_area.button.btn_trim)
        time.sleep(DELAY_TIME*2)
        if type.lower() == "video":
            timer = time.time()
            while time.time() - timer < 3:
                try:
                    elem = self.exist([{"AXSubrole": "AXDialog", "recursive": False},
                                        {"AXRole": "AXStaticText", "recursive": False, "get_all": True}])

                    # First text is 'Selected Segments' > [Enter Multi Trim] >> Second text is title text
                    if elem[0].AXValue == 'Selected Segments':
                        title = elem[1].AXValue
                    # else [Enter Single Trim] / fourth text is title text
                    else: title = elem[3].AXValue

                    if title: return "Trim |" in title

                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception(f'Exception occurs. log={e}')
                return None
        else:
            return self.is_exist([{"AXSubrole": "AXDialog", "recursive": False},
                                  {"AXValue": "Trim Audio", "recursive": False}])

    def click_TipsArea_btn_Modify(self, type, close_win=True):
        index = type.lower() == "effect"
        entry = [L.tips_area.button.btn_transition_modify, L.tips_area.button.btn_effect_modify][index]
        close = [L.tips_area.button.btn_transition_close, L.tips_area.button.btn_effect_close][index]
        self.exist(entry).press()
        timer = time.time()
        while time.time()-timer < 3:
            try:
                elem_close = self.exist(close, timeout=0)
                if elem_close:
                    if close_win: elem_close.press()
                    return True
                raise Exception(f"{type} Window is not found")
            except:
                pass
        else:
            return False

    def click_TipsArea_btn_Designer(self, type):
        title = [{"AXSubrole":"AXDialog"},{"AXRole":"AXStaticText", "recursive":False}]
        verify = ["Particle Designer","Title Designer"][type.lower()=="title"]
        self.exist(L.tips_area.button.btn_designer).press()
        timer = time.time()
        while time.time()-timer < 3:
            try:
                title_text = self.find(title).AXValue
                return verify in title_text
            except:
                pass
        else:
            return False

    @step('[Action][TipsArea] Click [Change Color] button in [Tips Area] and change color')
    def click_TipsArea_btn_ChangeColor(self, color=None):
        self.exist_click(L.tips_area.button.btn_change_color)
        if color:
            self.exist(L.tips_area.button.change_color_hex).AXFocused = True
            self.click(L.tips_area.button.change_color_hex)
            self.exist(L.tips_area.button.change_color_hex).AXValue = color
            time.sleep(0.5)
            self.keyboard.enter()
            self.keyboard.esc()
        return True
    
    @step('[Action][TipsArea] Click [Video Collage] button in [Tips Area]')
    def click_TipsArea_btn_VideoCollage(self):
        self.exist_click(L.tips_area.button.btn_video_collage)
        found = self.is_exist([{"AXSubrole": "AXDialog", "recursive": False},
                               {"AXValue": "Video Collage Designer", "recursive": False}])
        return True if found else  False

    def click_color_match_button(self):
        self.exist_click(L.tips_area.button.btn_color_match)
        found = self.is_exist({"AXTitle": "Match Color", "recursive": False})
        return True if found else False

