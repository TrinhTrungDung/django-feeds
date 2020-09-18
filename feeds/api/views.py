from rest_framework.viewsets import ModelViewSet

from .serializers import ItemSerializer
from ..models import Item


class ItemList(ModelViewSet):

    def get_queryset(self):
        items = Item.objects.all()
        category = self.request.GET.get('category', None)
        if category is not None:
            items = items.filter(categories__title=category)

        return items

    def get_serializer_class(self):
        return ItemSerializer
