from .models import Shop
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow shop owners to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the shop.
        return obj.owner == request.user.id


class CanManageShopItem(permissions.BasePermission):
    """
    Custom permission to only allow shop owners to add/edit items.
    """

    def has_permission(self, request, view):
        shop_id = view.kwargs.get('shop_id', None)
        is_shop_owner = False
        if shop_id:
            is_shop_owner = Shop.objects.filter(
                id=shop_id, owner=request.user.id).exists()

        if request.method in permissions.SAFE_METHODS:
            return True
        return is_shop_owner

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the shop.
        return obj.shop.owner == request.user.id
