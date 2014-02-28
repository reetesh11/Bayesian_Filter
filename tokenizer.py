import re


class Tokenizer:
    """A simple regex-based whitespace tokenizer.
    It expects a string and can return all tokens lower-cased
    or in their existing case.
    """

    WORD_RE = re.compile('\\w+', re.U)

    def __init__(self, lower=True):
        self.lower = lower

    def tokenize(self, obj):
        for match in self.WORD_RE.finditer(obj):
            if self.lower:
                yield match.group().lower()
            else:
                yield match.group()