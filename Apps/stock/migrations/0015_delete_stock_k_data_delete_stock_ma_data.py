# Generated by Django 4.1.7 on 2023-03-19 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0014_stock_data_d_stock_data_j_stock_data_k'),
    ]

    operations = [
        migrations.DeleteModel(
            name='stock_k_data',
        ),
        migrations.DeleteModel(
            name='stock_MA_data',
        ),
    ]