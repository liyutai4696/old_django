from django.urls import path,include
from Apps.CAW import views

urlpatterns = [
    path('Amazon_Best_Sellers/', include('Apps.CAW.Amazon_Best_Sellers.urls')),
    path('add_agent_pool/', views.add_agent_pool),
    path('get_agent/', views.get_agent),
]