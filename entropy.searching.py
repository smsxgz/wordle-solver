from collections import defaultdict, Counter
import numpy as np
import ray

from util import load_allowed_words, load_possible_words, load_cache, wordle

allowed = load_allowed_words()
possible = load_possible_words()
cache = load_cache()

ray.init()


def max_entropy_guess(candicates, n=5):
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

    entropy_list = sorted(entropy_dict.items(),
                          key=lambda x: x[1],
                          reverse=True)

    while n < len(entropy_list):
        if entropy_list[n][1] < entropy_list[n - 1][1]:
            break
        n += 1

    return entropy_list[:n]


def min_step(candicates, n=5, path=[]):
    if len(candicates) == 1:
        return [path + candicates]

    if len(candicates) == 2:
        return [
            path + candicates[:1],
            path + candicates,
        ]

    min_step_dict = dict()
    for guess, _ in max_entropy_guess(candicates, n):
        counter = defaultdict(list)

        for answer in candicates:
            wl = wordle(guess, answer)
            counter[wl].append(answer)

        if len(counter) == 1:
            continue

        min_step_cache = []
        for key in counter:
            if key == '22222':
                min_step_cache.append(path + [guess])
            else:
                min_step_cache += min_step(counter[key], n, path + [guess])

        min_step_dict[guess] = min_step_cache

    guess = min(min_step_dict,
                key=lambda x: sum(len(m) for m in min_step_dict[x]))
    return min_step_dict[guess]


@ray.remote(memory=500 * 1024 * 1024)
def first_search(guess, categories):
    min_step_cache = []
    for key in categories:
        candicates = categories[key]

        if key == '22222':
            min_step_cache.append([guess])
        else:
            min_step_cache += min_step(candicates, 5, [guess])

    return min_step_cache


def main():
    entropy_dict = dict()
    for guess in allowed:
        ent = 0
        for key in cache[guess]:
            p = len(cache[guess][key]) / len(possible)
            ent -= p * np.log(p)
        entropy_dict[guess] = ent

    entropy_list = sorted(entropy_dict.keys(),
                          key=lambda x: entropy_dict[x],
                          reverse=True)
    print('+' * 30)

    tasks = [
        first_search.remote(guess, cache[guess]) for guess in entropy_list[:25]
    ]

    min_step_dict = ray.get(tasks)

    out = min(min_step_dict, key=lambda x: sum(len(m) for m in x))
    out.sort(key=lambda x: x[-1])
    with open('entropy.searching.txt', 'w') as f:
        for p in out:
            f.write(','.join(p) + '\n')


if __name__ == "__main__":
    main()
