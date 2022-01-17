from numpy import NaN, nan
import yfinance as yf
import options as op
import pandas as pd
from maxpain import max_pain, get_current_price
from stocks_near_pain import *
from tinydb import TinyDB
from datetime import date



if __name__ == "__main__":
    symbols = read_csv_file("yfinance/maxpain.csv")
    today = date.today()

