import threading
import win32gui, win32ui, win32con

from PIL import Image
from time import sleep

class GameScreenMonitor():
    GAME_SCREEN_FILE = "game_screen.png"
    interval = 3.0

    def __init__(self, title, callback = None):
        self.title = title
        self.callback = callback
        threading.Thread(target=self.__loop_thread, daemon=True).start()

    def set_callback(self, callback):
        self.callback = callback

    def increase_interval(self):
        self.interval = self.interval + 0.5

    def decrease_interval(self):
        if self.interval >= 1:
            self.interval = self.interval - 0.5

    def get_interval(self):
        return self.interval
    
    def set_interval(self, seconds):
        self.interval = seconds
        if self.interval < 0.5:
            self.interval = 0.5
        return self.interval

    def __loop_thread(self):
        while True:
            sleep(self.interval)
            im = self.__get_screen()
            if im and self.callback:
                im.save(self.GAME_SCREEN_FILE)
                self.callback(self.GAME_SCREEN_FILE)

    def __get_screen(self):
        hwnd = win32gui.GetForegroundWindow()
        if win32gui.GetWindowText(hwnd) != self.title:
            return

        print("Get screen:", self.title)
        wndrect = win32gui.GetWindowRect(hwnd)
        clirect = win32gui.GetClientRect(hwnd)
        wnd_width = wndrect[2] - wndrect[0]
        wnd_height = wndrect[3] - wndrect[1]
        cli_width = clirect[2]
        cli_height = clirect[3]
        border = int((wnd_width - cli_width) / 2)

        wDC = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, wnd_width, wnd_height)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0), (wnd_width, wnd_height) , dcObj, (0,0), win32con.SRCCOPY)
        bmpinfo = dataBitMap.GetInfo()
        bmpstr = dataBitMap.GetBitmapBits(True)
        im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                            bmpstr, 'raw', 'BGRX', 0, 1)
        sx, sy = (border, wnd_height - cli_height - border)
        im = im.crop([sx, sy, sx + cli_width, sy + cli_height])

        return im