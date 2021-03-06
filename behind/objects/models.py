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


def storage_path(instance, filename):
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
    object = models.FileField(upload_to=storage_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Object {TYPE[self.type - 1][1]} {STATE[self.state - 1][1]}'

    class Meta:
        db_table = 'objects'
