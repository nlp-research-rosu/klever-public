def do_algebra(operator, operand):
    expression = ""
    oprn = 0
    oprt = ""
    for oprn, oprt in zip(operand, operator + [""]):
        expression += str(oprn) + oprt
    return eval(expression)
