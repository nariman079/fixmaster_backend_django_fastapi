# Generated by Django 5.0.6 on 2024-06-09 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0021_booking_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='name',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Имя пользователя'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='username',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Имя пользователя telegram'),
        ),
    ]