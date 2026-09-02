# solution.py — canonical verbatim minus the docstring (real lst.sort(),
# append filter loop, real sorted(new_lst, key=len)).


def sorted_list_sum(lst):
    lst.sort()
    new_lst = []
    for i in lst:
        if len(i)%2 == 0:
            new_lst.append(i)
    return sorted(new_lst, key=len)
