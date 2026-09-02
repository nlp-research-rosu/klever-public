# Independent adversarial review: 19-sort-numbers

Finding: the candidate contains a real, non-vacuous K reachability proof of the
submitted program, over arbitrary-length sequences of valid numeral words. The
proof is legitimate but has two material auditability limitations: its
proof-local symbolic `split` bridge has no bridge-free universal connection
theorem, and its final result is conditional on the supplied semantics'
uninterpreted `sortKeyVS` contract rather than a K theorem of numeric ordering.
Neither limitation yields a false candidate rule on the intended domain, so
they warrant concerns rather than rejection.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, `semantics_mode = SUPPLIED_SEMANTICS`, and mounts the
trusted semantics at `/reference/reference-semantics`. The mode and mounts are
consistent; there is no infrastructure breach.

I read the launcher record, campaign lock, `/run.json`, `/task.json`,
`/generation-result.json`, invocation and metrics records, present
`usage.json`, `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the
structured JSONL trace. The trace contains 239 valid JSON records, including 41
recorded function calls; this is summarized by
[trace_summary.py](/audit-output/evidence/trace_summary.py) and
[generation-trace-summary.log](/audit-output/evidence/generation-trace-summary.log).
These generation records were treated only as untrusted history.

Independent checks found:

- The campaign block is exactly equal to `/audit-campaign-lock.json`, and its
  independently computed SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- All required legacy-selected records' file hashes match the hashes in
  `/audit-input.json` and `/generation-result.json`, including the trace file
  hash `6ed9303d...f252f9`.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounted versions.
- `diff -r --no-dereference` reports exact equality between the candidate and
  trusted `reference-semantics` trees. Their entry names, types, and modes also
  match. No symlink occurs anywhere under candidate `reference-semantics`, the
  candidate tree, or generation evidence.
- Every mounted candidate, reference, and generation-evidence file was hashed
  independently.

The commands, statuses, tree metadata, and hashes are in
[stage1-integrity.log](/audit-output/evidence/stage1-integrity.log),
[campaign-lock-comparison.log](/audit-output/evidence/campaign-lock-comparison.log),
and
[all-mounted-file-hashes.log](/audit-output/evidence/all-mounted-file-hashes.log).
All checks exited 0.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: given a string whose tokens are English numeral names
from `zero` through `nine`, separated by spaces, return those same tokens in
ascending numeric order, separated by single spaces. The documented example is
`"three one five" -> "one three five"`. The canonical implementation removes
empty fields, looks up each word in a ten-entry numeric map, performs a stable
keyed sort, and joins with spaces.

The candidate implements the same behavior on the intended valid-token domain.
`number_value` returns 0 through 8 in explicit branches and 9 otherwise;
because the contract permits only the ten words, its final branch is exactly
the `nine` case. `sort_numbers` applies whitespace-splitting, keyed `sorted`,
and a single-space join. Its additional behavior on invalid words is outside
the stated domain.

Trusted regeneration used:

```text
python3 /tmp/audit-work/review-19/trusted/py2mpy.py \
  /tmp/audit-work/review-19/candidate/solution.py \
  > /tmp/audit-work/review-19/regenerated-solution.mpy
cmp -s regenerated-solution.mpy candidate/solution.mpy
```

Both commands exited 0, so the submitted `.mpy` is byte-identical to trusted
translation. See
[translator-regeneration.log](/audit-output/evidence/translator-regeneration.log).

The independent differential test imports the trusted canonical and candidate
entry points separately. It exercises the example, empty input, all ten
singleton key branches, all 100 ordered pairs, duplicate and order boundaries,
leading/trailing/repeated literal spaces, and deterministic generated sequences
up to length 256. It ran 524 distinct cases with zero mismatches:

```text
CASE_COUNT: 524
MISMATCH_COUNT: 0
EXIT_STATUS: 0
```

The complete deterministic input generator and record are
[differential_test.py](/audit-output/evidence/differential_test.py) and
[differential-test.log](/audit-output/evidence/differential-test.log).

## 3. Clean proof reconstruction

All builds occurred in the fresh source copy
`/tmp/audit-work/review-19/candidate`. No candidate-provided compiled
definition or cache was copied or used.

The concrete definition was rebuilt with:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
```

This exited 0. Running `krun concrete_tests.mpy --definition
runtime-audit-kompiled` exited 0 in a terminal configuration with `.K`,
`NoExc`, and exit code 0. The build's non-exhaustiveness warnings concern
unused cases such as `cellsMark` in generic helpers, not a value reachable in
this program. Evidence:
[llvm-kompile.log](/audit-output/evidence/llvm-kompile.log) and
[llvm-concrete-tests.log](/audit-output/evidence/llvm-concrete-tests.log).

An additional reviewer-authored 20-case LLVM batch covers every singleton,
empty input, the example, permutations, duplicates, all words in descending
order, and spacing boundaries. It also terminated with `.K`, `NoExc`, and exit
code 0. See
[k_concrete_differential.py](/audit-output/evidence/k_concrete_differential.py),
[k-concrete-translation.log](/audit-output/evidence/k-concrete-translation.log),
and
[k-concrete-differential.log](/audit-output/evidence/k-concrete-differential.log).

The proof definition was rebuilt with:

```text
kompile verification.k --backend haskell \
  --main-module SORT-NUMBERS-VERIFICATION \
  --syntax-module SORT-NUMBERS-VERIFICATION \
  --output-definition verification-audit-kompiled
```

It exited 0. Each of the eleven target claims was then invoked independently
with:

```text
kprove spec.k --definition verification-audit-kompiled \
  --spec-module SORT-NUMBERS-SPEC \
  --claims SORT-NUMBERS-SPEC.<label>
```

The labels were `number-value-zero` through `number-value-nine` and
`sort-numbers-symbolic`. Every command exited 0 and printed `#Top`. Exact logs
are [haskell-kompile.log](/audit-output/evidence/haskell-kompile.log) and the
eleven `kprove-*.log` files in
[evidence](/audit-output/evidence/). Thus the positive dynamic reconstruction
gate passes.

## 4. Adequacy and real-program pinning

The ten helper claims all have a fully concrete initial configuration. In plain
language, each loads the submitted module, calls its actual `number_value`
binding on one valid word, and requires the corresponding integer result while
preserving `NoExc` and exit code 0.

The main claim's precondition is the standard empty module state plus an
arbitrary `WORDS:NumWords`. `NumWords` is a free, recursively generated sequence
whose elements are exactly the ten valid words, so it covers arbitrary lengths,
duplicates, and the empty sequence. `encodedWords` uses exactly one ASCII space
between adjacent tokens. The postcondition requires the returned value to be:

```text
str(joinCodes(
  " ",
  sortKeyVS(wordsVS(WORDS), numberKey)))
```

where `numberKey` is the exact loaded closure for `number_value`. This is a
specific term, not a free result variable or tautological implication.

The program is mechanically pinned. I parsed both the trustedly regenerated
`solution.mpy` and the claim's `solutionModule` macro using the fresh definition
with macro expansion. Their JSON K ASTs are byte-identical and have the same
SHA-256:

```text
41854e94ba8c918121183643c7e656b7da2af9a280349e0dfc870a8aaf9ee490
```

See
[constructor-pinning.log](/audit-output/evidence/constructor-pinning.log).
The executed call follows actual load, name lookup, closure binding, body
execution, method/builtin lookup, allocation, return, and frame-pop rules.

Satisfying states are explicit. For example,
`WORDS = nw(threeW,nw(oneW,nw(fiveW,.NumWords)))` denotes the contract example.
The empty, singleton, example, and duplicate substitutions all agree in the two
Python implementations; their formal substitutions and results are recorded in
[ground-claim-witnesses.log](/audit-output/evidence/ground-claim-witnesses.log).
Under the named stable-key-sort contract for `sortKeyVS`, the claimed result for
the example is `"one three five"`.

Body sensitivity also succeeds. A scratch mutation changed the actual
`sortBody` term inside `solutionModule` to `Return(Str("wrong"))`. The mutated
definition compiled, but the main proof exited 1 with `WarnStuckClaimState` and
the residual actual value `"wrong"` versus `numericOutput(WORDS)`. See
[verification-body-mutated.k](/audit-output/evidence/verification-body-mutated.k),
[body-mutation-kompile.log](/audit-output/evidence/body-mutation-kompile.log),
and
[body-mutation-main-proof.log](/audit-output/evidence/body-mutation-main-proof.log).

The formal spelling domain does not include leading, trailing, or repeated
delimiters, although both Python implementations accept those spellings. I do
not treat that as material narrowing: such strings contain empty fields rather
than solely the valid numeral tokens stated by the prompt. The complete
arbitrary-length valid-token domain is covered.

## 5. Rule-by-rule static soundness review

The deterministic inventory covers every K source used by either the concrete
or proof build, plus `verification.k` and `spec.k`. It contains the complete
text and source line of every declaration and rule:
[k-rule-inventory.log](/audit-output/evidence/k-rule-inventory.log), generated by
[k_rule_inventory.py](/audit-output/evidence/k_rule_inventory.py).

Inventory totals are 238 syntax declarations, 726 rules, 5 contexts, one
configuration, and 11 claims across 26 files. Attribute-bearing records include
150 functions, 111 total declarations, 22 `no-evaluators` declarations, 46
priority rules, 36 concrete rules, 26 `owise` rules, and 8 macro declarations.
There are no local `functional` or `simplification` declarations.

| Source | Syntax | Rules | Static role/assessment |
|---|---:|---:|---|
| `semantics.k` | 0 | 0 | Assembly only; proof imports `MPY`, LLVM imports `MPY-KRUN`. |
| `syntax.k` | 16 | 0 | AST declarations; all submitted constructors are declared. |
| `core.k` | 37 | 46 | Configuration, loading, lookup, sequencing, literals, allocation, and argument evaluation; used rules preserve the declared cells and left-to-right order. |
| `functions.k` | 4 | 15 | Definitions, binding, calls, returns, and frame restoration; the plain closure path is used and matches the actual binding. |
| `call.k` | 3 | 21 | Callee/argument evaluation and dispatch; the proof reaches the exact builtin, bound-method, and closure values. |
| `controls.k` | 3 | 34 | `If` and truthiness rules execute every key-function branch; loop/import rules are unused. |
| `operators.k`, `int.k`, `bool.k` | 1 | 39 | Comparison dispatch and integer/boolean operations; string comparison routes to `str.k`. |
| `str.k` | 5 | 28 | ASCII literal codes and string equality/concatenation; exact for the ten ASCII words. |
| `methods.k` | 27 | 75 | The used fixed rules are whitespace `split`, list-argument dereference, and string `join`; recursive helpers descend structurally. |
| `list.k`, `tuple.k`, `iter.k` | 10 | 48 | List values/allocation and generic sequence support; only list values and allocation are material here. |
| `sort.k` | 6 | 19 | The used keyed sort is the fixed opaque `sortKeyVS` primitive; concrete keyed execution is deliberately elsewhere. |
| `concrete.k` | 5 | 16 | LLVM-only keyed sort executes the real key closure and stable insertion; absent from the Haskell proof definition as declared. |
| `range.k`, `subscript.k` | 17 | 46 | Unused by the submitted program; total/OOB abstractions do not contribute to closure. |
| `set.k`, `dict.k` | 18 | 40 | Unused collection semantics. |
| `comprehension.k` | 3 | 7 | Unused macro expansion. |
| `float.k` | 34 | 121 | All float and its opaque primitives are unused. |
| `builtins.k` | 38 | 137 | Registry/support rules; only builtin lookup and routing surrounding `sorted` are material. |
| `assert.k` | 0 | 3 | Used only by concrete smoke tests, not by proof claims. |
| `verification.k` | 11 | 31 | Four exact macros; ten `wordVal`; two `wordsVS`; ten `wordCodes`; three `encodedWords`; one split bridge; one result summary. |
| `spec.k` | 0 | 0 | Eleven reachability claims inventoried separately. |

### Construct coverage and execution path

The submitted `Module`, `FuncDef`, `Params`, statement sequencing, `If`,
`Compare`, `Name`, `CmpOp`, `Str`, `Return`, `Int`, `Call`, `Attribute`, and
`KwArg` nodes all map to declarations and active rules in the table above.
Execution loads both real functions, resolves globals and builtins through the
scope chain, creates and binds a real function frame, evaluates calls and
arguments left-to-right, allocates the split and sorted lists, dereferences the
join argument, returns, and restores the caller frame. No used construct is
silently dropped.

### Candidate-local equations

- `numberBody`, `sortBody`, `solutionModule`, and `numberKey` are syntax macros
  whose expansions exactly match the translated program and its loaded closure.
- `wordVal` and `wordCodes` have ten disjoint equations covering the ten
  `NumWord` constructors.
- `wordsVS` has disjoint empty/cons equations and structurally descends.
- `encodedWords` has disjoint empty, singleton, and two-or-more equations and
  structurally descends, inserting exactly one ASCII space.
- `numericOutput` has one covering equation and merely names the term returned
  after fixed `join` and fixed opaque keyed sort.

There are no local equation overlaps, unguarded contradictory cases,
non-descending recursion, or false totalization guards.

### Proof-local `split` operational bridge

The sole candidate operational bridge matches only the already-resolved,
zero-argument call:

```text
#applyK(toCall(boundMethodV(str(encodedWords(WORDS)), "split")), .Vals)
```

It preserves the arbitrary continuation admitted by `...`, introduces no
return/exception/frame effect, and reads or writes no cell directly. Its result
is `#alloc(list(wordsVS(WORDS)))`; consequently allocation still uses the fixed
heap and heap-location rule. Its priority 30 preempts the fixed priority-40
`splitWS` route. The fixed route has the same continuation and allocation
footprint, so the only obligation is:

```text
splitWS(encodedWords(WORDS), .IntSeq, .ValSeq) = wordsVS(WORDS)
```

That equality is mathematically true under the intended structural meaning of
`encodedWords`: each enumerated word has no whitespace, one ASCII space occurs
between adjacent words, and `splitWS` drops the empty token for the empty input.
No contrary ground or symbolic witness was found, so I do not label the bridge
unsound.

However, the candidate did not provide the bridge-free universal connection
theorem required to make this fully auditable. Removing the bridge and rerunning
the complete symbolic claim builds successfully but exits 1 at exactly the
unproved equality above. Even bridge-free ground attempts remain stuck because
the proof-only `encodedWords` rewrite does not normalize below the fixed
`splitWS` evaluator. Evidence:
[verification-bridge-free.k](/audit-output/evidence/verification-bridge-free.k),
[bridge-free-main-proof.log](/audit-output/evidence/bridge-free-main-proof.log),
[split-connection-attempt.log](/audit-output/evidence/split-connection-attempt.log),
and
[bridge-free-ground-proof.log](/audit-output/evidence/bridge-free-ground-proof.log).
This is a universal-evidence gap, not a witnessed false rule.

### Opaque keyed sorting

`sortKeyVS(ValSeq, Val)` is supplied, fixed semantics, not a candidate-added
symbol. It is declared `[function, total, symbol, no-evaluators]`; the Haskell
theory contains no equations establishing permutation, stability, ordering, or
that it invokes its key closure. The main proof therefore remains parametric in
this external primitive. The ten helper claims prove the key closure's values,
but they are not a K connection theorem for `sortKeyVS`.

A useful opposite-interpretation witness is the example sequence. The Haskell
equations permit an interpretation in which
`sortKeyVS([three,one,five], numberKey)` returns `[three,one,five]`; the proved
postcondition then denotes `"three one five"`, which is not the human contract
result. This does not make a K rule false—the theorem also executes `sorted`
through that same fixed primitive—but it shows that the human-facing ordering
conclusion is conditional on the named external `sortKeyVS = stable keyed
Python sorted` contract. The reviewer LLVM batch and 524-case CPython
differential provide finite support for that contract, not a universal theorem.

No rule is labeled unsound in this review; accordingly there is no unsupported
unsoundness allegation lacking a false-conclusion witness.

## 6. Fresh non-vacuity test

The fresh main-result mutation uses the satisfying input
`"three one five"` but changes the destination to the demonstrably false
reversed output `"five three one"`. Both Python implementations return
`"one three five"` for this witness.

The mutation at
[spec-vacuity-main.k](/audit-output/evidence/spec-vacuity-main.k) first
successfully dry-ran:

```text
kprove spec-vacuity-main.k --definition verification-audit-kompiled \
  --spec-module SORT-NUMBERS-SPEC-VACUITY-MAIN --dry-run -o none
EXIT_STATUS: 0
```

The actual proof then exited 1 with `WarnStuckClaimState`. Its residual is the
expected unmet equality between the reversed literal codes and the actual
`joinCodes(...sortKeyVS(...))` result, not a parser error, crash, timeout, or
unreachable mutation. See
[vacuity-main-dry-run.log](/audit-output/evidence/vacuity-main-dry-run.log) and
[vacuity-main-proof.log](/audit-output/evidence/vacuity-main-proof.log).

As an independent simpler check, changing the concrete `number_value("zero")`
postcondition from 0 to 1 also dry-ran successfully and then exited 1 with a
terminal actual result 0. See
[spec-vacuity.k](/audit-output/evidence/spec-vacuity.k),
[vacuity-dry-run.log](/audit-output/evidence/vacuity-dry-run.log), and
[vacuity-proof.log](/audit-output/evidence/vacuity-proof.log). The proof is
therefore result-discriminating and non-vacuous.

## 7. Proven-versus-assumed accounting

What is machine-checked:

- For each of the ten valid words, execution of the actual loaded
  `number_value` body returns its integer 0 through 9.
- For every arbitrary-length `NumWords` sequence, execution of the actual
  loaded `sort_numbers` body returns
  `str(joinCodes(" ", sortKeyVS(wordsVS(WORDS), numberKey)))`, under the
  candidate split bridge and fixed supplied semantics.
- The proof is sensitive to both the executed program body and its requested
  result.

What is trusted or informal:

| Boundary | Influence | Assessment/evidence |
|---|---|---|
| K toolchain and supplied `MPY` rules for load, binding, calls, strings, allocation, join, return | Control, state, and returned term | Ordinary verification trust boundary; rebuilt from the exact trusted tree. |
| Trusted `py2mpy.py` translation | Program identity | Byte-identical regeneration plus constructor-level K AST equality. |
| Proof-local `encodedWords`/`split` bridge | Converts every abstract input to the list consumed by sorting | Extensionally convincing and finitely exercised, but lacks a bridge-free universal connection theorem; principal auditability concern. |
| Fixed opaque `sortKeyVS` contract | Entire numeric ordering/permutation of the returned words | External Python-library boundary. LLVM concrete execution and 524 CPython differentials support it only finitely; K does not prove its ordering meaning. |
| ASCII code model | Literal words and separator | Exact for all contract tokens, which are ASCII. |
| Termination | Partial-correctness interpretation | Reachability closes for the modeled inputs, but the report makes no general claim about Python behaviors outside the supplied subset. |

The candidate does not prove a substituted function, does not bound input
length, does not leave the returned value as a free variable, and does not use
an inconsistent or witnessed-false proof rule. Its theorem is honest when read
conditionally on the fixed `sortKeyVS` contract. The missing universal split
connection and the informal sort-summary-to-human-contract bridge prevent a
clean `PASS`, but they do not make the reconstructed theorem illegitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
