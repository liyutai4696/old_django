from django.shortcuts import render,HttpResponse,redirect
import baostock as bs
import pandas as pd
import os
from datetime import datetime

import django
import multiprocessing as mp

from stock import fc

from old_django.settings import BASE_DIR,SQLITE_ENGINE
from stock.models import stock_list,stock_k_data


# Create your views here.

def index(request):

    context = {}
    context['page_title'] = '主页'
    context['context_title'] = '概览'

    return redirect('/select_page/')

    #return render(request,'index.html',context=context)

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

    start_time = datetime.now()

    st = stock_list.objects.all().delete()

    context = {}

    csv_path = os.path.join(BASE_DIR,'car_trunk/csv/') + '股票列表.csv'
    data_list = pd.read_csv(csv_path,encoding='gbk')
    data_list['is_cyb'] = [ True if code.find('sz.3')>0 else False for code in data_list['code']]
    data_list['is_kcb'] = [ True if code.find('sh.688')>0 else False for code in data_list['code']]
    
    data_list.to_sql('stock_list',SQLITE_ENGINE,index=False,if_exists='append')

    #pool = mp.Pool()
    #pool.map(fc.load_stock_csv,dl)
    #pool.close()
    #pool.join()

    context['message'] = '股票列表上传完成，用时{0}秒'.format(datetime.now() - start_time)
    return render(request,'select_page.html',context=context)

def load_stock_csv(data):

    code = getattr(data,'code')

    d = {
            'stock_code':code,
            'stock_name':getattr(data,'code_name'),
            'stock_industry':getattr(data,'industry'),
            'stock_industryClassification':getattr(data,'industryClassification'),
            'update':getattr(data,'updateDate'),
        }

    if code.find('sz.3')>=0:
        d['is_cyb'] = True

    if code.find('sh.688')>=0:
        d['is_kcb'] = True

    d = pd.DataFrame(d)
    print(d)

    #stock = stock_list.objects.create(**d)

def get_stock_k_data_csv(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    print(start_date,end_date)

    st_list = stock_list.objects.filter(is_kcb__exact=False).filter(is_cyb__exact=False)

    ### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:'+lg.error_code)
    print('login respond  error_msg:'+lg.error_msg)

    for st in st_list:
        print(st)


        #### 获取沪深A股历史K线数据 ####
        # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
        # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
        # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
        rs = bs.query_history_k_data_plus(st.code,
            "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
            start_date=start_date, end_date=end_date,
            frequency="d", adjustflag="3")
        #print('query_history_k_data_plus respond error_code:'+rs.error_code)
        #print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

        #### 打印结果集 ####
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)

        #### 结果集输出到csv文件 ####   
        csv_path = os.path.join(BASE_DIR,'car_trunk/stock_csv/') + '{0}.csv'.format(st.code)
        result.to_csv(csv_path, index=False)
        #print(result)

        stock = stock_list.objects.get(code=st)
        try:
            stock.k_data_update = result['date'].max()
            stock.save()
        except:
            pass

    #### 登出系统 ####
    bs.logout()

    context = {}
    context['message'] = '股票日线数据下载完成.csv'
    return render(request,'select_page.html',context=context)

def load_stock_k_data_csv(request):

    csv_path = os.path.join(BASE_DIR,'car_trunk/stock_csv/')

    for root,dirs,files in os.walk(csv_path):
        for filename in files[:2]:
            if filename.endswith('csv'):


                data = pd.read_csv(root + filename,encoding='gbk')
                #data['date'] = data['date'].astype('date')
                for d in data.itertuples():
                    load_stock_k_day_data(d)

    context = {}
    context['message'] = '股票日线数据上传完成.csv'
    return render(request,'select_page.html',context=context)

def load_stock_k_day_data(data):
    d = {
        'date': getattr(data,'date') ,
        'code': getattr(data,'code') ,
        'open': getattr(data,'open') ,
        'high': getattr(data,'high') ,
        'low': getattr(data,'low') ,
        'close': getattr(data,'close') ,
        'preclose': getattr(data,'preclose') ,
        'volume': getattr(data,'volume') ,
        'amount': getattr(data,'amount') ,
        'adjustflag': getattr(data,'adjustflag') ,
        'turn': getattr(data,'turn') ,
        'tradestatus': getattr(data,'tradestatus') ,
        'pctChg': getattr(data,'pctChg') ,
        'isST': getattr(data,'isST') ,
    }
    k_data = stock_k_data.objects.create(**d)