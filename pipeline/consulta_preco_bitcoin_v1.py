import requests

def extrair():
    url = "https://api.coinbase.com/v2/prices/spot"
    response = requests.get(url)
    return response.json()

def transformar(dados_json):
    valor = dados_json['data']['amount']
    criptomoeda = dados_json['data']['base']
    moeda = dados_json['data']['currency']
    
    dados_tratados = {
        "valor": valor,
        "criptomoeda": criptomoeda,
        "moeda": moeda
    }
    
    return dados_tratados

if __name__ == "__main__":
    dados_json = extrair()
    dados_tratados = transformar(dados_json)
    
    print(dados_tratados)
