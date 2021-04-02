# Generated by Django 3.1.7 on 2021-04-02 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0006_order_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_fee',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Order Sent', 'Order Sent'), ('Order Confirmed', 'Order Confirmed'), ('Payment Sent', 'Payment Sent'), ('Payment Confirmed', 'Payment Confirmed'), ('Ready for Pickup', 'Ready for Pickup'), ('To Be Delivered', 'To Be Delivered'), ('Order On The Way', 'Order On The Way'), ('Delivered', 'Delivered')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('GCash', 'GCash'), ('Cash On Delivery', 'Cash On Delivery'), ('Cash On Pickup', 'Cash On Pickup')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='receive_date',
            field=models.DateTimeField(null=True),
        ),
    ]
