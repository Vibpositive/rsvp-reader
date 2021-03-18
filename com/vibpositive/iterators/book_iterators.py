class ChapterIterator:

    def __init__(self, book, current_position=0):
        self.current_position = current_position
        self.book = book

    def __iter__(self):
        self.chapter = self.book[self.current_position] if len(self.book) > 0 else None
        return self

    def __next__(self):
        if self.current_position + 1 <= len(self.book):

            current_chapter = self.book[self.current_position]
            self.current_position += 1
            self.chapter = current_chapter

            return current_chapter
        else:
            raise StopIteration

book_ = ['aa', 'bb', 'cc', 'd', 'e']

myclass = ChapterIterator(book_)
myiter = iter(myclass)

for x in myiter:
    print(x)

