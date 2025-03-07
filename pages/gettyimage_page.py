import time, datetime, os, copy
import cv2
import numpy

from .base_page import BasePage
from ATFramework.utils import logger
from ATFramework.utils.Image_Search import CompareImage
# from AppKit import NSScreen
from .locator import locator as L
#from .locator.hardcode_0408 import locator as L
from .main_page import Main_Page
from reportportal_client import step

DELAY_TIME = 1 # sec

checked = numpy.frombuffer(b'UKHYOLf_]\x96\x98\x9c\xa6\xb2\xbf\xb1\xc7\xd8\xb3\xcf\xe1\xac\xc5\xd6\xa6\xba\xc9\x9f\xb0\xbe\x9b\xab\xb8\x9b\xa9\xb5\x99\xa5\xad\x8f\x98\xa1~\x88\x93O_pRGEe\\Y\xa3\x9e\x9cwvwXXYOLLOMMOMMOMMOMMOMMOMMOLLWXYty\x7f\x91\x9e\xabMDA\x8a\x86\x83sopROOURRVSSVTTVTTVTTVTTVTTVTTVSSPNNIGG\xa3\xa5\xa7IB@\x9f\xa0\xa3WVWWTTYVVZWWZWWZWWZWWZWWZWWZWWTRRNKK\xb2\xb1\xb2vuuTfu\xa5\xb8\xc7URRYVVZWWZWWZWWZWWZWWZWWYVVSQQPNN\xc3\xc3\xc3\xa2\xa1\xa1KII@b\x81\x92\x9f\xaaVSSZWWZWWZWWZWWZWWZWWXVVROOTRR\xce\xcd\xcd\xc9\xc9\xc9IGGUSS\x1d/A\x85\x8b\x8fTRRZWWZWWZWWZWWZWWXVVPNN\\ZZ\xd9\xd9\xd9\xe3\xe3\xe3YWWSQQXWW\x1b%/\x94\x96\x98JIIPNNXUUZWWZWWWUUOMMedd\xdf\xdf\xdf\xe9\xe9\xe9zyyNLLYVVXVV\x18\x1e#\x86\x88\x89\xc7\xc7\xc7yxxFDDQNNTSSMKKqqq\xe1\xe1\xe1\xe6\xe6\xe6\xa7\xa6\xa6HFFXUUZWWXVV\x19\x1f"z|}wvu\xe3\xe3\xe3\xc5\xc5\xc5qpp>=<\x7f~~\xe2\xe2\xe2\xe3\xe3\xe3\xc8\xc7\xc7LJJUSSZWWZWWXVV$,1\x86\x89\x8aIHH\x99\x98\x98\xe1\xe1\xe1\xe0\xe0\xe0\xca\xca\xca\xe1\xe1\xe1\xe1\xe1\xe1\xda\xda\xda_^^ROOZWWZWWZWWXVVDKN\x91\x93\x95RQQLJJ\xb7\xb7\xb7\xdd\xdd\xdd\xdd\xdd\xdd\xdd\xdd\xdd\xda\xda\xda\x86\x85\x85LJIYVVZWWZWWZWWXVV@??\x9b\x9c\x9dZWWTQQTSS\xca\xca\xca\xd9\xd9\xd9\xd7\xd7\xd7\xac\xac\xacGFFWTTZWWZWWZWWZWW[XX2./\x83\x81\x82wuvWUUQOOfff\xd4\xd4\xd4\xc6\xc6\xc6PNNTQQZWWZWWZWWZWWZWWqop.**GEF\x9c\x9b\x9cwuv\\ZZNKK\x85\x84\x84onnOMMYVVZWWZWWZWW_^^wuu\x8c\x8a\x8b)((\'))C@Ayxy\x86\x88\x89\x8c\x8e\x8f\x86\x88\x89\x8d\x8d\x8e\x98\x98\x99\x9c\x9b\x9c\x9b\x9a\x9b\x9a\x98\x99\x99\x97\x97\x8d\x8b\x8csop844', dtype="uint8").reshape((16,16,3))
unchecked = numpy.frombuffer(b'UKHYOLf_]\x96\x98\x9c\xa6\xb2\xbf\xb1\xc7\xd8\xb3\xcf\xe1\xac\xc5\xd6\xa6\xba\xc9\x9f\xb0\xbe\x9b\xab\xb8\x9b\xa9\xb5\x99\xa5\xad\x8f\x98\xa1~\x88\x93P`qRGEe\\Y\xa3\x9e\x9cwvwXXYOLLOMMOMMOMMOMMOMMOMMOLLWXYx~\x84\x9d\xac\xb9MDA\x8a\x86\x83sopROOURRVSSVTTVTTVTTVTTVTTVTTVSSURRSQQsw|IB@\x9f\xa0\xa3WVWWTTYVVZWWZWWZWWZWWZWWZWWZWWZWWYVVWTTXVWTfu\xa5\xb8\xc7URRYVVZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWYVVWUU@b\x81\x92\x9f\xaaVSSZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWXVV\x1d/A\x8a\x90\x95VTTZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWXWW\x1b%/\x8a\x8e\x91VTTZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWXWW\x18\x1e#\x89\x8b\x8dVTTZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWXWW\x19\x1f"\x88\x8a\x8cVTTZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWXVV$,1\x8a\x8d\x8eVTTZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWXVVDKN\x91\x93\x95VTTZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWXVV@??\x9b\x9c\x9dZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWZWW[XX2./\x83\x81\x82wuvYVVZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWZWWqop.**GEF\x9c\x9b\x9cwuv]]]ZWWZWWZWWZWWZWWZWWZWWZWW_^^wuu\x8c\x8a\x8b)((\'))C@Ayxy\x86\x88\x89\x90\x93\x94\x92\x94\x96\x98\x98\x9a\x9b\x9b\x9c\x9c\x9b\x9c\x9b\x9a\x9b\x9a\x98\x99\x99\x97\x97\x8d\x8b\x8csop844', dtype="uint8").reshape((16,16,3))

class Getty_Image(Main_Page, BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filter = self.Filter(*args, **kwargs)
        self.video = Video(*args, **kwargs)
        self.photo = Photo(*args, **kwargs)

    @step('Handle What is Stock Media dialog')
    def handle_what_is_stock_media(self):
        if self.exist(L.gettyimage.what_is_stock_media_dialog):
            self.exist_click(L.gettyimage.what_is_stock_media_dialog_ok)
        return True

    @step('[Action][Getty Image] Switch to [Getty Image] tab in [Download from Shutterstock] window')
    def switch_to_GI(self):
        try:
            if not self.exist(L.download_from_shutterstock.window):
                logger("No window show up")
                raise Exception("No window show up")
            self.exist_click(L.gettyimage.gettyimage_tab)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def switch_to_SS(self):
        try:
            if not self.exist(L.download_from_shutterstock.window):
                logger("No window show up")
                raise Exception
            self.handle_what_is_stock_media()
            time.sleep(DELAY_TIME*2)
            self.exist_click(L.gettyimage.shutterstock_tab)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_my_favorites_button(self):
        try:
            if not self.exist(L.download_from_shutterstock.window):
                logger("No window show up")
                raise Exception
            self.exist_click(L.gettyimage.btn_favorite)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_purchased_button(self):
        try:
            if not self.exist(L.download_from_shutterstock.window):
                logger("No window show up")
                raise Exception
            self.exist_click(L.gettyimage.btn_purchased)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_downloaded_button(self):
        try:
            if not self.exist(L.download_from_shutterstock.window):
                logger("No window show up")
                raise Exception
            self.exist_click(L.gettyimage.btn_download)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def check_no_favorite_yet(self):
        try:
            if not self.exist(L.download_from_shutterstock.window):
                logger("No window show up")
                raise Exception
            self.is_exist(L.gettyimage.no_favorite_msg)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @step('[Action][Getty Image] Click [Filter] button')
    def click_filter_button(self):
        try:
            if not self.exist(L.download_from_shutterstock.window):
                logger("No window show up")
                raise Exception("No window show up")
            self.exist_click(L.gettyimage.btn_filter)
            time.sleep(DELAY_TIME*2)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception(f'Exception occurs. log={e}')
        return True

    def click_filter_explorer_view(self):
        try:
            if not self.exist(L.download_from_shutterstock.window):
                logger("No window show up")
                raise Exception
            self.exist_click(L.gettyimage.btn_filter_explorer_view)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_clear_all_button(self):
        try:
            if not self.exist(L.download_from_shutterstock.window):
                logger("No window show up")
                raise Exception
            self.exist_click(L.gettyimage.btn_clear_all)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_add_to_cart_button(self):
        try:
            if not self.exist(L.download_from_shutterstock.window):
                logger("No window show up")
                raise Exception
            self.exist_click(L.gettyimage.btn_add_to_cart)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def return_add_to_cart_button_status(self):
        try:
            if not self.exist(L.download_from_shutterstock.window):
                logger("No window show up")
                raise Exception
            if self.is_exist(L.gettyimage.btn_add_to_cart):
                return True
            else:
                return False
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception

    def click_bubble_proceed_checkout(self):
        try:
            if not self.exist(L.download_from_shutterstock.window):
                logger("No window show up")
                raise Exception
            self.exist_click(L.gettyimage.bubble_proceed_to_checkout)
            time.sleep(2)
            self.close_chrome_page()
            return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception

    def handle_checkout_is_complete_dialog(self, option):
        try:
            if not self.exist(L.download_from_shutterstock.window):
                logger("No window show up")
                raise Exception
            self.activate()
            time.sleep(DELAY_TIME)
            if option == 'next':
                self.click(L.gettyimage.btn_next_checkout_dialog)
            elif option == 'cancel':
                self.click(L.gettyimage.btn_cancel_checkout_dialog)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_bubble_cart(self):
        try:
            if not self.exist(L.download_from_shutterstock.window):
                logger("No window show up")
                raise Exception
            self.exist_click(L.gettyimage.bubble_cart)
            if not self.exist(L.gettyimage.cart_window):
                logger("No cart show up")
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_shopping_cart_button(self):
        try:
            if not self.exist(L.download_from_shutterstock.window):
                logger("No window show up")
                raise Exception
            self.exist_click(L.gettyimage.btn_cart)
            if not self.exist(L.gettyimage.cart_window):
                logger("No cart show up")
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def is_enter_shopping_cart_window(self):
        try:
            if not self.exist(L.gettyimage.cart_window):
                logger("No cart show up")
                raise Exception
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def click_trash_can(self):
        try:
            if not self.exist(L.gettyimage.cart_window):
                logger("No cart show up")
                raise Exception
            self.exist_click(L.gettyimage.trash_can_button)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise
        return True

    def shopping_cart_click_checkout_button(self):
        try:
            if not self.exist(L.gettyimage.cart_window):
                logger("No cart show up")
                raise Exception
            self.exist_click(L.gettyimage.btn_proceed_to_checkout)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception

        return True

    def shopping_cart_check_total_items(self):
        try:
            if not self.exist(L.gettyimage.cart_window):
                logger("No cart show up")
                raise Exception
            subtotal_text = self.exist(L.gettyimage.subtotal_text).AXValue
            dict = [int(temp) for temp in subtotal_text.split() if temp.isdigit()]
            return dict[0]
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception

    def click_heart_icon(self, index):
        try:
            if not self.exist(L.download_from_shutterstock.window):
                logger("No shutterstock window show up")
                raise Exception
            x, y = self.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': index}).AXPosition
            self.mouse.move(x, y)
            heart_icon = self.exist([{'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': index}, L.gettyimage.heart_icon])
            heart_icon_x, heart_icon_y = heart_icon.center
            self.mouse.click(heart_icon_x, heart_icon_y)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise
        return True

    def hover_heart_icon(self, index):
        try:
            if not self.exist(L.download_from_shutterstock.window):
                logger("No shutterstock window show up")
                raise Exception
            x_index, y_index = self.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': index}).AXPosition
            self.mouse.move(x_index, y_index)
            time.sleep(1)
            heart_icon = self.exist([{'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': index}, L.gettyimage.heart_icon])
            heart_icon_x, heart_icon_y = heart_icon.center
            self.mouse.move(heart_icon_x, heart_icon_y)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def handle_no_match_dialog(self):
        try:
            if not self.exist(L.download_from_shutterstock.window):
                logger("No shutterstock window show up")
                raise Exception
            if self.exist(L.gettyimage.no_match_dialog):
                self.exist_click(L.gettyimage.no_match_dialog_ok)
                return True
            else:
                return True
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception


    class Filter(Main_Page, BasePage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.video = self.Video(*args, **kwargs)
            self.photo = self.Photo(*args, **kwargs)

        def set_video_scroll_bar(self, value):
            try:
                if not self.exist(L.download_from_shutterstock.window):
                    logger("No window show up")
                    raise Exception
                scroll = self.exist(L.gettyimage.video.scroll_bar_filter)
                scroll.AXValue = value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def get_video_scroll_bar(self):
            try:
                if not self.exist(L.download_from_shutterstock.window):
                    logger("No window show up")
                    raise Exception
                scroll = self.exist(L.gettyimage.video.scroll_bar_filter)
                return scroll.AXValue
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        def set_photo_scroll_bar(self, value):
            try:
                if not self.exist(L.download_from_shutterstock.window):
                    logger("No window show up")
                    raise Exception
                scroll = self.exist(L.gettyimage.photo.scroll_bar_filter)
                scroll.AXValue = value
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
            return True

        def get_photo_scroll_bar(self):
            try:
                if not self.exist(L.download_from_shutterstock.window):
                    logger("No window show up")
                    raise Exception
                scroll = self.exist(L.gettyimage.photo.scroll_bar_filter)
                return scroll.AXValue
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        def set_sort_by_type(self, index):
            try:
                if not self.exist(L.download_from_shutterstock.window):
                    logger("No window show up")
                    raise Exception
                if index == 0:
                    self.exist_click(L.gettyimage.sort_by.best_matched)
                    return True
                elif index == 1:
                    self.exist_click(L.gettyimage.sort_by.newest)
                    return True
                elif index == 2:
                    self.exist_click(L.gettyimage.sort_by.random)
                    return True
                elif index == 3:
                    self.exist_click(L.gettyimage.sort_by.popular)
                    return True
                elif index == 4:
                    self.exist_click(L.gettyimage.sort_by.best_matched_photo)
                    return True
                elif index == 5:
                    self.exist_click(L.gettyimage.sort_by.newest_photo)
                    return True
                elif index == 6:
                    self.exist_click(L.gettyimage.sort_by.random_photo)
                    return True
                elif index == 7:
                    self.exist_click(L.gettyimage.sort_by.popular_photo)
                    return True
                else:
                    logger("No index")
                    raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        def get_collection_type(self, set_video=1):
            try:
                if not self.exist(L.download_from_shutterstock.window):
                    logger("No window show up")
                    raise Exception
                if set_video:
                    if self.exist(L.gettyimage.collection.all).AXValue == 1:
                        return self.exist(L.gettyimage.collection.all).AXTitle
                    elif self.exist(L.gettyimage.collection.subscription).AXValue == 1:
                        return self.exist(L.gettyimage.collection.subscription).AXTitle
                    elif self.exist(L.gettyimage.collection.premium).AXValue == 1:
                        return self.exist(L.gettyimage.collection.premium).AXTitle
                    else:
                        logger("No collection exist")
                        raise Exception
                else:
                    # For photo
                    if self.exist(L.gettyimage.collection.all_photo).AXValue == 1:
                        return self.exist(L.gettyimage.collection.all_photo).AXTitle
                    elif self.exist(L.gettyimage.collection.subscription_photo).AXValue == 1:
                        return self.exist(L.gettyimage.collection.subscription_photo).AXTitle
                    elif self.exist(L.gettyimage.collection.premium_photo).AXValue == 1:
                        return self.exist(L.gettyimage.collection.premium_photo).AXTitle
                    else:
                        logger("No collection exist")
                        raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception
        @step('[Action][Getty Image][Filter] Set collection type')
        def set_collection_type(self, index):
            try:
                if not self.exist(L.download_from_shutterstock.window):
                    logger("No window show up")
                    raise Exception("No window show up")
                if index == 0:
                    self.exist_click(L.gettyimage.collection.all)
                elif index == 1:
                    self.exist_click(L.gettyimage.collection.subscription)
                elif index == 2:
                    self.exist_click(L.gettyimage.collection.premium)
                elif index == 3:
                    self.exist_click(L.gettyimage.collection.all_photo)
                elif index == 4:
                    self.exist_click(L.gettyimage.collection.subscription_photo)
                elif index == 5:
                    self.exist_click(L.gettyimage.collection.premium_photo)
                else:
                    logger("No index")
                    raise Exception(f"No index, index={index}. Please provide index 0~5")
                time.sleep(DELAY_TIME*2)
                return True
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception(f'Exception occurs. log={e}')

        def get_sort_by_type(self, set_video=1):
            #set_video = 1 for Video
            #set_video = 0 for Photo
            try:
                if not self.exist(L.download_from_shutterstock.window):
                    logger("No window show up")
                    raise Exception
                if set_video:
                    if self.exist(L.gettyimage.sort_by.best_matched).AXValue == 1:
                        return self.exist(L.gettyimage.sort_by.best_matched).AXTitle
                    elif self.exist(L.gettyimage.sort_by.newest).AXValue == 1:
                        return self.exist(L.gettyimage.sort_by.newest).AXTitle
                    elif self.exist(L.gettyimage.sort_by.random).AXValue == 1:
                        return self.exist(L.gettyimage.sort_by.random).AXTitle
                    elif self.exist(L.gettyimage.sort_by.popular).AXValue == 1:
                        return self.exist(L.gettyimage.sort_by.popular).AXTitle
                    else:
                        logger("No collection exist")
                        raise Exception
                else:
                    if self.exist(L.gettyimage.sort_by.best_matched_photo).AXValue == 1:
                        return self.exist(L.gettyimage.sort_by.best_matched_photo).AXTitle
                    elif self.exist(L.gettyimage.sort_by.newest_photo).AXValue == 1:
                        return self.exist(L.gettyimage.sort_by.newest_photo).AXTitle
                    elif self.exist(L.gettyimage.sort_by.random_photo).AXValue == 1:
                        return self.exist(L.gettyimage.sort_by.random_photo).AXTitle
                    elif self.exist(L.gettyimage.sort_by.popular_photo).AXValue == 1:
                        return self.exist(L.gettyimage.sort_by.popular_photo).AXTitle
                    else:
                        logger("No collection exist")
                        raise Exception
            except Exception as e:
                logger(f'Exception occurs. log={e}')
                raise Exception

        class Video(Main_Page, BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.composition = self.Composition(*args, **kwargs)
                self.viewpoint = self.Viewpoint(*args, **kwargs)
                self.image_technique = self.Image_technique(*args, **kwargs)

            def set_duration_type(self, index):
                try:
                    if not self.exist(L.download_from_shutterstock.window):
                        logger("No window show up")
                        raise Exception
                    if index == 0:
                        self.exist_click(L.gettyimage.video.duration.all)
                        return True
                    elif index == 1:
                        self.exist_click(L.gettyimage.video.duration._30s)
                        return True
                    elif index == 2:
                        self.exist_click(L.gettyimage.video.duration._1min)
                        return True
                    elif index == 3:
                        self.exist_click(L.gettyimage.video.duration._2min)
                        return True
                    else:
                        logger("No index")
                        raise Exception
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception

            def get_duration_type(self):
                try:
                    if not self.exist(L.download_from_shutterstock.window):
                        logger("No window show up")
                        raise Exception
                    if self.exist(L.gettyimage.video.duration.all).AXValue == 1:
                        return self.exist(L.gettyimage.video.duration.all).AXTitle
                    elif self.exist(L.gettyimage.video.duration._30s).AXValue == 1:
                        return self.exist(L.gettyimage.video.duration._30s).AXTitle
                    elif self.exist(L.gettyimage.video.duration._1min).AXValue == 1:
                        return self.exist(L.gettyimage.video.duration._1min).AXTitle
                    elif self.exist(L.gettyimage.video.duration._2min).AXValue == 1:
                        return self.exist(L.gettyimage.video.duration._2min).AXTitle
                    else:
                        logger("No collection exist")
                        raise Exception
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception

            def set_resolution_type(self, index):
                try:
                    if not self.exist(L.download_from_shutterstock.window):
                        logger("No window show up")
                        raise Exception
                    if index == 0:
                        self.exist_click(L.gettyimage.video.resolution.all)
                        return True
                    elif index == 1:
                        self.exist_click(L.gettyimage.video.resolution._4k)
                        return True
                    elif index == 2:
                        self.exist_click(L.gettyimage.video.resolution.hd)
                        return True
                    elif index == 3:
                        self.exist_click(L.gettyimage.video.resolution.sd)
                        return True
                    else:
                        logger("No index")
                        raise Exception
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception

            def get_resolution_type(self):
                try:
                    if not self.exist(L.download_from_shutterstock.window):
                        logger("No window show up")
                        raise Exception
                    if self.exist(L.gettyimage.video.resolution.all).AXValue == 1:
                        return self.exist(L.gettyimage.video.resolution.all).AXTitle
                    elif self.exist(L.gettyimage.video.resolution._4k).AXValue == 1:
                        return self.exist(L.gettyimage.video.resolution._4k).AXTitle
                    elif self.exist(L.gettyimage.video.resolution.hd).AXValue == 1:
                        return self.exist(L.gettyimage.video.resolution.hd).AXTitle
                    elif self.exist(L.gettyimage.video.resolution.sd).AXValue == 1:
                        return self.exist(L.gettyimage.video.resolution.sd).AXTitle
                    else:
                        logger("No collection exist")
                        raise Exception
                except Exception as e:
                    logger(f'Exception occurs. log={e}')
                    raise Exception

            class Composition(Main_Page, BasePage):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                def set_close_up(self, check):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if check == 0:
                            if self.exist(L.gettyimage.video.composition.close_up).AXValue == 0:
                                return True
                            elif self.exist(L.gettyimage.video.composition.close_up).AXValue == 1:
                                self.exist_click(L.gettyimage.video.composition.close_up)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        elif check == 1:
                            if self.exist(L.gettyimage.video.composition.close_up).AXValue == 1:
                                return True
                            elif self.exist(L.gettyimage.video.composition.close_up).AXValue == 0:
                                self.exist_click(L.gettyimage.video.composition.close_up)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        else:
                            logger('No bCheck')
                            raise Exception
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_close_up(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.video.composition.close_up).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def set_candid(self, check):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if check == 0:
                            if self.exist(L.gettyimage.video.composition.candid).AXValue == 0:
                                return True
                            elif self.exist(L.gettyimage.video.composition.candid).AXValue == 1:
                                self.exist_click(L.gettyimage.video.composition.candid)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        elif check == 1:
                            if self.exist(L.gettyimage.video.composition.candid).AXValue == 1:
                                return True
                            elif self.exist(L.gettyimage.video.composition.candid).AXValue == 0:
                                self.exist_click(L.gettyimage.video.composition.candid)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        else:
                            logger('No bCheck')
                            raise Exception
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_candid(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.video.composition.candid).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def set_looking(self, check):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if check == 0:
                            if self.exist(L.gettyimage.video.composition.looking).AXValue == 0:
                                return True
                            elif self.exist(L.gettyimage.video.composition.looking).AXValue == 1:
                                self.exist_click(L.gettyimage.video.composition.looking)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        elif check == 1:
                            if self.exist(L.gettyimage.video.composition.looking).AXValue == 1:
                                return True
                            elif self.exist(L.gettyimage.video.composition.looking).AXValue == 0:
                                self.exist_click(L.gettyimage.video.composition.looking)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        else:
                            logger('No bCheck')
                            raise Exception
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_looking(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.video.composition.looking).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

            class Viewpoint(Main_Page, BasePage):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                def set_lockdown(self, check):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if check == 0:
                            if self.exist(L.gettyimage.video.viewpoint.lockdown).AXValue == 0:
                                return True
                            elif self.exist(L.gettyimage.video.viewpoint.lockdown).AXValue == 1:
                                self.exist_click(L.gettyimage.video.viewpoint.lockdown)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        elif check == 1:
                            if self.exist(L.gettyimage.video.viewpoint.lockdown).AXValue == 1:
                                return True
                            elif self.exist(L.gettyimage.video.viewpoint.lockdown).AXValue == 0:
                                self.exist_click(L.gettyimage.video.viewpoint.lockdown)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        else:
                            logger('No bCheck')
                            raise Exception
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_lockdown(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.video.viewpoint.lockdown).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def set_panning(self, check):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if check == 0:
                            if self.exist(L.gettyimage.video.viewpoint.panning).AXValue == 0:
                                return True
                            elif self.exist(L.gettyimage.video.viewpoint.panning).AXValue == 1:
                                self.exist_click(L.gettyimage.video.viewpoint.panning)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        elif check == 1:
                            if self.exist(L.gettyimage.video.viewpoint.panning).AXValue == 1:
                                return True
                            elif self.exist(L.gettyimage.video.viewpoint.panning).AXValue == 0:
                                self.exist_click(L.gettyimage.video.viewpoint.panning)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        else:
                            logger('No bCheck')
                            raise Exception
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_panning(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.video.viewpoint.panning).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def set_tracking_shot(self, check):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if check == 0:
                            if self.exist(L.gettyimage.video.viewpoint.tracking_shot).AXValue == 0:
                                return True
                            elif self.exist(L.gettyimage.video.viewpoint.tracking_shot).AXValue == 1:
                                self.exist_click(L.gettyimage.video.viewpoint.tracking_shot)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        elif check == 1:
                            if self.exist(L.gettyimage.video.viewpoint.tracking_shot).AXValue == 1:
                                return True
                            elif self.exist(L.gettyimage.video.viewpoint.tracking_shot).AXValue == 0:
                                self.exist_click(L.gettyimage.video.viewpoint.tracking_shot)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        else:
                            logger('No bCheck')
                            raise Exception
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_tracking_shot(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.video.viewpoint.tracking_shot).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise

                def set_aerial_view(self, check):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if check == 0:
                            if self.exist(L.gettyimage.video.viewpoint.aerial_view).AXValue == 0:
                                return True
                            elif self.exist(L.gettyimage.video.viewpoint.aerial_view).AXValue == 1:
                                self.exist_click(L.gettyimage.video.viewpoint.aerial_view)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        elif check == 1:
                            if self.exist(L.gettyimage.video.viewpoint.aerial_view).AXValue == 1:
                                return True
                            elif self.exist(L.gettyimage.video.viewpoint.aerial_view).AXValue == 0:
                                self.exist_click(L.gettyimage.video.viewpoint.aerial_view)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        else:
                            logger('No bCheck')
                            raise Exception
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_aerial_view(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.video.viewpoint.aerial_view).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def set_high_angle(self, check):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if check == 0:
                            if self.exist(L.gettyimage.video.viewpoint.high_angle).AXValue == 0:
                                return True
                            elif self.exist(L.gettyimage.video.viewpoint.high_angle).AXValue == 1:
                                self.exist_click(L.gettyimage.video.viewpoint.high_angle)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        elif check == 1:
                            if self.exist(L.gettyimage.video.viewpoint.high_angle).AXValue == 1:
                                return True
                            elif self.exist(L.gettyimage.video.viewpoint.high_angle).AXValue == 0:
                                self.exist_click(L.gettyimage.video.viewpoint.high_angle)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        else:
                            logger('No bCheck')
                            raise Exception
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_high_angle(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.video.viewpoint.high_angle).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def set_low_angle(self, check):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if check == 0:
                            if self.exist(L.gettyimage.video.viewpoint.low_angle).AXValue == 0:
                                return True
                            elif self.exist(L.gettyimage.video.viewpoint.low_angle).AXValue == 1:
                                self.exist_click(L.gettyimage.video.viewpoint.low_angle)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        elif check == 1:
                            if self.exist(L.gettyimage.video.viewpoint.low_angle).AXValue == 1:
                                return True
                            elif self.exist(L.gettyimage.video.viewpoint.low_angle).AXValue == 0:
                                self.exist_click(L.gettyimage.video.viewpoint.low_angle)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        else:
                            logger('No bCheck')
                            raise Exception
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_low_angle(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.video.viewpoint.low_angle).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def set_tilt(self, check):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if check == 0:
                            if self.exist(L.gettyimage.video.viewpoint.tilt).AXValue == 0:
                                return True
                            elif self.exist(L.gettyimage.video.viewpoint.tilt).AXValue == 1:
                                self.exist_click(L.gettyimage.video.viewpoint.tilt)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        elif check == 1:
                            if self.exist(L.gettyimage.video.viewpoint.tilt).AXValue == 1:
                                return True
                            elif self.exist(L.gettyimage.video.viewpoint.tilt).AXValue == 0:
                                self.exist_click(L.gettyimage.video.viewpoint.tilt)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        else:
                            logger('No bCheck')
                            raise Exception
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_tilt(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.video.viewpoint.tilt).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def set_point_view(self, check):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if check == 0:
                            if self.exist(L.gettyimage.video.viewpoint.point_view).AXValue == 0:
                                return True
                            elif self.exist(L.gettyimage.video.viewpoint.point_view).AXValue == 1:
                                self.exist_click(L.gettyimage.video.viewpoint.point_view)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        elif check == 1:
                            if self.exist(L.gettyimage.video.viewpoint.point_view).AXValue == 1:
                                return True
                            elif self.exist(L.gettyimage.video.viewpoint.point_view).AXValue == 0:
                                self.exist_click(L.gettyimage.video.viewpoint.point_view)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        else:
                            logger('No bCheck')
                            raise Exception
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_point_view(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.video.viewpoint.point_view).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

            class Image_technique(Main_Page, BasePage):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                def set_real_time(self, check):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if check == 0:
                            if self.exist(L.gettyimage.video.image_technique.real_time).AXValue == 0:
                                return True
                            elif self.exist(L.gettyimage.video.image_technique.real_time).AXValue == 1:
                                self.exist_click(L.gettyimage.video.image_technique.real_time)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        elif check == 1:
                            if self.exist(L.gettyimage.video.image_technique.real_time).AXValue == 1:
                                return True
                            elif self.exist(L.gettyimage.video.image_technique.real_time).AXValue == 0:
                                self.exist_click(L.gettyimage.video.image_technique.real_time)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        else:
                            logger('No bCheck')
                            raise Exception
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_real_time(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.video.image_technique.real_time).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def set_time_lapse(self, check):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if check == 0:
                            if self.exist(L.gettyimage.video.image_technique.time_lapse).AXValue == 0:
                                return True
                            elif self.exist(L.gettyimage.video.image_technique.time_lapse).AXValue == 1:
                                self.exist_click(L.gettyimage.video.image_technique.time_lapse)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        elif check == 1:
                            if self.exist(L.gettyimage.video.image_technique.time_lapse).AXValue == 1:
                                return True
                            elif self.exist(L.gettyimage.video.image_technique.time_lapse).AXValue == 0:
                                self.exist_click(L.gettyimage.video.image_technique.time_lapse)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        else:
                            logger('No bCheck')
                            raise Exception
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_time_lapse(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.video.image_technique.time_lapse).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def set_slow_motion(self, check):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if check == 0:
                            if self.exist(L.gettyimage.video.image_technique.slow_motion).AXValue == 0:
                                return True
                            elif self.exist(L.gettyimage.video.image_technique.slow_motion).AXValue == 1:
                                self.exist_click(L.gettyimage.video.image_technique.slow_motion)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        elif check == 1:
                            if self.exist(L.gettyimage.video.image_technique.slow_motion).AXValue == 1:
                                return True
                            elif self.exist(L.gettyimage.video.image_technique.slow_motion).AXValue == 0:
                                self.exist_click(L.gettyimage.video.image_technique.slow_motion)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        else:
                            logger('No bCheck')
                            raise Exception
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_slow_motion(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.video.image_technique.slow_motion).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def set_color(self, check):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if check == 0:
                            if self.exist(L.gettyimage.video.image_technique.color).AXValue == 0:
                                return True
                            elif self.exist(L.gettyimage.video.image_technique.color).AXValue == 1:
                                self.exist_click(L.gettyimage.video.image_technique.color)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        elif check == 1:
                            if self.exist(L.gettyimage.video.image_technique.color).AXValue == 1:
                                return True
                            elif self.exist(L.gettyimage.video.image_technique.color).AXValue == 0:
                                self.exist_click(L.gettyimage.video.image_technique.color)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        else:
                            logger('No bCheck')
                            raise Exception
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_color(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.video.image_technique.color).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def set_black_white(self, check):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if check == 0:
                            if self.exist(L.gettyimage.video.image_technique.black_white).AXValue == 0:
                                return True
                            elif self.exist(L.gettyimage.video.image_technique.black_white).AXValue == 1:
                                self.exist_click(L.gettyimage.video.image_technique.black_white)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        elif check == 1:
                            if self.exist(L.gettyimage.video.image_technique.black_white).AXValue == 1:
                                return True
                            elif self.exist(L.gettyimage.video.image_technique.black_white).AXValue == 0:
                                self.exist_click(L.gettyimage.video.image_technique.black_white)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        else:
                            logger('No bCheck')
                            raise Exception
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_black_white(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.video.image_technique.black_white).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def set_animation(self, check):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if check == 0:
                            if self.exist(L.gettyimage.video.image_technique.animation).AXValue == 0:
                                return True
                            elif self.exist(L.gettyimage.video.image_technique.animation).AXValue == 1:
                                self.exist_click(L.gettyimage.video.image_technique.animation)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        elif check == 1:
                            if self.exist(L.gettyimage.video.image_technique.animation).AXValue == 1:
                                return True
                            elif self.exist(L.gettyimage.video.image_technique.animation).AXValue == 0:
                                self.exist_click(L.gettyimage.video.image_technique.animation)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        else:
                            logger('No bCheck')
                            raise Exception
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_animation(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.video.image_technique.animation).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def set_selective_focus(self, check):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if check == 0:
                            if self.exist(L.gettyimage.video.image_technique.selective_focus).AXValue == 0:
                                return True
                            elif self.exist(L.gettyimage.video.image_technique.selective_focus).AXValue == 1:
                                self.exist_click(L.gettyimage.video.image_technique.selective_focus)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        elif check == 1:
                            if self.exist(L.gettyimage.video.image_technique.selective_focus).AXValue == 1:
                                return True
                            elif self.exist(L.gettyimage.video.image_technique.selective_focus).AXValue == 0:
                                self.exist_click(L.gettyimage.video.image_technique.selective_focus)
                                return True
                            else:
                                logger('No close up checkbox')
                                raise Exception
                        else:
                            logger('No bCheck')
                            raise Exception
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_selective_focus(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.video.image_technique.selective_focus).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

        class Photo(Main_Page, BasePage):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.orientation = self.Orientation(*args, **kwargs)
                self.image_style = self.Image_Style(*args, **kwargs)
                self.number_people = self.Number_People(*args, **kwargs)

            class Orientation(Main_Page, BasePage):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                def set_vertical(self, bcheck=1):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if bcheck != self.exist(L.gettyimage.photo.orientation.vertical_chx).AXValue:
                            self.exist_click(L.gettyimage.photo.orientation.vertical_chx)
                            time.sleep(DELAY_TIME * 5)
                            return True
                        else:
                            return True

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_vertical(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.photo.orientation.vertical_chx).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def set_horizontal(self, bcheck=1):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if bcheck != self.exist(L.gettyimage.photo.orientation.horizontal_chx).AXValue:
                            self.exist_click(L.gettyimage.photo.orientation.horizontal_chx)
                            time.sleep(DELAY_TIME * 5)
                            return True
                        else:
                            return True

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_horizontal(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.photo.orientation.horizontal_chx).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def set_square(self, bcheck=1):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if bcheck != self.exist(L.gettyimage.photo.orientation.square_chx).AXValue:
                            self.exist_click(L.gettyimage.photo.orientation.square_chx)
                            time.sleep(DELAY_TIME * 5)
                            return True
                        else:
                            return True

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_square(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.photo.orientation.square_chx).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def set_panoramic(self, bcheck=1):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if bcheck != self.exist(L.gettyimage.photo.orientation.panoramic_chx).AXValue:
                            self.exist_click(L.gettyimage.photo.orientation.panoramic_chx)
                            time.sleep(DELAY_TIME * 5)
                            return True
                        else:
                            return True

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_panoramic(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.photo.orientation.panoramic_chx).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

            class Image_Style(Main_Page, BasePage):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                def set_abstract(self, bcheck=1):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if bcheck != self.exist(L.gettyimage.photo.image_style.abstract_chx).AXValue:
                            self.exist_click(L.gettyimage.photo.image_style.abstract_chx)
                            time.sleep(DELAY_TIME * 5)
                            return True
                        else:
                            return True

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_abstract(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.photo.image_style.abstract_chx).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def set_portrait(self, bcheck=1):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if bcheck != self.exist(L.gettyimage.photo.image_style.portrait_chx).AXValue:
                            self.exist_click(L.gettyimage.photo.image_style.portrait_chx)
                            time.sleep(DELAY_TIME * 5)
                            return True
                        else:
                            return True

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_portrait(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.photo.image_style.portrait_chx).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def set_close_up(self, bcheck=1):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if bcheck != self.exist(L.gettyimage.photo.image_style.close_up_chx).AXValue:
                            self.exist_click(L.gettyimage.photo.image_style.close_up_chx)
                            time.sleep(DELAY_TIME * 5)
                            return True
                        else:
                            return True

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_close_up(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.photo.image_style.close_up_chx).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def set_sparse(self, bcheck=1):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if bcheck != self.exist(L.gettyimage.photo.image_style.sparse_chx).AXValue:
                            self.exist_click(L.gettyimage.photo.image_style.sparse_chx)
                            time.sleep(DELAY_TIME * 5)
                            return True
                        else:
                            return True

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_sparse(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.photo.image_style.sparse_chx).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception


                def set_cut_out(self, bcheck=1):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if bcheck != self.exist(L.gettyimage.photo.image_style.cut_out_chx).AXValue:
                            self.exist_click(L.gettyimage.photo.image_style.cut_out_chx)
                            time.sleep(DELAY_TIME * 5)
                            return True
                        else:
                            return True

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_cut_out(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.photo.image_style.cut_out_chx).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def set_full_frame(self, bcheck=1):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if bcheck != self.exist(L.gettyimage.photo.image_style.full_frame_chx).AXValue:
                            self.exist_click(L.gettyimage.photo.image_style.full_frame_chx)
                            time.sleep(DELAY_TIME * 5)
                            return True
                        else:
                            return True

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_full_frame(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.photo.image_style.full_frame_chx).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception


                def set_copy_space(self, bcheck=1):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if bcheck != self.exist(L.gettyimage.photo.image_style.copy_space_chx).AXValue:
                            self.exist_click(L.gettyimage.photo.image_style.copy_space_chx)
                            time.sleep(DELAY_TIME * 5)
                            return True
                        else:
                            return True

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_copy_space(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.photo.image_style.copy_space_chx).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def set_macro(self, bcheck=1):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if bcheck != self.exist(L.gettyimage.photo.image_style.macro_chx).AXValue:
                            self.exist_click(L.gettyimage.photo.image_style.macro_chx)
                            time.sleep(DELAY_TIME * 5)
                            return True
                        else:
                            return True

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_macro(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.photo.image_style.macro_chx).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def set_still_life(self, bcheck=1):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if bcheck != self.exist(L.gettyimage.photo.image_style.still_life_chx).AXValue:
                            self.exist_click(L.gettyimage.photo.image_style.still_life_chx)
                            time.sleep(DELAY_TIME * 5)
                            return True
                        else:
                            return True

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_still_life(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.photo.image_style.still_life_chx).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

            class Number_People(Main_Page, BasePage):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                def set_no(self, bcheck=1):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if bcheck != self.exist(L.gettyimage.photo.number_people.no_people_chx).AXValue:
                            self.exist_click(L.gettyimage.photo.number_people.no_people_chx)
                            time.sleep(DELAY_TIME * 5)
                            return True
                        else:
                            return True

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_no(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.photo.number_people.no_people_chx).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def set_one(self, bcheck=1):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if bcheck != self.exist(L.gettyimage.photo.number_people.one_person_chx).AXValue:
                            self.exist_click(L.gettyimage.photo.number_people.one_person_chx)
                            time.sleep(DELAY_TIME * 5)
                            return True
                        else:
                            return True

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_one(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.photo.number_people.one_person_chx).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def set_two(self, bcheck=1):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if bcheck != self.exist(L.gettyimage.photo.number_people.two_people_chx).AXValue:
                            self.exist_click(L.gettyimage.photo.number_people.two_people_chx)
                            time.sleep(DELAY_TIME * 5)
                            return True
                        else:
                            return True

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_two(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.photo.number_people.two_people_chx).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def set_group(self, bcheck=1):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        if bcheck != self.exist(L.gettyimage.photo.number_people.group_people_chx).AXValue:
                            self.exist_click(L.gettyimage.photo.number_people.group_people_chx)
                            time.sleep(DELAY_TIME * 5)
                            return True
                        else:
                            return True

                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception

                def get_group(self):
                    try:
                        if not self.exist(L.download_from_shutterstock.window):
                            logger("No window show up")
                            raise Exception
                        return self.exist(L.gettyimage.photo.number_people.group_people_chx).AXValue
                    except Exception as e:
                        logger(f'Exception occurs. log={e}')
                        raise Exception


class Video(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.refreshed = False

    def _refresh_media(self):
        self.activate()
        if not self.refreshed:
            scroll = self.exist(L.gettyimage.scroll_media)
            temp = scroll.AXValue
            for i in range(5):
                scroll.AXValue = (i+1)/5
            scroll.AXValue = temp
            self.refreshed = True

    def hover_thumbnail(self, index, _scroll_only=False):
        self._refresh_media()
        boundary = (_ := self.exist(L.gettyimage.frame_scroll_view)).AXPosition + _.AXSize
        target = self.exist(L.gettyimage.frame_clips)[index]
        x0, y0 = target.center
        if not (boundary[1] < y0 < boundary[1] + boundary[3]):
            y_long, y_top = (_:=self.exist(L.gettyimage.frame_section)).AXSize[1], _.AXPosition[1]
            percentage = (y0 - y_top - boundary[3]/2) / (y_long-boundary[3])
            self.exist(L.gettyimage.scroll_media).AXValue = percentage
            time.sleep(0.5)
        if not _scroll_only: self.mouse.move(*target.center)
        return True

    def _get_selection_list(self, index=None):
        self._refresh_media()
        pos = self.mouse.position()
        top = self.get_top()
        _index = index.copy() if index else None
        self.activate()
        boundary = (_ := self.exist(L.gettyimage.frame_scroll_view)).AXPosition + _.AXSize
        clips = self.exist(L.gettyimage.frame_clips)
        if index:
            _clips = []
            for i in index:
                _clips.append(clips[i])
            clips = _clips
        els = []
        for clip in clips:
            if _index: self.hover_thumbnail(_index.pop(0),_scroll_only= True)
            x, y = [x + [clip.AXSize[0] - 5, +5][i] for i, x in enumerate(clip.AXPosition)]
            if (boundary[0] < x < boundary[0] + boundary[2]) and (boundary[1] < y < boundary[1] + boundary[3]):
                self.mouse.move(x, y, 0, wait=0.3)
                el = top.with_ref(top.getElementAtPosition((x, y)))
                els.append(el)  # if el.AXRole == "AXButton" else None
            else:
                els.append(None)
        self.mouse.move(*pos, 0, wait=0)
        return els

    def get_selected_list(self, _checkboxes = None, _click_list=None, _unclick_list=None):
        self._refresh_media()
        ret = []
        click_list = _click_list or []
        unclick_list = _unclick_list or []
        pos = self.mouse.position()
        checkboxes = _checkboxes or self._get_selection_list()
        # self.mouse.move(0,0) # by Jim - to capture the image of checkbox correctly
        full_screen = cv2.imread(self.driver.image.screenshot(), cv2.IMREAD_COLOR)
        logger(f"{checkboxes=}")
        for i, checkbox in enumerate(checkboxes):
            if not checkbox: continue
            logger(f"{checkbox=}")
            x, y, w, h = map(int, (*checkbox.AXPosition, *checkbox.AXSize))
            logger(f"{x=} / {y=} / {w=} / {h=} ")
            img1 = full_screen[y:y+h, x:x+w]
            img2 = numpy.fromstring(checked, dtype="uint8").reshape((h,w,3))
            res = cv2.matchTemplate(img1[2:-2, 2:-2], img2, 5)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            logger(f"{min_val=} /{max_val=} /{min_loc=} /{max_loc=}")
            if max_val > 0.85:
                logger(f"index-{i} : True")
                ret.append(i)
                if i in unclick_list or len(unclick_list) > 0 and unclick_list[0] == -1:
                    logger(f"unselect - {list(map(int,(x+w/2,y+h/2)))}", function="unselect_clip")
                    self.mouse.click(int(x+w/2),int(y+h/2))
            else:
                logger(f"index-{i} : False")
                if i in click_list or len(click_list) > 0 and click_list[0] == -1:
                    logger(f"select - {list(map(int, (x + w / 2, y + h / 2)))}", function="select_clip")
                    self.mouse.click(int(x+w/2),int(y+h/2))
        self.mouse.move(*pos, 0, wait=0)
        return ret

    def select_clip(self, value):
        self._refresh_media()
        mylist = value if isinstance(value, (list, tuple)) else [value]
        for index in mylist:
            self.hover_thumbnail(index)
            checkbox = self._get_selection_list([index])
            self.get_selected_list(_checkboxes=checkbox, _click_list=[-1])
        return True

    def unselect_clip(self, value):
        self._refresh_media()
        mylist = value if isinstance(value, (list, tuple)) else [value]
        for index in mylist:
            self.hover_thumbnail(index)
            checkbox = self._get_selection_list([index])
            self.get_selected_list(_checkboxes=checkbox, _unclick_list=[-1])
        return True

    def get_clip_status(self, value):
        self._refresh_media()
        self.hover_thumbnail(value)
        checkbox = self._get_selection_list([value])[0]
        return bool(self.get_selected_list([checkbox]))


class Photo(Video):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_thumbnail_raw_data(self, index, hovered=True):
        target = L.gettyimage.image_clip.copy()
        target["index"] = index
        img = self.exist(target)
        x, y, w, h = map(int, (*img.AXPosition, *img.AXSize))
        pos = self.mouse.position()
        if not hovered: self.mouse.move(0, 0, 0, 0)
        full_screen = cv2.imread(self.driver.image.screenshot(), 1)
        if not hovered: self.mouse.move(*pos, 0, 0)
        return full_screen[y:y+h, x:x+w]

    def get_clip_status(self,index):
        def get_res(img1, img2, similarity=0.8):
            res = cv2.matchTemplate(img1[1:, 2:], img2[1:, 2:], 5)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            return True if max_val >= similarity else False

        self._refresh_media()
        self.hover_thumbnail(index)
        thumbnail = self._get_thumbnail_raw_data(index, hovered=True)
        if get_res(thumbnail, checked):
            return True
        elif get_res(thumbnail, unchecked):
            return False
        else:
            return None

    def select_clip(self, value, _select=True, _force=False):
        self._refresh_media()
        mylist = value if isinstance(value, (list, tuple)) else [value]
        for index in mylist:
            target = L.gettyimage.image_clip.copy()
            target["index"] = index

            status = self.get_clip_status(index)
            logger(f"target is ticked? {status}")

            img = self.exist(target)
            x, y, w, h = map(int, (*img.AXPosition, *img.AXSize))
            x_new = int(x + w/2)
            y_new = int(y + h*3/4)

            if status is None:
                continue
            elif status is not _select or _force:
                logger(f"click position {x_new}, {y_new}")
                self.mouse.click(x_new, y_new)
        return True

    def unselect_clip(self, value):
        return self.select_clip(value, False)




















































































































