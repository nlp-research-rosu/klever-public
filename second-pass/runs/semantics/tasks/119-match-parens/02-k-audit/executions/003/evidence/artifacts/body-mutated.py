def is_good(s):
    return ''

def match_parens(lst):
    if is_good(lst[0] + lst[1]):
        return 'Yes'
    if is_good(lst[1] + lst[0]):
        return 'Yes'
    return 'No'
