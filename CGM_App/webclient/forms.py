from django import forms


class PostNewItemForm(forms.Form):
    nama_barang = forms.CharField(label='nama_barang')
    merek_barang = forms.CharField(label='merek_barang')
    harga_barang = forms.IntegerField(label='harga_barang', min_value=50)
    harga_barang_preview = forms.CharField(label='harga_barang_preview')
    part_nomer = forms.CharField(label='part_nomer', required=False)
    jumlah_stock_barang = forms.IntegerField(label='jumlah_stock_barang', min_value=0)
    satuan_barang = forms.CharField(label='satuan_barang')
    location = forms.CharField(label='location', required=False)
    preview_image = forms.ImageField(label='preview_image', required=False)


class EditItemForm(forms.Form):
    id_barang = forms.CharField(label='id_barang')
    nama_barang = forms.CharField(label='nama_barang')
    merek_barang = forms.CharField(label='merek_barang')
    harga_barang = forms.IntegerField(label='harga_barang', min_value=50)
    harga_barang_preview = forms.CharField(label='harga_barang_preview')
    part_nomer = forms.CharField(label='part_nomer', required=False)
    jumlah_stock_barang = forms.IntegerField(label='jumlah_stock_barang', min_value=0)
    satuan_barang = forms.CharField(label='satuan_barang')
    location = forms.CharField(label='location', required=False)
    preview_image = forms.ImageField(label='preview_image', required=False)


class PostNewOrderForm(forms.Form):
    id_order = forms.CharField(label='id_order')
    tanggal_order = forms.DateTimeField(label='tanggal_order')
    nama_barang = forms.CharField(label='nama_barang')
    jumlah_barang = forms.IntegerField(label='jumlah_barang')
    harga_barang = forms.IntegerField(label='harga_barang')
    note = forms.CharField(label='note', required=False)


class EditOrderForm(forms.Form):
    id_order = forms.CharField(label='id_order')
    tanggal_order = forms.DateTimeField(label='tanggal_order')
    nama_barang = forms.CharField(label='nama_barang')
    jumlah_barang = forms.IntegerField(label='jumlah_barang')
    harga_barang = forms.IntegerField(label='harga_barang')
    note = forms.CharField(label='note')
    tanggal_datang = forms.DateTimeField(label='tanggal_datang', required=False)


class PostTransactionItemForm(forms.Form):
    customer = forms.CharField(label='customer')
    datetime = forms.DateTimeField(label='datetime')
    json_list_of_items = forms.CharField(label='json_list_of_items')
