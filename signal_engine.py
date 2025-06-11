
from datetime import datetime, timedelta
from indicators import calcular_indicadores
from ai_analysis import analisar_contexto
from data_sources.cryptocompare import get_crypto_price
from data_sources.twelvedata import get_forex_price
import pytz

fuso_brasilia = pytz.timezone("America/Sao_Paulo")
ativos = [
    "BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT", "ADA/USDT",
    "EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF", "AUD/USD"
]

def gerar_sinal():
    melhores = []
    for ativo in ativos:
        dados = get_crypto_price(ativo) if "USDT" in ativo else get_forex_price(ativo)
        if not dados:
            continue
        score, tipo = calcular_indicadores(dados)
        reforco = analisar_contexto(dados, ativo)
        final_score = (score + reforco) / 2
        if final_score >= 90:
            hora_entrada = datetime.now(fuso_brasilia) + timedelta(minutes=2)
            hora_saida = hora_entrada + timedelta(minutes=1)
            preco = dados[-1]["close"]
            return {
                "ativo": ativo,
                "tipo": tipo,
                "hora_entrada": hora_entrada.strftime("%Y-%m-%d %H:%M:%S"),
                "hora_saida": hora_saida.strftime("%Y-%m-%d %H:%M:%S"),
                "score": round(final_score, 2),
                "preco_entrada": preco
            }
    return None

def validar_resultado(sinais):
    agora = datetime.now(fuso_brasilia)
    for s in sinais:
        if "resultado" not in s:
            saida = fuso_brasilia.localize(datetime.strptime(s["hora_saida"], "%Y-%m-%d %H:%M:%S"))
            if agora >= saida:
                dados = get_crypto_price(s["ativo"]) if "USDT" in s["ativo"] else get_forex_price(s["ativo"])
                preco_saida = dados[-1]["close"]
                preco_entrada = s["preco_entrada"]
                if s["tipo"] == "COMPRA":
                    s["resultado"] = "WIN" if preco_saida > preco_entrada else "LOSS"
                else:
                    s["resultado"] = "WIN" if preco_saida < preco_entrada else "LOSS"
    return sinais
