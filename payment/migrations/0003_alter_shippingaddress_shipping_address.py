# Generated by Django 5.1.4 on 2024-12-18 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_rename_shipping_address1_shippingaddress_shipping_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='shipping_address',
            field=models.TextField(),
        ),
    ]
