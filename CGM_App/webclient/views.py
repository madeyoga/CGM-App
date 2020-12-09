from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'webclient/webclient_gudang.html', {"Status": "OK"})


def order(request):
    return HttpResponse("Order")


def penjualan(request):
    return HttpResponse("Order")


def pembeli(request):
    return HttpResponse("Order")
