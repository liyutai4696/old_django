# Generated by Django 4.1.7 on 2023-03-19 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0013_stock_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock_data',
            name='d',
            field=models.FloatField(null=True, verbose_name='d'),
        ),
        migrations.AddField(
            model_name='stock_data',
            name='j',
            field=models.FloatField(null=True, verbose_name='j'),
        ),
        migrations.AddField(
            model_name='stock_data',
            name='k',
            field=models.FloatField(null=True, verbose_name='k'),
        ),
    ]