VALIDATED

## What is proven

Under the supplied MPY reference semantics, every terminating call of the exact
`unique_digits` implementation in `solution.py` on a finite list whose elements
are integers returns a newly allocated list represented by

```k
list(sortVS(collect(.ValSeq, XS)))
```

The fold `collect` preserves input order and retains exactly those elements for
which the exact digit-loop summary `scanBad(0, intOf(V))` is zero.  For the
HumanEval domain of positive integers, this means that every retained decimal
digit is odd.  The final ascending-order conclusion is conditional on the
supplied semantics' documented `sortVS` contract.

The theorem is partial correctness, as is standard for K reachability claims:
it constrains every terminating execution but does not independently prove
termination.

## Formal claim

`SPEC.program` in `spec.k` starts from the reference configuration with the
exact translated function body, executes `FuncDef`, resolves and calls
`unique_digits`, and universally quantifies `XS:ValSeq` subject to
`integerVals(XS)`.

At completion it proves all of the following:

- the returned value is `ref(1)`;
- heap object `0` is `list(collect(.ValSeq, XS))`, the unsorted filtered
  accumulator;
- heap object `1` is `list(sortVS(collect(.ValSeq, XS)))`;
- the call frame has been popped, the module binding is preserved, the
  exception cell is `NoExc`, and the exit code is `0`.

`SPEC.digit-loop` is the inner-loop circularity.  It proves that the loop
updates `bad` to `scanBad(B, N)` and updates `number` to `scanNumber(N)`.
`SPEC.outer-loop` is the outer-loop circularity.  It proves the exact
accumulator fold and also constrains the persistent Python loop locals
`value`, `number`, and `bad`.

The singleton expression `sum((value,))` is executed by the fixed semantics.
For integer elements it equals `value`; it is present to expose the result at
sort `Int` to the symbolic backend and has no source-level effect on the
function result.

## Proof-extension inventory

No proof-local rule replaces a program expression, statement, call, loop, or
control transition.  `verification.k` contains only mathematical summaries;
all program-defined operations execute under the supplied semantics.

| Extension | Class and semantic role | Domain, context, and state footprint | Justification and dependents |
|---|---|---|---|
| `integerVals` | Definitional summary; does not replace execution | Total on `ValSeq`; empty/cons equations are disjoint and exhaustive | Defines the theorem's input domain. Used by `outer-loop` and `program`. |
| `scanBad` | Definitional summary of the final integer counter | Total on `(Int, Int)`. Guards `N <= 0` and `N > 0` are disjoint/exhaustive. For `N > 0`, decimal division strictly decreases a nonnegative `N`. | Its equations exactly mirror one digit-loop iteration. Connected to execution by `SPEC.digit-loop`; used by filtering and `afterBad`. |
| `scanNumber` | Definitional summary | Total unconditional equation: `0` for positive `N`, otherwise `N` | Matches the loop guard's final `number`; connected by `SPEC.digit-loop`. |
| `appendCandidate` | Definitional summary | Used when `isInt(V)`; the zero/nonzero `scanBad` guards are disjoint and exhaustive in that domain | Names the exact append-or-skip effect. Used only by `collect`. |
| `collect` | Definitional summary | Empty/cons recursion over integer-only `ValSeq`; no rule applies outside the stated integer domain | Exact outer-loop accumulator fold. Connected by `SPEC.outer-loop`; used by `SPEC.program`. |
| `afterValue`, `afterNumber`, `afterBad` | Definitional summaries | Constructor-disjoint recursion over the remaining list; `afterValue` is total, and the other two are complete on integer lists | Constrain Python's persistent loop locals in `SPEC.outer-loop`. |
| `SPEC.digit-loop` | Derived reachability lemma/circularity; reasons about rather than replaces execution | Matches the exact `#while` body in any continuation and a plain five-key function frame. Reads/writes only `number` and `bad`; preserves `x`, `result`, `value`, and all framed cells. | Proved by fixed MPY execution and the truthful `scanBad`/`scanNumber` equations. Used by the outer and entry claims. |
| `SPEC.outer-loop` | Derived reachability lemma/circularity; reasons about rather than replaces execution | Matches the exact `#loop`, exact function/module bindings, result heap object, call frame, and an arbitrary caller continuation. It writes `value`, `number`, `bad`, and heap object `0`; other named cells are preserved. | Proved by fixed MPY execution, `SPEC.digit-loop`, and the fold equations. Used by `SPEC.program`. |
| imported `sortVS` | Trusted primitive supplied by the fixed reference semantics | Symbolic `ValSeq`; affects the final returned list's ordering and permutation | The K proof is conditional on the supplied contract that `sortVS` is ascending sort. LLVM concrete execution and differential tests provide finite evidence. |

There are no proof-local simplification lemmas, opaque program-derived values,
priority rules, or operational bridges.  Consequently there is no widened
bridge context or skipped binding/control/state transition to justify.

## Exact commands and actual outputs

All commands are recorded in executable `prove.sh`.  The complete reproduction
was run as:

```bash
./prove.sh > prove.log 2>&1
```

It exited `0`.  The material commands inside it are:

```bash
python3 py2mpy.py solution.py > solution.mpy
cmp <(python3 py2mpy.py solution.py) solution.mpy
python3 validate.py
python3 py2mpy.py concrete.py > concrete.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete.mpy --definition runtime-kompiled | tee concrete.krun
python3 validate_krun.py

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual positive evidence in `prove.log`:

```text
differential cases=1513 mismatches=0
krun expected-fragments=7 missing=0
#Top
```

The positive `kprove` command exited `0`.  Compiler warnings are confined to
unused variables in the supplied semantics and framed variables in the claims;
there were no positive-run errors.

The body-sensitivity mutation changes every digit test from `% 2` to `% 3`
while leaving `scanBad` unchanged:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  --claims SPEC-BODY-MUTATION.digit-loop
```

It exited `1` with `WarnStuckClaimState`; the residual explicitly contrasts the
`%Int 2` summary with `%Int 3` execution.  `prove.sh` records:

```text
EXPECTED FAILURE: body mutation rejected
```

The result mutation changes the entry destination from `ref(1)` to `ref(0)`:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.digit-loop,SPEC-VACUITY.outer-loop,SPEC-VACUITY.program
```

It exited `1` with `WarnStuckClaimState`.  Its residual contains the actual
`<k> ref ( 1 )` and cannot match the mutated destination.  `prove.sh` records:

```text
EXPECTED FAILURE: false result mutation rejected
```

## Gate results

### Gate A — PASS

- A1: The exact translated function body appears in the entry claim and the
  exact loop bodies appear in both circularities.  Fixed semantics executes
  definitions, lookup, calls, tuple construction, `sum`, both loops, append,
  return, and `sorted`.  The `% 3` body mutation is rejected.
- A2/A3: There is no operational bridge.  The claims constrain all state
  touched by their regions, including locals, heap mutation, frames, return,
  exception, and exit cells.  The input is the reference semantics' documented
  unboxed read-only list representation; the function does not mutate or test
  the identity of `x`.
- A4: All total equations have disjoint/exhaustive cases.  Partial summaries
  are guarded and are used only under `integerVals`; recursive calls descend
  structurally or by positive decimal division.
- A5: `XS = .ValSeq` is a realizable precondition witness, and the concrete
  examples are nonempty witnesses.  Mutating the returned reference from
  `ref(1)` to `ref(0)` is rejected after the actual execution reaches
  `ref(1)`.

### Gate B — PASS

- The HumanEval contract requires finite lists of positive integers.  The
  formal domain is broader—finite lists of all integers—so it includes every
  required input without strengthening the source precondition.
- On positive integers, repeated `% 2` and `// 10` scans exactly the decimal
  digits; `scanBad == 0` means no even digit was encountered.  Duplicates are
  preserved.
- `collect` is an execution characterization.  Its connection to the
  human-facing digit property is supported by the decimal equations and by the
  independent string-oracle differential test.
- Ascending order is conditional on the supplied `sortVS` contract.  This is
  the fixed semantics' explicit external sorting boundary, not a
  program-derived abstraction.

### Gate C — PASS

- The trust ledger below identifies every unproved boundary and its
  dependents.
- `validate.py`, `concrete.py`, `concrete.mpy`, `concrete.krun`,
  `validate_krun.py`, both mutation specs, `prove.log`, and `prove.sh` exist.
- Every empirical and mutation claim above has an exact reproducible command,
  input scope, oracle, actual outcome, and mismatch/exit result.
- Formal conclusions, conditional conclusions, finite evidence, and excluded
  behaviors are kept separate.

## Trust boundary

| Component | Why unproved here | Influence | Dependents and evidence |
|---|---|---|---|
| Supplied MPY semantics and K/Haskell backend | Required fixed foundation of the benchmark | All modeled values, control, state, and proof search | All claims. Concrete LLVM execution and CPython comparison provide independent finite checks. |
| `sortVS` in `MPY-SORT` | Intentionally opaque for symbolic arguments in the supplied semantics | Final list permutation and ascending order | `SPEC.program`. Three asserted LLVM examples and 1,513 CPython/string-oracle differential cases support the contract on tested inputs. |
| Partial-correctness termination assumption | Reachability proof does not establish liveness | Whether a result is eventually produced | All reachability conclusions are conditional on termination. Concrete tests terminate; source loops visibly decrease finite structures, but no separate liveness theorem is claimed. |

## Empirically supported facts

`validate.py` uses an independently implemented string oracle:

```python
sorted(v for v in values if all(d in "13579" for d in str(v)))
```

It checks the prompt examples, empty/all-keep/all-drop cases, every singleton
from `1` through `1000`, selected large boundaries, and 500 deterministic
random lists of length `0` through `12` with values up to `1,000,000,000`.
There were 1,513 cases and zero mismatches.

`concrete.py` runs three cases under the LLVM MPY semantics.
`validate_krun.py` asserts their module bindings, returned heap objects, and
zero exit code.  All seven expected fragments were present.

These finite tests support adequacy and the supplied sorting contract; they do
not replace the universal reachability proof.

## Excluded behavior

- Non-integer elements are outside `integerVals`.
- The HumanEval meaning is asserted only for positive integers; the formal
  theorem also characterizes zero and negative integers according to the
  literal source loop.
- Aliasing, mutation, or identity observations on the input list are not part
  of the function and are not observed by the theorem boundary.
- Exceptions and behavior outside the supplied Python subset are excluded.
- Termination and resource bounds are not separately proved.
