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
NORM_FONT = ('Verdona', 10)
SMALL_FONT = ('Verdona', 8)

style.use('ggplot')

# chart data
f = Figure()
a = f.add_subplot(111)  # 1x1 / 121 - #1x2 charts

exchange = 'BTC-e'
DatCounter = 9000
programName = 'btce'
resampleSize = '15Min'
DataPace = '1d'
candleWidth = 0.008
# indicators
topIndicator = 'none'
middleIndicator = 'none'
bottomIndicator = 'none'
SMAs = []
EMAs = []


# popup message
def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title('!')
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side='top', fill='x', pady=10)
    B1 = ttk.Button(popup, text='Ok', command=popup.destroy)
    B1.pack()
    popup.mainloop()


# Change Exchange
def changeExchange(toWhat, pn):
    global exchange
    global DatCounter
    global programName

    exchange = toWhat
    programName = pn
    DatCounter = 9000


def addTopIndicator(what):
    global topIndicator
    global DatCounter

    if DataPace == 'tick':
        popupmsg('Indicators in Tick Data not available.')

    elif what == 'none':
        topIndicator = what
        DatCounter = 9000

    elif what == 'rsi':
        rsiQ = tk.Tk()
        rsiQ.wm_title('Periods?')
        label = ttk.Label(rsiQ, text='Choose how many periods you want each RSI calculation to consider.')
        label.pack(side='top', fill='x', pady=10)

        e = ttk.Entry(rsiQ)
        e.insert(0, 14)
        e.pack()
        e.focus_set()

        def callback():
            global topIndicator
            global DatCounter

            periods = (e.get())
            group = []
            group.append('rsi')
            group.append(periods)

            topIndicator = group
            DatCounter = 9000
            print('Set top indicator to', group)
            rsiQ.destroy()

        b = ttk.Button(rsiQ, text='Submit', width=10, command=callback)
        b.pack()
        tk.mainloop()


    elif what == 'macd':
        topIndicator = 'macd'
        DatCounter = 9000


def addMiddleIndicator(what):
    global middleIndicator
    global DatCounter

    if DataPace == 'tick':
        popupmsg('Indicators in Tick Data not available.')
    if what != 'none':
        if middleIndicator == 'none':
            if what == 'sma':
                midIQ = tk.Tk()
                midIQ.wm_title('Periods?')
                label = ttk.Label(midIQ, text='Choose how many periods your SMA you  want to be.')
                label.pack(side='top', fill='x', pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0, 10)
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicator
                    global DatCounter

                    middleIndicator = []
                    periods = (e.get())
                    group = []
                    group.append('sma')
                    group.append(int(periods))
                    middleIndicator.append(group)
                    DatCounter = 9000
                    print('Middle Indicator set to: ', middleIndicator)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text='Submit', width=10, command=callback)
                b.pack()
                tk.mainloop()

            if what == 'ema':
                midIQ = tk.Tk()
                midIQ.wm_title('Periods?')
                label = ttk.Label(midIQ, text='Choose how many periods your SMA you  want to be.')
                label.pack(side='top', fill='x', pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0, 10)
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicator
                    global DatCounter

                    middleIndicator = []
                    periods = (e.get())
                    group = []
                    group.append('ema')
                    group.append(int(periods))
                    middleIndicator.append(group)
                    DatCounter = 9000
                    print('Middle Indicator set to: ', middleIndicator)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text='Submit', width=10, command=callback)
                b.pack()
                tk.mainloop()
        else:
            if what == 'sma':
                midIQ = tk.Tk()
                midIQ.wm_title('Periods?')
                label = ttk.Label(midIQ, text='Choose how many periods your SMA you  want to be.')
                label.pack(side='top', fill='x', pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0, 10)
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicator
                    global DatCounter

                    # middleIndicator = []
                    periods = (e.get())
                    group = []
                    group.append('sma')
                    group.append(int(periods))
                    middleIndicator.append(group)
                    DatCounter = 9000
                    print('Middle Indicator set to: ', middleIndicator)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text='Submit', width=10, command=callback)
                b.pack()
                tk.mainloop()

            if what == 'ema':
                midIQ = tk.Tk()
                midIQ.wm_title('Periods?')
                label = ttk.Label(midIQ, text='Choose how many periods your SMA you  want to be.')
                label.pack(side='top', fill='x', pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0, 10)
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicator
                    global DatCounter

                    # middleIndicator = []
                    periods = (e.get())
                    group = []
                    group.append('ema')
                    group.append(int(periods))
                    middleIndicator.append(group)
                    DatCounter = 9000
                    print('Middle Indicator set to: ', middleIndicator)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text='Submit', width=10, command=callback)
                b.pack()
                tk.mainloop()
    else:
        middleIndicator = 'none'


def addBottomIndicator(what):
    global bottomIndicator
    global DatCounter

    if DataPace == 'tick':
        popupmsg('Indicators in Tick Data not available.')

    elif what == 'none':
        bottomIndicator = what
        DatCounter = 9000

    elif what == 'rsi':
        rsiQ = tk.Tk()
        rsiQ.wm_title('Periods?')
        label = ttk.Label(rsiQ, text='Choose how many periods you want each RSI calculation to consider.')
        label.pack(side='top', fill='x', pady=10)

        e = ttk.Entry(rsiQ)
        e.insert(0, 14)
        e.pack()
        e.focus_set()

        def callback():
            global bottomIndicator
            global DatCounter

            periods = (e.get())
            group = []
            group.append('rsi')
            group.append(periods)

            bottomIndicator = group
            DatCounter = 9000
            print('Set bottom indicator to', group)
            rsiQ.destroy()

        b = ttk.Button(rsiQ, text='Submit', width=10, command=callback)
        b.pack()
        tk.mainloop()


    elif what == 'macd':
        bottomIndicator = 'macd'
        DatCounter = 9000


def changeTimeFrame(tf):
    global DatCounter
    global DataPace
    if tf == '7d' and resampleSize == '1Min':
        popupmsg('Too much data chosen, choose a smaller time frame or higher OHLC interval')
    else:
        DataPace = tf
        DatCounter = 9000


def changeSampleSize(size, width):
    global resampleSize
    global DatCounter
    global candleWidth
    if DataPace == '7d' and resampleSize == '1Min':
        popupmsg('Too much data chosen, choose a smaller time frame or higher OHLC interval')
    elif DataPace == 'tick':
        popupmsg('You\'re currently viewing tick data, not OHLC. ')
    else:
        resampleSize = size
        DatCounter = 9000
        candleWidth = width


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
    buys['datestamp'] = np.array(buys['timestamp']).astype('datetime64[ms]')
    buyDates = (buys['datestamp']).tolist()

    sells = data[(data['type'] == 'ask')]
    sells['datestamp'] = np.array(sells['timestamp']).astype('datetime64[ms]')
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

        # Filemenu menubar
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Save settings', command=lambda: popupmsg('Not available yet..'))
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=quit)
        menubar.add_cascade(label='File', menu=filemenu)

        # Exchange menubar
        exchangeChoise = tk.Menu(menubar, tearoff=1)
        exchangeChoise.add_command(label='BTC-e',
                                   command=lambda: changeExchange('BTC-e', 'btce'))
        exchangeChoise.add_command(label='Bitfinex',
                                   command=lambda: changeExchange('Bitfinex', 'bitfinex'))
        exchangeChoise.add_command(label='Bitstamp',
                                   command=lambda: changeExchange('Bitstamp', 'bitstamp'))
        exchangeChoise.add_command(label='Huobi',
                                   command=lambda: changeExchange('Huobi', 'huobi'))
        menubar.add_cascade(label='Exchange', menu=exchangeChoise)

        # DataTF menubar
        dataTF = tk.Menu(menubar, tearoff=1)
        dataTF.add_command(label='Tick',
                           command=lambda: changeTimeFrame('tick'))
        dataTF.add_command(label='1 Day',
                           command=lambda: changeTimeFrame('1d'))
        dataTF.add_command(label='3 Day',
                           command=lambda: changeTimeFrame('3d'))
        dataTF.add_command(label='1 Week',
                           command=lambda: changeTimeFrame('7d'))
        menubar.add_cascade(label='Data Time Frame', menu=dataTF)

        # OpenHighLevelClose Interval
        OHLCI = tk.Menu(menubar, tearoff=1)
        OHLCI.add_command(label='Tick',
                          command=lambda: changeTimeFrame('tick'))
        OHLCI.add_command(label='1 Minute',
                          command=lambda: changeSampleSize('1Min', 0.0005))
        OHLCI.add_command(label='5 Minute',
                          command=lambda: changeSampleSize('5Min', 0.003))
        OHLCI.add_command(label='15 Minutes',
                          command=lambda: changeSampleSize('15Min', 0.008))
        OHLCI.add_command(label='30 Minutes',
                          command=lambda: changeSampleSize('30Min', 0.16))
        OHLCI.add_command(label='1 Hour',
                          command=lambda: changeSampleSize('1Hr', 0.32))
        OHLCI.add_command(label='3 Hours',
                          command=lambda: changeSampleSize('3Hr', 0.96))

        menubar.add_cascade(label='OHLC', menu=OHLCI)

        # Indicators TOP
        topI = tk.Menu(menubar, tearoff=1)
        topI.add_command(label='None',
                         command=lambda: addTopIndicator('none'))
        topI.add_command(label='RSI',
                         command=lambda: addTopIndicator('rsi'))
        topI.add_command(label='MACD',
                         command=lambda: addTopIndicator('macd'))

        menubar.add_cascade(label='Top Indicator', menu=topI)

        # Indicators Main/Middle
        mainI = tk.Menu(menubar, tearoff=1)
        mainI.add_command(label='None',
                          command=lambda: addMiddleIndicator('none'))
        mainI.add_command(label='SMA',
                          command=lambda: addMiddleIndicator('sma'))
        mainI.add_command(label='EMA',
                          command=lambda: addMiddleIndicator('ema'))

        menubar.add_cascade(label='Main/Middle Indicator', menu=mainI)

        # Indicators Bottom
        bottomI = tk.Menu(menubar, tearoff=1)
        bottomI.add_command(label='None',
                            command=lambda: addBottomIndicator('none'))
        bottomI.add_command(label='RSI',
                            command=lambda: addBottomIndicator('rsi'))
        bottomI.add_command(label='MACD',
                            command=lambda: addBottomIndicator('macd'))

        menubar.add_cascade(label='Bottom Indicator', menu=bottomI)

        tk.Tk.config(self, menu=menubar)

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
ani = animation.FuncAnimation(f, animate, interval=5000)
app.mainloop()
