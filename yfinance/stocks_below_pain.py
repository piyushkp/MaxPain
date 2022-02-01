from maxpain import *
import logging
logging.getLogger("urllib3").setLevel(logging.WARNING)
import sys
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def get_stocks_below_max_pain(date, symbols):
    mp_list = []
    for symbol in symbols:
        mp, mp_COI, mp_POI, total = max_pain(date, symbol)
        if None not in  (mp, mp_COI, mp_POI ):
            if mp_COI + mp_POI > 5000:
                cp = get_current_price(symbol)
                per = percentage(cp, mp)
                if (per >= 80 and per <= 100):
                    print("{0}={1}   date={2}   MaxPain={3}   call_OI={4}   put_OI={5} $={6}".format(symbol, cp, date, mp, mp_COI, mp_POI, total))
                    mp_list.append((symbol, cp, date, mp, mp_COI, mp_POI))
    return mp_list

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 2 and args[0] == '-date':
        #symbols = get_stock_symbols()
        symbols = read_csv_file("yfinance/maxpain.csv")
        print(symbols)
        get_stocks_below_max_pain(date=args[1], symbols=symbols)