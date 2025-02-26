from rest_framework import serializers
from .models import *

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestStatus
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

class FotosProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotosProduto
        fields = '__all__'

class PedidoProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido_Produto
        fields = '__all__'

class PedidoOrderSerializer(serializers.ModelSerializer):
    pedidoProduto = PedidoProdutoSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido_order
        fields = '__all__'
        extra_fields = ['pedidoProduto']