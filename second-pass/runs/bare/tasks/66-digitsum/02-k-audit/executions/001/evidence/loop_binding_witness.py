def digitSum(s):
    total = 0
    char = "B"
    for char in s:
        if "A" <= char <= "Z":
            total = total + ord(char)
    return ord(char)
