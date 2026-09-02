# Slice obj[lo:hi:step] on list / str — CPython slice.indices. Each group below hits a
# distinct branch of the engine (omitted bounds, negative bounds, over-range clamping,
# negative step, empty results, empty/singleton sequences). Differential vs real Python;
# an exhaustive 13764-case (lo,hi,step) x length sweep also backs this — see PROOF notes.
a = [1, 2, 3, 4, 5]

# basic forward + omitted bounds
assert a[1:3] == [2, 3]
assert a[:2] == [1, 2]
assert a[2:] == [3, 4, 5]
assert a[:] == [1, 2, 3, 4, 5]

# negative bounds (count from the end)
assert a[-2:] == [4, 5]
assert a[:-1] == [1, 2, 3, 4]
assert a[-3:-1] == [3, 4]

# over-range bounds clamp (no error)
assert a[1:100] == [2, 3, 4, 5]
assert a[-100:2] == [1, 2]
assert a[3:1] == []          # start past stop, step +1 -> empty
assert a[10:] == []          # start at/after end -> empty

# steps
assert a[::2] == [1, 3, 5]
assert a[1::2] == [2, 4]
assert a[::-1] == [5, 4, 3, 2, 1]      # reverse
assert a[::-2] == [5, 3, 1]
assert a[4:1:-1] == [5, 4, 3]          # negative step, explicit bounds
assert a[-1:-4:-1] == [5, 4, 3]        # negative step, negative bounds
assert a[1:4:-1] == []                 # wrong direction for step -> empty

# empty / singleton sequences
assert [][:] == []
assert [][::-1] == []
assert [7][:] == [7]
assert [7][::-1] == [7]
assert [7][1:] == []

# strings behave identically
s = "hello"
assert s[1:4] == "ell"
assert s[:3] == "hel"
assert s[2:] == "llo"
assert s[::-1] == "olleh"
assert s[::2] == "hlo"
assert s[-3:] == "llo"
assert s[4:1:-1] == "oll"
assert s[10:] == ""
assert ""[:] == ""
assert ""[::-1] == ""
