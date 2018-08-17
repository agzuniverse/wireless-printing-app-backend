from rest_framework import serializers
from .models import Test


class TestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Test
        fields = ('id', 'url', 'name', 'desc')
