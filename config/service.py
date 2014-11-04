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
CLIENTJS_INST_QUERY_ENDPOINT = "/inst_query"