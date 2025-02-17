from rest_framework import serializers
from .models import *

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestStatus # Produto
        fields = '__all__'