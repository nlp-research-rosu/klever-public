VALIDATED

## What is proven

Under the supplied reference semantics, calling the exact translated
`has_close_elements(numbers, threshold)` program on any finite native
`ValSeq` whose elements are all `Float` values returns true exactly when some
pair of distinct positions is closer than `threshold`.

The proof is symbolic and unbounded in list length. Empty lists, singleton
lists, duplicates, negative thresholds, and arbitrary `Float` thresholds are
in the formal domain. This is a partial-correctness reachability proof.

## Formal claim

The entry claim `SPEC.has-close-elements` starts from the initial reference
configuration, loads the exact `Module(...)` emitted in `solution.mpy`, resolves
and calls `has_close_elements`, executes its body, and returns

```k
outerAcc(false, VS, T, 0, VS)
```

under:

```k
requires allFloats(VS)
```

`outerAcc` visits every outer position `i`; `rowAcc` visits every inner
position `j`; only `i < j` contributes

```k
pairNear(A, B, T)
  = floatLt(absF(subF(A, B)), T)
```

to the Boolean disjunction. Thus the recurrence is exactly the existential
property “there are two distinct list elements whose absolute difference is
strictly less than the threshold.”

The two auxiliary reachability claims are:

- `SPEC.inner-loop`: summarizes one complete inner iterator scan.
- `SPEC.outer-loop`: summarizes the remaining outer iterator scan and uses the
  inner-loop claim.

Both claims match the actual `#loop` form reached by the fixed semantics.

## Proof-extension inventory

### `allFloats`

- Class: definitional summary.
- Role and domain: recognizes exactly the native finite `ValSeq` values whose
  heads satisfy K's generated `isFloat` sort predicate.
- Matched context: pure function applications only; no configuration cells.
- State footprint and value influence: reads no cells; constrains the typed
  input domain and enables Float dispatch.
- Coverage/overlap: `.ValSeq` and `vCons(V,R)` are exhaustive and disjoint.
- Dependents: all three target claims.
- Justification and validation: structural definition over `ValSeq`; concrete
  empty, singleton, and multi-element witnesses execute in `smoke.mpy`.

### `pairNear`

- Class: definitional summary.
- Role and domain: names the exact fixed-semantics atom
  `floatLt(absF(subF(A,B)),T)` for all Float arguments.
- Matched context: pure function applications; no continuation or cells.
- State footprint and value influence: no state; affects `found` and the final
  result.
- Coverage/overlap: one unguarded equation covers the complete declared domain.
- Dependents: `rowAcc`, the target claim, and both negative probes.
- Justification and validation: a direct abbreviation, with no skipped program
  execution.

### `asFloat`

- Class: definitional summary.
- Role and domain: total sort projection over `Val`; it is identity on Float
  values and is explicitly totalized to `0.0` on non-Float values.
- Matched context: pure function applications; no continuation or cells.
- State footprint and value influence: no state; on the target domain it
  preserves the exact yielded Float value used by `pairNear`.
- Coverage/overlap: `F:Float` and `V:Val` guarded by `notBool isFloat(V)` are
  exhaustive and disjoint.
- Dependents: the guarded subtraction bridge and both accumulator summaries.
- Justification and validation: generated sort-predicate elimination; the
  non-Float totalization is outside the target's `allFloats` domain.

### Guarded `applyBin("-", A:Val, B:Val)` simplification

- Class: operational bridge, because it accelerates fixed operator dispatch.
- Complete domain: `isFloat(A) andBool isFloat(B)`.
- Complete matched context: a pure `applyBin` function occurrence after both
  Python operands have already been evaluated; simplification may occur under
  any pure enclosing term. It performs no lookup, evaluation ordering, call,
  return, exception, or continuation action.
- Justification scope: every pair of actual Float values. The generated
  `isFloat` predicate makes the bridge match domain exactly that scope.
- Context containment: the fixed operator is pure, and equational congruence
  lifts the bridge-free value theorem through any pure enclosing term.
- State footprint: reads, writes, preserves, and abstracts no cells.
- Value influence: supplies the subtraction value used by `absF`, `floatLt`,
  the branch, `found`, and the postcondition.
- Value justification: `asFloat(F) = F` plus the independently compiled,
  bridge-free `CONNECTION-SPEC.float-subtraction` theorem. That definition
  imports `MPY` only and proves
  `applyBin("-", A:Float, B:Float) => subF(A,B)` universally.
- Dependents: the inner loop and therefore the outer and entry claims.
- Control/value validation: `smoke.mpy` runs without the bridge under the LLVM
  reference definition; the connection proof prints `#Top`; true and false
  ground outcomes occur in the smoke suite; both negative probes are rejected.

### `rowAcc`

- Class: definitional summary.
- Role and domain: exact Boolean fold over every remaining inner-list element,
  carrying `found`, `i`, and `j`.
- Matched context: pure summary terms only.
- State footprint and value influence: no cells; describes the final `found`
  value of `SPEC.inner-loop`.
- Coverage/overlap/descent: empty and cons equations are disjoint and
  exhaustive; the cons equation structurally descends to the tail.
- Dependents: inner-loop, outer-loop, and entry claims.
- Justification and validation: its one-step equation is the same update made
  by the exact inner body. The inner-loop claim proves this connection by
  fixed-semantics execution and circularity.

### `outerAcc`

- Class: definitional summary.
- Role and domain: exact Boolean fold over all remaining outer-list elements.
- Matched context: pure summary terms only.
- State footprint and value influence: no cells; is the final program result.
- Coverage/overlap/descent: empty and cons equations are disjoint and
  exhaustive; the cons equation structurally descends to the tail.
- Dependents: outer-loop and entry claims.
- Justification and validation: its one-step equation invokes the proved
  `rowAcc` result and matches the exact outer body. The outer-loop circularity
  and entry claim execute all program-defined code.

### Loop claims

- Class: derived auxiliary reachability claims.
- Complete matched context: the exact inner and outer `#loop` terms, local
  bindings, environment `1`, module and builtins frames, parent links, and
  empty heap shown in `spec.k`. Only the normal trailing continuation is
  framed. The loop bodies contain no abrupt return, break, continue, exception,
  allocation, or output effect.
- State footprint: read `numbers`, `threshold`, indices, and current elements;
  write only `found`, `i`, `j`, `number1`, and `number2`; preserve all other
  cells.
- Justification: fixed-semantics base and inductive execution. The inner claim
  establishes one inner scan; the outer claim uses it for each outer element.
- Dependents: the outer claim depends on the inner claim; the entry claim
  depends on both.
- Validation: both prove together as part of the target `#Top` run. The
  close-branch body mutation does not match them and is rejected after direct
  fixed-size execution.

## Exact commands and actual outputs

All commands are recorded in `prove.sh`. A complete replay ended with exit 0.

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 check_artifacts.py
```

Actual output:

```text
artifact identity checks: passed
```

The check also confirms the prompt parameters, the smoke implementation, and
the translated `Module(...)` embedded in the entry claim. The only normalized
surface difference is that the K claim parser requires `.Stmts` where the
`.mpy` program parser accepts an empty list slot.

```bash
python3 test_solution.py
```

Actual output and exit:

```text
checked: 4686
mismatches: 0
Exit: 0
```

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
```

Actual result and exit:

```text
<k> .K </k>
<env> 0 </env>
<stack> .List </stack>
<ret> noRet </ret>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
Exit: 0
```

The LLVM compile emitted supplied-semantics exhaustiveness warnings but no
error.

```bash
kompile --backend haskell connection-verification.k \
  --main-module CONNECTION-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled
kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-SPEC
```

Actual output and exit:

```text
WarnTrivialClaim: Claim proven without rewriting
#Top
Exit: 0
```

The trivial-claim warning occurs because fixed function simplification already
normalizes the left side to the right side; the definition does not import the
proposed bridge.

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual output and exit:

```text
#Top
Exit: 0
```

This single positive target command proves all three required claims.

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual output and exit:

```text
WarnStuckClaimState
residual local state: "found" |-> true
Exit: 1
EXPECTED FAILURE: false-result mutation was rejected
```

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual output and exit:

```text
WarnStuckClaimState
residual local state: "found" |-> false
Exit: 1
EXPECTED FAILURE: changed-body mutation was rejected
```

The complete captured residuals from the validation run are in `vacuity.out`
and `body-mutation.out`.

## Gate results

### Gate A — PASS

- A1: `check_artifacts.py` confirms exact program identity. All
  program-defined statements, calls, loops, binding, and returns execute under
  fixed semantics. Mutating the close branch from `found = True` to
  `found = False` makes the connection fail.
- A2: the only operational bridge is pure and has no state footprint. The loop
  claims enumerate every local binding they read or write and preserve the
  remaining configuration.
- A3: module loading, name lookup, argument evaluation, builtin lookup, loop
  control, and function return execute normally. The bridge applies only after
  both operands have values and has no control effect. Its context is contained
  in the bridge-free fixed Float theorem.
- A4: every proof-local function has exhaustive, disjoint constructor or
  guarded equations and structural descent where recursive. The bridge guard
  is exactly the Float sort domain, and its RHS agrees with fixed dispatch.
- A5: `[1.0, 1.0]` with threshold `0.1` is a concrete satisfiable witness. The
  false-result mutation exits 1 with `found = true` in the residual.

### Gate B — PASS

- Input domain: every arbitrary finite `List[float]` and every Float threshold;
  there is no length bound or finite unrolling in the target theorem.
- Language model: list iteration, integer positions, strict comparison,
  function calls, and return use the supplied Python semantics. Float
  subtraction, absolute value, and comparison use its named Float primitives.
- Summary adequacy: the `rowAcc`/`outerAcc` recurrences formally enumerate
  exactly all `i < j` pairs and OR exactly `abs(a-b) < threshold`.
- Implementation alignment: the implementation has the requested signature
  and both prompt examples pass in LLVM smoke execution and the independent
  Python oracle run.

### Gate C — PASS

- The trust ledger below names every value-affecting unproved primitive.
- Every empirical and mutation statement above has an existing artifact,
  exact command, oracle or expected residual, actual result, and exit status.
- Formal conclusions, conditional trust, finite evidence, and excluded
  behavior are separated.

## Trust boundary

The supplied read-only semantics and K prover/kernel are trusted.

The reference symbols `subF`, `absF`, and `floatLt` are intentionally opaque
under Haskell symbolic proof. Their contracts are:

```k
subF(F1,F2)  = F1 -Float F2
absF(F)      = absFloat(F)
floatLt(F,T) = F <Float T
```

Their concrete equations are `[concrete]` in
`reference-semantics/semantics/float.k`. They affect the proximity atom,
branch, `found`, and final result. All target claims depend on them
conditionally. Evidence consists of the bridge-free dispatch theorem, LLVM
smoke execution, the two opposite Boolean outcomes in concrete tests, and the
independent differential run. Finite evidence supports but does not replace
these named primitive contracts.

K's generated `isFloat` predicate and sort injection/projection discipline are
also trusted as part of the K type system. The guarded bridge depends on them.

## Empirically supported facts

- `smoke.py` contains six LLVM assertions: empty, singleton, both prompt
  examples, equality at a zero threshold, and a duplicate below a positive
  threshold. All reached `.K` with `NoExc` and exit code 0.
- `test_solution.py` uses Python's independent `itertools.combinations` oracle.
  It checks every list of lengths 0 through 4 over
  `[-2.0, -0.5, 0.0, 0.5, 2.0]` and thresholds
  `[-1.0, 0.0, 0.25, 0.5, 1.0, 3.0]`: 4,686 cases, zero mismatches.
- These finite tests are evidence about those inputs, not a replacement for
  the symbolic unbounded proof.

## Excluded behavior

- Inputs outside the annotated `List[float]` and `float` contract are excluded,
  including non-list objects and lists containing non-Float values.
- The report does not prove properties of CPython behavior beyond the supplied
  reference semantics' Float primitive contracts.
- Reachability establishes partial correctness; resource bounds and a separate
  liveness/termination theorem are not claimed.
- The two fixed-size mutation claims are validation probes only. They are not
  used as the required target theorem.
