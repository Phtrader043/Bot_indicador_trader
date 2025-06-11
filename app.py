
import streamlit as st
from signal_engine import gerar_sinal, validar_resultado
import json
import pandas as pd
from datetime import datetime
import pytz
import time

st.set_page_config(page_title="Indicador GPT 1.0", layout="wide")

st.title("📊 INDICADOR GPT 1.0")
fuso_brasilia = pytz.timezone("America/Sao_Paulo")

# Carregar histórico de sinais
def carregar_sinais():
    try:
        with open("signals.json", "r") as f:
            return json.load(f)
    except:
        return []

def salvar_sinais(sinais):
    with open("signals.json", "w") as f:
        json.dump(sinais, f, indent=2)

sinais = carregar_sinais()

# Botão de geração manual
if st.button("🔁 Gerar SINAL"):
    sinal = gerar_sinal()
    if sinal:
        sinais.append(sinal)
        salvar_sinais(sinais)
        st.success(f"SINAL GERADO: {sinal['ativo']} - {sinal['tipo']} às {sinal['hora_entrada']} 🎯")
    else:
        st.warning("Nenhum sinal forte encontrado (score < 90%)")

# Validação automática
sinais_validados = validar_resultado(sinais)
salvar_sinais(sinais_validados)

# Exibição
st.subheader("📍 Sinal Atual")
if sinais:
    ultimo = sinais[-1]
    st.markdown(f"""
    **Ativo:** {ultimo['ativo']}  
    **Tipo:** {ultimo['tipo']}  
    **Hora Entrada:** {ultimo['hora_entrada']}  
    **Hora Saída:** {ultimo['hora_saida']}  
    **Score:** {ultimo['score']}  
    **Resultado:** {ultimo.get('resultado', '⏳ Aguardando')}  
    """)
else:
    st.info("Nenhum sinal gerado ainda.")

# Histórico
st.subheader("📈 Histórico de Sinais")
df = pd.DataFrame(sinais)
if not df.empty:
    df['hora_entrada'] = pd.to_datetime(df['hora_entrada'])
    df = df.sort_values(by="hora_entrada", ascending=False)
    st.dataframe(df[["ativo", "tipo", "hora_entrada", "hora_saida", "score", "resultado"]])
    acertos = df["resultado"].value_counts().to_dict()
    total = len(df)
    win = acertos.get("WIN", 0)
    percentual = (win / total) * 100 if total else 0
    st.metric("🎯 Taxa de Acerto", f"{percentual:.2f}%")
else:
    st.info("Nenhum dado para exibir ainda.")
