from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User
from rest_framework_api_key.models import AbstractAPIKey
import os

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nome = models.CharField(max_length=200,default="")
    sobrenome = models.CharField(max_length=200,default="")

    cpf_ou_cnpj = models.CharField(max_length=14,default="")
    cpf_ou_cnpj_formatado = models.CharField(max_length=20, default="")
    bool_cpf_cnpj = models.BooleanField(default=False)

    email = models.EmailField(default="")
    telefone = models.CharField(max_length=19,default="")

    data_criacao = models.DateTimeField(auto_now_add=True)

    verificado = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.telefone[0:3] != "+55":
            if self.telefone[-1] == "_":
                ddd = f"{self.telefone[1:3]}"
                telefoneNumero = f"{self.telefone[5:10]}{self.telefone[11:-1]}"
                self.telefone = f"+55 ({ddd}) {telefoneNumero[:4]}-{telefoneNumero[4:]}"
            elif self.telefone[-1].isdigit():
                self.telefone = f"+55 {self.telefone}"

        # Formatar CPF ou CNPJ
        cpf_cnpj = self.cpf_ou_cnpj
        if len(cpf_cnpj) == 11:  # CPF
            self.cpf_ou_cnpj_formatado = f"{cpf_cnpj[:3]}.{cpf_cnpj[3:6]}.{cpf_cnpj[6:9]}-{cpf_cnpj[9:]}"
            self.bool_cpf_cnpj = True
        elif len(cpf_cnpj) == 14:  # CNPJ
            self.cpf_ou_cnpj_formatado = f"{cpf_cnpj[:2]}.{cpf_cnpj[2:5]}.{cpf_cnpj[5:8]}/{cpf_cnpj[8:12]}-{cpf_cnpj[12:]}"
            self.bool_cpf_cnpj = False
        else:
            self.cpf_ou_cnpj_formatado = cpf_cnpj  # Caso não atenda os formatos esperados

        super(Cliente, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"

class Endereco(models.Model):
    cliente = models.ForeignKey(Cliente,on_delete=models.SET_NULL,null=True,blank=True)
    titulo = models.CharField(max_length=40,null=True,blank=True)
    cep = models.CharField(max_length=9,null=True,blank=True)
    estado = models.CharField(max_length=3,null=True,blank=True)
    cidade = models.CharField(max_length=35,null=True,blank=True)
    bairro = models.CharField(max_length=35,null=True,blank=True)
    rua = models.CharField(max_length=35,null=True,blank=True)
    numero = models.CharField(max_length=20,null=True,blank=True)
    complemento = models.CharField(max_length=140,null=True,blank=True)

    def __str__(self):
        return self.titulo + " | " + self.cliente.nome + " " + self.cliente.sobrenome

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #

class Categoria(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return str(self.id) + "- " + self.titulo

ACABAMENTO_SUPERFICIAL_PISOS=[
    ("Polido", "Polido"),
    ("Brilho", "Brilho"),
    ("Acetinado", "Acetinado"),
    ("Granilha", "Granilha"),
    ("Antiderrapante", "Antiderrapante"),
]

CLASSE_TECNICA_ABSORCAO_PISOS=[
    ("0,0 a 0,5","Porcelanato"),
    ("0,5 a 3,0", "Grês"),
    ("3,0 a 6,0", "Semi Grês"),
    ("6,0 a 10,0", "Bllb"),
    (">10", "Monoporosa"),
]

VARIACAO_FACES_PISOS=[
    ("Peças uniformes, onde a variação entre uma peça e outra não é perceptível", "V1"),
    ("Leve variação, existem diferenças perceptíveis entre as peças, mas as texturas e tons apresentados são muito próximos", "V2"),
    ("Variação moderada, algumas peças são diferentes umas das outras", "V3"),
    ("Alta variação, as peças tem uma diferença bem significativa entre elas", "V4"),
]

INDICACAO_DE_USO_PISOS=[
    ("Sem tráfego - Indicado para uso em paredes", "LA"),
    ("Pouco tráfego - Indicado para uso interno, sem acesso a áreas externas, em residências", "LB"),
    ("Médio tráfego - Indicado para todas as dependências residenciais e comerciais de médio tráfego", "LC"),
    ("Alto tráfego - Indicado para todas as dependências residenciais e comerciais de alto tráfego", "LD"),
]

def estoque_loja():
    return {"Casa HG - Várzea": 0, "Casa HG - Magé/Guapimirim": 0, "Casa HG - Atacadão Dos Pisos": 0}

class Produto(models.Model):
    #informações que virão do sistema externo
    codigo = models.CharField(max_length=10) #codigo interno consistente com sistema
    titulo = models.CharField(max_length=200,default="",null=True,blank=True)
    descricao = models.CharField(max_length=200)
    codigo_GTIN = models.CharField(max_length=14) #se o produto não tiver codigo GTIN cadastrado, usar codigo interno
    preco_unitario_bruto = models.DecimalField(max_digits=10,decimal_places=2) #preço cheio, sem desconto
    desconto_dinheiro = models.DecimalField(max_digits=10,decimal_places=2) # em %, percentual de desconto para pagamento em dinheiro, aplicado no preco_unitario_bruto
    desconto_retira = models.DecimalField(max_digits=10,decimal_places=2)  # em %, percentual de desconto para compras para retirada no depósito, aplicado no preco_unitario_bruto
    unidade = models.CharField(max_length=30,default="un") #unidade em que o produto é comercializado
    fechamento_embalagem = models.DecimalField(max_digits=10,decimal_places=2,default=1.00)
    em_estoque = models.BooleanField(default=False)
    # estoque_lojas = models.ManyToManyField(Endereco, related_name='estoqueLojas', blank=True)
    estoque_lojas = models.JSONField(default=estoque_loja)

    marca = models.CharField(max_length=20,null=True,blank=True)
    formato = models.CharField(max_length=15,null=True,blank=True)
    espessura = models.SmallIntegerField(null=True,blank=True)
    junta_minima = models.SmallIntegerField(null=True,blank=True)
    relevo = models.BooleanField(null=True,blank=True)
    acabamento_superficial = models.CharField(max_length=50,choices=ACABAMENTO_SUPERFICIAL_PISOS,null=True,blank=True)
    variacao_faces = models.CharField(max_length=121,choices=VARIACAO_FACES_PISOS,null=True,blank=True)
    classe_tecnica_absorcao_pisos = models.CharField(max_length=50,choices=CLASSE_TECNICA_ABSORCAO_PISOS,null=True,blank=True)
    indicacao_uso = models.CharField(max_length=100,choices=INDICACAO_DE_USO_PISOS,null=True,blank=True)
    pecas_caixa = models.SmallIntegerField(null=True,blank=True)
    peso_bruto_caixa = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    palet = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)

    #informações que precisam ser criadas por lógica do sistema externo
    slug = models.SlugField(unique=True)
    Categoria = models.ForeignKey(Categoria,on_delete=models.SET_NULL,default="",null=True)
    image = models.ImageField(upload_to="produtos",null=True,blank=True)

    # TODO-ALVAREZ deletar de forma responsável
    venda = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    garantia = models.CharField(max_length=300,null=True,blank=True)
    return_devolucao = models.CharField(max_length=300,null=True,blank=True)

    #informações que virão do sistema da loja online
    visualizacao = models.PositiveIntegerField(default=0)
    quantidade_vendas = models.PositiveIntegerField(default=0)
    num_fotos = models.SmallIntegerField(default=1,null=True,blank=True)

    
    def save(self, *args, **kwargs):
        if not self.titulo:
            self.titulo = self.descricao

        if not self.image:
            self.image.name = "produtos/NoImgAvailable.webp"

        t = 0
        for estoque_loja in self.estoque_lojas.values():
            t += estoque_loja
            if t > 0:
                self.em_estoque = True
            else:
                self.em_estoque = False

        super(Produto, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"

def user_upload_path(instance, filename):
    return f"produtos/{instance.produto.codigo}/{filename}"

class FotosProduto(models.Model):
    produto = models.ForeignKey(Produto,related_name="images",on_delete=models.CASCADE,default="")
    image = models.ImageField(upload_to=user_upload_path, unique=True)
    img_num = models.SmallIntegerField(null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.img_num:
            self.produto.num_fotos += 1
            self.produto.save()

            if self.produto.num_fotos == 2:
                self.produto.image.name = self.image.name
                self.produto.save()

            self.img_num = self.produto.num_fotos
        else:
            if self.img_num == 2:
                self.produto.image.name = self.image.name
                self.produto.save()

        return super(FotosProduto, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.produto.num_fotos -= 1
        self.produto.save()

        if self.produto.num_fotos == 1:
            new_path = f"/produtos/{self.produto.codigo}.webp"
            if not os.path.exists("media/" + new_path):
                new_path = "/produtos/NoImgAvailable.webp"

            self.produto.image.name = new_path
            self.produto.save()

        self.image.delete(save=False)

        for fp in FotosProduto.objects.filter(produto=self.produto):
            if fp.img_num > self.img_num:
                fp.img_num -= 1

                fp.save()

        super(FotosProduto, self).delete(*args, **kwargs)

    def __str__(self):
        return f"{self.produto.codigo} - {self.produto.titulo}: {self.img_num}"

class LogPesquisa(models.Model):
    pesquisa = models.CharField(max_length=50,default="")
    ocorrido_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ocorrido_em} - {self.pesquisa}"

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #

class Carro(models.Model):
    cliente = models.ForeignKey(Cliente,on_delete=models.SET_NULL,null=True,blank=True)
    total = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Carro: " + str(self.id)

class CarroProduto(models.Model):
    carro = models.ForeignKey(Carro,on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto,on_delete=models.SET_NULL,default="",null=True)
    preco_unitario = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    quantidade = models.PositiveIntegerField()
    subtotal_bruto = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Carro: " + str(self.carro.id) + " | CarroProduto: " + str(self.id)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #

PEDIDO_STATUS=[
    ("Pedido em Andamento", "Pedido em Andamento"),
    ("Pedido Recebido", "Pedido Recebido"),
    ("Pagamento Pendente", "Pagamento Pendente"),
    ("Pagamento Processando", "Pagamento Processando"),
    ("Pagamento Confirmado", "Pagamento Confirmado"),
    ("Pedido Processando", "Pedido Processando"),
    ("Pedido Caminho", "Pedido Caminho"),
    ("Pedido Pronta Retirada", "Pedido Pronta Retirada"),
    ("Pedido Completado", "Pedido Completo"),
    ("Pedido Cancelado", "Pedido Cancelado"),
]

class PedidoOrder(models.Model):
    cliente = models.ForeignKey(Cliente,on_delete=models.SET_NULL,default="",null=True)
    nome_cliente = models.CharField(max_length=200,default="")
    cpf_cnpj = models.CharField(max_length=20, default="") # cpf do cliente formatadinho direitinho
    codigo_cliente = models.CharField(max_length=8,default="",null=True,blank=True) # codigo consistente com sistema interno, se não tiver
    telefone = models.CharField(max_length=19,default="")
    email = models.EmailField(default="")

    carro = models.ForeignKey(Carro,on_delete=models.CASCADE)
    pedido_status = models.CharField(max_length=50, choices=PEDIDO_STATUS)

    total_bruto = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    frete = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    desconto_retirada = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    desconto_forma_pagamento = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    total_desconto = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    total_final = models.DecimalField(max_digits=10,decimal_places=2,default=0)

    local_de_pagamento = models.CharField(max_length=200,default="",null=True,blank=True)
    forma_de_pagamento = models.CharField(max_length=200,default="",null=True,blank=True)
    parcelas = models.PositiveIntegerField(default=1)
    valor_parcela = models.DecimalField(max_digits=10,decimal_places=2,default=0)

    endereco_envio = models.ForeignKey(Endereco,on_delete=models.SET_NULL,default="",null=True)
    endereco_envio_formatado = models.CharField(max_length=200,default="")

    criado_em = models.DateTimeField(auto_now_add=True)

    id_PagBank = models.CharField(max_length=200,default="",null=True,blank=True)
    order_PagBank = models.CharField(max_length=200,default="",null=True,blank=True)

    def __str__(self):
        return "Pedido: " + str(self.id) + " | Status: " + self.pedido_status + " | Cliente: " + self.nome_cliente

class PedidoProduto(models.Model):
    #importante repetir informações do produto para que uma mudança de cadastro não altere a venda
    pedido = models.ForeignKey(PedidoOrder,on_delete=models.CASCADE,related_name="pedidoProduto",default="")
    produto = models.ForeignKey(Produto,on_delete=models.SET_NULL,default="",null=True)
    nome_produto = models.CharField(max_length=200,default="")

    codigo = models.CharField(max_length=10,default="")
    descricao = models.CharField(max_length=200,default="")
    codigo_GTIN = models.CharField(max_length=14,default="")
    preco_unitario_bruto = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    desconto_dinheiro = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    desconto_retira = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    unidade = models.CharField(max_length=30, default="un")

    quantidade = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    total_bruto = models.DecimalField(max_digits=10,decimal_places=2,default=0) #total parcial sem desconto
    desconto_total = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True,default=0) # em reais
    desconto_unitario = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True,default=0) # em reais
    total_final = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True,default=0) # total parcial com desconto

    def save(self, *args, **kwargs):
        if not self.nome_produto:
            self.nome_produto = self.produto.titulo

        super(PedidoProduto, self).save(*args, **kwargs)

    def __str__(self):
        return "Pedido: " + str(self.pedido.id) + " | Codigo do produto: " + self.codigo + " | Produto: " + self.nome_produto

class PedidoErro(models.Model):
    cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE,default="",null=True)
    carro = models.ForeignKey(Carro,on_delete=models.CASCADE)

    ocorrido_em = models.DateTimeField(auto_now_add=True)

    erro_code = models.CharField(max_length=10,null=True,blank=True)
    erro_message = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return f"Carro: {self.carro} | Cliente: {self.cliente} | erro: {self.erro_code}"

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #

class Banner(models.Model):
    title = models.CharField(max_length=100, blank=True)

    image_grande = models.ImageField(upload_to='banners')
    image_pequena = models.ImageField(upload_to='banners')

    link = models.CharField(max_length=200, blank=True)

    active = models.BooleanField(default=True)

    position = models.PositiveSmallIntegerField(default=0,null=True,blank=True)

    def save(self, *args, **kwargs):
        if self.active:
            if self.position == 0:
                topBanner = Banner.objects.filter(active=True).aggregate(Max('position'))
                maxValue = topBanner['position__max']

                self.position = maxValue + 1
        else:
            self.position = 0

        return super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.image_grande.delete(save=False)
        self.image_pequena.delete(save=False)

        return super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.title} | Posição: {self.position}"
    
class Empresa(models.Model):
    titulo = models.CharField(max_length=200)
    link = models.CharField(max_length=200,null=True,blank=True)
    image = models.ImageField(upload_to="empresas")

    def __str__(self):
        return self.titulo

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=200,default="",null=True,blank=True)
    image = models.ImageField(upload_to="admin",null=True,blank=True)
    email = models.EmailField(default="",null=True,blank=True)
    telefone = models.CharField(max_length=19,default="",null=True,blank=True)

    def save(self, *args, **kwargs):
        self.nome_completo = self.user.get_full_name()
        self.email = self.user.email

        super(Admin, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

class AdminLog(models.Model):
    funcionario = models.ForeignKey(Admin,on_delete=models.SET_NULL,null=True)
    log = models.CharField(max_length=200)
    ocorrido_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ocorrido_em.strftime('%d/%m/%y %H:%M')} UTC | {self.funcionario} | {self.log}"

class APIKey(AbstractAPIKey):
    criado_em = models.DateTimeField(auto_now_add=True)
    obj = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="api_keys")

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #

class TestStatus(models.Model):
    status = models.CharField(max_length=2000,default="",null=True,blank=True)
    cu = models.CharField(max_length=2000,default="",null=True,blank=True)

    def __str__(self):
        return str(self.id) + ": " + self.status + ", " + self.cu