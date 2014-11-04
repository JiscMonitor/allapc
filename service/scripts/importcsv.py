if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--source", help="path to source csv to import")
    parser.add_argument("-i", "--institution", help="name of institution to import as (will override the csv value if present)")

    args = parser.parse_args()

    if not args.source:
        print "Please specify an source file with the -s option"
        exit()

    from octopus.core import app, initialise
    initialise()

    from service import importer
    importer.import_csv(args.source, args.institution)

