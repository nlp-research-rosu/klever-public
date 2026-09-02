assert "abc" in "xxabcyy"
assert not "abc" in "xxabyy"
assert "" in "anything"
assert "a" in "cat"
assert not "z" in "cat"
assert "cat" in "cat"
assert not "cats" in "cat"
assert ("bc" in "abcd") == True
assert ("q" not in "abc") == True
