import csv

from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, Title
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Load data from CSV files'

    def handle(self, *args, **options):
        base_path = 'static/data/'
        files = {
            'category.csv': Category,
            'genre.csv': Genre,
            'titles.csv': Title,
        }
        self.load_model_from_csv(base_path + 'category.csv', Category, ['id', 'name', 'slug'])
        self.load_model_from_csv(base_path + 'genre.csv', Genre, ['id', 'name', 'slug'])

    def load_model_from_csv(self, filename, model, fieldnames):
        try:
            with open(filename, encoding='utf-8') as f:
                reader = csv.DictReader(f, fieldnames=fieldnames)
                next(reader, None)
                for row in reader:
                    if not row.get('name'):
                        continue
                    obj, created = model.objects.get_or_create(
                        defaults=row,
                        **{field: row[field] for field in row if field != 'id'}
                    )
                    if created:
                        self.stdout.write(f'Created {model.__name__} {obj}')
        except FileNotFoundError:
            self.stdout.write(f'File {filename} not found')
