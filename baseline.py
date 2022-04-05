from util import load_allowed_words, load_possible_words, load_cache, Wordle, wordle
from collections import Counter
import numpy as np

allowed = load_allowed_words()
possible = load_possible_words()
cache = load_cache()


def max_entropy_guess(candicates):
    entropy_dict = dict()
    for guess in allowed:
        counter = Counter()

        # if len(candicates) == len(possible):
        #     for key in cache[guess]:
        #         counter[key] = len(cache[guess][key])
        # else:
        for answer in candicates:
            wl = wordle(guess, answer)
            counter[wl] += 1

        # assert sum(counter.values()) == len(candicates)
        ent = 0
        for key in counter:
            p = counter[key] / len(candicates)
            ent -= p * np.log(p)
        entropy_dict[guess] = ent

    max_entroy = -1
    max_guess = []
    for guess in allowed:
        if entropy_dict[guess] > max_entroy:
            max_entroy = entropy_dict[guess]
            max_guess = [guess]
        elif entropy_dict[guess] == max_entroy:
            max_guess.append(guess)

    for guess in max_guess:
        if guess in candicates:
            return guess
    return max_guess[0]


def entropy_solver():
    wordle = Wordle()
    while wordle.reset():
        candicates = possible

        guess = 'soare'
        while True:
            out, flag = wordle.action(guess)
            if flag:
                break

            new_candicates = []
            for word in cache[guess][out]:
                if word in candicates:
                    new_candicates.append(word)
            candicates = new_candicates

            guess = max_entropy_guess(candicates)


if __name__ == "__main__":
    entropy_solver()
