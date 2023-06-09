# Generated by Django 4.1.7 on 2023-03-16 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='stock_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_code', models.CharField(max_length=10, verbose_name='股票代码')),
                ('stock_name', models.CharField(max_length=10, verbose_name='股票名称')),
                ('stock_industry', models.CharField(max_length=8, verbose_name='行业类别')),
                ('stock_industryClassification', models.CharField(max_length=24, verbose_name='行业分类')),
                ('update', models.DateField(verbose_name='更新日期')),
            ],
            options={
                'verbose_name': '股票列表',
                'db_table': 'stock_list',
            },
        ),
    ]
