import csv, codecs
from service import models
from datetime import datetime

class Row2InstitutionalXwalk(object):
    @classmethod
    def row2institutional(cls, row):
        # 0 = Institution
        # 1 = Date of initial application by author
        # 2 = Submitted by
        # 3 = University department
        # 4 = PubMed Central (PMC) ID
        # 5 = PubMed ID
        # 6 = DOI
        # 7 = Affiliated author
        # 8 = Publisher
        # 9 = Journal
        # 10 = ISSN
        # 11 = Type of publication
        # 12 = Article title
        # 13 = Date of publication
        # 14 = Fund that APC is paid from (1)
        # 15 = Fund that APC is paid from (2)
        # 16 = Fund that APC is paid from (3)
        # 17 = Funder of research (1)
        # 18 = Funder of research (2)
        # 19 = Funder of research (3)
        # 20 = Grant number (1)
        # 21 = Grant number (2)
        # 22 = Grant number (3)
        # 23 = Date of APC payment
        # 24 = APC paid (actual currency) including VAT if charged
        # 25 = Currency of APC
        # 26 = APC paid (GBP) including VAT if charged
        # 27 = Additional costs (GBP)
        # 28 = Discounts, memberships & pre-payment agreements
        # 29 = Amount of APC charged to COAF grant (include VAT if charged) in GBP
        # 30 = Licence
        # 31 = Correct license applied?
        # 32 = Problem-free open access publication?
        # 33 = Notes

        # make the core objects we are building
        ir = models.InstitutionalRecord()
        monitor = ir.monitor
        apc = monitor.apc_for(row[0])

        # now xwalk all the values
        if cls._importable(row[1]): monitor.date_applied = cls._norm(row[1])
        if cls._importable(row[4]): monitor.pmcid = cls._norm(row[4])
        if cls._importable(row[5]): monitor.pmid = cls._norm(row[5])
        if cls._importable(row[6]): monitor.doi = cls._norm(row[6])
        if cls._importable(row[7]): monitor.add_author(cls._norm(row[7]))
        if cls._importable(row[8]): monitor.publisher = cls._norm(row[8])
        if cls._importable(row[9]): monitor.source = cls._norm(row[9])
        if cls._importable(row[10]): monitor.issn = cls._norm(row[10])
        if cls._importable(row[11]): monitor.publication_type = cls._norm(row[11])
        if cls._importable(row[12]): monitor.title = cls._norm(row[12])
        if cls._importable(row[13]): monitor.publication_date = cls._norm(row[13])

        if cls._importable(row[14]): apc.add_fund(cls._norm(row[14]))
        if cls._importable(row[15]): apc.add_fund(cls._norm(row[15]))
        if cls._importable(row[16]): apc.add_fund(cls._norm(row[16]))

        if cls._importable(row[17]):
            fs = cls._separate(row[17])
            for funder in fs:
                if cls._importable(row[20]):
                    monitor.add_funder(funder, cls._norm(row[20]))
                else:
                    monitor.add_funder(funder)
        if cls._importable(row[18]):
            fs = cls._separate(row[18])
            for funder in fs:
                if cls._importable(row[21]): monitor.add_funder(funder, cls._norm(row[21]))
                else: monitor.add_funder(funder)
        if cls._importable(row[19]):
            fs = cls._separate(row[19])
            for funder in fs:
                if cls._importable(row[22]): monitor.add_funder(funder, cls._norm(row[22]))
                else: monitor.add_funder(funder)

        if cls._importable(row[23]): apc.date_paid = cls._norm(row[23])
        if cls._importable(row[24]) and cls._float(row[24]) is not None: apc.amount = cls._float(row[24])
        if cls._importable(row[25]): apc.currency = cls._norm(row[25])
        if cls._importable(row[26]) and cls._float(row[26]) is not None: apc.amount_gbp = cls._float(row[26])
        if cls._importable(row[27]) and cls._float(row[27]) is not None: apc.additional_costs = cls._float(row[27])
        if cls._importable(row[28]): apc.add_discount(cls._norm(row[28]))

        if cls._importable(row[29]) and cls._float(row[29]) is not None: apc.add_fund("COAF", amount_gbp=cls._float(row[29]))

        if cls._importable(row[30]): monitor.set_license(cls._norm(row[30]))
        if cls._importable(row[31]):
            if cls._importable(row[13]):
                monitor.license_received(cls._norm(row[13]), cls._norm(row[31]))
            else:
                dt = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                monitor.license_received(cls._norm(dt), cls._norm(row[31]))

        if cls._importable(row[32]): apc.publication_process_feedback = cls._norm(row[32])
        if cls._importable(row[33]): apc.notes = cls._norm(row[33])

        return ir

    @classmethod
    def _separate(cls, val):
        f = cls._norm(val)
        if "," in f:
            fs = [x.strip() for x in f.split(",")]
            return fs
        elif ";" in f:
            fs = [x.strip() for x in f.split(";")]
            return fs
        return [f]


    @classmethod
    def _importable(cls, val):
        return val is not None and val != ""

    @classmethod
    def _norm(cls, val):
        return val.decode("utf-8", errors="ignore").strip()

    @classmethod
    def _float(cls, val):
        try:
            return float(cls._norm(val))
        except:
            return None

def import_csv(path, institution=None):
    with codecs.open(path, "r") as f:
        reader = csv.reader(f)
        first = True
        for row in reader:
            if first:
                first = False
                continue
            if len(row) == 33:
                row = [""] + row
            if institution is not None:
                row[0] = institution
            ir = Row2InstitutionalXwalk.row2institutional(row)
            ir.save()

from service.sheets import APCSheet
from service.institutional import Sheet2Institutional

def do_import(csv_path, institution=None):
    sheet = APCSheet(csv_path)
    for obj in sheet.objects():
        if institution is not None:
            obj["institution"] = institution
            ir = Sheet2Institutional.sheet2institutional(obj)
            ir.save()