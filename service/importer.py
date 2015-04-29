from octopus.core import app
from service.sheets import APCSheet
from service.institutional import Sheet2Institutional
from service.publishers import PUBLISHER_NAME_MAP
from datetime import datetime

def do_import(csv_path, institution=None):
    app.logger.info("Importing for institution {x}".format(x=institution))
    sheet = APCSheet(csv_path)
    count = 0
    for obj in sheet.objects():
        if institution is not None:
            obj["institution"] = institution
        ir = Sheet2Institutional.sheet2institutional(obj)

        # normalise the publisher name on the way in
        pub = ir.monitor.publisher
        if pub is not None:
            ir.monitor.publisher = PUBLISHER_NAME_MAP.get(ir.monitor.publisher, ir.monitor.publisher)

        ir.last_upload = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        ir.upload_source = "Spreadsheet: " + sheet.filename()

        ir.save()
        count += 1
    app.logger.info("{x} records imported for {y}".format(x=count, y=institution))