from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from Apps.CAW.models import Agent_Pool
import json

# Create your views here.
def add_agent_pool(request):
    if request.method == 'POST':
        select1 = Agent_Pool.objects.filter(ip_address=request.POST.get('IP'),ip_port=request.POST.get('PORT')).count()
        if select1==0:
            new = Agent_Pool.objects.create(
                ip_address = request.POST.get('IP'),
                ip_port = request.POST.get('PORT'),
                nnd = request.POST.get('匿名度'),
                lx = request.POST.get('类型'),
                wz = request.POST.get('位置'),
                xysd = request.POST.get('响应速度'),
                yzsj = request.POST.get('最后验证时间'),
                fffs = request.POST.get('付费方式')
                )
            
    return HttpResponse('')

def get_agent(request):
    if request.method == 'GET':
        select = Agent_Pool.objects.all().filter(is_ky=True,is_open=False)
        if select.count()>0:
            s = select[0]
            s.is_open = True
            s.save()
            return JsonResponse({"IP":s.ip_address,"PORT":s.ip_port})
    return HttpResponse('')