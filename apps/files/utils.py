import hashlib
import math

from django.utils.timezone import now


def human_file_size(size) -> str:
    i = math.floor(math.log(size) / math.log(1024))
    return "{size:.2f} {unity}".format(
        size=size / math.pow(1024, i), unity=["B", "kB", "MB", "GB", "TB"][i]
    )


def generate_hash(id_number):
    number = hashlib.sha256(
        str(str(now()) + str(id_number)).encode("utf-8")
    ).hexdigest()[:10]
    return number
