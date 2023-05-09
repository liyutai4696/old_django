from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('CAW/', include('Apps.CAW.urls')),
    path('stock/', include('Apps.stock.urls')),
]