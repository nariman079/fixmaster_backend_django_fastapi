# Generated by Django 5.0.6 on 2024-05-23 13:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("src", "0003_alter_order_customer_notice"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="telegram_id",
            field=models.CharField(max_length=30, verbose_name="ID Телеграм"),
        ),
    ]
