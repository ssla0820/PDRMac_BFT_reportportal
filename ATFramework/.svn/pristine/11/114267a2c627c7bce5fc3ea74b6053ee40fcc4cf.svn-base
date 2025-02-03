import ctypes
from .window import Window

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_ulong), ("y", ctypes.c_ulong)]

ctypes.windll.shcore.SetProcessDpiAwareness(2)

class Mouse:
    MOUSEEVENTF_MOVE = 0x0001 # mouse move 
    MOUSEEVENTF_LEFTDOWN = 0x0002 # left button down 
    MOUSEEVENTF_LEFTUP = 0x0004 # left button up 
    MOUSEEVENTF_RIGHTDOWN = 0x0008 # right button down 
    MOUSEEVENTF_RIGHTUP = 0x0010 # right button up 
    MOUSEEVENTF_MIDDLEDOWN = 0x0020 # middle button down 
    MOUSEEVENTF_MIDDLEUP = 0x0040 # middle button up 
    MOUSEEVENTF_WHEEL = 0x0800 # wheel button rolled 
    MOUSEEVENTF_ABSOLUTE = 0x8000 # absolute move 
    SM_CXSCREEN = 0
    SM_CYSCREEN = 1
    
    
    def _do_event(self, flags, x_pos, y_pos, data, extra_info):
        x_calc = int(65536 * x_pos / ctypes.windll.user32.GetSystemMetrics(self.SM_CXSCREEN) + 1)
        y_calc = int(65536 * y_pos / ctypes.windll.user32.GetSystemMetrics(self.SM_CYSCREEN) + 1)
        return ctypes.windll.user32.mouse_event(flags, x_calc, y_calc, data, extra_info)

    def _get_button_value(self, button_name, button_up=False):
        buttons = 0
        if button_name.find("right") >= 0:
            buttons = self.MOUSEEVENTF_RIGHTDOWN
        if button_name.find("left") >= 0:
            buttons = buttons + self.MOUSEEVENTF_LEFTDOWN
        if button_name.find("middle") >= 0:
            buttons = buttons + self.MOUSEEVENTF_MIDDLEDOWN
        if button_up:
            buttons = buttons << 1
        return buttons

    def move(self, x, y):
        old_pos = self.get_position()
        x =  x if (x != -1) else old_pos[0]
        y =  y if (y != -1) else old_pos[1]    
        self._do_event(self.MOUSEEVENTF_MOVE + self.MOUSEEVENTF_ABSOLUTE, x, y, 0, 0)

    def press_button(self, x=-1, y=-1, button_name="left", button_up=False):
        self.move(x, y)
        self._do_event(self.get_button_value(button_name, button_up), 0, 0, 0, 0)

    def click(self, x=-1, y=-1, button_name= "left", hwnd=None):
        delta_x, delta_y = Window(hwnd=hwnd).rect.raw()[:2] if hwnd else (0, 0)
        self.move(x + delta_x, y + delta_y)
        self._do_event(self._get_button_value(button_name, False)+self._get_button_value(button_name, True), 0, 0, 0, 0)

    def double_click(self, pos=(-1, -1), button_name="left"):
        for i in xrange(2): 
            self.click(pos, button_name)
    
    @property
    def position(self):
        return self.get_position()
    
    @position.setter
    def position(self, args):
        args = args if isinstance(args, (list,tuple)) else [args]
        return self.set_position(*args[:2])
            
    
    def get_position(self):
        point = POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.pointer(point))
        return point.x, point.y
        
    def set_position(self, x=None, y=None):
        if not (x or y):
            _x, _y = self.get_position()
            x, y = x or _x, y or _y
        ctypes.windll.user32.SetCursorPos(x, y)
        
if __name__ == "__main__":
    m=Mouse()
    m.position = 1900,300