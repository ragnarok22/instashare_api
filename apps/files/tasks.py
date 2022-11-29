import os.path
import zipfile
from time import sleep

import celery

from apps.accounts.models import User
from apps.files.models import File
from apps.files.utils import generate_hash
from django.conf import settings


@celery.shared_task
def compress_all_user_files(user_id):
    files = File.objects.filter(creator_id=user_id)
    creator = User.objects.get(pk=user_id)
    archive = "archive-{creator}-{hash}.zip".format(
        creator=creator.username, hash=generate_hash(creator.id)
    )

    path_to_save = os.path.join(settings.MEDIA_ROOT, archive)

    with zipfile.ZipFile(path_to_save, "w") as zf:
        for file in files:
            zf.write(file.file.path)

    return archive
