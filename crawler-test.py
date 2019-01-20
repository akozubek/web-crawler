import unittest
from crawler import WebCrawlerParser

class TestWebCrawlerParser(unittest.TestCase):
    def setUp(self):
        self.parser = WebCrawlerParser('google.com')

    def test_is_internal_fragment(self):
        self.assertTrue(self.parser._is_internal_link('#who-we-are'))

    def test_is_internal_absolute(self):
        self.assertTrue(self.parser._is_internal_link('/'))

    def test_is_internal_relative(self):
        self.assertTrue(self.parser._is_internal_link('/privacy/policy'))

    def test_is_internal_https(self):
        self.assertTrue(self.parser._is_internal_link('https://google.com'))

    def test_is_internal_http(self):
        self.assertTrue(self.parser._is_internal_link('http://google.com'))

    def test_is_internal_https_with_path(self):
        self.assertTrue(self.parser._is_internal_link('https://google.com/privacy/policy'))

    def test_is_internal_http_with_path(self):
        self.assertTrue(self.parser._is_internal_link('http://google.com/privacy/policy'))

    def test_is_internal_external_http(self):
        self.assertFalse(self.parser._is_internal_link('http://facebook.com/'))

    def test_is_internal_external_https(self):
        self.assertFalse(self.parser._is_internal_link('https://facebook.com/'))

    def test_is_internal_external_http_with_path(self):
        self.assertFalse(self.parser._is_internal_link('http://facebook.com/who-we-are/details'))

    def test_is_internal_external_https_with_path(self):
        self.assertFalse(self.parser._is_internal_link('https://facebook.com/who-we-are/details'))

    def test_is_internal_other_protocols(self):
        self.assertTrue(self.parser._is_internal_link('mailto:contact@google.com'))

if __name__ == '__main__':
    unittest.main()
