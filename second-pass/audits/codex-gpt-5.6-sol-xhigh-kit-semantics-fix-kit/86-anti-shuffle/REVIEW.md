# Adversarial audit: 86-anti-shuffle

The candidate's positive proof commands are reproducible, and the submitted
Python implementation agrees with the trusted canonical implementation on the
tested domain. Nevertheless, the proof is not legitimate. Both operational
bridges in `verification.k` are globally false: they match a loop with an
arbitrary framed continuation and replace the loop by a function `Return`.
The supplied return semantics discards that continuation. The auxiliary claims
prove only the real loop *together with its exact trailing return* and therefore
do not justify these broader rules.

This is not a hypothetical concern. Fresh concrete K counterexamples show that
fixed semantics returns `"x"` while each bridge proves a different result with
`#Top`. A material mutation of the exact translated target body from `return
result + word` to `return "x"` also still proves the original postcondition with
`#Top`; fresh Python and LLVM execution return `"x"` for the satisfying empty
input. The proof thus fails real-program body sensitivity and relies on
materially unsound proof rules.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and the trusted mount is consistent
with it: `/reference/reference-semantics` exists. There is no infrastructure
boundary breach.

- `/candidate/run-input.json`, `metrics.json`, `codex-last.txt`, and
  `codex-output.log` are present as regular, non-symlink files. Their claims
  were not trusted. The structured trace is one regular JSONL file containing
  832 valid and zero invalid JSON records. The untrusted generation summary
  claims three `#Top` results and 57,987 differential cases; these claims were
  independently replaced by the evidence below. See
  [03_generation_claims_summary.log](evidence/03_generation_claims_summary.log).
- The candidate's `prompt.py` is byte-identical to `/reference/prompt.py`, and
  its `py2mpy.py` is byte-identical to `/reference/py2mpy.py`. Their SHA-256
  values are respectively `f8a02b...a972` and `406485...b16`. See
  [01_mount_and_provenance.log](evidence/01_mount_and_provenance.log).
- A no-follow recursive type-and-content comparison found exactly 26 entries
  in each supplied-semantics tree and zero missing, additional, changed,
  mistyped, or symlinked candidate entries. See the reviewer-authored checker
  [check_tree_integrity.py](evidence/check_tree_integrity.py) and its result
  [02_semantics_integrity.log](evidence/02_semantics_integrity.log).
- All required source deliverables—`solution.py`, `solution.mpy`,
  `verification.k`, `spec.k`, `prove.sh`, and `PROOF.md`—are present as regular
  files. Candidate-built `runtime-kompiled` and `verification*-kompiled`
  directories, caches, bytecode, logs, smoke tests, and mutations are
  additional generation artifacts, not source-integrity failures; none was
  reused.

All executable sources needed for the audit were copied to
`/tmp/audit-work/86-anti-shuffle`. The reference semantics, prompt, canonical
implementation, and translator in scratch came from `/reference`; candidate
compiled definitions and caches were neither copied nor read as definitions.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt requires `anti_shuffle(s)` to preserve the order of words
and literal blank spaces while replacing each space-separated word by the same
characters in ascending ASCII-value order. The trusted canonical program is:

```python
return ' '.join([''.join(sorted(list(i))) for i in s.split(' ')])
```

Because splitting and joining use the literal string `' '`, leading, trailing,
and adjacent spaces are preserved exactly. Other whitespace characters remain
characters within a word.

The submitted `solution.py` implements insertion sort. `insert_char` scans the
currently sorted word, inserts before the first strictly greater character,
and appends otherwise. `anti_shuffle` accumulates a word, emits it at every
literal space, and emits the final word after the scan. Empty strings, empty
words between adjacent spaces, equality in insertion, insertion before the
first element, and insertion after the last element are all handled.

### Translation identity

Running the trusted translator in scratch generated
`solution.regenerated.mpy`. It was byte-identical to the submitted
`solution.mpy`; both have SHA-256
`388a688f8d6ebb78b4e842b16a6a636e05bc365eee956c347d8f7b0d4865ee8b`.
The translator and comparison both exited 0. See
[04_translation_identity.log](evidence/04_translation_identity.log).

### Independent differential test

The reviewer-authored [differential_audit.py](evidence/differential_audit.py)
loads the trusted canonical and submitted modules by separate file paths. It
checks:

- all three documented examples;
- empty, one-space, adjacent-space, leading-space, and trailing-space cases;
- already sorted, reverse sorted, equal-character, insert-first, and
  insert-last paths;
- ASCII code boundaries `0` and `127`, tab, and newline;
- representative non-ASCII and maximum-Unicode characters;
- every length-0-through-5 string over the seven-character alphabet
  `" aA!~\x00\x7f"`;
- every length-0-through-4 string over `" aéΩ🙂"`; and
- 5,000 deterministic random strings of length 0 through 64 over all ASCII
  codes and seven selected Unicode boundaries, seed `860726`.

It executed 25,409 entry cases and seven direct helper branch cases with zero
mismatches. The complete generated input scope is fixed in the script, and the
entry stream digest is
`79e114b9dab69d8e09a7721dec89f80f7ecd602abfadabe4a7c3ccdb6dcfae0b`.
See [05_differential.log](evidence/05_differential.log). This strongly supports
implementation-to-canonical fidelity for the tested inputs; it is finite
evidence, not a universal proof.

## 3. Clean proof reconstruction

K version `v7.1.293` was available independently. Every definition was rebuilt
from source under `/tmp/audit-work/86-anti-shuffle`; candidate-provided
compiled directories were not used.

### Concrete definition and execution

The trusted supplied semantics was freshly compiled with:

```text
kompile --backend llvm reference-semantics/semantics.k --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-audit-kompiled
```

The command exited 0; see [07_llvm_build.log](evidence/07_llvm_build.log).
Executing the actual submitted `solution.mpy` reached `.K`, normal control, an
empty heap, and exit code 0. A separately authored assertion program containing
the same two function bodies exercised eight normal and boundary calls under
LLVM and also reached `.K` with exit code 0; the same assertions passed under
Python. See [06_concrete_program_prepare.log](evidence/06_concrete_program_prepare.log),
[08_krun_solution.log](evidence/08_krun_solution.log), and
[09_krun_concrete_cases.log](evidence/09_krun_concrete_cases.log).

### Positive reachability claims

All three candidate positive claims rebuilt and closed:

| Layer | Fresh definition and proof | Result |
|---|---|---|
| Helper loop | `VERIFICATION-BASE`; `kprove ... --spec-module SPEC-HELPER` | build 0; proof 0; `#Top` |
| Outer loop | `VERIFICATION`; `kprove ... --spec-module SPEC --claims SPEC.anti-loop` | build 0; proof 0; `#Top` |
| Entry | `VERIFICATION-FULL`; `kprove ... --spec-module SPEC-ENTRY` | build 0; proof 0; `#Top` |

Exact commands and outputs are in
[10_haskell_base_build.log](evidence/10_haskell_base_build.log) through
[15_kprove_entry.log](evidence/15_kprove_entry.log). Compiler diagnostics were
warnings, principally supplied-semantics unused variables and known
non-exhaustive total-function warnings; all builds exited 0. Thus the
candidate's execution claim—closure under its supplied theory—is genuine.
This gate does not establish that the added theory is sound.

A diagnostic attempt to execute proof-only `[simplification]` summaries under
LLVM remained at `antiFinish`/`insertFinish` and exited 113
([19_summary_empty.log](evidence/19_summary_empty.log) through
[21_summary_insert_ab.log](evidence/21_summary_insert_ab.log)). This is not a
failed target proof: simplification lemmas are not ordinary LLVM execution
rules. Their concrete substitutions were instead normalized by the Haskell
proof simplifier in Stage 4.

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC-HELPER.insert-loop` has no explicit `requires`, but its configuration
requires an exact helper loop head, a singleton `char = C`, local `prefix` and
`suffix`, the helper frame at location 2, `scopeLoc = 3`, normal return and
exception state, and a top stack frame returning to environment 1. It says the
loop plus the helper's real trailing return and `#endcall` returns
`insertFinish(PREFIX,C,SUFFIX)`, deletes the helper scope, restores the caller,
and preserves heap state.

`SPEC.anti-loop` likewise begins at the exact outer loop with arbitrary
`OUT`, `WORD`, and `REM`, exact module closures for both submitted functions,
the main call frame at location 1, and normal control. It says the loop plus
the real trailing return and `#endcall` returns
`antiFinish(OUT,WORD,REM)`, removes the local frame, preserves the module and
builtins scopes, and leaves heap state unchanged.

`SPEC-ENTRY.anti-shuffle` requires `asciiCodes(CODES)`: every input code is an
integer in `0..127`. Starting from the initial configuration, it loads the two
function definitions and calls `anti_shuffle(str(CODES))`. It requires the
returned value to be exactly
`str(antiFinish(.IntSeq,.IntSeq,CODES))`; this is not a free result variable,
tautology, or one-way implication. The final module scope is existential, but
the result, environment, scope allocator, heap, heap allocator, stack, return
state, exception state, and exit code are constrained.

### Exact program and loop shapes

The entry's embedded `Module` differs textually from `solution.mpy` only by an
explicit `.Stmts` list unit. Parsing both through fresh K syntax produces
byte-identical KORE, SHA-256
`b8d948ec200e31332d7e8ebdc1e7e9defd560b62ae16c0484e39d91103a09166` as fully recorded in
[18b_structural_program_pinning.log](evidence/18b_structural_program_pinning.log).
The reviewer checker also confirms the exact helper and outer `For`/`#loop`
shapes, target call, and target result; see
[check_program_pinning.py](evidence/check_program_pinning.py) and
[16_program_pinning.log](evidence/16_program_pinning.log). The initial failed
surface-parser experiment is retained in
[18_structural_program_pinning.log](evidence/18_structural_program_pinning.log);
it motivated the correct structural comparison and is not evidence against
pinning.

The submitted `For` bodies and the bodies in both loop claims are syntactically
the real bodies. However, the higher proof rules fail to pin the computation
*after* those loop bodies. That material adequacy failure is demonstrated in
Stage 5.

### Satisfying states and concrete substitutions

All preconditions are satisfiable. For the helper claim, take `C=97`, empty
prefix/suffix, an otherwise valid normal helper frame, and any permitted heap.
For the outer claim, take empty `OUT`, `WORD`, and `REM` in its displayed normal
frame. For the entry, `CODES=.IntSeq` satisfies `asciiCodes` and returns empty.

The independent witness uses input `"ba ab"`, codes
`[98,97,32,97,98]`. K simplification proves that the claimed result is codes
`[97,98,32,97,98]`, i.e. `"ab ab"`; both trusted canonical and submitted Python
return `"ab ab"`. It also checks empty input and the helper insertion of `a`
before `b`. See [summary-witness-spec.k](evidence/summary-witness-spec.k),
[22_summary_witness_kprove.log](evidence/22_summary_witness_kprove.log), and
[23_witness_python_compare.log](evidence/23_witness_python_compare.log).

## 5. Rule-by-rule static soundness review

### Exhaustive inventory and reachable semantics

The reviewer-authored [k_inventory.py](evidence/k_inventory.py) inventories
every source file in the supplied semantics plus `verification.k` and `spec.k`.
The resulting [k_inventory.tsv](evidence/k_inventory.tsv) has 1,125 declaration
rows: all 707 local rules, all 230 local syntax declarations, all 25 source
`requires`, all imports/modules, five contexts, one configuration, and three
claims. Each row includes source lines, attributes, flattened declaration, and
an audit decision. See [24_k_inventory_summary.log](evidence/24_k_inventory_summary.log).

In supplied-semantics mode, the byte-identical reference tree is the selected
fixed language model. Its entries are therefore recorded as the fixed trusted
baseline, not as candidate-created proof extensions. Concrete-only entries in
`semantics/concrete.k` are marked separately because proof module `MPY` does
not import `MPY-CONCRETE`. Twenty-two `no-evaluators` opaque declarations are
identified separately and are unused by this target.

The full reachable construct-to-rule mapping is in
[construct_rule_map.md](evidence/construct_rule_map.md). In summary:

- `core.k:49-60` supplies all ten configuration cells. `Module` loading and
  statement sequencing preserve left-to-right control.
- `functions.k`, `call.k`, and `core.k` perform real name lookup, callee then
  argument evaluation, local-frame allocation, parameter binding, return,
  frame deletion, and caller restoration.
- `controls.k`, `str.k`, and `tuple.k` evaluate a `For` iterable once, yield
  one-character strings, bind the loop target, and sequence each body before
  recurrence.
- `operators.k` and `str.k` evaluate string operands left-to-right and provide
  exact concatenation, equality, and lexicographic comparison.
- `subscript.k` evaluates the used `suffix[1:]` bounds in order and builds the
  tail. No program path allocates a heap object or invokes a builtin, sort,
  float, digest, collection mutation, exception, or output primitive.

No relevant supplied priority overlap changes that path. Proof-local
priority 40, however, deliberately preempts the supplied default loop rule and
is where soundness fails.

### Sound proof-local equations

There are three proof-local `[function,total]` symbols, eight simplification
rules, two ordinary predicate rules, and two priority-40 operational rules.
There are no proof-local `functional`, `concrete`, or opaque declarations.

- The guarded map-deletion simplification (`verification.k:9-11`) is true when
  `I` is absent from `REST`.
- The `buildIS` tail lemma (`verification.k:16-22`) is true for empty and
  nonempty tails: the normalized `[1:]` start/stop indices yield exactly
  `REST`.
- `insertFinish` has disjoint empty/nonempty shapes; its two nonempty guards
  are Boolean complements, and recursion removes one suffix constructor.
- `antiFinish` has disjoint empty, code-32, and non-32 cases, and recursion
  removes one remainder constructor.
- `asciiCodes` is constructor-complete, non-overlapping, and descending.

The compiler's syntactic non-exhaustiveness warnings for the first two total
summaries do not reveal an uncovered mathematical case: constructor coverage
and complementary guards are complete. Concrete summary witnesses also
normalize correctly in Stage 4.

### Unsound helper operational bridge: concrete false conclusion

The helper bridge is `verification.k:69-103`. Its left side matches the exact
helper `#loop`, locals, top function frame, and `scopeLoc=L+1`, but `...` frames
an arbitrary continuation after the loop. Its right side is
`Return(str(insertFinish(...)))`.

Take the entirely concrete, ASCII-valued state preserved in
[bridge-unsoundness-concrete-spec.k](evidence/bridge-unsoundness-concrete-spec.k):
`C=97` (`a`), empty prefix and suffix, normal control/cells, and computation

```text
#loop(str(.IntSeq), exact-helper-body)
~> Return(Str("x")) ~> #endcall
```

Under fixed `VERIFICATION-BASE`, the empty iterator finishes the loop, control
continues to `Return(Str("x"))`, and the final value is code 120 (`x`). The
claim that it returns code 97 is rejected with `WarnStuckClaimState`, whose
residual explicitly contains `str(iCons(120,.IntSeq))`; the true-`x` claim
closes with `#Top`. See
[33_helper_base_false_concrete_rejects.log](evidence/33_helper_base_false_concrete_rejects.log)
and [34b_helper_base_true_concrete_proves.log](evidence/34b_helper_base_true_concrete_proves.log).

With the bridge enabled in `VERIFICATION`, its priority-40 rule fires first.
It produces `Return("a")`; supplied `functions.k:78` discards the framed
`Return("x")` continuation. The false-`a` claim prints `#Top` and exits 0. See
[32_helper_bridge_false_concrete_proves.log](evidence/32_helper_bridge_false_concrete_proves.log).
This is a concrete false conclusion using only valid ASCII values. The lower
`insert-loop` claim does not justify it: that claim includes the actual helper
trailing return in its left-hand computation and proves only that continuation.

### Unsound outer operational bridge: concrete false conclusion

The outer bridge at `verification.k:111-143` has the same defect. With empty
`REM`, empty `OUT`/`WORD`, normal cells, and continuation
`Return(Str("x")) ~> #endcall`, fixed `VERIFICATION` returns `x`; the false
empty-result claim is rejected with an `x` residual and the true-`x` claim
closes. See
[36_outer_base_false_concrete_rejects.log](evidence/36_outer_base_false_concrete_rejects.log)
and [37_outer_base_true_concrete_proves.log](evidence/37_outer_base_true_concrete_proves.log).
With `VERIFICATION-FULL`, the bridge prematurely returns
`antiFinish(empty,empty,empty)=empty`, discards `Return("x")`, and proves the
false empty result with `#Top`; see
[35_outer_bridge_false_concrete_proves.log](evidence/35_outer_bridge_false_concrete_proves.log).
The empty remainder also directly satisfies the target entry's ASCII domain.

These witnesses differ from the submitted control path only in the continuation
the bridge failed to constrain. The shared proof-extension contract explicitly
rejects a globally false rule even when its bad cases are claimed to be off
path. Here the defect also destroys real-program body sensitivity.

### Material target-body mutation still proves

The independent mutation changes the exact `anti_shuffle` final statement from
`return result + word` to `return "x"`, leaving the loop untouched. The trusted
translator generated the mutated MPY program; parsing the generated program
and the mutated entry claim produced byte-identical KORE. Python execution and
a fresh LLVM assertion establish that empty input returns `"x"`. See
[make_final_return_mutation.py](evidence/make_final_return_mutation.py),
[38_final_return_mutation_generation.log](evidence/38_final_return_mutation_generation.log),
[39_final_return_mutation_prepare.log](evidence/39_final_return_mutation_prepare.log),
and [40_final_return_mutation_krun.log](evidence/40_final_return_mutation_krun.log).

Nevertheless, the mutated entry claim retains the original required
`antiFinish` result and still prints `#Top` under `VERIFICATION-FULL`; see
[spec-final-return-body-mutation.k](evidence/spec-final-return-body-mutation.k)
and [41_final_return_body_mutation_still_proves.log](evidence/41_final_return_body_mutation_still_proves.log).
At empty input the formal target is empty while the exact mutated program
returns `x`. The outer bridge fires at the unchanged loop head and its inserted
`Return` discards the mutated real return statement. This is a direct Gate A1
failure and demonstrates material reliance on the unsound rule.

A preliminary symbolic counterexample allowed unrelated symbolic continuations
and explored into an unsupported Haskell float hook
([29_helper_base_false_rejects.log](evidence/29_helper_base_false_rejects.log));
it is not used as evidence. The concrete witnesses remove that branch and fail
or close for exactly the expected return-value obligation. One parallel Java
run also suffered a SIGBUS
([34_helper_base_true_concrete_proves.log](evidence/34_helper_base_true_concrete_proves.log));
the identical command was rerun alone and succeeded in `34b`. Neither
infrastructure event contributes to the verdict.

## 6. Fresh non-vacuity test

The candidate's `spec-vacuity.k` was inspected only as untrusted evidence. The
reviewer generated a distinct mutation: prefix ASCII code 63 (`?`) to the
required entry result while retaining the original program and
`asciiCodes(CODES)` precondition. The empty input is a satisfying witness; the
real result is empty and the mutated required result is `"?"`.

The generated mutation is
[spec-fresh-vacuity.k](evidence/spec-fresh-vacuity.k), produced by
[make_false_mutation.py](evidence/make_false_mutation.py). Its dry run compiled
successfully and exited 0; see
[26_false_mutation_dry_run.log](evidence/26_false_mutation_dry_run.log). The
actual proof exited 1 with `WarnStuckClaimState`, not a parser error or crash.
The residual is the expected unmet equality

```text
antiFinish(.IntSeq,.IntSeq,CODES)
== iCons(63,antiFinish(.IntSeq,.IntSeq,CODES))
```

See [27_false_mutation_proof.log](evidence/27_false_mutation_proof.log). The
entry postcondition is therefore result-constraining and non-vacuous. This
successful negative test cannot repair the false operational axioms exposed in
Stage 5.

## 7. Proven versus assumed accounting

### What the successful runs establish

- `SPEC-HELPER.insert-loop` closes against fixed supplied semantics plus the
  audited equations but no operational bridge. Subject to the K toolchain and
  the two sound simplification lemmas, it genuinely characterizes the exact
  displayed helper loop followed by its displayed real return.
- `SPEC.anti-loop` closes only after adding the false helper bridge. Its `#Top`
  establishes closure under that extended theory, not a sound theorem of the
  fixed semantics.
- `SPEC-ENTRY.anti-shuffle` closes only after adding both false bridges. It
  syntactically constrains the ASCII result to `antiFinish`, but because the
  proof accepts a translated body that actually returns `x` while retaining
  the empty target, this closure is not a legitimate partial-correctness proof
  of program execution.
- No K claim proves that `antiFinish` denotes a sorted permutation of each
  space-separated word. That meaning follows by an informal structural
  induction: `insertFinish` inserts before the first greater character, and
  `antiFinish` folds it within each literal-space-delimited word. Differential
  evidence supports this bridge on 25,409 cases. If Gate A were sound, this
  informal but straightforward intent bridge and the ASCII restriction would
  be documented limitations rather than a legitimacy failure.

### Trust and assumption ledger

1. **Supplied MPY semantics.** The unchanged 707-rule tree is the fixed
   semantics selected by the problem. This is an acceptable problem-level
   trust boundary, confirmed byte-for-byte. The target reaches only module and
   statement sequencing, scopes/maps, string values and iteration, assignment,
   conditionals, calls/returns, string operators, and positive-step slicing.
2. **K engine, SMT solver, and hooks.** `kompile`, LLVM/Haskell execution,
   `kprove`, SMT reasoning over integers/Booleans, and builtin Map/List/String
   operations are ordinary machine-checking trust. Used hooks include integer
   arithmetic/comparison, Boolean connectives, map lookup/update/deletion, and
   ASCII literal conversion (`lengthString`, `substrString`, `ordChar`).
3. **Unused supplied opaque primitives.** The inventory identifies all 22
   `no-evaluators` symbols: `md5hexCodes`; `intFloatDiv`, `divII`, `floatMod`,
   `floatLt`, `absF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
   `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
   `sqrtF`; and `sortVS`, `sortKeyVS`. The symbolic-total `floorFI`, `toF`, and
   `ceilF` symbols are also unused. None can affect target control or result.
   In particular, the proof does not call the supplied opaque `sorted` model.
4. **Proof-local equations.** Map deletion, the exact tail-slice lemma,
   `insertFinish`, `antiFinish`, and `asciiCodes` are trusted additions to the
   proof theory rather than separately proved K theorems. Their guards,
   coverage, overlap, descent, and concrete substitutions were audited and are
   acceptable.
5. **Operational bridges.** The helper and outer bridges are illegitimate
   trusted axioms. They affect control and the final returned value, are broader
   than their alleged justifying claims, enable the concrete false conclusions
   above, and are essential to the two higher proof layers.
6. **Python-to-canonical and summary-to-intent bridges.** Trusted-translation
   byte identity is exact. Python/canonical equivalence and Unicode behavior
   have only finite differential support. The sorted-permutation interpretation
   of `antiFinish` is an informal mathematical induction. Neither testing nor
   prose substitutes for the K execution connection, and neither is used to
   excuse the false operational rules.
7. **Domain.** The formal entry theorem covers finite ASCII-code sequences
   only. The prompt says “ascii value,” making this a plausible formalization,
   but Python and the canonical implementation also operate on Unicode. The
   audit's Unicode tests found no implementation divergence; Unicode remains
   outside the K theorem.

Gate A fails because the proof extensions are materially unsound and because a
material exact-body mutation does not invalidate the target proof. Gate B also
has the documented ASCII and informal-summary limitations. Gate C evidence is
reproducible, but strong evidence cannot validate a proof theory that admits
the demonstrated false conclusions. Under the required decision boundary this
is `FAIL / NOT_LEGIT`, even though the submitted Python program appears correct
and every original positive `kprove` command prints `#Top`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
