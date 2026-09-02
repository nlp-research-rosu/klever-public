VALIDATED

## What is proven

Under the supplied MPY semantics, `longest` is partially correct for every
finite `List[str]` represented as `list(ValSeq)`:

- the empty list returns `noneV`;
- a nonempty list returns an element of maximum string length; and
- if several elements have that maximum length, it returns the first one.

The theorem executes the exact translated function body, including module
loading, lookup of the `longest` binding, argument binding, the empty branch,
subscript initialization, every loop-body statement, builtin `len` lookup,
return, and frame pop.

K reachability proves partial correctness. Termination is not a reachability
conclusion, although the source loop consumes one constructor from a finite
`ValSeq` per iteration.

## Formal claims

`spec.k` contains:

- `SPEC.loop-invariant`: for an arbitrary symbolic remaining `ValSeq`, the real
  source loop changes `result = ACC` to `scanLongest(REST, ACC)`. Its
  precondition requires every remaining value and the accumulator to be
  strings.
- `SPEC.empty-input`: the exact program returns `noneV` on `.ValSeq`.
- `SPEC.nonempty-input`: for symbolic `FIRST:Val` and `REST:ValSeq`, with
  `isStringValue(FIRST)` and `allStrings(REST)`, the exact program returns
  `longestValue(vCons(FIRST, REST))`.

These entry claims partition all finite lists of strings; no list-size bound is
present.

`longestValue` seeds `scanLongest` with the first element. `scanLongest`
updates only when the next length is strictly greater. Induction on the
processed prefix gives:

1. the accumulator is a member of the processed nonempty prefix;
2. its length is at least every processed element's length; and
3. equality never replaces it, so it is the earliest processed maximizer.

The first scan step compares the first element with itself and keeps it.
Consequently the final fold is exactly the HumanEval “first longest” value.

`connection-spec.k`, compiled with `VERIFICATION-BASE` (which does not import
the dynamic dispatch twin), proves the universal canonical-string connections
for `seqLenString` and `projectString`.

## Proof-extension inventory

### `isStringValue` and `allStrings`

- **Class:** definitional summaries.
- **Semantic role:** state the input domain; they do not replace execution.
- **Domain:** all `Val` and all finite `ValSeq` terms. The `Str`/`owise` cases
  are disjoint and complete; the sequence equations cover empty and cons.
- **Matched context / justification scope:** pure function terms in any
  context; their equations are structural definitions over the fixed value
  constructors.
- **State footprint:** none.
- **Value influence:** guard the projection, loop invariant, and nonempty entry
  claim.
- **Value justification:** constructor case analysis.
- **Dependents:** the dispatch twin and all nonempty symbolic claims.
- **Control/value validation:** concrete, differential, and negative probes
  listed below.

### `projectString` and its ceil/orientation/collapse equations

- **Class:** definitional summary and derived sort-refinement lemmas.
- **Semantic role:** recover the fixed `Str` subsort already guaranteed by
  `isStringValue`; no source term or control step is skipped.
- **Domain:** only values satisfying `isStringValue`; collapse and idempotence
  cover already-static and repeated projections.
- **Matched context:** the projection/cast term only, with no continuation or
  cell pattern.
- **Justification scope / context containment:** the complete true domain of
  `isStringValue` is the fixed `Str` subsort. Every accepted term is therefore
  within the cast's domain, independently of its surrounding context.
- **State footprint:** none.
- **Value influence:** its projected value is consumed only by the
  string-length twin and thus can influence the loop branch and return value.
- **Value justification:** `CONNECTION-SPEC.string-projection-connection`,
  compiled without the dispatch twin; constructor collapse is exact.
- **Dependents:** `seqLenString`, `scanLongest`, and the loop/entry claims.
- **Control/value validation:** the universal connection prints `#Top`;
  ground one- and two-code-point witnesses compute distinct values; the
  opposite ground interpretation is rejected.

### `seqLenString`

- **Class:** definitional total twin of the fixed static-sort operation.
- **Semantic role:** names string length after guarded static projection; it
  does not rewrite source calls.
- **Domain:** `Str`. Its canonical equation
  `seqLenString(str(CS)) => isLen(CS)` is exactly the fixed equation
  `seqLen(str(CS)) => isLen(CS)`.
- **Matched context:** a pure function term in any context.
- **Justification scope / context containment:** all canonical `Str` values;
  projection reduces guarded dynamic values to this same subsort.
- **State footprint:** none.
- **Value influence:** loop comparison and the contract fold.
- **Value justification:** the bridge-free universal claim
  `CONNECTION-SPEC.string-length-connection`.
- **Dependents:** the `seqLen` dispatch twin, `scanLongest`, and target claims.
- **Validation:** universal connection `#Top`; concrete lengths differ; the
  false one-character-length-zero claim gets stuck at `1`.

### Guarded `seqLen(V) => seqLenString(projectString(V))`

- **Class:** operational bridge (a guarded dynamic-sort dispatch twin).
- **Semantic role:** accelerates the fixed pure `seqLen` operation only where
  symbolic `V:Val` is already proved to be a string.
- **Domain:** exactly `isStringValue(V)`.
- **Matched context:** a pure `seqLen(V)` term in any continuation. It matches
  no stack, environment, heap, exception, or control cell.
- **Justification scope / context containment:** the connection definition
  imports `VERIFICATION-BASE`, not this rule. It proves the fixed and total-twin
  constructor equations agree for arbitrary `CS:IntSeq`; guarded projection
  confines every bridge match to that static domain. Purity makes the
  connection context-independent.
- **State footprint:** reads and writes no cells; it returns only the same
  integer value as fixed string length.
- **Value influence:** the integer selects the loop branch and therefore the
  returned string.
- **Value justification:** the two bridge-free connection claims plus the fixed
  `seqLen(str(CS))` rule.
- **Dependents:** the loop invariant and nonempty entry theorem.
- **Control validation:** the body mutation changes `>` to `<` and is rejected,
  with residual result `"a"` instead of `"bb"`.
- **Value validation:** fixed and projected canonical equations agree
  universally; the false zero interpretation is rejected at residual `1`.

On syntactic `str(CS)`, the bridge overlaps the fixed equation only
extensionally: projection collapses and both right-hand sides are `isLen(CS)`.

### `scanLongest` and `longestValue`

- **Class:** definitional summaries.
- **Semantic role:** specify the mathematical result without replacing program
  execution.
- **Domain:** total over `ValSeq`/`Val`. `scanLongest` has disjoint empty/cons
  equations. `longestValue` has empty and complementary string/non-string head
  cases.
- **Matched context / justification scope:** pure summary terms only.
- **State footprint:** none.
- **Value influence:** they are the invariant and final postconditions.
- **Value justification:** structural equations; on the target domain the
  strict fold gives the first maximum by the induction above.
- **Dependents:** all target claims.
- **Validation:** 11,331 independent differential cases, including tie,
  empty, representative bounded products, and Unicode cases, have zero
  mismatches. The false result claim is rejected.

### `SPEC.loop-invariant`

- **Class:** derived lemma/circularity.
- **Semantic role:** summarizes fixed execution of the exact source `for`
  loop; it is a claim, not an ordinary rewrite in `verification.k`.
- **Domain:** arbitrary finite remaining `ValSeq` satisfying `allStrings`,
  string accumulator/current values, `L != 0`, `L != -1`, and a module scope
  that does not shadow builtin `len`.
- **Matched context:** the exact `#loop`, target, body, local map, environment,
  parent scopes, and arbitrary continuation. Unmentioned configuration cells
  are framed and unchanged.
- **Justification scope / context containment:** the proved claim has the same
  arbitrary continuation and framed cells as its uses. The body contains no
  abrupt control, allocation, mutation outside the local map, or exceptions on
  the guarded domain.
- **State footprint:** preserves `strings`; updates `result` to the fold and
  permits `string` to become the last iterated string; all other cells are
  preserved.
- **Value influence:** directly supplies the returned value in the entry
  theorem.
- **Value justification:** base case consumes `.ValSeq`; inductive case
  executes one actual iteration and applies the same claim to the symbolic
  remainder.
- **Dependents:** `SPEC.nonempty-input`.
- **Validation:** focused proof `#Top`, whole proof `#Top`, body mutation
  failure, and false-postcondition failure.

## Exact commands and actual results

The complete reproducible sequence is in `prove.sh`.

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
```

Actual result: all four assertions completed with `<k> .K </k>`,
`<exc> NoExc </exc>`, `<exit-code> 0 </exit-code>`, process exit 0. LLVM
reported only warnings originating in the supplied semantics.

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled
kprove connection-spec.k --definition connection-kompiled \
  --spec-module CONNECTION-SPEC
```

Actual result: `#Top`, exit 0. The backend also emitted
`WarnTrivialClaim` because both canonical connection sides simplify to the
same term before reachability rewriting.

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

Actual result: `#Top`, exit 0. This command proves every target claim
together, so the nonempty entry claim can use the proved loop circularity.

```bash
python3 differential_test.py
```

Actual output: `differential: 11331/11331 passed`; exit 0. The oracle computes
the maximum length and then independently selects the first element having
that length.

```bash
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit 1 with `WarnStuckClaimState`; residual result
`str(iCons(98, iCons(98, .IntSeq)))` (`"bb"`) cannot match the deliberately
false `"a"` postcondition.

```bash
kprove spec-body-mutation.k --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit 1 with `WarnStuckClaimState`; the mutated `<` body returns
`str(iCons(97, .IntSeq))` (`"a"`) and cannot match `"bb"`.

```bash
kprove spec-value-mutation.k --definition connection-kompiled \
  --spec-module SPEC-VALUE-MUTATION
```

Actual result: exit 1 with `WarnStuckClaimState`; the residual is integer `1`,
rejecting the deliberately false length `0`.

## Gate results

### Gate A — PASS

- **A1:** the entry claims contain the exact `solution.mpy` function AST and
  execute its program-defined body. The `<` body mutation fails.
- **A2:** the only operational bridge is pure and state-free. All loop-local
  state changes execute under fixed semantics and are captured by the proved
  invariant.
- **A3:** the loop claim fixes the local/module/builtin scope chain and excludes
  module shadowing of `len`; calls, argument evaluation, branches, return, and
  frame control execute normally. The bridge has no control effect.
- **A4:** definitional equations have complete, disjoint cases or agreeing
  overlap. The guarded length twin has a bridge-free canonical connection.
- **A5:** `["a", "bb"]` is a satisfiable witness. Both the false result and
  material body mutation are rejected.

During construction, an earlier opaque symbolic-length helper was removed
after the inventory found that its value connection was not explicit enough.
The `#Top` obtained with that helper was discarded. The final artifacts use
the static total twin and the separately compiled bridge-free connection
claims described above.

### Gate B — PASS

- **B1:** empty plus symbolic nonempty claims cover arbitrary finite
  `List[str]`; there is no bounded unrolling or fixed-size restriction.
- **B2:** symbolic strings are arbitrary finite `IntSeq` values, so their
  structural length models Python code-point length. Concrete `.mpy` string
  literals in the supplied semantics are ASCII-only, but the target theorem
  takes symbolic string values and is not ASCII-restricted.
- **B3:** the summary equations and prefix induction establish maximum length
  and first-tie behavior, not merely an opaque execution result.
- **B4:** the implementation and prompt agree on all stated examples and the
  complete formal domain.

### Gate C — PASS

All proof files, connection claims, smoke program, mutation artifacts,
differential oracle, exact commands, results, and scope are present in the
current directory and reproduced by `prove.sh`.

## Trust boundary

- The supplied read-only MPY semantics, K compiler/prover/backend, SMT
  reasoning, and CPython AST translator are trusted infrastructure.
- The theorem assumes the supplied semantics correctly models the exercised
  Python subset.
- No proof-local trusted primitive is used. Supplied opaque operations such as
  sorting, floating point, or hashing are not exercised.
- Reachability establishes partial correctness; total-correctness termination
  is outside the K claim, though finite structural consumption supports it.

## Empirically supported facts

- LLVM `krun` executes the prompt cases plus a tie witness without exception.
- CPython differential testing has zero mismatches over 11,331 cases.
- These finite tests support the semantics-to-Python adequacy bridge; they do
  not replace the unbounded symbolic K theorem.

## Excluded behavior

Inputs that are not finite lists of strings are outside the HumanEval type
contract and outside the target claims. Mutation of the input list, exceptions
from ill-typed operations, resource exhaustion, concurrency, and external state
are not part of this pure function theorem.
