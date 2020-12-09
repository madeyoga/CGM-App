from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Merek)
admin.site.register(Barang)
admin.site.register(Pembeli)
admin.site.register(Penjualan)
admin.site.register(DetailPenjualan)
admin.site.register(Order)
