def anti_shuffle(s):
    result = ''
    word = ''
    char = ''
    for char in s:
        if char == ' ':
            result = result + ''.join(sorted(list(word))) + ' '
            word = ''
        else:
            word = word + char
    return result + ''.join(sorted(list(word)))


assert anti_shuffle('') == ''
assert anti_shuffle(' ') == ' '
assert anti_shuffle('  ') == '  '
assert anti_shuffle('ba') == 'ab'
assert anti_shuffle('a  b') == 'a  b'
assert anti_shuffle('Hi') == 'Hi'
assert anti_shuffle('hello') == 'ehllo'
assert anti_shuffle('Hello World!!!') == 'Hello !!!Wdlor'
assert anti_shuffle('!a0 Zz~') == '!0a Zz~'
