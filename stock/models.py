from django.db import models

# Create your models here.

class stock_list(models.Model):
    stock_code = models.CharField(verbose_name='股票代码',max_length=10)
    stock_name = models.CharField(verbose_name='股票名称',max_length=10)
    stock_industry = models.CharField(verbose_name='行业类别',max_length=8)
    stock_industryClassification = models.CharField(verbose_name='行业分类',max_length=24)
    is_kcb = models.BooleanField(verbose_name='是否科创板',default=False)
    is_cyb = models.BooleanField(verbose_name='是否创业板',default=False)
    update = models.DateField(verbose_name='更新日期')
    k_data_update = models.DateField(verbose_name='日线数据更新日期',null=True)

    def __str__(self):
        return self.stock_code
    
    class Meta:
        verbose_name = "股票列表"
        db_table = 'stock_list'