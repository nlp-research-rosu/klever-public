def _evaluate(operator, operand, start, end, level):
    if level == 0:
        i = end - 1
        while i >= start:
            if operator[i] == "+":
                return _evaluate(operator, operand, start, i, 0) + _evaluate(operator, operand, i + 1, end, 1)
            if operator[i] == "-":
                return _evaluate(operator, operand, start, i, 0) - _evaluate(operator, operand, i + 1, end, 1)
            i -= 1
        return _evaluate(operator, operand, start, end, 1)

    if level == 1:
        i = end - 1
        while i >= start:
            if operator[i] == "*":
                return _evaluate(operator, operand, start, i, 1) * _evaluate(operator, operand, i + 1, end, 2)
            if operator[i] == "//":
                return _evaluate(operator, operand, start, i, 1) // _evaluate(operator, operand, i + 1, end, 2)
            i -= 1
        return _evaluate(operator, operand, start, end, 2)

    if level == 2:
        i = start
        while i < end:
            if operator[i] == "**":
                return _evaluate(operator, operand, start, i, 3) ** _evaluate(operator, operand, i + 1, end, 2)
            i += 1
        return _evaluate(operator, operand, start, end, 3)

    return operand[start]


def do_algebra(operator, operand):
    return _evaluate(operator, operand, 0, len(operator), 0)
