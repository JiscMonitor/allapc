from service import models

class Sheet2Institutional(object):

    @classmethod
    def sheet2institutional(cls, sheet_obj):
        # construct the core objects
        ir = models.InstitutionalRecord()
        monitor = ir.monitor
        apc = monitor.apc_for(sheet_obj.get("institution"))

        # now crosswalk all the values
        apc.additional_costs = sheet_obj.get("additional_costs")
        monitor.add_author(sheet_obj.get("affiliated_author"))

        if sheet_obj.get("amount") is None and sheet_obj.get("amount_gbp") is not None:
            apc.amount = sheet_obj.get("amount_gbp")
            apc.currency = "GBP"
        else:
            apc.amount = sheet_obj.get("amount")
            apc.currency = sheet_obj.get("currency")

        apc.amount_gbp = sheet_obj.get("amount_gbp")
        apc.date_paid = sheet_obj.get("apc_payment_date")

        if sheet_obj.get("coaf") is not None:
            apc.add_fund("COAF", amount_gbp=sheet_obj.get("coaf"))

        apc.add_discount(sheet_obj.get("discounts"))
        monitor.doi = sheet_obj.get("doi")

        if not apc.has_fund(sheet_obj.get("fund_1")):
            apc.add_fund(sheet_obj.get("fund_1"))

        if not apc.has_fund(sheet_obj.get("fund_2")):
            apc.add_fund(sheet_obj.get("fund_2"))

        if not apc.has_fund(sheet_obj.get("fund_3")):
            apc.add_fund(sheet_obj.get("fund_3"))

        fs = cls._separate(sheet_obj.get("funder_1"))
        for f in fs:
            monitor.add_funder(f, sheet_obj.get("grant_number_1"))

        fs = cls._separate(sheet_obj.get("funder_2"))
        for f in fs:
            monitor.add_funder(f, sheet_obj.get("grant_number_2"))

        fs = cls._separate(sheet_obj.get("funder_3"))
        for f in fs:
            monitor.add_funder(f, sheet_obj.get("grant_number_3"))

        monitor.date_applied = sheet_obj.get("initial_application_date")
        monitor.issn = sheet_obj.get("issn")
        monitor.set_license(sheet_obj.get("licence"))

        lr = sheet_obj.get("licence_received")
        if lr is not None:
            lr = lr.lower().strip() == "yes"
        monitor.license_received(sheet_obj.get("publication_date"), lr)

        apc.notes = sheet_obj.get("notes")
        monitor.pmcid = sheet_obj.get("pmcid")
        monitor.pmid = sheet_obj.get("pmid")
        monitor.publication_date = sheet_obj.get("publication_date")
        apc.publication_process_feedback = sheet_obj.get("publication_process_feedback")
        monitor.publisher = sheet_obj.get("publisher")
        monitor.source = sheet_obj.get("source")
        monitor.title = sheet_obj.get("title")
        monitor.publication_type = sheet_obj.get("type")

        return ir

    @classmethod
    def _separate(cls, f):
        if f is None:
            return []
        if "," in f:
            fs = [x.strip() for x in f.split(",")]
            return fs
        elif ";" in f:
            fs = [x.strip() for x in f.split(";")]
            return fs
        return [f]