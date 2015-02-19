from octopus.modules.es import testindex
from service import models

class TestModels(testindex.ESTestCase):

    def setUp(self):
        super(TestModels, self).setUp()

    def tearDown(self):
        super(TestModels, self).tearDown()

    def test_01_model(self):
        ir = models.InstitutionalRecord()
        monitor = ir.monitor
        apc = monitor.apc_for("Test University")

        assert monitor is not None
        assert apc is not None
        assert apc.name == "Test University"

        # test the attributes of the record
        ir.local_id = "localid"
        ir.account_id = "accid"
        ir.green_option = "maybe"

        assert ir.local_id == "localid"
        assert ir.account_id == "accid"
        assert ir.green_option == "maybe"

        # test the attributes of the apc
        apc.add_fund("COAF", "100", "ALL", "10")
        apc.name = "University of Test"
        apc.date_paid = "2015-01-01"
        apc.amount = 100
        apc.currency = "ALL"
        apc.amount_gbp = 10.00
        apc.additional_costs = 20
        apc.add_discount("coupon")
        apc.publication_process_feedback = "ok"
        apc.notes = "my note"

        assert len(apc.funds) == 1
        assert apc.funds[0]["name"] == "COAF"
        assert apc.funds[0]["amount"] == 100.0
        assert apc.funds[0]["currency"] == "ALL"
        assert apc.funds[0]["amount_gbp"] == 10.0
        assert apc.name == "University of Test"
        assert apc.date_paid == "2015-01-01"
        assert apc.amount == 100.0
        assert apc.currency == "ALL"
        assert apc.amount_gbp == 10.0
        assert apc.additional_costs == 20.0
        assert len(apc.discounts) == 1
        assert apc.discounts[0] == "coupon"
        assert apc.publication_process_feedback == "ok"
        assert apc.notes == "my note"

        # test the attributes of the monitor section
        monitor.date_applied = "2014-01-01"
        monitor.add_identifier("something", "S1234")
        monitor.pmcid = "PMC1234"
        monitor.pmid = "1234"
        monitor.doi = "10.1234"
        monitor.add_author("AN Other")
        monitor.publisher = "PLOS"
        monitor.source = "PLOS One"
        monitor.issn = "1234-5678"
        monitor.publication_type = "journal"
        monitor.title = "The Title"
        monitor.publication_date = "2016-01-01"
        monitor.license_received("2016-01-01", True)
        monitor.add_funder("BBSRC", "B/123/4")
        monitor.set_license("title", "type", "http://url", "4.0")

        assert len(monitor.has_apcs_for()) == 1
        assert "University of Test" in monitor.has_apcs_for()
        assert monitor.date_applied == "2014-01-01"
        assert monitor.get_unique_identifier("something") == "S1234"
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
        assert monitor.publication_date == "2016-01-01"
        assert len(monitor.funder) == 1
        assert monitor.funder[0]["name"] == "BBSRC"
        assert monitor.funder[0]["grant_number"] == "B/123/4"
        assert monitor.license["title"] == "title"
        assert monitor.license["type"] == "type"
        assert monitor.license["url"] == "http://url"
        assert monitor.license["version"] == "4.0"