# Generated by Django 5.0.6 on 2024-06-07 11:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("src", "0016_customer_master_alter_master_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="booking_end_time",
            field=models.TimeField(verbose_name="Длительность процедуры"),
        ),
    ]
