import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter import font

from datetime import datetime
from imgurpython import ImgurClient
from PIL import Image, ImageDraw, ImageFont

import os
import requests
import threading
import traceback
import sys
import webbrowser

from uwo_ps_app import towns_table
from uwo_ps_utils import market_rates_cropper as mrc

class MainApp(tk.Tk):
    __version__ = "0.9.0"
    PAD = "7"
    CLIENT_ID = '077727de8f6f20d'
    SUGGESTION = './suggestion.png'
    REPORT_IMG = './report_img.png'

    reporting = False
    suggestion_text = None
    last_estimate = ""

    def __init__(self, estimator, formatter,  monitor):
        tk.Tk.__init__(self)
        self.estimator = estimator
        self.formatter = formatter
        self.monitor = monitor

        self.title("UWO Price Share Aide")
        self.geometry("640x240")

        self.__create_menus()
        self.__create_ui()

        self.monitor.set_callback(self.on_screen_captured)

    def __create_menus(self):
        self.menubar = tk.Menu(self, tearoff=0, relief="raised")
        self.menubar.add("command", label="About",
                         command=self.menu_about, underline=0)
        self.menubar.add("separator")
        self.menubar.add("command", label="Send Suggestion",
                         command=self.menu_send_suggestion, underline=0)
        self.config(menu=self.menubar)

    def __create_ui(self):
        result_frame = tk.Frame(self, relief="flat", bd=1)
        result_frame.pack(side="top",
                          fill="x", expand=False)

        self.result_str = tk.StringVar()
        self.result_view = tk.Entry(result_frame,
                                    textvariable=self.result_str)
        self.result_view.pack(side="left", anchor="w",
                              padx=self.PAD, pady=self.PAD,
                              fill="x", expand=True)

        self.copy_btn = tk.Button(result_frame, text="Copy To Clipboard")
        self.copy_btn.pack(side="right", anchor="w",
                           padx=self.PAD, pady=self.PAD)
        self.copy_btn.bind("<Button-1>", self.copy_to_clipboard)

        info_frame = tk.Frame(self, relief="flat", bd=1)
        info_frame.pack(side="top",
                        fill="x", expand=False)
        interval_frame = tk.Frame(info_frame, relief="flat", bd=1)
        interval_frame.pack(side=tk.RIGHT)
        interval_lbl = tk.Label(interval_frame, text="Interval:")
        interval_lbl.pack(side=tk.LEFT)
        interval_dec = tk.Button(interval_frame, text="-", bd=1, width=1,
                                 command=self.__dec_interval)
        interval_dec.pack(side=tk.LEFT)
        self.interval = tk.StringVar()
        self.interval.set(str(self.monitor.get_interval()) + 's')
        self.interval_widget = tk.Label(interval_frame, 
                                        textvariable=self.interval,
                                        relief=tk.SUNKEN, bd=1, width=6)
        self.interval_widget.pack(side=tk.LEFT, padx=1, fill="y")
        interval_inc = tk.Button(interval_frame, text="+", bd=1, width=1,
                                 command=self.__inc_interval)
        interval_inc.pack(side=tk.LEFT, padx=(0, self.PAD))

        self.list_frame = tk.LabelFrame(self, text=" History ")
        self.list_frame.pack(side="bottom", anchor="n",
                             padx=self.PAD, pady="3",
                             fill="both", expand=True)
        self.list_box = tk.Listbox(self.list_frame, highlightthickness=0,
                                   bd=0, activestyle="none",
                                   selectmode=tk.EXTENDED)
        self.list_box.pack(side="top", anchor="n",
                           padx="0", pady="0",
                           fill="both", expand=True)

    def on_screen_captured(self, path):
        result = self.estimator.estimate(path)
        if not result:
            return
        self.last_screenshot = path

        result.insert(1, self.__get_current_town(result))
        # result = self.__verify_and_revise_rates(result, path)
        fmt_str = self.formatter.apply(result)
        if fmt_str != self.last_estimate:
            self.last_estimate = fmt_str
            self.result_str.set(fmt_str)
            self.copy_to_clipboard(None)

            self.log(self.result_str.get())
            self.attributes('-topmost', 1)
            self.attributes('-topmost', 0)

    def __get_current_town(self, result):
        nearbys = []
        for (town, _, _) in result[1:]:
            nearbys.append(town)
        current_town = towns_table.get_current_town(nearbys)
        return (current_town, result[0][1], result[0][2])

    # def __verify_and_revise_rates(self, result, path):
    #     rates = mrc.get_rates_from_bar(Image.open(path))
    #     rates.insert(0, 0)  # due to different index to result
    #     for i in range(1, len(rates)):
    #         if result[i][0] == "UNKNOWN":
    #             continue
    #         if (rates[i] - int(result[i][1])) ** 2 > 10:    # Revise wrong estimate
    #             result[i] = (result[i][0], str(rates[i]), result[i][2])

    #     return result

    def menu_about(self):
        webbrowser.open('https://github.com/ommokazza/uwo_ps_app')

    def __report_screenshot(self, path):
        im = mrc.clear_outside(path)
        im.save(self.REPORT_IMG)
        threading.Thread(target=self.__bug_report,
                         args=[self.REPORT_IMG]).start()

    def __bug_report(self, imgpath):
        if self.reporting:
            self.log("Can not reporting for now.")
            return
        self.reporting = True

        try:
            self.log(">> Reporting started")
            client = ImgurClient(self.CLIENT_ID, None)
            config = {
                'album': "lP33mCsHgZrsO8K",
                'title': self.__version__
                }
            image = client.upload_from_path(imgpath,
                                            config=config)
            deletehash = image['deletehash']
            url = 'https://api.imgur.com/3/image/' + deletehash
            headers = {'Authorization': 'Client-ID ' + self.CLIENT_ID}
            requests.post(url, headers=headers, data={'description': deletehash})
            self.log(image['link'])
            self.log("<< Reporting completed" )
            self.suggestion_text = None
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            for l in lines:
                self.log(l)
            self.log("<< Reporting Failed")
        finally:
            self.reporting = False

    def menu_send_suggestion(self):
        self.suggestion_window = tk.Toplevel(self)
        self.suggestion_window.geometry("480x320")
        self.suggestion_window.title("Send Suggestion / Bug Report")

        send_btn = tk.Button(self.suggestion_window, text="Send",
                             command=self.__send_suggestion)
        send_btn.pack(side="bottom",
                      padx="5", pady="5",
                      fill="x")
        self.suggestion_textview = tk.Text(self.suggestion_window)
        self.suggestion_textview.pack(side="top",
                                      padx="5", pady="5",
                                      fill="both", expand=True)
        if self.suggestion_text:
            self.suggestion_textview.insert(0.0, self.suggestion_text)

    def __send_suggestion(self):
        self.suggestion_text = self.suggestion_textview.get(1.0, tk.END)
        im = Image.new('RGB', (800, 600), (255,255,255))
        draw = ImageDraw.Draw(im)
        fnt = ImageFont.truetype('./NanumGothic.ttf', 12)
        draw.multiline_text((5, 5), self.suggestion_text,
                            font=fnt, fill=(0, 0, 0))
        im.save(self.SUGGESTION)
        self.suggestion_window.destroy()
        threading.Thread(target=self.__bug_report,
                         args=[self.SUGGESTION]).start()

    def copy_to_clipboard(self, event):
        self.clipboard_clear()
        self.clipboard_append(self.result_str.get())

    def __dec_interval(self):
        self.monitor.decrease_interval()
        self.interval.set(str(self.monitor.get_interval()) + 's')

    def __inc_interval(self):
        self.monitor.increase_interval()
        self.interval.set(str(self.monitor.get_interval()) + 's')
    
    def log(self, msg):
        size = self.list_box.size()
        message = '(%s) %s' % (datetime.now().strftime('%H:%M:%S'), msg)
        self.list_box.insert(size, message)
        self.list_box.see(size)

