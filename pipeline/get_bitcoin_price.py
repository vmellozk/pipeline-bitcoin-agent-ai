import requests

url = "https://api.coinbase.com/v2/prices/spot"

response = requests.get(url)

print(response.json())

