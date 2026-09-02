# Independent adversarial review: HumanEval 97-multiply

The candidate contains a freshly reproducible, non-vacuous K reachability
proof of its own generated program. That program is not a correct
implementation of the trusted HumanEval canonical function over the stated
integer domain. The decisive witness is `a = -1, b = 1`: the candidate and its
K semantics return `1`, while `/reference/canonical.py` returns `9`.

This review followed the mounted `using-kit`, `writing-semantics`, and
`validating-proof` procedures. Candidate prose, logs, `kprove.out`, and the
generation trace were treated only as untrusted historical claims.

## 1. Input and provenance integrity

The launcher record declares:

- problem `97-multiply`;
- condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`;
- no mounted reference-semantics tree.

The generated-semantics boundary is consistent. `/reference` contains regular
files `canonical.py`, `prompt.py`, and `py2mpy.py`, and
`/reference/reference-semantics` is absent. I did not infer or use any hidden
semantics.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, all required
legacy-selected-stage1 generation records, the present `usage.json`,
`legacy-metrics.json`, `legacy-run-input.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and the 172-record structured JSONL trace.
Historical `runtime-metrics.json` is absent, but that record is not required
for `legacy-selected-stage1`.

The campaign lock is byte-hash correct and its parsed object exactly equals
the `audit_campaign` block in `/audit-input.json`. Every launcher-required
file/directory is present with the expected type, and no required artifact or
trace entry is a symlink. The candidate, reference, and provenance mounts are
read-only.

Independent SHA-256 checks match every declared per-file hash, including the
canonical source, trusted and candidate prompt/translator, run/task/result
manifests, invocation, metrics, usage, prompt, last message, output log, and
structured trace file. The candidate prompt and translator are byte-identical
to their trusted versions. The independently recomputed length-delimited
pipeline-v2 candidate-tree digest is
`3ea222492bf4a6c8bcbf958e01a52249f425ca43cb5e8ad08f20793fa03751cf`,
matching `generation-result.json`; the trace-tree digest is
`3d80dd8b4632f8217b550e5ec34339b2230ee9ce845860ddef2f751c7ee4a3c0`,
matching `usage.json`. `audit-input.json` also contains launcher snapshot
digests under a convention not declared in the record; I did not substitute
those for the independently reproducible pipeline digests.

The historical trace records an earlier `#Top`, six finite concrete checks,
and a final `KPROVE_PASSED` claim. None was used as proof evidence.

Evidence:

- [independent provenance checks](evidence/01-provenance.log)
- [structured-trace inventory](evidence/01-trace-inventory.log)
- [provenance checker](evidence/provenance_check.py)
- [trace inventory script](evidence/trace_inventory.py)

Stage 1 result: input and provenance gate intact; no audit-infrastructure
breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Trusted contract

`/reference/prompt.py:2-10` asks `multiply(a, b)` to take two integers and
return the product of their unit digits. It says inputs are valid and includes
the negative example `multiply(14, -15) == 20`; negative integers therefore
cannot be excluded.

The trusted executable interpretation in `/reference/canonical.py:6-16` is:

```python
return abs(a % 10) * abs(b % 10)
```

Python remainder with positive divisor `10` is nonnegative. Consequently the
canonical function returns `9` for `multiply(-1, 1)`.

### Submitted implementation and translation

`/candidate/solution.py:1-6` first negates each negative input and then returns:

```python
(a % 10) * (b % 10)
```

Thus its mathematical result is
`(abs(a) mod 10) * (abs(b) mod 10)`. For `(-1, 1)` it returns `1`, not the
trusted result `9`. The documented `-15` example happens to mask the
difference because both calculations yield digit `5`.

I regenerated the constructor term with the trusted translator:

```text
WORKDIR: /tmp/audit-work/reconstruction
COMMAND: bash -lc 'python3 py2mpy.py solution.py > regenerated-solution.mpy; ...'
EXIT_STATUS: 0
```

The regenerated and submitted `solution.mpy` files are byte-identical, both
with SHA-256
`d860df715e34cbe117902f177b536f6f8a92baf503ead76ad17158df9e1556a6`.

The independent differential test imported both trusted canonical and
generated entry points. It ran:

- all four documented examples;
- nine sign-branch boundaries around `-1, 0, 1`;
- 156 digit-boundary cross-product cases;
- three very large boundary pairs;
- 2,000 deterministic generated pairs over
  `[-10**100, 10**100]`.

There is no “empty” value for this integer-only signature. Across 2,172
inputs, canonical and generated results differed 1,126 times. A string-based
decimal-unit-digit oracle agreed with the candidate on all samples, which
explains the natural-language ambiguity, but it cannot override the trusted
canonical source. The test deliberately exits 1 on the material
canonical/generated divergence.

Evidence:

- [translation regeneration log](evidence/02-regeneration.log)
- [differential test and exact reproducible input scope](evidence/differential_test.py)
- [differential results](evidence/02-differential.log)

Stage 2 result: material program/contract fidelity failure on valid negative
integers.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/reconstruction`. Candidate
compiled definitions, caches, `kprove.out`, and trace claims were not copied or
used. The observed toolchain was K `v7.1.293` and Python `3.10.12`.

### Fresh generated-semantics build and execution

```text
WORKDIR: /tmp/audit-work/reconstruction
COMMAND: kompile semantic.k --backend llvm --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX --output-definition semantic-kompiled
EXIT_STATUS: 0
```

Twelve fresh `krun` executions cover normal examples, zero, both sign
boundaries, negative digit boundaries, and a large integer pair. Every run
exited 0. K had zero mismatches with the submitted Python implementation and
six mismatches with the canonical function. In particular:

```text
CASE a=-1 b=1 K=1 generated=1 canonical=9
CASE a=-1 b=-1 K=1 generated=1 canonical=81
```

This establishes that the generated semantics executes the submitted program
as written on the tested construct set; it also independently reproduces the
fidelity defect.

### Fresh proof build and every positive claim

`spec.k` contains one positive target claim.

```text
WORKDIR: /tmp/audit-work/reconstruction
COMMAND: kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
EXIT_STATUS: 0

COMMAND: kprove spec.k --definition verification-kompiled \
  --spec-module SPEC
OUTPUT: #Top
EXIT_STATUS: 0
```

Evidence:

- [toolchain log](evidence/03-toolchain.log)
- [fresh concrete-definition build](evidence/03-kompile-semantic.log)
- [fresh concrete executions](evidence/03-krun-concrete.log)
- [concrete comparison script](evidence/k_concrete_check.py)
- [fresh proof-definition build](evidence/03-kompile-verification.log)
- [fresh positive proof](evidence/03-kprove-spec.log)

Stage 3 result: the sole target claim genuinely reconstructs to exit 0 and
`#Top`; the generated semantics concretely matches the submitted implementation,
not the canonical implementation.

## 4. Adequacy and real-program pinning

### Claim in plain language

The claim at `/candidate/spec.k:9-19` has no semantic `requires` clause. Its
sorted input domain is every pair of mathematical K integers `A, B`.

The initial configuration has:

- `<k>` equal to `multiplyProgram ~> #invoke("multiply", A, B)`;
- empty `<env>` and `<functions>` maps;
- `<result>` equal to `noResult`.

The destination requires:

- all computation consumed (`.K`);
- final locals `a = absInt(A)` and `b = absInt(B)`;
- the exact `multiply` function binding and `multiplyBody`;
- result
  `unitDigit(A) *Int unitDigit(B)`, where
  `unitDigit(I) = absInt(I) %Int 10`.

This is an equivalence-strength, result-bearing destination cell rewrite, not
a free variable, tautology, or one-way implication.

### Program identity

I mechanically extracted the right-hand sides of the `multiplyProgram` and
`multiplyBody` rules from `verification.k`, substituted the body, and compared
the normalized constructor term to the trusted-regenerated `solution.mpy`.
Normalization removed only comments, whitespace, and explicit `.Stmts`
spellings for empty lists. Both normalized terms have SHA-256
`96eeac53bb2469e8bb167e3fc0e658aed6f4b8f607d2c411b03ba525451ce776`.
The claim therefore executes the actual submitted binding and body.

There is no automatic source-to-proof regeneration, which is a maintenance
observation rather than an identity failure for this immutable candidate.

### Satisfiability and ground substitutions

`A = -1, B = 1` with empty maps and `noResult` is a realizable state satisfying
the entry condition. Ground substitution gives:

| `A, B` | claimed result | generated Python | trusted canonical |
|---|---:|---:|---:|
| `148, 412` | 16 | 16 | 16 |
| `-1, 1` | 1 | 1 | 9 |
| `-1, -1` | 1 | 1 | 81 |
| `0, 0` | 0 | 0 | 0 |

The claim is adequate for the submitted body but not for the benchmark's
trusted result on its full integer domain.

### Body sensitivity

In a separate scratch definition I changed the term actually executed by the
claim from the translated multiplication return to `Return(Int(0))`, leaving
the destination unchanged. That definition compiled successfully (exit 0).
The proof then exited 1 with `WarnStuckClaimState` and the unmet equality
between `0` and the digit product. The theorem is sensitive to its program
body.

Evidence:

- [mechanical constructor comparison](evidence/04-term-pinning.log)
- [comparison script](evidence/term_pinning_check.py)
- [satisfying states and substitutions](evidence/04-claim-witnesses.log)
- [body mutation](evidence/04-verification-body-mutation.k)
- [body-mutation build](evidence/04-body-mutation-kompile.log)
- [body-mutation failed proof](evidence/04-body-mutation-kprove.log)

Stage 4 result: real-program pinning and formal result constraint pass; intent
adequacy fails on valid negative inputs.

## 5. Rule-by-rule static soundness review

The exhaustive inventory in
[evidence/05-rule-inventory.md](evidence/05-rule-inventory.md) enumerates:

- 27 local syntax/declaration entries (D01-D27);
- all four configuration cells;
- 22 explicit semantic rules (S01-S22);
- every generated strict evaluation context;
- three verification extensions (V01-V03);
- the sole target claim;
- every submitted constructor's declaration/rule mapping.

The source-level declaration extraction is preserved in
[evidence/05-source-declarations.log](evidence/05-source-declarations.log).
There are no candidate helper K files beyond the three audited K sources.

### Operational semantics

S01-S05 schedule the module and statements, store the exact function body, and
bind the two already-evaluated entry arguments. S06-S15 implement literals,
local lookup, unary minus, the used `%` and `*`, and the used `<` comparison.
S16-S22 implement guard evaluation, branch selection, assignment, and entry
return. Map, result, and function-cell footprints are explicit.

K `%Int` uses truncating remainder, unlike Python's negative modulo. This is
sound on every submitted execution because both inputs are made nonnegative
before the only modulo operations and the divisor is the positive literal
`10`. The candidate/canonical discrepancy originates in `solution.py`'s
algorithm, not in a false application of S12.

Binary helpers use generated `strict` rather than `seqstrict`, so either
unfinished operand may be evaluated first. All declared and used expression
forms are pure reads or integer operations; there is no state, control, output,
allocation, or exception difference on this program.

The return rule discards a framed suffix. For every submitted-program state and
every integer input, that suffix is only the remaining entry-function body and
there is no caller/top-level continuation after `#invoke`, so this matches
return behavior. The semantics would not by itself justify arbitrary nested
calls or reusable continuation frames. Because no false conclusion witness
exists on the submitted program's intended input domain, I record that as the
declared minimal-semantics scope, not as an unsoundness finding.

Every constructor used by `solution.mpy` is declared and exercised. Missing
translator constructs are unused and are not a defect in generated minimal
semantics.

### Proof extensions

- V01 expands `multiplyBody` to the exact translated statement sequence.
- V02 expands `multiplyProgram` to the exact module/function wrapper.
- V03 is the sole `[function,total]` extension:
  `unitDigit(I) => absInt(I) %Int 10`. It has unconditional coverage, no
  overlap, and terminates in built-in integer operations.

V01 and V02 are definitional closed-term expansions, not operational result
bridges. V03 appears only in the postcondition; it never replaces program
execution. There are no local `[functional]`, simplification, concrete,
priority, fresh-value, opaque result, auxiliary-claim, or oracle rules. No
rule encodes or fabricates the returned product.

I found no local rule that permits a false conclusion about this submitted
program on any integer input. The false benchmark conclusion instead comes
from choosing the candidate's `abs(input) % 10` property rather than the
trusted canonical `abs(input %Python 10)` property. The concrete false
conclusion witness is:

```text
input: (-1, 1)
proved/candidate conclusion: result = 1
trusted canonical conclusion: result = 9
```

This is an intent/implementation failure, not a mislabeled semantic-rule
unsoundness.

Stage 5 result: the local K theory is sound for the actual generated program's
used fragment; it proves the wrong benchmark behavior on part of the intended
domain.

## 6. Fresh non-vacuity test

The candidate supplies no `spec-vacuity.k`; no candidate mutation evidence was
trusted.

I created a fresh scratch module `SPEC-VACUITY` changing only the final result
obligation to:

```k
noResult => (unitDigit(A) *Int unitDigit(B)) +Int 1
```

`A = 0, B = 0` satisfies the original precondition. The submitted program
returns `0`, while the mutation requires `1`.

The mutation's dry run parsed and built the proof request:

```text
COMMAND: kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
EXIT_STATUS: 0
```

The actual mutation proof exited 1, not because of parsing or an unrelated
crash, but with `WarnStuckClaimState` and a residual equality requiring the
real digit product plus one to equal the executed digit product.

Evidence:

- [fresh false spec](evidence/06-spec-vacuity.k)
- [successful dry run](evidence/06-vacuity-dry-run.log)
- [expected failed proof and residual](evidence/06-vacuity-kprove.log)

Stage 6 result: non-vacuity passes.

## 7. Proven-versus-assumed accounting and decision

### What the successful proof establishes

Conditional on the audited K definition and K's built-in theory, for every K
integer pair `A, B`, executing the exact submitted constructor program from the
specified empty entry configuration reaches empty computation with:

- local `a = absInt(A)`, `b = absInt(B)`;
- the exact stored function binding/body;
- result
  `(absInt(A) %Int 10) *Int (absInt(B) %Int 10)`.

The proof is universal over integers, not a finite unrolling or fixed-size
claim. It is body-sensitive and result-sensitive.

### Trust ledger

| Boundary | Influence and classification |
|---|---|
| Trusted `py2mpy.py` | Maps CPython AST to constructors. Byte identity and trusted regeneration pin the submitted `.mpy`; accepted benchmark boundary. |
| Generated `semantic.k` | Handwritten language model, not formally derived from CPython. Exhaustive static review and fresh concrete comparisons support every used construct. Minimal unused-language coverage is acceptable in this mode. |
| K built-ins | Mathematical unbounded integers, maps, Booleans, `absInt`, comparison, addition/subtraction, multiplication, `%Int`, equality, and generated strict contexts. These affect values/control and are part of the K/toolchain trust base. |
| V01/V02 term abbreviations | Manually maintained source-to-claim bridge. Mechanical constructor comparison fixes their exact value; no result abstraction is introduced. |
| V03 `unitDigit` | Truthful total definition of the candidate's summary and used only in the destination. It is not a universal theorem that this summary equals the trusted HumanEval canonical function. |
| K compiler/prover/backend | `kompile`, `kprove`, LLVM/Haskell backends, and matching-logic implementation are trusted for reported build/execution/proof results. |
| Differential/concrete tests | Finite empirical evidence only. They support translation/semantic bridges and, decisively, provide counterexamples to canonical equivalence; they do not replace the K proof. |

There are no opaque symbols, unconstrained result variables, empirical oracles
inside execution, proof-local simplifications, or assumed auxiliary lemmas.
The theorem is partial-correctness in the Kit sense; it does not constitute a
general semantics of all Python constructs or nested calls.

### Decision

The K proof is formally honest about the real submitted program. Nevertheless,
the candidate was required to prove a correct implementation of the trusted
HumanEval task. Its implementation and its postcondition materially disagree
with `/reference/canonical.py` on valid negative integers explicitly within
the source-contract domain. A different algorithm is allowed only when it is
extensionally equivalent; this one is not.

Because the proof establishes the wrong intended result over a material part
of the unrestricted integer domain, it is not a legitimate proof of the
benchmark contract.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
