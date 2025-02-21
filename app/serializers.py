from rest_framework import serializers
from .models import *

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestStatus # Produto
        fields = '__all__'

class PedidoOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido_order
        fields = '__all__'