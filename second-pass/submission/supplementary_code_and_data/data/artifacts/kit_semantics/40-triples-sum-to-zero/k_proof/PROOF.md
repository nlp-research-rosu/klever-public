VALIDATED

## What is proven

Under the supplied `MPY` semantics, the exact public call
`triples_sum_to_zero(l)` is partially correct for every arbitrary finite list
of mathematical integers.  If the call terminates, it returns `true` exactly
when there are indices `i < j < k` whose three list values sum to zero, and
returns `false` otherwise.

The theorem includes name lookup, argument evaluation, function-frame
creation, the complete translated function body, list indexing, integer
arithmetic and comparison, all three loops, return, and frame restoration.
The list and all other modeled state are unchanged.  The inaccessible heap
entry at location `-1` is a proof ghost preserved exactly by every claim.

## Formal claim

`SPEC.triples-sum-to-zero` starts with an arbitrary `IS:IntSeq`, represented as
the Python list `list(intVals(IS))`, and proves:

```k
Call(Name("triples_sum_to_zero"), (ref(0), .Exprs))
  => tripleFrom(IS, 0)
```

There is no length bound and no finite-size precondition.  The total summary
functions are nested bounded existentials:

- `thirdFrom(IS,I,J,K)` searches all `k >= K` with `I < J < k`;
- `pairFrom(IS,I,J)` searches all `j >= J` and their later `k`;
- `tripleFrom(IS,I)` searches all `i` and therefore all `i < j < k`.

Their step equation tests
`intAt(IS,i) + intAt(IS,j) + intAt(IS,k) == 0`.  Strictly increasing indices
mean distinct occurrences, while equal integer values remain allowed.

The three circularity claims discharge:

1. the inner-loop base and step for all remaining `k`;
2. the middle-loop base and step using the inner claim;
3. the outer-loop base and step using both inner claims;
4. the whole public call using the outer claim.

## Proof-extension inventory

No operational bridge and no proof-local trusted primitive is present.

### `intVals`

- **Class / role:** Definitional summary; embeds every `IntSeq` as the
  corresponding `ValSeq`.  It does not rewrite a program computation.
- **Domain:** Both constructors of every finite `IntSeq`; equations are
  disjoint, exhaustive, and structurally terminating.
- **Matched context / containment:** Mathematical `intVals(IS)` terms only;
  this is exactly the representation used by the claims.
- **State footprint:** None.  The resulting value is placed in the input heap
  by the claim.
- **Value influence / justification:** It determines the represented input
  list.  The two constructor equations fix every element and preserve order.
- **Dependents:** All loop and target claims.
- **Control/value validation:** No control effect.  Concrete MPY tests and the
  137,257-case differential test exercise the corresponding ordinary lists.

### `intSeqGhost`

- **Class / role:** Inert definitional constructor used only for symbolic name
  stability when a circularity rematches the heap.
- **Domain and matched context:** Every `IS:IntSeq`, only at unreachable heap
  key `-1` in the four positive claims.
- **Justification scope / containment:** The exact same constructor and
  sequence occur on both sides of every claim.
- **State footprint:** Read by no semantics rule, never written, and preserved
  exactly.  The program can access only `ref(0)`.
- **Value/control influence:** None; it cannot affect a branch, result,
  exception, allocation, or control.
- **Dependents / validation:** It assists circularity matching only.  The full
  proof closes while preserving it.

### `intAt`

- **Class / role:** Definitional summary for total mathematical integer
  indexing; it does not replace a source term by itself.
- **Domain:** All `IntSeq` and integer indices.  Empty, zero, positive, and
  negative cases are disjoint and exhaustive.  Positive recursion consumes one
  constructor.  Out-of-bounds values are totalized to zero.
- **Matched context / containment:** Used by the guarded in-bounds indexing
  lemma and by the result summary.  Only its in-bounds value can affect the
  program proof.
- **State footprint:** None.
- **Value influence / justification:** Its in-bounds value affects the tested
  sum and final Boolean.  Exhaustive constructor equations uniquely fix that
  value; off-domain totalization is unreachable under the lemma guard and loop
  invariants.
- **Dependents:** Index lemma, summaries, and all positive claims.
- **Control/value validation:** The false-result probe reaches actual `true`
  for `[0,0,0]` and rejects `false`; concrete and differential tests have zero
  mismatches.

### Length and indexing lemmas

- **Extensions:** `vsLen(intVals(IS)) => isLen(IS)` and the guarded
  `valSeqAt(intVals(IS),I) => intAt(IS,I)`.
- **Class / role:** Derived structural lemmas over the frozen semantics'
  helpers; no K-cell or source control term is intercepted.
- **Domain:** Length is universal.  Indexing requires
  `0 <= I < isLen(IS)`.
- **Matched context / containment:** Exactly the helper calls produced by
  frozen `len` and subscript execution on `list(intVals(IS))`; the indexing
  guard is the fixed semantics' valid in-bounds domain.
- **Justification scope:** Constructor induction.  `intVals` and `vsLen`
  consume corresponding heads; `valSeqAt` and `intAt` return corresponding
  heads and recurse with `I-1`.
- **State footprint:** None.
- **Value influence / justification:** Length selects loop branches and
  indexing supplies the summed integers.  The equations above fix both values
  over the complete used domain.
- **Dependents:** All loop and target claims.
- **Control/value validation:** No abrupt control.  LLVM execution, result
  mutation, body mutation, and the independent differential oracle all agree
  with the fixed concrete behavior.

### `thirdFrom`, `pairFrom`, and `tripleFrom`

- **Class / role:** Definitional result summaries, not operational rewrites.
- **Domain:** Their guards are pairwise disjoint and exhaustive for all integer
  indices.  Each recursive step increments an index and is guarded by the
  finite sequence length.
- **Matched context / containment:** They occur only in invariant and target
  postconditions.
- **State footprint:** None.
- **Value influence / justification:** They are the final Boolean property.
  Their equations directly define the three nested increasing-index
  existentials; no requested result is asserted by an extra lemma.
- **Dependents:** Corresponding inner, middle, outer, and target claims.
- **Control/value validation:** The positive proof establishes their
  connection to fixed execution.  The false-result mutation is rejected.

### Source syntax abbreviations and binding

- **Extensions:** `innerCond`, `innerBody`, `middleCond`, `middleBody`,
  `outerCond`, `outerBody`, `programBody`, `triplesClosure`, and
  `solutionBindings`.
- **Class / role:** Nullary definitional syntax abbreviations.  They expand to
  the exact AST constructors in `solution.mpy`; fixed semantics executes the
  expanded body.
- **Domain:** One exhaustive equation per nullary symbol.
- **Matched context / containment:** The exact global name
  `"triples_sum_to_zero"` is bound to the exact closure used by the entry
  claim.  Loop claims match the exact recurring `#while` terms, exact local
  scope, exact heap, exact call frame, and arbitrary active K continuation.
- **State footprint:** The body reads the input, updates only
  `found/i/j/k`, and returns through the fixed frame rules.
- **Value/control influence / justification:** Full influence; justified by
  literal constructor-for-constructor correspondence with `solution.mpy`.
- **Dependents:** Every claim.
- **Control/value validation:** Replacing the body with `return False` makes
  the `[0,0,0] => true` probe fail with residual `false`.

### Loop circularities

- **Extensions:** `SPEC.inner-loop`, `SPEC.middle-loop`, and
  `SPEC.outer-loop`.
- **Class / role:** Machine-checked auxiliary reachability claims; they
  summarize fixed execution after proving base and inductive paths.
- **Domain / matched context:** Their exact preconditions and complete
  configurations are in `spec.k`.  Each includes the active `#while`, local
  and global bindings, preserved heap and ghost, scope locations, call frame,
  return/exception state, and continuation frame.
- **Justification scope / containment:** Each claim is proved by `kprove` over
  that same complete match domain.  The middle proof uses the inner claim; the
  outer uses both; the target uses all three.
- **State footprint:** Exactly the loop counters and monotone `found` Boolean
  stated on each claim RHS; all other cells are fixed or framed identically.
- **Value/control influence:** They determine the target result and consume
  their loop computation without adding return, exception, break, or frame
  behavior.
- **Validation:** The joint positive run prints `#Top`; both negative probes
  are rejected.

## Exact commands and actual outputs

The reproducible runner is `./prove.sh`.  Its material commands are:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
cmp -n "$(wc -c < solution.py)" solution.py concrete-tests.py
python3 concrete-tests.py
python3 differential-test.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled --spec-module SPEC

kprove spec-vacuity.k \
  --definition verification-kompiled --spec-module SPEC-VACUITY
kprove spec-body-mutation.k \
  --definition verification-kompiled --spec-module SPEC-BODY-MUTATION
```

Actual results:

- `python3 differential-test.py`: `DIFFERENTIAL_CASES=137257`,
  `MISMATCHES=0`, exit 0.
- LLVM `kompile`: exit 0.  It emitted only supplied-semantics warnings.
- `krun`: exit 0 with final `<k> .K </k>`, `<exc> NoExc </exc>`, and
  `<exit-code> 0 </exit-code>`.
- Haskell `kompile`: exit 0.  It emitted only supplied-semantics unused-variable
  warnings.
- Positive `kprove`: `#Top`, exit 0.  See `proof-run.log`.
- False-result mutation: exit 1 with `WarnStuckClaimState`; actual residual is
  `true ~> .K` against requested `false`.  See `mutation-run.log`.
- Mutated-body probe: exit 1 with `WarnStuckClaimState`; actual residual is
  `false ~> .K` against requested `true`.  See `body-mutation-run.log`.
- The complete runner exits 0 and prints
  `POSITIVE_PROOF=#Top`, `FALSE_RESULT_MUTATION=REJECTED`, and
  `BODY_MUTATION=REJECTED`.

## Gate results

- **Gate A — PASS.** The exact program body executes under fixed semantics.
  There are no operational bridges or opaque result oracles.  Equations are
  exhaustive, disjoint, terminating where recursive, and guarded to their
  derivation domain.  `[0,0,0]` is a satisfiable witness.  False-result and
  body-sensitivity mutations both fail as required.
- **Gate B — PASS.** `IS:IntSeq` covers every arbitrary finite list of
  mathematical integers, with no size or value bound.  `i < j < k` is exactly
  the contract's distinct-element requirement, and the nested summary is
  definitionally the requested zero-sum existence property.
- **Gate C — PASS.** Commands, artifacts, input scopes, oracle, exit statuses,
  and residuals are recorded and reproducible.  Formal results, finite
  evidence, infrastructure trust, and exclusions are separated below.

## Trust boundary

Trusted infrastructure consists of the supplied read-only `MPY` semantics,
`py2mpy.py`, K v7.1.293 and its Haskell/LLVM backends.  There is no
proof-local trusted primitive.  The inaccessible `intSeqGhost` is preserved
state, not an assumed value contract.

This is a K partial-correctness theorem.  Termination is not a formal
reachability result, although every loop counter increases toward the fixed
finite length and all executable tests terminate.

## Empirically supported facts

`concrete-tests.py` uses the byte-identical implementation prefix verified by
`cmp` and checks all five prompt examples plus `[0,0,0]` and `[0,0]` under
both CPython and the required LLVM semantics.

`differential-test.py` uses `itertools.combinations` as an independently
implemented oracle and exhaustively compares all 137,257 lists of lengths
0 through 6 with values in `[-3,3]`.  It reports zero mismatches.  These finite
tests support implementation and modeling adequacy; they are not substituted
for the symbolic theorem.

## Excluded behavior

Non-integer list elements, list subclasses, concurrent mutation, and behavior
outside the supplied Python subset are outside the prompt contract and theorem.
Module-definition loading is setup; the theorem pins the exact translated
closure binding and proves the complete public invocation.  No finite list
length is excluded.
