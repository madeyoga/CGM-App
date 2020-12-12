from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .forms import PostNewItemForm
from datacenter.models import *
from django.core import serializers


# Create your views here.
def index(request):
    items = Barang.objects.all().values('id', 'nama_barang', 'harga', 'harga_preview', 'quantity',
                                        'part_nomor_barang', 'merek__nama_merek')
    return render(request,
                  'webclient/webclient_gudang.html',
                  {"Status": "OK", "data": list(items)})


def order(request):
    return HttpResponse("Order")


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
        return HttpResponseRedirect("/webclient/")
    else:
        messages.error(request, "Please make sure to fill all the fields before submit form")
        return HttpResponseRedirect("/webclient/")
