from octopus.modules.es import testindex

from service import sheets

import os

APC_SHEET = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "resources", "apcs.csv")

class TestSheets(testindex.ESTestCase):

    def setUp(self):
        super(TestSheets, self).setUp()

    def tearDown(self):
        super(TestSheets, self).tearDown()

    def test_01_apc(self):
        # load the sheet and read the two records out of it
        sheet = sheets.APCSheet(APC_SHEET)
        gen = sheet.objects()
        one = gen.next()
        two = gen.next()

        # check that the first record - which should be fully complete, has come through ok
        assert one.get("amount") == "100"
        assert one.get("amount_gbp") == "10"
        assert one.get("additional_costs") == "20"
        assert one.get("affiliated_author") == "AN Other"
        assert one.get("coaf") == "40"
        assert one.get("title") == "The Title"
        assert one.get("licence_received") == "Yes"
        assert one.get("currency") == "ALL"
        assert one.get("doi") == "10.1234"
        assert one.get("apc_payment_date") == "01/01/14"
        assert one.get("initial_application_date") == "05/04/2013"
        assert one.get("publication_date") == "01/01/16"
        assert one.get("discounts") == "coupon"
        assert one.get("fund_1") == "COAF"
        assert one.get("fund_2") == "RCUK"
        assert one.get("fund_3") == "Institutional"
        assert one.get("funder_1") == "BBSRC"
        assert one.get("funder_2") == "AHRC"
        assert one.get("funder_3") == "Wellcome Trust"
        assert one.get("grant_number_1") == "BB/F016832/1"
        assert one.get("grant_number_2") == "AH/123/4"
        assert one.get("grant_number_3") == "WEL-01"
        assert one.get("issn") == "1234-5678"
        assert one.get("source") == "PLOS One"
        assert one.get("licence") == "CC BY"
        assert one.get("notes") == "Whatever"
        assert one.get("publication_process_feedback") == "Fine"
        assert one.get("pmcid") == "PMC1234"
        assert one.get("pmid") == "1234"
        assert one.get("publisher") == "PLOS"
        assert one.get("submitted_by") == "Tester"
        assert one.get("type") == "journal"
        assert one.get("department") == "Physics"

        # check the second record, which will have missing values
        assert two.get("amount") is None
        assert two.get("amount_gbp") == "1068"
        assert two.get("additional_costs") is None
        assert two.get("affiliated_author") is None
        assert two.get("coaf") is None
        assert two.get("title") is None
        assert two.get("licence_received") is None
        assert two.get("currency") == "GBP"
        assert two.get("doi") == "10.1038/srep01239"
        assert two.get("apc_payment_date") is None
        assert two.get("initial_application_date") == "10/04/2013"
        assert two.get("publication_date") is None
        assert two.get("discounts") is None
        assert two.get("fund_1") is None
        assert two.get("fund_2") is None
        assert two.get("fund_3") is None
        assert two.get("funder_1") == "EPSRC"
        assert two.get("funder_2") == "Other"
        assert two.get("funder_3") is None
        assert two.get("grant_number_1") == "EP/J007544/1"
        assert two.get("grant_number_2") is None
        assert two.get("grant_number_3") is None
        assert two.get("issn") is None
        assert two.get("source") == "Scientific Reports"
        assert two.get("licence") == "CC BY"
        assert two.get("notes") is None
        assert two.get("publication_process_feedback") is None
        assert two.get("pmcid") is None
        assert two.get("pmid") is None
        assert two.get("publisher") == "Nature Publishing Group"
        assert two.get("submitted_by") is None
        assert two.get("type") is None
        assert two.get("department") is None