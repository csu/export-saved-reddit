#!/usr/bin/env python
'''
export-saved.py
Christopher Su
Exports saved Reddit posts into a HTML file that is ready to be imported into Google Chrome.
'''

import argparse
import csv
import logging
import os
import sys
from time import time

import praw

import AccountDetails


## Converter class from https://gist.github.com/raphaa/1327761
class Converter():
    """Converts a CSV instapaper export to a Chrome bookmark file."""
 
    def __init__(self, file):
        self._file = file
 
    def parse_urls(self):
        """Parses the file and returns a folder ordered list."""
        efile = open(self._file)
        urls = csv.reader(efile, dialect='excel')
        parsed_urls = {}
        urls.next()
        for url in urls:
            folder = url[3].strip()
            if folder not in parsed_urls.keys():
                parsed_urls[folder] = []
            parsed_urls[folder].append([url[0], url[1]])
        return parsed_urls
 
    def convert(self):
        """Converts the file."""
        urls = self.parse_urls()
        t = int(time())
        content = ('<!DOCTYPE NETSCAPE-Bookmark-file-1>\n'
                   '<META HTTP-EQUIV="Content-Type" CONTENT="text/html;'
                   ' charset=UTF-8">\n<TITLE>Bookmarks</TITLE>'
                   '\n<H1>Bookmarks</H1>\n<DL><P>\n<DT><H3 ADD_DATE="%(t)d"'
                   ' LAST_MODIFIED="%(t)d">Reddit</H3>'
                   '\n<DL><P>\n' % {'t': t})
        for folder in urls.keys():
            content += ('<DT><H3 ADD_DATE="%(t)d" LAST_MODIFIED="%(t)d">%(n)s'
                        '</H3>\n<DL><P>\n' % {'t': t, 'n': folder})
            for url in urls[folder]:
                content += ('<DT><A HREF="%s" ADD_DATE="%d">%s</A>\n'
                            % (url[0], t, url[1]))
            content += '</DL><P>\n'
        content += '</DL><P>\n' * 3
        ifile = open('chrome-bookmarks.html', 'w')
        ifile.write(content)


def main():
    """main func."""
    parser = argparse.ArgumentParser(
        description=(
            'Exports saved Reddit posts into a HTML file'
            'that is ready to be imported into Google Chrome'
        )
    )
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    args = parser.parse_args()

    # set logging config
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    # login
    r = praw.Reddit(user_agent='export saved 1.0')
    r.login(AccountDetails.REDDIT_USERNAME, AccountDetails.REDDIT_PASSWORD)
    logging.debug('Login succesful')

    # csv setting
    csv_fields = ['URL', 'Title', 'Selection', 'Folder']
    csv_rows = []
    delimiter = ','

    # filter saved item for link
    for idx, i in enumerate(r.user.get_saved(limit=None, time='all'), 1):
        logging.debug('processing {}#'.format(idx))
        if not hasattr(i, 'title'):
           i.title = i.link_title
        try:
            folder = str(i.subreddit)
        except AttributeError:
            folder = "None"
        csv_rows.append([i.permalink.encode('utf-8'), i.title.encode('utf-8'),None, folder])

    # write csv using csv module
    with open("export-saved.csv", "w") as f:
        csvwriter = csv.writer(f, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(csv_fields)
        for row in csv_rows:
            csvwriter.writerow(row)
    logging.debug('csv written.')

    # convert csv to bookmark
    converter = Converter("export-saved.csv")
    converter.convert()
    logging.debug('html written.')

    sys.exit(0)

if __name__ == "__main__":
    main()
