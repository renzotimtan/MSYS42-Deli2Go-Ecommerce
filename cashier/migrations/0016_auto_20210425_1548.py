# Generated by Django 3.1.7 on 2021-04-25 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0015_auto_20210424_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='home_phone',
            field=models.CharField(blank=True, max_length=8),
        ),
    ]
