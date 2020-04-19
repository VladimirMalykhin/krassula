from rest_framework import serializers
from .models import *

class ProductsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Products

        exclude = ()
        

class TovarsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Products
        filter_fields=("category__id",)
        exclude = ()
        

class CatalogSerializers(serializers.ModelSerializer):
    class Meta:
        model = Categories

        exclude = ()