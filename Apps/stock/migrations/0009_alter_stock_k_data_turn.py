# Generated by Django 4.1.7 on 2023-03-19 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0008_rename_stock_code_stock_list_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock_k_data',
            name='turn',
            field=models.FloatField(null=True, verbose_name='换手率'),
        ),
    ]
