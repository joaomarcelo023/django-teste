from rest_framework import serializers
from .models import *

class ChoiceDisplayField(serializers.ChoiceField):
    def to_internal_value(self, data):
        for key, label in self.choices.items():
            if str(data).lower() == str(label).lower():
                return key
        self.fail('invalid_choice', input=data)

    def to_representation(self, value):
        return self.choices.get(value, value)

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestStatus
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
    variacao_faces = ChoiceDisplayField(choices=VARIACAO_FACES_PISOS)
    classe_tecnica_absorcao_pisos = ChoiceDisplayField(choices=CLASSE_TECNICA_ABSORCAO_PISOS)
    indicacao_uso = ChoiceDisplayField(choices=INDICACAO_DE_USO_PISOS)

    class Meta:
        model = Produto
        fields = '__all__'

class FotosProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotosProduto
        fields = '__all__'

class PedidoProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoProduto
        fields = '__all__'

class PedidoOrderSerializer(serializers.ModelSerializer):
    pedidoProduto = PedidoProdutoSerializer(many=True, read_only=True)

    class Meta:
        model = PedidoOrder
        fields = '__all__'
        extra_fields = ['pedidoProduto']