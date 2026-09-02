# Claim witnesses and concrete substitutions

These are reviewer-selected satisfiable states. The executable comparisons are
recorded in `stage2_differential.log`, `stage3_krun_concrete.log`,
`stage4_pinning_retry.log`, `stage5_fixed_control.log`, and
`stage5_bridge_control.log`.

## `SPEC.digit-loop`

Choose `L = 1`, `N = 1`, `XS = .ValSeq`, `RH = 0`, `W = 1`, and a plain local
scope with exactly `x`, `result`, `value`, `number`, and `valid`, parent `0`.
Set `number = 1`, `valid = true`, and heap location `0` to any list. This
satisfies `N >Int 0`. Fixed execution and bridge execution both reach
`number = 0`, `valid = true`; the analogous `N = 2` witness reaches
`valid = false`. Both execute the trailing assignment `value = 7`.

## `SPEC.outer-loop`

Choose `L = 1`, `H = 0`, `ACC = .ValSeq`, and
`VS = vCons(15, vCons(33, vCons(1422, vCons(1, .ValSeq))))`. Every element is
an integer greater than zero, so `positiveIntSeq(VS) = true`. The claim's
post-state changes heap location `0` from `list(.ValSeq)` to
`list(vCons(15, vCons(33, vCons(1, .ValSeq))))`; final scratch locals are
existential and do not affect the result.

## `SPEC.unique-digits`

The exact pre-state is the one written in the claim: module environment `0`,
only the translated `unique_digits` closure in scope `0`, builtins in scope
`-1`, empty heap, next scope location `1`, next heap location `0`, empty stack,
`noRet`, `NoExc`, and exit code `0`.

Two concrete substitutions are:

| `VS` | `positiveIntSeq` | `oddDigitFilter(VS)` | claimed sorted result | canonical Python | generated Python |
|---|---:|---|---|---|---|
| `.ValSeq` | true | `.ValSeq` | `[]` | `[]` | `[]` |
| `[15, 33, 1422, 1]` | true | `[15, 33, 1]` | `[1, 15, 33]` | `[1, 15, 33]` | `[1, 15, 33]` |
| `[152, 323, 1422, 10]` | true | `[]` | `[]` | `[]` | `[]` |
| `[33, 1, 33, 2, 1]` | true | `[33, 1, 33, 1]` | `[1, 1, 33, 33]` | `[1, 1, 33, 33]` | `[1, 1, 33, 33]` |

The increasing-order column uses the supplied `sortVS` contract. Its concrete
insertion-sort execution is exercised by the fresh LLVM run; the Haskell target
claim retains `sortVS` as an opaque symbolic term.
