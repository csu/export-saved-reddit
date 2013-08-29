#!/usr/bin/env python
'''
export-saved.py
Christopher Su
Exports saved Reddit posts into a HTML file that is ready to be imported into Google Chrome.
'''

import csv
import os
import sys
from time import time

import praw
import AccountDetails

## from https://gist.github.com/raphaa/1327761
class Converter():
    """Converts an CSV instapaper export to a Chrome bookmark file."""
 
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
                   ' LAST_MODIFIED="%(t)d">Instapaper</H3>'
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
    r = praw.Reddit(user_agent='Subot 1.0')
    r.login(AccountDetails.REDDIT_USERNAME, AccountDetails.REDDIT_PASSWORD)
    export_csv = 'URL,Title,Selection,Folder\n'
    for i in r.user.get_saved():
        export_csv += ("%s,%s,,%s\n" % (str(i.permalink), i.title, str(i.subreddit)))
    with open("export-saved.csv", "w") as f:
        f.write(export_csv)
    converter = Converter("export-saved.csv")
    converter.convert()
    sys.exit(0)

if __name__ == "__main__":
    main()