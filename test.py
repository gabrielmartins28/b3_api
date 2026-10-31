import requests

def consultar_empresa():

    valor = input("Insira a tag da empresa que você quer consultar:")

    url = f"https://brapi.dev/api/quote/{valor}"
    response = requests.request("GET", url, headers = {
    "Authorization": "pr66QBYroQwx2FWuEGKGmM"
    })

    
    print(response.text)

consultar_empresa()