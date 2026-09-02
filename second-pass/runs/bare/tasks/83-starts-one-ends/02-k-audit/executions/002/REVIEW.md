# Independent adversarial review: 83-starts-one-ends

Audit status: completed. The candidate is legitimate, with non-fatal concerns
about an over-broad off-path semantic rule, an informal intent bridge, and two
launcher aggregate hashes whose serialization could not be reproduced. Neither
semantic limitation can change the target theorem for the submitted program.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, condition `bare`, and
`semantics_mode = GENERATED_SEMANTICS`. I used only its `container_paths`
mounts, not the host provenance paths.

All required records are present, readable real files, not symlinks:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and the structured trace. The optional
`usage.json` is present and was inspected. The one JSONL trace has 141 valid
JSON records and no malformed line. The generation transcript and final report
were treated only as untrusted historical claims; bounded excerpts are in
[02-generation-record-inspection.log](/audit-output/evidence/02-generation-record-inspection.log).

The campaign object in `/audit-input.json` is exactly equal to
`/audit-campaign-lock.json`, whose observed SHA-256 is the recorded
`ad5dfcc0...a78d745`. Every recorded regular-file hash independently checked
in [01-provenance-check.log](/audit-output/evidence/01-provenance-check.log)
matches: the campaign lock, trusted canonical/prompt/translator, candidate
prompt/translator, run/task/result/invocation/metrics/usage records, prompt,
Codex output, and Codex last message. Candidate `prompt.py` and `py2mpy.py` are
byte-identical to their trusted mounts.

The generated-semantics boundary is consistent: neither
`/reference/reference-semantics` nor `/candidate/reference-semantics` exists.
No hidden or inferred reference semantics was used. The candidate and trace
trees contain only real directories and regular files. A full per-file digest
manifest is preserved in
[16-tree-file-manifest.log](/audit-output/evidence/16-tree-file-manifest.log).

There is one provenance limitation. The independently implemented canonical
pipeline tree serialization gives:

- candidate tree:
  `4cf9af2b4cdea83d5b9a9f604765245f229cf11af575ad7ceb29359eaf42025b`;
- trace tree:
  `364aa8909e658d65095d1b7f9c7513409bc1a1df0ad6229abfb379f3f674efb2`.

Those are respectively identical to all four workspace hashes in
`generation-result.json`/`invocation.json` and the
`usage.json.source_trace_sha256` value. However, the two launcher-only fields
`audit-input.hashes.candidate_tree_sha256` and
`generation_codex_trace_sha256` contain different values (`2ab48a...` and
`a803f2...`). The audit-input schema does not state an alternate tree
serialization. Because every mounted record is present/readable, every
regular-file hash checks, and the actual trees exactly match the generation
records' source-tree hashes, this is an evidence-format limitation rather than
evidence that a mounted artifact changed. The independent implementation is
[reviewer_tree_hash.py](/audit-output/evidence/reviewer_tree_hash.py).

The intact candidate mount contains every required proof artifact:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
executable `prove.sh`. Candidate caches, `proof-output.txt`, and historical
compiled claims were not used.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: for a positive integer `n`, return how many positive
`n`-digit decimal integers start with digit 1 or end with digit 1. There are no
documented examples. For `n=1`, only the integer 1 qualifies. For `n>1`,
inclusion-exclusion gives
`10^(n-1) + 9*10^(n-2) - 10^(n-2) = 18*10^(n-2)`.

The trusted [canonical.py](/reference/canonical.py) returns 1 at `n=1` and
`18 * 10 ** (n-2)` otherwise. The candidate
[solution.py](/candidate/solution.py) implements the same branch and formula;
the explicit `else` does not change behavior.

From the scratch copy, this exact command used the trusted translator:

```text
python3 trusted/py2mpy.py candidate/solution.py > regenerated.mpy
```

It exited 0. `cmp candidate/solution.mpy regenerated.mpy` exited 0, and both
files have SHA-256
`64dfaaf494cf54e3dd5732d844c926ef4b8e3ec55559d344e397efe7889d9ea2`.

The reviewer-authored
[differential_test.py](/audit-output/evidence/differential_test.py) imported
the trusted and generated entry points independently. It checked 45
deterministic positive inputs spanning 1 through 116, including `1`, the
branch boundary `2`, small values, and larger representatives through 100.
There were zero result/type mismatches. An independent enumeration of every
positive `n`-digit integer for `n=1,2,3,4` also had zero mismatches against
both implementations. An empty input is inapplicable because the contract
takes one scalar positive integer. Exact inputs and results are in
[03-fidelity-differential.log](/audit-output/evidence/03-fidelity-differential.log).

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/83-review`; no candidate
definition, cache, or compiled output was copied. The observed toolchain was K
v7.1.293.

The generated semantics was rebuilt from `semantic.k`:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX --output-definition ../semantic-kompiled
```

It exited 0
([05-kompile-llvm.log](/audit-output/evidence/05-kompile-llvm.log)).
Fresh executions of the regenerated `solution.mpy` all exited 0:

| Input | K result | Python/canonical result |
|---:|---:|---:|
| 1 | 1 | 1 |
| 2 | 18 | 18 |
| 3 | 180 | 180 |
| 5 | 18000 | 18000 |
| 10 | 1800000000 | 1800000000 |

The complete configurations are in
[06-krun-concrete.log](/audit-output/evidence/06-krun-concrete.log). Across
these runs, every construct used by `solution.mpy` is exercised; inputs 1 and 2
exercise both branches.

The proof definition was independently rebuilt:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --output-definition ../verification-kompiled
```

It exited 0
([07-kompile-haskell.log](/audit-output/evidence/07-kompile-haskell.log)).
The aggregate target command

```text
kprove spec.k --definition ../verification-kompiled --spec-module SPEC
```

printed `#Top` and exited 0
([08-kprove-all.log](/audit-output/evidence/08-kprove-all.log)). Each claim was
also selected and run independently:

```text
kprove spec.k --definition ../verification-kompiled \
  --spec-module SPEC --claims SPEC.positive-n-one
kprove spec.k --definition ../verification-kompiled \
  --spec-module SPEC --claims SPEC.positive-n-gt-one
```

Each printed `#Top` and exited 0
([09-kprove-each.log](/audit-output/evidence/09-kprove-each.log)).

A supplementary attempt to state bare functional ground claims for
`qualifyingCount` was rejected before proof because this Haskell backend does
not support functional claims
([10-proof-function-ground.log](/audit-output/evidence/10-proof-function-ground.log)).
That experiment is not a target claim and supplies no positive or negative
evidence about the reconstructed reachability proofs.

## 4. Adequacy and real-program pinning

The two entry claims have these meanings:

1. `positive-n-one` starts with the literal submitted `Module(...)`, configured
   entry call `starts_one_ends(1)`, `noFunction`, empty environment, normal
   control, and no result. It requires termination with empty `<k>`, the exact
   function body registered, environment `n |-> 1`, normal control, and
   `result(qualifyingCount(1))`, which reduces to `result(1)`.
2. `positive-n-gt-one` has the same complete initial/final machine shape with
   symbolic integer `N` and precondition `N > 1`. It requires
   `result(qualifyingCount(N))`, whose guarded definitions reduce by
   inclusion-exclusion to `result(18 * 10^(N-2))`.

Both preconditions are satisfiable: `n=1` satisfies the first and `N=2`
satisfies the second. Substituting `N=2`, `3`, and `5` yields 18, 180, and
18000, matching both Python implementations and fresh K execution.

The reviewer-authored
[program_pinning_check.py](/audit-output/evidence/program_pinning_check.py)
lexically balances each `Module(...)` term and removes whitespace only outside
quoted strings. It found exactly two claim terms and both are constructor-level
identical to trusted-regenerated `solution.mpy`. Thus each `<k>` cell executes
the submitted binding and body; this is not merely a source-file comparison.
There are no loop/helper claims or substituted helpers.

Body sensitivity was checked separately. In
[spec-body-mutation.k](/audit-output/evidence/spec-body-mutation.k), the
executed then-branch and registered body both change from `Return(Int(1))` to
`Return(Int(2))`, while the original result obligation is retained. Its dry run
exited 0, then proof exited 1 with `WarnStuckClaimState` and the concrete
residual `result(2)`
([14-body-mutation-proof.log](/audit-output/evidence/14-body-mutation-proof.log)).
The theorem therefore depends on the executed body.

The postcondition is equality to a determined integer expression, not a free
variable, tautology, or one-way implication.

## 5. Rule-by-rule static soundness review

The exhaustive declaration/rule inventory is
[RULE-INVENTORY.md](/audit-output/evidence/RULE-INVENTORY.md); the lexical
source inventory is
[11-lexical-inventory.log](/audit-output/evidence/11-lexical-inventory.log).
It enumerates all syntax/configuration declarations, 18 `semantic.k` rules, 6
`verification.k` rules, and both claims. There are no local `total`,
`functional`, `simplification`, `opaque`, priority, or `owise` declarations.
The only relevant attributes are constructor `symbol` and pure `function`.

The operational rules execute:

- module/function registration and the selected binding;
- left-to-right statement sequencing;
- one argument environment;
- docstring expression statement;
- complementary `if` guards;
- return/control propagation;
- integer/name lookup, subtraction, multiplication, nonnegative exponentiation,
  and equality.

The `N>1` guard ensures the exponent `N-2` is nonnegative; `n=1` never evaluates
that branch. Python and K both use unbounded mathematical integers for all
material operations here. State changes are explicit in the function,
environment, control, and result cells. There is one call and no heap, I/O,
allocation, exception, or mutable object behavior in the submitted program.
Sequence/control overlaps are guard-disjoint, the if guards are complements,
and the expression equations are constructor/operator-disjoint.

`verification.k` contains no rule touching `<k>` and no operational bridge.
Its five count functions are guarded, nonrecursive definitional summaries:
10 choices per free digit, 9 choices for a nonzero leading digit, and
inclusion-exclusion. Their guards are disjoint/complete at every use.
No program-derived fresh or opaque value influences the result, and no
task answer is injected before program execution.

One rule is intentionally broader than justified:

```text
rule <k> Expr(_E) => .K ... </k>
```

For the only reachable instance, `Expr(Str(docstring))`, discarding the value
is exactly Python behavior. Globally, however, the rule would also discard an
expression that raises or has effects. The concrete reviewer witness
[expr-overbreadth.py](/audit-output/evidence/expr-overbreadth.py) uses
`Expr(Name("missing"))` at positive input 1: Python raises `NameError`, while
this K rule silently continues and returns 1
([15-expr-rule-overbreadth.log](/audit-output/evidence/15-expr-rule-overbreadth.log)).
That false behavior is for an altered program term, not the submitted term;
the rule cannot introduce such a term or apply to any non-string expression in
either entry proof. It therefore does not enable a false target conclusion,
but it is a real reuse/scope limitation and prevents an unqualified endorsement
of the generated semantics as a general Python-subset semantics.

No other false rule witness or rule gap affecting the submitted program was
found.

## 6. Fresh non-vacuity test

The fresh reviewer mutation
[spec-false-post.k](/audit-output/evidence/spec-false-post.k) executes the exact
submitted `n=1` program but changes the result obligation from 1 to
`qualifyingCount(1) + 1 = 2`. Input 1 satisfies its complete initial state and
the mutation is demonstrably false.

First,

```text
kprove spec-false-post.k --definition ../verification-kompiled \
  --spec-module SPEC-FALSE-POST --dry-run
```

exited 0 and emitted KORE, establishing that the mutation parses/builds
([12-mutation-dry-runs.log](/audit-output/evidence/12-mutation-dry-runs.log)).
The actual proof command then exited 1 with `WarnStuckClaimState`. Its residual
is the fully executed final state with `result(1)`, so the failure is exactly
the unmet result obligation, not a parser error, missing import, timeout,
unreachable mutation, or unrelated crash
([13-false-post-proof.log](/audit-output/evidence/13-false-post-proof.log)).

## 7. Proven versus assumed accounting

The successful reachability proofs establish, under the rebuilt generated
semantics, that executing the exact submitted function:

- reaches result 1 for input 1; and
- reaches `qualifyingCount(N) = 18 * 10^(N-2)` for every integer `N>1`,

with the exact registered function, argument environment, normal returned
control, and empty continuation stated in the claims. Together the claims cover
the full positive-integer source-contract domain. The false-post and body
mutations show that both the result and the executed body are material.

Trust/assumption ledger:

- **Trusted translator.** `/reference/py2mpy.py` is launcher-trusted; fresh
  translation is byte-identical to the submitted constructor term. Both claims
  mechanically contain that exact term.
- **Generated semantic correspondence.** The correspondence between these 18 K
  rules and Python is audited rather than proved in K. Fresh boundary execution
  and differential evidence support all reachable behavior. The only witnessed
  mismatch is the unreachable over-broad `Expr` instance described in stage 5.
- **K built-ins and toolchain.** Integer/map/Boolean operations (`+Int`,
  `-Int`, `*Int`, `^Int`, comparisons, map lookup), K rewriting, `kompile`, and
  `kprove` v7.1.293 are trusted. All exponent uses are within the nonnegative
  domain.
- **Counting-to-intent bridge.** The proof-local equations formalize the usual
  inclusion-exclusion arithmetic, but the theorem does not build and cardinality-
  count the set of decimal strings. The assertion that those guarded equations
  mean “numbers that start or end with 1” is an ordinary but informal
  combinatorial argument. Independent exhaustive enumeration through four
  digits and broader differential tests are finite support, not a universal
  replacement for the K proof.
- **No opacity/oracle.** There is no opaque symbol, unconstrained fresh value,
  totality axiom, proof-local operational rewrite, or unproved call/loop
  summary.
- **Provenance aggregation.** Individual files and generation source-tree
  hashes are reproducible; the two audit-input aggregate tree fields have an
  undocumented differing serialization as recorded in stage 1.

The proof is sound and result-constraining for the actual generated program and
does not narrow the HumanEval domain. The over-broad but unreachable expression
rule, informal intent bridge, and aggregate-hash auditability issue are
non-fatal concerns; none permits a false conclusion for the submitted program.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
