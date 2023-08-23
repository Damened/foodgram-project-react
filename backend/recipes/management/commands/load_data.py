import csv
import os
from time import sleep

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient

DATA_ROOT = os.path.join(settings.BASE_DIR, "data/ingredients.csv")


class Command(BaseCommand):
    """Загрузка ингредиентов в базу данных"""

    def handle(self, *args, **options):
        with open(os.path.join(DATA_ROOT), "r", encoding="utf-8") as file:
            file_reader = csv.reader(file)
            total_rows = sum(1 for _ in file_reader)
            file.seek(0)

            ingredients = [
                Ingredient(
                    name=row[0], measurement_unit=row[1])for row in file_reader
            ]

            for i, _ in enumerate(ingredients, 1):
                progress = int(i / total_rows * 100)
                self.update_progress(progress)

        Ingredient.objects.bulk_create(ingredients)

        self.stdout.write(
            self.style.SUCCESS("=== Данные успешно загружены ==="))

    def update_progress(self, progress):
        width = 30
        left = width * progress // 100
        right = width - left
        print(
            "\r[",
            "#" * left,
            " " * right,
            "]",
            f" {progress:.0f}%",
            sep="",
            end="",
            flush=True,
        )
        sleep(0.1)
