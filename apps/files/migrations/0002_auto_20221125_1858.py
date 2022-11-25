# Generated by Django 3.2.16 on 2022-11-25 18:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("files", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="file",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="file",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
