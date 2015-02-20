"""Show duplicates in the index of the given field. """

import esprit

def detect_dupes(connection, type, ):
    conn = esprit.raw.Connection("http://localhost:9200", "allapc")

    for results in esprit.tasks.scroll(conn, TYPE, ):



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

    detect_dupes(args.connection, args.type)
