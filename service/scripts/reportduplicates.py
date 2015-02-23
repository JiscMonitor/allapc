"""Show duplicates in the index of the given field. """

import esprit
import json

count_terms_query = {
    "aggregations": {
        "count_terms": {
            "terms": {
                "field": "<field_to_count>",
                "min_doc_count": "<min threshold>"
            }
        }
    }
}

def detect_dupes(connection, index, doctype, field):
    conn = esprit.raw.Connection(connection, index)
    query = count_terms_query.copy()
    query['aggregations']['count_terms']['terms']['field'] = field
    query['aggregations']['count_terms']['terms']['min_doc_count'] = 2

    resp = esprit.raw.search(conn, doctype, query=query)
    try:
        results = json.loads(resp.text)['aggregations']['count_terms']['buckets']
        maxlen = max([len(result['key']) for result in results])
        rowformat = "{:<%s}{}" % (maxlen + 4)
        print "Duplicate entries for {0} found:".format(field)
        for res in results:
            print rowformat.format(res['key'], res['doc_count'])
    except ValueError:
        print "No duplicates found"

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-c",
                        "--connection",
                        help="Connection to ES, e.g. \"http://localhost:9200\"",
                        default="http://localhost:9200")
    parser.add_argument("-i",
                        "--index",
                        help="Index to use",
                        default="allapc")
    parser.add_argument("type",
                        help="Type to use")
    parser.add_argument("field",
                        help="The field to detect duplicates on")

    args = parser.parse_args()
    detect_dupes(args.connection, args.index, args.type, args.field)
