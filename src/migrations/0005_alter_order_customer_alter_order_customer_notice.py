# Generated by Django 5.0.6 on 2024-05-23 19:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("src", "0004_alter_customer_telegram_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="customer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="src.customer",
                verbose_name="Клиент",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="customer_notice",
            field=models.CharField(
                default="0", max_length=120, verbose_name="Коментарий"
            ),
        ),
    ]
