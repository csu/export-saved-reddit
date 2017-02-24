"""test module."""
from unittest import mock
import argparse

import pytest


@pytest.mark.parametrize(
    'argv, exp_res',
    [(
        [],
        {
            'all': False, 'upvoted': False, 'verbose': False,
            'client_secret': None, 'password': None,
            'username': None, 'client_id': None
        }
    )]
)
def test_get_args(argv, exp_res):
    """test func."""
    from export_saved import get_args
    res = get_args(argv)
    assert res.__dict__ == exp_res


@pytest.mark.parametrize(
    'item, csv_rows',
    [
        (
            argparse.Namespace(
                link_title='link_title', subreddit='subreddit',
                permalink='permalink', created='10'),
            ['https://www.reddit.com/permalink', 'link_title', 10, None, 'subreddit']
        ),
        (
            argparse.Namespace(
                title='title', permalink='permalink', created='invalid'),
            ['https://www.reddit.com/permalink', 'title', 0, None, 'None']
        ),
    ]
)
def test_get_csv_rows(item, csv_rows):
    """test func."""
    from export_saved import get_csv_rows
    reddit = mock.Mock()
    reddit.config.reddit_url = "https://www.reddit.com/"
    res = get_csv_rows(reddit, seq=[item])
    assert res == [csv_rows]


def test_write_csv():
    """test func."""
    csv_rows = [['url1', 'title1', 10, None, 'folder1']]
    with mock.patch('export_saved.open') as m_open:
        from export_saved import write_csv
        write_csv(csv_rows)
        m_open.return_value.__enter__.return_value.assert_has_calls([
            mock.call.write('URL,Title,Created,Selection,Folder\r\n'),
            mock.call.write('url1,title1,10,,folder1\r\n')
        ])
