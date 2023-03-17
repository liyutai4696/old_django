from django.db import models

# Create your models here.

class stock_list(models.Model):
    code = models.CharField(primary_key=True,verbose_name='股票代码',max_length=10)
    code_name = models.CharField(verbose_name='股票名称',max_length=10)
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

class stock_k_data(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='主键')
    date = models.DateField(verbose_name='日期')
    code = models.CharField(verbose_name='股票代码',max_length=10)
    open = models.FloatField(verbose_name='开盘价')
    high = models.FloatField(verbose_name='最高价')
    low = models.FloatField(verbose_name='最低价')
    close = models.FloatField(verbose_name='收盘价')
    preclose = models.FloatField(verbose_name='昨日收盘价')
    volume = models.IntegerField(verbose_name='成交数量')
    amount = models.FloatField(verbose_name='成交金额')
    adjustflag = models.CharField(verbose_name='复权状态',max_length=10)
    turn = models.FloatField(verbose_name='换手率')
    tradestatus = models.CharField(verbose_name='交易状态',max_length=10)
    pctChg = models.FloatField(verbose_name='涨跌幅')
    isST = models.CharField(verbose_name='是否ST',max_length=10)

    def __str__(self):
        return self.id
    
    class Meta:
        verbose_name = "K线数据"
        db_table = 'stock_k_data'