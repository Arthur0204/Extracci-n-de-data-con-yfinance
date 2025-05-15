#ETL_general
import yfinance as yf
import pandas as pd

def ETL(Ticker,start,end):

    ticker = yf.Ticker(Ticker) #el ticker GAAAAAAAAAA

    # Obtener precios ajustados (sin 'Adj Close', ni dividendos/splits en el df principal)
    df = ticker.history(start=start, end=end, auto_adjust=False)

    # Obtener dividendos y splits por separado (Series con fecha como índice)
    dividends = ticker.dividends.loc[start:end]
    splits = ticker.splits.loc[start:end]

    # Unir los dividendos y splits como columnas al DataFrame principal
    df["Dividends"] = dividends
    df["Stock Splits"] = splits

    df[["Dividends", "Stock Splits"]] = df[["Dividends", "Stock Splits"]].fillna(0) #rellenar los nulos o vacíos con 0 para evitar errores
    df = df.reset_index().rename(columns={"index": "Fecha"})

    return df