# Generated by Django 4.1.7 on 2023-03-16 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_stock_list_is_cyb_stock_list_is_kcb'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock_list',
            name='k_data_update',
            field=models.DateField(null=True, verbose_name='日线数据更新日期'),
        ),
    ]
