""" Make screenshots of windows on Windows and Linux.
We need this to do visual tests.
"""
 
import sys
import os
import uuid
import ctypes
from ctypes import windll,  WINFUNCTYPE, POINTER
from ctypes.wintypes import (BOOL, DOUBLE, DWORD, HBITMAP, HDC, HGDIOBJ,  
                             HWND, INT, LPARAM, LONG, UINT, WORD)  

import numpy as np
import cv2

from .window import Window


try: # >= win 8.1
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except: # win 8.0 or less
    ctypes.windll.user32.SetProcessDPIAware()
    
CAPTUREBLT = 0x40000000 #transparent / menu window
SRCCOPY = 0x00CC0020
DWMWA_EXTENDED_FRAME_BOUNDS = 0x9
DIB_RGB_COLORS = BI_RGB = 0
TEMP = os.environ.get('temp',".")

class POINT(ctypes.Structure):
    _fields_ = [('x', ctypes.c_long),
                ('y', ctypes.c_long)]

class RECT(ctypes.Structure):
    _fields_ = [('left', ctypes.c_long),
                ('top', ctypes.c_long),
                ('right', ctypes.c_long),
                ('bottom', ctypes.c_long)]
    x = property(lambda self: ctypes.c_long(self.left).value)
    y = property(lambda self: ctypes.c_long(self.top).value)
    w = property(lambda self: self.right-self.x)
    h = property(lambda self: self.bottom-self.y)
    
    def __repr__(self):
        return f"x:{self.x},y:{self.y},w:{self.w},h:{self.h}"
    
    def init(self, x, y, w, h):
        self.left = x
        self.top = y
        self.right = x+w
        self.bottom = y+h
        return self
    
    def raw(self):
        return self.x, self.y,self.w, self.h
        
    def get_dict(self):
        return {"x":self.x, "y":self.y, "w":self.w, "h":self.h}
            
class BITMAPINFOHEADER(ctypes.Structure):
        _fields_ = [('biSize', DWORD), ('biWidth', LONG), ('biHeight', LONG),
                    ('biPlanes', WORD), ('biBitCount', WORD),
                    ('biCompression', DWORD), ('biSizeImage', DWORD),
                    ('biXPelsPerMeter', LONG), ('biYPelsPerMeter', LONG),
                    ('biClrUsed', DWORD), ('biClrImportant', DWORD)]
 
class BITMAPINFO(ctypes.Structure):
    _fields_ = [('bmiHeader', BITMAPINFOHEADER), ('bmiColors', DWORD * 3)]


GetClientRect = windll.user32.GetClientRect
GetWindowRect = windll.user32.GetWindowRect
ClientToScreen = windll.user32.ClientToScreen
DwmGetWindowAttribute = ctypes.windll.dwmapi.DwmGetWindowAttribute
PrintWindow = windll.user32.PrintWindow
GetWindowThreadProcessId = windll.user32.GetWindowThreadProcessId
IsWindowVisible = windll.user32.IsWindowVisible
GetSystemMetrics = windll.user32.GetSystemMetrics
GetDesktopWindow = windll.user32.GetDesktopWindow
EnumDisplayMonitors = windll.user32.EnumDisplayMonitors
EnumWindows = windll.user32.EnumWindows


EnumWindowsProc = WINFUNCTYPE(ctypes.c_bool,
                                     ctypes.POINTER(ctypes.c_int),
                                     ctypes.POINTER(ctypes.c_int))
MonitorNumProc = WINFUNCTYPE(INT, DWORD, DWORD, POINTER(RECT), DOUBLE)
 
GetWindowDC = windll.user32.GetWindowDC
GetDC = windll.user32.GetDC
CreateCompatibleDC = windll.gdi32.CreateCompatibleDC
CreateCompatibleBitmap = windll.gdi32.CreateCompatibleBitmap
SelectObject = windll.gdi32.SelectObject
BitBlt = windll.gdi32.BitBlt
DeleteObject = windll.gdi32.DeleteObject
GetDIBits = windll.gdi32.GetDIBits
 
# Arg types
windll.user32.GetWindowDC.argtypes = [HWND]
windll.gdi32.CreateCompatibleDC.argtypes = [HDC]
windll.gdi32.CreateCompatibleBitmap.argtypes = [HDC, INT, INT]
windll.gdi32.SelectObject.argtypes = [HDC, HGDIOBJ]
windll.gdi32.BitBlt.argtypes = [HDC, INT, INT, INT, INT, HDC, INT, INT, DWORD]
windll.gdi32.DeleteObject.argtypes = [HGDIOBJ]
windll.gdi32.GetDIBits.argtypes = [HDC, HBITMAP, UINT, UINT, ctypes.c_void_p,
                                    ctypes.POINTER(BITMAPINFO), UINT]
# Return types
windll.user32.GetWindowDC.restypes = HDC
windll.gdi32.CreateCompatibleDC.restypes = HDC
windll.gdi32.CreateCompatibleBitmap.restypes = HBITMAP
windll.gdi32.SelectObject.restypes = HGDIOBJ
windll.gdi32.BitBlt.restypes = BOOL
windll.gdi32.GetDIBits.restypes = INT
windll.gdi32.DeleteObject.restypes = BOOL




class Image():
    def get_dwm_rect(self, hwnd):
        rect = RECT()
        DwmGetWindowAttribute(HWND(hwnd),
                              DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
                              ctypes.byref(rect),
                              ctypes.sizeof(rect)
                              )
        return rect

    def get_monitor(self, index=None):
        mon = [{
            "x":int(GetSystemMetrics(76)), # SM_XVIRTUALSCREEN
            "y":int(GetSystemMetrics(77)), # SM_YVIRTUALSCREEN
            "w":int(GetSystemMetrics(78)), # SM_CXVIRTUALSCREEN
            "h":int(GetSystemMetrics(79)), # SM_CYVIRTUALSCREEN
        }]
        def _callback(monitor, data, lp_rect, dc_):
            rect = lp_rect.contents
            mon.append(rect.get_dict())
            return 1
        callback = MonitorNumProc(_callback)
        EnumDisplayMonitors(0, 0, callback, 0)
        return mon if index is None else mon[index]
    
    def screenshot_raw(self, hwnd=0, monitor=0, background_mode=False):
        
        
        shift = 0
        if hwnd:
            rect_w = RECT()
            GetWindowRect(hwnd, ctypes.byref(rect_w))
            rect = self.get_dwm_rect(hwnd)
            shift = int((rect_w.w-rect.w)/2)
            x,y,w,h = rect.raw()
        else:
            # print("Using desktop hwnd")
            hwnd = 0
            rect = self.get_monitor(monitor)
            x, y, w, h = [rect.get(i) for i in ["x","y","w","h"]] # ensure correct order only
        # w,h = 993, 519
        # h=593
        # x,y,w,h = 94,50,1426,737
        # print(f"{x=},{y=},{w=},{h=}, {shift=}")
        if background_mode:
            x = shift
            y = 0
        hwndDC = saveDC = bmp = None
        try:
            # Get device contexts
            hwndDC = GetWindowDC(hwnd if background_mode else 0) 
            saveDC = CreateCompatibleDC(hwndDC)
            # Get bitmap
            bmp = CreateCompatibleBitmap(hwndDC, w, h)
            SelectObject(saveDC, bmp)
            
            BitBlt(
                saveDC,
                0,
                0,
                w,
                h,
                hwndDC,
                x,
                y,
                SRCCOPY|CAPTUREBLT,
            )
            # PrintWindow(hwnd, saveDC,1)

            buffer_len = h * w * 4
            bmi = BITMAPINFO()
            bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
            bmi.bmiHeader.biWidth = w
            bmi.bmiHeader.biHeight = -h 
            bmi.bmiHeader.biPlanes = 1  # Always 1
            bmi.bmiHeader.biBitCount = 32
            bmi.bmiHeader.biCompression = BI_RGB
            # print(f"1 -> {time.time()-timer:10f}ms")
            # Blit
            image_raw = ctypes.create_string_buffer(buffer_len)
            
            bits = windll.gdi32.GetDIBits(saveDC, bmp, 0, h, image_raw, bmi, DIB_RGB_COLORS)
            
            image = np.frombuffer(image_raw, dtype=np.uint8).reshape(h,w,4)
               
            
         
        finally:
            # Clean up
            if hwndDC:
                DeleteObject(hwndDC)
            if saveDC:
                DeleteObject(saveDC)
            if bmp:
                DeleteObject(bmp)
        return image
        
    def screenshot(self, file=None, ext="png", hwnd=None, monitor=0):
        file = file or f"{TEMP}/{uuid.uuid4()}.{ext}"
        raw = self.screenshot_raw(hwnd, monitor)
        cv2.imwrite(file, raw)


def show(hwnd, client=False):
    img_ori = screenshot(hwnd,client)
    rect = Window(hwnd=hwnd,client=client).get_rect()
    img = np.frombuffer(img_ori, dtype=np.uint8).reshape(rect.h, rect.w,4)
    print(f"2 -> {time.time()-timer:10f}ms")
    print(rect)
    img = cv2.resize(img, (960, 540), interpolation=cv2.INTER_AREA)
    cv2.imshow("show",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




# test
def test_monitor():
    monitors = Image().get_monitor()
    for i,monitor in enumerate(monitors):
        print(f"Monitor-{i}: \t {monitor}")
    
def test_screenshot_raw():
    div_size = 2
    for i in range(3):
        try:
            img = Image().screenshot_raw(monitor=i)
            h,w = [int(x/div_size) for x in img.shape[:2]]
            img = cv2.resize(img, (w,h), interpolation=cv2.INTER_AREA)
            cv2.imshow("Full screen" if not i else f"Monitor-{i}",img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except:
            break
    print(f"{i-1} monitor(s)")
    
    
def test_screenshot_raw_hwnd():
    hwnd = 0xA0568
    # hwnd = Window(class_name="U").get_hwnd()
    div_size=1
    img = Image().screenshot_raw(hwnd=hwnd,background_mode=True)
    h,w = [int(x/div_size) for x in img.shape[:2]]
    img = cv2.resize(img, (w,h), interpolation=cv2.INTER_AREA)
    cv2.imshow(f"hwnd- {hex(hwnd)}",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

if __name__ == '__main__':
    import time
    
    
    # timer = time.time()
    # im= screenshot(Window().get_desktop().get_hwnd()) #.get_hwnd()
    # print(f"2 -> {time.time()-timer:10f}ms")
    # img = np.frombuffer(im, dtype=np.uint8).reshape(1080,1920,4)
    # print(f"3 -> {time.time()-timer:10f}ms")
    # img1 = cv2.cvtColor(img,cv2.COLOR_BGRA2GRAY)
    # print(f"4 -> {time.time()-timer:10f}ms")
    # cv2.imshow("test2",img)
    # cv2.waitKey()
    # show(Window().get_desktop().get_hwnd())
    # window = Window(title="Program Manager").get_hwnd()
    # window = ctypes.windll.user32.GetDesktopWindow()
    # print(f"{window=}")
    # show(window)
    # show(window,True)
    # mon = get_monitor()
    # test_monitor()
    # test_screenshot_raw()
    test_screenshot_raw_hwnd()