import codecs
import datetime
import json
import tempfile
import time
from argparse import FileType

import requests
from django.core import files
from django.core.management.base import BaseCommand
from nanoid import generate

from companies.models import Company, Job
from objects.models import Object, TYPE, STATE


class Command(BaseCommand):
    help = 'Create company names and logos seed'

    def add_arguments(self, parser):
        parser.add_argument('--company-list', type=FileType('r'))

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting company seed data creation ...'))
        company_list_json_file = codecs.open(options['company_list'].name, 'r', 'utf-8-sig')
        company_list_json = json.load(company_list_json_file)
        jobs = Job.objects.all()
        for company_object in company_list_json:
            # Create company instance
            company = Company.objects.create(
                name=company_object['name'],
                email_domain='thebehind.com'
            )
            company.jobs.set(jobs)
            company.save()
            # Download image
            request = requests.get(company_object['image_url'].rsplit('?', 1)[0], stream=True)
            if request.status_code != requests.codes.ok:
                self.stdout.write(self.style.ERROR(f"{company_object['name']} Failed."))
                self.stdout.write(self.style.ERROR(f"Image URL: {company_object['image_url']}"))
                continue
            filename = company_object['image_url'].split('/')[-1]
            temp = tempfile.NamedTemporaryFile()
            for block in request.iter_content(1024 * 8):
                if not block:
                    break
                temp.write(block)
            timestamp = int(datetime.datetime.now().timestamp() * 10 ** 6)
            file_extension = filename.rsplit('.', 1)[1].lower().rsplit('?', 1)[0]
            object_name = f"{generate(size=32)}_{str(timestamp)}.{file_extension}"
            # Create image object instance linked with company
            image_object = Object.objects.create(
                link_alias=f'company-logos/{company.id}/',
                name=object_name,
                type=TYPE[0][0],
                state=STATE[1][0]
            )
            image_object.object.save(object_name, files.File(temp))
            time.sleep(3)
            self.stdout.write(self.style.SUCCESS(f'Company: {company.id} {company.name}'))
        self.stdout.write(self.style.SUCCESS('Done'))
