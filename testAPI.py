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
import base64
from django_teste import settings
import pandas as pd
import unicodedata
from PIL import Image

def postTest(_message):
    # API_URL_TEST = "http://127.0.0.1:8000/api_test/"
    API_URL_TEST = "https://www.loja-casahg.com.br/api_test/"

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
    # API_URL_TEST = "https://www.loja-casahg.com.br/api_test/"

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
    # API_URL_TEST = "https://www.loja-casahg.com.br/api_test/" + str(_id) + "/"

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
    API_URL_TEST = "https://www.loja-casahg.com.br/api_test/" + str(_id) + "/"

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
    # API_URL_PEDIDO_ORDER = "https://www.loja-casahg.com.br/api_pedido_order/"

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
    # API_URL_PEDIDO_ORDER = "http://127.0.0.1:8000/api_pedido_order/"
    API_URL_PEDIDO_ORDER = "https://www.loja-casahg.com.br/api_pedido_order/"

    headers = {
        # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        "Authorization": f"Api-Key {settings.TESTKEY_API_CASAHG_PYTHONANYWHERE}",
        "Content-Type": "application/json"
    }

    response = requests.get(API_URL_PEDIDO_ORDER, headers=headers)

    if response.status_code == 200:
        pedidos = response.json()
        for pedido in pedidos:
            print(f"Pedido: {pedido['id']}: {pedido['endereco_envio']}")
    else:
        print("Erro ao obter produtos:", response.status_code, response.text)
        
def getByIdPedidoOrder(_id):
    API_URL_PEDIDO_ORDER = "http://127.0.0.1:8000/api_pedido_order/" + str(_id) + "/"
    # API_URL_PEDIDO_ORDER = "https://www.loja-casahg.com.br/api_pedido_order/" + str(_id) + "/"

    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE,
        "Content-Type": "application/json"
    }

    response = requests.get(API_URL_PEDIDO_ORDER, headers=headers)

    if response.status_code == 200:
        pedido = response.json()
        print(f"Pedido: {pedido}")
    else:
        print("Erro ao obter produtos:", response.status_code)

def postProduto(_produtodata, _prodfiles):
    API_URL_PRODUTO = "http://127.0.0.1:8000/api_produtos/"
    # API_URL_PRODUTO = "https://www.loja-casahg.com.br/api_produtos/"

    cat_slug = unicodedata.normalize('NFKD', _produtodata['Categoria']).encode('ascii', 'ignore').decode('utf-8').lower().replace(" ", "_")
    API_URL_CATEGORIA = f"http://127.0.0.1:8000/api_categorias/{cat_slug}/"
    # API_URL_CATEGORIA = f"https://www.loja-casahg.com.br/api_categorias/{}/"
    
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
    # API_URL_PRODUTO = "http://127.0.0.1:8000/api_produtos/"
    API_URL_PRODUTO = "https://www.loja-casahg.com.br/api_produtos/"

    headers = {
        # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE,
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
    # API_URL_PRODUTO = "https://www.loja-casahg.com.br/api_produtos/" + str(_id) + "/"

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
    # API_URL_PRODUTOS = "https://www.loja-casahg.com.br/chunked_json_upload/"

    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE,
        "Content-Type": "application/json"
    }

    large_json = open(_arq, "r", encoding='utf-8').read()

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
    # API_URL_PRODUTOS = "https://www.loja-casahg.com.br/chunked_json_update/"

    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE,
        "Content-Type": "application/json"
    }

    large_json = open(_arq, "r", encoding='utf-8').read()

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

def pisosFichaTecJson(_arq):
    API_URL_PISOS = "http://127.0.0.1:8000/chunked_piso_ficha_tec_json_upload/"
    # API_URL_PISOS = "https://www.loja-casahg.com.br/chunked_piso_ficha_tec_json_upload/"

    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE,
        "Content-Type": "application/json"
    }

    large_json = open(_arq, "r", encoding='utf-8').read()

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
        response = requests.post(API_URL_PISOS, headers=headers, json=data)
        
        print(f"Chunk {i+1}/{total_chunks}: {response.json()}")

def estoquelojasJson(_arq):
    API_URL_ESTOQUE = "http://127.0.0.1:8000/chunked_estoque_json_upload/"
    # API_URL_ESTOQUE = "https://www.loja-casahg.com.br/chunked_estoque_json_upload/"

    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE,
        "Content-Type": "application/json"
    }

    large_json = open(_arq, "r", encoding='utf-8').read()

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
        response = requests.post(API_URL_ESTOQUE, headers=headers, json=data)
        
        print(f"Chunk {i+1}/{total_chunks}: {response.json()}")

def upload_image(_image_path):
    API_URL_IMG = "http://127.0.0.1:8000/chunked_img_upload/"
    # API_URL_IMG = "https://www.loja-casahg.com.br/chunked_img_upload/"

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

def getProdStats():
    API_URL_PRODUTOS = "http://127.0.0.1:8000/produto_stats/"
    # API_URL_PRODUTOS = "https://www.loja-casahg.com.br/produto_stats/"

    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE,
        "Content-Type": "application/json"
    }

    response = requests.get(API_URL_PRODUTOS, headers=headers)

    return response.json()

def postFotoExtra(_produtodata, _prodfiles):
    API_URL_PRODUTO = "http://127.0.0.1:8000/api_fotos_produtos_upload/"
    # API_URL_PRODUTO = "https://www.loja-casahg.com.br/api_fotos_produtos_upload/"
    
    headers = {
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE,
        #"Content-Type": "application/json"
    }

    response = requests.post(API_URL_PRODUTO, data=_produtodata, files=_prodfiles, headers=headers)

    if response.status_code >= 200 and response.status_code < 300:
        resp = response.json()
        print(f"{resp['message']}: foto {resp['file_url']}, produto {resp['Produto']}")
    else:
        print("Erro ao cadastrar produto:", response.status_code)

def manda_grupo_imagem(self):
    # Dados para a API
    # API_URL_PRODUTO = "http://127.0.0.1:8000/api_fotos_produtos/"
    API_URL_PRODUTO = "https://www.loja-casahg.com.br/api_fotos_produtos/"
    
    headers = {
        # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
        "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE,
        #"Content-Type": "application/json"
    }

    # Coleta e envio das imagens
    df = pd.read_json("dados/codigos_site_filtrados.json", encoding="latin-1")
    base = r"cria_ambientes"

    for codigo in df['codigo']:
        pasta_codigo = os.path.join(base, str(codigo))
        if os.path.isdir(pasta_codigo):
            for nome_arquivo in os.listdir(pasta_codigo):
                if nome_arquivo.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    caminho = os.path.join(pasta_codigo, nome_arquivo)

                    prodData = {"codigo": codigo}
                    prodFiles = {"image": open(caminho, "rb")}

                    response = requests.post(API_URL_PRODUTO, data=prodData, files=prodFiles, headers=headers)

                    if response.status_code == 201:
                        print("Foto enviada com sucesso!")
                    else:
                        print("Erro ao enviar foto:", response.status_code)
        else:
            print(f"Aviso: pasta não encontrada para código {codigo}")

def manda_grupo_imagem(self):
    API_URL_PRODUTO = "https://www.loja-casahg.com.br/api_fotos_produtos/"
    headers = {"Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE}

    df = pd.read_json("dados/codigos_site_filtrados.json", encoding="latin-1")
    base = r"../../cria_ambientes/revestimentos"

    for codigo in df['codigo']:
        pasta_codigo = os.path.join(base, str(codigo))

        if not os.path.isdir(pasta_codigo):
            print(f"Aviso: pasta não encontrada para código {codigo}")

            continue

        json_path = None
        for f in os.listdir(pasta_codigo):
            if f.lower().endswith('.json'):
                json_path = os.path.join(pasta_codigo, f)

                # Passei essa parte pra dentro desse if e tirei o envio pra api, ele já vai enviar no proximo for
                with open(json_path, 'r', encoding='utf-8') as jf:
                    j = json.load(jf)
                cor = j.get('cor', {}).get('0')
                altura = j.get('altura', {}).get('0')
                largura = j.get('largura', {}).get('0')

                if cor and altura and largura:
                    w, h = int(largura), int(altura)
                    rgb = tuple(cor)
                    img = Image.new('RGB', (w, h), rgb)

                    img_solid_path = os.path.join(pasta_codigo, f"{codigo}_solid.png")
                    img.save(img_solid_path)

                break

        ## Se rodar com as mudanças pode apagar essa parte
        # if json_path:
        #     with open(json_path, 'r', encoding='utf-8') as jf:
        #         j = json.load(jf)
        #     cor = j.get('cor', {}).get('0')
        #     altura = j.get('altura', {}).get('0')
        #     largura = j.get('largura', {}).get('0')

        #     if cor and altura and largura:
        #         w, h = int(largura), int(altura)
        #         rgb = tuple(cor)
        #         img = Image.new('RGB', (w, h), rgb)

        #         img_solid_path = os.path.join(pasta_codigo, f"{codigo}_solid.png")
        #         img.save(img_solid_path)

        #         with open(img_solid_path, 'rb') as f_im:
        #             data = {"codigo": codigo}
        #             files = {"image": f_im}
        #             response = requests.post(API_URL_PRODUTO, data=data, files=files, headers=headers)

        #         if response.status_code == 201:
        #             print(f"Foto sólida do código {codigo} enviada com sucesso!")
        #         else:
        #             print(f"Erro ao enviar foto sólida do código {codigo}:", response.status_code)

        #         continue

        for nome_arquivo in os.listdir(pasta_codigo):
            if nome_arquivo.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                caminho = os.path.join(pasta_codigo, nome_arquivo)
                with open(caminho, 'rb') as f_img:
                    data = {"codigo": codigo}
                    files = {"image": f_img}
                    response = requests.post(API_URL_PRODUTO, data=data, files=files, headers=headers)

                if response.status_code == 201:
                    print(f"Foto {nome_arquivo} do código {codigo} enviada com sucesso!")
                else:
                    print(f"Erro ao enviar foto {nome_arquivo} do código {codigo}:", response.status_code)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

# postTest("Fala ai") # A mensagem é printada na pagina /contato/
# getTest()
# getByIdTest(10)
# patchTest(10, "fala")
# getByIdTest(10)

# postPedidoOrder("cu") # Não usar, não ta direito
getPedidoOrder()
# getByIdPedidoOrder(115)

# getProduto()
# getByCodigoProduto(143830)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

# Categorias:
#               3 -> Pisos Cerâmicos
#               4 -> Porcelanatos
#               5 -> Argamassas

# prodData = {
#     "codigo": "Giratina",
#     "descricao": "Giratina",
#     "codigo_GTIN": "Giratina",
#     "preco_unitario_bruto": 69.69,
#     "desconto_dinheiro": 5,
#     "desconto_retira": 5,
#     "unidade": "CM3",
#    "fechamento_embalagem": 1,
#     "em_estoque": False,
#     "slug": "Giratina",
#     "Categoria": "Cerâmicas",
#     "indicação_uso": "LA",
# }

# prodFiles = {
#     "image": open("E:/Users/HP/Pictures/pokemonTCGPocket/Weezing.jpg", "rb"),
# }

# postProduto(prodData, prodFiles)

# postProduto(prodData, None)

# prodData = {
#     "codigo": "143830",
# }

# postFotoExtra(prodData, prodFiles)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

# postJson("C:/djvenv/ProjetoJoaoMarcelo/estoque/codigos_site_filtrados_2.json")
# patchJson("C:/djvenv/ProjetoJoaoMarcelo/estoque/codigos_site_filtrados_2.json")
# estoquelojasJson("C:/djvenv/ProjetoJoaoMarcelo/estoque/estoque_master_2.json")
# pisosFichaTecJson("C:/djvenv/ProjetoJoaoMarcelo/estoque/codigos_site_3.json")
# postImg("E:/Users/HP/Pictures/pokemonTCGPocket")

# imgDic = {
#     "0": "C:/djvenv/ProjetoJoaoMarcelo/img/testDicList/Pagamento_Confirmado.png",
#     "1": "C:/djvenv/ProjetoJoaoMarcelo/img/testDicList/Pedido_Caminho.png"
# }

# imgList = ["C:/djvenv/ProjetoJoaoMarcelo/img/testDicList/Pedido_Cancelado.png", "C:/djvenv/ProjetoJoaoMarcelo/img/testDicList/Pedido_Recebido.png"]

# postImg("C:/djvenv/ProjetoJoaoMarcelo/img/testDir", imgDic, imgList)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

# stats = getProdStats()
# print(stats['Vendas_json'])