from django.urls import path
from stock import views


urlpatterns = [
    path('', views.index),
    path('function_page/',views.function_page),
    path('select_page/',views.select_page),
    path('get_stock_list_csv/',views.get_stock_list_csv),
    path('load_stock_list_csv/',views.load_stock_list_csv),
    path('get_stock_k_data_csv/',views.get_stock_k_data_csv),
    path('load_stock_data_csv/',views.load_stock_data_csv),
    path('update_stock_k_data/',views.update_stock_k_data),
    path('update_stock_MA_KDJ_data/',views.update_stock_MA_KDJ_data),
    path('Three_sheep_went_up_the_mountain/',views.Three_sheep_went_up_the_mountain),
    path('see_Three_sheep_went_up_the_mountain/',views.see_Three_sheep_went_up_the_mountain),
    path('look_stock/',views.look_stock),
]