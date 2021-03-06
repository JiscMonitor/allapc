from octopus.lib import dataobj
from service import dao
from copy import deepcopy

class Monitor(dataobj.DataObj):
    """
    {
        "@context": {
            "jm": "http://jiscmonitor.jiscinvolve.org/",
            "dc": "http://purl.org/dc/elements/1.1/",
            "dcterms": "http://purl.org/dc/terms/",
            "rioxxterms": "http://rioxx.net/v2-0-beta-1/",
            "ali" : "http://www.niso.org/schemas/ali/1.0/jsonld.json"
        },

        "dcterms:dateAccepted" : "<date article was accepted for publication>",
        "jm:dateApplied" : "<date APC was initially applied for by author>",
        "rioxxterms:publication_date" : "<publication date>",

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
            ],

            "oa_type" : "<hybrid|oa>",
            "self_archiving" : {
                "preprint" : {
                    "policy" : "<can|restricted|cannot>",
                    "embargo" : <number of months>
                },
                "postprint" : {
                    "policy" : "<can|restricted|cannot>",
                    "embargo" : <number of months>
                },
                "publisher" : {
                    "policy" : "<can|restricted|cannot>",
                    "embargo" : <number of months>
                }
            }
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

        "rioxxterms:type" : "<publication type (article, etc)>",
        "dc:title" : "<title>",

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

        "ali:license_ref" : {
            "title" : "<name of licence>",
            "type" : "<type>",
            "url" : "<url>",
            "version" : "<version>",
        },

        "jm:license_received" : [
            {"date" : "<date licence was checked>", "received" : true|false}
        ],

        "jm:repository" : [
            {
                "name" : "<Name of repository which holds a copy>",
                "repo_url" : "<url for repository>",
                "record_url" : "<url to representation of record in repository>",
                "metadata" : "True|False|Unknown",
                "fulltext" : "True|False|Unknown",
                "machine_readable_fulltext" : "True|False|Unknown",
                "aam" : "True|False|Unknown"
            }
        ],

        "jm:provenance" : [
            "<provenance information for the data in this record>"
        ]
    }
    """

    CONTEXT = {
        "@context": {
            "jm": u"http://jiscmonitor.jiscinvolve.org/",
            "dc": u"http://purl.org/dc/elements/1.1/",
            "dcterms": u"http://purl.org/dc/terms/",
            "rioxxterms": u"http://rioxx.net/v2-0-beta-1/",
            "ali" : u"http://www.niso.org/schemas/ali/1.0/jsonld.json"
        }
    }

    def __init__(self, raw=None):
        super(Monitor, self).__init__(raw)
        if "@context" not in self.data:
            self.data.update(deepcopy(self.CONTEXT))

    def apc_for(self, institution_name):
        for apc in self._get_list("jm:apc"):
            if apc.get("name") == institution_name:
                return InstitutionalAPC(apc)
        obj = {"name" : institution_name}
        self._add_to_list("jm:apc", obj)
        return InstitutionalAPC(obj)

    def has_apcs_for(self):
        return [apc.get("name") for apc in self._get_list("jm:apc")]

    @property
    def date_accepted(self):
        return self._get_single("dcterms:dateAccepted", coerce=self._date_str())

    @date_accepted.setter
    def date_accepted(self, val):
        self._set_single("dcterms:dateAccepted", val, coerce=self._date_str())

    @property
    def date_applied(self):
        return self._get_single("jm:dateApplied", coerce=self._date_str())

    @date_applied.setter
    def date_applied(self, val):
        self._set_single("jm:dateApplied", val, coerce=self._date_str(), allow_none=False, ignore_none=True)

    def add_identifier(self, type, val, unique_type=True):
        if type is None or val is None:
            return

        # coerce the values
        uc = self._utf8_unicode()
        type = self._coerce(type, uc).lower()
        val = self._coerce(val, uc)

        # remove any existing identifier o this type
        if unique_type:
            self.remove_identifier(type)

        # add the new identifier
        self._add_to_list("dc:identifier", {"type" : type, "id" : val})

    def remove_identifier(self, type):
        uc = self._utf8_unicode()
        type = self._coerce(type, uc).lower()
        self._delete_from_list("dc:identifier", matchsub={"type" : type})

    def get_unique_identifier(self, type):
        uc = self._utf8_unicode()
        type = self._coerce(type, uc).lower()
        for identifier in self._get_list("dc:identifier"):
            if identifier.get("type") == type:
                return identifier.get("id")
        return None

    @property
    def pmcid(self):
        return self.get_unique_identifier("pmcid")

    @pmcid.setter
    def pmcid(self, val):
        self.add_identifier("pmcid", val, unique_type=True)

    @property
    def pmid(self):
        return self.get_unique_identifier("pmid")

    @pmid.setter
    def pmid(self, val):
        self.add_identifier("pmid", val, unique_type=True)

    @property
    def doi(self):
        return self.get_unique_identifier("doi")

    @doi.setter
    def doi(self, val):
        self.add_identifier("doi", val, unique_type=True)

    def add_author(self, name):
        if name is None:
            return
        uc = self._utf8_unicode()
        name = self._coerce(name, uc)
        self._add_to_list("rioxxterms:author", {"name" : name})

    @property
    def authors(self):
        return self._get_list("rioxxterms:author")

    @property
    def publisher(self):
        return self._get_single("dcterms:publisher.name")

    @publisher.setter
    def publisher(self, val):
        self._set_single("dcterms:publisher.name", val, coerce=self._utf8_unicode(), allow_none=False, ignore_none=True)

    @property
    def source(self):
        return self._get_single("dc:source.name")

    @source.setter
    def source(self, val):
        self._set_single("dc:source.name", val, coerce=self._utf8_unicode(), allow_none=False, ignore_none=True)

    @property
    def issn(self):
        for identifier in self._get_list("dc:source.identifier"):
            if identifier.get("type") == "issn":
                return identifier.get("id")
        return None

    @issn.setter
    def issn(self, val):
        if val is None:
            return

        if not isinstance(val, list):
            val = [val]

        uc = self._utf8_unicode()
        val = [self._coerce(v, uc) for v in val]

        self._delete_from_list("dc:source.identifier", matchsub={"type" : "issn"})

        for v in val:
            self._add_to_list("dc:source.identifier", {"type" : u"issn", "id" : v})

    def add_issn(self, val):
        if val is None:
            return
        uc = self._utf8_unicode()
        val = self._coerce(val, uc)
        self._add_to_list("dc:source.identifier", {"type" : u"issn", "id" : val})

    @property
    def oa_type(self):
        return self._get_single("dc:source.oa_type", coerce=self._utf8_unicode())

    @oa_type.setter
    def oa_type(self, val):
        self._set_single("dc:source.oa_type", val, allowed_values=["hybrid", "oa"], coerce=self._utf8_unicode())

    @property
    def self_archiving_preprint(self):
        policy = self._get_single("dc:source.self_archiving.preprint.policy", coerce=self._utf8_unicode())
        embargo = self._get_single("dc:source.self_archiving.preprint.embargo", coerce=self._int())
        return policy, embargo

    @self_archiving_preprint.setter
    def self_archiving_preprint(self, val):
        if not isinstance(val, tuple):
            raise dataobj.DataSchemaException("self_archiving_preprint must be a tuple of policy and number of months")
        self._set_single("dc:source.self_archiving.preprint.policy", val[0], coerce=self._utf8_unicode())
        self._set_single("dc:source.self_archiving.preprint.embargo", val[1], coerce=self._int())

    @property
    def self_archiving_postprint(self):
        policy = self._get_single("dc:source.self_archiving.postprint.policy", coerce=self._utf8_unicode())
        embargo = self._get_single("dc:source.self_archiving.postprint.embargo", coerce=self._int())
        return policy, embargo

    @self_archiving_postprint.setter
    def self_archiving_postprint(self, val):
        if not isinstance(val, tuple):
            raise dataobj.DataSchemaException("self_archiving_postprint must be a tuple of policy and number of months")
        self._set_single("dc:source.self_archiving.postprint.policy", val[0], coerce=self._utf8_unicode())
        self._set_single("dc:source.self_archiving.postprint.embargo", val[1], coerce=self._int())

    @property
    def self_archiving_publisher(self):
        policy = self._get_single("dc:source.self_archiving.publisher.policy", coerce=self._utf8_unicode())
        embargo = self._get_single("dc:source.self_archiving.publisher.embargo", coerce=self._int())
        return policy, embargo

    @self_archiving_publisher.setter
    def self_archiving_publisher(self, val):
        if not isinstance(val, tuple):
            raise dataobj.DataSchemaException("self_archiving_publisher must be a tuple of policy and number of months")
        self._set_single("dc:source.self_archiving.publisher.policy", val[0], coerce=self._utf8_unicode())
        self._set_single("dc:source.self_archiving.publisher.embargo", val[1], coerce=self._int())

    @property
    def publication_type(self):
        return self._get_single("rioxxterms:type", coerce=self._utf8_unicode())

    @publication_type.setter
    def publication_type(self, val):
        self._set_single("rioxxterms:type", val, coerce=self._utf8_unicode(), allow_none=False, ignore_none=True)

    @property
    def title(self):
        return self._get_single("dc:title", coerce=self._utf8_unicode())

    @title.setter
    def title(self, val):
        self._set_single("dc:title", val, coerce=self._utf8_unicode(), allow_none=False, ignore_none=True)

    @property
    def publication_date(self):
        return self._get_single("rioxxterms:publication_date", coerce=self._date_str())

    @publication_date.setter
    def publication_date(self, val):
        self._set_single("rioxxterms:publication_date", val, coerce=self._date_str(), allow_none=False, ignore_none=True)

    @property
    def received_license(self):
        return self._get_list("jm:license_received")

    def license_received(self, date, received):
        if date is None or received is None:
            return

        # FIXME: date should be handled as a date at some point
        ds = self._date_str()
        date = self._coerce(date, ds)
        self._add_to_list("jm:license_received", {"date" : date, "received" : bool(received)})

    def add_funder(self, name, grant_number=None):
        if name is None:
            return

        uc = self._utf8_unicode()
        name = self._coerce(name, uc)
        obj = {"name" : name}
        if grant_number is not None:
            grant_number = self._coerce(grant_number, uc)
            obj["grant_number"] = grant_number
        self._add_to_list("rioxxterms:project", obj)

    @property
    def funder(self):
        return self._get_list("rioxxterms:project")

    def set_license(self, title, type=None, url=None, version=None):
        if title is None:
            return

        uc = self._utf8_unicode()
        obj = {"title" : uc(title)}
        if type is not None:
            obj["type"] = uc(type)
        if url is not None:
            obj["url"] = uc(url)
        if version is not None:
            obj["version"] = uc(version)
        self._set_single("ali:license_ref", obj)

    @property
    def license(self):
        return self._get_single("ali:license_ref")

    @property
    def repository(self):
        return [Repository(x) for x in self._get_list("jm:repository")]

    @repository.setter
    def repository(self, val):
        if not isinstance(val, list):
            val = [val]

        rawvals = []
        for v in val:
            if not isinstance(v, Repository):
                v = Repository(v)
            rawvals.append(v.data)

        self._set_list("jm:repository", rawvals)

    def add_repository(self, val):
        if isinstance(val, Repository):
            val = val.data
        self._add_to_list("jm:repository", val)


class Repository(dataobj.DataObj):
    def __init__(self, raw=None):
        super(Repository, self).__init__(raw)

    @property
    def name(self):
        return self._get_single("name", coerce=self._utf8_unicode())

    @name.setter
    def name(self, val):
        self._set_single("name", val, coerce=self._utf8_unicode())

    @property
    def url(self):
        return self._get_single("repo_url", coerce=self._utf8_unicode())

    @url.setter
    def url(self, val):
        self._set_single("repo_url", val, coerce=self._utf8_unicode())

    @property
    def record_url(self):
        return self._get_single("record_url", coerce=self._utf8_unicode())

    @record_url.setter
    def record_url(self, val):
        self._set_single("record_url", val, coerce=self._utf8_unicode())

    @property
    def metadata(self):
        return self._get_single("metadata", coerce=self._utf8_unicode())

    @metadata.setter
    def metadata(self, val):
        self._set_single("metadata", val, allowed_values=["True", "False", "Unknown"], coerce=self._utf8_unicode())

    @property
    def fulltext(self):
        return self._get_single("fulltext", coerce=self._utf8_unicode())

    @fulltext.setter
    def fulltext(self, val):
        self._set_single("fulltext", val, allowed_values=["True", "False", "Unknown"], coerce=self._utf8_unicode())

    @property
    def machine_readable_fulltext(self):
        return self._get_single("machine_readable_fulltext", coerce=self._utf8_unicode())

    @machine_readable_fulltext.setter
    def machine_readable_fulltext(self, val):
        self._set_single("machine_readable_fulltext", val, allowed_values=["True", "False", "Unknown"], coerce=self._utf8_unicode())

    @property
    def aam(self):
        return self._get_single("aam", coerce=self._utf8_unicode())

    @aam.setter
    def aam(self, val):
        self._set_single("aam", val, allowed_values=["True", "False", "Unknown"], coerce=self._utf8_unicode())


class InstitutionalAPC(dataobj.DataObj):
    def __init__(self, raw=None):
        super(InstitutionalAPC, self).__init__(raw)

    def add_fund(self, name, amount=None, currency=None, amount_gbp=None):
        if name is None:
            return

        uc = self._utf8_unicode()
        flc = self._float()
        obj = {"name" : self._coerce(name, uc)}
        if amount is not None:
            obj["amount"] = self._coerce(amount, flc)
        if currency is not None:
            obj["currency"] = self._coerce(currency, uc)
        if amount_gbp is not None:
            obj["amount_gbp"] = self._coerce(amount_gbp, flc)
        self._add_to_list("fund", obj)

    @property
    def funds(self):
        return self._get_list("fund")

    def has_fund(self, name):
        uc = self._utf8_unicode()
        name = uc(name)
        return name in [f.get("name") for f in self.funds]

    @property
    def name(self):
        return self._get_single("name", coerce=self._utf8_unicode())

    @name.setter
    def name(self, val):
        self._set_single("name", val, coerce=self._utf8_unicode(), allow_none=False, ignore_none=True)

    @property
    def date_paid(self):
        return self._get_single("date_paid", coerce=self._date_str())

    @date_paid.setter
    def date_paid(self, val):
        self._set_single("date_paid", val, coerce=self._date_str(), allow_none=False, ignore_none=True)

    @property
    def amount(self):
        return self._get_single("amount", coerce=self._float())

    @amount.setter
    def amount(self, val):
        self._set_single("amount", val, coerce=self._float(), allow_none=False, ignore_none=True)

    @property
    def currency(self):
        return self._get_single("currency", coerce=self._utf8_unicode())

    @currency.setter
    def currency(self, val):
        self._set_single("currency", val, coerce=self._utf8_unicode(), allow_none=False, ignore_none=True)

    @property
    def amount_gbp(self):
        return self._get_single("amount_gbp", coerce=self._float())

    @amount_gbp.setter
    def amount_gbp(self, val):
        self._set_single("amount_gbp", val, coerce=self._float(), allow_none=False, ignore_none=True)

    @property
    def additional_costs(self):
        return self._get_single("additional_costs", coerce=self._float())

    @additional_costs.setter
    def additional_costs(self, val):
        self._set_single("additional_costs", val, coerce=self._float(), allow_none=False, ignore_none=True)

    def add_discount(self, val):
        self._add_to_list("discounts", val, coerce=self._utf8_unicode())

    @property
    def discounts(self):
        return self._get_list("discounts")

    @property
    def publication_process_feedback(self):
        return self._get_single("publication_process_feedback")

    @publication_process_feedback.setter
    def publication_process_feedback(self, val):
        self._set_single("publication_process_feedback", val, coerce=self._utf8_unicode(), allow_none=False, ignore_none=True)

    @property
    def notes(self):
        return self._get_single("notes", coerce=self._utf8_unicode())

    @notes.setter
    def notes(self, val):
        self._set_single("notes", val, coerce=self._utf8_unicode(), allow_none=False, ignore_none=True)


class InstitutionalRecord(dataobj.DataObj, dao.InstitutionalRecordDAO):
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
        return self._get_single("admin.local_id", coerce=self._utf8_unicode())

    @local_id.setter
    def local_id(self, val):
        self._set_single("admin.local_id", val, coerce=self._utf8_unicode(), allow_none=False, ignore_none=True)

    @property
    def account_id(self):
        return self._get_single("admin.account", coerce=self._utf8_unicode())

    @account_id.setter
    def account_id(self, val):
        self._set_single("admin.account", val, coerce=self._utf8_unicode(), allow_none=False, ignore_none=True)

    @property
    def last_upload(self):
        return self._get_single("admin.last_upload", coerce=self._date_str())

    @last_upload.setter
    def last_upload(self, val):
        self._set_single("admin.last_upload", val, coerce=self._date_str())

    @property
    def upload_source(self):
        return self._get_single("admin.upload_source", coerce=self._utf8_unicode())

    @upload_source.setter
    def upload_source(self, val):
        self._set_single("admin.upload_source", val, coerce=self._utf8_unicode())

    @property
    def green_option(self):
        return self._get_single("index.green_option", coerce=self._utf8_unicode())

    @green_option.setter
    def green_option(self, val):
        self._set_single("index.green_option", val, coerce=self._utf8_unicode(), allow_none=False, ignore_none=True)

    @property
    def journal_type(self):
        return self._get_single("index.journal_type", coerce=self._utf8_unicode())

    @journal_type.setter
    def journal_type(self, val):
        self._set_single("index.journal_type", val, coerce=self._utf8_unicode(), allowed_values=[u"oa", u"hybrid"])


class APCRecord(dao.APCRecordDAO):
    pass