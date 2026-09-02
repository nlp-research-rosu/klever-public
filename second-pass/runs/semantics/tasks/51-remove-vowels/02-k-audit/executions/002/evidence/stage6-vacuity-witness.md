# False-postcondition witness

The fresh mutation changes only the entry claim's returned code sequence from
`removeVowelCodes(CODES)` to
`seqConcat(removeVowelCodes(CODES), iCons(120, .IntSeq))`.

A satisfying witness is `CODES = .IntSeq`, corresponding to Python input `""`.
The real generated program and the trusted canonical both return `""`; the
mutated postcondition requires `"x"` (code 120 appended). Thus the mutation is
meaningfully false on a realizable entry state.

`stage6-vacuity-dry-run.log` records successful parsing/building (exit 0).
`stage6-vacuity-kprove.log` records exit 1 with `WarnStuckClaimState` and the
unmet equality between the true summary and that summary with code 120
appended.
