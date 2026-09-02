VALIDATED

## What is proven

Under the supplied reference semantics and the proof-local mathematical
definitions in `verification.k`, the following partial-correctness theorem is
machine checked for every K `Int` value `N`:

> Calling the exact translated `even_odd_count` closure with `N` returns a
> two-element tuple whose first component is the number of even decimal digits
> of `abs(N)` and whose second component is the number of odd decimal digits.
> Zero has the one-digit representation `"0"`, hence returns `(1, 0)`.

The theorem includes name lookup, argument evaluation, the `abs` builtin,
function-frame creation, parameter binding, the exact program body, return
control, frame removal, and restoration of caller state. It is a
partial-correctness result; termination is not a formal conclusion.

## Formal claim and scope

`SPEC.even-odd-count` in `spec.k` starts from:

- `<k> Call(Name("even_odd_count"), N:Int) </k>`;
- module binding `"even_odd_count" |-> evenOddClosure`;
- the supplied builtins scope;
- empty heap and stack, module environment 0, `noRet`, `NoExc`, and exit code 0.

It ends in `tuple(vCons(?ER, vCons(?OR, .ValSeq)))`, with:

```text
?ER ==Int decEven(N)
?OR ==Int decOdd(N)
```

The formal domain is all unbounded mathematical integers (`N:Int`), with no
sign or magnitude restriction. The result tuple is the observable result. The
final environment, scopes, heap, stack, return state, exception state, and exit
code are also constrained by the claim.

For positive `n`, the proof summaries use:

```text
q = (n - pyMod(n, 10)) /Int 10
p = pyMod(n, 2)

evenPos(0) = 0
oddPos(0)  = 0
evenPos(n) = 1 - p + evenPos(q)
oddPos(n)  = p     + oddPos(q)
```

This is decimal digit removal by division by 10. A digit has the same parity as
the represented integer, so `p` is precisely the oddness of the removed final
digit. `decEven` and `decOdd` add the special representation of zero and apply
the positive summaries to the magnitude of negative inputs.

## Proof-extension inventory

### Exact program syntax

**Extensions:** `evenOddBody` and `evenOddClosure`.

- **Class:** definitional summaries.
- **Semantic role:** name the exact translated `Stmts` value and closure; they
  do not replace execution.
- **Domain and matched context:** unconditional constructor equations, with no
  operational configuration match.
- **State footprint:** none.
- **Value influence:** fixes the closure body used by the entry and identity
  claims.
- **Value justification:** `IDENTITY-SPEC.translated-program-identity` starts
  from the `Module(...)` term generated from the current `solution.mpy` and,
  using fixed module-loading semantics, proves that it installs
  `evenOddClosure`.
- **Dependents:** the loop connection theorem, entry theorem, and validation
  probes.
- **Validation:** identity proof `#Top`; the concrete harness function AST is
  checked equal to the `solution.py` function AST.

### Decimal summaries

**Extensions:** `evenPos`, `oddPos`, `decEven`, and `decOdd`; their zero,
negative-magnitude, and sign-split equations; the duplicate guarded zero
simplifiers; and the guarded matching-logic recurrence equalities in
`verification.k`.

- **Class:** definitional summaries and derived mathematical lemmas.
- **Semantic role:** reason about returned integer values only; they do not
  rewrite any Python term or operational cell.
- **Domain:** `evenPos`/`oddPos` have base value 0 at zero, magnitude
  totalization for negative arguments, and recurrence lemmas guarded by
  `N >Int 0`. `decEven`/`decOdd` use the mutually disjoint and exhaustive
  guards `N == 0`, `N > 0`, and `N < 0`.
- **Matched context:** the recurrence lemmas match only equality proof
  obligations of the exact forms
  `E + evenPos(N) = E + 1 - p + evenPos(q)` and
  `O + oddPos(N) = O + p + oddPos(q)`, in both orientations. They match no K
  computation, continuation, binding, or state cell.
- **State footprint:** none.
- **Value influence:** both tuple components and their postconditions.
- **Value justification:** base equations plus the decimal quotient/parity
  recurrence. For `N > 0`, `0 <= q < N`, so the recurrence descends uniquely
  to zero. The two orientations agree identically; zero rules overlap only
  with the same right-hand side.
- **Dependents:** `LOOP-PROOF.loop-tail`, the bridge result, and
  `SPEC.even-odd-count`.
- **Control validation:** not applicable; these extensions do not replace
  execution.
- **Value validation:** the bridge-free loop theorem connects fixed execution
  universally to these exact values. Concrete K tests cover distinct results,
  the false-postcondition probe rejects `decEven(N) + 1`, and the independent
  differential oracle reports zero mismatches over 20,005 inputs.

The additional matching-logic lemmas relating
`evenPos(absInt(N))/oddPos(absInt(N))` to `decEven(N)/decOdd(N)` are derived
sign-normalization facts. Their guards split zero from strictly positive
magnitude, and their two equality orientations have identical meaning.

### Loop connection theorem

**Extension:** `LOOP-PROOF.loop-tail`.

- **Class:** derived auxiliary reachability theorem.
- **Semantic role:** executes the fixed `#while` semantics, its exact body,
  the remaining `Return(...) .Stmts`, `#endcall`, and frame pop.
- **Domain:** `N >=Int 0`, arbitrary integer counters `E` and `O`, arbitrary
  preserved builtins scope `B`, arbitrary preserved module value `C`, and
  arbitrary caller continuation `CONT`.
- **Matched context:** exact loop syntax; exact return statement-list suffix;
  exact environment 1; exact local bindings `num/even/odd`; exact parent
  links; exact one-frame stack `frame(CONT, 0, 1)`; exact empty heap,
  `scopeLoc` 2, `heapLoc` 0, `noRet`, `NoExc`, and exit code 0.
- **State footprint:** reads the loop/control state and local bindings; updates
  the counters and `num` during execution; returns the tuple; removes local
  scope 1; restores environment 0 and `scopeLoc` 1; pops the stack frame.
  `B`, `C`, heap, heap location, return state, exception state, exit code, and
  `CONT` are preserved as stated.
- **Value influence:** fixes both returned count components.
- **Value justification:** fixed-semantics execution plus the guarded decimal
  recurrence lemmas.
- **Dependents:** the operational bridge below.
- **Validation:** proved with the bridge-free definition, printing `#Top` and
  exiting 0.

### Exact-context operational bridge

**Extension:** the sole rule in `verification-with-lemma.k`.

- **Class:** operational bridge.
- **Semantic role:** replaces the loop, return, and frame-pop region by the
  tuple characterized by `LOOP-PROOF.loop-tail`.
- **Domain and matched context:** identical to the complete connection-theorem
  domain above. There are no additional frames, wildcards in an affected
  cell, weaker guards, or omitted control/state cells. `B`, `C`, and `CONT`
  are universally quantified in both theorem and bridge.
- **Justification scope and containment:** the bridge-free definition
  `loop-verification-kompiled` does not import
  `verification-with-lemma.k`. The proved theorem and bridge have the same
  K term, continuation, stack, bindings, cells, and `N >=Int 0` guard.
- **State footprint and value influence:** exactly the footprint and returned
  values listed for the connection theorem.
- **Justification:** the independently machine-checked universal connection
  theorem.
- **Dependents:** `SPEC.even-odd-count` and `CONTEXT-SPEC.caller-continuation`.
- **Control validation:** `CONTEXT-SPEC` proves that a caller continuation
  which discards the call result and then evaluates `Int(7)` is preserved.
  The body mutation changes the displaced loop syntax, prevents bridge
  matching, executes fixed semantics, returns `(0, 0)` for input 2, and is
  rejected against `(1, 0)`.
- **Value validation:** fixed-semantics connection theorem, concrete LLVM
  witnesses, differential oracle, and rejected off-by-one result mutation.

No proof-local rule intercepts name lookup, argument evaluation, `abs`,
function entry, initialization, or the zero-return branch.

## Commands and actual outputs

The complete reproducible command sequence is in `prove.sh`. The final run:

```bash
./prove.sh > prove.log 2>&1
```

exited 0. K was:

```text
K version: v7.1.293
Build date: Fri Oct 03 13:32:35 CDT 2025
```

Key commands and actual results:

```bash
python3 py2mpy.py solution.py > solution.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled
```

Actual concrete result: command exit 0; final `<k>` is `.K`, `<exc>` is
`NoExc`, and `<exit-code>` is `0` (`concrete-krun.log`).

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition loop-verification-kompiled
kprove spec.k \
  --definition loop-verification-kompiled \
  --spec-module LOOP-PROOF
kprove identity-spec.k \
  --definition loop-verification-kompiled \
  --spec-module IDENTITY-SPEC
```

Actual results: both `kprove` commands printed `#Top` and exited 0
(`loop-proof.log`, `identity-proof.log`).

```bash
kompile --backend haskell verification-with-lemma.k \
  --main-module VERIFICATION-WITH-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
kprove context-spec.k \
  --definition verification-kompiled \
  --spec-module CONTEXT-SPEC
```

Actual results: both `kprove` commands printed `#Top` and exited 0
(`target-proof.log`, `context-proof.log`).

The supplied semantics emitted compiler warnings about unrelated
non-exhaustive helper cases and unused `str.k` variables. All builds exited 0.

Negative validation commands:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
kprove body-mutation-spec.k \
  --definition verification-kompiled \
  --spec-module BODY-MUTATION-SPEC
```

Actual results: both exited 1 with `WarnStuckClaimState`. The vacuity residual
contains `decEven(N) +Int 1 #Equals evenPos(absInt(N))`. The body mutation
residual contains the fixed-semantics result `(0, 0)` for input 2, which does
not unify with required `(1, 0)` (`vacuity.log`, `body-mutation.log`).

```bash
python3 differential_test.py
```

Actual output:

```text
differential cases: 20005; mismatches: 0
```

## Gate results

### Gate A — PASS

- **A1:** `identity-spec.k` connects the freshly generated `solution.mpy`
  program term to `evenOddClosure`. The function executes under fixed
  semantics outside the one justified loop bridge. A material loop-body
  mutation is not matched by the bridge and fails with a concrete wrong result.
- **A2:** the bridge and connection theorem have identical complete state
  footprints; no output, exception, heap, resource, return, or control cell is
  silently omitted.
- **A3:** lookup, argument evaluation, `abs`, binding, initialization, exact
  return suffix, frame pop, and arbitrary caller continuation are preserved.
  The positive continuation probe prints `#Top`.
- **A4:** summary cases are guarded, exhaustive on their used domains,
  consistent on overlaps, and descending. The bridge has a bridge-free
  universal connection theorem over its complete match domain.
- **A5:** inputs 0, -12, 123, -24680, 13579, and 1002 are realizable concrete
  witnesses. The off-by-one postcondition is rejected with exit 1.

### Gate B — PASS

- **B1:** the formal domain is every mathematical integer, matching the
  prompt's “Given an integer”; there is no hidden magnitude or sign
  precondition.
- **B2:** K `Int` is unbounded, as Python integers are for this task. The
  supplied semantics directly models every used operation: integer `abs`,
  positive `%` and `//`, comparisons, assignments, while, tuple construction,
  function calls, and return. Non-integer Python values are outside the stated
  contract.
- **B3:** the summary is the decimal digit-count recurrence itself, not an
  unrelated execution summary. Division by 10 removes the final decimal digit
  and modulo 2 classifies its parity.
- **B4:** the implementation returns `(1, 0)` for zero and matches both prompt
  examples and all recorded validation cases.

### Gate C — PASS

- Every proof extension, dependency, domain, state footprint, and trust
  assumption is recorded above.
- Every claimed build, proof, mutation, concrete test, and differential result
  has an artifact, exact command in `prove.sh`, persistent log, and actual
  result.
- Formal results, mathematical proof-local definitions, finite evidence, and
  excluded behavior are separated explicitly.

## Trust boundary

- The unmodified files under `reference-semantics/` are trusted to represent
  the relevant Python subset.
- K v7.1.293, its Haskell/LLVM backends, SMT reasoning, and host arithmetic are
  trusted.
- The guarded decimal recurrence and sign-normalization simplification lemmas
  are proof-local mathematical facts. They affect returned values but never
  operational control or state. Their guards, overlaps, descent, and use sites
  were audited; they are also supported by independent finite differential
  evidence.
- The loop bridge is not an unproved trust assumption: its exact behavior is
  established by `LOOP-PROOF.loop-tail` using a definition that cannot import
  the bridge.
- `differential_test.py` uses CPython string conversion and character counting,
  not the proof recurrence, as its independent oracle.

## Empirically supported facts

- LLVM/K concrete execution passed the two prompt examples and four boundary
  cases: zero, all-even digits, all-odd digits, and embedded zeros.
- CPython differential testing checked every integer from -10000 through 10000
  plus four 30- and 50-digit boundary values: 20,005 total inputs and zero
  mismatches.
- Finite evidence supports implementation intent and the mathematical
  summaries; it is not presented as the universal proof. The universal
  program/summary connection is the K reachability theorem.

## Excluded behavior

- Python booleans, floats, strings, user-defined numeric objects, and other
  non-integer inputs are outside the prompt and formal domain.
- CPython resource limits, timing, concurrency, I/O, and implementation details
  outside the supplied reference semantics are not modeled.
- The proof establishes partial correctness only. It does not formally prove
  termination, although concrete execution terminates and the loop measure
  `num` decreases by decimal division for positive values.
