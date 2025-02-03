import os
import sys
import shutil
import hashlib
from configparser import ConfigParser
import subprocess
import getpass
import argparse
from password import Authorization

try:
    from ..log import logger
except:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))
    print(os.path.dirname(SCRIPT_DIR))
    from log import logger


class Ecl_Operation():
    def __init__(self, src_path, dest_path, work_dir=''): # prod_name, sr_no, tr_no, prog_path_sub, dest_path, work_dir (for password and tr_db file), mail_list(list)
        try:
            self.user_name = ''
            self.password = ''
            self.work_dir = os.path.dirname(__file__)
            if work_dir:
                self.work_dir = work_dir
            self.src_path = src_path
            self.dest_path = os.path.join(self.work_dir, "download_build")
            if dest_path:
                self.dest_path = dest_path
            self.password_file = 'password'
            self.err_msg = ''
            # decrypt the username/ password
            obj_authorization = Authorization(self.work_dir)
            passwd_list = obj_authorization.decryption_vigenere_clt_account()
            self.user_name = passwd_list[0]
            self.password = passwd_list[1]
        except Exception as e:
            err_msg = f'Exception occurs. Incorrect format of parameter or missing keys. ErrorLog={e}'
            self.err_msg = err_msg

    def _md5(self, filename):
        try:
            md5_object = hashlib.md5()
            block_size = 128 * md5_object.block_size
            a_file = open(filename, 'rb')

            chunk = a_file.read(block_size)
            while chunk:
                md5_object.update(chunk)
                chunk = a_file.read(block_size)

            md5_hash = md5_object.hexdigest()
        except Exception as e:
            logger(f'Exception occurs. ErrLog={e}')
            raise Exception
        return md5_hash

    def _md5_check_folder(self, path_folder):
        try:
            file_md5 = 'Cyberlink.MD5'
            if os.name == 'nt':
                path_md5 = '\\'.join([path_folder, file_md5]) # for windows
            else: # mac
                path_md5 = '/'.join([path_folder, file_md5])
            if not os.path.isfile(path_md5):
                logger('No Cyberlink.MD5 file')
                return False

            config = ConfigParser()
            config.read(path_md5)
            section_name = 'Info'
            file_count = int(config[section_name]['Count'])
            # print(f'{file_count=}')
            list_keys = config.items(section_name)
            # print(f'{list_keys=}')
            file_count_pass = 0
            for index in range(len(list_keys)):
                if index == 0:
                    continue
                if os.name == 'nt':
                    file = ''.join([path_folder, list_keys[index][0]])
                else: # mac
                    sub_path = list_keys[index][0].replace('\\', '/')
                    file = ''.join([path_folder, sub_path])
                # print(file)
                if list_keys[index][1] == '':
                    file_count_pass += 1
                    continue
                if not os.path.isfile(file):
                    print(f'{file} doesn\'t exist.')
                    continue
                value = self._md5(file)
                if not value:
                    print(f'Generate MD5 checksum of {file}')
                    continue
                if value.upper() == list_keys[index][1].upper():
                    file_count_pass += 1
                else:
                    print(f'[_md5_check_folder] MD5 check FAIL. {file=}, MD5_expected={list_keys[index][1]}, MD5_check={value.upper()}')

            if not file_count_pass == file_count:
                err_msg = f'[_md5_check_folder] MD5 check is FAIL. Expected={file_count}, Passed={file_count_pass}, folder_path={path_folder}'
                print(err_msg)
                self.error_msg = err_msg
                return False
            print(f'MD5 check is Done. Expected={file_count}, Passed={file_count_pass}')
        except Exception:
            return False
        return True

    def download_tr_build(self, src_path, dest_path):
        logger('download_tr_build - Start')
        logger(f'{src_path=}')
        logger(f'{dest_path=}')
        mount_local_folder = ''
        mount_server_path = r'//CLT-QASERVER/Testing'
        network_path = r'\\clt-qaserver'
        curr_user = ''
        try:
            # [0] check current os type
            curr_os = 'windows'
            if os.name != 'nt':
                curr_os = 'mac'
                curr_user = getpass.getuser()
                mount_local_folder = rf'/Users/{curr_user}/Desktop/my_mount'

            # [1] - Grant permission of clt-qaserver
            if curr_os == 'windows':
                if not os.path.exists(src_path):
                    print('Current OS: Windows')
                    cmd = 'NET USE ' + network_path + ' /User:' + self.user_name + ' ' + self.password
                    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                    stdout, stderr = process.communicate()
                    exit_code = process.wait()
                    print(stdout, stderr, exit_code)  # success - exit_code=0
            else:  # for mac
                print('Current OS: Mac')
                if not os.path.exists(mount_local_folder):
                    os.mkdir(mount_local_folder)
                if not os.path.ismount(mount_local_folder):
                    print('mount the local folder')
                    self.user_name = self.user_name.replace('clt\\', '')
                    os.system(f"mount_smbfs //{self.user_name}:{self.password}@clt-qaserver/Testing ~/Desktop/my_mount")
                print(f'Folder {mount_local_folder} is mounted.')

            # [2] Download build to local
            if os.path.exists(dest_path):
                shutil.rmtree(dest_path)
            if curr_os == 'mac':
                src_path = src_path.replace('\\', '/')
                src_path = src_path.replace(mount_server_path, mount_local_folder)
                print(f'{src_path=}')
            shutil.copytree(src_path, dest_path)

            # [3] Remove the permission/ unmount the folder
            if curr_os == 'mac':
                # for mac, unmount the folder and remove
                os.system(f'diskutil unmount {mount_local_folder}')
                os.rmdir(mount_local_folder)

            # do the MD5 check
            result = self._md5_check_folder(dest_path)
            if not result:
                self.err_msg = '[download_tr_build] MD5 check fail.'
                logger(f'{self.err_msg}')
                return False
        except Exception as e:
            logger(f'Exception occurs. ErrorLog={e}')
            if self.err_msg == '':
                self.err_msg = f'[download_tr_build] Exception occurs. ErrorLog={e}'
            return False
        return True


if __name__ == '__main__':
    src_build_path = ''
    dest_build_path = ''
    working_dir = ''
    # initialize parser
    parser = argparse.ArgumentParser()

    # add arguments to parser
    parser.add_argument("--s", help="source build path", type=str, default='')
    parser.add_argument("--d", help="destination build path", type=str, default='')
    parser.add_argument("--w", help="working dir", type=str, default='')

    # read arguments from command line
    args = parser.parse_args()

    if args.s:
        src_build_path = args.s

    if args.d:
        dest_build_path = args.d

    if args.w:
        working_dir = args.w

    # Initial the class
    obj_ecl_operation = Ecl_Operation(src_build_path, dest_build_path, working_dir)
    result = obj_ecl_operation.download_tr_build(obj_ecl_operation.src_path, obj_ecl_operation.dest_path)
    if result:
        logger('Download TR Build is Done.')
    else:
        logger(f'Download TR Build is Fail. Error={obj_ecl_operation.err_msg}')
