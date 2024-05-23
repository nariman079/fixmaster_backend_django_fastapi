# Generated by Django 5.0.6 on 2024-05-22 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='addidional_info',
            new_name='additional_info',
        ),
        migrations.AddField(
            model_name='customer',
            name='user_keyword',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Слово пароль'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='Номер телефона'),
        ),
    ]