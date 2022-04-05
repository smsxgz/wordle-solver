# import numpy as np
from collections import Counter, defaultdict
import json


def wordle(guess, answer):
    ans_couter = Counter(answer)
    res = ''
    for i, ch in enumerate(guess):
        if ch in ans_couter:
            if answer[i] == ch:
                res += '2'
            else:
                res += '1'
            ans_couter[ch] -= 1
        else:
            res += '0'
    return res


def load_allowed_words():
    allowed = []
    with open('allowed_words.txt', 'r') as f:
        for line in f.readlines():
            allowed.append(line.strip())
    return allowed


def load_possible_words():
    possible = []
    with open('possible_words.txt', 'r') as f:
        for line in f.readlines():
            possible.append(line.strip())
    return possible


def prepare():
    allowed = load_allowed_words()
    possible = load_possible_words()

    cache = defaultdict(lambda: defaultdict(list))
    for guess in allowed:
        for answer in possible:
            wl = wordle(guess, answer)
            cache[guess][wl].append(answer)

    with open('cache.json', 'w') as outfile:
        json.dump(cache, outfile)


def load_cache():
    with open('cache.json', 'r') as f:
        cache = json.load(f)
    return cache


class Wordle:
    def __init__(self):
        self.possible = load_possible_words()
        self.idx = -1
        self.n = len(self.possible)

    def reset(self):
        self.idx += 1
        if self.idx < self.n:
            self.answer = self.possible[self.idx]
            self.path = []
            return True
        else:
            return False

    def action(self, guess):
        self.path.append(guess)

        flag = False
        if guess == self.answer:
            flag = True
            print(','.join(self.path))
        return wordle(guess, self.answer), flag


if __name__ == "__main__":
    prepare()
