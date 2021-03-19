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

    def test_negative_epubtohtml(self):
        filename = "hello_world.epub"
        filestream = open(filename, 'w')
        filestream.close()

        self.reader = Reader(filename)
        self.reader.epubtohtml()
        # TypeError: 'NoneType' object is not callable
        self.assertRaises(TypeError, self.reader.html_chapters)

    def test_chapter_to_text(self):
        self.reader.epubtohtml()
        chapter_three = self.reader.html_chapters[2].decode('UTF-8')
        chapter_three_text = self.reader.chapter_to_text(chapter_three)

        self.assertNotIn('<!DOCTYPE html>', chapter_three_text)

    def test_negative_chapter_to_text(self):
        self.reader.epubtohtml()
        chapter_three = ""
        chapter_three_text = self.reader.chapter_to_text(chapter_three)

        self.assertEqual('', chapter_three_text)

    def test_epub_to_text(self):
        self.reader.epubtohtml()
        self.reader.epub_to_text()

        for text_chapter in self.reader.text_chapters:
            self.assertNotIn('<!DOCTYPE html>', text_chapter)


    def test_set_author(self):
        self.fail()

    def test_set_title(self):
        self.fail()

    def test_create_books_dir(self):
        self.fail()

    def test_read_book(self):
        self.fail()
