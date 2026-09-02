VALIDATED

# What is proven

Under the supplied `MPY` reference semantics, for every finite semantic list
`FULL` satisfying `allInts(FULL)`, loading the exact translated
`pairs_sum_to_zero` definition and calling it returns a Boolean equal to
`anyInverse(FULL, FULL)`.

`anyInverse(FULL, FULL)` is true exactly when some integer occurrence has a
distinct-position additive inverse occurrence. For a nonzero `x`, the inverse
must occur at least once. For zero, zero must occur at least twice. Thus the
result is true exactly when two distinct list positions contain integers whose
sum is zero.

This is a partial-correctness reachability proof. It establishes the result
whenever the call terminates; termination is not a separate liveness theorem.

# Formal claim

`spec.k` contains:

- `SPEC.loop-invariant`: starting at the exact source-loop head with remaining
  sequence `REM`, full input `FULL`, and current Boolean `FOUND`, fixed
  execution finishes with
  `FOUND orBool anyInverse(REM, FULL)`. The final, unobserved `x` binding is
  existentially framed as a `Val`.
- `SPEC.pairs-sum-to-zero`: starts at `#loadAll(Module(...))` containing the
  exact `solution.mpy` function body followed by a wrapper assignment that
  calls the loaded binding. The final `$result` is constrained to
  `anyInverse(FULL, FULL)`.

The precondition `allInts(FULL)` matches the prompt's list-of-integers domain.
The observable final state is the returned Boolean, captured by the wrapper's
`$result`. The wrapper itself only observes the return value.

The loop proof discharges:

1. Base: `REM == .ValSeq`, so `anyInverse(REM, FULL) == false` and the loop
   preserves `FOUND`.
2. Step: the real body computes the zero or nonzero occurrence-count test,
   updates `found` only to `true`, and the circularity applies to the tail.
3. Entry: initialization gives `FOUND == false` and `REM == FULL`, so the loop
   result is `anyInverse(FULL, FULL)`; fixed call/return and assignment rules
   place it in `$result`.

# Proof-extension inventory

## `intProj` and its equations

- Extension: `intProj(Val)` in `projection.k`.
- Class: definitional summary.
- Semantic role: names a total mathematical sort projection; it does not
  replace program execution.
- Domain: all `Val`; it is identity on `Int` and zero when `notBool isInt(V)`.
- Matched context: pure function terms only; no continuation, binding, or cell
  is matched.
- Justification scope: the two guards cover every `Val` and are disjoint.
- Context containment: equations are context-free mathematical equalities.
- State footprint: none.
- Value influence: supplies the integer value used by the two guarded bridges
  and by `anyInverse`.
- Value justification: `intProj(I:Int) => I`; the non-Int equation is explicit
  and unreachable under bridge guards and the target precondition.
- Justification: exhaustive, terminating equations.
- Dependents: `anyInverse`, both bridge rules, and both connection claims.
- Control validation: not control-bearing.
- Value validation: `connection-spec.k` proves both fixed operations through
  `intProj`; opposite ground interpretations are rejected.
- Validation: PASS.

## `hasInverse`

- Extension: `hasInverse(Int, ValSeq)` and its one unconditional equation.
- Class: definitional summary.
- Semantic role: specifies the distinct-partner property; it does not rewrite
  a program term.
- Domain: every integer and `ValSeq`.
- Matched context: pure function term only.
- Justification scope: unconditional and total.
- Context containment: exact; no frames or cells.
- State footprint: none.
- Value influence: contributes directly to the postcondition.
- Value justification: for `x == 0`, `cntOccVS(FULL, 0) > 1`; otherwise,
  `cntOccVS(FULL, -x) > 0`. `cntOccVS` is the fixed reference-semantics
  definition of list count.
- Justification: these are exactly the necessary and sufficient occurrence
  conditions for a distinct inverse position.
- Dependents: `anyInverse`, loop invariant, entry claim.
- Control validation: not control-bearing.
- Value validation: prompt examples, zero edge cases, and the independent
  3,906-case differential run agree.
- Validation: PASS.

## `anyInverse`

- Extension: `anyInverse(ValSeq, ValSeq)` and its empty/cons equations.
- Class: definitional summary.
- Semantic role: folds the mathematical partner predicate over a sequence; it
  does not replace source execution.
- Domain: all `ValSeq`; non-Int elements are explicitly ignored. The theorem
  separately requires `allInts`.
- Matched context: pure function term only.
- Justification scope: `.ValSeq` and `vCons` are exhaustive and recursive calls
  descend structurally.
- Context containment: exact; no operational context.
- State footprint: none.
- Value influence: this is the final result specification.
- Value justification: Boolean disjunction of `hasInverse(intProj(X), FULL)`
  for integer heads and the recursively defined tail property.
- Justification: structural definition of existence over the list.
- Dependents: loop invariant and entry claim.
- Control validation: not control-bearing.
- Value validation: loop base/step close under the equation; concrete and
  differential evidence has zero mismatches.
- Validation: PASS.

## `allInts`

- Extension: `allInts(ValSeq)` and its empty/cons equations.
- Class: definitional summary.
- Semantic role: formalizes the prompt's input type and exposes `isInt` facts.
- Domain: all `ValSeq`.
- Matched context: pure function term only.
- Justification scope: exhaustive, total structural recursion.
- Context containment: exact.
- State footprint: none.
- Value influence: restricts the theorem domain and guards sort recovery.
- Value justification: empty is true; cons is `isInt(head) and allInts(tail)`.
- Justification: definition of an integer-only sequence.
- Dependents: both target claims.
- Control validation: not control-bearing.
- Value validation: direct exhaustive equations.
- Validation: PASS.

## Guarded `applyCmp("==", V, I)` simplification

- Extension: the `[simplification]` rule in `verification.k`.
- Class: operational bridge, because it accelerates a fixed semantic function.
- Semantic role: recovers the fixed integer equality result when symbolic
  iteration leaves an injected integer at super-sort `Val`.
- Domain: `V:Val`, `I:Int`, with `isInt(V)`.
- Matched context: the pure `applyCmp` term in any enclosing term context.
- Justification scope: every injected integer `V` and every integer `I`.
  `connection-spec.k` proves
  `applyCmp("==", I, J) => intProj(I) ==Int J` using a definition that imports
  `MPY` and `INT-PROJECTION` but not `VERIFICATION`.
- Context containment: `isInt(V)` is precisely the injected-`Int` domain of the
  connection theorem. The equality is pure and congruent in enclosing contexts;
  the connection claim frames an arbitrary `<k>` continuation and all cells.
- State footprint: reads/writes/abstracts no cells.
- Value influence: selects the outer zero/nonzero source branch and therefore
  can affect the returned Boolean.
- Value justification: fixed `MPY-INT` equality plus `intProj(I) == I`.
- Justification: bridge-free universal connection claim
  `CONNECTION-SPEC.int-equality`, output `#Top`.
- Dependents: loop invariant and entry claim.
- Control validation: no control is discarded or introduced; the same Boolean
  is returned to the existing context. Ground opposite interpretation
  `2 == 2 => false` is rejected with residual `true`.
- Value validation: fixed and extended values coincide on the complete guard;
  the opposite ground value exits 1.
- Validation: PASS.

## Guarded `applyUn("-", V)` simplification

- Extension: the `[simplification]` rule in `verification.k`.
- Class: operational bridge.
- Semantic role: accelerates fixed integer unary minus under a recovered
  `isInt(V)` fact.
- Domain: `V:Val` with `isInt(V)`.
- Matched context: pure `applyUn("-", V)` in any enclosing term context.
- Justification scope: every injected integer. `connection-spec.k` proves
  `applyUn("-", I) => 0 -Int intProj(I)` without importing the bridge.
- Context containment: the guard exactly selects the connection theorem's
  integer domain; purity plus the arbitrary framed continuation preserves every
  enclosing use.
- State footprint: no cells read, written, or abstracted.
- Value influence: supplies the argument to `list.count`, affecting branches
  and the returned Boolean.
- Value justification: fixed `MPY-INT` unary-minus rule plus projection
  identity.
- Justification: bridge-free universal connection claim
  `CONNECTION-SPEC.int-unary-minus`, output `#Top`.
- Dependents: loop invariant and entry claim.
- Control validation: no control effect. The opposite interpretation
  `-2 => 2` is rejected; the residual is `-2`.
- Value validation: universal connection plus the rejected ground opposite.
- Validation: PASS.

## `SPEC.loop-invariant`

- Extension: the circular reachability claim over the exact translated `For`
  body.
- Class: derived lemma/circularity.
- Semantic role: summarizes repeated fixed-semantics loop execution; it is not
  a rewrite rule in `verification.k` and does not replace the function binding
  or body.
- Domain: `allInts(FULL) andBool allInts(REM)`, exact local scope containing
  `found`, `l`, and `x`.
- Matched context: exact `#loop(list(REM), Name("x"), BODY)` with the remainder
  of `<k>` framed; exact active environment and local scope; all other cells
  are preserved.
- Justification scope: the claim proves the same framed configuration it can
  match, for every `FULL`, `REM`, `FOUND`, and local environment location.
- Context containment: the source body has no return, break, continue,
  exception, output, allocation, or cleanup; it preserves the framed
  continuation. The claim explicitly tracks both modified bindings (`found`
  and existential final `x`) and fixes `l`.
- State footprint: reads `l`, `found`, and `x`; writes `found` and `x`;
  preserves scopes outside the active local frame and every other configuration
  cell.
- Value influence: determines the returned Boolean via `found`.
- Value justification: fixed execution of both branches and `list.count`,
  followed by the total `anyInverse` recurrence.
- Justification: machine-checked base and inductive cases in the successful
  target `kprove`.
- Dependents: `SPEC.pairs-sum-to-zero`.
- Control validation: the exact body is executed. Mutating its nonzero threshold
  from `> 0` to `> 1` is rejected on `[1, -1]`, leaving `found |-> false`.
- Value validation: false-result and body-mutation probes both exit 1.
- Validation: PASS.

The two claims in `connection-spec.k` are bridge-free derived lemmas and are
supporting evidence, not axioms imported into the target definition.

# Exact commands and actual outputs

The complete reproducible command is:

```bash
./prove.sh
```

Actual exit: `0`. Complete combined output is in `prove.out`.

The positive connection proof command was:

```bash
kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-SPEC
```

Actual output: two `WarnTrivialClaim` notices (the fixed equations normalize
both sides) and `#Top`. Exit: `0`.

The positive target proof command was:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual output: `#Top` plus non-fatal supplied-semantics unused-variable
warnings. Exit: `0`. This command proves every claim in `spec.k`.

The concrete command was:

```bash
krun concrete-tests.mpy --definition runtime-kompiled
```

Actual final observations: `<k>.K</k>`, `<exc>NoExc</exc>`, and
`<exit-code>0</exit-code>`. Exit: `0`. The nine cases include every prompt
example, `[]`, `[0]`, `[0, 0]`, and `[-4, 4]`.

The validation probes were:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual: `WarnStuckClaimState`, residual `found |-> false` against the mutated
`true` result, exit `1`.

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual: `WarnStuckClaimState`, residual `found |-> false` on `[1, -1]`, exit
`1`.

```bash
kprove connection-mutation-spec.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-MUTATION-SPEC \
  --claims CONNECTION-MUTATION-SPEC.bad-int-equality
```

Actual: `WarnStuckClaimState`, residual `true`, exit `1`.

```bash
kprove connection-mutation-spec.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-MUTATION-SPEC \
  --claims CONNECTION-MUTATION-SPEC.bad-int-unary-minus
```

Actual: `WarnStuckClaimState`, residual `-2`, exit `1`.

```bash
python3 differential_test.py
```

Actual:

```text
DIFFERENTIAL_CASES=3906
MISMATCHES=0
```

Exit: `0`.

# Gate results

## Gate A — PASS

- A1: `spec.k` loads and calls the exact `solution.mpy` body. Program-defined
  code, lookup, method binding, calls, loop execution, and return all run under
  fixed semantics. The body mutation is rejected.
- A2: the only operational bridges are pure value equations and touch no state.
  The loop claim explicitly accounts for every modified local binding and
  preserves other cells.
- A3: fixed lookup selects the loaded closure and fixed attribute/call rules
  select `list.count`. Arguments and branches execute in source order. Both
  bridges have bridge-free universal connection claims over their full guarded
  value domains and preserve context/control.
- A4: every proof-local function has disjoint, exhaustive, terminating
  equations. No false off-domain equation or result-bearing oracle is present.
- A5: the empty-list precondition is realizable. The deliberately false result
  is rejected, as are the source-body and both opposite-value mutations.

## Gate B — PASS

- Input domain: finite lists of mathematical integers, exactly the prompt's
  stated domain. Non-integers and K `Bool` values are excluded.
- Model adequacy: K `Int` is unbounded, matching Python integer arithmetic for
  the used operations. List iteration, integer equality/negation, `count`,
  function binding, and return are modeled by the supplied semantics.
- Property adequacy: `hasInverse` encodes distinct positions by requiring two
  zeros for `x == 0` and one inverse occurrence for nonzero `x`;
  `anyInverse(FULL, FULL)` structurally expresses existence of such an
  occurrence. This is the requested human-facing property, not merely an
  execution trace summary.
- Implementation alignment: concrete examples and exhaustive small-domain
  differential tests agree with the contract.

## Gate C — PASS

- Every proof extension and dependency is inventoried above.
- Positive proof, concrete execution, body/postcondition mutations, bridge
  mutations, and differential evidence have existing artifacts, exact commands,
  outputs, and exit statuses.
- Formal results, finite evidence, trust assumptions, and excluded behavior are
  separated below.

# Trust boundary

- Trusted input: the supplied read-only `reference-semantics/` definition as
  the model of the supported Python subset.
- Trusted machinery: K 7.1.293, its Haskell reachability backend, and LLVM
  concrete backend.
- No opaque float, sorting, digest, external, or result-bearing trusted
  primitive is used by this program or proof.
- The operational bridges are not trusted assumptions: both are connected to
  fixed execution by bridge-free `#Top` claims.
- The theorem is partial correctness; termination is outside its formal
  conclusion. For finite lists the implementation plainly performs one finite
  outer traversal and finite `count` traversals, but that is not a kprove
  liveness result.

# Empirically supported facts

- LLVM execution passed nine concrete assertions under the supplied semantics.
- CPython execution matched an independently written double-index oracle for
  all 3,906 lists of lengths 0 through 5 over values `-2..2`.
- These finite checks support implementation/intent and concrete-semantics
  alignment. They are not used as substitutes for either universal K proof.

# Excluded behavior

- Inputs containing non-integers, including Python/K booleans.
- Behavior outside constructs modeled by the supplied reference semantics.
- Resource bounds and termination as formal liveness properties.
- Mutation probes are deliberately false artifacts and are not part of the
  positive theorem.
