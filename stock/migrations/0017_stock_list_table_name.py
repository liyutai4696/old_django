# Generated by Django 4.1.7 on 2023-03-19 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0016_strategic_stock_selection_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock_list',
            name='table_name',
            field=models.CharField(max_length=10, null=True, verbose_name='表名称'),
        ),
    ]
