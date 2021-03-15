import os
from pathlib import Path

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub


# there may be more elements you don't want, such as "style", etc.

class Reader(object):

    def __init__(self, book):
        # TODO read blacklist from yaml
        self.blacklist = ['[document]', 'noscript', 'header', 'html', 'meta', 'head', 'input', 'script', '\n']
        self.text_chapters = []
        self.VERSION = None
        self.html_chapters = None
        self.title = None
        self.authors = None
        self.book_path = None
        self.library_dir = "/tmp/"
        self.book = None

        self.read_book(book)
        self.set_title()
        self.set_author()
        self.create_books_dir()
        self.epubtohtml()
        self.epub_to_text()

    def epubtohtml(self):
        chapters = []
        for item in self.book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                chapters.append(item.get_content())
        self.html_chapters = chapters

    def chapter_to_text(self, chap):
        output = ''
        soup = BeautifulSoup(chap, 'html.parser')
        text = soup.find_all(text=True)
        for t in text:
            if t.parent.name not in self.blacklist:
                output += '{} '.format(t)
        return output

    def epub_to_text(self):
        for html in self.html_chapters:
            text = self.chapter_to_text(html)
            self.text_chapters.append(text.rstrip("\n"))

    def set_author(self):
        self.authors = self.book.get_metadata('DC', 'creator')

    def set_title(self):
        self.title = self.book.get_metadata('DC', 'title')[0][0]

    def create_books_dir(self):
        try:
            if self.book_path.endswith('epub'):

                authors = ""

                for author in self.authors:
                    authors += str(author[0])

                authors_path = f"{os.getenv('HOME')}/rsvp/" + authors + os.sep + str(self.title)
                path = Path(authors_path)

                if not os.path.exists(path):
                    try:
                        os.makedirs(path)
                    except OSError as e:
                        # TODO Log
                        print(e)
                    else:
                        print("Successfully created the directory %s " % path)

        except IOError as e:
            if e.errno != 17:
                raise e

    # def book_to_json(self, book):
    #     with open("sample.json", "w") as outfile:
    #         json.dump(book, outfile)

    def read_book(self, book):
        self.book_path = book
        self.book = epub.read_epub(book)

# reader = Reader('../../../../epub/ebook.epub')
