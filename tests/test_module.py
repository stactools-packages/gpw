import unittest

import stactools.gpw


class TestModule(unittest.TestCase):
    def test_version(self):
        self.assertIsNotNone(stactools.gpw.__version__)
