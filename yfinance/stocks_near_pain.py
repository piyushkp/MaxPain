from maxpain import *

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
                    print("{0}={1}   date={2}   MaxPain={3}   call_OI={4}   put_OI={5}".format(symbol, cp, date, mp, mp_COI, mp_POI))
                    mp_list.append((symbol, cp, date, mp, mp_COI, mp_POI))
                    if (oi >= 60 and oi <= 100) or (oi>= 100 and oi <= 160):
                        print("{0}={1}   date={2}   strangle={3}   call_OI={4}   put_OI={5}".format(symbol, cp, date, mp, mp_COI, mp_POI))
    return mp_list

if __name__ == "__main__":
    #symbols = get_stock_symbols()
    symbols = read_csv_file("yfinance/maxpain.csv")
    get_stocks_around_max_pain(date="2022-01-21", symbols=symbols)