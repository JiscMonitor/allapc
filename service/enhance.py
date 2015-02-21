from octopus.modules.sherpafact import client as sfact
from octopus.modules.doaj import client as doaj
from service import models
import time

THROTTLE = 1

def do_enhance():
    report = {
        "fact": {
            "errors" : 0,
            "saved" : 0,
            "skipped" : 0,
            "nomatch" : 0,
            "nofunder" : 0,
            "unnecessary" : 0
        },
        "doaj" : {
            "errors" : 0,
            "skipped" : 0,
            "unnecessary" : 0
        }
    }

    for ir in models.InstitutionalRecord.scroll(keepalive="100m", page_size=100):
        enhance(ir, report)
        time.sleep(THROTTLE)

    print report

def enhance(ir, report):
    facted = do_fact(ir, report["fact"])
    doajd = do_doaj(ir, report["doaj"])
    if facted or doajd:
        ir.save()

##############################################################
# fact lookup stuff

fc = sfact.FactClient()

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

def do_fact(ir, report):
    if ir.green_option is not None and ir.green_option != "":
        print "unnecessary, already done", ir.id
        report["unnecessary"] += 1
        return False

    # get the fields to use
    funder_names = [f.get("name") for f in ir.monitor.funder if f.get("name") is not None]
    journal_title = ir.monitor.source

    if len(funder_names) == 0 or journal_title is None or journal_title == "":
        print "skipping", ir.id
        report["skipped"] += 1
        return False

    # prep the fields to use
    jids = get_juliet_ids(funder_names)
    jt = journal_title.strip()

    if len(jids) == 0:
        print "no recognised funder", ir.id
        report["nofunder"] += 1
        return False

    print "requesting", ir.id
    try:
        facts = fc.query(jids, journal_title=jt)
    except:
        print "exception processing", ir.id
        report["errors"] += 1
        return False

    if facts.result_count != 1:
        print "not exactly 1 result for", ir.id
        report["nomatch"] += 1
        return False

    print "recording", ir.id
    report["saved"] += 1
    ir.green_option = facts.green_compliance

    return True

##############################################################
# doaj lookup stuff

dc = doaj.DOAJSearchClient()

def do_doaj(ir, report):
    if ir.journal_type is not None:
        print "unnecessary, already done", ir.id
        report["unnecessary"] += 1
        return False

    issn = ir.monitor.issn
    if issn is None:
        print "no issn, skipping", ir.id
        report["skipped"] += 1
        return False

    journals = dc.journals_by_issns(issn)
    if journals is None:
        print "error from DOAJ", ir.id
        report["errors"] += 1
        return False

    if len(journals) == 0:
        ir.journal_type = "hybrid"
    else:
        ir.journal_type = "oa"

    return True

