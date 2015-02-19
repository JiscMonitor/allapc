from octopus.core import app
from service.sheets import APCSheet
from service.institutional import Sheet2Institutional

def do_import(csv_path, institution=None):
    app.logger.info("Importing for institution {x}".format(x=institution))
    sheet = APCSheet(csv_path)
    count = 0
    for obj in sheet.objects():
        if institution is not None:
            obj["institution"] = institution
        ir = Sheet2Institutional.sheet2institutional(obj)
        ir.save()
        count += 1
    app.logger.info("{x} records imported for {y}".format(x=count, y=institution))