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

    return f"{file_path()}/{instance.name}"


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
