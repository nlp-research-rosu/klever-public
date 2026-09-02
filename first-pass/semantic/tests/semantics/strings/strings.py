# Strings are str(IntSeq) of char codes — literal, concat (+), == / !=, single-char
# membership (in / not in), and iteration (for c in s binds c to a 1-char string).
assert "ab" + "cd" == "abcd"
assert "hello" == "hello"
assert "hello" != "world"
assert "a" in "banana"
assert "z" not in "banana"

vowels = 0
for c in "education":
    if c in "aeiou":
        vowels += 1
assert vowels == 5

out = ""
for c in "abc":
    out = out + c + c
assert out == "aabbcc"
