import os

from django.db import migrations
from django.contrib.auth import get_user_model

from src.models.organization_models import OrganizationType, Organization


def create_superuser(apps, schema_editor):
    User = get_user_model()
    user_password = os.getenv("ROOT_USER_PASSWORD")
    if not User.objects.filter(username="root").exists():
        User.objects.create_superuser(username="root", password=user_password)
    org_type = OrganizationType.objects.create(title="Салон красоты")
    _ = Organization.objects.create(
        title="title",
        telegram_id="default",
        address="address",
        contact_phone="92323923",
        time_begin="12:00:00",
        time_end="12:00:00",
        work_schedule="12-19",
        organization_type=org_type,
    )


# def remove_superuser(apps, schema_editor):
#     User = get_user_model()
#     User.objects.filter(username='admin').delete()


class Migration(migrations.Migration):
    dependencies = [
        ("src", "0029_order_create_at"),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
