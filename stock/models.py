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