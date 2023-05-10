from django.db import models

# Create your models here.

class Agent_Pool(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='序号')
    ip_address = models.CharField(verbose_name='IP',max_length=255)
    ip_port = models.CharField(verbose_name='PORT',max_length=255,null=True)
    nnd = models.CharField(verbose_name='匿名度',max_length=255,null=True)
    lx = models.CharField(verbose_name='类型',max_length=255,null=True)
    wz = models.CharField(verbose_name='位置',max_length=255,null=True)
    xysd = models.CharField(verbose_name='响应速度',max_length=255,null=True)
    yzsj = models.DateTimeField(verbose_name='最后验证时间',max_length=255,null=True)
    fffs = models.CharField(verbose_name='付费方式',max_length=255,null=True)
    is_open = models.BooleanField(verbose_name='使用中',default=False)
    is_ky = models.BooleanField(verbose_name='是否可用',default=True)

    def __str__(self):
        return self.ip_address
    
    class Meta:
        verbose_name = "代理池"
        db_table = 'agent_pool'