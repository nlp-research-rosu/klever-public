# solution.py — canonical verbatim minus the docstring (element iteration,
# real list1.count(i), real split, dict subscript-assign).


def histogram(test):
    dict1 = {}
    list1 = test.split(" ")
    t = 0
    for i in list1:
        if(list1.count(i) > t) and i != '':
            t = list1.count(i)
    if t > 0:
        for i in list1:
            if(list1.count(i) == t):
                dict1[i] = t
    return dict1


# Smoke checks — the HumanEval/111 dataset `check` cases (bare-value asserts).
assert histogram('a b b a') == {'a': 2, 'b': 2}
assert histogram('a b c a b') == {'a': 2, 'b': 2}
assert histogram('a b c d g') == {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'g': 1}
assert histogram('r t g') == {'r': 1, 't': 1, 'g': 1}
assert histogram('b b b b a') == {'b': 4}
assert histogram('') == {}
assert histogram('a') == {'a': 1}
