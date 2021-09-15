from django.shortcuts import render
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from .serilaizers import ShopSerializer, ItemSerializer, ShopWithItemSerializer
from .models import Shop, Item
from .permissions import IsOwnerOrReadOnly, CanManageShopItem

# Create your views here.


class ShopList(GenericAPIView):
    serializer_class = ShopSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Shop.objects.all()

    def get(self, request, *args, **kwargs):
        shops = self.get_queryset().filter(owner=request.user.id)
        serializer = self.serializer_class(shops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ShopDetail(RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'shop_id'
    serializer_class = ShopWithItemSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Shop.objects.all()


class ItemList(GenericAPIView):
    serializer_class = ItemSerializer
    permission_classes = (CanManageShopItem,)
    queryset = Item.objects.all()

    def get(self, request, *args, **kwargs):
        items = self.get_queryset().filter(shop=kwargs['shop_id'])
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            shop = Shop.objects.get(id=kwargs['shop_id'])
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(shop=shop)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Shop.DoesNotExist:
            return Response({"Error": "No shop with this id exists"}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"Error": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)


class ItemDetail(RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'item_id'
    serializer_class = ItemSerializer
    permission_classes = (CanManageShopItem,)
    queryset = Item.objects.all()
