def insert_char(word, char):
    prefix = ""
    suffix = word
    current = ""
    for current in word:
        if char < current:
            return prefix + char + suffix
        else:
            prefix = prefix + current
            suffix = suffix[1:]
    return prefix + char


def anti_shuffle(s):
    result = ""
    word = ""
    char = ""
    for char in s:
        if char == " ":
            result = result + word + " "
            word = ""
        else:
            word = insert_char(word, char)
    return result + word


assert anti_shuffle("") == ""
assert anti_shuffle(" ") == " "
assert anti_shuffle("Hi") == "Hi"
assert anti_shuffle("hello") == "ehllo"
assert anti_shuffle("Hello World!!!") == "Hello !!!Wdlor"
assert anti_shuffle("ba ab") == "ab ab"
assert anti_shuffle("a  cb") == "a  bc"
assert anti_shuffle("\x7f\x00 ~!") == "\x00\x7f !~"
