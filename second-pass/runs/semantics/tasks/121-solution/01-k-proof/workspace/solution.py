def solution(lst):
    total = 0
    even_position = True
    value = 0
    for value in lst:
        if even_position:
            total = total + value * (value % 2)
        even_position = not even_position
    return total
