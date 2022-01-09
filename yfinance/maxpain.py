from numpy import NaN, nan
import yfinance as yf
import options as op
import pandas as pd


def max_pain(date="2022-01-07", symbol="MSFT"):
    try:
        data = op.options_chain_by_date(symbol, date)
        maxpain = pd.DataFrame()  
        for value in list(get_strike_prices(data)): 
            price = value
            putcash = callcash = 0.0
            for index, row in data.iterrows():
                strike = row['strike']
                if strike > price and row["CALL"] == False:
                    oi = row['openInterest']
                    if pd.isna(oi) is False:
                        putcash += (strike - price) * oi * 100
                if strike < price and row["CALL"] == True:
                    oi = row['openInterest']
                    if pd.isna(oi) is False:
                        callcash += (price - strike) * oi * 100
            maxpain = maxpain.append({"price" : price, "putcash" : putcash, "callcash": callcash, "total" : putcash + callcash}, ignore_index = True)

        mp = maxpain.sort_values(by="total").iloc[0]["price"]
        cp = get_current_price(symbol)

        for index, row in data.iterrows():
            strike = row['strike']
            if strike == mp:
                if row["CALL"] == False:
                    mp_POI = row['openInterest']
                else:
                    mp_COI = row['openInterest']

        #print(maxpain.sort_values(by="total"))
        #print("{0}={1}   {2}   MaxPain: {3}".format(symbol, cp, date, mp))
        return mp, mp_COI, mp_POI
    except:
        return None, None, None

def get_index_maxpain():
    for symbol in ["^ndx", "^spx", "QQQ", "^RUT"]:
        tk = yf.Ticker(symbol)
        exps = tk.options
        cp = get_current_price(symbol)
        for index, tuple in enumerate(exps):
            mp, mp_COI, mp_POI = max_pain(date=exps[index], symbol=symbol)
            print("{0}={1}   {2}   MaxPain: {3} call_OI: {4}  put_OI: {5}".format(symbol, cp, exps[index], mp, mp_COI, mp_POI))

def get_strike_prices(data):
    strikes = set()
    for value in data.get("strike"): 
        strikes.add(value)
    return sorted(strikes)

def get_current_price(symbol):
    stock = yf.Ticker(symbol)
    price = stock.info['regularMarketPrice']   
    return price 

if __name__ == "__main__":
    #print(max_pain(date="2022-01-21", symbol="UBER"))
    get_index_maxpain()
