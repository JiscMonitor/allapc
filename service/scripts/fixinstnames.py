from service import models

NAME_MAP = {
    "Univer\nsity of Manchester" : "University of Manchester",
    "Unive\nrsity of Southampton" : "University of Southampton",
    "Univers\nity of Edinburgh" : "University of Edinburgh",
    "Universit\ny of Bristol" : "University of Bristol",
    "University \nof Leeds" : "University of Leeds",
    "Queen\ns University Belfast" : "Queens University Belfast",
    "Univer\nsity of St Andrews" : "University of St Andrews",
    "Durham Univer\nsity" : "Durham University",
    "Swansea Univ\nersity" : "Swansea University",
    "Lancaster \nUniversity" : "Lancaster University",
}

for ir in models.InstitutionalRecord.scroll():
    m = ir.monitor
    inst = m.has_apcs_for()[0]
    if inst in NAME_MAP:
        nn = NAME_MAP.get(inst)
        apc = m.apc_for(inst)
        apc.name = nn
        ir.save()
