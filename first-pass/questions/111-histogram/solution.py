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
