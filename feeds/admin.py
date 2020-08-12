from django.conf import settings
from django.contrib import admin

from .forms import ItemAdminForm
from .models import Item, Category


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_per_page = settings.LIST_PER_PAGE
    form = ItemAdminForm
    search_fields = ('categories__title',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_per_page = settings.LIST_PER_PAGE
