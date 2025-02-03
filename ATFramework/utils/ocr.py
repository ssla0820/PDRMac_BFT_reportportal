import os
import configparser
import numpy
import platform

import cv2

from .log import logger
try:
    import pytesseract
    from PIL import Image, ImageEnhance, ImageFilter
except Exception as e:
    logger(f"[Warning] {e}")

def modi_conf(fn):
    def tofloat(n):
        try:
            return float(n)
        except:
            return -1

    def wrap(self, *args, **kwargs):
        ret = fn(self, *args, **kwargs)
        if conf := ret.get('conf'): ret['conf'] = [tofloat(x) for x in conf]
        return ret

    return wrap
try:
    setattr(pytesseract, "image_to_data", modi_conf(getattr(pytesseract, "image_to_data")))
except:
    pass



# ==================================================================================================================
# Class: OCR
# Description: optical character recognize
# functions:
#   - analyze():
#      | analyze()    , ex: OCR(photo_path, 'CyberLink').analyze()
#   - get_count():
#      | get_count()    , ex: OCR(photo_path, 'Version').get_count()
#   - get_pos(index):
#      | get_pos(index)    , ex: OCR(photo_path, 'SR').get_pos(1)
# Note: pytesseract(GitHub: https://github.com/tesseract-ocr/tesseract/wiki)
# Author: Terence
# Revise: v1.0 (1st version)
#         v1.1 (add 2 more img filter/img enhancement for high accuracy (2019/12/27)
#         v1.2 (add extend the width size for more accuracy) (2020/01/16)
#         v1.3 (add cv2 as method 4 & 5 to handle black background with white text)  (2020/01/17)
#         v1.3.1 (add tracking log to analyze)  (2020/01/21)
#         v1.4 (implement database analyzing system)    (2020/01/22)
#         v1.4.1 (add threshold(=127) method)   (2020/02/06)
#         v1.5 (method 7, BGR to HSV and filter blue/reverse/threshold/blur)    (2020/02/24)
#         v1.6 (fix multi-index cases)      (2020/06/29)
#         v1.7 (1)refine tolerance argument, (2)add str format index(ex: '2/3'), (3)sort out feature    (2020/07/28)
#         v1.8 porting PDVD highlighted text(small pixel text), new algorithm  (2020/07/31)
#         v1.8.1 fix pytesseract error(returned 'level' length doesn't match the length of 'text')      (2020/08/24)
#         v1.8.2 use pos y-axis as sort by ref.     (2020/10/06)
# ==================================================================================================================

# assign pytesseract path
if platform.system() == 'Windows':
    pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files (x86)\Tesseract-OCR\\tesseract.exe'

class OCR(object):
    # initial
    def __init__(self, target_img_path, target_text, default_conf=30):
        # make sure target_text is text
        if type(target_text) is str:
            self.img = target_img_path
            self.text = str(target_text)
            self.default_conf = default_conf
            self.conf = None
            self.im = None
            self.im_cv2 = None
            self.im_temp = None
            self.resize_im = None
            self.resize_im_cv = None
            self.size = ()
            self.data = None
            self.count = 0
            self.result_dict = {}
            self.pos = None
        else:
            logger(f"target text isn't string. {target_text}")

    # in order to analyze and create dictionary
    # return value: False or Dict. (ex: {1: (200, 500), 2: (100, 400)}
    def analyze(self, search_index=1, im=None):
        """
        index : 2 formats: (2020/7/28)
          => 1: int , direct use the index
          => 2: str (ex: '2/3') , 1st number(2) is target, 2nd number(3) is total,
                would detect if finding 3 index then return 2nd position
        :param search_index:
        :return: result (result format:  ex: {1: (363, 125), 2: (333, 555)}  )
        """
        try:
            # resize image x1.5 to x2.3
            resize_range = [
                1,
                1.5,
                2.3,
                1.7,
                2.0,
                2.1
            ]
            # check if has analyze data
            analyze = self.log_ReadTextData()
            # scan all case if no data
            if analyze is None:
                # scan all data
                logger(f'analyze: 1st time search(No Data)')
                for x in range(len(resize_range)):
                    method, result = self.scan_all(resize_range[x], search_index, im)
                    if len(result) != 0:
                        # write to data
                        method_str = f'method{str(method)}'
                        self.log_OKData(resize_range[x], method_str)
                        self.log_WriteTextData(resize_range[x], method_str)
                        return result
                return 0

            # scan the ratio_method in data
            for obj in range(len(analyze)):
                logger(f'analyze: search database')
                # jump to which resize_range
                resize_range_index = resize_range.index(float(analyze[obj].split('_')[0]))
                # jump to method
                method = int(analyze[obj].split('_')[1][6:])
                logger(f'setting is : {analyze[obj]}')
                # start to scan
                result = self.scan_method(method, resize_range[resize_range_index], im)
                if len(result) != 0:
                    # write to data
                    method_str = f'method{str(method)}'
                    self.log_OKData(resize_range[resize_range_index], method_str)
                    # check if search_index is int or str
                    # |int: directly use int
                    # |str(ex:'2/3'): total index should be 3, and return 2nd position
                    if type(search_index) is int:
                        if search_index <= len(result):
                            return result
                    elif type(search_index) is str:
                        if '/' in search_index:
                            target_index, total_index = search_index.split('/')
                            target_index = int(target_index)
                            total_index = int(total_index)
                        if len(result) >= total_index:
                            return result

            # still can't find result case even use data (scan all again)
            # scan all data
            logger(f"analyze: 2st time search(has data but no result)")
            for x in range(len(resize_range)):
                method, result = self.scan_all(resize_range[x], search_index, im)
                if len(result) != 0:
                    # write to data
                    method_str = f'method{str(method)}'
                    self.log_OKData(resize_range[x], method_str)
                    self.log_WriteTextData(resize_range[x], method_str)
                    # |str(ex:'2/3'): total index should be 3, and return 2nd position
                    if type(search_index) is int:
                        if search_index <= len(result):
                            return result
                    elif type(search_index) is str:
                        if '/' in search_index:
                            target_index, total_index = search_index.split('/')
                            target_index = int(target_index)
                            total_index = int(total_index)
                        if len(result) >= total_index:
                            return result
            return 0
        except Exception as e:
            logger(f'analyze:Exception: ({e})')
            return False

    def read_im_via_PIL(self):
        """
        PIL method
        :return: im(PIL format) list: [im,
                                       im_cv2,
                                       w,
                                       h]
        """
        im = Image.open(self.img)
        w, h = im.size
        im_cv2 = cv2.imread(self.img)
        return [im, im_cv2, w, h]

    def scan_method(self, method, resize_range, im=None):
        """
        :param method:
        :param resize_range:
        :param crop: None/['axis', 'proportion' ]
        :return: pos dict. (ex: {1: (200, 300), 2: (300, 400)}
        """
        # define numpy
        np = numpy
        # define tolerance
        # ex: find 2 position (100, 105), (102, 105), if tolerance is +-2, then skip 1 position and return 1 position
        tolerance = 3
        tolerance_list = []
        for t in range(tolerance * 2 + 1):
            tolerance_list.append(t - tolerance)

        # determine if img exists
        for y in range(3):  # for file handle(avoid getting fail)
            if os.path.isfile(self.img):
                break
            else:
                if y == 2:
                    logger(f"Can't find target_img_path. ({self.img})")
                    return False
        width = ''
        height = ''
        if im is None:
            im_data = self.read_im_via_PIL()
            # read file as img
            self.im = im_data[0]

            # for cv2
            self.im_cv2 = im_data[1]

            # get resolution(for expand the width)
            width = im_data[2]
            height = im_data[3]
        else:
            # 新image + 遞迴
            '''
            [im_crop_list (ex: [im_1, im_2, im_3...]) (PIL format) ,
                       gap_size (ex: 50)
                       axis (ex: 'horizontal') ]'''
            self.im = im
            width, height = self.im.size

        # make sure resize_range is float
        resize_range = float(resize_range)

        # resize im
        self.resize_im = self.im.resize((int(width * resize_range), height), Image.BILINEAR)
        self.resize_im_cv = cv2.resize(self.im_cv2, (int(width * resize_range), height))

        if method == 1:
            self.data = pytesseract.image_to_data(self.resize_im, output_type='dict')
            #for_print = pytesseract.image_to_data(self.resize_im, output_type='string')
            #logger(for_print)
            logger(f'===================')
            logger(f'==>Method: {method}, Target: ({self.text})')
            logger(f'==>resize range: {resize_range}')
            logger(f'DATA: ({self.data})')
            len_level = len(self.data['level'])
            len_text = len(self.data['text'])
            if len_level != len_text:
                len_level = len_text
                logger(f'OCR pytesseract return wrong index: work around')
            for x in range(len_level):
                if self.data['text'][x] == self.text:
                    self.conf = self.data['conf'][x]  # type of conf is int
                    if self.conf >= self.default_conf:
                        self.pos = (int((self.data['left'][x] + (self.data['width'][x] / 2)) / resize_range),
                                    int(self.data['top'][x] + self.data['height'][x] / 2))
                        # print(self.data['left'][x])
                        # make sure each dict item is unique(2020/6/29)
                        if len(self.result_dict) == 0:
                            self.count += 1
                            self.result_dict.update({self.count: self.pos})
                        else:
                            check_flag_list = []
                            for z in range(1, len(self.result_dict) + 1):
                                check_flag_list.append(self.result_dict[z])
                            # skip tolerance (+/- 1)
                            pos_list = []
                            for i in tolerance_list:
                                for j in tolerance_list:
                                    pos_list.append((self.pos[0] + i, self.pos[1] + j))
                            is_in_list_check_flag = 0
                            for check in range(len(pos_list)):
                                if pos_list[check] in check_flag_list:
                                    is_in_list_check_flag = 1
                                    break
                            if is_in_list_check_flag == 0:
                                self.count += 1
                                self.result_dict.update({self.count: self.pos})
            logger(f"current dict: {self.result_dict}")
            logger(f'===================\n')
        elif method == 2:
            # [Method 2] try enhance color to 0.0
            self.temp = ImageEnhance.Color(self.resize_im).enhance(0.0)
            self.data = pytesseract.image_to_data(self.temp, output_type='dict')
            logger(f'===================')
            logger(f'==>Method: {method}, Target: ({self.text})')
            logger(f'==>resize range: {resize_range}')
            logger(f'DATA: ({self.data})')
            len_level = len(self.data['level'])
            len_text = len(self.data['text'])
            if len_level != len_text:
                len_level = len_text
                logger(f'OCR pytesseract return wrong index: work around')
            for x in range(len_level):
                if self.data['text'][x] == self.text:
                    self.conf = self.data['conf'][x]  # type of conf is int
                    if self.conf >= self.default_conf:
                        self.pos = (int((self.data['left'][x] + (self.data['width'][x] / 2)) / resize_range),
                                    int(self.data['top'][x] + self.data['height'][x] / 2))
                        # make sure each dict item is unique(2020/6/29)
                        if len(self.result_dict) == 0:
                            self.count += 1
                            self.result_dict.update({self.count: self.pos})
                        else:
                            check_flag_list = []
                            for z in range(1, len(self.result_dict) + 1):
                                check_flag_list.append(self.result_dict[z])
                            # skip tolerance (+/- 1)
                            pos_list = []
                            for i in tolerance_list:
                                for j in tolerance_list:
                                    pos_list.append((self.pos[0] + i, self.pos[1] + j))
                            is_in_list_check_flag = 0
                            for check in range(len(pos_list)):
                                if pos_list[check] in check_flag_list:
                                    is_in_list_check_flag = 1
                                    break
                            if is_in_list_check_flag == 0:
                                self.count += 1
                                self.result_dict.update({self.count: self.pos})
            logger(f"current dict: {self.result_dict}")
            logger(f'===================\n')
        elif method == 3:
            # [Method 3] try to add filter
            self.temp = self.resize_im.filter(ImageFilter.CONTOUR)
            self.temp = ImageEnhance.Color(self.temp).enhance(0.0)
            self.data = pytesseract.image_to_data(self.temp, output_type='dict')
            logger(f'===================')
            logger(f'==>Method: {method}, Target: ({self.text})')
            logger(f'==>resize range: {resize_range}')
            logger(f'DATA: ({self.data})')
            len_level = len(self.data['level'])
            len_text = len(self.data['text'])
            if len_level != len_text:
                len_level = len_text
                logger(f'OCR pytesseract return wrong index: work around')
            for x in range(len_level):
                if self.data['text'][x] == self.text:
                    self.conf = self.data['conf'][x]  # type of conf is int
                    if self.conf >= self.default_conf:
                        self.pos = (int((self.data['left'][x] + (self.data['width'][x] / 2)) / resize_range),
                                    int(self.data['top'][x] + self.data['height'][x] / 2))
                        # make sure each dict item is unique(2020/6/29)
                        if len(self.result_dict) == 0:
                            self.count += 1
                            self.result_dict.update({self.count: self.pos})
                        else:
                            check_flag_list = []
                            for z in range(1, len(self.result_dict) + 1):
                                check_flag_list.append(self.result_dict[z])
                            # skip tolerance (+/- 1)
                            pos_list = []
                            for i in tolerance_list:
                                for j in tolerance_list:
                                    pos_list.append((self.pos[0] + i, self.pos[1] + j))
                            is_in_list_check_flag = 0
                            for check in range(len(pos_list)):
                                if pos_list[check] in check_flag_list:
                                    is_in_list_check_flag = 1
                                    break
                            if is_in_list_check_flag == 0:
                                self.count += 1
                                self.result_dict.update({self.count: self.pos})
            logger(f"current dict: {self.result_dict}")
            logger(f'===================\n')
        elif method == 4:
            # [Method 4] try to add filter (gray - > white/black reverse)(for black background with white text)
            self.temp = cv2.cvtColor(self.resize_im_cv, cv2.COLOR_BGR2GRAY)
            self.temp = 255 - self.temp
            self.data = pytesseract.image_to_data(self.temp,
                                                  output_type='dict')
            logger(f'===================')
            logger(f'==>Method: {method}, Target: ({self.text})')
            logger(f'==>resize range: {resize_range}')
            logger(f'DATA: ({self.data})')
            len_level = len(self.data['level'])
            len_text = len(self.data['text'])
            if len_level != len_text:
                len_level = len_text
                logger(f'OCR pytesseract return wrong index: work around')
            for x in range(len_level):
                if self.data['text'][x] == self.text:
                    self.conf = self.data['conf'][x]  # type of conf is int
                    if self.conf >= self.default_conf:
                        self.pos = (
                            int((self.data['left'][x] + (self.data['width'][x] / 2)) / resize_range),
                            int(self.data['top'][x] + self.data['height'][x] / 2))
                        # make sure each dict item is unique(2020/6/29)
                        if len(self.result_dict) == 0:
                            self.count += 1
                            self.result_dict.update({self.count: self.pos})
                        else:
                            check_flag_list = []
                            for z in range(1, len(self.result_dict) + 1):
                                check_flag_list.append(self.result_dict[z])
                            # skip tolerance (+/- 1)
                            pos_list = []
                            for i in tolerance_list:
                                for j in tolerance_list:
                                    pos_list.append((self.pos[0] + i, self.pos[1] + j))
                            is_in_list_check_flag = 0
                            for check in range(len(pos_list)):
                                if pos_list[check] in check_flag_list:
                                    is_in_list_check_flag = 1
                                    break
                            if is_in_list_check_flag == 0:
                                self.count += 1
                                self.result_dict.update({self.count: self.pos})
            logger(f"current dict: {self.result_dict}")
            logger(f'===================\n')
        elif method == 5:
            # [Method 5] try to add filter (gray - > white/black reverse -> get rid of gray)(for black background with white text)
            self.temp = cv2.cvtColor(self.resize_im_cv, cv2.COLOR_BGR2GRAY)
            self.temp = 255 - self.temp
            # get rid of gray
            _, self.temp = cv2.threshold(self.temp, 130, 255, cv2.THRESH_BINARY)
            self.data = pytesseract.image_to_data(self.temp,
                                                  output_type='dict')
            logger(f'===================')
            logger(f'==>Method: {method}, Target: ({self.text})')
            logger(f'==>resize range: {resize_range}')
            logger(f'DATA: ({self.data})')
            len_level = len(self.data['level'])
            len_text = len(self.data['text'])
            if len_level != len_text:
                len_level = len_text
                logger(f'OCR pytesseract return wrong index: work around')
            for x in range(len_level):
                if self.data['text'][x] == self.text:
                    self.conf = self.data['conf'][x]  # type of conf is int
                    if self.conf >= self.default_conf:
                        self.pos = (
                            int((self.data['left'][x] + (self.data['width'][x] / 2)) / resize_range),
                            int(self.data['top'][x] + self.data['height'][x] / 2))
                        # make sure each dict item is unique(2020/6/29)
                        if len(self.result_dict) == 0:
                            self.count += 1
                            self.result_dict.update({self.count: self.pos})
                        else:
                            check_flag_list = []
                            for z in range(1, len(self.result_dict) + 1):
                                check_flag_list.append(self.result_dict[z])
                            # skip tolerance (+/- 1)
                            pos_list = []
                            for i in tolerance_list:
                                for j in tolerance_list:
                                    pos_list.append((self.pos[0] + i, self.pos[1] + j))
                            is_in_list_check_flag = 0
                            for check in range(len(pos_list)):
                                if pos_list[check] in check_flag_list:
                                    is_in_list_check_flag = 1
                                    break
                            if is_in_list_check_flag == 0:
                                self.count += 1
                                self.result_dict.update({self.count: self.pos})
            logger(f"current dict: {self.result_dict}")
            logger(f'===================\n')
        elif method == 6:
            # [Method 6] try to add filter (gray - > white/black reverse -> get rid of gray)(for black background with white text)
            self.temp = cv2.cvtColor(self.resize_im_cv, cv2.COLOR_BGR2GRAY)
            self.temp = 255 - self.temp
            # get rid of gray
            _, self.temp = cv2.threshold(self.temp, 127, 255, cv2.THRESH_BINARY)
            self.data = pytesseract.image_to_data(self.temp,
                                                  output_type='dict')
            logger(f'===================')
            logger(f'==>Method: {method}, Target: ({self.text})')
            logger(f'==>resize range: {resize_range}')
            logger(f'DATA: ({self.data})')
            len_level = len(self.data['level'])
            len_text = len(self.data['text'])
            if len_level != len_text:
                len_level = len_text
                logger(f'OCR pytesseract return wrong index: work around')
            for x in range(len_level):
                if self.data['text'][x] == self.text:
                    self.conf = self.data['conf'][x]  # type of conf is int
                    if self.conf >= self.default_conf:
                        self.pos = (
                            int((self.data['left'][x] + (self.data['width'][x] / 2)) / resize_range),
                            int(self.data['top'][x] + self.data['height'][x] / 2))
                        # make sure each dict item is unique(2020/6/29)
                        if len(self.result_dict) == 0:
                            self.count += 1
                            self.result_dict.update({self.count: self.pos})
                        else:
                            check_flag_list = []
                            for z in range(1, len(self.result_dict) + 1):
                                check_flag_list.append(self.result_dict[z])
                            # skip tolerance (+/- 1)
                            pos_list = []
                            for i in tolerance_list:
                                for j in tolerance_list:
                                    pos_list.append((self.pos[0] + i, self.pos[1] + j))
                            is_in_list_check_flag = 0
                            for check in range(len(pos_list)):
                                if pos_list[check] in check_flag_list:
                                    is_in_list_check_flag = 1
                                    break
                            if is_in_list_check_flag == 0:
                                self.count += 1
                                self.result_dict.update({self.count: self.pos})
            logger(f"current dict: {self.result_dict}")
            logger(f'===================\n')
        elif method == 7: # has problem
            # [Method 7]
            # Gray to HSV -> remove blue -> gray -> reverse -> threshold -> blur and enlarge the height
            # redefine resize_im_cv for enlarging the height length
            # get HSV
            # channel
            #   hsv_channel[0] is hue
            #   hsv_channel[1] is saturation
            #   hsv_channel[2] is visibility
            self.resize_im_cv = cv2.resize(self.im_cv2, (int(width * resize_range), int(height * 2)))
            self.temp = cv2.cvtColor(self.resize_im_cv, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(self.temp)
            ''' other mask
            mask = cv2.inRange(self.temp, (0, 0, 0), (180, 50, 130))
            dst1 = cv2.bitwise_and(self.im_cv2, self.im_cv2, mask=mask)

            th, threshed = cv2.threshold(v, 150, 255, cv2.THRESH_BINARY_INV)
            dst2 = cv2.bitwise_and(self.im_cv2, self.im_cv2, mask=threshed)
            '''
            th, threshed2 = cv2.threshold(s, 30, 255, cv2.THRESH_BINARY_INV)
            self.temp = cv2.bitwise_and(self.resize_im_cv, self.resize_im_cv, mask=threshed2)
            self.data = pytesseract.image_to_data(self.temp,
                                                  output_type='dict')
            logger(f'===================')
            logger(f'==>Method: {method}, Target: ({self.text})')
            logger(f'==>resize range: {resize_range}')
            logger(f'DATA: ({self.data})')
            len_level = len(self.data['level'])
            len_text = len(self.data['text'])
            if len_level != len_text:
                len_level = len_text
                logger(f'OCR pytesseract return wrong index: work around')
            for x in range(len_level):
                if self.data['text'][x] == self.text:
                    self.conf = self.data['conf'][x]  # type of conf is int
                    if self.conf >= self.default_conf:
                        self.pos = (
                            int((self.data['left'][x] + (self.data['width'][x] / 2)) / resize_range),
                            int((self.data['top'][x] + self.data['height'][x] / 2) / 2))
                        # make sure each dict item is unique(2020/6/29)
                        if len(self.result_dict) == 0:
                            self.count += 1
                            self.result_dict.update({self.count: self.pos})
                        else:
                            check_flag_list = []
                            for z in range(1, len(self.result_dict) + 1):
                                check_flag_list.append(self.result_dict[z])
                            # skip tolerance (+/- 1)
                            pos_list = []
                            for i in tolerance_list:
                                for j in tolerance_list:
                                    pos_list.append((self.pos[0] + i, self.pos[1] + j))
                            is_in_list_check_flag = 0
                            for check in range(len(pos_list)):
                                if pos_list[check] in check_flag_list:
                                    is_in_list_check_flag = 1
                                    break
                            if is_in_list_check_flag == 0:
                                self.count += 1
                                self.result_dict.update({self.count: self.pos})
            logger(f"current dict: {self.result_dict}")
            logger(f'===================\n')
        elif method == 8: # for PDVD
            # [Method 8]
            # RGB to HSV -> A. hsv mask(white with blue) -> B. hsv mask(get red part)
            #   -> bitwise_not (
            def img_hsv_mask_white(img):
                """
                only return white part
                :param img:
                :return:
                """
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                # for hsv, OpenCV uses H: 0-179, S: 0-255, V: 0-255
                lower_hsv = np.array([0, 0, 200])
                upper_hsv = np.array([179, 255, 235])
                mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
                blur = cv2.blur(mask, (80, 80))
                img2 = cv2.bitwise_and(img, img, mask=blur)
                #cv2.imshow("mask", mask)
                #cv2.waitKey(0)
                return img2

            self.resize_im_cv = cv2.resize(self.im_cv2, (int(width * resize_range), int(height)))
            self.temp = cv2.cvtColor(self.resize_im_cv, cv2.COLOR_BGR2HSV)
            hsv_im_white = img_hsv_mask_white(self.resize_im_cv)
            # define range of blue color in HSV
            lower_red = np.array([10, 110, 46])
            upper_red = np.array([179, 248, 255])
            mask = cv2.inRange(self.temp, lower_red, upper_red)
            self.temp = cv2.bitwise_and(self.temp, self.temp, mask=mask)
            self.temp = cv2.bitwise_not(hsv_im_white, self.temp)
            self.data = pytesseract.image_to_data(self.temp,
                                                  output_type='dict')
            logger(f'===================')
            logger(f'==>Method: {method}, Target: ({self.text})')
            logger(f'==>resize range: {resize_range}')
            logger(f'DATA: ({self.data})')
            len_level = len(self.data['level'])
            len_text = len(self.data['text'])
            if len_level != len_text:
                len_level = len_text
                logger(f'OCR pytesseract return wrong index: work around')
            for x in range(len_level):
                if self.data['text'][x] == self.text:
                    self.conf = self.data['conf'][x]  # type of conf is int
                    if self.conf >= self.default_conf:
                        self.pos = (
                            int((self.data['left'][x] + (self.data['width'][x] / 2)) / resize_range),
                            int((self.data['top'][x] + self.data['height'][x] / 2)))
                        # make sure each dict item is unique(2020/6/29)
                        if len(self.result_dict) == 0:
                            self.count += 1
                            self.result_dict.update({self.count: self.pos})
                        else:
                            check_flag_list = []
                            for z in range(1, len(self.result_dict) + 1):
                                check_flag_list.append(self.result_dict[z])
                            # skip tolerance (+/- 1)
                            pos_list = []
                            for i in tolerance_list:
                                for j in tolerance_list:
                                    pos_list.append((self.pos[0] + i, self.pos[1] + j))
                            is_in_list_check_flag = 0
                            for check in range(len(pos_list)):
                                if pos_list[check] in check_flag_list:
                                    is_in_list_check_flag = 1
                                    break
                            if is_in_list_check_flag == 0:
                                self.count += 1
                                self.result_dict.update({self.count: self.pos})
            logger(f"current dict: {self.result_dict}")
            logger(f'===================\n')
        # sort out position list(2020/07/28)
        pos_list = []
        for o in range(len(self.result_dict)):
            pos_list.append(self.result_dict[o + 1])
        # use y-axis as sort by ref.(2020/10/06)
        pos_list = sorted(pos_list, key=lambda s: s[1])
        dict_new_none = {}
        for r in range(len(self.result_dict)):
            dict_new_none[r + 1] = pos_list[r]
        logger(f'===================')
        logger(f'tolerance is +/-{tolerance}')
        logger(f"final dict(sorted): {dict_new_none}")
        logger(f'===================\n')
        return dict_new_none

    def cut_img(self, axis='horizontal', proportion='1/2'):
        """
        2020/06/30
        sometimes can't recognize text for full frame but cutting image, so cut_img and then perform OCR
        Note: need add the position value back
        :axis: vertical, horizontal
        :proportion: '1/2', '1/4'
        :return: list [im_crop_list (ex: [im_1, im_2, im_3...]) (PIL format) ,
                       gap_size (ex: 50)
                       axis (ex: 'horizontal') ]
        """
        try:
            # read(PIL)
            self.im = Image.open(self.img)
            w, h = self.im.size

            # check axis
            if axis == 'vertical':
                pass
            elif axis == 'horizontal':
                crop_part_list = []
                add_back_h_list = []
                gap_size = int(h / int(proportion.split('/')[-1]))
                print(gap_size)
                for x in range(int(proportion.split('/')[-1])):
                    crop_part_list.append((0, gap_size * x, w, gap_size * (x + 1)))
                    add_back_h_list.append(gap_size * x)
                im_crop_list = []
                for y in range(len(crop_part_list)):
                    im_crop_list.append(self.im.crop(crop_part_list[y]))
                return [im_crop_list, gap_size, axis]
            else:
                logger('incorrect parameter')
                return False
        except Exception as e:
            logger(f'Exception. ({e})')
            return False

    def scan_all(self, resize_range, search_index=1, im=None):
        try:
            for x in range(1, 9):       # method 1 ~ 7 (method 7 has problem, maybe skip)
                result = self.scan_method(x, resize_range, im)
                # check if search_index is int or str
                # |int => find index
                # |str => ex:('2/3'), means check if having 3 result, if yes, return 2nd position
                if type(search_index) is int:
                    if search_index == 1:
                        if len(result) != 0:
                            break
                    if search_index <= len(result):
                        break
                elif type(search_index) is str:
                    # split / symbol
                    if '/' in search_index:
                        target_index, total_index = search_index.split('/')
                        target_index = int(target_index)
                        total_index = int(total_index)
                    if len(result) >= total_index:
                        break
            return x, result
        except Exception as e:
            logger(f'scan all Exception: {e}')
            return False

    # get count
    def get_count(self):
        try:
            result = self.analyze()
            if result == 0:
                logger(f"Can't find ['{self.text}'] in the image")
                return False
            return len(result) if not False else False
        except Exception as e:
            logger(f'get_count:Exception: ({e})')
            return False

    # get_position
    def get_pos(self, index=1, crop=('horizontal', '1/2')):
        try:
            result = self.analyze(search_index=index)
            logger(f'Result: {result}')
            if result == 0:
                logger(f"Can't find ['{self.text}'] {index}-index . index is out of range in the image")
                return False
            # Check if index is int or str
            # |int: directly return corresponding result
            # |str(ex:'2/3'): need to find out 3 results, and return 2nd position
            if type(index) is int:
                if index < 0:
                    logger('incorrect parameter')
                    return False
                if index > len(result):
                    """
                    # try crop and then analyze method (2020/06/30)
                    """
                    logger(f"only can find ['{self.text}']  {len(result)}-time . index is out of range")
                    return False
                return result[index] if not False else False
            elif type(index) is str:
                if '/' in index:
                    target_index, total_index = index.split('/')
                    target_index = int(target_index)
                    total_index = int(total_index)
                if len(result) < total_index:
                    logger(f'total obj(s) are {total_index}, but only find {len(result)} obj(s)')
                    return False
                else:
                    # len(result >= total_index case
                    return result[target_index] if not False else False
        except Exception as e:
            logger(f'get_pos:Exception: ({e})')
            return False

    @staticmethod
    def log_OKData(ratio, method):
        path = os.getcwd() + r'/ocr_log.ini'
        if not os.path.exists(path):
            open(path, 'w')
        config = configparser.ConfigParser(delimiters='==')
        # avoid lower case for writing key
        config.optionxform = str
        if not config.has_section('Log'):
            config.add_section('Log')
        option_text = f'{ratio}_{method}'
        config.read(path)
        value = config.get('Log', f'{option_text}', fallback=None)
        if value is None:
            value = 0
        value = int(value)
        value += 1
        config.set('Log', f'{option_text}', str(value))
        with open(path, 'w') as configwrite:
            config.write(configwrite)
        return True

    def log_ReadTextData(self):
        """
        return a list
        """
        path = os.getcwd() + r'/ocr_log.ini'
        if not os.path.exists(path):
            return None
        config = configparser.ConfigParser(delimiters='==')
        # avoid lower case for writing key
        config.optionxform = str
        config.read(path)
        #data_analyze = config.get('Data', self.text, fallback=None)
        try:
            data_keys = config.items('Data')
        except:
            return None
        value_list = []
        # read list
        for k in range(len(data_keys)):
            if data_keys[k][0] == self.text:
                value_list_str = data_keys[k][1]
                # transform to list from str
                items = value_list_str.strip('[]').split(', ')
                for l in range(len(items)):
                    #print(items[l])
                    value_list.append(items[l].strip("''"))
                break
        if len(value_list) == 0:
            value_list = None
        return value_list

    def log_WriteTextData(self, ratio, method):
        path = os.getcwd() + r'/ocr_log.ini'
        if not os.path.exists(path):
            open(path, 'w')
        config = configparser.ConfigParser(delimiters='==')
        # avoid lower case for writing key
        config.optionxform = str
        config.read(path)
        if not config.has_section('Data'):
            config.add_section('Data')
        # read data
        try:
            data_keys = config.items('Data')
        except:
            return None
        value_list = []
        # read list
        for k in range(len(data_keys)):
            if data_keys[k][0] == self.text:
                value_list_str = data_keys[k][1]
                # transform to list from str
                items = value_list_str.strip('[]').split(', ')
                for l in range(len(items)):
                    #print(items[l])
                    value_list.append(items[l].strip("''"))
                break
        # append data
        method = f'{ratio}_{method}'
        if method in value_list:
            return True
        value_list.append(method)
        config.set('Data', self.text, f'{value_list}')
        with open(path, 'w') as configwrite:
            config.write(configwrite)
        return True

# SAMPLE:
def sample():
    photo_path = r'/Users/Terence/Downloads/U-2019-12-26.png'
    get_dict = OCR(photo_path, 'CyberLink').analyze()
    get_count = OCR(photo_path, 'Version').get_count()
    get_pos = OCR(photo_path, 'SR').get_pos(1)
    get_pos = OCR(photo_path, 'Videos').get_pos("2/5")
    logger(f'dict: {get_dict}')
    logger(f'count: {get_count}')
    logger(f'pos: {get_pos}')