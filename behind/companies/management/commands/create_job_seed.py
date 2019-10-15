from django.core.management.base import BaseCommand

from companies.models import Job


class Command(BaseCommand):
    help = 'Create company names and logos seed'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting job seed data creation ...'))
        job_titles = [
            '개발, 데이터', '비즈니스, 기획', '마케팅, 광고',
            '디자인', '영업', '고객서비스, 리테일',
            '인사, 교육', '미디어', '게임 제작',
            '투자, 분석', '엔지니어링, 설계', '제조, 생산',
            '법률', '의료, 제약', '물류, 운송', '건설, 시설',
            '정부, 공무원',
        ]
        jobs = Job.objects.bulk_create([Job(title=title) for title in job_titles])
        for job in jobs:
            self.stdout.write(self.style.SUCCESS(f'Job: {job.title}'))
        self.stdout.write(self.style.SUCCESS('Done'))
