import yfinance as yf
from maxpain import max_pain, get_current_price

def get_index_maxpain():
    for symbol in ["^ndx", "^spx", "QQQ", "^RUT"]:
        tk = yf.Ticker(symbol)
        exps = tk.options
        cp = get_current_price(symbol)
        for index, tuple in enumerate(exps):
            mp, mp_COI, mp_POI = max_pain(date=exps[index], symbol=symbol)
            print("{0}={1}   Date={2}   MaxPain={3}   call_OI={4}   put_OI={5}".format(symbol, cp, exps[index], mp, mp_COI, mp_POI))


if __name__ == "__main__":
    get_index_maxpain()