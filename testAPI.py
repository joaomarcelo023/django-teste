import requests
from django_teste import settings

def post(_site, _message):
    new_product = {
        "status": _message,
    }

    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        "Content-Type": "application/json"
    }

    response = requests.post(_site, json=new_product, headers=headers)

    if response.status_code == 201:
        print("Produto cadastrado com sucesso!")
    else:
        print("Erro ao cadastrar produto:", response.status_code)

def get(_site):
    response = requests.get(_site)

    if response.status_code == 200:
        produtos = response.json()
        for produto in produtos:
            print(f"Produto: {produto['status']}")
    else:
        print("Erro ao obter produtos:", response.status_code)


API_URL = "http://127.0.0.1:8000/api-produtos/"
# API_URL = "https://vendashg.pythonanywhere.com/api-produtos/"

post(API_URL, "cu") # A mensagem é printada na pagina /contato
# get(API_URL)