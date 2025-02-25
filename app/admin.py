from django.contrib import admin

from .models import *

class FotosProdutoAdmin(admin.ModelAdmin):
    def delete_model(self, request, obj):
        obj.delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

admin.site.register([Cliente, Categoria, Produto, FotosProduto, Carro, CarroProduto, Pedido_order, Pedido_Produto, Endereco, Banner, Empresa, Admin, APIKey, TestStatus], FotosProdutoAdmin)