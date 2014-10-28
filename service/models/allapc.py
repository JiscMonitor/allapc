from service import dao
from copy import deepcopy

class Monitor(object):
    """
    {
        "@context": {
            "jm": "http://jiscmonitor.jiscinvolve.org/",
            "dc": "http://purl.org/dc/elements/1.1/",
            "dcterms": "http://purl.org/dc/terms/",
            "rioxxterms": "http://rioxx.net/v2-0-beta-1/"
        }

        "jm:dateApplied" : "<date APC was applied for by author>",

        "dc:identifier" : [
            {"type" : "pmcid", "id" : "<europe pubmed central id>"},
            {"type" : "pmid", "id" : "<pubmed id>"},
            {"type" : "doi", "id" : "<doi>"},
            {"type" : "url", "id" : "<url to object>"}
        ],

        "dc:source" : {
            "name" : "<name of the journal or other source (e.g. book)>",
            "identifier" : [
                {"type" : "issn", "id" : "<issn of the journal (could be print or electronic)>" },
                {"type" : "eissn", "id" : "<electronic issn of the journal>" },
                {"type" : "pissn", "id" : "<print issn of the journal>" },
                {"type" : "doi", "id" : "<doi for the journal or series>" }
            ]
        },

        "rioxxterms:author" : [
            {
                "name" : "<author name>",
                "identifier" : [
                    {"type" : "orcid", "id" : "<author's orcid>"},
                    {"type" : "email", "id" : "<author's email address>"},
                ]
            }
        ],

        "dcterms:publisher" : {
            "name" : "<publisher of the article>",
            "identifier" : [
                {"type" : "<identifier type>", "id" : "<publisher identifier>"}
            ]
        },

        "rioxxterms:type" : "<publication type>",
        "dc:title" : "<title>",
        "rioxxterms:publication_date" : "<publication date>",

        "rioxxterms:project" : [
            {
                "name" : "<name of funder>",
                "identifier" : [
                    {"type" : "<identifier type>", "id" : "<funder identifier>"}
                ]
                "grant_number" : "<funder's grant number>"
            }
        ],

        "jm:apc" : [
            {
                "name" : "<name of organisation>",
                "identifier" : [
                    {"type" : "<identifier type>", "id" : "<organisation identifier>"}
                ]
                "amount" : <amount paid in native currency>,
                "currency" : "<currency paid in>",
                "amount_gbp" : <amount paid in equivalent GBP>,
                "fund" : [
                    {
                        "name" : "<name of the fund paid from>",
                        "amount" : "<amount paid from this fund>",
                        "currency" : "<currency received from this fund>",
                        "amount_gbp" : "<amout paid from this fund in equivalent GBP>"
                    }
                ],
                "date_paid" : "<date apc paid>",
                "additional_costs" : <additional apc costs in GBP>,
                "discounts" : "<description of any discounts applied>",
                "publication_process_feedback" : ["<notes on the process of publication>"],
                "notes" : "<free text notes on the APC record from this institution>"
            }
        ],

        "license_ref" : {
            "title" : "<name of licence>",
            "type" : "<type>",
            "url" : "<url>",
            "version" : "<version>",
        },

        "jm:license_received" : [
            {"date" : "<date licence was checked>", "received" : true|false}
        ]
    }
    """

    CONTEXT = {
        "@context": {
            "jm": "http://jiscmonitor.jiscinvolve.org/",
            "dc": "http://purl.org/dc/elements/1.1/",
            "dcterms": "http://purl.org/dc/terms/",
            "rioxxterms": "http://rioxx.net/v2-0-beta-1/"
        }
    }

    def __init__(self, raw=None):
        self.data = raw
        if self.data is None:
            self.data = {}
            self.data.update(deepcopy(self.CONTEXT))


class InstitutionalRecord(dao.InstitutionalRecordDAO):
    @property
    def monitor(self):
        if "monitor" not in self.data:
            self.data["monitor"] = Monitor().data
        return Monitor(self.data.get("monitor"))

    @monitor.setter
    def monitor(self, val):
        if isinstance(val, Monitor):
            self.data["monitor"] = val.data
        else:
            self.data["monitor"] = Monitor(val).data    # looks obtuse, but it allows us to be sure that the monitor object is right

    @property
    def local_id(self):
        return self.data.get("admin", {}).get("local_id")

    @local_id.setter
    def local_id(self, val):
        if "admin" not in self.data:
            self.data["admin"] = {}
        self.data["admin"]["local_id"] = val

    @property
    def account_id(self):
        return self.data.get("admin", {}).get("account")

    @account_id.setter
    def account_id(self, val):
        if "admin" not in self.data:
            self.data["admin"] = {}
        self.data["admin"]["account"] = val

class APCRecord(dao.APCRecordDAO):
    pass