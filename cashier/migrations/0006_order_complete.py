# Generated by Django 3.1.7 on 2021-04-02 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0005_auto_20210324_0117'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]
