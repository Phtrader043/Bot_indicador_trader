import cohere

COHERE_API_KEY = "0zIapnzQSu4BXmPPkFbL4A0E4HZG9wM6IotodQOn"
client = cohere.Client(COHERE_API_KEY)

def analisar_contexto(dados, ativo):
    texto = f"Analisando o ativo {ativo}. {dados}"

    response = client.classify(
        inputs=[texto],
        examples=[
            {"text": "mercado em alta", "label": "positivo"},
            {"text": "subida de preço", "label": "positivo"},
            {"text": "compra forte", "label": "positivo"},
            {"text": "mercado em baixa", "label": "negativo"},
            {"text": "queda de preço", "label": "negativo"},
            {"text": "venda forte", "label": "negativo"}
        ]
    )

    return response.classifications[0].prediction