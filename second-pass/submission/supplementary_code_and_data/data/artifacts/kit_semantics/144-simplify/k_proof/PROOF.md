VALIDATED

## What is proven

Under the supplied Python reference semantics, `solution.py`'s exact translated
`simplify(x, n)` body returns `True` exactly when the product of the two valid
positive fractions is a whole number.

The theorem covers arbitrary finite, nonempty digit sequences, including
arbitrarily large values and leading zeroes. It is not a bounded-size proof.
As with the Kit, the reachability result is a partial-correctness theorem.

## Formal claim

`spec.k` invokes the exact `simplifyBody` closure on symbolic nonempty strings
`str(iCons(XHEAD, XTAIL))` and `str(iCons(NHEAD, NTAIL))`.

The precondition requires:

- `XHEAD` is an ASCII decimal digit; and
- `validScan(XTAIL ++ "/" ++ iCons(NHEAD, NTAIL),
  0, XHEAD - 48, 0, 0, 0)`.

`validScan` structurally accepts exactly three slash transitions, accepts only
ASCII digit codes otherwise, and requires all four Horner accumulators to be
positive at the end. Every pair of valid source-contract fractions satisfies
this precondition. The formal domain is actually a harmless superset because
the predicate validates the combined `x + "/" + n` stream; no valid
source-contract input is excluded.

The postcondition is:

```k
scanResult(xCodes ++ "/" ++ nCodes, 0, 0, 0, 0, 0)
```

The exhaustive `scanResult` equations perform the same four Horner folds. Its
valid base case is:

```k
pyMod(A *Int C, B *Int D) ==Int 0
```

Since `B` and `D` are positive, this is exactly the statement that
`(A / B) * (C / D)` is a whole number.

The seven bridge-free claims in `loop-spec.k` establish the loop obligations:
four digit phases and the three slash transitions. Together they are the
universal connection theorem used by the final proof.

## Proof-extension inventory

### `simplifyBody`, `simplifyLoopBody`, and `simplifyReturn`

- Class: definitional summaries.
- Semantic role: name exact AST terms; they do not replace execution.
- Domain and context: closed, argument-free terms.
- State footprint: none.
- Value/control influence: `simplifyBody` is executed by the target;
  `simplifyLoopBody` and `simplifyReturn` constrain the connection claims and
  bridge guards.
- Value justification: their equations are the literal translated body.
- Dependents: all loop claims, both bridges, and the target claim.
- Validation: `python3 check_body_identity.py` regenerates `solution.mpy` with
  `py2mpy.py`, expands these aliases, normalizes only explicit empty list
  terminators, and reports both comparisons as true.

### `simplifyScope`

- Class: definitional summary.
- Semantic role: names the exact callee scope map; it does not replace a state
  transition.
- Domain: all two `Val` arguments, phase/accumulator `Int` arguments, and the
  current character `Val`.
- Matched context: scope location 1 with parent module scope 0 and exactly the
  eight local bindings `x`, `n`, `part`, `a`, `b`, `c`, `d`, and `ch`.
- State footprint: none by itself.
- Value influence: constrains the bridge match domain.
- Justification and validation: a single exhaustive equation; its expansion is
  exactly the scope created by fixed call/binding/assignment execution.
- Dependents: all loop claims and both bridges.

### `validScan`

- Class: definitional summary.
- Semantic role: a mathematical/domain predicate; it does not replace program
  execution.
- Domain: all `IntSeq` values, all phase integers, and all four accumulator
  integers.
- Equations: disjoint cases for empty/cons sequences and phases 0 through 3,
  plus an `owise` false case. The equations are total, and recursion strictly
  decreases the remaining `IntSeq`.
- Value influence: target precondition and bridge guards.
- Value justification: digit cases use the exact Horner update
  `ACC * 10 + (CODE - 48)`; slash cases advance exactly one phase; the base
  requires phase 3 and four positive values.
- Dependents: all loop claims, both bridges, and the target claim.
- Validation: prompt examples, leading-zero and large-number LLVM cases, and
  161,005 differential cases all satisfy the same accepted grammar.

### `scanResult`

- Class: definitional summary.
- Semantic role: names the mathematical result threaded through the invariant;
  it does not replace execution.
- Domain: it is defined on every state for which `validScan` is true.
- Equations: digit and slash cases are disjoint (`47` versus `48..57`);
  recursion strictly decreases `IntSeq`; the positive phase-3 base returns the
  exact `pyMod(A*C, B*D) == 0` property.
- Value influence: the returned Boolean and final postcondition.
- Value justification: exhaustive structural equations thread the
  result-characterizing invariant through every character; the requested
  result is not asserted by a standalone lemma.
- Dependents: all loop claims, both bridges, and the target.
- Validation: the bridge-free loop proof reaches this value, and the
  `fractions.Fraction` differential oracle agrees on every tested case.

### Claims `loop-phase-0..3` and `loop-slash-0..2`

- Class: derived reachability lemmas/circularities.
- Semantic role: execute the exact fixed-semantics loop body and return
  continuation; no operational bridge is imported by `VERIFICATION-BASE`.
- Domain: the four digit claims require the corresponding phase, a digit head,
  and a valid recursive tail. The three slash claims require phases 0, 1, or 2
  and the valid next phase.
- Matched context: exact `#loop` term, exact loop body, exact
  `(simplifyReturn .Stmts) ~> #endcall` continuation, environment 1, exact
  module/callee/builtin scopes, scope location 2, empty heap at heap location
  0, exact `frame(.K, 0, 1)`, `noRet`, and `NoExc`. The omitted exit-code cell
  is preserved and unobserved.
- State footprint: fixed execution updates `ch`, `part`, and the selected
  accumulator, then removes callee scope 1, restores environment/scope
  location/stack, and returns the Boolean. Heap, heap location, module scope,
  builtin scope, exception state, and exit code are preserved.
- Value justification: `scanResult`'s one-character equation is exactly the
  loop's one-character update.
- Dependents: the two final operational bridges.
- Validation: all seven claims together print `#Top` using
  `verification-base-kompiled`, which contains no bridge rules.

### `loop-digit-bridge`

- Class: operational bridge.
- Semantic role: accelerates the exact remaining digit-phase loop plus exact
  return and frame pop.
- Domain: `0 <= P <= 3`, digit head, `validScan` true, and equality guards
  fixing the loop body, return statement list, callee scope, and builtin scope.
- Matched context: exact continuation `.K`, environment 1, module scope 0,
  callee scope 1, builtin scope -1, scope location 2, empty heap/heapLoc 0,
  exact stack frame, `noRet`, `NoExc`, and a preserved arbitrary exit code.
- Justification scope: the union of bridge-free claims `loop-phase-0..3`.
  `validScan`'s phase equations show the generic guard is exactly that union.
- Context containment: every body, continuation, binding, cell, and phase
  accepted by the bridge occurs in one of those four claims; there is no
  continuation frame or state wildcard beyond the preserved exit code.
- State footprint/value/control: exactly the footprint recorded for the
  connection claims, including return, scope removal, and stack restoration.
- Dependents: `simplify-full-domain`.
- Validation: universal bridge-free `#Top`, exact body-identity check, priority
  40 only after connection, concrete LLVM agreement, false-result rejection,
  and empty-body mutation rejection.

### `loop-slash-bridge`

- Class: operational bridge.
- Semantic role: accelerates the exact remaining slash-transition loop plus
  return and frame pop.
- Domain: `0 <= P < 3`, slash head code 47, `validScan` true, and the same exact
  body/return/scope/builtin equality guards.
- Matched context, state footprint, value/control influence, and containment:
  identical to the digit bridge, restricted to the three slash phases.
- Justification scope: the union of bridge-free claims
  `loop-slash-0..2`; the guard is exactly that union.
- Dependents: `simplify-full-domain`.
- Validation: the same universal, body-identity, concrete, mutation, and
  differential evidence as the digit bridge.

The two bridge domains do not overlap: code 47 is not an ASCII digit code.

## Exact commands and actual outputs

The complete reproducer is `./prove.sh`; its final run exited 0.

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 check_body_identity.py
```

Output:

```text
solution_mpy_matches=True proof_body_matches=True
```

```bash
python3 differential_test.py
```

Output:

```text
cases=161005 mismatches=0
```

```bash
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled
```

Output and exit:

```text
<k> .K </k>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
Exit: 0
```

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
kprove loop-spec.k \
  --definition verification-base-kompiled \
  --spec-module LOOP-SPEC
```

Output and exit:

```text
#Top
Exit: 0
```

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Output and exit:

```text
#Top
Exit: 0
```

The compiler also printed only warnings from the supplied semantics
(unused variables and pre-existing non-exhaustive total-function matches) and
unused proof variables; all positive commands exited 0.

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result:

```text
WarnStuckClaimState
<k> true ~> .K </k>
Exit: 1 (expected)
```

```bash
kprove body-mutation-spec.k \
  --definition verification-base-kompiled \
  --spec-module BODY-MUTATION-SPEC
```

Actual result:

```text
WarnStuckClaimState
applyBin("%", 1, 0) ...
Exit: 1 (expected)
```

## Gate results

### Gate A — PASS

- A1: fixed execution proves all seven exact loop connection claims without
  bridges. `check_body_identity.py` establishes source/MPY/proof-body identity.
  Replacing the parser loop body with `.Stmts` makes the proof fail.
- A2: the connection claims and bridges enumerate and agree on every active
  state cell; return, frame pop, scope removal, and stack restoration are
  included.
- A3: exact body, return statement-list continuation, scopes, builtins,
  environment, stack, and guards fix binding/evaluation/control. Bridge
  priority is admitted only after the universal connection proof.
- A4: all definitional equations are disjoint and terminating on their stated
  domains; `validScan` is total; `scanResult` covers every `validScan`-true
  state; digit/slash bridges are disjoint.
- A5: `"1/5", "5/1"` is a realizable true witness. The false-result mutation
  reaches `true` and is rejected with exit 1.

### Gate B — PASS

- B1: arbitrary finite valid positive fraction strings are covered. There is
  no size or integer bound, and leading zeroes are included.
- B2: the supplied semantics models strings as code sequences and its literal
  path is ASCII-only. The theorem covers every valid ASCII decimal fraction
  represented by that model. Unicode numeral spellings outside this fixed
  model are an explicit model boundary, not a proof-created length bound.
- B3: `scanResult`'s formal equations thread the four decimal accumulators and
  reduce at the valid base to the requested modulo property.
- B4: the implementation computes that same property.

### Gate C — PASS

- All proof-local symbols, equations, claims, and bridges are inventoried
  above.
- Every claimed test, connection proof, body check, mutation, and differential
  run has an existing artifact and exact command in `prove.sh`.
- Formal facts, fixed-model trust, finite evidence, and excluded inputs are
  separated below.

## Trust boundary

The proof trusts the supplied, unmodified `reference-semantics/`, K
v7.1.293/Haskell backend and its SMT reasoning, LLVM concrete backend, and the
fixed `py2mpy.py` translator. The fixed semantics' integer operations,
`ord`, string iteration/concatenation, function frames, and `pyMod` are inside
that trusted reference model.

There are no opaque proof-local values and no unproved operational bridge.
The only model boundary material to the source contract is the supplied
semantics' ASCII string representation. Invalid fractions, zero
numerators/denominators, non-digit fields, and extra/missing separators are
outside the prompt's precondition and are rejected by `validScan`.

## Empirically supported facts

- `concrete-tests.py` executes the three prompt examples, a leading-zero case,
  and a large-integer case under both CPython and the LLVM K semantics.
- `differential_test.py` uses Python's independently implemented
  `fractions.Fraction` normalization as the oracle. It checks the prompt and
  boundary cases, every `a,b,c,d` in `1..20` (160,000 cases), and 1,000 seeded
  random 30-digit/leading-zero cases: 161,005 total, zero mismatches.
- These finite checks support implementation/model adequacy; the universal
  result comes from the two `#Top` proof commands, not from testing.

## Excluded behavior

Inputs violating the prompt's valid-positive-fraction assumption are excluded,
including empty fields, non-ASCII digits or other characters, wrong separator
counts, and zero-valued numerator or denominator fields. Python exceptions on
such invalid inputs are not claimed. Termination is not a separate theorem;
the Kit result is partial correctness over finite strings.
