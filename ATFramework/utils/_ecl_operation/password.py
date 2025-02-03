
import os
from configparser import ConfigParser
from tkinter import *
import tkinter.messagebox
import requests
import base64
import sys

try:
    from ..log import logger
except:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))
    from log import logger

# from distutils.core import setup
# import PyInstaller
# setup (windows = ['password.exe'],
#        options = { 'PyInstaller' : {'packages':['Tkinter']}})

window = ''

class Authorization():
    def __init__(self, work_dir=''):
        self.key = 'testautomation'
        self.file_credential = 'credential'
        self.account = ''
        self.password = ''
        self.otp_code = ''
        self.work_dir = os.path.dirname(__file__)
        if work_dir:
            self.work_dir = work_dir
        self.file_credential = os.path.normpath(os.path.join(self.work_dir, self.file_credential))
        logger(f'file_credential = {self.file_credential}')

    def encryption_vigenere_clt_account(self, account, pw):
        try:
            # encryption
            ascii_key = [ord(c) for c in self.key]
            ascii_password = [ord(c) for c in pw]
            len_key = len(ascii_key)
            for index in range(len(ascii_password)):
                ascii_password[index] = ascii_password[index] + ascii_key[index % len_key]

            if not os.path.exists(self.file_credential):
                fo = open(self.file_credential, 'w')
                fo.close()
            config = ConfigParser()
            config.optionxform = str  # reference: http://docs.python.org/library/configparser.html
            config.read(self.file_credential)
            section_name = 'CREDENTIAL'
            if not config.has_section(section_name):
                config.add_section(section_name)
            config.set(section_name, "ACCOUNT", account)
            config.set(section_name, "PASSWD", str(ascii_password))
            config.write(open(self.file_credential, 'w'))
        except Exception as e:
            print(f'Exception occurs. Error={e}')
            raise Exception
        return True

    def decryption_vigenere_clt_account(self):
        result = []
        try:
            config = ConfigParser()
            config.read(self.file_credential)
            section_name = 'CREDENTIAL'
            account = config[section_name]['ACCOUNT']
            ascii_password = eval(config[section_name]['PASSWD'])

            # decryption
            ascii_key = [ord(c) for c in self.key]
            len_key = len(ascii_key)

            for index in range(len(ascii_password)):
                ascii_password[index] = ascii_password[index] - ascii_key[index % len_key]
            password = ''.join(map(chr, ascii_password))
            result.append(account)
            result.append(password)
            # print(f'{account=}, {password=}')
        except Exception as e:
            print(f'Exception occurs. Error={e}')
            raise
        return result

    def get_eclid_by_otp_code(self):
        try:
            url = f'https://ecl.cyberlink.com/ZFA/auth/OTOPVerify?U=https://cl-eportal.cyberlink.com&DC=ecl.cyberlink.com&C={self.otp_code}'
            r = requests.post(url, auth=(self.account, self.password))
            value = r.cookies["ECLID"]
            logger(f'ECLID={value}')
        except Exception as e:
            print(f'Exception occurs. Error={e}')
            raise Exception
        return value

    def create_eclid_file(self):
        try:
            if not self.otp_code:
                print(f'Please help to provide OTP Code.')
                return False
            ecl_id = self.get_eclid_by_otp_code()
            file_name = os.path.normpath(os.path.join(self.work_dir, 'eclid'))
            f = open(file_name, "wb")
            bytes_content = ecl_id.encode('utf-8')
            encoded = base64.b64encode(bytes_content)
            f.write(encoded)
            f.close()
            logger('create eclid file successfully')
        except Exception as e:
            print(f'Exception occurs. Error={e}')
            raise Exception
        return True

    def gui_save(self):
        self.account = name.get()
        self.password = password.get()
        self.otp_code = otp_code.get()
        print(f'name={self.account}, password={self.password}, otp_code={self.otp_code}')
        tkinter.messagebox.showinfo(title='Save', message='Complete')
        window.destroy()
        return True


if __name__ == '__main__':
    account = ''
    pw = ''
    work_dir = os.path.dirname(__file__)
    if len(sys.argv) > 1:
        if os.path.isdir(sys.argv[1]):
            work_dir = sys.argv[1]
    obj_authorization = Authorization(work_dir)
    # GUI
    window = Tk()
    window.title('Password + OTP code')
    window.geometry('300x200')
    window.maxsize(300, 130)  # int
    window.resizable(0, 0)  # cannot resize

    label1 = Label(window, text='account: ')
    name = StringVar()
    password = StringVar()
    otp_code = StringVar()
    btn = Button(window, text='Save', command=obj_authorization.gui_save)
    nameEntry = Entry(window, textvariable=name)
    nameEntry.config(font=('Arial', 11))
    label2 = Label(window, text='password: ')
    passwordEntry = Entry(window, show='*', textvariable=password)
    passwordEntry.config(font=('Arial', 11))
    label3 = Label(window, text='otp_code: ')
    otpEntry = Entry(window, textvariable=otp_code)
    otpEntry.config(font=('Arial', 11))
    label1.grid(row=0, column=0)
    nameEntry.grid(row=0, column=1)
    label2.grid(row=1, column=0)
    passwordEntry.grid(row=1, column=1)
    label3.grid(row=2, column=0)
    otpEntry.grid(row=2, column=1)
    btn.place(x=250, y=90)
    window.mainloop()

    if obj_authorization.account and obj_authorization.password:
        obj_authorization.encryption_vigenere_clt_account(obj_authorization.account, obj_authorization.password)
        obj_authorization.create_eclid_file()