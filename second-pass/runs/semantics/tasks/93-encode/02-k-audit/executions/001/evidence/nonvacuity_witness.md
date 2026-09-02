# False-mutation witness

The fresh mutation is
`str(encodeCodes(INPUT))` → `str(iCons(88, encodeCodes(INPUT)))`.

Take `INPUT = .IntSeq` and the exact initial cells in the entry claim. This is a
satisfying initial state because the claim has no side condition and every cell
is ground. Fixed execution returns `str(.IntSeq)`, corresponding to Python
`encode("") == ""`. The mutated destination is
`str(iCons(88, .IntSeq))`, corresponding to `"X"`. Thus the mutated obligation
is false on a concrete satisfying input.
