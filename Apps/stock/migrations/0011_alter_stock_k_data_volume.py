# Generated by Django 4.1.7 on 2023-03-19 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0010_alter_stock_k_data_adjustflag_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock_k_data',
            name='volume',
            field=models.BigIntegerField(null=True, verbose_name='成交数量'),
        ),
    ]