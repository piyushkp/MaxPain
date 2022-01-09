
from numpy import NaN, nan
import yfinance as yf
import csv
import os
import options as op
import pandas as pd
from pandas_datareader import data
from yahoo_fin import stock_info as si
from maxpain import max_pain, get_current_price
import logging
logging.getLogger("urllib3").setLevel(logging.WARNING)

def get_stocks_around_max_pain(date, symbols):
    mp_list = []
    for symbol in symbols:
        mp, mp_COI, mp_POI = max_pain(date, symbol)
        if mp is not None:
            if mp_COI + mp_POI > 10000:
                cp = get_current_price(symbol)
                per = percentage(cp, mp)
                oi = percentage(mp_COI, mp_POI)
                if (per >= 1 and per <= 20) or (per >= 100 and per <= 120):
                    print("{0}={1}   {2}   MaxPain: {3}  call_OI: {4}  put_OI: {5}".format(symbol, cp, date, mp, mp_COI, mp_POI))
                    mp_list.append((symbol, cp, date, mp, mp_COI, mp_POI))
                    if (oi >= 60 and oi <= 100) or (oi>= 100 and oi <= 160):
                        print("{0}={1}   {2}   strangle: {3}  call_OI: {4}  put_OI: {5}".format(symbol, cp, date, mp, mp_COI, mp_POI))
    return mp_list

def read_csv_file(csvfile):
    tickers = []
    data = pd.read_csv(csvfile)
    return data

def get_stock_symbols():
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    # gather stock symbols from major US exchanges
    df1 = pd.DataFrame( si.tickers_sp500() )
    df2 = pd.DataFrame( si.tickers_nasdaq() )
    df3 = pd.DataFrame( si.tickers_dow() )
    df4 = pd.DataFrame( si.tickers_other() )

    # convert DataFrame to list, then to sets
    sym1 = set( symbol for symbol in df1[0].values.tolist() )
    sym2 = set( symbol for symbol in df2[0].values.tolist() )
    sym3 = set( symbol for symbol in df3[0].values.tolist() )
    sym4 = set( symbol for symbol in df4[0].values.tolist() )

    # join the 4 sets into one. Because it's a set, there will be no duplicate symbols
    symbols = set.union( sym1, sym2, sym3, sym4 )

    # Some stocks are 5 characters. Those stocks with the suffixes listed below are not of interest.
    my_list = ['W', 'R', 'P', 'Q']
    del_set = set()
    sav_set = set()
    for symbol in symbols:
        if symbol != "":
            if len( symbol ) > 4 and symbol[-1] in my_list:
                del_set.add( symbol )
            else:
                try:
                    market_cap=int(data.get_quote_yahoo(symbol)['marketCap'])
                    price=int(data.get_quote_yahoo(symbol)['price'])
                    avdv=int(data.get_quote_yahoo(symbol)['averageDailyVolume3Month'])
                    # check if market cap is > 5b
                    if market_cap / 1000000 > 5000 and price > 20 and avdv > 500000:
                        sav_set.add(symbol)
                except:
                    continue
    print(sav_set)
    return sav_set

def percentage(part, whole):
    if whole < 1 :
        return 0
    percentage = 100 * float(part)/float(whole)
    return percentage

if __name__ == "__main__":
    #symbols = get_stock_symbols()
    symbols = read_csv_file("yfinance/maxpain.csv")
    get_stocks_around_max_pain(date="2022-01-21", symbols=symbols)