from unittest import TestCase
from reader import *


class TestReader(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reader = Reader('../../../../epub/ebook.epub')
        cls.reader.read_book()

    @classmethod
    def tearDownClass(cls):
        del cls.reader

    def test_epubtohtml(self):
        expected = '<!DOCTYPE html>'
        self.reader.epubtohtml()
        chapter_zero = self.reader.html_chapters[0].decode('UTF-8')

        self.assertIn(expected, chapter_zero)

    def test_chapter_to_text(self):
        self.fail()

    def test_epub_to_text(self):
        self.fail()

    def test_set_author(self):
        self.fail()

    def test_set_title(self):
        self.fail()

    def test_create_books_dir(self):
        self.fail()

    def test_read_book(self):
        self.fail()
