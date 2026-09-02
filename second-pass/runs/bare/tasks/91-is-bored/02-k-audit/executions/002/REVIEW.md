# Independent adversarial review: 91-is-bored

The candidate does not contain a legitimate proof of the HumanEval contract.
Fresh reconstruction confirms a real but much narrower fact: its translated
program produces the asserted result on eight fixed strings. It contains no
symbolic entry claim over arbitrary input strings. Moreover, the submitted
Python implementation is not extensionally equal to the trusted canonical
implementation; the independent differential test found 2,339 mismatches in
39,560 cases. The generated semantics also has an over-broad, globally false
function-entry rule, with a concrete false-conclusion witness.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `91-is-bored`, condition `bare`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = GENERATED_SEMANTICS`;
- complete input provenance; and
- no mounted reference-semantics tree.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, every required
legacy-selected-stage1 generation record, the present `usage.json`, all 6,863
lines of `codex-output.log`, and all 157 structured JSONL trace records.
Historical `runtime-metrics.json` is absent, but is not required for this
legacy-selected-stage1 layout. The complete record parse and bounded trace/log
summary are in
[16-generation-record-audit.log](/audit-output/evidence/logs/16-generation-record-audit.log).

All required mounts and records are readable real files/directories. There are
no symlinks or unsupported nodes under `/candidate`, `/generation-evidence`,
or `/reference`. All launcher-declared file hashes match independently
computed SHA-256 values, including the campaign lock, run/task/result records,
invocation, metrics, prompt, usage, output log, last message, trusted sources,
and the individual trace JSONL. The campaign-lock JSON exactly equals the
`audit_campaign` block, and its hash is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.

The independently recomputed pipeline tree digest of the mounted candidate is
`8ac0126223c06a58e4d7d2707d2a3a8f619c842edb4e6b669159e122abf69fdd`,
exactly the stage-1 output/retained-workspace digest. The trace tree digest is
`ca26171efc3a23b7ce9feae3413132362442b8068658563ebd4cdf93b23e49b1`,
exactly `usage.json`'s source-trace digest. The audit input also records
launcher-level aggregate tree hashes using an unspecified serialization; the
independent checks above use the pipeline's documented tree algorithm and
file-level hashes rather than assuming that opaque aggregation convention.
See
[provenance_check.py](/audit-output/evidence/provenance_check.py) and
[01-provenance-check.log](/audit-output/evidence/logs/01-provenance-check.log).
The cross-record and file-level matches establish that the mounted evidence is
the recorded stage-1 evidence; there is no infrastructure breach.

`/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to the
trusted `/reference/prompt.py` and `/reference/py2mpy.py`. As required in
generated-semantics mode, `/reference/reference-semantics` does not exist. I
did not search for or use a hidden reference semantics.

The generation trace is treated only as an untrusted historical claim. It is
not proof evidence. Of note, it records that the generator created a universal
`S:String` claim, received `WarnStuckClaimState`, then deleted it and retained
only concrete claims. That history agrees with, but is not needed for, the
independent scope finding below. It also shows that the reported “10,000
randomized differential” oracle used
`part.strip().startswith("I ")`, which restated the submitted algorithm rather
than importing the trusted canonical implementation.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The prompt accepts a string `S` with no size bound or other precondition. A
“boredom” is a sentence beginning with the word `I`; sentences are delimited
by `.`, `?`, or `!`. The trusted canonical makes this precise by splitting at
`[.?!]\s*` and counting segments whose first two characters equal `"I "`.
Thus the intended theorem domain is arbitrary Python strings, not eight
examples or a bounded finite set.

The candidate instead normalizes delimiters, splits on `.`, then applies
`sentence.strip().startswith("I ")`. This changes behavior:

- `"I "`: canonical `1`, candidate `0`, because `strip()` removes the space
  needed by `startswith("I ")`.
- `" I lead"`: canonical `0`, candidate `1`, because the candidate removes
  leading whitespace from the first sentence.
- Submitted claim 4's input
  `" I am here?You are there!  I agree"`: canonical `1`, candidate and claim
  `2`.
- Submitted claim 7's leading-tab input: canonical `1`, candidate and claim
  `2`.

The trusted translator regenerated `solution.mpy` byte-for-byte; both files
have SHA-256
`f1425ef9768862e9616ade04b4745aa99d678335a15a4bd8b3070ee499cc9fa6`.
See
[02-regenerate-mpy.log](/audit-output/evidence/logs/02-regenerate-mpy.log).

The independent differential script imports both trusted canonical and
submitted entry points from scratch copies. It covers both documented
examples, empty and delimiter-only strings, all `I`/space/whole-word branch
boundaries, all delimiters, whitespace boundaries, an exhaustive alphabet
through length six, and 20,000 seeded representative strings. It tested 39,560
inputs and found 2,339 mismatches. The deterministic generators and seed are
the preserved input set:
[differential_test.py](/audit-output/evidence/differential_test.py);
the exact command, exit 1, counts, and first 25 mismatches are in
[03-differential-test.log](/audit-output/evidence/logs/03-differential-test.log).

This is a material implementation/specification discrepancy on the intended
domain, not an alternate correct algorithm.

## 3. Clean proof reconstruction

I copied source artifacts only into `/tmp/audit-work/reconstruction`; I did
not copy or use the candidate's compiled definitions or caches.

Fresh concrete definition:

```text
kompile semantic.k --backend haskell --syntax-module MPY-SYNTAX \
  --main-module MPY --output-definition concrete-kompiled
```

This exited 0; see
[04-kompile-concrete.log](/audit-output/evidence/logs/04-kompile-concrete.log).
Fresh `krun` executions of the actual `solution.mpy` completed on both prompt
examples, empty input, `"I "`, and claim 4's boundary witness. They returned
`0`, `1`, `0`, `0`, and `2`, respectively; see logs
[05a](/audit-output/evidence/logs/05a-krun-example1.log),
[05b](/audit-output/evidence/logs/05b-krun-example2.log),
[05c](/audit-output/evidence/logs/05c-krun-empty.log),
[05d](/audit-output/evidence/logs/05d-krun-I-space.log), and
[05e](/audit-output/evidence/logs/05e-krun-claim4-witness.log).

A separate 16-input generated-semantics differential run included normal,
empty, delimiter, whole-word, leading/trailing whitespace, newline, and
non-ASCII cases. K had zero mismatches against the submitted Python program
but four against the canonical. See
[semantics_differential.py](/audit-output/evidence/semantics_differential.py)
and
[12b-semantics-differential.log](/audit-output/evidence/logs/12b-semantics-differential.log).
This supports fidelity to the submitted rewrite on those cases; it does not
establish universal Python-semantic equivalence.

Fresh proof definition:

```text
kompile verification.k --backend haskell --syntax-module MPY-SYNTAX \
  --main-module VERIFICATION --output-definition verification-kompiled
```

This exited 0; see
[06-kompile-proof.log](/audit-output/evidence/logs/06-kompile-proof.log).
The original, unmodified positive command exited 0 and printed `#Top`:
[07-kprove-all-original.log](/audit-output/evidence/logs/07-kprove-all-original.log).

Because the candidate left its eight claims unlabeled, I made a
semantically identical labeled scratch copy and selected each claim
independently. All eight separate commands exited 0 and printed `#Top`.
The preserved derived file is
[spec-labeled.k](/audit-output/evidence/spec-labeled.k), with per-claim logs
[claim 1](/audit-output/evidence/logs/08-kprove-claim-1.log),
[claim 2](/audit-output/evidence/logs/08-kprove-claim-2.log),
[claim 3](/audit-output/evidence/logs/08-kprove-claim-3.log),
[claim 4](/audit-output/evidence/logs/08-kprove-claim-4.log),
[claim 5](/audit-output/evidence/logs/08-kprove-claim-5.log),
[claim 6](/audit-output/evidence/logs/08-kprove-claim-6.log),
[claim 7](/audit-output/evidence/logs/08-kprove-claim-7.log), and
[claim 8](/audit-output/evidence/logs/08-kprove-claim-8.log).

The positive reconstruction gate therefore passes for the candidate's actual
eight ground claims. It does not upgrade their scope.

## 4. Adequacy and real-program pinning

Each entry claim has no `requires` clause. Its precondition is the single exact
initial configuration consisting of:

- `<k> start </k>`;
- `<program> solutionModule </program>`;
- one fixed literal `<input>` string; and
- `<result> 0 </result>`.

Its postcondition requires `<k> done </k>`, preserves program and input, and
requires the result below:

| Claim | Fixed input description | Required result |
|---|---|---:|
| 1 | `"Hello world"` | 0 |
| 2 | second prompt example | 1 |
| 3 | four concrete sentences/all delimiters | 3 |
| 4 | concrete leading-whitespace string | 2 |
| 5 | concrete `It`/`Island`/`In`/`I ` boundary string | 1 |
| 6 | concrete repeated-delimiter string | 1 |
| 7 | concrete tab/newline/carriage-return string | 2 |
| 8 | `"I first! No. I second?"` | ground `boredSpec(...)`, which reduces to 2 |

Every precondition is satisfiable: the exact initial configuration itself is
a witness. There are no symbolic inputs, loop claims, helper claims, or
invariants. All iteration is concretely unrolled by big-step functions for the
eight literal strings.

For each claim I substituted its literal input into both Python
implementations and compared the formal result. All eight results match the
submitted implementation. Claims 4 and 7 do not match the trusted canonical.
See
[ground_claim_check.py](/audit-output/evidence/ground_claim_check.py) and
[09-ground-claim-check.log](/audit-output/evidence/logs/09-ground-claim-check.log).

Program pinning itself is adequate for these ground theorems:

1. trusted regeneration is byte-identical to submitted `solution.mpy`;
2. K parsed the regenerated file to an explicit constructor term; and
3. a source-derived configuration claim equating `solutionModule` to that
   term printed `#Top`.

Artifacts:
[generate_pin_check.py](/audit-output/evidence/generate_pin_check.py),
[pin-check.k](/audit-output/evidence/pin-check.k),
[10c parser log](/audit-output/evidence/logs/10c-kast-regenerated.log), and
[10g pin proof](/audit-output/evidence/logs/10g-kprove-pin-check-config.log).
The warning that the pin claim was trivial means the compiled function
normalized to that same constructor term; it is not a proof of the program's
contract.

Body sensitivity was tested inside the term actually executed by the claim,
not by changing an ignored external file. The scratch definition changed
`Assign(Name("count"), Int(0))` to `Int(1)` in `solutionModule`. It built
successfully; the `"Hello world"` claim then became stuck with final result
`1` instead of required `0`. See
[verification-body-mutated.k](/audit-output/evidence/verification-body-mutated.k),
[body-sensitivity.k](/audit-output/evidence/body-sensitivity.k),
[11a build](/audit-output/evidence/logs/11a-kompile-body-mutation.log), and
[11b failed proof](/audit-output/evidence/logs/11b-kprove-body-mutation.log).

The fatal adequacy gap is that eight singleton preconditions materially narrow
the unrestricted string domain. No finite set of concrete executions proves
the HumanEval function for arbitrary strings. Under the benchmark's explicit
decision rule, this narrowing is not merely a concern; it is not a legitimate
solution-contract proof.

## 5. Rule-by-rule static soundness review

The exhaustive declaration, constructor-coverage, and 86-rule inventory is
[rule-inventory.md](/audit-output/evidence/rule-inventory.md). The raw
declaration/rule/claim extraction is
[15-static-declaration-extract.log](/audit-output/evidence/logs/15-static-declaration-extract.log).
It covers every local syntax declaration, configuration cell, function,
ordinary rule, guarded equation, and `[owise]` priority fallback in
`semantic.k` and `verification.k`.

There are no candidate helper K files and no local `[total]`, `[functional]`,
`[simplification]`, `[concrete]`, numeric-priority, macro, anywhere, or opaque
declarations. All submitted constructors—module/function/parameters, statement
lists, assignment, for, if, augmented assignment, return, names/literals,
attributes, and the four string method-call shapes—map to explicit syntax and
rules.

For the exact submitted body, statement order, pure-expression evaluation,
loop target updates, branch choice, return propagation, and all observable
cells are preserved. Recursive definitions descend on list length, remaining
delimiters, or string length. Guarded pairs are disjoint or agree on overlap.
The whitespace literals are the Python 3.10 `str.strip` character set.
`solutionModule` is a definition of the source-derived constructor tree, not
an execution-bypassing summary. `boredSpec` is separately defined and appears
only as the ground expected value in claim 8; it does not preempt execution.
There is no candidate-local result oracle.

One semantics rule family is nevertheless globally false over its declared
match domain. Lines 51-58 accept any supported body but initialize the abstract
state as `state(INPUT, 0, "")`, thereby fabricating bindings for Python locals
that may be unbound. The required concrete false-conclusion witness is:

```python
def is_bored(S):
    return count
```

The trusted translator generates
`Module(FuncDef("is_bored", Params("S"), Return(Name("count"))))`. On intended
string input `"x"`, Python raises `NameError`; the generated K semantics
returns integer `0`. The exact artifacts and executions are
[uninitialized-count.py](/audit-output/evidence/uninitialized-count.py),
[uninitialized-count.mpy](/audit-output/evidence/uninitialized-count.mpy),
[14a translator check](/audit-output/evidence/logs/14a-unsound-witness-translate.log),
[14b Python witness](/audit-output/evidence/logs/14b-unsound-witness-python.log),
and
[14c K witness](/audit-output/evidence/logs/14c-unsound-witness-krun.log).
This is not labeled unsound merely because some behavior is unmodeled: it
produces a concrete false normal result for a term accepted by the rules.

The exact submitted body overwrites `count` before reading it, so that
over-broad rule does not by itself falsify the observed eight closures.
Nevertheless, the prompt requires globally false generated semantic rules to
be rejected rather than excused as off-path.

Finally, the prose calling `boredSpec` a contract model is not supported. Its
equations faithfully define the candidate's strip-based algorithm, but
`boredSpec("I ")` is 0 while the trusted canonical result is 1. I classify this
as a summary-to-intent failure, not as an inconsistent equation for the fresh
symbol.

## 6. Fresh non-vacuity test

I created a distinct result mutation for the satisfiable second-example
configuration. The actual submitted result is 1; the mutated destination
requires 2. This changes the result-constraining obligation and leaves program
execution unchanged.

The mutation is
[spec-vacuity-audit.k](/audit-output/evidence/spec-vacuity-audit.k).
Its `kprove --dry-run` exited 0, establishing successful parsing/spec
construction:
[13a-vacuity-dry-run.log](/audit-output/evidence/logs/13a-vacuity-dry-run.log).
The real proof exited 1 with `WarnStuckClaimState` and a final `<result> 1
</result>` that could not unify with the mutated destination:
[13b-vacuity-proof.log](/audit-output/evidence/logs/13b-vacuity-proof.log).

This is valid non-vacuity evidence for the eight concrete claims. It does not
supply the missing universal theorem.

## 7. Proven versus assumed accounting

### Machine-checked result

Conditional on the freshly compiled candidate theory and K toolchain, the
reachability proof establishes exactly this: starting from each of eight
literal initial configurations, execution of the source-pinned submitted
constructor term reaches `done` with its asserted literal result. All eight
claims are result-constraining and non-vacuous.

It does **not** establish:

- correctness for an arbitrary `S:String`;
- equivalence of the submitted Python implementation to the trusted
  canonical;
- that `boredSpec` denotes the HumanEval contract;
- a loop invariant or inductive statement over an arbitrary sentence list; or
- universal equivalence of the generated semantics to Python.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 compiler, parser, Haskell backend, and reachability engine | all builds/proofs | Normal unavoidable toolchain trust. Version was independently checked. |
| Trusted CPython AST translator | source-to-`solution.mpy` bridge | Benchmark-trusted input; byte regeneration proves artifact identity, not translator semantic correctness. |
| K `STRING`, `INT`, and `BOOL` primitives (`replaceAll`, `findString`, `substrString`, `lengthString`, equality, arithmetic, Boolean operations) | string processing and all results | Acceptable low-level fixed-toolchain boundary; 16 fresh cases provide finite support only. |
| Candidate big-step Python subset semantics | relation between `solution.mpy` and submitted Python | Generated rather than supplied. Exact used-path review and finite comparison support it, but the entry-state rule is globally false as witnessed above. |
| `solutionModule` | every positive claim | Mechanically pinned to trusted regeneration; acceptable for this immutable candidate. |
| `boredSpec`, `countBored`, `boolInt` | only claim 8's ground destination | Fully defined fresh functions, not opaque; they model the wrong strip-based contract and have no universal execution connection theorem. |
| Independent Python differential testing | implementation-to-canonical comparison | Finite but decisive for refutation because one mismatch suffices; it is not used as a proof substitute. |
| Fresh K/Python concrete comparison | used-path semantic bridge | Finite evidence only; zero K/candidate mismatches on 16 cases. |

There are no candidate-local opaque symbols or empirical values injected into
the result. The proof's failure is more basic: its formal domain is eight fixed
examples, the submitted implementation disagrees with the trusted canonical
on ordinary boundary inputs, and the generated language includes a witnessed
false entry-state behavior. A successful `#Top` for the eight claims cannot
overcome those defects.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
