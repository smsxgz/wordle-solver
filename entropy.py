from util import load_allowed_words, load_possible_words, load_cache, wordle
from collections import Counter, defaultdict
import numpy as np

allowed = load_allowed_words()
possible = load_possible_words()
cache = load_cache()


def max_entropy_solver(candicates, path=[]):
    if len(candicates) == 1:
        yield path + candicates
        return

    entropy_dict = dict()
    for guess in allowed:
        counter = Counter()

        if len(candicates) == len(possible):
            for key in cache[guess]:
                counter[key] = len(cache[guess][key])
        else:
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

    word = max_guess[0]
    for guess in max_guess:
        if guess in candicates:
            word = guess

    counter = defaultdict(list)
    for answer in candicates:
        wl = wordle(word, answer)
        counter[wl].append(answer)

    for key in counter:
        if key == '22222':
            yield path + [word]
        else:
            yield from max_entropy_solver(counter[key], path + [word])
    return


def main():
    out = []
    for p in max_entropy_solver(possible):
        out.append(p)

    out.sort(key=lambda x: x[-1])
    with open('entropy.txt', 'w') as f:
        for p in out:
            f.write(','.join(p) + '\n')


if __name__ == "__main__":
    main()
