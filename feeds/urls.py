from django.urls import path

from .views import index, add, edit, delete


urlpatterns = [
    path('', view=index, name="item_list"),
    path('add/', view=add, name="add"),
    path('<int:item_id>/edit', view=edit, name='edit'),
    path('<int:item_id>/delete', view=delete, name='delete'),
]
