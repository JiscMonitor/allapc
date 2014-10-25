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