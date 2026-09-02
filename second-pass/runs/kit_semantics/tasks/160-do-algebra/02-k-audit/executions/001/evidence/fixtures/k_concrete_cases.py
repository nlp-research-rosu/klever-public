def do_algebra(operator, operand):
    expression = ""
    oprn = 0
    oprt = ""
    for oprn, oprt in zip(operand, operator + [""]):
        expression += str(oprn) + oprt
    return eval(expression)


documented = do_algebra(["+", "*", "-"], [2, 3, 4, 5])
plus_boundary = do_algebra(["+"], [0, 0])
minus_boundary = do_algebra(["-"], [0, 7])
multiply_boundary = do_algebra(["*"], [0, 999])
floor_boundary = do_algebra(["//"], [7, 3])
power_boundary = do_algebra(["**"], [2, 0])
precedence = do_algebra(["+", "*"], [2, 3, 4])
right_power = do_algebra(["**", "**"], [2, 3, 2])
