import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("token_api")

def consultar_empresa():

    valor = input("Insira a tag da empresa que você quer consultar:")

    url = f"https://brapi.dev/api/quote/{valor}"
    response = requests.request("GET", url, headers = {
    "Authorization": token})


    print(response.text)

consultar_empresa()