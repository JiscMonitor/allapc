from octopus.modules.sherpafact import client
from service import models
import time

fc = client.FactClient()

JULIET_MAP = {
    14 : ["Arthritis Research UK"],
    698 : ["Arts and Humanities Research Council (AHRC)", "AHRC"],
    709 : ["Biotechnology and Biological Sciences Research Council (BBSRC)", "BBSRC", "BBRSC"],
    873 : ["Breast Cancer Campaign"],
    18 : ["British Heart Foundation"],
    19 : ["Cancer Research UK"],
    717 : ["Economic and Social Research Council (ESRC)", "ESRC"],
    722 : ["Engineering and Physical Sciences Research Council (EPSRC)", "EPSRC", "ESPRC"],
    925 : ["Leukaemia & Lymphoma Research"],
    705 : ["Medical Research Council (MRC)", "MRC"],
    726 : ["Natural Environment Research Council (NERC)", "NERC"],
    716 : ["Science and Technology Facilities Council (STFC)", "STFC", "STRC"],
    695 : ["Wellcome Trust"]
}

JULIET_LOOKUP = {}
for k, vs in JULIET_MAP.iteritems():
    for v in vs:
        JULIET_LOOKUP[v.lower().strip()] = k

def get_juliet_ids(funder_names):
    jids = []
    for fn in funder_names:
        jid = JULIET_LOOKUP.get(fn.lower().strip())
        if jid is not None:
            jids.append(jid)
    return jids

throttle = 2
report = {
    "errors" : 0,
    "saved" : 0,
    "skipped" : 0,
    "nomatch" : 0,
    "nofunder" : 0
}
i = 0
for ir in models.InstitutionalRecord.scroll(keepalive="5m", page_size=100, limit=10):
    i += 1

    # get the fields to use
    funder_names = [f.get("name") for f in ir.monitor.funder if f.get("name") is not None]
    journal_title = ir.monitor.source

    if len(funder_names) == 0 or journal_title is None or journal_title == "":
        print i, "skipping", ir.id
        report["skipped"] += 1
        continue

    # prep the fields to use
    jids = get_juliet_ids(funder_names)
    jt = journal_title.strip()

    if len(jids) == 0:
        print i, "no recognised funder", ir.id
        report["nofunder"] += 1
        continue

    print i, "requesting", ir.id
    try:
        facts = fc.query(jids, journal_title=jt)
    except:
        print i, "exception processing", ir.id
        report["errors"] += 1
        continue

    if facts.result_count != 1:
        print i, "not exactly 1 result for", ir.id
        report["nomatch"] += 1
        continue

    print i, "saving", ir.id
    report["saved"] += 1
    ir.green_option = facts.green_compliance
    ir.save()

    # sleep for a bit, so as not to overload fact
    time.sleep(throttle)

print report