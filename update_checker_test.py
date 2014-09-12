#!/usr/bin/env python
import sys
import unittest
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO  # NOQA
from update_checker import UpdateChecker, update_check


class UpdateCheckerTest(unittest.TestCase):
    def test_bad_package(self):
        checker = UpdateChecker()
        self.assertFalse(checker.check('update_checker_slkdflj', '0.0.1'))

    def test_bad_url(self):
        checker = UpdateChecker('http://sdlkjsldfkjsdlkfj.com')
        self.assertFalse(checker.check('praw', '0.0.1'))

    def test_successful(self):
        checker = UpdateChecker()
        result = checker.check('update_checker', '0.0.1')
        self.assertTrue(result is not None)

    def test_update_check_failed(self):
        prev_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            update_check('update_checker_slkdflj', '0.0.1')
        finally:
            result = sys.stdout
            sys.stdout = prev_stdout
        self.assertTrue(len(result.getvalue()) == 0)

    def test_update_check_successful(self):
        prev_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            update_check('update_checker', '0.0.1')
        finally:
            result = sys.stdout
            sys.stdout = prev_stdout
        self.assertTrue(len(result.getvalue()) > 0)


if __name__ == '__main__':
    unittest.main()
