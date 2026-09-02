VALIDATED

## What is proven

Under the supplied MPY reference semantics, the translated `solution.mpy`
implementation of `get_closest_vowel` satisfies the following all-path
reachability claim for every finite `CS:IntSeq`:

- it returns the singleton string containing the rightmost internal ASCII vowel
  whose immediate neighbors are not ASCII vowels; and
- it returns the empty string when no such index exists.

The proof treats the ten case-sensitive vowel codes as
`a,e,i,o,u,A,E,I,O,U`. On the prompt's stated domain of English-letter strings,
"not a vowel" is therefore exactly "a consonant." The K claim is a reachability
/ partial-correctness result. Source termination is also evident from the
strictly decreasing outer index and the one-shot inner/helper loops, but no
separate total-correctness claim is made.

The proof-quality headline `VALIDATED` is the result of Gates A, B, and C below.
It is separate from the runner's `KPROVE_PASSED` marker, which records only that
all required positive `kprove` commands printed `#Top` and exited 0.

## Formal claim

The claim `[entry]` in `spec.k` starts from the exact initial MPY configuration:

```k
#loadAll(getClosestProgram)
~> Call(Name("get_closest_vowel"), (str(CS), .Exprs))
```

with the initial global and builtin scopes, empty heap and stack, `noRet`,
`NoExc`, and exit code 0. It reaches:

```k
str(closestVowel(CS))
```

while leaving the two exact loaded function closures in the global scope.
There is no precondition on `CS:IntSeq`; this is stronger than the prompt's
English-letter input assumption.

`closestVowel(CS)` initializes a scan at `isLen(CS) -Int 2`. `closestScan`
decrements the index to 1, stores a singleton candidate only when the current
code is a vowel and both neighboring codes are not vowels, and preserves the
first candidate encountered. Because traversal is right-to-left, that candidate
is the requested closest vowel from the right. Lengths below three immediately
produce the empty string.

## Proof-extension inventory

The following two complete contexts are referenced by the records below.

**Helper context H.** The active term is the selected closure invocation
`#applyK(toCall(closureVal(("ch", .ParamNames), isVowelBody, 0)),
(str(iCons(C, .IntSeq)), .Vals)) ~> CONT`. The environment is 1. Scope 0
contains exactly the `_is_vowel` and `get_closest_vowel` closures with the exact
macro-expanded bodies and parent -1. Scope 1 contains exactly `word |-> str(CS)`,
`result |-> str(R)`, `found |-> F`, and `i |-> I`, with parent 0. Scope -1 is
an arbitrary `BUILTINS` map. `scopeLoc` is 2, the heap is empty, `heapLoc` is 0,
the stack is exactly `ListItem(frame(.K, 0, 1))`, and the remaining cells are
`noRet`, `NoExc`, and exit code 0.

**Loop context L.** The active term is the exact translated outer `#while`
whose body is `getClosestLoopBody`, followed by exactly
`(Return(Name("result")) .Stmts) ~> #endcall` and no further K continuation.
Its cells and bindings are H's cells. The guard is
`I >=Int 0 andBool I +Int 1 <Int isLen(CS)`. The justified destination is
`str(closestScan(CS,I,R,F))`, environment 0, the exact global and builtin scopes
with local scope 1 removed, `scopeLoc` 1, an empty stack, and all other cells
unchanged.

### 1. Exact syntax aliases

- **Extension:** the `[macro]` symbols `isVowelBody`,
  `getClosestLoopBody`, `getClosestBody`, and `getClosestProgram` in
  `foundation.k`.
- **Class:** definitional summary.
- **Semantic role:** compile-time names for exact MPY constructor terms; they
  neither replace nor add runtime execution.
- **Domain:** unconditional syntactic expansion.
- **Matched context / state footprint / value influence:** no runtime context
  or state; `getClosestProgram` determines which program the entry claim loads.
- **Justification scope and context containment:** macro expansion only.
  Expanded KORE for `getClosestProgram` and freshly translated `solution.mpy`
  was compared with `cmp`; both files were 21,104 bytes and identical.
- **Value justification / justification:** the constructor terms are direct
  transcriptions of `solution.mpy`, mechanically checked by the identity
  comparison.
- **Dependents:** both connection claims, both operational bridges, and
  `[entry]`.
- **Control and value validation:** mutating the helper body or the loop
  decrement prevents the corresponding negative claim from proving.
- **Validation:** Gate A1 PASS.

### 2. Vowel and candidate equations

- **Extension:** `vowelPred`, `isVowelCode`, `closestCandidate`, and
  `closestQualifies` in `foundation.k`.
- **Class:** definitional summary.
- **Semantic role:** mathematical values only; none rewrites an MPY program
  configuration.
- **Domain:** `vowelPred` and `isVowelCode` cover every integer.
  `closestCandidate` and `closestQualifies` are partial when their indices are
  out of bounds and intentionally have no `[total]` attribute. Their proof uses
  are in bounds. `closestQualifies` is documentary and is not needed by claim
  closure.
- **Matched context:** ordinary function terms, with no continuation, stack,
  bindings, or cells.
- **Justification scope / context containment:** `vowelPred(C)` is exactly the
  disjunction of the ten ASCII vowel codes. The two `isVowelCode` guards,
  `vowelPred(C)` and its negation, are disjoint and exhaustive.
  `closestCandidate(CS,I)` is used only where `0 <= I < isLen(CS)`.
- **State footprint:** none.
- **Value influence:** `vowelPred` determines helper results and scan branches;
  `closestCandidate` determines the returned singleton string.
- **Value justification:** direct exhaustive equations over integer equality
  and in-bounds `intSeqAt`.
- **Justification:** definitions plus the supplied integer and `IntSeq`
  equations.
- **Dependents:** helper claims/bridges and `closestScan`; ultimately `[entry]`.
- **Control validation:** not applicable to non-operational equations.
- **Value validation:** the helper's symbolic true and false connection claims
  fix both predicate outcomes; the mutated helper returning false for code 97 is
  rejected.
- **Validation:** Gate A4 PASS.

### 3. Scan and final-summary equations

- **Extension:** the five guarded `closestScan` recurrence rules and
  `closestVowel`, including the `[simplification]` attributes on the recurrence.
- **Class:** definitional summary.
- **Semantic role:** they define the mathematical post-state; they do not
  directly rewrite source-program syntax.
- **Domain:** the base case is `I <= 0`. For `I > 0`, `F=true` has one case.
  For `F=false`, the four cases are: current code non-vowel; current vowel with
  vowel on the left; current vowel with non-vowel left and vowel right; or the
  qualifying current vowel with two non-vowel neighbors.
- **Matched context:** function terms only; no K continuation or semantic cells.
- **Justification scope / context containment:** the cases above are pairwise
  disjoint and exhaustive. Every recursive rule changes `I` to `I - 1`.
  `closestVowel` starts at `len-2`; for lengths at most two the base rule
  applies, while for longer inputs all three inspected indices are in bounds.
- **State footprint:** none.
- **Value influence:** these equations define the entire entry postcondition.
- **Value justification:** right-to-left structural recursion. A qualifying
  candidate switches `found` to true, after which no later (more-leftward)
  index can replace it.
- **Justification:** induction on `max(I,0)`.
- **Dependents:** loop connection claim, loop bridge, and `[entry]`.
- **Control validation:** not applicable to the equations themselves.
- **Value validation:** the universal loop connection theorem connects exact
  execution to this value. Concrete and differential witnesses are listed
  below; the false result for `"yogurt"` is rejected.
- **Validation:** Gate A4 and Gate B3 PASS.

### 4. Definedness lemmas

- **Extension:** the two guarded simplification rules
  `#Ceil(intSeqAt(CS,I)) => #Top` for `0 <= I < isLen(CS)` and
  `#Ceil(closestScan(CS,I,R,F)) => #Top` for
  `I >= 0` and `I+1 < isLen(CS)`.
- **Class:** derived lemma.
- **Semantic role:** discharge definedness obligations; no program execution is
  replaced.
- **Domain:** exactly the guards above. There are no global totality assertions
  for `intSeqAt`, `closestCandidate`, `closestQualifies`, or `closestScan`.
- **Matched context:** only the stated `#Ceil` terms; no semantic configuration.
- **Justification scope / context containment:** `intSeqAt` is defined by
  structural induction on an in-bounds constructor sequence. `closestScan` is
  defined by induction on `I`: its cases are exhaustive, its accesses are in
  bounds under the guard, and the recursive call decreases `I`.
- **State footprint:** none.
- **Value influence:** definedness only; the recurrence equations separately
  fix values.
- **Value justification / justification:** the two inductions just stated.
- **Dependents:** symbolic simplification in the loop and entry proofs.
- **Control validation:** not applicable.
- **Value validation:** removing the formerly over-broad `[total]` attributes
  from candidate/qualification left all three positive proofs at `#Top`.
- **Validation:** Gate A4 PASS.

### 5. Helper connection claims

- **Extension:** `[helper-vowel]` and `[helper-consonant]` in
  `connection-spec.k`.
- **Class:** derived lemma (bridge-free universal auxiliary execution claims).
- **Semantic role:** execute the exact program-defined `_is_vowel` closure from
  context H to `true ~> CONT` under `vowelPred(C)`, or
  `false ~> CONT` under its negation.
- **Domain / matched context:** the complete H context for every integer `C`,
  arbitrary `CS,R,F,I,BUILTINS`, and arbitrary `CONT:K`, partitioned by the two
  disjoint predicate guards.
- **Justification scope:** fixed supplied MPY semantics plus the truthful
  foundation equations; `connection-spec.k` imports no helper bridge.
- **Context containment:** the helper operational rules accept exactly H and
  the same guards, so every bridge match is covered.
- **State footprint:** the exact invocation temporarily creates and removes its
  call scope; its net effect is only replacement of the call by the Boolean
  value. All listed cells and caller bindings are preserved.
- **Value influence:** the Boolean controls all three qualification tests in the
  outer loop.
- **Value justification / justification:** direct symbolic execution of the
  exact helper body. Both claims collectively printed `#Top`.
- **Dependents:** the helper operational rules and, through them, the loop
  theorem and `[entry]`.
- **Control validation:** arbitrary `CONT` is quantified by the theorem, and
  the exact caller stack/state is fixed.
- **Value validation:** both true/false symbolic domains are proved. The
  opposite result for the ground vowel `"a"` is rejected by
  `helper-body-mutation-spec.k`.
- **Validation:** Gates A1-A4 PASS.

### 6. Helper operational rules

- **Extension:** the two priority-40 `#applyK` rules in
  `helper-verification.k`.
- **Class:** operational bridge.
- **Semantic role:** accelerate the exact helper call to the Boolean established
  by the connection claims.
- **Domain / matched context:** exactly H with the corresponding
  `vowelPred(C)` or negated guard. The K-cell ellipsis admits exactly the
  arbitrary `CONT` quantified by the connection claims; no other cell is
  omitted.
- **Justification scope / context containment:** identical to the domains of
  `[helper-vowel]` and `[helper-consonant]`; `connection-spec.k` requires only
  `foundation.k`, so it cannot use these bridges.
- **State footprint:** reads the selected closure, singleton argument, exact
  caller bindings, environment, stack, and control cells; rewrites only the
  active call term to a Boolean. Heap, allocation counter, scopes, scope
  counter, caller stack, return, exception, and exit cells have the same net
  values as fixed execution.
- **Value influence:** the Boolean affects loop branches and the final result.
- **Value justification / justification:** the two universal bridge-free
  helper claims.
- **Dependents:** `[loop-invariant]` and `[entry]`.
- **Control validation:** the universal `CONT` connection proof covers the
  bridge's complete suffix domain.
- **Value validation:** vowel and consonant outcomes are separately proved; the
  mutated helper ground probe exits 1 with residual `false`.
- **Validation:** Gates A1-A4 PASS.

### 7. Loop connection claim

- **Extension:** `[loop-invariant]` in `loop-connection-spec.k`.
- **Class:** derived lemma (universal auxiliary execution claim).
- **Semantic role:** executes the exact translated outer loop, exact return,
  and exact `#endcall`, including frame/scope cleanup, to the scan summary.
- **Domain / matched context:** exactly L.
- **Justification scope:** supplied fixed semantics, foundation equations, and
  the already justified helper bridge only. It does not import
  `verification.k` or the loop bridge.
- **Context containment:** the loop operational bridge's expanded body,
  continuation, guard, bindings, stack, and every cell are identical to L.
- **State footprint:** reads the local word/result/found/index and helper
  binding; may update local result/found/index during execution; then returns,
  removes local scope 1, restores environment 0 and `scopeLoc` 1, pops the
  exact frame, and preserves heap, heap counter, globals, builtins, return,
  exception, and exit cells.
- **Value influence:** establishes the complete return value and final control
  state used by `[entry]`.
- **Value justification / justification:** symbolic execution with the scan
  recurrence as loop invariant; the claim printed `#Top`.
- **Dependents:** the loop operational rule and `[entry]`.
- **Control validation:** exact suffix and frame cleanup are part of the
  theorem, not inferred from a value-only result.
- **Value validation:** exact body mutation changes the fixed result and is
  rejected; scan outcomes are also covered by differential tests.
- **Validation:** Gates A1-A4 PASS.

### 8. Loop operational rule

- **Extension:** the priority-40 exact-loop rule in `verification.k`.
- **Class:** operational bridge.
- **Semantic role:** accelerates precisely the loop/return/frame-pop execution
  established by `[loop-invariant]`.
- **Domain / matched context:** exactly L. The rule contains the literal
  expanded loop body and exact suffix; it has no K-cell ellipsis.
- **Justification scope / context containment:** identical to L. The
  bridge-free theorem imports no loop bridge.
- **State footprint:** exactly the changes listed for the loop connection claim;
  no cell is framed or omitted.
- **Value influence:** supplies the final function result and cleanup state.
- **Value justification / justification:** `[loop-invariant]`, which printed
  `#Top`.
- **Dependents:** `[entry]`.
- **Control validation:** a suffix that first assigns `"x"` does not match the
  bridge and fixed execution returns `"x"`; the deliberately false `"a"`
  destination is rejected. Thus the rule cannot swallow an unproved
  continuation.
- **Value validation:** changing the decrement from 1 to 2 prevents the bridge
  from matching and yields the fixed empty result for the witness; the false
  `"a"` destination is rejected.
- **Validation:** Gates A1-A4 PASS.

No trusted primitive was added. `isVowelCode` and `closestVowel` retain
`[total]`; their exhaustive definitions justify totality. The audit removed
`[total]` from the partial `closestCandidate` and `closestQualifies` symbols
before the final rebuild.

## Exact commands and actual outputs

All commands are preserved in executable `prove.sh`. The final end-to-end run
was:

```sh
./prove.sh
```

Actual exit: 0.

The required concrete definition and execution were:

```sh
python3 py2mpy.py solution.py > solution.mpy
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
krun concrete-tests.mpy --definition runtime-kompiled
```

Actual exits: 0. Relevant final bindings were:

```text
r_yogurt   = str(iCons(117, .IntSeq))  # "u"
r_full     = str(iCons(85,  .IntSeq))  # "U"
r_quick    = str(.IntSeq)
r_ab       = str(.IntSeq)
r_empty    = str(.IntSeq)
r_rightmost= str(iCons(105, .IntSeq))  # "i"
```

The three positive proof layers were:

```sh
kompile --backend haskell foundation.k \
  --main-module FOUNDATION --syntax-module FOUNDATION-SYNTAX \
  --output-definition connection-kompiled
kprove connection-spec.k --definition connection-kompiled \
  --spec-module CONNECTION-SPEC
# Actual: #Top; exit 0

kompile --backend haskell helper-verification.k \
  --main-module HELPER-VERIFICATION \
  --syntax-module HELPER-VERIFICATION-SYNTAX \
  --output-definition loop-connection-kompiled
kprove loop-connection-spec.k --definition loop-connection-kompiled \
  --spec-module LOOP-CONNECTION-SPEC
# Actual: #Top; exit 0

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled --spec-module SPEC
# Actual: #Top; exit 0
```

The exact program-identity check was:

```sh
kast --definition verification-kompiled --module VERIFICATION-SYNTAX \
  --sort Module --expression getClosestProgram --expand-macros \
  --output kore > /tmp/get-closest-proof-program.kore
kast --definition verification-kompiled --module VERIFICATION-SYNTAX \
  --sort Module solution.mpy --expand-macros \
  --output kore > /tmp/get-closest-solution-program.kore
cmp /tmp/get-closest-proof-program.kore \
    /tmp/get-closest-solution-program.kore
wc -c /tmp/get-closest-proof-program.kore \
      /tmp/get-closest-solution-program.kore
```

Actual `cmp` exit: 0. Actual sizes:

```text
21104 /tmp/get-closest-proof-program.kore
21104 /tmp/get-closest-solution-program.kore
42208 total
```

The independent differential run was:

```sh
python3 validate.py
```

Actual output and exit:

```text
differential cases=102662 mismatches=0
exit 0
```

The four negative probes, also invoked by `prove.sh`, were:

```sh
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
# exit 1; residual result str(iCons(117,.IntSeq)), not empty

kprove helper-body-mutation-spec.k --definition connection-kompiled \
  --spec-module HELPER-BODY-MUTATION-SPEC
# exit 1; residual result false, not true

kprove loop-body-mutation-spec.k --definition verification-kompiled \
  --spec-module LOOP-BODY-MUTATION-SPEC
# exit 1; residual result str(.IntSeq), not "a"

kprove continuation-mutation-spec.k --definition verification-kompiled \
  --spec-module CONTINUATION-MUTATION-SPEC
# exit 1; residual result str(iCons(120,.IntSeq)), "x" rather than "a"
```

Each printed `WarnStuckClaimState` and terminated non-zero as expected. Compiler
output contained only warnings, chiefly unused-variable warnings and existing
non-exhaustiveness warnings in the supplied reference semantics.

## Per-gate results

### Gate A — PASS

- **A1:** the exact macro-expanded proof program equals freshly translated
  `solution.mpy`. Exact helper and loop bodies have bridge-free connection
  claims. Helper-body and loop-body mutations are rejected.
- **A2:** both operational bridges match complete configurations. Helper net
  state is unchanged; the loop theorem explicitly proves environment, scope,
  scope counter, stack, return, exception, heap, allocation, and exit state.
- **A3:** helper lookup and argument evaluation have already selected the exact
  closure before its bridge; arbitrary continuation is covered by its theorem.
  The loop bridge accepts only the exact return/endcall suffix. The changed
  continuation probe is rejected with the observable `"x"` result.
- **A4:** predicate and scan cases are disjoint/exhaustive, recursion descends,
  all accesses are guarded in bounds, and only genuinely total symbols carry
  `[total]`. The two definedness lemmas have valid guarded inductions.
- **A5:** `"yogurt"` is a realizable witness. Mutating its expected result from
  `"u"` to empty exits 1 with the actual code 117 visible in the residual.

### Gate B — PASS

- **B1:** the formal domain contains every finite code sequence and therefore
  contains the required English-letter strings without adding a restriction.
- **B2:** the used MPY subset models the relevant finite strings, ASCII
  literals, length, indexing, Boolean operations, comparisons, calls, and
  integer decrement. On the prompt's English-letter domain there is no material
  model mismatch for the stated property.
- **B3:** the scan equations encode the natural-language property directly:
  internal indices only, exact case-sensitive vowels, two non-vowel neighbors,
  and first hit in a right-to-left scan. This follows by induction on the scan
  index and is corroborated, not replaced, by the independent differential run.
- **B4:** the implementation's behavior matches every prompt example and the
  stated empty-result behavior.

### Gate C — PASS

- Every proof-local equation, lemma, claim, priority rule, bridge, guard,
  matched context, state effect, and dependent is inventoried above.
- `prove.sh` rebuilds every definition, reruns all positive claims, checks exact
  program identity, performs concrete and differential validation, and requires
  every negative probe to fail.
- The trust ledger and exclusions below separate formal results from finite
  evidence and model assumptions.

## Trust boundary

- **Supplied MPY semantics:** all behavior of MPY configurations, calls,
  scopes, builtins, strings, indexing, Booleans, and control is conditional on
  the correctness of the read-only `reference-semantics/`. It affects value,
  control, state, and termination modeling, and every K claim depends on it.
  No supplied file was modified.
- **K toolchain:** parsing, compilation, the Haskell symbolic backend, its SMT
  integration, and reachability implementation are trusted. Version used:
  K v7.1.293. All three symbolic proof layers depend on this boundary.
- **Translator boundary:** the theorem is directly about the generated MPY
  module. The unmodified `py2mpy.py` is trusted to represent the corresponding
  Python AST; the exact expanded-term comparison prevents proving a different
  MPY term than the generated `solution.mpy`.
- **LLVM and CPython:** LLVM `krun` and CPython testing provide empirical
  evidence only; the symbolic theorem does not depend on their concrete test
  outcomes.
- **Local derived lemmas:** the two `#Ceil` simplifications are proof-local
  derived facts, not external primitives. Their guarded structural inductions
  are recorded in the inventory and their domains do not include out-of-bounds
  access.

There are no fresh opaque result symbols and no externally trusted
program-derived oracle in the proof.

## Empirically supported facts

`validate.py` uses an independently written Python oracle: it scans indices
`len(word)-2` down to 1 and tests membership in the literal vowel set, without
calling any K summary. It checks:

- all six named boundary/example cases;
- every string of length 0 through 7 over alphabet `"abEYZ"` (97,656 cases);
  and
- 5,000 deterministic random `ascii_letters` strings of length 0 through 40,
  using seed 20260725.

The combined 102,662 cases had zero mismatches. This is finite evidence for
implementation/intent alignment, not a universal proof.

The LLVM execution establishes only the six displayed concrete results.
The four mutation probes establish sensitivity for their named witnesses; they
do not independently generalize beyond the universal connection claims.

## Excluded behavior

- Inputs that are not MPY string values and Python type-error behavior are
  outside the entry claim.
- Full CPython semantics, arbitrary Unicode literal translation, interpreter
  implementation details, I/O, concurrency, and external state are outside the
  supplied reference semantics and this theorem.
- The formal theorem treats any integer code outside the ten vowel codes as a
  consonant-like non-vowel. The prompt only requires English letters, where
  this coincides with the intended consonant classification.
- The K result is stated as reachability/partial correctness. A separate
  machine-checked total-correctness theorem is not claimed.
