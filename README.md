# ALL APC

An APC demonstrator collection/dissemination API, and reports based on the data it can collect

## Installation

Clone the project:

    git clone https://github.com/JiscMonitor/allapc

get all the submodules

    cd allapc
    git submodule init
    git submodule update

This will initialise and clone the esprit and magnificent octopus libraries

Then get the submodules for Magnificent Octopus

    cd allapc/magnificent-octopus
    git submodule init
    git submodule update

Create your virtualenv and activate it

    virtualenv /path/to/venv
    source /path/tovenv/bin/activate

Install esprit and magnificent octopus (in that order)

    cd allapc/esprit
    pip install -e .
    
    cd allapc/magnificent-octopus
    pip install -e .
    
Create your local config

    cd allapc
    touch local.cfg

Then you can override any config values that you need to

To start the application, you'll also need to install it into the virtualenv just this first time

    cd allapc
    pip install -e .

Then, start your app with

    python service/web.py

### Importing data

You can import data directly from the TCO spreadsheets with

    python service/scripts/importcsv.py -s "source/spreadsheet.csv", -i "Institution Name"


## Data Model

The data models presented below represents a JSON-based object structure indicating the hierarchy and therefore relationships
of the data elements in the object.  

### APC Data Interchange Model

This section details the structure of the data to be used in transmission over the API.  It can be used to represent either
of the following situations:

1. An Institution's individual perspective of the APC they paid
2. A complete picture of the APC paid for an article

It has been expressed using the syntax of [JSON-LD](http://json-ld.org/) and represents both the shareable APC data and 
the internal information required for an application to manage the data.

Where possible top-level keys in the model have been taken from the following metadata schemas/profiles:

* [The DCMI Terms](http://dublincore.org/documents/dcmi-terms/)
* [RIOXX](http://rioxx.net/v2-0-beta-1/)
* [NISO Access and Licence Indicators (ALI)](http://www.niso.org/workrooms/ali/)

```python
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
```

Note that each entity in the data (such as author, publisher, organisation) have space for both a name (ideally from a standard 
list) and an identifier.  The hope is that we can at least find a way to uniquely identify these entities
such that we can determine equivalences across the dataset.

Descriptions of notable fields, and the requirements for their use are as follows:

* **jm:dateApplied** - an ISO 8601 formatted date (e.g. 2014-10-16T17:34:03Z)
* **dc:identifier** - should contain at least a URL to the object (as per RIOXX).  **Mandatory**
* **dc:source** - the RIOXX profile considers this to principally a journal, but it will take any other object that is a suitable source
such as a book.  **Mandatory where applicable**.
* **dc:source.oa_type** - whether this journal is pure oa or hybrid
* **dc:source.self_archiving** - for each of the doucument types *preprint*, *postprint* and *publisher* version, what the self-archiving policy is, and whether there is an associated embargo
* **rioxxterms:author**  - as per the RIOXX profile this field is **Mandatory** (although note that it often isn't present)
* **dc:publisher** - as per the RIOXX profile this field is **Recommended**.
* **rioxxterms:type** - confirms to the RIOXX profile for controlled vocabulary of terms.  **Mandatory** (although note that it often isn't present).
* **dc:title** - as per the RIOXX profile this field is **Mandatory**
* **rioxxterms:project**  - as per the RIOXX profile this field is **Mandatory**
* **jm:apc** - this field should not be confused with rioxxterms:apc, which has a different purpose.  In this data model this provides a 
wrapper for detailed information about APC payments.
* **jm:apc.amount** and **jm:apc.amount_gbp** - these are the pure costs for the APC, and should not include costs for extras such as page charges 
or colour charges.  Any additional charges associated with publication should be summed in **jm:apc.additional_costs**.
* **jm:apc.fund** - this covers information about the fund or source of finance that the APC was paid from.  It could include RCUK, COAF or Institutional funds, and **does not** refer
 to the original funder of the work (which is covered in **rioxxterms:project**)
* **jm:apc.currency** - the standard 3 letter currency code
* **ali:license_ref** - an object based on the OAG and DOAJ licence data formats for recording the type, version and url of a licence that should
have been applied to this item
* **jm:licence_received** - was the licence that was ultimately applied to the publication that which the APC paid for?  This may be checked periodically by
different organisations, so date provenance of the check is required.
* **jm:repository** - list of known repositories that the record appears in.  Each repository may contain the *metadata* and the *fulltext* ad may also provide the fulltext as *machine_readable_fulltext*, such as in an XML format.


### Institutional Records

This section details the extended information required by the APC aggregation to manage records coming from individual institutions

```python
{
    "id" : "<opaque internal record identifier>",
    "created_date" : "<date the record was created>",
    "last_updated" : "<date the record was last modified>",
    
    "admin" : {
        "account" : "<user account who provided this record originally>",
        "local_id" : "<identifier supplied by the user for this record>",
        "last_upload" : "<date of last upload of this record>",
        "upload_source" : "<name of spreadsheet of last upload if relevant>"
    },
    
    "monitor" : { <apc record, as defined above> },
}
```

In the **admin** section we store information about the originator of this particular record, which will then allow them
to update or delete the record in the future.  The **account** is some user identifier (such as a username or an API key)
and the **local_id** is an identifier that we keep on behalf of the providing institution if they wish to provide one, so
that they can retrieve their record again by their own identifiers at a later date.

### APC Records

This section details the extended information required by the APC aggregation to manage records which have been derived by
merging **Institutional Records** for the same article.

```python
{
    "id" : "<opaque internal record identifier>",
    "created_date" : "<date the record was created>",
    "last_updated" : "<date the record was last modified>",
    
    "admin" : {
        "origin" : ["<list of ids of Institutional Records>"]
    },
    
    "monitor" : { <merged apc record, as defined above> },
    
    "index" : {
        "doi" : "<doi of the article>",
        "url" : "<url for the article>",
        "issn" : ["<all known issns for the journal (print and electronic)>"],
        "orcid" : ["<all known orcids for authors of this article>"],
        "total_gbp" : <sum of all monitor.jm:apc.amount_gbp>
    }
}
```

In the **admin** section here we just store the internal identifiers of the institutional records which have been merged
to produce this APC record.

The **index** section provides us with quick look-up fields for important data that is otherwise more complex to retrieve
from the document.  In particular note the **issn** field is a list of all known ISSNs for the journal, so we do not need
to distinguish between electronic and print ISSNs during search.  The **total_gbp** field is the sum of all the known APCs
paid by institutions in the **monitor.jm:apc** field, which will allow us to quickly perform statistical analysis on the totals.

## APC Spreadsheet Mapping

The objective of this work is to provide a data model and process which expands upon the work at Jisc Collections
which gathers APC data from institutions in spreadsheets.  In order to be successful it must always be possible for us
to map the spreadsheets to our data model above.  

This section defines that mapping.  Note that mappings are to the **Institutional Record** model.


| Spreadsheet Field | Data Model Field |
| ----------------- | ---------------- |
| Institution | monitor.jm:apc.name |
| Date of initial application by author	| monitor.jm:dateApplied |
| Submitted by | - |
| University department	| - |
| PubMed Central (PMC) ID | monitor.dc:identifier.type="pmcid" and monitor.dc:identifier.id |
| PubMed ID | monitor.dc:identifier.type="pmid" and monitor.dc:identifier.id |
| DOI | monitor.dc:identifier.type="doi" and monitor.dc:identifier.id |
| Affiliated author	| monitor.rioxxterms:author.name |
| Publisher | monitor.dcterms:publisher.name |
| Journal | monitor.dc:source.name |
| ISSN | monitor.dc:source.identifier.type="issn" and monitor.dc:source.identifier.id |
| Type of publication | monitor.rioxxterms:type |
| Article title | monitor.dc:title |
| Date of publication | monitor.rioxxterms:publication_date and monitor.jm:license_received.date |
| Fund that APC is paid from (1) | monitor.jm:apc.fund.name |
| Fund that APC is paid from (2) | monitor.jm:apc.fund.name |
| Fund that APC is paid from (3) | monitor.jm:apc.fund.name |
| Funder of research (1) | monitor.rioxxterms:project.name |
| Funder of research (2) | monitor.rioxxterms:project.name |
| Funder of research (3) | monitor.rioxxterms:project.name |
| Grant number (1) | monitor.rioxxterms:project.grant_number |
| Grant number (2) | monitor.rioxxterms:project.grant_number |
| Grant number (3) | monitor.rioxxterms:project.grant_number |
| Date of APC payment | monitor.jm:apc.date_paid |
| APC paid (actual currency) including VAT if charged | monitor.jm:apc.amount |
| Currency of APC | monitor.jm:apc.currency |
| APC paid (£) including VAT if charged | monitor.jm:apc.amount_gbp |
| Additional costs (£) | monitor.jm:apc.additional_costs |
| Discounts, memberships & pre-payment agreements | monitor.jm:apc.discounts |
| Amount of APC charged to COAF grant (include VAT if charged) in £ | monitor.jm:apc.fund.name="COAF" and monitor.jm:apc.fund.amount_gbp |
| Licence | monitor.license_ref.title and monitor.license_ref.type |
| Correct license applied? | monitor.license_received.received |
| Problem-free open access publication? | monitor.jm:apc.publication_process_feedback |
| Notes | monitor.jm:apc.notes |


## CRUD API

The specification of the API below is a full imagining of a CRUD interface, which must be validated for usefulness.  We may not want to do all of it.  

Each section also indicates Authentication and Authorisation parameters (AuthNZ) - we do not anticipate implementing these, but they exist to indicate
what would likely be required from a full system/protocol specification.

Note that the only kinds of objects it is possible to manipulate are those specified by the section **Institutional Records**.  All data
sent or received regarding APCs, though, will conform strictly to the specification in the **APC Data Interchange Model**


### Create

Mechanisms to create individual or groups of APC data records.

#### Add a new record

**AuthNZ**: Authenticated User

Create a single Institutional Record:

    POST /apc?api_key=<api key>
    Slug: <local id>
    Content-Type: application/json
    <apc data>

Returns 201, and a Location header with the URL for the created object, plus a JSON response body with the URL for the object:

    201 Created
    Location: <URL to retrieve created object>
    Content-Type: application/json
    
    {
        "status" : 201,
        "location" : "<URL to retrieve created object>",
        "local" : "<URL to retrieve created object via local identifier (if provided in request)>"
    }


### Retrieve

Mechanisms to retrieve APC data records

#### Individual APC Record

**AuthNZ**: None

Get an individual APC record back by id

    GET /apc/<id>

Returns 200 and the APC record as JSON in the body, or 404 if the record could not be found

    200 OK
    Content-Type: application/json
    
    <apc data>


#### Individual APC Record via Local ID

**FIXME: doesn't look quite right from a REST point of view, but difficult to see how else to do it such that
the user doesn't need to remember anything except the local id**

**AuthNZ**: Authenticated User

Get an individual APC record back by the local id provided at creation

    GET /local/<id>?api_key=<api key>

Returns 200 and the APC record as JSON in the body, or 404 if the record could not be found under the user's account

    200 OK
    Content-Type: application/json
    
    <apc data>

### Update

#### Replace an APC record by ID

**AuthNZ**: Authenticated User + (Owner of APC Record *OR* Super User) 

Replace an existing APC record by its unique id

    PUT /apc/<id>?api_key=<api_key>
    Slug: <local_id>
    <new apc record>

Returns a 204 if successful, or a 404 if an APC with that ID does not exist under the user's account.  

    204 No Content

If a local_id is not supplied, the  existing local_id on the record will be removed.  If a local_id is supplied, it will 
overwrite the existing one.


### Delete

#### Delete by ID

**AuthNZ**: Authenticated User + (Owner of APC Record *OR* Super User) 

Delete an existing APC record by its unique id

    DELETE /apc/<id>?api_key=<api_key>

Returns a 204 if successful, or a 404 if an APC with that ID does not exist under the user's account.

    204 No Content

## Discovery API

This describes an application specific search and discovery API which would be used to build a custom search
interface, or for third parties to embed a search/query interface or allow them to keep up to date with change to
the system

### Search

**AuthNZ**: None

Obtain a set of search results from the APC data.

Simple approach

    GET /search?q=<search terms>

Advanced approach, using [Elasticsearch](http://elasticsearch.org) semantics:

    GET /search?source=<query object>

Either method will return the results in the format provided by Elasticsearch

*Note: the planned implementation will use Elasticsearch, which provides powerful search semantics, and a URL-based
search interface which wraps this seems unnecessary.  If there are regular searches which warrant explicit semantics
then we may wish to consider that in the future (e.g. see the Change List below)*


### Change List

**AuthNZ**: None

Obtain the changes to the set of records in a given time period

    GET /changes?from=<date>&until=<date>&size=<page size>&page=<page number>

Returns the results in the format provided by Elasticsearch

*Note: the change list is a special case of an Elasticsearch query - it will effectively proxy for a time-boxed, ordered
query against the index, hence the reason that the result set will be Elasticsearch formatted*


## Reporting Requirements

### Funder Perspective

These requirements come from the perspective of a funder who is interested in particular with negotiation with
publishers over subscription/APC costs.

* Total Expenditure on a particular publisher
    * across the sector
    * for a given group of institutions
    * for a given institution
* Total Expenditure on Hybrid Journals
    * across the sector
    * for a given group of institutions
    * for a given institution
    * for a given publisher
* Number of Articles APC paid for
    * across the sector
    * for a given group of institutions
    * for a given institution
    * for a given publisher
* Average, Highest and Lowest APC per publisher
* Journal ranking (e.g. by Impact Factor) against average APC costs
    * comparison between the whole sector vs a given publisher
    * comparison between given publishers
* Total Expenditure on individual journals
    * principally for publishers with few journals
* Correct licence applied, per publisher

Additional Functional Requirements:

* Flexible reporting periods:
    * monthly
    * annually, with varying start dates

### Institutional Perspective

These requirements are from institutions interested in both their own reporting requirements, and also in the data
available in an aggregation of all APCs.

Institutional Requirements (unlikely to be addressed by the aggregation)

* Custom reports for funders: RCUK and Wellcome in particular
* Break-down of finances: APC, Additional Costs, VAT, Overseas Currency Transactions
* Total expenditure by faculty/department/researcher (e.g. by ORCID)
* Numbers Published vs Numbers Committed to Pay vs Numbers Paid but not Published
* Amount paid vs Staff Effort

General Requirements (which may be addressable by the aggregation)

* Gold publications for which Green was possible
* By Fund (paid from, e.g. COAF/RCUK) by Institution
* Discount vs Non-Discount cost per publisher per institution
* Number of APCs paid vs Total Cost per institution
* Time spent on APCs by institution
* Green vs Gold across the sector
* Total Expenditure on individual journals
* Journal ranking (e.g. by Impact Factor) against average APC costs

Additional Requirements

* Detection of APCs paid by another institution, so that they can be reported as compliant

## Analytics API

This section describes a theoretical, application-specific API endpoint which would provide analytical information which could be used in 
a variety of reporting use cases.  It will be extended during the process of prototype development.

### Expenditure Stats

Statistics on expenditure can be obtained by hitting the /stats endpoint, which has the following forms

To obtain a result-set of expenditure per value of an aspect (e.g. the list of expenditures by publisher):

    GET /stats/<aspect>

To obtain the statistics for a single value of an aspect (e.g. the expenditure on a specific publisher):

    GET /stats/<aspect>/<value>
    
The statistics for each value within an aspect will provide:

* Total expenditure on APCs
* Average expenditure on APCs
* Smallest single APC payment
* Largest single APC payment

Requests can be further refined by limiting the APC payments that are counted into the statistics using the following query parameters:

* **funder** - consider only APCs for articles published on projects funded by this funder
* **publisher** - consider only APCs for articles published with this publisher
* **institution** - consider only APCs paid by this institution
* **author** - consider only APCs paid on behalf of this author (by ORCID)
* **journal** - consider only APCs for articles published in this journal
* **licence** - consider only APCs for articles with this licence
* **date_applied_from** - consider only APCs which were applied for after this date
* **date_applied_to** - consider only APCs which were applied for before this date
* **publication_type** - consider only APCs for publications of this type
* **publication_date_from** - consider only APCs for articles published after this date
* **publication_date_to** - consider only APCs for articles publisher before this date

Not all query parameters will be supported by all aspects (see below for details).

Aspects that can be requested are as follows

#### Funder

Get a list of statistics for each funder

    GET /stats/funder

Get the statistics for a given funder identified by name (as it appears in the data) or the funder's id

    GET /stats/funder/<name or funder id>
    
Does not support query parameters: funder

#### Publisher

Get a list of statistics for each publisher

    GET /stats/publisher

Get the statistics for a given publisher identified by name (as it appears in the data)

    GET /stats/publisher/<name>

Does not support query parameters: publisher

#### Institution

Get a list of statistics for each institution

    GET /stats/institution

Get the statistics for a given institution identified by name (as it appears in the data)

    GET /stats/institution/<name>

Does not support query parameters: institution

#### Author

Get a list of statistics for each author

    GET /stats/author

Get the statistics for a given author identified by ORCID

    GET /stats/author/<orcid>

Does not support query parameters: author

#### Journal

Get a list of statistics for each journal

    GET /stats/journal

Get the statistics for a given journal identified by name (as it appears in the data) or ISSN

    GET /stats/journal/<name or issn>

Does not support query parameters: journal, publisher

#### Licence

Get a list of statistics for each licence type

    GET /stats/licence

Get the statistics for a given licence identified by type (as it appears in the data)

    GET /stats/licence/<type>

Does not support query parameters: licence


### Expenditure Histograms

Date histograms on expenditure can be obtained by hitting the /hist endpoint, which has the following form:

Get the date histogram for a single value of a given aspect (e.g. APCs over time for a specific publisher)

    GET /hist/<aspect>/<value>/[expenditure|count]

This will return a list of expenditure statistics or counts of APCs paid divided into date boxes.

You can also provide the following query parameters:

* **interval** - granularity of the date boxes, one of: year, quarter, month
* **from** - only include APCs paid after this date
* **until** - only include APCs paid before this date
* **funder** - consider only APCs for articles published on projects funded by this funder
* **publisher** - consider only APCs for articles published with this publisher
* **institution** - consider only APCs paid by this institution
* **author** - consider only APCs paid on behalf of this author (by ORCID)
* **journal** - consider only APCs for articles published in this journal
* **licence** - consider only APCs for articles with this licence

Aspects that can be requested are as follows

#### Funder

Get a hisogram for the funder

    GET /hist/funder/<name or funder id>/[expenditure|count]

#### Publisher

Get a hisogram for the publisher

    GET /hist/publisher/<name>/[expenditure|count]

#### Institution

Get a hisogram for the institution

    GET /hist/institution/<name>/[expenditure|count]

#### Author

Get a hisogram for the author

    GET /hist/author/<orcid>/[expenditure|count]

#### Journal

Get a hisogram for the journal

    GET /hist/journal/<name or issn>/[expenditure|count]

#### Licence

Get a hisogram for the licence

    GET /hist/licence/<type>/[expenditure|count]
