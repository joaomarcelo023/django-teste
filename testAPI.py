import requests
from django_teste import settings

def postTest(_site, _message):
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

def getTest(_site):
    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        "Content-Type": "application/json"
    }

    response = requests.get(_site, headers=headers)

    if response.status_code == 200:
        produtos = response.json()
        for produto in produtos:
            print(f"Produto: {produto['status']}")
    else:
        print("Erro ao obter produtos:", response.status_code)

def postPedidoOrder(_site, _message):
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

def getPedidoOrder(_site):
    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        "Content-Type": "application/json"
    }

    response = requests.get(_site, headers=headers)

    if response.status_code == 200:
        produtos = response.json()
        for produto in produtos:
            print(f"Produto: {produto['id']}")
    else:
        print("Erro ao obter produtos:", response.status_code)


API_URL_TEST = "http://127.0.0.1:8000/api-produtos/"
# API_URL_TEST = "https://vendashg.pythonanywhere.com/api-produtos/"

API_URL_PEDIDO_ORDER = "http://127.0.0.1:8000/api_pedido_order/"
# API_URL_PEDIDO_ORDER = "http://vendashg.pythonanywhere.com/api_pedido_order/"

# postTest(API_URL_TEST, "cu") # A mensagem é printada na pagina /contato
# getTest(API_URL_TEST)

# postPedidoOrder(API_URL_PEDIDO_ORDER, "cu")
getPedidoOrder(API_URL_PEDIDO_ORDER)