from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .forms import *
from datacenter.models import *
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict


# Create your views here.
@login_required(login_url='/login/')
def index(request):
    items = Barang.objects.all().values('id', 'nama_barang', 'harga', 'harga_preview', 'quantity',
                                        'part_nomor_barang', 'merek__nama_merek', 
                                        'preview_image', 'location', 'unit_type')
    return render(request,
                  'webclient/webclient_gudang.html',
                  {"Status": "OK", "data": list(items)})


@login_required(login_url='/login/')
def order(request):
    orders = Order.objects.filter(tanggal_datang=None).values()
    return render(request,
                  'webclient/webclient_order.html',
                  {'data': list(orders)})


@login_required(login_url='/login/')
def order_history(request):
    order_histories = Order.objects.all().values()
    return render(request, 'webclient/webclient_order_history.html', {'data': list(order_histories)})


@login_required(login_url='/login/')
def transaction(request):
    if request.method == 'POST':
        post_form = PostTransactionItemForm(request.POST)
        if post_form.is_valid():
            penjualan = Penjualan.save_form(post_form)
            messages.success(request, "Save data success!")
        else:
            messages.error(request, "Invalid form input")
        return HttpResponseRedirect("/webclient/transaksi/")
    
    items = Barang.objects.all().values('nama_barang')
    brands = Merek.objects.all().values('nama_merek')
    return render(request, 
                  'webclient/webclient_transaction_history_submission.html', 
                  {'items': list(items), 'brands': list(brands)})


@login_required(login_url='/login/')
@require_http_methods(["GET"])
def transaction_history(request):
    transactions = Penjualan.objects.all()
    list_of_transactions = []
    for transaction in transactions.iterator():
        temp_transaction = model_to_dict(transaction)
        temp_transaction['nama_pembeli'] = transaction.pembeli.nama_pembeli
        # temp_transaction['barangs'] = list(transaction.barangs.all().values())
        for index, item in enumerate(temp_transaction['barangs']):
            temp_transaction['barangs'][index] = model_to_dict(item)
            del temp_transaction['barangs'][index]['preview_image']
        list_of_transactions.append(temp_transaction)
    return render(request, 
                  'webclient/webclient_transaction_history.html', 
                  {'data': list_of_transactions})


@login_required(login_url='/login/')
def pembeli(request):
    return HttpResponse("Pembeli")


# Forms for Item


@require_http_methods(["POST"])
def post_item(request):
    post_form = PostNewItemForm(request.POST, request.FILES)
    if post_form.is_valid():
        Barang.save_form(post_form, request.FILES)
        messages.success(request, "Save data success!")
    else:
        messages.error(request, "Please make sure to fill all the fields before submit form")
    return HttpResponseRedirect("/webclient/")


@require_http_methods(["POST"])
def edit_item(request):
    edit_form = EditItemForm(request.POST, request.FILES)
    if edit_form.is_valid():
        edited_item = Barang.edit_item(edit_form, request.FILES)
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
