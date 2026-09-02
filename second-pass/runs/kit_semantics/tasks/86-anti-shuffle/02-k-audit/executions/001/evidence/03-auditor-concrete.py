def anti_shuffle(s):
    result = ''
    word = ''
    char = ''
    new_word = ''
    inserted = False
    old_char = ''
    for char in s:
        if char == ' ':
            result += word
            result += ' '
            word = ''
        else:
            new_word = ''
            inserted = False
            for old_char in word:
                if not inserted and char < old_char:
                    new_word += char
                    inserted = True
                new_word += old_char
            if not inserted:
                new_word += char
                inserted = True
            word = new_word
    result += word
    return result


assert anti_shuffle('Hi') == 'Hi'
assert anti_shuffle('hello') == 'ehllo'
assert anti_shuffle('Hello World!!!') == 'Hello !!!Wdlor'
assert anti_shuffle('') == ''
assert anti_shuffle(' ') == ' '
assert anti_shuffle('  ') == '  '
assert anti_shuffle(' a ') == ' a '
assert anti_shuffle('ba') == 'ab'
assert anti_shuffle('aa') == 'aa'
assert anti_shuffle('ab') == 'ab'
assert anti_shuffle('  cba  a') == '  abc  a'
assert anti_shuffle('tabs\tstay') == '\taabsstty'
