from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from datacenter.models import *
from django.forms.models import model_to_dict


# Create your views here.
@require_http_methods(["GET"])
def index(request):
    return HttpResponse("API Index")


@require_http_methods(["GET", "POST"])
def items(request):

    if request.method == 'POST':
        new_item = Barang.save_post_request(request.POST)
        return JsonResponse({"POST": "OK", "item": model_to_dict(new_item)})

    item_list = Barang.objects.values('id', 'nama_barang', 'harga', 'harga_preview', 'quantity',
                                      'part_nomor_barang', 'merek__nama_merek')

    return JsonResponse(list(item_list), safe=False)
