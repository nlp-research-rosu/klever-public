# Independent adversarial audit: 21-rescale-to-unit

Audit date: 2026-07-24  
Rendered mode: `SUPPLIED_SEMANTICS`

The trusted mounts are consistent with the rendered mode, so this is a
candidate verdict rather than an infrastructure error. The reconstructed
`kprove` run does print `#Top`, but the proof is not legitimate: its result is
defined using unconstrained extrema oracles that are inserted into execution by
priority rewrites, and its comprehension bridge changes fixed-semantics state.
The formal domain also includes equal-extrema inputs on which both real Python
implementations raise while the K claim proves a normal list return.

## 1. Input and provenance integrity

### Trusted-mode boundary

- `/reference/reference-semantics` is present and is a real directory, as
  required in supplied-semantics mode. The other trusted inputs are regular
  files. See [03-trusted-input-types.log](evidence/03-trusted-input-types.log).
- A no-symlink, type-aware, SHA-256 recursive comparison found all 26 entries of
  `/candidate/reference-semantics` identical to the trusted tree, with no
  missing, additional, changed, mistyped, or symlinked entry. See the reviewer
  script [tree_integrity.py](evidence/tree_integrity.py) and
  [05-semantics-integrity.log](evidence/05-semantics-integrity.log).
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  versions. See [04-prompt-translator-integrity.log](evidence/04-prompt-translator-integrity.log).
- The supplied-semantics tree is therefore accepted as the fixed selected
  semantics. Its comments do not justify any rule added in `verification.k`.

### Candidate artifact inventory

`solution.py`, `solution.mpy`, `spec.k`, `verification.k`, `prove.sh`, the smoke
files, the prompt, translator, and supplied-semantics copy are regular files.
There are no candidate symlinks. There is an extraneous `__pycache__` directory,
which was neither trusted nor copied into the audit build.

The requested provenance artifacts are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`
- any structured generation trace discoverable by `*trace*` or `*.jsonl`

These absences are a provenance/auditability failure, not an infrastructure
contradiction. The complete bounded inventory is
[02-provenance-inventory.log](evidence/02-provenance-inventory.log). Candidate
prose and scripts were treated only as untrusted claims; the audited sources
are reproduced in [07-candidate-proof-sources.log](evidence/07-candidate-proof-sources.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and actual Python behavior

The prompt asks for a linear rescaling of a list containing at least two
numbers, with the smallest result equal to `0` and the largest equal to `1`.
The trusted canonical implementation computes

`(x - min(numbers)) / (max(numbers) - min(numbers))`

for each element. It does not state or enforce a distinct-extrema precondition.
Consequently, an equal-valued list of length two is within the literal stated
domain but raises `ZeroDivisionError`; the requested endpoint property is
itself impossible for such a list.

The submitted `solution.py` uses the same algorithm and order of operations,
with only variable/layout differences. It does not mutate the input.

### Translation identity

The trusted translator regenerated `solution.mpy` with SHA-256
`bdb65c4c8c0e79045c2cfb52c9643f3803e3e3f6ff93ee83716c423f19b0da88`.
The regenerated and submitted files are byte-identical:

```text
python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy
TRANSLATOR_EXIT=0
BYTE_CMP_EXIT=0
```

See [09-translation-identity.log](evidence/09-translation-identity.log).

### Independent differential test

The reviewer-authored [differential_test.py](evidence/differential_test.py)
imports the trusted canonical and scratch-copied generated entry points
independently. It compares float results by hexadecimal representation,
exception type/message, and input mutation. Its inputs include the documented
example; empty and singleton out-of-domain boundaries; equal extrema; ascending
and descending pairs; interior/duplicate extrema; signed zero; subnormal,
large, infinite, and NaN values; and 500 deterministic generated finite lists.
The full inputs are preserved in
[differential-inputs.json](evidence/differential-inputs.json).

```text
seed=210021 explicit_cases=17 generated_cases=500 total_cases=517
canonical_return_cases=513 canonical_raise_cases=4
mismatch_count=0
```

The command exited 0; see [10-python-differential.log](evidence/10-python-differential.log).
This establishes strong finite implementation fidelity, not a K theorem.

Stage result: the generated Python program and submitted constructor term are
faithful to the canonical algorithm. The equal-extrema behavior remains a
material contract/domain edge.

## 3. Clean proof reconstruction

Only source artifacts were copied to
`/tmp/audit-work/21-rescale-to-unit`; no candidate kompiled definition, cache,
or `__pycache__` was reused. The scratch-copy inventory is
[08-scratch-copy.log](evidence/08-scratch-copy.log).

The installed live toolchain is K `v7.1.337`; see
[01-toolchain.log](evidence/01-toolchain.log).

### Concrete definition

The following fresh LLVM build exited 0:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

See [11-kompile-runtime.log](evidence/11-kompile-runtime.log). The fresh smoke
run also exited 0 and terminated with `.K`, `NoExc`, and exit code 0:

```text
krun smoke.mpy --definition audit-runtime-kompiled
```

See [12-krun-smoke.log](evidence/12-krun-smoke.log).

### Proof definition and every positive claim

The fresh Haskell proof build exited 0:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition audit-verification-kompiled
```

See [13-kompile-verification.log](evidence/13-kompile-verification.log).
There is exactly one target claim, in `spec.k`; `verification.k` contains no
helper or loop claims. See [14-positive-claims-inventory.log](evidence/14-positive-claims-inventory.log).

The only positive claim independently closed:

```text
COMMAND: kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
EXIT_STATUS: 0
OUTPUT_BEGIN
#Top
```

See [15-kprove-spec.log](evidence/15-kprove-spec.log).

Stage result: fresh dynamic reconstruction succeeds under the candidate-extended
theory. This is verification closure, not validation of that theory.

## 4. Adequacy and real-program pinning

### Formal entry claim in plain language

Precondition:

- The initial configuration has module scope 0, the supplied builtin scope at
  -1, empty heap/stack, environment 0, no return, no exception, and exit code 0.
- The argument is a `ValSeq` containing at least two K `Float` values.
- `allFloats(REST)` requires every remaining element to be a float.
- There is no requirement that values be finite, ordered, non-NaN, or have
  distinct extrema.

Postcondition:

- Normal execution leaves the `<k>` cell equal to an unboxed list whose
  sequence is `scaleAcc` over the input.
- Scaling uses supplied `subF`/`divF`, but the low and high values are
  `minVF(input)` and `maxVF(input)`.
- Final scope, heap, and heap-location values are existential and unconstrained.
  Environment, stack, return state, exception state, and exit code must be
  restored to their normal values.

### Program identity

The `#runRescale` harness contains an embedded `Module(...)` rather than reading
`solution.mpy` at proof time. A reviewer script extracted that module, parsed
both it and submitted `solution.mpy` to KORE, and obtained identical SHA-256
`90fa8d2ef6f00ea1c5a535ab4d86b0728eb21254ff1514e56457b87e40aaacc3`.
See [extract_embedded_program.py](evidence/extract_embedded_program.py) and
[18-embedded-program-equivalence.log](evidence/18-embedded-program-equivalence.log).
Thus the body is syntactically pinned, not substituted.

The harness invokes the function with an unboxed `list(VS)` value. Ordinary
program syntax creates a heap reference for a `ListExpr`. In the ordinary-call
witness, the candidate comprehension bridge does not match that referenced
binding, while its extrema bridges still do; compare
[22-fixed-bridge-witness.log](evidence/22-fixed-bridge-witness.log) and
[23-extended-bridge-witness.log](evidence/23-extended-bridge-witness.log).
The supplied core semantics permits unboxed read-only list inputs, so this is
an informal input-representation bridge, not a syntactic body substitution.

### Satisfying witnesses and result comparison

`[1.0, 2.0]` satisfies every entry precondition. The specialized candidate
postcondition closes with `#Top`; see
[19-kprove-ground-claimed.log](evidence/19-kprove-ground-claimed.log).
Both Python implementations return `[0.0, 1.0]`. Replacing the opaque
postcondition with that genuine result does not close: the residual explicitly
requires the unproved equalities between `0.0`/`1.0` and expressions containing
`minVF`/`maxVF`. See
[20-kprove-ground-expected.log](evidence/20-kprove-ground-expected.log).

This is not merely a backend inability to print a concrete float. The candidate
theory contains no equation connecting its extrema symbols to fixed execution.
The compatible reviewer extension in
[opposite-theory.k](evidence/opposite-theory.k) assigns those symbols arbitrary
opaque float results for `[1.0,2.0]`; the correspondingly altered result claim
still closes with `#Top`. See
[33-kompile-opposite-theory.log](evidence/33-kompile-opposite-theory.log) and
[34-kprove-opposite-theory.log](evidence/34-kprove-opposite-theory.log). A model
may interpret those opaque float results as reversed extrema. The base theory
does not exclude that false interpretation.

`[2.0, 2.0]` is a second, decisive satisfying witness. The K claim specialized
to this input closes normally with `#Top`; see
[38-kprove-equal-boundary.log](evidence/38-kprove-equal-boundary.log). Both real
Python entries instead raise `ZeroDivisionError`, as recorded in
[37-python-equal-boundary.log](evidence/37-python-equal-boundary.log). The fixed
supplied LLVM semantics returns `[NaN, NaN]` with `NoExc`, showing the precise
Python-to-K language-model gap; see
[40-krun-fixed-equal.log](evidence/40-krun-fixed-equal.log).

There are no helper/loop reachability claims to connect `scaleAcc` or the
comprehension summary to real control flow.

Stage result: **FAIL**. The embedded body is exact, but the postcondition does
not constrain the returned value to the intended extrema and proves a normal
return for a real-program exception case.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-authored [k_rule_inventory.py](evidence/k_rule_inventory.py)
enumerates every source `configuration`, `context`, `syntax`, `rule`, and
`claim` declaration in the supplied root/helpers, `verification.k`, and
`spec.k`, including multiline source, attributes, and a per-entry decision.
The full 951-row inventory is
[rule-inventory.tsv](evidence/rule-inventory.tsv); counts and per-file totals
are in [rule-inventory-summary.txt](evidence/rule-inventory-summary.txt).

```text
files=26
records=951
claim:1 configuration:1 context:5 rule:708 syntax:236
concrete:35 function:152 macro:4 no-evaluators:23 ordinary:673
owise:26 priority:48 symbol:27 total:113
```

No `[functional]` declaration or `[simplification]` rule occurs. The 928
supplied-semantics entries are marked `SUPPLIED_BASELINE_FIXED`: they are
byte-identical to the authoritative selected semantics and are not candidate
proof extensions. The root `semantics.k` is an import/assembly module with no
local declaration. The used-construct subset, configuration, evaluation order,
calls/returns, state, and allocation paths are mapped in
[construct-map.md](evidence/construct-map.md).

### Used semantics and control flow

The fixed semantics evaluates assignment right-hand sides first; resolves
`min`/`max` through the builtin scope; evaluates callees and arguments
left-to-right; allocates an annotated function frame and closure cells; expands
the comprehension to an accumulator closure/loop; evaluates binary operands
left-to-right; allocates each list construction; records the return; and
restores the caller frame. The exact declarations/rules are cited in the
construct map.

The candidate min/max rules overlap the fixed builtin-dispatch rules on exactly
one list argument and priority 40 makes them preempt fixed execution. The min
and max guards are mutually disjoint by builtin name. The comprehension rule
matches the exact submitted expression plus a scope/heap shape, but admits any
following continuation and does not require `allFloats(VS)`.

### Complete candidate-local inventory and decisions

| `verification.k` entries | Classification and decision |
|---|---|
| `minVF`, `maxVF` declaration (line 9) | Result-bearing, total, opaque functions. Illegitimate as extrema: no equation or bridge-free connection theorem constrains their values. |
| Priority min/max rewrites (lines 12, 15) | **Unsound operational result bridges.** They replace fixed folds with the unconstrained symbols and preempt the fixed dispatch. |
| `asFloat` declaration/equation (21-22) | Equation `asFloat(F)=F` is sound on floats. Totality over all `Val` leaves arbitrary non-float cases; that is an over-broad evidence gap, not a false equation on the entry domain. |
| `scaleF` declaration/equation (24-26) | Sound definitional abbreviation for the supplied `subF`/`divF` terms. |
| `scaleAcc` declaration/base/step (28-35) | Sound, guard-disjoint structural recursion decreasing on `REST`; it preserves order and length. |
| `allFloats` declaration/base/step (37-40) | Sound, exhaustive structural predicate. |
| `FloatSeq`, `injectFloats` declarations/base/step (44-48) | Sound, exhaustive structural injection; unused by the target claim. |
| Exact comprehension rewrite (54-81) | **Unsound operational bridge.** No bridge-free universal connection theorem exists; it skips fixed allocations and accepts a broader continuation/state context. |
| `#observe` declaration/rule (85-87) | Sound local observation helper: it reads the value stored at an existing reference without changing heap state. |
| `#runRescale` declaration/rule (91-119) | Syntactically exact execution harness. It preserves its suffix, but its unboxed-list input convention requires an informal representation bridge. |

The single `spec.k` claim is separately inventoried as
`ILLEGIT_CIRCULAR_POSTCONDITION` because the same unconstrained extrema symbols
appear in the execution bridges and final result.

### Required false-conclusion witnesses

1. **Min bridge, `verification.k:12-14`.** On the satisfying intended input
   `[1.0,2.0]`, fixed semantics and both Python implementations select `1.0`.
   The bridge returns `minVF([1.0,2.0])`, for which the theory admits an
   interpretation of `2.0`. The genuine `[0.0,1.0]` obligation remains stuck,
   while the compatible arbitrary-oracle theory closes. Evidence:
   [20-kprove-ground-expected.log](evidence/20-kprove-ground-expected.log) and
   [34-kprove-opposite-theory.log](evidence/34-kprove-opposite-theory.log).

2. **Max bridge, `verification.k:15-17`.** On the same input, fixed semantics
   and Python select `2.0`; the unconstrained `maxVF` may be interpreted as
   `1.0`. Together with the preceding witness, the claimed scaling can denote
   reversed `[1.0,0.0]` rather than `[0.0,1.0]`. Nothing in the candidate theory
   rejects this opposite interpretation.

3. **Comprehension bridge, `verification.k:54-81`.** For the exact direct-list
   `[1.0,2.0]` invocation, bridge-free supplied LLVM execution returns the
   correct list after seven heap allocations and ends at `<heapLoc> 7`; see
   [fixed-harness-llvm.k](evidence/fixed-harness-llvm.k) and
   [28-krun-fixed-direct-list-harness.log](evidence/28-krun-fixed-direct-list-harness.log).
   The bridge-enabled claim closes with `<heapLoc> 3`; see
   [spec-extended-heap.k](evidence/spec-extended-heap.k) and
   [26-kprove-extended-heap.log](evidence/26-kprove-extended-heap.log).
   Thus the rule enables the false selected-semantics conclusion that the same
   region preserves the fixed allocation transition. The target claim hides
   this mismatch by existentially framing final heap state.

There is no rule overlap or recursion defect in `scaleF`, `scaleAcc`,
`allFloats`, or `injectFloats`. Their soundness cannot repair the two missing
operational connection theorems. A diagnostic bridge-free Haskell proof attempt
encountered the backend's unsupported `FLOAT.min` hook
([25-kprove-fixed-heap.log](evidence/25-kprove-fixed-heap.log)); this explains
why the shortcut may have been tempting, but it does not justify it. Concrete
LLVM fixed execution supplies the ground witness and the candidate had no
universal proof.

Stage result: **FAIL**. Three proof-local operational rules fail the selected
semantics contract with explicit value/state witnesses.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` exists. The fresh reviewer mutation
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k) prepends an impossible
extra `0.0` to the result while leaving the entry execution and precondition
unchanged. `[1.0,2.0]` is a satisfying witness: the program/candidate summary
has length two, whereas the mutated postcondition demands length three.

The mutation built successfully:

```text
kprove spec-vacuity-audit.k --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run
EXIT_STATUS: 0
```

See [35-vacuity-dry-run.log](evidence/35-vacuity-dry-run.log).

The actual proof failed for the intended obligation:

```text
kprove spec-vacuity-audit.k --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT
EXIT_STATUS: 1
WarnStuckClaimState
```

The residual is the impossible equality between the produced sequence and
`vCons(0.0, produced-sequence)`, not a parser/import/crash failure. See
[36-vacuity-proof.log](evidence/36-vacuity-proof.log).

Stage result: **PASS for structural non-vacuity**. The claim constrains list
shape, but this does not constrain the opaque extrema to their real values or
make the operational bridges sound.

## 7. Proven versus assumed accounting

### What the successful reachability proof actually establishes

Under the candidate-extended K theory, for a synthetic unboxed list containing
at least two floats and an all-float tail, the exact embedded function body
reaches a normal result of the following form:

`scaleAcc([], input, minVF(input), maxVF(input))`

using supplied opaque `subF`/`divF` operations, with final heap/scope state
existentially ignored. Module loading, function creation/call, the two
assignments, return, frame restoration, observation, list order, and list
length are exercised. The proof does **not** establish that `minVF` is the
minimum, that `maxVF` is the maximum, that the endpoints become 0 and 1, that
the result equals either Python implementation, or that equal-extrema calls
raise.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Trusted prompt, canonical, and translator | Intent, Python oracle, constructor identity | Acceptable trusted inputs; candidate copies match where required. |
| Byte-identical supplied K semantics | All execution/proof rules below `verification.k` | Accepted as the selected semantics level, not as a complete proof of CPython fidelity. |
| Supplied `subF`/`divF` no-evaluator symbols with LLVM concrete equations | `scaleF`, every result element | Acceptable low-level conditional primitive within supplied semantics; normal concrete smoke supports ground behavior only. |
| Supplied float min/max folds | Real fixed min/max execution | Concrete LLVM behavior is available. Haskell lacks the relevant float hook; this is a proof-tool boundary, not authority for an oracle. |
| Candidate `minVF`/`maxVF` | Both assignments, every scaled element, final postcondition | **Illegitimate.** Program-derived, result-bearing, unconstrained, and used circularly in bridge plus postcondition; no universal connection theorem. |
| Candidate comprehension bridge | Returned list and heap allocation state | **Illegitimate.** Program-defined computation is skipped without a connection theorem, and a concrete state-transition witness disagrees. |
| `asFloat` totalization outside floats | Potential non-float bridge uses | Concerning over-breadth, but the entry precondition is all-float and no false intended-domain equation was found. |
| `#observe` | Converts returned heap reference to list value | Acceptable reviewer-visible observation helper; exact heap lookup rule. |
| Unboxed `list(VS)` invocation convention | Entry-argument representation and comprehension bridge applicability | Informal/concerning. It is allowed by supplied syntax and read-only here, but no equivalence theorem connects ordinary heap-referenced calls. |
| Python-to-K float/exception bridge | Claim about the real generated program | **Illegitimate over the stated formal domain.** Equal extrema raise in Python but return NaNs in fixed K and a normal opaque list in the proof. |
| 517-case Python differential run | Candidate-versus-canonical fidelity only | Strong finite evidence, not a universal proof and not evidence for `minVF`, `maxVF`, or the comprehension bridge. |
| Fresh false mutation | Structural result sensitivity | Valid non-vacuity evidence only; it does not validate semantic meaning. |
| Missing generation provenance/logs | Reproducibility of the candidate's construction history | Auditability concern; no candidate trace was trusted. |

### Decision

The candidate reconstructs to `#Top` and is non-vacuous in list shape, but the
successful proof is circular at its decisive values and relies on an
allocation-changing operational shortcut. It also proves normal behavior for
an explicit satisfying input on which the real generated program raises.
Those are material Gate A and real-program adequacy failures, not limitations
that can be downgraded to concerns.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
