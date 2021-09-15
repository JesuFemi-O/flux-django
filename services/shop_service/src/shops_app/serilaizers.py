from rest_framework import serializers
from .models import Item, Shop


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        extra_kwargs = {"shop": {"read_only": True}}


class ShopSerializer(serializers.ModelSerializer):

    def get_items(self, obj):
        items = Item.objects.filter(shop=obj.id)
        serializer = ItemSerializer(items, many=True)
        return serializer.data

    class Meta:
        model = Shop
        fields = '__all__'
        extra_kwargs = {"owner": {"read_only": True}}


class ShopWithItemSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    def get_items(self, obj):
        items = Item.objects.filter(shop=obj.id)
        serializer = ItemSerializer(items, many=True)
        return serializer.data

    class Meta:
        model = Shop
        fields = '__all__'
        extra_kwargs = {"owner": {"read_only": True}}
