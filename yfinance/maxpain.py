from numpy import NaN, nan
import yfinance as yf
import options as op
import pandas as pd
import logging
import math
from pandas_datareader import data
import os
from yahoo_fin import stock_info as si
logging.getLogger("urllib3").setLevel(logging.WARNING)
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def max_pain(date, symbol):
    try:
        data = op.options_chain_by_date(symbol, date)
        maxpain = pd.DataFrame()  
        for value in list(get_strike_prices(data)): 
            price = value
            putcash = callcash = credit = 0.0
            for index, row in data.iterrows():
                strike = row['strike']
                if strike > price:
                    if row["CALL"] == False:
                        oi = row['openInterest']
                        if pd.isna(oi) is False:
                            putcash += (strike - price) * oi * 100
                    else:
                        if pd.isna(row['openInterest']) is False:
                            credit += (strike - price) * row['openInterest'] * 100
                elif strike < price:
                    if row["CALL"] == True:
                        oi = row['openInterest']
                        if pd.isna(oi) is False:
                            callcash += (price - strike) * oi * 100
                    else:
                        if pd.isna(row['openInterest']) is False:
                            credit += (price - strike) * row['openInterest'] * 100
                else:
                    if pd.isna(row['openInterest']) is False:
                            credit += row['openInterest'] * 100 * ((row['bid'] + row['ask'])/2)

            maxpain = maxpain.append({"price" : price, "putcash" : putcash, "callcash": callcash, "debit" : putcash + callcash, "credit" : credit}, ignore_index = True)

        mp = maxpain.sort_values(by="debit").iloc[0]["price"]
        mp_POI = None
        mp_COI = None
        for index, row in data.iterrows():
            strike = row['strike']
            if strike == mp:
                if row["CALL"] == False:
                    mp_POI = row['openInterest']
                else:
                    mp_COI = row['openInterest']

        debit = millify(maxpain.sort_values(by="debit").iloc[0]["debit"])
        credit = millify(maxpain.sort_values(by="debit").iloc[0]["credit"])
        #print("{0}={1}   {2}   MaxPain: {3}".format(symbol, cp, date, mp))
        return mp, mp_COI, mp_POI, credit, debit
    except BaseException as err:
        #print("exception: {0}.".format(err))
        return None, None, None, None, None


def get_strike_prices(data):
    strikes = set()
    for value in data.get("strike"): 
        strikes.add(value)
    return sorted(strikes)


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
    return sav_set

def percentage(part, whole):
    if whole < 1 :
        return 0
    percentage = 100 * float(part)/float(whole)
    return percentage

millnames = ['',' Thousand',' Million',' Billion',' Trillion']

def millify(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

def read_csv_file(csvfile):
    tickers = []
    data = pd.read_csv(csvfile)
    return data


def get_current_price(symbol):
    stock = yf.Ticker(symbol)
    price = stock.info['regularMarketPrice']   
    return price
