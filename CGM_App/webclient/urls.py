from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='webclient_index'),
    path('gudang/', views.index, name='webclient_gudang'),
    path('order/', views.order, name='webclient_order'),
    path('pembeli/', views.pembeli, name='webclient_pembeli'),
    path('penjualan/', views.penjualan, name='webclient_penjualan'),
    path('post_item/', views.post_item, name='webclient_post_item'),
    path('edit_item/', views.edit_item, name='webclient_edit_item'),
    path('delete_item/<int:item_id>', views.delete_item, name='webclient_delete_item'),
]
