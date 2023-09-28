from rest_framework import serializers
from .models import TarefaModel
class TarefaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TarefaModel
        fields=[
            "id",
            "nome",
            "descricao",
            "feito",
            "delete",
            "user"
        ]

    def create(self, validated_data):
        return super().create(validated_data)