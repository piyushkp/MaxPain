from maxpain import *
import sys
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def get_stocks_in_max_pain(date, symbols):
    mp_list = []
    for symbol in symbols:
        mp, mp_COI, mp_POI, credit, debit = max_pain(date, symbol)
        if mp is not None:
            cp = get_current_price(symbol)
            per = percentage(cp, mp)
            if (per >= 95 and per <= 105):
                print("{0}={1}   date={2}   MaxPain={3}   call_OI={4}   put_OI={5}  credit={6} debit={7}".format(symbol, cp, date, mp, mp_COI, mp_POI, credit, debit))
                mp_list.append((symbol, cp, date, mp, mp_COI, mp_POI))

    return mp_list

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 2 and args[0] == '-date':
        #symbols = get_stock_symbols()
        symbols = read_csv_file("yfinance/maxpain.csv")
        get_stocks_in_max_pain(date=args[1], symbols=symbols)