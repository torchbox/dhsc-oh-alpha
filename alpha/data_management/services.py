import csv
from tempfile import NamedTemporaryFile

from django.core.exceptions import ValidationError


def parse_csv(file):
    # Read the file in memory for now
    # TODO consider large files, might be worth using pandas

    with NamedTemporaryFile(mode="w+b") as temp:
        temp.write(file.read())
        temp.seek(0)
        with open(temp.name, "rt", encoding="utf-8-sig") as file:
            reader = csv.reader(file, delimiter=",")
            for index, row in enumerate(reader):
                # TODO - put in place some validation use cases to raise
                if row:
                    raise ValidationError(
                        "There was a problem with your CSV file...",
                    )
