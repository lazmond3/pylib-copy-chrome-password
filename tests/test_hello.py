# -*- coding: utf-8 -*-

# from .context import use_hello
import unittest
from . import context
from debug import DEBUG

chrome_password = context.chrome_password


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_hello(self):
        assert chrome_password.hello.hello() == "hello"


if __name__ == '__main__':
    unittest.main()
