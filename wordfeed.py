from settings import WPM


# This class generates words/phrases to display and the length of time in
# milliseconds to display each (based on words/minute and pauses for stops.)
class WordFeed(object):
    def __init__(self, text, inext=0):
        self.text_tuple = tuple(text.split())
        self.inext = inext if inext <= len(self.text_tuple) else 0

    def get_statistics(self):
        num_words = len(self.text_tuple)
        total_minutes = num_words / WPM
        return num_words, total_minutes

    def next(self):
        self.inext = max(self.inext, 0)
        if len(self.text_tuple) <= self.inext:
            return None
        text = self.text_tuple[self.inext]
        self.inext += 1
        return text
