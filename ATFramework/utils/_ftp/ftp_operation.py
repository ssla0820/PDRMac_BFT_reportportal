import os
import atexit
import shutil

from ftplib import FTP, error_perm

# ==================================================================================================================
# Class: FtpOperation
# Description: FTP operation for upload/download file/folder
# Interface: ftp_upload_file, ftp_download_file, ftp_upload_folder, ftp_download_folder
# parameter: string
#            1) local_path: path in local machine
#            2) remote_path: path in ftp server, use '/' to separate folder, e.g. 'FTP_folder/Sub_folder'
#            3) server_address: ftp address
#            4) ac: ftp account
#            5) pw: ftp password
# Return: True/Raise Exception
# Usage: Please refer to sample code at below
# Author: Volath Liu
# ==================================================================================================================


class FtpOperation:
    def __init__(self, host, user, passwd):
        self.buffer_size = 1024
        self.host = host
        self.user = user
        self.passwd = passwd
        try:
            self.ftp = FTP(self.host, self.user, self.passwd)
            self.ftp.encoding = 'utf-8'
            if self.ftp.getwelcome():
                print(f'Connect to {self.host} success')
            atexit.register(self.ftp_quit)
        except error_perm as err:
            print(f'ftp error={err}')
            raise Exception(err)

    def ftp_quit(self):
        print(f'Close connection...')
        return self.ftp.quit()

    def isfile(self, file_name):
        try:
            self.ftp.size(file_name)
        except:
            return False
        return True

    def ftp_cwd(self, path):
        path_list = path.split('/')
        try:
            for folder in path_list:
                try:
                    self.ftp.cwd(folder)
                except Exception as err:
                    # print(f'{folder} is not exist, create it')
                    self.ftp.mkd(folder)
                    self.ftp.cwd(folder)
            return self.ftp.pwd()
        except error_perm as err:
            print(f'ftp error={err}')
            raise Exception(err)
        except Exception as err:
            print(f'Exception, {err=}')
            raise Exception(err)

    def upload_file(self, local_file, remote_file, exist_ok=False):
        if not os.path.isfile(local_file):
            raise Exception('Source file is invalid or not exist')
        try:
            if not exist_ok:
                self.ftp.cwd(os.path.dirname(remote_file))
                remote_file_list = self.ftp.nlst()
                if os.path.basename(remote_file) in remote_file_list:
                    raise Exception(f'{remote_file} already exists')
            with open(local_file, "rb") as file_handler:
                self.ftp.storbinary(f'STOR {remote_file}', file_handler, self.buffer_size)
        except error_perm as err:
            print(f'ftp error={err}')
            raise Exception(err)
        except Exception as err:
            print(f'Exception, {err=}')
            raise Exception(err)
        return True

    def upload_folder(self, local_path, remote_path, exist_ok=True, is_root=True):
        if not os.path.isdir(local_path):
            raise Exception('Source folder is invalid or not exist')
        try:
            root_folder_name = os.path.basename(local_path)
            self.ftp.cwd(remote_path)
            remote_file_list = self.ftp.nlst()
            if is_root:
                if not exist_ok and root_folder_name in remote_file_list:
                    raise Exception(f'{root_folder_name} already exists in {remote_path}')
                if root_folder_name not in remote_file_list:
                    self.ftp.mkd(root_folder_name)
                self.ftp.cwd(root_folder_name)
                remote_file_list = self.ftp.nlst()
            file_list = os.listdir(local_path)
            for file in file_list:
                src_path = os.path.join(local_path, file)
                if os.path.isdir(src_path):
                    if not exist_ok:
                        self.ftp.mkd(file)
                    elif file not in remote_file_list:
                        self.ftp.mkd(file)
                    self.upload_folder(src_path, file, exist_ok, False)
                else:
                    self.upload_file(src_path, file, exist_ok)
            self.ftp.cwd("..")
        except error_perm as err:
            print(f'ftp error={err}')
            raise Exception(err)
        except Exception as err:
            print(f'Exception, {err=}')
            raise Exception(err)
        return True

    def download_file(self, local_file, remote_file, exist_ok=False):
        try:
            if exist_ok:
                if os.path.isfile(local_file):
                    os.remove(local_file)
            os.makedirs(os.path.dirname(local_file), exist_ok=True)
            with open(local_file, 'wb') as file_handler:
                self.ftp.retrbinary(f'RETR {remote_file}', file_handler.write)
        except error_perm as err:
            print(f'ftp error={err}')
            raise Exception(err)
        except Exception as err:
            print(f'Exception, {err=}')
            raise Exception(err)
        return True

    def download_folder(self, local_path, remote_path, exist_ok=False, is_root=True):
        dst_folder_name = os.path.basename(remote_path)
        if not os.path.isdir(local_path):
            os.makedirs(local_path)
        if dst_folder_name in os.listdir(local_path):
            if not exist_ok:
                raise Exception(f'{dst_folder_name} already exists in {local_path}')
        elif is_root:
            os.makedirs(os.path.join(local_path, dst_folder_name))
        try:
            self.ftp.cwd(remote_path)
            remote_file_list = self.ftp.nlst()
            for file in remote_file_list:
                dst_path = os.path.join(local_path, file)
                if is_root:
                    dst_path = os.path.join(local_path, dst_folder_name, file)
                if self.isfile(file):
                    self.download_file(dst_path, file, exist_ok)
                else:
                    os.makedirs(dst_path, exist_ok=True)
                    self.download_folder(dst_path, file, exist_ok, False)
            self.ftp.cwd("..")
        except error_perm as err:
            print(f'ftp error={err}')
            raise Exception(err)
        except Exception as err:
            print(f'Exception, {err=}')
            raise Exception(err)
        return True


def ftp_upload_file(local_file, remote_file, server_address, ac, pw, exist_ok=False):
    myftp = FtpOperation(server_address, ac, pw)
    return myftp.upload_file(local_file, remote_file, exist_ok)


def ftp_download_file(local_file, remote_file, server_address, ac, pw, exist_ok=False):
    myftp = FtpOperation(server_address, ac, pw)
    return myftp.download_file(local_file, remote_file, exist_ok)


def ftp_upload_folder(local_path, remote_path, server_address, ac, pw, exist_ok=False):
    myftp = FtpOperation(server_address, ac, pw)
    return myftp.upload_folder(local_path, remote_path, exist_ok)


def ftp_download_folder(local_path, remote_path, server_address, ac, pw, exist_ok=False, is_root=True):
    myftp = FtpOperation(server_address, ac, pw)
    return myftp.download_folder(local_path, remote_path, exist_ok, is_root)


if __name__ == '__main__':
    SERVER_ADDRESS = 'CLT-QAFilesrv'
    ACCOUNT = 'TEST'
    PASSWORD = '1234'

    # D:/TEST/test.txt >> FTP_TEST/Sub_TEST/123.txt (FTP_TEST/Sub_TEST path must exist in ftp server)
    ftp_upload_file('D:/TEST/test.txt', 'FTP_TEST/123.txt', SERVER_ADDRESS, ACCOUNT, PASSWORD)

    # D:/TEST/my_Test >> FTP_TEST/Sub_TEST/my_Test (FTP_TEST/Sub_TEST path must exist in ftp server)
    ftp_upload_folder('D:/TEST/my_Test', 'FTP_TEST/Sub_TEST', SERVER_ADDRESS, ACCOUNT, PASSWORD)

    # FTP_TEST/test.txt >> D:/TEST/123.txt
    ftp_download_file('D:/TEST/123.txt', 'FTP_TEST/test.txt', SERVER_ADDRESS, ACCOUNT, PASSWORD)

    # FTP_TEST/my_Test >> D:/TEST/Sub_TEST/my_Test
    ftp_download_folder('D:/TEST/Sub_TEST', 'FTP_TEST/my_Test', SERVER_ADDRESS, ACCOUNT, PASSWORD)
