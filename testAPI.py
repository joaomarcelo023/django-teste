# ListCreateAPIView:
#                               GET     Get a list of objects
#                               POST    Create a new object
# RetrieveUpdateDestroyAPIView:
#                               GET     Get a single object
#                               PUT	    Replaces an object
#                               PATCH	Update an object
#                               DELETE	Delete an object
# Error codes:
#                               https://www.django-rest-framework.org/api-guide/status-codes/
import os
import requests
import json
from django_teste import settings
import pandas as pd

def postTest(_message):
    # API_URL_TEST = "http://127.0.0.1:8000/api_test/"
    API_URL_TEST = "https://vendashg.pythonanywhere.com/api_test/"

    new_product = {
        "status": _message,
    }

    headers = {
        # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE,
        # "Content-Type": "application/json"
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

def patchTest(_id, _message):
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

def postProduto(_produtodata, _prodfiles):
    API_URL_PRODUTO = "http://127.0.0.1:8000/api_produtos/"
    # API_URL_PRODUTO = "http://vendashg.pythonanywhere.com/api_produtos/"

    API_URL_CATEGORIA = f"http://127.0.0.1:8000/api_categorias/{_produtodata['Categoria']}/"
    # API_URL_CATEGORIA = f"http://vendashg.pythonanywhere.com/api_categorias/{}/"
    
    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE,
        #"Content-Type": "application/json"
    }

    titulo_categoria = requests.get(API_URL_CATEGORIA, headers=headers)

    _produtodata["Categoria"] = titulo_categoria.json()["id"]

    response = requests.post(API_URL_PRODUTO, data=_produtodata, files=_prodfiles, headers=headers)

    if response.status_code == 201:
        print("Produto cadastrado com sucesso!")
    else:
        print("Erro ao cadastrar produto:", response.status_code)

def getProduto():
    API_URL_PRODUTO = "http://127.0.0.1:8000/api_produtos/"
    # API_URL_PRODUTO = "http://vendashg.pythonanywhere.com/api_produtos/"

    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE,
        "Content-Type": "application/json"
    }

    response = requests.get(API_URL_PRODUTO, headers=headers)

    if response.status_code == 200:
        produtos = response.json()
        for produto in produtos:
            print(f"Produto: {produto['codigo']}")
    else:
        print("Erro ao obter produtos:", response.status_code)

def getByCodigoProduto(_codigo):
    API_URL_PRODUTO = "http://127.0.0.1:8000/api_produtos/" + str(_codigo) + "/"
    # API_URL_PRODUTO = "https://vendashg.pythonanywhere.com/api_produtos/" + str(_id) + "/"

    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE,
        "Content-Type": "application/json"
    }

    response = requests.get(API_URL_PRODUTO, headers=headers)

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

def patchJson(_arq):
    API_URL_PRODUTOS = "http://127.0.0.1:8000/chunked_json_update/"
    # API_URL_PRODUTOS = "https://vendashg.pythonanywhere.com/chunked_json_update/"

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

def upload_image(_image_path):
    API_URL_IMG = "http://127.0.0.1:8000/chunked_img_upload/"
    # API_URL_IMG = "https://vendashg.pythonanywhere.com/chunked_img_upload/"

    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE,
        # "Content-Type": "application/json"
    }

    chunk_size = 1024 * 1024  # 1MB chunks

    file_name = os.path.basename(_image_path)
    total_size = os.path.getsize(_image_path)
    total_chunks = (total_size // chunk_size) + 1

    with open(_image_path, "rb") as f:
        for chunk_index in range(total_chunks):
            chunk = f.read(chunk_size)
            files = {"file": (file_name, chunk)}
            data = {
                "file_name": file_name,
                "chunk_index": chunk_index,
                "total_chunks": total_chunks
            }
            response = requests.post(API_URL_IMG, headers=headers, files=files, data=data)
            print(response.json())

def postImg(_imgDir, _imgDic, _imgList):
    # Escolhe o metodo que melhor servir pra tu
    # Se quiser testar um sem apagar os outros ou comentar só passar None como valor pros argumentos não usados
    if _imgDir:
        # Ex: _imgDir = "C:/Users/panel/OneDrive/Imagens"
        for image in os.listdir(_imgDir):
            image_path = os.path.join(_imgDir, image)
            if os.path.isfile(image_path):
                upload_image(image_path)

    if _imgDic:
        # Ex: {"0": "C:/Users/panel/OneDrive/Imagens/goku.jpg", "1": "C:/Users/panel/OneDrive/Imagens/vegeta.jpg"}
        for i in range(len(_imgDic)):
            image_path = _imgDic[str(i)]
            if os.path.isfile(image_path):
                upload_image(image_path)

    if _imgList:
        # Ex: _imgList = ["C:/Users/panel/OneDrive/Imagens/goku.jpg", "C:/Users/panel/OneDrive/Imagens/vegeta.jpg"]
        for image_path in _imgList:
            if os.path.isfile(image_path):
                upload_image(image_path)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# postTest("Fala mano") # A mensagem é printada na pagina /contato/
# getTest()
# getByIdTest(10)
# patchTest(10, "fala")
# getByIdTest(10)

# postPedidoOrder("cu") # Não usar, não ta direito
# getPedidoOrder()
# getByIdPedidoOrder(85)

# getProduto()
# getByCodigoProduto(143830)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Categorias:
#               3 -> Pisos Cerâmicos
#               4 -> Porcelanatos
#               5 -> Argamassas

# prodData = {
#     "codigo": "SeiLa5",
#     "descricao": "SeiLa5",
#     "codigo_GTIN": "SeiLa5",
#     "preco_unitario_bruto": 420.69,
#     "desconto_dinheiro": 5,
#     "desconto_retira": 5,
#     "unidade": "CM3",
#    "fechamento_embalagem": 1,
#     "em_estoque": True,
#     "slug": "SeiLa5",
#     "Categoria": "Porcelanatos",
# }

#prodFiles = {
#     "image": open("C:/Users/panel/OneDrive/Imagens/goku.jpg", "rb"),
# }

# postProduto(prodData, prodFiles)

# postProduto(prodData, None)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# postJson("C:/djvenv/ProjetoJoaoMarcelo/estoque/test.json")
patchJson("C:/djvenv/ProjetoJoaoMarcelo/estoque/test_update.json")
# postImg("E:/Users/HP/Pictures/pokemonTCGPocket")

# imgDic = {
#     "0": "C:/djvenv/ProjetoJoaoMarcelo/img/testDicList/Pagamento_Confirmado.png",
#     "1": "C:/djvenv/ProjetoJoaoMarcelo/img/testDicList/Pedido_Caminho.png"
# }

# imgList = ["C:/djvenv/ProjetoJoaoMarcelo/img/testDicList/Pedido_Cancelado.png", "C:/djvenv/ProjetoJoaoMarcelo/img/testDicList/Pedido_Recebido.png"]

# postImg("C:/djvenv/ProjetoJoaoMarcelo/img/testDir", imgDic, imgList)