VALIDATED

## What is proven

Under the supplied `MPY` semantics, the exact translated body of
`match_parens` is partially correct for every two-element input list whose
elements are strings containing only `(` and `)`.  If the call terminates, its
result is:

- `Yes` exactly when either concatenation order has final parenthesis balance
  zero and no prefix with negative balance; and
- `No` otherwise.

The proof executes name lookup, argument binding, both source loops, branches,
returns, frame creation, and frame removal using the fixed reference semantics.
It contains no rule that intercepts or replaces a program computation.

## Formal claim

The entry claim is `SPEC.match-parens` in `spec.k`.  Its input is

```k
list(vCons(str(A), vCons(str(B), .ValSeq)))
```

with `parenCodes(A) andBool parenCodes(B)`.  The module scope binds
`"match_parens"` to a closure containing the exact `solution.mpy` body, with
the caller environment, scopes, heap, stack, return state, exception state, and
exit code stated explicitly.  Its postcondition is:

```k
?RESULT ==K matchAnswer(A, B)
```

`matchAnswer` is `Yes` iff
`goodParens(seqConcat(A,B)) orBool goodParens(seqConcat(B,A))`.
`goodParens` requires final balance zero and minimum prefix balance at least
zero.  The claim is a partial-correctness theorem; it is not a separate
termination proof.

## Proof-extension inventory

There are no operational bridges, opaque symbols, trusted proof-local
primitives, priority rules, or `<k>` rewrite rules in `verification.k`.

| Extension | Class and domain | Match/state/value record and justification | Dependents |
|---|---|---|---|
| `parenCodes` | Definitional summary; all `IntSeq` values | Constructor recursion; empty/cons cases are exhaustive, descend structurally, and do not match a configuration. It fixes the theorem's input domain. | Entry precondition |
| `nextBalance` | Definitional summary; all `Int × Int` | Guards `C == 40` and `C =/= 40` are disjoint and exhaustive. The `[simplification]` equations are the two exact source branches. | `scanBalance`, `scanMinimum`, loop claims |
| `scanBalance` | Definitional summary; all `IntSeq × Int` | Empty/cons equations are exhaustive and structurally descending. It names, but does not replace, the balance computed by source execution. | Loop claims, `goodParens` |
| `nextMinimum` | Definitional summary; all `Int × Int` | Guards `N < M` and `N >= M` are disjoint and exhaustive and exactly mirror the source conditional assignment. | `scanMinimum` |
| `scanMinimum` | Definitional summary; all `IntSeq × Int × Int` | Empty/cons equations are exhaustive and structurally descending; its value is connected to actual execution by both loop claims. | Loop claims, `goodParens` |
| `scanLast` | Definitional summary; all `IntSeq × Val` | Empty/cons equations are exhaustive and structurally descending. It accounts for Python's persistent `for` target local. | Loop claims |
| `goodParens` | Definitional summary; all `IntSeq` | Transparent equation: final balance is zero and minimum prefix balance is nonnegative. No execution is skipped. | `possibleMatch` |
| `possibleMatch` | Definitional summary; all pairs of `IntSeq` | Transparent disjunction over the two concatenation orders. | `matchAnswer` |
| `matchAnswer` | Definitional summary; all pairs of `IntSeq` | Guards `possibleMatch` and its negation are disjoint and exhaustive; results are the exact code sequences for `Yes` and `No`. | Entry postcondition |
| `SPEC.loop-first` | Derived auxiliary reachability claim | Exact loop term and exact five-local plain-frame map. It reads `text`, `balance`, `minimum`, and `char`; writes only `balance`, `minimum`, and `char`; preserves `lst`, `text`, the parent, arbitrary continuation, other scopes, heap, stack, return/exception state, and exit code. Its match domain and justification domain are identical because the claim itself proves that framed configuration using fixed semantics. | First source loop and entry claim |
| `SPEC.loop-second` | Derived auxiliary reachability claim | Separate proof obligation for the second syntactically identical source loop, with the same exact context and state footprint. It independently prints `#Top`. | Second source loop and entry claim |

The whole-function target claim is the theorem being proved, not an assumed
extension. `check-spec-body.py` mechanically compares its closure body with the
translator-produced `solution.mpy` body after normalizing only the two parsers'
equivalent spelling of empty `Stmts`.

## Exact commands and actual outputs

The complete reproducible command sequence is in `prove.sh`.

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py
python3 check-spec-body.py
```

Output and exit: `spec-body-identity: PASS`; exit 0.

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Exit 0. The compiler emitted only supplied-semantics warnings, including
non-exhaustive declarations outside this task's exercised operations and
unused `strLt` variables.

```bash
python3 py2mpy.py krun-tests.py > krun-tests.mpy
# prove.sh then checks AST identity with solution.py
krun krun-tests.mpy --definition runtime-kompiled --output json \
  | python3 check-krun-json.py
```

Output and exit:

```text
harness-body-identity: PASS
krun-json: .K, NoExc, exit-code 0
```

Exit 0.

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Exit 0, with only the supplied `strLt` unused-variable warnings.

```bash
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.loop-first
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.loop-second
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

Actual positive results:

```text
#Top   Exit: 0
#Top   Exit: 0
#Top   Exit: 0
```

The final command proves every claim in `SPEC` together and discharges the
whole function with both loop circularities available.

```bash
python3 differential-test.py
```

Output and exit:

```text
differential: 20481 pairs, 0 mismatches
```

Exit 0.

The A5 mutation replaces the result postcondition with the one-character
string `X`:

```bash
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit 1 with `WarnStuckClaimState`; the residual contains the
real `Yes` value `str(iCons(89,iCons(101,iCons(115,.IntSeq))))`, which cannot
match `X`. Full output is in `vacuity.log`.

The body-sensitivity mutation changes only the final source-body return from
`No` to `Yes`:

```bash
kprove spec-body-mutation.k --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit 1 with `WarnStuckClaimState` on the branch where neither
order has zero final balance. Full output is in `body-mutation.log`.

The final end-to-end command was:

```bash
./prove.sh
```

It exited 0 after all positive commands produced `#Top` and both negative
probes failed as expected.

## Gate results

### Gate A — PASS

- A1: `solution.mpy` and the entry closure body compare equal; both
  program-defined loops execute under fixed semantics and have independently
  proved exact auxiliary claims. The material body mutation is rejected.
- A2/A3: no operational bridge exists. The entry claim pins lookup, closure
  body, argument, environment, stack, heap, return and exception state. Loop
  claims explicitly account for every changed local and preserve the complete
  framed context their LHS accepts.
- A4: all proof-local functions have exhaustive, disjoint constructor or guard
  cases and structurally descending recursion. The only simplification
  equations (`nextBalance`) are true on their complete guards.
- A5: `A = .IntSeq` and `B = .IntSeq` is a satisfiable witness returning
  `Yes`; the false `X` postcondition is rejected with a stuck result.

### Gate B — PASS

The formal input is exactly a pair of parenthesis-only strings. On that domain,
code 40 is `(` and code 41 is `)`, so final balance zero plus a nonnegative
minimum prefix is precisely balanced-parenthesis goodness. The disjunction
checks both permitted concatenation orders and returns the prompt's exact
`Yes`/`No` strings. Both prompt examples are present in the LLVM harness. The
unboxed read-only list value used by the claim is observationally equivalent
for this function to the heap-allocated list used by concrete list literals.

### Gate C — PASS

Every assumption and dependent artifact is listed below. All claimed concrete,
differential, identity, mutation, and proof artifacts exist; `prove.sh`
reproduces their exact commands and checks their exit conditions. Formal proof,
conditional trust, and finite evidence are kept separate.

## Trust boundary

| Assumption | Effect and dependents | Evidence/audit |
|---|---|---|
| The supplied read-only `reference-semantics/` correctly models the exercised Python subset. | All K claims are conditional on it; it affects value, binding, control, and state. | Exact source is imported unchanged; LLVM execution covers both result branches, both orders, empty strings, and prompt examples. |
| K 7.1.293's compiler, LLVM runtime, Haskell backend, and SMT reasoning are correct. | All `krun` and `kprove` results depend on the toolchain. | Version was recorded; focused claims and full proof agree; independent Python evidence agrees on the finite domain. |
| The supplied `py2mpy.py` faithfully translates the supported CPython AST. | Connects `solution.py` to `solution.mpy`. | The required translator command succeeds; `check-spec-body.py` checks the exact generated body used by the claim; the LLVM harness's function AST is identical to `solution.py`. |

There are no proof-local trusted primitives or opaque result-bearing
abstractions.

## Empirically supported facts

- `krun-tests.py` contains six assertions: both prompt examples, empty strings,
  a direct balanced order, a reversed successful order, and an impossible
  imbalance. Its function AST is checked against `solution.py`; LLVM execution
  ends at `.K`, `NoExc`, exit code 0.
- `differential-test.py` uses an independently written early-rejection
  stack-depth oracle. It checks every pair of parenthesis strings whose
  combined length is at most 10: 20,481 pairs, zero mismatches.
- `spec-vacuity.k` and `spec-body-mutation.k` are generated artifacts whose
  expected nonzero results are checked by `prove.sh`.

These finite tests support the semantics/intent bridge but do not replace the
universal K proof.

## Excluded behavior

- Inputs other than a list of exactly two strings containing only `(` and `)`.
- Python behaviors outside the supplied semantics, including arbitrary Unicode,
  unrelated exceptions, concurrency, I/O, and external state.
- A general theorem about arbitrary preexisting heaps or aliased mutable input
  objects; the function itself performs only read operations on its input.
- Termination/liveness as a separate formal theorem. The reported K claims are
  partial-correctness reachability claims.
