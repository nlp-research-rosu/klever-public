# Independent adversarial audit — 158-find-max

This audit reconstructed the submitted sources without using
`/candidate/verification-kompiled`, its caches, the generation log's prior
`#Top`, or the final agent report as authority.

## 1. Input and provenance integrity

The rendered mode is `GENERATED_SEMANTICS`. The required boundary is intact:
`/reference/reference-semantics` does not exist. There is therefore no mount or
mode contradiction and no infrastructure breach.

All artifacts named by the audit request are present as regular, non-symlink
files: `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, the JSONL generation trace, `prompt.py`, `py2mpy.py`,
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`. There are no additional candidate K source/helper files. The
candidate also contains a compiled definition and Python bytecode; these are
extra generated outputs, not source-integrity failures, and were ignored.
There is no candidate `PROOF.md` or `spec-vacuity.k`; neither was required by
the original generation prompt.

The candidate prompt is byte-identical to `/reference/prompt.py` (both SHA-256
`c40e718aa330b51ea3bb37b1532061de990739b868af73c34faa3af0512626c3`).
The translator is byte-identical to `/reference/py2mpy.py` (both SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
No required source artifact is missing, changed, mistyped, or symlinked.

The metadata and generation records were read only as claims. They report a
bare/generated-semantics run, exit 0, three successful concrete examples,
`#Top`, and 4,680 alleged differential cases. None of those claims was reused
as proof evidence. The structured trace has 272 valid JSONL records and ends
with the same untrusted success report.

Evidence:

- [`evidence/provenance_check.sh`](evidence/provenance_check.sh) and
  [`evidence/provenance_check.log`](evidence/provenance_check.log): artifact
  types, mount boundary, hashes, translator regeneration commands, and all exit
  statuses (final status 0).
- [`evidence/inspect_generation_claims.py`](evidence/inspect_generation_claims.py)
  and [`evidence/generation_claims.log`](evidence/generation_claims.log):
  bounded extraction of the untrusted run claims and trace structure (exit 0).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and domain

The trusted prompt asks `find_max(words)` to select the word with the greatest
number of distinct characters and, on a tie, the lexicographically smallest
word. “The list contains different words,” together with the trusted
canonical's indexing of the first sorted element, gives the intended domain:
a finite, nonempty list of pairwise-distinct Python strings. Python strings are
Unicode; the prompt states no ASCII-only restriction.

The trusted canonical computes:

```python
sorted(words, key=lambda x: (-len(set(x)), x))[0]
```

The candidate uses a left-to-right accumulator with `best_count = -1`, replaces
on a greater distinct-character count, and replaces on an equal count only for
a lexicographically smaller word. This is a valid alternative algorithm on the
intended domain.

### Exact translation

Running the trusted translator on the scratch copy of `solution.py` exited 0.
The regenerated and submitted `solution.mpy` files are byte-identical and both
have SHA-256
`65fdcbb262c7d5ed2d66958afb5f260004155a4467c8cc2241d68f914a49b1a8`.
The exact commands and comparison statuses are in
[`evidence/provenance_check.log`](evidence/provenance_check.log).

### Independent Python differential

[`evidence/differential_test.py`](evidence/differential_test.py) imports the
trusted canonical and generated solution through separate module objects. It
records every input and both outcomes in
[`evidence/differential-inputs.jsonl`](evidence/differential-inputs.jsonl)
(4,969 lines, SHA-256
`f2d4a86f3df1f8df1adb4d4342f3b7f0a59f5a451058b9ddedb156221bab0d6a`).
The run covered:

- all three documented examples;
- first-iteration replacement, greater/lower count, both equality/tie
  directions, singleton, empty-string, Unicode, empty-list, and duplicate-word
  boundaries;
- every ordered pairwise-distinct list of lengths 1–3 over all strings of
  lengths 0–3 on alphabet `{a,b}` (2,955 exhaustive cases);
- 2,000 seeded generated, pairwise-distinct lists of lengths 1–8 over ASCII,
  accented, combining-mark, and astral characters.

The command exited 0 with zero intended-domain mismatches. The empty-list
boundary is the sole recorded divergence: canonical Python raises
`IndexError`, while the generated function returns `""`. Empty input is
outside the implicit nonempty canonical domain, so this does not by itself
invalidate the implementation; it remains an explicit formal-domain
overextension.

Evidence: [`evidence/differential_test.log`](evidence/differential_test.log).

## 3. Clean proof reconstruction

All sources needed for execution were copied to `/tmp/audit-work/source`.
No candidate-built definition or cache was copied.

### Fresh builds

The following fresh builds used K v7.1.293:

```text
kompile --backend llvm /tmp/audit-work/source/semantic.k \
  --main-module SEMANTIC --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/reconstruction/semantics-kompiled \
  -I /tmp/audit-work/source

kompile --backend haskell /tmp/audit-work/source/verification.k \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition /tmp/audit-work/reconstruction/verification-kompiled \
  -I /tmp/audit-work/source
```

Both builds exited 0. The LLVM build warned that the `[total]`
`distinctCount` function has a non-exhaustive symbolic match. LLVM concrete
execution then exited 113 at `distinctCount("name")`; this backend-specific
failure is recorded but is not used as a candidate verdict. A separate fresh
Haskell concrete definition built directly from `semantic.k` exited 0 and
executed normally:

```text
kompile --backend haskell /tmp/audit-work/source/semantic.k \
  --main-module SEMANTIC --syntax-module MPY-SYNTAX \
  --output-definition \
    /tmp/audit-work/reconstruction/semantics-haskell-kompiled \
  -I /tmp/audit-work/source
```

Evidence:

- [`evidence/rebuild_definitions.sh`](evidence/rebuild_definitions.sh) and
  [`evidence/rebuild_definitions.log`](evidence/rebuild_definitions.log);
- [`evidence/llvm_concrete_probe.log`](evidence/llvm_concrete_probe.log);
- [`evidence/rebuild_concrete_haskell.sh`](evidence/rebuild_concrete_haskell.sh)
  and
  [`evidence/rebuild_concrete_haskell.log`](evidence/rebuild_concrete_haskell.log).

### Positive claims

The fresh aggregate proof command exited 0 and printed `#Top`:

```text
kprove /tmp/audit-work/source/spec.k \
  --definition /tmp/audit-work/reconstruction/verification-kompiled \
  --spec-module SPEC
```

The `loop-correct` and `program-initializes` labels also each exited 0 and
printed `#Top` when selected separately. Selecting `find-max-correct` alone
removes its loop lemma and does not close promptly; that diagnostic was
auditor-terminated and is not treated as a proof failure. To audit composition
without relying on the aggregate command, I first established `loop-correct`
separately, then retained it as the explicitly trusted, already-proved
dependency while selecting the end-to-end target:

```text
kprove /tmp/audit-work/source/spec.k \
  --definition /tmp/audit-work/reconstruction/verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-correct,SPEC.find-max-correct \
  --trusted SPEC.loop-correct
```

That command exited 0 and printed `#Top`. Thus all three positive reachability
obligations reconstruct under the candidate theory. This is verification under
that theory, not yet proof that the theory models Python.

Evidence:

- [`evidence/kprove_all_claims.log`](evidence/kprove_all_claims.log);
- [`evidence/kprove_loop-correct.log`](evidence/kprove_loop-correct.log);
- [`evidence/kprove_program-initializes.log`](evidence/kprove_program-initializes.log);
- [`evidence/kprove_find-max-correct.log`](evidence/kprove_find-max-correct.log)
  (bounded missing-lemma diagnostic);
- [`evidence/kprove_find-max-with-proved-loop.log`](evidence/kprove_find-max-with-proved-loop.log).

### Fresh generated-semantics execution

[`evidence/concrete_execution.py`](evidence/concrete_execution.py) ran the
submitted `solution.mpy` against the fresh Haskell definition built from
`semantic.k`, with expected results independently obtained from Python. Nine
normal/ASCII/boundary cases matched. Two valid Unicode cases did not, so the
script exited 1 with `k_python_mismatches=2`.

The decisive satisfying witness is:

```text
words = ["é", "e\u0301", "😀😀a"]
```

where the middle word consists of U+0065 followed by U+0301. Both trusted
canonical Python and generated Python return that middle word. Fresh K
execution instead records count 5 for `"😀😀a"` and returns `"😀😀a"`.
An even smaller value witness is `words = ["😀"]`: K records
`<bestCount> 4 </bestCount>`, while Python evaluates
`len(set("😀"))` to 1.

These are nonempty lists of strings; the three-word witness is pairwise
distinct. They are within the stated input domain. The discrepancy is a
candidate semantic-model failure, not a tool/container uncertainty.

Evidence:

- [`evidence/concrete-inputs.jsonl`](evidence/concrete-inputs.jsonl);
- [`evidence/concrete_execution.log`](evidence/concrete_execution.log);
- [`evidence/unicode_witness.log`](evidence/unicode_witness.log);
- [`evidence/unicode_single_emoji.log`](evidence/unicode_single_emoji.log).

## 4. Adequacy and real-program pinning

### Claim meanings

`loop-correct` has no explicit `requires`. In plain language: for any finite
remaining `Words` list and any current `(BEST, BESTCOUNT)` accumulator,
executing the real submitted loop body followed by the real return statement
returns the word obtained by folding `consider` over that remaining list.
Final local/work cells are existential, but `<result>` is fixed to the contract
fold's word.

`program-initializes` also has no explicit `requires`. From the displayed
initialized cells and any `WORDS`, executing `solutionAST` must perform the two
assignments and reach the real `loop("word", WORDS, solutionLoopBody)` with the
real return continuation. It is a control-flow/initialization lemma and does
not claim a final result.

`find-max-correct` has no explicit `requires`. From exact initialized cells and
any finite `WORDS`, executing `solutionAST` must consume `<k>` and set
`<result>` to exactly `result(strVal(findMaxSpec(WORDS)))`. The result is not a
free variable, tautology, or one-way implication. Warnings about unused
existential final locals do not weaken the constrained `<result>` cell.

### Program identity and satisfying states

`solutionAST` and `solutionLoopBody` are `[function]` names whose equations
expand constructor-for-constructor to the byte-regenerated `solution.mpy`.
They do not replace execution. Entry rule S01 extracts and runs `BODY`; all
assignments, loop iterations, comparisons, and return rules then execute.

[`evidence/pinning-witness.k`](evidence/pinning-witness.k) supplies satisfiable
ground states for every claim shape:

- loop state: `REST = ["ba","ab"]`, `BEST = ""`, `BESTCOUNT = -1`,
  returning `"ab"`;
- initialization state: literal submitted AST and
  `WORDS = ["name","enam","game"]`, reaching the exact loop head;
- end-to-end state: the same literal AST/input, returning `"enam"`.

The ground end-to-end and initialization claims spell out the literal
submitted AST rather than `solutionAST`. Their proof command exited 0 and
printed `#Top`; both Python implementations also return `"enam"`.
Evidence: [`evidence/pinning-witness.log`](evidence/pinning-witness.log) and the
Python differential record.

Real-program pinning is therefore structurally adequate. The fatal adequacy
failure is value semantics: substituting the equally satisfiable Unicode input
above into the universal result claim yields the K fold's `"😀😀a"`, while both
real Python implementations yield the decomposed `"e\u0301"`.

The universal formal domain also includes `nil` and specifies result `""`;
trusted canonical Python raises on an empty list. This overbreadth is secondary
to, and independent of, the valid-domain Unicode counterexample.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[`evidence/rule-inventory.md`](evidence/rule-inventory.md), backed by the
source/line extraction and hashes in
[`evidence/rule_inventory_extract.log`](evidence/rule_inventory_extract.log).
It enumerates:

- 23 grouped local syntax/configuration declarations (D01–D23);
- every one of 42 rules in `semantic.k` (S01–S42);
- every one of 9 rules in `verification.k` (V01–V09);
- all 3 claims (C01–C03);
- every local `function`, `total`, `concrete`, and `simplification`
  attribute.

There are no local `[functional]` declarations, priorities, `owise` rules,
macros, anywhere rules, fresh symbols, explicit opaque declarations, or other
helper K files.

### Construct coverage and control/state audit

Every constructor in `solution.mpy` maps to syntax and operational rules:
`Module`/`FuncDef`/`Params` to S01; statement juxtaposition to S03/S04;
assignments and all five names to S05–S16; unary minus to S17/S18; nested
`set`/`len` calls to S19–S21 and S37–S40; comparisons to S22–S26; conditionals
to S27–S29; `for` to S30–S33; and return to S34–S36.

The configuration has only cells that are used. Assignment RHSs, call
arguments, and comparison operands evaluate in the required order for this
side-effect-free program. Branch guards are disjoint/exhaustive over Bool.
Loop setup snapshots the immutable recursive input; each cons iteration writes
`word`, executes the exact body, and recurs. Return writes the observable result
from `noResult` and correctly discards the single function's pending
continuation. There is no heap or allocation in the program. Unsupported
unused constructs stop rather than fabricate behavior.

The `consider` rules V03–V05 have pairwise-disjoint, exhaustive guards. The
`maxCandidate` recursion structurally descends over finite `Words`.
`solutionAST` and `solutionLoopBody` are exact definitional aliases, not
operational bridges. No rule encodes a particular task answer or replaces the
loop with an oracle.

### Materially unsound result-bearing bridge

S21 maps the real source operation `len(set(S))` to `distinctCount(S)`.
S37–S40 implement that symbol by scanning K string positions with
`lengthString`, `substrString`, and `findString`. In the rebuilt semantics,
astral Python characters are scanned as their UTF-8 bytes: the one Python
character `"😀"` produces count 4. Consequently, this rule family enables the
false real-program conclusion documented in Stage 3.

This is the required concrete false-conclusion witness for the only rule family
labelled unsound:

```text
S = "😀"
K/S21+S37-S40: len(set(S)) model = 4
CPython:        len(set(S))       = 1

words = ["é", "e\u0301", "😀😀a"]
K observable result:       "😀😀a"
both Python observables:   "e\u0301"
```

The witness is reachable from the submitted AST under its exact initialized
entry configuration and changes the final return. This is not merely missing
evidence; it refutes the bridge over the prompt's unrestricted Python-string
domain.

`distinctCount` is declared `[function, total]`, but its defining rule is
`[concrete]`; the fresh compiler correctly warns that symbolic matching is
non-exhaustive. It therefore acts as a result-bearing opaque primitive during
symbolic proof. S42 supplies the true nonnegativity fact needed by the loop
proof, and both execution and `findMaxSpec` use the same symbol. The K theorem
is sound as a parametric theorem about this nonnegative K metric, but sharing
the symbol does not establish that it equals Python distinct-character count.
The concrete implementation was the proposed connection, and the witness
refutes it.

S38–S40 have disjoint/exhaustive guards and terminate from their reachable
index-0 domain; they consistently count distinct K bytes. They are not
internally inconsistent. Their illegitimacy is specifically their use to
justify S21 as Python character semantics. S41 (string-order irreflexivity) and
S42 (nonnegative count) are ordinary true simplifications. No additional rule
is labelled unsound without a witness.

## 6. Fresh non-vacuity test

No candidate mutation was trusted or present. The fresh auditor artifact
[`evidence/spec-vacuity.k`](evidence/spec-vacuity.k) uses the satisfiable
ground input `["a"]` and changes the result-constraining obligation to the
demonstrably false `result(strVal(""))`.

The `--dry-run` command parsed and built the mutation successfully, exiting 0:

```text
kprove /audit-output/evidence/spec-vacuity.k \
  --definition /tmp/audit-work/reconstruction/verification-kompiled \
  --spec-module SPEC-VACUITY -I /tmp/audit-work/source --dry-run
```

The real proof command exited 1 with `WarnStuckClaimState`. Its residual is the
fully executed submitted program state:

```text
<k> .K </k>
<words> cons("a", nil) </words>
<result> result(strVal("a")) </result>
```

This is the expected unmet result obligation, not a parser/import error,
timeout, unrelated crash, or unreachable mutation. The proof is
result-constraining and non-vacuous.

Evidence:
[`evidence/spec-vacuity-build.log`](evidence/spec-vacuity-build.log) and
[`evidence/spec-vacuity-proof.log`](evidence/spec-vacuity-proof.log).

Passing non-vacuity does not cure the unsound Python semantic bridge.

## 7. Proven versus assumed accounting

### What the successful reachability proof actually establishes

Under the submitted K theory, for every finite recursive K `Words` term, if the
submitted constructor AST terminates from the displayed initialized
configuration, it returns `findMaxSpec(WORDS)`. That function folds the input
left-to-right, preferring a larger value of the K symbol `distinctCount` and
breaking equal-metric ties with K string order. The separately proved loop
claim is the induction/circularity, and `program-initializes` connects the exact
AST to its loop head.

This is a sound, non-vacuous theorem about the generated K language as written.
It is not a partial-correctness theorem of the real Python program on the
natural contract's full string domain.

### Trust ledger

| Boundary | Dependents | Accounting |
|---|---|---|
| K engine, reachability logic, and built-in Bool/Int operations | All builds/proofs | Ordinary external tool trust; acceptable. |
| K `String`, `lengthString`, `substrString`, `findString`, and `<String` primitives | S26, S37–S41, every result-bearing claim | Acceptable as K primitives, but they require a valid representation bridge to CPython Unicode. That bridge is not interpretation-parametric and is concretely false for S21/S37–S40. |
| Trusted `py2mpy.py` transliteration | Program identity | Acceptable; independently regenerated byte-identical `solution.mpy`. |
| V01/V02 manual names for body/AST | All claims | Acceptable; exact source comparison plus literal-AST ground execution pins the real submission. |
| `distinctCount` as symbolic opaque/total result | Loop branches, V03–V09, C01/C03 | Concerning in isolation but potentially acceptable as an external `set`/`len` primitive if its Python contract were stated and validated. Here the proposed concrete bridge is refuted, so this boundary is illegitimate for the claimed theorem. |
| S42 nonnegativity simplifier | First-iteration/guard reasoning | True for set cardinality and concrete byte count; acceptable ordinary mathematics, but it fixes only sign, not the missing value equivalence. |
| V03–V09 fold means “maximum unique characters with lexical tie-break” | Natural-language intent | The fold/max correspondence is an informal mathematical induction, not a separate K theorem. Its control logic is correct for any nonnegative metric. It cannot repair the false identification of that metric with Python character count. |
| K `Words`/`String` terms represent Python lists/strings | Natural-language bridge | Transparent for finite list shape and supported ASCII tests. Illegitimate as a universal Python-string bridge because the Unicode witness changes the result. |
| Differential evidence | Implementation-to-canonical bridge only | 4,969 finite Python/Python cases support the generated Python algorithm, not the K semantic abstraction. It is not substituted for the K proof. |

The candidate therefore proves a generic maximum-by-K-byte-metric program,
not the required Python maximum-by-unique-Unicode-character program. The
failure is material, result-observable, and occurs on a satisfying intended
input. Clean `#Top`, exact AST pinning, and a good mutation test cannot make
that theory a legitimate proof of the real generated program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
