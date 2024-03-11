from django.contrib import admin

from .models import *

admin.site.register([Admin,Cliente,Categoria,Produto,Carro,CarroProduto,Pedido_order,Empresa])

@admin.register(Curso)
class CursoAdmin (admin.ModelAdmin):
    list_display = ('titulo','url','criacao','atualizacao','ativo')

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('curso','nome','email','avaliacao','criacao','atualizacao','ativo')