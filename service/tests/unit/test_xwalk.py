from octopus.modules.es import testindex

from service import sheets, institutional

import os

APC_SHEET = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "resources", "apcs.csv")

class TestXwalk(testindex.ESTestCase):

    def setUp(self):
        super(TestXwalk, self).setUp()

    def tearDown(self):
        super(TestXwalk, self).tearDown()

    def test_01_sheet2ir(self):
        sheet = sheets.APCSheet(APC_SHEET)
        gen = sheet.objects()
        one = gen.next()

        one["institution"] = "University of Test"
        irone = institutional.Sheet2Institutional.sheet2institutional(one)

        monitor = irone.monitor
        apc = monitor.apc_for("University of Test")

        assert len(apc.funds) == 3

        fs = [f["name"] for f in apc.funds]
        fs.sort()
        assert fs == ["COAF", "Institutional", "RCUK"]
        for f in apc.funds:
            if f["name"] == "COAF":
                assert f["amount_gbp"] == 40.0

        assert apc.name == "University of Test"
        assert apc.date_paid == "01/01/14"
        assert apc.amount == 100.0
        assert apc.currency == "ALL"
        assert apc.amount_gbp == 10.0
        assert apc.additional_costs == 20.0
        assert len(apc.discounts) == 1
        assert apc.discounts[0] == "coupon"
        assert apc.publication_process_feedback == "Fine"
        assert apc.notes == "Whatever"

        assert len(monitor.has_apcs_for()) == 1
        assert "University of Test" in monitor.has_apcs_for()
        assert monitor.date_applied == "05/04/2013"
        assert monitor.pmcid == "PMC1234"
        assert monitor.pmid == "1234"
        assert monitor.doi == "10.1234"
        assert len(monitor.authors) == 1
        assert monitor.authors[0]["name"] == "AN Other"
        assert monitor.publisher == "PLOS"
        assert monitor.source == "PLOS One"
        assert monitor.issn == "1234-5678"
        assert monitor.publication_type == "journal"
        assert monitor.title == "The Title"
        assert monitor.publication_date == "01/01/16"
        assert len(monitor.funder) == 3

        fs = [f["name"] for f in monitor.funder]
        fs.sort()
        assert fs == ["AHRC", "BBSRC", "Wellcome Trust"]
        for f in monitor.funder:
            if f["name"] == "AHRC":
                assert f["grant_number"] == "AH/123/4"
            elif f["name"] == "BBSRC":
                assert f["grant_number"] == "BB/F016832/1"
            elif f["name"] == "Wellcome Trust":
                assert f["grant_number"] == "WEL-01"

        assert monitor.license["title"] == "CC BY"
