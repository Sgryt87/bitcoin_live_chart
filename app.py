# https://wex.nz/
# https://wex.nz/api/3/trades/btc_usd?limit=2000

import matplotlib

matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg, NavigationToolbar2Tk
# from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

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
f = plt.figure()
# a = f.add_subplot(111)  # 1x1 / 121 - #1x2 charts

exchange = 'BTC-e'
DatCounter = 9000
programName = 'btce'
resampleSize = '15Min'
DataPace = 'tick'

candleWidth = 0.008
paneCount = 1
chartLoad = True

# indicators
topIndicator = 'none'
middleIndicator = 'none'
bottomIndicator = 'none'

LIGHT_COLOR = '#00a3e0'
DARK_COLOR = '#183a54'

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


# Load Chart
def loadChart(run):
    global chartLoad
    if run == 'start':
        chartLoad = True
    elif run == 'stop':
        chartLoad = False


# HELP
def tutorial():
    # def leavemini(what):
    #     what.destroy()

    def page2():
        tut.destroy()
        tut2 = tk.Tk()

        def page3():
            tut2.destroy()
            tut3 = tk.Tk()

            tut3.wm_title('Part 3')

            label = ttk.Label(tut3, text='Part 3', font=NORM_FONT)
            label.pack(side='top', fill='x', pady=10)
            b = ttk.Button(tut3, text='Done!', command=tut3.destroy)
            b.pack()
            tut3.mainloop()

        tut2.wm_title('Part 2')

        label = ttk.Label(tut2, text='Part 2', font=NORM_FONT)
        label.pack(side='top', fill='x', pady=10)
        b = ttk.Button(tut2, text='Done!', command=tut2.destroy)
        b.pack()
        tut2.mainloop()

    tut = tk.Tk()
    tut.wm_title('Tutorial')
    label = ttk.Label(tut, text='What do you to help with?', font=NORM_FONT)
    label.pack(side='top', fill='x', pady=10)

    b1 = ttk.Button(tut, text='Overview of the application', command=page2)
    b1.pack()

    b2 = ttk.Button(tut, text='How do I trade with this client?'
                    , command=lambda: popupmsg('Not completed yet....'))
    b2.pack()

    b3 = ttk.Button(tut, text='Indicator Question Help'
                    , command=lambda: popupmsg('Not completed yet....'))
    b3.pack()

    tut.mainloop()


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
    global refreshRate
    global DatCounter

    if chartLoad:
        if paneCount == 1:
            if DataPace == 'tick':
                try:
                    if exchange == 'BTC-e':
                        a = plt.subplot2grid((6, 4), (0, 0), rowspan=5, colspan=4)
                        a2 = plt.subplot2grid((6, 4), (5, 0), rowspan=1, colspan=4, sharex=a)  # sharex align zooms

                        dataLink = 'https://wex.nz/api/3/trades/btc_usd?limit=2000'
                        data = urllib.request.urlopen(dataLink)
                        data = data.read().decode('utf-8')
                        data = json.loads(data)

                        data = data['btc_usd']
                        data = pd.DataFrame(data)

                        data['datestamp'] = np.array(data['timestamp']).astype('datetime64[s]')
                        allDates = data['datestamp'].tolist()

                        buys = data[(data['type'] == 'bid')]
                        # buys['datestamp'] = np.array(buys['timestamp']).astype('datetime64[ms]')
                        buyDates = (buys['datestamp']).tolist()

                        sells = data[(data['type'] == 'ask')]
                        # sells['datestamp'] = np.array(sells['timestamp']).astype('datetime64[ms]')
                        sellDates = (sells['datestamp']).tolist()

                        # volume
                        volume = data['amount'].apply(float).tolist()

                        a.clear()

                        a.plot_date(buyDates, buys['price'], LIGHT_COLOR, label='buys')
                        a.plot_date(sellDates, sells['price'], DARK_COLOR, label='sells')

                        a2.fill_between(allDates, 0, volume, facecolor=DARK_COLOR)

                        a.xaxis.set_major_locator(mticker.MaxNLocator(5))
                        a.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
                        plt.setp(a.get_xticklabels(), visible=False)

                        a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3, ncol=2, borderaxespad=0)

                        title = 'BTC-e BTCUSD Prices\nLast Price: ' + str(data['price'][1999])
                        a.set_title(title)

                    if exchange == 'Bitfinex':
                        a = plt.subplot2grid((6, 4), (0, 0), rowspan=5, colspan=4)
                        a2 = plt.subplot2grid((6, 4), (5, 0), rowspan=1, colspan=4, sharex=a)  # sharex align zooms

                        dataLink = 'https://api.bitfinex.com/v1/trades/btcusd?limit=2000'
                        data = urllib.request.urlopen(dataLink)
                        data = data.read().decode('utf-8')
                        data = json.loads(data)

                        data = pd.DataFrame(data)

                        data['datestamp'] = np.array(data['timestamp']).astype('datetime64[s]')
                        allDates = data['datestamp'].tolist()

                        buys = data[(data['type'] == 'buy')]
                        # buys['datestamp'] = np.array(buys['timestamp']).astype('datetime64[ms]')
                        buyDates = (buys['datestamp']).tolist()

                        sells = data[(data['type'] == 'sell')]
                        # sells['datestamp'] = np.array(sells['timestamp']).astype('datetime64[ms]')
                        sellDates = (sells['datestamp']).tolist()

                        # volume
                        volume = data['amount'].apply(float).tolist()

                        a.clear()

                        a.plot_date(buyDates, buys['price'], LIGHT_COLOR, label='buys')
                        a.plot_date(sellDates, sells['price'], DARK_COLOR, label='sells')

                        a2.fill_between(allDates, 0, volume, facecolor=DARK_COLOR)

                        a.xaxis.set_major_locator(mticker.MaxNLocator(5))
                        a.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
                        plt.setp(a.get_xticklabels(), visible=False)

                        a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3, ncol=2, borderaxespad=0)

                        title = 'Bitfinex BTCUSD Prices\nLast Price: ' + str(data['price'][0])
                        a.set_title(title)

                    if exchange == 'Bitstamp':
                        a = plt.subplot2grid((6, 4), (0, 0), rowspan=5, colspan=4)
                        a2 = plt.subplot2grid((6, 4), (5, 0), rowspan=1, colspan=4, sharex=a)  # sharex align zooms

                        dataLink = 'https://www.bitstamp.net/api/transactions/'
                        data = urllib.request.urlopen(dataLink)
                        data = data.read().decode('utf-8')
                        data = json.loads(data)

                        data = pd.DataFrame(data)

                        data['datestamp'] = np.array(data['date'].apply(int)).astype('datetime64[s]')
                        dateStamps = data['datestamp'].tolist()

                        # volume
                        volume = data['amount'].apply(float).tolist()

                        a.clear()

                        a.plot_date(dateStamps, data['price'], LIGHT_COLOR, label='buys')

                        a2.fill_between(dateStamps, 0, volume, facecolor=DARK_COLOR)

                        a.xaxis.set_major_locator(mticker.MaxNLocator(5))
                        a.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
                        plt.setp(a.get_xticklabels(), visible=False)

                        a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3, ncol=2, borderaxespad=0)

                        title = 'Bitstamp BTCUSD Prices\nLast Price: ' + str(data['price'][0])
                        a.set_title(title)

                    if exchange == 'Huobi':
                        a = plt.subplot2grid((6, 4), (0, 0), rowspan=6, colspan=4)
                        # TODO: work on a URL parsing
                        data = urllib.request.urlopen('https://api.huobi.pro/market/depth?symbol=ethbtc&type=step1')
                        data = data.read().decode()
                        data = json.loads(data)

                        dateStamp = np.array(data[0]).astype('datetime64[s')
                        dateStamp = dateStamps.tolist()

                        df = pd.DataFrame({'Datetime': dateStamp})
                        df['price'] = data[1]
                        df['Volume'] = data[2]
                        df['Symbol'] = 'BTCUSD'

                        df['MPLDate'] = df['Datetime'].apply(lambda date: mdates.date2num(date.to_pydatetime()))

                        df = df.set_index('Datetime')

                        lastPrice = df['Price'][-1]

                        a.plot_date(df['MPLDate'][-4500:], df['Price'][-4500:], LIGHT_COLOR, label='price')

                        a.xaxis.set_major_locator(mticker.MaxNLocator(5))
                        a.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
                        plt.setp(a.get_xticklabels(), visible=False)

                        title = 'Huobi BTCUSD Prices\nLast Price: ' + str(lastPrice)
                        a.set_title(title)
                        # print(dateStamps[:5])

                except Exception as e:
                    print('Failed: ', e)


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

        # Trading buttons
        tradeButton = tk.Menu(menubar, tearoff=1)
        tradeButton.add_command(label='Manual Trading',
                                command=lambda: popupmsg('Not Live yet.....'))
        tradeButton.add_command(label='Automated Trading',
                                command=lambda: popupmsg('Not Live yet.....'))
        tradeButton.add_separator()
        tradeButton.add_command(label='Quick Buy',
                                command=lambda: popupmsg('Not Live yet.....'))
        tradeButton.add_command(label='Quick Sell',
                                command=lambda: popupmsg('Not Live yet.....'))
        tradeButton.add_separator()
        tradeButton.add_command(label='Set up Quck Buy/Sell',
                                command=lambda: popupmsg('Not Live yet.....'))
        menubar.add_cascade(label='Trading', menu=tradeButton)

        # start/pause chart
        startStop = tk.Menu(menubar, tearoff=1)
        startStop.add_command(label='Resume',
                              command=lambda: loadChart('start'))
        startStop.add_command(label='Pause',
                              command=lambda: loadChart('stop'))
        menubar.add_cascade(label='Resume/Pause client', menu=startStop)

        # help meny
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label='Tutorial', command=tutorial)

        menubar.add_cascade(label='Help', menu=helpmenu)
        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        for F in (StartPage, PageOne, BTCe_Page):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0,
                       sticky='nsew')  # sticky='nsew' - north/south/east/west - aligning for the whole window

        self.show_frame(StartPage)

        tk.Tk.iconbitmap(self, 'default.ico')

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
