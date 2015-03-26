from flask import Blueprint, request, url_for, make_response, abort, render_template
from service.models import InstitutionalRecord

blueprint = Blueprint('duplicates', __name__)

@blueprint.route("/report/duplicates")
def index():
    # Check which DOIs are duplicated in the data
    dup_doi = detect_dupes("monitor.dc:identifier.id.exact")

    return render_template("duplicates.html")

count_terms_query = {
    "query": { "match_all" : {} },
    "aggregations": {
        "count_terms": {
            "terms": {
                "field": "<field_to_count>",
                "size": 1000,
                "min_doc_count": "<min threshold>"
            }
        }
    }
}

def detect_dupes(field):
    query = count_terms_query.copy()
    query['aggregations']['count_terms']['terms']['field'] = field
    query['aggregations']['count_terms']['terms']['min_doc_count'] = 2

    resp = InstitutionalRecord.query(count_terms_query)
    dupes = []
    try:
        results = resp['aggregations']['count_terms']['buckets']
        for res in results:
            dupes.append((res['key'], res['doc_count']))
    except ValueError:
        # No duplicates found
        return None

    return dupes
