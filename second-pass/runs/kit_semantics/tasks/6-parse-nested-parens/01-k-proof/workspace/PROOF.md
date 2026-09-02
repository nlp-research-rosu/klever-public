VALIDATED

## What is proven

Under the supplied `MPY` semantics, the exact translated
`parse_nested_parens` implementation is partially correct for every finite
symbolic input `CS:IntSeq` satisfying `validInput(CS)`. This is an unbounded
domain theorem: neither the number of groups nor any group length is fixed.

`validInput` accepts sequences containing only `(`, `)`, and ASCII space,
requires nonnegative parenthesis depth at every prefix, permits spaces only at
depth zero, and requires final depth zero. Leading, trailing, and repeated
spaces are also accepted. The result is a fresh list whose entries, in group
order, are the maximum nesting depths. The final environment, stack, return,
exception, heap-location, and exit-code cells are constrained by the target
claim.

## Formal claim

The required target is `SPEC.parse-nested-parens` in `spec.k`:

```k
<k>
  #loadAll(solutionModule)
  ~> Call(Name("parse_nested_parens"), str(CS))
  => ref(0)
</k>
<heap> .Map => 0 |-> list(expectedDepths(CS)) </heap>
...
requires validInput(CS)
```

The claim starts at module loading, resolves the named function through the
fixed environment rules, evaluates the call and exact function body, and
constrains the returned reference and pointed-to list. The auxiliary
`SPEC.scan-loop` claim is a guarded circularity over arbitrary finite suffix
`CS`; fixed semantics executes one loop iteration before the circularity is
reused.

`expectedDepths` is the constructive mathematical contract. `nextDepth`
updates current nesting, `openDeepest` takes the running maximum,
`delimiterOutput` emits a completed nonempty group's maximum, and
`finishOutput` emits the final group. Because `validInput` permits separators
only at depth zero and enforces balanced groups, these equations define exactly
the deepest nesting level of each space-separated group.

## Proof-extension inventory

### Exact AST shorthands

- **Extension:** `loopBody`, `afterLoop`, `solutionBody`, and `solutionModule`.
- **Class:** Definitional summaries.
- **Semantic role:** Name exact AST fragments; they reduce to program syntax
  before fixed semantics executes it. They do not replace lookup, evaluation,
  control, or state transitions.
- **Domain:** Each is an unconditional, total, nullary function.
- **Matched context:** Only occurrences of the corresponding nullary AST
  symbol. No configuration cells, continuation, binding, or control stack are
  matched.
- **Justification scope:** The generated `solution.mpy` AST. Its SHA-256 is
  `f1320cc5aa8f242a9ad1695acd5a0f3d12c0033053d911a8bd4f7ebae6b3848c`.
- **Context containment:** Substitution is ordinary value expansion and is
  independent of surrounding context.
- **State footprint:** None.
- **Value influence:** Selects the exact loaded function, body, and loop used
  by both claims.
- **Value justification:** The equations reproduce the constructors emitted
  by `python3 py2mpy.py solution.py > solution.mpy`.
- **Justification:** Direct syntactic identity; `prove.sh` regenerates and
  hash-checks the term.
- **Dependents:** `SPEC.scan-loop` and `SPEC.parse-nested-parens`.
- **Control validation:** `spec-body-mutation.k` changes initial `depth` from
  `0` to `1`; the unchanged result claim is rejected and exposes `[2]`.
- **Value validation:** The LLVM smoke artifact uses an AST-identical copy of
  the function, checked by `ast.dump`.
- **Validation:** PASS.

### Scanner and output equations

- **Extension:** `nextDepth`, `scanDepth`, `openDeepest`,
  `delimiterDeepest`, `nextDeepest`, `scanDeepest`, `delimiterOutput`,
  `nextOutput`, `scanOutput`, `scanChar`, `finishOutput`, and
  `expectedDepths`.
- **Class:** Definitional summaries.
- **Semantic role:** Describe mathematical scalar and list values on claim
  right-hand sides. None matches or rewrites a program computation in `<k>`.
- **Domain:** All `Int` values, all finite `IntSeq` values, and all finite
  `ValSeq` accumulators of the declared sorts.
- **Matched context:** Function applications only; there are no configuration
  frames, bindings, continuations, or omitted cells.
- **Justification scope:** The complete declared domains. Character cases are
  `40`, `41`, and other; maximum/delimiter cases are `> 0` versus `<= 0` (or
  `D + 1 > M` versus `D + 1 <= M`).
- **Context containment:** Each use is within those complete domains.
- **State footprint:** None; the summaries name values but do not mutate
  scopes or heap.
- **Value influence:** They determine the invariant's scalar/list
  post-state and the target result.
- **Value justification:** Constructor recursion consumes one `IntSeq`
  element per step. Guards are pairwise disjoint and exhaustive, and their
  right-hand sides are the exact updates performed by the Python body.
- **Justification:** Structural recursion and integer trichotomy; the
  machine-checked `scan-loop` claim connects these values to fixed execution.
- **Dependents:** Both claims in `spec.k`.
- **Control validation:** No control is replaced. The body mutation probe
  confirms that changed fixed execution is not hidden by the summaries.
- **Value validation:** The false-result claim expecting `[2]` for `()` is
  rejected with the fixed execution exposing `[1]`; 8,323 independent finite
  differential cases have zero mismatches.
- **Validation:** PASS.

### Input-domain equations

- **Extension:** `wellFormedStep`, `wellFormed`, and `validInput`.
- **Class:** Definitional summaries.
- **Semantic role:** Define the target claim's source-contract precondition;
  they do not rewrite execution.
- **Domain:** All finite `IntSeq` inputs and all integer intermediate depths.
- **Matched context:** Predicate applications only.
- **Justification scope:** Complete character partition `40`, `41`, `32`,
  and all other codes; empty and cons sequence cases.
- **Context containment:** Every predicate use is within the complete declared
  domain.
- **State footprint:** None.
- **Value influence:** Restricts theorem inputs but does not select program
  branches after execution begins.
- **Value justification:** The rules directly encode balanced parentheses,
  nonnegative prefixes, and depth-zero separators.
- **Justification:** Structural recursion with disjoint, exhaustive guards.
- **Dependents:** `SPEC.parse-nested-parens`.
- **Control validation:** Not applicable; no operational control is replaced.
- **Value validation:** The example and `()` are realizable witnesses; the
  broader differential set is generated entirely from balanced groups.
- **Validation:** PASS.

### Loop circularity

- **Extension:** `SPEC.scan-loop`.
- **Class:** Derived lemma (auxiliary reachability claim).
- **Semantic role:** Executes the fixed `#loop` semantics and exact program
  body, then summarizes the resulting locals and pointed-to output list.
- **Domain:** Every finite `CS:IntSeq`, arbitrary integer `D` and `M`,
  arbitrary `OUT:ValSeq`, and the exact plain callee scope shown in the claim.
- **Matched context:** Exact `#loop(str(CS), Name("char"), loopBody)` with an
  arbitrary continuation; environment `L`; exact local bindings and
  `parent(0)`; heap entry `H |-> list(OUT)`; every other configuration cell and
  non-`H` heap/scope entry is framed.
- **Justification scope:** The claim is machine-checked over that same complete
  context. Its circular use is guarded by fixed-semantics iteration.
- **Context containment:** The matched and proved configurations are
  identical, including the arbitrary continuation and framed cells.
- **State footprint:** Reads/writes `depth`, `deepest`, `char`, and the list at
  heap location `H`; preserves `paren_string`, `depths`, environment, parent,
  continuation, stack, return/exception state, allocation counters, and all
  framed heap/scope entries.
- **Value influence:** Supplies every scalar and list value consumed by the
  final `if`, `append`, and returned result.
- **Value justification:** The total scanner equations above.
- **Justification:** Base case executes `#iterDone`; each inductive branch
  executes one fixed `#iterYield`, target binding, exact loop body, and loop
  control before reusing the circularity.
- **Dependents:** `SPEC.parse-nested-parens`.
- **Control validation:** Concrete LLVM execution terminates at `.K` with
  `NoExc`; the body-sensitivity mutation fails.
- **Value validation:** The false-result mutation fails and the ground
  residual exposes the actual list.
- **Validation:** PASS.

There are no operational bridges, priority rules, opaque result-bearing
symbols, proof-local trusted primitives, or execution-intercepting rewrites.

## Exact commands and actual outputs

The complete reproducible command sequence is in `prove.sh`; running
`./prove.sh` exited `0`. Material commands and observed results were:

```text
python3 py2mpy.py solution.py > solution.mpy
sha256sum -c -
solution.mpy: OK

python3 test_differential.py
differential cases=8323 mismatches=0

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
Exit: 0

krun smoke.mpy --definition runtime-kompiled
Exit: 0
Final: <k> .K </k>, <exc> NoExc </exc>, <exit-code> 0 </exit-code>

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
Exit: 0

kprove spec.k --definition verification-kompiled --spec-module SPEC
#Top
Exit: 0

kprove spec-vacuity.k \
  --definition verification-kompiled --spec-module SPEC-VACUITY
WarnStuckClaimState; residual heap contains list(vCons(1, .ValSeq))
Exit: 1 (expected)

kprove spec-body-mutation.k \
  --definition verification-kompiled --spec-module SPEC-BODY-MUTATION
WarnStuckClaimState; residual heap contains list(vCons(2, .ValSeq))
Exit: 1 (expected)
```

Both `kompile` invocations emitted only warnings originating in the supplied
reference semantics. The installed `kompile` and `kprove` report K
`v7.1.293`.

## Gate results

### Gate A — PASS

- **A1:** The proof loads the exact module, resolves the named binding, and
  executes the function and loop bodies under fixed semantics. The generated
  AST is pinned, and the material body mutation is rejected.
- **A2:** The target constrains result, scopes, environment, heap,
  allocation counter, stack, return state, exception state, and exit code.
  The loop claim explicitly accounts for its complete state footprint.
- **A3:** Lookup, argument evaluation, iteration, conditionals, append,
  return, and frame popping all execute in the supplied semantics. There is no
  bridge or abrupt-control shortcut.
- **A4:** Every proof-local function is total. Constructor cases and integer
  guards are exhaustive and pairwise disjoint; recursive definitions descend
  structurally.
- **A5:** `()` is a satisfiable witness. The false `[2]` result is rejected,
  with residual `[1]`.

### Gate B — PASS

- **B1:** `CS` is symbolic and unbounded over all finite inputs satisfying the
  full described contract; no list length, group count, or nesting depth is
  bounded.
- **B2:** On this ASCII parenthesis/space domain, the reference semantics'
  unbounded integers, code-sequence strings, ordered lists, iteration, and
  exceptions materially agree with Python behavior used by the program.
- **B3:** Fixed execution is connected to `scanOutput` by the loop claim.
  `expectedDepths` initializes that scanner at depth/maximum zero and its
  equations constructively define the maximum prefix depth of each balanced
  group.
- **B4:** The implementation and prompt example agree; the implementation
  also correctly treats `()()` as one group and tolerates repeated boundary
  spaces.

### Gate C — PASS

- **C1:** The trust ledger below names all remaining external assumptions and
  their dependents. There are no unproved proof-local value abstractions.
- **C2:** All claimed artifacts and logs exist. `prove.sh` regenerates them,
  checks program identity, runs the unbounded proof, and checks both expected
  failures. Concrete and differential evidence is explicitly finite.
- **C3:** Machine-checked facts, external trust, finite evidence, and excluded
  behavior are separated in this report.

## Trust boundary

- The supplied, unmodified `reference-semantics/` definition is trusted as the
  intended model for function calls, string iteration/comparison, integer
  arithmetic, lists, mutation, control, and exceptions. Both formal claims
  depend on it; LLVM smoke execution provides finite evidence.
- K `v7.1.293`, its Haskell/LLVM backends, and their solvers are trusted to
  implement K reachability logic. All machine-checked conclusions depend on
  this toolchain.
- `py2mpy.py` is trusted as the supplied CPython-AST transliterator. The proof
  pins its generated output by SHA-256 and the LLVM smoke function is
  AST-compared with `solution.py`.

## Empirically supported facts

- `smoke.py` runs three assertions under the LLVM semantics, including the
  prompt example, a same-group `()()` case, and repeated boundary spaces. The
  final state is `.K`, `NoExc`, exit code `0`.
- `test_differential.py` uses an independently written split-and-prefix-depth
  oracle over 8,323 cases generated from every balanced group through five
  pairs plus pair combinations and spacing variants. It reports zero
  mismatches.
- These finite checks support implementation intent and the supplied execution
  model; they are not used as a substitute for the symbolic theorem.

## Excluded behavior

- Strings containing characters other than `(`, `)`, and ASCII space,
  unbalanced groups, separators inside a group, tabs/newlines as separators,
  and arbitrary Unicode text are outside `validInput` and outside the prompt's
  described input format.
- The report establishes partial correctness under the supplied semantics; it
  does not make a separate complexity or resource-bound theorem.
- Behavior of Python features not exercised by this implementation is outside
  the theorem.
