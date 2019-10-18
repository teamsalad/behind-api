import datetime
from nanoid import generate


def unique_filename(original_filename):
    """
    Create unique filename
    Nano id(Better uuid) + timestamp + file extension
    :param original_filename: original filename
    :return: uniquely generated filename
    """
    timestamp = int(datetime.datetime.now().timestamp() * 10 ** 6)
    file_extension = original_filename.rsplit('.', 1)[1].lower()
    return f"{generate(size=32)}_{str(timestamp)}.{file_extension}"
