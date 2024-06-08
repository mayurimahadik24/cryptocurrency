# scraper/serializers.py


from rest_framework import serializers
from .models import Coin

class CryptoRequestSerializer(serializers.Serializer):
    class Meta:
        model = Coin
        fields = '__all__'
