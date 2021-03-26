from yahooquery import Ticker
import pandas as pd
import pandas_ta as ta
import datetime as dt

#Global Var
NoVal = "-"


def candle_dict(open , high , low , close):
    return {"open" : open , "high" : high , "low" : low , "close" : close}

def dateRange(period , datelist = [] , add = False ,current = None ):
    if period is None:
        return None
    if add is True:
        range = pd.bdate_range(periods = period, freq = "C" ,holidays = datelist, end = current  , weekmask = "Mon Tue Wed Thu Fri" )
    else:
        end = dt.date.today().strftime("%Y-%m-%d")
        range = pd.bdate_range(periods = period, freq = "C" ,holidays = datelist, end = end  , weekmask = "Mon Tue Wed Thu Fri" )
    return range.date

def hist_price(symbol , start = None , end = None , interval = '1d'):
    if end is None and start is None:
        raise ValueError('Requires at value for start or end')
    if start is None:
        raise ValueError('Requires value for start')
    stockyq = Ticker(symbol)
    price = stockyq.history(interval = interval , start = start , end = end)
    #price.to_excel("price.xlsx")
    return price

#SMA50 > SMA150 and EMA20 > EMA40 and close > SMA50 Within 4 bars and low < SMA50 within 4 bars
def dip50(priceHist , sma50 , sma150 , ema20 , ema40):
    last4 = False
    for i in range(1 , 5):
        if priceHist['close'][len(priceHist) - i] > sma50[len(sma50) - i] and priceHist['low'][len(priceHist) - i] < sma50[len(sma50) - i]:
            last4 = True
        else:
            last4 = False

    if sma50[len(sma50) - 1] > sma150[len(sma150) - 1] and ema20[len(ema20) - 1] > ema40[len(ema40) - 1] and last4 == True:
        return True
    else:
        return False

def dip100(priceHist , sma50 , sma150 , sma100 , ema20 , ema40):
    last4 = False
    for i in range(1 , 5):
        if priceHist['close'][len(priceHist) - i] > sma100[len(sma100) - i] and priceHist['low'][len(priceHist) - i] < sma100[len(sma100) - i]:
            last4 = True
        else:
            last4 = False

    if sma50[len(sma50) - 1] > sma150[len(sma150) - 1] and ema20[len(ema20) - 1] > ema40[len(ema40) - 1] and last4 == True:
        return True
    else:
        return False

def PinBar(current , sma , trend):
    bar = current['high'] - current['low']
    if trend == "uptrend" and current['low'] <= sma and (((current['open'] - current['low'])/bar >= (2/3) and current['open'] <= current['close']) or ((current['close'] - current['low'])/bar >= (2/3) and current['close'] <= current['open'])):
        return "bull"
    elif trend == "downtrend" and current['high'] >= sma and (((current['high'] - current['open'])/bar >= (2/3) and current['open'] >= current['close']) or ((current['high'] - current['close'])/bar >= (2/3) and current['close'] >= current['open'])):
        return "bear"
    else:
        return NoVal
        
def tweezers(current, prev , sma , trend):
    high = current['high'] if current['high'] >= prev['high'] else prev['high']
    low = current['low'] if current['low'] >= prev['low'] else prev['low']
    combine = candle_dict(prev['open'] , high , low , current['close'] )
    if current['open'] < current['close'] and prev['open'] > prev['close'] and current['close'] == prev['open']:
        bar = PinBar(combine , sma , trend)
        return 'twtop' if bar == "bull" else NoVal
    if current['open'] > current['close'] and prev['open'] < prev['close'] and current['open'] == prev['close']:
        bar = PinBar(combine , sma , trend)
        return 'twbot' if bar == "bear" else NoVal

    return NoVal

def oneSolCrow(current , prev , sma , trend):
    if prev['open'] > prev['close'] and current['open'] < current['close'] and current['open'] > prev['close'] and current['close'] > prev['close'] and trend == "uptrend" and prev['low'] <= sma and (current['high'] >= prev['high'] or current['low'] >= prev['low']):
        return "soldier"
    elif prev['open'] < prev['close'] and current['open'] > current['close'] and current['open'] < prev['close'] and current['close'] < prev['close'] and trend == "downtrend" and prev['high'] >= sma and (current['high'] <= prev['high'] or current['low'] <= prev['low']):
        return "crow"   
    else:
        return NoVal     

def morEveStar(current , prev1 , prev2 ,  sma , trend):
    if trend == "uptrend" and prev1['low'] <= sma:
        if prev2['open'] > prev2['close'] and current['open'] < current['close'] and abs(prev2['open'] - prev2['close']) > abs(prev1['open'] - prev1['close']) and abs(prev2['open'] - prev2['close']) > abs(current['open'] - current['close']) and abs(prev1['open'] - prev1['close']) < abs(current['open'] - current['close']):
            if (prev2['close'] > prev1['open'] or prev2['close'] > prev1['close']) and (current['open'] > prev1['open'] or current['open'] > prev1['close']) and current['close'] > ((abs(prev2['open'] - prev2['close'])/2) + prev2['close']):
                return "morningstar"    

    elif trend == "downtrend" and prev1['high'] >= sma:
        if prev2['open'] < prev2['close'] and current['open'] < current['close'] and abs(prev2['open'] - prev2['close']) > abs(prev1['open'] - prev1['close']) and abs(prev2['open'] - prev2['close']) > abs(current['open'] - current['close']) and abs(prev1['open'] - prev1['close']) < abs(current['open'] - current['close']):
            if (prev2['close'] < prev1['open'] or prev2['close'] < prev1['close']) and (current['open'] < prev1['open'] or current['open'] < prev1['close']) and current['close'] < ((abs(prev2['open'] - prev2['close'])/2) + prev2['close']):
                return "eveningstar"    

    return NoVal
def engulfing(current , prev , sma , trend):
    if trend == "uptrend":
        if current['close'] > current['open'] and prev['close'] < prev['open']:
            if current['low'] < prev['low'] and current['high'] > prev['high'] and current['open'] < prev['close'] and current['close'] > prev['open']:
                return "bullengulf"

    elif trend == "downtrend":
        if current['close'] < current['open'] and prev['close'] > prev['open']:
            if current['low'] < prev['low'] and current['high'] > prev['high'] and current['open'] > prev['close'] and current['close'] < prev['open']:
                return "bearengulf"

    return NoVal

def trend(sma50 , sma150):
    trend = []
    for i in range(1 , 6):
        if sma50[len(sma50) - i] > sma150[len(sma150) - i]:
            trend.append('uptrend')
        elif sma50[len(sma50) - i] < sma150[len(sma150) - i]:
            trend.append('downtrend')
    if trend.count("uptrend") > trend.count("downtrend"):
        return 'uptrend'
    elif trend.count("uptrend") < trend.count("downtrend"):
        return 'downtrend'
    else:
        if trend[-1] == 'uptrend':
            return 'uptrend'
        elif trend[-1] == 'downtrend':
            return 'downtrend'

def todf(symbols = None , range = 200):
    if symbols is None:
        raise ValueError("Require at least 1 Symbol")
    
    tick = hist_price(symbols , start = dateRange(range)[0])
    df = pd.DataFrame(columns = ["symbol" , "dip50" , "dip100" , "pinBar50" , "pinBar150" , "tweezers50" , "tweezers150" ,  "oneSolCrow50" , "oneSolCrow150" , "morEveStar50" , "morEveStar150" , "engulfing50" , "engulfing150" , "Trend"])
    for i in symbols:
        hist = tick.xs(i, level = 0)
        sma50 = ta.sma(hist['close'] , length = 50)
        sma100 = ta.sma(hist['close'] , length = 100)
        sma150 = ta.sma(hist['close'] , length = 150)
        ema20 = ta.ema(hist['close'] , length = 20)
        ema40 = ta.ema(hist['close'] , length = 40)
        trnd = trend(sma50 , sma150)
        prev2 = candle_dict(hist['open'][len(hist) - 2 - 1] , hist['high'][len(hist) - 2 - 1] , hist['low'][len(hist) - 2 - 1] , hist['close'][len(hist) - 2 - 1])
        prev1 = candle_dict(hist['open'][len(hist) - 1 - 1] , hist['high'][len(hist) - 1 - 1] , hist['low'][len(hist) - 1 - 1] , hist['close'][len(hist) - 1 - 1])
        current = candle_dict(hist['open'][len(hist) - 1] , hist['high'][len(hist) - 1] , hist['low'][len(hist) - 1] , hist['close'][len(hist) - 1])
        datadict = {
            "symbol": i,
            "dip50": dip50(hist , sma50 , sma150, ema20 , ema40),
            "dip100": dip100(hist , sma50 , sma150 , sma100 , ema20 , ema40),
            "pinBar50": PinBar(current , sma50[-1] , trnd),
            "pinBar150": PinBar(current , sma150[-1] , trnd),
            "tweezers50": tweezers(current, prev1 , sma50[-1] , trnd),
            "tweezers150": tweezers(current, prev1 , sma150[-1] , trnd),
            "oneSolCrow50": oneSolCrow(current , prev1 , sma50[-1] , trnd),
            "oneSolCrow150": oneSolCrow(current , prev1 , sma150[-1] , trnd),
            "morEveStar50": morEveStar(current , prev1 , prev2 ,  sma50[-1] , trnd),
            "morEveStar150": morEveStar(current , prev1 , prev2 ,  sma150[-1] , trnd),
            "engulfing50": engulfing(current , prev1 , sma50[-1] , trnd),
            "engulfing150": engulfing(current , prev1 , sma150[-1] , trnd),
            "Trend": trnd
        }
        df = df.append(datadict , ignore_index=True)
    df = df.set_index('symbol')
    return df


symbols = ['fb', 'aapl', 'amzn', 'nflx', 'goog']
print(todf(symbols))


# for i in range(1 , 200):
#     prev1 = candle_dict(tick['open'][len(tick) - i - 2] , tick['high'][len(tick) - i - 2] , tick['low'][len(tick) - i - 2] , tick['close'][len(tick) - i - 2])
#     prev = candle_dict(tick['open'][len(tick) - i - 1] , tick['high'][len(tick) - i - 1] , tick['low'][len(tick) - i - 1] , tick['close'][len(tick) - i - 1])
#     current = candle_dict(tick['open'][len(tick) - i] , tick['high'][len(tick) - i] , tick['low'][len(tick) - i] , tick['close'][len(tick) - i])
#     x = morEveStar(current , prev , prev1 , sma50[len(sma50) - i] ,  trend = trend(sma50 , sma150))
#     print(f"{tick.index[len(tick) - i][1]} - {x}")




