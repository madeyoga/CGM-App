from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='webclient_index'),
    path('gudang/', views.index, name='webclient_gudang'),
    path('order/', views.index, name='webclient_order'),
    path('pembeli/', views.index, name='webclient_pembeli'),
    path('penjualan/', views.index, name='webclient_penjualan'),
    path('post_item/', views.post_item, name='webclient_post_item'),
]