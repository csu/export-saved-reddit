"""test module."""
from itertools import product
from unittest import mock
import argparse
import os

import pytest


@pytest.mark.parametrize(
    'argv, exp_res',
    [(
        [],
        {
            'all': False, 'upvoted': False, 'verbose': False,
            'client_secret': None, 'password': None,
            'username': None, 'client_id': None,
            'version': False
        }
    )]
)
def test_get_args(argv, exp_res):
    """test func."""
    from export_saved import get_args
    res = get_args(argv)
    assert res.__dict__ == exp_res


def get_str_permalink():
    """Return string permalink."""
    return 'permalink'


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
        (
            argparse.Namespace(
                title='title', permalink=get_str_permalink, created='invalid'),
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


def test_write_csv_with_str(tmpdir):
    """test func."""
    file_name = os.path.join(tmpdir.strpath, 'test.csv')
    csv_rows = ['url1', 'title1', '10', '', 'folder1']
    from export_saved import write_csv
    write_csv(csv_rows, file_name)


def test_write_csv():
    """test func."""
    csv_rows = [['url1', 'title1', '10', '', 'folder1']]
    with mock.patch('export_saved.open') as m_open:
        from export_saved import write_csv
        write_csv(csv_rows)
        m_open.return_value.__enter__.return_value.assert_has_calls([
            mock.call.write('URL,Title,Created,Selection,Folder\r\n'),
            mock.call.write('url1,title1,10,,folder1\r\n')
        ])


def test_login():
    """test func."""
    args = mock.Mock()
    account = {
        'username': mock.Mock(),
        'password': mock.Mock(),
        'client_id': mock.Mock(),
        'client_secret': mock.Mock(),
    }
    with mock.patch('export_saved.praw') as m_praw, \
            mock.patch('export_saved.account_details') as m_ad:
        m_ad.return_value = account
        from export_saved import login
        res = login(args)
        m_ad.assert_called_once_with(args=args)
        assert res == m_praw.Reddit.return_value


@pytest.mark.parametrize(
    'username, password, client_id, client_secret',
    product([None, mock.Mock()], repeat=4)
)
def test_account_details(username, password, client_id, client_secret):
    """test account details."""
    ns_kwargs = {
        'username': username,
        'password': password,
        'client_id': client_id,
        'client_secret': client_secret,
    }
    args = argparse.Namespace(**ns_kwargs)
    cond_match = all(ns_kwargs[key] for key in ns_kwargs)
    from export_saved import account_details
    if not cond_match:
        with pytest.raises(SystemExit):
            with mock.patch.dict('sys.modules', {'AccountDetails': None}):
                account_details(args)
        return
    res = account_details(args)
    assert res == ns_kwargs


def test_process():
    """test func."""
    reddit = mock.Mock()
    seq = mock.Mock()
    file_name = 'filename'
    folder_name = 'folder_name'
    with mock.patch('export_saved.get_csv_rows'),\
            mock.patch('export_saved.write_csv'),\
            mock.patch('export_saved.Converter') as m_converter:
        from export_saved import process
        # run
        process(reddit, seq, file_name, folder_name)
        # test
        m_converter.assert_has_calls([
            mock.call('filename.csv', 'filename.html', folder_name=folder_name),
            mock.call().convert()
        ])


@pytest.mark.parametrize('key', ['upvoted', 'saved', 'comments', 'submissions'])
def test_save(key):
    """test func."""
    reddit = mock.Mock()
    seq = mock.Mock()
    if key in ('saved', 'upvoted'):
        getattr(reddit.user.me.return_value, key).return_value = seq
    else:
        getattr(reddit.user.me.return_value, key).new.return_value = seq
    with mock.patch('export_saved.process') as m_p:
        import export_saved
        getattr(export_saved, 'save_{}'.format(key))(reddit)
        m_p.assert_called_once_with(
            reddit, seq, 'export-{}'.format(key), "Reddit - {}".format(key.title()))


@pytest.mark.parametrize('verbose, upvoted, all', product([True, False], repeat=3))
def test_main(verbose, upvoted, all):
    """test func"""
    reddit = mock.Mock()
    with mock.patch('export_saved.get_args') as m_ga, \
            mock.patch('export_saved.logging') as m_logging, \
            mock.patch('export_saved.login') as m_login, \
            mock.patch('export_saved.save_upvoted'), \
            mock.patch('export_saved.save_saved'), \
            mock.patch('export_saved.save_submissions'), \
            mock.patch('export_saved.save_comments'):
        m_login.return_value = reddit
        m_ga.return_value = argparse.Namespace(
            verbose=verbose,
            upvoted=upvoted,
            all=all,
            version=False
        )
        import export_saved
        # run
        with pytest.raises(SystemExit):
            export_saved.main()
        if verbose:
            m_logging.basicConfig.assert_called_once_with(level=m_logging.DEBUG)
        if upvoted:
            export_saved.save_upvoted.assert_called_once_with(reddit)
        elif all:
            export_saved.save_upvoted.assert_called_once_with(reddit)
            export_saved.save_saved.assert_called_once_with(reddit)
            export_saved.save_submissions.assert_called_once_with(reddit)
            export_saved.save_comments.assert_called_once_with(reddit)
        else:
            export_saved.save_saved.assert_called_once_with(reddit)
