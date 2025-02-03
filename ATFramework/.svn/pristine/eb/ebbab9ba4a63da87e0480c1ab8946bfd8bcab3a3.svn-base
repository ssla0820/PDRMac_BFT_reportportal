import configparser
import os
import time
import ctypes
import subprocess
import shutil
import re
import mmap
import socket
from contextlib import contextmanager
import pyperclip as pc
import platform
if platform.system() == 'Windows':
    from pywinauto import Desktop # for handling win32 window/control

from .driver.window import Window
from .driver.mouse import Mouse
from .driver.keyboard import Keyboard


mouse=Mouse()
keyboard=Keyboard()

class U:
    def __init__(self, email, pwd, is_prod=True, instance_name=None, **kwargs):
        self.email = email
        self.pwd = pwd
        self.is_prod = is_prod
        self.name_product = "U" if is_prod else "UBeta"
        self.instance_name = instance_name
        self.path_data = f"{os.getenv('localappdata')}\\CyberLink\\{self.name_product}{self.instance_name or ''}"
        self.name_exe = f"{self.name_product}-Messenger.exe"
        self.path_full = f"C:\\ProgramData\\CyberLink\\{self.name_product}\\{self.name_exe}"
        self.meeting = Meeting(self)
        
        self.pid = None
        self.window = None
    
    def update_ini(self):
        raw = """
        [Option]
        currentlang = 'ENU'
        fontlang = u'ENU'
        pageduration = 0.2
        isfirstlaunch = False
        msgfontsize = 14
        showtooltips = False
        useanimeffect = True
        rememberlogin = True
        startwithwindows = False
        keepintaskbar = True
        playsoundwithmessage = False
        enable_coredump = False
        sendmessagewheninputfinish = True
        enableautoupdate = True
        enable_memorydb = False
        disablehdpi = False
        colortheme = 'Black'
        showtutorialtips = False
        showaddcontacttutorialtips = False
        showmakegroupcalltutorialtips = False
        showmeetingtutorialtips = False
        supportraw = True
        checkupdatedatefromresumesuspend = 0
        checkupdatedatefrommeeting = 0
        checkupdatedatefrommeetingdowngradevideonotify = 0
        checkrelaunchfromresumesuspend = 0
        showdeletemessagewarning = True
        showautocompresswarning = True
        lasthttpcachecleartime = 1639994552
        showpfcupdatedlg = True
        pfcupdatedlgresult = True

        [you]
        term_of_use_check_date = '2033-1-1'
        term_of_use_time_stamp = u'2018-05-02'
        term_of_use_accepted = True
        rememberme = True

        [Browser]
        drawvideoicon = True
        drawvideoduration = True

        [PLProxy]
        check_proxy_timeout = 7
        disable_auto_proxy = False
        proxy_info = []

        [Meeting]
        enablewaitingroom = True
        enablewaitingroom2 = False
        waitingroomtype = 0

        [meetings]
        position = (0, 0)
        size = (1920, 1032)
        enable_minimode = True
        scrmini_mode = 1
        ismaxscreen = True
        delaycount = 1
        alwayshidesharefile = False
        enablesendlogtos = False
        fullscreen = False
        defaultspeaker = '*'
        defaultaudio = '*'
        """
        default = configparser.ConfigParser()
        u = configparser.ConfigParser()
        default.read_string(raw)
        os.makedirs(self.path_data, exist_ok=True)
        u.read(self.path_data + r"\settings.ini")
        u.update(default)
        with open(self.path_data + r"\settings.ini", 'w') as f: u.write(f)
        
    def ulog(self):
        return ULog(self.path_data)
        
    def launch(self, inst_name=None):
        print('enter Launch')
        inst_name = inst_name or self.instance_name
        if (exist := Window(title=f"U{inst_name}")).hwnd : 
            exist.close()
        instance = f"multipleinstance={inst_name}" if inst_name is not None else ""
        cmd = [self.path_full,
                                f"{instance}",
                                f"email={self.email}",
                                f"pwd={self.pwd}"]
        print(cmd)
        p = subprocess.Popen(cmd)
        self.pid = p.pid
        print(f'{self.pid=}')
        # self.hwnd = Window().get_hwnd(pid=p.pid, timeout = 180)
        self.hwnd = Window().get_hwnd(pid=p.pid, timeout=180)
        print(f'{self.hwnd=}')
        self.window = Window(pid=p.pid)
        print(f'{self.window=}')
        if not self.is_ui_ready(): raise Exception("UI is not found.")
        return p.pid

    @staticmethod
    def check_internet_connection(timeout=30, delay_per_run=1):  # timeout: min, delay_per_run: min
        time_start = time.time()
        curr_run = 1
        is_connected = False
        while time.time() - time_start < timeout * 60:
            try:
                print(f"[{curr_run}] checking internet connection..")
                socket.setdefaulttimeout(5)
                host = socket.gethostbyname("www.google.com")
                s = socket.create_connection((host, 80), 2)
                s.close()
                print('Internet is connected.')
                is_connected = True
                break
            except Exception as e:
                print(f'Exception occurs. error={e}')
                curr_run += 1
                time.sleep(delay_per_run * 60)
        return is_connected

    def launch_u(self, inst_name=None):
        print('enter Launch')
        if not self.check_internet_connection():
            raise Exception('No internet connection.')
        inst_name = inst_name or self.instance_name
        if (exist := Window(title=f"U{inst_name}")).hwnd :
            exist.close()
        instance = f"multipleinstance={inst_name}" if inst_name is not None else ""
        cmd = [self.path_full,
                                f"{instance}",
                                f"email={self.email}",
                                f"pwd={self.pwd}"]
        # print(cmd)
        p = subprocess.Popen(cmd)
        # self.pid = p.pid
        # print(f'{self.pid=}')
        # self.hwnd = Window().get_hwnd(pid=p.pid, timeout = 180)
        self.hwnd = Window().get_hwnd(title='U', timeout=180)
        print(f'{self.hwnd=}')
        self.window = Window(title='U')
        print(f'{self.window=}')
        if not self.is_ui_ready(): raise Exception("UI is not found.")
        # handle install upgrade
        self.handle_update_installation()
        return True

    def handle_update_installation(self, timeout=300):
        try:
            start_time = time.time()
            wnd_title = 'CyberLink'
            print('handle_update_installation')
            hwnd_install = Window().get_hwnd(title=wnd_title, class_name='Koan', timeout=5)
            print(f'Detect Install Dialog - {hwnd_install=}')
            is_install = False
            if hwnd_install:
                while time.time() - start_time < 30:
                    hwnd_install = Window().get_hwnd(title=wnd_title, class_name='Koan', timeout=5)
                    print(f'Detect Install Dialog - {hwnd_install=}')
                    if not hwnd_install:
                        time.sleep(3)
                        continue
                    ret = Window().is_visible(hwnd_install)
                    print(f'Install Dialog - is_visible={ret}')
                    if ret:
                        print(f'Install upgrade build dialog is visible')
                        is_install = True
                        Window().activate(hwnd_install)
                        time.sleep(2)
                        break
                    time.sleep(3)
            if is_install:
                print(f'Start to install upgrade build')
                rect = Window().get_rect(hwnd_install)
                mouse.click(rect.x + 334, rect.y + 183)
                Window().get_hwnd(title='Installing U', timeout=timeout - (time.time() - start_time))
                self.hwnd = Window().get_hwnd(title='U', class_name='U', timeout=timeout - (time.time() - start_time))
                if self.hwnd:
                    print(f'{self.hwnd=}')
                    self.window = Window(title='U', class_name='U')
                    print(f'{self.window=}')
                    is_visible = False
                    while time.time() - start_time < timeout:
                        ret = Window().is_visible(self.hwnd)
                        if ret:
                            is_visible = True
                            break
                        time.sleep(3)
                    if not is_visible:
                        raise Exception('U is Launched FAIL. Not visible - Timeout')
                    time.sleep(5)
                    print('U is ready NOW.')
                else:
                    print('U is launched FAIL.')
                    raise Exception('U is Launched FAIL.')
            else:
                print('No install upgrade build dialog is visible')
        except Exception as e:
            print(f'Exception occurs. error={e}')
            return False
        return True
        
    def is_ui_ready(self , timeout=30, window=None):
        # check visible
        app = Desktop(backend='win32')
        open_window = app.window(title='U', class_name='U')
        open_window.wait('visible', timeout=30)
        print('ui is visible now.')
        # timer = time.time()  # the adjust window size will be blocked by upgrade dialog
        # window = window if window else self.window
        # size_prev = window.rect.raw()[2:]
        # size_new = tuple((x+1 for x in size_prev))
        # while time.time()-timer < timeout:
        #     window.resize(*size_new)
        #     print(f'[is_ui_ready] {size_new=}')
        #     if window.rect.raw()[2:] == size_new:
        #         window.resize(*size_prev)
        #         return True
        # else:
        #     return False
        return True
    
    def is_ui_respond(self,timeout=30, window=None):
        timer = time.time()
        window = window if window else self.window
        while time.time()-timer < timeout:
            ret = ctypes.windll.user32.IsHungAppWindow(window.hwnd)
            if not ret: return True
        
        
    def close(self,force=False, timeout=5):
        if force:
            os.system(f"taskkill -f -im {U_EXE}")
            return True
        else:
            hwnd = self.hwnd or Window(title="U").hwnd
            ctypes.windll.user32.SendMessageW(hwnd, 0x10, 0, 0)
            pid = ctypes.wintypes.DWORD()
            timer = time.time()
            while time.time()-timer < timeout:
                if not ctypes.windll.user32.GetWindowThreadProcessId(hwnd,ctypes.byref(pid)):
                    return True
            else:
                print("Timeout, switch to force close mode")
                self.close(force=True)
        
    def clear_data(self):
        shutil.rmtree(self.path_data, ignore_errors=True)
        
    def click(self, x, y, button_name="left"):
        _x = self.window.rect.x + x
        _y = self.window.rect.y + y
        # print(f"click {_x},{_y}")
        mouse.click(_x, _y, button_name)
        
    def switch_tab(self, name):
        mapping_shift = {
            "home" : (-115, 80),
            "chats" : (-25, 80),
            "contacts" : (25, 80),
            "webinars" : (115, 80),
        }
        shift = mapping_shift.get(name, None)
        if shift:
            x_mid = int(self.window.rect.w/2)
            self.click(x_mid + shift[0], shift[1])

    def send_message_to_contact(self, name, message, is_first_message=False):
        # open chatroom from search
        shift = (80, 170)
        x_mid = int(self.window.rect.w / 2)
        self.click(x_mid + shift[0], shift[1])
        if is_first_message:
            time.sleep(2)
            self.click(x_mid - shift[0], shift[1])
            time.sleep(2)
        pc.copy(name)
        time.sleep(5)
        keyboard.press_control_a()
        time.sleep(3)
        keyboard.press_control_v()
        time.sleep(5)
        keyboard.press_key('enter')
        dlg_chatroom = Window(title=name, class_name="KOAN MSO DLG")
        dlg_chatroom.get_hwnd(timeout=10)
        if not self.is_ui_ready(window=dlg_chatroom): raise Exception("Chatroom Window is not ready")
        print('Chatroom window is ready.')
        # send message
        pc.copy(message)
        time.sleep(2)
        keyboard.press_control_v()
        time.sleep(1)
        keyboard.press_key('enter')
        time.sleep(2)
        print('send message ok')
        # close chatroom
        dlg_chatroom.close()
        return True




    
    def join(self, id, name=None):
        x_mid = int(self.window.rect.w/2)
        self.click(x_mid, 275)
        dlg_join = Window(title="Join meetings", class_name="KOAN MSO DLG")
        dlg_join.get_hwnd(timeout = 10)
        # print(f"{dlg_join=}")
        if not self.is_ui_ready(window=dlg_join): raise Exception("Join Window is not ready")
        keyboard.send(id)
        if name:
            keyboard.press_key("tab")
            keyboard.send(name)
        time.sleep(1)
        mouse.click(150, 310, hwnd=dlg_join.hwnd)
        #>> highcpu dlg
        dlg_highcpu = Window(title="CyberLink",class_name="Koan")

        x,y = None, None
        while (y:=dlg_highcpu.is_visible() and dlg_highcpu.hwnd) or (x:=dlg_join.is_visible() and dlg_join.hwnd):
            if y: mouse.click(170, 210, hwnd=y)
            time.sleep(0.3)
        #<< highcpu dlg
        meeting = Window(title="U Meeting", class_name="CLMeetingsMainWindow")
        meeting.get_hwnd(timeout = 30)
        print(f"{meeting.hwnd=}")
        return True
            
class Meeting:
    def __init__(self, u):
        #[MainWindow::onCallbackUpdateParticipant] <<
        #[Meeting] Query history chat msg before joined
        self.u = u
        self._log = None
        
    @property
    def log(self):
        self._log = self._log or self.u.ulog()
        return self._log 
        
    def is_ready(self, timeout = 30):
        return self.log.wait("\\[Meeting\\] Query history chat msg before joined", timeout = timeout)
        
    def get_participants_number(self):
        return int(self.log.find_last(f"\\[Meeting\\]\\[onParticipantUpdate\\] VIDEO_NUM (\d+)"))
        
    def wait_participants_number(self, number, timeout=60):
        return self.log.wait(f"\\[Meeting\\]\\[onParticipantUpdate\\] VIDEO_NUM {number}", timeout = timeout)
        
        
class ULog:
    def __init__(self, path_data):
        print(f"{path_data=}")
        files_all = next(os.walk(f"{path_data}\\dmp"), (None, None, []))[2]
        files_log = [x for x in reversed(files_all) if re.match("logger-[\d]{6}-[\d]{6}\.txt",x)]
        self.path = f"{path_data}\\dmp\\{files_log[0]}" if len(files_log) else ""
        print(f"U log path = {self.path}")
        self.log = open(self.path,"r", encoding="utf-8")
    
    def wait(self,find_string, timeout=30, seek=0):
        ''' from: 
                0 -> last query (from end if never queried)
                1 -> begin
                2 -> end
        '''
        if seek or not self.log.tell():
            self.log.seek(0,1 if seek == 1 else 2) 
        timer = time.time()
        ret = False
    
        # print(f"Search timestamp = {time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())}")
        while time.time()-timer < timeout:
            if re.match("[\w\W]*" + find_string, self.log.read()):
                ret = True
                break
        return ret
        
    def find_last(self, find_string):
        with mmap.mmap(self.log.fileno(),0,access=mmap.ACCESS_READ) as m:
            try:
                return re.findall( find_string , m.read().decode("utf-8"))[-1]
            except:
                return
        
        
def test_u_join_meeting():
    global receiver
    receiver = U(email="clsignupstress+audio_recv@gmail.com",
                 pwd=123123,
                 is_prod=True,
                 is_sender=False)
    receiver.clear_data()
    receiver.update_ini()
    receiver.launch()
    
    receiver.switch_tab("home")
    receiver.join(555988679)
    print(f"Meeting is ready? {receiver.meeting.is_ready()}")
    print(f"Meeting participants number? {receiver.meeting.get_participants_number()}")
    return receiver
        
def test_multiple_u():
    a = U("webinarsbugverify0621@gmail.com",
            "123123",
            True,
            "0")
    a.clear_data()
    a.update_ini()
    a.launch()
    return a
        
if __name__ == "__main__":
    u = test_u_join_meeting()
    # a = test_multiple_u()
