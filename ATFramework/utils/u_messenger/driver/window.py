import ctypes
import time
from ctypes.wintypes import ULONG

__all__ = ("Window")


SWP_NOSIZE     = 0x01
SWP_NOMOVE     = 0x02
SWP_SHOWWINDOW = 0x40
SWP_HIDEWINDOW = 0x80

try: # >= win 8.1
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except: # win 8.0 or less
    ctypes.windll.user32.SetProcessDPIAware()
class RECT(ctypes.Structure):
    _fields_ = [
        ('left',  ULONG ),
        ('top',    ULONG ),
        ('right',  ULONG ),
        ('bottom', ULONG )
    ]
    
    x = property(lambda self: ctypes.c_long(self.left).value)
    y = property(lambda self: ctypes.c_long(self.top).value)
    w = property(lambda self: self.right-self.x)
    h = property(lambda self: self.bottom-self.y)
    
    def __repr__(self):
        return f"x={self.x},y={self.y},w={self.w},h={self.h}"
    
    def raw(self):
        return self.x, self.y,self.w, self.h 

class Window:
    
    pid = property(lambda self: self.get_pid())
    hwnd = property(lambda self: self.get_hwnd())
    title = property(lambda self: self.get_title())
    rect = property(lambda self: self.get_rect())
    
    def __init__(self, pid=None, title=None, class_name=None, hwnd=None, client=False):
        self._pid = pid
        self._title = title
        self._class_name = class_name
        self._hwnd = hwnd
        self._client = client
        
    def enum_hwnd(self):
        EnumWindows = ctypes.windll.user32.EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        IsWindowVisible = ctypes.windll.user32.IsWindowVisible
        
        ret = []
        def foreach_window(hwnd, lParam):
            if IsWindowVisible(hwnd):
                ret.append(ctypes.cast(hwnd, ctypes.c_void_p).value)
        EnumWindows(EnumWindowsProc(foreach_window), 0)
        return ret
        
    def get_pid(self, title=None, class_name=None, hwnd=None):
        title = title or self._title
        class_name = class_name or self._class_name
        hwnd = hwnd or self._hwnd
        if title or class_name or hwnd:
            hwnd = hwnd or self.get_hwnd(title=title, class_name=class_name)
            pid = ctypes.wintypes.DWORD()
            ctypes.windll.user32.GetWindowThreadProcessId(hwnd,ctypes.byref(pid))
            return pid.value
        elif self._pid:
            return self._pid
        else:
            print("[Error] No input pid")
            return
        
    def get_hwnd(self, pid=None, title=None, class_name=None, get_all=False, timeout=0):
        print(f'get_hwnd - {pid=}')
        if self._hwnd is not None: return self._hwnd
        pid = pid if pid is not None else self._pid
        title = title or self._title
        class_name = class_name or self._class_name
        if title or class_name:
            timer =time.time()
            while True:
                if ret:=ctypes.windll.user32.FindWindowW(class_name,title):
                    return ret
                if time.time()-timer>timeout: return None
                
        elif pid is not None:
            print('enter pid section')
            timer = time.time()
            while True:
                hwnds = self.enum_hwnd()
                print(f'{hwnds=}')
                time.sleep(1)
                ret = []
                for hwnd in hwnds:
                    print(f'{hwnd=}, pid={self.get_pid(hwnd=hwnd)}')
                    if pid ==self.get_pid(hwnd=hwnd):
                        print(f'Match pid={pid}')
                        if not get_all and not ctypes.windll.user32.GetParent(hwnd):
                            print(f'find {hwnd=}')
                            return hwnd
                        else:
                            print(f'append {hwnd=}')
                            ret.append(hwnd)
                if ret or time.time() - timer > timeout:
                    return ret
        else:
            print("[Error] get hwnd fail")
            return
    
    def get_title(self, hwnd=None, pid=None):
        pid = pid or self._pid
        hwnd = hwnd or self._hwnd
        if hwnd or pid:
            hwnd = hwnd or self.get_hwnd(pid=pid)
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
            return buff.value
        else:
            print("[Error] get title fail")
            return
            
    def get_desktop(self):
        return self.__class__(class_name="Progman", title="Program Manager")
        # return ctypes.windll.user32.GetDesktopWindow()
    
    def get_desktop_(self):
        return self.__class__(hwnd = ctypes.windll.user32.GetDesktopWindow())
    
    def get_rect(self,hwnd=None, client=None):
        client =  client if client is not None else self._client
        getRect = [ ctypes.windll.user32.GetWindowRect, 
                    ctypes.windll.user32.GetClientRect][client]
        hwnd = hwnd or self._hwnd or self.get_hwnd()
        win_rect = RECT()
        getRect(hwnd, ctypes.byref(win_rect))
        return win_rect
        
    def activate(self, hwnd=None):
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        
    def get_activate(self):
        return ctypes.windll.user32.GetForegroundWindow()
        
    def set_console_title(self, hwnd=None):
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    
    def get_console_title(self, length=256):
        buffer = ctypes.create_unicode_buffer(length)
        types.windll.kernel32.GetConsoleTitleW(buffer, length)
        return buffer.value
    
    def set_pos(self,x=None, y=None, w=None, h=None, hwnd=None, flag=SWP_SHOWWINDOW):
        hwnd = hwnd or self.hwnd
        return bool(ctypes.windll.user32.SetWindowPos(hwnd, 0, x, y, h, w, flag))
        
    def move(self, x, y, hwnd=None):
        hwnd = hwnd or self.hwnd
        return self.set_pos(x=x, y=y, hwnd=hwnd, flag=SWP_NOSIZE)
    
    def resize(self, h, w, hwnd=None):
        return self.set_pos(w=w, h=h, hwnd=hwnd, flag=SWP_NOMOVE)
        
    def close(self, hwnd=None):
        ctypes.windll.user32.SendMessageW(hwnd or self.hwnd, 0x10, 0, 0)
        
    def is_visible(self,hwnd=None):
        hwnd = hwnd or self.hwnd
        return bool(ctypes.windll.user32.IsWindowVisible(hwnd))
    
if __name__ == "__main__":
    dt=Window().get_desktop()
    print(f"{dt.rect}")
    
    u = Window(title="U")
    pid = u.pid
    print(f"{pid=}")
    h = Window(pid=pid)
    print(f'{h=}')
    
    # for i, hwnd in enumerate(h.hwnd):
        # print(f"{i} - {h.get_rect(hwnd)}")
        
    # a = Window(pid=13444)
    # print(f"{a.hwnd=}")