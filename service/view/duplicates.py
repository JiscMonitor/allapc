from flask import Blueprint, url_for, render_template
from service.models import InstitutionalRecord
import json

blueprint = Blueprint('duplicates', __name__)

count_terms_query = {
    "query": {"match_all": {}},
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

doi_query = {
    "query" : {
        "query_string" : {
            "query" : "<DOI>",
            "default_operator" : "OR"
        }
    }
}

# A list of [ (duplicate_val, count) ]
dupes_list = []

@blueprint.route("/report/duplicates")
def index():
    # Check which DOIs are duplicated in the data
    doi_field = "monitor.dc:identifier.id.exact"
    x = detect_dupes(doi_field)
    if x:
        return render_template("duplicates.html", field=doi_field, duplicates=dupes_list)
    else:
        return "Something went wrong. Maybe there were no duplicates!"

def detect_dupes(field):
    query = count_terms_query.copy()
    query['aggregations']['count_terms']['terms']['field'] = field
    query['aggregations']['count_terms']['terms']['min_doc_count'] = 2

    resp = InstitutionalRecord.query(count_terms_query)
    try:
        results = resp['aggregations']['count_terms']['buckets']
        for res in results:
            dupes_list.append((res['key'], res['doc_count']))
        return True
    except ValueError:
        # No duplicates found
        return False

@blueprint.app_template_filter()
def build_doi_search_url(doi):
    this_doi_query = doi_query.copy()
    this_doi_query["query"]["query_string"]["query"] = "\"" + doi + "\""
    url = url_for('search', source=json.dumps(doi_query, separators=(',', ':')))
    return url.replace('+', ' ')

