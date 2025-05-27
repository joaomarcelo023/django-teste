from django.contrib import admin
from django.db.models import Count

from .models import *

class FotosProdutoAdmin(admin.ModelAdmin):
    def delete_model(self, request, obj):
        obj.delete()

    def delete_queryset(self, request, queryset):
        related_produtos = (
            queryset
            .values('produto_id', 'id')  # Group by the ForeignKey
            .annotate(total=Count('id'))  # Count FPs per F
            .filter(total__gt=0)  # Safety check
        )
        
        for entry in related_produtos:
            # prod_obj = Produto.objects.get(id=entry['produto_id'])
            # prod_obj.num_fotos -= entry['total']
            # prod_obj.save()
            FotosProduto.objects.get(id=entry['id']).delete()

        # for obj in related_produtos:
        #     obj.delete()

# class ProdutoAdmin(admin.ModelAdmin):
#     filter_horizontal = ('estoque_lojas',)

admin.site.register([Cliente, Endereco, Categoria, Produto, Carro, CarroProduto, PedidoOrder, PedidoProduto, Banner, Empresa, Admin, APIKey, TestStatus])
admin.site.register(FotosProduto, FotosProdutoAdmin)
# admin.site.register(Produto, ProdutoAdmin)