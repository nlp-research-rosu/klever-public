assert eval("2 + 3 * 4") == 14
assert eval("2 ** 3 ** 2") == 512
assert eval("10 - 2 - 3") == 5
assert eval("7 // 2 - 1") == 2
assert eval("5 * 2 ** 3") == 40
assert eval("100 // 7 // 2") == 7
assert eval("1 + 2 - 3 * 4 // 5") == 1
expression = str(6)
expression = expression + "*" + str(3)
assert eval(expression) == 18
