from django.urls import path
from stock import views


urlpatterns = [
    path('', views.index),
    path('function_page/',views.function_page),
    path('select_page/',views.select_page),
    path('get_stock_list_csv/',views.get_stock_list_csv),
    path('load_stock_list_csv/',views.load_stock_list_csv),
    path('get_stock_k_data_csv/',views.get_stock_k_data_csv),
]