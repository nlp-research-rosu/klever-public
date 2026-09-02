# Proof-local extension assessment

## `numCodes(Int)` and `fractionCodes(Int,Int)`

Classification: result-bearing, opaque constructors used as the entire entry
input domain. They are not functions and have no equations connecting them to
the fixed `iCons` decimal-code representation. `abstract_constructor_search.log`
confirms they occur nowhere in the trusted semantics.

Disposition: reject as a representation of the HumanEval domain. The target
claim ranges only over these newly invented `IntSeq` terms, not the concrete
strings accepted by `solution.py`.

## `splitSep(fractionCodes(A,B),47,.IntSeq) => ...`

Classification: operational bridge/summary equation. It replaces the fixed
recursive separator scan on the value that supplies both numerator and
denominator. Its pure-state footprint is the returned `ValSeq`; downstream it
controls both split-list heap objects, all four integer conversions, and the
final Boolean.

There is no bridge-free universal connection theorem, because fixed semantics
cannot mention `fractionCodes`. An opposite symbolic interpretation is a false
conclusion witness: if `fractionCodes(1,2)` denotes the valid concrete code
sequence for `"1/1"`, fixed `split("/")` returns `["1","1"]`, while this rule
returns `[numCodes(1),numCodes(2)]`. At `n="1/1"` the fixed program returns
`True`, but the candidate abstraction derives `False` from
`pyMod(1,2) == 0`.

Disposition: reject as an unjustified result-bearing bridge.

## `applyBuiltin("int",str(numCodes(I)),.Vals) => I`

Classification: operational bridge/summary equation. It replaces the fixed
single/multi-digit decimal conversion and directly supplies every arithmetic
operand and the final postcondition.

There is no connection theorem or exhaustive definition of `numCodes`.
An opposite symbolic interpretation is a false conclusion witness: if
`numCodes(2)` denotes the fixed code sequence `iCons(51,.IntSeq)` (the valid
string `"3"`), fixed `int` returns `3`, while this rule returns `2`. The theory
fixes the label as the value without proving the label denotes those digits.

Disposition: reject as an unconstrained program-derived, result-bearing
abstraction. The same `I` appears in this bridge and the postcondition, which
is circular rather than a proof of parsing.

## `runSimplify(Val,Val)`

Classification: operational wrapper. It rewrites only the head `<k>` item to
an ordinary application of a closure with captured scope 0 and the two
arguments in order. It preserves arbitrary continuation and every other cell.
`program_pinning.log` gives constructor-level body equality, and
`kprove_body_mutation.log` shows a mutation of the actually executed `%` term
causes the target proof to stick.

Disposition: acceptable wrapper. It does not cure the two input/parsing
bridges above.
