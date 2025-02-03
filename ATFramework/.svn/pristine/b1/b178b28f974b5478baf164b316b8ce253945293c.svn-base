import os
import sys
import zipfile
try:
    from .log import logger
except:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))
    print(os.path.dirname(SCRIPT_DIR))
    from log import logger


def single_file_to_zip(src_file='', dst_zip=''):
    result_dict = {'result': True, 'file_path': dst_zip}
    try:
        if not os.path.exists(src_file):
            logger(f'File is missing, {src_file=}')
            return False
        if os.path.isfile(dst_zip):
            os.remove(dst_zip)
        os.makedirs(os.path.dirname(dst_zip), exist_ok=True)
        with zipfile.ZipFile(dst_zip, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
            zf.write(src_file, arcname=os.path.basename(src_file))
        if not os.path.isfile(dst_zip):
            logger(f'zip file generate failed.')
            result_dict['result'] = False
    except Exception as e:
        logger(f'Exception occurs. error={e}')
        result_dict['result'] = False
    return result_dict


def multiple_file_to_zip(src_file_list=None, dst_zip=''):
    result_dict = {'result': True, 'file_path': dst_zip}
    if src_file_list is None:
        src_file_list = []
    try:
        for file in src_file_list:
            if not os.path.exists(file):
                logger(f'File is missing, {file=}')
                continue
        os.makedirs(os.path.dirname(dst_zip), exist_ok=True)
        with zipfile.ZipFile(dst_zip, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
            for file in src_file_list:
                if not os.path.exists(file):
                    continue
                zf.write(file, arcname=os.path.basename(file))
        if not os.path.isfile(dst_zip):
            logger(f'zip file generate failed.')
            result_dict['result'] = False
    except Exception as e:
        logger(f'Exception occurs. error={e}')
        result_dict['result'] = False
    return result_dict


if __name__ == '__main__':
    file_path = r"C:\Users\user\Downloads\526.98-notebook-win10-win11-64bit-international-nsd-dch-whql.exe"
    dst_path = r"C:\Users\user\Downloads\single.zip"
    result = single_file_to_zip(file_path, dst_path)
    print(result)
    file_path = [r"C:\Users\user\Downloads\526.98-notebook-win10-win11-64bit-international-nsd-dch-whql.exe",
                 r"C:\Users\user\Downloads\U_7.9.10724.948154(7.9.0Prod)_Free_YOU221018-03.exe"]
    dst_path = r"C:\Users\user\Downloads\multiple.zip"
    result = multiple_file_to_zip(file_path, dst_path)
    print(result)
