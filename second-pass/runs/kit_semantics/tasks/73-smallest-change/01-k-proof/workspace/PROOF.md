VALIDATED

# Proof report

## What is proved

For every arbitrary finite MPY list `list(VS)` whose elements are MPY
integers (`allInts(VS)`), loading `solution.mpy` and calling
`smallest_change(list(VS))` reaches

```k
mismatchCount(VS, 0, halfLen(VS))
```

with normal return state.  `mismatchCount` examines every disjoint mirrored
pair with left index `i` in `0 <= i < len(VS) // 2` and contributes one
exactly when the two values differ.

This result is the minimum number of permitted changes.  Every unequal
mirrored pair requires at least one of its two positions to change, and the
pairs are disjoint, so any palindrome requires at least
`mismatchCount(VS, 0, halfLen(VS))` changes.  Conversely, changing one member
of every unequal pair to the value of the other member constructs a palindrome
using exactly that many changes.  Thus the lower bound is attainable.

The input is symbolic and unbounded in length and integer magnitude.  This is
not a proof for finitely many sizes or values.

## Formal claims

`spec.k` contains both:

- `loop-invariant`, a symbolic claim from an arbitrary loop head with
  integer accumulator `C`, arbitrary integer index `I >= 0`, and arbitrary
  finite integer sequence `VS`;
- `smallest-change`, the required whole-program claim, beginning with
  `#loadAll(Module(smallestDef))` followed by the source-level call and ending
  in the mismatch count.

The whole-program claim includes the exact MPY environment, scopes, call
stack, heap, return, exception, and exit-code cells.  It proves normal
execution and the result for the full contract domain.

## Proof-extension inventory

The proof uses the following local additions to the supplied, unmodified MPY
semantics.

| Extension | Classification | Domain and role | State/value effect | Justification and validation |
| --- | --- | --- | --- | --- |
| `smallestLoopBody`, `smallestBody`, `smallestDef` | Definitional syntax macros | Exact constructor AST emitted in `solution.mpy` | None after macro expansion | Compared directly with `solution.mpy`; the target starts by loading this exact definition. |
| `fixedBuiltins` | Definitional syntax macro | Constructor-only spelling of the supplied `builtinsScope` | None; it denotes the same fixed scope map | Entry-for-entry expansion of `MPY-CORE`'s `builtinsScope`; needed because a function symbol cannot occur on an ordinary rule left-hand side. |
| `allInts` | Total structural predicate | Exactly finite `ValSeq` values containing only MPY `Int` values | No execution effect | Base and recursive constructor equations are exhaustive and disjoint. |
| `halfLen` | Total definitional summary | Every finite `ValSeq`; exact MPY value of `len(arr) // 2` | No execution effect | It expands the supplied MPY integer floor-division equation for nonnegative sequence length and divisor 2. |
| comparison `#Ceil` lemma | Derived definedness lemma | `allInts(VS)` and `0 <= I < halfLen(VS)` | Establishes only that the supplied `applyCmp("!=", ...)` is defined; it does not choose its Boolean value | Bounds imply both indices lie in `0 .. len(VS)-1`; structural induction through `allInts` makes both selected values integers. |
| branch/AugAssign rule | Operational bridge | Only `#branch(B, changes += 1, .Stmts)` in local scope 1; arbitrary remaining K continuation and arbitrary other scope map | Removes that branch and adds `1` iff the already-computed Boolean `B` is true; preserves all other named state | `branch-connection-spec.k` proves both Boolean paths and both exact counter updates under the fixed MPY semantics in a definition that does not contain the bridge. |
| `pairDiff` and `mismatchCount` | Partial mathematical summaries | Mirrored integer-list positions used under `allInts` and valid loop bounds | No direct machine-state change; retains the supplied comparison result | Recursive guards `I >= STOP` and `I < STOP` are disjoint and exhaustive for integers.  In the recursive case `I` increases by one toward fixed `STOP`.  Neither partial function is declared `total`. |
| integer addition reassociation | Derived algebraic lemma | MPY integers | Reassociates only, preserving value | Associativity of K's mathematical `Int` addition; used to align accumulator and recursive summary shapes. |
| exact initial-loop rule in `verification.k` | Operational bridge | The submitted loop body at `changes = 0`, `i = 0`, with the exact return and `#endcall` continuation and complete call configuration | Replaces the complete call remainder with the mismatch summary and performs the exact normal-return state transition | `loop-connection-spec.k` proves the stronger theorem for arbitrary `C` and `I >= 0` in `LOOP-CONNECTION`, which imports the branch bridge but does not contain this loop bridge.  The body mutation probe confirms the rule cannot match a different body. |

No proof rule states that an unknown comparison is true or false, and no rule
introduces an unconstrained return value.  The comparison Boolean comes from
the supplied MPY operator semantics and is threaded into the count.

## Reproduction and observed results

All exact commands, definitions, checks, and expected-failure handling are in
`prove.sh`.  The complete run command was:

```sh
./prove.sh
```

It exited `0`.  Its decisive output was:

```text
LLVM_KOMPILE_EXIT=0
KRUN_SMOKE_EXIT=0
#Top
#Top
#Top
VACUITY_EXPECTED_FAILURE_EXIT=1
BODY_MUTATION_EXPECTED_FAILURE_EXIT=1
cases=10347 mismatches=0
```

The three `#Top` lines respectively come from:

```sh
kprove branch-connection-spec.k \
  --definition branch-connection-kompiled \
  --spec-module BRANCH-CONNECTION-SPEC

kprove loop-connection-spec.k \
  --definition loop-connection-kompiled \
  --spec-module LOOP-CONNECTION-SPEC

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Each positive `kprove` command exited `0`.  The full logs are
`branch-connection-proof.log`, `loop-connection-proof.log`, and
`target-proof.log`.  Compiler warnings are limited to unused symbolic
variables, including pre-existing warnings in the supplied string semantics.

The LLVM smoke run uses the required compilation form:

```sh
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
```

It terminated with `.K` and `<exit-code> 0 </exit-code>` after checking all
three prompt examples plus empty, singleton, and unequal-pair cases.

## Gate A — extension soundness: PASS

**A1, body connection.**  The submitted AST is represented exactly by syntax
macros.  The branch bridge is proved in `branch-connection-spec.k` without
that bridge present.  The stronger general loop transition is proved in
`loop-connection-spec.k` without the loop bridge present.  A material mutation
that advances `i` by 2 instead of 1 fails with `WarnStuckClaimState`, leaving
the incompatible `I +Int 2` recursive state visible.

**A2, explicit footprint.**  The branch bridge exposes the K continuation,
active environment, full local binding fragment, and arbitrary residual scope
map.  The loop bridge and its connection theorem spell out every MPY
configuration cell and the exact scope deletion, environment restoration, and
stack pop at return.

**A3, no oracle behavior.**  Bindings, body syntax, and continuation are exact.
The only comparison lemma proves definedness, not a result.  Both branch
outcomes are separately connected to fixed semantics.  The general loop
connection theorem checks the summary against actual MPY execution.

**A4, summary domains.**  `allInts` and `halfLen` are genuinely total.
`pairDiff` and `mismatchCount` are deliberately not marked total.  Their
recursive cases are guarded, disjoint, exhaustive on the theorem's integer
domain, and decreasing in remaining distance to `STOP`.

**A5, non-vacuity.**  `spec-vacuity.k` changes the realizable result for input
`[1, 2]` from `1` to `0`.  `kprove` exits `1` and reports a stuck final
configuration whose K cell contains `1 ~> .K`; therefore the precondition is
realizable and the postcondition is not automatically accepted.

## Gate B — theorem adequacy: PASS

**B1, domain coverage.**  `VS:ValSeq` is arbitrary and finite, constrained
only by the prompt's integer-element requirement.  There is no bound on list
length or integer value, and empty and odd/even lengths are covered.

**B2, model boundary.**  The theorem covers MPY `Int` elements and ordinary
MPY lists, which is the supplied semantics' representation of the prompt's
“array of integers.”  It makes no hidden sortedness, distinctness, sign, or
size assumption.

**B3, intended property.**  The postcondition counts unequal mirrored pairs,
and the lower-bound/construction argument above proves this count is precisely
the minimum number of arbitrary single-element changes needed to obtain a
palindrome.

**B4, implementation correspondence.**  The loaded AST initializes the count
and index to zero, visits exactly the left half, compares each element with its
unique mirror, increments once for each mismatch, advances by one, and returns
the count.  This is the submitted implementation, not a surrogate function.

## Gate C — validation and trust audit: PASS

The proof was replayed from generated source through LLVM concrete execution
and Haskell symbolic proof.  The operational bridges have independent
bridge-free connection proofs.  Two negative probes fail as expected: a false
ground result tests non-vacuity, and a material body mutation tests body
sensitivity.  An independent brute-force palindrome oracle checks 10,347
concrete cases and reports zero mismatches.

The trust boundary consists of:

- the supplied `reference-semantics/` MPY definition;
- the installed K parser, compiler, LLVM backend, Haskell backend, and
  reachability prover;
- the local definitional and derived equations inventoried above;
- the mathematical argument that unequal disjoint mirrored pairs give both a
  lower bound and a matching construction.

The supplied semantics is not modified.  The comparison-definedness and
addition-associativity lemmas are transparent proof-local equations with their
domains shown above, rather than opaque external procedures.  The operational
summaries are not trusted on their own: their fixed-semantics connection
claims are part of the positive proof run.

## Empirical support and excluded behavior

`differential_test.py` exhaustively searches all arrays of lengths 0 through 8
over `(-2, 0, 3)`, checks 500 deterministic random arrays of lengths 0 through
12, and repeats six examples/boundaries.  Its oracle enumerates palindromic
targets and minimizes Hamming distance; it does not reuse the mismatch-count
formula.  These tests support the formal result but are not its domain basis.

Excluded behavior is limited to values outside the stated integer-list
contract (non-list arguments, mixed/non-integer elements, or ill-formed MPY
terms).  Resource exhaustion and behavior outside the supplied partial Python
semantics are also outside the theorem.  The function does not mutate its
input.  Within the stated domain, no fixed-size, finite-enumeration, or
exceptional-input exclusion remains.
