import os
import sys
import configparser
import platform

import pyautogui
import easyocr

try:
    from .log import logger
except:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))
    print(os.path.dirname(SCRIPT_DIR))
    from log import logger


"""
Need Log module (https://qadroid/svn/ATFramework/utils/log.py)
"""


class OCR:
    def __init__(self, target_img_path, target_text='', lang_list=None, gpu=False, conf=0.3, is_include=False):
        try:
            if os.path.isfile(target_img_path):
                self.img = target_img_path
                self.text = target_text
                self.conf = conf
                self.lang_list = lang_list if lang_list is not None else ['en']
                self.gpu = gpu
                self.ocr = easyocr.Reader(lang_list=self.lang_list, gpu=self.gpu)
                print('\n')
                self.detail_text_list = self.ocr.readtext(self.img, detail=1)
                self.text_list = self._get_text_list()
                self.is_include = is_include
            else:
                logger(f"target file isn't exist. {target_img_path}")
        except Exception as e:
            logger(f'Initial fail, Exception occurs - {e}')

    @staticmethod
    def find_center_coordinate(bounding_box):
        try:
            x_coordinates = [point[0] for point in bounding_box]
            y_coordinates = [point[1] for point in bounding_box]
            x_center = sum(x_coordinates) / len(x_coordinates)
            y_center = sum(y_coordinates) / len(y_coordinates)
        except:
            return False
        return int(x_center), int(y_center)

    @staticmethod
    def find_indices(_list, _item):
        indices = []
        try:
            for idx, value in enumerate(_list):
                if value == _item:
                    indices.append(idx)
        except:
            pass
        return indices

    def _get_text_list(self):
        _list = []
        for _, text, _ in self.detail_text_list:
            _list.append(text)
        return _list

    def get_text_position(self, target_text='', index=1):
        # target_text: string
        # index: int, 1-based
        find_text = self.text
        position = -1, -1
        try:
            if target_text:
                find_text = target_text
            if not find_text:
                logger(f'Target text is empty')
                return position
            if self.is_include:
                find_text_list = [text_partial for text_partial in self.text_list if find_text in text_partial]
                find_text_dict = self.analyze(no_log=True)
                position = find_text_dict.get(index)
                if position:
                    logger(f'text={find_text_list[index-1]}, {position=}')
                else:
                    logger(f'{index=} is out of range with text={find_text}')
            else:
                if self.text_list.count(find_text) >= index > 0:
                    text_index_list = self.find_indices(self.text_list, find_text)
                    bounding_box, text, conf = self.detail_text_list[text_index_list[index-1]]
                    if conf < self.conf:
                        logger(f'Confidence is low, {conf=}')
                        return position
                    position = self.find_center_coordinate(bounding_box)
                    logger(f'text={find_text}, {position=}')
                else:
                    logger(f'{index=} is out of range with text={find_text}')
        except Exception as e:
            logger(f'Exception occurs - {e}')
        return position

    def get_text_count(self, target_text=''):
        # target_text: string
        find_text = self.text
        text_count = 0
        try:
            if target_text:
                find_text = target_text
            if not find_text:
                logger(f'Target text is empty')
                return text_count
            if self.is_include:
                find_text_list = [text_partial for text_partial in self.text_list if find_text in text_partial]
                text_count = len(find_text_list)
            else:
                text_count = self.text_list.count(find_text)
            if text_count:
                logger(f'text={find_text}, {text_count=}')
            else:
                logger(f'Cannot find text={find_text}')
        except Exception as e:
            logger(f'Exception occurs - {e}')
        return text_count

    def get_text_count_by_conf(self, target_text=''):
        # target_text: string
        find_text = self.text
        text_count = 0
        try:
            if target_text:
                find_text = target_text
            if not find_text:
                logger(f'Target text is empty')
            elif find_text in self.text_list:
                text_index_list = self.find_indices(self.text_list, find_text)
                for idx in text_index_list:
                    bounding_box, text, conf = self.detail_text_list[idx]
                    if conf < self.conf:
                        # logger(f'{text=}, coord={self.find_center_coordinate(bounding_box)}, {conf=}')
                        continue
                    else:
                        text_count += 1
                if text_count:
                    logger(f'text={find_text}, {text_count=}')
                else:
                    logger(f'Cannot find text={find_text} by Confidence={self.conf}')
        except Exception as e:
            logger(f'Exception occurs - {e}')
        return text_count

    def get_text_detail_list(self, target_text=''):
        find_text = self.text
        detail_list = []
        try:
            if target_text:
                find_text = target_text
            if not find_text:
                logger(f'Target text is empty')
            elif find_text in self.text_list:
                text_index_list = self.find_indices(self.text_list, find_text)
                for idx in text_index_list:
                    text_detail_item = list(self.detail_text_list[idx])
                    text_detail_item[0] = self.find_center_coordinate(text_detail_item[0])
                    detail_list.append(tuple(text_detail_item))
        except Exception as e:
            logger(f'Exception occurs - {e}')
        return detail_list

    def get_all_text_in_image(self):
        return self.text_list

    def get_all_text_detail_in_image(self):
        return self.detail_text_list

    def analyze(self, target_text='', no_log=False):
        find_text = self.text
        analyze_dict = {}
        idx = 1
        try:
            if target_text:
                find_text = target_text
            if not find_text:
                logger(f'Target text is empty')
            else:
                for bounding_box, text, conf in self.detail_text_list:
                    if self.is_include:
                        if find_text in text and conf >= self.conf:
                            # logger(f'{bounding_box}, {text}, {conf}')
                            analyze_dict[idx] = self.find_center_coordinate(bounding_box)
                            idx += 1
                    else:
                        if find_text == text and conf >= self.conf:
                            # logger(f'{bounding_box}, {text}, {conf}')
                            analyze_dict[idx] = self.find_center_coordinate(bounding_box)
                            idx += 1
            if 1 not in analyze_dict.keys():
                analyze_dict = 0
            None if no_log else logger(f'analyze result={analyze_dict}')
        except Exception as e:
            logger(f'Exception occurs - {e}')
        return analyze_dict

    def get_count(self):
        count_result = self.get_text_count()
        if not count_result:
            return False
        return count_result

    def get_pos(self, index=1):
        pos_result = self.get_text_position(index=index)
        if pos_result[0] == -1:
            return False
        return pos_result


if __name__ == '__main__':
    pos = OCR(r"D:\_Programming\_code_test\find_sample.png", 'Photos')
    print(pos.analyze())
    print(pos.get_count())
    print(pos.get_pos(2))
