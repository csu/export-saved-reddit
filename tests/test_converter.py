"""test class."""
import os
from unittest import mock

import pytest


def test_init():
    """test init."""
    file_ = mock.Mock()
    from export_saved import Converter
    obj = Converter(file=file_)
    assert obj._file == file_


@pytest.mark.parametrize(
    'urls_lists, exp_res',
    [
        (
            [
                ['header0', 'header1', 'header2', 'header3'],
                ['url0', 'url1', None, 'folder1'],
                ['url2', 'url3', None, 'folder2'],
                ['url4', 'url5', None, 'folder1'],
            ],
            {
                'folder1': [
                    ['url0', 'url1'],
                    ['url4', 'url5'],
                ],
                'folder2': [
                    ['url2', 'url3']
                ]
            }
        )
    ]
)
def test_parse_url(urls_lists, exp_res):
    """test method."""
    with mock.patch('export_saved.open'), \
            mock.patch('export_saved.csv') as m_csv:
        m_csv.reader.return_value = iter(urls_lists)
        from export_saved import Converter
        obj = Converter(file=mock.Mock())
        res = obj.parse_urls()
        assert res == exp_res


def test_convert():
    """test method."""
    parse_urls_result = {
        'folder1': [
            ['url0', 'url1'],
            ['url4', 'url5'],
        ],
        'folder2': [
            ['url2', 'url3']
        ]
    }
    ifile = mock.Mock()
    exp_bookmark_html = os.path.join(os.path.dirname(__file__), 'convert_result.html')
    with open(exp_bookmark_html) as ff:
        exp_bookmark_html_text = ff.read()
    with mock.patch('export_saved.open') as m_open, \
            mock.patch('export_saved.time', return_value=0):
        m_open.return_value = ifile
        from export_saved import Converter
        obj = Converter(file=mock.Mock())
        obj.parse_urls = mock.Mock(return_value=parse_urls_result)
        obj.convert()
        content = ifile.write.call_args[0][0]
        for exp_line, c_line in zip(exp_bookmark_html_text.splitlines(), content.splitlines()):
            assert exp_line == c_line
