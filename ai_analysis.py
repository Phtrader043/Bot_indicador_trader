import cohere

COHERE_API_KEY = "0zIapnzQSu4BXmPPkFbL4A0E4HZG9wM6IotodQOn"
client = cohere.Client(COHERE_API_KEY)

def analisar_contexto(dados, ativo):
    prompt = f"""
Você é um analista de mercado financeiro. Avalie se o seguinte contexto indica um momento POSITIVO ou NEGATIVO para entrar em uma operação de COMPRA no ativo {ativo}.
Contexto: {dados}
Responda apenas com: POSITIVO ou NEGATIVO
    """.strip()

    response = client.generate(
        model="command",
        prompt=prompt,
        max_tokens=5,
        temperature=0.3,
        stop_sequences=["\n"]
    )

    texto_resposta = response.generations[0].text.strip().upper()

    if "POSITIVO" in texto_resposta:
        return "positivo"
    elif "NEGATIVO" in texto_resposta:
        return "negativo"
    else:
        return "neutro"
