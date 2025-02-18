from django.contrib import admin

from .models import *

admin.site.register([Cliente, Categoria, Produto, FotosProduto, Carro, CarroProduto, Pedido_order, Pedido_Produto, Endereco, Banner, Empresa, Admin, APIKey, TestStatus])