from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='webclient_index'),
    path('gudang/', views.index, name='webclient_gudang'),
    path('order/', views.index, name='webclient_gudang'),
    path('gudang/', views.index, name='webclient_gudang'),
]