import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from alpha.providers.models import Provider


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        self.data_path = Path(settings.PROJECT_DIR) / "providers" / "data"
        super().__init__(*args, **kwargs)

    @transaction.atomic
    def handle(self, **options):
        self.stdout.write("Importing fake providers data...")

        Provider.objects.all().delete()

        with open(self.data_path / "fake_providers.csv") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                covers_england = True if row["england"] else None
                Provider.objects.create(
                    name=row["name"],
                    address=row["address"],
                    covers_england=covers_england,
                )

        self.stdout.write("...Done")
