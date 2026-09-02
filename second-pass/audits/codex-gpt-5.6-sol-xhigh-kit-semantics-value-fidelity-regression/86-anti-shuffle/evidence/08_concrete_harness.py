def anti_shuffle(s):
    result = ""
    word = ""
    character = ""
    existing = ""
    new_word = ""
    inserted = False
    for character in s:
        if character == " ":
            result += word
            result += " "
            word = ""
        else:
            new_word = ""
            inserted = False
            for existing in word:
                if inserted:
                    new_word += existing
                else:
                    if character < existing:
                        new_word += character
                        inserted = True
                    new_word += existing
            if inserted:
                word = new_word
            else:
                word = new_word + character
    result += word
    return result


assert anti_shuffle("") == ""
assert anti_shuffle("Hi") == "Hi"
assert anti_shuffle("hello") == "ehllo"
assert anti_shuffle("Hello World!!!") == "Hello !!!Wdlor"
assert anti_shuffle(" ") == " "
assert anti_shuffle(" ba") == " ab"
assert anti_shuffle("ba ") == "ab "
assert anti_shuffle("ba  dc") == "ab  cd"
assert anti_shuffle("    ") == "    "
assert anti_shuffle("x") == "x"
assert anti_shuffle("dcba") == "abcd"
assert anti_shuffle("dabc") == "abcd"
assert anti_shuffle("baab") == "aabb"
assert anti_shuffle("z!A~") == "!Az~"
