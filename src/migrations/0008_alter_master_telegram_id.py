# Generated by Django 5.0.6 on 2024-05-23 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0007_alter_customer_telegram_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='master',
            name='telegram_id',
            field=models.CharField(default='web_user', max_length=30, verbose_name='ID Телеграм'),
        ),
    ]