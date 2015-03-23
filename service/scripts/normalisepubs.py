from service.models import InstitutionalRecord
from service.publishers import PUBLISHER_NAME_MAP

for ir in InstitutionalRecord.scroll():
    current = ir.monitor.publisher
    if current is not None:
        updated = PUBLISHER_NAME_MAP.get(current)
        if updated is not None and updated != current:
            print "Normalised ", current, "to", updated
            ir.monitor.publisher = updated
            ir.save()
        else:
            print "No normalisation available/required for", current
