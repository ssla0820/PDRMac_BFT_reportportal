import ctypes

VK_TAB = 0x09 #TAB key
VK_SHIFT = 0x10 #SHIFT key
VK_CONTROL = 0x11 #CTRL key
VK_MENU = 0x12 #ALT key
VK_ESCAPE = 0x1B #ESC key
VK_ENTER = 0x0D # ENTER key (by Jim)

            
class Keyboard:
    def send(self, string):
        string = string if isinstance(string, str) else str(string)
        for char in string:
            if 0x30 <= ord(char) <= 0x39:
                keycode = ord(char)
            else:
                keycode = ord(char) & ~0x20
            if (~ord(char) & 0x20):
                print(f"^{hex(keycode)}")
                ctypes.windll.user32.keybd_event(VK_SHIFT, 0, 0, 0)
            ctypes.windll.user32.keybd_event(keycode, 0, 0, 0)
            ctypes.windll.user32.keybd_event(keycode, 0, 0x0002, 0)
            if (~ord(char) & 0x20):
                ctypes.windll.user32.keybd_event(VK_SHIFT, 0, 0x0002, 0)
                
    def press_key(self, key):
        table = {
            "tab" : VK_TAB,
            "enter": VK_ENTER
        }
        keycode = table.get(key,"")
        if keycode:
            ctypes.windll.user32.keybd_event(keycode, 0, 0, 0)
            ctypes.windll.user32.keybd_event(keycode, 0, 0x0002, 0)

    def press_control_v(self):
        ctypes.windll.user32.keybd_event(0x11, 0, 0, 0)
        ctypes.windll.user32.keybd_event(0x56, 0, 0, 0)
        ctypes.windll.user32.keybd_event(0x56, 0, 0x0002, 0)
        ctypes.windll.user32.keybd_event(0x11, 0, 0x0002, 0)

    def press_control_a(self):
        ctypes.windll.user32.keybd_event(0x11, 0, 0, 0)
        ctypes.windll.user32.keybd_event(0x41, 0, 0, 0)
        ctypes.windll.user32.keybd_event(0x41, 0, 0x0002, 0)
        ctypes.windll.user32.keybd_event(0x11, 0, 0x0002, 0)