import os
from pathlib import Path

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub


class Reader(object):

    def __init__(self, book):
        # TODO read blacklist from yaml
        self.blacklist = ['[document]', 'noscript', 'header', 'html', 'meta', 'head', 'input', 'script', '\n']
        self.text_chapters = []
        self.VERSION = None
        self.html_chapters = None
        self.title = None
        self.authors = None
        self.library_dir = "/tmp/"
        self.book = book
        self.epub_book = None
    # Sets chapters in html
    def epubtohtml(self):
        chapters = []
        try:
            for item in self.epub_book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    chapters.append(item.get_content())
            self.html_chapters = chapters
        except AttributeError as e:
            # TODO log
            print('invalid ebook')
            pass

    def chapter_to_text(self, chap):
        output = ''
        soup = BeautifulSoup(chap, 'html.parser')
        text = soup.find_all(text=True)
        for t in text:
            if t.parent.name not in self.blacklist:
                output += '{} '.format(t)
        return output

    def epub_to_text(self):
        for html_chapter in self.html_chapters:
            text = self.chapter_to_text(html_chapter)
            self.text_chapters.append(text.rstrip("\n"))

    def set_author(self):
        self.authors = self.epub_book.get_metadata('DC', 'creator')
        print(self.epub_book.get_metadata('DC', 'identifier'))

    def set_title(self):
        self.title = self.epub_book.get_metadata('DC', 'title')[0][0]

    def create_books_dir(self):
        try:
            if self.book.endswith('epub'):

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
                        pass
                    else:
                        print("Successfully created the directory %s " % path)

        except IOError as e:
            if e.errno != 17:
                raise e

    def read_book(self):
        try:
            self.epub_book = epub.read_epub(self.book)
        except Exception as e:
            print(e)
            pass
        # TODO log


# reader = Reader('../../../../epub/ebook.epub')
# for i, chapter in enumerate(reader.text_chapters):
#     if i < 10:
#         lista = chapter.split(' ')
#         stripped_list = [line.strip() for line in [line.strip() for line in lista] if line != ""]
#         print(stripped_list)
