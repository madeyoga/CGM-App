from django.db import models
from django.db import connection
from datacenter.utils import fetchall_as_dict
from webclient.fields import NameField

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

    @staticmethod
    def delete_item(item_id):
        Barang.objects.get(id=item_id).delete()

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

    def __str__(self):
        return "{}-{}-{}".format(self.tanggal, self.pembeli, self.harga_total)


class DetailPenjualan(models.Model):
    id_detail_penjualan = models.IntegerField(primary_key=True)
    penjualan = models.ForeignKey(Penjualan, on_delete=models.CASCADE)
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE)
    jumlah = models.IntegerField()
    total_harga = models.IntegerField()

    def __str__(self):
        return "{}-{}-{}".format(self.penjualan, self.barang, self.jumlah)


class Order(models.Model):
    nama_barang = NameField(max_length=256, default="", blank=True)
    tanggal_order = models.DateTimeField(auto_now=True)
    note = models.TextField()
    jumlah = models.IntegerField(default=1)
    harga = models.BigIntegerField(default=1)
    barang_datang = models.BooleanField()
    tanggal_datang = models.DateTimeField(null=True, blank=True, default="")
    batal = models.BooleanField()

    def __str__(self):
        return "{}-{}".format(self.tanggal_order, self.nama_barang)
