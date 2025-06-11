import json
import pytz
from datetime import datetime, timedelta
from indicators import calcular_indicadores
from ai_analysis import analisar_contexto
from data_sources.cryptocompare import obter_dados_cripto
from data_sources.twelvedata import obter_dados_forex
from utils import salvar_sinal, validar_resultado, ativos_cripto, pares_forex

fuso_brasilia = pytz.timezone("America/Sao_Paulo")

def gerar_sinal():
    agora = datetime.now(pytz.utc).astimezone(fuso_brasilia)
    melhor_sinal = None
    maior_score = 0

    for ativo in ativos_cripto + pares_forex:
        dados = obter_dados_cripto(ativo) if ativo in ativos_cripto else obter_dados_forex(ativo)
        indicadores = calcular_indicadores(dados)

        score = indicadores["score"]
        direcao = indicadores["direcao"]

        # Reforço IA
        reforco = analisar_contexto(dados, ativo)

        if reforco == "positivo":
            reforco_score = 100
        elif reforco == "neutro":
            reforco_score = 50
        else:
            reforco_score = 0

        final_score = (score + reforco_score) / 2

        if final_score >= 90 and final_score > maior_score:
            melhor_sinal = {
                "ativo": ativo,
                "tipo": "COMPRA" if direcao == "alta" else "VENDA",
                "hora_entrada": (agora + timedelta(minutes=2)).strftime("%H:%M:%S"),
                "hora_saida": (agora + timedelta(minutes=3)).strftime("%H:%M:%S"),
                "probabilidade": round(final_score, 2),
                "preco_entrada": dados[-1]["close"],
                "resultado": "Aguardando"
            }
            maior_score = final_score

    if melhor_sinal:
        salvar_sinal(melhor_sinal)
        return melhor_sinal

    return None


def verificar_resultados():
    try:
        with open("signals.json", "r") as f:
            sinais = json.load(f)
    except FileNotFoundError:
        sinais = []

    agora = datetime.now(pytz.utc).astimezone(fuso_brasilia).strftime("%H:%M:%S")

    for sinal in sinais:
        if sinal["resultado"] == "Aguardando" and sinal["hora_saida"] <= agora:
            resultado = validar_resultado(sinal)
            sinal["resultado"] = resultado

    with open("signals.json", "w") as f:
        json.dump(sinais, f, indent=4)
        
