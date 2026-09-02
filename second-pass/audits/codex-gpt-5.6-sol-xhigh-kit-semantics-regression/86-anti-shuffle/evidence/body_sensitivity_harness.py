def anti_shuffle(s):
    result = ""
    word = "x"
    for char in s:
        if char == " ":
            result = result + "".join(sorted(list(word))) + " "
            word = ""
        else:
            word = word + char
    return result + "".join(sorted(list(word)))


# The original theorem gives "" for this satisfying input. The mutated body gives "x".
assert anti_shuffle("") == ""
