def select_words(s, n):
    result = []
    current = ""
    cnt = 0
    has = False
    ch = ""
    for ch in s + " ":
        if ch == " ":
            if has:
                if cnt == n:
                    result = result + [current]
                current = ""
                cnt = 0
                has = False
        else:
            current = current + ch
            if ch not in "aeiouAEIOU":
                cnt = cnt + 1
            has = True
    return result
