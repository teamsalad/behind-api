import datetime

from nanoid import generate

from django.db import models

STATE = (
    (1, 'staging'),
    (2, 'aliased'),
    (3, 'unaliased'),
)
TYPE = (
    (1, 'company'),
    (2, 'gifticon'),
)


def unique_filename(instance, filename):
    def file_path():
        paths = {
            'company': 'company-logos',
            'gifticon': 'gifticons'
        }
        return paths[TYPE[instance.type - 1][1]]

    # Nano id(Better uuid) + timestamp + file extension
    timestamp = int(datetime.datetime.now().timestamp() * 10 ** 6)
    file_extension = filename.rsplit('.', 1)[1].lower()
    name = f"{file_path()}/{generate(size=32)}_{str(timestamp)}.{file_extension}"
    instance.name = name
    instance.link_alias = name
    return name


class Object(models.Model):
    link_alias = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    type = models.PositiveSmallIntegerField(
        choices=TYPE)
    state = models.PositiveSmallIntegerField(
        choices=STATE,
        default=STATE[0][0]
    )
    object = models.FileField(upload_to=unique_filename)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'objects'
