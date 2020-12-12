from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='api_index'),
    path('items/', views.items, name='api_barang'),
]
