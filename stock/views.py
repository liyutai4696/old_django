from django.shortcuts import render,HttpResponse
import baostock as bs
import pandas as pd
import os
from datetime import datetime

from old_django.settings import BASE_DIR

# Create your views here.

def index(request):

    context = {}
    context['page_title'] = '主页'
    context['context_title'] = '概览'

    return render(request,'index.html',context=context)

def function_page(request):
    context = {}
    context['page_title'] = '主页'
    context['context_title'] = '功能'



    return render(request,'function_page.html',context=context)


def select_page(request):
    context = {}
    context['today'] = datetime.now().strftime("%Y-%m-%d")
    print(context['today'])

    return render(request,'select_page.html',context=context)

def get_stock_list_csv(request):

    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:'+lg.error_code)
    print('login respond  error_msg:'+lg.error_msg)

    # 获取行业分类数据
    rs = bs.query_stock_industry()
    # rs = bs.query_stock_basic(code_name="浦发银行")
    print('query_stock_industry error_code:'+rs.error_code)
    print('query_stock_industry respond  error_msg:'+rs.error_msg)

    # 打印结果集
    industry_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        industry_list.append(rs.get_row_data())
    result = pd.DataFrame(industry_list, columns=rs.fields)
    # 结果集输出到csv文件
    result_path = os.path.join(BASE_DIR,'car_trunk/csv/') + '股票列表.csv'
    result.to_csv(result_path, encoding="gbk", index=False)
    print(result)

    # 登出系统
    bs.logout()


    context = {}
    context['message'] = '股票列表下载完成'
    return render(request,'select_page.html',context=context)


def load_stock_list_csv(request):


    context = {}
    context['message'] = '股票列表上传完成'
    return render(request,'select_page.html',context=context)


def get_stock_k_data_csv(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    print(start_date,end_date)
    
    
    
    context = {}
    context['message'] = '股票日线数据下载完成.csv'
    return render(request,'select_page.html',context=context)