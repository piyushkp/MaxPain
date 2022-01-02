import yfinance as yf
import options as op
import pandas as pd

def max_pain(date="2022-01-07", symbol="MSFT"):
    data = op.options_chain_by_date(symbol, date)
    maxpain = pd.DataFrame()  
    for value in list(get_strike_prices(data)): 
        price = value
        putcash = callcash = 0.0
        for index, row in data.iterrows():
            strike = row['strike']
            if strike > price and row["CALL"] == False:
                oi = row['openInterest']
                putcash += (strike - price) * oi * 100
            if strike < price and row["CALL"] == True:
                oi = row['openInterest']
                callcash += (price - strike) * oi * 100
        maxpain = maxpain.append({"price" : price, "putcash" : putcash, "callcash": callcash, "total" : putcash + callcash}, ignore_index = True)

    return maxpain.sort_values(by="total").iloc[0]["price"]
        
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
    print(max_pain(date="2022-01-21", symbol="MSFT"))



