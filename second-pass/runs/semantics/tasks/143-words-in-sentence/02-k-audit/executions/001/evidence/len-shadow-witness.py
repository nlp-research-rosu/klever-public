def words_in_sentence(sentence):
    words = sentence.split()
    result = ""
    word = ""
    n = 0
    _plain = 0
    len = 4
    for word in words:
        n = len(word)
        if n == 2:
            if result == "":
                result = word
            else:
                result = result + " " + word
    return result


# "aa" is a contract-valid input. Python and the fixed semantics do not return
# "aa": the local integer binding shadows the builtin and is not callable.
# The candidate's priority len bridge ignores this binding and fabricates 2.
assert words_in_sentence("aa") == "aa"
