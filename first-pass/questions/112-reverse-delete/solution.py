def reverse_delete(s, c):
    kept = ""
    rev = ""
    ch = ""
    for ch in s:
        if ch not in c:
            kept = kept + ch
            rev = ch + rev
    return (kept, kept == rev)
