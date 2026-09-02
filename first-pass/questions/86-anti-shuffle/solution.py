# solution.py — canonical verbatim minus the docstring (the per-word
# ''.join(sorted(list(i))) comprehension over s.split(' '), space-joined).


def anti_shuffle(s):
    return ' '.join([''.join(sorted(list(i))) for i in s.split(' ')])
