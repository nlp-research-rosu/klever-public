def generate_integers(a, b):
    result = []
    if a <= b:
        if a <= 2:
            if 2 <= b:
                result = result + [2]
        if a <= 4:
            if 4 <= b:
                result = result + [4]
        if a <= 6:
            if 6 <= b:
                result = result + [6]
        if a <= 8:
            if 8 <= b:
                result = result + [8]
    else:
        if b <= 2:
            if 2 <= a:
                result = result + [2]
        if b <= 4:
            if 4 <= a:
                result = result + [4]
        if b <= 6:
            if 6 <= a:
                result = result + [6]
        if b <= 8:
            if 8 <= a:
                result = result + [8]
    return result
