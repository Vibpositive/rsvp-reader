import tkinter as tki
from math import ceil
from sys import platform
from tkinter.font import Font

from settings import RSVP_FONT_DICT, RSVP_SHAPE, WPM
from wordfeed import WordFeed

master = tki.Tk()
master.title('Window Title')


class NewGui(object):

    def __init__(self):
        self.master = master
        self.master.attributes('-alpha', 0.0)
        self._pause_flag = True
        # self.master.geometry('{}x{}'.format(460, 350))
        self.master.geometry('{}x{}'.format(600, 600))
        # 
        #
        self.input_frame = InputFrame(self.master, self)
        self.input_frame.pack(side=tki.TOP)
        self.rsvp_frame = RsvpFrame(self.master, self)
        self.rsvp_frame.pack(side=tki.TOP)
        self.control_frame = ControlFrame(self.master, self)
        # self.control_frame.pack(side=tki.TOP)
        self.rate_string = rs = tki.StringVar()
        self.rate_label = tki.Label(self.master, textvariable=rs)
        self.rate_label.pack(side=tki.TOP)
        # #
        self.master.bind('<Escape>', lambda e: self.master.destroy())
        self.master.resizable(True, True)
        # #
        self.wordfeed = None
        self.update_wordfeed()
        #
        # self.apply_settings()
        # self.pause_resume()
        center(self.master)
        self.master.attributes('-alpha', 1.0)

    def apply_settings(self):
        pass

    def export_settings(self, path):
        pass

    def update_wordfeed(self, name=None, index=None, mode=None):
        inext = self.wordfeed.inext if self.wordfeed else 0
        text = self.input_frame.entry.get()
        self.wordfeed = WordFeed(text, inext)
        self.rsvp_frame.update()
        self.update_rate()

    def update_rate(self):
        num_words, total_minutes = self.wordfeed.get_statistics()
        if num_words < 1:
            return
        stat_format = '{0} words in {1:.2f} minutes = {2} WPM.'
        self.rate_string.set(
            stat_format.format(
                num_words,
                total_minutes,
                WPM
            )
        )

    def update_rsvp(self):
        text = self.wordfeed.next()
        print("next word:", text)
        if text is None:
            self.pause()
        else:
            self.rsvp_frame.display_text(text)

    def rsvp_kernel(self):
        if self._pause_flag:
            return
        self.update_rsvp()
        delay_ms = ceil(60000 / 350)
        print(delay_ms)
        if delay_ms:
            self.master.after(delay_ms, self.rsvp_kernel)

    def pause_resume(self, event=None):
        if self._pause_flag:
            self.resume()
        else:
            self.pause()

    def pause(self, event=None):
        self._pause_flag = True
        # print('pause')

    def resume(self, event=None):
        self._pause_flag = False
        # print('resume')
        self.rsvp_kernel()

    def back10(self, event=None):
        # print('back 10')
        self.wordfeed.inext -= 10
        self.update_rsvp()

    def back50(self, event=None):
        # print('back 50')
        self.wordfeed.inext -= 50
        self.update_rsvp()


class InputFrame(tki.Frame):
    def __init__(self, master, gui):
        tki.Frame.__init__(self, master)
        self.gui = gui
        self.inputvar = tki.StringVar(value='''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras ornare lorem quis nunc porttitor, eu porttitor tellus bibendum. Cras tincidunt ullamcorper egestas. Integer hendrerit sit amet purus eget vehicula. Donec in orci in quam condimentum auctor hendrerit ut sapien. Nunc at ultrices risus. Praesent facilisis mauris at libero lacinia, at tincidunt felis fringilla. Donec egestas nulla sed ligula porttitor convallis. Donec tincidunt justo turpis, non venenatis enim fermentum et. Nulla augue odio, vulputate nec malesuada vel, placerat interdum nisi. Nam condimentum interdum justo, vitae ultricies libero imperdiet quis. Suspendisse posuere arcu leo, id gravida mauris consequat a.

Nam accumsan massa in cursus euismod. Morbi massa velit, lacinia in tellus sed, varius convallis purus. Mauris et orci non purus ultrices pharetra. Quisque tincidunt mattis sagittis. Mauris id laoreet tellus, eu porttitor ante. Nulla eget elementum libero. Cras et odio ut ante convallis molestie eu iaculis urna. Vivamus ultrices metus quam, in lobortis mauris dictum sit amet. Maecenas porta sapien congue ligula sodales iaculis. Morbi eget purus ut augue semper dapibus. Fusce vel libero nibh. Nunc justo nisl, porta quis lacus eget, mollis sagittis nulla. Duis finibus ligula ac tellus eleifend ultricies. Donec consectetur accumsan lectus.

Donec rutrum euismod vehicula. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Proin lacus arcu, vehicula ac urna a, accumsan convallis eros. Morbi eros erat, ultricies vitae varius in, bibendum euismod sapien. Aenean eu mauris lorem. Integer venenatis, lectus ac consequat semper, urna nulla posuere quam, ut lobortis arcu mauris eget velit. Quisque neque velit, pellentesque ac felis nec, euismod ullamcorper magna. Sed a mauris eget tortor volutpat blandit. Ut egestas feugiat odio a fringilla. Nunc in tellus tempus, finibus lacus eu, fermentum justo. Morbi ullamcorper erat a neque pulvinar, at faucibus justo facilisis. Vestibulum a eros magna. Aenean maximus semper.''')
        self.inputvar.trace('w', self.gui.update_wordfeed)
        self.entry = tki.Entry(self, textvariable=self.inputvar, width=50)
        self.entry.pack()

        sel_all_cmd = '<Command-a>' if platform == 'darwin' else '<Control-a>'
        self.entry.bind(sel_all_cmd, self.select_all)

    def select_all(self, event=None):
        self.entry.selection_range(0, tki.END)
        return 'break'


def center(root):
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()

    frm_width = root.winfo_rootx() - root.winfo_x()
    win_width = width + 2 * frm_width
    title_bar_height = root.winfo_rooty() - root.winfo_y()
    win_height = height + title_bar_height + frm_width
    x = root.winfo_screenwidth() // 2 - win_width // 2
    y = (root.winfo_screenheight() // 2 - win_height // 2) - 75

    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    root.deiconify()


class RsvpFrame(tki.Frame):
    def __init__(self, master, gui):
        tki.Frame.__init__(self, master)
        self.gui = gui
        self.font = Font(**RSVP_FONT_DICT)
        self.shape = width, height = RSVP_SHAPE
        self.canvas = tki.Canvas(self, width=width, height=height)

        self.t1 = self.canvas.create_text(300, height / 2, text='a ', anchor='e', font=("Courier", 25))
        self.t2 = self.canvas.create_text(300, height / 2, text='b', anchor='e', font=("Courier", 25), fill='red')
        self.t3 = self.canvas.create_text(300, height / 2, text='c', anchor='w', font=("Courier", 25))

        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.gui.pause_resume)

    def display_text(self, text):
        middle = (len(text) + 1) // 2

        self.canvas.itemconfigure(self.t1, text=text[:middle - 1] + ' ')
        self.canvas.itemconfigure(self.t2, text=text[middle - 1:middle], fill='red')
        self.canvas.itemconfigure(self.t3, text=text[middle:])


class ControlFrame(tki.Frame):
    def __init__(self, __master, gui):

        tki.Frame.__init__(self, __master, bg='yellow', width=600, height=100, pady=3)

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_rowconfigure(2, weight=1)

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)

        self.pack_propagate(False)
        self.master.pack_propagate(False)

        self.grid(column=0, row=2, sticky="nsew", columnspan=3)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        #
        self.gui = gui

        for r in range(3):
            for c in range(3):
                tki.Label(self, text='R%s/C%s' % (r, c), borderwidth=1).grid(row=r, column=c)

        b = self.pause_button = tki.Button(
            self,
            text='Play/Pause',
            command=gui.pause_resume)
        b.grid(column=0, row=0)

        b = self.back10_button = tki.Button(
            self,
            text='< 10',
            command=gui.back10)
        b.grid(column=1, row=0)

        b = self.back50_button = tki.Button(
            self,
            text='< 50',
            command=gui.back50)
        b.grid(column=2, row=0)

        # wpm.set(WPM)
        # wpm = tki.IntVar(self.master)
        # spin = tki.Spinbox(self, from_=1, to=999, textvariable=wpm)
        spin = tki.Spinbox(self, from_=1, to=999)
        spin.grid(column=1, row=1)
def nothing():
    print("nothing")