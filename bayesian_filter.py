import os
import re
from collections import Counter
import math


def read_files(path):
    """A simple Function to check whether
        the file path exists or not.
    """
    if os.path.exists(path):
        for filename in os.listdir(path):
            if filename[0] == "!":
                continue
            with open(dir + "/" + filename, "rt") as f:
                yield filename, f.read()

    else:
        raise Exception('Invalid file path:'.format(path))


def read_corpus(filename):
    """A Function to open the file and read the
    email string and Save those individual Strings
    into a Corpus.
    """
    with open(filename, "rt") as file_string:
        corpus = list()
        for line in file_string:
            key, target = line.split()
            corpus[key] = target

        return corpus


class BayesianFilter(object):
    def __init__(self):
        self.spams = Counter()
        self.genuines = Counter()
        self.spam_percentage = {}
        self.regexp = re.compile(r"(?:(?:\w+(?:\.\w+)*@)?(?:[a-zA-Z0-9_]+\.)+[a-z]{2,12})|[a-zA-Z0-9]+")

    def word_list(self, email_string):
        return [word.lower() for word in self.regexp.findall(email_string) if len(word) < 30]

    def training(self, path):

        corpus = read_corpus(path + "/!truth.txt")
        total_spam = 0
        total_genuine = 0

        for id, message in read_files(path):
            target = corpus[id]

            if target == "SPAM":
                total_spam += 1
            else:
                total_genuine += 1
            for words in set(self.word_list(message)):
                if target == "SPAM":
                    self.spams[words] += 1
                else:
                    self.genuines[words] += 1

        spam_probability = total_spam / (total_spam + total_genuine)
        genuine_probability = 1 - spam_probability

        for words in (set(self.spams.keys()) | set(self.genuines.key())):
            self.spam_percentage[words] = (self.spams[words] / total_spam * spam_probability) / \
                                          (self.spams[words] / total_spam * spam_probability +

                                           self.genuines[words] / total_genuine * genuine_probability)

    EASING = 0.095
    SLICING = 38

    def is_spam(self, path):

        with open(path + "/!prediction.txt", "wt") as file_name:
            for id, message in read_files(file_name(path)):
                a, b = 1.0, 1.0

                for words, spam_percent in sorted([(w, 0.5 if self.spam_percentage.get(w) is None
                                                    else self.spam_percentage[w]) for w in self.word_list(message)],
                                                  key=lambda x: .5 - math.fabs(0.5 - x[1]))[0:self.SLICING]:
                    a *= math.fabs(spam_percent - self.EASING)
                    b *= 1.0 - spam_percent + self.EASING
                file.name.write(id + " " + ("SPAM" if (a / (a + b)) >= 1.0 else "OK") + "\n")