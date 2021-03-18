import redislite
import os

DB_PATH = '/tmp/rsvp/'
DB_NAME = 'rsvp.db'
DB_FULL_PATH = DB_PATH + DB_NAME

try:
    os.mkdir(DB_PATH)
except:
    pass

redis_connection = redislite.Redis(DB_FULL_PATH)


def add_book(book):
    author = book['author']
    title = book['title']
    redis_connection.sadd(author, title)


def get_book_by_author(author, title=None):
    return title if redis_connection.sismember(author, title) else None


def get_books_by_author(book):
    for __book in redis_connection.smembers(book['author']):
        __book_decoded = __book.decode("UTF-8")
        if __book_decoded == book['title']:
            return __book_decoded
    return None


def get_book_progress(book):
    if redis_connection.sismember(book['author'], book['title']):
        return int(redis_connection.get(book['title'] + '.progress'))
    return None


def set_book_progress(book, progress):
    if redis_connection.sismember(book['author'], book['title']):
        redis_connection.set(book['title'] + '.progress', int(progress))


def flush_db():
    redis_connection.flushdb()
