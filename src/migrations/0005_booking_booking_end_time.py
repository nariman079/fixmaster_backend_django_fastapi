# Generated by Django 4.2.6 on 2024-05-16 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0004_remove_order_master'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booking_end_time',
            field=models.IntegerField(blank=True, editable=False, null=True, verbose_name='Длительность процедуры'),
        ),
    ]
