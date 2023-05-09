from django.urls import path,include

urlpatterns = [
    path('Amazon_Best_Sellers/', include('Apps.CAW.Amazon_Best_Sellers.urls'))
]