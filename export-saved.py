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
import argparse

import praw
from django.template.defaultfilters import default
try : 
    import AccountDetails
    ACCOUNT_DETAILS_OPTION = True
except ImportError:
    ACCOUNT_DETAILS_OPTION = False


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
 
    def convert(self,html_filename):
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
        ifile = open(html_filename, 'w')
        ifile.write(content)

def main(args):
    # check arg
    if args.user is '' :
        if ACCOUNT_DETAILS_OPTION is True and AccountDetails.REDDIT_USERNAME is not '' :
            reddit_username = AccountDetails.REDDIT_USERNAME
        else : #throw error
            print 'No username is given.'
            sys.exit(1)
    else : 
        reddit_username = args.user
        
    if args.password is '' :
        if ACCOUNT_DETAILS_OPTION is True and AccountDetails.REDDIT_PASSWORD is not '' :
            reddit_password = AccountDetails.REDDIT_PASSWORD
        else : #throw error
            print 'No password is given.'
            sys.exit(1)
    else : 
        reddit_password = args.password
    
    r = praw.Reddit(user_agent='export-saved 1.1') 
    '''last user agent contain word bot which print a warning. change into "export-saved"'''
    r.login(reddit_username, reddit_password)
    export_csv = 'URL,Title,Selection,Folder\n'
    for i in r.user.get_saved(limit=None, time='all'):
        if not hasattr(i, 'title'):
           i.title = i.link_title
        export_csv += ("%s,%s,,%s\n" % (i.permalink.encode('utf-8'), i.title.encode('utf-8'), str(i.subreddit)))
    with open(args.csv_output, "w") as f:
        f.write(export_csv)
    converter = Converter(args.csv_output)
    converter.convert(args.html_output)
    sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Exports saved Reddit posts into a HTML file that is ready to be imported into Google Chrome.')
    parser.add_argument('--user', default='',help='Reddit username.')
    parser.add_argument('--password', default='',help='Reddit user password.')
    parser.add_argument('csv_output',default="export-saved.csv",help='path to csv file.')
    parser.add_argument('html_output',default='chrome-bookmarks.html',help='path to html bookmark file.')
    args = parser.parse_args()

    main(args)