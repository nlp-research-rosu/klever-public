# Satisfiable claim states and plain-language obligations

## `SPEC.member-fold`

Precondition: the active continuation starts with the supplied operational term
`#memberAcc(V, list(VS))`; all surrounding cells are arbitrary and preserved.

Postcondition: that one operational membership fold is replaced by the Boolean
`memberVS(V, VS)` before the exact same continuation.

Satisfying state: choose `V = 2`,
`VS = vCons(1, vCons(2, .ValSeq))`, `CONT = .K`, and the pristine values for all
configuration cells. The state is well formed and the precondition matches.

## `SPEC.common-loop`

Precondition: environment `L` contains a plain scope binding `l1` to any original
list, `l2` to `list(SECOND)`, `result` to `ref(H)`, and `item` to `OLD`; heap
location `H` contains `list(ACC)`; the active computation is the real internal
loop `#loop(list(FIRST), Name("item"), commonLoopBody)` followed by arbitrary
`CONT`. Unmentioned map entries and configuration cells are framed.

Postcondition: the loop is consumed, heap `H` contains
`list(commonAcc(FIRST, SECOND, ACC))`, `item` contains the last value yielded
from `FIRST` (or keeps `OLD` when empty), and `CONT` resumes unchanged.

Satisfying state: take `L = 1`, `H = 0`, `FIRST = vCons(2, .ValSeq)`,
`SECOND = vCons(2, .ValSeq)`, `ACC = .ValSeq`, `OLD = 0`,
`_ORIGINAL = FIRST`, and `CONT = .K`; bind scope 1 and heap 0 exactly as the
claim requires, with all other top-level cells pristine.

## `SPEC.common-function`

Precondition: the pristine configuration loads `Module(commonDefinition)` and
then invokes the resulting global closure on arbitrary unboxed
`list(FIRST)`/`list(SECOND)` values. There is no `requires` clause.

Postcondition: execution returns the concrete reference `ref(1)`; module scope
0 holds the exact closure; heap object 0 is
`list(commonSpec(FIRST, SECOND))`; heap object 1 is
`list(sortVS(commonSpec(FIRST, SECOND)))`; exactly two heap allocations have
occurred; stack, return state, exception state, and exit code are normal.

Satisfying state used dynamically: `FIRST = [2,2,1,1]`,
`SECOND = [1,2,2]`. `commonSpec` is `[2,1]` and the claimed sorted result is
`[1,2]`. The preserved ground K claim closes with `#Top`, and both Python
implementations return `[1,2]`.

The final result is not a free variable: the returned reference is fixed to 1
and the value at heap location 1 is fixed to the result expression. The false
mutation to `ref(0)` is rejected with the residual actual value `ref(1)`.
