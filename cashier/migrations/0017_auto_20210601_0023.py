# Generated by Django 3.1.7 on 2021-05-31 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0016_auto_20210425_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='overall_total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='home_phone',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]