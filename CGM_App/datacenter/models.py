from django.db import models


# Create your models here.
class Merek(models.Model):
    nama_merek = models.CharField(max_length=256)

    def __str__(self):
        return "{}".format(self.nama_merek)


class Barang(models.Model):
    merek = models.ForeignKey(Merek, on_delete=models.CASCADE)
    nama_barang = models.CharField(max_length=256)
    harga = models.BigIntegerField()
    part_nomor_barang = models.CharField(max_length=128)
    quantity = models.IntegerField()

    def __str__(self):
        return "{}-{}-{}".format(self.merek, self.nama_barang, self.harga)


class Pembeli(models.Model):
    nama_pembeli = models.CharField(max_length=256)

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
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE)
    tanggal_order = models.DateTimeField(auto_now=True)
    note = models.TextField()
    barang_datang = models.BooleanField()
    tanggal_datang = models.DateTimeField(null=True, blank=True, default="")
    batal = models.BooleanField()

    def __str__(self):
        return "{}-{}-{}".format(self.tanggal_order, self.barang, self.batal)
