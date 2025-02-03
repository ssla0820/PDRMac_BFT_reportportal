import ctypes
class Mouse:
    """It simulates the mouse"""
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

    def _do_event(self, flags, x_pos, y_pos, data=0, extra_info=0):
        """generate a mouse event"""
        x_calc = int(65536 * x_pos / ctypes.windll.user32.GetSystemMetrics(self.SM_CXSCREEN) + 1)
        y_calc = int(65536 * y_pos / ctypes.windll.user32.GetSystemMetrics(self.SM_CYSCREEN) + 1)
        return ctypes.windll.user32.mouse_event(flags+ self.MOUSEEVENTF_ABSOLUTE, x_calc, y_calc, data, extra_info)

    def _get_button_value(self, button_name, button_up=False):
        """convert the name of the button into the corresponding value"""
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

    def move(self, x,y):
        """move the mouse to the specified coordinates"""
        if x <0 or y < 0: return
        self._do_event(self.MOUSEEVENTF_MOVE , x, y)

    def press_button(self, pos=(-1, -1), button_name="left", button_up=False):
        """push a button of the mouse"""
        self.move(*pos)
        self._do_event(self.get_button_value(button_name, button_up), 0, 0)

    def click(self,x,y, button_name= "left"):
        """Click at the specified placed"""
        self.move(x,y)
        self._do_event(self._get_button_value(button_name, False)+self._get_button_value(button_name, True), 0, 0)

    def double_click (self, x,y, button_name="left"):
        """Double click at the specifed placed"""
        for i in range(2): 
            self.click(x,y, button_name)

        
mouse=Mouse()