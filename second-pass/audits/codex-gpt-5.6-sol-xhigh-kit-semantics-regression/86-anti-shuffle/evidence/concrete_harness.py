def anti_shuffle(s):
    result = ""
    word = ""
    for char in s:
        if char == " ":
            result = result + "".join(sorted(list(word))) + " "
            word = ""
        else:
            word = word + char
    return result + "".join(sorted(list(word)))


assert anti_shuffle("") == ""
assert anti_shuffle("Hi") == "Hi"
assert anti_shuffle("hello") == "ehllo"
assert anti_shuffle("Hello World!!!") == "Hello !!!Wdlor"
assert anti_shuffle(" ") == " "
assert anti_shuffle("  ") == "  "
assert anti_shuffle(" ba") == " ab"
assert anti_shuffle("ba ") == "ab "
assert anti_shuffle("ba  dc") == "ab  cd"
assert anti_shuffle("~!  bA ") == "!~  Ab "
