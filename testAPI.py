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
# from app import models

def postTest(_message):
    API_URL_TEST = "http://127.0.0.1:8000/api_test/"
    # API_URL_TEST = "https://vendashg.pythonanywhere.com/api_test/"

    new_product = {
        "status": _message,
    }

    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE,
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL_TEST, json=new_product, headers=headers)

    if response.status_code == 201:
        print("Teste cadastrado com sucesso!")
    else:
        print("Erro ao cadastrar teste:", response.status_code)

def getTest():
    API_URL_TEST = "http://127.0.0.1:8000/api_test/"
    # API_URL_TEST = "https://vendashg.pythonanywhere.com/api_test/"

    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE,
        "Content-Type": "application/json"
    }

    response = requests.get(API_URL_TEST, headers=headers)

    if response.status_code == 200:
        tests = response.json()
        for test in tests:
            print(f"Teste: {test['status']}")
    else:
        print("Erro ao obter teste:", response.status_code)

def putTest(_id, _message):
    API_URL_TEST = "http://127.0.0.1:8000/api_test/" + str(_id) + "/"
    # API_URL_TEST = "https://vendashg.pythonanywhere.com/api_test/" + str(_id) + "/"

    update_teste = {
        "status": _message,
    }

    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE,
        "Content-Type": "application/json"
    }

    response = requests.patch(API_URL_TEST, json=update_teste, headers=headers)

    if response.status_code == 200:
        print("Teste cadastrado com sucesso!")
    else:
        print("Erro ao cadastrar teste:", response.status_code)

def getByIdTest(_id):
    # API_URL_TEST = "http://127.0.0.1:8000/api_test/" + str(_id) + "/"
    API_URL_TEST = "https://vendashg.pythonanywhere.com/api_test/" + str(_id) + "/"

    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE,
        "Content-Type": "application/json"
    }

    response = requests.get(API_URL_TEST, headers=headers)

    if response.status_code == 200:
        test = response.json()
        print(f"Teste: {test['status']}")
    else:
        print("Erro ao obter teste:", response.status_code)

def postPedidoOrder(_message): # Não ta funfando ainda
    API_URL_PEDIDO_ORDER = "http://127.0.0.1:8000/api_pedido_order/"
    # API_URL_PEDIDO_ORDER = "http://vendashg.pythonanywhere.com/api_pedido_order/"

    new_product = {
        "status": _message,
    }

    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE,
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
        # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE,
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
        # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE,
        "Content-Type": "application/json"
    }

    response = requests.get(API_URL_PEDIDO_ORDER, headers=headers)

    if response.status_code == 200:
        produto = response.json()
        print(f"Produto: {produto}")
    else:
        print("Erro ao obter produtos:", response.status_code)

def postProduto(_produtodata, _prodfiles): # Não ta funfando ainda
    API_URL_PEDIDO_ORDER = "http://127.0.0.1:8000/api_produtos/"
    # API_URL_PEDIDO_ORDER = "http://vendashg.pythonanywhere.com/api_produtos/"
    
    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE,
        # "Content-Type": "application/json"
    }

    response = requests.post(API_URL_PEDIDO_ORDER, data=_produtodata, files=_prodfiles, headers=headers)

    if response.status_code == 201:
        print("Produto cadastrado com sucesso!")
    else:
        print("Erro ao cadastrar produto:", response.status_code)
        print(response.text)

def getProduto():
    API_URL_PEDIDO_ORDER = "http://127.0.0.1:8000/api_produtos/"
    # API_URL_PEDIDO_ORDER = "http://vendashg.pythonanywhere.com/api_produtos/"

    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE,
        "Content-Type": "application/json"
    }

    response = requests.get(API_URL_PEDIDO_ORDER, headers=headers)

    if response.status_code == 200:
        produtos = response.json()
        for produto in produtos:
            print(f"Produto: {produto['codigo']}")
    else:
        print("Erro ao obter produtos:", response.status_code)

def getByCodigoProduto(_codigo):
    API_URL_PEDIDO_ORDER = "http://127.0.0.1:8000/api_produtos/" + str(_codigo) + "/"
    # API_URL_PEDIDO_ORDER = "https://vendashg.pythonanywhere.com/api_produtos/" + str(_id) + "/"

    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE,
        "Content-Type": "application/json"
    }

    response = requests.get(API_URL_PEDIDO_ORDER, headers=headers)

    if response.status_code == 200:
        produto = response.json()
        print(f"Produto: {produto}")
    else:
        print("Erro ao obter produto:", response.status_code)

postTest("Fala comigo bb") # A mensagem é printada na pagina /contato/
# getTest()
# getByIdTest(10)
# putTest(10, "Olá")
# getByIdTest(10)

# postPedidoOrder("cu") # Não usar, não ta direito
# getPedidoOrder()
# getByIdPedidoOrder(85)

# getProduto()
# getByCodigoProduto(143830)

prodData = {
    "codigo": "12456",
    "descricao": "Teste da API pra lançamento de produto",
    "codigo_GTIN": "12456",
    "preco_unitario_bruto": 69.69,
    "desconto_dinheiro": 7,
    "desconto_retira": 9,
    "fechamento_embalagem": 3.5,
    "slug": "12456",
    "Categoria": 4,
    "titulo": "Teste da API pra lançamento de produto",    
    "venda": 0,
}

prodFiles = {
    "image": open("E:/Users/HP/Pictures/pokemonTCGPocket/Bidoof.jpg", "rb"),
}

# postProduto(prodData, prodFiles)