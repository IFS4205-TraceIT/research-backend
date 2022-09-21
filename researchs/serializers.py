from .models import (
    Researchdata
)

from rest_framework import exceptions, serializers 

class ResearchdataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Researchdata
        fields = '__all__'