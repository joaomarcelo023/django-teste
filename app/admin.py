from django.contrib import admin

from .models import *

class FotosProdutoAdmin(admin.ModelAdmin):
    def delete_model(self, request, obj):
        obj.delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

class ProdutoAdmin(admin.ModelAdmin):
    filter_horizontal = ('estoque_lojas',)

admin.site.register([Cliente, Categoria, FotosProduto, Carro, CarroProduto, Pedido_order, Pedido_Produto, Endereco, Banner, Empresa, Admin, APIKey, TestStatus], FotosProdutoAdmin)
admin.site.register(Produto, ProdutoAdmin)