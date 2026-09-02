# Claim preconditions, postconditions, and satisfying witnesses

## `SPEC.incr-loop`

The starting computation is the real loop head
`#loop(list(intVals(IS)), Name("x"), incrLoopBody) ~> CONT`.  The current
scope at location `L` contains an arbitrary input binding `l`, a `result`
binding to heap reference `H`, and an existing `x` value.  Heap address `H`
contains `list(PREFIX)`.  There is no `requires` condition.

At completion, the continuation is exactly `CONT`; the same accumulator
address contains `list(valSeqConcat(PREFIX, incrVals(IS)))`; and the final
`x` binding is existentially unconstrained.  Other scope and heap entries are
framed.

A concrete satisfying constructor state is:

```text
IS = iCons(2, iCons(-1, .IntSeq))
CONT = .K
L = 1
H = 0
_INPUT = list(intVals(iCons(2, iCons(-1, .IntSeq))))
_OLD_X = 99
_PAR = parent(0)
_REST_SCOPES = .Map
PREFIX = vCons(7, .ValSeq)
_REST_HEAP = .Map
```

The post-state accumulator is
`vCons(7, vCons(3, vCons(0, .ValSeq)))`, corresponding to `[7, 3, 0]`.

## `SPEC.incr-list`

The input parameter is any algebraic `IntSeq IS`; there is no `requires`
restriction.  The claim starts from the semantics' exact initial module
configuration, loads `solutionProgram`, calls `incr_list` with
`list(intVals(IS))`, and applies the post-call observer.

The destination result is `list(?RESULT)` with the mandatory condition
`?RESULT ==K incrVals(IS)`.  The final scopes, heap, and heap counter are
existential, while environment, stack, return state, and exception state must
have the displayed normal values.

Two satisfying substitutions are:

```text
IS = .IntSeq
expected ?RESULT = .ValSeq

IS = iCons(2, iCons(-1, .IntSeq))
expected ?RESULT = vCons(3, vCons(0, .ValSeq))
```

The matching K ground claims are preserved in `spec-ground-witness.k`; native
substitutions against both Python implementations are recorded in
`stage4-witness-check.log`.
