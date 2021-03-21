from unittest import TestCase
from dao import *
import os

redis_connection = redislite.Redis(DB_FULL_PATH)


class TestDAO(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.book = {'author': 'Gabriel', 'title': 'Random3 title'}
        add_book(cls.book)

    @classmethod
    def tearDownClass(cls):
        del cls.book
        print(os.listdir(DB_PATH))

        try:
            os.remove(DB_FULL_PATH)
        except FileNotFoundError as e:
            print("Failed with:", e)
            pass

        print(os.listdir(DB_PATH))

        flush_db()

    def test_get_book_by_author(self):
        result = get_book_by_author('Gabriel', self.book['title'])
        expected = self.book['title']

        self.assertEqual(result, expected)

    def test_get_book_progress(self):
        expected = 400
        set_book_progress(self.book, expected)
        actual = get_book_progress(self.book)
        self.assertEqual(actual, expected)

    def test_negative_get_book_progress(self):
        expected = 400
        book = {'author': 'John Doe', 'title': 'Some title that does not exist'}
        set_book_progress(self.book, expected)
        self.assertIsNone(get_book_progress(book))

    def test_positive_get_books_by_author(self):
        expected = str(self.book['title'])
        actual = get_books_by_author(self.book)
        self.assertEqual(expected, actual)

    def test_negative_get_books_by_author(self):
        expected = None
        book = {"author": "Gabriel", 'title': "nonexistent"}
        actual = get_books_by_author(book)
        self.assertEqual(expected, actual)

