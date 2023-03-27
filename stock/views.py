from django.shortcuts import render,HttpResponse,redirect
import baostock as bs
import pandas as pd
import os
from datetime import datetime,timedelta

from bs4 import BeautifulSoup
import multiprocessing as mp
from pyecharts.charts import Line,Kline,Grid
import pyecharts.options as opts

from stock import fc

from old_django.settings import BASE_DIR,SQLITE_ENGINE
from stock.models import stock_list,Strategic_Stock_Selection_Table


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

    context = {}

    csv_path = os.path.join(BASE_DIR,'car_trunk/csv/') + '股票列表.csv'
    data_list = pd.read_csv(csv_path,encoding='gbk')
    data_list['is_cyb'] = [ True if code.find('sz.3')>=0 else False for code in data_list['code']]
    data_list['is_kcb'] = [ True if code.find('sh.688')>=0 else False for code in data_list['code']]
    data_list['table_name'] = [ code.replace('.','_') for code in data_list['code']]
    
    print(data_list)
    st = stock_list.objects.all().delete()
    data_list.to_sql('stock_list',SQLITE_ENGINE,index=False,if_exists='append')

    context['message'] = '股票列表上传完成，用时{0}秒'.format(datetime.now() - start_time)
    return render(request,'select_page.html',context=context)

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

def load_stock_data_csv(request):
    start_time = datetime.now()

    csv_path = os.path.join(BASE_DIR,'car_trunk/stock_csv/')
    dl = []

    for root,dirs,files in os.walk(csv_path):
        for filename in files:
            if filename.endswith('csv'):
                dl.append(root + filename)

    pool = mp.Pool()
    pool.map(fc.mp_load_stock_k_and_ma_day_data,dl)
    pool.close()
    pool.join()

    context = {}
    context['message'] = '股票日线数据上传并初始化MA、KDJ完成，用时{0}秒'.format(datetime.now() - start_time)
    return render(request,'select_page.html',context=context)

def update_stock_k_data(request):
    context = {}
    today = datetime.now().strftime("%Y-%m-%d")

    st_list = get_stock_list()

    code_list = []

    ### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    #print('login respond error_code:'+lg.error_code)
    #print('login respond  error_msg:'+lg.error_msg)

    for st in st_list:
        code = st.code.replace('.','_')
        

        sql = 'select isST from {0} order by date desc LIMIT 1'.format(code)

        try:
            ST = SQLITE_ENGINE.execute(sql).fetchall()[-1]
            if ST[0]=='1':
                continue
        except:
            continue

        sql = 'select max(date) from ' + code
        start_date = SQLITE_ENGINE.execute(sql).fetchall()

        s = (start_date[0])[0].strftime("%Y-%m-%d")
        if s == start_date:
            continue
        
        try:
            start_date = ((start_date[0])[0] + timedelta(days=1)).strftime("%Y-%m-%d")
        except:
            continue

        print(code,start_date,today)

        #### 获取沪深A股历史K线数据 ####
        # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
        # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
        # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
        rs = bs.query_history_k_data_plus(st.code,
            "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
            start_date=start_date, end_date=today,
            frequency="d", adjustflag="3")
        #print('query_history_k_data_plus respond error_code:'+rs.error_code)
        #print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

        #### 打印结果集 ####
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())

       
        result = pd.DataFrame(data_list, columns=rs.fields)
        if len(result)==0:
            continue
        
        #### 结果集输出到csv文件 ####   
        #csv_path = os.path.join(BASE_DIR,'car_trunk/stock_csv/') + '{0}.csv'.format(st.code)
        result.drop(['code'],axis=1,inplace=True)
        result['volume'] = [0 if x=='' else x for x in result['volume'] ]
        result['amount'] = [0 if x=='' else x for x in result['amount'] ]
        result['turn'] = [0 if x=='' else x for x in result['turn'] ]
        result['pctChg'] = [0 if x=='' else x for x in result['pctChg'] ]
        result.to_sql(code,SQLITE_ENGINE,index=False,if_exists="append")
        #result.to_csv(csv_path, index=False)
        #print(result)

        stock = stock_list.objects.get(code=st)
        try:
            stock.k_data_update = result['date'].max()
            stock.save()
        except:
            pass

    #### 登出系统 ####
    bs.logout()


    context['message'] = '日线数据更新完成'
    return render(request,'select_page.html',context=context)

def update_stock_MA_KDJ_data(request):
    context = {}

    st_list = get_stock_list()

    dl = []
    for st in st_list:
        dl.append(st.table_name)

    pool = mp.Pool()
    pool.map(fc.mp_update_stock_MA_KDJ_data,dl)
    pool.close()
    pool.join()

    context['message'] = '移动平均线MA指标更新完成'
    return render(request,'select_page.html',context=context)

def Three_sheep_went_up_the_mountain(request):

    start_time = datetime.now()
    context = {}

    st_list = stock_list.objects.filter(is_kcb__exact=False).filter(is_cyb__exact=False)
    dl = []
    for st in st_list:
        dl.append(st.code.replace('.',"_"))

    pool = mp.Pool()
    pool.map(fc.mp_Three_sheep_went_up_the_mountain,dl)
    pool.close()
    pool.join()

    context['message'] = '三羊上山选股完成，用时{0}秒'.format(datetime.now() - start_time)
    return render(request,'select_page.html',context=context)


def look_stock(request):
    context = {}
    context['gpc_name'] = request.GET.get('gpc')
    data_date = request.GET.get('data_date')
    if data_date==None:
        data_date = datetime.now()
    try:
        data_date = datetime(int(data_date.split('-')[0]),int(data_date.split('-')[1]),int(data_date.split('-')[2]))
    except:
        pass
    context['data_date'] = data_date.strftime("%Y-%m-%d")

    data_length = request.GET.get('data_length')
    if data_length==None:
        data_length = 30
    
    context['data_length'] = data_length
    
    code_list = Strategic_Stock_Selection_Table.objects.all()
    context['stock_count'] = code_list.count()

    c_html = ""

    for code in code_list:
        table_name = code.code
        start_date = (data_date - timedelta(days=int(data_length))).strftime("%Y-%m-%d")
        sql = 'select * from {0} where date>=\'{1}\''.format(table_name,start_date)
        stock_data = pd.read_sql(sql,SQLITE_ENGINE)
        #print(stock_data)
        
        date_list = stock_data['date'].to_list()
        close_list = stock_data['close'].to_list()
        MA5_list = stock_data['MA_5'].to_list()
        MA10_list = stock_data['MA_10'].to_list()
        MA20_list = stock_data['MA_30'].to_list()
        MA30_list = stock_data['MA_30'].to_list()
        data = []

        for x in stock_data.itertuples():
            d = []
            d.append(getattr(x,'open'))
            d.append(getattr(x,'high'))
            d.append(getattr(x,'low'))
            d.append(getattr(x,'close'))
            data.append(d)

        stock = stock_list.objects.get(code=table_name.replace('_','.'))

        line1 = (
            Line()
            .add_xaxis(date_list)
            .add_yaxis("close", close_list,label_opts=False,is_symbol_show=False)
            .add_yaxis("MA5", MA5_list,label_opts=False,is_symbol_show=False)
            .add_yaxis("MA10", MA10_list,label_opts=False,is_symbol_show=False)
            .add_yaxis("MA20", MA20_list,label_opts=False,is_symbol_show=False)
            .add_yaxis("MA30", MA30_list,label_opts=False,is_symbol_show=False)
            .set_global_opts(
                title_opts=opts.TitleOpts(title=table_name, subtitle=stock.code_name),
                yaxis_opts=opts.AxisOpts(min_='dataMin'),
                tooltip_opts=opts.TooltipOpts(trigger="axis"),
                )
            )

        kline1 = (
            Kline()
            .add_xaxis(date_list)
            .add_yaxis("kline", data)
            .set_global_opts(
                xaxis_opts=opts.AxisOpts(is_scale=True),
                yaxis_opts=opts.AxisOpts(
                    is_scale=True,
                    splitarea_opts=opts.SplitAreaOpts(
                        is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                    ),
                ),
            )
        )
        overlap_1 = line1.overlap(kline1)

        grid1 = (
            Grid(init_opts=opts.InitOpts(width="1200px", height="800px"))
            .add(
                overlap_1, grid_opts=opts.GridOpts(pos_right="5%")
            )
        )

        bar_html = BeautifulSoup(grid1.render_embed(),'html.parser')
        bar_html = bar_html.body.contents

        for html in bar_html:
            c_html = c_html + str(html)
    
    context['context'] =  c_html
    return render(request,'look_stock.html',context=context)

def get_stock_list():
    return stock_list.objects.filter(is_kcb__exact=False).filter(is_cyb__exact=False)