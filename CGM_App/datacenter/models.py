from django.db import models
from django.db import connection
from django.utils import timezone

from datacenter.utils import fetchall_as_dict
from webclient.fields import NameField
import json

# Create your models here.


class Merek(models.Model):
    nama_merek = models.CharField(max_length=256)

    @staticmethod
    def try_get_brand(brand_name):
        if not Merek.objects.filter(nama_merek=brand_name).exists():
            brand = Merek.objects.create(nama_merek=brand_name)
            brand.save()
        else:
            brand = Merek.objects.filter(nama_merek=brand_name).get()
        return brand

    def __str__(self):
        return "{}".format(self.nama_merek)


class ItemGroup(models.Model):
    group_name = models.CharField(max_length=256)

    def __str__(self):
        return self.group_name


class Barang(models.Model):
    merek = models.ForeignKey(Merek, on_delete=models.CASCADE)
    # kelompok = models.ForeignKey(ItemGroup, on_delete=models.CASCADE)
    nama_barang = NameField(max_length=256, blank=True)
    harga = models.BigIntegerField()
    harga_preview = models.CharField(max_length=16, default="Rp. -")
    part_nomor_barang = models.CharField(max_length=128)
    quantity = models.IntegerField()

    @staticmethod
    def get_all():
        with connection.cursor() as cursor:
            query = "SELECT * FROM datacenter_BARANG " \
                    "JOIN datacenter_MEREK ON datacenter_MEREK.ID = datacenter_BARANG.MEREK_ID"
            cursor.execute(query)
            items = fetchall_as_dict(cursor)
        return items

    @staticmethod
    def save_form(post_form):
        item_name = post_form.cleaned_data['nama_barang']
        item_brand = post_form.cleaned_data['merek_barang']
        item_price = post_form.cleaned_data['harga_barang']
        item_price_preview = post_form.cleaned_data['harga_barang_preview']
        item_part_number = post_form.cleaned_data['part_nomer']
        item_stock = post_form.cleaned_data['jumlah_stock_barang']

        # Check brand
        if not Merek.objects.filter(nama_merek=item_brand).exists():
            brand = Merek.objects.create(nama_merek=item_brand)
            brand.save()
        else:
            brand = Merek.objects.filter(nama_merek=item_brand).get()

        new_item = Barang.objects.create(nama_barang=item_name,
                                         merek=brand,
                                         harga=item_price,
                                         harga_preview=item_price_preview,
                                         part_nomor_barang=item_part_number,
                                         quantity=item_stock)
        new_item.save()

        return new_item

    @staticmethod
    def save_post_request(post):
        item_name = post.get('nama_barang', '')
        item_brand = post.get('merek_barang', '')
        item_price = post.get('harga_barang', 50)
        item_price_preview = post.get('harga_barang_preview', item_price)
        item_part_number = post.get('part_nomer', '')
        item_stock = post.get('jumlah_stock_barang', 0)

        # Check brand
        if not Merek.objects.filter(nama_merek=item_brand).exists():
            brand = Merek.objects.create(nama_merek=item_brand)
            brand.save()
        else:
            brand = Merek.objects.filter(nama_merek=item_brand).get()

        new_item = Barang.objects.create(nama_barang=item_name,
                                         merek=brand,
                                         harga=item_price,
                                         harga_preview=item_price_preview,
                                         part_nomor_barang=item_part_number,
                                         quantity=item_stock)
        new_item.save()

        return new_item

    @staticmethod
    def edit_item(edit_form):
        item_id = int(edit_form.cleaned_data['id_barang'])

        if Barang.objects.filter(id=item_id).exists():
            target_item = Barang.objects.filter(id=item_id).get()
            item_name = edit_form.cleaned_data['nama_barang']
            item_brand = edit_form.cleaned_data['merek_barang']
            item_price = edit_form.cleaned_data['harga_barang']
            item_price_preview = edit_form.cleaned_data['harga_barang_preview']
            item_part_number = edit_form.cleaned_data['part_nomer']
            item_stock = edit_form.cleaned_data['jumlah_stock_barang']

            item_brand = Merek.try_get_brand(item_brand)

            target_item.merek_barang = item_brand
            target_item.nama_barang = item_name
            target_item.harga = item_price
            target_item.harga_preview = item_price_preview
            target_item.part_nomor_barang = item_part_number
            target_item.quantity = item_stock

            target_item.save()

            return target_item

        return None

    def __str__(self):
        return "{}-{}-{}".format(self.merek, self.nama_barang, self.harga)


class Pembeli(models.Model):
    nama_pembeli = NameField(max_length=256)

    def __str__(self):
        return "{}".format(self.nama_pembeli)


class Penjualan(models.Model):
    pembeli = models.ForeignKey(Pembeli, on_delete=models.CASCADE)
    barangs = models.ManyToManyField(Barang, through="DetailPenjualan")
    tanggal = models.DateTimeField(auto_now=True)
    harga_total = models.BigIntegerField()

    @staticmethod
    def save_form(post_form):
        list_of_items = json.loads(post_form.cleaned_data["json_list_of_items"])
        buyer_name = post_form.cleaned_data["customer"]
        buy_datetime = post_form.cleaned_data["datetime"]

        # Check if Pembeli is not exists yet, create new
        if Pembeli.objects.filter(nama_pembeli=buyer_name).exists():
            buyer = Pembeli.objects.filter(nama_pembeli=buyer_name).get()
        else:
            buyer = Pembeli.objects.create(nama_pembeli=buyer_name)
            buyer.save()

        transaction_data = Penjualan.objects.create(pembeli=buyer, tanggal=buy_datetime, harga_total=0)

        # Process Items
        total_price = 0
        for item in list_of_items:
            total_price += int(item['harga'])

            item_name = item['barang'].upper()
            if Barang.objects.filter(nama_barang=item_name).exists():
                barang = Barang.objects.filter(nama_barang=item_name).get()
            else:
                barang = Barang.objects.create(
                    nama_barang=item_name, 
                    merek=Merek.try_get_brand('unknown'), 
                    harga=1, 
                    harga_preview="Rp. 1", 
                    quantity=1)
                barang.save()
            
            transaction_data.barangs.add(barang)

        transaction_data.harga_total = total_price
        transaction_data.save()

    def __str__(self):
        return "{}-{}-{}".format(self.tanggal, self.pembeli, self.harga_total)


class DetailPenjualan(models.Model):
    id_detail_penjualan = models.IntegerField(primary_key=True)
    penjualan = models.ForeignKey(Penjualan, on_delete=models.CASCADE)
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE)

    def __str__(self):
        return "{}-{}".format(self.penjualan, self.barang)


class Order(models.Model):
    nama_barang = NameField(max_length=256, default="", blank=True)
    tanggal_order = models.DateTimeField(default=timezone.now)
    note = models.TextField()
    jumlah = models.IntegerField(default=1)
    harga = models.BigIntegerField(default=1)
    barang_datang = models.BooleanField()
    tanggal_datang = models.DateTimeField(null=True, blank=True, default="")
    batal = models.BooleanField()

    @staticmethod
    def save_form(post_form):
        order_item_name = post_form.cleaned_data['nama_barang']
        order_date = post_form.cleaned_data['tanggal_order']
        note = post_form.cleaned_data['note']
        quantity = post_form.cleaned_data['jumlah_barang']
        each_price = post_form.cleaned_data['harga_barang']

        new_order = Order.objects.create(nama_barang=order_item_name,
                                         tanggal_order=order_date,
                                         note=note,
                                         jumlah=quantity,
                                         harga=each_price,
                                         barang_datang=False,
                                         batal=False,
                                         tanggal_datang=None)
        new_order.save()

        return new_order

    @staticmethod
    def edit_form(edit_form):
        order_id = edit_form.cleaned_data['id_order']

        if Order.objects.filter(id=order_id).exists():
            target_order_data = Order.objects.filter(id=order_id).get()

            order_item_name = edit_form.cleaned_data['nama_barang']
            order_date = edit_form.cleaned_data['tanggal_order']
            note = edit_form.cleaned_data['note']
            quantity = edit_form.cleaned_data['jumlah_barang']
            each_price = edit_form.cleaned_data['harga_barang']
            complete_date = edit_form.cleaned_data['tanggal_datang']

            target_order_data.nama_barang = order_item_name
            target_order_data.tanggal_order = order_date
            target_order_data.note = note
            target_order_data.jumlah = quantity
            target_order_data.harga = each_price
            target_order_data.tanggal_datang = complete_date

            target_order_data.save()

            return target_order_data

        return None

    def __str__(self):
        return "{}-{}".format(self.tanggal_order, self.nama_barang)
