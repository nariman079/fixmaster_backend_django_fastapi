# Generated by Django 5.0.6 on 2024-05-30 18:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("src", "0008_alter_master_telegram_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="master",
            name="code",
            field=models.IntegerField(
                default=31011, max_length=255, verbose_name="Слово пароль"
            ),
        ),
    ]
