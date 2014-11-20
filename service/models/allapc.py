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
                "discounts" : ["<names or identifiers of any discounts applied>"],
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

    def apc_for(self, institution_name):
        if "jm:apc" not in self.data:
            self.data["jm:apc"] = []
        for apc in self.data.get("jm:apc"):
            if apc.get("name") == institution_name:
                return InstitutionalAPC(apc)
        obj = {"name" : institution_name}
        self.data["jm:apc"].append(obj)
        return InstitutionalAPC(obj)

    @property
    def date_applied(self):
        return self.data.get("jm:dateApplied")

    @date_applied.setter
    def date_applied(self, val):
        self.data["jm:dateApplied"] = val

    def remove_identifier(self, type):
        if "dc:identifier" not in self.data:
            return

        removes = []
        i = 0
        for identifier in self.data["dc:identifier"]:
            if identifier.get("type") == type:
                removes.append(i)
            i += 1

        removes.sort(reverse=True)
        for r in removes:
            del self.data["dc:identifier"][r]

        if len(self.data["dc:identifier"]) == 0:
            del self.data["dc:identifier"]

    def add_identifier(self, type, val, unique_type=True):
        if unique_type:
            self.remove_identifier(type)
        if "dc:identifier" not in self.data:
            self.data["dc:identifier"] = []
        self.data["dc:identifier"].append({
            "type" : type,
            "id" : val
        })

    def get_unique_identifier(self, type):
        for identifier in self.data.get("dc:identifier", []):
            if identifier.get("type") == type:
                return identifier.get("id")
        return None

    @property
    def pmcid(self):
        return self.get_unique_identifier("pmcid")

    @pmcid.setter
    def pmcid(self, val):
        self.add_identifier("pmcid", val)

    @property
    def pmid(self):
        return self.get_unique_identifier("pmid")

    @pmid.setter
    def pmid(self, val):
        self.add_identifier("pmid", val)

    @property
    def doi(self):
        return self.get_unique_identifier("doi")

    @doi.setter
    def doi(self, val):
        self.add_identifier("doi", val)

    def add_author(self, name):
        if "rioxxterms:author" not in self.data:
            self.data["rioxxterms:author"] = []
        self.data["rioxxterms:author"].append({"name" : name})

    @property
    def publisher(self):
        return self.data.get("dcterms:publisher", {}).get("name")

    @publisher.setter
    def publisher(self, val):
        if "dcterms:publisher" not in self.data:
            self.data["dcterms:publisher"] = {}
        self.data["dcterms:publisher"]["name"] = val

    @property
    def source(self):
        return self.data.get("dc:source", {}).get("name")

    @source.setter
    def source(self, val):
        if "dc:source" not in self.data:
            self.data["dc:source"] = {}
        self.data["dc:source"]["name"] = val

    @property
    def issn(self):
        source = self.data.get("dc:source")
        if source is None:
            return None
        for identifier in source.get("identifier", []):
            if identifier.get("type") == "issn":
                return identifier.get("id")
        return None

    @issn.setter
    def issn(self, val):
        if "dc:source" not in self.data:
            self.data["dc:source"] = {}
        for identifier in self.data["dc:source"].get("identifier", []):
            if identifier.get("type") == "issn":
                identifier["id"] = val
                return
        if "identifier" not in self.data["dc:source"]:
            self.data["dc:source"]["identifier"] = []
        self.data["dc:source"]["identifier"].append({
            "type" : "issn",
            "id" : val
        })

    @property
    def publication_type(self):
        return self.data.get("rioxxterms:type")

    @publication_type.setter
    def publication_type(self, val):
        self.data["rioxxterms:type"] = val

    @property
    def title(self):
        return self.data.get("dc:title")

    @title.setter
    def title(self, val):
        self.data["dc:title"] = val

    @property
    def publication_date(self):
        return self.data.get("rioxxterms:publication_date")

    @publication_date.setter
    def publication_date(self, val):
        self.data["rioxxterms:publication_date"] = val

    def license_received(self, date, received):
        if "jm:license_received" not in self.data:
            self.data["jm:license_received"] = []
        self.data["jm:license_received"].append({
            "date" : date,
            "received" : bool(received)
        })

    def add_funder(self, name, grant_number=None):
        if "rioxxterms:project" not in self.data:
            self.data["rioxxterms:project"] = []
        obj = {"name" : name}
        if grant_number is not None:
            obj["grant_number"] = grant_number
        self.data["rioxxterms:project"].append(obj)

    @property
    def funder(self):
        return self.data.get("rioxxterms:project", [])

    def set_license(self, title, type=None, url=None, version=None):
        obj = {"title" : title}
        if type is not None:
            obj["type"] = type
        if url is not None:
            obj["url"] = url
        if version is not None:
            obj["version"] = version
        self.data["license_ref"] = obj


class InstitutionalAPC(object):
    def __init__(self, raw=None):
        self.data = raw
        if self.data is None:
            self.data = {}

    def add_fund(self, name, amount=None, currency=None, amount_gbp=None):
        if "fund" not in self.data:
            self.data["fund"] = []
        obj = {"name" : name}
        if amount is not None:
            obj["amount"] = float(amount)
        if currency is not None:
            obj["currency"] = currency
        if amount_gbp is not None:
            obj["amount_gbp"] = float(amount_gbp)
        self.data["fund"].append(obj)

    @property
    def date_paid(self):
        return self.data.get("date_paid")

    @date_paid.setter
    def date_paid(self, val):
        self.data["date_paid"] = val

    @property
    def amount(self):
        return self.data.get("amount")

    @amount.setter
    def amount(self, val):
        self.data["amount"] = float(val)

    @property
    def currency(self):
        return self.data.get("currency")

    @currency.setter
    def currency(self, val):
        self.data["currency"] = val

    @property
    def amount_gbp(self):
        return self.data.get("amount_gbp")

    @amount_gbp.setter
    def amount_gbp(self, val):
        self.data["amount_gbp"] = float(val)

    @property
    def additional_costs(self):
        return self.data.get("additional_costs")

    @additional_costs.setter
    def additional_costs(self, val):
        self.data["additional_costs"] = float(val)

    def add_discount(self, val):
        if "discounts" not in self.data:
            self.data["discounts"] = []
        self.data["discounts"].append(val)

    @property
    def publication_process_feedback(self):
        return self.data.get("publication_process_feedback")

    @publication_process_feedback.setter
    def publication_process_feedback(self, val):
        self.data["publication_process_feedback"] = val

    @property
    def notes(self):
        return self.data.get("notes")

    @notes.setter
    def notes(self, val):
        self.data["notes"] = val


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

    @property
    def green_option(self):
        return self.data.get("index", {}).get("green_option")

    @green_option.setter
    def green_option(self, val):
        if "index" not in self.data:
            self.data["index"] = {}
        self.data["index"]["green_option"] = val;

class APCRecord(dao.APCRecordDAO):
    pass