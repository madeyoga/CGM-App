from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .forms import PostNewItemForm, EditItemForm, PostNewOrderForm, EditOrderForm
from datacenter.models import *


# Create your views here.
def index(request):
    # edit_form = EditItemForm(request.POST or None)
    items = Barang.objects.all().values('id', 'nama_barang', 'harga', 'harga_preview', 'quantity',
                                        'part_nomor_barang', 'merek__nama_merek')
    return render(request,
                  'webclient/webclient_gudang.html',
                  {"Status": "OK", "data": list(items)})


def order(request):
    orders = Order.objects.filter(tanggal_datang=None).values()
    return render(request,
                  'webclient/webclient_order.html',
                  {'data': list(orders)})


def order_history(request):
    order_histories = Order.objects.all().values()
    return render(request, 'webclient/webclient_order_history.html', {'data': list(order_histories)})


def penjualan(request):
    return HttpResponse("Penjualan")


def pembeli(request):
    return HttpResponse("Pembeli")


# Forms for Item


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
        Barang.objects.get(id=item_id).delete()
        messages.success(request, "Delete data success!")
    else:
        messages.error(request, "Only super user can delete data.")
    return HttpResponseRedirect("/webclient/")


# Forms for Order


@require_http_methods(["POST"])
def post_order(request):
    post_form = PostNewOrderForm(request.POST)
    if post_form.is_valid():
        Order.save_form(post_form)
        messages.success(request, "Save data success!")
    else:
        messages.error(request, "Please make sure to fill all the fields before submit form")
    return HttpResponseRedirect("/webclient/order/")


@require_http_methods(["POST"])
def edit_order(request):
    edit_form = EditOrderForm(request.POST)
    if edit_form.is_valid():
        edited_item = Order.edit_form(edit_form)
        if edited_item is None:
            messages.error(request, "Error when updating data (INVALID_ITEM_ID)! Please contact admin!")
        else:
            messages.success(request, "Update data success!")
    else:
        messages.error(request, "Invalid edit form")
    return HttpResponseRedirect("/webclient/order/")


def delete_order(request, order_id):
    if request.user.is_superuser:
        Order.objects.get(id=order_id).delete()
        messages.success(request, "Delete data success!")
    else:
        messages.error(request, "Only super user can delete data.")
    return HttpResponseRedirect("/webclient/order/")
