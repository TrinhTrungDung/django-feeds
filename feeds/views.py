from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from .models import Item
from .forms import ItemCreationForm


def index(request):
    item_list = Item.objects.all()
    category = request.GET.get('category', None)
    if category is not None:
        item_list = item_list.filter(categories__title=category)
    page = request.GET.get('page', 1)
    paginator = Paginator(item_list, settings.LIST_PER_PAGE)

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return render(request, 'item_list.html', {'items': items})


def add(request):
    form = ItemCreationForm()
    if request.method == "POST":
        form = ItemCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feeds:item_list')
        else:
            return render(request, 'item_add.html', {'form': form})

    return render(request, 'item_add.html', {'form': form})


def edit(request, item_id):
    item_id = int(item_id)
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return redirect('feeds:item_list')
    form = ItemCreationForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('feeds:item_list')

    return render(request, 'item_edit.html', {'form': form, 'item': item})


def delete(request, item_id):
    item_id = int(item_id)
    try:
        item = Item.objects.get(id=item_id)
        item.delete()
    except Item.DoesNotExist:
        return redirect('feeds:item_list')

    return redirect('feeds:item_list')
