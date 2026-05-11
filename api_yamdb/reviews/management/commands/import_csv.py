import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import (
    Category, Comment, Genre, Review, Title
)
from users.models import User


FILE_ORDER = [
    'users.csv',
    'category.csv',
    'genre.csv',
    'titles.csv',
    'review.csv',
    'comments.csv',
]


class Command(BaseCommand):
    """Команда для импорта данных из CSV-файлов в базу данных."""

    help = 'Загружает данные из CSV-файлов в базу данных.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            default=str(settings.BASE_DIR / 'static' / 'data'),
            help='Путь к директории с CSV-файлами',
        )

    def handle(self, *args, **options):
        path = Path(options['path'])
        self.stdout.write(f'Ищу CSV в: {path}')
        if not path.is_dir():
            self.stdout.write(
                self.style.ERROR(f'Директория {path} не найдена.')
            )
            return
        for filename in FILE_ORDER:
            filepath = path / filename
            if not filepath.is_file():
                self.stdout.write(
                    self.style.WARNING(f'Файл {filepath} не найден, пропускаем.')
                )
                continue
            model = self.get_model_for_file(filename)
            if not model:
                self.stdout.write(
                    self.style.ERROR(f'Нет модели для файла {filename}.')
                )
                continue
            self.process_file(filepath, model, filename)
        self.process_genre_relations(path)
        self.stdout.write(self.style.SUCCESS('Импорт завершён.'))

    @staticmethod
    def get_model_for_file(filename):
        """Возвращает модель, соответствующую CSV-файлу."""
        mapping = {
            'users.csv': User,
            'category.csv': Category,
            'genre.csv': Genre,
            'titles.csv': Title,
            'review.csv': Review,
            'comments.csv': Comment,
        }
        return mapping.get(filename)

    def process_file(self, filepath, model, filename):
        """Читает CSV и создаёт объекты модели."""
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            objs = []
            for row in reader:
                if not any(row.values()):
                    continue
                prepared = self.prepare_row(row, filename)
                objs.append(model(**prepared))
            model.objects.bulk_create(objs, ignore_conflicts=True)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Успешно загружено {len(objs)} записей из {filename}'
                )
            )

    def prepare_row(self, row, filename):
        """Приводит имена полей CSV к ожидаемым в модели."""
        mapping = {
            'users.csv': {
                'username': 'username',
                'email': 'email',
                'role': 'role',
                'first_name': 'first_name',
                'last_name': 'last_name',
                'bio': 'bio',
            },
            'category.csv': {
                'name': 'name',
                'slug': 'slug',
            },
            'genre.csv': {
                'name': 'name',
                'slug': 'slug',
            },
            'titles.csv': {
                'name': 'name',
                'year': 'year',
                'category': 'category_id',
            },
            'review.csv': {
                'title': 'title_id',
                'text': 'text',
                'author': 'author_id',
                'score': 'score',
                'pub_date': 'pub_date',
            },
            'comments.csv': {
                'review': 'review_id',
                'text': 'text',
                'author': 'author_id',
                'pub_date': 'pub_date',
            },
        }
        field_map = mapping.get(filename, {})
        prepared = {}
        for csv_key, model_key in field_map.items():
            if csv_key in row:
                prepared[model_key] = row[csv_key]
        if filename == 'titles.csv' and 'description' in row:
            prepared['description'] = row['description']
        return prepared

    def process_genre_relations(self, path):
        """Устанавливает связи many-to-many для произведений и жанров."""
        filepath = path / 'titles.csv'
        if not filepath.is_file():
            return
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not any(row.values()):
                    continue
                title_id = row.get('id')
                genre_field = row.get('genre', '')
                if not title_id or not genre_field:
                    continue
                try:
                    title = Title.objects.get(pk=title_id)
                except Title.DoesNotExist:
                    continue
                genre_ids = [
                    int(g.strip())
                    for g in genre_field.split(',')
                    if g.strip()
                ]
                genres = Genre.objects.filter(pk__in=genre_ids)
                title.genre.set(genres)
        self.stdout.write(
            self.style.SUCCESS('Связи "произведение-жанр" обновлены.')
        )
