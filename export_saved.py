#!/usr/bin/env python
"""
export-saved.py

Christopher Su
Exports saved Reddit posts into a HTML file that is ready to be imported into Google Chrome.
"""

from time import time
import argparse
import csv
import logging
import sys

import praw


# # Converter class from https://gist.github.com/raphaa/1327761
class Converter():
    """Converts a CSV instapaper export to a Chrome bookmark file."""

    def __init__(self, file):
        """init method."""
        self._file = file

    def parse_urls(self):
        """Parse the file and returns a folder ordered list."""
        efile = open(self._file)
        urls = csv.reader(efile, dialect='excel')
        parsed_urls = {}
        next(urls)
        for url in urls:
            if not url:
                continue
            else:
                folder = url[3].strip()
            if folder not in list(parsed_urls.keys()):
                parsed_urls[folder] = []
            parsed_urls[folder].append([url[0], url[1]])
        return parsed_urls

    def convert(self):
        """Convert the file."""
        urls = self.parse_urls()
        t = int(time())
        content = ('<!DOCTYPE NETSCAPE-Bookmark-file-1>\n'
                   '<META HTTP-EQUIV="Content-Type" CONTENT="text/html;'
                   ' charset=UTF-8">\n<TITLE>Bookmarks</TITLE>'
                   '\n<H1>Bookmarks</H1>\n<DL><P>\n<DT><H3 ADD_DATE="%(t)d"'
                   ' LAST_MODIFIED="%(t)d">Reddit</H3>'
                   '\n<DL><P>\n' % {'t': t})
        for folder in sorted(list(urls.keys())):
            content += ('<DT><H3 ADD_DATE="%(t)d" LAST_MODIFIED="%(t)d">%(n)s'
                        '</H3>\n<DL><P>\n' % {'t': t, 'n': folder})
            for url in urls[folder]:
                content += ('<DT><A HREF="%s" ADD_DATE="%d">%s</A>\n'
                            % (url[0], t, url[1]))
            content += '</DL><P>\n'
        content += '</DL><P>\n' * 3
        ifile = open('chrome-bookmarks.html', 'w')
        ifile.write(content)


def get_args(argv):
    """get args.

    Args:
        argv (list): List of arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description=(
            'Exports saved Reddit posts into a HTML file '
            'that is ready to be imported into Google Chrome'
        )
    )

    parser.add_argument("-u", "--username", help="pass in username as argument")
    parser.add_argument("-p", "--password", help="pass in password as argument")
    parser.add_argument("-id", "--client-id", help="pass in client id  as argument")
    parser.add_argument("-s", "--client-secret", help="pass in client secret as argument")

    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    parser.add_argument("-up", "--upvoted", help="get upvoted posts instead of saved posts",
                        action="store_true")

    args = parser.parse_args(argv)
    return args


def login(args):
    """login.

    Args:
        args (argparse.Namespace): Parsed arguments.

    Returns:
        Reddit object instance.
    """
    username = None
    password = None
    client_id = None
    client_secret = None
    if args.username and args.password and args.client_id and args.client_secret:
        username = args.username
        password = args.password
        client_id = args.client_id
        client_secret = args.client_secret
    else:
        try:
            import AccountDetails
            username = AccountDetails.REDDIT_USERNAME
            password = AccountDetails.REDDIT_PASSWORD
            client_id = AccountDetails.CLIENT_ID
            client_secret = AccountDetails.CLIENT_SECRET
        except ImportError:
            print(
                'You must specify a username, password, client id, '
                'and client secret, either in an AccountDetails file '
                'or by passing them as arguments (run the script with '
                'the --help flag for more info).'
            )
            exit(1)

    if not username or not password or not client_id or not client_secret:
        print('You must specify ALL the arguments')
        print(
            'Either use the options (write [-h] for help menu) '
            'or add them to an AccountDetails module.'
        )
        exit(1)
    return {
        'username': username,
        'password': password,
        'client_id': client_id,
        'client_secret': client_secret,
    }


def get_csv_rows(seq):
    """get csv rows.

    Args:
        seq (list): List of Reddit item.

    Returns:
        list: Parsed reddit item.
    """
    csv_rows = []

    # filter items for link
    for idx, i in enumerate(seq, 1):
        logging.debug('processing item #{}'.format(idx))

        if not hasattr(i, 'title'):
            i.title = i.link_title

        # Fix possible buggy utf-8
        title = i.title.encode('utf-8').decode('utf-8')
        logging.debug('title: {}'.format(title))
        try:
            folder = str(i.subreddit)
        except AttributeError:
            folder = "None"
        if callable(i.permalink):
            permalink = i.permalink()
        else:
            permalink = i.permalink
        csv_rows.append([permalink, title, None, folder])

    return csv_rows


def write_csv(csv_rows):
    """write csv using csv module.

    Args:
        csv_rows (list): CSV rows.
    """
    # csv setting
    csv_fields = ['URL', 'Title', 'Selection', 'Folder']
    delimiter = ','

    # write csv using csv module
    with open("export-saved.csv", "w") as f:
        csvwriter = csv.writer(f, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(csv_fields)
        for row in csv_rows:
            csvwriter.writerow(row)


def main():
    """main func."""
    args = get_args(sys.argv[1:])

    # set logging config
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    # login
    account = login(args=args)
    client_id = account['client_id']
    client_secret = account['client_secret']
    username = account['username']
    password = account['password']
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent='export saved 2.0',
                         username=username,
                         password=password)
    logging.debug('Login succesful')

    seq = None
    if args.upvoted:
        seq = reddit.redditor(username).upvoted(limit=None)
    else:
        seq = reddit.redditor(username).saved(limit=None)

    csv_rows = get_csv_rows(seq)

    # write csv using csv module
    write_csv(csv_rows)
    logging.debug('csv written.')

    # convert csv to bookmark
    converter = Converter("export-saved.csv")
    converter.convert()
    logging.debug('html written.')

    sys.exit(0)


if __name__ == "__main__":
    main()
