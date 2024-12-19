# Generated by Django 5.1.4 on 2024-12-18 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='shipping_address1',
            new_name='shipping_address',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='shipping_address2',
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.TextField(),
        ),
    ]
