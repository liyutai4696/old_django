from django.shortcuts import render
from django.http import HttpResponse
from Apps.CAW.Amazon_Best_Sellers.models import ymx_url_list,Amazon_Best_Sellers

# Create your views here.

def get_url(requets):

    url = ymx_url_list.objects.get().filter()

    return HttpResponse('')

def post_url(request):

    if request.method == 'POST':
        select1 = ymx_url_list.objects.filter(category=request.POST.get('类目')).count()
        select2 = ymx_url_list.objects.filter(category=request.POST.get('地址')).count()
        if select1==0 and select2==0:
            new = ymx_url_list.objects.create(
                category = request.POST.get('类目'),
                url_address = request.POST.get('地址'),
                is_execute= request.POST.get('执行中'),
                is_complete = request.POST.get('已执行')
                )

    return HttpResponse('')

def update_url(request):

    return HttpResponse('')  

def empty_url(request):

    d = ymx_url_list.objects.all().delete()

    return HttpResponse('')  