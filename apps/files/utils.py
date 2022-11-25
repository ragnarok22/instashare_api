import math


def human_file_size(size) -> str:
    i = math.floor(math.log(size) / math.log(1024))
    return "{size:.2f} {unity}".format(
        size=size / math.pow(1024, i), unity=["B", "kB", "MB", "GB", "TB"][i]
    )
