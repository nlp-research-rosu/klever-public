def is_good(s):
    balance = 0
    for char in s:
        if char == '(':
            balance += 1
        else:
            balance -= 1
        if balance < 0:
            return ''
    if balance == 0:
        return 'T'
    return ''


def match_parens(lst):
    if is_good(lst[0] + lst[1]):
        return 'Yes'
    if is_good(lst[1] + lst[0]):
        return 'Yes'
    return 'No'
