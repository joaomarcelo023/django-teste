from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.titulo

class Produto(models.Model):

    #informações que virão do sistema externo
    codigo = models.CharField(max_length=10) #codigo interno consistente com sistema
    descricao = models.CharField(max_length=200)
    codigo_GTIN = models.CharField(max_length=14) #se o produto não tiver codigo GTIN cadastrado, usar codigo interno
    preco_unitario_bruto = models.DecimalField(max_digits=10, decimal_places=2) #preço cheio, sem desconto
    desconto_dinheiro = models.DecimalField(max_digits=10, decimal_places=2) # em %, percentual de desconto para pagamento em dinheiro, aplicado no preco_unitario_bruto
    desconto_retira = models.DecimalField(max_digits=10,decimal_places=2)  # em %, percentual de desconto para compras para retirada no depósito, aplicado no preco_unitario_bruto
    unidade = models.CharField(max_length=30,default="un") #unidade em que o produto é comercializado
    fechamento_embalagem = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)

    #informações que precisam ser criadas por lógica do sistema externo
    slug = models.SlugField(unique=True)
    Categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)

    #entrada manual de algum admin
    image = models.ImageField(upload_to="produtos")

    # TODO-ALVAREZ deletar de forma responsável
    titulo = models.CharField(max_length=200)
    venda = models.DecimalField(max_digits=10, decimal_places=2)
    garantia = models.CharField(max_length=300,null=True,blank=True)
    return_devolucao = models.CharField(max_length=300,null=True,blank=True)
    
    #informações que virão do sistema da loja online
    visualizacao = models.PositiveIntegerField(default=0)
    quantidade_vendas = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.titulo

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
    
    def save(self, *args, **kwargs):
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
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL,null=True,blank=True)
    titulo = models.CharField(max_length=20,null=True,blank=True)
    cep = models.CharField(max_length=9,null=True,blank=True)
    estado = models.CharField(max_length=3,null=True,blank=True)
    cidade = models.CharField(max_length=35,null=True,blank=True)
    bairro = models.CharField(max_length=35,null=True,blank=True)
    rua = models.CharField(max_length=35,null=True,blank=True)
    numero = models.CharField(max_length=20,null=True,blank=True)
    complemento = models.CharField(max_length=140,null=True,blank=True)


    def __str__(self):
        return self.titulo + " | " + self.cliente.nome + " " + self.cliente.sobrenome


class Carro(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL,null=True,blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Carro: " + str(self.id)


class CarroProduto(models.Model):
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    quantidade = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Carro: " + str(self.carro.id) + " | CarroProduto: " + str(self.id)

PEDIDO_STATUS=[
    ("Pedido em Andamento", "Pedido em Andamento"),
    ("Pedido Recebido", "Pedido Recebido"),
    ("Pagamento Pendente", "Pagamento Pendente"),
    ("Pagamento Processando", "Pagamento Processando"),
    ("Pagamento Confirmado", "Pagamento Confirmado"),
    ("Pedido Processando", "Pedido Processando"),
    ("Pedido Caminho", "Pedido Caminho"),
    ("Pedido Completado", "Pedido Completo"),
    ("Pedido Cancelado", "Pedido Cancelado"),
]

class Pedido_order(models.Model):    
    cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE,default="")
    nome_cliente = models.CharField(max_length=200,default="")
    cpf_cnpj = models.CharField(max_length=20, default="") # cpf do cliente formatadinho direitinho
    codigo_cliente = models.CharField(max_length=8,default="",null=True,blank=True) # codigo consistente com sistema interno, se não tiver
    telefone = models.CharField(max_length=19,default="")
    email = models.EmailField(default="")

    carro = models.ForeignKey(Carro,on_delete=models.CASCADE)
    pedido_status = models.CharField(max_length=50, choices=PEDIDO_STATUS)

    total_bruto = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    frete =  models.DecimalField(max_digits=10,decimal_places=2,default=0)
    total_desconto = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    total_final = models.DecimalField(max_digits=10,decimal_places=2,default=0)

    local_de_pagamento = models.CharField(max_length=200,default="",null=True,blank=True)
    forma_de_pagamento = models.CharField(max_length=200,default="",null=True,blank=True)
    parcelas = models.PositiveIntegerField(default=1)
    valor_parcela = models.DecimalField(max_digits=10,decimal_places=2,default=0)

    endereco_envio = models.ForeignKey(Endereco,on_delete=models.CASCADE,default="")
    endereco_envio_formatado = models.CharField(max_length=200,default="")

    criado_em = models.DateTimeField(auto_now_add=True)

    # TODO-ALVAREZ deletar de forma responsável
    ordenado_por = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return "Pedido_order: " + str(self.id) + " | Status: " + self.pedido_status + " | Cliente: " + self.nome_cliente

class Pedido_Produto(models.Model):
    #importante repetir informações do produto para que uma mudança de cadastro não altere a venda
    pedido = models.ForeignKey(Pedido_order,on_delete=models.CASCADE,default="")
    produto = models.ForeignKey(Produto,on_delete=models.CASCADE,default="")

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

    def __str__(self):
        return "Pedido: " + str(self.pedido.id) + " | Codigo do produto: " + self.codigo + " | Produto: " + self.produto.titulo

class Banner(models.Model):    
    title = models.CharField(max_length=100, blank=True)

    image_grande = models.ImageField(upload_to='banners')
    image_pequena = models.ImageField(upload_to='banners')

    link = models.CharField(max_length=200, blank=True)

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class Empresa(models.Model):
    titulo = models.CharField(max_length=200)
    link = models.CharField(max_length=200,null=True,blank=True)
    image = models.ImageField(upload_to="empresas")

    def __str__(self):
        return self.titulo

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=200,default="")
    image = models.ImageField(upload_to="admin",null=True,blank=True)
    email = models.EmailField(default="")
    telefone = models.CharField(max_length=19,default="")


    def __str__(self):
        return self.user.username