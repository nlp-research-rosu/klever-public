VALIDATED

## What is proven

For every finite modeled string `str(IS)`, any terminating call to the exact
translated `is_happy` closure has Boolean result

```k
(isLen(IS) >=Int 3) andBool scanHappy(IS, 0, -1, -1)
```

under the supplied `MPY` reference semantics. `scanHappy` structurally scans
the character-code sequence. Its first two steps establish the two-character
history; every later step conjoins the three pairwise inequalities for the
current three-character window. Thus the result is true exactly when the input
has length at least three and every three consecutive characters are distinct.

This is a reachability/partial-correctness result under the Kit contract. The
entry computation is the call after the module-level function binding has been
installed. The claim includes the exact closure body, argument binding,
builtins scope, empty heap and stack, scope allocator, return state, and
exception state. Module loading itself and the exit-code cell are not observed.

## Formal claims and obligations

`SPEC.loop-invariant` starts at the reference semantics' real `#loop` term with
`I >=Int 2`. It proves:

- final `happy` is `H andBool scanHappy(IS, I, P2, P1)`;
- final `i` is `I +Int isLen(IS)`;
- the fixed loop executes and consumes its remaining `str(IS)` iterator;
- `s`, the environments, and the scoped bindings outside the loop's local
  updates are preserved; the unobserved final history/code bindings exist.

The base case is `.IntSeq`, where `scanHappy` is true and the loop performs no
updates. In the inductive case, fixed semantics yields head code `C`, executes
the exact Python loop body, and re-establishes the claim on `REST`; the
corresponding `scanHappy` equation supplies precisely the window condition.

`SPEC.is-happy` executes the exact closure. It symbolically handles strings of
length zero, one, and two, unrolls the first two iterations, uses the loop claim
from `i = 2` onward, and evaluates `i >= 3 and happy` to the stated result.

## Proof-extension inventory

### `scanHappy`

- **Class:** definitional summary.
- **Semantic role:** names the mathematical result of the remaining scan; it
  never rewrites a Python term or skips execution.
- **Domain:** every finite `IntSeq` and all `Int` values for `I`, `P2`, and
  `P1`.
- **Matched context / justification scope:** no operational context is
  matched. The empty-sequence equation and the two constructor equations are
  the complete definition.
- **Coverage and overlap:** `.IntSeq` is disjoint from `iCons`; on `iCons`, the
  guards `I <Int 2` and `I >=Int 2` are disjoint and exhaustive. Recursion is
  structural on `REST`.
- **State footprint:** none.
- **Value influence:** the loop invariant's final `happy` binding and the
  target postcondition.
- **Value justification:** for `I >= 2`, the equation conjoins exactly
  `C != P1`, `C != P2`, and `P1 != P2`, then advances the two-code history.
  The fixed-execution loop claim connects this value to the Python body.
- **Dependents:** both claims.
- **Validation:** the positive proof closed; negating this summary in
  `spec-vacuity.k` was rejected; concrete and independent differential tests
  exhibit both true and false outcomes.

### `SPEC.loop-invariant`

- **Class:** derived reachability claim/circularity.
- **Semantic role:** summarizes fixed execution of the real `#loop`; it is not
  an operational rewrite.
- **Domain:** a remaining `str(IS)` iterator, Boolean `H`, integer history and
  counter values, and `I >=Int 2`.
- **Matched context:** the exact target `Name("ch")`, exact loop body, local
  scope at location 1, builtins at -1, module scope at 0, and an arbitrary
  framed continuation in `<k>`.
- **Justification scope / containment:** the machine-checked claim has the same
  context and arbitrary continuation it later accepts as a circularity. The
  body has no return, break, continue, exception, allocation, or other abrupt
  control.
- **State footprint:** reads/updates `happy`, `previous2`, `previous1`, `i`,
  `ch`, and `code`; reads the iterator; preserves `s`, environment structure,
  and every omitted/framed cell.
- **Value influence:** supplies final `happy` and `i` to the entry claim.
- **Justification:** base and structural-step reachability under fixed `MPY`
  rules plus the truthful `scanHappy` equations.
- **Dependents:** `SPEC.is-happy`.
- **Control/value validation:** the claim itself printed `#Top` in focused
  construction, the full proof printed `#Top`, concrete execution agrees, and
  both the body and summary mutations were rejected.

There are no proof-local simplification rules, concrete rules, priority rules,
ordinary operational rewrites, opaque values, operational bridges, or trusted
primitives.

## Reproducible commands and actual results

The complete rerunnable command sequence is in `prove.sh`.

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py
python3 differential_test.py
```

Actual result: all exited 0; the differential test printed:

```text
differential cases: 3290, mismatches: 0
```

Concrete LLVM execution:

```bash
python3 py2mpy.py smoke.py > smoke.mpy
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled --output none
```

Actual result: all exited 0. `krun --output none` intentionally printed no
configuration. The supplied semantics emitted compile-time coverage warnings
in unrelated float/list helpers; none is exercised by this program.

Symbolic build and complete positive proof:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual result: compilation exited 0; `kprove` printed:

```text
#Top
```

and exited 0. This full command proves both claims together and keeps the loop
claim available to the entry claim.

Gate A5 false-postcondition probe:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit 1 with `WarnStuckClaimState`. The residual requires a
symbolic Boolean to equal its own negation:

```text
scanHappy ( R0 , 2 , C , C0 ) ==Bool
notBool scanHappy ( R0 , 2 , C , C0 )
```

Gate A1 body-sensitivity probe:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual result: exit 1 with `WarnStuckClaimState` after mutating the closure's
initial `happy = True` to `happy = False`. The residual contains:

```text
false ==Bool scanHappy ( R0 , 2 , C , C0 )
```

## Gate results

### Gate A — PASS

- **A1:** `solution.mpy` is generated from `solution.py`; the target claim
  contains the corresponding exact closure body and executes it via fixed
  function/call/loop semantics. `differential_test.py` checks that the function
  AST copied into the LLVM smoke artifact is identical. The material body
  mutation exits 1.
- **A2/A3:** no execution is bridged or skipped. The target pins the
  `is_happy` closure binding and builtins scope; fixed semantics performs
  lookup, argument binding, left-to-right evaluation, iteration, return, and
  frame popping. The loop claim's arbitrary continuation is within its own
  universally machine-checked context, and the loop body has no abrupt
  control.
- **A4:** the only new equations are disjoint, exhaustive, structurally
  descending `scanHappy` equations. No conflicting or off-domain equation
  exists.
- **A5:** realizable witnesses include `"adb"` (true) and `"xyy"` (false).
  LLVM smoke execution checks both, and the negated-postcondition proof exits
  1.

### Gate B — PASS

- **Input domain:** exactly modeled strings `str(IS)`, matching the prompt's
  string input. Non-string Python objects are outside the theorem.
- **Language model:** the proof uses the supplied reference semantics as
  required. Its direct formal input is an arbitrary finite code sequence.
  Concrete literal smoke tests are ASCII because that parser path is
  ASCII-only; this does not restrict the symbolic `str(IS)` theorem.
- **Summary/property adequacy:** by structural induction on `IS`,
  `scanHappy(IS, 0, -1, -1)` is the conjunction of pairwise distinctness for
  every length-three window. The `isLen(IS) >= 3` conjunct supplies the prompt's
  minimum-length condition.
- **Implementation alignment:** all prompt examples, overlapping-window cases,
  and the independent finite differential sample agree with the contract.

### Gate C — PASS

- **Trust ledger:** proof-local trust is empty. The trusted base is the
  user-supplied `MPY` semantics (notably its core, iterator, string, builtin,
  operator, control, function, and call rules), `py2mpy.py`, the K
  compiler/prover, the Haskell backend, and its SMT reasoning. Both claims
  depend on that base. No imported opaque float, sort, or digest operation is
  reachable in this program.
- **Evidence:** `smoke.py`/`smoke.mpy` contain the prompt examples and two
  overlap cases; `differential_test.py` uses an independent set-based oracle
  over every string on alphabet `{a,b,c}` of lengths 0 through 7, plus ten
  named cases, for 3290 comparisons and zero mismatches. The two mutation
  artifacts and their exact commands are preserved.
- **Result language:** `#Top` establishes the two reachability claims under the
  supplied theory. Finite tests support implementation/intent alignment but
  are not presented as universal proofs.

## Excluded behavior

- non-string Python inputs and behavior outside the supplied semantics;
- module loading before the exact function binding used by the entry claim;
- parser-level non-ASCII K literals in concrete smoke programs;
- liveness as a separate theorem, resource bounds, and equivalence to all of
  CPython beyond the supplied reference model.
