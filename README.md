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
}
```
