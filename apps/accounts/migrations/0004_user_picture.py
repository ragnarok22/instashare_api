# Generated by Django 3.2.16 on 2022-11-30 21:02

import apps.accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_auto_20221128_2003"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="picture",
            field=models.ImageField(
                blank=True, null=True, upload_to=apps.accounts.models.upload_to
            ),
        ),
    ]
