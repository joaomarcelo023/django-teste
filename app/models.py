from django.db import models
from django.contrib.auth.models import User

class Base(models.Model):
    criacao = models.DateTimeField(auto_created=True)
    atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Curso(Base):
    titulo = models.CharField(max_length=255)
    url = models.URLField(unique=True)

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

    def __str__(self):
        return self.titulo

class Avaliacao(Base):
    curso = models.ForeignKey(Curso, related_name='avaliacoes', on_delete=models.CASCADE)
    nome = models.CharField(max_length = 255)
    email = models.EmailField()
    comentario = models.TextField(blank=True, default='')
    avaliacao = models.DecimalField(max_digits=2,decimal_places=1)

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        unique_together = ['email','curso']

        def __str__(self):
            return f'{self.nome} avaliou o curso {self.curso} com a nota {self.avaliacao}'


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
    preco_mercado = models.PositiveIntegerField()
    venda = models.PositiveIntegerField()
    descricao = models.TextField()
    garantia = models.CharField(max_length=300,null=True,blank=True)
    return_devolucao = models.CharField(max_length=300,null=True,blank=True)
    visualizacao = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titulo

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=200)
    endereco = models.CharField(max_length=200,null=True,blank=True)
    data_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_completo


class Carro(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL,null=True,blank=True)
    total = models.PositiveIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Carro:" + str(self.id)


class CarroProduto(models.Model):
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    avaliacao = models.PositiveIntegerField()
    quantidade = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField(default=0)
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