from django.urls import path
from . import views

urlpatterns = [
    path('shops/', view=views.ShopList.as_view(), name='shop list'),
    path('shop/<int:shop_id>/',
         view=views.ShopDetail.as_view(), name='shop detail'),
    path('items/<int:shop_id>/', view=views.ItemList.as_view(), name='shop list'),
    path('item/<int:shop_id>/<int:item_id>/',
         view=views.ItemDetail.as_view(), name='item detail')
]
