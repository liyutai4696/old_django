from old_django.settings import SQLITE_ENGINE

import pandas as pd
from datetime import datetime,timedelta
import baostock as bs

def mp_load_stock_k_and_ma_day_data(path):
    print(path)

    code = path.split('/')[-1].replace('.csv','').replace('.','_')

    create_table(code)

    data = pd.read_csv(path,encoding='gbk')

    data.drop(['code'],axis=1,inplace=True)

    ma_list = [5,10,20,30,60,120,180,360]
    for ma in ma_list:
        data["MA_"+str(ma)] = data["close"].rolling(ma).mean()

    #九天最低价
    lowest = data["low"].rolling(9).min()
    lowest.fillna(value=data["low"].expanding().min(),inplace=True)
    
    #九天最高价
    highest = data["high"].rolling(9).max()
    highest.fillna(value=data["high"].expanding().min(),inplace=True)

    #计算RSV
    rsv = (data["close"] - lowest) / (highest - lowest) * 100
    rsv.fillna(value=100.0,inplace=True)

    data["k"] = rsv.ewm(com=2, adjust=False).mean()
    data["d"] = data["k"].ewm(com=2, adjust=False).mean()
    data["j"] = 3 * data["k"] - 2 * data["d"]


    #print(data)

    data.to_sql(code,SQLITE_ENGINE,index=False,if_exists='append')

    return

def mp_update_stock_MA_KDJ_data(code):
    sql = 'select date,code,close from stock_k_data where code=\'{0}\' order by date'.format(code)

    print(sql)
    data = pd.read_sql(sql,SQLITE_ENGINE)

    if len(data)==0:
        return

    ma_list = [5,10,20,30,60,120,180,360]

    for ma in ma_list:
        data["MA_"+str(ma)] = data["close"].rolling(ma).mean()
        
    data.to_sql('stock_ma_data',SQLITE_ENGINE,index=False,if_exists="append")

    return

def mp_Three_sheep_went_up_the_mountain(code):

    print(code)

    date = (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d")

    sql = "select date,close,preclose,MA_5,MA_10,MA_30 from {0} where date>=\'{1}\'".format(code,date)

    data = pd.read_sql(sql,SQLITE_ENGINE)

    if len(data)==0:
        return

    data = data.iloc[-5:,:].reset_index().drop(['index'],axis=1)

    pd_list = ""

    for x in range(len(data)):
        if data.loc[x,'close'] > data['close'].values[-5] :     #float(data.loc[x,'昨日收盘价']) :
            pd_list = pd_list + "1"
        else:
            pd_list = pd_list + "0"

    sp = data['close'].values[-1]
    ma5 = data['MA_5'].values[-1]
    ma10 = data['MA_10'].values[-1]
    ma30 = data['MA_30'].values[-1] 

    if pd_list.find('111') != -1 and sp > 6.0 and sp < 15.0 and ma5 > ma10 and ma5 > ma30:
        for q in range(len(data)):
            if data['MA_5'].values[q] < data['MA_30'].values[q]:
                d = {
                    'date':datetime.now(),
                    'code':code,
                    'selection_strategy':'三羊上山',
                }
                d = pd.DataFrame(d,index=[0])
                d.to_sql('strategic_stock_selection_table',SQLITE_ENGINE,index=False,if_exists='append')
                return
    return

def create_table(code):
    try:
        sql = 'drop table ' + code
        SQLITE_ENGINE.execute(sql)
    except:
        pass


    ll="""(date DATE primary key,
                        open double(15,3),
                        high double(15,3),
                        low double(15,3),
                        close double(15,3),
                        preclose double(15,3),
                        volume BIGINT,
                        amount BIGINT,
                        adjustflag VARCHAR(10),
                        turn double(15,3),
                        tradestatus VARCHAR(10),
                        pctChg double(15,3),
                        isST VARCHAR(10),
                        MA_5 double(15,3),
                        MA_10 double(15,3),
                        MA_20 double(15,3),
                        MA_30 double(15,3),
                        MA_60 double(15,3),
                        MA_120 double(15,3),
                        MA_180 double(15,3),
                        MA_360 double(15,3),
                        k double(15,3),
                        d double(15,3),
                        j double(15,3)
                    )"""
    sql = 'create table if not exists ' + code + ll
    SQLITE_ENGINE.execute(sql)
