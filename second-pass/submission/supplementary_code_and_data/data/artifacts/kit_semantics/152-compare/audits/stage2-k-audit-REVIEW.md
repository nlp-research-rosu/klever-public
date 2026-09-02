# Independent adversarial review: 152-compare

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted program over equal-length finite lists of integer match
scores. I reconstructed the proof from source with the trusted supplied
semantics; I did not use either candidate-provided kompiled directory. The only
remaining concern is an intent-level typing ambiguity: the trusted prompt calls
the elements “scores” and all examples use integers, but it does not contain an
explicit type annotation. The theorem covers the material HumanEval integer
score domain, not floating-point or arbitrary Python numeric objects.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, problem `152-compare`, and condition
`kit-semantics`. The required trusted tree
`/reference/reference-semantics` is present, so the mount agrees with the
rendered mode.

I independently checked the following:

- The JSON value at `.audit_campaign` is exactly equal to
  `/audit-campaign-lock.json`, and the lock's raw SHA-256 is the declared
  `ad5dfc...d745`.
- Every required pipeline-v3 record is a real, readable regular file or
  directory. This includes `/run.json`, `/task.json`,
  `/generation-result.json`, all seven named generation metadata/text records,
  and the structured trace.
- All declared direct file hashes match. The trace file also matches the
  `4dae0c...e08` hash recorded in both the invocation and generation-result
  records. The launcher/pipeline tree digests for the candidate, supplied
  semantics, and trace all independently match their recorded values.
- All 542 structured-trace lines parse as JSON (170 `event_msg`, 369
  `response_item`, and one each of the three metadata types).
- No symlink occurs anywhere under `/candidate`, `/reference`, or
  `/generation-evidence`.
- `/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
  trusted mounted versions.
- Recursive type/path/content comparison of all 25 entries in
  `/candidate/reference-semantics` against
  `/reference/reference-semantics` is exact: no missing, additional,
  mistyped, changed, or linked entry.

The generation records claim success, but I used that only as historical
evidence. The actual audit results below are fresh.

Evidence:

- `evidence/01-provenance-integrity.log`
- `evidence/01b-provenance-json-and-trace.log`
- `evidence/01c-generation-record-review.log`
- `evidence/01f-independent-and-pipeline-tree-hashes.log`
- `evidence/verify_provenance.py`
- `evidence/verify_tree_hashes.py`

`01d` and `01e` are preserved exploratory hash-format probes. They compared
different recorded tree-digest formats to one another; `01f` applies each
declared pipeline format to its corresponding field and is the authoritative
successful check.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: for two equal-length arrays of match scores and
guesses, return an array of the same length whose element at each index is the
absolute difference between score and guess (zero when they are equal). The
trusted canonical implementation is
`[abs(x-y) for x,y in zip(game,guess)]`.

The submitted `solution.py` initializes a result list, iterates over the same
`zip(game, guess)`, appends `abs(score - predicted)`, and returns the list. It
is the same algorithm expressed as a loop.

Running the trusted `/reference/py2mpy.py` on the submitted `solution.py`
produced a file byte-identical to `/candidate/solution.mpy`:

```text
ed01c1a...b9d21  /candidate/solution.mpy
ed01c1a...b9d21  /tmp/audit-work/candidate/solution.regenerated.mpy
byte_identity_cmp_exit=0
```

The independent differential test imports the trusted canonical entry point
and the scratch-copy candidate entry point. It checks both prompt examples,
empty, equal, positive/negative difference, negative operands, and arbitrary
precision integer boundaries; exhaustively checks every pair of lists through
length 3 over `{-3,-1,0,1,3}`; and checks 10,000 seeded equal-length generated
pairs through length 30 with elements in `[-10^12,10^12]`. Result:

```text
cases=26284
mismatches=0
EXIT_STATUS: 0
```

Evidence:

- `evidence/02-source-and-proof-artifacts.log`
- `evidence/02a-translator-byte-identity.log`
- `evidence/02b-independent-differential.log`
- `evidence/differential_audit.py`

The formal proof domain is arbitrary-length equal-length integer lists. This is
not a finite-size or bounded-unrolling theorem. Unequal lists are outside the
stated source contract. The prompt does not explicitly spell out the element
type, although “match scores” and every example are integer-valued. I therefore
treat integers as the material HumanEval domain while recording the absence of
an explicit annotation as the final non-fatal concern. If the contract were
instead read as requiring all floating-point or arbitrary duck-typed numeric
objects accepted accidentally by the canonical Python expression, this K
theorem would not cover that broader reading.

## 3. Clean proof reconstruction

I copied source artifacts to `/tmp/audit-work`, moved the copied
`runtime-kompiled`, `verification-kompiled`, and `__pycache__` trees out of the
active scratch candidate, and replaced its copied semantics source with the
trusted mounted semantics tree. No candidate cache or compiled definition was
used.

The live tools are K 7.1.293. Fresh builds succeeded:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
EXIT_STATUS: 0

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
EXIT_STATUS: 0
```

A reviewer-authored concrete program ran the real function on empty, equality,
both subtraction signs, negative values, and both prompt examples. It ended at
`.K`, `NoExc`, and exit code `0`.

The complete positive specification independently closed:

```text
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
#Top
EXIT_STATUS: 0
```

Claim-level checks also closed:

- `SPEC.compare-loop-step`: `#Top`, exit `0`.
- `SPEC.compare-entry-empty`: `#Top`, exit `0`.
- `SPEC.compare-entry-step` together with its required
  `SPEC.compare-loop-step` circularity: `#Top`, exit `0`.

An additional diagnostic selected `compare-entry-step` while deliberately
excluding its loop circularity and was manually interrupted after divergence;
that selection removes a required proof dependency and is not a failed target
proof. It is transparently preserved as `03h`. The aggregate run and the
dependency-complete claim selection are the relevant positive runs.

Evidence:

- `evidence/03a-toolchain.log`
- `evidence/03b-clean-llvm-kompile.log`
- `evidence/03c-clean-concrete-execution.log`
- `evidence/03d-clean-haskell-kompile.log`
- `evidence/03e-kprove-all-positive.log`
- `evidence/03f-kprove-claim-loop.log`
- `evidence/03g-kprove-claim-entry-empty.log`
- `evidence/03h-kprove-claim-entry-step.log`
- `evidence/03i-kprove-claim-entry-step-with-loop.log`
- `evidence/concrete_audit.py`

## 4. Adequacy and real-program pinning

### Claims in plain language

`compare-loop-step` starts at the real loop head with a nonempty zipped pair,
integer heads, equal-length integer tails, the precise loop target/body,
function-local bindings, output reference `0`, and an accumulated output
prefix. It executes the remaining loop and leaves heap location `0` equal to
`compareAcc(prefix, scores, predictions)`. The guard also rules out a
module-level binding that would shadow builtin `abs`.

`compare-entry-empty` loads the submitted `compare` definition, calls it on two
empty list values from the normal initial module/builtin scopes, and requires
return value `ref(0)`, heap `0 |-> list(.ValSeq)`, a single fresh allocation,
empty stack, `noRet`, `NoExc`, and exit code `0`.

`compare-entry-step` loads the same definition and calls it on arbitrary
nonempty equal-length integer lists. Its postcondition requires return value
`ref(0)` and heap
`0 |-> list(compareAcc(.ValSeq, scores, predictions))`, plus the same normal
control-state obligations. `sameIntLists` recursively constrains every tail
element and proves equal shape; it is not a fixed-size premise.

### Program identity and result constraint

Trusted regeneration first pins `solution.py` to `solution.mpy`. A separate
mechanical checker tokenized the regenerated module and both `#loadAll`
arguments. After removing only explicit empty sequence units `.Stmts` and
`.Exprs`, which are syntax-normalization units, both entry terms have the same
105 constructor/string/integer tokens as `solution.mpy`.

```text
entry_1_constructor_token_identity: True
entry_2_constructor_token_identity: True
all_entry_modules_identical_after_empty-unit_normalization: True
```

The return is not a free value or implication-only observation. It is fixed to
`ref(0)`, and the referred heap value is fixed to the accumulator recurrence.
The accumulator uses the supplied `applyBin("-",...)`,
`applyBuiltin("abs",...)`, and `valSeqConcat`; it introduces no arithmetic
oracle.

Satisfiable states include:

- Empty entry: `game=[]`, `guess=[]`.
- Nonempty entry: `game=[5]`, `guess=[2]`; all guards reduce to true.
- Loop entry: prefix `[]`, current pair `(5,2)`, both tails empty, module map
  containing `compare` but not `abs`, locals exactly as in the claim, and heap
  `0 |-> list([])`.

For `[5],[2]`, `compareAcc([], [5], [2])` reduces to `[3]`; both Python
implementations return `[3]`. For the second prompt example, both return
`[4,4,1,0,0,6]`. Reviewer-authored ground K claims for those two substitutions
returned `#Top`, exit `0`.

A reviewer-authored body-sensitivity claim changed the program term actually
loaded and executed so that it appends `abs(score-predicted)+1`. It built
successfully, executed `[5],[2]` to residual heap `[4]`, and failed the original
`[3]` obligation with `WarnStuckClaimState`, exit `1`. This confirms theorem
dependence on the loaded body rather than an external source filename.

Evidence:

- `evidence/04a-mechanical-program-pinning.log`
- `evidence/check_program_pinning.py`
- `evidence/04b-ground-substitution-kprove.log`
- `evidence/ground-witnesses.k`
- `evidence/04c-body-sensitivity-dry-run.log`
- `evidence/04d-body-sensitivity-kprove.log`
- `evidence/fresh-body-sensitivity.k`

## 5. Rule-by-rule static soundness review

The exhaustive inventory covers `semantics.k`, every supplied helper K file,
`verification.k`, and `spec.k`: 2,402 source lines, 229 syntax-declaration start
lines, 700 rules, and 3 claims. The attribute inventory records every function,
`total`, priority, `concrete`, `owise`, symbol/no-evaluator, and macro line.
There is no `[functional]` declaration and no simplification rule in these
sources. The complete numbered rule bodies and hashes are preserved in
`evidence/05a-exhaustive-source-inventory.log`; declarations and attributes are
enumerated in `evidence/05b-declaration-classification.log`.

Per-file rule accounting is:

| Source family | Rules | Static decision |
|---|---:|---|
| `semantics.k`, `syntax.k`, `iter.k` | 0 | Assembly, AST declarations, and iterator protocol declarations only; consistent imports/sorts. |
| `core.k` | 46 | Configuration, allocation, lookup, sequencing, evaluation order, and structural helpers are ordinary state-preserving semantics; used path reviewed in full. |
| `operators.k`, `int.k`, `bool.k` | 39 | Dispatch, dereference priorities, integer mathematics, and short-circuit equations are guard-disjoint or agree on overlaps. Used subtraction is exact K integer subtraction. |
| `list.k`, `tuple.k` | 48 | Allocation, iteration, tuple binding, and `append` preserve evaluation order and update only the selected heap object. These are used directly. |
| `controls.k`, `functions.k`, `call.k` | 70 | Loop/control, frames, binding, callee/argument order, lookup, return, and pop rules preserve the relevant cells. Used priority rules only select cell/ref/mutator-specific behavior over generic dispatch. |
| `builtins.k` | 137 | Registry implementations and folds are structural. The used `zip` rules yield pairs in order and stop at either empty tail; the used `abs(Int)` rule is exact. The opaque MD5 symbol is unused. |
| `range.k`, `str.k`, `set.k`, `dict.k` | 74 | Guarded structural subset semantics; none of these constructs occurs in the submitted module. |
| `subscript.k`, `methods.k`, `comprehension.k` | 122 | Indexed/slice, method, and macro families are unused. Their partial/total subset boundaries cannot influence these claims. |
| `float.k` | 121 | Explicit supplied-semantics opaque symbolic float primitives with concrete LLVM twins; duplicate mixed numeric equations have identical right-hand sides. No float term is reachable under `sameIntLists`. |
| `sort.k` | 19 | Explicit opaque supplied sort primitives plus concrete insertion equations; no `sorted` call is present. |
| `assert.k`, `concrete.k` | 19 | Assertion behavior is unused in proofs. `MPY-CONCRETE` is imported only by the LLVM main module and is absent from `VERIFICATION`. |
| `verification.k` | 5 | Proof-local equations reviewed individually below. |

The exact submitted-construct mapping is in
`evidence/used-construct-rule-map.md`. It covers module loading, `FuncDef`,
parameters, list allocation, `For`, `zip`, tuple target binding, `Expr`,
bound-method `append`, integer subtraction, `abs`, and return/frame pop.

### Proof-local inventory

`sameIntLists` is a total definitional summary:

1. Empty left sequence returns whether the right is empty.
2. Nonempty left/empty right returns false.
3. Two nonempty sequences require integer, non-reference heads and recursively
   check both tails.

Those constructor cases are exhaustive and disjoint. The recursion strictly
descends both sequences. On integer heads, the additional reference and
subtraction-result guards are true and exclude no concrete integer.

`compareAcc` is a partial definitional summary used only under equal-shape
inputs:

1. Two empty tails return the prefix.
2. Two nonempty tails append exactly
   `applyBuiltin("abs", applyBin("-", score, predicted), .Vals)` and recurse.

The cases are disjoint and strictly descending. Mismatched tails are outside
every use. `compareAcc` appears only as a mathematical post-state term; it
never rewrites a program redex or bypasses execution.

There are no proof-local priorities, simplifications, trusted primitives,
opaque symbols, operational bridges, or rules encoding this task's answer.
The loop claim is a reachability circularity, not an installed semantic
rewrite. The fixed semantics executes tuple binding, lookup, subtraction,
builtin dispatch, append, and loop control before the circularity can summarize
the next matching loop head.

The supplied float, sort, and MD5 opaque symbols are a broader semantics trust
boundary, but none affects a branch, value, state cell, exception, or
postcondition in this theorem. No inventoried rule was labeled unsound, so
there is no unsupported unsoundness allegation requiring a false-conclusion
witness.

Evidence:

- `evidence/05a-exhaustive-source-inventory.log`
- `evidence/05b-declaration-classification.log`
- `evidence/used-construct-rule-map.md`

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The fresh mutation
`evidence/fresh-false-mutation.k` executes the exact original program on the
satisfying input `[5],[2]` but changes the required result from `[3]` to `[4]`.

The mutation first built/parsed successfully:

```text
kprove fresh-false-mutation.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-FRESH-FALSE-MUTATION --dry-run
EXIT_STATUS: 0
```

The actual proof failed for the intended obligation:

```text
Warning (WarnStuckClaimState)
residual heap: 0 |-> list(vCons(3, .ValSeq))
[Error] Prover: backend terminated because the configuration cannot be
rewritten further.
EXIT_STATUS: 1
```

This is neither a parser failure nor an unreachable mutation: the residual is
the complete normal result and differs exactly at the mutated heap value.

Evidence:

- `evidence/06a-false-mutation-dry-run.log`
- `evidence/06b-false-mutation-kprove.log`
- `evidence/fresh-false-mutation.k`

## 7. Proven versus assumed accounting

What the successful reachability proof establishes is:

> Under the supplied `MPY` semantics, for every pair of finite, equal-length K
> `ValSeq`s whose elements are K integers, loading the exact regenerated
> `compare` module and calling `compare` from the specified initial
> configuration is partially correct: every terminating execution returns the
> fresh reference `ref(0)`, whose heap object is the in-order list of
> `absInt(score -Int prediction)` values, with normal restored control state.

Proven inside K:

- The exact submitted function body is loaded and executed.
- Module/builtin lookup selects the real `zip` and `abs` bindings.
- Both arguments bind in a fresh function frame.
- The result list is freshly allocated.
- Every pair is unpacked in order, subtraction and integer absolute value are
  executed, and `append` mutates that list.
- The invariant handles arbitrary remaining list length.
- The return reference escapes while the function frame is removed, and the
  required normal stack/return/exception/exit cells hold.

Trusted or informal boundaries:

- The K 7.1.293 implementation, Haskell prover, LLVM executor, and K's integer,
  Boolean, map, list, equality, and heating/cooling primitives are trusted
  infrastructure.
- The mounted translator is launcher-designated trusted. Byte-identical
  regeneration and constructor-level claim comparison connect Python source,
  `.mpy`, and the proof term; this is a mechanical bridge, not a differential
  assumption.
- The supplied semantics is the fixed theorem model. Its used rules were
  statically audited and concretely exercised, but correspondence of that model
  to full CPython remains the usual language-semantics trust boundary.
- Treating unannotated “match scores” as integers is an intent bridge supported
  by every prompt example and the benchmark's material score domain. This is
  the reason for `CONCERNS` rather than `PASS`; floats and arbitrary Python
  numeric objects are not formally covered.
- The 26,284 differential cases and concrete K runs are finite bridge evidence,
  not substitutes for the reachability proof.
- Termination is not separately established; the theorem is explicitly partial
  correctness.

Gate A (real-program soundness) passes: exact body, fixed execution, truthful
summaries, satisfiable witnesses, body sensitivity, and false-result rejection
all hold. Gate B covers the material equal-length integer-score contract, with
the documented non-fatal lack of an explicit prompt type annotation. Gate C
passes: all trust boundaries and reproducible evidence are identified.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
