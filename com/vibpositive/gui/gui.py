import tkinter as tki
from sys import platform
from tkinter import filedialog
from tkinter.font import Font

from settings import RSVP_FONT_DICT, RSVP_SHAPE, WPM
from wordfeed import WordFeed

master = tki.Tk()
master.title('Window Title')


class MainGui(object):

    def __init__(self, logger):
        self.logger = logger
        self.master = master
        self.master.attributes('-alpha', 0.0)
        self.master.WPM = WPM
        self._pause_flag = True
        self.master.geometry('{}x{}'.format(460, 350))
        self.master.geometry('{}x{}'.format(600, 600))
        #
        #
        self.input_frame = InputFrame(self.master, self)
        self.input_frame.pack(side=tki.TOP)

        self.rsvp_frame = RsvpFrame(self.master, self)
        self.rsvp_frame.pack(side=tki.TOP)

        self.control_frame = ControlFrame(self.master, self)

        self.rate_string = tki.StringVar()
        self.rate_seconds = tki.StringVar()
        self.time_elapsed = tki.StringVar()
        self.time_elapsed_int = int(0)
        self.display_frame = DisplayFrame(self.master, self)

        # #
        self.master.bind('<Escape>', lambda e: self.master.destroy())
        self.master.resizable(True, True)
        # #
        self.wordfeed = None
        self.update_wordfeed()
        self.control_frame.set_update_wpm()
        self.counter = 0
        #
        # self.apply_settings()
        # self.pause_resume()
        center(self.master)
        self.master.attributes('-alpha', 1.0)

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_rowconfigure(2, weight=1)

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)

    def apply_settings(self):
        pass

    def export_settings(self, path):
        pass

    def update_wordfeed(self, name=None, index=None, mode=None):
        self.logger.debug('This message should go to the log file')
        inext = self.wordfeed.inext if self.wordfeed else 0
        text = self.input_frame.entry.get()
        self.wordfeed = WordFeed(text, inext)
        self.rsvp_frame.update()
        self.update_rate()

    def update_rate(self):
        num_words, total_minutes = self.wordfeed.update_statistics(self.master.WPM)
        if num_words < 1:
            return
        stat_format = '{0} words in {1:.2f} minutes = {2} WPM'
        self.rate_string.set(
            stat_format.format(
                num_words,
                total_minutes,
                self.master.WPM,
                "%.1f" % (total_minutes * 60)
            )
        )

        seconds_format = '{0} seconds'
        divisor = 1

        if 60 <= (total_minutes * 60) < 3600:
            seconds_format = '{0} minutes'
            divisor = 60
        elif (total_minutes * 60) >= 3600:
            seconds_format = '{0} hours'
            divisor = 3600

        self.rate_seconds.set(
            seconds_format.format(
                "%.1f" % ((total_minutes * 60) / divisor)
            )
        )

    def update_rsvp(self):
        text = self.wordfeed.next()
        # print("next word:", text)
        if text is None:
            self.pause()
        else:
            self.rsvp_frame.display_text(text)

    def rsvp_kernel(self):
        self.update_rsvp()

        if self._pause_flag:
            return

        delay_ms = (60000 / self.master.WPM)

        self.counter = self.counter + 1
        self.time_elapsed_int += delay_ms

        # TODO: reset counter
        if delay_ms:
            self.master.after(int(delay_ms), self.rsvp_kernel)
            time_elapsed_format = '{0} seconds'

            self.time_elapsed.set(
                time_elapsed_format.format(
                    "%.1f" % (self.time_elapsed_int * 0.001)
                )
            )
            # print('time_elapsed_int', self.time_elapsed_int, 'self.time_elapsed_int * 0.001',
            #       self.time_elapsed_int * 0.001)

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
        # self.wordfeed.i()
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


class DisplayFrame(tki.Frame):
    def __init__(self, __master, gui):
        # tki.Frame.__init__(self, __master, bg='blue', width=600, height=200, pady=3)
        tki.Frame.__init__(self, __master, width=600, height=200, pady=3)
        self.grid(column=0, row=1, sticky="sew", columnspan=3)

        self.rate_label = tki.Label(self.master, textvariable=gui.rate_string)
        self.rate_seconds_label = tki.Label(self.master, textvariable=gui.rate_seconds)
        self.time_elapsed_label = tki.Label(self.master, textvariable=gui.time_elapsed)

        self.rate_label.pack(side=tki.TOP)
        self.rate_seconds_label.pack(side=tki.TOP)
        self.time_elapsed_label.pack(side=tki.TOP)

        self.label_open_file = tki.Label(
            self,
            text="File Explorer using Tkinter",
            fg="blue")
        self.label_open_file.grid(column=0, row=2)


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
        self.wpm = tki.IntVar(self.master)

        #
        self.gui = gui

        # for r in range(3):
        #     for c in range(3):
        #         tki.Label(self, text='R%s/C%s' % (r, c), borderwidth=1).grid(row=r, column=c)

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

        spin = tki.Spinbox(self, from_=1, to=999, textvariable=self.wpm)
        spin.grid(column=1, row=1)

        button_explore = tki.Button(self,
                                    text="Browse Files",
                                    command=self.browseFiles)

        button_exit = tki.Button(self,
                                 text="Exit",
                                 command=exit)

        # Grid method is chosen for placing
        # the widgets at respective positions
        # in a table like structure by
        # specifying rows and columns


        button_explore.grid(column=1, row=2)

        button_exit.grid(column=2, row=2)

    def set_update_wpm(self):
        self.wpm.set(self.master.WPM)
        self.wpm.trace('w', self.update_wpm)

    def update_wpm(self, *args):
        try:
            self.master.WPM = self.wpm.get()
            self.gui.update_wordfeed()
            self.gui.update_rate()
        except tki.TclError as e:
            if e == 'expected floating-point number but got ""':
                print("User erased spin")
                exit(99)

    # TODO: add flag to not execute reader
    def browseFiles(self):
        filename = filedialog.askopenfilename(filetypes=[('Epub files', '.epub')])

        self.gui.display_frame.label_open_file.configure(text="File Opened: " + filename)
