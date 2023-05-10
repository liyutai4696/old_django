# Generated by Django 4.1.7 on 2023-05-10 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agent_Pool',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='序号')),
                ('ip_address', models.CharField(max_length=255, verbose_name='IP')),
                ('id_port', models.CharField(max_length=255, null=True, verbose_name='PORT')),
                ('nnd', models.CharField(max_length=255, null=True, verbose_name='匿名度')),
                ('lx', models.CharField(max_length=255, null=True, verbose_name='类型')),
                ('wz', models.CharField(max_length=255, null=True, verbose_name='位置')),
                ('xysd', models.CharField(max_length=255, null=True, verbose_name='响应速度')),
                ('yzsj', models.DateTimeField(max_length=255, null=True, verbose_name='最后验证时间')),
                ('fffs', models.CharField(max_length=255, null=True, verbose_name='付费方式')),
                ('is_ky', models.BooleanField(null=True, verbose_name='是否可用')),
            ],
            options={
                'verbose_name': '代理池',
                'db_table': 'agent_pool',
            },
        ),
    ]
