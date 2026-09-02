# Independent adversarial review: 124-valid-date

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted `solution.mpy` under the supplied semantics. I independently
rebuilt both definitions, proved each entry claim separately, proved the
original combined spec, mechanically pinned the claim’s program term to trusted
regeneration, exhaustively inventoried the K theory, and rejected a fresh false
result mutation.

The concern is external to proof closure: the generated implementation and
proved postcondition follow the explicit `mm-dd-yyyy` prompt, but disagree with
the trusted HumanEval canonical implementation on 48 of 24,521 differential
inputs. Some disagreements are central well-formed cases such as
`01-31-2000`. Inspection shows that the canonical implementation’s
unparenthesized `and`/`or` conditions reject every day above 29, contrary to the
prompt. It also accepts whitespace, variable-width years, signed years, and
Unicode decimal digits that do not satisfy a strict reading of
`mm-dd-yyyy`. I therefore treat this as a non-fatal oracle/intent conflict,
not as a substituted-program or narrowed-domain proof.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, condition `semantics`, and
`semantics_mode = SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, so the rendered mode and
trusted mounts agree. No infrastructure-stop condition occurred.

I read and checked `/audit-input.json`, `/audit-campaign-lock.json`,
`/run.json`, `/task.json`, `/generation-result.json`, all required
legacy-selected-stage1 generation records, optional `usage.json`, and the
complete structured trace. Historical `runtime-metrics.json` is absent, which
is permitted for this record layout. The trace contains one declared JSONL
file with 296 parseable records.

Independent checks established:

- The campaign-lock JSON equals the `audit_campaign` block exactly, and its
  SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- Every required manifest and generation record is a real regular file, and
  the candidate, generation-trace, and trusted-semantics roots are real
  directories.
- Every directly recorded SHA-256 for the campaign lock, run/task/result
  manifests, invocation, metrics, usage, generation prompt/output/last,
  candidate prompt/translator, trusted prompt/translator, and canonical file
  matches.
- The declared trace-file set equals the mounted set; the JSONL digest is the
  declared
  `6e8e5f25f81b7512ea6bf5cac8342cd4e8a32bf10743b12446200ba8d4e66770`.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts.
- Recursive type/path/content inventories of candidate and trusted
  `reference-semantics/` are identical: 25 entries, no missing or additional
  entry, and no symlink or unsupported filesystem node. A direct
  `diff -qr --no-dereference` exits 0.
- No symlink or unsupported node exists anywhere below the candidate,
  reference, or generation-evidence mounts.

The generation report’s `#Top` and success marker were treated only as
untrusted claims. The replayable checks and hashes are in
[`evidence/01_integrity.log`](evidence/01_integrity.log), with reviewer code in
[`evidence/01_integrity.py`](evidence/01_integrity.py).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a string input, return `True` exactly when it is a nonempty ten-character
ASCII form `mm-dd-yyyy`, both separators are hyphens, the eight other
characters are decimal digits, the numeric month is 1–12, and the numeric day
is:

- 1–31 for months 1, 3, 5, 7, 8, 10, and 12;
- 1–30 for months 4, 6, 9, and 11;
- 1–29 for month 2.

The prompt supplies no year-range or leap-year condition.

`solution.py` checks length before indexing; checks separators; obtains all
eight character codes with `ord`; rejects non-ASCII digits; computes the month
and day; and returns the appropriate bound check. It has no loop or hidden
input precondition.

Trusted regeneration used:

```text
python3 trusted_py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
```

Both commands exited 0. The submitted and regenerated files have the same
SHA-256:
`4b8074c08ffd6d1bf22303e98c10e1c55db2d9b4d65f54cc2342f9989d26125e`.
See [`evidence/02_fidelity.log`](evidence/02_fidelity.log).

The independent differential script imports the trusted canonical and
generated functions and also evaluates a direct prompt oracle. Its 24,521
distinct inputs include all documented examples, empty and malformed strings,
lengths 0–14, every two-digit month/day pair for years `0000` and `2000`, all
month/day branch boundaries, whitespace, signs, Unicode digits, and 5,000
seed-124 generated strings over the recorded alphabet.

Results:

```text
generated_vs_prompt_mismatches=0
generated_vs_canonical_mismatches=48
```

The complete input ledger is
[`evidence/02_differential_inputs.tsv`](evidence/02_differential_inputs.tsv);
the executable test and bounded result are
[`evidence/02_differential.py`](evidence/02_differential.py) and
[`evidence/02_fidelity.log`](evidence/02_fidelity.log).

The canonical mismatches are material evidence, but they expose a conflict in
the trusted sources rather than a formal-domain restriction. For example, the
prompt and generated program return true for `01-31-2000`,
`04-30-2000`, and `12-31-2000`, while the canonical returns false. Because
Python binds `and` more tightly than `or`, the canonical’s last condition is
effectively `(month == 2 and day < 1) or day > 29`; consequently every date
with day 30 or 31 is rejected. Conversely, the canonical’s `strip`, `split`,
and `int` calls accept inputs such as `" 03-11-2000"`, `"3-1-2000"`, and
`"03-11-+2000"`, although these violate the explicit format. The formal
postcondition matches the explicit prompt and the generated program, not these
canonical implementation artifacts.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/124-valid-date`; no
candidate-compiled definition or cache was copied or used. The live tools were
K 7.1.293 and Python 3.10.12.

Fresh commands and results were:

| Purpose | Exact command summary | Exit/result |
|---|---|---|
| Concrete definition | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled` | 0 |
| Concrete boundary assertions | `krun 03_concrete_tests.mpy --definition audit-runtime-kompiled` | 0; final configuration has exit code 0 and no assertion failure |
| Proof definition | `kompile verification.k --backend haskell --main-module VALID-DATE-VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled` | 0 |
| Non-ten claim alone | `kprove spec-length-not-ten.k --definition audit-verification-kompiled --spec-module AUDIT-SPEC-LENGTH-NOT-TEN` | 0, `#Top` |
| Ten-code claim alone | `kprove spec-length-ten.k --definition audit-verification-kompiled --spec-module AUDIT-SPEC-LENGTH-TEN` | 0, `#Top` |
| Original combined spec | `kprove spec.k --definition audit-verification-kompiled --spec-module VALID-DATE-SPEC` | 0, `#Top` |

The bounded logs are
[`evidence/03a_kompile_llvm.log`](evidence/03a_kompile_llvm.log),
[`evidence/03c_krun_concrete.log`](evidence/03c_krun_concrete.log),
[`evidence/03d_kompile_haskell.log`](evidence/03d_kompile_haskell.log),
[`evidence/03e_kprove_length_not_ten.log`](evidence/03e_kprove_length_not_ten.log),
[`evidence/03f_kprove_length_ten.log`](evidence/03f_kprove_length_ten.log), and
[`evidence/03g_kprove_original_combined.log`](evidence/03g_kprove_original_combined.log).
All three positive proof logs contain one exact `#Top` and exit status 0.

Compiler warnings concern unused `strLt` variables and the supplied total
list-index helper. Neither sorting nor list indexing occurs in this program;
the used string-index helper is covered on all reachable calls as analyzed
below.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

1. Starting from the standard empty module configuration, load
   `validDateModule` and call `valid_date` on any `str(CS)` whose `IntSeq`
   length is not ten. The computation must finish with value `false`; module
   scope 0 must contain the exact `valid_date` closure; and environment, heap,
   stack, return, exception, and exit-code cells have the stated final values.
2. From the same initial configuration, load and call the function on any
   exactly ten-element `IntSeq`. The returned value must equal
   `validDate10(M0,...,Y3)`, with the same complete state constraints.

These shapes partition every finite `IntSeq`: the first has the explicit
precondition `isLen(CS) =/=Int 10`, and the second structurally names ten
arbitrary integers followed by `.IntSeq`. The formal domain is therefore all
strings in the selected model, not finitely many sizes or examples.

### Program identity

The mechanical pinning check:

- extracts the `FuncDef("valid_date", Params("date"), ...)` body from trusted
  regeneration;
- extracts the RHS of `validDateBody`;
- normalizes only the parser-equivalent empty-list spellings `, )` and
  `, .Stmts)`;
- proves the normalized bodies textually identical;
- verifies the exact equations
  `validDateClosure => closureVal("date", validDateBody, 0)` and
  `validDateModule => Module(FuncDef("valid_date", Params("date"),
  validDateBody))`; and
- verifies that `verification.k` contains zero operational `<k>` rules.

The check reports
`body_equal_after_empty_stmts_normalization=True`. It is recorded in
[`evidence/04_pinning.log`](evidence/04_pinning.log). This is a
constructor-level identity check, not a mutation of an external file while
leaving the theorem term unchanged.

Under the fixed semantics, `#loadAll` executes the exact `FuncDef`, which
installs that closure in scope 0. The generic call route looks up this binding,
evaluates the argument left-to-right, allocates a callee frame, binds `date`,
executes the body statements, handles `Return`, and pops/restores the caller.
No candidate rule intercepts those operations.

### Satisfiable states and ground substitutions

The standard empty module configuration in each claim is manifestly
constructible. Concrete substitutions include:

| Claim/input | Precondition | Claimed formula | Generated Python | Canonical Python |
|---|---:|---:|---:|---:|
| non-ten / `""` | true | false | false | false |
| ten / `02-29-2000` | true | true | true | true |
| ten / `04-31-2040` | true | false | false | false |
| ten / `01-31-2000` | true | true | true | false |

The last row is the already explained canonical/prompt conflict. The K
destination is a value equality, not a free RHS variable, implication, or
tautology. The mutation in stage 6 independently confirms result sensitivity.

There are no helper or loop reachability claims to mis-pin. The manually named
constructor constants are an artifact-maintenance risk for a future changed
source, but trusted regeneration plus the immutable-body comparison closes that
gap for this candidate.

## 5. Rule-by-rule static soundness review

I inventoried all source-level configurations, syntax declarations, evaluation
contexts, rules, functions, attributes, priorities, opaque declarations, and
claims in the 24 supplied K files plus `verification.k` and `spec.k`.
[`evidence/05_rule_inventory.tsv`](evidence/05_rule_inventory.tsv) contains
944 individually located and classified items:

```text
configuration: 1
syntax declarations: 234
evaluation contexts: 5
equational rules: 464
operational rules: 238
reachability claims: 2
function declarations: 152
total declarations: 116
opaque/no-evaluator declarations: 24
priority rules: 49
concrete rules: 36
simplification rules: 0
functional declarations: 0
```

Each row has a material-use flag and reviewer assessment. The full material
constructor/rule mapping and candidate-local decisions are in
[`evidence/05_static_review.md`](evidence/05_static_review.md).

### Candidate-local extensions

`verification.k` contributes seven single-equation total functions:
`validDateBody`, `validDateClosure`, `validDateModule`, `digitCode`,
`dateNumber`, `dateLimit`, and `validDate10`.

- The first three are exact constructor definitions for the submitted program;
  they do not replace execution.
- `digitCode` is exactly code range 48–57.
- `dateNumber` is the exact two-digit arithmetic used in the body.
- `dateLimit` is a total, non-overlapping nested conditional.
- `validDate10` is the conjunction of separator, digit, month, positive-day,
  and month-limit conditions.

All have one unguarded equation, so coverage is complete and pairwise overlap
does not arise. No local function is opaque. There is no local priority,
ordinary operational rule, simplification, lemma, or fresh result symbol. In
particular, the postcondition helper never rewrites a program expression and
there is no circular execution-oracle/postcondition dependency.

### Material fixed-semantics path

The used rules preserve:

- module binding and lexical lookup through the pinned scope chain;
- callee-before-argument and left-to-right argument evaluation;
- short-circuiting `or`;
- integer arithmetic and comparisons;
- length-before-index control flow;
- in-bounds string indexing and singleton-string `ord`;
- local assignments;
- strict guards and return expressions; and
- call-frame, scope, stack, return, exception, heap, and exit-code state.

For the non-ten branch, the first `If` returns before any subscript. For the
ten-code branch, all indices 0–9 are in bounds, so every call to the supplied
partial `intSeqAt` is covered, and `applyIndex(str, I)` always creates the
singleton required by `ord`. K unbounded integers accurately cover all
reachable code and arithmetic values. No allocation, exception, I/O, or
external state occurs.

The proof imports `MPY`, not the LLVM-only `MPY-CONCRETE`; thus concrete-only
sorting/equality rules cannot assist symbolic closure.

### Unused supplied-semantics limitations

The supplied semantics is intentionally a Python subset. The inventory marks
all unused rules and all 24 opaque primitives. None of the opaque sort, keyed
sort, MD5, or symbolic-float values can affect this program’s control or
postcondition.

One globally over-broad but unused fixed rule has a concrete false-behavior
witness: the supplied multi-character `int(str)` fold maps the code sequence
for `"ab"` to 540, whereas CPython raises `ValueError`. The supplied import
no-op approximation likewise differs from CPython on
`import definitely_missing`, which raises `ModuleNotFoundError`. These are
fixed-semantics fidelity gaps, not candidate proof rules, and neither symbol
can occur on the submitted program path. No unsoundness is alleged without
such a witness.

I found no task-reachable false rule, execution bypass, answer-encoding rule,
unconstrained result oracle, unmodeled material operation, overlap conflict, or
invalid totalization.

## 6. Fresh non-vacuity test

The fresh ground mutation in
`/tmp/audit-work/124-valid-date/spec-vacuity-audit.k` executes the exact module
on `02-29-2000`, for which the program, prompt formula, and canonical all
return true, but demands final result `false`.

Commands:

```text
kprove spec-vacuity-audit.k --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY --dry-run
# exit 0

kprove spec-vacuity-audit.k --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY
# exit 1, WarnStuckClaimState, no #Top
```

The residual contains `<k> true ~> .K </k>` and states that it cannot unify
with the destination. This is the expected unmet result obligation, not a
parser error, missing import, timeout, or unrelated crash. See
[`evidence/06a_mutation_dry_run.log`](evidence/06a_mutation_dry_run.log),
[`evidence/06b_mutation_proof.log`](evidence/06b_mutation_proof.log), and
[`evidence/06_mutation_summary.log`](evidence/06_mutation_summary.log).

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the supplied MPY semantics, for every finite code sequence `CS`:

- if `isLen(CS) != 10`, loading and calling the submitted `valid_date` body
  reaches Boolean `false`; and
- if `CS` has exactly ten elements
  `(M0,M1,SEP1,D0,D1,SEP2,Y0,Y1,Y2,Y3)`, the same execution reaches the
  Boolean conjunction:
  - `SEP1 = SEP2 = 45`;
  - all eight non-separator codes are in 48–57;
  - decoded month is 1–12;
  - decoded day is at least 1; and
  - decoded day is at most 29 for month 2, 30 for 4/6/9/11, and 31 otherwise.

The proof also constrains the observable modeled state cells in the claim. It
is a reachability/partial-correctness result. Differential tests and generation
logs are not substitutes for this theorem.

### Trust ledger

| Boundary | Dependence and assessment |
|---|---|
| K 7.1.293 compiler, Haskell backend, and builtin Int/Bool/Map/List theories | Necessary low-level proof checker and mathematical trust boundary; accepted. |
| Supplied MPY semantics | Integrity-checked unchanged. Its material load/call/control/string/int rules define the theorem and were statically reviewed. Unused subset/opaque gaps are documented and cannot contribute. |
| Trusted `py2mpy.py` | Trusted source-to-constructor translator. Byte-identical regeneration plus constructor comparison pins its output to the claim. |
| `IntSeq` as a Python-string code sequence | Informal execution-model bridge. The claim is over-broad (arbitrary integers) and therefore does not omit any modeled string; finite Python/K tests support reachable ordinary strings but are not a universal CPython theorem. |
| Prompt formula `validDate10` | Its arithmetic meaning is defined in K and proved equal to execution. Its correspondence to the English prompt is a direct informal reading, independently tested on 24,521 inputs. |
| Trusted canonical implementation | Conflicts with the explicit prompt on well-formed day-30/day-31 dates and accepts some malformed formats. This is the material non-fatal concern behind the verdict. |
| Termination and behavior outside string inputs | The report claims partial correctness for the prompt’s string domain. Non-string CPython calls and full-Python exception behavior are outside the theorem. |

Gate A (real-program soundness) passes: exact body, no bridge/oracle, satisfiable
preconditions, constrained result, and rejecting mutation. Gate B passes
against the explicit natural-language contract and covers the full string
domain, with the canonical conflict recorded rather than hidden. Gate C passes:
all commands, inputs, logs, inventories, and assumptions are reproducible;
[`evidence/07_evidence_manifest.log`](evidence/07_evidence_manifest.log)
records reviewer-evidence hashes.

The canonical/prompt inconsistency prevents an unqualified `PASS`, but it does
not invalidate the reconstructed theorem, substitute another body, narrow the
formal domain, or make a false prompt conclusion provable. The appropriate
benchmark decision is therefore legitimate with concerns.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
