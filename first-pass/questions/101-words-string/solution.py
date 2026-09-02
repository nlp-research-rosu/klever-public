def words_string(s):
    result = []
    current = ""
    has = False
    ch = ""
    for ch in s + " ":
        if ch in ", ":
            if has:
                result = result + [current]
                current = ""
                has = False
        else:
            current = current + ch
            has = True
    return result
