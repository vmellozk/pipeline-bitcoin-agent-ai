import requests
from dotenv import load_dotenv
import os

load_dotenv()

nasa_api = os.getenv('NASA_API')

url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key={nasa_api}"

response = requests.get(url)

print(response.json())

