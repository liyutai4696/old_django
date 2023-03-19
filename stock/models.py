from django.db import models

# Create your models here.

class stock_list(models.Model):
    code = models.CharField(primary_key=True,verbose_name='股票代码',max_length=10)
    code_name = models.CharField(verbose_name='股票名称',max_length=10)
    table_name = models.CharField(verbose_name='表名称',max_length=10,null=True)
    industry = models.CharField(verbose_name='行业类别',max_length=8,null=True)
    industryClassification = models.CharField(verbose_name='行业分类',max_length=24)
    is_kcb = models.BooleanField(verbose_name='是否科创板',default=False,null=True)
    is_cyb = models.BooleanField(verbose_name='是否创业板',default=False,null=True)
    updateDate = models.DateField(verbose_name='更新日期')
    k_data_update = models.DateField(verbose_name='日线数据更新日期',null=True)

    def __str__(self):
        return self.code
    
    class Meta:
        verbose_name = "股票列表"
        db_table = 'stock_list'

class stock_data(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='主键')
    date = models.DateField(verbose_name='日期')
    code = models.CharField(verbose_name='股票代码',max_length=10,null=True)
    open = models.FloatField(verbose_name='开盘价',null=True)
    high = models.FloatField(verbose_name='最高价',null=True)
    low = models.FloatField(verbose_name='最低价',null=True)
    close = models.FloatField(verbose_name='收盘价',null=True)
    preclose = models.FloatField(verbose_name='昨日收盘价',null=True)
    volume = models.BigIntegerField(verbose_name='成交数量',null=True)
    amount = models.FloatField(verbose_name='成交金额',null=True)
    adjustflag = models.CharField(verbose_name='复权状态',max_length=10,null=True)
    turn = models.FloatField(verbose_name='换手率',null=True)
    tradestatus = models.CharField(verbose_name='交易状态',max_length=10,null=True)
    pctChg = models.FloatField(verbose_name='涨跌幅',null=True)
    isST = models.CharField(verbose_name='是否ST',max_length=10,null=True)
    MA_5 = models.FloatField(verbose_name='MA_5',null=True)
    MA_10 = models.FloatField(verbose_name='MA_10',null=True)
    MA_20 = models.FloatField(verbose_name='MA_20',null=True)
    MA_30 = models.FloatField(verbose_name='MA_30',null=True)
    MA_60 = models.FloatField(verbose_name='MA_60',null=True)
    MA_120 = models.FloatField(verbose_name='MA_120',null=True)
    MA_180 = models.FloatField(verbose_name='MA_180',null=True)
    MA_360 = models.FloatField(verbose_name='MA_360',null=True)
    k = models.FloatField(verbose_name='k',null=True)
    d = models.FloatField(verbose_name='d',null=True)
    j = models.FloatField(verbose_name='j',null=True)


    def __str__(self):
        return self.id
    
    class Meta:
        verbose_name = "股票数据"
        db_table = 'stock_data'

class Strategic_Stock_Selection_Table(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='主键')
    date = models.DateField(verbose_name='日期')
    code = models.CharField(verbose_name='股票代码',max_length=10)
    selection_strategy  = models.CharField(verbose_name='选择策略',max_length=10)

    def __str__(self):
        return self.id
    
    class Meta:
        verbose_name = "策略选股表"
        db_table = 'strategic_stock_selection_table'