# ALL APC

An APC demonstrator collection/dissemination API, and reports based on the data it can collect

## Data Model

The data model presented below represents a JSON-based object structure indicating the hierarchy and therefore relationships
of the data elements in the object.  It has been expressed using the syntax of [JSON-LD](http://json-ld.org/).

This is the format that we will both store and expose the data over the API for this application.

```python
{
    "@context": {
        "jm": "http://jiscmonitor.jiscinvolve.org/",
        "dc": "http://purl.org/dc/elements/1.1/",
        "dcterms": "http://purl.org/dc/terms/",
        "rioxxterms": "http://rioxx.net/v2-0-beta-1/"
    }
    
    "id" : "<opaque internal record identifier>",
    
    "jm:dateApplied" : "<date APC was applied for by author>",
    "jm:submittedBy" : "<identifier for author submitting request (ORCID)>",
    "jm:orgUnit" : "<organisational unit the submitting author belongs to>",
    "jm:org" : "<organisation handling this request>",
    
    "dc:identifier" : [
        {"type" : "pmcid", "value" : "<europe pubmed central id>"},
        {"type" : "pmid", "value" : "<pubmed id>"},
        {"type" : "doi", "value" : "<doi>"}
    ],
    
    "dc:source" : {
        "journal" : "<name of the journal>",
        "value" : "<issn of the journal>"
    },
    
    "rioxxterms:author" : [
        {"id" : "<author's orcid>", "value" : "<author name>"}
    ],
    
    "dcterms:publisher" : "<publisher of the article>",
    "rioxxterms:type" : "<publication type>",
    "dc:title" : "<title>",
    "rioxxterms:publication_date" : "<publication date>",
    "rioxxterms:project" : [
        {
            "funder_name" : "<name of funder>", 
            "funder_id" : "<id of funder>", 
            "value" : "<funder's grant number>"
        }
    ],
    "jm:apc" : {
        "paid_from" : [ "<name of organisation>"],
        "date_paid" : "<date apc paid>",
        "amount_paid" : <amount paid in native currency>,
        "currency" : "<currency paid in>",
        "amount_paid_gbp" : <amount paid in equivalent GBP>,
        "additional_costs" : <additional apc costs>,
        "discounts" : "<description of any discounts applied>",
        "coaf" : <amount charged to coaf in GBP>
    },
    
    "jm:license" : {
        "requested" : "<name of licence requested>",
        "received" : true|false,                     # was the licence as requested
        "problem_free" : true|false                  # problem free OA publication?
    },
    
    "jm:notes" : ["<notes associated with the record>"]
    
    "jm:admin" : {
        "owner" : "<user who provided this record originally>"
    }
}
```


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


#### Add a list of records

**AuthNZ**: Authenticated User

Create records in bulk either in the standard format or from a CSV

    POST /list
    Content-Type: application/json OR text/csv
    [list of apc objects or csv]
    
    
Returns 201 if all records can be successfully imported, or a 400 if any of the records could not be imported.

In the event of success the response body contains a list of URLs to the created resources.

*Note: in order to be fully REST compliant, we must provide a "list" resource upon which to carry out such bulk operations*

*Note 2: lists of records must succeed or fail in bulk otherwise we require a complex return body to describe to the 
client what happened, and clients will need to be sufficiently advanced to handle such a return.  As such, for simplicity
we should require operations either clearly succeed or clearly fail, rather than some in-between state*


### Retrieve

Mechanisms to retrieve APC data records

#### Individual APC Record

**AuthNZ**: None

Get an individual APC record back by id

    GET /apc/<id>

Returns 200 and the APC record as JSON in the body, or 404 if the record could not be found


#### Search

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


#### Change List

**AuthNZ**: None

Obtain the changes to the set of records in a given time period

    GET /changes?from=<date>&until=<date>&size=<page size>&page=<page number>

Returns the results in the format provided by Elasticsearch

*Note: the change list is a special case of an Elasticsearch query - it will effectively proxy for a time-boxed, ordered
query against the index, hence the reason that the result set will be Elasticsearch formatted*

### Update

#### Replace an APC record by ID

**AuthNZ**: Authenticated User + (Owner of APC Record *OR* Super User) 

Replace an existing APC record by its unique id

    PUT /apc/<id>
    [new apc record]

Returns a 204 if successful, or a 404 if an APC with that ID does not exist

#### Update a list of records

**AuthNZ**: Authenticated User + (Owner of all APC Records *OR* Super User) 

Update APCs in bulk (essentially identical to **Add a list of records**)

    POST /list
    Content-Type: application/json OR text/csv
    [list of apc objects or csv]

Each record must provide an identifier for the existing record that it replaces.

Mixed create/replace operations can be supported - records which provide an ID will be overwritten, record which do not will create new entries.

Returns 200 if all records can be successfully imported, or a 400 if any of the records could not be imported.

In the event of success the response body contains a list of URLs to the created resources and whether they were creates or updates

*Note: similar comments as appear in "Add a list of records" apply here with regard to having an operation which either clearly
completes or clearly fails, rather than some in-between state*


### Delete

#### Delete by ID

**AuthNZ**: Authenticated User + (Owner of APC Record *OR* Super User) 

Delete an existing APC record by its unique id

    DELETE /apc/<id>

Returns a 204 if successful, or a 404 if an APC with that ID does not exist

#### Delete list of records

**AuthNZ**: Authenticated User + (Owner of all APC Records *OR* Super User) 

Delete a list of records as identified by their unique ids

    DELETE /list/<id1>,<id2>,...
    
Returns a 204 if all records can be successfully deleted (and are), or a 404 if any of the records do not exist

*Note: similar comments as appear in "Add a list of records" apply here with regard to having an operation which either clearly
completes or clearly fails, rather than some in-between state*

## Analytics API

This section describes a theoretical API endpoint which would provide analytical information which could be used in 
a variety of reporting use cases.

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
