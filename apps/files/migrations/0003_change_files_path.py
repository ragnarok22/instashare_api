import os
from pathlib import Path

from django.conf import settings
from django.db import migrations


def change_path(app, schema_editor):
    FileModel = app.get_model("files", "File")
    base_dir = settings.BASE_DIR / "instashare_api"
    for file in FileModel.objects.all():
        old_path = file.file.path.split(os.sep)
        new_path = base_dir / "instashare_api/media/{creator}/files/{file}".format(
            creator=file.creator.username, file=old_path[-1]
        )

        Path(new_path).parent.mkdir(parents=True, exist_ok=True)
        try:
            os.rename("/".join(old_path), new_path)
        except FileNotFoundError:
            pass
        except OSError:
            pass

        file.file.name = "{creator}/files/{file}".format(
            creator=file.creator.username, file=old_path[-1]
        )
        file.save()


class Migration(migrations.Migration):
    dependencies = [
        ("files", "0002_auto_20221125_1858"),
    ]

    operations = [migrations.RunPython(change_path)]
