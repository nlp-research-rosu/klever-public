def do_algebra(operator, operand):
    expression = ""
    oprn = 0
    oprt = ""
    for oprn, oprt in zip(operand, operator + [""]):
        expression += str(oprn) + oprt
    return eval(expression)


assert do_algebra(["+", "*", "-"], [2, 3, 4, 5]) == 9
assert do_algebra(["**", "**"], [2, 3, 2]) == 512
assert do_algebra(["//", "+"], [7, 3, 1]) == 3
assert do_algebra(["-", "*"], [10, 2, 3]) == 4
