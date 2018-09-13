import matplotlib

matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt

import tkinter as tk
from tkinter import ttk

import urllib
import json

import pandas as pd
import numpy as np

# consts
LARGE_FONT = ('Verdona', 12)
style.use('ggplot')

# chart data
f = Figure()
a = f.add_subplot(111)  # 1x1 / 121 - #1x2 charts

# animation
pd.options.mode.chained_assignment = None


def animate(i):
    dataLink = 'https://wex.nz/api/3/trades/btc_usd?limit=2000'
    data = urllib.request.urlopen(dataLink)
    data = data.read().decode('utf-8')
    data = json.loads(data)

    data = data['btc_usd']
    data = pd.DataFrame(data)

    buys = data[(data['type'] == 'bid')]
    buys['datestamp'] = np.array(buys['timestamp']).astype('datetime64[s]')
    buyDates = (buys['datestamp']).tolist()

    sells = data[(data['type'] == 'ask')]
    sells['datestamp'] = np.array(sells['timestamp']).astype('datetime64[s]')
    sellDates = (sells['datestamp']).tolist()

    a.clear()

    a.plot_date(buyDates, buys['price'], '#00a3e0', label='buys')
    a.plot_date(sellDates, sells['price'], '#183a54', label='sells')

    a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3, ncol=2, borderaxespad=0)

    title = 'BTCe- BTCUSD Prices \nLast Price: ' + str(data['price'][1999])
    a.set_title(title)


class SeaofBTCapp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, 'default.ico')
        tk.Tk.wm_title(self, 'Sea of BTC client')

        container = tk.Frame(self)  # window
        container.pack(side='top', fill='both', expand=True)  # filling the window
        container.grid_rowconfigure(0, weight=1)  # 0 - size, weight=1 - priority
        container.grid_columnconfigure(0, weight=1)  # 0 - size, weight=1 - priority

        menubar = tk.Menu(container)

        self.frames = {}

        for F in (StartPage, PageOne, BTCe_Page):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0,
                       sticky='nsew')  # sticky='nsew' - north/south/east/west - aligning for the whole window

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()  # raise to the front page


def qaf(str):
    print(str)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Alpha Bitcoin trading application', font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text='Agree',
                             command=lambda: controller.show_frame(BTCe_Page))
        button1.pack()

        button2 = ttk.Button(self, text='Disagree',
                             command=quit)
        button2.pack()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Page One', font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text='Back Home',
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()


class BTCe_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Graph Page', font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text='Back Home',
                            command=lambda: controller.show_frame(StartPage))
        button.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        # canvas.show() - .show is deprecated
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar = NavigationToolbar2TkAgg(canvas, self) / NavigationToolbar2TkAgg - deprecated
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = SeaofBTCapp()
app.geometry('1280x720')
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()
