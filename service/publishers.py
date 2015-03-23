from octopus.core import app
from octopus.lib import clcsv

import csv

tsv = app.config.get("UNIQUE_PUBLISHER_MAPPING")
print tsv
sheet = clcsv.ClCsv(file_path=tsv, input_dialect=csv.excel_tab)

PUBLISHER_NAME_MAP = {}
for o in sheet.objects():
    orig = o.get("Original Publisher")
    clean = o.get("Cleaned Publisher")
    PUBLISHER_NAME_MAP[orig] = clean
