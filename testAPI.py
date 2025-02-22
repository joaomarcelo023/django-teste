# ListCreateAPIView:
#                               GET     Get a list of objects
#                               POST    Create a new object
# RetrieveUpdateDestroyAPIView:
#                               GET     Get a single object
#                               PUT	    Replaces an object
#                               PATCH	Update an object
#                               DELETE	Delete an object
import requests
from django_teste import settings

def postTest(_message):
    # API_URL_TEST = "http://127.0.0.1:8000/api-produtos/"
    API_URL_TEST = "https://vendashg.pythonanywhere.com/api-produtos/"

    new_product = {
        "status": _message,
    }

    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE, # settings.TESTKEY_API_CASAHG,
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL_TEST, json=new_product, headers=headers)

    if response.status_code == 201:
        print("Produto cadastrado com sucesso!")
    else:
        print("Erro ao cadastrar produto:", response.status_code)

def getTest():
    # API_URL_TEST = "http://127.0.0.1:8000/api-produtos/"
    API_URL_TEST = "https://vendashg.pythonanywhere.com/api-produtos/"

    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE, # settings.TESTKEY_API_CASAHG,
        "Content-Type": "application/json"
    }

    response = requests.get(API_URL_TEST, headers=headers)

    if response.status_code == 200:
        produtos = response.json()
        for produto in produtos:
            print(f"Produto: {produto['status']}")
    else:
        print("Erro ao obter produtos:", response.status_code)

def putTest(_id, _message):
    API_URL_TEST = "http://127.0.0.1:8000/api-produtos/" + str(_id) + "/"
    # API_URL_TEST = "https://vendashg.pythonanywhere.com/api-produtos/" + str(_id) + "/"

    update_product = {
        "status": _message,
    }

    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        "Content-Type": "application/json"
    }

    response = requests.patch(API_URL_TEST, json=update_product, headers=headers)

    if response.status_code == 200:
        print("Produto cadastrado com sucesso!")
    else:
        print("Erro ao cadastrar produto:", response.status_code)

def getByIdTest(_id):
    API_URL_TEST = "http://127.0.0.1:8000/api-produtos/" + str(_id) + "/"
    # API_URL_TEST = "https://vendashg.pythonanywhere.com/api-produtos/" + str(_id) + "/"

    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        "Content-Type": "application/json"
    }

    response = requests.get(API_URL_TEST, headers=headers)

    if response.status_code == 200:
        produto = response.json()
        print(f"Produto: {produto['status']}")
    else:
        print("Erro ao obter produtos:", response.status_code)

def postPedidoOrder(_message):
    API_URL_PEDIDO_ORDER = "http://127.0.0.1:8000/api_pedido_order/"
    # API_URL_PEDIDO_ORDER = "http://vendashg.pythonanywhere.com/api_pedido_order/"

    new_product = {
        "status": _message,
    }

    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL_PEDIDO_ORDER, json=new_product, headers=headers)

    if response.status_code == 201:
        print("Produto cadastrado com sucesso!")
    else:
        print("Erro ao cadastrar produto:", response.status_code)

def getPedidoOrder():
    API_URL_PEDIDO_ORDER = "http://127.0.0.1:8000/api_pedido_order/"
    # API_URL_PEDIDO_ORDER = "http://vendashg.pythonanywhere.com/api_pedido_order/"

    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        "Content-Type": "application/json"
    }

    response = requests.get(API_URL_PEDIDO_ORDER, headers=headers)

    if response.status_code == 200:
        produtos = response.json()
        for produto in produtos:
            print(f"Produto: {produto['id']}")
    else:
        print("Erro ao obter produtos:", response.status_code)
        
def getByIdPedidoOrder(_id):
    API_URL_PEDIDO_ORDER = "http://127.0.0.1:8000/api_pedido_order/" + str(_id) + "/"
    # API_URL_PEDIDO_ORDER = "https://vendashg.pythonanywhere.com/api_pedido_order/" + str(_id) + "/"

    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        "Content-Type": "application/json"
    }

    response = requests.get(API_URL_PEDIDO_ORDER, headers=headers)

    if response.status_code == 200:
        produto = response.json()
        print(f"Produto: {produto}")
    else:
        print("Erro ao obter produtos:", response.status_code)


postTest("Fala comigo bb") # A mensagem é printada na pagina /contato/
# getTest()
# getByIdTest(10)
# putTest(10, "Olá")
# getByIdTest(10)

# postPedidoOrder("cu") # Não usar, não ta direito
# getPedidoOrder()
# getByIdPedidoOrder(85)