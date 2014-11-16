# overrides for the webapp deployment
DEBUG = True
PORT = 5000
SSL = False
THREADED = True

# elasticsearch back-end connection settings
ELASTIC_SEARCH_HOST = "http://localhost:9200"
ELASTIC_SEARCH_INDEX = "allapc"

# Classes from which to retrieve ES mappings to be used in this application
ELASTIC_SEARCH_MAPPINGS = [
    "service.dao.InstitutionalRecordDAO",
    "service.dao.APCRecordDAO"
]

# Query route configuration
QUERY_ROUTE = {
    "inst_query" : {                            # the URL route at which it is mounted
        "institutional" : {                     # the URL name for the index type being queried
            "auth" : False,                     # whether the route requires authentication
            "role" : None,                      # if authenticated, what role is required to access the query endpoint
            "filters" : [],                     # names of the standard filters to apply to the query
            "dao" : "service.dao.InstitutionalRecordDAO"       # classpath for DAO which accesses the underlying ES index
        }
    }
}

# query endpoint for the above inst_query for the javascript UI
CLIENTJS_INST_QUERY_ENDPOINT = "/inst_query/institutional"

AUTOCOMPLETE_COMPOUND = {
    "publisher" : {                             # name of the autocomplete, as represented in the URL (have as many of these sections as you need)
        "fields" : ["monitor.dcterms:publisher.name"],     # fields to return in the compound result
        "field_name_map" : {                    # map field name to name it will be referred to in the result
            "monitor.dcterms:publisher.name" : "publisher"
        },
        "filters" : {                           # filters to apply to the result set
            "monitor.dcterms:publisher.name.exact" : {                    # field on which to filter
                "start_wildcard" : True,        # apply start wildcard?
                "end_wildcard": True,           # apply end wildcard?
                "boost" : 1.0                   # boost to apply to matches on this field
            }
        },
        "input_filter" : lambda x : x ,         # function to apply to an incoming string before being applied to the es query
        "default_size" : 10,                    # if no size param is specified, this is how big to make the response
        "max_size" : 25,                        # if a size param is specified, this is the limit above which it won't go
        "dao" : "service.dao.InstitutionalRecordDAO"           # classpath for DAO which accesses the underlying ES index
    }
}

AUTOCOMPLETE_TERM = {
    "publisher" : {                                  # name of the autocomplete, as represented in the URL (have as many of these sections as you need)
        "filter" : {                            # The filter to apply to the result set
            "monitor.dcterms:publisher.name.exact" : {                    # field on which to apply the filter
                "start_wildcard" : True,        # apply start wildcard
                "end_wildcard" : True          # apply end wildcard
            }
        },
        "facet" : "monitor.dcterms:publisher.name.exact",                 # facet from which to get our results
        "input_filter" : lambda x : x,          # function to apply to an incoming string before being applied to the es query
        "default_size" : 10,                    # if no size param is specified, this is how big to make the response
        "max_size" : 25,                        # if a size param is specified, this is the limit above which it won't go
        "dao" : "service.dao.InstitutionalRecordDAO"             # classpath for DAO which accesses the underlying ES index
    }
}