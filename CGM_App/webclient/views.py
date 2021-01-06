from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .forms import PostNewItemForm, EditItemForm
from datacenter.models import *
from django.core import serializers


# Create your views here.
def index(request):
    # edit_form = EditItemForm(request.POST or None)
    items = Barang.objects.all().values('id', 'nama_barang', 'harga', 'harga_preview', 'quantity',
                                        'part_nomor_barang', 'merek__nama_merek')
    return render(request,
                  'webclient/webclient_gudang.html',
                  {"Status": "OK", "data": list(items)})


def order(request):
    return render(request, 'webclient/webclient_order.html')


def penjualan(request):
    return HttpResponse("Order")


def pembeli(request):
    return HttpResponse("Order")


@require_http_methods(["POST"])
def post_item(request):
    post_form = PostNewItemForm(request.POST)
    if post_form.is_valid():
        Barang.save_form(post_form)
        messages.success(request, "Save data success!")
    else:
        messages.error(request, "Please make sure to fill all the fields before submit form")
    return HttpResponseRedirect("/webclient/")


@require_http_methods(["POST"])
def edit_item(request):
    edit_form = EditItemForm(request.POST)
    if edit_form.is_valid():
        edited_item = Barang.edit_item(edit_form)
        if edited_item is None:
            messages.error(request, "Error when updating data (INVALID_ITEM_ID)! Please contact admin!")
        else:
            messages.success(request, "Update data success!")
    else:
        messages.error(request, "Invalid edit form")
    return HttpResponseRedirect("/webclient/")


def delete_item(request, item_id):
    if request.user.is_superuser:
        Barang.delete_item(item_id)
        messages.success(request, "Delete data success!")
    else:
        messages.error(request, "Only super user can delete data.")
    return HttpResponseRedirect("/webclient/")
