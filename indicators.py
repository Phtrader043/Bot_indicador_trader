
import numpy as np
import pandas as pd

def calcular_indicadores(dados):
    df = pd.DataFrame(dados)
    df["EMA9"] = df["close"].ewm(span=9).mean()
    df["RSI"] = 100 - (100 / (1 + df["close"].pct_change().rolling(14).mean()))
    df["MACD"] = df["close"].ewm(12).mean() - df["close"].ewm(26).mean()
    score = 0
    if df["close"].iloc[-1] > df["EMA9"].iloc[-1]:
        score += 30
    if df["RSI"].iloc[-1] < 30 or df["RSI"].iloc[-1] > 70:
        score += 30
    if df["MACD"].iloc[-1] > 0:
        score += 30
    tipo = "COMPRA" if df["MACD"].iloc[-1] > 0 else "VENDA"
    return score, tipo
