def int_to_mini_roman(number):
    M = ['', 'm']
    H = ['', 'c', 'cc', 'ccc', 'cd', 'd', 'dc', 'dcc', 'dccc', 'cm']
    T = ['', 'x', 'xx', 'xxx', 'xl', 'l', 'lx', 'lxx', 'lxxx', 'xc']
    U = ['', 'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix']
    return M[number // 1000] + H[(number // 100) % 10] + T[(number // 10) % 10] + U[number % 10]


# Smoke checks from the prompt docstring (NOT hidden tests).
assert int_to_mini_roman(19) == 'xix'
assert int_to_mini_roman(152) == 'clii'
assert int_to_mini_roman(426) == 'cdxxvi'
assert int_to_mini_roman(1) == 'i'
assert int_to_mini_roman(1000) == 'm'
