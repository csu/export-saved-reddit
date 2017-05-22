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


__version__ = '0.1.1'


# # Converter class from https://gist.github.com/raphaa/1327761
class Converter():
    """Converts a CSV instapaper export to a Chrome bookmark file."""

    def __init__(self, file, html_file=None, folder_name="Reddit"):
        """init method."""
        self._file = file
        self._html_file = html_file if html_file is not None else 'chrome-bookmarks.html'
        self._folder_name = folder_name if folder_name is not None else 'Reddit'

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
                folder = url[4].strip()
            if folder not in list(parsed_urls.keys()):
                parsed_urls[folder] = []
            parsed_urls[folder].append([url[0], url[1], url[2]])
        return parsed_urls

    def convert(self):
        """Convert the file."""
        urls = self.parse_urls()
        t = int(time())
        content = ('<!DOCTYPE NETSCAPE-Bookmark-file-1>\n'
                   '<META HTTP-EQUIV="Content-Type" CONTENT="text/html;'
                   ' charset=UTF-8">\n<TITLE>Bookmarks</TITLE>'
                   '\n<H1>Bookmarks</H1>\n<DL><P>\n<DT><H3 ADD_DATE="%(t)d"'
                   ' LAST_MODIFIED="%(t)d">%(folder_name)s</H3>'
                   '\n<DL><P>\n' % {'t': t, 'folder_name': self._folder_name})

        for folder in sorted(list(urls.keys())):
            content += ('<DT><H3 ADD_DATE="%(t)d" LAST_MODIFIED="%(t)d">%(n)s'
                        '</H3>\n<DL><P>\n' % {'t': t, 'n': folder})
            for url, title, add_date in urls[folder]:
                content += ('<DT><A HREF="%(url)s" ADD_DATE="%(created)d"'
                            ' LAST_MODIFIED="%(created)d">%(title)s</A>\n'
                            % {'url': url, 'created': int(add_date), 'title': title})
            content += '</DL><P>\n'
        content += '</DL><P>\n' * 3
        ifile = open(self._html_file, 'wb')
        try:
            ifile.write(content)
        except TypeError:
            ifile.write(content.encode('utf-8', 'ignore'))


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
            'that is ready to be imported into Google Chrome or Firefox'
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
    parser.add_argument("-all", "--all", help="get upvoted, saved, comments and submissions",
                        action="store_true")
    parser.add_argument("-V", "--version", help="get program version.", action="store_true")

    args = parser.parse_args(argv)
    return args


def login(args):
    """login method.

    Args:
        args (argparse.Namespace): Parsed arguments.

    Returns: a logged on praw instance
    """
    # login
    account = account_details(args=args)
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
    return reddit


def account_details(args):
    """Extract account informations.

    Args:
        args (argparse.Namespace): Parsed arguments.

    Returns:
        Account details
    """
    username = None
    password = None
    client_id = None
    client_secret = None
    if args and args.username and args.password and args.client_id and args.client_secret:
        username = args.username
        password = args.password
        client_id = args.client_id
        client_secret = args.client_secret
    else:
        try:  # pragma: no cover
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

    if not username or not password or not client_id or not client_secret:  # pragma: no cover
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


def get_csv_rows(reddit, seq):
    """get csv rows.

    Args:
        reddit: reddit praw's instance
        seq (list): List of Reddit item.

    Returns:
        list: Parsed reddit item.
    """
    csv_rows = []
    reddit_url = reddit.config.reddit_url

    # filter items for link
    for idx, i in enumerate(seq, 1):
        logging.debug('processing item #{}'.format(idx))

        if not hasattr(i, 'title'):
            i.title = i.link_title

        # Fix possible buggy utf-8
        title = i.title.encode('utf-8').decode('utf-8')
        try:
            logging.debug('title: {}'.format(title))
        except UnicodeEncodeError:
            logging.debug('title: {}'.format(title.encode('utf8', 'ignore')))

        try:
            created = int(i.created)
        except ValueError:
            created = 0

        try:
            folder = str(i.subreddit).encode('utf-8').decode('utf-8')
        except AttributeError:
            folder = "None"

        if callable(i.permalink):
            permalink = i.permalink()
        else:
            permalink = i.permalink
        permalink = permalink.encode('utf-8').decode('utf-8')

        csv_rows.append([reddit_url + permalink, title, created, None, folder])

    return csv_rows


def write_csv(csv_rows, file_name=None):
    """write csv using csv module.

    Args:
        csv_rows (list): CSV rows.
        file_name (string): filename written
    """
    file_name = file_name if file_name is not None else 'export-saved.csv'

    # csv setting
    csv_fields = ['URL', 'Title', 'Created', 'Selection', 'Folder']
    delimiter = ','

    # write csv using csv module
    try:
        with open(file_name, "wb") as f:
            csvwriter = csv.writer(f, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(csv_fields)
            for row in csv_rows:
                csvwriter.writerow(row)
    except TypeError:
        with open(file_name, "w") as f:
            csvwriter = csv.writer(f, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(csv_fields)
            for row in csv_rows:
                try:
                    csvwriter.writerow(row)
                except UnicodeEncodeError:
                    csvwriter.writerow(str(row).encode('utf-8', 'ignore'))


def process(reddit, seq, file_name, folder_name):
    """Write csv and html from a list of results.

    Args:
      reddit: reddit praw's instance
      seq (list): list to write
      file_name: base file name without extension
      folder_name: top level folder name for the exported html bookmarks
    """
    csv_rows = get_csv_rows(reddit, seq)
    # write csv using csv module
    write_csv(csv_rows, file_name + ".csv")
    logging.debug('csv written.')
    # convert csv to bookmark
    converter = Converter(file_name + ".csv", file_name + ".html",
                          folder_name=folder_name)
    converter.convert()
    logging.debug('html written.')


def save_upvoted(reddit):
    """ save upvoted posts """
    seq = reddit.user.me().upvoted(limit=None)
    process(reddit, seq, "export-upvoted", "Reddit - Upvoted")


def save_saved(reddit):
    """ save saved posts """
    seq = reddit.user.me().saved(limit=None)
    process(reddit, seq, "export-saved", "Reddit - Saved")


def save_comments(reddit):
    """ save comments posts """
    seq = reddit.user.me().comments.new(limit=None)
    process(reddit, seq, "export-comments", "Reddit - Comments")


def save_submissions(reddit):
    """ save saved posts """
    seq = reddit.user.me().submissions.new(limit=None)
    process(reddit, seq, "export-submissions", "Reddit - Submissions")


def main():
    """main func."""
    args = get_args(sys.argv[1:])

    # set logging config
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    # print program version.
    if args.version:
        print(__version__)
        return

    reddit = login(args=args)
    if args.upvoted:
        save_upvoted(reddit)
    elif args.all:
        save_upvoted(reddit)
        save_saved(reddit)
        save_submissions(reddit)
        save_comments(reddit)
    else:
        save_saved(reddit)

    sys.exit(0)


if __name__ == "__main__":  # pragma: no cover
    main()
