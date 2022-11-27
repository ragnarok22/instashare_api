from django.contrib.auth.hashers import make_password
from django.db import migrations


def create_superuser(apps, schema_editor):
    # noinspection PyPep8Naming
    User = apps.get_model("accounts", "User")

    user_admin, is_new = User.objects.get_or_create(username="admin")
    if is_new:
        user_admin.first_name = "Admin"
        user_admin.last_name = "User"
        user_admin.email = "admin@example.com"
        user_admin.is_superuser = True
        user_admin.is_staff = True
        user_admin.password = make_password("admin1")
        user_admin.save()


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [migrations.RunPython(create_superuser)]
