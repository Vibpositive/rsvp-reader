import os
from pathlib import Path


def create_books_dir(authors, title):
    try:
        __authors = "".join(authors)
        authors_path = f"{os.getenv('HOME')}/rsvp/" + __authors + os.sep + str(title)
        path = Path(authors_path)

        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as e:
                # TODO Log
                pass
            else:
                # TODO Log
                print("Successfully created the directory %s " % path)

    except IOError as e:
        if e.errno != 17:
            raise e
    except TypeError as e:
        # TODO Log
        print(e)
    except Exception as e:
        # TODO Unknow exception log
        print("unknown error: ", e)
