"""Polyglot Import CSV

Usage: polyglotimportcsv.py [OPTIONS] CSVFILE

  CSVFILE: CSV file to be imported

Options:
  --dbconfig FILENAME             JSON database configuration file. If
                                  omitted, there will be needed to pass
                                  database credentials through command line.
  -d, --database [postgres|mongodb|cassandra|redis|neo4j]
  --entity TEXT
  --rel TEXT
  --help                          Show this message and exit.
"""