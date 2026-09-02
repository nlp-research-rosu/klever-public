# General lists: list(ValSeq), a Python list holding any Val. Literal, concat (+),
# == / !=, membership (in / not in), and iteration. Lists are heterogeneous; here
# int-element and str-element lists.
assert [1, 2] + [3] == [1, 2, 3]
assert ["a", "b"] + ["c"] == ["a", "b", "c"]
assert [1, 2, 3] == [1, 2, 3]
assert [1, 2] != [1, 3]
assert 2 in [1, 2, 3]
assert 5 not in [1, 2, 3]
assert "b" in ["a", "b", "c"]

joined = ""
for w in ["foo", "bar", "baz"]:
    joined = joined + w
assert joined == "foobarbaz"
