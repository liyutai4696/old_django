from django.db import models

# Create your models here.

class ymx_url_list(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='序号')
    category = models.CharField(verbose_name='类目名称',max_length=255)
    url_address = models.CharField(verbose_name='链接地址',max_length=255,null=True)
    is_execute = models.BooleanField(verbose_name='执行中',default=False,null=True)
    is_complete = models.BooleanField(verbose_name='已执行',default=False,null=True)

    def __str__(self):
        return self.category
    
    class Meta:
        verbose_name = "亚马逊链接列表"
        db_table = 'ymx_ljlb'

class Amazon_Best_Sellers(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='序号')
    category = models.CharField(verbose_name='类目名称',max_length=255)
    product_title = models.TextField(verbose_name='商品标题',null=True)
    rank = models.IntegerField(verbose_name='排名',null=True)
    ASIN = models.CharField(verbose_name='ASIN',max_length=255,null=True)
    brand = models.CharField(verbose_name='品牌',max_length=255,null=True)
    days30_parent = models.CharField(verbose_name='近30天销量(父体)',max_length=255,null=True)
    score = models.IntegerField(verbose_name='评分',null=True)
    score_count = models.IntegerField(verbose_name='评分数',null=True)
    lsting_time = models.DateField(verbose_name='上架时间',null=True)
    selling_price = models.FloatField(verbose_name='销售价格($)',null=True)

    def __str__(self):
        return self.product_title
    
    class Meta:
        verbose_name = "亚马逊销量排行榜"
        db_table = 'amazon_best_sellers'