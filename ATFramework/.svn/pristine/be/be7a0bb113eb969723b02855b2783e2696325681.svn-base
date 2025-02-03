#!/usr/bin/python3
# compare.py
import os
import argparse
from .correlation import correlate
from .media_info import parse_media_info

try:
    from ..log import logger
except:
    import sys
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))
    print(os.path.dirname(SCRIPT_DIR))
    from log import logger

# ==================================================================================================================
# Description: Compare audio file by using acoustic fingerprinting and media info
# Note: n/a
# Author: Jim Huang
# ==================================================================================================================
# Interface: compare_audio

def initialize():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i ", "--source-file", help="source file")
    parser.add_argument("-o ", "--target-file", help="target file")
    args = parser.parse_args()

    SOURCE_FILE = args.source_file if args.source_file else None
    TARGET_FILE = args.target_file if args.target_file else None
    if not SOURCE_FILE or not TARGET_FILE:
        raise Exception("Source or Target files not specified.")
    return SOURCE_FILE, TARGET_FILE


def compare_audio(source_file, target_file, acoustic_threshold=1.0, check_media_info=True, with_media_info=False):
    compare_result = {'result': True, 'source_media_info': '', 'target_media_info': ''}
    try:
        if not os.path.exists(source_file):
            logger(f'File Not Exists. {source_file=}')
            raise Exception
        if not os.path.exists(target_file):
            logger(f'File Not Exists. {target_file=}')
            raise Exception
        # verify by media info
        if check_media_info:
            media_info_src = parse_media_info(source_file)
            logger(f'{media_info_src=}')
            media_info_dest = parse_media_info(target_file)
            logger(f'{media_info_dest=}')
            if with_media_info:
                compare_result['source_media_info'] = media_info_src
                compare_result['target_media_info'] = media_info_dest
            for key in media_info_src.keys():
                if not media_info_src[key] == media_info_dest[key]:
                    logger(f'Media info compare FAIL with [{key}]. Src:{media_info_src[key]}, Dest:{media_info_dest[key]}')
                    if with_media_info:
                        compare_result['result'] = False
                        return compare_result
                    return False
            logger(f'Verify by Media Info is Pass')
        # verify by acoustic fingerprinting
        max_corr_offset, correlation_value = correlate(source_file, target_file)
        logger(f'correlation_value={float(correlation_value)/100}')
        if float(acoustic_threshold) > float(correlation_value)/100:
            logger(f'Fail to compare. The correlation value is lower than {acoustic_threshold=}')
            return False
        logger(f'Verify by acoustic fingerprinting is Pass')
        if with_media_info:
            compare_result['result'] = True
            return compare_result
    except Exception as e:
        logger(f'Exception occurs. Error={e}')
        return False
    return True


def compare_audio_ex(source_file, target_file, acoustic_threshold=1.0, check_media_info=True, exclude_list: list = None):
    try:
        if not os.path.exists(source_file):
            logger(f'File Not Exists. {source_file=}')
            raise Exception
        if not os.path.exists(target_file):
            logger(f'File Not Exists. {target_file=}')
            raise Exception
        # verify by media info
        if check_media_info:
            media_info_src = parse_media_info(source_file)
            logger(f'{media_info_src=}')
            media_info_dest = parse_media_info(target_file)
            logger(f'{media_info_dest=}')
            for key in media_info_src.keys():
                if exclude_list is not None and key in exclude_list:
                    logger(f'{key=}, {exclude_list=}, skip it')
                    continue
                if not media_info_src[key] == media_info_dest[key]:
                    logger(f'Media info compare FAIL with [{key}]. Src:{media_info_src[key]}, Dest:{media_info_dest[key]}')
                    return False
            logger(f'Verify by Media Info is Pass')
        # verify by acoustic fingerprinting
        max_corr_offset, correlation_value = correlate(source_file, target_file)
        logger(f'correlation_value={float(correlation_value)/100}')
        if float(acoustic_threshold) > float(correlation_value)/100:
            logger(f'Fail to compare. The correlation value is lower than {acoustic_threshold=}')
            return False
        logger(f'Verify by acoustic fingerprinting is Pass')
    except Exception as e:
        logger(f'Exception occurs. Error={e}')
        return False
    return True


def compare_audio_ex_v2(source_file, target_file, acoustic_threshold=1.0, check_media_info=True, exclude_list: list = None):
    try:
        if not os.path.exists(source_file):
            logger(f'File Not Exists. {source_file=}')
            raise Exception
        if not os.path.exists(target_file):
            logger(f'File Not Exists. {target_file=}')
            raise Exception
        # verify by media info
        if check_media_info:
            media_info_src = parse_media_info(source_file)
            logger(f'{media_info_src=}')
            media_info_dest = parse_media_info(target_file)
            logger(f'{media_info_dest=}')
            for key in media_info_src.keys():
                if exclude_list is not None and key in exclude_list:
                    logger(f'{key=}, {exclude_list=}, skip it')
                    continue
                if not media_info_src[key] == media_info_dest[key]:
                    logger(f'Media info compare FAIL with [{key}]. Src:{media_info_src[key]}, Dest:{media_info_dest[key]}')
                    return False
            logger(f'Verify by Media Info is Pass')
        # verify by acoustic fingerprinting
        max_corr_offset, correlation_value = correlate(source_file, target_file)
        result_correlation_value = float(correlation_value)/100
        logger(f'correlation_value={result_correlation_value}')
        if float(acoustic_threshold) > result_correlation_value:
            logger(f'Fail to compare. The correlation value is lower than {acoustic_threshold=}')
            return False, result_correlation_value
        logger(f'Verify by acoustic fingerprinting is Pass')
    except Exception as e:
        logger(f'Exception occurs. Error={e}')
        return False, -1
    return True, result_correlation_value


if __name__ == "__main__":
    SOURCE_FILE, TARGET_FILE = initialize()
    correlate(SOURCE_FILE, TARGET_FILE)
