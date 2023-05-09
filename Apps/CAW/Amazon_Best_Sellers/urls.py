from django.urls import path
from Apps.CAW.Amazon_Best_Sellers import views

urlpatterns = [
    path('get_url', views.get_url),
    path('post_url', views.post_url),
    path('update_url', views.update_url),
    path('empty_url', views.empty_url),
]