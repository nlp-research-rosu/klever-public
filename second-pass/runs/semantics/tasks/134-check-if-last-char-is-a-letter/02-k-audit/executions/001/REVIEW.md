# Independent adversarial review

Problem: `134-check-if-last-char-is-a-letter`  
Rendered mode: `SUPPLIED_SEMANTICS`

## Executive decision

The candidate is **not a legitimate proof of the real submitted program**.
Fresh reconstruction does produce `#Top` for all six claims, and a fresh false
result mutation is correctly rejected. The local suffix lemmas are also
mathematically sound. Those positive facts do not overcome two material
failures:

1. `verification.k` never loads or invokes `solution.mpy`. It defines a new
   `#checkIfLastChar` term whose rule embeds a hand-copied closure. Replacing
   `solution.py` with unconditional `return True`, regenerating a radically
   different `solution.mpy`, and rebuilding the proof leaves all six original
   claims at `#Top`. Thus the theorem is not body-sensitive and is not pinned to
   the submitted artifact.
2. The actual Python program uses Unicode-aware `str.isalpha()`, while both the
   trusted canonical and the active supplied K rules use ASCII A–Z/a–z. For the
   satisfying input `"é"`, the formal claim proves `false` and the canonical
   returns `False`, but the submitted Python function returns `True`. This is a
   concrete false-conclusion witness for treating the K theorem as a theorem
   about the real generated program.

The detailed evidence is under
[`/audit-output/evidence/`](/audit-output/evidence/).

## Stage 1 — Input and provenance integrity

### Mode/mount gate

The rendered mode and trusted mounts are consistent:
`/reference/reference-semantics` is present. No infrastructure breach occurred,
so candidate verdict markers are appropriate.

The candidate supplied-semantics tree was compared recursively against the
trusted tree by relative path, entry type, symlink target, and SHA-256 content.
The manifests are identical. There are no candidate symlinks in that tree and
no missing, additional, mistyped, or changed semantics entries. Candidate
`prompt.py` and `py2mpy.py` are byte-identical to their trusted versions.
Evidence: [integrity script](/audit-output/evidence/integrity_audit.sh) and
[integrity log](/audit-output/evidence/01-integrity.log).

### Missing provenance artifacts

The following explicitly requested candidate artifacts are absent:

- `run-input.json`
- `metrics.json`
- `codex-last.txt`
- `codex-output.log`

No trace-like path, JSONL file, JSON file, or structured generation trace is
present. Because a structured trace was required only when present, its absence
is recorded but not treated as a mistyped trace. The four named provenance
files are missing-artifact failures. Candidate `PROOF.md` is also absent, though
the audit did not rely on candidate prose. The candidate `__pycache__` was
ignored and never copied as a proof definition or cache.

All source artifacts needed for execution were copied to
`/tmp/audit-work/candidate-src`; no candidate-built definition was used.
Evidence: [scratch-copy log](/audit-output/evidence/03-scratch-copy.log).

## Stage 2 — Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt asks for `True` exactly when the final character is
alphabetical and is a one-character final space-separated word; empty input,
a trailing space, or a multi-character final word must return `False`. The
trusted canonical makes “alphabetical” precise as ASCII A–Z/a–z:
`txt.split(" ")[-1]` must have length one and its lowercased ordinal must be
between 97 and 122.

The submitted implementation instead says:

- empty string: `False`;
- non-`isalpha()` final character: `False`;
- a one-character alphabetic string: `True`;
- otherwise: whether the penultimate character is a literal space.

This is equivalent on ASCII strings but uses Python's Unicode-aware
`str.isalpha()`.

### Trusted translation

Running the trusted `/reference/py2mpy.py` on the scratch copy of `solution.py`
exited 0. The regenerated MPY is byte-identical to submitted `solution.mpy`;
both have SHA-256
`9e03fdeff3da93d08bca16e915284912d738d1557badd000f682a8c690d61395`.
Evidence:
[translation log](/audit-output/evidence/04-translation-identity.log).

### Independent differential test

The reviewer-authored test imports the trusted canonical and scratch candidate
entry points independently. It covers all four examples, explicit witnesses for
every branch, Unicode boundaries, every length-zero-through-four string over an
eight-symbol alphabet, and 2,000 deterministic generated strings. Duplicate
inputs are removed. The exact scope is documented in
[differential_inputs.md](/audit-output/evidence/differential_inputs.md), and the
executable oracle is
[differential_test.py](/audit-output/evidence/differential_test.py).

The run compared 6,508 unique inputs and found 153 mismatches. The first are:

- `"é"`: canonical `False`, candidate `True`;
- `"Ω"`: canonical `False`, candidate `True`;
- `"中"`: canonical `False`, candidate `True`;
- the same non-ASCII letters following a literal space: canonical `False`,
  candidate `True`.

The documented examples and ASCII branch boundaries agree. Exit 1 reflects the
material mismatches, not an infrastructure error. Evidence:
[differential log](/audit-output/evidence/05-differential.log).

## Stage 3 — Clean proof reconstruction

K 7.1.337 was available independently at `/usr/bin`. From source-only scratch
copies:

- the concrete supplied semantics was compiled with LLVM, exit 0:
  [command/output](/audit-output/evidence/06-build-concrete.log);
- `verification.k` was compiled with the Haskell backend, exit 0:
  [command/output](/audit-output/evidence/07-build-proof.log);
- candidate concrete tests ran to an empty `<k>` with exit code cell 0:
  [command/output](/audit-output/evidence/08-concrete-candidate-tests.log);
- the original six-claim `spec.k` ran with exit 0 and printed `#Top`:
  [command/output](/audit-output/evidence/09-proof-all-original.log).

The original claims had no labels. A reviewer copy added labels and made no
other change; its exact diff is in
[the construction log](/audit-output/evidence/10-labeled-spec-construction.log)
and the artifact is
[spec-labeled.k](/audit-output/evidence/spec-labeled.k).
Every claim was then run independently:

| Claim | Final command evidence | Exit/result |
|---|---|---|
| empty | [11a](/audit-output/evidence/11a-proof-audit-empty.log) | 0, `#Top` |
| one ASCII alpha | [12a](/audit-output/evidence/12a-rerun-proof-audit-one-alpha.log) | 0, `#Top` |
| one non-alpha | [12b](/audit-output/evidence/12b-rerun-proof-audit-one-nonalpha.log) | 0, `#Top` |
| length ≥2, true branch | [11d](/audit-output/evidence/11d-proof-audit-long-true.log) | 0, `#Top` |
| length ≥2, last non-alpha | [11e](/audit-output/evidence/11e-proof-audit-long-last-nonalpha.log) | 0, `#Top` |
| length ≥2, previous non-space | [11f](/audit-output/evidence/11f-proof-audit-long-prev-nonspace.log) | 0, `#Top` |

Two initially concurrent commands suffered a Java-discovery race and backend
exit 137 respectively
([11b](/audit-output/evidence/11b-proof-audit-one-alpha.log),
[11c](/audit-output/evidence/11c-proof-audit-one-nonalpha.log)).
They are retained as infrastructure-attempt evidence and were not used against
the candidate. Their sequential reruns above both cleanly closed.

The clean reconstruction gate therefore passes as a statement about the theory
actually compiled.

## Stage 4 — Adequacy and real-program pinning

### Plain-language claims

All claims start with the same concrete, satisfiable cells: environment 0;
empty module scope 0 with parent -1; the supplied builtins scope at -1;
`scopeLoc=1`; empty heap and stack; `heapLoc=0`; `noRet`; `NoExc`; exit code 0.
They require the same cells at the destination and constrain the returned
`<k>` value exactly:

1. Empty code sequence returns `false`.
2. One character `C` returns `true` when supplied `isAlphaC(C)` holds.
3. One character `C` returns `false` when `isAlphaC(C)` does not hold.
4. A sequence `PREFIX ++ [PREV,LAST]` returns `true` when `LAST` is an
   ASCII letter and `PREV=32`.
5. The same length-at-least-two shape returns `false` when `LAST` is not an
   ASCII letter.
6. The same shape returns `false` when `LAST` is an ASCII letter and
   `PREV≠32`.

For finite `IntSeq`, `isLen(PREFIX) >= 0` is satisfiable and the cases partition
all empty, singleton, and length-at-least-two sequences. The returned Boolean
is neither fresh nor free, and the postconditions are exact equalities rather
than implications.

### Satisfying witnesses and substitutions

The six advertised witnesses are respectively `""`, `"a"`, `"7"`, `" a"`,
`"a!"`, and `"aa"`. Each satisfies its formal precondition, and its claimed
result agrees with both Python implementations. The exact substitutions are in
[claim_witnesses.py](/audit-output/evidence/claim_witnesses.py) and
[its run](/audit-output/evidence/15-claim-witnesses.log).

The same log also substitutes `"é"` (`C=233`) and `" é"`
(`PREV=32,LAST=233`). Those satisfy the formal non-alpha preconditions and
demand `false`. The canonical agrees, but the submitted Python implementation
returns `True` in both cases.

### The `<k>` cell does not execute the submitted program

Every entry begins with the synthetic term `#checkIfLastChar(V)`. Its local rule
constructs a closure containing copied AST text and calls it. The proof never
executes `Module(FuncDef(...))`, never creates/selects the named binding from
`solution.mpy`, and neither `verification.k` nor its build imports or reads
`solution.mpy`.

The embedded current body is textually consistent with the current MPY, but
that is only an informal/manual association. A body-sensitivity experiment
replaced `solution.py` with:

```python
def check_if_last_char_is_a_letter(txt):
    return True
```

The trusted translator produced a three-line, byte-different MPY. A fresh
Haskell proof definition was then built from that mutated scratch tree, and the
unchanged original six-claim spec still exited 0 with `#Top`.

Evidence:
[mutation diff/hashes](/audit-output/evidence/16b-body-mutation-artifact.log),
[mutant Python](/audit-output/evidence/solution-body-mutant.py),
[mutant MPY](/audit-output/evidence/solution-body-mutant.mpy),
[fresh build](/audit-output/evidence/16c-body-mutation-build-proof.log), and
[unchanged successful proof](/audit-output/evidence/16d-body-mutation-proof.log).

This fails real-program pinning and the required body-sensitivity check. It is
not a claim that the `#checkIfLastChar` rewrite is internally contradictory;
it is a missing connection theorem between that helper and the submitted
artifact.

## Stage 5 — Rule-by-rule static soundness review

The exhaustive line-located inventory is
[rule-inventory.txt](/audit-output/evidence/rule-inventory.txt), generated by
[inventory_rules.py](/audit-output/evidence/inventory_rules.py). It records
source hashes and exact blocks for all 26 K source files:

- 699 rules;
- 228 syntax declarations;
- 5 contexts;
- 1 configuration;
- 6 claims;
- 145 function declarations;
- all `total`, `symbol`, `no-evaluators`, priority, `owise`, concrete, strict,
  and simplification attributes.

There are no `[functional]` declarations. The complete per-file decision and
every proof-local extension assessment are in
[static-rule-assessment.md](/audit-output/evidence/static-rule-assessment.md).
That document assigns every rule/declaration to an active reviewed path or a
supplied-but-unreachable path; the latter cannot influence any target proof.

### Mapping the submitted constructs

The used AST constructors map to `semantics/syntax.k`. Their active execution
path is:

`#checkIfLastChar` → ordinary closure call and parameter bind → `If` condition
strictness → name/builtin lookup for `len` → string length → comparison/branch
→ negative string subscript normalization and in-bounds `intSeqAt` → bound
method dispatch for `isalpha` → exact `Return`/frame pop.

The final branch additionally evaluates the ASCII literal `" "` and string
equality. Argument evaluation is left-to-right. The function allocates no heap
objects. Call entry and pop restore the environment, scope store, scope
location, stack, and return cell required by the claim. The length tests ensure
`-1` is used only for a nonempty string and `-2` only for length at least two.

### Proof-local inventory

`verification.k` contains exactly one local syntax declaration and four rules:

1. The `#checkIfLastChar` harness rule. It executes the copied body under the
   ordinary semantics and preserves control/state through the normal call
   rules, but it has the material pinning gap proven in Stage 4.
2. `isLen(PREFIX ++ [A,B]) = isLen(PREFIX)+2`, marked
   `[simplification]`.
3. `intSeqAt(PREFIX ++ [A,B], isLen(PREFIX)) = A`, marked
   `[simplification]`.
4. `intSeqAt(PREFIX ++ [A,B], isLen(PREFIX)+1) = B`, marked
   `[simplification]`.

The three simplifications are true for every algebraic `IntSeq`: structural
induction on `PREFIX` reduces both concatenation and length/index, with base
cases `[A,B]` at indices 0 and 1. They terminate, have no false guarded case,
and have no overlap with a disagreeing right-hand side. They are valid derived
lemmas and are not task-answer oracles. There are no local total functions,
opaque values, priority rules, or result-bearing abstractions.

### Concrete active semantics false-conclusion witness

The supplied baseline was copied faithfully, but its active `isalpha` model is
not faithful to CPython over the actual input type. In
`semantics/methods.k`, `applyMethod(str(CS),"isalpha",.Vals)` reduces through
`allAlpha` and `isAlphaC`, where `isAlphaC(C)` is only
`65≤C≤90 or 97≤C≤122`.

For `C=233` (U+00E9):

- the formal ground claim returning `false` exits 0 with `#Top`:
  [18a](/audit-output/evidence/18a-unicode-formal-proof.log);
- the opposite formal result `true` fails with a final `false` residual:
  [18b](/audit-output/evidence/18b-unicode-opposite-proof.log);
- CPython evaluates `"é".isalpha()` and the submitted function to `True`:
  [15](/audit-output/evidence/15-claim-witnesses.log).

The witness artifact is
[spec-unicode-witness.k](/audit-output/evidence/spec-unicode-witness.k).
This is a false conclusion enabled by treating the ASCII supplied rule as the
real Python operation on the intended `str` domain. It is a language-model and
real-program soundness failure, not a semantics-tree integrity failure.

### Opaque and total boundaries

The only baseline functions with no local equation are `md5hexCodes` and
`sortKeyVS`. The proof-opaque sort and float symbols, along with all build
warnings about partial totality (`mapStrVS`, `floorFI`, `toF`, `ceilF`,
`joinCodes`, `valSeqAt`), are unreachable from this submitted program and from
all six claims. They cannot affect control, state, a branch, or the result here.
No hidden oracle contributes to closure.

## Stage 6 — Fresh non-vacuity test

No candidate `spec-vacuity.k` exists. The reviewer created a fresh, distinct
module changing the satisfiable empty-string obligation from `false` to
`true`: [spec-audit-vacuity.k](/audit-output/evidence/spec-audit-vacuity.k).
The concrete witness is the empty string, for which both Python implementations
return `False`.

The mutation parsed and generated KORE successfully under `kprove --dry-run`
with exit 0:
[dry-run log](/audit-output/evidence/19a-vacuity-dry-run.log).
The actual proof then exited 1 with `WarnStuckClaimState`; its residual contains
`false ~> .K` while the destination demands `true`:
[proof log](/audit-output/evidence/19b-vacuity-proof.log).

This is the expected unmet result obligation, not a parser error, missing
import, timeout, or unrelated crash. The formal theory is result-constraining
and non-vacuous. This stage passes.

## Stage 7 — Proven versus assumed accounting

### What the successful reachability proof actually establishes

Conditional on the supplied K definition plus the four local rules, the
synthetic operation `#checkIfLastChar` terminates for every finite `IntSeq` and
returns:

- `false` for empty;
- for length one, whether its integer code is an ASCII letter;
- for length at least two, whether the last integer code is an ASCII letter and
  the penultimate code is 32.

The listed configuration cells are restored to their initial values. This is a
machine-checked partial-correctness result about the synthetic helper under the
compiled theory.

It does **not** establish that:

- the submitted `solution.mpy` module was executed or its named function was
  selected;
- a changed submitted body would change or invalidate the theorem;
- the result equals the submitted CPython function for all Python strings;
- the submitted Python function equals the trusted canonical on its full
  domain;
- termination in CPython follows from the reachability proof.

### Trust ledger

| Boundary | Dependents | Accounting |
|---|---|---|
| K toolchain and builtin integer/Boolean/map/string hooks | all machine results | Ordinary foundational trust; fresh builds and exact versions are recorded. |
| Byte-identical supplied semantics | all execution claims | Correctly selected and integrity-checked. Its active ASCII `isalpha` abstraction is unacceptable as a bridge to the submitted Unicode-aware CPython operation without an ASCII-only precondition. |
| Local `#checkIfLastChar` → embedded closure association | all six claims | Illegitimate program-identity bridge: no source import/connection claim; body mutation is invisible to the proof. |
| Three suffix simplifications | length-at-least-two claims | Acceptable ordinary mathematics, valid by structural induction; no oracle or unconstrained value. |
| Opaque sort, float, and MD5 symbols | none | Inactive and harmless for this theorem. |
| Trusted translator byte comparison | source-to-MPY fidelity | Strong evidence that submitted MPY matches submitted Python, but it does not connect MPY to the synthetic proof helper. |
| Differential testing | intent/implementation bridge only | Finite evidence, not a proof. Here it positively disproves the universal candidate-versus-canonical bridge with 153 witnesses. |
| Manual observation that the current embedded closure matches current MPY | helper/source association | Informal and body-insensitive; insufficient for Gate A. |
| Finite `IntSeq` suffix decomposition | claim coverage | Acceptable algebraic reasoning: every length-at-least-two constructor sequence has a prefix and last two elements. |

### Gate accounting and verdict rationale

- Clean verification: **passes** for the compiled synthetic-helper theory.
- Result constraint/non-vacuity: **passes**.
- Proof-local suffix-rule soundness: **passes**.
- Real-program pinning/body sensitivity: **fails materially**.
- Real CPython value fidelity: **fails materially** with U+00E9 witnesses.
- Candidate-versus-canonical fidelity: **fails materially** with 153 observed
  divergences.
- Provenance completeness: **fails** because four named artifacts are absent.

A clean `#Top`, sound local lemmas, and a good mutation test cannot turn a
body-insensitive theorem about a substituted helper into a proof of the real
submitted program. The concrete Unicode witness additionally shows that the
formal conclusion is false for the submitted program on the intended string
domain. Under the stated decision boundary, these are `FAIL / NOT_LEGIT`
conditions.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
