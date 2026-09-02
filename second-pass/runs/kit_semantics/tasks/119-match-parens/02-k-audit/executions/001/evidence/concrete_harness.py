def match_parens(lst):
    text = lst[0] + lst[1]
    balance = 0
    minimum = 0
    char = ''
    for char in text:
        if char == '(':
            balance += 1
        else:
            balance -= 1
        if balance < minimum:
            minimum = balance
    if balance == 0:
        if minimum >= 0:
            return 'Yes'

    text = lst[1] + lst[0]
    balance = 0
    minimum = 0
    char = ''
    for char in text:
        if char == '(':
            balance += 1
        else:
            balance -= 1
        if balance < minimum:
            minimum = balance
    if balance == 0:
        if minimum >= 0:
            return 'Yes'

    return 'No'


assert match_parens(['()(', ')']) == 'Yes'
assert match_parens([')', ')']) == 'No'
assert match_parens(['', '']) == 'Yes'
assert match_parens(['(', ')']) == 'Yes'
assert match_parens([')', '(']) == 'Yes'
assert match_parens([')(', ')(']) == 'No'
assert match_parens(['(((', ')))']) == 'Yes'
