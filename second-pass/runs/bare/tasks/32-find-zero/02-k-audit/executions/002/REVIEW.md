# Independent adversarial audit: 32-find-zero

The candidate does **not** contain a legitimate partial-correctness proof of
the HumanEval contract. Fresh reconstruction confirms that all five submitted
ground claims close and are non-vacuous, but they prove only five fixed input
examples. The prompt’s domain is every nonempty even-length coefficient list
whose highest coefficient is nonzero. That material domain restriction is
decisive under the benchmark mapping: finite examples are
`FAIL / NOT_LEGIT`, even when the finite theorems themselves are honest.

There is also a concrete language-fidelity counterexample on the intended
domain. The generated K semantics uses exact rationals, while the submitted
Python begins using IEEE-754 floats after `/`. For
`[2^53 + 1, -2^54]`, Python and K take opposite branches at `x = 1/2` and
return different values.

## 1. Input and provenance integrity

Status: **PASS; no audit infrastructure breach.**

- `/audit-input.json` declares `legacy-selected-stage1`,
  condition `bare`, problem `32-find-zero`, and
  `GENERATED_SEMANTICS`. All required files for that layout are present,
  readable real files; `/candidate`, `/generation-evidence`, and the structured
  trace are real directories. The checked mounts are read-only. No candidate
  or generation-evidence entry is a symlink or unsupported node.
- The `audit_campaign` block is exactly equal to
  `/audit-campaign-lock.json`; the lock and audit-prompt SHA-256 values match.
  The observed K tools report 7.1.293, matching the campaign.
- All launcher-recorded direct file hashes checked in
  [stage1-provenance.log](/audit-output/evidence/stage1-provenance.log) match:
  canonical, trusted/candidate prompts, trusted/candidate translators,
  run/task/result manifests, invocation, metrics, usage, generation prompt,
  last message, output log, and the trace JSONL file.
- The independently reimplemented pipeline tree digest of `/candidate` is
  `565eed00...e1c98`, exactly matching both
  `generation-result.outputs.workspace_sha256` and
  `invocation.retained_workspace_sha256`. The trace-tree digest is
  `46612388...7f61`, exactly matching `usage.source_trace_sha256`. The
  audit-input also carries launcher-specific aggregate fields
  (`candidate_tree_sha256` and `generation_codex_trace_sha256`) whose
  construction is not declared in the container; these were not substituted
  for the independently checked per-file and pipeline-tree hashes.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounted versions. As required for generated-semantics mode,
  `/reference/reference-semantics` is absent.
- I read `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, the present `usage.json`,
  `codex-last.txt`, all 24,219 lines of `codex-output.log`, `prompt.txt`, and
  all 288 JSON records in the structured trace. Runtime metrics absent from
  this historical layout were not reconstructed. Generation `SUCCEEDED`,
  `KPROVE_PASSED`, and prior `#Top` records were treated only as claims.

Reproducible evidence:
[provenance script](/audit-output/evidence/provenance_audit.py),
[provenance log](/audit-output/evidence/stage1-provenance.log),
[toolchain log](/audit-output/evidence/stage1-toolchain.log), and
[mount log](/audit-output/evidence/stage1-readonly-mounts.log).

## 2. Program fidelity and candidate-versus-canonical checks

Status: **implementation fidelity supported on ordinary inputs; no material
tested contract divergence.**

The trusted prompt says `find_zero(xs)` accepts coefficients of a polynomial,
with an even number of coefficients and a nonzero highest coefficient (hence
odd degree and a real zero), and returns one zero. The examples are `[1,2]`
and `[-6,11,-6,1]`. The trusted canonical brackets symmetrically, bisects
until width `1e-10`, and returns the left endpoint.

The submitted [solution.py](/candidate/solution.py) computes the polynomial by
successive powers, uses the same bracket/bisection decisions, and returns the
final midpoint rather than the canonical left endpoint. Trusted regeneration
of `solution.mpy` is byte-identical to the submission, SHA-256
`a7f52038...b3fc`; see
[stage2-translator-identity.log](/audit-output/evidence/stage2-translator-identity.log).

The independent differential test exercised:

- 12 fixed cases: both prompt examples, initial zero, both endpoint roots,
  both one-step expansion directions, both multi-step expansion directions,
  a flat cubic, a degree-five case, and a small-leading-coefficient case;
- 180 deterministic generated valid lists of lengths 2, 4, and 6; and
- out-of-domain empty, constant, and zero-highest-coefficient probes with
  timeouts where necessary.

All 192 intended-domain results differ exactly because midpoint is used, but
the maximum result difference is only `2.9103830456733704e-11`; there are zero
material differences under the recorded `1.1e-10` relative comparison. The
worst generated residual in this finite sample is
`2.6613271586484188e-08`. That last fact also shows that the candidate’s
chosen `1e-8` `VerifyRoot` predicate would not hold for every valid input even
if its five claims were generalized.

The empty and invalid-leading-coefficient cases are outside the stated
contract. Their different exception/nontermination behavior was recorded, not
used against the proof.

Reproducible evidence:
[differential script](/audit-output/evidence/differential_test.py) and
[complete log](/audit-output/evidence/stage2-differential.log).

## 3. Clean proof reconstruction

Status: **all submitted positive ground claims reconstruct and close.**

Only source artifacts were copied to `/tmp/audit-work/32-find-zero`; no
candidate kompiled definition, cache, or trace was reused.

Fresh builds:

- LLVM concrete semantics: `kompile semantic.k --backend llvm
  --main-module SEMANTIC --syntax-module SEMANTIC-SYNTAX
  --output-definition semantic-concrete-kompiled` exited 0. It warned that
  all seven `[total]` rational helpers have non-exhaustive matches.
  [Build log](/audit-output/evidence/stage3-kompile-concrete.log).
- Standalone Haskell semantics: the analogous Haskell build to
  `semantic-concrete-haskell-kompiled` exited 0.
  [Build log](/audit-output/evidence/stage3-kompile-concrete-haskell.log).
- Proof definition: `kompile verification.k --backend haskell
  --main-module VERIFICATION --syntax-module VERIFICATION
  --output-definition verification-proof-kompiled` exited 0.
  [Build log](/audit-output/evidence/stage3-kompile-proof.log).

The unmodified aggregate target command exited 0 and printed `#Top`.
I then made a labeling-only copy of the exact five claims and ran each
independently. Every command exited 0 and printed `#Top`:
[aggregate](/audit-output/evidence/stage3-kprove-all.log),
[c1](/audit-output/evidence/stage3-kprove-c1.log),
[c2](/audit-output/evidence/stage3-kprove-c2.log),
[c3](/audit-output/evidence/stage3-kprove-c3.log),
[c4](/audit-output/evidence/stage3-kprove-c4.log), and
[c5](/audit-output/evidence/stage3-kprove-c5.log).

The LLVM interpreter could not execute the semantics: each ordinary case
exited 113 with residual `negRat(rat(1,1))`. The rational equations are marked
only `[simplification]`, so this backend does not provide an executable
operational rule. These failures are preserved in
`stage3-krun-{linear,empty,zero,expansion,endpoint}.log`. This is a candidate
semantics portability limitation, not infrastructure uncertainty.

The standalone Haskell semantics did execute the real regenerated constructor
term. Linear, empty, zero-root, expansion, and endpoint cases all exited 0.
Their exact rational outputs equal `Fraction.from_float` of independent Python
execution in every case. See
[comparison script](/audit-output/evidence/compare_concrete.py),
[comparison log](/audit-output/evidence/stage3-concrete-comparison.log), and
the five `stage3-krun-haskell-*.log` files.

## 4. Adequacy and real-program pinning

Status: **program pinning and result constraint pass for the five ground
claims; source-contract adequacy fails.**

Each claim has no `requires` clause. Its precondition is the exact, realizable
ground configuration with empty environment/function/stack cells and this
computation:

`solution ;; VerifyRoot(COEFFICIENTS,
Invoke("find_zero", list(COEFFICIENTS)), 1/100000000)`.

Its postcondition is completion with `<k> bool(true) </k>` and the three
state cells empty. Thus each literal initial configuration is a satisfying
state; there is no inconsistent or symbolic precondition.

The five coefficient/postcondition pairs are:

| Claim | Fixed coefficients | Proven ground postcondition |
|---|---|---|
| c1 | `[1,2]` | returned root has exact-rational residual `<= 1e-8` |
| c2 | `[-6,11,-6,1]` | same |
| c3 | `[0,1]` | same |
| c4 | `[-8,0,0,1]` | same |
| c5 | `[8,0,0,1]` | same |

`VerifyRoot` is strict in the invocation argument. It therefore consumes the
actual returned value and independently evaluates the polynomial; the result
is neither free nor tautological. The Python candidate and trusted canonical
values/residuals for every entry input appear in the differential log.

Trusted regeneration plus a mechanical 435-token constructor comparison shows
that `verification.k`’s `solution` macro is exactly `solution.mpy`, not a
substituted body. See
[pinning script](/audit-output/evidence/check_program_pinning.py) and
[pinning log](/audit-output/evidence/stage4-program-pinning.log). There are no
helper/loop claims: each ground proof executes both real while loops
concretely.

A separate body-sensitivity mutation changed the program term actually
executed by the claim so `find_zero` returned `42`. The mutated definition
built successfully; its proof exited 1 with `WarnStuckClaimState` and final
`bool(false)` instead of required `bool(true)`. See
[mutated definition](/audit-output/evidence/verification-body-mut.k),
[mutated spec](/audit-output/evidence/spec-body-mut.k),
[mutation build](/audit-output/evidence/stage4-body-mutation-kompile.log) and
[mutation proof](/audit-output/evidence/stage4-body-mutation-kprove.log).

`prove.sh` regenerates `solution.mpy`, but the proof macro is separately
hard-coded rather than mechanically regenerated. For this immutable candidate
the constructor comparison passes, so this is maintenance risk, not the
decisive failure.

The decisive adequacy defect is that none of these claims quantifies over an
input list. Five fixed examples cannot establish partial correctness for every
even-length list with a nonzero highest coefficient.

## 5. Rule-by-rule static soundness review

Status: **complete inventory; actual ground paths are operationally covered,
but the generated semantics is not faithful to Python on the full intended
domain.**

The exhaustive inventory is
[static-inventory.md](/audit-output/evidence/static-inventory.md), backed by
[declaration extraction](/audit-output/evidence/stage5-declarations.log). It
individually enumerates and decides:

- every syntax/configuration/runtime declaration;
- all 46 rules S01–S46 in `semantic.k`;
- all seven rules V01–V07 in `verification.k`;
- all `[function]`, `[total]`, `[simplification]`, `[strict]`, macro, and
  context attributes; and
- all five claims in `spec.k`.

There are no local priority rules, operational shortcuts, result oracles,
opaque proof symbols, or auxiliary circularities. All source constructors
actually used by `solution.mpy` map to a declaration and operational rule:
module/function definitions, parameters, assignment, names/integers, unary
minus, four binary operators, for/while/if, comparison, one/two-argument
calls, and return. Environment updates, call frames, full caller continuation,
return unwinding, loop order, and left-to-right expression/argument evaluation
are correct for the submitted bodies.

Three limitations remain:

1. `gcdInt`, `makeRat`, `addRat`, `subRat`, `mulRat`, `divRat`, and `negRat`
   are all declared `[total]` over broader sorts than their equations cover.
   Ground `addRat(bool(true),rat(1,1))` and `makeRat(1,0)` remain residual
   despite the total declarations. This is an over-broad trust/portability
   defect; neither term is reached by the five claims.
2. Syntax admits arbitrary `rat(N,D)` while comparison, `absRat`, and `leRat`
   silently require positive denominators. Ground probes demonstrate the
   discrepancy: `rat(1,-1) > rat(0,1)` becomes true, its `absRat` remains
   `rat(1,-1)`, and `leRat(rat(1,-1),rat(0,1))` becomes false. These terms lie
   outside the informal normalized-rational representation invariant and are
   not used as an intended-input verdict witness. Logs are
   `stage5-probe-*.log`.
3. The material intended-domain mismatch is exact rational versus Python
   float arithmetic. For valid input
   `[9007199254740993,-18014398509481984]`, Python computes
   `p(0.5) = 0.0`; exact arithmetic computes `p(1/2) = 1`. Python therefore
   takes the nonpositive branch, whereas rules S20–S26 take the positive
   branch. K returns `17179869185/34359738368`; the real generated Python
   returns `17179869183/34359738368`. This is the required concrete false
   observable conclusion witness on the stated input domain:
   [K run](/audit-output/evidence/stage5-rounding-witness-krun.log) and
   [independent witness](/audit-output/evidence/stage5-rounding-witness-python.log).

The third item means the generated language definition cannot support a
universal theorem about the real Python program without an explicit restricted
numeric model or a proved source-to-exact-rational bridge. The five small
ground paths happen to agree with Python, as Stage 3 records.

## 6. Fresh non-vacuity test

Status: **PASS for the submitted ground theorem shape.**

I created a new spec module that keeps the real `[1,2]` program execution and
changes only its result-constraining destination from `bool(true)` to the
demonstrably false `bool(false)`:
[mutation source](/audit-output/evidence/spec-vacuity-auditor.k).

- `kprove ... --dry-run` exited 0, showing that the mutation parses and builds:
  [dry-run log](/audit-output/evidence/stage6-vacuity-dry-run.log).
- The actual mutated proof exited 1 with `WarnStuckClaimState`. The residual
  configuration is cleanly terminated at `bool(true)`, which cannot unify
  with the false destination:
  [proof log](/audit-output/evidence/stage6-vacuity-kprove.log).

This is an expected unmet result obligation, not a parser error, timeout,
unreachable mutation, or unrelated crash.

## 7. Proven versus assumed accounting

### What is formally proven

Conditional on the supplied K definition and K backend, the real constructor
body terminates on each of the five fixed coefficient lists and its returned
exact rational makes the independently defined exact-rational polynomial
residual at most `1e-8`. Nothing in the K artifacts proves the property for a
sixth list, for a symbolic list, or for the prompt’s unrestricted valid-list
domain.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K compiler/prover and built-in `INT`, `BOOL`, `STRING`, `MAP`, `LIST` theories | all builds and claims | Ordinary low-level trusted primitive. |
| Trusted `py2mpy.py` translation | source-to-constructor identity | Byte identity and macro-token identity are checked; translator correctness itself remains trusted. |
| Generated operational semantics S01–S46 | all executions | Audited rule by rule. Adequate on the five normalized-rational paths; not a faithful universal Python-float model. |
| Positive-denominator `rat` invariant | comparisons and verification helpers | Informal and unenforced at syntax boundaries; true on all submitted claim paths. |
| `polyValue`, `absRat`, `leRat`, `VerifyRoot` | final ground postconditions | Truthful on normalized rationals; they check execution results and do not bypass the program. |
| Haskell backend behavior of `[simplification]` equations | concrete and proof execution | Works in fresh runs; LLVM execution fails on the same helpers, a documented portability limitation. |
| Differential tests | candidate/canonical and small-input semantic bridge | Finite empirical support only: 192 intended cases plus boundaries. It is not a universal proof. |
| Python-float versus exact-rational equivalence | any theorem about the real unrestricted Python program | False; the Stage 5 intended-domain witness refutes it. |

### Gate accounting and decision

- Fresh dynamic reconstruction: **PASS** for all five submitted claims.
- Ground program identity, result constraint, body sensitivity, and
  non-vacuity: **PASS**.
- Exhaustive theory review: **FAIL** as a universal Python semantics because
  of the intended-domain float counterexample; limited ground paths remain
  sound.
- Human-facing contract adequacy: **FAIL** because the proof contains only
  five fixed inputs and materially narrows the source domain.
- Evidence auditability: **PASS with documented trust boundaries**.

In generic Kit terminology, the five ground theorems are sound-but-limited.
The benchmark prompt expressly maps a material HumanEval domain narrowing of
that kind to `FAIL / NOT_LEGIT`, not `CONCERNS`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
