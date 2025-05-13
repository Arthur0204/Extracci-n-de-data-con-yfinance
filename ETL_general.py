#ETL_general
import yfinance as yf
import pandas as pd

def ETL(Ticker,start,end):

    df = yf.download(Ticker, start=start, end=end)
    df.columns = df.columns.droplevel(1) # eliminamos el segundo nivel (el que tiene el nombre de las acciones)
    
    return df

