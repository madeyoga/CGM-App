from django import forms


class PostNewItemForm(forms.Form):
    nama_barang = forms.CharField(label='nama_barang')
    merek_barang = forms.CharField(label='merek_barang')
    harga_barang = forms.IntegerField(label='harga_barang', min_value=50)
    harga_barang_preview = forms.CharField(label='harga_barang_preview')
    part_nomer = forms.CharField(label='part_nomer')
    jumlah_stock_barang = forms.IntegerField(label='jumlah_stock_barang', min_value=0)
