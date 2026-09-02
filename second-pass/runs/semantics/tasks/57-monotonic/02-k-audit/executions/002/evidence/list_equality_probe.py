# This is inside the proof bridge's complete match domain but unrelated to sorted().
assert [] == []
assert not ([] == [1])
assert [1, 2] == [1, 2]
assert not ([1, 2] == [2, 1])
