# solution.py — canonical verbatim minus the docstring (element loop over the
# real split, real .isdigit()/int()/.append(), real sum).


def fruit_distribution(s, n):
    lis = list()
    for i in s.split(' '):
        if i.isdigit():
            lis.append(int(i))
    return n - sum(lis)
