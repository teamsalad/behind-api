import datetime
import os
import tempfile

from nanoid import generate

from django.core.management.base import BaseCommand
from django.core.files import File

from objects.models import Object, TYPE, STATE
from rewards.models import Gifticon


class Command(BaseCommand):
    help = 'Create company names and logos seed'

    def add_arguments(self, parser):
        parser.add_argument('--gifticon-directory', type=str)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting gifticon image upload ...'))
        gifticon_directory_path = options['gifticon_directory']
        with os.scandir(gifticon_directory_path) as gifticon_files:
            for f in gifticon_files:
                with open(f.path, 'rb') as gifticon_file:
                    last_slash = gifticon_file.name.rfind('/')
                    barcode_number = gifticon_file.name[last_slash + 1:].rsplit('.', 1)[0]
                    try:
                        gifticon = Gifticon.objects.get(barcode_number=barcode_number)
                        timestamp = int(datetime.datetime.now().timestamp() * 10 ** 6)
                        file_extension = f.name.rsplit('.', 1)[1].lower()
                        object_name = f"{generate(size=32)}_{str(timestamp)}.{file_extension}"
                        # Create image object instance linked with company
                        if Object.objects.filter(link_alias=f'gifticons/{gifticon.id}/').exists():
                            self.stdout.write(self.style.ERROR(f'{barcode_number} already uploaded.'))
                            continue
                        image_object = Object.objects.create(
                            link_alias=f'gifticons/{gifticon.id}/',
                            name=object_name,
                            type=TYPE[1][0],
                            state=STATE[1][0]
                        )
                        image_object.object.save(object_name, File(gifticon_file))
                    except Gifticon.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f'{barcode_number} does not exist.'))
        self.stdout.write(self.style.SUCCESS('Done'))
