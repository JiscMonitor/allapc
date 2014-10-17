# ALL APC

An APC demonstrator collection/dissemination API, and reports based on the data it can collect

## Data Model

The data model presented below represents a JSON-based object structure indicating the hierarchy and therefore relationships
of the data elements in the object.  It has been expressed using the syntax of [JSON-LD](http://json-ld.org/) where appropriate 
(i.e inside the "montior" element), and reprenents both the shareable APC data and the internal information required for an 
application to manage the data.

Where possible top-level keys in the "monitor" section of the model have been taken from the following metadata schemas/profiles:

* [The DCMI Terms](http://dublincore.org/documents/dcmi-terms/)
* [RIOXX](http://rioxx.net/v2-0-beta-1/)

```python
{
    "id" : "<opaque internal record identifier>",
    
    "admin" : {
        "owner" : "<user account who provided this record originally>",
        "local_id" : "<identifier supplied by the user for this record>"
    },
    
    "monitor" : {
        "@context": {
            "jm": "http://jiscmonitor.jiscinvolve.org/",
            "dc": "http://purl.org/dc/elements/1.1/",
            "dcterms": "http://purl.org/dc/terms/",
            "rioxxterms": "http://rioxx.net/v2-0-beta-1/"
        }
        
        "jm:dateApplied" : "<date APC was applied for by author>",
        "jm:submittedBy" : {
            "name" : "<name of the corresponding author>",
            "id" : "<identifier for author submitting request (ORCID)>",
        }
        "jm:orgUnit" : "<organisational unit the submitting author belongs to>",
        "jm:org" : {
            "name" : "<organisation handling this request>",
            "id" : "<organisation identifier>"
        }
        
        "dc:identifier" : [
            {"type" : "pmcid", "id" : "<europe pubmed central id>"},
            {"type" : "pmid", "id" : "<pubmed id>"},
            {"type" : "doi", "id" : "<doi>"},
            {"type" : "url", "id" : "<url to object>"}
        ],
        
        "dc:source" : {
            "name" : "<name of the journal or other source (e.g. book)>",
            "identifier" : [
                {"type" : "issn", "id" : "<issn of the journal>" },
                {"type" : "doi", "id" : "<doi for the journal or series>" }
            ]
        },
        
        "rioxxterms:author" : [
            {"id" : "<author's orcid>", "value" : "<author name>"}
        ],
        
        "dcterms:publisher" : {
            "name" : "<publisher of the article>",
            "id" : "<publisher identifier>"
        },
        "rioxxterms:type" : "<publication type>",
        "dc:title" : "<title>",
        "rioxxterms:publication_date" : "<publication date>",
        "rioxxterms:project" : [
            {
                "funder_name" : "<name of funder>", 
                "funder_id" : "<id of funder>", 
                "grant_number" : "<funder's grant number>"
            }
        ],
        "jm:apc" : {
            "paid_by" : [
                { 
                    "name" : "<name of organisation>",
                    "id" : "<organisation identifier>",
                    "amount" : <amount paid in native currency>,
                    "currency" : "<currency paid in>"
                    "amount_gbp" : <amount paid in equivalent GBP>
                }
            ],
            "date_paid" : "<date apc paid>",
            "amount" : <amount paid in native currency>,
            "currency" : "<currency paid in>",
            "amount_gbp" : <amount paid in equivalent GBP>,
            "additional_costs" : <additional apc costs in GBP>,
            "discounts" : "<description of any discounts applied>",
            "coaf" : <amount charged to coaf in GBP>
        },
        
        "jm:licence" : {
            "requested" : "<name of licence requested>",
            "received" : true|false,
            "problem_free" : true|false
        },
        
        "jm:notes" : ["<notes associated with the record>"]
    }
}
```

Note that each entity in the data (such as author, publisher, organisation) have space for both a name (ideally from a standard 
list) and an identifier (of unspecified schema).  The hope is that we can at least find a way to uniquely identify these entities
such that we can determine equivalences across the dataset.

QUESTION: do we need to be even more flexible with identifiers here?  Should we have either the id field be a list of opaque identifiers,
or a full fledged "identifier" section with a type and an id?

Descriptions of notable fields, and the requirements for their use are as follows:

* **admin** - this is where we will store all data to do with administering the record within an application.  It will therefore be unlikely to 
be shared via an API, and the values in here should not be held to a requirement to be "standardised".
* **monitor** - this is the field where the main data concerning the APC is held.  This is the data that will be shared via the API, and is
therefore the part of the model expressed with JSON-LD, as it should be "standardised" as much as possible.
* **monitor.jm:dateApplied** - an ISO 8601 formatted date (e.g. 2014-10-16T17:34:03Z)
* **monitor.dc:identifier** - should contain at least a URL to the object (as per RIOXX).  **Mandatory**
* **monitor.dc:source** - the RIOXX profile considers this to principally a journal, but it will take any other object that is a suitable source
such as a book.  **Mandatory where applicable**.
* **monitor.rioxxterms:author**  - as per the RIOXX profile this field is **Mandatory** (although note that it often isn't present)
* **monitor.dc:publisher** - as per the RIOXX profile this field is **Recommended**.
* **monitor.rioxxterms:type** - confirms to the RIOXX profile for controlled vocabulary of terms.  **Mandatory** (although note that it often isn't present).
* **monitor.dc:title** - as per the RIOXX profile this field is **Mandatory**
* **monitor.rioxxterms:project**  - as per the RIOXX profile this field is **Mandatory**
* **monitor.jm:apc** - this field should not be confused with rioxxterms:apc, which has a different purpose.  In this data model this provides a 
wrapper for detailed information about APC payments.
* **monitor.jm:apc.paid_by** - This may contain a list of organisations who in some way contributed to the APC.  They may not have contributed financially, in which case
"amount" can be omitted or set to 0 (this will be the default if not value is provided).  The total of all the amounts in this list MUST add up to the
total amount paid.
* **monitor.jm:licence.received** - was the licence that was ultimately applied to the publication that which the APC paid for?
* **monitor.jm:licence.problem_free** - was the Open Access publication of the material problem free?
* **monitor.jm:notes** - free text content to be supplied by the organisation providing the record.  Can be used to detail any information that is not
codified elsewhere in the data model.


## CRUD API

The specification of the API below is a full imagining of a CRUD interface, which must be validated for usefulness.  We may not want to do all of it.  

Each section also indicates Authentication and Authorisation parameters (AuthNZ) - we do not anticipate implementing these, but they exist to indicate
what would likely be required from a full system/protocol specification.

### Create

Mechanisms to create individual or groups of APC data records.

#### Add a new record

**AuthNZ**: Authenticated User

Create a single record using the APC object specified in the Data Model:

    POST /apc
    [apc object]

Returns 201, and a Location header with the URL for the created object, plus a response body with the URL for the object


### Retrieve

Mechanisms to retrieve APC data records

#### Individual APC Record

**AuthNZ**: None

Get an individual APC record back by id

    GET /apc/<id>

Returns 200 and the APC record as JSON in the body, or 404 if the record could not be found


### Update

#### Replace an APC record by ID

**AuthNZ**: Authenticated User + (Owner of APC Record *OR* Super User) 

Replace an existing APC record by its unique id

    PUT /apc/<id>
    [new apc record]

Returns a 204 if successful, or a 404 if an APC with that ID does not exist


### Delete

#### Delete by ID

**AuthNZ**: Authenticated User + (Owner of APC Record *OR* Super User) 

Delete an existing APC record by its unique id

    DELETE /apc/<id>

Returns a 204 if successful, or a 404 if an APC with that ID does not exist



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
