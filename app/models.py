from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.titulo

class Produto(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    Categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="produtos")
    venda = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    garantia = models.CharField(max_length=300,null=True,blank=True)
    return_devolucao = models.CharField(max_length=300,null=True,blank=True)
    visualizacao = models.PositiveIntegerField(default=0)
    unidade = models.CharField(max_length=30,default="un")
    fechamento_embalagem = models.DecimalField(max_digits=10, decimal_places=2,default=1.00)

    def __str__(self):
        return self.titulo

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nome = models.CharField(max_length=200,default="")
    sobrenome = models.CharField(max_length=200,default="")

    cpf_ou_cnpj = models.CharField(max_length=14,default="")
    cpf_ou_cnpj_formatado = models.CharField(max_length=20, default="")
    bool_cpf_cnpj = models.BooleanField(default=False)

    email = models.EmailField(default=2)
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
    cep = models.CharField(max_length=8,null=True,blank=True)
    estado = models.CharField(max_length=3,null=True,blank=True)
    cidade = models.CharField(max_length=35,null=True,blank=True)
    bairro = models.CharField(max_length=35,null=True,blank=True)
    rua = models.CharField(max_length=35,null=True,blank=True)
    numero = models.CharField(max_length=20,null=True,blank=True)
    complemento = models.CharField(max_length=140,null=True,blank=True)


    def __str__(self):
        return self.titulo


class Carro(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL,null=True,blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Carro:" + str(self.id)


class CarroProduto(models.Model):
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    quantidade = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Carro:" + str(self.carro.id) + "CarroProduto:" + str(self.id)

PEDIDO_STATUS=[
    ("Pedido Recebido","Pedido Recebido"),
    ("Pedido Processando", "Pedido Processando"),
    ("Pedido Caminho", "Pedido Caminho"),
    ("Pedido Completado", "Pedido Completo"),
    ("Pedido Cancelado", "Pedido Cancelado"),
]

class Pedido_order(models.Model):
    carro = models.OneToOneField(Carro,on_delete=models.CASCADE)
    ordenado_por = models.CharField(max_length=200)
    telefone = models.CharField(max_length=10)
    email = models.EmailField(null=True,blank=True)
    endereco_envio = models.CharField(max_length=200)
    subtotal = models.PositiveIntegerField()
    desconto = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    pedido_status = models.CharField(max_length=50,choices=PEDIDO_STATUS)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Pedido_order:" + str(self.id)

class Empresa(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="empresas")

    def __str__(self):
        return self.titulo

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=200)
    data_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="admins")
    tel = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

class encarte(models.Model):

    pdf1 = models.FileField(upload_to='pdfs/')
    pdf2 = models.FileField(upload_to='pdfs/')
    pdf3 = models.FileField(upload_to='pdfs/')

    def __str__(self):
        return "Encarte numero:" + str(self.id)
    
class Banner(models.Model):    
    title = models.CharField(max_length=100, blank=True)

    image_grande = models.ImageField(upload_to='banners')
    image_pequena = models.ImageField(upload_to='banners')

    link = models.CharField(max_length=200, blank=True)

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title