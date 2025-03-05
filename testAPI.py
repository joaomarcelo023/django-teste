# ListCreateAPIView:
#                               GET     Get a list of objects
#                               POST    Create a new object
# RetrieveUpdateDestroyAPIView:
#                               GET     Get a single object
#                               PUT	    Replaces an object
#                               PATCH	Update an object
#                               DELETE	Delete an object
import requests
import json
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

def postJson(_arq):
    API_URL_PRODUTOS = "http://127.0.0.1:8000/chunked_json_upload/"
    # API_URL_PRODUTOS = "https://vendashg.pythonanywhere.com/chunked_json_upload/"

    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE,
        "Content-Type": "application/json"
    }

    large_json = open(_arq, "r").read()

    # large_json = {"data": ["item1", "item2", "item3", "..."]}  # Example JSON
    json_str = json.dumps(large_json)
    chunk_size = 1024 * 1024  # 1MB chunks
    file_id = "json123"

    total_chunks = len(json_str) // chunk_size + 1

    for i in range(total_chunks):
        chunk = json_str[i * chunk_size: (i + 1) * chunk_size]
        data = {
            "file_id": file_id,
            "chunk_index": i,
            "total_chunks": total_chunks,
            "chunk_data": chunk,
        }
        response = requests.post(API_URL_PRODUTOS, headers=headers, json=data)
        
        print(f"Chunk {i+1}/{total_chunks}: {response.json()}")
    
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# postTest("Fala comigo bb") # A mensagem é printada na pagina /contato/
# getTest()
# getByIdTest(10)
# putTest(10, "Olá")
# getByIdTest(10)

# postPedidoOrder("cu") # Não usar, não ta direito
# getPedidoOrder()
# getByIdPedidoOrder(85)

# getProduto()
# getByCodigoProduto(143830)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# prodData = {
#     "codigo": "234567",
#     "descricao": "Teste 2 da API pra lançamento de produto",
#     "codigo_GTIN": "234567",
#     "preco_unitario_bruto": 420,
#     "desconto_dinheiro": 5,
#     "desconto_retira": 5,
#     "unidade": "CM3",
#     "fechamento_embalagem": 1,
#     "em_estoque": True,
#     "slug": "234567",
#     "Categoria": 4,
#     "titulo": "Teste 2 da API pra lançamento de produto",    
#     "venda": 0,
# }

# prodFiles = {
#     "image": open("E:/Users/HP/Pictures/pokemonTCGPocket/Croagunk.jpg", "rb"),
# }

# postProduto(prodData, prodFiles)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

postJson("C:/djvenv/ProjetoJoaoMarcelo/estoque/estoque_ATACADAO.json")