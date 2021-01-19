from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='webclient_index'),
    path('gudang/', views.index, name='webclient_gudang'),
    path('order/', views.order, name='webclient_order'),
    path('order_history/', views.order_history, name='webclient_order_history'),
    # path('pembeli/', views.pembeli, name='webclient_pembeli'),
    # path('penjualan/', views.penjualan, name='webclient_penjualan'),

    # Item Routes
    path('post_item/', views.post_item, name='webclient_post_item'),
    path('edit_item/', views.edit_item, name='webclient_edit_item'),
    path('delete_item/<int:item_id>', views.delete_item, name='webclient_delete_item'),

    # Order Routes
    path('post_order/', views.post_order, name="webclient_post_order"),
    path('edit_order/', views.edit_order, name="webclient_post_order"),
    path('delete_order/<int:order_id>', views.delete_order, name='webclient_delete_order'),

    # Transaksi
    path('transaksi/', views.transaction, name='webclient_transaction'),
    path('transaction_history/', views.transaction_history, name='webclient_transaction_history')
]
