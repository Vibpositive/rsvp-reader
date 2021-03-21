from unittest import TestCase

from com.vibpositive.readers.epub.reader import Reader
from utils import create_books_dir
import os
import shutil


class TestUtils(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.book = '../../../epub/ebook.epub'
        cls.reader = Reader(cls.book)
        cls.reader.read_book()
        cls.reader.set_author()
        cls.reader.set_title()
        cls.authors = cls.reader.authors
        cls.title = cls.reader.title

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(f"{os.getenv('HOME')}/rsvp/")
        del cls.reader

    def test_create_books_dir(self):
        self.reader.set_author()
        create_books_dir(self.authors, self.title)
        for author in self.reader.authors:
            self.assertIn(author, os.listdir(f"{os.getenv('HOME')}/rsvp/"))
