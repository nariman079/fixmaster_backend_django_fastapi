# Generated by Django 5.0.6 on 2024-06-09 21:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("src", "0019_remove_customer_user_keyword_customer_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="is_verified",
            field=models.BooleanField(
                default=False, verbose_name="Верифицированный клиент"
            ),
        ),
    ]
